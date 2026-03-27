# LangGraph State API 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方文件 — Graph API | [docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api#state) |
| 官方文件 — Use Graph API | [docs.langchain.com/oss/python/langgraph/use-graph-api](https://docs.langchain.com/oss/python/langgraph/use-graph-api) |
| StateGraph API Reference | [reference.langchain.com](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) |
| LangGraph Notes: State Management | [Medium — Ömer Yalçın](https://medium.com/@omeryalcin48/langgraph-notes-state-management-62ea5b5a5cdd) |
| Mastering LangGraph State Management in 2025 | [sparkco.ai](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025) |
| Optimizing Custom State Reducers | [azguards.com](https://azguards.com/ai-engineering/the-memory-leak-in-the-loop-optimizing-custom-state-reducers-in-langgraph/) |
| Understanding Reducers and State Updates | [Medium — HARSHA J S](https://harshaselvi.medium.com/building-ai-agents-using-langgraph-part-8-understanding-reducers-and-state-updates-c8056963a42c) |

## 專案概述

LangGraph 是 LangChain 生態系的 **圖狀態機框架**，用於建構具有循環、分支、持久化能力的 AI Agent 工作流。其核心抽象是 `StateGraph` — 一個以 **共享狀態（State）** 為通訊媒介的有向圖，所有節點透過讀寫同一份 State 來協作。

State 是 LangGraph 中最重要的概念：它是整個圖在任意時間點的快照（snapshot），定義了節點之間「看到什麼」和「能改什麼」。理解 State API 是使用 LangGraph 的前提。

## 核心概念：State 與 Channel

### State 的本質

```
┌─────────────────────────────────────────────┐
│  State = TypedDict + Annotated Reducers     │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Channel │  │ Channel │  │ Channel │     │
│  │  "foo"  │  │  "bar"  │  │ "msgs"  │     │
│  │ int     │  │ list    │  │ list    │     │
│  │ 覆寫    │  │ append  │  │ add_msg │     │
│  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────┘
```

- **State** = 一個 Python 型別（TypedDict / dataclass / Pydantic BaseModel）
- **Channel** = State 中的每個 key，各自可以有獨立的更新策略（reducer）
- **Node** 的簽名：`State → Partial<State>`（接收完整 State，回傳只需變更的欄位）

### 三種定義方式

| 方式 | 適用場景 | 特性 |
|------|---------|------|
| `TypedDict` | 最常用，官方推薦 | 輕量、型別安全 |
| `dataclass` | 需要 default 值 | 支援預設值 |
| `Pydantic BaseModel` | 需要遞迴驗證 | 功能最強但效能較低 |

## Reducer 機制

Reducer 是 LangGraph State 管理的核心 — 決定當多個節點更新同一個 channel 時，值如何合併。

### 預設行為：覆寫（Overwrite）

沒有 reducer 的 channel，新值直接覆蓋舊值：

```python
class State(TypedDict):
    foo: int       # 無 reducer → 覆寫
    bar: list[str] # 無 reducer → 覆寫
```

```
輸入: {"foo": 1, "bar": ["hi"]}
Node 回傳: {"foo": 2}
結果: {"foo": 2, "bar": ["hi"]}  ← foo 被覆寫，bar 未動
```

### Annotated Reducer：自訂合併邏輯

用 `typing.Annotated` 為 channel 附加 reducer function：

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]  # ← operator.add 作為 reducer
```

```
輸入: {"foo": 1, "bar": ["hi"]}
Node 回傳: {"bar": ["bye"]}
結果: {"foo": 1, "bar": ["hi", "bye"]}  ← list 串接而非覆寫
```

### 內建與常用 Reducer 一覽

| Reducer | 型別 | 行為 | 適用場景 |
|---------|------|------|---------|
| _(無)_ | 任意 | 覆寫 | 單值狀態（current_stage） |
| `operator.add` | `int` | 數學加法 | 計數器 |
| `operator.add` | `list` | 串接 | 累積結果 |
| `operator.add` | `str` | 串接 | log 累積 |
| `add_messages` | `list[AnyMessage]` | 智慧追加+ID更新 | 對話歷史 |
| `lambda x, y: y` | 任意 | 強制覆寫 | 暫存區（每輪重置） |
| `lambda x, y: {**x, **y}` | `dict` | 淺合併 | metadata / config |

### 自訂 Reducer 範例

```python
# 去重追加
def unique_append(current: list, new: list) -> list:
    result = current[:]
    for item in new:
        if item not in result:
            result.append(item)
    return result

# 有上限的滾動視窗
def bounded_list(max_size: int):
    def reducer(current: list, new: list) -> list:
        combined = current + new
        return combined[-max_size:] if len(combined) > max_size else combined
    return reducer

class State(TypedDict):
    tags: Annotated[list, unique_append]
    recent_items: Annotated[list, bounded_list(10)]
```

## Messages 處理

LLM 對話的核心是訊息列表。LangGraph 提供專用的 `add_messages` reducer 和 `MessagesState` 快捷型別。

### add_messages Reducer

```python
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

`add_messages` 的三個關鍵能力：

1. **追加**新訊息到列表
2. **依 ID 更新**已存在的訊息（而非重複追加）
3. **反序列化**字典格式為 LangChain Message 物件

```python
# 兩種格式都支援
{"messages": [HumanMessage(content="Hello")]}
{"messages": [{"type": "human", "content": "Hello"}]}
```

### MessagesState 快捷型別

```python
from langgraph.graph import MessagesState

# 直接使用
graph = StateGraph(MessagesState)

# 或繼承擴充
class State(MessagesState):
    documents: list[str]
    user_id: str
```

`MessagesState` 已內建 `messages: Annotated[list[AnyMessage], add_messages]`，適合快速原型。

### Overwrite 繞過 Reducer

當需要完全替換（而非合併）時：

```python
from langgraph.types import Overwrite

def reset_messages(state: State):
    return {"messages": Overwrite([SystemMessage("重置")])}
```

⚠️ **限制**：並行節點在同一 super-step 中，同一 key 只能有一個節點使用 `Overwrite`。

## 多 Schema 模式

LangGraph 支援分離 **輸入 / 輸出 / 內部** Schema，實現更精細的資料流控制：

```python
class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

class PrivateState(TypedDict):
    bar: str  # 只在特定節點間傳遞

builder = StateGraph(
    OverallState,
    input_schema=InputState,    # 外部只能傳入這些欄位
    output_schema=OutputState   # 外部只拿到這些欄位
)
```

```
                    input_schema          output_schema
                    ┌─────────┐           ┌────────────┐
user_input ────────►│ node_1  │──► foo ──►│   node_3   │──► graph_output
                    └─────────┘           └────────────┘
                         │                      ▲
                         ▼                      │
                    ┌─────────┐                 │
                    │ node_2  │──► bar ──────────┘
                    └─────────┘
                    PrivateState
```

**關鍵洞見**：節點可以寫入任何 OverallState 的 channel，即使該 channel 不在節點的輸入 Schema 中。透過函式簽名可以宣告新的 channel。

## Node 與 Edge 中的 State

### Node 函式簽名

```python
# 最簡形式
def plain_node(state: State) -> dict:
    return {"results": "done"}

# 帶 Runtime context
def node_with_runtime(state: State, runtime: Runtime[Context]) -> dict:
    user = runtime.context.user_id
    return {"results": f"Hello, {user}!"}

# 帶 RunnableConfig
def node_with_config(state: State, config: RunnableConfig) -> dict:
    thread_id = config["configurable"]["thread_id"]
    return {"results": f"Thread: {thread_id}"}
```

### Conditional Edge 路由

```python
def routing_function(state: State) -> str:
    if state["score"] > 0.8:
        return "approve"
    return "review"

graph.add_conditional_edges(
    "evaluator",
    routing_function,
    {"approve": "finalizer", "review": "human_review"}
)
```

## 進階模式：生產環境的 State 最佳化

### 問題：Append-Only 的記憶體膨脹

預設 `add_messages` 是 **append-only**，在迭代式工作流（自我修正、反思 Agent）中產生 **O(N²) token 消耗**：

| 迭代 | 累積 token |
|------|-----------|
| 1 | 1,000 |
| 5 | 3,500 |
| 10 | 5,500 |
| **總計（10 輪）** | **~37,500** |

### 解法一：里程碑滾動視窗

保留最近 N 條 + 標記為「里程碑」的關鍵訊息：

```python
def milestone_reducer(current: list, update: list) -> list:
    window_size = 10
    full_history = current + update
    kept = []
    cutoff = len(full_history) - window_size
    for i, msg in enumerate(full_history):
        is_recent = i >= cutoff
        is_milestone = msg.additional_kwargs.get('milestone', False)
        if is_recent or is_milestone:
            kept.append(msg)
    return kept
```

### 解法二：雙通道暫存架構

將 State 分為**持久通道**和**暫存通道**：

```python
class DualMemoryState(TypedDict):
    # 持久：只保留關鍵交互（用戶輸入、最終答案）
    conversation_history: Annotated[list[BaseMessage], add_messages]

    # 暫存：內部推理（每輪覆寫、不累積）
    reasoning_scratchpad: Annotated[list[BaseMessage], lambda x, y: y]

    # 知識圖譜：淺合併
    knowledge_graph: Annotated[dict, lambda x, y: {**x, **y}]
```

| 指標 | 標準累積 | 雙通道覆寫 |
|------|---------|-----------|
| 10 輪 token 消耗 | ~37,500 | ~15,000 |
| 每步複雜度 | O(N) 線性增長 | O(1) 常數 |
| Token 節省 | — | **~60%** |

## State Migration

LangGraph 支援帶 checkpoint 的圖定義變更：

| 場景 | 已完成的 thread | 被中斷的 thread |
|------|----------------|----------------|
| 完整拓撲變更 | ✅ 支援 | ⚠️ 不支援刪除/重命名節點 |
| Key 新增/移除 | ✅ 向前/向後相容 | ✅ 向前/向後相容 |
| Key 重命名 | ⚠️ 現有 thread 遺失舊資料 | ⚠️ 現有 thread 遺失舊資料 |
| 型別不相容變更 | ❌ 舊 thread 可能報錯 | ❌ 舊 thread 可能報錯 |

## 目前限制 / 注意事項

1. **Pydantic BaseModel 效能較差** — 每次更新都會做遞迴驗證，高頻場景建議用 TypedDict
2. **Overwrite 並行限制** — 同一 super-step 中同一 key 只能有一個節點使用 `Overwrite`
3. **add_messages 非生產級** — 預設 append-only，迭代密集的 Agent 必須自訂 reducer 或採用雙通道架構
4. **State 不可變性** — 節點中直接修改 `state` 物件會繞過 reducer，破壞歷史追蹤和並發安全
5. **State Migration 限制** — 被中斷的 thread 不支援刪除或重命名節點

## 研究價值與啟示

### 關鍵洞察

1. **Reducer 即策略模式** — LangGraph 用 `Annotated[Type, reducer_fn]` 把「資料如何合併」提升為一等公民。這不只是語法糖，而是讓每個 State channel 都能獨立選擇合併策略（覆寫、追加、去重、滾動視窗），比傳統的單一 state update 機制靈活得多。這個設計值得借鏡到任何多步驟工作流系統。

2. **Append-Only 是原型陷阱** — 預設的 `add_messages` 在 demo 中看起來很完美，但在自我修正/反思 Agent 的迭代迴圈中會造成 O(N²) token 膨脹。生產環境必須從第一天就設計有上限的 reducer（bounded reducer 或 dual-channel 架構），而非事後修補。

3. **多 Schema 是 Agent 間資訊隔離的關鍵** — `input_schema` / `output_schema` / `PrivateState` 的組合讓圖的對外介面與內部實作分離，類似 API 的 request/response DTO。這在多 Agent 系統中防止資訊洩漏和狀態污染，是良好的軟體工程實踐。

4. **Node 回傳差量而非全量** — `State → Partial<State>` 的約定讓 reducer 得以正確運作，也讓系統能追蹤每步變更。這與 React 的 `setState(partial)` 和 Redux 的 reducer 概念一脈相承，是 UI 狀態管理智慧在 AI Agent 領域的遷移。

5. **不可變性是並發安全的基石** — LangGraph 要求節點不得直接修改 state 物件，而是回傳新的 partial dict。這確保了並行節點執行時的 thread safety，也讓 checkpoint/replay 成為可能。直接修改 state 是最常見的陷阱，會導致難以除錯的 race condition。

### 與其他專案的關聯

- **LangChain**（`langchain.md`）：LangGraph 是 LangChain 生態系的一部分，State API 中的 `AnyMessage`、`HumanMessage`、`AIMessage` 等都來自 `langchain-core`。LangGraph 可視為 LangChain 從線性 chain 進化到圖狀態機的關鍵升級。
- **CrewAI**（`crewai.md`）：CrewAI 的多 Agent 協作隱藏了狀態管理細節，LangGraph 則完全暴露 State 讓開發者精確控制。兩者的取捨是「易用性 vs 可控性」。
- **TradingAgents**（`tradingagents.md`）：作為基於 LangGraph 的多 Agent 交易系統，其內部大量使用 State reducer 來累積各 Agent（基本面分析、技術分析、情緒分析）的報告。雙通道暫存架構可直接應用於最佳化其推理迴圈的 token 消耗。
- **AI Agents 黃佳**（`ai-agents.md`）：書中的 Agent 架構概念（記憶、規劃、工具使用）在 LangGraph 中透過 State channels 具體實現 — `messages` 是記憶、conditional edge 是規劃、tool node 是工具使用。
