---
date: "2026-03-30"
category: "AI Agent 框架"
card_icon: "material-account-group-outline"
oneliner: "LangGraph Supervisor 模式教學範例——Researcher/Writer/Reviewer 三 Agent 研究助理，附 human-in-the-loop"
---
# LangGraph Multi-Agent Research Assistant 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [melroyanthony/langgraph-multi-agent](https://github.com/melroyanthony/langgraph-multi-agent) |

## 專案概述

| 項目 | 數值 |
|------|------|
| Stars | 0 |
| Forks | 0 |
| Language | Python |
| License | — |
| 最近 commit | 2026-02-17 |

這是一個用 LangGraph Supervisor 模式實作的**多 Agent 研究助理教學專案**。三個專家 Agent（Researcher、Writer、Reviewer）由一個 Supervisor 協調，自動完成「搜尋 → 撰稿 → 審稿」的研究流程，支援最多 3 輪修訂迴圈。

雖然星數為零，但它是 LangGraph 官方 Supervisor + Swarm 庫的**最佳實踐參考實作**，展示了完整的 production 模式。

## 核心架構

```
Supervisor ──route──→ Researcher（web_search + summarize）
    │                      │ notes
    │                      ▼
    ├──route──→ Writer（draft / revise）
    │                      │ draft
    │                      ▼
    ├──route──→ Reviewer（critique + verdict）
    │                      │ ACCEPT / REVISE
    │                      ▼
    └──── complete ──→ FINISH
```

### Agent 角色

| Agent | 職責 | 工具 |
|-------|------|------|
| **Supervisor** | 檢查共享 state，路由到正確的專家 | LLM 路由（無工具） |
| **Researcher** | 網路搜尋 + 摘要整理 | `web_search`（Tavily）、`summarize` |
| **Writer** | 將研究筆記寫成報告，納入 reviewer 回饋修訂 | LLM 生成 |
| **Reviewer** | 審查稿件的正確性、清晰度、完整性，給出 ACCEPT 或 REVISE | LLM 評估 |

### 關鍵設計模式

1. **Supervisor routing** — 用 conditional edges 動態分派，避免 hard-coded pipeline
2. **Human-in-the-loop** — 用 LangGraph 的 `interrupt_before` 在 reviewer 前暫停，讓人類注入回饋
3. **Iterative refinement** — Writer-Reviewer 迴圈最多跑 3 次，確保輸出品質
4. **Multi-provider LLM** — 一個環境變數切換 OpenAI / Anthropic

### 技術棧

| 元件 | 技術 |
|------|------|
| 編排 | LangGraph |
| LLM | GPT-4o / Claude Sonnet 4.5 |
| 搜尋 | Tavily |
| 設定 | python-dotenv + pydantic |
| 套件管理 | uv |

## 目前限制與注意事項

1. **個人教學專案** — 0 stars、無社群維護，僅供學習參考
2. **Supervisor 延遲** — 每次路由都經 supervisor，比 swarm 模式多 ~40% 延遲
3. **固定 3 輪修訂** — 修訂次數硬編碼，無法根據品質動態調整
4. **單一搜尋來源** — 只用 Tavily，無法整合多個搜尋引擎

## 研究價值與啟示

### 關鍵洞察

1. **「Supervisor + 修訂迴圈」是研究類 Agent 的標準範本** — Researcher → Writer → Reviewer 的三角色分工 + iterative refinement 是最常見的 LangGraph 多 Agent 模式。這個專案是這個範本的最乾淨實作。

2. **Human-in-the-loop 的正確插入點** — 在 Reviewer 之前（而非之後）暫停讓人類介入，是因為人類回饋可以直接融入 reviewer 的評估，比等 reviewer 評完再覆蓋更高效。

3. **教學專案的價值在於「可讀性」而非「功能」** — 這個 repo 的專案結構（agents/config.py + graph.py + tools.py）和 Dockerfile 都是教科書等級的整潔。適合作為 LangGraph 多 Agent 的起始模板。

### 與其他專案的關聯

- **vs. [LangGraph Supervisor](langgraph-supervisor-py.md)** — 這個專案是 Supervisor 庫的**實作範例**，展示了 `create_supervisor` 的完整用法。
- **vs. [LangGraph Swarm](langgraph-swarm-py.md)** — 如果把 Supervisor 換成 Swarm handoff，Writer 可以直接把稿件交給 Reviewer，不需繞回 Supervisor，降低延遲。
- **vs. [Open SWE](open-swe.md)** — Open SWE 是 production 等級的 coding agent，這個是教學等級的 research agent。架構概念相同但複雜度差距巨大。
- **vs. [多 Agent 辯論會](multi-agent-debate.md)** — 辯論會用 Copilot SDK 實作多 Agent，這個用 LangGraph。都是「多個 Agent 互相協作」但框架不同。
