---
date: "2026-04-16"
category: "Coding Agent 工具"
card_icon: "material-shield-check"
oneliner: "Karpathy 的 LLM 編程痛點轉化為一份 CLAUDE.md — 四大原則讓 AI 少犯愚蠢錯誤，44K stars"
---

# andrej-karpathy-skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) |
| Karpathy 原始推文 | [x.com/karpathy](https://x.com/karpathy/status/2015883857489522876) |
| Antigravity 完整分析 | [Karpathy CLAUDE.md Skills Guide](https://antigravity.codes/blog/karpathy-claude-code-skills-guide) |
| The Unwind AI 分析 | [Karpathy's AI Coding Agent Rant](https://www.theunwindai.com/p/karpathy-s-ai-coding-agent-rant-in-a-claude-md-file) |
| 10x Claude Skills 分析 | [Linas Substack](https://linas.substack.com/p/10xclaudeskills) |

**作者：** Forrest Chang（同時也是 [Multica](https://github.com/multica-ai/multica) 的作者）

**專案狀態：** ⭐ 44.1K+ stars · 純 Markdown · MIT · 2026-01-27 創建 · GitHub 最快成長的 repo 之一

## 專案概述

andrej-karpathy-skills 是一個只有**一份 CLAUDE.md 檔案**的 repo，卻獲得 44K+ stars——因為它把 Andrej Karpathy（OpenAI 共同創辦人、前 Tesla AI 負責人、「vibe coding」一詞創造者）對 LLM 編程的痛點觀察，轉化為四條可執行的行為準則。

## Karpathy 的三大痛點

> "The models make wrong assumptions on your behalf and just run along with them without checking."

> "They really like to overcomplicate code and APIs, bloat abstractions... implement a bloated construction over 1000 lines when 100 would do."

> "They still sometimes change/remove comments and code they don't sufficiently understand as side effects."

## 四大原則

| 原則 | 解決的問題 | 核心規則 |
|------|-----------|---------|
| **1. Think Before Coding** | 隱含假設、隱藏困惑、缺少取捨 | 不確定就問，不要靜默猜測；有多種解讀要列出來；更簡單的方法存在就反推 |
| **2. Simplicity First** | 過度工程、膨脹抽象 | 不加沒被要求的功能；不為一次性程式碼做抽象；不寫不可能場景的 error handling；200 行能用 50 行就重寫 |
| **3. Surgical Changes** | 附帶影響、改不該改的東西 | 不「改善」相鄰程式碼；不重構沒壞的東西；match 現有風格；只清理自己造成的 dead code |
| **4. Goal-Driven Execution** | 模糊指令、無法驗證的結果 | 把「加驗證」轉成「寫測試 → 讓測試通過」；多步驟任務列出計畫+驗證點；給成功標準而非步驟指令 |

### Goal-Driven Execution 的轉換範例

| 不要這樣說 | 改成這樣說 |
|-----------|-----------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

## Before/After 實際效果

### Export 功能需求
- **Without：** 靜默假設範圍、格式、敏感欄位
- **With：** 列出 4 個假設，問 pagination 偏好

### 折扣計算
- **Without：** Strategy pattern + 多個 class，50+ 行
- **With：** 單一函式，相同功能，最小程式碼

### Bug 修復
- **Without：** 改 15 行，包含不相關的 docstring、type hints、引號格式
- **With：** 只改 3 行，直接修 bug

## 安裝

```bash
# 方法一：Plugin（推薦）
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills

# 方法二：直接下載 CLAUDE.md
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md

# 方法三：附加到現有 CLAUDE.md
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

## 如何知道有效？

- **diff 更乾淨** — 只有被要求的變更
- **更少因過度工程而重寫** — 第一次就簡單正確
- **先問再做** — 釐清問題在實作之前
- **PR 更精簡** — 沒有附帶重構或「改善」

## 目前限制 / 注意事項

- **偏向謹慎而非速度** — 對瑣碎任務（typo fix、one-liner）可能過度嚴格
- **不保證正確性** — 行為準則改善風格，但 LLM 仍可能幻覺或誤解領域需求
- **依賴使用者紀律** — 效果取決於人寫好 success criteria 的能力
- **純文字檔** — 不含腳本、不含驗證工具、不含 agent 定義
- **可能與其他 CLAUDE.md 衝突** — 原則 3（Surgical Changes）可能與「主動重構」類 skill 矛盾

## 研究價值與啟示

### 關鍵洞察

1. **一份檔案 44K stars 說明了「控制 AI 行為」是最大痛點。** 不是缺工具、不是缺模型——而是「AI 太自作主張」。這個 repo 的爆紅證明：教 AI 「不要做什麼」比教它「怎麼做」更有價值。

2. **Karpathy 的痛點觀察本質上是「AI junior engineer 問題」。** 社群稱之為「confident junior developer」——有速度但缺判斷力。四大原則就是資深工程師對 junior 的標準要求：先想再做、保持簡單、只改需要改的、用測試驗證。

3. **Goal-Driven Execution 是最深刻的原則。** 前三條是「限制」（不要假設、不要過度工程、不要亂改），第四條是「賦能」——把模糊指令轉成可驗證目標，讓 LLM 可以自主 loop 直到完成。這呼應了 Karpathy 的觀察：「LLMs are exceptionally good at looping until they meet specific goals.」

4. **Forrest Chang 同時做了 Karpathy Skills 和 Multica，這不是巧合。** Karpathy Skills 控制單個 Agent 的行為品質，Multica 管理多個 Agent 的團隊協作——這是同一個問題的兩個面向：先讓一個 Agent 不犯蠢（skills），再讓多個 Agent 協同工作（platform）。

5. **這份 CLAUDE.md 不到 70 行，刻意精簡。** 因為 CLAUDE.md 佔 context window——太長反而降低效果。這是「less is more」的極致：與其寫 500 行規範，不如寫 70 行精煉原則讓 LLM 自行推導適用情境。

### 與其他專案的關聯

- **vs Boris Cherny 57 Tips：** Boris 的 tips 覆蓋 Claude Code 的全部功能（並行、排程、語音、自動化），Karpathy Skills 只聚焦一件事——改善 AI 的編程行為。Boris 教你「如何用 Claude Code 做更多事」，Karpathy 教你「如何讓 Claude Code 犯更少錯」。
- **vs Multica（筆記庫中）：** 同一作者。Karpathy Skills 是「單 Agent 行為規範」，Multica 是「多 Agent 團隊平台」——先讓每個 Agent 表現好，再把它們組成團隊。
- **vs OpenAI Agent 建構指南：** 指南說「Instructions 減少模糊性 → 改善決策 → 更少錯誤」——Karpathy Skills 就是這個理念的極簡實踐。
- **vs Asgard Skills：** Asgard 封裝 263 個領域方法論（做什麼），Karpathy Skills 封裝 4 條行為原則（怎麼做）。兩者互補——一個提供知識，一個控制行為。
- **對個人 CLAUDE.md 的啟示：** 可以直接 append 到你的 CLAUDE.md。四條原則不與專案特定規則衝突，是通用的「行為底線」。
