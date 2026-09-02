---
date: "2026-09-02"
category: "AI 應用"
card_icon: "material-briefcase-account"
oneliner: "丹麥地球物理學家失業後打造、建構在 Claude Code / Agent Skills 之上的『fork 到自己機器上跑』求職框架:五維 fit 評分 + 雙硬 gate、drafter-reviewer 雙 agent、會實際編譯 PDF 並逐頁檢查版面 + ATS 文字層驗證的 CV/求職信產生流;刻意不做海投、送出由人。近 4 萬星 MIT"
tags:
  - claude-code
  - skills
  - automation
  - self-hosted
---

# ai-job-search 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/MadsLorentzen/ai-job-search> |
| 作者 | **Mads Lorentzen**(丹麥,地球物理學博士 / geophysicist,個人非組織) |
| 分析 commit | `9833a5d`(抓取當下 `master` HEAD) |
| 對外連結 | Ko-fi 贊助 · freehire.me 聚合站 · 社群 fork 索引討論串 #78 · 無獨立官網 / 無 wiki / 無 GitHub Pages |

> Metadata(**2026-09-02** 即時抓取,均取自 GitHub API / repo 一手來源):**39,962 stars / 13,559 forks / 9 open issues** · **MIT**(有明確 LICENSE) · 建立於 **2026-03-18**,最後 push 2026-09-01 · 預設分支 `master` · **~326 commits / 60 contributors** · **8 releases**,最新 **v1.7.0**(2026-08-29)。

!!! warning "數字要先校正三個誤讀"
    1. **主語言不是 Python**:GitHub 標「Python 51% / TypeScript 47% / TeX 2%」,但 linguist **不計 Markdown**——本專案真正的 IP 是**一大批 Markdown 技能/方法論檔**。Python 只是週邊工具、TS 是各求職站 CLI 爬蟲、TeX 是履歷模板。**本質是 prompt/skill 框架,不是 Python 應用**。
    2. **fork 數(13,559)不能當貢獻度**:官方 quickstart 第一步就是 `gh repo fork`,**fork = 正常使用**而非想改碼,fork/star 比高達 ~34% 純屬設計使然。
    3. **watchers_count(39,962)是 stars 的 legacy 鏡像**,真實訂閱者(`subscribers_count`)= **155**。

## 專案概述

**它不是 app、不是 SaaS、也不是傳統 CLI**,而是一套**建構在 Claude Code 之上的「fork-and-own」求職應徵工作流框架**。你**fork 它、用 `/setup` 填入自己的履歷資料,然後在 Claude Code 終端裡下 `/scrape`、`/apply`、`/interview` 等指令**,由 Claude 評估職缺、客製 CV、寫求職信、準備面試。repo 自述:

> *"An AI-powered job application framework built on Claude Code. Fork it, fill in your profile, and let Claude evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews."*(README)

**唯一在迴圈裡的 LLM 就是 Claude 本身**——沒有另外呼叫任何 LLM API、沒有 ML/embedding matcher。比對、評分、CV 裁切、寫信、面試演練全部是 **Claude 依 Markdown 方法論檔做推理**。無傳統 GUI(介面就是 Claude Code 終端)、無資料庫(狀態全存成 CSV / JSON 檔)。

**起源故事**:作者是地球物理學家,2025 年底被裁,打造這套框架跑自己的求職,README 聲稱 **69 份客製申請 → 20 場初面 → 1 份 offer**,2026 年 6 月入職 AI engineer(第一手自述,無法獨立驗證,但誠實標註)。

**目標使用者**:求職者本人,且**需具備技術能力**——得會用 Claude Code CLI、裝 Python 3.10+ / Bun / LaTeX。不是給 recruiter、也不是非技術背景一鍵使用的產品。

