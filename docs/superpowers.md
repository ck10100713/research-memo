# Superpowers 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [obra/superpowers](https://github.com/obra/superpowers) |
| 作者部落格 | [Superpowers: How I'm using coding agents (Oct 2025)](https://blog.fsck.com/2025/10/09/superpowers/) |
| Simon Willison 評論 | [simonwillison.net](https://simonwillison.net/2025/Oct/10/superpowers/) |
| 心理學說服分析 | [DEV Community — 說服 AI Agent 的技術](https://dev.to/tumf/superpowers-the-technology-to-persuade-ai-agents-why-psychological-principles-change-code-quality-2d2f) |
| Termdock 評介 | [Superpowers: Skills Framework Reshaping AI Dev](https://www.termdock.com/en/blog/superpowers-framework-agent-skills) |
| Discord 社群 | [discord.gg/Jd8Vphy9jq](https://discord.gg/Jd8Vphy9jq) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | Jesse Vincent (obra) / [Prime Radiant](https://primeradiant.com) |
| Stars | 124K+（截至 2026-03-30） |
| 最新版本 | v5.0.6（2026-03-24） |
| 語言 | Shell (SKILL.md 純 Markdown) |
| 授權 | MIT |
| 建立 | 2025-10-09 |

Superpowers 是一套 **agentic skills 框架與軟體開發方法論**，專為 coding agent（Claude Code、Cursor、Codex CLI、Gemini CLI 等）設計。核心理念不是讓 agent 更聰明，而是**給予它紀律**——把資深工程師花數十年建立的開發紀律，編碼成可組合的 skill 檔案，強制 agent 遵循。

專案在 2025 年 10 月發布後迅速成為 Claude Code Marketplace 安裝量最高的 plugin，超越 Playwright 等官方工具。2026 年 1 月正式被 Anthropic 官方 Marketplace 收錄。

## 核心工作流程

```
使用者輸入需求
    │
    ▼
┌─────────────────┐
│  brainstorming   │ ← 蘇格拉底式追問，釐清真正需求
│  (不寫程式)       │   分段呈現設計文件，逐段確認
└────────┬────────┘
         ▼
┌─────────────────┐
│  writing-plans   │ ← 拆解成 2-5 分鐘的小任務
│                  │   每個任務有精確檔案路徑 + 驗證步驟
└────────┬────────┘
         ▼
┌─────────────────┐
│ using-git-       │ ← 建立隔離 worktree + 新 branch
│ worktrees        │   驗證乾淨的測試基線
└────────┬────────┘
         ▼
┌─────────────────┐
│ subagent-driven- │ ← 每個任務派 fresh subagent 執行
│ development      │   兩階段 review：規格 → 品質
│                  │   防止 context pollution
└────────┬────────┘
         ▼
┌─────────────────┐
│ test-driven-     │ ← 嚴格 RED → GREEN → REFACTOR
│ development      │   測試前寫的程式碼會被刪除
└────────┬────────┘
         ▼
┌─────────────────┐
│ requesting-      │ ← 依嚴重度回報問題
│ code-review      │   Critical 問題阻擋進度
└────────┬────────┘
         ▼
┌─────────────────┐
│ finishing-a-     │ ← 提供 merge/PR/keep/discard 選項
│ development-     │   自動清理 worktree
│ branch           │
└─────────────────┘
```

## 14 個內建 Skills

| 分類 | Skill | 用途 |
|------|-------|------|
| **測試** | `test-driven-development` | 強制 RED-GREEN-REFACTOR 循環，含測試反模式參考 |
| **除錯** | `systematic-debugging` | 4 階段根因分析（含 root-cause-tracing、defense-in-depth） |
| | `verification-before-completion` | 確保真正修好，不只是看起來修好 |
| **協作** | `brainstorming` | 蘇格拉底式設計精煉 |
| | `writing-plans` | 拆解成可驗證的小任務 |
| | `executing-plans` | 分批執行 + 人工檢查點 |
| | `dispatching-parallel-agents` | 並行 subagent 工作流 |
| | `subagent-driven-development` | 兩階段 review 的快速迭代 |
| | `requesting-code-review` | Review 前檢查清單 |
| | `receiving-code-review` | 回應 review 回饋的流程 |
| | `using-git-worktrees` | 平行開發分支隔離 |
| | `finishing-a-development-branch` | Merge/PR 決策流程 |
| **Meta** | `writing-skills` | 建立新 skill 的最佳實踐 |
| | `using-superpowers` | Skills 系統介紹 |

## 平台支援

| 平台 | 安裝方式 |
|------|---------|
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| Codex CLI | Fetch INSTALL.md 手動設定 |
| OpenCode | Fetch INSTALL.md 手動設定 |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |

## 技術架構：Skill 檔案結構

每個 skill 是一個 `skills/<name>/SKILL.md` 檔案，用純 Markdown 撰寫。這個設計選擇極為關鍵——不需要任何程式碼、不依賴特定平台 API，任何 LLM 都能讀懂。

Skills 透過 plugin 機制自動注入 agent 的 system prompt，agent 在每次動作前**被強制檢查**是否有相關 skill 可用。這不是建議，而是強制性工作流。

## 心理學說服設計

Superpowers 最獨特的技術洞察：**Robert Cialdini 的七大說服原則對 LLM 同樣有效**（Wharton 研究已證實）。

| 原則 | 在 Superpowers 中的應用 |
|------|----------------------|
| **Authority（權威）** | Skills 被框架為強制性指令，不是可選建議 |
| **Commitment（承諾）** | Agent 必須先宣告要使用哪個 skill 才能繼續 |
| **Social Proof（社會證明）** | 將 skill 檢查行為正常化為「所有優秀工程師都這麼做」 |
| **Scarcity（稀缺）** | 利用時間壓力框架強化遵從 |
| **Unity（統一）** | 建立 agent 與最佳實踐的共同身份認同 |

### Pressure Scenarios（壓力測試）

作者發明了「壓力情境」來驗證 skill 的有效性——刻意製造 agent 想跳過規則的場景：

- **時間壓力 + 自信**：生產系統當機，每分鐘損失 $5K，agent 會不會跳過 debugging skill？
- **沉沒成本 + 成功**：已花 45 分鐘寫出能動的非同步測試，agent 會不會跳過 async testing guideline review？

這種「不是測試功能，而是測試紀律」的方法論本身就是一個重大創新。

## v5.0 重大變更（2026-03）

v5.0.0 於 2026-03-09 發布，是架構層級的重大升級：

| 變更 | 說明 |
|------|------|
| **強制 subagent-driven development** | 在支援的 harness 上，subagent 模式從可選變為強制 |
| **視覺化 Brainstorming Companion** | 可選的 browser-based 視覺化介面，在 ideation 階段即時呈現設計 |
| **文件 review 系統** | 透過 subagent dispatch 自動驗證 spec 和 plan |
| **Inline self-review 取代 subagent review loop** | 執行時間從 ~25 分鐘降至 ~30 秒，品質相當（v5.0.6） |
| **文件結構重組** | specs 移至 `docs/superpowers/specs/`，plans 移至 `docs/superpowers/plans/` |
| **架構引導** | 整個 skill pipeline 整合隔離性、清晰度、檔案大小感知的架構建議 |
| **多平台擴展** | v5.0.1 正式加入 Gemini CLI extension，v5.0.2 移除所有 vendored 依賴改用 Node.js 內建模組 |

### 版本演進

| 版本 | 日期 | 重點 |
|------|------|------|
| v5.0.0 | 2026-03-09 | 強制 subagent、visual brainstorming、doc review |
| v5.0.1 | 2026-03-10 | Gemini CLI support、brainstorm server 重新定位 |
| v5.0.2 | 2026-03-11 | 移除 vendored 依賴（Express/Chokidar/WebSocket → Node.js built-in） |
| v5.0.5 | 2026-03-17 | ESM 相容 Node.js 22+、Windows/MSYS2 PID 監控修復 |
| v5.0.6 | 2026-03-24 | Inline self-review 取代 subagent review loop（25min → 30s） |

## 目前限制 / 注意事項

- **高 token 消耗**：每個任務啟動 fresh subagent 意味著大量 context 重新載入（v5.0.6 的 inline self-review 已大幅改善 review 階段）
- **Shell 為主**：核心邏輯依賴 Markdown + Shell script，IDE 整合程度各平台差異大
- **覆蓋範圍**：14 個 skills 涵蓋開發流程，但缺乏部署、監控、安全等 DevOps 面向
- **學習曲線**：嚴格的 TDD 和 brainstorming 流程可能讓習慣「直接寫 code」的使用者感到受限
- **單一作者主導**：目前核心設計高度依賴 Jesse Vincent 的工程哲學

## 研究價值與啟示

### 關鍵洞察

1. **「給紀律」比「給智慧」更有效**：Superpowers 證明了 coding agent 的瓶頸不在能力而在紀律。一個被強制執行 TDD 的 agent，產出品質遠超一個「更聰明但隨意」的 agent。這與人類工程團隊的經驗完全一致。

2. **純 Markdown 是最佳 skill 格式**：不用 YAML、不用 JSON、不用程式碼——純 Markdown 就是 LLM 最自然的「指令格式」。這個設計讓 skills 跨平台、跨模型、零依賴。我們自己的 SKILL.md 系統也驗證了這一點。

3. **心理學說服原則可遷移到 LLM**：這可能是 Superpowers 最具學術價值的發現。Cialdini 的框架不只適用於人類——Authority、Commitment、Social Proof 等原則在 prompt engineering 中同樣有效，且可透過 pressure scenarios 系統性驗證。

4. **Subagent 隔離防止 context pollution**：每個任務用 fresh subagent 執行，避免前一個任務的 context 汙染下一個任務的判斷。代價是 token 用量增加，但換來的是更可預測的輸出品質。

5. **124K stars 驗證了「開發流程 > 開發工具」**：Superpowers 本質上不是工具，而是方法論。它的爆紅說明開發者社群已經認知到：AI coding 的問題不是模型不夠好，而是我們不知道如何有效指揮 agent。

### 與其他專案的關聯

- **vs Everything Claude Code**：Everything Claude Code 是完整的 agent harness 系統（28 agents + 116 skills），而 Superpowers 專注在軟體開發工作流的 14 個核心 skills。兩者的 skill 設計理念高度相似（都用 SKILL.md），但 scope 完全不同。
- **vs Claude Skills Guide**：我們的 Skills Guide 教的是「如何寫 skill」，而 Superpowers 本身就是一套完整的 skill 集合 + 開發方法論。可以視為 Claude Skills Guide 的最佳實踐範例。
- **vs gstack**：Garry Tan 的 gstack（56K stars）同樣是 Claude Code 工作流系統，但定位不同。Superpowers 強制流程紀律（automatic enforcement），gstack 提供角色化的按需工具（manual invocation）。Superpowers 擅長強制 TDD 和長時間自主 session，gstack 擅長 visual QA 和完整 sprint 生命週期。兩者可互補：gstack 負責 planning/QA/deploy 階段，Superpowers 負責 implementation 紀律。
