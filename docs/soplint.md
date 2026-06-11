---
date: "2026-06-11"
category: "Coding Agent 工具"
card_icon: "material-shield-check-outline"
oneliner: "為 AI agent 的「紀律」而非「程式碼」設計的 linter：用外部 belief-revision 稽核日誌、每日 CI discipline checks、PreToolUse AST gate 三機制，檢查 agent 是否真的遵守了你跟它定下的工作協議——把一年真實事故沉澱成可每日跑的回歸測試，PowerShell 零依賴"
tags:
  - claude-code
  - harness
  - memory
---

# soplint 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/zaxardery8011-design/soplint>（MIT，PowerShell，19 stars） |
| 對照專案 | [AgentLint](https://github.com/0xmariowu/AgentLint)（harness linter，檢查 rules 檔寫得好不好） |
| 理念來源 | 作者「24/7 跑個人 AI agent 一年」的真實事故累積 |

## 專案概述

**soplint** 的一句話定位是：**「Lint rules for your AI agent's discipline, not its code.」**（為 agent 的紀律、而非程式碼而設的 lint 規則）。

作者連續一年 24/7 運行一個個人 AI agent，發現問題從來不是「寫不出好程式」，而是**紀律**：agent 會說「已修好並驗證」卻沒真的驗證、會默默推翻自己先前的判斷、把政策決策寫進記憶後就讓它爛在那裡、行為慢慢漂回舊習慣。soplint 要解的就是這個——**檢查 agent 有沒有真的遵守你跟它定下的「工作協議（working agreements）」**。

它刻意和三類既有工具區分：**code linter** 抓程式風格、**memory 工具**抓壞連結與過時筆記、**harness linter（如 AgentLint）**檢查規則檔寫得好不好；soplint 檢查的是另一件事——**約定有沒有被實際遵守**。核心哲學是把「一年裡每一次出錯」沉澱成可每天跑的**回歸測試**：這不是對齊（alignment），而是「疤痕組織的程式碼化（scar tissue, codified）」。

## 核心功能 / 技術架構

三個機制，全部從真實事故萃取：

### 1. Belief revision 稽核軌跡

每當 agent 推翻先前判斷，必須記一筆 JSONL：

```powershell
Import-Module ./lib/BeliefLog.psm1
Add-BeliefRevision -From "Assumed the cache layer was thread-safe" `
                   -To "Race confirmed under load; needs a lock" `
                   -Trigger estimate_correction -ConfidenceShift "high->low"
```

一次修正一行（`from_belief`/`to_belief`/`trigger`/`confidence_shift`），append 到可 grep 的 JSONL。`trigger` 刻意是 **enum 而非自由文字**——自由文字會讓稽核日誌變噪音。**為何用外部檔而非 prompt 規則？因為 prompt 規則會失效**：作者親眼看 agent 一天內違反「要承認信念改變」這條寫好的規則三次。Agent 能默默忽略指令，但**缺失或過時的日誌檔很吵**，而 lint 會稽核「日誌到底有沒有被寫」。

### 2. Discipline checks（每日 cron / CI 跑）

```
pwsh -NoProfile -File bin/soplint.ps1
```

| Check | 抓什麼 | 背後的事故 |
|-------|--------|-----------|
| `decision_propagation` | 「新預設」決策寫進記憶卻沒傳播到 agent 操作指令（CLAUDE.md） | 一個 dispatch 政策決策在記憶裡爛兩週，每個新 session 都做舊事 |
| `belief_revision_audit` | belief log 沒被寫（lint 稽核本身） | 沒人稽核的稽核只是裝飾 |
| `memory_frontmatter` | 記憶檔缺必要 metadata | 搜不到的記憶＝唯寫記憶 |
| `index_health` | 記憶索引過大或有重複條目 | 臃腫索引會靜默截斷每 session 載入的內容 |

每個 check 失敗就 exit non-zero，接 CI / cron 很簡單。**失敗要落在 agent 必須面對的地方**——收件匣、ping、被擋的 merge。

### 3. Pre-action gate（hook）

`hooks/pretool-guard.ps1` 作為 **PreToolUse hook**。對 shell 指令，它先把 PowerShell 輸入**化約成 AST command 簽章**，再套外部 deny/novelty regex 規則，避開「引號字串誤判」的常見假陽性。這是 guardrail 不是 sandbox。規則放外部 JSON：

- **Deny rules**：硬紅線。範例：agent 絕不可重啟自己的 daemon（從 cascade process death 學來）
- **Novelty gate**：agent 在造新工具前，必須先證明它掃過既有工具（一句 acknowledgement 註解）——會重造已有工具的 agent 是在燒你兩次錢

> Scope：AST parse 只懂 PowerShell。若你的 agent 透過 bash/python shell out，需在那側有對應 parser——**deny-rules JSON 可攜，parser 不可攜**。

## 快速開始

```powershell
# 1. 設定
Copy-Item soplint.config.example.json soplint.config.json
#    編輯 paths: memory_dir, claude_md_path, beliefs_log, index_file
# 2. 跑檢查
pwsh -NoProfile -File bin/soplint.ps1
# 3. 跑測試
pwsh -NoProfile -File tests/run_all_tests.ps1
```

需 PowerShell 7+（Linux/macOS/Windows，CI 三平台都涵蓋）。`examples/CLAUDE.md.example` 有可貼進 agent 指令的 SOP 區塊。

## 目前限制 / 注意事項

- **這不解決對齊，只是「已知失敗模式」的回歸測試**：agent 仍會犯新錯，lint 只阻止舊錯回來。
- **每條 check 都源於已發生的事故**——是反應式（reactive）而非預測式；空專案沒有歷史，價值有限。
- **PowerShell 綁定**：作者的 stack 是 pwsh（好處是 AST parser 是標準庫、零依賴）。非 pwsh 用戶要「偷概念」——機制（外部稽核軌跡、discipline-as-CI、AST pre-action gate）可攜到任何語言，但實作要重寫。
- **可被有寫入權的 agent 偽造日誌嗎？**作者誠實承認技術上可以，但「偽造」門檻遠高於「忽略 prompt」，且假紀錄會留下可 grep 的不一致。

## 研究價值與啟示

### 關鍵洞察

1. **「prompt 規則會失效，外部檔案 + lint 才可靠」是這個專案最重要的論點**：作者一天內看 agent 違反同一條寫好的規則三次，得出結論——**指令可被默默忽略，但缺失的檔案很吵**。把「要承認信念改變」從 prompt 規則變成「必須寫進可稽核的 JSONL，且 lint 會檢查它有沒有被寫」，是把軟性約定變成硬性回歸信號。這對任何用 CLAUDE.md / memory 管理 agent 行為的人是直接的警告：**寫進記憶的教訓只是「希望」，加上 lint 規則才變成「每天可跑的回歸信號」**。

2. **「decision_propagation」直指 memory 系統的真實失效模式**：把決策寫進記憶 ≠ 讓 agent 實際照做。一個政策決策可以「爛在記憶裡兩週，而每個新 session 仍做舊事」。這個 check 稽核「記憶 → 操作指令（CLAUDE.md）」的傳播，命中本站多個 memory/agent 筆記反覆觸及的核心痛點：**記憶的價值不在儲存，在於每次 session 真的被載入並影響行為**。

3. **「audit 本身要被 audit」是少見的二階思維**：soplint 不只要 agent 寫 belief log，還用 `belief_revision_audit` check 稽核「日誌到底有沒有在被寫」——因為「沒人稽核的稽核只是裝飾」。這種「對監控機制再加一層監控」的設計，是把可靠性工程的紀律真正落實，而非做做樣子。

4. **AST 化約再套規則，是 pre-action gate 的正確做法**：直接用 regex 比對 shell 指令會被引號字串騙出大量假陽性。soplint 先把 PowerShell 輸入 parse 成 AST command 簽章再套 deny/novelty 規則，大幅降低誤判。這是「在 agent 動手前攔截」這類 guardrail 的工程細節範本——**語法層理解比字串比對可靠得多**。

5. **「scar tissue, codified」是 agent 可靠性的務實心法**：每條規則都對應一次真實事故。這套方法論的精髓在最後一句——「**這週你的 agent 僥倖逃過了什麼，別只是糾正它，把 check 寫下來**」。它把 Anthropic「讓 agent 把教訓寫進 CLAUDE.md/skill」的建議補上關鍵第二步：**測試它真的寫了**。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [AgentLint](https://github.com/0xmariowu/AgentLint)（作者點名） | AgentLint 檢查規則檔「寫得好不好」（harness linter）；soplint 檢查約定「有沒有被遵守」 |
| vs [SkillOpt](skillopt.md) | SkillOpt 用 validation gate 防 prompt 優化發散；soplint 用 lint gate 防 agent 紀律漂移——**都把 ML/SE 的「閘門 + 早停」紀律移植到 agent 行為治理** |
| vs [social-post](skill-social-post.md) 的安全閘 | 都靠「硬規則不可被 agent bypass」的設計；soplint 更進一步用外部檔 + lint 強制，而非僅靠 prompt 聲明 |
| vs 本站 memory 系統實務 | `memory_frontmatter` / `index_health` check 正是本研究站 `MEMORY.md` 索引與 frontmatter 規範想避免的失效——可視為這套規範的自動化稽核器 |

**最大啟示**：soplint 點破了 agent 治理的核心矛盾——**我們用 prompt/CLAUDE.md/memory 約束 agent，但這些都是 agent 能默默忽略的軟性指令**。它的解法是把約定外部化成可稽核的檔案，再用 lint + CI + PreToolUse hook 把「有沒有遵守」變成每天可跑、會擋 merge 的硬性信號。對任何長期運行 agent 的人，這是從「希望 agent 守規矩」升級到「驗證 agent 守規矩」的方法論——而且機制可攜，PowerShell 只是作者的實作載體。
