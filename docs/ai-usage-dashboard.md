---
date: "2026-07-08"
category: "Coding Agent 工具"
card_icon: "material-heart-pulse"
oneliner: "本機執行的 AI 用量儀表板，以電玩血條顯示 Claude/Codex/MiniMax/Antigravity/Kiro 使用率，零執行期依賴"
tags:
  - claude-code
  - reverse-engineering
  - self-hosted
  - desktop-app
---

# AI 使用量儀表板（danleetw/ai_usage_dashboard）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/danleetw/ai_usage_dashboard> |
| README（繁中） | <https://github.com/danleetw/ai_usage_dashboard/blob/main/README.md> |
| server.js（核心後端） | <https://github.com/danleetw/ai_usage_dashboard/blob/main/server.js> |
| 逆向來源：steipete/CodexBar | <https://github.com/steipete/CodexBar> |
| 同類專案：tddworks/ClaudeBar | <https://github.com/tddworks/ClaudeBar> |
| 分析型同類：getagentseal/codeburn | <https://github.com/getagentseal/codeburn> |

> Repo 狀態（截至 2026-07-08）：建立於 2026-07-03、53 stars、12 forks、語言 HTML、無授權標示（License 欄位為空）。是一個剛滿一週就有熱度的台灣開發者專案。

## 專案概述

這是一個**在本機執行的 AI 用量儀表板**：一橫列一個 AI 供應商，用「電玩血條」的視覺呈現目前使用率、下次重生（reset）倒數、Context 使用率、每週/每月使用率。目前支援 **Claude / Codex / MiniMax / Antigravity / Kiro** 五家自動同步。

它解決的痛點很具體——AI coding 工具的額度分散在各家、各自有 5 小時窗 / 每週 / 每月的不同重置週期，使用者很難一眼看出「我還剩多少、什麼時候回血」。這個專案把它們併成一面血條牆。

最大的設計特色是**零執行期依賴**：前端是單一 `index.html`，伺服器 `server.js` 只用 Node.js 內建模組（`http`/`https`/`fs`/`crypto`/`child_process`…），**不需要 `npm install`** 就能跑（`npm install` 只在跑 Playwright E2E 測試時才需要）。伺服器只綁定 `127.0.0.1:3789`，不對外開放。介面支援繁中/English 切換，預設依瀏覽器語言判斷。跨平台三支啟動腳本：Windows `start.bat`、macOS `start.command`、Linux `start.sh`，啟動後自動開瀏覽器。

## 核心技術：五家供應商的用量怎麼抓出來

整個專案的精華在 `server.js` 如何取得各家的用量——**越封閉的供應商，接法越 hacky**，剛好構成一條「開放度光譜」：

| 供應商 | 接法 | 端點 / 機制 | 脆弱度 |
|--------|------|-------------|--------|
| **Claude** | 讀 `~/.claude/.credentials.json` 的 OAuth token | `GET https://api.anthropic.com/api/oauth/usage`（即 `claude /usage` 背後的官方 API） | 低（官方端點） |
| **Codex** | 讀 `~/.codex/auth.json` | `GET https://chatgpt.com/backend-api/codex/usage`，帶 `originator: codex_cli_rs`、`User-Agent: codex_cli_rs` 標頭 | 中（半官方 backend API） |
| **MiniMax** | 用 API Key（加密存 `config.json`） | `GET https://www.minimax.io/v1/token_plan/remains` | 中（需自備 key） |
| **Antigravity**（Google `agy` CLI） | 無公開 API；`agy` 執行期間會在 `127.0.0.1` 開一個自帶 quota 資料的 Connect-RPC 本機服務 | `POST https://127.0.0.1:<port>/exa.language_server_pb.LanguageServerService/RetrieveUserQuotaSummary`（自簽憑證、免 CSRF token） | 高（僅 `agy` 行程存活時才在） |
| **Kiro** | 無公開 API；呼叫 `kiro-cli chat --no-interactive "/usage"` 解析 TUI 輸出 | 用 `execFile` 直接傳陣列參數（不經 shell），ANSI 要 strip，且報表印在 **stderr** 而非 stdout | 高（CLI 版本一改就壞） |

幾個值得記下的實作細節：

- **Antigravity 的探測心路歷程**（作者寫在註解裡）：`agy.exe` 本體是加殼封閉二進位、雲端 usage 端點也走不通——兩條路都撞牆；最後在 CodexBar 的 `docs/antigravity.md` 找到「CLI 執行時會開本機 loopback Connect-RPC」這條路。限制是此服務只在 `agy` 行程活著時才開，關掉終端機就沒了，所以偵測不到時只提示使用者「請先在終端機跑 `agy` 保持連線」，**不會**主動幫使用者背景啟動一個 `agy`（避免意外 side effect）。
- **Kiro 的取巧**：原本想走 `kiro-cli serve`（本機 ACP WebSocket、JSON-RPC over `ws://127.0.0.1:8082`），但 `account/getUsage` 需要 client 端反向實作 auth callback，太麻煩；改抄 CodexBar 的 `docs/kiro.md`——直接呼叫 `/usage` 這個唯讀 metadata 查詢。用 `execFile` 傳陣列（不經 shell）避免注入。
- **正規化**：Codex/MiniMax 的重置時間格式各異（unix 秒 / 毫秒 / ISO 字串 / `reset_after_seconds`），程式碼有一整套 `normalize*Window` 把它們統一成 `{ usedPct, resetsAt, windowMinutes }`。

