---
date: "2026-06-17"
category: "Coding Agent 工具"
card_icon: "material-content-cut"
oneliner: "把『最懶的資深工程師』裝進 AI agent 的跨平台 ruleset：寫程式前先過六層 YAGNI 篩子，少寫 80-94% 程式碼"
tags:
  - claude-code
  - prompt-engineering
  - skills
---

# Ponytail 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/DietrichGebert/ponytail>（⭐ 22,026、JavaScript、MIT） |
| SKILL.md（核心規則） | <https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md> |
| Benchmark 方法與原始數據 | <https://github.com/DietrichGebert/ponytail/tree/main/benchmarks> |
| 第三方介紹（AgentCrunch） | <https://agentcrunch.ai/article/ponytail-lazy-dev-ai-agents> |
| Agent Skills 目錄收錄 | <https://mcpservers.org/agent-skills/dietrichgebert/ponytail> |
| 作者 | Dietrich E. Gebert |

> 標語：*He says nothing. He writes one line. It works.* 自稱可比無 skill 的 agent **少寫 80-94% 程式碼、快 3-6×、省 47-77% 成本**（Haiku/Sonnet/Opus 各跑 10 次取中位數，可用 `npx promptfoo eval` 自行重現）。

## 專案概述

Ponytail 是一套**跨 AI coding agent 的行為規則集（ruleset / skill）**，核心理念一句話：**「最好的程式碼是你從沒寫的那段」（The best code is the code you never wrote）**。它把那位「在公司比版本控制系統還久、看你寫五十行、一句話不說直接換成一行」的資深工程師，塞進你的 AI agent 裡。

它要解決的問題是 **AI agent 的過度工程傾向（over-engineering）**：你叫 agent 做個日期選擇器，它會去裝 flatpickr、寫一個 wrapper component、加一份 stylesheet，還順便開一場時區的討論。Ponytail 介入後，答案是一行：

```html
<!-- ponytail: browser has one -->
<input type="date">
```

它不是一個套件、不是 MCP server，而是**一份注入到 agent 每輪對話的精簡規則 + 幾個 slash 指令**，靠改變 agent 的決策順序來壓低產出量。適合所有覺得「AI 寫太多沒必要的程式碼」的人。

## 核心機制：六層 YAGNI 篩子

Agent 在寫任何程式前，停在第一個成立的階梯就收手：

```
1. 這東西需要存在嗎？   → 不需要：跳過           (YAGNI)
2. 標準庫能做嗎？       → 能：用 stdlib
3. 平台原生功能有嗎？   → 有：用 native feature
4. 已安裝的依賴能做嗎？ → 能：用現有 dependency
5. 一行能解決嗎？       → 能：就一行
6. 以上皆非            → 才寫「能動的最小實作」
```

**懶，但不失職（Lazy, not negligent）**：信任邊界驗證、資料遺失處理、安全性、無障礙（accessibility）這四件事**永遠不在被砍的範圍**。每個它走的捷徑都會在程式碼留下一個 `ponytail:` 註解，標明「升級路徑」，方便日後需要時補回。

## 功能與指令

| 指令 | 作用 |
|------|------|
| `/ponytail [lite\|full\|ultra\|off]` | 設定強度或關閉；無參數則回報目前等級（預設 `full`） |
| `/ponytail-review` | 審查目前 diff 的過度工程，回傳一份「該刪清單」 |
| `/ponytail-audit` | 審查**整個 repo**（不只 diff）的過度工程 |
| `/ponytail-debt` | 把先前 `ponytail:` 標記的捷徑收成一份「技術債帳本」，避免「之後再說」變「永不」 |
| `/ponytail-help` | 指令速查 |

- **強度分級**：`lite / full / ultra / off`。`ultra` 是「codebase 惹到你本人時」用的。
- **預設等級**可用 `PONYTAIL_DEFAULT_MODE` 環境變數或 `~/.config/ponytail/config.json` 的 `defaultMode` 設定，但**完全不需要設定檔也能跑**。

## 跨平台支援（13 種 agent）

Ponytail 最大的工程亮點是**一套規則、多端適配**。兩種運作層級：

| 模式 | 平台 | 機制 |
|------|------|------|
| **Plugin + 指令 + 常駐** | Claude Code、Codex、Copilot CLI、pi、OpenCode、Gemini/Antigravity CLI、OpenClaw | 透過各家 plugin/extension 機制安裝，含 slash 指令、強度切換、生命週期 hook |
| **Instruction-only（僅常駐規則）** | Cursor、Windsurf、Cline、Copilot（編輯器）、Aider、Kiro | 複製對應的 rules 檔（`.cursor/rules/`、`AGENTS.md`、`.github/copilot-instructions.md` 等），有常駐規則但無指令/hook |

