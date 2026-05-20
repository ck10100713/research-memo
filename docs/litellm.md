---
date: "2026-05-20"
category: "開發工具"
card_icon: "material-router-network"
oneliner: "BerriAI 開源 AI Gateway，把 100+ LLM provider 統一成 OpenAI 格式 + virtual keys + cost tracking + guardrails，YC W23，被 Stripe/Netflix/OpenAI Agents SDK 採用，47k stars"
---

# LiteLLM 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/BerriAI/litellm> |
| 官方網站 | <https://www.litellm.ai/> |
| 文件 | <https://docs.litellm.ai/docs/> |
| Models catalog | <https://models.litellm.ai/> |
| Proxy (AI Gateway) 文件 | <https://docs.litellm.ai/docs/simple_proxy> |
| Enterprise tier | <https://litellm.ai/enterprise> |
| PyPI | `litellm` / `litellm[proxy]` |
| YC | Winter 2023 batch |
| Discord / Slack / WhatsApp | 多通路社群支援 |
| 規模 | 47,639 stars / 8,184 forks / 創建 2023-07-27（**接近 3 年**） |
| Topics | ai-gateway、llm-gateway、llmops、**mcp-gateway**、openai-proxy |

## 概述

**LiteLLM** 是 BerriAI（YC W23）開源的 **AI Gateway** + **Python SDK** 雙形態工具，slogan：

> *"Open Source AI Gateway for 100+ LLMs. Self-hosted. Enterprise-ready. Call any LLM in OpenAI format."*

它解決的問題：**LLM 供應商越來越多（OpenAI / Anthropic / Gemini / Bedrock / Azure / Cohere / DeepSeek / Mistral / Groq / together.ai / Ollama / vLLM ...），每家 SDK / 認證 / 請求格式 / 錯誤處理都不一樣**。LiteLLM 把這個 fragmentation 收成「**一個 SDK / 一個 endpoint，所有都長得像 OpenAI API**」。

**OSS 採用者** (README 列出)：**Stripe、Google ADK、Greptile、OpenHands、Netflix、OpenAI Agents SDK** —— 業界一線都在用。

**Performance**：官方 benchmark 1k RPS 下 P95 latency **8ms**——對 production gateway 來說是極快。

## 雙產品形態

### 1. Python SDK（給開發者直接 import）

```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"]    = "..."
os.environ["ANTHROPIC_API_KEY"] = "..."

# OpenAI
r = completion(model="openai/gpt-4o",                 messages=[{"role":"user","content":"Hello"}])

# Anthropic（同一行 code 換 model 字串）
r = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role":"user","content":"Hello"}])
```

→ **同一個 `completion()` 函式，model 字串前綴決定走哪家**。所有 vendor 都接受 OpenAI 格式的 messages，內部 LiteLLM 自動轉成各家的原生格式。

### 2. AI Gateway / Proxy Server（部署成獨立 service）

```bash
uv tool install 'litellm[proxy]'
litellm --model gpt-4o
```

```python
# Client 用 OpenAI SDK，但 base_url 指向 LiteLLM proxy
import openai
client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(model="gpt-4o", messages=[...])
```

→ **整個團隊 / 整個組織共用一個 gateway**，team 內任何語言任何 framework 只要呼叫 OpenAI-compatible API 都能用。

## 內建功能（為什麼是 enterprise-ready）

| 能力 | 內容 |
|------|------|
| **Unified API** | 100+ providers 一致 OpenAI 格式 |
| **Drop-in OpenAI compatibility** | 換 provider 不用改 client code |
| **Virtual Keys** | 給 dev / team / project 各自發 token，沒人看到真實 vendor key |
| **Spend tracking** | 自動算每個 key / model / user 花多少錢 |
| **Guardrails** | 內容過濾、PII 偵測、prompt injection 防護 |
| **Load balancing** | 多 model / 多 key 自動分流 + failover |
| **Admin Dashboard** | 內建管理介面 |
| **8ms P95 @ 1k RPS** | production 級 latency |

## 11 種 Endpoint 全覆蓋

LiteLLM 不只 chat completions，**把 OpenAI 整套 API 都實作了**：

```text
/chat/completions    對話
/responses           OpenAI 新版 Responses API
/messages            Anthropic Messages 風格
/embeddings          向量
/images              影像生成
/audio/transcriptions / /audio/speech   語音
/batches             批次
/rerank              重排序
/a2a                 ← Agent-to-Agent 協議
/moderations         內容審核
```

→ **`/a2a` endpoint 是 2026 新賣點**——支援跟 LangGraph / Vertex AI Agent Engine / Azure AI Foundry / Bedrock AgentCore / Pydantic AI 等 agent 服務的 Agent-to-Agent 通訊協議。

## MCP Gateway（這是 2026 LiteLLM 的最重要新功能）

LiteLLM 把自己同時做成「**LLM gateway**」+「**MCP gateway**」雙身分：

### MCP Bridge（SDK 內呼叫）

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from litellm import experimental_mcp_client
import litellm

