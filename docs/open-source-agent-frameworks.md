---
date: "2026-04-14"
category: "AI Agent 框架"
card_icon: "material-compare-horizontal"
oneliner: "2026 年功能完善的開源 Agent 框架橫向比較：從 Dify 到 LangGraph 的選型指南"
---

# 開源 AI Agent 框架比較 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| Langfuse — AI Agent 比較 | [langfuse.com/blog](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) |
| Firecrawl — 最佳開源框架 | [firecrawl.dev/blog](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks) |
| Galileo — AutoGen vs CrewAI vs LangGraph | [galileo.ai/blog](https://galileo.ai/blog/autogen-vs-crewai-vs-langgraph-vs-openai-agents-framework) |
| Fungies — 2026 框架比較 | [fungies.io](https://fungies.io/ai-agent-frameworks-comparison-2026-langchain-crewai-autogen/) |
| 知乎 — 2025 開源 AI Agent 全景圖 | [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/p/1992410866923091778) |
| Shakudo — Top 9 AI Agent Frameworks | [shakudo.io/blog](https://www.shakudo.io/blog/top-9-ai-agent-frameworks) |

## 專案概述

2025-2026 年，開源 AI Agent 框架已從早期的「能動就好」進入功能分化與生產就緒的階段。全球 Agent 市場在 2025 年達到 78.4 億美元，預計 2030 年成長至 526.2 億美元。Gartner 預測 2026 年底 40% 企業應用將內建 Agent 功能。

本筆記橫向比較目前最具代表性的開源框架，從架構風格、功能完整度、社群活躍度到適用場景，協助判斷不同需求下的最佳選擇。

## 核心框架一覽

### GitHub 即時數據（2026-04-14）

| 框架 | ⭐ Stars | 語言 | License | 架構風格 |
|------|---------|------|---------|---------|
| **Dify** | 137,626 | TypeScript | Custom | Low-code 視覺化平台 |
| **AutoGen** | 57,055 | Python | CC-BY-4.0 | 事件驅動多 Agent 對話 |
| **CrewAI** | 48,813 | Python | MIT | 角色扮演協作 |
| **Agno** | 39,404 | Python | Apache-2.0 | 無狀態高效能 Runtime |
| **LangGraph** | 29,172 | Python | MIT | 有向圖狀態機 |
| **Mastra** | 22,971 | TypeScript | — | TypeScript-first 工作流 |
| **Google ADK** | 18,954 | Python | Apache-2.0 | 模組化階層式 Agent |

## 框架深度比較

### 架構與設計哲學

```
Dify        ─── 視覺化拖拉 → 適合非工程師快速建構
CrewAI      ─── 角色 + 任務 → 20 行啟動，最低門檻
Agno        ─── 無狀態 Runtime → 529x faster than LangGraph（官方宣稱）
LangGraph   ─── 有向圖 + 檢查點 → 最精細的流程控制
AutoGen     ─── GroupChat 對話 → 多 Agent 即時協作
Google ADK  ─── 階層式組合 → 多語言 + Google 生態整合
Mastra      ─── .then().branch().parallel() → JS/TS 團隊首選
```

### 功能矩陣

| 功能 | Dify | CrewAI | Agno | LangGraph | AutoGen | Google ADK | Mastra |
|------|------|--------|------|-----------|---------|------------|--------|
| Multi-Agent | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 視覺化 UI | ✅ 核心 | ❌ | ✅ 控制台 | ❌ | ✅ Studio | ✅ Web UI | ❌ |
| 記憶系統 | ✅ | ✅ | ✅ 多層 | ✅ 檢查點 | ⚠️ 記憶體 | ✅ Session | ✅ 四層 |
| RAG 內建 | ✅ | ⚠️ | ✅ | ❌ 需整合 | ❌ 需整合 | ⚠️ | ✅ |
| Human-in-the-Loop | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MCP 支援 | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| 串流輸出 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 雙向 | ✅ |
| Model-Agnostic | ✅ 數百 | ✅ | ✅ 23+ | ✅ | ✅ | ✅ LiteLLM | ✅ 81+ |
| 生產部署 | ✅ Docker | ⚠️ | ✅ FastAPI | ✅ LangServe | ⚠️ | ✅ Vertex AI | ✅ |
| Observability | ✅ 內建 | ⚠️ | ✅ 內建 | ✅ LangSmith | ⚠️ | ✅ | ✅ OTel |

> ✅ = 原生支援　⚠️ = 需額外設定或第三方整合　❌ = 不支援

### 效能與基準測試

| 框架 | Task Success Rate | 平均延遲 | 備註 |
|------|------------------|---------|------|
| LangGraph | 87% | — | GAIA benchmark 表現穩定 |
| CrewAI | 82% | 1.8s | 宣稱比 LangGraph 快 5.76x |
| Agno | — | — | 宣稱比 LangGraph 快 529x（啟動速度） |
| AutoGen | — | — | GAIA benchmark 領先（研究場景） |

### 學習曲線與上手成本

```
最低門檻 ◄──────────────────────────────────► 最高控制
  Dify   CrewAI   Agno   Mastra   ADK   AutoGen   LangGraph
  拖拉    20行    10行    中等     中等   中等       需理解圖論
```

## 各框架適用場景

### 🏢 Dify — 「不寫 code 也能做 Agent」

**最適合：** 產品經理、非技術團隊、快速 PoC

- 視覺化 workflow builder，拖拉即可建構 Agent
- 內建 RAG、Function Calling、ReAct 策略
- 支援數百個 LLM，Docker 一鍵部署
- **限制：** 複雜自訂邏輯受限於視覺化界面

### ⚙️ LangGraph — 「流程控制之王」

**最適合：** 需要精細流程控制的生產系統

- 有向圖（DAG）建模，支援條件分支、循環、回溯
- 內建 checkpointing + time travel，可隨時回到任意狀態
- LangSmith 深度整合，生產級 observability
- **真實案例：** Klarna 客服 bot 處理 2/3 客戶諮詢，年省 6000 萬美元
- **限制：** 學習曲線較高，需理解圖論概念

### 🎭 CrewAI — 「最直覺的多 Agent 協作」

**最適合：** 快速啟動多 Agent 專案、非技術背景開發者

- 角色扮演設計，每個 Agent 有明確職責
- Crews 模式（自主協作）+ Flows 模式（事件驅動）
- 60% Fortune 500 企業已採用
- **限制：** 複雜流程控制不如 LangGraph 精細

### 🚀 Agno — 「效能怪獸」

**最適合：** 高吞吐量、低延遲的生產環境

- 無狀態設計，水平擴展無上限
- FastAPI-based AgentOS，原生支援 session + 記憶 + 知識庫
- 100+ toolkits、23+ LLM providers
- 資料存在你自己的資料庫，完全可控
- **限制：** 較新的框架，社群生態仍在發展中

### 🤖 AutoGen — 「研究先鋒（正在轉型）」

**最適合：** 研究場景、需要 Agent 寫和執行 code

- 微軟研究院出品，GAIA benchmark 表現優異
- 2025/10 已與 Semantic Kernel 合併為 Microsoft Agent Framework
- 目前處於維護模式，GA 預計 2026 Q1
- **限制：** 正在經歷架構轉型，不建議新專案採用舊版

### 🌐 Google ADK — 「Google 生態系的最佳入口」

**最適合：** 已深度使用 Google Cloud 的團隊

- Python / TypeScript / Go / Java 四語言支援
- 內建雙向音視訊串流（獨家）
- 智慧 context 管理：自動過濾、摘要、lazy-load
- 可組合其他框架（LangGraph、CrewAI）作為工具
- **限制：** 最佳化針對 Gemini，其他模型需額外配置

### 📘 Mastra — 「TypeScript 開發者的 LangGraph」

**最適合：** JS/TS 技術棧的團隊

- `.then()` / `.branch()` / `.parallel()` 流暢的工作流 API
- 四層記憶系統（訊息歷史、工作記憶、語意回憶、RAG）
- 81+ LLM providers、2,436+ models
- **真實案例：** Replit Agent 3 任務成功率從 80% 提升至 96%
- **限制：** 僅限 TypeScript/JavaScript 生態

## 選型決策流程

```
你的團隊技術背景？
├── 非技術 / 低程式碼 → Dify
├── Python
│   ├── 需要精細流程控制？ → LangGraph
│   ├── 快速啟動多 Agent？ → CrewAI
│   ├── 追求極致效能？ → Agno
│   └── 深度 Google Cloud？ → Google ADK
├── TypeScript/JavaScript → Mastra
└── .NET / 微軟生態 → Microsoft Agent Framework (AutoGen 後繼)
```

## 目前限制 / 注意事項

1. **框架更迭快速** — AutoGen 合併、CrewAI 獨立於 LangChain、Agno 改名（原 Phidata），生態每 3-6 個月洗牌一次
2. **效能宣稱需謹慎** — Agno「529x faster」和 CrewAI「5.76x faster」的數字多來自特定 benchmark，實際生產表現取決於任務特性
3. **Lock-in 風險** — Google ADK 和 OpenAI SDK 在各自生態內最優，跨生態遷移成本高
4. **企業合規** — 只有 LangGraph 和 AutoGen 目前有企業級認證（SOC 2 等），其餘框架仍在追趕
5. **Stars ≠ 品質** — Dify 13.7 萬星但它是平台而非框架；真正的框架層比較應看 API 設計和生產案例

## 研究價值與啟示

### 關鍵洞察

1. **「框架」和「平台」的界線正在模糊** — Dify（平台）和 Agno（框架 + AgentOS + 控制台）代表了兩種收斂方向：要不往上走向 no-code，要不往下走向 infrastructure。純「框架」正被夾在中間。

2. **TypeScript Agent 生態正在崛起** — Mastra 被 Replit 和 Marsh McLennan 採用、Next.js 團隊背景（前 Gatsby）、拿到 Y Combinator 投資。Python 不再是 Agent 的唯一選擇，前端團隊現在有了一流的 Agent 框架。

3. **記憶系統成為關鍵差異化** — 所有框架都支援 multi-agent，真正的分水嶺是記憶管理。Mastra 的四層記憶、Agno 的「資料在你的資料庫」、LangGraph 的 checkpointing + time travel，各自代表不同的記憶哲學。

4. **「Model-Agnostic」已成標配，但深度不同** — 所有框架都宣稱支援多模型，但 Google ADK 對 Gemini 有明顯最佳化、LangGraph 對 OpenAI 整合最成熟。真正的 agnostic 需要看 fallback 和 routing 的設計。

5. **生產就緒的真正指標是 observability** — 有 LangSmith 的 LangGraph、有內建 tracing 的 Agno、有 OpenTelemetry 的 Mastra，比那些只有 `print()` 除錯的框架在生產環境中領先一個世代。

### 與其他專案的關聯

- 本站已有 [CrewAI](crewai.md)、[Google ADK](google-adk.md)、[OpenAI Agents SDK](openai-agents-sdk.md)、[LangGraph Multi-Agent](langgraph-multi-agent.md) 等個別框架深度筆記，本文提供橫向比較視角
- [Claude Agent SDK](claude-agent-sdk.md) 作為閉源 SDK 未列入比較，但其 orchestration 設計可參照 LangGraph 的有向圖模型
- [Agent Orchestrator](agent-orchestrator.md) 探討的 multi-agent 協調問題，在本文各框架中有不同的解法
- 量化交易分類中的 [TradingAgents](tradingagents.md) 使用 LangGraph 作為底層框架，是 LangGraph 生產應用的具體案例
