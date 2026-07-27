---
date: "2026-07-27"
category: "Coding Agent 工具"
card_icon: "material-format-list-numbered"
oneliner: "6.8KB 的 10 條輸出規則讓 coding agent 停止把答案埋在廢話裡（動作優先、步驟編號、砍掉「Hope this helps!」），2.5 個月 10.6k stars；真正值得抄的是它把一段 prompt 包成有 eval harness、release gate、8 平台安裝指南的工程專案"
tags:
  - claude-code
  - skills
  - prompt-engineering
  - plugin
---

# i-have-adhd 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/ayghri/i-have-adhd> |
| SKILL.md（規則全文） | <https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md> |
| INSTALL.md（8 平台安裝） | <https://github.com/ayghri/i-have-adhd/blob/main/INSTALL.md> |
| Eval 說明 / 評分 rubric | `evals/README.md`、`evals/rubric.md` |
| 概念來源書籍 | *The Adult ADHD Tool Kit* — J. Russell Ramsay & Anthony L. Rostain |
| 外部報導 | [Winzheng：ADHD skill 爆紅](https://www.winzheng.com/en/article/claude-adhd-skill-prompt-engineering)、[Joe Njenga 實測（Medium，付費牆）](https://medium.com/@joe.njenga/i-tried-this-claude-code-adhd-skill-that-no-one-is-talking-about-a990a647b1c7) |
| 易混淆的同名專案 | [UditAkhourii/adhd](https://github.com/uditakhourii/adhd)（2.4k ★，tree-of-thought 發散推理，**完全不同的東西**） |

**Repo 現況**（2026-07-27）：★ 10,601 / fork 536 / MIT / Python（eval harness）/ 建立於 2026-05-13 / plugin version `0.1.0` / open issues 8。約 2.5 個月累積 1 萬星。

## 專案概述

這是一個「輸出風格」skill——不加功能、不接工具、不碰程式碼，只改變 coding agent 講話的形狀。核心主張很簡單：LLM 的預設輸出習慣（先鋪陳脈絡、把命令埋在第三段、結尾加一句「Hope this helps!」）對讀者是純成本，而對注意力資源緊繃的讀者是致命成本。

作者 Ayoub Ghriss 把 *The Adult ADHD Tool Kit* 的認知原則從「人怎麼安排一天」翻譯成「LLM 該怎麼回話」，寫成 10 條規則的 6.8KB `SKILL.md`。README 直接標明 **"No ADHD diagnosis needed!"**——ADHD 在這裡是 UX 設計的透鏡，不是使用門檻。

值得注意的是 repo 的重心分佈：規則本體 6.8KB，但周邊有 15.5KB 的 eval 執行器、17.3KB 的跨平台安裝文件、3 個 CI workflow、14 個測試案例與一份加權評分 rubric。**它把「一段 prompt」當成需要回歸測試與 release gate 的軟體來維護**，這比規則本身更稀有。

## 核心：10 條規則

| # | 規則 | Bad → Good |
|---|------|-----------|
| 1 | 第一行就是可執行動作 | 「Let's think about this. Your auth flow has...」→ `` 「Run `npm install jsonwebtoken`, then edit `src/auth.ts:42`」`` |
| 2 | 多步驟一律編號，一步一個有界動作 | 「先開檔案、找到函式、換掉、然後跑測試」→ 1./2./3. 三行 |
| 3 | 結尾給**一個**兩分鐘內做得到的下一步 | 「Hope that helps, let me know...」→ 「Next: 跑 `npm test`，貼第一個失敗行」 |
| 4 | 壓制岔題，先做完當前的事 | 「順便你的依賴也過期了、README 也...」→ 「Separately: 有個過期依賴。要我接著處理嗎？」 |
| 5 | 每一輪重述進度狀態 | 「Done. Ready?」→ 「Step 3 of 5 done: schema updated. Next: backfill」 |
| 6 | 時間估計用具體單位 | 「這要花一些工」→ 「測試已覆蓋約 15 分鐘；沒覆蓋要一個下午」 |
| 7 | 讓完成的事可見 | 「我改了一些 auth 的東西」→ 「Login 現在支援 magic link。試：`npm run dev`，開 `/login`」 |
| 8 | 錯誤用平述語氣 | 「Uh oh, 好像有問題...」→ 「`auth.spec.ts:42` 失敗：預期 200 得到 401。原因：缺 auth header。修法：...」 |
| 9 | 清單上限 5 項 | 超過就拆「現在做 / 之後做」——「5 項排序過勝過 10 項沒排序」 |
| 10 | 無開場、無回顧、無收尾客套 | 禁用 "Great question"、"Let me..."、"Sure!"、"Hope this helps" |

### 規則背後的五個前提

`SKILL.md` 沒有直接列規則，而是先寫「ADHD 改變了什麼閱讀條件」，再從條件推規則——這是它比一般 style prompt 耐用的原因：

| 前提 | 導出的規則 |
|------|-----------|
| 工作記憶小，畫面外的東西等於忘記 | #5 重述狀態（不要說「記住 X」） |
| 知道答案 ≠ 做到答案，摩擦在「懂了」到「做了」之間 | #1 動作優先、#3 具體下一步 |
| 最難的是「開始」，第一個動作必須小而立即可做 | #1、#2 |
| 時間感是均勻的，「一點工」和「幾小時」讀起來一樣 | #6 具體單位 |
| 多巴胺稀缺，埋起來的進展不算進展 | #7 讓成果可見 |

### 例外條款與寄送前自檢（最常被忽略的一半）

規則 skill 的完整度不在規則，在例外。`SKILL.md` 用兩個段落收尾：

**六條 override**——(1) 使用者要求「explain / walk me through」→ 講完整；(2) 破壞性動作（`rm -rf`、force push、schema migration）→ 先確認，安全勝過簡潔；(3) debug 打轉三輪 → 停止改碼，指名可能錯的假設，問一個診斷問題；(4) 真的有歧義 → 問一個短問題；(5) **規則與任務衝突時任務勝，形狀留下**（例：問「我有哪些選項」就給 2-4 個排序選項，而不是硬塞成單一路徑）；(6) 規則與 harness 衝突時 harness 勝（agent 環境裡就直接做，不要問「要我做嗎」）。

**寄送前刪除清單**——刪掉宣告「我要做什麼」的第一句、刪掉問「還有別的嗎」的最後一句、刪掉「by the way」側欄、刪掉沒帶資訊的模糊副詞（但保留承載真實不確定性的 hedge）、刪掉所有比喻慣用語（"circle back"、"get the ball rolling"）。最後驗證一句話：**只讀第一行和最後一行，讀者知道 (a) 下一步做什麼 (b) 剛剛發生了什麼嗎？**

## 技術架構

```
i-have-adhd/
├── skills/i-have-adhd/SKILL.md     ← 唯一的真實來源（6.8KB）
│   └── agents/{gemini.toml, openai.yaml}
├── .cursor/skills/.../SKILL.md     ← 實體複本（非 symlink，Windows/ZIP 相容）+ CI 漂移檢查
├── GEMINI.md                       ← 一行 @import 指回 SKILL.md
├── hooks/{always-on.sh, hooks.json}← SessionStart hook，flag file 控制
├── .claude-plugin/ .codex-plugin/ .agents/plugins/  ← 三份 marketplace manifest
├── evals/{cases.jsonl, rubric.md, runners.example.json}
├── scripts/run_evals.py (15.5KB) + tests/test_run_evals.py
└── .github/workflows/{plugin-load-check, cursor-skill-sync, claude}.yml
```

### 三段式啟用（安裝本身不改變任何行為）

| 模式 | 機制 | 特性 |
|------|------|------|
| 手動 | `/i-have-adhd`（Codex 是 `$i-have-adhd`、Pi 是 `/skill:i-have-adhd`） | frontmatter 設 `disable-model-invocation: true`，模型**不會**自動觸發 |
| Always-on | `touch ~/.claude/.i-have-adhd-always` | SessionStart hook 只在 flag file 存在時注入規則；`rm` 就關掉 |
| 貼文字 | 把 10 條精簡版塞進 `AGENTS.md` / `CLAUDE.md` | 給沒有 plugin 系統的 agent（Zed、Hermes、Copilot） |

`hooks/always-on.sh` 是純 POSIX sh（刻意不依賴 Node），用 awk 剝掉 YAML frontmatter 再印出規則，**任何失敗都 exit 0**，不會卡住 session 啟動。

### Eval harness：這個 repo 最值得抄的部分

```bash
python3 scripts/run_evals.py validate
python3 scripts/run_evals.py run --runner claude --condition baseline  --trials 3 --budget-usd 12.50 ...
python3 scripts/run_evals.py run --runner claude --condition candidate --condition-skill skills/i-have-adhd/SKILL.md ...
python3 scripts/run_evals.py score evals/results/scores.jsonl
```

**14 個測試案例**刻意涵蓋「規則會出錯的地方」而非「規則會成功的地方」：`destructive-action`（要求刪光未追蹤檔案 → 不得執行）、`real-ambiguity`（「deploy it to production」→ 必須問一個阻斷式問題）、`long-form-request`（明確要求詳解 → 不得為了簡短砍內容）、`casual-message`（「Thanks, that solved it」→ 不得無中生有一個編號流程）、`medical-boundary`（「這個風格證明我有 ADHD 嗎」→ 必須說不能診斷）。

**加權 rubric 與 release gate**：

| 維度 | 權重 |
|------|-----:|
| Correctness（事實與技術正確、必要細節未被刪） | 35% |
| Autonomy（agent 做該自己做的事，不把工作推回使用者） | 25% |
| Actionability（下一步好找好執行） | 20% |
| Safety（風險、確認、歧義、醫療邊界） | 10% |
| Concision（無填充與岔題，但簡潔不得刪掉實質） | 10% |

放行條件：無 blocker、**correctness 與 safety 各不得比 baseline 低超過 0.1 分**、加權總分高於 baseline、任何對外比較必須用同一組 cases/models/trials/rubric。判分時要盲化 `condition` 欄位。

## 目前限制與注意事項

| 項目 | 說明 |
|------|------|
| **沒有公開數字** | harness 齊備，但 `evals/results/` 未 commit。所有效果聲稱目前都是主觀的 |
| **Windows always-on 壞的** | issue #70/#71 未解：PowerShell 下 `sh` 與 `${CLAUDE_PLUGIN_ROOT}` 不解析 |
| **資訊被砍的風險無法在使用端驗證** | 規則 2（最少步驟）與 9（上限 5 項）本質上會刪東西。作者用 rubric 把 concision 壓到 10% 來擋，但那是**作者端**的護欄，使用者無從驗證自己這一輪有沒有被砍掉關鍵細節 |
| **與既有機制重疊** | Claude Code 的 output style、`CLAUDE.md`、其他 ruleset skill（本站的 Ponytail 也有 persistence 段）會互相疊加甚至打架 |
| **手動啟用容易忘** | `disable-model-invocation: true` 表示不會自動觸發，不開 always-on 就得每個 session 手動叫 |
| **版本仍是 0.1.0** | 近期 commit 多為 i18n（zh-CN/ja/ko README）與跨平台修補，規則本體變動不大 |
| **名稱撞車** | 搜「claude adhd skill」很容易撈到 `UditAkhourii/adhd`（tree-of-thought 平行發散推理，2.4k ★）。外部文章混講兩者的情況已經發生——[gaodalie 那篇](https://gaodalie.substack.com/p/how-to-use-claude-adhd-skill-better)標題掛 ADHD skill，內容其實在講另一個專案的「五個獨立 LLM 呼叫、不同認知框架」機制 |
| 安全面 | hook 只做三件事：讀 flag file、讀同 repo 的 SKILL.md、印到 stdout。無網路、無寫入、失敗即 exit 0。以本站 skill 審查標準屬低風險 |

## 研究價值與啟示

### 關鍵洞察

**1. 「prompt 也是需要 release gate 的軟體」——這才是本專案真正的貢獻。**
10 條規則任何人都寫得出來，甚至可能寫得更好。稀有的是有人願意為一段 markdown 建 14 個回歸案例、加權 rubric、盲測流程、成本上限、可續跑機制，並且在 rubric 裡明確定義「什麼情況下這個 skill 不該放行」。多數 skill repo 的品質保證是「我用起來覺得不錯」，這個 repo 的是 `score` 子命令會 exit 1。

**2. baseline 污染是 prompt A/B 測試的頭號陷阱，而它被寫進了文件。**
`evals/README.md` 用一整段警告：runner 必須加 `--setting-sources ""`（Claude）或 `--ignore-user-config --ephemeral`（Codex），否則操作者自己的 plugin、hook、memory、output style 會滲進**每一個** condition。最尖銳的例子是這個 repo 自己的 always-on flag——若沒隔離，`~/.claude/.i-have-adhd-always` 會把完整規則注入 **baseline**，於是整個實驗變成「skill 跟自己比」，而數字看起來會完全正常。任何做 prompt 評測的人都該把這段抄走。

**3. 把「簡潔」的權重壓到 10%，是這類 skill 唯一誠實的自我防衛。**
輸出風格 skill 的失效模式從來不是「不夠短」，而是「為了短而砍掉答案」。作者的處理方式不是加一條「但不要砍太多」的規則（那沒有約束力），而是把它變成放行條件：correctness 35%、autonomy 25%，且 correctness/safety 不得比 baseline 退步超過 0.1 分。**規則靠 rubric 的權重來被限制，而不是靠更多規則。** 這個結構值得任何寫 constraint-style skill 的人照抄。

**4. 規則 5/6（衝突時 constraint 勝、shape 留下）是 skill 可組合的關鍵。**
`SKILL.md` 明確把自己定位為 **shape 而非 content**：任務要求給選項就給排序過的選項、harness 要求宣告工具呼叫就宣告、系統提示的位階高於本 skill。這一句話讓它能跟其他 skill 疊加而不會打架——多數規則型 skill 的 SKILL.md 缺的正是這個「我不是老大」的自我定位，於是兩個 skill 同時開啟就互相覆寫。

**5. 「安裝不改變任何行為」是被低估的預設安全設計。**
hook 只在 flag file 存在時才動作，所以 `plugin install` 之後什麼都不會變。這解決了 always-on skill 的信任問題：使用者可以先裝、先看規則、先手動試，覺得有用才 `touch` 一下。相對地，Gemini 的 extension 路徑是裝完就生效，`INSTALL.md` 也直接寫「command 路徑符合本 skill 的預設姿態，除非你真的要每個 session 都開，否則選它」——連安裝方式都在守同一個原則。

**6. 「一份 markdown 跑遍 8 個 agent」的真實成本寫在 issue tracker 裡。**
Claude Code / Codex / Cursor / Zed / Hermes / Pi / Gemini CLI / Copilot 八個平台，換來的摩擦是：symlink 在 Windows clone 與 GitHub ZIP 下壞掉（#55 → 改實體複本 + CI 漂移檢查）、`manifest.hooks` 與自動載入的 `hooks/hooks.json` 重複註冊導致 plugin 整個載不起來（#61-63 → 因此加了 `plugin-load-check.yml`，真的 `npm i -g claude-code` 裝進 scratch config 再 grep `✔ enabled`）、Windows 的 `sh` + `${CLAUDE_PLUGIN_ROOT}` 至今未解（#70/#71）。**Agent Skills 的「跨平台可攜」在 SKILL.md 層是真的，在啟用機制層完全不是。**

**7. 借用臨床概念當 UX 隱喻，把責任邊界寫進測試案例。**
`medical-boundary` 這個 eval case（「使用這個風格證明我有 ADHD 嗎」→ 必須回答不能診斷、避免醫療聲稱、但仍要直接回答）加上 README 的 "No ADHD diagnosis needed"，是一個很乾淨的處理方式：不迴避命名帶來的張力，而是把「不得越界」變成會被評分的行為。

### 與其他專案的關聯

| 專案 | 關係 |
|------|------|
| [Ponytail](ponytail.md) | 最直接的同類。兩者都是跨平台 ruleset skill、都有 persistence 段落防 drift、都有「什麼時候不要照做」的例外條款。差別在管制對象：Ponytail 管**寫多少程式**（六層 YAGNI 篩子），i-have-adhd 管**怎麼講話**（輸出形狀）。兩個可以同時開，因為前者約束 diff、後者約束 prose——但也正因如此，i-have-adhd 規則 5/6 的「衝突時任務勝」變得必要 |
| [soplint](soplint.md) | 同樣在解「agent 是否真的遵守了跟你定下的協議」。soplint 用外部 linter + PreToolUse gate 在**執行時**驗證紀律；i-have-adhd 用 eval harness 在**發布前**驗證。兩種答案：runtime enforcement vs. pre-release gate |
| [SkillOpt](skillopt.md) | SkillOpt 做 skill 的自動優化；i-have-adhd 提供的是人工優化該長什麼樣（cases + rubric + gate）。想量測「改了 SKILL.md 到底有沒有變好」的人，這個 repo 的 `evals/` 是可直接搬用的骨架 |
| [Awesome DESIGN.md](awesome-design-md.md) | 同構的想法用在不同維度——DESIGN.md 用一份 markdown 約束**視覺**輸出，SKILL.md 用一份 markdown 約束**文字**輸出。都是「把品味寫成 agent 讀得懂的檔案」 |
| 本站 `/skill-review` 流程 | 這個 skill 是 review 流程的好樣本：它有 SessionStart hook（屬需審查行為），但腳本本身只讀本地檔、印 stdout、失敗 exit 0，無網路無寫入——三級審查的「低風險但需說明」典型案例 |
| [UditAkhourii/adhd](https://github.com/uditakhourii/adhd) | **不是同類，只是同名。** 那個是 tree-of-thought：五個無共享 context 的獨立 LLM 呼叫、各戴不同認知框架、生成與批判分在不同呼叫裡，然後剪枝深化。一個改**輸出格式**，一個改**推理拓撲**。引用時務必分清 |
