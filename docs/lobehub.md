---
date: ""
category: "AI Agent 框架"
icon: "material-hub"
oneliner: "74K stars 的 AI Agent 協作平台，Supervisor + Executor 多 Agent 架構、39K+ MCP 市集、White-Box Memory"
---
# LobeHub 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [github.com/lobehub/lobehub](https://github.com/lobehub/lobehub) |
| 官方網站 | [lobehub.com](https://lobehub.com/) |
| 架構文件 | [Architecture Design](https://lobehub.com/docs/development/basic/architecture) |
| AI Agent 系統分析 | [DeepWiki — AI Agent System](https://deepwiki.com/lobehub/lobehub/3-ai-agent-system) |
| AWS 案例研究 | [AWS + LobeHub Multi-Agent Collaboration](https://aws.amazon.com/solutions/case-studies/lobehub/) |
| 技術深度分析 | [The Engineer's Guide to LobeHub](https://typevar.dev/articles/lobehub/lobehub) |
| Product Hunt | [LobeHub on Product Hunt](https://www.producthunt.com/products/lobehub) |

## 專案概述

LobeHub（前身 LobeChat）是一個開源的 **AI Agent 協作平台**，定位為「人與 Agent 共同演化的網路」。74.3K GitHub stars，TypeScript 建構，由 LobeChat（單人聊天介面）進化為多 Agent 協作工作空間。

核心轉變：從「一次性對話工具」→「**Agent 作為工作單元**」。Agent 不再是用完即丟的 chatbot，而是有持久身份、記憶、技能、能彼此協作的「隊友」。

LobeHub 目前在 Google、ByteDance、AWS、Alibaba Cloud 等公司被工程師和團隊使用。

| 指標 | 數值 |
|------|------|
| GitHub Stars | 74.3K |
| Forks | 14.8K |
| 語言 | TypeScript |
| 預設分支 | canary |
| License | Other (custom) |
| Skills 市集 | 217,527+ |
| MCP Server 市集 | 39,603+ |
| 支援模型供應商 | 50+ |

## 核心功能

### 三大支柱：Create → Collaborate → Evolve

```
┌─────────────────────────────────────────────────────────────┐
│                        LobeHub                              │
│                                                             │
│  ┌─────────────┐   ┌──────────────────┐   ┌────────────┐  │
│  │   CREATE     │   │   COLLABORATE    │   │   EVOLVE   │  │
│  │             │   │                  │   │            │  │
│  │ Agent       │   │ Agent Groups     │   │ Personal   │  │
│  │ Builder     │   │ Pages            │   │ Memory     │  │
│  │ 一句話建立   │   │ Schedule         │   │ 持續學習    │  │
│  │ Agent       │   │ Project          │   │ 白盒記憶    │  │
│  │             │   │ Workspace        │   │ 可編輯     │  │
│  │ 10,000+     │   │                  │   │            │  │
│  │ Skills/MCP  │   │ Supervisor +     │   │ 透明決策    │  │
│  │             │   │ Executor 模式    │   │            │  │
│  └─────────────┘   └──────────────────┘   └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Create：Agent 作為工作單元

- **Agent Builder**：一句話描述需求即可自動配置 Agent
- **統一智慧**：接入任何模型（OpenAI、Claude、DeepSeek、Gemini、本地 LLM）、任何模態
- **10,000+ Skills**：透過 MCP（Model Context Protocol）一鍵安裝外部工具
- **MCP 市集**：39,603+ 個 MCP Server，涵蓋開發工具、生產力工具、資料來源

### Collaborate：多 Agent 協作網路

| 功能 | 說明 |
|------|------|
| **Agent Groups** | 多 Agent 團隊，自動組裝適合任務的 Agent 組合 |
| **Pages** | 多 Agent 在共享 context 中協作撰寫內容 |
| **Schedule** | 排程執行，Agent 在指定時間自主工作 |
| **Project** | 專案化組織工作，結構化追蹤進度 |
| **Workspace** | 團隊共享空間，跨組織的 Agent 協作 |

### Evolve：人與 Agent 共演化

- **Personal Memory**：Agent 從你的工作方式中學習，在對的時機行動
- **White-Box Memory**：結構化、可編輯的記憶系統，使用者完全控制 Agent 記住什麼
- **透明性**：不是黑盒的「AI 記住了什麼」，而是可審計的記憶結構

## 技術架構

### Agent Runtime 雙執行模型

```
┌──────────────────────────────────────────────┐
│            Client-side (Browser)              │
│                                              │
│  • 一對一聊天                                 │
│  • Continue generation                       │
│  • Group orchestration 決策                   │
│                                              │
│      Zustand Store ──► /api/chat/stream      │
└──────────────────────┬───────────────────────┘
                       │ SSE
┌──────────────────────▼───────────────────────┐
│            Server-side (Queue/Local)          │
│                                              │
│  • Group chat supervisor agent               │
│  • Sub-agent tasks                           │
│  • API / Cron triggers                       │
│                                              │
│  AgentRuntimeService.executeStep()           │
│      │                                       │
│      ▼                                       │
│  @lobechat/agent-runtime                     │
│      │                                       │
│      ▼                                       │
│  @lobechat/model-runtime (50+ providers)     │
└──────────────────────────────────────────────┘
```

### Chat Pipeline 執行流程

```
1. User → Zustand store 提交訊息
2. Client service → POST /api/chat/stream
3. Server: ToolsEngine.generateTools() 組裝 context
4. Model runtime → 外部 AI provider (streaming)
5. SSE stream 回傳
6. fetchSSE() 解析 normalized chunks
7. Zustand 增量更新 UI (text / tool calls / reasoning tokens)
```

### 多 Agent 協作：Supervisor + Executor 模式

```
┌─────────────────────────────────────────────┐
│           Supervisor Agent Loop              │
│                                             │
│  • 維護全域狀態與軌跡                         │
│  • 將使用者目標分解為子任務                    │
│  • 路由到適當的 Worker Agent                  │
│  • 綜合結果                                  │
│                                             │
│      ┌────────┬────────┬────────┐           │
│      ▼        ▼        ▼        ▼           │
│  ┌───────┐┌───────┐┌───────┐┌───────┐      │
│  │Agent A││Agent B││Agent C││Agent D│      │
│  │(獨立  ││(獨立  ││(獨立  ││(獨立  │      │
│  │context)││context)││context)││context)│      │
│  └───────┘└───────┘└───────┘└───────┘      │
│                                             │
│  每個 Agent 的 context 空間隔離               │
│  防止記憶或假設互相污染                        │
└─────────────────────────────────────────────┘
```

**響應模式**：
- **Natural**：Agent 並行執行，同時產出
- **Sequential**：Agent 依序回應，前一個的輸出作為後一個的 context

### Tool & Skill 整合

`createAgentToolsEngine()` 聚合四類工具：

| 類別 | 內容 |
|------|------|
| **Built-in Tools (6)** | Web browsing、Knowledge-base RAG、Python interpreter、Cloud sandbox、Notebook、Memory |
| **MCP Plugins** | 10,000+ 市集工具，透過 Model Context Protocol |
| **Klavis OAuth** | 30+ 預整合服務（GitHub、Google Drive 等） |
| **LobeHub Skills** | Premium 整合 |

平台特定篩選：stdio MCP plugins 需要 Electron IPC，雲端環境會自動過濾不相容的工具。

### 資料庫 Schema

```
agents              → 系統角色、配置
chat_groups         → 團隊容器、orchestration 設定
chat_groups_agents  → 成員角色與職責
sessions            → 對話容器
topics              → trigger: cron / chat / api / eval
threads             → type: continuation / standalone / eval
messages            → role-based content
agent_eval_benchmarks → 評測基準
agent_documents     → Agent 級別知識儲存 (BM25 搜尋)
```

## 部署選項

| 方式 | 說明 | 適合場景 |
|------|------|---------|
| **Vercel** | 一鍵部署 | 快速試用、個人使用 |
| **Docker** | `docker run -d -p 3210:3210 lobehub/lobe-chat` | 自架、團隊使用 |
| **Zeabur / Sealos / 阿里雲** | 一鍵部署 | 亞太區域部署 |
| **Desktop App** | macOS 原生應用 | 無瀏覽器限制的完整體驗 |
| **LobeHub Cloud** | 官方雲端服務（免費 tier） | 零設定即用 |

資料庫支援：本地 SQLite 或遠端 PostgreSQL。

## 生態系統

```
lobehub/lobehub           ← 主專案（Agent 協作平台）
lobehub/lobe-chat         ← 前身（單人聊天介面）
lobehub/lobe-ui           ← UI 元件庫
lobehub/lobe-icons        ← AI/LLM 品牌 icon 集
lobehub/lobe-tts          ← TTS/STT 語音模組
lobehub/chat-plugin-sdk   ← Plugin 開發 SDK
lobehub/lobe-midjourney   ← Midjourney WebUI Plugin
```

## 其他亮點功能

| 功能 | 說明 |
|------|------|
| Chain of Thought | 視覺化 AI 推理過程，逐步展示問題拆解 |
| Branching Conversations | 對話可分岔（Continuation 或 Standalone 模式） |
| Artifacts | 即時建立 SVG、HTML、文件（類似 Claude Artifacts） |
| Knowledge Base | 上傳文件建立知識庫，支援 RAG 對話 |
| 語音對話 | TTS + STT 完整語音互動 |
| Text to Image | 文字生圖整合 |
| Agent Market | GPTs 風格的 Agent 市集 |
| 多用戶管理 | 支援 SSO、權限控制 |
| PWA | Progressive Web App，行動裝置適配 |
| 自訂主題 | 深色/淺色模式 + 自訂配色 |

## 目前限制 / 注意事項

1. **License 模糊** — GitHub 標示 "Other"（非標準開源 License），商業使用前需仔細確認條款
2. **canary 為預設分支** — 代表開發節奏快但穩定性可能有取捨，生產環境應注意版本鎖定
3. **Client-side 殘留架構** — 雖然已遷移到 server-side agent runtime，部分功能仍在 client-side 執行，混合執行模型增加除錯複雜度
4. **Agent 評測仍在早期** — 有 `agent_eval_benchmarks` 和 `eval-rubric` 模組，但生態系統中的評測工具尚不成熟
5. **MCP 市集品質參差** — 39,603+ 個 MCP Server 數量龐大，但缺乏嚴格的品質審查和安全審計機制
6. **成本不透明** — 雲端版免費 tier 限制、Premium Skills 定價在文件中不夠明確
7. **依賴外部模型供應商** — 平台本身不提供推理能力，完全依賴 50+ 外部 provider 的 API 可用性與定價

## 研究價值與啟示

### 關鍵洞察

1. **「Agent 作為工作單元」是下一代 AI 產品的核心範式** — LobeHub 把 Agent 從「對話的另一端」提升為「團隊成員」，有持久身份、記憶、專長。這不只是 UX 包裝，而是架構層面的根本轉變 — Agent 有自己的 DB record（`agents` 表）、可被分配到 Group（`chat_groups_agents`）、有觸發機制（cron/api/eval）。這個範式在軟體開發工具、企業知識管理、教育等領域都有巨大遷移潛力。

2. **Supervisor + Executor 模式是多 Agent 協作的事實標準** — LobeHub 的雙 Runtime（agent loop + supervisor loop）與 context 隔離原則，與 LangGraph 的 State channel 隔離、Anthropic Harness 的 Planner-Generator-Evaluator 三角異曲同工。不同框架殊途同歸，說明「中央協調 + 獨立執行 + 隔離 context」是多 Agent 系統的基本架構共識。

3. **White-Box Memory 是 Agent 可信度的關鍵** — 大多數 Agent 平台的記憶是黑盒（你不知道 Agent 記住了什麼），LobeHub 選擇結構化、可編輯的白盒記憶。這在企業場景中至關重要 — 合規要求可審計性，使用者信任要求透明性。Claude Code 的 `MEMORY.md` 也是同樣理念的不同實現。

4. **MCP 成為 Agent 工具生態的 HTTP** — 10,000+ Skills + 39,603+ MCP Servers 的規模說明 Model Context Protocol 正在成為 Agent 與外部世界互動的事實標準。就像 HTTP 統一了 web 通訊，MCP 正在統一 Agent-to-Tool 的介面。LobeHub 押注 MCP 是正確的戰略選擇。

5. **從 LobeChat 到 LobeHub 的演化路徑值得研究** — 單人對話工具 → 多 Agent 協作平台 → 企業級工作空間，這個產品演化路徑與 AWS 案例研究中 client-side → server-side 的架構遷移相呼應。每一步都是因為前一步的架構假設被打破（client-side 無法支撐多 Agent 並行、單人對話無法表達團隊協作需求）。

### 與其他專案的關聯

- **Anthropic Harness Design**（`harness-design-long-running-apps.md`）：LobeHub 的 description 直接使用 "agent harness" 一詞，其 Supervisor + Executor 模式與 Anthropic 的 Planner-Generator-Evaluator 三角互為對照。LobeHub 是通用平台，Anthropic Harness 是特定工作流，但架構思想一致。
- **LangGraph State API**（`langgraph-state-api.md`）：LobeHub 的 Agent Groups 中 context 隔離原則，類似 LangGraph 的多 Schema 模式（input/output/private state）。兩者都在解決同一問題：多 Agent 之間如何分享必要資訊同時防止狀態污染。
- **CrewAI**（`crewai.md`）：CrewAI 和 LobeHub 都實現了多 Agent 角色扮演協作，但 CrewAI 是框架（給開發者寫 code），LobeHub 是平台（給使用者拖拉設定）。CrewAI 更靈活，LobeHub 更易用。
- **Everything Claude Code**（`everything-claude-code.md`）：LobeHub 的 Skills 市集概念與 Claude Code 的 skills 系統類似，都是將 Agent 能力模組化。但 LobeHub 走的是平台市集路線（39K+ MCP servers），Claude Code 走的是本地 skill 檔案路線。