### HTTP 端點

```
GET  /api/usage        → { time, providers: { claude, codex, minimax, kiro, antigravity } }
POST /api/minimax/key  → 設定 / 清除 MiniMax API Key
GET  /  或  /index.html → 送出單檔前端
```

## 機密資料：硬體綁定的加密設計

MiniMax API Key 等機密只在本機使用，以 **AES-256-GCM** 加密後存於 `config.json`，加密金鑰由**本機硬體識別碼**衍生：

| OS | 硬體 ID 來源 |
|----|-------------|
| Windows | BIOS 序號 + MachineGuid |
| macOS | `IOPlatformUUID` |
| Linux | `/etc/machine-id` |

這代表 `config.json` **綁定單一機器**，複製到別台電腦無法解密——不需要、也不應該把它上傳或分享。這是「把不可攜性當成安全特性」的設計，比明文 `.env` 安全得多。

## 桌面浮動小工具（僅 Windows，選用）

除了瀏覽器分頁，另可開一個無邊框、逐像素透明、釘在螢幕右上角的浮動小視窗（WPF + WebView2），只顯示供應商卡片、血條與捲軸半透明，做成「隨時瞄一眼」的 HUD：

- `floating-widget.bat`（卡片版）/ `floating-widget-mini.bat`（迷你橫式，約 20px 高、螢幕 1/5 寬，一次一家，↑/↓ 切換）；偵測到伺服器沒跑會自動背景啟動。
- 拖曳卡片任意空白處搬移，拖邊緣/角落調整大小，關閉用 **Alt+F4**（無關閉按鈕）。
- 首次使用需手動從 nuget.org 下載 3 個 WebView2 SDK DLL（約 9MB，不隨版控發佈）。

## 目前限制 / 注意事項

- **Antigravity 需 `agy` CLI 保持在終端機執行**；**Kiro 需安裝 `kiro-cli` 並登入**——這兩家不開就抓不到。
- Kiro 靠**解析 CLI TUI 輸出**，kiro-cli 版本一改格式就可能壞；Codex / Antigravity 走**未公開端點**，隨時可能失效。
- 浮動小工具**僅 Windows**，且要手動下載 WebView2 DLL；macOS 首次執行會被 Gatekeeper 擋（需右鍵開啟一次或 `xattr -d com.apple.quarantine`）。
- 這是**即時快照**式的「現在還剩多少」，**沒有歷史趨勢 / 成本拆解**（要那種分析請看 codeburn、tokscale）。
- Repo **無授權條款（no License）**，商用/二次散布前需向作者確認。

## 研究價值與啟示

### 關鍵洞察

1. **「零執行期依賴」是一種被低估的架構決策。** 單一 `index.html` + 只用 Node 內建模組的 server，換來的不只是「省一步 `npm install`」——它同時消滅了整條 npm 供應鏈風險（沒有 dependency confusion、沒有 post-install script、沒有 transitive CVE）。對一個「要讀你本機憑證」的工具來說，這種極簡本身就是最強的信任訊號。這是 ponytail 式的「能不寫就不寫」做對的範例。

2. **供應商整合的 hacky 程度，反映的是各家 usage 透明度的落差。** 從 Claude 的官方 OAuth 端點 → Codex 的半官方 backend API → MiniMax 的自備 key → Antigravity 的本機 RPC 探測 → Kiro 的 CLI 輸出爬取，是一條清楚的「開放度衰減曲線」。越不想讓你看到額度的供應商，社群就用越脆弱的方式硬把它挖出來——而脆弱度也正好倒過來排。

3. **逆向工程知識正在變成社群共享資產。** Antigravity 與 Kiro 的接法都**直接引用 CodexBar 的 `docs/`**。真正的護城河不是那幾百行程式碼，而是「知道哪個未公開端點會回 quota」這件事——CodexBar 的 docs 事實上成了一本可被下游專案 cite 的「逆向工程食譜」。

4. **硬體綁定加密把「不可攜」當成安全特性。** 金鑰從 machine-id 衍生，讓 `config.json` 天生不能搬家。這比「加密但金鑰也放在同一台」高明，也比明文 `.env` 安全，代價只是換機要重設 key——對本機單機工具是划算的取捨。

5. **血條 / 遊戲化 UI 是「ambient information」模式。** 把用量做成半透明浮動 HUD 釘在角落，把「我是不是快撞到 limit 了？」這種焦慮迴圈變成一眼可見的環境資訊，是很聰明的注意力設計。

### 與其他專案的關聯

- **[usage（aqua5230 menu bar tracker）](aqua-usage-menubar.md)**：本站已收錄的另一個本機 AI 用量追蹤器，可直接對比——aqua 走 macOS menu bar，本專案走跨平台瀏覽器 + Windows 浮動視窗，兩者都在解「額度可視化」同一個題。
- **steipete/CodexBar**：本專案的逆向來源，是 macOS-only 的原生 menu bar app（支援 20+ 家）。可把 `ai_usage_dashboard` 理解為它的「跨平台、零依賴、遊戲化」重寫版——用 CodexBar 的逆向知識，換一套 UI 哲學重做一遍。
- **[Claude Code Reverse](claude-code-reverse.md)／[Kuberwastaken](kuberwastaken-claude-code.md)／[xorespesp](xorespesp-claude-code.md)**：同屬「逆向工程 AI coding 工具」主題脈絡，差別在那些是拆 Claude Code 本體，這個是拆各家的 usage 端點。
