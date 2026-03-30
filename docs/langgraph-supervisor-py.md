---
date: "2026-03-30"
category: "AI Agent 框架"
card_icon: "material-account-supervisor"
oneliner: "LangGraph 官方 Supervisor 多 Agent 庫——中央調度器模式，支援多層階層與訊息歷史控制（1.5K stars）"
---
# LangGraph Supervisor 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [langchain-ai/langgraph-supervisor-py](https://github.com/langchain-ai/langgraph-supervisor-py) |
| Medium 對比文 | [LangGraph SWARM vs SUPERVISOR](https://medium.com/@sameernasirshaikh/langgraph-swarm-vs-langgraph-supervisor-ce8194837d0a) |
| LangChain 官方基準 | [Benchmarking Multi-Agent Architectures](https://blog.langchain.com/benchmarking-multi-agent-architectures/) |

## 專案概述

| 項目 | 數值 |
|------|------|
| Stars | 1,532 |
| Forks | 234 |
| Language | Python |
| License | MIT |
| 最近 commit | 2026-03-02 |

LangGraph Supervisor 是 LangChain 官方的**階層式多 Agent 協調庫**。核心概念：一個 Supervisor agent 扮演中央調度器，接收使用者輸入後決定把任務委派給哪個專家 agent，收集結果後再回覆或繼續委派。

> **官方提醒**：LangChain 現在推薦直接用 tool-calling 實作 supervisor 模式，而非依賴此庫。此庫主要用於升級既有程式碼到 LangChain 1.0。

## 核心架構

```
User → Supervisor → [research_agent | math_agent | ...] → Supervisor → User
              ↑                                              │
              └──────────────── 多輪委派 ────────────────────┘
```

### 關鍵 API

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt="You are a team supervisor..."
)
app = workflow.compile(checkpointer=checkpointer)
```

### 訊息歷史控制

| 模式 | 說明 |
|------|------|
| `full_history` | 保留 agent 的完整對話歷史 |
| `last_message` | 只保留 agent 的最終回應 |

### 多層階層

```python
research_team = create_supervisor([...]).compile(name="research_team")
writing_team = create_supervisor([...]).compile(name="writing_team")
top_level = create_supervisor([research_team, writing_team]).compile()
```

## 目前限制與注意事項

1. **官方已半棄用** — README 明確建議改用 tool-calling 手動實作
2. **額外延遲** — 每次委派都經過 supervisor 翻譯，token 用量比 swarm 高 ~40%
3. **中央瓶頸** — 所有通訊必經 supervisor，不支援 agent 間直接對話

## 研究價值與啟示

### 關鍵洞察

1. **Supervisor 模式是多 Agent 的「安全預設」** — 對 sub-agent 的假設最少，任何場景都能用，但效率較低。適合原型階段或需要嚴格控制的場景。
2. **官方推動從「庫」到「模式」的轉變** — LangChain 鼓勵用 tool-calling 手寫 supervisor，而非依賴封裝庫。這反映了 AI 框架從「黑盒」走向「透明模式」的趨勢。

### 與其他專案的關聯

- **vs. [LangGraph Swarm](langgraph-swarm-py.md)** — Supervisor 是中央集權，Swarm 是去中心化。Supervisor 更安全但更慢，Swarm 更快但需要每個 agent 知道所有其他 agent。
- **vs. [LangGraph Multi-Agent](langgraph-multi-agent.md)** — Multi-Agent 是用 Supervisor 模式實作的教學範例。
- **vs. [Open SWE](open-swe.md)** — Open SWE 用 Deep Agents 做子 agent 編排，概念上和 Supervisor 的多層階層類似。