```
# Claude Code
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

Claude Code / Codex plugin 會跑兩個輕量 Node.js 生命週期 hook（需 `node` 在 PATH 上）；若沒有，skill 仍可用，只是「常駐啟用」會安靜略過而非報錯。

## 目前限制 / 注意事項

- **效果依賴宿主 agent 是否忠實執行 prompt**：它本質是 prompt/ruleset 注入，沒有強制力。Agent 可能在長對話中「忘記」規則，或在複雜任務下仍過度發揮。
- **Benchmark 偏向小型日常任務**：五項基準（email 驗證、debounce、CSV 加總、倒數計時、rate limiter）都是「正確答案就是少寫」的題目，天然有利於 ponytail。Production 級任務另有 writeup，但「80-94% less code」這個數字不宜直接外推到所有場景。
- **「懶」的邊界靠 prompt 守住**：安全/驗證/無障礙雖被列為不可砍，但這仍是規則層的約定，遇到 agent 判斷失誤時沒有硬性保障——關鍵程式仍需人工複查。
- **指令僅在 skill-capable 宿主可用**：Cursor/Windsurf 等只能吃常駐規則，拿不到 `/ponytail-review` 這類指令。
- **常駐注入有 token 成本**：每輪對話注入規則文字，雖精簡仍是固定開銷（換來的是產出變少的淨節省）。

## 研究價值與啟示

### 關鍵洞察

1. **AI agent 的預設失敗模式是「過度工程」，而非「能力不足」。** Ponytail 22k stars 的爆紅，反證了一個被廣泛感受到的痛點：現代 LLM 不缺生成能力，缺的是**克制**。把工程哲學裡最反直覺的美德——「少做」——產品化成一個 skill，本身就是對 AI coding 現況的精準診斷。

2. **「決策階梯」比「禁令清單」更能改變 agent 行為。** 它不是列一堆「不要做 X」，而是給一個**有順序的提問流程**（需要嗎 → stdlib → native → 依賴 → 一行 → 最小實作）。讓 agent 在每個決策點先爬階梯，是把抽象原則（YAGNI）轉成**可執行 checklist** 的好範例——這正是 prompt engineering 的精髓。

3. **「Lazy, not negligent」劃出的紅線，是這類 skill 能不能用的關鍵。** 極簡主義最大的風險是把安全/驗證/無障礙一起砍掉。Ponytail 明確把這四項列為不可協商，等於替「偷懶」設了護欄。任何鼓勵 AI「少做」的工具，都必須先回答「哪些事絕不能省」——否則就是在生產 bug。

4. **`ponytail:` 註解 + `/ponytail-debt` 帳本，把「捷徑」變成「可追蹤的技術債」。** 偷懶最怕「之後再說」變「永不」。它在每個捷徑留標記、再用指令把標記收斂成帳本，等於給極簡主義配了一套**債務可見化機制**——這是它比「叫 AI 寫少一點」高明的地方。

5. **「一套規則、13 端適配」示範了 agent skill 的可攜性工程。** 同一份規則，在 plugin-capable 宿主跑成 skill+指令+hook，在只認 rules 檔的編輯器跑成常駐 context。這種「核心邏輯與宿主解耦、靠 adapter 落地」的設計，是 agent skill 想要跨生態散播的標準做法，值得任何想做跨平台 skill 的人參考。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [soplint（AI agent 紀律 linter）](soplint.md) | 同樣針對「約束 AI agent 行為紀律」，soplint 用 lint 規則檢查、ponytail 用決策階梯前置攔截，一個事後查、一個事前擋 |
| [Superpowers](superpowers.md) | 同為跨 agent 的 skill 體系；Superpowers 加能力、ponytail 減產出，剛好是「賦能 vs 克制」兩個方向 |
| [Why Your AI Is Dumbing Down](why-your-ai-is-dumbing-down.md) | 都在處理「AI 產出品質失控」議題；ponytail 從『寫太多』切入，可與其對照 |
| [Andrej Karpathy Skills](andrej-karpathy-skills.md) | 同屬「把資深工程直覺壓縮成 skill」的思路 |
| [軟體工程 56 大定律](laws-of-software-engineering.md) | ponytail 是 YAGNI / KISS 這類經典原則的「agent 可執行版」落地 |
