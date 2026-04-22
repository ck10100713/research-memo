---
date: "2026-04-22"
category: "Coding Agent 工具"
card_icon: "material-console"
oneliner: "tony1223 出品的跨平台 Electron 終端機聚合器，內建 Claude Code Agent 面板、cache 成本追蹤、worktree 隔離與 WebSocket 遠端控制，4 個月累積 339 stars"
---

# Better Agent Terminal 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/tony1223/better-agent-terminal> |
| Releases | <https://github.com/tony1223/better-agent-terminal/releases/latest> |
| Homebrew Tap | `tonyq-org/tap/better-agent-terminal` |
| 作者 | [tony1223](https://github.com/tony1223) |

## 專案概述

**Better Agent Terminal（BAT）** 是一個跨平台（Windows / macOS / Linux）的 Electron 桌面應用，把「多專案終端機聚合器」和「內建 Claude Code Agent 面板」融合在同一個視窗裡。作者把終端機使用者平常同時開 iTerm、VSCode、Claude Code CLI、GitHub 網頁的工作流收攏成一個 App，每個 workspace 綁定一個專案目錄，內建 xterm.js 終端、檔案瀏覽器、Git 檢視器、Snippet 管理、PR/Issue 瀏覽。

專案 2025-12-17 建立，在 2026-04-22 當天即有 339 stars、83 forks、版本已到 v2.1.41，更新頻率極高（README 記錄 topics 有 `ai-agent`、`claude-code`、`electron`、`multi-terminal`）。定位介於「iTerm 替代品」和「Claude Code 宿主」之間，核心差異點是**把 Claude Code SDK 直接嵌進 App**，不再需要另開 CLI 終端跑 agent。

適合場景：同時維護多個專案、重度使用 Claude Code、希望把 agent cost / cache / usage 都看得見、或想要用手機遠端遙控桌面 Claude Code 的開發者。

## 核心功能

### 三大支柱

```
┌─────────────────────────────────────────────────────────┐
│ Better Agent Terminal                                   │
├───────────────┬─────────────────┬───────────────────────┤
│ Workspace     │ Claude Agent    │ Remote Access         │
│ Management    │ Panel           │ (WebSocket)           │
│               │                 │                       │
│ 多專案切換    │ 內嵌 Claude SDK │ Host/Client 模式      │
│ Groups / Tags │ Cache 成本追蹤  │ QR Code 配對          │
│ Profiles      │ Session Resume  │ Tailscale 建議        │
│ 分離視窗      │ Subagent 追蹤   │ Mobile 可連線         │
└───────────────┴─────────────────┴───────────────────────┘
```

### Workspace Management

| 功能 | 說明 |
|------|------|
| Multi-Workspace | 每個 workspace 綁一個資料夾，側欄拖拉排序 |
| Groups | 把 workspaces 分組，配篩選 dropdown |
| Profiles | 儲存多組設定（本地或遠端），快速切換 |
| Detachable Windows | 把 workspace 分離成獨立視窗，重啟自動 reattach |
| Per-Workspace Env Vars | 每個 workspace 獨立環境變數 |
| Agent Presets | 預設終端角色：Claude Code / Claude Code (worktree) / Codex Agent / plain terminal |

### Claude Agent 面板（專案最大賣點）

- **內嵌 SDK**：透過 `@anthropic-ai/claude-agent-sdk` 在 App 內直接跑 agent，不需另開終端
- **四種權限模式**：Default（逐一批准）、Accept Edits（自動通過編輯）、Plan mode（先提計畫再執行）、Bypass（全自動）
- **Session Resume / Fork / Rest/Wake**：對話可持久化、分叉，或暫停釋放資源
- **Subagent 追蹤**：顯示子任務進度、已花時間、stall detection
- **Auto-compact**：token 超過門檻自動壓縮 context
- **Git worktree 隔離**：透過 `worktree-manager.ts` 把 agent 跑在 worktree 裡，避免動到主工作區

### Statusline（15 個可配置項目）

橫跨 left / center / right 三區，可拖拉排序、上色、開關：

| Item | 資訊 |
|------|------|
| Session ID | SDK session 前 8 碼（點擊 resume） |
| Git Branch | 當前 branch |
| Tokens / Turns / Duration / Context % | Session 即時狀態 |
| Cost | 本次 session 累計美金成本 |
| 5h / 7d Usage & Reset | Anthropic rate limit 視覺化倒數 |
| Cache Eff. | Cache read 效率%（點擊看每輪 cost breakdown） |
| Max Output | 當前模型 max output tokens |

### Cache 成本意識（其他 Claude Code host 少見的功能）

- **Cache history**：每一輪對話的 cache read/write 明細，依 Opus / Sonnet / Haiku 分別計價
- **Cache TTL countdown**：右上角浮動徽章顯示 5 分鐘 / 1 小時 cache 剩餘時間，每 30 秒更新
- **Cache expiry warning**：送出前若偵測到 >150k cached tokens 已過期（>1 小時），彈窗防止全價重送

### `/auto-continue` Slash Command

解決 Claude Code 常見「agent 卡在中途、或等你說『繼續』」的痛點：

```bash
/auto-continue                  # 預設 max 3，prompt="繼續"
/auto-continue 5                # max 5，prompt="繼續"
/auto-continue 10 keep going    # max 10，自訂 prompt
/ac off                         # 關閉
```

狀態**存在 host 端**，所以遠端 client / 其他視窗看到同一個 counter。只在上一輪 `subtype=success` 時才觸發，遇到 error / abort / rate-limit 會中斷。每次 auto-send 會在訊息列標 `[auto N/max]`，避免誤以為是你自己打的。

### Remote Access（實驗功能）

BAT 內建 WebSocket server（預設 port 9876）：

1. Host 開啟 server，產生 32 字元 hex **Connection Token**
2. Client（另一台 BAT 或手機）用 Remote Profile 或掃 QR Code 配對
3. 連上後 client 可操作 host 的所有終端、Claude Agent session、workspaces
4. 跨網路情境建議搭配 [Tailscale](https://tailscale.com/) 免費方案做 peer-to-peer VPN

### 其他值得一提

- **Worker Panel（Procfile）**：在單一 tab 內跑多個 process，合併 log、可單獨 start/stop/restart，靈感來自 [Overmind](https://github.com/DarthSim/overmind)
- **Ctrl+P File Picker**：fuzzy-search 專案檔案，直接附加到 agent context
- **Snippet Manager**：SQLite-backed，支援分類、favorites、搜尋
- **Markdown Preview**：獨立側欄 + live file watching
- **Multi-account Switching**：`/switch` 在多個 Claude 帳號間切換，對付 rate limit
- **i18n**：英文、繁中、簡中

## 技術架構

```
Electron Main (Node.js)             Renderer (React 18 + TypeScript)
├─ main.ts                          ├─ App.tsx
├─ pty-manager.ts                   ├─ ClaudeAgentPanel.tsx
├─ claude-agent-manager.ts   ←→     ├─ TerminalPanel.tsx (xterm.js)
├─ codex-agent-manager.ts           ├─ Sidebar / WorkspaceView
├─ worktree-manager.ts              ├─ GitPanel / GitHubPanel
├─ account-manager.ts               ├─ FileTree / MarkdownPreview
├─ snippet-db.ts (SQLite)           ├─ SnippetPanel / WorkerPanel
└─ remote/                          └─ stores/ (pub-sub)
   ├─ remote-server.ts (ws)
   ├─ remote-client.ts
   └─ tunnel-manager.ts (QR / Tailscale)
```

**Tech Stack**

| 層 | 技術 |
|----|------|
| Framework | Electron 28.3.3 |
| Frontend | React 18 + TypeScript + i18next |
| Terminal | xterm.js + node-pty |
| AI | `@anthropic-ai/claude-agent-sdk` |
| Storage | better-sqlite3（snippets / session） |
| Remote | `ws` + `qrcode` |
| Build | Vite 5 + electron-builder |

## 快速開始

```bash
# macOS Homebrew
brew install --cask tonyq-org/tap/better-agent-terminal

# 一鍵安裝腳本（macOS / Linux / Windows Git Bash）
curl -fsSL https://raw.githubusercontent.com/tony1223/better-agent-terminal/main/install.sh | bash

# 從源碼建置
git clone https://github.com/tony1223/better-agent-terminal.git
cd better-agent-terminal && npm install
npm run dev     # 開發
npm run build   # 產出 .dmg / .AppImage / .exe
```

前置：Node.js 18+、Claude Code CLI（`npm install -g @anthropic-ai/claude-code`）已登入。

## 目前限制 / 注意事項

- **Remote Access 標記為實驗性**：WebSocket 協議、token 機制可能還會變動
- **Chocolatey 套件待審核**：Windows 目前只能走 NSIS installer / zip / 腳本
- **macOS 首次啟動需解鎖**：要到「系統設定 → 隱私與安全」按 Open Anyway
- **Native 相依需要 Xcode CLT**（`node-pty`、`better-sqlite3`）
- **依賴 Claude Code CLI**：沒裝 CLI 或沒登入，agent 面板啟動不了
- **Bypass 權限模式**：README 明確警告「use with caution」——全自動會讓 agent 在沒確認下執行任何工具

## 研究價值與啟示

### 關鍵洞察

1. **把「host 身分」做好，差異化就出來了**
   Claude Code 生態裡，做 skill / sub-agent 的人很多，做「更好的 host」的人反而少。BAT 把 cache TTL 倒數、cache expiry 警告、per-turn cost breakdown、5h/7d rate limit 視覺化這些官方 CLI 沒做的「使用者痛點」直接攤在 statusline 上，立刻就讓同一個 SDK 跑起來的體驗變得不一樣。值得對照 [cc-statusline](cc-statusline.md)、[Claude HUD](claude-hud.md) 這類純 statusline 工具——BAT 等於把這些功能內建進宿主。

2. **`/auto-continue` 是「token 經濟」下的產物**
   這個 slash command 解決的是 Claude Code 常見的「中途停下等確認」，但設計細節透露出作者踩過的坑：counter 只在 `subtype=success` 時遞增、手動輸入就重置、`/abort` 會清狀態、每次 auto-send 標 `[auto N/max]`。這些護欄都是避免「半夜自動燒掉 rate limit」的實務經驗，比單純 while-loop 成熟很多。可對照 [Copilot Ralph](copilot-ralph.md)、[ralph-loop](https://github.com/) 這類迭代 loop 工具——BAT 的做法是**保守派**，只在成功且未 streaming 時續跑。

3. **Git worktree 隔離 = 防止 agent 炸主分支**
   `worktree-manager.ts` 專門處理 Claude agent 的 worktree lifecycle，配合 `Claude Code (worktree)` 預設角色，讓每個 agent session 跑在獨立 worktree 裡。這是把「agent 會亂改檔案」當作必然前提、從**目錄層級**隔離的設計，比只做權限提示更徹底。

4. **WebSocket Remote + QR Code 把 Claude Code 推向行動端**
   把桌面 Claude Code 變成 server，手機掃 QR 就能遙控——對於「通勤時也想看 agent 跑到哪」的場景非常實用。協議仍在實驗階段，但 `protocol.ts` + `broadcast-hub.ts` + `handler-registry.ts` 這套「unified IPC + remote handler registry」的架構值得參考，想做任何「桌面 agent + 手機 client」的人都可以借鑒。

5. **「多帳號切換」是合規 + 成本的現實解**
   `/switch` 搭配 5h / 7d usage 顯示，讓使用者可以在多個 Anthropic 帳號間輪換，避開單帳號 rate limit。這個功能在官方 CLI 沒有、但真正重度使用者需要——作者顯然是自己痛過。

### 與其他研究筆記的關聯

| 主題 | 關聯性 |
|------|--------|
| [Claude HUD](claude-hud.md) / [cc-statusline](cc-statusline.md) | BAT 把類似的 statusline 功能內建進宿主，對照觀察「外掛 vs 內建」取捨 |
| [Claude Code SDK (cloclo)](claude-code-sdk.md) / [Claude Agent SDK](claude-agent-sdk.md) | BAT 是 SDK 宿主的完整實作範例 |
| [Copilot Ralph](copilot-ralph.md) / [ralph-loop](https://github.com/) 系列 | `/auto-continue` 是另一種 iterative loop 思路，護欄設計更保守 |
| [gstack](gstack.md) / [Everything Claude Code](everything-claude-code.md) | 同樣聚焦「Claude Code 工作流」，但 BAT 是桌面 GUI、非 CLI 套件 |
| [Claude Code Showcase](claude-code-showcase.md) | 一個「把 Claude Code 變成產品」的實作樣本 |

簡言之，BAT 回答了一個很實際的問題——「如果我每天 8 小時都在跟 Claude Code 互動，我需要的是什麼？」答案不是更多 skills 或 sub-agents，而是一個**能把成本看清楚、把 session 管好、能從手機遙控、能隔離破壞**的宿主。
