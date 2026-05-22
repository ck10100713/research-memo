---
date: "2026-05-22"
category: "Coding Agent 工具"
card_icon: "material-console-line"
oneliner: "Anomaly (前 SST 團隊) 開源 AI coding agent，163k stars/19k forks，TUI 為主、支援 75+ LLM provider、MCP、桌面 App、GitHub Action、SDK，與 Claude Code 同級的多 provider 替代品"
---

# OpenCode (anomalyco/opencode) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/anomalyco/opencode> |
| 官方網站 | <https://opencode.ai> |
| 官方文件 | <https://opencode.ai/docs> |
| Discord | <https://opencode.ai/discord> |
| npm 套件 | <https://www.npmjs.com/package/opencode-ai> |
| Dax 公告改名推文 | <https://x.com/thdxr/status/2007199285251842478> |
| OpenCode vs Claude Code 比較（MorphLLM） | <https://www.morphllm.com/comparisons/opencode-vs-claude-code> |
| Grokipedia 條目 | <https://grokipedia.com/page/opencode> |
| AI Wiki 條目 | <https://aiwiki.ai/wiki/opencode> |

## 專案概述

**OpenCode** 是 **Anomaly**（原 SST / Serverless Stack 團隊）開發的開源 AI coding agent，2025-06-19 公開發布。截至 2026-05 已累積 **163,734 stars、19,338 forks、5,959 open issues**，是過去一年成長最快的開發者工具之一（mid-2026 達 6.5M 月活開發者）。

主打三個賣點：

1. **Terminal-native** — 預設介面是 TUI，但也提供桌面 App（Tauri，macOS/Windows/Linux）、IDE extension、Web、GitHub Action。
2. **75+ LLM provider** — 不綁定單一廠商，可接 Anthropic / OpenAI / Google / 開源模型 / Ollama 本地推論，BYOK 或使用官方 OpenCode Zen gateway。
3. **完整 MIT 授權** — 與 Claude Code（閉源、需訂閱）形成鮮明對比。

> **2026 改名事件**：原本掛在 `sst/opencode`，2026 Q1 公司公開更名為 Anomaly，repo 轉移到 `anomalyco/opencode`。舊 URL 仍可重導，但 GitHub Action 使用者必須手動更新。

> **2026-01 OAuth 封鎖事件**：Anthropic 在 2026-01 阻擋 OpenCode 使用 Claude consumer OAuth token，迫使 OpenCode 轉向獨立 gateway（OpenCode Zen）與 BYOK 策略。這是「閉源 vendor vs 開源 agent」博弈的標誌性事件。

## Monorepo 架構

從 `packages/` 目錄結構可推測團隊把 agent 拆成 21 個獨立子套件：

```
packages/
├── opencode/           # 核心 CLI / TUI
├── core/               # agent runtime
├── llm/                # provider 抽象層（75+ providers）
├── plugin/             # 外掛系統
├── sdk/                # 開發者 SDK
├── desktop/            # Tauri 桌面 App
├── web/                # 官網 + Web UI
├── console/            # opencode.ai/console 管理介面
├── docs/               # 文件站
├── extensions/         # IDE 擴充套件
├── enterprise/         # 企業版功能
├── http-recorder/      # HTTP 錄製（debug 用）
├── identity/           # 認證
├── containers/         # 容器化部署
├── function/           # serverless functions
├── slack/              # Slack 整合
├── script/             # 腳本工具
├── effect-drizzle-sqlite/  # 內部 Effect-TS + Drizzle ORM 整合
├── ui/                 # 共用 UI 元件
├── storybook/          # UI 元件 storybook
└── app/                # 主應用框架
```

此架構透露幾個訊息：

