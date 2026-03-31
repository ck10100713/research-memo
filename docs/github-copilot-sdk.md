---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-github"
oneliner: "GitHub 官方 Agent SDK — 把 Copilot CLI 的 Agent 引擎以 JSON-RPC 暴露為可嵌入的多語言函式庫"
---

# GitHub Copilot SDK 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub 儲存庫 | [github.com/github/copilot-sdk](https://github.com/github/copilot-sdk) |
| InfoQ 報導 | [infoq.com/news/2026/02/github-copilot-sdk](https://www.infoq.com/news/2026/02/github-copilot-sdk/) |
| .NET 開發者指南 | [devleader.ca](https://www.devleader.ca/2026/02/26/github-copilot-sdk-for-net-complete-developer-guide) |
| GitHub Changelog | [github.blog/changelog/2026-01-14](https://github.blog/changelog/2026-01-14-copilot-sdk-in-technical-preview/) |
| GitHub Docs | [docs.github.com/en/copilot](https://docs.github.com/en/copilot) |
| 發布公告 | [github.blog](https://github.blog/news-insights/company-news/build-an-agent-into-any-app-with-the-github-copilot-sdk/) |

## 專案概述

GitHub Copilot SDK 於 2026 年 1 月進入 **Technical Preview**，是 GitHub 官方提供的函式庫，將 Copilot CLI 背後的 Agent 引擎（Planner、Tool Loop、Runtime）以 JSON-RPC 協議暴露出來，讓開發者可以在自己的應用程式中嵌入 Copilot 的 agentic 工作流。

與 Claude Agent SDK 和 OpenAI Agents SDK 最大的差異是：**Copilot SDK 不是獨立的 Agent 框架，而是 Copilot CLI 的程式化介面**——SDK 客戶端透過 JSON-RPC 與本地執行的 Copilot CLI（server mode）溝通，CLI 才是真正的 Agent Runtime。

## 核心架構

```
┌─────────────────┐
│  Your Application│
│  (TS/Python/Go/ │
│   .NET/Java)    │
└────────┬────────┘
         │ JSON-RPC (stdio / TCP)
         ▼
┌─────────────────┐
│  Copilot CLI    │
│  (Server Mode)  │
│  ┌───────────┐  │
│  │  Planner  │  │
│  │ Tool Loop │  │
│  │  Runtime  │  │
│  └───────────┘  │
└────────┬────────┘
         │
┌────────▼────────┐
│   AI Models     │
│ (GPT/Claude/...) │
└─────────────────┘
```

SDK 自動管理 CLI 的生命週期（`auto_start`、`auto_restart`），也支援連接外部 CLI server。

## 安裝

| 語言 | 安裝指令 | 狀態 |
|------|---------|------|
| TypeScript/Node.js | `npm install @github/copilot-sdk` | 官方 |
| Python | `pip install github-copilot-sdk` | 官方 |
| Go | `go get github.com/github/copilot-sdk/go` | 官方 |
| .NET | `dotnet add package GitHub.Copilot.SDK` | 官方 |
| Java | `com.github:copilot-sdk-java` (Maven) | 官方 |
| Rust / C++ | 社群維護 | 非官方 |

**前置條件**：必須先安裝 Copilot CLI。

## 認證方式

| 方式 | 說明 |
|------|------|
| GitHub 登入使用者 | 使用已儲存的 OAuth 憑證（`use_logged_in_user=True`） |
| OAuth GitHub App Token | 適合 CI/CD 和伺服器端 |
| 環境變數 | `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN` |
| BYOK (自帶金鑰) | 支援 OpenAI、Azure AI Foundry、Anthropic API keys |

**計費**：需要 GitHub Copilot 訂閱（除非用 BYOK），每次 prompt 計入 premium request quota。

**BYOK 限制**：不支援 Microsoft Entra ID、Managed Identities、第三方 Identity Provider。

## 核心功能

### 內建工具

預設啟用等同 `--allow-all` 的所有一方工具：

- 檔案系統操作（讀/寫/搜尋）
- Git 操作
- Web 請求
- 程式碼編輯

### CopilotClient 設定

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `cli_path` | CLI 執行檔路徑 | `"copilot"` |
| `cli_url` | 連接現有伺服器 | `None` |
| `port` | TCP 模式端口 | `None` |
| `use_stdio` | 使用 stdio 傳輸 | `True` |
| `auto_start` | 自動啟動伺服器 | `True` |
| `auto_restart` | 崩潰時自動重啟 | `True` |
| `github_token` | GitHub 認證 Token | `None` |

### Session 設定

| 參數 | 說明 |
|------|------|
| `model` | 模型識別碼（BYOK 時必填） |
| `reasoning_effort` | 推理模型的努力程度 |
| `streaming` | 啟用串流回應 |
| `tools` | 自訂工具列表 |
| `system_message` | 自訂系統提示 |
| `hooks` | 生命週期事件處理器 |
| `provider` | 自訂 API Provider 設定 |
| `on_user_input_request` | Agent 請求輸入時的處理器 |

### 事件類型

| 事件 | 說明 |
|------|------|
| `assistant.message` | 完整訊息回應 |
| `assistant.message_delta` | 串流訊息片段 |
| `assistant.reasoning_delta` | 推理過程片段 |
| `session.idle` | Session 閒置，可發送下一個請求 |

### 基本使用範例

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({ model: "gpt-5" });
await session.send({ prompt: "Hello, world!" });
```

### 自訂擴充

- 自訂 Agent、Skills、Tools
- MCP Server 整合
- 多模型支援（所有 Copilot CLI 支援的模型）

## 與 Microsoft Agent Framework 的整合

Copilot SDK 可與 Microsoft Agent Framework 結合，提供：

- 一致的 Agent 抽象層，可切換或組合不同 provider
- 多 Agent 工作流支援，內建 orchestrator
- 不需重構程式碼即可替換底層模型

## 社群使用案例

| 案例 | 說明 |
|------|------|
| YouTube 章節產生器 | 自動分析影片產生時間軸章節 |
| 自訂圖形介面 | 為 Copilot 打造客製化 GUI |
| 內容摘要工具 | 大量文件自動摘要 |
| 企業內部 Agent | 串接內部系統的自動化 Agent |
| 多 Agent 工作流 | 序列管線 + 編排器模式 |

## Cookbook 範例

| 範例 | 說明 | 難度 |
|------|------|------|
| Basic Chat | 基本對話 | 入門 |
| Streaming | 串流回應 | 入門 |
| Custom Tool | 自訂工具（Pydantic） | 基礎 |
| BYOK Ollama | 本地模型 / 自訂 Provider | 基礎 |
| Image Attachment | 圖片附件與視覺分析 | 基礎 |
| Hooks & Permissions | 生命週期事件與權限控制 | 進階 |
| User Input Handler | 使用者輸入處理 | 進階 |
| Multi Session | 多 Session 管理與 Session 池 | 進階 |

## 目前限制 / 注意事項

- **Technical Preview 狀態**：API 可能有破壞性變更，不建議用於生產環境
- **依賴 Copilot CLI**：SDK 不是獨立執行的，必須有 CLI 作為 server
- **BYOK 限制**：不支援 Microsoft Entra ID、Managed Identities
- **需要訂閱**：非 BYOK 模式需要 GitHub Copilot 付費訂閱
- **五語言維護成本**：同時支援 5 種語言可能導致功能差距

## 研究價值與啟示

### 關鍵洞察

1. **「CLI as Server」架構是獨特設計**——Claude Agent SDK 和 OpenAI Agents SDK 都是獨立函式庫，但 Copilot SDK 選擇讓 CLI 作為 JSON-RPC server，SDK 只是 client wrapper。好處是 SDK 天生跟 CLI 功能同步（不需要分別維護兩套工具實作），壞處是部署時多了一個程序依賴。

2. **五語言支援（TS/Python/Go/.NET/Java）是最廣的覆蓋面**——Claude Agent SDK 僅 2 語言、OpenAI Agents SDK 僅 2 語言、Google ADK 4 語言。Copilot SDK 的 5 語言支援反映了 GitHub/Microsoft 在企業市場的野心——.NET 和 Java 開發者是最大的企業開發者群體。

3. **BYOK 模式解耦了訂閱依賴**——允許使用者自帶 API key（OpenAI / Azure / Anthropic），不一定要有 Copilot 訂閱。這讓 SDK 可以在沒有 GitHub Copilot 訂閱的環境中使用，降低採用門檻。

4. **與 Microsoft Agent Framework 的深度整合**——這不只是 GitHub 的產品，而是 Microsoft AI 平台戰略的一環。SDK 可以無縫接入 Microsoft 的 Agent 抽象層，在企業場景（Azure、Teams、Office）中具有生態優勢。

5. **Technical Preview 代表尚早，但方向明確**——相比 Claude Agent SDK（0.1.x/0.2.x）和 OpenAI Agents SDK（0.13.x），Copilot SDK 連正式版號都還沒有。但 JSON-RPC 架構意味著功能更新主要在 CLI 端，SDK 端相對穩定。

### 與其他專案的關聯

- **vs [Claude Agent SDK](claude-agent-sdk.md)**：Claude = 內建 8 工具 + 獨立執行；Copilot = CLI 代理 + JSON-RPC。Claude 更適合獨立 coding agent，Copilot 更適合嵌入現有應用
- **vs [OpenAI Agents SDK](openai-agents-sdk.md)**：OpenAI = Handoffs + Guardrails 多代理框架；Copilot = CLI 引擎的程式化包裝。OpenAI 更通用，Copilot 更偏向 GitHub 生態
- **vs [GitHub Copilot CLI](copilot-cli.md)**：SDK 是 CLI 的程式化版本，共用同一個 Agent Runtime
- **vs [GitHub Copilot Configs](github-copilot-configs.md)**：Configs 用於配置 CLI 行為，SDK 用於程式化呼叫
- **vs [Google ADK](google-adk.md)**：ADK = 工作流 Agent + 共享 state；Copilot = CLI 代理。ADK 在多代理編排上更豐富，Copilot 在生態整合上更強
