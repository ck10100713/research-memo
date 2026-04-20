---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-account-group"
oneliner: "台灣交大 NYCU-Chung 作品，把 Claude Code 變成 12 人工程團隊，9 天衝 218 stars 的 P7/P9/P10 企業職級方法論"
---

# my-claude-devteam 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/NYCU-Chung/my-claude-devteam> |
| 英文 README | <https://github.com/NYCU-Chung/my-claude-devteam/blob/main/README.md> |
| 繁中 README | <https://github.com/NYCU-Chung/my-claude-devteam/blob/main/README.zh-TW.md> |
| 英文 CLAUDE.md | <https://raw.githubusercontent.com/NYCU-Chung/my-claude-devteam/main/CLAUDE.en.md> |
| 繁中 CLAUDE.md | <https://raw.githubusercontent.com/NYCU-Chung/my-claude-devteam/main/CLAUDE.zh-TW.md> |
| 方法論源頭 | <https://github.com/tanweai/pua>（探微安全實驗室 PUA，MIT） |
| openpua 官網 | <https://openpua.ai/> |
| 反向工程討論 | <https://dev.to/nwyin/reverse-engineering-claude-code-agent-teams-architecture-and-protocol-o49> |

## 專案概述

**my-claude-devteam** 是台灣國立陽明交通大學（NYCU）學生 `NYCU-Chung` 於 **2026-04-11** 開源的 Claude Code Plugin。定位不是「多一個 agent 市集」，而是**把整個工程組織塞進 Claude Code**：12 個職能明確的 subagent、15 個自動化 hook，再掛上借自中國大廠 P 級職階文化的 **P7/P9/P10 方法論** 與 **三條紅線** 紀律。

專案宣稱解決的痛點很直白：「大部分人把 Claude Code 當一個 coder 用」；作者要把它升級成「planner + senior engineer + refactor lead + migration lead + frontend designer + critic + pentester + debugger + DB specialist + onboarder + tool expert + web researcher」的 12 人團隊，每個 agent 有獨立的 tool permission 與 model 配置，由一套嚴格的委派規則決定誰能動哪些檔案。

截至 **2026-04-20**（本筆記撰寫日，距釋出僅 9 天）：**218 stars / 42 forks / 0 open issues**，已經有 dev.to 作者反向工程該團隊架構，屬於 Claude Code plugin 生態裡罕見的「台灣出品 × 中國大廠文化 × 英文為主 README」三角型作品。

## 12 Agent 團隊表

| Role | Agent | 主要任務 | 觸發條件 |
|------|-------|----------|----------|
| 📋 Tech Lead | `planner` | 把模糊需求拆成可平行化的 Task Prompt，用六元素契約（goal / scope / input / output / acceptance / boundaries），**禁止寫 code** | 任務觸及 3+ 檔案或 2+ 模組 |
| 🛠 Senior Engineer | `fullstack-engineer` | P7 方法論：讀實況 → 設計 → 影響分析 → 實作 → 三問自審 → `[P7-COMPLETION]` | 單一功能或跨模組實作 |
| 🔄 Refactor Lead | `refactor-specialist` | 大規模安全重構，atomic commit、全呼叫點驗證、單一 revert 可回溯 | 10+ 檔案的改名/搬移/抽模組 |
| 🚀 Migration Lead | `migration-engineer` | 框架大版本升級：讀 upstream changelog、漸進執行、每步驟驗證 | Next.js 13→14、Vue 2→3、Tailwind 3→4 |
| 🎨 Designer | `frontend-designer` | 拒絕 AI slop 風格的有主見視覺設計 | 新頁面、UI 改版 |
| 🔍 Code Reviewer | `critic` | 找 bug / 安全漏洞 / 邏輯錯誤 / 邊界條件，每條附檔名+行號，**嚴禁「看起來還行」** | commit / deploy / merge 前 |
| 🧪 Pentester | `vuln-verifier` | 把 critic 的發現寫成 PoC 測試，**證明漏洞真實** 才能進下一步 | critic 標記安全問題後 |
| 🐛 Debug Engineer | `debugger` | 讀日誌 → 建假設 → 驗證 → 修正，禁止猜測 | Bug report、服務事故、測試失敗 |
| 🗄 DB Specialist | `db-expert` | Schema / migration / query 的安全性、索引、鎖、race condition 審查 | 資料層變更 |
| 🗺 Onboarder | `onboarder` | 首次進入 codebase 產出架構、入口、可疑點的心智模型 | 接手新專案、評估 OSS |
| ⚙️ Tool Expert | `tool-expert` | 選對 MCP 工具、串複雜工作流、除錯工具失效 | MCP 失效、複雜工具鏈 |
| 📚 Researcher | `web-researcher` | 抓官方文件、API spec、錯誤碼含義，**幻覺解毒劑** | API 使用不確定時 |

