---
date: "2026-08-06"
category: "Coding Agent 工具"
card_icon: "material-account-tie"
oneliner: "Matt Pocock (Total TypeScript) 把每天用的 agent skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnosing-bugs / improve-codebase-architecture，半年衝到 205k stars"
tags:
  - skills
  - claude-code
---

# mattpocock/skills 研究筆記

> **更新沿革**：初次整理 2026-05-15（當時 90k stars、`.claude/` 佈局）；**2026-08-06 大幅更新**——repo 已 205k stars、遷到 `.agents` 佈局、進了 Claude Code 官方 plugin marketplace，並把 skills 依「誰能呼叫」重新分成 user-invoked / model-invoked 兩軸。caveman、zoom-out 等舊 skill 已從本 repo 移除。

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/mattpocock/skills> |
| 作者 | <https://github.com/mattpocock>（Matt Pocock / Total TypeScript） |
| 安裝器（skills.sh） | <https://skills.sh/mattpocock/skills> |
| Claude Code 官方 plugin | `claude plugins install mattpocock-skills` |
| 作者 newsletter | <https://www.aihero.dev/s/skills-newsletter>（~60,000 訂閱者） |
| 規模 | **205,105 stars / 17,711 forks** / MIT / 創建 2026-02-03（2026-08-06 抓取，**半年破 20 萬星**；5 月時為 90k） |
| Repo 結構 | `skills/`、`docs/`、`scripts/`、`.claude-plugin/`、`.agents/`（含 `adr/`）、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md` |

## 專案概述

**mattpocock/skills** 是 Matt Pocock（Total TypeScript 創辦人、TypeScript 圈最知名教育者之一）把自己每天在用的 agent skills 公開的 repo。slogan 是 **"Skills for Real Engineers — not vibe coding"**，明確劃清跟「GSD / BMAD / Spec-Kit 那種接管整個流程」的差異——他的 skills **設計為小、可改、可組合、且與模型無關（"work with any model"）**，留控制權給工程師。

Repo 在 2026-02-03 建立、半年飆到 **205k stars**，是目前 agent skills 領域社群熱度最高的個人作品集，且**對「Skill 是該被組合的小工具，不是要取代工程師思考的 framework」這個立場做了相當清晰的示範**。

> **從 `.claude/` 到 `.agents/`**：5 月時 repo 圍繞 Claude 打造；如今根目錄同時有 `AGENTS.md` 與 `CLAUDE.md`、skill 來源改放 `.agents/`（連 ADR 都放在 `.agents/adr/`），描述也改成「Straight from my .agents directory」。這反映立場從「Claude skills」轉為**模型無關的 agent skills**，同一套 skill 要能跑在 Claude Code、Codex 等多個 agent 上。

### 兩種安裝哲學：subscribe vs fork

新版把安裝拆成**兩條路、兩種哲學**（README 明說「二選一，兩個都裝會讓每個 skill 出現兩次」）：

```bash
# 路線 A — Claude Code 官方 plugin（managed、read-only、我一 ship 就自動更新）
claude plugins install mattpocock-skills      # 或 session 內 /plugin install mattpocock-skills
#   → 「訂閱」而非「fork」：你拿到託管的整包，不改它、跟著上游走

# 路線 B — skills.sh（把可編輯的 skill 檔複製進你的專案）
npx skills@latest add mattpocock/skills       # 選要哪些 skill、裝到哪些 agent
#   → 「擁有」：檔案是你的、隨便改，要更新才 npx skills update
#   ⚠ 記得把 setup-matt-pocock-skills 一起選進來

