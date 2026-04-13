---
date: "2026-04-13"
category: "Coding Agent 工具"
card_icon: "material-account-group"
oneliner: "開源 Managed Agents 平台，把 Coding Agent 當隊友管理 — 派工、追蹤、技能複用"
---

# Multica 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [multica-ai/multica](https://github.com/multica-ai/multica) |
| 官網 | [multica.ai](https://multica.ai) |
| Cloud 版 | [multica.ai/app](https://multica.ai/app) |
| 自架指南 | [SELF_HOSTING.md](https://github.com/multica-ai/multica/blob/main/SELF_HOSTING.md) |
| 評論文章 | [MOGE.ai 介紹](https://moge.ai/product/multica) |

**專案狀態：** ⭐ 9.9K+ stars · TypeScript + Go · 2026-01 創建 · 活躍開發中

## 專案概述

Multica 的核心理念是：**「你下一批 10 個新員工不會是人類。」** 它是一個開源的 Managed Agents 平台，讓 Coding Agent（Claude Code、Codex、OpenClaw、OpenCode、Hermes）像真正的隊友一樣運作——出現在看板上、接收任務分派、自主執行工作、回報進度與阻礙、並將解決方案積累為可複用的技能。

這解決了目前 Coding Agent 使用上的核心痛點：**缺乏統一的專案管理與經驗積累機制。** 現狀是每次都要手動貼 prompt、盯著執行、跨 agent 重複解決相同問題。Multica 把這些碎片化的操作包裝成一個完整的生命週期管理系統。

## 核心功能

| 功能 | 說明 |
|------|------|
| **Agents as Teammates** | Agent 有個人 profile，出現在看板上，可評論、建 issue、主動回報 blocker |
| **Autonomous Execution** | 完整任務生命週期：enqueue → claim → start → complete/fail，WebSocket 即時串流進度 |
| **Reusable Skills** | 每個解決方案自動成為可複用技能，部署、遷移、code review 都能跨 agent 累積 |
| **Unified Runtimes** | 一個 dashboard 管理所有算力——本地 daemon 與雲端 runtime，自動偵測可用 CLI |
| **Multi-Workspace** | 按團隊隔離工作空間，各自獨立的 agent、issue、設定 |

### 支援的 Agent Runtime

| Agent CLI | 狀態 |
|-----------|------|
| Claude Code (`claude`) | ✅ 支援 |
| Codex (`codex`) | ✅ 支援 |
| OpenClaw (`openclaw`) | ✅ 支援 |
| OpenCode (`opencode`) | ✅ 支援 |
| Hermes (`hermes`) | ✅ 支援 |

## 技術架構

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Next.js 16     │────>│   Go Backend     │────>│  PostgreSQL 17   │
│   (App Router)   │<────│  (Chi + WS)      │<────│  (+ pgvector)    │
│   Web Dashboard  │     │  REST + WebSocket │     │  主要資料庫       │
└──────────────────┘     └────────┬─────────┘     └──────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │      Agent Daemon          │
                    │  (本地機器 / 雲端 Runtime)   │
                    │  自動偵測 PATH 上的 CLI      │
                    │  Claude / Codex / OpenClaw  │
                    └────────────────────────────┘
```

| 層級 | 技術棧 |
|------|--------|
| Frontend | Next.js 16 (App Router) |
| Backend | Go (Chi router, sqlc, gorilla/websocket) |
| Database | PostgreSQL 17 + pgvector |
| Agent Runtime | 本地 daemon，偵測並執行 Coding Agent CLI |
| 部署 | Docker Compose（自架）/ Multica Cloud |

### Runtime 架構的設計

Runtime 是 Multica 的核心抽象——一個「可執行 Agent 任務的計算環境」。可以是開發者的本機（透過 daemon）或雲端實例。每個 Runtime 會回報可用的 Agent CLI，讓 Multica 知道如何路由工作。這意味著：

- **團隊成員各自的機器都是 Runtime**，各自安裝不同的 Agent CLI
- 任務分派時 Multica 根據 Runtime 的能力自動路由
- 即時監控每個 Runtime 的狀態與負載

## 快速開始

### Cloud 版（最快）

```bash
# 安裝 CLI
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash

# 登入 + 啟動 daemon
multica login          # 開瀏覽器驗證
multica daemon start   # 啟動本地 Agent Runtime
```

### 自架版

```bash
# 一鍵安裝（需要 Docker）
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash -s -- --local

# 或手動
git clone https://github.com/multica-ai/multica.git
cd multica
make selfhost          # 自動建 .env、生成 JWT_SECRET、啟動 Docker Compose
```

自架版登入：開啟 `http://localhost:3000`，任意 email + 驗證碼 `888888`（非 production 環境）。

### CLI 常用指令

| 指令 | 說明 |
|------|------|
| `multica setup` | 一鍵設定（configure + login + start daemon） |
| `multica daemon start/stop/status` | 管理本地 Agent daemon |
| `multica issue list/create` | 查看、建立 issue |
| `multica config local` | 切換至自架 server |
| `multica update` | 更新 CLI |

### 使用流程

1. `multica login` + `multica daemon start` → 連接 Runtime
2. Web App → Settings → Runtimes 確認機器已上線
3. Settings → Agents → 建立 Agent（選 Runtime + Provider）
4. 建 issue → 分派給 Agent → Agent 自動接手執行

## 目前限制 / 注意事項

- **License 未明確宣告** — GitHub 顯示 `NOASSERTION`，商用前需確認授權條款
- **Agent 支援範圍有限** — 目前僅支援 5 種 CLI-based Coding Agent，不支援 API-only 的 LLM
- **Skill 系統的品質取決於累積量** — 冷啟動時缺乏可用技能，需要團隊持續使用才能發揮複利效應
- **自架需要 Docker** — 對部分企業環境可能是限制
- **pgvector 依賴** — 技能搜尋可能依賴向量相似度，需要 PostgreSQL 17 + pgvector 擴展
- **Agent 執行在本機** — 目前主要是本地 daemon 模式，雲端 Runtime 的生產級部署文件較少

## 研究價值與啟示

### 關鍵洞察

1. **「Agent 即隊友」是正確的產品抽象層級。** Multica 不試圖做另一個 Agent 框架（CrewAI、LangGraph 那一層），而是在更上層做「Agent 的專案管理」——用人類已熟悉的看板、issue、assignee 等概念來管理 Agent。這降低了認知負擔，也讓 human-agent 混合團隊成為可能。

2. **Skill 複用是 Coding Agent 規模化的關鍵瓶頸。** 目前 Coding Agent 的最大問題不是單次執行能力，而是**經驗無法跨任務、跨 Agent 累積**。Multica 的 Skill Library 讓每個 Agent 解決的問題都成為團隊資產——這是從「每次從零開始」到「持續複利」的關鍵轉變。

3. **Vendor-neutral Runtime 抽象的策略價值。** 同時支援 Claude Code、Codex、OpenClaw、OpenCode 的設計，讓團隊不被綁定在單一 AI 供應商。在 AI 能力快速迭代的時期，這種中立層特別重要——今天最強的 Agent 三個月後可能不是。

4. **Go + Next.js 的技術選型反映了「基礎設施」定位。** 不用 Python（Agent 框架的主流語言），而用 Go 做後端——追求的是低延遲、高並發的基礎設施品質，而非快速原型。sqlc（而非 ORM）的選擇也體現了性能優先的工程取向。

5. **WebSocket 即時串流是 Agent 管理的必要條件。** 跟傳統專案管理工具不同，Agent 任務的進度是秒級更新的。Multica 用 gorilla/websocket 做即時串流，這在架構上就決定了它不是給「5 分鐘看一次」的經理用的，而是給「需要即時感知 Agent 狀態」的開發者用的。

### 與其他專案的關聯

- **vs Agent Orchestrator / Claude Cowork Dispatch：** 這些是更底層的 Agent 調度工具，Multica 則提供完整的 UI + 專案管理層。可以想像 Multica 內部使用類似的調度邏輯，但包裝成非技術人員也能操作的介面。
- **vs OpenHarness / Open SWE：** 這些聚焦在 Agent 的執行環境與 benchmark，Multica 則聚焦在「如何把 Agent 整合進團隊工作流程」。
- **vs Agency Agents / Page Agent：** 這些是單一 Agent 的增強工具，Multica 是多 Agent 的管理平台——層級不同，互補而非競爭。
- **對 Fluffy 生態的啟示：** Multica 的 Skill 複用機制與 Runtime 抽象層，對 fluffy-agent-core 設計多 Agent 協作有參考價值——特別是「如何讓 Agent 的解決方案跨任務累積」這個問題。
