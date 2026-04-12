---
date: "2026-04-12"
category: "學習資源"
card_icon: "material-book-open-page-variant"
oneliner: "18 章深度逆向工程 Claude Code 架構 — 從 npm source map 解析 2,000 個 TypeScript 檔案"
---

# Claude Code from Source — 逆向工程架構全書

## 資料來源

| 項目 | 連結 |
|------|------|
| 線上閱讀 | [claude-code-from-source.com](https://claude-code-from-source.com/) |
| GitHub Repo | [alejandrobalderas/claude-code-from-source](https://github.com/alejandrobalderas/claude-code-from-source) |
| Ch.1 架構章 | [ch01-architecture.md](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch01-architecture.md) |
| Ch.18 結語 | [ch18-epilogue.md](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch18-epilogue.md) |

## 專案概述

這是一本完全由 AI 生成的技術書籍，深度解析 Anthropic Claude Code 的內部架構。當 Anthropic 將 Claude Code 發布到 npm 時，`.js.map` source map 檔案包含了完整的原始 TypeScript 原始碼（`sourcesContent` 欄位），共計近 2,000 個檔案。作者 Alejandro Balderas 率領 **36 個 AI Agent** 在 4 個階段（探索→分析→寫作→審閱修訂）完成了這本 18 章、約 400 頁的技術書——整個過程僅耗時約 6 小時。

**重要聲明**：書中不包含任何 Claude Code 原始碼，所有程式碼區塊都是原創的虛擬碼（使用不同的變數名稱），僅用於說明架構模式。

截至研究時，GitHub repo 已累積 1,045 stars。

## 全書結構：18 章 7 大部分

### Part I：Foundations（基礎）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 1 | The Architecture of an AI Agent | **6 大抽象**：Query Loop、Tool System、Tasks、State、Memory、Hooks |
| 2 | Starting Fast — The Bootstrap Pipeline | 5 階段初始化、模組層級 I/O 平行化、信任邊界 |
| 3 | State — The Two-Tier Architecture | Bootstrap singleton（~80 欄位）+ AppState store（34 行 Zustand） |
| 4 | Talking to Claude — The API Layer | 多 provider client、prompt cache、streaming、錯誤復原 |

### Part II：The Core Loop（核心迴圈）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 5 | The Agent Loop | `query.ts` 1,730 行深度解析、4 層壓縮、token 預算 |
| 6 | Tools — From Definition to Execution | Tool 介面 45 個成員、14 步執行 pipeline、7 種權限模式 |
| 7 | Concurrent Tool Execution | 分區演算法、streaming executor、投機執行 |

### Part III：Multi-Agent Orchestration（多 Agent 編排）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 8 | Spawning Sub-Agents | AgentTool、15 步 runAgent 生命週期 |
| 9 | Fork Agents and the Prompt Cache | Byte-identical prefix 技巧、cache 共享、節省 ~95% input token |
| 10 | Tasks, Coordination, and Swarms | Task 狀態機、coordinator 模式、swarm messaging |

### Part IV：Persistence and Intelligence（持久化與智能）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 11 | Memory — Learning Across Conversations | 檔案式記憶、4 種分類法、LLM recall、陳舊處理 |
| 12 | Extensibility — Skills and Hooks | 兩階段 skill 載入、27 個生命週期 hook 事件 |

### Part V：The Interface（介面層）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 13 | The Terminal UI | 自訂 Ink fork、渲染管線、double-buffer |
| 14 | Input and Interaction | Key parsing、keybindings、chord 支援、vim 模式 |

### Part VI：Connectivity（連接性）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 15 | MCP — The Universal Tool Protocol | 8 種 transport、OAuth for MCP、tool wrapping |
| 16 | Remote Control and Cloud Execution | Bridge v1/v2、CCR、upstream proxy |

### Part VII：Performance Engineering（效能工程）

| 章 | 標題 | 核心內容 |
|----|------|---------|
| 17 | Performance — Every Millisecond and Token Counts | 啟動、context window、prompt cache、渲染、搜尋 |
| 18 | Epilogue — What We Learned | 5 大架構賭注、可轉移的模式、Agent 的未來 |

## 6 大核心抽象

```
User → REPL (Ink/React)
         ↓
    Query Loop ←──── Memory (CLAUDE.md, MEMORY.md)
    (async generator,         ↕ LLM-powered recall
     yields Messages)
         ↓↑
    Tool System ←──── Hooks (27 lifecycle events)
    (40+ tools,              can block/modify
     Tool<I,O,P>)
         ↓
    Tasks (Sub-agents, state machines)
         ↓
    State Layer (Bootstrap STATE + AppState store)
```

| 抽象 | 實作 | 規模 | 角色 |
|------|------|------|------|
| Query Loop | `query.ts` | ~1,730 行 | 系統心跳——streaming、tool 執行、context 管理、錯誤復原 |
| Tool System | `Tool.ts` + 40+ 工具 | 介面 45 成員 | 14 步執行管線，每個工具自描述（名稱、schema、權限、並發安全性） |
| Tasks | `Task.ts` | 狀態機 | pending → running → completed/failed/killed |
| State | 雙層架構 | ~80 欄位 + 34 行 store | 基礎設施（STATE）不觸發 re-render；UI（AppState）響應式更新 |
| Memory | `memdir/` | 3 層 | 專案級（CLAUDE.md）、使用者級（MEMORY.md）、團隊級（symlink） |
| Hooks | `hooks/` | 27 事件 × 4 執行類型 | 可阻擋 tool 執行、修改輸入、注入上下文、短路 query loop |

## 10 個關鍵設計模式

| # | 模式 | 說明 |
|---|------|------|
| 1 | **AsyncGenerator as agent loop** | yield Messages、typed Terminal return、自然背壓和取消 |
| 2 | **Speculative tool execution** | 模型 streaming 期間先啟動唯讀工具，不等回應完成 |
| 3 | **Concurrent-safe batching** | 依安全性分區工具：reads 平行、writes 序列化 |
| 4 | **Fork agents for cache sharing** | 子 Agent 共享 byte-identical prompt prefix，節省 ~95% input token |
| 5 | **4-layer context compression** | snip → microcompact → collapse → autocompact，逐層減輕 |
| 6 | **File-based memory with LLM recall** | Sonnet side-query 選取相關記憶，非關鍵字匹配 |
| 7 | **Two-phase skill loading** | 啟動時只讀 frontmatter，呼叫時才載入完整內容 |
| 8 | **Sticky latches for cache stability** | beta header 一旦送出就不撤回，避免 mid-session cache miss |
| 9 | **Slot reservation** | 8K 預設輸出上限，命中時升級到 64K（99% 請求省 context） |
| 10 | **Hook config snapshot** | 啟動時凍結設定，防止 runtime injection 攻擊 |

## 5 大架構賭注（Ch.18 結語）

| 賭注 | 選擇 | 替代方案 | 結果 |
|------|------|---------|------|
| Generator Loop | 單一 `query()` async generator（1,700 行） | 分散式 callback graph | 勝出：所有互動通過一個函數，10 個終止狀態由型別系統保證窮舉處理 |
| File-Based Memory | 純 Markdown 檔案 | SQLite / Vector DB / 雲端服務 | 勝出：使用者用 vim 開 `MEMORY.md` 就能看到 Agent 記住什麼——**外部可觀察性 > 查詢效能** |
| Self-Describing Tools | 每個 Tool 自帶 name/schema/permissions | 中央 tool registry | 勝出：MCP 工具透過同一介面成為一等公民，不需要額外 adapter 層 |
| Fork Agents | 共享 parent prompt cache 的 fork 子 Agent | 獨立 Agent + 對話摘要 | 勝出：背景記憶提取 Agent 因 cache 共享而成本微乎其微 |
| Hooks Over Plugins | 外部行程 + exit code + stdin/stdout | 行程內 plugin API | 勝出：行程隔離——plugin 可 crash host，hook 只 crash 自己 |

## 7 種權限模式

| 模式 | 行為 |
|------|------|
| `bypassPermissions` | 全部允許，不檢查（內部/測試用） |
| `dontAsk` | 全部允許但記錄，不提示使用者 |
| `auto` | LLM transcript classifier 決定允許/拒絕 |
| `acceptEdits` | 檔案編輯自動允許；其他 mutation 需提示 |
| `default` | 標準互動模式，使用者逐一核准 |
| `plan` | 唯讀模式，所有 mutation 被阻擋 |
| `bubble` | 升級決策到 parent agent（sub-agent 模式） |

## 這本書是怎麼做出來的

```
Phase 1：Exploration — 6 個平行 Agent 讀取所有原始碼檔案
Phase 2：Analysis   — 12 個 Agent 產出 494KB 原始技術文件
Phase 3：Writing    — 15 個 Agent 從零重寫為敘事型章節
Phase 4：Review     — 3 個編輯審閱者產出 900 行回饋 + 3 個修訂 Agent 套用修正
────────────────────────────────────────────────────────
總計：36 個 AI Agent，約 6 小時完成全書
```

## 目前限制

| 限制 | 說明 |
|------|------|
| 基於 source map 的靜態分析 | 無法觀察運行時行為、A/B 測試邏輯、伺服器端決策 |
| 時間快照 | 基於特定版本的 npm 發布，後續版本可能已大幅變更 |
| AI 生成的分析 | 36 個 Agent 的理解可能有偏差或錯誤推論 |
| 無官方背書 | Anthropic 未確認或否認分析的準確性 |
| 虛擬碼而非真實碼 | 所有程式碼區塊是原創虛擬碼，非直接引用 |
| 智財灰色地帶 | source map 是否構成「合理的逆向工程」有爭議 |

## 研究價值與啟示

### 關鍵洞察

1. **「36 個 AI Agent 6 小時寫完 400 頁技術書」本身就是一個里程碑**：這不只是一本關於 Claude Code 的書——它的製作過程（Exploration→Analysis→Writing→Review，36 個專職 Agent 平行工作）本身就是 multi-agent 系統的最佳展示。書的內容教你 Agent 架構，書的製作方式展示 Agent 架構。

2. **AsyncGenerator 是 Agent Loop 的正確抽象**：書中最有價值的洞見之一是：為什麼 Claude Code 選擇 async generator 而非 event emitter 或 callback。背壓（backpressure）、typed return value（10 種終止狀態）、`yield*` 組合性——這三個理由適用於任何人在建造 Agent 系統。

3. **「投機執行」改變了 Agent 的效能上限**：模型還在 streaming 回應時就先啟動唯讀工具（Read、Glob、Grep），等回應完成時結果已經拿到了。這是 CPU 投機執行概念在 AI Agent 中的應用——大多數 Agent 框架都是等模型回完才開始執行工具。

4. **Fork Agent + Prompt Cache 共享是成本控制的關鍵**：子 Agent 共享 parent 的 byte-identical prompt prefix，節省 ~95% input token。這讓「每次 query loop 結束後跑一個背景記憶提取 Agent」變得成本可忽略。沒有這個機制，Claude Code 的記憶系統根本不可能存在。

5. **Hooks Over Plugins 是安全性的根本選擇**：Plugin 在 host process 內執行（可 crash host、可洩漏記憶體），Hook 在獨立 process 執行（crash 只影響自己）。stdin/stdout + exit code 是 1971 年就穩定的 protocol——不需要維護 API 版本。這解釋了為什麼 Claude Code 選擇 hook 而非 plugin 作為擴展機制。

### 與其他專案的關聯

- **Claude Code Reverse (Yuyz0112)**：視覺化 Claude Code 的 LLM 互動，是「看」互動的工具；本書是「讀」架構的教材——互補
- **Claude Code Leak Breakdown (Kuberwastaken)**、**Claude Code Reconstructed (xorespesp)**：同為 Claude Code 逆向工程，但本書的深度和系統性遠超其他分析（18 章 vs 單篇文章）
- **OpenHarness (HKUDS)**：OpenHarness 用 11,700 行 Python 重現 98% Claude Code 工具能力。本書提供了「為什麼這樣設計」的理論基礎，OpenHarness 提供了「如何用另一種語言實作」的實踐
- **Analysis Claude Code**：同分類的架構分析筆記，但本書更完整，涵蓋 MCP、multi-agent、performance engineering 等面向
- **Learn Claude Code**：Learn Claude Code 教你「怎麼用」，本書教你「怎麼建」——對 Agent 開發者來說，後者更有價值
