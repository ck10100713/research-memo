---
date: "2026-05-15"
category: "Coding Agent 工具"
card_icon: "material-account-tie"
oneliner: "Matt Pocock (Total TypeScript) 把每天用的 Claude Skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnose / improve-codebase-architecture，3 個月 90k stars"
tags:
  - skills
  - claude-code
---

# mattpocock/skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/mattpocock/skills> |
| 作者 | <https://github.com/mattpocock>（Matt Pocock / Total TypeScript） |
| 安裝器 | <https://skills.sh/mattpocock/skills> |
| 作者 newsletter | <https://www.aihero.dev/s/skills-newsletter>（~60,000 訂閱者） |
| 規模 | 90,028 stars / 7,891 forks / MIT / 創建 2026-02-03（May 15 2026 抓取，**3 個月衝到 90k stars**） |
| Repo 結構 | `skills/`、`docs/`、`scripts/`、`.claude-plugin/`、`CLAUDE.md`、`CONTEXT.md` |

## 專案概述

**mattpocock/skills** 是 Matt Pocock（Total TypeScript 創辦人、TypeScript 圈最知名教育者之一）把自己 `.claude/` 目錄裡每天在用的 Claude Skills 公開的 repo。slogan 是 **"Skills for Real Engineers — not vibe coding"**，明確劃清跟「GSD / BMAD / Spec-Kit 那種接管整個流程」的差異——他的 skills **設計為小、可改、可組合**，留控制權給工程師。

Repo 在 2026-02-03 建立、3 個月飆到 90k stars，是目前 Claude Skills 領域社群熱度最高的個人作品集，且**對「Skill 是該被組合的小工具，不是要取代工程師思考的 framework」這個立場做了相當清晰的示範**。

整個系統的安裝體驗也是亮點：

```bash
npx skills@latest add mattpocock/skills    # 用 skills.sh 一鍵安裝
# 之後在 agent 內跑 /setup-matt-pocock-skills
# 它會問你：issue tracker (GitHub/Linear/local files)
#         triage 用的 label 集合
#         docs 存放路徑
```

→ 不是丟一包 markdown 就走人，而是**用 setup skill 把 per-repo config 寫進去**，後續其他 skill 自動讀這份 config 運作。

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
- **`/diagnose`** — disciplined diagnosis loop：reproduce → minimise → hypothesise → instrument → fix → regression-test

### 失敗 #4 — 蓋出一坨泥球

引用 Kent Beck「Invest in the design of the system *every day*」+ John Ousterhout「The best modules are deep」。

**對應 skill**：
- **`/to-prd`** — 寫 PRD 前先質問你要動哪些模組
- **`/zoom-out`** — 強制 agent 把片段 code 放回整個系統脈絡解釋
- **`/improve-codebase-architecture`** ⭐ — Matt 推薦「每幾天跑一次」的 anti-ball-of-mud skill

## Skills 完整清單

repo 用「bucket 分類 + per-folder README」結構（CLAUDE.md 規定每個 skill 必須在頂層 README、`.claude-plugin/plugin.json`、bucket README 三處同步登錄）：

### Engineering（每日 code work）

| Skill | 用途 |
|-------|------|
| `diagnose` | 困難 bug / 效能 regression 的 disciplined loop |
| `grill-with-docs` | Grilling + 寫 `CONTEXT.md` + 寫 ADR 三合一 |
| `triage` | 把 issue 用 state machine 推進不同 triage role |
| `improve-codebase-architecture` | 找 deepening 機會、依 CONTEXT.md + ADR 重整 |
| `setup-matt-pocock-skills` | 安裝其他 skills 前的 per-repo 設定 |
| `tdd` | red-green-refactor 引導，垂直切片實作 |
| `to-issues` | 把 plan / spec / PRD 拆成可獨立 grab 的 GitHub issues |
| `to-prd` | 把當前對話脈絡 synthesize 成 PRD 並送進 issue（不再面試一次） |
| `zoom-out` | 提醒 agent 跳出片段、講整體脈絡 |
| `prototype` | 寫**丟掉用**的原型，分 terminal 邏輯版本 / 多 UI 變體版本 |

### Productivity（非 code workflow）

| Skill | 用途 |
|-------|------|
| `caveman` ⭐ | 超壓縮溝通模式，**砍 ~75% token** 但保留技術精準 |
| `grill-me` | 對 plan / design 反覆面試直到所有決策樹分支解掉 |
| `handoff` | 把當前 conversation 壓成 handoff doc 讓另一個 agent 接手 |
| `write-a-skill` | 用 progressive disclosure 結構幫你寫新 skill |

### Misc（少用工具）

| Skill | 用途 |
|-------|------|
| `git-guardrails-claude-code` | 設 Claude Code hook 擋掉 `git push --force / reset --hard / clean` 等危險指令 |
| `migrate-to-shoehorn` | 把 test 檔的 `as` 型別斷言遷移到 `@total-typescript/shoehorn` |
| `scaffold-exercises` | 建 exercise 目錄結構（sections / problems / solutions / explainers） |
| `setup-pre-commit` | 設 Husky + lint-staged + Prettier + type check + test 的 pre-commit |

### 隱藏 buckets（不對外公開）

