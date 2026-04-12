---
date: "2026-03-23"
category: "Coding Agent 工具"
card_icon: "material-monitor-dashboard"
oneliner: "11.5K stars 的 Claude Code 狀態列 plugin，即時顯示 context 用量、工具活動、Agent 狀態"
---
# Claude HUD 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) |
| Claude Plugin Hub | [claudepluginhub.com](https://www.claudepluginhub.com/plugins/jarrodwatts-claude-hud-2) |
| Oreate AI 評介 | [Taming the Context Window](https://www.oreateai.com/blog/taming-the-context-window-a-new-hud-for-claude-code-users/67979f4b99a77d9d8ff0b129752821b6) |
| AIToolly 評測 | [Claude HUD: Monitoring Tool](https://aitoolly.com/ai-news/article/2026-03-20-claude-hud-a-new-plugin-for-real-time-monitoring-of-claude-code-context-and-agent-activity) |
| DeepWiki | [jarrodwatts/claude-hud](https://deepwiki.com/jarrodwatts/claude-hud) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | Jarrod Watts |
| Stars | 11.5K+ |
| 語言 | JavaScript / TypeScript |
| 授權 | MIT |
| 建立 | 2026-01-02 |
| 需求 | Claude Code v1.0.80+、Node.js 18+ 或 Bun |

Claude HUD 是一個 Claude Code plugin，在終端機輸入行下方顯示一個**常駐狀態列（HUD）**，即時呈現 context 使用量、活躍工具、執行中的 subagent、以及 todo 進度。解決的核心問題：**開發者在深度 coding session 中完全不知道 context window 快用完了，直到突然收到警告。**

不需要額外視窗、不需要 tmux，利用 Claude Code 原生的 **statusline API** 實作。

## HUD 顯示內容

### 預設兩行

```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

- **第一行**：模型名稱、Provider 標籤（Bedrock/API）、專案路徑、Git 分支
- **第二行**：Context bar（綠 → 黃 → 紅）+ 訂閱用量 rate limit

### 可選額外行

```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2        ← 工具活動
◐ explore [haiku]: Finding auth code (2m 15s)    ← Agent 狀態
▸ Fix authentication bug (2/5)                   ← Todo 進度
```

## 資料流架構

```
Claude Code
    │
    ├─ stdin JSON ──→ claude-hud ──→ stdout ──→ 終端機 statusline
    │                    ▲
    └─ transcript JSONL ─┘  (tools, agents, todos 活動)
```

| 資料來源 | 說明 |
|---------|------|
| stdin JSON | Claude Code 每 ~300ms 推送一次，包含原生 token 數據（非估算） |
| transcript JSONL | 工具調用、subagent 狀態、todo 進度的即時日誌 |
| rate_limits | Pro/Max/Team 訂閱者的用量限制資料 |

關鍵：**context 使用量來自 Claude Code 原生數據**，會自動適應不同的 context window 大小（包括 1M context session）。

## 原始碼結構

```
src/
├── index.ts              # 主入口，讀取 stdin、協調渲染
├── stdin.ts              # 解析 Claude Code 推送的 JSON
├── transcript.ts         # 解析 transcript JSONL（工具/Agent/Todo）
├── config.ts             # 設定讀取與預設值
├── config-reader.ts      # 設定檔 I/O
├── git.ts                # Git 分支與狀態偵測
├── speed-tracker.ts      # Token 輸出速度追蹤
├── memory.ts             # 系統記憶體使用偵測
├── render/
│   ├── index.ts          # 渲染協調器
│   ├── colors.ts         # 色彩系統（256色 + hex）
│   ├── lines/
│   │   ├── project.ts    # 專案路徑 + Git 狀態
│   │   ├── usage.ts      # Context bar + 用量顯示
│   │   ├── identity.ts   # 模型名稱 + Provider
│   │   ├── memory.ts     # RAM 使用
│   │   └── environment.ts# 環境資訊
│   ├── tools-line.ts     # 工具活動渲染
│   ├── agents-line.ts    # Subagent 狀態渲染
│   └── todos-line.ts     # Todo 進度渲染
├── types.ts              # TypeScript 型別定義
└── utils/
    └── terminal.ts       # 終端機寬度偵測
```

## 安裝與設定

```bash
# 1. 新增 marketplace
/plugin marketplace add jarrodwatts/claude-hud

# 2. 安裝 plugin
/plugin install claude-hud

# 3. 設定 statusline（引導式）
/claude-hud:setup
```

重新啟動 Claude Code 即生效。

### 三種預設 Preset

| Preset | 顯示內容 |
|--------|---------|
| **Full** | 全部啟用：工具、Agent、Todo、Git、用量、時長 |
| **Essential** | 活動行 + Git 狀態，精簡資訊 |
| **Minimal** | 僅模型名稱 + Context bar |

### 客製化

執行 `/claude-hud:configure` 進入引導式設定，或直接編輯：

```
~/.claude/plugins/claude-hud/config.json
```

支援自訂色彩（256色 / hex）、顯示元素開關、排列順序、Git 狀態細節、路徑層數等。

## 主要設定選項

| 選項 | 預設 | 說明 |
|------|------|------|
| `lineLayout` | `expanded` | `expanded`（多行）或 `compact`（單行）|
| `pathLevels` | 1 | 專案路徑顯示層數（1-3）|
| `display.showContextBar` | true | 視覺化 Context bar |
| `display.contextValue` | `percent` | 格式：`percent` / `tokens` / `remaining` / `both` |
| `display.showUsage` | true | 訂閱用量（僅 Pro/Max/Team）|
| `display.showTools` | false | 工具活動行 |
| `display.showAgents` | false | Subagent 狀態行 |
| `display.showTodos` | false | Todo 進度行 |
| `display.showSpeed` | false | Token 輸出速度 `out: 42.1 tok/s` |
| `display.showMemoryUsage` | false | 系統 RAM 使用（近似值）|
| `display.showDuration` | false | Session 時長 |

## 目前限制 / 注意事項

- **Linux 安裝問題**：`/tmp` 為獨立 filesystem 時會報 `EXDEV: cross-device link not permitted`，需設 `TMPDIR`
- **Playwright 相容性限制**：如同所有 Claude Code statusline plugin，依賴 Claude Code 的 stdin JSON 格式，版本更新可能影響
- **Usage 顯示限制**：僅 Claude Pro/Max/Team 訂閱者可見，API key 使用者無此功能
- **記憶體數據近似**：`showMemoryUsage` 報告的是系統 RAM，包含 OS cache/buffer，可能高估實際壓力
- **Context 數據延遲**：`rate_limits` 在 session 第一次模型回應後才開始推送
- **無跨 session 持久化**：HUD 狀態僅限當前 session，不會跨 session 保留歷史趨勢

## 研究價值與啟示

### 關鍵洞察

1. **「可觀測性」是 AI coding 工作流最被忽略的基礎設施**：開發者花大量時間研究如何讓 Agent 更聰明（更好的 prompt、更好的 skill），卻對 Agent 的「運行狀態」幾乎毫無能見度。Claude HUD 證明了一個簡單的狀態列就能顯著改善使用體驗——這不是高科技，而是基本的工程素養。

2. **statusline API 是 Claude Code 最被低估的擴展點**：Claude Code 的 plugin 生態大多聚焦在 skill（教 Agent 做什麼）和 command（觸發什麼動作），但 statusline API 提供了一個完全不同的維度——**被動式持續監控**。不需要使用者主動輸入 `/context`，資訊永遠在眼前。這個 API 的設計模式值得學習。

3. **Token 消耗的視覺化比數字更有效**：用 `█████░░░░░` 進度條 + 綠黃紅色彩漸變，比顯示 `45,000 / 200,000 tokens` 更能讓人直覺感受到「剩下多少」。這是一個小但重要的 UX 洞察——人類對「漸變的視覺信號」的反應速度遠快於對數字的認知解讀。

4. **11.5K stars 證明開發者對 context 管理有真實焦慮**：這是一個非常聚焦的工具——只做狀態顯示，不做任何 AI 功能。它能拿到 11.5K stars 說明 context window 焦慮是普遍痛點，也暗示 Claude Code 原生應該內建更好的狀態可視化。

5. **Plugin 的 marketplace 分發機制成熟度**：Claude HUD 的安裝流程（marketplace add → plugin install → setup）展示了 Claude Code plugin 生態系統的三步式分發模式，這個模式已經接近 VSCode extension 的體驗。

### 與其他專案的關聯

- **vs Everything Claude Code**：Everything Claude Code 是完整的 agent harness 系統，包含 statusline 配置在內的 116 個 skills。Claude HUD 則專注做好一件事——狀態可視化。兩者可以互補使用。
- **vs Superpowers**：Superpowers 專注在「教 Agent 如何工作」（紀律 + 方法論），Claude HUD 專注在「讓人看到 Agent 在幹嘛」（可觀測性）。一個是輸入端優化，一個是輸出端監控。
- **vs Learn Claude Code / Claude Skills Guide**：這些是學習資源，而 Claude HUD 是實際工具。但 Claude HUD 的原始碼（特別是 stdin 解析和 transcript 處理）是學習 Claude Code plugin 開發的優秀範例。
