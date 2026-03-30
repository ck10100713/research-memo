---
date: "2026-02-09"
category: "Coding Agent 工具"
card_icon: "material-cog"
oneliner: "GitHub Copilot 設定與自訂指令"
---
# GitHub Copilot Configs 研究筆記

## 基本資訊

| 項目 | 內容 |
|------|------|
| **來源** | https://github.com/doggy8088/github-copilot-configs |
| **作者** | Will 保哥（doggy8088） |
| **說明** | GitHub Copilot 最佳設定集合 |
| **研究日期** | 2026-02-09 |

## 專案概述

保哥整理的 GitHub Copilot 最佳設定集合，包含完整的 VS Code 設定、140+ 個 Agent 定義、170+ 個 Instructions 指令、160+ 個 Prompt 模板。透過 GitHub Actions 每日從官方 [github/awesome-copilot](https://github.com/github/awesome-copilot) 自動同步社群資源，確保永遠擁有最新內容。

## 專案結構

```
.github/
├── copilot-instructions.md          # 主要 Copilot 程式碼指引（VS Code 風格）
├── agents/                           # 140+ 個 Agent 定義檔（*.agent.md）
│   ├── debug.agent.md               # 四階段結構化除錯
│   ├── plan.agent.md                # 策略規劃模式
│   ├── Thinking-Beast-Mode.agent.md # 量子認知深度思考
│   ├── repo-architect.agent.md      # 儲存庫架構師
│   ├── context7.agent.md            # Context7 文件查詢
│   ├── playwright-tester.agent.md   # Playwright 自動化測試
│   ├── implementation-plan.agent.md # 結構化實作計畫
│   ├── github-actions-expert.agent.md # CI/CD 專家
│   └── ...
├── instructions/                     # 170+ 個指令檔（*.instructions.md）
│   ├── agents.instructions.md       # Agent 檔案建立規範
│   ├── memory-bank.instructions.md  # AI Agent 記憶庫系統
│   ├── csharp.instructions.md       # C# 開發指引
│   ├── python.instructions.md       # Python 開發指引
│   ├── angular.instructions.md      # Angular 指引
│   ├── nextjs.instructions.md       # Next.js 指引
│   ├── security-and-owasp.instructions.md # 安全性指引
│   └── ...
├── prompts/                          # 160+ 個提示檔（*.prompt.md）
│   ├── conventional-commit.prompt.md # 自動化 Conventional Commits
│   ├── github-copilot-starter.prompt.md # 專案初始化助手
│   ├── create-agentsmd.prompt.md    # 建立 AGENTS.md
│   ├── create-readme.prompt.md      # 建立 README
│   └── ...
└── workflows/
    └── sync-awesome-copilot.yml     # 每日自動同步 workflow

.vscode/
├── settings.json                     # VS Code 完整最佳設定
├── keybindings.json                 # 快捷鍵設定
└── mcp.json                         # MCP 伺服器設定（台北時區）
```

## 核心設計模式

### 1. 多層級自訂提示架構

`settings.json` 中為不同場景分別指定專屬指令檔，每項都支援混合 `text`（內嵌文字）與 `file`（外部檔案）兩種來源：

| 設定 | 用途 |
|------|------|
| `codeGeneration.instructions` | 程式碼生成 |
| `commitMessageGeneration.instructions` | commit 訊息 |
| `pullRequestDescriptionGeneration.instructions` | PR 描述 |
| `reviewSelection.instructions` | 程式碼審查 |
| `testGeneration.instructions` | 測試生成 |

範例：

```json
"github.copilot.chat.codeGeneration.instructions": [
    { "text": "Always response in #zh-tw." },
    { "file": ".copilot-instructions.md" }
],
"github.copilot.chat.commitMessageGeneration.instructions": [
    { "text": "# Use Conventional Commits 1.0.0 for commit messages." },
    { "text": "請一律使用正體中文來撰寫記錄" },
    { "file": ".copilot-commit-message-instructions.md" }
]
```

### 2. 繁體中文最佳化

- `localeOverride: "zh-TW"` 強制繁體中文回應
- 內建 30+ 組術語對照表（create=建立、object=物件、queue=佇列、stack=堆疊、information=資訊 等）
- commit message 和 PR 描述也強制使用正體中文

```json
"github.copilot.chat.codeGeneration.instructions": [
    {
        "text": "When outputing any text, use the following term mappings: create = 建立, object = 物件, queue = 佇列, stack = 堆疊, information = 資訊, ..."
    },
    { "text": "Always response in #zh-tw." }
]
```

### 3. Agent Mode 最佳化

| 設定 | 值 | 說明 |
|------|----|------|
| `chat.agent.maxRequests` | `100` | 預設 15，大幅提升自主迭代上限 |
| `chat.agent.enabled` | `true` | 啟用 Agent 模式 |
| `github.copilot.chat.agent.thinkingTool` | `true` | 啟用思考工具 |
| `github.copilot.chat.codesearch.enabled` | `true` | 啟用程式碼搜尋 |
| `github.copilot.nextEditSuggestions.enabled` | `true` | 啟用 NES |
| `terminal.integrated.scrollback` | `50000` | 提高終端回捲行數 |

### 4. 自動同步社群資源

透過 `.github/workflows/sync-awesome-copilot.yml`：

- 每天 UTC 00:00（台北 08:00）由 cron 自動執行
- 支援手動觸發（`workflow_dispatch`）
- 同步 `agents/`、`instructions/`、`prompts/`、`chatmodes/` 四個資料夾
- 清除舊檔案後再複製新檔案（非增量同步）
- 自動提交並推送變更

### 5. MCP 整合

`.vscode/mcp.json` 設定 MCP 伺服器：

```json
{
  "servers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time", "--local-timezone=Asia/Taipei"]
    }
  }
}
```

- 關閉其他 MCP Host 的自動發現（claude-desktop、windsurf、cursor 等）
- 多個 Agent 檔案內建 MCP 伺服器連接設定（如 context7）

## 三層 Agent 架構模型

`repo-architect.agent.md` 定義的標準化結構：

```
┌─────────────────────────────────────────────┐
│  Layer 1 - Foundation（系統 DNA）             │
│  copilot-instructions.md / AGENTS.md         │
├─────────────────────────────────────────────┤
│  Layer 2 - Specialists（角色與專業）           │
│  .github/agents/*.agent.md                   │
├─────────────────────────────────────────────┤
│  Layer 3 - Capabilities（執行能力）            │
│  .github/skills/ / prompts/ / instructions/  │
└─────────────────────────────────────────────┘
```

- **Layer 1 — Foundation**: `copilot-instructions.md` 和 `AGENTS.md` 定義整個專案的基底規則
- **Layer 2 — Specialists**: 各種 `.agent.md` 檔案定義不同角色（除錯、規劃、測試、架構 等）
- **Layer 3 — Capabilities**: `skills/`、`prompts/`、`instructions/` 提供可組合的執行能力

## 重要 Agent 詳解

### debug.agent.md — 除錯模式

四階段結構化除錯流程：
1. **Problem Assessment** — 評估問題
2. **Investigation** — 調查原因
3. **Resolution** — 解決問題
4. **Quality Assurance** — 品質驗證

指定工具：`editFiles`, `search`, `getTerminalOutput`, `runInTerminal`, `problems`, `testFailure`, `runTests`

### plan.agent.md — 策略規劃模式

核心原則：**Think First, Code Later**
- 扮演「技術顧問」角色
- 專注理解與規劃，而非立即實作
- 涵蓋 Information Gathering、Planning Approach、Communication 等面向

### Thinking-Beast-Mode.agent.md — 極致思維模式

量子認知架構（Quantum Cognitive Workflow Architecture）五階段流程：
- 強制使用 `sequential_thinking` 工具
- 要求 adversarial thinking（紅隊分析、失敗模式分析）
- 極其詳細的 Todo List 框架與溝通協議

### repo-architect.agent.md — 儲存庫架構師

提供五個指令：
- `/bootstrap` — 初始化專案設定
- `/validate` — 驗證現有設定
- `/migrate` — 遷移舊設定
- `/sync` — 同步社群資源
- `/suggest` — 建議最佳化方向

### context7.agent.md — Context7 文件專家

- 強制使用 Context7 MCP 工具查詢最新函式庫文件
- 自動偵測版本並提供升級建議
- 支援多語言生態系（JavaScript、Python、Ruby、Go、Rust、PHP、Java、.NET）
- 內建 MCP 伺服器設定（HTTP 類型，連接 `https://mcp.context7.com/mcp`）

### playwright-tester.agent.md — Playwright 測試模式

- 指定使用 Claude Sonnet 4 模型
- 整合 Playwright MCP 進行網站探索
- 流程：網站探索 → 測試改進 → 測試生成 → 執行與迭代 → 文件

## 重要 Instructions 詳解

### agents.instructions.md — Agent 檔案建立規範

完整的 `.agent.md` YAML frontmatter 規範：
- **必要欄位**: `description`
- **選用欄位**: `name`, `tools`, `model`, `target`, `infer`
- 工具設定支援 read/write/edit 群組、MCP 整合
- 包含 handoffs（代理轉交）機制

### memory-bank.instructions.md — 記憶庫系統

解決 AI Agent 記憶重置問題的完整文件系統：
- 核心檔案：`projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`
- `tasks/` 資料夾進行任務管理
- 支援 Plan Mode 和 Act Mode 兩種工作流程

### Instructions 的 `applyTo` 限定機制

各語言 instructions 可透過 `applyTo` 限定只在特定檔案類型中生效：
- `csharp.instructions.md` → `applyTo: '**/*.cs'`
- `python.instructions.md` → `applyTo: '**/*.py'`
- `typescript-5-es2022.instructions.md` → `applyTo: '**/*.ts'`

## 重要 Prompt 詳解

### conventional-commit.prompt.md

自動化 git commit 工作流程：`git status` → `git diff` → `git add` → `git commit`，使用 Conventional Commits 1.0.0 格式。

### github-copilot-starter.prompt.md

專案初始化設定助手，自動建立：
- `.github/copilot-instructions.md`
- `.github/instructions/`
- `.github/prompts/`
- `.github/agents/`
- `.github/workflows/copilot-setup-steps.yml`

優先從 awesome-copilot 社群資源取用。

### generate-custom-instructions-from-codebase.prompt.md

從程式碼庫分析兩個版本之間的差異，自動產生轉換規則，支援框架版本升級、架構重構、技術遷移等場景。

## VS Code 完整設定參考

### 關鍵設定項目

```json
{
    "github.copilot.chat.localeOverride": "zh-TW",
    "github.copilot.selectedCompletionModel": "gpt-41-copilot",
    "github.copilot.nextEditSuggestions.enabled": true,
    "github.copilot.chat.agent.thinkingTool": true,
    "chat.agent.enabled": true,
    "chat.agent.maxRequests": 100,
    "chat.promptFiles": true,
    "chat.mcp.enabled": true,
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "telemetry.telemetryLevel": "off"
}
```

### 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+U` | 開始/停止語音聊天 |
| `Alt+L` | 開始/停止編輯器聽寫 |
| `Ctrl+Alt+L` | 切換語言模式 |

## 關鍵啟發

1. **模組化設計** — 將 Copilot 設定拆分為 agents / instructions / prompts 三類，各司其職，可自由組合
2. **社群驅動** — 自動同步官方 awesome-copilot 資源，確保永遠保持最新
3. **在地化** — 完整的繁體中文術語對照表與語言設定，提升中文開發者體驗
4. **可組合性** — instructions 可透過 `applyTo` 限定檔案範圍，agents 可指定工具清單與模型
5. **三層架構** — Foundation → Specialists → Capabilities 的清晰分層，易於理解與擴展
6. **實用導向** — 每個設定項都有明確用途，避免過度配置

## 與本專案的關聯

此研究與本專案中的以下項目相關：
- **Copilot Ralph** (`research/copilot-ralph/`) — 同為保哥的 Copilot 生態系工具
- **GitHub Copilot SDK** (`research/github-copilot-sdk/`) — Copilot 擴展開發
- **Claude Code Showcase** (`research/claude-code-showcase/`) — 類似的 AI 工具設定最佳實踐
- **多 Agent 辯論會系統** (`research/multi-agent-debate/`) — Agent 架構設計參考