# 兩條路都一樣：在 agent 內跑一次 per-repo 設定
/setup-matt-pocock-skills
#   會問你：issue tracker (GitHub/Linear/local files)、triage 用的 label 集合、docs 存放路徑
```

→ 不是丟一包 markdown 就走人，而是**用 setup skill 把 per-repo config 寫進去**，後續其他 skill 自動讀這份 config 運作。原生 Codex plugin 已在 roadmap（見 `.agents/adr/0002`）。

## 四大「失敗模式 → 對應 Skill」設計哲學

Matt 在 README 直接列了「Claude Code / Codex / 其他 coding agent 最常見的四種失敗」，**每種對應特定 skill**：

### 失敗 #1 — Agent 沒做你要的事

> 引用 Pragmatic Programmer：「No-one knows exactly what they want」

**對應 skill**：
- **`/grill-me`** — 對「非 code」場景反覆質問
- **`/grill-with-docs`** ⭐ — 對 code 場景做 grilling + 同步寫進 `CONTEXT.md` 與 ADR

Matt 親口說「這可能是整個 repo 最酷的 skill」。**Grilling 取代「agent 自己揣摩需求」**——對齊先做完再寫 code。

### 失敗 #2 — Agent 太囉嗦

引用 DDD 的 Ubiquitous Language——agent 跟你語言不通，所以用 20 個字描述 1 個概念。

**對應 skill**：`/grill-with-docs` 同時建立 **`CONTEXT.md`**（domain language 字典 + ADR）。

實例（README 直接舉）：
- BEFORE：「There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)」
- AFTER：「There's a problem with the materialization cascade」

→ 一份共享語言文件 = **變數命名一致 + codebase 對 agent 變友善 + 每次思考省 token**。

### 失敗 #3 — Code 不能用

引用 Pragmatic Programmer：「Always take small, deliberate steps. The rate of feedback is your speed limit.」

**對應 skill**：
- **`/tdd`** ⭐ — 強制 red-green-refactor，先寫失敗測試再修
- **`/diagnosing-bugs`** — disciplined diagnosis loop：建立「對這個 bug 會變紅」的 feedback loop → minimise → hypothesise → instrument → fix → regression-test（原 `/diagnose`）

### 失敗 #4 — 蓋出一坨泥球

引用 Kent Beck「Invest in the design of the system *every day*」+ John Ousterhout「The best modules are deep」。

**對應 skill**：
- **`/to-spec`** — 把當前對話直接 synthesize 成 spec 送進 issue tracker（原 `/to-prd`）
- **`/improve-codebase-architecture`** ⭐ — Matt 推薦「每幾天跑一次」的 anti-ball-of-mud skill；新版會產出**視覺化 HTML 報告**列出 deepening 候選，再帶你 grill。README 誠實加註：**「這是一份 survey、不是 rescue」**——老 codebase 上它會找出真候選，但**不會替你把泥球解開**。

## 新版核心：user-invoked vs model-invoked 兩軸（★ 最大概念改動）

新版 README 的 Reference 不再只用「engineering / productivity」分 bucket，而是新增一條**「誰能呼叫」的軸**——這是這半年最重要的設計演進：

| | User-invoked | Model-invoked |
|---|---|---|
| **誰能觸發** | **只有你打 `/xxx`** 才會跑 | 你可以打，**agent 也能在任務吻合時自動抓來用** |
| **職責** | **orchestrate（編排）** | **hold reusable discipline（承載可重用紀律）** |
| **組合規則** | 可呼叫 model-invoked skill，**但不能呼叫另一個 user-invoked skill** | 被 user-invoked 或 agent 呼叫 |

最能說明這個哲學的例子是 **`grilling`**：它被抽成一個 **model-invoked 的「面試 primitive」**，而 `grill-me`、`grill-with-docs`、`triage`、`wayfinder`、`improve-codebase-architecture` 這些 user-invoked skill 全都**組合它**。→ 「小、可組合」不再只是口號，而是**用 orchestrator / primitive 的分層在架構上落實**。

## Skills 完整清單（2026-08-06 現況）

repo 用「bucket 分類 + per-folder README」結構（CLAUDE.md 規定每個 skill 必須在頂層 README、`.claude-plugin/plugin.json`、bucket README 三處同步登錄）：

### Engineering — User-invoked（orchestrator）

| Skill | 用途 |
|-------|------|
| `ask-matt` | **router**：問它「我這情境該用哪個 skill / flow」，導覽所有 user-invoked skill |
| `grill-with-docs` ⭐ | Grilling + 建 domain model + 更新 `CONTEXT.md` 與 ADR 三合一 |
| `triage` | 把 issue 用 state machine 推進不同 triage role |
| `improve-codebase-architecture` ⭐ | 掃 deepening 機會 → 視覺化 HTML 報告 → grill 你選的那個 |
| `setup-matt-pocock-skills` | 安裝其他 skills 前的 per-repo 設定 |
| `to-spec` | 把當前對話 synthesize 成 spec 送進 issue tracker（不再面試，原 `to-prd`） |
| `to-tickets` | 把 plan / spec / 對話拆成 **tracer-bullet tickets**，每張宣告自己的 blocking edges（原 `to-issues`） |
| `implement` | 依 spec / tickets 實作，在**預先約定的 seam** 驅動 `/tdd`，收尾跑 `/code-review` 才 commit |
| `wayfinder` | 規劃**超過單一 agent session 容量**的大工作：在 issue tracker 上鋪一張 decision ticket 地圖，逐一解到路徑清晰 |

### Engineering — Model-invoked（primitive／可被 agent 自動抓）

| Skill | 用途 |
|-------|------|
| `tdd` ⭐ | red-green-refactor 引導，垂直切片實作 |
| `diagnosing-bugs` | 困難 bug / 效能 regression 的 disciplined loop（原 `diagnose`） |
| `code-review` | 對 diff 做**兩軸**審查：Standards（守 repo 規範 + Fowler smell baseline）與 Spec（忠實實作原 issue），**兩個並行 sub-agent 互不污染** |
| `codebase-design` | deep module 設計的共享紀律與詞彙：大量行為藏在小介面後、放在乾淨 seam、可透過介面測 |
| `domain-modeling` | 主動打造／磨利 domain model，拿詞彙挑戰 glossary、用 edge-case 壓測，更新 `CONTEXT.md` + ADR |
| `resolving-merge-conflicts` | 逐 hunk 依 intent（追到雙方一手來源）解 merge/rebase 衝突，**絕不 `--abort`** |
| `research` | 以背景 agent 對高信任一手來源調查，產出**帶引用的 markdown** 存進 repo |
| `prototype` | 寫**丟掉用**的原型：state/logic 問題出單一可分享 HTML；UI 問題出多個可切換變體 |
| `wizard` | 產一支互動式 bash wizard，帶人做**只有人能做**的步驟（開基礎設施、設 CI secret、走陌生第三方 dashboard、一次性 migration） |

### Productivity — User-invoked

| Skill | 用途 |
|-------|------|
| `grill-me` | 對 plan / design 反覆面試直到所有決策樹分支解掉 |
| `handoff` | 把當前 conversation 壓成 handoff doc 讓另一個 agent 接手 |
| `teach` | 跨多個 session 教你一個新技能／概念，**用當前目錄當 stateful 教學 workspace** |
| `to-questionnaire` | 把「你一個人答不了的決策」變成 markdown 問卷，丟給唯一能答的人（async 或會議中一起填） |
| `wait-what` | 訊息沒傳達到時就開火：agent 用你缺的脈絡、以白話 + `CONTEXT.md` 詞彙重新 pitch 一次 |

### Productivity — Model-invoked

| Skill | 用途 |
|-------|------|
| `grilling` | `grill-me` / `grill-with-docs` / `triage` / `wayfinder` / `improve-codebase-architecture` 背後**共用的面試 primitive** |
| `writing-for-agents` | 寫「給 agent 看」的文件的紀律：skills、`AGENTS.md`/`CLAUDE.md`、任何 agent 靠指標會讀到的 doc（原 `write-a-skill` 演化而來） |

### Misc（少用工具，維持不變）

| Skill | 用途 |
|-------|------|
| `git-guardrails-claude-code` | 設 Claude Code hook 擋掉 `git push --force / reset --hard / clean` 等危險指令 |
| `migrate-to-shoehorn` | 把 test 檔的 `as` 型別斷言遷移到 `@total-typescript/shoehorn` |
| `scaffold-exercises` | 建 exercise 目錄結構（sections / problems / solutions / explainers） |
| `setup-pre-commit` | 設 Husky + lint-staged + Prettier + type check + test 的 pre-commit |

### 隱藏 buckets（不對外公開）

CLAUDE.md 規範 `personal/`（Matt 環境綁定）、`in-progress/`（草稿，現有 `loop-me`、`setup-ts-deep-modules`、`writing-*` 等）、`deprecated/`（淘汰）**都不能**進頂層 README 或 `plugin.json`。→ 這個治理規則本身就是值得抄的 skill repo 維護模式。

> **從 5 月移除的 skill**：`caveman`（超壓縮溝通）與 `zoom-out` 已不在本 repo。壓縮／簡潔輸出的紀律部分被 `writing-for-agents` 吸收，caveman 式的規則式壓縮則以獨立工具形式存在於社群（如 [[headroom]] README 就把 Caveman 列為選配搭配）。

## CONTEXT.md 範本（值得抄）

Matt 自己 repo 的 `CONTEXT.md` 就是 grill-with-docs 產生的範例：

```markdown
## Language

