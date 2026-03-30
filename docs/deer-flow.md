---
date: "2026-03-30"
category: "AI Agent 框架"
card_icon: "material-file-document-outline"
oneliner: ""
---
# DeerFlow 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) |
| 官方網站 | [deerflow.tech](https://deerflow.tech) |
| DEV Community 深度分析 | [DeerFlow 2.0: What It Is, How It Works](https://dev.to/arshtechpro/deerflow-20-what-it-is-how-it-works-and-why-developers-should-pay-attention-3ip3) |
| VentureBeat | [What enterprises should know about DeerFlow](https://venturebeat.com/orchestration/what-is-deerflow-and-what-should-enterprises-know-about-this-new-local-ai) |
| DeepWiki | [bytedance/deer-flow](https://deepwiki.com/bytedance/deer-flow) |
| SitePoint | [Managing Long-Running Autonomous Tasks](https://www.sitepoint.com/deerflow-deep-dive-managing-longrunning-autonomous-tasks/) |
| MarkTechPost（v1） | [ByteDance Open-Sources DeerFlow](https://www.marktechpost.com/2025/05/09/bytedance-open-sources-deerflow-a-modular-multi-agent-framework-for-deep-research-automation/) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 開發公司 | **ByteDance（字節跳動）** |
| 全名 | Deep Exploration and Efficient Research Flow |
| Stars | 53.2K（截至 2026-03-30） |
| Forks | 6.4K |
| 語言 | Python 3.12+ / Node.js 22+ |
| 授權 | MIT |
| 版本 | v2.0（2026-02-28 發布，完全重寫，與 v1 不共用程式碼） |

DeerFlow 是一套**開源 SuperAgent 執行框架（harness）**，能編排 sub-agent、記憶體、沙箱來處理從幾分鐘到數小時的複雜任務——研究、寫程式、產生內容。

> 關鍵定位：DeerFlow 不是「框架」（framework），而是「執行框架」（harness）——batteries included, fully extensible。不需要自己接線，開箱就是一個完整的 agent runtime。

v2.0 發布當天（2026-02-28）登上 GitHub Trending 全語言 #1。

---

## 版本演進

| 版本 | 時間 | 定位 |
|------|------|------|
| v1.0 | 2025-05 | **Deep Research 框架** — 專注自動化資料收集與摘要，multi-agent 深度研究 |
| v2.0 | 2026-02-28 | **SuperAgent Harness** — 完全重寫，從研究工具進化為通用執行框架 |

**為何重寫**：v1 做研究做得好，但開發者開始把它硬掰去做資料管線、建 dashboard、自動化內容工作流。ByteDance 團隊意識到 DeerFlow 不只是研究工具，而是一個等待被完善的「執行框架」。

v1 仍在 `1.x` branch 維護，但主力開發已完全轉向 v2。

---

## 核心架構

```
使用者輸入（Web UI / IM Channel / API）
    │
    ▼
┌──────────────────────────────────┐
│  Lead Agent（單一 LangGraph agent）│
│  make_lead_agent(config)          │
│  ├─ 動態模型選擇（thinking + vision）│
│  ├─ 9 個 Middleware chain         │
│  └─ Tool 系統                     │
│     ├─ Sandbox tools              │
│     ├─ MCP tools（OAuth 支援）     │
│     ├─ Community tools            │
│     └─ Built-in tools             │
└────────────┬─────────────────────┘
             │  分解任務、決定並行策略
             ▼
    ┌────────┼────────┐
    ▼        ▼        ▼
Sub-Agent  Sub-Agent  Sub-Agent
（scoped context, 獨立 tools, 終止條件）
    │        │        │
    ▼        ▼        ▼
┌─────────────────────────┐
│  Sandbox（隔離執行環境）   │
│  ├─ Local                │
│  ├─ Docker container     │
│  └─ Kubernetes pod       │
│  每個任務有完整 filesystem：│
│  skills/ workspace/      │
│  uploads/ outputs/       │
└─────────────────────────┘
             │
             ▼
    結構化結果彙整
    （報告 / 網站 / 簡報 / 程式碼）
```

### 設計哲學

DeerFlow 與 LangGraph、CrewAI、AutoGen 的差異在於：**那些是積木，DeerFlow 是成品**。它內建了預設執行模型、Skills、沙箱和記憶體層，開發者用 YAML 設定就能啟動，不需要寫 orchestration 程式碼。代價是繼承了框架的架構約束。

---

## 六大核心能力

### 1. Skills & Tools

Skills 是 Markdown 格式的結構化工作流定義，描述最佳實踐和支援資源。漸進式載入，只在需要時載入相關 skill，維持 context window 可控。

內建 Skills：
- Deep web research
- Report generation
- Slide deck creation
- Web page generation
- Image/video generation

支援 Claude Code 整合。

### 2. Sub-Agents

Lead agent 可即時 spawn 多個特化 sub-agent，每個有：
- 獨立 scoped context（避免 context 互相汙染）
- 專屬 tools
- 明確終止條件

可並行執行，適合 fan-out / fan-in 模式（例：研究任務分散 12 個 sub-agent 各探索不同角度，最終匯總成一份報告）。

### 3. Sandbox Execution

每個任務在隔離環境中執行：

| 模式 | 說明 |
|------|------|
| Local | 直接在本機執行 |
| Docker | 隔離容器，完整 filesystem + bash terminal |
| Kubernetes | 透過 provisioner 建立 pod |

這是**真正的程式碼執行**，不是模擬——agent 產生的是可下載、可使用的輸出物。

### 4. Context Engineering

9 個 middleware chain 處理 cross-cutting concerns：
- 動態模型選擇
- Thinking / vision 支援
- Prompt 管理

### 5. Long-Term Memory

- 以 `memory.json` 儲存事實，帶 confidence score
- 短期 + 長期記憶，跨 session 建立使用者 profile
- 更新透過 debounced queue 非同步處理，不阻塞主執行緒
- Gateway 管理記憶體存取

> **注意**：agent memory 仍是未解問題。不要假設它會在正確時機回憶正確的事——需要針對特定場景測試驗證。

### 6. IM Channels（訊息閘道）

| 平台 | 模式 |
|------|------|
| Telegram | Long-polling |
| Slack | Socket Mode |
| Feishu / Lark | WebSocket |

原生整合，不需額外開發 bot。

---

## 安裝與設定

### Docker（推薦）

```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make config        # 生成 config.yaml + .env
make docker-init
make docker-start  # 自動偵測 sandbox 模式
```

### 本機開發

```bash
make check    # 驗證 Node.js 22+, pnpm, uv, nginx
make install  # 安裝依賴
make dev      # 啟動所有服務
```

存取：`http://localhost:2026`

### 模型設定（config.yaml）

```yaml
models:
  - name: gpt-4
    display_name: GPT-4
    use: langchain_openai:ChatOpenAI
    model: gpt-4
    api_key: $OPENAI_API_KEY
```

支援 OpenAI、Claude、DeepSeek、Doubao、Kimi、OpenRouter 等。

ByteDance 推薦模型：**Doubao-Seed-2.0-Code**、**DeepSeek v3.2**、**Kimi 2.5**。

### 可觀測性

- LangSmith 整合（選用）：啟用 tracing 即可

---

## 典型使用場景

| 場景 | 說明 |
|------|------|
| 自動化研究 | 並行 sub-agent 探索不同角度，匯總成結構化報告 |
| 資料管線 | 在沙箱中執行 ETL script |
| 內容產生 | 從 prompt 生成完整簡報 / 網頁 / 影片 |
| 全端 scaffolding | 從需求描述建立完整應用骨架 |
| 競品分析 | 多 sub-agent 並行研究不同競品 |

---

## 與其他框架比較

| 面向 | DeerFlow 2.0 | LangGraph | CrewAI | AutoGen |
|------|-------------|-----------|--------|---------|
| **定位** | 成品 harness（batteries included） | 底層積木（build your own） | 角色扮演多 agent | 對話式多 agent |
| **沙箱** | 內建（Local/Docker/K8s） | 無 | 無 | 有（code executor） |
| **記憶體** | 內建長期記憶 + confidence score | 需自建 | 有 | 需自建 |
| **Skills** | Markdown-based，漸進載入 | 無 | 無 | 無 |
| **IM 整合** | Telegram/Slack/Feishu 原生 | 無 | 無 | 無 |
| **部署** | Docker/K8s，make 一鍵啟動 | 需自行包裝 | 需自行包裝 | 需自行包裝 |
| **LLM 支援** | 多廠商 YAML 設定 | 多廠商 | 多廠商 | 多廠商 |
| **彈性** | 中（繼承架構約束） | 高 | 中 | 高 |

---

## 限制與注意事項

- **安全**：生產環境需容器加固、網路 egress 限制；沙箱預設信任度高
- **模型要求**：任務分解需要強指令遵循能力，小型本地模型可能無法勝任 orchestration
- **ByteDance 背景**：在某些地區/企業可能觸發額外合規審查
- **記憶體可靠性**：架構設計周全但實際表現不穩定，需逐案驗證
- **v2 成熟度**：2026-02 才發布的完全重寫，生態和文件仍在快速演進中
- **資源消耗**：多 sub-agent + 沙箱 = 較高的運算和 token 成本

---

## 成長數據

| 時間點 | Stars |
|--------|-------|
| 2026-02-28（v2 發布） | GitHub Trending #1 |
| 30 天後（~2026-03-30） | 53.2K |

---

## 研究價值與啟示

### 關鍵洞察

1. **Harness > Framework**：DeerFlow 最重要的設計決策是選擇做「成品」而非「積木」。開發者不想從零組裝 agent——他們想要一個能跑的系統，然後在上面客製化。這與 gstack/Superpowers 的「skill plugin」路線不同：DeerFlow 提供完整 runtime，gstack/Superpowers 強化已有的 agent。

2. **沙箱是真正執行 agent 的必要條件**：DeerFlow 給每個任務一台「虛擬電腦」（filesystem + bash + 隔離），這是從「建議程式碼」到「真正執行程式碼」的關鍵基礎設施。沒有沙箱，agent 只能停留在 suggestion 層。

3. **IM Channel 原生整合是差異化**：直接透過 Telegram/Slack/Feishu 與 agent 對話，不需要開 Web UI。這對企業部署特別有價值——agent 就在團隊已有的溝通管道中。

4. **v1→v2 的演進說明了 agent 工具的通用化趨勢**：從「研究專用」到「通用執行框架」，因為使用者會把工具推向它設計以外的用途。如果你的工具夠好，使用者會自己找到新場景。

5. **ByteDance 的開源策略**：透過推薦 Doubao/DeepSeek/Kimi 等中國模型（同時支援 OpenAI/Claude），DeerFlow 同時服務中國和全球開發者市場。整合 InfoQuest（BytePlus 搜尋工具）也是生態綁定策略。

6. **53K stars 的速度（1 個月）**：與 gstack（19 天 56K）和 Superpowers（6 個月 124K）相比，DeerFlow 的成長介於兩者之間，反映了字節跳動的品牌效應和 agent runtime 的市場需求。

### 與 Fluffy 的潛在關聯

- **架構參考**：DeerFlow 的 Lead Agent → Sub-Agent fan-out 模式可參考用於 Fluffy Agent Core 的任務分解
- **沙箱設計**：Docker/K8s sandbox 模式可作為 Fluffy 執行不受信任程式碼的參考
- **IM 整合**：Telegram/Slack/Feishu 的原生整合模式可參考用於 Fluffy 的客戶溝通管道
- **記憶體系統**：confidence score + debounced async update 的設計可參考
