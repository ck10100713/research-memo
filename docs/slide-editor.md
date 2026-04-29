---
date: "2026-04-29"
category: "Coding Agent 工具"
card_icon: "material-presentation"
oneliner: "garyyang1001 打造的瀏覽器內 HTML 簡報編輯器，串 Claude Code / Codex CLI 做元件級 AI 改寫，把 Claude Design 後續迭代成本壓到零頭"
---

# Claude Slide Editor 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/garyyang1001/slide-editor> |
| 介紹影片（Remotion） | <https://www.youtube.com/watch?v=XzqKnguk63k> |
| 出品方｜好事發生數位 Ohya Digital | <https://ohya.co> |
| Claude Design（搭配工具） | <https://claude.ai/> |

## 專案概述

`slide-editor`（產品名 **Claude Slide Editor**）是一個**單檔 Python、零外部相依**的瀏覽器內 HTML 簡報編輯器。作者 Gary（好事發生數位創辦人）為了一個明確工作流而做：**第一版用 Claude Design 從零生整份 deck，後續所有迭代都在本機編輯器裡完成**。

它解的痛點很具體：Claude Design / Artifacts 出第一版簡報很猛，但每改一句話、調一張卡片，都要把整份 deck 重灌進 LLM context，幾輪下來 token quota 就燒光。`slide-editor` 把後續迭代拆成「手動編輯（免費）」+「AI 改寫單一元件（每次只送一個 element + 一個指令）」兩條路徑，token 用量是 Claude Design 重生整份的零頭。

repo 2026-04-29 剛建立、MIT、5 stars，topic 標 `claude / codex / contenteditable / ohya-digital`。

## 核心功能

| 類別 | 能力 |
|------|------|
| **直接編輯** | hover slide 內任何文字 → 淡灰細線提示 → 點下去打字（自動偵測 leaf 元素並標 `contenteditable`） |
| **新增元件** | 工具列「＋ 標題 / ＋ 文字」→ 游標準心 → 點 slide 任意位置放，用 `position:absolute` 不破壞 layout |
| **字體系統** | 13 款 Google Fonts（Noto Sans/Serif TC、Inter、Plus Jakarta、IBM Plex、Crimson Pro、Lora、JetBrains Mono…），動態載入 |
| **字重 / 字級 / 粗斜底** | 浮動工具列下拉 + `⌘B/I/U`、`Alt+↑/↓` 字級 ±2px、RESET 一鍵清 |
| **移動元件** | 移動模式下拖元件，存成 `transform: translate(x,y)`，雙擊還原；自動處理 `<deck-stage>` scale 換算 |
| **插入圖片** | 拖檔到 slide（指定位置）或工具列按鈕（自動放當前 slide 中央，四層 fallback 偵測） |
| **縮放圖片** | 點圖 → 四角 handle → 鎖比例縮放 |
| **AI 即時改寫** | 標元素 + 寫指令 → 10–18 秒 → 改前/改後並排 → 套用 / 丟棄 / 改 prompt 再試 |
| **AI 佇列改寫** | prompt 寫到 `prompts.json`，回 Claude Code 對話框說「跑 queue」批次處理 |
| **右鍵刪除** | 紙底選單「刪這個 / 刪外層容器」 |
| **存檔 + 備份** | `⌘S` 寫回原檔，每次存前自動備份到 `.backups/`，保留 20 份 |
| **啟動首頁** | 拖 Claude Design zip / 貼路徑 / 最近 10 個專案點開 |

## 技術架構

```
slide-editor/
├── main.py                # 入口（13 行）
├── editor.py              # 向後相容 shim
└── slide_editor/
    ├── server.py          # Config + Handler + main()  (~520 行)
    ├── launcher.py        # zip 解壓 + recents + 模式切換  (~140)
    ├── images.py          # multipart 解析器 + 圖片上傳  (~140)
    ├── ai.py              # Claude / Codex CLI backends  (~165)
    └── overlay/
        ├── editor.js      # 注入到 deck 的 JS bundle  (~1850)
        └── launcher.html  # 啟動首頁  (~250)
```

Python 約 1000 行（從原本單檔 3000+ 行拆出）。**沒有 build step、沒有 npm、沒有外部 Python 套件**，`python3 main.py` 一行跑起來。

伺服器五件事：

1. **服務 deck 檔**：GET 時把 `overlay/editor.js` 注入到 `</body>` 前才回傳；原檔不動。
2. **slide 級存檔**：`POST /save-slide` 用 regex 找對應 slide 區塊，換 inner HTML、寫回；先備份。
3. **管 prompt + 跑 AI**：`/queue-prompt`、`/list-prompts`、`/clear-prompts` 操作 `prompts.json`；`/ai-edit` shells out 到 `claude` 或 `codex` CLI。
4. **圖片上傳**：`POST /upload-image` 自帶 multipart 解析器（不依賴已 deprecate 的 `cgi` module），驗副檔名/MIME/大小、`realpath` 防穿越，存到 `<docroot>/images/`。
5. **Launcher 模式**：不傳 deck arg 時啟動成 launcher；解壓 zip 到 `~/.slide-editor/projects/<name>-<時間戳>/`、`recent.json` 記最近 20 筆。

## AI Backend

兩個都用 OAuth 登入吃訂閱 quota，**完全不用 API key**：

| Backend | 安裝 | 登入 |
|---------|------|------|
| **Claude Code CLI** | docs.claude.com/en/docs/claude-code | Anthropic 帳號 |
| **OpenAI Codex CLI** | `npm i -g @openai/codex` | ChatGPT 帳號 OAuth |

