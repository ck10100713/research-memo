---
date: "2026-04-01"
category: "Coding Agent 工具"
card_icon: "material-magnify-scan"
oneliner: "Claude Code 洩漏源碼深度拆解 + clean-room Rust 重寫，揭露 BUDDY/KAIROS/Dream 等未公開系統"
---

# Kuberwastaken Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [github.com/Kuberwastaken/claude-code](https://github.com/Kuberwastaken/claude-code) |
| 作者部落格 | [kuber.studio — Claude Code Leak Breakdown](https://kuber.studio/blog/AI/Claude-Code's-Entire-Source-Code-Got-Leaked-via-a-Sourcemap-in-npm,-Let's-Talk-About-it) |
| Axios 報導 | [Anthropic leaked its own Claude source code](https://www.axios.com/2026/03/31/anthropic-leaked-source-code-ai) |
| SiliconANGLE 報導 | [Anthropic accidentally exposes Claude Code source code](https://siliconangle.com/2026/03/31/anthropic-accidentally-exposes-claude-code-source-code-npm-packaging-error/) |
| VentureBeat 報導 | [Claude Code's source code appears to have leaked](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know) |

## 專案概述

**Kuberwastaken/claude-code** 是 2026/3/31 Claude Code 洩漏事件後，由印度開發者 **Kuber Mehta** 建立的專案，包含兩大部分：

1. **深度技術拆解文章**：目前網路上對洩漏原始碼最詳盡的逐系統分析
2. **Clean-room Rust 重寫**：採用兩階段法（spec → implementation），由不同 AI agent 分別負責

與 [Claw Code](claw-code.md)（Python/Rust 重寫）不同，此專案的核心價值在**分析文章**而非重寫的程式碼本身。

## Clean-Room 重寫架構

### 兩階段法

```
Phase 1: Specification（AI Agent A）
├── 分析原始碼 → 產出行為規格書
├── 偏離原始架構，重新設計 data flows、tool contracts
└── 不攜帶任何原始碼 → 輸出到 spec/

Phase 2: Implementation（AI Agent B）
├── 僅從 spec/ 實作，從未參照原始 TypeScript
├── 輸出 idiomatic Rust
└── 重現行為（behavior），非表達（expression）→ src-rust/
```

法律依據引用 Phoenix Technologies v. IBM（1984）BIOS clean-room 先例、Baker v. Selden（1879）版權保護表達而非概念。

### Rust Crate 結構

```
src-rust/crates/
├── cli/        # CLI 入口
├── core/       # 核心邏輯（權限、設定、常數）
├── api/        # Anthropic API 通訊
├── query/      # LLM query engine、agent、coordinator
├── tools/      # 工具系統（40+ tools）
├── commands/   # Slash 指令
├── tui/        # 終端 UI（Ink → Ratatui?）
├── bridge/     # IDE / claude.ai 橋接
├── buddy/      # Tamagotchi 寵物系統
├── mcp/        # MCP 整合
└── (10 crates total)
```

### Spec 文件索引

| 檔案 | 涵蓋範圍 |
|------|----------|
| `00_overview.md` | 整體架構概覽 |
| `01_core_entry_query.md` | 入口點與 query engine |
| `02_commands.md` | 50+ slash 指令 |
| `03_tools.md` | 40+ 工具定義 |
| `04_components_core_messages.md` | 核心組件與訊息系統 |
| `05_components_agents_permissions_design.md` | Agent 與權限設計 |
| `06_services_context_state.md` | 服務、context、狀態管理 |
| `07_hooks.md` | Hook 系統 |
| `08_ink_terminal.md` | 終端 UI |
| `09_bridge_cli_remote.md` | 橋接與遠端控制 |
| `10_utils.md` | 工具函式 |
| `11_special_systems.md` | 特殊系統（Dream、KAIROS 等） |
| `12_constants_types.md` | 常數與型別 |
| `13_rust_codebase.md` | Rust 實作指引 |

## 洩漏揭露的 Claude Code 核心系統

以下為文章中分析的關鍵未公開系統，這是此 repo 最有價值的部分：

### BUDDY — 終端 Tamagotchi 寵物

隱藏在 `BUDDY` feature flag 背後的完整寵物系統：

| 機制 | 細節 |
|------|------|
| 抽卡系統 | Mulberry32 PRNG，seed = userId hash + salt `'friend-2026-401'` |
| 物種 | 18 種，名稱以 `String.fromCharCode()` 混淆 |
| 稀有度 | Common 60% / Uncommon 25% / Rare 10% / Epic 4% / Legendary 1% |
| 閃光 | 獨立 1% 機率（Shiny Legendary Nebulynx = 0.01%） |
| 屬性 | DEBUGGING / PATIENCE / CHAOS / WISDOM / SNARK（0-100） |
| 外觀 | 6 種眼睛 + 8 種帽子（部分依稀有度解鎖） |
| 靈魂 | 首次孵化時由 Claude 撰寫的角色描述 |
| 渲染 | 5 行高 × 12 字元寬 ASCII art，含動畫幀 |
| 排程 | April 1-7, 2026 預告窗口，May 2026 正式上線 |

### KAIROS — Always-On 主動助手

`PROACTIVE` / `KAIROS` feature flag 控制的持續運行模式：

- **Append-only 日誌**：每日記錄觀察、決策、行動
- **Tick 機制**：定期 `<tick>` prompt，決定主動行動或保持安靜
- **15 秒阻塞預算**：超過 15 秒的主動操作自動延後
- **Brief 模式**：極簡輸出，避免刷屏
- **專屬工具**：`SendUserFile`、`PushNotification`、`SubscribePR`

### ULTRAPLAN — 30 分鐘遠端規劃

將複雜規劃任務卸載到 **Cloud Container Runtime（CCR）**：

```
1. Claude Code 識別需要深度規劃的任務
2. 啟動遠端 CCR session（Opus 4.6）
3. 終端每 3 秒 polling 結果
4. 瀏覽器 UI 可即時觀看 + 批准/拒絕
5. 批准後透過 __ULTRAPLAN_TELEPORT_LOCAL__ 傳回本地
```

### Dream System — 記憶整合引擎

背景 forked subagent，模擬「做夢」進行記憶整合：

**三重觸發閘門**：

1. 距上次 dream ≥ 24 小時
2. 距上次 dream ≥ 5 個 session
3. 取得 consolidation lock（防止並行 dream）

**四個階段**：

| 階段 | 動作 |
|------|------|
| Orient | ls memory 目錄、讀 MEMORY.md、瀏覽既有 topic files |
| Gather | 從 daily logs → drifted memories → transcript search 收集新資訊 |
| Consolidate | 寫入/更新 memory files、轉換相對日期、刪除矛盾事實 |
| Prune | MEMORY.md < 200 行 + ~25KB、移除過期指標、解決矛盾 |

> Dream subagent 僅有 **read-only bash**，可觀察專案但不可修改。

### Undercover Mode — 內部員工匿名模式

防止 Anthropic 員工（`USER_TYPE === 'ant'`）在公開 repo 中暴露內部資訊：

- **禁止內容**：內部代號（Capybara、Tengu）、未發布版號、內部工具/Slack 頻道、「Claude Code」字樣、AI 署名
- **啟動邏輯**：`CLAUDE_CODE_UNDERCOVER=1` 強制開啟；否則自動判斷（非內部 repo = undercover on）
- **無法強制關閉**：*「if we're not confident we're in an internal repo, we stay undercover」*
- **揭露事實**：Anthropic 員工主動用 Claude Code 貢獻開源，且 AI 被指示隱藏身分

### Coordinator Mode — 多 Agent 協調

`CLAUDE_CODE_COORDINATOR_MODE=1` 啟動的多 agent 系統：

| 階段 | 角色 | 任務 |
|------|------|------|
| Research | Workers（平行） | 調查 codebase、找檔案、理解問題 |
| Synthesis | **Coordinator** | 讀取發現、理解問題、撰寫規格 |
| Implementation | Workers | 按規格修改、commit |
| Verification | Workers | 測試變更 |

支援 Agent Teams/Swarm（`tengu_amber_flint` gate）：in-process teammates + tmux/iTerm2 panes + 團隊記憶同步。

## 其他重要發現

### 未發布模型代號

| 代號 | 說明 |
|------|------|
| **Capybara** | 新模型家族（v2），含 `capybara-v2-fast` 變體，支援 1M context |
| **Opus 4.7** | 已在程式碼中被引用 |
| **Sonnet 4.8** | 已在程式碼中被引用 |
| **Fennec** | 舊 Opus 代號（migration: `migrateFennecToOpus`） |
| **Tengu** | Claude Code 內部專案代號（數百個 `tengu_` prefix flag） |

### Beta API Headers

```
interleaved-thinking-2025-05-14    // Extended thinking
context-1m-2025-08-07              // 1M context window
structured-outputs-2025-12-15      // Structured output
fast-mode-2026-02-01               // Fast mode (Penguin)
redact-thinking-2026-02-12         // Redacted thinking（未公開）
afk-mode-2026-01-31                // AFK mode（未公開）
advisor-tool-2026-03-01            // Advisor tool（未公開）
token-efficient-tools-2026-03-28   // Token-efficient tool schemas
```

### 權限系統

- **四種模式**：`default`（互動）、`auto`（ML 分類器自動批准）、`bypass`、`yolo`（全拒絕）
- **風險分級**：LOW / MEDIUM / HIGH
- **YOLO 分類器**：ML-based 快速權限決策
- **路徑穿越防護**：URL-encoded、Unicode normalization、backslash injection

### 內部趣聞

- Fast Mode 內部叫 **Penguin Mode**，endpoint: `api/claude_code_penguin_mode`
- Computer Use 代號 **Chicago**，建在 `@ant/computer-use-mcp` 上
- `DANGEROUS_uncachedSystemPromptSection()` — 命名暗示有人踩過 cache 坑

## 目前限制 / 注意事項

- **無 License**：repo 未標示任何授權，法律狀態不明確
- **Rust 重寫完成度未知**：crate 結構存在但未有功能驗證報告
- **洩漏資訊時效性**：分析基於 v2.1.88，後續版本可能已大幅修改
- **Clean-room 合法性待驗證**：雖引用法律先例，但 AI agent 分析原始碼再產出 spec 是否等同 clean-room 仍有爭議
- **部分資訊為推測**：Capybara 發布日期、BUDDY 上線時程等為作者推斷

## 研究價值與啟示

### 關鍵洞察

1. **這是目前對 Claude Code 內部架構最完整的技術文件**：13 份 spec 文件涵蓋從 entry point 到 special systems 的所有層面。相比 [Claw Code](claw-code.md) 的 metadata mirror，這裡有真正可參考的架構設計。

2. **Dream System 是 persistent memory 的工程典範**：三重觸發閘門（時間 + session 數 + lock）+ 四階段整合流程，解決了「何時整合記憶」和「如何防止過度整合」兩個核心問題。這個設計 pattern 可直接套用到任何 agent 記憶系統。

3. **Feature Flag 架構值得學習**：compile-time flag（`feature()` from `bun:bundle`）+ runtime flag（GrowthBook `tengu_*`）的雙層設計，配合 `getFeatureValue_CACHED_MAY_BE_STALE()` 的刻意允許 stale data 策略，是大型 agent 系統的工程最佳實踐。

4. **System Prompt 的分段 cache 策略**：`SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 將 prompt 分為可 cache 的靜態段和必須重建的動態段，在 token 成本和個人化之間取得平衡。

5. **Undercover Mode 揭露了 AI 對開源的隱性影響**：Anthropic 員工使用 Claude Code 貢獻開源但刻意隱藏 AI 身分，這對開源社群的透明度和信任有深遠影響。

### 與其他專案的關聯

| 相關筆記 | 關聯 |
|----------|------|
| [Claw Code](claw-code.md) | 同一事件的另一個重寫專案（Python 路線），由 Sigrid Jin 主導 |
| [Anthropic Harness Design](harness-design-long-running-apps.md) | Anthropic 官方 harness 設計文件，洩漏源碼是其實際實作 |
| [Analysis Claude Code](analysis-claude-code.md) | 另一個 Claude Code 分析專案 |
| [Claude Code Reverse](claude-code-reverse.md) | 逆向工程研究，與此文的分析角度互補 |
| [OpenClaw](openclaw.md) | BUDDY 系統中提到 OpenClaw 的 soul description 機制 |