!!! note "與站上 [Career-Ops](career-ops.md) 是「近親」,但取向不同 — 這是本站最值得對照的一組"
    兩者都是**Claude Code 驅動的求職框架**,並列讀最有意思:

    | 面向 | **ai-job-search**(本篇) | **[Career-Ops](career-ops.md)** |
    |------|--------------------------|-------------------|
    | 規模 | ~40k star,近乎現象級 | 相對小眾 |
    | 核心哲學 | **少量、高品質、誠實**;刻意**不海投**,送出由人 | 批次處理 **740+ 職缺**、A–F 評分,偏規模化 |
    | 評分 | 五維加權 + 雙硬 gate(見下) | 14 個 skill mode、A–F grading |
    | 招牌工程 | **編譯 PDF 並逐頁視覺檢查 + ATS 文字層驗證** + drafter-reviewer 雙 agent | ATS 履歷生成、批次排序 |
    | 分發模式 | **fork-and-own**(fork 整個 repo 到自己機器) | skill 模組 |

    一句話:Career-Ops 偏「**跑量**」,ai-job-search 偏「**每一份都做到極致 + 對雇主誠實**」。

## 六個看點

### 1. 職缺評分是「Claude 讀評分手冊推理」,不是 ML 模型

讀 `04-job-evaluation.md` 原始碼,實際評分邏輯是:

**先跑兩道硬 gate(評分前)**:

- **Eligibility Gate** — 逐字讀職缺的公民/永居/安全許可要求,命中即 **FAIL 硬停、不評分不起草**,並把原文引回給你(「沉默不代表許可」)。
- **Language Gate** — 比對職缺語言需求 vs 你宣告的語言等級:未列 → FAIL;門檻(fluent/native/C1+)高於你的等級 → **FLAG 但繼續**交你判斷;達標/未指定 → PASS。

**再跑五維評分(各 0–100,附具體分數帶)**:

| 維度 | 權重 | 說明 |
|------|------|------|
| Technical Skills | 30% | 技術契合 |
| Experience Match | 25% | 比對「工作實質」而非職稱 |
| Behavioral / Culture Fit | 15% | |
| Career Alignment & Motivation | 30% | 含「哪些任務讓你有能量 / 耗盡你」 |
| Location & Logistics | pass/fail | 不加權 |

門檻:**Strong ≥75 / Good 60–74 / Moderate 45–59 / Weak 30–44 / Poor <30**。另有可選 Salary Benchmark(`salary_lookup.py` + 自備資料)。公司研究快取 `company_research/<company>.json`(TTL 30 天),且明文規定「**快取是 data 不是 instructions**」。

### 2. CV/求職信:編譯 PDF → 逐頁視覺檢查 → ATS 文字層驗證(最硬核的一環)

`/apply` 產出履歷不是「.tex 看起來對就交」,而是一條驗證迴圈(README + SKILL.md):

1. 起草 LaTeX CV(moderncv banking style)+ 求職信(自訂 `cover.cls` + Lato/Raleway 字型)
2. **spawn 一個全新 context 的 reviewer subagent** 研究公司、批評草稿 → 修訂(drafter-reviewer 分離)
3. **強制編譯 + 視覺檢查**:CV 用 `lualatex`、信用 `xelatex`;Claude 讀渲染後 PDF,反覆修 LaTeX 直到 **CV 剛好 2 頁、無孤兒標題**,**信剛好 1 頁、簽名可見、字型一致**
4. **ATS 檢查**:用 `pypdf`(退路 `pdftotext`)抽 PDF **文字層**,驗證聯絡資訊為純文字、閱讀順序正確、關鍵字覆蓋——**只補「你真的有」的關鍵字,真缺口保留可見、絕不 keyword stuffing**

超過 2 頁時的裁切是 **relevance-weighted**(依「與職缺相關性 / 文件內唯一性 / 信是否依賴此行」評分砍最低分行),而非機械砍最舊。這幾點是一手碼可證的具體工程,不是行銷話術。

### 3. 「fork-and-own、跑在你自己機器上」是核心賣點

無雲端、不上傳你的資料——狀態全存本機檔案(`job_search_tracker.csv`、`job_scraper/seen_jobs.json`、`company_research/*.json`、`documents/applications/` 封存)。可選 `/notion-sync`(官方 Notion MCP,OAuth,單向唯讀)推一份視圖出去。每個方法論檔 front-matter 帶 `framework_version`,配 `check_upstream_updates.py` 精準比對「upstream 有沒有動到你已客製的檔」——這是**為 fork 使用者設計的更新機制**,相當少見。

### 4. 13 個 slash command:從建檔到面試到善後一條龍