`--backend auto`（預設）先用 claude，沒裝才用 codex。`--no-ai` 完全停用即時改寫，但佇列功能還在。

## 自訂 deck 結構

預設假設每張 slide 是 `<section class="slide" data-label="...">`。其他結構用三個旗標調整：

```bash
# <article class="page" id="page-1">
python3 editor.py deck.html --slide-tag article --slide-class page --slide-key id

# <div data-slide="1">
python3 editor.py deck.html --slide-tag div --slide-class slide --slide-key data-slide
```

regex 會根據這三個值組出來找對應 slide 區塊。

## 設計系統

對齊「好事發生數位 design system v2.0」── 紙感背景、hairline rules、直角、Noto Sans TC 300、紅色只用在「決定性標記」。**無 emoji、無陰影、無圓角、無 tech-blue**。色票只有 5 色 + 2 個 surface 階：

| Token | Hex | 角色 |
|-------|-----|------|
| `--ed-ink` | `#2D2A26` | 主要文字、anchor border |
| `--ed-bg` | `#F5F5F0` | 紙張背景 |
| `--ed-gray` | `#8C8C88` | 次要文字、caption |
| `--ed-line` | `#E0E0D8` | 細線分隔 |
| `--ed-red` | `#C84630` | 決定性標記（每頁 ≤5%） |

所有編輯器樣式用 `--ed-*` 命名空間，不撞 deck 自己的 CSS。

## 目前限制與注意事項

- **適用範圍窄**：專為 HTML 簡報設計，不是泛用 HTML 編輯器；slide 結構需固定 tag/class/key 三件式。
- **AI 改寫依賴 CLI**：`claude` 或 `codex` 必須先裝好並 OAuth 登入，否則只剩手動 + 佇列。
- **新元件用 absolute**：避免破壞原 layout 但也意味著新元件不會跟著 deck 響應式換版。
- **小規模專案**：今天剛建（2026-04-29）、5 stars、1 fork、Python 3.7+，目前還是 early stage 個人工具。
- **regex 存檔**：用 regex 找 slide 區塊覆寫，遇到嵌套或非標準結構可能失敗 ── 自動備份是 safety net。

## 研究價值與啟示

### 關鍵洞察

1. **「分工到 token 粒度」是 LLM 工作流的核心成本槓桿**：Claude Design 擅長從零生整份 deck（這是它的甜蜜區），但用它改一句話的 token 成本完全不合理。`slide-editor` 把這條線切得很乾淨 ── **整體生成交給 Claude Design，元素級修改交給本機 + 單元素 prompt**，每次 AI 呼叫的 context 從「整份 deck」壓到「一個元素 + 一個指令」。這個 pattern 可以套用到任何「AI 生大件，人類迭代細節」的情境。

2. **CLI as backend 是聰明的工程取捨**：作者沒有去碰 Anthropic / OpenAI API、不用維護 API key 流程，而是直接 shell out 到 `claude` / `codex` CLI，吃使用者既有的 OAuth 訂閱 quota。對個人工具/開源專案來說，這把「使用者要先有 API key」的門檻完全移除了，也省掉了計費、限流、密鑰管理的複雜度。**「把 CLI 當 backend」這個設計值得記下來**，下次做小型 AI 工具時可參考。

3. **「立即改寫 vs 加入佇列」的 dual-mode 設計**：即時改寫適合「我知道我要什麼、希望快」；佇列適合「我有 5 處想改、想一次處理省 context switch」。佇列的玩法尤其有趣 ── prompt 寫到 `prompts.json` 後，作者讓使用者**回到 Claude Code 對話框說「跑 queue」**，由 Claude Code 自己讀檔、看上下文、用 Edit 改 HTML。等於是讓編輯器變成「Claude Code 的 prompt 收集器」，主腦還是 Claude Code。

4. **零依賴 + 單檔 Python 是 distribution 的終極形態**：`python3 main.py` 一行跑起來，不用 npm install、不用 venv、不用 build。對「想分享給非技術用戶或客戶」的工具，這個門檻低到不能再低。代價是 JS bundle 1850 行混在一個檔裡寫，但作者已經拆出 `overlay/editor.js` 解決 IDE syntax highlighting 問題。

5. **「副產品開源」的可信度**：作者明說這是顧問工作流的副產品 ── 他們每週都在打磨客戶 deck，這工具是自用的、痛點是真的。比起為了開源而做的工具，這種「自用 → 順手開源」的專案通常 dogfooding 程度高、設計取捨乾淨、長期維護動機在。

### 與其他研究筆記的關聯

- **[Claude Design](claude-design.md)**：本工具的「上游」，slide-editor 補的是 Claude Design 「生第一版很強、迭代很貴」的痛點，兩者組合才是完整工作流。
- **[design-md-chrome](design-md-chrome.md)**：另一個串「設計」與「coding agent」的工具（瀏覽器擴充把網站 DESIGN.md 餵給 Claude Code），都展示「把現成 CLI 當 backend」的小工具設計模式。
- **[Better Agent Terminal](better-agent-terminal.md)**：類似精神 ── 把 Claude Code SDK 包進更易用的桌面 UI；slide-editor 則是把 Claude / Codex CLI 包進編輯器 UI。
- **[Claude Code SDK](claude-code-sdk.md)**：相對於 SDK 路線，slide-editor 走「直接 shell out CLI 吃 OAuth quota」這條更輕量的路，對個人工具是合理選擇。
