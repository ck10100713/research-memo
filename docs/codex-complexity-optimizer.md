---
date: "2026-06-01"
category: "Coding Agent 工具"
card_icon: "material-speedometer"
oneliner: "Codex skill：掃描 codebase 複雜度熱點、產生「只報告不亂改」的安全優化報告"
tags:
  - skills
  - software-engineering
  - automation
---

# Codex Complexity Optimizer 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/Kappaemme-git/codex-complexity-optimizer> |
| npm 套件 | `codex-complexity-optimizer`（v0.1.1, MIT） |
| Codex Skills 官方文件 | <https://developers.openai.com/codex/skills> |
| Awesome Codex Skills | <https://github.com/ComposioHQ/awesome-codex-skills> |
| Skills in OpenAI Codex（背景文章） | <https://blog.fsck.com/2025/12/19/codex-skills/> |

> Repo metadata（擷取於 2026-06-01）：883 stars、57 forks、Python、MIT、建立於 2026-05-15。短短半個月衝到近 900 星，是當前 Codex skill 生態的熱門範例。

## 專案概述

`codex-complexity-optimizer` 是一個 **OpenAI Codex 的 Agent Skill**，目標是讓 Codex 掃描整個 codebase、找出演算法複雜度與效能熱點（nested loops、N+1 query、重複掃描、render 中的昂貴計算等），並產生**結構化的優化報告**。

它解決的核心痛點是：讓 LLM 做效能優化很危險——模型常常「自作主張」改寫程式碼，破壞既有行為、API、輸出順序或測試。這個 skill 用一條明確的**安全契約**收斂這個風險：

> **預設只分析、產報告，不碰任何檔案。只有使用者明確說「implement / fix / optimize / apply / refactor」時才動 code。**

適用場景：接手陌生 codebase 想先做效能體檢、code review 前的熱點盤點、想要 LLM 給「可審查的優化建議」而非直接 PR。

## 核心設計：分析與修改分離

整個 skill 的價值集中在 `SKILL.md` 定義的行為契約，而非掃描器本身。

```
使用者說「analyze / scan / audit / give me a report」
        │
        ▼
   ┌─────────────────────────┐
   │  report-only 模式（預設）  │  ← 不修改任何檔案
   │  輸出：file:line / 現複雜度 │
   │  / 建議改法 / 改後複雜度    │
   │  / 風險等級 / 需要的測試    │
   └─────────────────────────┘
        │
使用者明確說「implement / fix / optimize」
        ▼
   ┌─────────────────────────┐
   │  implement 模式           │  ← 才會改 code，且要跑測試
   │  最低風險優先、localized   │
   │  改前後跑 narrow→broad 測試 │
   └─────────────────────────┘
```

## 技術架構

專案以 npm 套件分發，安裝後把 skill 複製到 Codex 的 skills 目錄：

```
npm install -g codex-complexity-optimizer
# postinstall 自動執行 scripts/install.js
# → 複製到 ${CODEX_HOME:-~/.codex}/skills/complexity-optimizer
```

| 檔案 | 角色 |
|------|------|
| `SKILL.md` | skill 主體：frontmatter（name/description 供 Codex 漸進式載入）+ 5 步工作流 + 安全檢查清單 |
| `agents/openai.yaml` | Codex UI 顯示資訊（display_name、預設 prompt） |
| `scripts/analyze_complexity.py` | 第一手熱點掃描器（mixed-language） |
| `references/optimization-playbook.md` | O(n²)→O(n log n)/O(n) 的標準轉換手冊 |
| `references/report-template.md` | 報告輸出模板 |
| `scripts/install.js` | npm postinstall 安裝器 |

### 掃描器：刻意「啟發式」而非完整靜態分析

`analyze_complexity.py` 是純標準函式庫（無第三方依賴）的單檔掃描器，支援 Python / JS / TS / JSX / TSX / Java / Go / C / C++ / C# / Ruby / PHP / Swift。它用**兩套策略**：

| 語言 | 策略 | 精準度 |
|------|------|--------|
| Python | `ast` 解析 → `NodeVisitor` 追蹤 `loop_depth` | 高（真正理解巢狀結構） |
| 其他語言 | 正則 + 縮排堆疊（`loop_stack`）模擬巢狀 | 低（基於文字啟發式） |

偵測的 pattern（severity 分 high/medium/info）：

- **nested-loop**（high）— 巢狀迴圈疑似 O(n²)
- **membership-in-loop**（medium）— 迴圈內 `in` / `.includes()` / `.indexOf()`，疑似 O(n·m)
- **sort-in-loop**（high）— 迴圈內重複排序
- **io-or-query-in-loop**（high）— 迴圈內 `fetch`/`query`/`findMany`/`execute`，疑似 N+1
- **render-derived-work**（medium）— UI component（大寫開頭函式）render path 內的 `.filter/.map/.sort/.reduce`

作者對掃描器的定位很誠實，寫在 SKILL.md 裡：

> *"It intentionally favors readable leads over perfect static analysis."*
> *"Treat scanner output as leads, not proof."*（把輸出當線索，不是證據）

JSX/TSX 的 component 偵測用 `component_ranges()`：偵測到大寫開頭的 function/const 就假設後續 ~120 行是 component body，用 brace balance 估算邊界——典型的「夠用就好」啟發式。

