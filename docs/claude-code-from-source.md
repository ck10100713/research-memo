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

## 全書逐章翻譯與重點

---

### Part I：Foundations（基礎層）

#### Ch.1 AI Agent 的架構

> 原題：The Architecture of an AI Agent

傳統 CLI 是函數：接收參數、執行、退出。Agent CLI 打破這個契約——接收自然語言 prompt，自行決定用哪些工具、以什麼順序執行，循環直到任務完成。

**核心關鍵：6 大抽象**

| 抽象 | 比喻 | 關鍵數據 |
|------|------|---------|
| Query Loop | 心跳 | `query.ts` ~1,730 行，async generator，10 種終止狀態 |
| Tool System | 神經系統 | 40+ 工具，介面 45 個成員，14 步 pipeline |
| Tasks | 工作單元 | 狀態機 pending→running→completed/failed/killed |
| State | 雙層記憶 | Bootstrap STATE ~80 欄位 + AppState 34 行 Zustand |
| Memory | 持久上下文 | 3 層：專案(CLAUDE.md)→使用者(MEMORY.md)→團隊(symlink) |
| Hooks | 生命週期攔截器 | 27 事件 × 4 執行類型，可阻擋/修改/注入/短路 |

**Golden Path（黃金路徑）**：User 輸入 → REPL → Query Loop → Model API（streaming）→ StreamingToolExecutor（投機執行唯讀工具）→ Tool 執行 → 結果回饋 → 迴圈

**權限系統**：7 種模式（bypassPermissions → dontAsk → auto → acceptEdits → default → plan → bubble），解析鏈為 Hook rule → tool.checkPermissions → Permission mode 判斷

---

#### Ch.2 快速啟動——Bootstrap 管線

> 原題：Starting Fast — The Bootstrap Pipeline

**核心約束：300ms 內完成啟動**——超過這個閾值使用者會感覺遲鈍。

**5 階段管線**：

| Phase | 檔案 | 耗時 | 做什麼 |
|-------|------|------|--------|
| 0 | `cli.tsx` | ~5ms | Fast-path 分流：`--version`、`--help` 等直接退出，不載入完整系統 |
| 1 | `main.tsx` | ~138ms | **模組層級 I/O**：import 時就 fire keychain 和 MDM subprocess，和模組載入平行 |
| 2 | `init.ts` | ~30ms | Commander 解析、設定載入、**信任邊界**（Trust Boundary） |
| 3 | `setup.ts` | ~35ms | 平行註冊：Commands、Agents、Hooks、Plugins、MCP server 連線 |
| 4 | `replLauncher.ts` | ~30ms | 7 條啟動路徑匯聚（REPL、print、SDK、resume、continue、pipe、headless） |

**關鍵概念——信任邊界**：不是使用者信任 Claude Code，而是 Claude Code 信任「環境」。惡意的 `.bashrc` 可以設定 `LD_PRELOAD` 注入程式碼。信任對話確保使用者明確同意在可能被他人配置的目錄中操作。

**關鍵概念——Hook 設定快照**：setup 時 hook 設定從磁碟讀取一次後凍結為不可變快照，session 期間磁碟上的修改被忽略——防止攻擊者在 session 開始後修改 hook 規則。

---

#### Ch.3 狀態——雙層架構

> 原題：State — The Two-Tier Architecture

**核心問題**：Cost tracker 更新同一個 store 會觸發 React re-render；基礎設施模組在 React mount 前就需要狀態——不能用同一個 store。

**解法：雙層分離**

| 層 | 實作 | 欄位數 | 特性 |
|----|------|--------|------|
| Bootstrap STATE | 可變 singleton | ~80 | 不觸發 re-render，通過 getter/setter 存取，NFC 正規化所有路徑 |
| AppState Store | 34 行 Zustand-like | ~150 | 響應式，`DeepImmutable<>`，`useSyncExternalStore` 整合 React |

**關鍵概念——5 個 Sticky Latches（黏性閂鎖）**：