### Workflow 圖解

```
         ┌─────────────┐
         │  Your Task  │
         └──────┬──────┘
                │
       ┌────────▼────────┐
       │   📋 planner    │ ← 3+ 檔案才呼叫
       └────────┬────────┘
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ fullstk │ │ fullstk │ │ fullstk │ ← 平行 P7 執行
└────┬────┘ └────┬────┘ └────┬────┘
     └───────────┼───────────┘
                 ▼
         ┌──────────────┐
         │  🔍 critic   │ ← 強制 pre-deploy review
         └───────┬──────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
 ┌──────────────┐  ┌─────────────┐
 │ 🐛 debugger  │  │   Deploy    │
 └──────────────┘  └─────────────┘
```

> 安全敏感工作額外繞路：`critic` flag → `vuln-verifier` 寫 PoC → fix 或開 PR。

## 方法論：三條紅線 × P7/P9/P10 × PUA 模式

### 三條紅線（所有 agent 強制）

- **🔒 Closure Discipline 閉環紀律**：每個任務都要有明確 DoD，「這樣大概夠了」不是結束。
- **📎 Fact-Driven 事實導向**：所有判斷必須引用實際程式碼與行號。「應該」「可能」「大概」算違反。
- **✅ Exhaustiveness 窮盡原則**：Checklist 不能跳過，清爽項目要明確註記「已檢查、無問題」。

### P7 / P9 / P10 模式切換

> 這不是 role-play，而是 Claude 根據任務規模自動切換的**工作模式**。

| 規模 | 模式 | 行為 |
|------|------|------|
| 單一功能 | **P7 資深工程師** | 設計 → 影響分析 → 實作 → 三問自審 → `[P7-COMPLETION]` |
| 多模組、3+ 檔案 | **P9 技術主管** | 把任務拆成六元素 Task Prompt，**禁止寫 code**，輸出是 prompt |
| 跨團隊、5+ sprint | **P10 CTO** | 輸出策略文件：目標、成功指標、風險、時程、資源 |

### PUA 模式（高壓觸發器）

以下條件任一發生，agent 切進窮盡模式：

- 同一任務失敗 2+ 次 → 寫三個新假設，禁止沿用舊方向
- 差點要說「我無法解決」→ 禁止，強制查文件與原始碼
- 被動等指令 → 自己找下一步
- 使用者說「try harder」/「為什麼又失敗」→ 進入反省模式
- 使用者說「不要再被打臉」→ 每個假設用三種方式交叉驗證

