---
date: "2026-05-19"
category: "Coding Agent 工具"
card_icon: "material-counter"
oneliner: "aqua5230 隱私優先 macOS menu bar 用量追蹤器，把 Claude Code + Codex 5h/7d/今日 token 釘在右上角，零 API 呼叫純讀本機檔，台灣版專屬面板"
tags:
  - claude-code
  - terminal
  - taiwan
---

# usage (aqua5230) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/aqua5230/usage> |
| 作者 | aqua5230（看起來是台灣開發者——專屬「台灣用量監控」面板） |
| 規模 | 47 stars / 6 forks / MIT / 創建 **2026-05-17（只有 2 天舊）** |
| 平台 | macOS only（Python 3.13 + PyObjC） |
| 雙語 README | 繁體中文 + English |
| Topics | claude-code、codex、launchagent、macos、menubar、pyobjc、statusline-hook、usage-tracker |

## 概述

**usage** 是 aqua5230 在 2026-05-17 上線、極新的小工具——把 **Claude Code 跟 Codex 的用量同時釘在 macOS 右上角 menu bar**。最大設計賣點：**完全不呼叫 Anthropic / OpenAI 的 API、也不讀 Keychain**，純讀本機檔。作者的精準表述：

> *「不會發生『自己每分鐘 ping 一次也算用量』這種事」*

對「想看用量但不想浪費 quota」的使用者，這是個重要的隱私 / 成本承諾。

## 兩條取數路線（核心架構）

**Claude Code 跟 Codex 用了完全不同的方法取用量**，因為兩個 CLI 提供的介面不同：

### 路線 A — Claude Code: statusLine hook

```mermaid
flowchart LR
    A[Claude Code 主程式] -->|每次刷新狀態列<br/>把 JSON 透過 stdin 餵給 hook| B[usage-statusline.py<br/>hook 腳本]
    B -->|寫入| C[(~/.claude/<br/>usage-status.json)]
    D[usage menu bar / TUI] -->|讀取| C
    D -->|顯示| E[macOS menu bar]
    F((Anthropic API)) -.x.- D
```

1. `python3 main.py --setup` 把 `usage_statusline.py` 複製到 `~/.claude/usage-statusline.py`
2. 改 `~/.claude/settings.json` 把 `statusLine` 指向這個 hook（**原本的 statusLine 自動備份到 `settings.usage.previousStatusLine`，不會被蓋掉**）
3. 之後 Claude Code 每次刷新狀態列時，hook 自動跑、把 JSON 寫進 `~/.claude/usage-status.json`
4. usage menu bar / TUI 讀這個檔

→ **數字跟 Claude Code 自己看到的完全一樣**（同一份來源）。

### 路線 B — Codex: 掃 session JSONL

Codex CLI **沒有 statusLine hook 機制**，所以走另一條路：

- 掃 `~/.codex/sessions/*.jsonl` 對話紀錄檔
- 每筆對話有 `rate_limits` 欄位（Codex 自己寫的配額資訊）
- 直接讀其中的 5 小時 + 7 天用量百分比 + token 統計

→ 沒裝 Codex 或沒這個資料夾，Codex 那塊自動隱藏，不影響 Claude Code 顯示。

## 讀檔優先順序（兼容性設計）

```text
1. ~/.claude/usage-status.json     ← usage 自己寫的（v0.2+）
2. ~/.claude/usag-status.json      ← v0.1.x legacy 自動 fallback（拼錯但保留兼容）
3. ~/.claude/tt-status.json        ← stormzhang/token-tracker 共用備援
```

→ **跟 token-tracker 共用狀態檔**這點很重要——已經裝過 token-tracker 的人 fork 不用做任何事就能用，零摩擦遷移。

## 唯一會連網的情況

整個 app 只有一個地方碰外網：**估算 Codex 成本時下載 LiteLLM 價格表**