- **不是純 CLI 玩具**：有 console、enterprise、identity、containers，顯然在走 SaaS / 企業化路線。
- **Effect-TS 重度使用者**：`effect-drizzle-sqlite` 暗示用 [Effect](https://effect.website) 函式式框架做後端。
- **多入口策略**：CLI / 桌面 / IDE / Web / Slack 五條通路平行推進。

## 核心功能

### 1. 兩個內建 Agent + 子 agent

| Agent | 用途 | 行為 |
|-------|------|------|
| `build`（預設） | 全權限開發 | 可直接編輯檔案、執行命令 |
| `plan` | 唯讀分析 | 拒絕檔案編輯、執行 bash 前先問權限 |
| `@general`（子 agent） | 複雜搜尋、多步任務 | 訊息中用 `@general` 觸發 |

**Tab 鍵切換**主 agent，這是與 Claude Code 的 `/agent` 指令最大的 UX 差異。

### 2. 多 Provider 與本地模型

| Tier | 內容 | 定價 |
|------|------|------|
| BYOK | 自帶 API key（Anthropic / OpenAI / Google / 任何 provider） | 免費（只付 API 費用） |
| Go | 開源權重模型（GLM-5.1、DeepSeek V4 等） | $10/月 |
| Zen | OpenCode 團隊驗證過的精選模型 | 視模型而定 |
| Black | 高階模型 | 視模型而定 |
| Local | Ollama / 本機推論 | 完全免費 |

### 3. MCP Server 支援

原生支援 Model Context Protocol，可接任何 MCP server 擴充工具能力。

### 4. GitHub / GitLab 整合

- **GitHub Action**：在 PR 中自動 review、回應 code comment。
- **GitLab Action**：同等功能。
- 文件位於 <https://opencode.ai/docs/github/>。

### 5. 桌面 App（BETA）

```bash
# macOS
brew install --cask opencode-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/opencode-desktop
```

平台檔案：

| 平台 | 下載 |
|------|------|
| macOS (Apple Silicon) | `opencode-desktop-mac-arm64.dmg` |
| macOS (Intel) | `opencode-desktop-mac-x64.dmg` |
| Windows | `opencode-desktop-windows-x64.exe` |
| Linux | `.deb`、`.rpm`、`.AppImage` |

### 6. SDK 與外掛

- `packages/sdk/`：開發者可以把 OpenCode 嵌入自己的應用。
- `packages/plugin/`：自訂工具、自訂 agent skill。
- HTTP API 可從遠端 / 手機控制 agent（搭配桌面 App 用）。

## 快速開始

### 安裝

```bash
# 一鍵安裝（YOLO 模式）
curl -fsSL https://opencode.ai/install | bash

# 套件管理器
npm i -g opencode-ai@latest
brew install anomalyco/tap/opencode    # macOS / Linux（推薦，永遠最新）
brew install opencode                  # 官方 Homebrew formula（更新較慢）
scoop install opencode                 # Windows
choco install opencode                 # Windows
sudo pacman -S opencode                # Arch Linux Stable
paru -S opencode-bin                   # Arch AUR Latest
mise use -g opencode                   # 跨平台
nix run nixpkgs#opencode               # Nix
```

> ⚠️ 若安裝過 0.1.x 之前的版本，必須先移除舊版。

### 安裝路徑優先順序

1. `$OPENCODE_INSTALL_DIR` — 自訂目錄
2. `$XDG_BIN_DIR` — XDG 規範
3. `$HOME/bin` — 標準使用者 bin
4. `$HOME/.opencode/bin` — 預設備援

### 設定範例

```bash
OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://opencode.ai/install | bash
```

### 啟動

```bash
opencode              # 在當前目錄啟動 TUI
# 按 Tab 切換 build / plan agent
# 訊息中 @general 喚起子 agent
```

## 發布節奏

近期 release 顯示**每日多次 minor patch**的高速迭代：

| 版本 | 日期 |
|------|------|
| v1.15.7 | 2026-05-21 |
| v1.15.6 | 2026-05-20 |
| v1.15.5 | 2026-05-18 |
| v1.15.4 | 2026-05-17 |
| v1.15.3 | 2026-05-16 |

預設分支是 **`dev`** 而非 `main`，呼應 SST 系專案一貫的 trunk-based 風格。

## OpenCode vs Claude Code 對照

| 維度 | OpenCode | Claude Code |
|------|----------|-------------|
| Provider | 75+（Anthropic、OpenAI、開源、Ollama） | Anthropic + gateway proxy |
| 授權 | MIT，完全開源 | 閉源 |
| 起步成本 | $0（BYOK / 本地） | Claude Pro $20/月起 |
| Agent 切換 | Tab 鍵切換 build/plan | `/agent` 指令 |
| 子 agent | `@general` mention | subagent mode |
| 外部研究 | Scout subagent（原生） | WebFetch 工具 |
| 自主長任務 | Background agents | `/goal` + Agent View fleet |
| Undo 機制 | 手動 git checkpoint | Esc×2 rewind 系統 |
| 本地模型 | Ollama v2 streaming | 不支援 |
| 桌面 App | Tauri（macOS/Win/Linux） | VS Code extension |
| 速度 | 基準 | 約快 45% |
| Architecture | YAML agent 檔案（`.opencode/agents/`） | 編譯式 2,896-token core prompt |

兩者在「同模型下準確率相近」，差異主要在**生態鎖定程度**與**任務形態**。

## 目前限制

- **桌面 App 仍是 BETA**：穩定性與 TUI 版本有落差。
- **5,959 open issues**：高速成長 + 大社群帶來大量未處理回報。
- **default branch = `dev`**：拉 origin/main 會抓不到最新；fork 工作流要留意。
- **Anthropic OAuth 風險**：依賴 consumer OAuth 的玩法已被封，必須用 BYOK / 第三方 gateway。
- **多入口維護成本高**：21 個 packages 同時推進，文件碎片化嚴重，新使用者上手成本不低。
- **企業版功能不透明**：`packages/enterprise/` 存在但文件未公開定價。

## 研究價值與啟示

### 關鍵洞察

1. **「閉源 agent vs 開源 agent」博弈正式進入主戰場**
   163k stars 在不到 12 個月達成，意味著開發者願意用「自帶 API key」換取脫離單一廠商鎖定。Anthropic 在 2026-01 封 OAuth 是承認此威脅的訊號。

2. **Anomaly 把 OpenSource 當行銷漏斗**
   公司同時擁有 SST、OpenNext、OpenAuth、OpenTUI、OpenCode 等「Open*」系列，每個都用 MIT 開源累積 mindshare，最後在 enterprise / hosting 層收費。這是現代 dev-tools 公司的標準商業模式（類比 [LiteLLM](litellm.md)、Vercel、Supabase）。

3. **Monorepo + Effect-TS 是新一代 TS 後端組合**
   `effect-drizzle-sqlite` 暗示團隊用 Effect（函式式錯誤處理 + 依賴注入）做後端。這個技術選型在 2026 年正在快速流行，值得學習其架構。

4. **Tab 切換 agent 的 UX 設計值得借鑑**
   把 `build / plan` 做成「鍵盤層級切換」而非「指令層級切換」，比 Claude Code 的 `/agent` 更貼近編輯器思維（vim 的 mode、tmux 的 prefix）。對 [OpenClaw](openclaw.md) 之類想做多 agent 介面的專案是直接的設計參考。

5. **多入口策略需要強架構紀律**
   21 個 packages 不是炫技，是把 CLI / TUI / 桌面 / Web / IDE / Slack / SDK 全部覆蓋，逼迫 core 必須抽象化。如果你想做 coding agent 框架，這個 monorepo 是值得逐 package 拆解的教材。

### 與其他研究筆記的關聯

- **[LiteLLM](litellm.md)**：OpenCode 內建的 75+ provider 抽象層解決的是同樣的問題（LLM gateway），但 OpenCode 是 agent-facing、LiteLLM 是 API-facing。
- **[OpenClaw](openclaw.md)** 與 **[OpenAB](openab.md)**：同樣是開源 coding agent 替代品，但 OpenCode 量級大兩個數量級。
- **[Claude Code Reverse](claude-code-reverse.md)** / **[Analysis Claude Code](analysis-claude-code.md)**：研究 Claude Code 內部設計時，可拿 OpenCode 的開源實作做對照。
- **[Open SWE](open-swe.md)**：LangGraph 系的開源 coding agent，與 OpenCode 形成「TypeScript vs Python」「TUI-first vs Server-first」的對照組。
- **[OpenHarness](open-harness.md)**：Anthropic 的 harness 設計與 OpenCode 的 agent runtime 是同一問題的不同解法。