> 來源註記：**P7/P9/P10 與 PUA 模式改編自 [tanweai/pua](https://github.com/tanweai/pua)**（中國探微安全實驗室，MIT License），原版是帶 KPI、排行榜、自演化追蹤、Loop 模式的完整 plugin（<https://openpua.ai>）。`my-claude-devteam` 只取核心紀律，換成西式「工程組織」敘事。

## 15 Automation Hooks

| Hook | 觸發點 | 攔截內容 |
|------|--------|----------|
| 💰 `cost-tracker.js` | 每次回應後 | Token 用量 + Opus/Sonnet/Haiku 估算成本，累積到 `~/.claude/stats-cache.json` |
| ✋ `commit-quality.js` | Pre-commit | 擋 JS/TS/Python 的 `debugger` 語句與 hardcoded 秘密 |
| 🔧 `mcp-health.js` | MCP 工具失效 | 偵測 MCP server 異常並建議重啟路徑 |
| 🛡 `config-protection.js` | 寫入關鍵檔 | 保護重要 config 不被誤覆蓋 |
| 🎨 `design-quality.js` | 前端變更 | 檢查 UI code 的 AI slop 徵兆 |
| 📝 `check-console.js` | Pre-commit | 標記 production path 的 `console.log` |
| 📊 `audit-log.js` | 所有工具呼叫 | 保留重要 tool call 的 audit trail |
| 🎯 `batch-format.js` | 多檔編輯後 | 對修改檔案批次跑 formatter |
| 💡 `suggest-compact.js` | Context 壓力大 | 提醒 `/compact` |
| 📈 `accumulator.js` | Session tracking | 累積 session 指標 |
| 🚨 `log-error.sh` | 任何錯誤 | 寫進 `~/.claude/error-log.md` |
| 🧪 `test-runner.js` | 檔案編輯後 | 找 sibling test，跑 vitest/jest，non-blocking 回報 |
| 🔒 `branch-protection.js` | Pre-Bash | **硬擋** force push、**硬擋** 直接在 main/master/production/release/prod commit |
| 📏 `large-file-warner.js` | Pre-Read | 500 KB 警告、2 MB 直接擋，保護 context window |
| 📚 `session-summary.js` | Stop | 寫 session 摘要到 `~/.claude/sessions/` 方便日後搜尋 |

`branch-protection.js` 是很代表性的實戰 hook：偵測當前分支若屬於 `/^(main|master|production|release|prod)$/`，`git commit` 直接 `exit 2`，而 `git push --force` 到這些分支不管目前在哪都硬擋。

## 快速開始

**一行安裝（Plugin 模式）：**

```
/plugin marketplace add NYCU-Chung/my-claude-devteam
/plugin install devteam@my-claude-devteam
```

**選配：安裝方法論 CLAUDE.md**

```bash
# 英文
curl -sL https://raw.githubusercontent.com/NYCU-Chung/my-claude-devteam/main/CLAUDE.en.md -o ~/.claude/CLAUDE.md

# 繁體中文
curl -sL https://raw.githubusercontent.com/NYCU-Chung/my-claude-devteam/main/CLAUDE.zh-TW.md -o ~/.claude/CLAUDE.md
```

**手動安裝（不用 Plugin）：**

```bash
git clone https://github.com/NYCU-Chung/my-claude-devteam ~/my-claude-devteam
mv ~/.claude/agents ~/.claude/agents.bak 2>/dev/null
mv ~/.claude/hooks  ~/.claude/hooks.bak  2>/dev/null
cp -r ~/my-claude-devteam/agents ~/.claude/
cp -r ~/my-claude-devteam/hooks  ~/.claude/
cp ~/my-claude-devteam/settings.example.json ~/.claude/settings.json
```

## 實戰戰績（作者自述）

### critic 是團隊 MVP

在 500–2000 行的中型模組上，`critic` 一次通常能挖出 **20–30 個問題**；在大型 OSS（OpenClaw 352K⭐、Mermaid 87K⭐、Storybook 85K⭐、React Router 56K⭐）一次聚焦審查仍能找出 **5–10 個 issue tracker 沒提過的 bug**。值得注意的實際漏報：

- OpenClaw 352K⭐ 的 **CWE-208 timing-safe comparison gap**，**三次先前的安全強化 PR 都沒抓到**（diff 裡 `!==` 對比 `safeEqualSecret` 的差異）
- auth 相鄰 allowlist 檔案的非原子 `writeFileSync` race，併發時會壞狀態
- Ollama 推理模型辨識的 heuristic regex `/r1/` 誤判其他無關模型

### debugger 救過兩次烏龍 PR

- **Svelte #18083**：看似 infinite-loop reconcile bug，`debugger` 在 HEAD 跑 repro 測試 pass，發現已在 5.44.0+ 修好（PR #17191/#17240/#17550）。
- **Mermaid #6953**：sequence diagram alias+type 組合，`debugger` 發現 11.14.0（PR #7136）已修，作者只是忘了關 issue。

### planner 取代 clarification loop

觸及 3+ 檔案的任務交給 `planner`，原本 30 句來回澄清變一次結構化 Task Prompt。六元素契約逼你**在任何人寫 code 前先講清楚 DoD**。

### vuln-verifier 的「無聊」才是價值

多數被回報的「漏洞」是偽陽性或只對一半。**PoC-or-it-didn't-happen** 協議把「我覺得可以打」這種模糊報告，轉成有實際程式輸出的判決。每個判決同時附**攻擊輸入 + baseline 對照輸入**，確保觸發的確是攻擊本身而不是任意輸入。

## 目前限制與注意事項

- **不是 Kitchen Sink**：作者明講沒附專案特化的 subagent（VPS ops、deploy 自動化、客製整合都要自己加）。
- **CLAUDE.md 專案段落要自補**：基礎設施、repo 列表、部署指令不在公開 repo 裡。
- **不重新散布第三方 skill pack**：需要的工具要自己接。
- **v1.1.0 無 release tag**：repo 沒有 GitHub Release，版號只寫在 `.claude-plugin/plugin.json`；升級只能靠 `/plugin marketplace update`。
- **PUA 模式文化落差風險**：「面試被刷」「不要再被打臉」這類高壓 prompt 對西式團隊接受度未知；README 英文版保留 PUA 用語，在合規敏感團隊可能需要換皮。
- **3 個 agent 改用 Sonnet**（commit `3d26c22`，2026-04-11）：為了成本效率，作者在首日就把部分 agent 從 Opus 降到 Sonnet，哪 3 個未在 README 明示。
- **License 乾淨但歸屬需注意**：MIT，但 P7/P9/P10 / PUA 方法論要回溯引用 tanweai/pua。

## 研究價值與啟示

### 關鍵洞察

1. **「Claude Code 就是一個 coder」是最大的認知落差**：把 Claude 當單人 IC 用，是絕大多數使用者的預設；`my-claude-devteam` 的論點是「它的上限應該是一整個工程組織」，而解鎖方式不是更多工具，而是**把權限與紀律切成 12 份並強制委派**。這個框架實質上在回答：**怎麼把 LLM 的 context 從「一個大腦」切成「一個團隊」**。

2. **P7/P9/P10 是解決幻覺的管理學答案**：hallucination 的根源常是「單一 context 被迫同時做 IC 實作與 tech lead 拆解」。P9 模式明確**禁止 code**、只輸出 Task Prompt；這等於把「拆解」與「實作」兩種認知模式強制分庫，避免同一次 LLM 呼叫既當 CEO 又當 junior。這是**管理學洞察解決 AI 問題**，不是 prompt hack。

3. **「三條紅線」把 Anthropic 系統提示的模糊鼓勵變硬規**：Claude 內建 system prompt 裡已有「不要猜」「附檔名」這類軟指引，但落地執行率極低。`my-claude-devteam` 把這些升級成**可被 hook 與 agent 檢查的硬紀律**（fact-driven 要附行號、exhaustiveness 要明確註記無問題），把「軟規範」轉成「可驗證條件」。

4. **PUA 模式是中國大廠 KPI 文化的 prompt 具象化**：P 級職階 + 封閉回路 + 重複失敗觸發新假設，直接對應中國網路大廠（阿里 P7、騰訊 T3、位元組 2-1）的「結果閉環 + KPI + 窮盡可能」文化。台灣工程師把這套翻成英文、包裝成 dev team，輸出到國際 Claude Code 社群——這是**華語工程文化反向輸出到英語圈**的有趣案例。

5. **15 hooks 是「被坑過」的殘影**：`branch-protection` 硬擋 main commit、`commit-quality` 擋 debugger 語句、`large-file-warner` 500KB 警告、`test-runner` non-blocking 報測試——每條都不是設計出來的好看清單，而是**每條對應一次真實踩雷**。hook 清單的密度可以當成「Claude Code 使用者會遇到的痛點分布圖」。

6. **9 天 218 stars 說明市場在等「組織型」plugin**：同期 Claude Code plugin 多是單一功能（statusline、skill pack、MCP 接線器）。`my-claude-devteam` 首週的成長速度，指向社群對**整合方法論 + agent + hook 的完整工程範本**有強需求，而不是對更多工具本身。

### 與其他專案的關聯

| 對比對象 | 差異 / 啟示 |
|----------|------------|
| [superpowers](superpowers.md) | 兩者都主打「紀律 > 工具」。Superpowers 是 **skill 驅動**（用 flowchart 強制進入特定流程），`my-claude-devteam` 是 **agent 驅動**（把紀律內建到每個 subagent 的 system prompt）。前者更通用，後者更像「已架好的組織」。 |
| [wshobson agents](wshobson-agents.md) | wshobson agents 是**數量導向**的 agent 集合（擴充可選），`my-claude-devteam` 是**精選 12 人 + 嚴格委派**（不鼓勵自己亂加）。適合對比「多工具箱 vs 精簡編制」兩種哲學。 |
| [khazix-skills](khazix-skills.md) | 都是華語圈開發者的方法論輸出。khazix 偏「個人 AI」哲學與學習向；`my-claude-devteam` 偏「工程組織紀律」落地。合起來可以看出華語 Claude Code KOL 的兩條路線：個人成長派 vs 工程管理派。 |
| [KC AI Skills](kc-ai-skills.md) | KC AI Skills 也是中文圈 skill 集合，但 skill 橫向展開（每個 skill 獨立）。`my-claude-devteam` 走**縱向委派 + 強制流程**，更適合團隊 onboard；兩者可互補。 |
| [claude-skills-guide](claude-skills-guide.md) | skills-guide 教你寫好 skill，`my-claude-devteam` 實作「skill 不夠、要升級成 subagent + hook」的下一階；適合讀完 skills-guide 後想再進一階的使用者。 |
| [tanweai/pua](https://github.com/tanweai/pua) | 方法論直系源頭。PUA 原版是單一 skill + Loop；`my-claude-devteam` 把方法論拆散、套進 12 agents，把「單體 pressure skill」工程化為「組織紀律」。若讀者在意**方法論完整度**讀 PUA，在意**團隊範本**讀 my-claude-devteam。 |

### 值得追蹤的後續

- **是否推出 release / v2 路線圖**：目前 `v1.1.0` 沒 GitHub Release，追蹤是否演化出版本化的生命週期。
- **3 個 Sonnet-降級 agent 的選擇邏輯是否公開**：成本效率是 Claude Code plugin 的真正差異化點，這份 trade-off matrix 對其他作者很有價值。
- **國際化後 PUA 敘事的保留比例**：若進一步商業化（企業 plugin 市場），作者會保留「被 PIP」「不要再被打臉」的強烈敘事，還是轉型更中性的「engineering discipline」? 這會是華語工程文化國際輸出的有趣觀察點。
- **社群 fork / 衍生版本**：42 forks 已出現，值得追蹤哪些客製化方向被 merge 回主線（例如新增領域 agent、hook 門檻參數化）。