## 快速開始

```bash
# 安裝
npm install -g codex-complexity-optimizer

# 在 Codex 中（report-only，不改檔案）
Use $complexity-optimizer to analyze this codebase and give me a report.

# 明確要求實作（才會動 code + 跑測試）
Use $complexity-optimizer to implement the lowest-risk optimization
from the report and run the relevant tests.

# 也可單獨跑掃描器
python3 scripts/analyze_complexity.py /path/to/repo --format markdown
python3 scripts/analyze_complexity.py /path/to/repo --format json
```

## 優化安全檢查清單（最有價值的部分之一）

SKILL.md 與 playbook 列出一份「改 code 前必須確認」的清單，這是把 LLM 常見的優化翻車點明文化：

**改之前確認：**

- 資料量夠大，複雜度才有意義（小資料 / 冷路徑不要動）
- 優化是否保留**輸出順序**（caller 可能依賴）
- object identity、mutability、reference sharing 是否屬於 public behavior
- cache 是否有合理的失效策略
- 去重是否會把「顯示標籤相同但實際不同」的記錄錯誤合併
- DB 批次化是否保留 tenant / 權限 / soft-delete / 分頁 / 排序約束

**Playbook 的「What Not To Do」：**

- 資料量小或冷路徑時，別把清楚的線性程式碼換成複雜結構
- 不要無失效策略地 cache
- 不要拿 JSON 序列化當通用 key（除非格式穩定且無碰撞）
- 沒有測試與 caller 證明順序無關前，別改 public ordering
- 別為了 O(n)→O(n log n) 而換，除非它解掉更大的瓶頸或啟用批次化

## 目前限制與注意事項

- **掃描器是啟發式的**：非 Python 語言靠正則 + 縮排判斷巢狀，會有 false positive / false negative。輸出僅供初篩。
- **複雜度估算交給 LLM**：掃描器只標 pattern，真正的「現複雜度 / 改後複雜度」由 Codex 讀周邊程式碼推斷，品質取決於模型。
- **版本仍早期**（v0.1.1）：功能聚焦，沒有 CI、benchmark harness 整合等進階能力。
- **依賴 Codex 遵守契約**：「只報告不改檔」是靠 prompt 指令約束模型，不是硬性 sandbox；理論上模型仍可能越界，需人工把關。

## 研究價值與啟示

### 關鍵洞察

1. **「分析 / 修改」兩階段契約是 LLM 改 code 的安全模式範本。** 真正讓人敢用的不是掃描器，而是「預設只讀、明確指令才寫」這條規則。任何讓 AI 動既有程式碼的工具，都該內建這種 opt-in 的破壞性操作閘門——這與本研究站既有的 `careful` / `guard` 安全 skill 哲學一致。

2. **「leads, not proof」的誠實定位是工程務實主義。** 作者沒有假裝做完整靜態分析（那需要型別推導、call graph、別名分析），而是用 80 行能搞定的啟發式抓出 80% 的明顯熱點，再把判斷權交給 LLM 的語境理解。**這正是 LLM 時代工具設計的甜蜜點：機械化做粗篩，語意理解做精判。**

3. **安全檢查清單把「優化翻車的隱性知識」明文化。** 「去重別合併同標籤的不同記錄」「DB 批次別漏掉權限/分頁」這些都是資深工程師踩過坑才會記得的細節。把它寫進 skill，等於讓 LLM 繼承這份直覺——這是 skill 作為「可攜帶的工程經驗載體」的最佳示範。

4. **混合語言策略反映現實 codebase。** 用 Python AST 做精準偵測、其他語言退回文字啟發式，承認了「一個工具不可能對所有語言都做深度分析」，而是按投資報酬率分配精準度。

5. **npm 分發 + postinstall 自動安裝，降低 Codex skill 的採用門檻。** 把 skill 包成 npm 套件、`postinstall` 自動複製到 `~/.codex/skills/`，是 Codex skill 生態走向「套件化分發」的訊號——對比 Claude Code 的 plugin marketplace，兩邊都在解決「skill 如何被發現與安裝」的問題。

### 與其他研究筆記的關聯

- **vs. Claude Code Skills 生態**（`andrej-karpathy-skills`、`asgard-skills`、`khazix-skills` 等）：本站累積了大量 Claude Code skill 研究，這是少數的 **Codex（OpenAI）skill** 案例。兩邊的 skill 機制高度相似（SKILL.md + frontmatter + 漸進式載入 + scripts/references 子目錄），印證了「Agent Skill」格式正在跨廠商收斂成準標準。
- **vs. 安全護欄 skill**（`careful` / `guard`）：本專案的「report-only 預設」與這些 skill 的「破壞性操作前先警告」是同一套防呆哲學的不同實作。
- **vs. Code Review 類研究**（`code-review-graph`、`difftastic`）：都聚焦在「不改 code 先給可審查的洞察」，差別在這個專注效能 / 複雜度維度。
- **掃描器設計可借鏡到本站 `research` skill 的 `sync.py`**：兩者都是「單檔、零依賴、啟發式夠用就好」的 Python 工具，務實主義一脈相承。