CLAUDE.md 規範：
- `personal/`：Matt 自己環境綁定，不對外推
- `in-progress/`：草稿
- `deprecated/`：淘汰
- 這三類**不能**進頂層 README，也不能進 `plugin.json`

→ 這個治理規則本身就是值得抄的 skill repo 維護模式。

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
- **`caveman` 對 CJK 場景未驗證**：對照 [[zeuikli-claude-code-best-practices]] 指出「CJK 不要用 LLMLingua」，caveman 雖然是規則式壓縮（理論上比 token-pruning 安全），但實際 CJK 表現需自測。
- **過度依賴 grilling 容易讓速度感降低**：每次都先 grill 對小任務是 overkill，要自己拿捏。
- **90k stars 但仍是個人 repo**：沒有公司支持，**未來維護節奏依賴 Matt 個人**——這是任何個人 skill 集合的風險。

## 研究價值與啟示

### 關鍵洞察

1. **「四種失敗模式」是優於「skill 字母清單」的 README 結構**：Matt 沒有用「engineering / productivity」分類組織 README，而是用**問題 → 解法**結構敘述。對使用者來說，遇到問題能直接找到對應 skill，這個寫法值得任何 skill repo 抄。
2. **`grill-with-docs` 是 Skill 設計的範式級作品**：把「grilling（讓 agent 質問你）」、「建立 ubiquitous language（CONTEXT.md）」、「記決策（ADR）」三件事**綁定成一個 skill 自動同步發生**——比起三個獨立 skill，使用者根本不會跳過任何一步。這是「composable skills」哲學的標竿例子。
3. **CONTEXT.md ＞ CLAUDE.md**：傳統做法把所有專案知識塞進 CLAUDE.md，Matt 把它一分為二——**CLAUDE.md 是 meta-rules（repo 維護規矩），CONTEXT.md 是 domain language（給 agent 看的詞庫）**。配合 [[zeuikli-claude-code-best-practices]] 的「CLAUDE.md ≤ 60 行黃金法則」，這個拆分剛好解決「CLAUDE.md 該長還是該短」的兩難。
4. **`_Avoid_` + `Flagged ambiguities` 段的力量**：主動列禁用詞、主動列已解決的歧義，比只列正面範例更能對抗 agent 飄移。可以直接拿來改自己 repo 的 CONTEXT.md。
5. **`/improve-codebase-architecture` 是少見的「agent 反熵」工具**：agent 加速 coding 也加速 entropy，但業界討論最少的就是「怎麼定期反熵」。Matt 建議「每幾天跑一次」這個 skill，把它當作 **agent 時代的 lint**——值得納入任何長期使用 Claude Code 的工作流。
6. **「real engineering vs vibe coding」是個顯性立場**：明確跟 GSD / BMAD / Spec-Kit 等「flow framework」劃清界線，**主張小、可改、可組合**。這條哲學光譜的另一端是 Casper [[casper-claude-skill-design-gallery]]（也是小、可改、可組合），兩者形成相互佐證的社群共識。
7. **`/handoff` 是被低估的 multi-session 工具**：agent 接力（從一個 session 把脈絡傳給另一個）目前社群討論很少，Matt 直接做成 skill。對於 [[ralph-loop]] 或長期專案的 session 切換有實用價值。
8. **`caveman` 主張規則式壓縮比 token-pruning 安全**：用「caveman rules」（no preamble、bullets over prose、max 150 words）規則式約束 LLM 輸出，砍 ~75% token 而不改變內容——這個方法跟 [[zeuikli-claude-code-best-practices]] 第 9.3 章的繁中 caveman 實驗（-86.2% token、品質無衰退）完全吻合，互相驗證。

### 與其他研究的關聯

- 與 [[casper-claude-skill-design-gallery]]：兩者都示範「小、可改、可組合」的 Skill 哲學——Matt 走「engineering workflow」、Casper 走「design output」。對 Skill 系統的兩種典型應用領域。
- 與 [[zeuikli-claude-code-best-practices]]：Matt 的 repo 是**實作層**（具體 skill 程式碼），zeuikli 的報告是**方法論層**（從 81 篇文獻整理而來的原則）。兩篇剛好可以對讀——zeuikli 提出「Skill description 要寫『Do NOT use for ...』」，Matt repo 裡的 SKILL.md 全部都這麼做了。
- 與 [[claude-skills-guide]]、[[andrej-karpathy-skills]]、[[asgard-skills]]：本 repo 是 2026-05 截至目前最大的個人 Skills 作品集（90k stars），是這些觀念整理研究的「Skill 實戰範本標竿」。
- 與 [[abdixere-api]]：abdixere-api 主張「Agent context memory 應該下放給 Skill 系統」，Matt 的 `CONTEXT.md + ADR + skills` 三層架構正是這個哲學在工程實踐上的具體答卷。
- 與 [[learn-claude-code]]、[[mcp-for-beginners]]、[[ai-agents-for-beginners]]：對學習者來說，這 repo 是「看別人實際用的 skills」最完整的範本，建議跟 [[zeuikli-claude-code-best-practices]] 一起當進階對齊材料。
- 與 [[harness-design-long-running-apps]]、[[boris-cherny-opus-4-7]]：Matt 跟 Anthropic 官方視角獨立，但結論大量重合（PGE、CONTEXT 分離、小 skill 組合），是 Anthropic 路線之外的**社群獨立驗證**。
