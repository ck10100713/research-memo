---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-code-braces-box"
oneliner: "單檔 18,500 行的多 Provider Claude Code 替代品——13 個 LLM 後端 + Ink TUI + NDJSON Bridge + Skills Marketplace，npm 安裝即用"
---
# cloclo (claude-code-sdk) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [SeifBenayed/claude-code-sdk](https://github.com/SeifBenayed/claude-code-sdk) |
| npm | [cloclo](https://www.npmjs.com/package/cloclo) |
| 授權 | MIT |

## 專案概述

| 指標 | 數值 |
|------|------|
| Stars | 93 |
| Forks | 26 |
| 語言 | JavaScript（單檔 `claude-native.mjs`，~18,500 行） |
| 建立日期 | 2026-03-23 |

cloclo（原名 claude-code-sdk）是一個**多 Provider 的 AI Coding Agent CLI**，目標是成為 Claude Code 的開源替代品。核心賣點是**單檔架構 + 13 個 LLM 後端**，從 Anthropic、OpenAI 到本地 Ollama 都支援，且可在 REPL 中即時切換。

### 與 Claude Code 的定位差異

```
Claude Code         = 官方工具、僅 Anthropic 模型、閉源
cloclo              = 開源替代、13 Provider、單檔可讀
Claude Agent SDK    = 官方 SDK、每用戶一個 CLI 進程
cloclo NDJSON       = 輕量嵌入、無額外進程開銷
```

## 核心功能

### 13 個 LLM 後端

| 分類 | Provider | 代表模型 |
|------|---------|---------|
| 雲端付費 | Anthropic | claude-sonnet-4-6, claude-opus-4-6 |
| 雲端付費 | OpenAI Chat | gpt-5.4, gpt-4o, o3 |
| 雲端付費 | OpenAI Responses | gpt-5.3-codex |
| 雲端付費 | Google Gemini | gemini-2.5-flash/pro |
| 雲端付費 | DeepSeek | deepseek-chat/coder |
| 雲端付費 | Mistral | mistral-small, codestral |
| 雲端付費 | Groq | llama-3.3-70b, mixtral-8x7b |
| 本地 | Ollama | 任何已 pull 的模型 |
| 本地 | LM Studio | 本地模型 |
| 本地 | vLLM | 本地模型 |
| 本地 | Jan | 本地模型 |
| 本地 | llama.cpp | 本地模型 |

REPL 中即時切換：`/model codex` → `/model ollama/llama3.2`

### Agent 能力

- **完整 Agent Loop**：streaming + tool calling + multi-turn + sub-agent
- **內建工具**：Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, MemoryShare
- **Extended Thinking**：`--thinking 8192`
- **MCP 整合**：`--mcp-config servers.json`
- **6 種權限模式**：auto → bypassPermissions
- **Session 管理**：resume, checkpoints, rewind
- **Skills Marketplace**：45+ skills 可瀏覽安裝
- **NDJSON Bridge**：程式化嵌入，任何語言可呼叫

### 外部工具整合

支援兩種外部工具類型：

| 類型 | 用途 | 範例 |
|------|------|------|
| `cli` | 包裝 CLI 二進位 | gh, vercel, kubectl |
| `http` | 包裝 REST API | 內部微服務、Webhook |

```bash
cloclo tool install ./my-tool/   # 安裝
cloclo tool test my-tool         # 測試
```

### 架構

```
AgentLoop (streaming, tools, permissions, hooks)
  ├── AnthropicClient       → /v1/messages
  ├── OpenAIClient          → /v1/chat/completions
  ├── OpenAIResponsesClient → /v1/responses
  └── OpenAI-compat         → Gemini, DeepSeek, Mistral, Groq, local
```

每個 Provider 實作 `detect()`, `createClient()`, `resolveAuth()`, `capabilities`。AgentLoop 只讀 capabilities，不檢查 provider 名稱。

## 目前限制 / 注意事項

- **單檔 18,500 行**：可讀但不易維護，PR 合併困難
- **Stars 僅 93**：社群規模小，穩定性未經大規模驗證
- **安全分類器依賴 LLM**：28 BLOCK rules + 7 ALLOW exceptions，但準確度未知
- **OAuth 登入**：支援 Anthropic Pro/Max 和 ChatGPT Plus/Pro 訂閱直接用

## 研究價值與啟示

### 關鍵洞察

1. **「Provider-agnostic Agent Loop」的正確抽象**：AgentLoop 從不 `if (provider === "openai")`，而是透過 capabilities 合約讓 provider 自描述能力。這是多 Provider Agent 的教科書級抽象。

2. **單檔架構的取捨**：18,500 行單檔讓安裝和部署極簡（`npx cloclo`），但犧牲了可維護性。適合原型期，不適合大型團隊。

3. **NDJSON Bridge 是最被低估的功能**：允許任何語言透過 stdin/stdout 與 Agent 互動，不需要啟動完整 CLI 進程。這比官方 Claude Agent SDK 的「每用戶一個 CLI 進程」輕量得多。

4. **Skills Marketplace 的野心**：45+ skills + `/marketplace` 命令，試圖建立生態系統。但 93 stars 的社群規模難以支撐。

### 與其他專案的關聯

- **Claude Code**：cloclo 試圖成為其開源替代品，功能覆蓋相當完整
- **Learn Claude Code**（`docs/learn-claude-code.md`）：learn-claude-code 教你理解原理，cloclo 給你一個可用的實作
- **Everything Claude Code**（`docs/everything-claude-code.md`）：everything-claude-code 是 Claude Code 的擴展，cloclo 是獨立替代品
