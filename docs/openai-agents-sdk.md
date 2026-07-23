---
date: "2026-07-17"
category: "AI Agent 框架"
card_icon: "material-robot-industrial"
oneliner: "OpenAI 官方 Agent 框架 — Handoffs + Guardrails 起家，v0.18 補上 Sandbox Agents 與 Human-in-the-loop"
tags:
  - agent-framework
  - multi-agent
  - mcp
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

與 Claude Agent SDK 的「把產品能力變成函式庫」不同，OpenAI Agents SDK 起家時更偏向「多代理協作框架」——核心不是內建工具，而是 Agent 間的 Handoff（委派）和 Guardrails（護欄）機制。但到了 2026 年中，它已補上 Sandbox Agents（容器化 coding harness）與 Human-in-the-loop，定位往通用 agent 平台擴張（見下方「2026 年重大新增」）。

**GitHub 社群數據**（2026-07 更新）：27.9k stars、4.3k forks、108+ releases（最新 **v0.18.3**，2026-07-17）、MIT License

> **本次更新（v0.13 → v0.18）重點**：新增 ① Sandbox Agents（beta，持久化工作區 + `apply_patch`/`ShellTool`）② Human-in-the-loop（`needs_approval` + `RunState` 續跑）③ Agents-as-tools（把 Agent 當工具呼叫）；Realtime 模型升至 `gpt-realtime-2.1`；模型層新增 `any-llm`（與 LiteLLM 並列）。

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

## 2026 年重大新增（v0.14 → v0.18）

半年間，框架從「純多代理協作」擴張成涵蓋 coding agent 的完整 harness。README 現在把執行方式分成三種：**Sandbox Agent（長時任務）／Text Agent（一般）／Realtime Agent（語音）**。核心新增三塊：

### Sandbox Agents（beta）— 容器化長時任務

`SandboxAgent` 給模型一個**持久化工作區**：搜尋大量文件、編輯檔案、跑指令、產生產物、從存檔的 sandbox 狀態接續工作。你不用自己接檔案 staging、filesystem 工具、shell、sandbox 生命週期與快照——維持原本的 `Agent` / `Runner` 流程，加上 `Manifest` + `Capabilities` + `SandboxRunConfig` 即可。這正面回應了舊筆記「無內建檔案操作工具」的批評。

```python
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import GitRepo
from agents.sandbox.sandboxes import UnixLocalSandboxClient

agent = SandboxAgent(
    name="Workspace Assistant",
    instructions="Inspect the sandbox workspace before answering.",
    default_manifest=Manifest(entries={"repo": GitRepo(repo="openai/openai-agents-python", ref="main")}),
)
result = Runner.run_sync(
    agent, "Inspect the repo README and summarize what this project does.",
    run_config=RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient())),
)
```

| 元件 | 角色 |
|------|------|
| `Manifest` | 定義工作區內容：`GitRepo`（clone repo）、`LocalDir`（掛載本地目錄） |
| `Capabilities` | 開啟 sandbox 原生工具；含 `Skills` + lazy skill source，可把 Claude Skills 風格的技能**按需複製**進 sandbox |
| `SandboxRunConfig` | 決定工作跑在哪：`UnixLocalSandboxClient`（本地）或 `openai-agents[docker]`（Docker） |
| `apply_patch` / `ShellTool` | 模型在 sandbox 內編輯檔案、執行指令的內建工具 |

**接下來會調的旋鈕**（Quickstart 的 "Key choices"）：

| 旋鈕 | 作用 |
|------|------|
| `default_manifest` | 新 sandbox session 的初始檔案 / repo / 掛載 |
| `instructions` | 跨 prompt 的短工作流規則 |
| `base_instructions` | 進階逃生口：**整個換掉 SDK 的 sandbox 系統提示** |
| `capabilities` | sandbox 原生工具：檔案編輯 / 看圖、shell、`Skills`、memory、compaction |
| `run_as` | 模型面向工具用的 **sandbox 使用者身分** |
| `SandboxRunConfig.client` | sandbox 後端：Unix-local / Docker / hosted provider |
| `.session` / `.session_state` / `.snapshot` | 後續 run **怎麼接回**先前的工作（續跑的關鍵） |