**Issue tracker**:
  The tool that hosts a repo's issues — GitHub Issues, Linear,
  a local `.scratch/` markdown convention, or similar.
  Skills like `to-issues`, `to-prd`, `triage`, and `qa` read from and write to it.
  _Avoid_: backlog manager, backlog backend, issue host

**Issue**:
  A single tracked unit of work inside an Issue tracker — a bug, task, PRD, or slice
  produced by `to-issues`.
  _Avoid_: ticket (use only when quoting external systems that call them tickets)

**Triage role**:
  A canonical state-machine label applied to an Issue during triage
  (e.g. `needs-triage`, `ready-for-afk`).

## Relationships
- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time

## Flagged ambiguities
- "backlog" was previously used to mean both the *tool* hosting issues and
  the *body of work* inside it — resolved: the tool is the **Issue tracker**;
  "backlog" is no longer used as a domain term.
```

→ `_Avoid_` 段+`Flagged ambiguities` 段是亮點：**主動列出禁用詞**，比只列「該怎麼說」更能對抗 agent 飄移。

## 目前限制與注意事項

- **強相依 Matt 自家 issue tracker 假設**：很多 skill 預設 GitHub Issues / Linear；自架 issue system 或 Jira 環境需要客製。
- **強相依 TypeScript 生態**：`migrate-to-shoehorn`、`setup-pre-commit`（Husky + lint-staged）、`scaffold-exercises` 對非 JS/TS 專案幫助有限。
- **skill 陣容更新很快，跟緊有成本**：半年內大量改名、新增、移除（caveman/zoom-out 已消失，`diagnose→diagnosing-bugs`、`to-prd→to-spec`、`to-issues→to-tickets`）。走 skills.sh「fork/own」路線的人要自己追上游；不想追的請改用官方 plugin「訂閱」路線。
- **過度依賴 grilling 容易讓速度感降低**：每次都先 grill 對小任務是 overkill，要自己拿捏。
- **205k stars 但仍是個人 repo**：即便已進官方 marketplace，仍是 Matt 個人維護、無公司背書，**未來節奏依賴他個人**——這是任何個人 skill 集合的風險。

## 研究價值與啟示

### 關鍵洞察

1. **「四種失敗模式」是優於「skill 字母清單」的 README 結構**：Matt 沒有用「engineering / productivity」分類組織 README，而是用**問題 → 解法**結構敘述。對使用者來說，遇到問題能直接找到對應 skill，這個寫法值得任何 skill repo 抄。
2. **`grill-with-docs` 是 Skill 設計的範式級作品**：把「grilling（讓 agent 質問你）」、「建立 ubiquitous language（CONTEXT.md）」、「記決策（ADR）」三件事**綁定成一個 skill 自動同步發生**——比起三個獨立 skill，使用者根本不會跳過任何一步。這是「composable skills」哲學的標竿例子。
3. **CONTEXT.md ＞ CLAUDE.md**：傳統做法把所有專案知識塞進 CLAUDE.md，Matt 把它一分為二——**CLAUDE.md 是 meta-rules（repo 維護規矩），CONTEXT.md 是 domain language（給 agent 看的詞庫）**。配合 [[zeuikli-claude-code-best-practices]] 的「CLAUDE.md ≤ 60 行黃金法則」，這個拆分剛好解決「CLAUDE.md 該長還是該短」的兩難。
4. **`_Avoid_` + `Flagged ambiguities` 段的力量**：主動列禁用詞、主動列已解決的歧義，比只列正面範例更能對抗 agent 飄移。可以直接拿來改自己 repo 的 CONTEXT.md。
5. **`/improve-codebase-architecture` 是少見的「agent 反熵」工具**：agent 加速 coding 也加速 entropy，但業界討論最少的就是「怎麼定期反熵」。Matt 建議「每幾天跑一次」這個 skill，把它當作 **agent 時代的 lint**——值得納入任何長期使用 Claude Code 的工作流。
6. **「real engineering vs vibe coding」是個顯性立場**：明確跟 GSD / BMAD / Spec-Kit 等「flow framework」劃清界線，**主張小、可改、可組合**。這條哲學光譜的另一端是 Casper [[casper-claude-skill-design-gallery]]（也是小、可改、可組合），兩者形成相互佐證的社群共識。
7. **`/handoff` + `/wayfinder` 是被低估的「超出單一 context window」工具組**：agent 接力（handoff：把脈絡傳給下一個 session）與**長程規劃**（wayfinder：把大於單一 session 的工作攤成 issue tracker 上的 decision ticket 地圖）目前社群討論很少。Matt 直接把「工作比 context window 大」這個真實限制做成兩個 skill——對長期專案的 session 切換極有實用價值。
8. **★ user-invoked / model-invoked 分軸，是 Skill 系統成熟的訊號**：把 skill 明確分成「orchestrator（只有人能開、負責編排）」與「primitive（人或 agent 都能用、承載可重用紀律）」，並定下「orchestrator 不能呼叫另一個 orchestrator」的規則，等於給 skill 生態一套**組合語法**。`grilling` 被抽成 primitive、被五個 orchestrator 共用，是「小而可組合」從口號變成架構的最佳範例——這條經驗可直接搬進任何自建 skill 庫。
9. **`/code-review` 的「兩個並行 sub-agent 互不污染」是可抄的審查模式**：Standards 軸與 Spec 軸分別交給獨立 sub-agent 並行跑，避免一個視角的結論污染另一個。這跟本站 [[code-review-graph]] 的多視角審查思路一致，是「用 sub-agent 隔離關注點」的具體實作。
10. **「訂閱 vs fork」是 skill 散布的兩種商業／維運模型**：官方 plugin（managed、read-only、自動更新）= 訂閱；skills.sh（複製可編輯檔）= 擁有。Matt 明講「二選一，兩個都裝會重複」。這替 skill 作者示範了**如何同時服務「想跟緊上游」與「想改成自己的」兩種使用者**，且不讓兩者打架。

### 與其他研究的關聯

- 與 [[casper-claude-skill-design-gallery]]：兩者都示範「小、可改、可組合」的 Skill 哲學——Matt 走「engineering workflow」、Casper 走「design output」。對 Skill 系統的兩種典型應用領域。
- 與 [[zeuikli-claude-code-best-practices]]：Matt 的 repo 是**實作層**（具體 skill 程式碼），zeuikli 的報告是**方法論層**（從 81 篇文獻整理而來的原則）。兩篇剛好可以對讀——zeuikli 提出「Skill description 要寫『Do NOT use for ...』」，Matt repo 裡的 SKILL.md 全部都這麼做了。
- 與 [[claude-skills-guide]]、[[andrej-karpathy-skills]]、[[asgard-skills]]：本 repo 是目前最大的個人 Skills 作品集（**205k stars**、已進 Claude Code 官方 marketplace），是這些觀念整理研究的「Skill 實戰範本標竿」。
- 與 [[abdixere-api]]：abdixere-api 主張「Agent context memory 應該下放給 Skill 系統」，Matt 的 `CONTEXT.md + ADR + skills` 三層架構正是這個哲學在工程實踐上的具體答卷。
- 與 [[learn-claude-code]]、[[mcp-for-beginners]]、[[ai-agents-for-beginners]]：對學習者來說，這 repo 是「看別人實際用的 skills」最完整的範本，建議跟 [[zeuikli-claude-code-best-practices]] 一起當進階對齊材料。
- 與 [[harness-design-long-running-apps]]、[[boris-cherny-opus-4-7]]：Matt 跟 Anthropic 官方視角獨立，但結論大量重合（PGE、CONTEXT 分離、小 skill 組合），是 Anthropic 路線之外的**社群獨立驗證**。