一旦某 beta header 在 session 中首次送出，就永遠不撤回——因為 header 是 cache key 的一部分，撤回會 bust 50K+ token 的 prompt cache。

| Latch | 防止什麼 |
|-------|---------|
| `afkModeHeaderLatched` | Shift+Tab 切換 AFK 模式時 flip header |
| `fastModeHeaderLatched` | Fast mode 冷卻進出 flip header |
| `cacheEditingHeaderLatched` | Remote feature flag 變更 bust 所有使用者 cache |
| `thinkingClearLatched` | 確認 cache miss 後防止重啟 thinking blocks bust 新 cache |
| `pendingPostCompaction` | 區分 compaction 觸發的 cache miss vs TTL 過期 |

---

#### Ch.4 與 Claude 對話——API 層

> 原題：Talking to Claude — The API Layer

**多 Provider 工廠**：`getAnthropicClient()` 根據環境變數分派到 Direct API / AWS Bedrock / Google Vertex / Azure Foundry，全部 cast 為 `Anthropic` 型別——「我們一直在對回傳型別說謊」。

**System Prompt 的 Dynamic Boundary（動態邊界）**：

```
Static Content（全域 cache）  ← 所有使用者共享、跨 session
─── DYNAMIC BOUNDARY ───
Dynamic Content（per-session） ← 含使用者 memory、MCP 指令
```

- 邊界前：無條件內容，一個 boolean 條件就會讓 cache 變體數翻倍（2^N 問題）
- 邊界後的 section 命名：`DANGEROUS_uncachedSystemPromptSection`（附帶 `_reason` 參數強制說明理由）

**Idle Watchdog**：TCP 連線可能靜默斷開。每收到一個 chunk 重置 90 秒倒計時；45 秒時發出警告；超時則 abort 並 fallback 到非 streaming 重試。

**Output Token Cap**：預設 8K（非 32K/64K）——因為 p99 輸出只有 4,911 token。命中 cap 時升級到 64K 重試，99% 的請求省下大量 context。

---

### Part II：The Core Loop（核心迴圈）

#### Ch.5 Agent 迴圈

> 原題：The Agent Loop

**為什麼是 Async Generator 而非 Event Emitter？**

| 理由 | 說明 |
|------|------|
| 背壓（Backpressure） | Generator 只在 consumer 呼叫 `.next()` 時 yield，React renderer 忙時自然暫停 |
| Return Value 語意 | `Terminal` 聯合型別編碼 10 種終止原因（正常完成/user abort/token 耗盡/hook 介入/max turns...） |
| `yield*` 組合性 | 外層 `query()` 委派給 `queryLoop()`，子 generator 透明轉發所有值和最終 return |

**4 層 Context 壓縮**：

```
Raw messages
  → Tool Result Budget（截斷過長的工具結果）
    → Snip Compact（移除可省略的中間訊息）
      → Microcompact（壓縮對話中的冗餘）
        → Context Collapse（合併歷史為摘要）
          → Auto-Compact（LLM 重寫整段對話）
```

每層比前一層更重（成本更高），只在前一層不足以控制 token 時才觸發。

**Loop State 不可變轉換**：每次 `continue` 都建構全新的 `State` 物件（不是 `state.turnCount++`），`transition` 欄位記錄「為什麼繼續」——測試可 assert 正確的恢復路徑。

---

#### Ch.6 工具——從定義到執行

> 原題：Tools — From Definition to Execution

**Tool 介面 3 個型別參數**：`Tool<Input, Output, ProgressData>`

- `Input`：Zod schema，同時生成 JSON Schema（給 API）和驗證 runtime 輸入
- `Output`：工具結果型別
- `ProgressData`：執行中的進度事件（Bash 輸出 stdout chunk、Grep 輸出 match count）

**Fail-Closed 預設值**：`buildTool()` 工廠函數的安全預設——忘記實作 `isConcurrencySafe` 就預設 `false`（序列執行），忘記 `isReadOnly` 就預設 `false`（視為寫入操作）。