- `Skills` 用 **lazy 載入**：技能放 host 目錄，模型要用到才複製進 sandbox（對抗 context rot，呼應 [microsoft/skills](microsoft-skills.md) 的「啟動脈絡」哲學）
- **何時用**：只是偶爾跑個 shell → 用 hosted shell 就好；當「工作區隔離、選 sandbox 後端、session 續跑」本身是設計的一環 → 才上 Sandbox Agent
- `base_instructions` 這個逃生口透露：這層 harness 高度 **prompt-driven**，可深度客製，但也意味預設行為會隨版本變

> 官方範例用 `gpt-5.6-sol`（coding 導向模型）。功能仍是 **beta**，API、預設值與支援能力在正式版前會變。

**Sandbox client 選擇（工作跑在哪）**：靈魂是「**同一個 `SandboxAgent` 定義不變，只換 `SandboxRunConfig` 的 client**」——agent「做什麼」與「在哪執行」徹底解耦。

| 層級 | client | 安裝 |
|------|--------|------|
| 本地最快迭代 | `UnixLocalSandboxClient` | 無 |
| 容器隔離 / 環境對齊 | `DockerSandboxClient` | `openai-agents[docker]` |
| Hosted / 正式級 | E2B / Modal / Cloudflare / Vercel / Blaxel / Daytona / Runloop | 各自 `openai-agents[<name>]` |

