---
date: "2026-10-28"
category: "Coding Agent 工具"
card_icon: "material-crown-outline"
oneliner: "Lauren Tan(@poteto,React core、Cursor)的 pstack plugin 入口 skill:一句 /poteto-mode 把任務對到 23 份 playbook 之一、步驟原文抄成 todolist,主控只負責設計 / 審查 / 驗證,實作派給 subagent;配 24 條 principle skill、多模型對抗審查(只收跑得出失敗的 finding)、能實驗就不問人。Cursor 原生,Claude Code 有官方對照表,社群另有多個移植版"
tags:
  - claude-code
  - skills
  - multi-agent
  - ai-coding
---

# poteto-mode(pstack)研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 上游 | [cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack)(v0.15.36,MIT) |
| 入口 skill | `pstack/skills/poteto-mode/SKILL.md` |
| Claude Code 對照 | `pstack/docs/harness/claude-code.md` |
| 社群移植 | [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude)(3.5k★)、[backnotprop/pstack](https://github.com/backnotprop/pstack)(3.0k★,鏡像)、[ericlitman/open-pstack](https://github.com/ericlitman/open-pstack)(531★) |
| 分析 commit | `cursor/plugins@c742dd6`(2026-10-27) |

作者 Lauren Tan(@poteto)待過 Meta、Netflix,現在在 Cursor,也是 React core team 成員(負責 React Compiler)。open-pstack 的 README 引她的訪談說,這套流程讓她一個月 ship 了 1,000 個 PR。我沒看那段訪談,這個數字是轉述。

## 一句話

pstack 是一包 agent skill:1 個入口 `poteto-mode`、23 份 playbook、24 條 principle、二十多個工具 skill。口號是「if you want to go fast, go deep first」,目標是少寫但寫好的 code,做到敢同時開好幾個 agent 平行跑。

## poteto-mode 怎麼運作

`/poteto-mode <任務>` 之後:

1. **對到 playbook**:把任務對到 23 份 playbook 之一,步驟**原文照抄**成 todolist 的前幾項。不做的步驟留著,寫 `skip: <原因>`。都對不上或規模很大,就交給 `figure-it-out` 現場設計一份
2. **第一句重述目標**:用自己的話講使用者的目標、要解的問題、預期的最小改動,不等確認就開工。證據顯示要求的改法本身是錯的,就擺出證據停下來。每個 subagent brief、PR 的 `## Why`、最終報告開頭都要再講一次目標
3. **按情境觸發其他 skill**(Non-negotiables)
4. **回覆時點名用到的 principle** 和它改變的決定,而且只能引用這次 session 真的讀過的 principle

### 主要觸發規則

| 情境 | 動作 |
|------|------|
| 非小改動、架構決策、「確定嗎?」 | `how`:先摸清現有系統 |
| 寫任何 code | 先講 data shape,用 state machine / registry / typed model 代替散落的條件判斷 |
| 跨 function 邊界 | `architect`:平行探索幾種設計 |
| 有爭議的設計 | `interrogate`:多模型對抗審查 |
| 想問「要用哪個做法」 | 先分類:能跑實驗觀察到的(行為、效能、版面)就做 prototype 讓結果決定,只有產品或偏好問題才問人 |
| 任何文字(含回覆) | `unslop`;commit 前 `deslop`,review 前 `no-comments` |
| 量了效能數字 | `benchmark-checklist`,報數字前先解釋限制在哪 |
| 長時間、自主、使用者離開 | `show-me-your-work` 留決策紀錄 |
| skill 本身壞了 | 開獨立 PR 修,不擋主線也不偷偷繞過 |

### 23 份 playbook

Investigation、Bug fix、Perf issue、Hillclimb、Runtime forensics、Trace forensics、Feature、Refactoring、Prototype、Visual parity、Authoring a skill、Eval、Babysit、Shipping、Autonomous run、Orchestrate、Autopilot-full、Autopilot-stack、Session pickup、Pause safely、Multi-phase plan、Worktree cleanup、Opening a PR(其他 playbook 最後都會呼叫它)。

**Feature** 的步驟:

1. `how` 看受影響的子系統
2. `architect` 平行探索設計
3. 寫 throughput checkpoint 四項:阻塞的前置步驟、可平行的工作流、共享可變狀態(預設拆開而不是加鎖)、最小安全拆分
4. 把實作派給 subagent,指定檔案、data shape、成功條件。有多種合理實作就改用 `arena` 讓幾個 runner 比稿。**這步強制,Laziness Protocol 也不能拿來省掉**,因為重點是讓寫和審分開
5. 在對應的真實介面上驗證,「inconclusive」或在錯的介面上驗證都不算過
6. rebase 成小而有序的 commit
7. 設計有爭議就 `interrogate`
8. Opening a PR

**Bug fix** 強調「科學」:自己先重現(不准叫使用者重現,除非講得出控制介面到不了的具體原因);用二分法排除假設;每一行出貨的程式都要對應到 runtime 證據;證據推翻假設就把它帶來的改動 revert;commit 順序是失敗的 repro 先進、修正後進。

### 24 條 principle

分五組,每條是一個獨立的 `principle-*` skill,寫明什麼情境適用:

- **Core**:Laziness Protocol、Foundational Thinking、Redesign from First Principles、Attack the Premise、Subtract Before You Add、Minimize Reader Load、Outcome-Oriented Execution、Experience First、Exhaust the Design Space、Build the Lever
- **Architecture**:Model the Domain、Boundary Discipline、Type System Discipline、Make Operations Idempotent、Migrate Callers Then Delete Legacy APIs、Separate Before Serializing Shared State
- **Verification**:Prove It Works、Fix Root Causes、Sequence Work into Verifiable Units、Test Behavior Not Implementation、Explain the Number
- **Delegation**:Guard the Context Window、Never Block on the Human
- **Meta**:Encode Lessons in Structure(同一句指示寫第二次,就改成 lint、flag 或 script)

### Subagent 規則

- 主控 chat 跑 playbook,實作一律派給 `poteto-agent`。主控要自己看 diff、自己寫總結,不轉貼 subagent 的話
- **新工作開新 subagent**:修正、重試、下一件事都開新的,把原始 brief、後來的指示、前一個 agent 的報告和分支整理進去。理由是用中斷接續會悄悄漏掉指示。只有需要它的本機 checkout、未 commit 改動或還在跑的 process 時才續用
- 預設 code 給 `grok-4.7-xhigh-fast`,判斷和文字給 `claude-opus-5-5-xhigh`,最難的改動也給 Opus。只有 CI 紅了或有人正被擋住才用 fast 模式
- 第二意見是「同一個 prompt 換一個模型」,兩邊同意就是強訊號

### Autonomy

- 可逆的動作和對外動作(team chat、更新 ticket、跑 eval)直接做
- 一定要停:force-push 共用分支、deploy、刪資料、發訊息給客戶
- 「No is an acceptable answer」:被問要不要加 scope,真心覺得不值得就說不值得,不預設同意

### 回覆文風

短句、一句一件事;全文禁用破折號;句中冒號也禁用(列表前的冒號可以);每個論點同一句內標明是實測、推論還是猜測;不准編造連結或引用;能自己跑的檢查不要丟給使用者。

### interrogate

幾個不同模型的對手各自在 worktree 裡想辦法打爆改動。brief 明講:**沒有實際跑過的不要報**,風格、命名、需要未來改動才會出事的風險都排除。主控再把每個 finding 的指令重跑一次,確認真的失敗、而且違反意圖才保留。只回報 finding,不自己修。

## 在 Claude Code 使用

```text
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
/pstack:setup-pstack          # 選模型與 effort,寫到 ~/.claude/rules/pstack-models.md
/pstack:poteto-mode <任務>
```

- 第三方 marketplace 預設不自動更新,要到 `/plugin` 的 Marketplaces 分頁打開
- `docs/harness/claude-code.md` 是官方對照表:`Task` → `Agent`、`AskQuestion` → `AskUserQuestion`、`environment: "cloud"` → `isolation: "worktree"`、`claude-opus-5-5-xhigh` → `model: "opus", effort: "xhigh"`
- Grok / GPT 這類非 Claude 角色會退回 session 模型;Bugbot、Automations、cloud agents 這些 Cursor 專屬功能會跳過,留一行 `Skipped in Claude Code: ...`
- 想保留多模型陣容,社群的 open-pstack 用各家 CLI 把工作派給 Codex、Grok 等 9 個 provider,panel 預設 Opus / Sol / Grok 三方

## 值得注意的地方

1. **很重**。沒有「小任務走輕量流程」的分級,連小功能都要 how → architect → 派 subagent → 驗證 → PR,還預設 xhigh effort 加多模型 panel。token 成本會比一般用法高很多,這是我從設計推的,沒實測
2. **「能實驗就不問人」的分類規則很值得借**。把「要不要問人」變成「這是事實還是偏好」的判斷,比單純說「少打擾使用者」好執行
3. **interrogate 只收跑得出失敗的 finding**,直接解決 AI code review 一大堆雜訊和「可能會有問題」的通病
4. **把 playbook 步驟原文抄進 todolist、不做的寫 skip 理由**,讓 agent 很難悄悄跳步驟,人也看得到它跳了什麼
5. **Cursor 綁定程度不低**:預設模型陣容、Bugbot triage、custom mode、`/loop`、cloud agent 都是 Cursor 的東西。在 Claude Code 能用,但有一部分會降級

## 跟其他筆記的關係

- [Ponytail](ponytail.md) 也是「最小改動」取向,但只管寫 code 時的 scope;poteto-mode 的 Laziness Protocol 只是 24 條原則之一,整體是完整的工程流程
- [Superpowers](superpowers.md) 同樣是「一包 skill 規範整個開發流程」,可以對照兩者怎麼切 playbook
- [humanlayer/skills](humanlayer-skills.md) 的 context engineering 跟 Guard the Context Window、fresh subagent 規則講的是同一個問題