**14 步執行管線**（簡化）：

```
1. Input validation (Zod parse)
2. Semantic validation (validateInput)
3. PreToolUse hooks
4. Permission check (hook → tool → mode)
5. User approval (if needed)
6. Concurrency classification
7. Execution (call())
8. Result budgeting (截斷過長結果)
9. PostToolUse hooks
10. Error classification
11. Result formatting
12. Analytics/telemetry
13. UI rendering
14. Context modifier application
```

**ToolUseContext 是「God Object」**：~40 個欄位，包含 abort controller、file cache、app state、message history、MCP connections、UI callbacks。書中坦承它是 god object，但替代方案（15+ 參數的函數簽名）更糟。

---

#### Ch.7 並發工具執行

> 原題：Concurrent Tool Execution

**核心洞見：安全性是 per-call 而非 per-tool-type**。`Bash("ls -la")` 可安全平行，`Bash("rm -rf build/")` 不行。

**兩層並發優化**：

| 層 | 時機 | 機制 |
|----|------|------|
| Batch Orchestration | 模型回應完成後 | 分區 tool calls 為 concurrent/serial groups |
| Speculative Execution | **模型還在 streaming 時** | 先啟動 concurrency-safe tools，不等回應完成 |

投機執行：Read 呼叫可以在模型還在生成其餘回應時就完成並回傳結果。如果模型最終輸出使 tool call 無效（罕見），結果會被丟棄。

---

### Part III：Multi-Agent Orchestration（多 Agent 編排）

#### Ch.8 生成子 Agent

> 原題：Spawning Sub-Agents

`AgentTool` 生成一個新的 `query()` generator，擁有自己的 message history、tool set 和 permission mode。15 步 `runAgent` 生命週期涵蓋從 prompt 組裝到結果回傳的完整流程。

**關鍵**：子 Agent 可以遞迴委派——Agent 可以 spawn 子 Agent，子 Agent 再 spawn 孫 Agent。

---

#### Ch.9 Fork Agent 與 Prompt Cache

> 原題：Fork Agents and the Prompt Cache

**Byte-identical prefix 技巧**：Fork agent 以 parent 的完整對話作為自己的 context window 起點，共享 parent 的 prompt cache prefix。

- 常規子 Agent：每次都要從零處理 context → 支付全額 input token
- Fork Agent：共享 parent cache → **~90-95% 的 input token 折扣**

這讓背景記憶提取 Agent（每次 query loop 結束後執行）的成本微乎其微——沒有 fork cache 共享，這個 Agent 根本不可能存在。

---

#### Ch.10 Task、協調與 Swarm

> 原題：Tasks, Coordination, and Swarms

Task 狀態機：`pending → running → completed | failed | killed`

- **Coordinator 模式**：一個 Agent 扮演協調者，分派工作給多個子 Agent
- **Swarm Messaging**：多個 Agent 之間的訊息傳遞機制

---

### Part IV：Persistence and Intelligence（持久化與智能）

#### Ch.11 記憶——跨對話學習

> 原題：Memory — Learning Across Conversations

**3 層記憶**：

| 層 | 位置 | 範圍 |
|----|------|------|
| 專案級 | `CLAUDE.md`（repo 根目錄） | 所有使用此 repo 的人 |
| 使用者級 | `~/.claude/MEMORY.md` | 此使用者的所有專案 |
| 團隊級 | symlink 共享 | 團隊成員間共享 |

**4 種記憶分類法**：user（使用者資訊）、feedback（行為回饋）、project（專案狀態）、reference（外部資源指標）

**LLM-powered recall**：Session 開始時，不是用關鍵字匹配，而是用 Sonnet side-query 從 manifest 中選擇最相關的記憶注入 system prompt。比 embedding similarity 更精確，且零基礎設施需求。

---

#### Ch.12 擴展性——Skills 與 Hooks

> 原題：Extensibility — Skills and Hooks

**兩階段 Skill 載入**：

