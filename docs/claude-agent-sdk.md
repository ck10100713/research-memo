---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-robot-outline"
oneliner: "Anthropic 官方 Agent SDK — 把 Claude Code 的工具與 Agent Loop 變成可程式化的 Python / TypeScript 函式庫"
---

# Claude Agent SDK 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方文件 | [platform.claude.com/docs/en/agent-sdk/overview](https://platform.claude.com/docs/en/agent-sdk/overview) |
| Quickstart | [platform.claude.com/docs/en/agent-sdk/quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart) |
| Python SDK GitHub | [github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) |
| TypeScript SDK GitHub | [github.com/anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) |
| 範例 Agents | [github.com/anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos) |
| 工程部落格 | [anthropic.com/engineering/building-agents-with-the-claude-agent-sdk](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) |
| 社群教學 (Nader) | [nader.substack.com](https://nader.substack.com/p/the-complete-guide-to-building-agents) |

## 專案概述

Claude Agent SDK 是 Anthropic 的官方函式庫，前身為 **Claude Code SDK**（已正式更名）。它將 Claude Code 內部的工具系統、Agent Loop 與上下文管理機制，以 Python 和 TypeScript 雙語言暴露給開發者，讓你可以用幾行程式碼建構出能自主讀檔、執行指令、搜尋網路、編輯程式碼的 AI Agent。

核心差異在於：**Client SDK 需要你自己寫 tool loop；Agent SDK 由 Claude 自主執行工具**。開發者只要定義目標（prompt）、授權工具（allowed_tools）、設定權限模式（permission_mode），剩下的迴圈控制、工具呼叫、錯誤重試全由 SDK 處理。

## 核心架構

```
┌─────────────────────────────────────────────────┐
│                   query()                        │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐ │
│  │  prompt   │──▶│  Agent   │──▶│  async iter  │ │
│  │ + options │   │   Loop   │   │  (messages)  │ │
│  └──────────┘   └────┬─────┘   └──────────────┘ │
│                      │                            │
│         ┌────────────┼────────────┐               │
│         ▼            ▼            ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│   │ Built-in │ │   MCP    │ │ Subagent │        │
│   │  Tools   │ │ Servers  │ │  (Agent) │        │
│   └──────────┘ └──────────┘ └──────────┘        │
│                                                   │
│   Hooks: PreToolUse / PostToolUse / Stop / ...    │
└─────────────────────────────────────────────────┘
```

## 安裝與認證

=== "TypeScript"

    ```bash
    npm install @anthropic-ai/claude-agent-sdk
    ```

=== "Python"

    ```bash
    pip install claude-agent-sdk
    ```

**認證方式：**

| 方式 | 環境變數 | 說明 |
|------|---------|------|
| Anthropic API | `ANTHROPIC_API_KEY` | 直接使用 Anthropic API |
| Amazon Bedrock | `CLAUDE_CODE_USE_BEDROCK=1` | 需配合 AWS credentials |
| Google Vertex AI | `CLAUDE_CODE_USE_VERTEX=1` | 需配合 GCP credentials |
| Microsoft Azure | `CLAUDE_CODE_USE_FOUNDRY=1` | 需配合 Azure credentials |

## 核心功能

### 1. 內建工具（Built-in Tools）

| 工具 | 功能 |
|------|------|
| `Read` | 讀取工作目錄下任何檔案 |
| `Write` | 建立新檔案 |
| `Edit` | 精確編輯現有檔案 |
| `Bash` | 執行終端指令、腳本、git 操作 |
| `Glob` | 以 pattern 搜尋檔案（`**/*.ts`） |
| `Grep` | 以 regex 搜尋檔案內容 |
| `WebSearch` | 搜尋網路取得最新資訊 |
| `WebFetch` | 抓取並解析網頁內容 |
| `AskUserQuestion` | 向使用者提問（含多選項） |

### 2. Hooks（生命週期鉤子）

在 Agent 生命週期的關鍵時刻執行自訂邏輯：

| Hook | 觸發時機 |
|------|---------|
| `PreToolUse` | 工具執行前（可攔截、修改） |
| `PostToolUse` | 工具執行後（可記錄、驗證） |
| `Stop` | Agent 結束前 |
| `SessionStart` | 會話開始 |
| `SessionEnd` | 會話結束 |
| `UserPromptSubmit` | 使用者提交 prompt 時 |

```python
# 範例：記錄所有檔案變更到 audit log
async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}
```

### 3. Subagents（子代理）

可定義專門化的子 Agent，主 Agent 透過 `Agent` 工具委派任務：

```python
agents={
    "code-reviewer": AgentDefinition(
        description="Expert code reviewer for quality and security reviews.",
        prompt="Analyze code quality and suggest improvements.",
        tools=["Read", "Glob", "Grep"],
    )
}
```

子 Agent 的訊息包含 `parent_tool_use_id` 欄位，可追蹤歸屬。

### 4. MCP（Model Context Protocol）

透過 MCP 連接外部系統——資料庫、瀏覽器、API 等：

```python
mcp_servers={
    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
}
```

### 5. Sessions（會話管理）

支援跨查詢維持上下文，可暫停後透過 `session_id` 恢復：

```python
# 第一次查詢：擷取 session_id
async for message in query(prompt="Read the auth module", ...):
    if hasattr(message, "subtype") and message.subtype == "init":
        session_id = message.session_id

# 第二次查詢：以完整上下文繼續
async for message in query(prompt="Now find all callers", 
                           options=ClaudeAgentOptions(resume=session_id)):
    ...
```

### 6. 結構化輸出

支援 JSON Schema 格式化輸出：

```typescript
outputFormat: {
  type: "json_schema",
  schema: yourSchema
}
// 結果在 message.structured_output 中
```

### 7. 權限控制

| 模式 | 行為 | 適用場景 |
|------|------|---------|
| `default` | 需 `canUseTool` callback 審核 | 自訂審核流程 |
| `acceptEdits` | 自動批准檔案編輯 | 受信任的開發工作流 |
| `dontAsk` (TS only) | 拒絕非 allowedTools 的一切 | 鎖定的 headless agent |
| `bypassPermissions` | 所有工具無需提示 | 沙箱 CI、完全受信任環境 |

## Claude Code 整合功能

啟用 `setting_sources=["project"]` 後可使用：

| 功能 | 說明 | 位置 |
|------|------|------|
| Skills | Markdown 定義的專門能力 | `.claude/skills/*/SKILL.md` |
| Slash Commands | 常用任務的自訂指令 | `.claude/commands/*.md` |
| Memory | 專案上下文與指示 | `CLAUDE.md` / `.claude/CLAUDE.md` |
| Plugins | 擴充自訂指令、Agent、MCP | 程式化 `plugins` 選項 |

## 快速開始範例

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

## 訊息串流類型

| 類型 | 說明 |
|------|------|
| `system` (subtype: `init`) | 會話初始化、可用工具清單 |
| `assistant` | Claude 的回覆、工具呼叫 |
| `result` | 最終結果、費用追蹤 |

費用追蹤可透過 `message.total_cost_usd`、`message.usage`、`message.modelUsage` 取得。

## Agent SDK vs Client SDK vs CLI

| 面向 | Client SDK | Agent SDK | CLI |
|------|-----------|-----------|-----|
| 工具執行 | 自行實作 loop | 自動執行 | 自動（互動式） |
| 適用場景 | 簡單 API 呼叫 | 生產自動化、CI/CD | 日常開發、一次性任務 |
| 自訂性 | 最高 | 高（hooks/subagents） | 中（config files） |
| 語言 | Python / TS / Java / Go | Python / TypeScript | CLI |

## 目前限制 / 注意事項

- **版本尚未穩定**：Python 0.1.x、TypeScript 0.2.x，API 可能持續調整
- **品牌限制**：不得使用 "Claude Code" 或 "Claude Code Agent" 作為產品名稱
- **認證限制**：不允許第三方使用 claude.ai 登入或速率限制（除非事先批准）
- **費用控制**：需自行監控 `total_cost_usd`，無內建預算上限機制
- **沙箱**：SDK 本身不提供執行沙箱，`Bash` 工具會在本機執行真實指令

## 研究價值與啟示

### 關鍵洞察

1. **「Claude Code as a Library」是關鍵定位**——不是另一個 Agent 框架，而是把已經被驗證有效的 Claude Code 產品能力（工具、Loop、上下文管理）直接抽出來給開發者。這比從零開始設計 Agent 框架有更高的實用性基礎。

2. **內建工具是最大差異化**——相比 OpenAI Agents SDK 的「空工具箱 + 自行組裝」，Claude Agent SDK 出廠即帶 8 個經過 Claude Code 驗證的工具（Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch）。開發者不需要實作檔案讀寫或指令執行，直接開始業務邏輯。

3. **Hooks 系統取代 Guardrails**——Claude 選擇用生命週期鉤子（Pre/PostToolUse）來實現安全控制，而非 OpenAI 的獨立 Guardrails 抽象。優點是更靈活（可攔截任何工具的任何階段），缺點是需要更多開發者手動設計安全策略。

4. **Sessions 設計支援 long-running agent**——可暫停、恢復、分岔（fork），適合需要跨多輪互動的複雜工作流，也適合 CI/CD pipeline 中的背景任務。

5. **雙語言支援（Python + TypeScript）降低採用門檻**——不像某些框架只有 Python，Agent SDK 同時支援前後端開發者，特別適合全端團隊。

### 與其他專案的關聯

- **vs [Claude Code SDK (cloclo)](claude-code-sdk.md)**：Claude Agent SDK 是 Claude Code SDK 的正式繼任者（renamed），cloclo 的逆向工程分析可作為理解 Agent SDK 內部機制的參考
- **vs [Analysis Claude Code](analysis-claude-code.md)**：Agent SDK 將 Claude Code 的架構正式 API 化，之前的架構分析可對照理解哪些內部機制被暴露
- **vs CrewAI / LangGraph 等框架**：Claude Agent SDK 是「單一模型 + 內建工具」路線，不走多框架抽象層；適合明確使用 Claude 的場景，不適合需要模型切換的需求