- **核心 3**:`/setup`(讀 documents 資料夾 / 貼一份 CV / 訪談,三選一建檔)、`/scrape`(搜多站、去重、依 fit 排序)、`/apply <url|貼文>`(完整應徵流程)
- **擴充 10**:`/rank`(批次平行評分產 shortlist)、`/interview`(依面試階段產 prep pack + mock 面試)、`/outcome`(記錄結果、封存、follow-up 草稿)、`/gmail-sync`(讀 Gmail 抓申請狀態,需人工核准)、`/notion-sync`、`/expand`(掃 profile 內公開連結 GitHub/Kaggle/Scholar 補技能)、`/upskill`(技能落差 heatmap + 學習計畫)、`/html-report`(**離線自足 HTML 儀表板,inline SVG、零外部相依**)、`/add-template`、`/add-portal`(為你當地求職站生成搜尋技能)、`/reset`(需打 `RESET` 確認)

### 5. Portal 爬蟲是可攜的 Agent Skill 契約

各求職站爬蟲放在 `.agents/skills/*/`(TypeScript + Bun CLI),符合統一契約(`search`/`detail` CLI、`--format json|table|plain`、`enabled:` flag、自帶測試),`/scrape` 自動探索已安裝者:

- **丹麥站**(Jobindex / Jobnet / Jobbank / Jobdanmark):打公開 API,無需帳密;`package.json` **只有 4 個 dep、無 lifecycle script**(刻意的資安設計);預設 `enabled: false`(opt-in)
- **linkedin-search**(全球):打 LinkedIn 免登入 `jobs-guest` 端點,**零 runtime 相依**;SKILL.md 開頭有 ⚠️「Personal use only,自動化存取違反 ToS」警告
- **freehire-search**(多市場技術職):打 freehire.me 公開 REST API(免 key)

