---
date: ""
category: "Coding Agent 工具"
card_icon: "material-console"
oneliner: "GitHub Copilot 命令列工具"
---
# GitHub Copilot CLI 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/github/copilot-cli |
| 官方文件 | https://docs.github.com/copilot/concepts/agents/about-copilot-cli |
| npm | https://www.npmjs.com/package/@github/copilot |

## 專案概述

GitHub Copilot CLI 是 GitHub 官方推出的終端機 AI 輔助工具，將 GitHub Copilot 的 AI 能力直接帶入命令列環境。它基於與 GitHub Copilot coding agent 相同的 agentic 框架，能夠理解程式碼和 GitHub 上下文，提供智慧輔助。

這個工具解決的核心問題是讓開發者在不離開終端機的情況下，就能獲得 AI 輔助的程式碼編輯、除錯和重構能力。它與 GitHub 生態系統深度整合，可以直接存取 repositories、issues 和 pull requests。

適合場景：
- 終端機為主的開發工作流程
- 需要 AI 輔助進行程式碼編輯與除錯
- GitHub 整合的專案開發
- 需要 MCP 擴展功能的進階使用者

## 核心功能

1. **終端機原生開發**：直接在命令列與 Copilot coding agent 互動，無需切換環境
2. **GitHub 整合**：使用自然語言存取 repositories、issues、pull requests
3. **Agentic 能力**：可以規劃並執行複雜的多步驟任務（建構、編輯、除錯、重構）
4. **MCP 擴展**：內建 GitHub MCP server，支援自訂 MCP servers 擴展功能
5. **完全控制**：每個操作都需要使用者明確批准，不會自動執行
6. **多模型支援**：預設 Claude Sonnet 4.5，可切換到 Claude Sonnet 4、GPT-5 等
7. **LSP 支援**：支援 Language Server Protocol，提供 go-to-definition、hover 等智慧功能
8. **Autopilot 模式**（實驗性）：讓 agent 持續工作直到任務完成

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                    使用者終端機                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                 copilot 命令                            ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   ││
│  │  │ /model    │  │ /login    │  │ /experimental     │   ││
│  │  │ /feedback │  │ /lsp      │  │ Shift+Tab (modes) │   ││
│  │  └───────────┘  └───────────┘  └───────────────────┘   ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    Agentic Harness                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • 任務規劃與執行                                        ││
│  │  • 程式碼編輯與除錯                                      ││
│  │  • 使用者批准機制                                        ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    整合層                                    │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ GitHub API    │  │ MCP Servers   │  │ LSP Servers     │ │
│  │ ───────────── │  │ ───────────── │  │ ─────────────── │ │
│  │ • Repos       │  │ • 內建 GitHub │  │ • TypeScript    │ │
│  │ • Issues      │  │ • 自訂擴展    │  │ • 其他語言      │ │
│  │ • PRs         │  │               │  │                 │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    LLM 後端                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Claude Sonnet 4.5 (預設) / Claude Sonnet 4 / GPT-5    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 安裝方式

```bash
# Windows (WinGet)
winget install GitHub.Copilot

# macOS / Linux (Homebrew)
brew install copilot-cli

# npm (跨平台)
npm install -g @github/copilot

# 安裝腳本 (macOS / Linux)
curl -fsSL https://gh.io/copilot-install | bash
```

### 前置需求

- **有效的 Copilot 訂閱**（個人、組織或企業）
- Windows 需要 PowerShell v6+
- 可選：GitHub Personal Access Token（需要 "Copilot Requests" 權限）

### 基本使用範例

```bash
# 啟動 Copilot CLI
copilot

# 首次使用需要登入
/login

# 切換模型
/model

# 啟用實驗性功能
/experimental

# 配置 LSP（可選）
# 編輯 ~/.copilot/lsp-config.json
```

### LSP 配置範例

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript"
      }
    }
  }
}
```

## 與其他工具的比較

| 特性 | GitHub Copilot CLI | MCP CLI | Claude Code |
|------|-------------------|---------|-------------|
| 官方支援 | ✅ GitHub 官方 | ❌ 社群專案 | ✅ Anthropic |
| GitHub 整合 | ✅ 原生整合 | ⚠️ 需配置 | ⚠️ 需配置 |
| MCP 支援 | ✅ 內建 + 自訂 | ✅ 原生支援 | ⚠️ 有限 |
| 本地 LLM | ❌ 僅雲端 | ✅ Ollama | ❌ 僅 Claude |
| 訂閱需求 | ✅ 需要 Copilot | ❌ 免費 | ✅ 需要訂閱 |
| Agentic 能力 | ✅ 完整 | ⚠️ 有限 | ✅ 完整 |

## 研究心得

GitHub Copilot CLI 是目前最成熟的終端機 AI 輔助工具之一，特別適合深度使用 GitHub 生態系統的開發者。

**優點：**
1. 與 GitHub 生態系統無縫整合，可直接操作 repos、issues、PRs
2. Agentic 能力強大，可處理複雜的多步驟任務
3. 使用者控制機制完善，所有操作需要明確批准
4. MCP 擴展機制提供良好的可擴展性

**限制：**
1. 需要 Copilot 訂閱，非免費使用
2. 僅支援雲端 LLM，無法使用本地模型
3. 組織/企業可能需要管理員啟用

**適用場景：**
- 已有 GitHub Copilot 訂閱的開發者
- 重度使用 GitHub 的團隊
- 需要終端機原生 AI 輔助的工作流程
- 希望使用 MCP 擴展功能的進階使用者

---
研究日期：2026-02-03
