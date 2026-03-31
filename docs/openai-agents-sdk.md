---
date: "2026-03-31"
category: "AI Agent 框架"
card_icon: "material-robot-industrial"
oneliner: "OpenAI 官方 Agent 框架 — 以 Handoffs + Guardrails 為核心的輕量多代理工作流系統"
---

# OpenAI Agents SDK 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方文件 | [developers.openai.com/api/docs/guides/agents-sdk](https://developers.openai.com/api/docs/guides/agents-sdk) |
| Python SDK 文件 | [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/) |
| Python SDK GitHub | [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python) |
| TypeScript SDK GitHub | [github.com/openai/openai-agents-js](https://openai.github.io/openai-agents-js) |
| Handoffs 文件 | [openai.github.io/openai-agents-python/handoffs](https://openai.github.io/openai-agents-python/handoffs/) |
| Guardrails 文件 | [openai.github.io/openai-agents-python/guardrails](https://openai.github.io/openai-agents-python/guardrails/) |
| 發布公告 | [openai.com/index/new-tools-for-building-agents](https://openai.com/index/new-tools-for-building-agents/) |

## 專案概述

OpenAI Agents SDK 是 OpenAI 的官方 Agent 開發框架，前身為實驗性的 **Swarm** 專案，於 2025 年 3 月正式發布。它是一個輕量、抽象層極少的 Python-first 框架（也有 TypeScript 版本），設計哲學是「足夠的功能讓你值得用，但抽象層少到幾分鐘就能學會」。

與 Claude Agent SDK 的「把產品能力變成函式庫」不同，OpenAI Agents SDK 更偏向「多代理協作框架」——核心不是內建工具，而是 Agent 間的 Handoff（委派）和 Guardrails（護欄）機制。

**GitHub 社群數據**：20.4k stars、3.3k forks、77 releases（最新 v0.13.2）、MIT License

## 核心架構

```
┌──────────────────────────────────────────────┐
│              Runner.run() / run_sync()         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐  │
│  │  Agent A  │──▶│  Agent   │──▶│ RunResult│  │
│  │ (primary) │   │   Loop   │   │          │  │
│  └──────────┘   └────┬─────┘   └──────────┘  │
│                      │                         │
│      ┌───────────────┼───────────────┐         │
│      ▼               ▼               ▼         │
│ ┌──────────┐  ┌───────────┐  ┌───────────┐   │
│ │  Tools   │  │ Handoffs  │  │Guardrails │   │
│ │(function,│  │(Agent B,C)│  │(input /   │   │
│ │ MCP,     │  │           │  │ output /  │   │
│ │ hosted)  │  │           │  │ tool)     │   │
│ └──────────┘  └───────────┘  └───────────┘   │
│                                                │
│   Tracing: 全程追蹤 → 視覺化 / 除錯 / 微調     │
└──────────────────────────────────────────────┘
```

## 安裝

```bash
pip install openai-agents
# 可選：pip install 'openai-agents[voice]'   # 語音支援
# 可選：pip install 'openai-agents[redis]'   # Redis Session
```

需設定 `OPENAI_API_KEY` 環境變數。支援 Python 3.10+。

## 三大核心原語

### 1. Agent — 配備指令和工具的 LLM

```python
from agents import Agent

agent = Agent(
    name="Refund Specialist",
    instructions="Handle refund requests. Verify order, check policy, process refund.",
    tools=[check_order, process_refund],     # function tools
    handoffs=[escalation_agent],              # 可委派的其他 Agent
    input_guardrails=[safety_check],          # 輸入護欄
    output_guardrails=[pii_filter],           # 輸出護欄
)
```

### 2. Handoffs — Agent 間的委派機制

Handoffs 讓 Agent 將對話委派給另一個專門的 Agent。對 LLM 來說，Handoff 呈現為一個工具（如 `transfer_to_refund_agent`）。

```python
from agents import Agent, handoff

triage_agent = Agent(
    name="Triage",
    instructions="Route customer to the right specialist.",
    handoffs=[
        handoff(
            agent=refund_agent,
            tool_description_override="Transfer when customer wants a refund",
            on_handoff=lambda ctx: log_handoff(ctx),  # callback
            input_type=HandoffReason,                   # 結構化理由
        ),
        billing_agent,   # 簡單傳入 Agent 也可以
    ]
)
```

**進階功能：**

- `input_filter`：修改下一個 Agent 收到的歷史訊息
- `is_enabled`：動態控制 Handoff 是否可用
- `nest_handoff_history`（beta）：巢狀 Handoff 時壓縮前序對話為摘要

### 3. Guardrails — 輸入 / 輸出 / 工具的安全護欄

| 類型 | 觸發時機 | 說明 |
|------|---------|------|
| Input Guardrail | 工作流開始時（第一個 Agent） | 驗證使用者輸入 |
| Output Guardrail | 工作流結束時（最後一個 Agent） | 驗證最終輸出 |
| Tool Guardrail | 工具執行前後 | 驗證工具輸入/輸出 |

**執行模式（僅 Input Guardrail）：**

- `parallel`（預設）：與 Agent 同時執行，延遲最低但可能已消耗 token
- `blocking`：Guardrail 先完成，才啟動 Agent

**Tripwire 模式**：Guardrail 失敗時拋出例外（`InputGuardrailTripwireTriggered`），立即中止執行。

```python
from agents import input_guardrail, GuardrailFunctionOutput, Runner

@input_guardrail
async def math_homework_check(ctx, agent, input):
    result = await Runner.run(guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework
    )
```

## Runner（執行引擎）

| 方法 | 類型 | 回傳 | 適用場景 |
|------|------|------|---------|
| `Runner.run()` | async | `RunResult` | 一般非同步使用 |
| `Runner.run_sync()` | sync | `RunResult` | 簡單腳本、同步環境 |
| `Runner.run_streamed()` | async | `RunResultStreaming` | 即時串流 LLM 事件 |

**Agent Loop 執行流程：**

```
呼叫 LLM → 評估輸出:
  ├─ 文字輸出（無工具呼叫）→ 結束，回傳結果
  ├─ Handoff → 切換 Agent，重新開始 loop
  └─ Tool Call → 執行工具，附加結果，繼續 loop
  
超過 max_turns → 拋出 MaxTurnsExceeded
```

## RunConfig 設定

```python
from agents import RunConfig

config = RunConfig(
    model="gpt-4o",                    # 全域模型覆蓋
    max_turns=50,                       # 最大迴圈次數
    tracing_disabled=False,             # 追蹤開關
    workflow_name="customer-support",   # 追蹤命名
)

result = await Runner.run(agent, input, run_config=config)
```

## 其他重要功能

### Tools（工具系統）

| 類型 | 說明 |
|------|------|
| Function Tools | 任何 Python function + 自動 schema 生成 |
| MCP Tools | 透過 Model Context Protocol 連接外部系統 |
| Hosted Tools | OpenAI 託管（web search、file search、code interpreter） |

### Sessions（會話管理）

自動管理跨 Agent 執行的對話歷史，支援三種策略：

1. **手動**：`result.to_input_list()` 取得歷史
2. **Session 持久化**：使用 Redis 等後端自動保存
3. **伺服器端**：透過 `conversation_id` 或 `previous_response_id`

### Tracing（追蹤系統）

內建的全程追蹤系統，支援：

- 視覺化 Agent 執行流程
- 除錯工具呼叫和 Handoff
- 匯出用於微調訓練資料

### Realtime Agents（即時語音）

使用 `gpt-realtime-1.5` 模型建構語音 Agent，支援中斷偵測和完整 Agent 功能。

## 最小範例

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
# >> Endless loop of calls,
#    Functions echo themselves,
#    Depth becomes the key.
```

## 多代理範例

```python
from agents import Agent, Runner

refund_agent = Agent(name="Refund Agent",
    instructions="Process refunds. Ask for order ID if not provided.")

billing_agent = Agent(name="Billing Agent",
    instructions="Handle billing inquiries. Check account status.")

triage_agent = Agent(name="Triage",
    instructions="Route customer queries to the right specialist.",
    handoffs=[refund_agent, billing_agent])

result = Runner.run_sync(triage_agent, "I want a refund for order #12345")
print(result.final_output)
```

## 目前限制 / 注意事項

- **Python-first 設計**：TypeScript 版本功能可能落後 Python 版
- **無內建檔案操作工具**：不像 Claude Agent SDK 內建 Read/Write/Edit/Bash，需自行實作或使用 MCP
- **Hosted Tools 僅限 OpenAI**：web search、file search、code interpreter 跑在 OpenAI 基礎設施上，無法自託管
- **模型提供者鎖定風險**：雖聲稱支援 100+ LLM（透過 LiteLLM），但核心功能針對 OpenAI 模型優化
- **Guardrails 可能消耗額外 token**：parallel 模式下 Agent 可能在 Guardrail 觸發前已執行部分工作

## 研究價值與啟示

### 關鍵洞察

1. **Handoffs 是真正的差異化設計**——多數 Agent 框架用 orchestrator 或 supervisor 模式管理多個 Agent，OpenAI 選擇讓 Agent「自己決定」何時把對話交給誰。這更接近人類團隊的協作方式（「這個問題我處理不了，轉給退款部門」），對客服、多部門工作流特別自然。

2. **Guardrails 的「Tripwire + 平行執行」模式值得學習**——不是在 Agent 啟動前做完所有檢查，而是與 Agent 平行跑，「有問題就拉停」。這在延遲敏感的場景（如即時對話）中兼顧安全與效能。

3. **Swarm → Agents SDK 的演進路徑有參考價值**——從實驗性的 multi-agent 探索框架，演進為生產級 SDK，保留了核心理念（agents, handoffs）並加入企業級功能（guardrails, tracing, sessions）。這種「先驗證概念、再產品化」的路線值得關注。

4. **「空工具箱」是刻意的設計選擇**——與 Claude Agent SDK 的「出廠 8 工具」相比，OpenAI 選擇不預設任何工具。好處是更通用（不綁定檔案系統操作），壞處是建構 coding agent 需要更多前置工作。兩種策略反映了產品定位差異：Claude = coding agent 框架，OpenAI = 通用 agent 框架。

5. **Tracing 整合微調的閉環設計**——追蹤資料不只用於除錯，還能直接匯出為微調訓練資料。這形成了「部署 → 觀察 → 微調 → 改善」的閉環，是其他框架較少強調的功能。

### 與其他專案的關聯

- **vs [Claude Agent SDK](claude-agent-sdk.md)**：最直接的競品比較。Claude = 內建工具 + Hooks 生命週期控制；OpenAI = Handoffs + Guardrails 多代理協作。選擇取決於是 coding agent（Claude）還是通用多代理（OpenAI）
- **vs [CrewAI](crewai.md)**：CrewAI 也是多代理框架，但用 Role/Goal/Backstory 定義 Agent，更偏向「團隊模擬」。OpenAI Agents SDK 更輕量、更貼近 API
- **vs [LangGraph](langgraph-multi-agent.md)**：LangGraph 用圖結構定義工作流，適合複雜的狀態機。OpenAI Agents SDK 的 Handoffs 更簡單但也更受限——適合線性委派，不適合複雜分支
- **vs [TradingAgents](tradingagents.md)**：TradingAgents 的多 Agent 辯論模式可以用 Handoffs 實現，但需要額外抽象層
