---
date: "2026-03-31"
category: "AI Agent 框架"
card_icon: "material-google"
oneliner: "Google 官方 Agent 框架 — 以 LlmAgent + Workflow Agents 為核心的 code-first 多代理開發套件"
---

# Google Agent Development Kit (ADK) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方文件 | [google.github.io/adk-docs](https://google.github.io/adk-docs/) |
| Python SDK GitHub | [github.com/google/adk-python](https://github.com/google/adk-python) |
| 範例集 | [github.com/google/adk-samples](https://github.com/google/adk-samples) |
| Google Cloud 文件 | [cloud.google.com/agent-builder/agent-development-kit](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) |
| Multi-Agent 模式指南 | [developers.googleblog.com](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) |
| LlmAgent 文件 | [adk-docs/agents/llm-agents](https://google.github.io/adk-docs/agents/llm-agents/) |
| LY Corp 技術部落格 | [techblog.lycorp.co.jp/zh-hant/adk-1-agent](https://techblog.lycorp.co.jp/zh-hant/adk-1-agent) |
| Quickstart | [adk-docs/get-started/quickstart](https://google.github.io/adk-docs/get-started/quickstart/) |

## 專案概述

Google Agent Development Kit（ADK）是 Google 的開源 Agent 開發框架，設計目標是**讓 Agent 開發感覺像軟體開發**。雖然為 Gemini 和 Google 生態系優化，但保持模型無關（model-agnostic）和部署無關（deployment-agnostic），也支援 Claude、Ollama、vLLM 等模型。

與其他 Agent SDK 相比，ADK 的獨特之處在於同時提供了**兩類 Agent**：

- **LlmAgent**：LLM 驅動的動態推理 Agent（非確定性）
- **Workflow Agents**：確定性的工作流編排（Sequential、Parallel、Loop）

這種雙軌設計讓開發者可以在同一框架內混合使用「AI 自主決策」和「程式化控制流」。

**GitHub 社群數據**：18.7k stars、2,394+ commits、Apache 2.0 License

## 核心架構

```
┌──────────────────────────────────────────────────┐
│              ADK Runtime                          │
│                                                    │
│  ┌──────────────┐     ┌──────────────────────┐    │
│  │   LlmAgent   │     │   Workflow Agents    │    │
│  │  (動態推理)   │     │  (確定性控制流)       │    │
│  │              │     │                      │    │
│  │ ● instructions│     │ ● SequentialAgent    │    │
│  │ ● tools      │     │ ● ParallelAgent      │    │
│  │ ● sub_agents │     │ ● LoopAgent          │    │
│  │ ● output_key │     │                      │    │
│  └──────┬───────┘     └──────────┬───────────┘    │
│         │                        │                 │
│         └────────┬───────────────┘                 │
│                  ▼                                  │
│         ┌──────────────┐                           │
│         │ Shared State │ ← session.state           │
│         │ (白板模式)    │                           │
│         └──────────────┘                           │
│                                                    │
│  Tools: google_search | code_exec | MCP | custom   │
│  Deploy: Local | Cloud Run | Vertex AI Agent Engine│
└──────────────────────────────────────────────────┘
```

## 安裝

| 語言 | 安裝指令 | 狀態 |
|------|---------|------|
| Python | `pip install google-adk` | 穩定版，雙週發布 |
| TypeScript | `npm install @google/adk` | 穩定 |
| Go | `go get google.golang.org/adk` | v1.0.0 |
| Java | Maven/Gradle（v1.0.0） | v1.0.0 |

支援模型：Gemini、Claude、Vertex AI Hosted、Ollama、vLLM、LiteLLM 等。

## 兩類 Agent

### LlmAgent（動態推理）

核心 Agent 類型，使用 LLM 進行推理、決策、工具呼叫：

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Answer user questions using search.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

**關鍵參數：**

| 參數 | 說明 |
|------|------|
| `name` | 唯一識別名，多代理系統中必須 |
| `model` | LLM 模型 ID（如 `gemini-2.5-flash`） |
| `instruction` | 系統提示詞，支援 `{var}` 動態值 |
| `description` | 能力描述，用於其他 Agent 路由決策 |
| `tools` | 工具清單（function、BaseTool、AgentTool） |
| `sub_agents` | 子 Agent 清單，形成階層結構 |
| `output_key` | 將最終回覆寫入 session.state 的指定 key |
| `input_schema` / `output_schema` | Pydantic BaseModel 定義輸入/輸出結構 |
| `include_contents` | `'default'` 或 `'none'`（無狀態模式） |
| `planner` | `BuiltInPlanner` 或 `PlanReActPlanner` |
| `code_executor` | 內建程式碼執行器 |

### Workflow Agents（確定性控制流）

| Agent 類型 | 功能 | 典型場景 |
|-----------|------|---------|
| `SequentialAgent` | 依序執行多個子 Agent | PDF 解析 → 擷取 → 摘要 |
| `ParallelAgent` | 平行執行多個子 Agent | 同時搜尋多個來源 |
| `LoopAgent` | 迴圈執行直到條件滿足 | Generator-Critic 迭代改進 |

## 8 大多代理模式

| # | 模式 | 使用的 Agent | 關鍵機制 |
|---|------|-------------|---------|
| 1 | Sequential Pipeline | `SequentialAgent` | `output_key` 寫入共享 state |
| 2 | Coordinator/Dispatcher | `LlmAgent` + `sub_agents` | AutoFlow 根據 description 路由 |
| 3 | Parallel Fan-Out/Gather | `ParallelAgent` + 合成器 | 各 Agent 寫入不同 state key |
| 4 | Hierarchical Decomposition | `LlmAgent` + `AgentTool` | 子 Agent 包裝為可呼叫工具 |
| 5 | Generator-Critic | `LoopAgent` | 迴圈直到 Critic 通過 |
| 6 | Iterative Refinement | `LoopAgent` | `escalate=True` 中斷迴圈 |
| 7 | Human-in-the-Loop | 任意 Agent + 審核工具 | 自訂工具暫停等待人類審核 |
| 8 | Composite | 混合上述模式 | 實際應用通常組合多種模式 |

## 工具系統

| 類型 | 說明 |
|------|------|
| Python Function | 任何 Python function 自動包裝為 `FunctionTool` |
| Pre-built Tools | `google_search`、`code_execution` 等 |
| MCP Tools | 透過 Model Context Protocol 連接外部系統 |
| OpenAPI Tools | 從 OpenAPI spec 自動生成工具 |
| AgentTool | 將其他 Agent 包裝為工具 |
| Tool Confirmation (HITL) | 人類審核確認後才執行工具 |

## Session 與共享狀態

```python
# Agent A 寫入 state
agent_a = LlmAgent(
    name="parser",
    output_key="parsed_data",  # → session.state["parsed_data"]
    ...
)

# Agent B 讀取 state
agent_b = LlmAgent(
    name="summarizer",
    instruction="Summarize the following: {parsed_data}",  # 從 state 讀取
    ...
)
```

**共享狀態 = 共用白板**：所有 Agent 透過 `session.state` 讀寫，每個 Agent 用不同的 `output_key` 避免衝突。

## 開發與部署

### 開發工具

```bash
adk web              # 瀏覽器 UI（含事件檢視、追蹤）
adk run <agent>      # 終端介面
adk api_server       # API 伺服器
adk eval <agent> <test.json>  # 評估框架
```

### 部署選項

| 目標 | 說明 |
|------|------|
| Local | 本地開發和測試 |
| Cloud Run | Docker 容器化部署 |
| Vertex AI Agent Engine | Google 託管的全管理服務 |
| A2A Protocol | Agent-to-Agent 遠端通訊協議 |

## 快速開始範例

```python
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Get weather for a city."""
    weather_data = {"New York": "sunny, 25°C", "London": "cloudy, 15°C"}
    return {"weather": weather_data.get(city, f"No data for {city}")}

def get_current_time(city: str) -> dict:
    """Get current time for a city."""
    import datetime
    return {"time": datetime.datetime.now().strftime("%H:%M")}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-flash",
    description="Agent that answers weather and time questions.",
    instruction="You are a helpful agent who can answer questions about weather and time.",
    tools=[get_weather, get_current_time],
)
```

```bash
adk run weather_time_agent
```

## 多代理範例

```python
from google.adk.agents import LlmAgent, SequentialAgent

parser = LlmAgent(
    name="parser",
    model="gemini-2.5-flash",
    instruction="Parse the user input and extract key entities.",
    output_key="parsed_entities",
)

enricher = LlmAgent(
    name="enricher",
    model="gemini-2.5-flash",
    instruction="Enrich the following entities with details: {parsed_entities}",
    output_key="enriched_data",
)

pipeline = SequentialAgent(
    name="processing_pipeline",
    sub_agents=[parser, enricher],
)
```

## 目前限制 / 注意事項

- **Gemini 優先**：雖聲稱 model-agnostic，但 `output_schema` + `tools` 組合需要 Gemini 3.0 等特定模型支援
- **LiteLLM 安全警告**：LiteLLM 1.82.7-1.82.8 版本被植入未授權程式碼，需立即更新並輪換憑證
- **ParallelAgent 競態風險**：共享 `session.state` 在平行執行時需手動確保每個 Agent 寫入不同 key
- **無內建 coding 工具**：不像 Claude Agent SDK 內建 Read/Edit/Bash，ADK 的 coding 能力需要自行用 `code_executor` 或自訂工具實現
- **Session Rewind 為新功能**：可回溯 session 狀態到特定時間點，但尚在早期階段

## 研究價值與啟示

### 關鍵洞察

1. **「LlmAgent + Workflow Agents」的雙軌設計是最大亮點**——其他框架通常只提供 LLM-driven Agent（OpenAI、Claude）或只提供 DAG 控制流（Airflow、Prefect）。ADK 在同一框架內結合兩者，讓開發者可以用 `SequentialAgent` 確保關鍵步驟按序執行，同時讓 `LlmAgent` 在每個步驟內自主推理。

2. **`output_key` + `session.state` 的「白板模式」是簡單但有效的 Agent 間通訊**——不需要複雜的 message passing 或 event bus，所有 Agent 共用一個 state dict，透過 key naming convention 避免衝突。比 OpenAI 的 Handoffs 更簡單，比 LangGraph 的 State API 更直覺。

3. **8 大多代理模式形成了實用的 design pattern catalog**——Sequential Pipeline、Coordinator/Dispatcher、Generator-Critic 等模式不只適用於 ADK，是通用的 multi-agent 設計參考。Google 把這些模式文件化並附上具體實作，降低了多代理系統的設計門檻。

4. **A2A Protocol 代表 Google 的跨服務 Agent 互操作願景**——除了本地的 `sub_agents` 階層，ADK 還支援 Agent-to-Agent 遠端通訊。這意味著不同團隊可以獨立開發和部署 Agent，再透過 A2A 組合成更大系統，是真正的微服務式 Agent 架構。

5. **四語言支援（Python/TS/Go/Java）+ Vertex AI 部署是企業級定位**——Go 和 Java 的 v1.0.0 release 表明 Google 認真對待後端和企業市場，不只是 Python 開發者的玩具。

### 與其他專案的關聯

- **vs [Claude Agent SDK](claude-agent-sdk.md)**：Claude = 內建 coding 工具 + Hooks 生命週期；ADK = 工作流 Agent + 共享 state。Claude 更適合 coding agent，ADK 更適合複雜多步驟工作流
- **vs [OpenAI Agents SDK](openai-agents-sdk.md)**：OpenAI = Handoffs 線性委派；ADK = SequentialAgent/ParallelAgent 結構化編排。ADK 在多代理模式上更豐富
- **vs [LangGraph](langgraph-multi-agent.md)**：兩者都用圖/流程定義工作流，但 LangGraph 更偏向圖理論（nodes + edges + state），ADK 更偏向 Agent 階層（parent + sub_agents）
- **vs [CrewAI](crewai.md)**：CrewAI = Role/Goal/Backstory 角色扮演；ADK = code-first 工具組合。ADK 的工程化程度更高，CrewAI 的上手門檻更低