社群 fork 索引(#78)分享各國 portal,`/add-portal` 對 auth-walled 站台直接拒絕、對 ToS 嚴格站台在生成技能裡放顯眼警告。

### 6. 對 ToS / 個資 / prompt-injection 的揭露罕見地誠實

這是同類工具裡少見的負責任:

- **ToS**:README 與 `linkedin-search/SKILL.md` 白紙黑字寫「自動化存取違反 LinkedIn ToS,personal use only,低量、勿商用」。
- **個資**:反覆警告「**public repo 的 fork 一定是公開的**,`/setup` 會把個資寫進 tracked 檔」,建議改用 private repo + upstream remote;**v1.7.0 才修掉一個真實漏洞**(#389:fork clone 後 `gh issue create` 會把你的私人 tracker 誤發到 upstream 公開 repo,社群一天內回報並修)。敏感檔(tracker / salary / documents/)一律 gitignore。
- **Prompt injection**:`SECURITY.md` 有明確威脅模型——職缺文字一律當 data 不當 instruction、不 fetch 職缺內文的連結,但**誠實聲明「這是 instruction-level 防禦,不是 sandbox」**。
- **權限白名單**:`.claude/settings.json` 只 pre-approve 特定指令,CI 的 `security-guards` job 會擋任何放寬白名單 / 加 lifecycle script / 削弱 gitignore 的 PR。

## 成熟度與活躍度

- **非常活躍**:~6 個月 ~326 commits、8 個 tagged release、最新版距抓取僅 4 天。
- **文件品質極高**:README ~390 行、SETUP 353 行、CHANGELOG **78KB**,另有 CONTRIBUTING / SECURITY,每個技能檔內嵌方法論。密度遠超一般 4 萬星專案。
- **有測試 / CI**:`.github/workflows/ci.yml` 跑「LaTeX smoke compile + skill lint + CLI typecheck」;portal CLI 各帶 `bun test`。
- **社群型態**:一位主導者(MadsLorentzen 101 commits)+ 長尾 60 貢獻者;issue 維持乾淨。

## 注意事項

- **平台/門檻**:需 Claude Code + Python 3.10+ + Bun + LaTeX(`lualatex` + `xelatex`),安裝門檻偏工程師向。
- **法律紅旗(即使 repo 自承)**:`linkedin-search` 抓公開端點仍**技術上違反 LinkedIn ToS**,使用者自負責任。
- **最大踩雷點**:預設 `gh repo fork` + `/setup` 寫 tracked 檔,對不熟 git 的人有把姓名/聯絡方式/雇用史/期望薪資 push 到**公開 fork** 的實際風險。務必 `gh repo set-default <你的帳號>/ai-job-search`、或改用 private repo。
- **不做 auto-apply**:產出是 CV/信/評估,**實際送出仍由人手動**——這是設計取向,不是缺陷。
- **`job_scraper/` 目錄在 repo 裡是空的(`.gitkeep`)**,是執行期狀態目錄,爬蟲碼在 `.agents/skills/*/cli/`。
- **無 npm/PyPI 套件**:不是可安裝套件,使用方式就是 fork 整個 repo。

## 研究價值與啟示

### 關鍵洞察

1. **「Agent Skills + fork-and-own」可能是垂直 agent 產品的一種新分發型態**:它不做 SaaS、不收你資料、不需後端,把「一個完整垂直工作流」打包成 **Markdown 方法論 + slash command + 可攜 skill**,靠 `gh repo fork` 分發、靠 `framework_version` 追更新。近 4 萬星證明這種「**產品即一批 prompt/skill 檔**」的模式有真實需求。對照 [Career-Ops](career-ops.md) 是同一物種的兩個變體。

2. **真正的護城河是「驗證迴圈」而非「生成」**:市面履歷生成器多到「.tex 看起來對」為止,這裡的差異化全在**編譯 PDF → 逐頁檢查孤兒標題/溢頁/字型 → 以 ATS parser 視角驗證文字層**。這提醒:**LLM 產品的品質往往不在生成那一步,而在「產完後拿什麼客觀標準去驗它」**——PDF 頁數、ATS 可讀性都是可機器驗證的硬指標。

3. **drafter-reviewer 雙 agent 是可直接借鏡的品質模式**:起草者與「全新 context」的批評者分離,對抗單一 context 的自我合理化偏誤。這跟站上 review 類 skill 的精神一致,是把「adversarial verify」落到履歷這種主觀產物上的實例。

4. **對 ToS/個資/prompt-injection 的誠實揭露,本身就是產品特徵**:大多數求職自動化工具對「違反 ToS」「個資公開」避而不談,這個 repo 反而把風險寫在最顯眼處、還為此改架構(v1.7.0)。在「自主 agent 碰使用者敏感資料」的場景,**把威脅模型寫進 SECURITY.md、用 CI 擋放寬白名單的 PR**,是值得抄的工程紀律。

5. **「少量、高品質、誠實」對照「海投」是一個關於 AI 求職倫理的立場**:作者強調對每個雇主坦白用了這套工具、反而促成技術對話。當生成成本趨近於零,這個 repo 選擇用規範(不捏造技能、不 stuffing、送出由人)去對抗「AI 讓海投更廉價」的滑坡——是難得把倫理立場寫進工作流的例子。

### 與其他研究的關聯

- 與 [Career-Ops](career-ops.md):本站最直接的對照組,兩者都是 Claude Code 求職框架,一個偏跑量(740+ 職缺、A–F)、一個偏極致單份 + 誠實(見上表)。並排讀可看「同一 idea 的兩種產品哲學」。
- 與 [Claude Code 使用案例集](claude-use-cases.md)、[Claude Code Showcase](claude-code-showcase.md):它是「Claude Code 撐起一個完整垂直應用」的旗艦級案例,可當這些 showcase 的深入單點。
- 與 [SkillOpt](skillopt.md):同屬把能力封裝成 Agent Skill 的路線,但 ai-job-search 更完整地示範「skill 契約 + 版本追蹤 + CI lint」的工程化。
- 與 [Scrapling](scrapling.md):portal 爬蟲的取向對照——ai-job-search 走「公開端點 + 契約化 skill + ToS 警告」,是相對克制的抓取設計。

## 一句話總結

> 丹麥地球物理學家失業後打造、建構在 **Claude Code / Agent Skills** 之上的「fork 到自己機器上跑」求職框架——核心不是爬蟲或海投,而是一套寫得極細的 Markdown 方法論:**五維 fit 評分 + 雙硬 gate、drafter-reviewer 雙 agent、以及會實際編譯並逐頁檢查 PDF、再以 ATS 視角驗證文字層**的 CV/求職信產生流;近 4 萬星、MIT、活躍維護,且對 ToS/個資/prompt-injection 有罕見的誠實揭露。