- 可 Unix 開發 → Docker 對齊 → hosted 上線，**agent 定義一路不動**；7 家 hosted 都是第一方支援（執行層不綁 OpenAI 自家 sandbox）
- 遠端儲存（S3/R2/GCS/Azure/Box）用 mount 掛入；`read_only` 預設 `True`
- ⚠️ **陷阱**：mount 是 ephemeral，**不會進 snapshot**——別以為存檔會把遠端儲存內容一起存下來（詳見官方 [sandbox/clients.md](https://github.com/openai/openai-agents-python/blob/main/docs/sandbox/clients.md)）

**Agent memory（跨 run 學習）**：與 `Session`（存訊息歷史）不同，Agent memory 把**過去 run 的「教訓」提煉成檔案**存進 sandbox，讓未來的 run 少走冤枉路、記住使用者偏好、免重打背景。加 `Memory()` capability 啟用（讀需 `Shell()`、live update 需 `Filesystem()`）。

- **讀取用 progressive disclosure**：run 開始注入小摘要 `memory_summary.md`，agent 判斷相關才搜 `MEMORY.md` 索引、需要細節才展開 `rollout_summaries/`
- **生成兩階段**：Phase 1 對話萃取 → Phase 2 整併進 `MEMORY.md`；內建**遺忘機制**（raw memories 超上限〔預設 256〕就汰舊留新，反映最新環境）
- **讀寫可分離**：`Memory(generate=None)` 只讀（checker/subagent）、`Memory(read=None)` 只寫（不想被舊記憶影響）
- **隔離按 `MemoryLayoutConfig`（`memories_dir`）不按 agent 名**：不同 layout 各自獨立 `MEMORY.md`，即使同 sandbox
- 這套「`MEMORY.md` 索引 + 漸進揭露 + 生成/整併 + 遺忘」**與 Claude Code / 本站 memory 模式同源**——業界記憶設計正在收斂（詳見 [sandbox/memory.md](https://github.com/openai/openai-agents-python/blob/main/docs/sandbox/memory.md)）

**概念與生命週期**（[sandbox/guide.md](https://github.com/openai/openai-agents-python/blob/main/docs/sandbox/guide.md)）：`SandboxAgent` 仍是 `Agent`，變的只是**執行邊界**，權責二分——外層 runtime 管 approvals/tracing/handoffs/resume，sandbox session 管指令執行/檔案變動/隔離。整套圍繞正交三軸：**做什麼**（`SandboxAgent`）／**在哪跑**（`SandboxRunConfig`+client）／**怎麼接續**（snapshot / session_state），所以能換 client、換 workspace、換續跑來源而**不動 agent 定義**。

| 面向 | 重點 |
|------|------|
| **生命週期** | **SDK-owned**（只傳 `client=`，runner 建→跑→存→關）vs **Developer-owned**（自己 `client.create()` + `session=`，`async with`，跨多 run 重用）；`stop()` 只存 snapshot 不拆、`aclose()` 才完整清理 |
| **turn 語意** | turn ≠ sandbox 操作（一個 turn 是一次模型步，非一條指令）；`Agent.as_tool()` 的巢狀 run **不加**外層 turn 計數，handoff 則是同一 run 換 active agent |
| **縱深防禦** | workspace 相對路徑（禁絕對/`..`）、`extra_path_grants` 屬受信設定**不可來自模型輸出**、`Permissions`+`User`+`run_as` 做最小權限、`archive_limits` 防解壓炸彈 |

> 洞見：OpenAI 等於在 SDK 內重建了一套迷你「容器 OS」（users/權限/檔案系統/snapshot/生命週期）——給模型 shell 很危險，所以配了完整縱深防禦，比「丟個 Docker 給模型」謹慎得多。

### Human-in-the-loop（HITL）— 敏感工具需人工核准

工具用 `needs_approval=True`（或 async 判斷函式）宣告需審核。執行到該工具時**暫停**，`RunResult.interruptions` 冒出 `ToolApprovalItem`；把結果轉成 `RunState`（`result.to_state()`），呼叫 `state.approve()` / `state.reject()`，再 `Runner.run(agent, state)` 從斷點續跑。

```python
from agents import Agent, function_tool

@function_tool(needs_approval=True)          # 也可傳 async 函式做逐次判斷
async def cancel_order(order_id: int) -> str:
    return f"Cancelled order {order_id}"
```

- **適用範圍廣**：`function_tool`、`Agent.as_tool`、`ShellTool`、`ApplyPatchTool` 皆支援 `needs_approval`；本地 MCP server 用 `require_approval`，Hosted MCP 用 `tool_config={"require_approval": "always"}`
- **核准是跨整個 run 的**：handoff 之後的 agent、巢狀 `Agent.as_tool()` 內部工具冒出的核准，都在**最外層 run** 的 `RunState` 上核准並續跑
- **黏著決定**：`always_approve=True` / `always_reject=True` 存進 run state，可隨 `to_json`/`from_json` 序列化，跨程序恢復同一個暫停的 run

### Agents as tools — 把 Agent 當工具呼叫

除了 Handoff（把對話**整個交出去**、不回頭），現在能用 `Agent.as_tool()` 把一個 Agent 包成工具，由主 Agent 呼叫、**取回結果後繼續**自己的流程。

| 委派方式 | 語意 | 適合 |
|---------|------|------|
| **Handoff** | 換人接手，控制權轉移 | 客服轉接、分流到專責 Agent |
| **Agent-as-tool** | 外包一段子任務再收回結果 | 翻譯／檢索／子分析等可組合的能力 |

這補上了 Handoff「線性委派、交出去就不回來」的限制——也讓舊筆記提到的「多 Agent 辯論」這類需要收束結果的模式更容易實作。

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

### Sessions / 記憶策略（會話管理）

跨輪維持對話狀態有**四種策略**，差別在**狀態存哪、綁不綁 OpenAI、手動還是自動**：

| 策略 | 狀態存哪 | 適合場景 | 綁 OpenAI？ |
|------|---------|---------|:---:|
| `result.to_input_list()` | 你的 app 記憶體 | 小對話、要完全手控、任何 provider | ❌ 通用 |
| `session`（如 `SQLiteSession`） | 儲存後端 + SDK 管理 | 需持久化、可續跑、自訂 store（SQLite/Redis/SQLAlchemy） | ❌ 通用 |
| `conversation_id` | OpenAI Conversations API | 具名伺服器對話、跨服務共享 | ✅ 只限 OpenAI |
| `previous_response_id` | OpenAI Responses API | 輕量接續、不建對話資源 | ✅ 只限 OpenAI |

> ⚠️ 同一次 run，**session 持久化不能與 server 端對話設定（conversation_id / previous_response_id）混用**——歷史只能有一個真相來源。

**真正的分水嶺是 provider lock-in**：`to_input_list()`/`session` 把歷史留在你這邊 → 換模型不受影響；`conversation_id`/`previous_response_id` 託管在 OpenAI 伺服器 → 省事但綁死 OpenAI。且「自動」（session）省掉手動接歷史，代價是放棄「這輪送多少 token」的直接控制——延遲/成本敏感時 `to_input_list()` 的囉唆反而是特點。

### Tracing（追蹤系統）

內建的全程追蹤系統，支援：

- 視覺化 Agent 執行流程
- 除錯工具呼叫和 Handoff
- 匯出用於微調訓練資料

### Realtime Agents（即時語音）

使用 `gpt-realtime-2.1` 模型建構語音 Agent（透過 `RealtimeAgent` + `RealtimeRunner`，走 WebSocket），支援中斷偵測和完整 Agent 功能。

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
- **檔案操作改善但仍 beta**：v0.18 起 Sandbox Agents 補上 `apply_patch`/`ShellTool` 與持久化工作區，回應了原本「無內建檔案工具」的缺口，但整套 sandbox 仍是 beta，API 與預設值會變
- **Hosted Tools 僅限 OpenAI**：web search、file search、code interpreter 跑在 OpenAI 基礎設施上，無法自託管
- **模型提供者鎖定風險**：雖聲稱支援 100+ LLM（透過 `any-llm` / LiteLLM），但核心功能針對 OpenAI 模型優化；Sandbox/Realtime 更明顯綁定 OpenAI 最新模型（`gpt-5.6-sol`、`gpt-realtime-2.1`）
- **Guardrails 可能消耗額外 token**：parallel 模式下 Agent 可能在 Guardrail 觸發前已執行部分工作

## 研究價值與啟示

### 關鍵洞察

1. **Handoffs 是真正的差異化設計**——多數 Agent 框架用 orchestrator 或 supervisor 模式管理多個 Agent，OpenAI 選擇讓 Agent「自己決定」何時把對話交給誰。這更接近人類團隊的協作方式（「這個問題我處理不了，轉給退款部門」），對客服、多部門工作流特別自然。

2. **Guardrails 的「Tripwire + 平行執行」模式值得學習**——不是在 Agent 啟動前做完所有檢查，而是與 Agent 平行跑，「有問題就拉停」。這在延遲敏感的場景（如即時對話）中兼顧安全與效能。

3. **Swarm → Agents SDK 的演進路徑有參考價值**——從實驗性的 multi-agent 探索框架，演進為生產級 SDK，保留了核心理念（agents, handoffs）並加入企業級功能（guardrails, tracing, sessions）。這種「先驗證概念、再產品化」的路線值得關注。

4. **「空工具箱」的設計選擇正在收斂**——舊筆記時 OpenAI 刻意不預設任何工具（通用但難做 coding agent），與 Claude Agent SDK 的「出廠內建工具」形成對比。但 v0.18 的 Sandbox Agents 直接補上 `apply_patch`/`ShellTool` + 持久化工作區，等於把 coding-agent harness 收進框架。兩家的產品定位正在互相靠攏：OpenAI 從「通用框架」往下補 coding，Claude 從「coding 框架」往上補通用編排。

5. **Tracing 整合微調的閉環設計**——追蹤資料不只用於除錯，還能直接匯出為微調訓練資料。這形成了「部署 → 觀察 → 微調 → 改善」的閉環，是其他框架較少強調的功能。

6. **HITL 把「核准」做成 run 層級的一等公民**——多數框架的人工核准是綁在單一工具或單一 agent 上；OpenAI 讓核准跨越 handoff 與巢狀 `Agent.as_tool()`，全部在最外層 `RunState` 上處理，且能序列化後跨程序續跑。對「暫停等人審 → 幾小時後恢復」的非同步審批流（如金融、退款、寄信）特別關鍵——這也是與 Sandbox（長時任務）搭配的必要安全閥。

7. **Sandbox 的 Skills 機制呼應了 Claude Skills**——`Capabilities` 可掛 lazy skill source，把技能按需複製進 sandbox。這與 Anthropic 的 Agent Skills 是同一個方向：用「可插拔的技能包」擴充 agent，而非把所有能力寫死在 prompt/工具裡。

### 與其他專案的關聯

- **vs [Claude Agent SDK](claude-agent-sdk.md)**：最直接的競品比較。原本分野是 Claude = 內建工具 + Hooks 生命週期控制、OpenAI = Handoffs + Guardrails 多代理協作；但 v0.18 的 Sandbox Agents（`apply_patch`/shell + Skills）讓 OpenAI 也踏進 coding-agent 地盤，兩者能力持續收斂，選型差異縮小到生態與模型偏好
- **vs [CrewAI](crewai.md)**：CrewAI 也是多代理框架，但用 Role/Goal/Backstory 定義 Agent，更偏向「團隊模擬」。OpenAI Agents SDK 更輕量、更貼近 API
- **vs [LangGraph](langgraph-multi-agent.md)**：LangGraph 用圖結構定義工作流，適合複雜的狀態機。OpenAI Agents SDK 的 Handoffs 更簡單但也更受限——適合線性委派，不適合複雜分支
- **vs [TradingAgents](tradingagents.md)**：TradingAgents 的多 Agent 辯論模式可以用 Handoffs 實現，但需要額外抽象層
