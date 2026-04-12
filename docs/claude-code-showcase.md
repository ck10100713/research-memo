---
date: "2026-03-23"
category: "Coding Agent 工具"
card_icon: "material-star-shooting"
oneliner: "Claude Code 使用案例展示"
---
# Claude Code Showcase 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/ChrisWiles/claude-code-showcase |
| 作者 | Chris Wiles |

## 專案概述

Claude Code Showcase 是一個展示如何充分利用 Claude Code 的專案配置範例庫。它展示了如何透過 Skills、Agents、Hooks、Commands 和 MCP Servers 等機制，將 Claude Code 打造成團隊的超級戰力。

這個專案的核心理念是：「大多數軟體工程師嚴重低估了 LLM agents 的能力，尤其是像 Claude Code 這樣的工具」。透過建立一套可重複使用的 Skills 和 Agents，可以讓 Claude Code 像一個超強隊友一樣運作。

適合場景：
- 想要最大化 Claude Code 效能的團隊
- 需要建立程式碼品質自動化流程的專案
- 希望整合 JIRA/Linear 等工單系統的開發團隊
- 尋找 Claude Code 最佳實踐的開發者

## 核心功能

1. **Skills 系統**：定義專案特定的知識文件，讓 Claude 自動套用團隊規範
2. **Agents 系統**：建立專門的 AI 助手（如程式碼審查 Agent）
3. **Hooks 機制**：自動化流程（格式化、測試、型別檢查、分支保護）
4. **Commands 系統**：自訂 slash commands（如 `/ticket`、`/pr-review`）
5. **MCP 整合**：連接 JIRA、Linear 等外部工具
6. **GitHub Actions**：自動化 PR 審查、文件同步、程式碼品質檢查
7. **Skill 評估系統**：根據 prompt 自動建議啟用哪些 Skills
8. **LSP 整合**：即時程式碼智慧功能

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                     專案根目錄                               │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ CLAUDE.md   │  │ .mcp.json   │                           │
│  │ 專案記憶    │  │ MCP 配置    │                           │
│  └─────────────┘  └─────────────┘                           │
├─────────────────────────────────────────────────────────────┤
│                    .claude/ 目錄                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  settings.json                                          ││
│  │  ├─ PreToolUse Hooks   (執行前驗證)                      ││
│  │  ├─ PostToolUse Hooks  (執行後處理)                      ││
│  │  └─ UserPromptSubmit   (提示送出時)                      ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐│
│  │ agents/   │  │ commands/ │  │ hooks/    │  │ skills/   ││
│  │ ───────── │  │ ───────── │  │ ───────── │  │ ───────── ││
│  │ code-     │  │ /onboard  │  │ skill-    │  │ testing-  ││
│  │ reviewer  │  │ /pr-review│  │ eval.sh   │  │ patterns/ ││
│  │           │  │ /ticket   │  │ skill-    │  │ graphql/  ││
│  │           │  │           │  │ rules.json│  │ core-     ││
│  │           │  │           │  │           │  │ components││
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘│
├─────────────────────────────────────────────────────────────┤
│                  .github/workflows/                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • pr-claude-code-review.yml    (自動 PR 審查)           ││
│  │  • scheduled-claude-code-docs-sync.yml  (每月文件同步)   ││
│  │  • scheduled-claude-code-quality.yml    (每週品質檢查)   ││
│  │  • scheduled-claude-code-dependency-audit.yml (依賴審計) ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    MCP Servers                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  JIRA ──────▶ jira_get_issue, jira_update_issue         ││
│  │  GitHub ────▶ repo, issues, PRs                         ││
│  │  Slack ─────▶ 通知整合                                   ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 目錄結構建立

```bash
# 建立 .claude 目錄結構
mkdir -p .claude/{agents,commands,hooks,skills}
```

### CLAUDE.md 範例

```markdown
# Project Name

## Quick Facts
- **Stack**: React, TypeScript, Node.js
- **Test Command**: `npm run test`
- **Lint Command**: `npm run lint`

## Key Directories
- `src/components/` - React components
- `src/api/` - API layer
- `tests/` - Test files

## Code Style
- TypeScript strict mode
- Prefer interfaces over types
- No `any` - use `unknown`
```

### settings.json 配置範例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"Cannot edit on main branch\"}' >&2; exit 2; }",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Skill 文件範例

```markdown
---
name: testing-patterns
description: Jest testing patterns for this project. 
---

# Testing Patterns

## Test Structure
- Use `describe` blocks for grouping
- Use `it` for individual tests
- Follow AAA pattern: Arrange, Act, Assert
```

## 與其他工具的比較

| 特性 | Claude Code Showcase | 傳統 Linting | CI/CD |
|------|---------------------|-------------|-------|
| AI 驅動 | ✅ 智慧理解 | ❌ 規則型 | ❌ 規則型 |
| 自動修復 | ✅ 可自動修正 | ⚠️ 有限 | ❌ 無 |
| 上下文理解 | ✅ 理解業務邏輯 | ❌ 無 | ❌ 無 |
| 學習能力 | ✅ 透過 Skills | ❌ 無 | ❌ 無 |
| 整合深度 | ✅ JIRA/GitHub | ⚠️ 有限 | ⚠️ 有限 |

## 研究心得

Claude Code Showcase 展示了如何將 Claude Code 從簡單的 AI 助手提升為團隊的核心生產力工具。

**核心價值：**
1. **Skills 機制**：讓 AI 理解並遵循團隊規範，生成符合標準的程式碼
2. **自動化品質把關**：透過 Hooks 自動執行格式化、測試、型別檢查
3. **工單系統整合**：透過 MCP 連接 JIRA/Linear，實現從工單到 PR 的完整工作流程
4. **持續品質維護**：排程任務自動進行文件同步、程式碼品質檢查

**最佳實踐：**
1. Skill 的 `description` 欄位非常重要，Claude 會根據它決定何時套用
2. 使用 Hooks 建立品質防護網（禁止在 main 分支編輯）
3. 善用 GitHub Actions 進行自動化 PR 審查
4. MCP 整合讓 AI 能夠讀取工單並自動更新狀態

**對 AI Agent 開發的啟示：**
- 「配置即程式碼」的理念可以應用到 Agent 開發
- Skills 系統展示了如何讓 Agent 具備領域專業知識
- Hooks 機制展示了 Agent 行為的控制方式

---
研究日期：2026-02-03