| 階段 | 時機 | 讀什麼 |
|------|------|--------|
| Phase 1 | 啟動時 | 只讀 SKILL.md frontmatter（name、description、triggers） |
| Phase 2 | 呼叫時 | 才載入完整 SKILL.md 內容到 context |

這樣啟動時只付 frontmatter 的 cost，不管你裝了多少 skill。

**27 個 Hook 事件 × 4 執行類型**：

| 執行類型 | 說明 |
|----------|------|
| Shell command | 執行 bash 腳本 |
| Single-shot LLM | 一次性 LLM 判斷 |
| Multi-turn agent | 多輪 Agent 對話 |
| HTTP webhook | 發送 HTTP 請求 |

---

### Part V：The Interface（介面層）

#### Ch.13 終端 UI

> 原題：The Terminal UI

**為什麼自建渲染器？** 原版 Ink 每個 cell 每幀分配一個 JS 物件——200×120 終端 = 每 16ms 產生 24,000 個物件然後 GC。Claude Code fork 了 Ink，重寫關鍵路徑：

| 原版 Ink | Claude Code 版 |
|----------|---------------|
| Object-per-cell | Packed typed arrays |
| String-per-frame | Pool-based string interning |
| 字串級 diffing | **Cell-level dirty tracking** + double buffer |
| 逐行比較 ANSI | 合併相鄰 terminal writes 為最小 escape sequences |

---

#### Ch.14 輸入與互動

> 原題：Input and Interaction

Key parsing、keybindings 系統、chord 支援（多鍵組合）、vim 模式模擬。處理 terminal 輸入的複雜性——不同終端模擬器發送不同的 escape sequences。

---

### Part VI：Connectivity（連接性）

#### Ch.15 MCP——通用工具協定

> 原題：MCP — The Universal Tool Protocol

**8 種 Transport**：

| Transport | 場景 |
|-----------|------|
| `stdio` | 本地子程序（預設） |
| `http` | 遠端 Streamable HTTP（現行規格） |
| `sse` | Legacy Server-Sent Events |
| `ws` | WebSocket（雙向，少見） |
| `claudeai-proxy` | 透過 Claude.ai 基礎設施 |
| `sdk` | SDK 控制訊息 over stdio |
| `InProcessTransport` | 直接函數呼叫（63 行） |
| `sse-ide` / `ws-ide` | IDE 擴展 |

**7 個設定範圍**：MCP server config 從 7 個 scope 載入、合併、去重。

**Tool Wrapping**：MCP 工具透過 wrapping 變成標準 `Tool` 物件——從此和內建工具無法區分，走同一個 14 步 pipeline。

---

#### Ch.16 遠端控制與雲端執行

> 原題：Remote Control and Cloud Execution

- **Bridge v1/v2**：連接遠端 Claude Code 實例
- **CCR (Claude Code Remote)**：雲端執行環境
- **Upstream Proxy**：透過代理伺服器路由

---

### Part VII：Performance Engineering（效能工程）

#### Ch.17 效能——每一毫秒和 Token 都重要

> 原題：Performance — Every Millisecond and Token Counts

涵蓋 5 個效能維度：

| 維度 | 關鍵手段 |
|------|---------|
| 啟動速度 | Dynamic import、模組層級 I/O、fast-path 分流 |
| Context Window | 4 層壓縮、slot reservation（8K→64K） |
| Prompt Cache | Sticky latches、dynamic boundary、全域 cache scope |
| 渲染效能 | Packed arrays、cell-level diffing、double buffer |
| 搜尋效能 | 平行 glob/grep、結果串流 |

---

#### Ch.18 結語——我們學到了什麼

> 原題：Epilogue — What We Learned

**5 大架構賭注的完整論述**——見下方「5 大架構賭注」段落。

**可轉移的模式**：書中每一章都以「Apply This」結尾，提煉出可用於任何 Agent 系統的設計決策。

**Agent 的未來方向**：從單一 Agent 到多 Agent 協作、從 CLI 到跨平台、從文字到多模態。

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
