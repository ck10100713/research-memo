---
date: "2026-03-30"
category: "Coding Agent 工具"
card_icon: "material-code-braces-box"
oneliner: "LangChain 開源的企業內部 Coding Agent 框架——複製 Stripe/Ramp/Coinbase 的內部架構（8.8K stars）"
---
# Open SWE 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) |
| 官方部落格 | [Introducing Open SWE](https://blog.langchain.com/introducing-open-swe-an-open-source-asynchronous-coding-agent/) |
| DeepWiki | [langchain-ai/open-swe](https://deepwiki.com/langchain-ai/open-swe) |
| DevOps.com 評析 | [Open SWE Captures the Architecture](https://devops.com/open-swe-captures-the-architecture-that-stripe-coinbase-and-ramp-built-independently-for-internal-coding-agents/) |

## 專案概述

| 項目 | 數值 |
|------|------|
| Stars | 8,842 |
| Forks | 1,023 |
| Language | Python |
| License | MIT |
| 最近 commit | 2026-03-30 |

Open SWE 是 LangChain 官方推出的**企業內部 Coding Agent 框架**。它不是又一個 coding agent，而是把 Stripe（Minions）、Ramp（Inspect）、Coinbase（Cloudbot）三家頂級公司獨立開發的內部 coding agent 架構**抽象成一套開源框架**。

核心定位：讓任何工程團隊都能在 10 分鐘內部署一個連接 Slack/Linear/GitHub 的自主 coding agent，在雲端沙箱中執行任務、自動開 PR。

## 核心架構

```
Slack / Linear / GitHub（觸發）
         │
         ▼
┌─────────────────────────────────────┐
│  Open SWE（LangGraph + Deep Agents）  │
├─────────────────────────────────────┤
│  Context Engineering                 │
│  • AGENTS.md（repo 級規則）           │
│  • Issue/Thread 完整上下文            │
├─────────────────────────────────────┤
│  Orchestration                       │
│  • Subagent spawning（task tool）     │
│  • Middleware hooks                   │
│    - check_message_queue（即時追加訊息）│
│    - open_pr_if_needed（安全網）       │
│    - ToolErrorMiddleware              │
├─────────────────────────────────────┤
│  Sandbox（隔離雲端環境）              │
│  • Modal / Daytona / Runloop / 自訂   │
│  • 每個 task 獨立沙箱，平行執行       │
├─────────────────────────────────────┤
│  Tools（~15 個，精選非堆積）          │
│  execute, fetch_url, http_request,   │
│  commit_and_open_pr, linear_comment, │
│  slack_thread_reply + Deep Agents 內建│
└─────────────────────────────────────┘
         │
         ▼
    GitHub Draft PR
```

### 與 Stripe/Ramp/Coinbase 的對比

| 決策 | Open SWE | Stripe Minions | Ramp Inspect | Coinbase Cloudbot |
|------|---------|----------------|--------------|-------------------|
| Harness | Composed（Deep Agents） | Forked（Goose） | Composed（OpenCode） | 從零打造 |
| Sandbox | 可插拔 | AWS EC2 | Modal | 內部方案 |
| Tools | ~15 精選 | ~500 精選 | OpenCode SDK | MCPs + Skills |
| 觸發 | Slack/Linear/GitHub | Slack + 按鈕 | Slack/Web/Chrome | Slack-native |
| 驗證 | Prompt + PR 安全網 | 3 層驗證 | DOM 視覺驗證 | Agent councils |

### 七大設計原則

1. **Compose, Don't Fork** — 基於 Deep Agents 組合，保留升級路徑
2. **Isolate First** — 沙箱內給完整權限，沙箱外零存取
3. **Curate, Don't Accumulate** — 工具寧少勿多（Stripe 教訓）
4. **AGENTS.md** — repo 級規則注入（等同 CLAUDE.md）
5. **Middleware > Prompt** — 關鍵步驟用確定性 middleware 兜底
6. **Meet Engineers Where They Are** — Slack/Linear/GitHub 三入口
7. **Message Mid-Run** — 執行中可追加指令，不需等完再重來

## 快速開始

```bash
# 安裝
pip install open-swe

# 設定 GitHub App、LangSmith、Slack/Linear trigger
# 詳見 INSTALLATION.md

# 啟動
open-swe serve
```

支援的沙箱：Modal、Daytona、Runloop、LangSmith，或自訂。

## 目前限制與注意事項

1. **依賴 LangGraph + Deep Agents** — 框架套框架，debug 時需要理解兩層抽象
2. **沙箱成本** — 每個 task 獨立雲端沙箱，平行跑時計費可觀
3. **驗證層薄** — 目前只有 prompt-driven + PR 安全網，沒有 Stripe 的 3 層驗證或 Ramp 的 DOM 視覺檢查
4. **模型依賴** — 預設用 Claude Opus 4.6，其他模型效果未驗證

## 研究價值與啟示

### 關鍵洞察

1. **「企業 coding agent 三巨頭收斂」是真趨勢** — Stripe、Ramp、Coinbase 獨立開發的架構驚人地相似（沙箱隔離 + Slack 觸發 + 精選工具 + PR 自動化）。Open SWE 把這個收斂點開源，是 LangChain 最聰明的產品策略之一。

2. **Middleware > Prompt 是 production coding agent 的關鍵洞察** — `open_pr_if_needed` 這個 middleware 本身就值得研究：它不信任 LLM 會記得開 PR，用確定性邏輯兜底。這比「在 system prompt 裡多說幾次」可靠得多。

3. **AGENTS.md 是 CLAUDE.md 的通用化** — Open SWE 把 Anthropic 的 CLAUDE.md 概念泛化成 AGENTS.md，讓任何 agent 都能讀取 repo 級規則。

### 與其他專案的關聯

- **vs. [Agent Orchestrator](agent-orchestrator.md)** — 同為多 agent coding 控制平面，但 Agent Orchestrator 偏向 CI/review 閉環，Open SWE 偏向 Slack/Linear 觸發 + 沙箱隔離。
- **vs. [LangGraph Supervisor](langgraph-supervisor-py.md)** — Supervisor 是 Open SWE 底層用到的多 agent 協調模式之一。
- **vs. [LangGraph Swarm](langgraph-swarm-py.md)** — Swarm 是另一種多 agent 模式，Open SWE 的子 agent 機制更接近 swarm 的去中心化 handoff。
- **vs. [Everything Claude Code](everything-claude-code.md)** — Claude Code 是個人開發者的終端工具，Open SWE 是企業團隊的非同步 Slack bot。定位互補。