server_params = StdioServerParameters(command="python", args=["mcp_server.py"])
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
        # 任意 LLM 都能呼叫 MCP tools
        response = await litellm.acompletion(model="gpt-4o", messages=..., tools=tools)
```

### MCP Gateway（proxy 內路由）

```bash
curl http://0.0.0.0:4000/v1/chat/completions \
  -H 'Authorization: Bearer sk-1234' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role":"user","content":"Summarize the latest open PR"}],
    "tools": [{
      "type": "mcp",
      "server_url": "litellm_proxy/mcp/github",
      "server_label": "github_mcp",
      "require_approval": "never"
    }]
  }'
```

→ **把 MCP server 註冊到 proxy 後，任何走 LiteLLM 的 LLM call 都能用該 MCP**。對「**多 LLM × 多 MCP server**」的 N×M 整合是極大簡化。

### 也是 Cursor MCP Server

```json
{
  "mcpServers": {
    "LiteLLM": {
      "url": "http://localhost:4000/mcp/",
      "headers": { "x-litellm-api-key": "Bearer sk-1234" }
    }
  }
}
```

→ Cursor 透過 LiteLLM proxy 用到的 MCP server，**安全 token 不外洩**。

## 100+ Provider 覆蓋（部分摘錄）

從 README 表格的不完全列表（每個都至少支援 `/chat/completions`）：

```text
OpenAI / Azure / Azure AI / Anthropic / Anthropic Text
Google: Gemini / VertexAI / Vertex AI Agent Engine
AWS: Bedrock / Sagemaker / Bedrock AgentCore
Cohere / AI21 / Aleph Alpha / Amazon Nova / Mistral
DeepSeek / Cerebras / Groq / Together.ai / Fireworks / Anyscale
HuggingFace / Replicate / Ollama / vLLM / NVIDIA NIM
Bytez / Baseten / Cloudflare Workers AI / Codestral
Aliyun Dashscope（通義千問）/ DataRobot / Deepgram / DeepInfra
AssemblyAI / Clarifai / CometAPI / CompactifAI / Custom（自定義 OpenAI-compatible）
... 還有 60+ 個
```

→ **這是目前最完整的 LLM provider abstraction 層**，比任何單一 SDK（OpenAI / Anthropic 官方）都涵蓋廣。

## 部署選項

| 方式 | 適合 |
|------|------|
| **`uv tool install 'litellm[proxy]'`** | 本機 / 小團隊 |
| **Render 一鍵 deploy** | 個人 / PoC |
| **Railway 一鍵 deploy** | 小 production |
| **Docker** | 標準 self-host |
| **Kubernetes** | 大規模生產 |
| **Hosted LiteLLM Proxy** | BerriAI 自家託管 |
| **Enterprise Tier** | 公司 / 機構級需求（含付費功能） |

## 商業模式：Open Core

LiteLLM 是 **open-core**：

- **OSS（這個 repo）**：所有 LLM 路由、SDK、proxy 核心功能
- **Enterprise Tier**：SSO、audit logs、custom branding、SLA、priority support、自家託管

→ 跟 [[quantdinger]] 的「OSS + USDT billing primitive」、Hashicorp 的 OSS + Enterprise、Sentry 的雙授權路線一致。**LiteLLM 是 LLM infra 領域最成功的 open-core 商業案例**。

## 目前限制與注意事項

- **License 標 "Other"**：repo 內有 LICENSE，但 GitHub 無法自動分類。**核心是 MIT，Enterprise 功能有商業條款**，使用前讀清楚。
- **OpenAI 格式不能完全表達所有 provider 細節**：例如 Anthropic 的 `prompt caching`、Gemini 的 `system instruction` 等 vendor-specific 功能，**LiteLLM 翻譯時可能有損**。要榨乾某家功能仍建議直接用原生 SDK。
- **新功能可能不穩定**：A2A、MCP gateway 都還在 experimental 階段，**production 用要 pin version**。
- **多 provider 一致性的代價是「最低公因數」**：例如 streaming 行為、function calling schema、error code，**LiteLLM 會把所有 provider 強制 normalize 成 OpenAI 風格**——對需要 provider-specific 行為的場景是限制。
- **`pricing` 表是社群維護**：[[zeuikli-claude-code-best-practices]] 跟 [[aqua-usage-menubar]] 都用 LiteLLM 的 pricing 表算 Codex 成本，**但這個表更新有延遲**——新模型剛上市時可能還沒進表。
- **不是 vector DB / agent framework**：LiteLLM **只解 LLM provider abstraction 這一層**，不做 RAG（用 [[rag-anything]]）、不做 agent orchestration（用 LangGraph / Strands）。
- **47k stars 中相當比例是「listed in awesome lists」貢獻**：作為 infra 工具，「被需要時 100% 必要」但「日常 visibility 低」，star 增長慢、但會持續累積。
- **Performance 8ms 是 best case**：實際 production 還要加 LLM provider 本身的網路 RTT 跟 inference time（往往 500ms~5s），LiteLLM 自身 overhead 確實低。

## 研究價值與啟示

### 關鍵洞察

1. **「LLM 領域的 OpenAI 標準化」已經發生**：100+ provider 接受 OpenAI 格式（不論原生支援還是被 LiteLLM 翻譯）——**OpenAI API 是事實上的 LLM 通用協議**，跟 SQL 對 RDBMS、HTTP/REST 對 Web 一樣的角色。任何新 LLM 服務都會優先實作 OpenAI 相容。
2. **「AI Gateway pattern」是 LLM infra 必經之路**：你的應用發展到一定階段，**遲早會需要 virtual keys、spend tracking、load balancing、fallback、guardrails**——這些不是「最佳實踐」是「沒做就會出事」。LiteLLM 是這個 pattern 的事實標準實作。
3. **MCP Gateway 是 2026 最被低估的設計**：MCP server 越來越多（[[cli-anything]] 60+ 個、[[tlc-agent-skills]] 19 個 agent...），如果每個 client 都自己連 MCP，N×M 整合會爆炸。**LiteLLM 把 MCP server 集中註冊在 gateway**，所有 LLM call 共用——這個架構會在 2026 成為標準。
4. **「Virtual Keys」是企業 LLM 採用的關鍵**：沒有 virtual key 機制，**沒人敢給整個團隊 vendor key**——成本不可控、權限沒邊界。LiteLLM 解這個痛點是它能進 Stripe / Netflix 的核心理由。
5. **「Drop-in OpenAI compatibility」反向統治了 LLM 領域**：本來是 OpenAI 為了相容自家舊 API 設計的格式，**反而變成業界共通語言**——Anthropic、Google、Mistral 都被迫支援。LiteLLM 把這個趨勢工程化到極致。
6. **`/a2a` endpoint 預示 Agent 互通協議的方向**：2026 出現的 A2A 協議是 Google 提的（[[ai-agents-for-beginners]] 第 11 課提到），**LiteLLM 把 A2A 變成 gateway 級的支援**——意味著未來 agent 互通可能不需要直連，而是走 gateway。
7. **OSS 採用清單（Stripe / Netflix / OpenAI Agents SDK）反映 LLM infra 已是工程紀律議題**：當 OpenAI 自家的 Agents SDK 都用 LiteLLM 當底層、Netflix / Stripe 等高標準公司採用，**「LLM gateway 是 production 必需品」這件事已沒有爭議**。
8. **YC W23 但 3 年成長到 47k stars，是 LLM infra 的標準成長曲線**：對比 [[fincept-terminal]]（5 個月 21k）、[[cli-anything]]（2 個月 36k）——LiteLLM 的成長慢但持久，**infra 工具是「長期累積」勝出，不靠爆紅**。

### 與其他研究的關聯

- 與 [[zeuikli-claude-code-best-practices]]、[[aqua-usage-menubar]]：兩篇都用 LiteLLM 的 **公開 pricing 表**算成本——它已經是社群事實上的「LLM 價格表 source of truth」。
- 與 [[quantdinger]] 的 Agent Gateway：兩者哲學相同——**用 gateway 隔離 vendor key、提供 audit / scope / spend**。QuantDinger 是金融交易場景的 Agent Gateway、LiteLLM 是通用 LLM 場景的 Gateway。
- 與 [[cli-anything]]、[[tlc-agent-skills]]、[[mattpocock-skills]]：Skill / MCP 生態系越大，**MCP Gateway 需求越強**。LiteLLM 是這個需求的目前最強供給。
- 與 [[openhuman]]：OpenHuman 的「model routing」（推理 / 快速 / 視覺自動分流）本質就是 LiteLLM 提供的能力。OpenHuman 內部可能就是用 LiteLLM 包的（或抄 LiteLLM 邏輯）。
- 與 [[rag-anything]]：兩者是 LLM stack 的不同層——LiteLLM 是「**model abstraction**」、RAG-Anything 是「**knowledge abstraction**」。production 系統通常**兩個都用**。
- 與 [[ai-hedge-fund]]、[[daily-stock-analysis]]、[[fincept-terminal]]：這些量化工具都支援多 LLM provider，**底層大概率都是 LiteLLM 或它的精神替代**——「多 vendor 支援」已是 retail quant 標配。
- 與 [[harness-design-long-running-apps]]、[[boris-cherny-opus-4-7]]：Anthropic 自家 harness 設計強調「不要動態改 system prompt」、Cache rules everything——**這些原則靠 LiteLLM gateway 強制執行最容易**（在 gateway 層 enforce caching policy、prevent prompt 動態變動）。
- 對 startup：**任何想做「中介層」LLM 服務的 startup，都要先評估能否被 LiteLLM 取代**。如果你的差異化只是「我也支援 100 個 provider」，那你必輸 LiteLLM——除非有更深的垂直整合（如 [[quantdinger]] 走金融、[[fincept-terminal]] 走桌面）。
