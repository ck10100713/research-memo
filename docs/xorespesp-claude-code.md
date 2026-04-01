---
date: "2026-04-01"
category: "Coding Agent 工具"
card_icon: "material-source-branch"
oneliner: "Claude Code 洩漏原始碼的可運行 TypeScript 復原版，含 shims 替代 native modules"
---

# xorespesp Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [github.com/xorespesp/claude-code](https://github.com/xorespesp/claude-code) |
| 類似專案 (oboard) | [github.com/oboard/claude-code-rev](https://github.com/oboard/claude-code-rev) |
| 類似專案 (beita6969) | [github.com/beita6969/claude-code](https://github.com/beita6969/claude-code) |
| 類似專案 (leeyeel) | [github.com/leeyeel/claude-code-sourcemap](https://github.com/leeyeel/claude-code-sourcemap) |
| Penligent 分析 | [Claude Code Source Map Leak, What Was Exposed and What It Means](https://www.penligent.ai/hackinglabs/claude-code-source-map-leak-what-was-exposed-and-what-it-means/) |

## 專案概述

**xorespesp/claude-code** 是 Claude Code 洩漏原始碼的 **可運行 TypeScript 復原版**。與其他洩漏相關專案不同，這個 repo 的目標不是重寫（如 [Claw Code](claw-code.md) 的 Python/Rust）或分析（如 [Kuberwastaken](kuberwastaken-claude-code.md) 的深度拆解），而是**直接從 source map 復原出可以 `bun run dev` 跑起來的完整 TypeScript 專案**。

| 指標 | 數值 |
|------|------|
| Stars | 91 |
| Forks | 111 |
| 語言 | TypeScript |
| 檔案數 | ~2,067 |
| Repo 大小 | ~9.4 MB |
| Source 檔案 | ~2,006 TS/TSX |
| 工具數 | 53 |
| Slash 指令 | 87 |
| License | 無（聲明 research & learning only） |

## 復原方式與 Shims

### 從 Source Map 到可運行專案

原始 npm 套件 `@anthropic-ai/claude-code` v2.1.88 的 `.map` 檔案包含完整 `sourcesContent`，但 source map 無法 100% 復原所有內容：

| 缺失類型 | 說明 |
|----------|------|
| Type-only 檔案 | `.d.ts` 可能遺漏 |
| Build artifacts | 建置過程中生成的程式碼不在 source map 中 |
| Native bindings | 私有 native modules 被 shims 替代 |
| Dynamic resources | 動態 import 和資源檔可能不完整 |

### Shims 目錄

`shims/` 替代了 Anthropic 內部的 native modules：

| Shim | 替代對象 |
|------|----------|
| `ant-claude-for-chrome-mcp` | Chrome MCP 整合 |
| `ant-computer-use-input` | Computer Use 輸入處理 |
| `ant-computer-use-mcp` | Computer Use MCP（代號 Chicago） |
| `ant-computer-use-swift` | macOS Swift native binding |
| `color-diff-napi` | 色彩 diff NAPI binding |
| `modifiers-napi` | 修飾鍵 NAPI binding |
| `url-handler-napi` | URL 處理 NAPI binding |

## 專案結構與架構

### Boot Sequence

```
dev-entry.ts → entrypoints/cli.tsx → main.tsx → REPL (React/Ink)
  │                │          │
  │                │          └─ Full Init: Auth → GrowthBook → MCP → Settings → Commander.js
  │                └─ Fast Path: --version / daemon / ps / logs
  └─ Startup Gate: 掃描 missing relative imports，全部 resolve 才啟動
```

### 核心目錄

```
src/
├── entrypoints/    # CLI 入口
├── main.tsx        # 主初始化（auth / MCP / settings / feature flags）
├── QueryEngine.ts  # 核心引擎（~1,295 行，LLM API loop + persistence）
├── tools/          # 53 個工具（Bash, Read, Edit, Agent...）
├── commands/       # 87 個 slash 指令
├── services/       # 後端服務（API, MCP, OAuth, Datadog telemetry）
├── utils/          # 工具函式（git, permissions, model, token budget）
├── components/     # 終端 UI（~406 檔案，React + Ink）
├── hooks/          # Custom React Hooks
├── ink/            # 自訂 Ink 分支（layout / focus / ANSI / virtual scroll）
├── vim/            # Vim 模式引擎
├── coordinator/    # 多 Agent 協調
├── bridge/         # IDE 雙向通訊 + 遠端橋接
├── remote/         # 遠端 session teleportation
├── skills/         # 可重用 workflow & skill 系統
├── plugins/        # Plugin 系統
├── memdir/         # 持久記憶系統（5 層架構）
├── voice/          # 語音互動（streaming STT，未發布）
├── buddy/          # Gacha 寵物系統
└── assistant/      # KAIROS daemon mode（未發布）
```

### Token 優化：3 層壓縮系統

這是 Claude Code 核心競爭力之一：

| 層級 | 名稱 | 機制 |
|------|------|------|
| 1 | **Microcompact** | 用 `cache_edits` API 從 server cache 移除訊息，不破壞 prompt cache（零 API 成本） |
| 2 | **Session Memory** | 預先提取的 session memory 作為摘要，避免壓縮時呼叫 LLM |
| 3 | **Full Compact** | Sub-agent 將對話壓縮為 9 段結構化格式，用 `<analysis>` tag stripping 減少 token |

**其他優化**：
- `FILE_UNCHANGED_STUB`：重複讀取的檔案回傳 30 字 stub
- 動態 max output cap（預設 8K，重試時 64K）
- Cache latch 防止 UI toggle（Shift+Tab）破壞 70K context
- Circuit breaker 防止連續壓縮失敗時浪費 API call

### 5 層記憶架構

| 層級 | 名稱 | 範圍 |
|------|------|------|
| 1 | **Memdir** | 專案級索引 + topic files（`MEMORY.md`） |
| 2 | **Auto Extract** | Fire-and-forget forked agent，session 後整合記憶 |
| 3 | **Session Memory** | 即時 context 追蹤，無額外 LLM overhead |
| 4 | **Team Memory** | 共享遠端狀態，SHA-256 delta upload + git-leaks secret guard |
| 5 | **Agent Memory** | Agent 專屬知識，scope: local / project / user |

### 權限模式（6 種）

| 模式 | 說明 |
|------|------|
| `acceptEdits` | 自動接受編輯 |
| `bypassPermissions` | 繞過權限檢查 |
| `default` | 互動式確認 |
| `dontAsk` | 不詢問 |
| `plan` | 規劃模式 |
| `auto` | yoloClassifier ML 自動批准 |
| `bubble` | Sub-agent 權限傳播 |

### 未發布子系統

隱藏在 **88+ compile-time flags** 和 **700+ GrowthBook runtime gates** 背後：

| 系統 | 代號 | 說明 |
|------|------|------|
| KAIROS | `PROACTIVE` | Always-on daemon + Dream 記憶整合 |
| Computer Use | Chicago | macOS 桌面控制 MCP |
| Voice Mode | — | Streaming STT 語音輸入 |
| ULTRAPLAN | — | 30 分鐘 CCR 多 agent 規劃 |
| Web Browser | Bagel | 整合網頁導航 |
| Teleport | — | 遠端 session context 傳送 |

### 已包含的 Patch

| Patch | 說明 | Issue |
|-------|------|-------|
| Welcome banner toggle | 新增 `showWelcomeBanner` 設定，可在 `~/.claude/settings.json` 中關閉啟動 banner | [#2254](https://github.com/anthropics/claude-code/issues/2254) |

## 快速開始

```bash
# 需要 Bun ≥ 1.3.5 + Node.js ≥ 24
bun install       # 安裝依賴
bun run dev       # 啟動 CLI（互動模式）
bun run version   # 驗證版本號
```

## 目前限制 / 注意事項

- **版權歸 Anthropic**：聲明僅供研究學習，不得商用
- **無 License**：法律狀態不明確
- **Native modules 被替代**：7 個 `@ant/` 私有模組用 shims 替代，Computer Use 等功能不可用
- **Source map 復原限制**：type-only files、build artifacts、dynamic imports 可能缺失
- **安全風險**：運行洩漏原始碼可能觸發 Anthropic 遙測上報
- **版本凍結**：基於 v2.1.88，不會有後續更新

## 研究價值與啟示

### 關鍵洞察

1. **這是唯一可直接運行的洩漏復原版**：相比 Claw Code（Python metadata mirror）和 Kuberwastaken（Rust 重寫），xorespesp 的價值在於「原汁原味」——可以直接 `bun run dev` 啟動，觀察 Claude Code 的實際行為。

2. **3 層壓縮系統是 token 效率的教科書**：Microcompact（零成本 cache 編輯）→ Session Memory（免 LLM 摘要）→ Full Compact（結構化壓縮），這個漸進式設計解決了 long-running agent 的 context 膨脹問題。

3. **5 層記憶架構展示了 production agent 的記憶需求層次**：從 session 級的即時追蹤到 team 級的共享狀態，每一層解決不同的 persistence 需求。特別是 Team Memory 的 SHA-256 delta upload + git-leaks guard，展示了多 agent 記憶共享的安全考量。

4. **88 個 compile-time flags + 700 個 runtime gates 的規模驚人**：這代表 Claude Code 的功能開發遠超公開版本，也揭示了 Anthropic 的 staged rollout 策略——先內部員工 canary，再外部 A/B test。

5. **Shims 清單揭露了 Anthropic 的 native 投入**：7 個 `@ant/` 私有 NAPI binding（包括 Swift binding），表明 Claude Code 不只是 JS/TS——在 Computer Use、色彩 diff、URL 處理等底層能力上有 native 效能投入。

### 與其他專案的關聯

| 相關筆記 | 關聯 |
|----------|------|
| [Claw Code](claw-code.md) | 同事件的 Python/Rust clean-room 重寫，走不同路線 |
| [Kuberwastaken Claude Code](kuberwastaken-claude-code.md) | 深度拆解文章 + Rust 重寫，分析最詳盡但不可運行 |
| [Analysis Claude Code](analysis-claude-code.md) | 靜態分析取向 |
| [Claude Code Reverse](claude-code-reverse.md) | 逆向工程研究 |
| [Anthropic Harness Design](harness-design-long-running-apps.md) | 官方 harness 設計文件，此 repo 是其實際程式碼 |