- 從 [LiteLLM GitHub](https://github.com/BerriAI/litellm) 抓 token 單價表
- 存 `~/.claude/pricing_cache.json`
- 7 天過期再抓
- 下載失敗用內建 fallback 價格，**不影響用量百分比顯示**

## 三種使用模式

### 1. Menu bar（預設 / 推薦）

```bash
python3 main.py
```

選單列顯示：`🐾 37%`（Claude only）或 `🐾 37% · 📜 10%`（雙引擎）

點開 popover 顯示：
- 兩張卡片（Claude + Codex，各有 5h Session + 7d Weekly 進度條）
- 速率 / 同步狀態 / 今日 token + 成本估算
- 「立即更新」/「結束」按鈕

### 2. TUI（純文字介面）

```bash
python3 main.py --tui
```

留在終端機內、Claude pixel art logo + 旋轉 spinner + 輪播 Claude Code 經典搞笑 loading 字串 + 進度條。

### 3. Mock 預覽

```bash
python3 main.py --mock         # menu bar 用假資料
python3 main.py --tui --mock   # TUI 用假資料
```

→ **還沒裝 hook 也能先看 UI 長什麼樣**，這個體驗設計很細心。

## 面板主題系統（v0.3.0+）

popover 內建兩個主題，**選擇記在 `NSUserDefaults`**（macOS 偏好設定）：

| 主題 | 風格 |
|------|------|
| **預設** | 英式淡雅，兩張卡 + 速率/狀態/今日 |
| **台灣用量監控** | **紅底白字 + TAIWAN 旗 icon 標題列** |

→ 台灣主題擺在跟「預設」同等 first-class 位置——是個非常明確的「我做給台灣人用」訊號。對應 [[casper-claude-skill-design-gallery]] 把 `design-taiwan-temple` 跟 Bauhaus / Swiss 並列，**「在地化美學進入 LLM 工具」是 2026 新訊號**。

## LaunchAgent（開機自動跑）

```bash
./scripts/install-launchagent.sh    # 安裝
launchctl start com.lollapalooza.usage   # 手動啟動測試
./scripts/uninstall-launchagent.sh   # 移除
```

Log 位置：
- 一般訊息：`~/Library/Logs/usage/usage.log`
- 錯誤：`~/Library/Logs/usage/usage.err.log`

## 安裝方式（三條路線）

| 使用者類型 | 路徑 |
|----------|------|
| 一般使用者 | Releases 下載 `usage.app.zip` → 拖 `/Applications` → 第一次開 popover 點「立即安裝 hook」 |
| 開發者 | `git clone` → `python3 -m venv .venv` → `pip install -e .` → `python3 main.py --setup` |
| 不想雙擊也不想跑 Python | LaunchAgent 開機自動 |

⚠️ **沒有 Apple Developer 簽章**：第一次開 macOS Gatekeeper 會擋。解法：Finder → 按住 Ctrl 右鍵 → 打開 → 確認。

## 工程細節亮點

| 細節 | 為什麼值得看 |
|------|------------|
| `setup_hook.py` **備份原本的 statusLine** 到 `settings.usage.previousStatusLine` | 不會破壞使用者已有客製 |
| `--unsetup` **完整還原**（恢復 statusLine + 刪 hook + 刪 status 檔） | 卸載乾淨，這是少見的好設計 |
| `--interval N` 重讀間隔（最小 30 秒、預設 60 秒） | 避免狀態檔 hammering |
| `USAGE_DEBUG=1` 環境變數 debug 模式 | 不污染預設輸出 |
| 狀態檔 > 6 小時未更新自動標註「N 分鐘未更新，數字可能過時」 | 防止使用者看到 stale data |
| pricing 下載失敗 fallback 內建價格表 | 不會因網路問題壞掉 |
| pyproject.toml 標 Python 3.13 | 用最新 Python，沒包袱 |

→ **這份 7 個工程細節，是判斷「menu bar 小工具是不是認真做」的標誌性 checklist**。多數類似工具會省略 backup / unsetup / fallback / staleness 警告，aqua5230 全做了。

## 目前限制與注意事項

- **macOS only**：Linux / Windows 沒戲；Pyobjc 強相依 Cocoa。
- **Python 3.13 才 2024-10 釋出**，**對沒升級系統 Python 的人不友善**——`brew install python@3.13` 之類前置工作必須做完。
- **無 Apple 簽章**：每次大版本更新 Gatekeeper 都會擋，需要走 Ctrl+右鍵手動允許。
- **47 stars / 2 天舊 / 47 stars / 一人 repo**：作者個人專案，**社群驗證度低 / 持續維護依賴一個人**。
- **依賴 `~/.codex/sessions/` 內 `rate_limits` 欄位的格式不變**：Codex CLI 一旦改了內部 JSON schema，這個工具會壞。
- **只追蹤本機用量**：團隊 / 組織級用量需要走 Anthropic Admin Console / OpenAI Usage Dashboard，這個工具不取代那個用途。
- **`tt-status.json` 共用是個雙刃**：跟 token-tracker 共用降低遷移摩擦，**但也意味著如果 token-tracker 改格式，usage 會跟著炸**。
- **無「歷史趨勢」功能**：只看當下用量百分比 / 今日 token 數，**沒有「過去 30 天每天用多少」圖表**——對量化使用者較不夠用。

## 研究價值與啟示

### 關鍵洞察

1. **「不呼叫 API 取用量」是個重要的設計倫理**：絕大多數「用量監控」工具的做法是定期 ping API 看 quota，**諷刺地是工具本身在消耗 quota**。aqua5230 明確抓住這個矛盾，純讀本機檔——對 Anthropic Pro 每日 5 hour reset 這種有限資源，這個取捨價值很大。
2. **「statusLine hook 是 Claude Code 被低估的擴充點」**：多數人知道 Claude Code 有 plugin、skill、MCP，**但 statusLine hook 是個很乾淨的「Claude Code 主動把資訊推給我」的機制**——usage 把它當作「免費的監控 API」用。值得當作任何 Claude Code 監控 / 觀測類工具的範本。
3. **Codex 與 Claude Code 工具生態差距明顯**：Codex 沒 statusLine hook、只能掃 JSONL；Claude Code 有完整 hook 系統。**這個差距反映在生態系——Claude Code 的觀測 / 監控 / 整合工具會比 Codex 多很多**。對選 IDE 的人是個訊號。
4. **「跟 token-tracker 共用狀態檔」是個聰明的社群策略**：不要求使用者從 token-tracker 遷過來，**直接吃同一份狀態檔**——這降低了採用摩擦，也避免社群分裂。任何 Claude Code 觀測工具新進者都該抄這個 pattern。
5. **「台灣用量監控」面板是台灣開源圈在地化的小亮點**：跟 [[casper-claude-skill-design-gallery]] 的 `design-taiwan-temple` 一樣，**把在地美學放進跟 Bauhaus / Swiss 同等 first-class 位置**——2026 開始浮現「**LLM 工具在地化視覺**」是個有意思的子分支。
6. **2 天 47 stars 的成長速度，是「Claude Code 用量焦慮」的市場訊號**：Anthropic Pro 訂閱者極度想看用量、Anthropic 自己又不主動提供清楚介面——這個空缺**會被無數 menu bar / TUI / web 小工具填滿**。aqua5230 抓對了時機。
7. **單檔 PyObjC menu bar app 是 macOS 個人工具的範本**：menubar.py 17 KB / 整個 repo 不到 1 MB / 跑起來不到 30 MB RAM——**對「我想做個 menu bar 小工具」的人，這 repo 是極好的學習素材**（比 Rumps、SwiftBar 等 framework 更輕量）。
8. **「不要破壞使用者已有設定」的工程紀律**：自動備份 statusLine、`--unsetup` 完整還原、fallback 兼容舊檔名——這些**「小心對待別人系統」的紀律**比實際功能更值錢。是判斷「這個 dev 寫不寫 production 軟體」的指標。

### 與其他研究的關聯

- 與 [[cc-statusline]]：cc-statusline 是 Claude Code 自家的 statusLine plugin 範本／工具集，**aqua-usage 把 statusLine 當「資料來源」**，cc-statusline 把它當「UI 客製化點」——兩個研究放在一起可以理解 statusLine hook 的兩種應用方向。
- 與 [[boris-cherny-opus-4-7]]、[[zeuikli-claude-code-best-practices]]：兩份都引用 Boris Cherny「Cache rules everything」的監控思路，**aqua-usage 是這個思路的 client-side 落地**——把用量 cache（本機檔）當 SLA 監控。
- 與 [[mattpocock-skills]]、[[claude-skills-guide]]：本研究**不是 skill repo**，但它示範的是「**對 Claude Code 行為的觀測層**」，跟 skill 是 orthogonal 的擴充維度。值得對照思考 Claude Code 擴充體系：plugin / skill / MCP / hook / statusLine 各管什麼。
- 與 [[casper-claude-skill-design-gallery]]：兩者都在做「**在地化視覺**」的事——Casper 把 Taiwan Temple 放進設計風格 first-class、aqua 把台灣用量監控放進 panel theme first-class。
- 與 [[fincept-terminal]]：Fincept 是「重型桌面金融 app」，aqua-usage 是「輕量 menu bar 用量小工具」——**對「desktop native vs Electron」的兩端代表**。
- 對 retail quant：用同樣 statusLine hook 模式可以做「**Claude Code 在分析股票時即時把分析結果寫進 menu bar**」、「**回測進度條釘在 menu bar**」等小工具——這個 pattern 可以遷移到很多場景。
