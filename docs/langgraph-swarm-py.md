---
date: "2026-03-30"
category: "AI Agent 框架"
card_icon: "material-swap-horizontal-circle"
oneliner: "LangGraph 官方 Swarm 多 Agent 庫——去中心化 handoff 模式，agent 間直接交接，延遲低 40%（1.4K stars）"
---
# LangGraph Swarm 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [langchain-ai/langgraph-swarm-py](https://github.com/langchain-ai/langgraph-swarm-py) |
| DEV Community 教學 | [Building Multi-Agent Systems with LangGraph Swarm](https://dev.to/sreeni5018/building-multi-agent-systems-with-langgraph-swarm-a-new-approach-to-agent-collaboration-15kj) |
| 架構對比 | [Agent Swarm vs Anthropic Workflows vs LangGraph](https://softmaxdata.com/blog/agent-architectures-compared/) |
| LangChain 基準測試 | [Benchmarking Multi-Agent Architectures](https://blog.langchain.com/benchmarking-multi-agent-architectures/) |

## 專案概述

| 項目 | 數值 |
|------|------|
| Stars | 1,449 |
| Forks | 201 |
| Language | Python |
| License | MIT |
| 最近 commit | 2026-03-28 |

LangGraph Swarm 是 LangChain 官方的**去中心化多 Agent 協調庫**。受 OpenAI Swarm 概念啟發，核心機制是 agent 之間透過 handoff tool 直接交接控制權，沒有中央調度器。系統記住最後活躍的 agent，後續對話自動繼續。

## 核心架構

```
User → Alice ──handoff──→ Bob ──handoff──→ Alice → User
         │                  │
         └──── 直接交接，無需經過中央調度器 ────┘
```

### 關鍵 API

```python
from langgraph_swarm import create_handoff_tool, create_swarm

alice = create_agent(model, tools=[
    add,
    create_handoff_tool(agent_name="Bob", description="Transfer to Bob"),
], name="Alice")

bob = create_agent(model, tools=[
    create_handoff_tool(agent_name="Alice", description="Transfer to Alice"),
], name="Bob")

workflow = create_swarm([alice, bob], default_active_agent="Alice")
app = workflow.compile(checkpointer=checkpointer)
```

### Swarm vs Supervisor 效能對比

| 指標 | Swarm | Supervisor |
|------|-------|-----------|
| 端到端延遲 | **基準** | +40% |
| LLM 呼叫次數 | **較少** | 較多（supervisor 翻譯） |
| Token 用量 | **較少** | 較多 |
| Agent 間知識要求 | 每個 agent 需知道所有其他 agent | 只需知道 supervisor |
| 適用場景 | 動態、跨領域對話 | 結構化、可預測流程 |

### 自訂 Handoff Tool

可以自訂 handoff 行為：帶任務描述、篩選傳遞的訊息、使用不同的 state key：

```python
def create_custom_handoff_tool(*, agent_name, name, description):
    @tool(name, description=description)
    def handoff_to_agent(
        task_description: Annotated[str, "Detailed description for next agent"],
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        return Command(goto=agent_name, graph=Command.PARENT, update={...})
    return handoff_to_agent
```

## 目前限制與注意事項

1. **Agent 需互相知道** — 每個 agent 要有其他所有 agent 的 handoff tool，不適合第三方 agent
2. **共享訊息歷史** — 預設所有 agent 共用同一個 `messages` 列表，內部對話會暴露
3. **無內建路由邏輯** — 路由完全靠 LLM 判斷，沒有確定性的 fallback

## 研究價值與啟示

### 關鍵洞察

1. **Swarm 是「對話型」多 Agent 的最佳架構** — 當使用者可能在對話中動態切換需求（從數學問到翻譯再問天氣），swarm 的直接 handoff 比 supervisor 的中央路由更自然、更快。
2. **Handoff Tool 是關鍵抽象** — `create_handoff_tool` 把 agent 間的控制轉移封裝成一個普通的 tool call，讓 LLM 用自然語言決定「該交給誰」。這比硬編碼路由圖優雅得多。
3. **共享 vs 隔離訊息是核心取捨** — 預設共享所有訊息讓 handoff 簡單，但隱私和 context 膨脹是代價。自訂 state schema 可以解決但增加複雜度。

### 與其他專案的關聯

- **vs. [LangGraph Supervisor](langgraph-supervisor-py.md)** — 互補的兩種多 Agent 模式：Supervisor 中央集權，Swarm 去中心化。Swarm 快 40% 但要求更多 agent 間知識。
- **vs. [LangGraph Multi-Agent](langgraph-multi-agent.md)** — Multi-Agent 用 Supervisor 模式，可以改用 Swarm 模式重構以降低延遲。
- **vs. [Open SWE](open-swe.md)** — Open SWE 的 subagent spawning 本質上也是 handoff，但更像 task delegation 而非 conversation handoff。
- **vs. [CrewAI](crewai.md)** — CrewAI 也是多 agent 協作，但用 role-based 抽象而非 tool-based handoff。
