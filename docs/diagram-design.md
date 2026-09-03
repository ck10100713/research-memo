---
date: "2026-09-03"
category: "Coding Agent 工具"
card_icon: "material-sitemap"
oneliner: "BestSelf Co 創辦人 Cathryn Lavery 開發、4.5 個月衝上 ~29.8k 星的跨 agent Claude 圖表 Skill(plugin):不產 Mermaid/Excalidraw,而是把『編輯設計品味』編碼成可執行規則(刪除哲學、4px grid、單一 accent、六條連線鐵律、anti-AI-slop 清單)產出自帶 inline-SVG 的單一 HTML。39 種圖表 × light/dark/full,可從網址套品牌、redraw draw.io/Mermaid、Playwright 匯出 PNG,跨平台幾何/像素級 CI"
tags:
  - claude-code
  - skills
  - design
  - plugin
---

# diagram-design 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/cathrynlavery/diagram-design> |
| 作者 | **Cathryn Lavery** — BestSelf Co 創辦人(bio 逐字:「Founder @bestselfco ($55M+ bootstrapped). Sold to PE in 2022. Bought it back 2024. Becoming AI Native…」);個人站 littlemight.com |
| 實機 gallery | <https://cathrynlavery.github.io/diagram-design/>(GitHub Pages,light/dark/full 分頁) |
| skill 名稱 | `diagram-design`(以 plugin 打包,`plugin.json` 版本 2.6.12 / SKILL frontmatter 2.6) |

> Metadata(**2026-09-03** 即時抓取,均取自 GitHub API / repo 一手來源):**29,795 stars / 1,905 forks** · **MIT**(©2025 Cathryn Lavery) · 建立於 **2026-04-16**,最後 push = 抓取當天 · **~135 commits / 30 contributors**(作者 74)· **無 release / tag**(版本走檔案內號)· repo size 11MB。**4.5 個月衝到近 3 萬星,極活躍**。

!!! warning "四個要先校正的判讀"
    - **類型數是 39 不是 38**:GitHub description 欄仍寫「38 editorial diagram types」,但 README / SKILL.md / 選型表皆為 **39**(description 欄過期)。
    - **主語言 HTML 是誤標**:真正的技能內容是 **Markdown**(SKILL.md + 53 個 `references/*.md`)+ Python 工具鏈;HTML byte 最高只因 `assets/` 有 ~150 個範例 HTML。
    - **watchers 29,795 = stars 的 legacy 鏡像**(真 `subscribers_count` = 92)。
    - **open issues 35 含 PR**(實際 open issue ~16 + PR ~19)。

## 專案概述

**這是一個跨 agent 的 Claude Agent Skill(以 plugin 形式打包)**,把「達到編輯設計水準的圖表」產生為**單一自帶 HTML 檔**(inline SVG + CSS)。關鍵在於:它**不產 Mermaid、不產 Excalidraw、不丟給 draw.io**——而是直接輸出可在瀏覽器打開的自包含 `.html`,圖形本體是**手工排版的 inline `<svg>`**。

README 標題句一句話點題:

> *「Editorial diagrams your designer won't hate.」*(你的設計師不會討厭的編輯級圖表)

**觸發此 skill 的 SKILL.md `description` frontmatter**(逐字節錄開頭):

> *"Create branded architecture, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, swimlane, quadrant, radar/spider... as standalone HTML/SVG/PNG. Redraw .drawio/.drawio.png/.drawio.svg or Mermaid .mmd sources...; onboard brand tokens from a website; add semantic patterns, callouts, accessible motion, or sketchy/hand-drawn styling."*

- **輸入**:自然語言描述、或既有 `.drawio` / Mermaid `.mmd`(redraw)、或一個網站 URL(抽品牌 tokens)
- **輸出**:單一 `.html`(唯一外部依賴 Google Fonts);可再匯出 `.svg` / `.png`(Playwright 光柵化)
- **目標使用者**:寫技術/創業內容的作者、部落客、工程師、顧問——想要「配合自家品牌、達到編輯設計水準」的圖,又不想花 30 分鐘跟 Figma 搏鬥、或收到 Claude 預設的圓角方塊

**它是完整的大型套件,不是單一 SKILL.md**:`SKILL.md`(40KB,非常密)+ `references/`(**53 個 .md**,含 39 個 `type-*.md`,採 **progressive disclosure、選到該類型才載入**)+ `scripts/`(drawio/mermaid extract、self_check、repo 級 ~15 支 CI 驗證)+ `assets/`(~150 個範例 HTML + live gallery)+ 多家 agent 的 plugin manifest(`.claude-plugin` / `.codex-plugin` / `.factory-plugin` / `.agents`)。

## 六個看點

### 1. 把「編輯設計品味」硬編碼成可執行規則(這才是核心賣點)

它賣的不是「又一個 render 引擎」,而是**風格與紀律**。SKILL.md 把設計品味寫成 agent 必須遵守的規則:

- **刪除哲學**:*"The highest-quality move is usually deletion."* 每個 node 都要有存在理由;兩個總是一起出現的 node 併成一個;layout 已能表達的關係就刪掉連線。「圖不是加到滿才完成,而是**沒有東西能再刪**時才完成。」
- **目標密度 4/10**,**超過 9 個 node 大概就是兩張圖**(並對每型細分:sequence ≤5 lifelines、ER ≤8 entities、Gantt ≤12 tasks…超過就拆 overview + detail)。
- **單一 accent(珊瑚橘)是「編輯強調」不是「訊號系統」**:每張圖只有 1–2 個 focal node 用 accent,用在 5 個就失去信號。
- **anti-"AI slop" 清單**:明列「深色底 + 青紫發光、每個 node 一樣大的方塊、圖內浮動 legend、垂直文字、3 張等寬卡片、**重現 Mermaid 的自動排版**」等為反模式。
- **§9 Pre-Output "Taste Gate"**:出圖前跑一份數十項清單(type fit / remove test / signal / typography)。

作者在 README 直言:4px grid 這條規則「**就是讓圖不像 AI 生成的關鍵**」。

### 2. 一套可換膚設計系統:配色 / 字型 / 4px grid / 六條連線鐵律

單一真相源 `references/style-guide.md`,所有顏色/字型用**語意角色**引用(`accent` 而非 `#eb6c36`):

- **預設調色盤**:`paper #f5f5f5`(white-smoke)、`ink #2d3142`(jet-black)、`accent #eb6c36`(atomic-tangerine)、`link #2e5aa8`;每個角色都有 light/dark 對應。
- **字型 3 家(全 Google Fonts)**:`Instrument Serif`(標題 + 斜體 callout)、`Geist`(node 名稱)、`Geist Mono`(port/URL/型別等技術子標籤)——**明令禁止把 JetBrains Mono 當萬用「dev 字型」**。
- **4px grid 不可協商**:字級、座標、寬高、間距全部須被 4 整除,附允許值表。
- **無陰影只用邊框**(陰影列為 anti-pattern);圓角上限 6–10px。
- **六條連線鐵律(non-negotiable)**:圓角直角肘線禁斜線、標籤與線留 6–10px 間隙、連線不得重疊(交叉用 bridge/hop)、多線各自 attach point、線不得穿過非端點方塊、label mask 不壓後畫的節點——可跑 `scripts/verify-geometry.py` **幾何驗證**。
- **無障礙為預設**:每張 `<svg>` 帶 `role="img"` + `aria-labelledby`,`<title>`/`<desc>` 為首子元素。

### 3. 品牌 onboarding:讀你的網址,60 秒讓圖符合自家品牌

新專案第一張圖前有 **style-guide gate**:若仍是預設皮膚就暫停詢問要不要先套品牌。套品牌可**讀網站 URL → 抽 paper/ink/accent/字型 → 映射語意角色 → 出 fidelity receipt(含 WCAG AA 對比檢查)**。多 client 情境可把 onboard 結果存成 named profile(`~/.diagram-design/profiles/<slug>.md`),各專案放 `.diagram-design` marker,跨 workspace 用不同品牌不互相覆蓋。

### 4. Import 是「redraw 不是 convert」(且防 prompt injection)

吃 `.drawio` / Mermaid `.mmd` 當**輸入**,但:

- **只解析文字不算繪**(`drawio_extract.py` / `mermaid_extract.py` 產 nodes/edges 結構摘要),且把來源 label/link/directive **一律視為不可信資料、不當指令**(anti-injection)。
- **Redraw:丟掉來源座標/顏色/字型/形狀怪癖,只留內容**(components、關係、分組、方向)——README 名句:不保留「draw.io 的對角連線義大利麵」與「Mermaid 的自動排版」。
- **四個 dial**:Format(html/svg/png)、Size(doc-inline / slide-16x9 / social-og / print-a4)、Detail(faithful ≤24 / balanced ≤12 / simplified ≤7)、Audience(engineer/mixed/executive,只改用詞不改數量);結尾出 **fidelity ledger**(merged/collapsed/dropped 明細)。

### 5. semantic pattern 與 visual type 解耦(避免型別無限膨脹)

行為/狀態/風險(queue/bottleneck、policy trace、trust boundary、secure paved road…7 個 routed pattern)先用 `semantic-patterns.md` 選主 pattern,再挑最接近的**視覺 type** 做 layout。這樣「行為語意」用既有 type 的排版表達,不必為每種行為都新增一種圖表類型。

### 6. 跨 host 打包 + 幾何/像素級 CI(工程紀律遠超一般 skill)

- **跨 agent 安裝**:Claude Code(`/plugin marketplace add`)、Codex、Factory Droid、Pi、Kiro、OpenCode、Claude Cowork 全支援;同一份技能打包成多家 plugin manifest。
- **工具鏈 Python、產出 HTML+SVG、無 Node、無 build step**;唯一 runtime 外部依賴是 Google Fonts;PNG 匯出與 render lint 用 **Playwright + Chromium**。
- **CI 跨 Linux/Windows/macOS**:`lint-skin`、`lint-render`(headless Chromium 比對「實際畫出的像素」抓裁切)、`verify-geometry/treemap/sankey/polar`、`verify-docs-sync`…多道 gate。
- Icon 55 個(Tabler Icons MIT + Simple Icons CC0,用 `currentColor` 繼承皮膚)。

## 成熟度與活躍度

- **極活躍**:4.5 個月 ~135 commits、最後 push = 抓取當天、plugin 版本已到 2.6.12、30 位 contributor。
- **文件品質高**:README 44KB、CONTRIBUTING 22KB、有 ADR、cookbook、live gallery、Trendshift 徽章;範例充足且可見(`docs/screenshots/` 全解析 PNG + README 內嵌 39 種 WebP 縮圖)。
- **每型 3 變體**:Minimal light(預設)/ Minimal dark / Full editorial;另有 sketchy(SVG turbulence 手繪感)、terminal(CLI 風)、consultant(BCG/McKinsey 2×2)可選 register;動畫四模式(none/reveal/step/loop,`prefers-reduced-motion` 顯示完整靜態幀)。

## 注意事項

- **無 release/tag**(版本走 `plugin.json 2.6.12`),仍在密集迭代。
- **範例 HTML 尚未全面對齊最新皮膚**:`style-guide.md` 自承 `assets/` 內範例是「較早皮膚」所建,全面重生成列為待辦(內部里程碑命名「v5.1」與 plugin 版本 2.6.x 不一致,屬命名殘留)。
- **description 欄類型數(38)落後實際(39)**;**linguist 語言誤標 HTML**(見上)。
- 安裝以各 host 的 plugin marketplace 為主(也可 clone + symlink editable install)。

## 研究價值與啟示

### 關鍵洞察

1. **「把設計品味編碼成可驗證規則」是這份 skill 真正的護城河**:29.8k 星撐起來的不是「多一個 render 引擎」,而是**刪除哲學 + 4px grid + 單一 accent + 六條連線鐵律 + anti-slop 清單 + taste gate**這套可執行、且用幾何/像素 CI 驗證的紀律。這呼應本 session 另兩份筆記的同一心得:[slide-deck-skill](slide-deck-skill.md) 用 Playwright 驗排版溢出、[ai-job-search](ai-job-search.md) 驗 PDF 頁數/ATS——**LLM 產品的品質常不在生成,而在「產完後拿什麼可機器驗證的硬標準去驗它」**。diagram-design 把這個標準推到「像素級幾何驗證」。

2. **刪除哲學 = 對抗「AI slop」的設計立場**:它明確站在「Mermaid slop / 通用圓角方塊 / 深色發光」的對立面,主張「沒有東西能再刪時才完成」。這跟本機的 ponytail「最少可行」精神同源——**好的產出是刪到剩本質,不是加到滿**;差別在 diagram-design 把它落到視覺設計上。

3. **「redraw 不 convert」是 import 的關鍵設計**:多數工具把 draw.io/Mermaid「轉檔」會連同爛排版一起繼承;這裡只抽內容、丟掉座標重畫成自家系統,並把來源當不可信資料防注入。這對「吃外部結構化輸入的 agent 工具」是可借鏡的安全 + 品質雙贏做法。

4. **semantic pattern 與 visual type 解耦,是控制複雜度的巧思**:用既有 type 的 layout 表達行為語意,避免「每種行為都新增一種圖表」的型別爆炸——這是把「維度正交化」用在 skill 設計上的好例子。

5. **作者設計信譽是分發力,但技術才是留存力**:BestSelf Co 創辦人的品牌帶來初始曝光,但真正讓它衝到近 3 萬星並持續高頻迭代的,是「可驗證的品味編碼 + 自包含 HTML 產出 + 跨 host 打包」這組工程實質。

### 與其他研究的關聯

- 與 [Claude Design](claude-design.md)、[Awesome DESIGN.md](awesome-design-md.md)、[UI UX Pro Max Skill](ui-ux-pro-max-skill.md)、[Casper Design Gallery](casper-claude-skill-design-gallery.md):同屬「把設計品味/設計系統餵給 agent」的 skill 家族,但 diagram-design 專攻**圖表**、且把規則做到**幾何/像素 CI 可驗證**,是這條線裡工程化最深的一個。
- 與 [slide-deck-skill](slide-deck-skill.md):本 session 的近親——兩者都**拒絕框架、手刻自包含 HTML + inline SVG、並用 Playwright 做品質驗收**。並排讀可看「self-contained HTML+SVG + 機器驗收」這個模式在簡報 vs 圖表兩個領域的落地。
- 與 [ai-job-search](ai-job-search.md):同屬「用可機器驗證的硬標準做驗收迴圈」的工程思路,是本站三個最好的對照(圖表幾何 / 簡報排版 / 履歷 ATS)。
- 與本機 [artifact-diagramming 技能]:diagram-design 走「手刻 SVG + 編輯設計系統」,與「原生 mermaid 渲染」路線正好互補——前者重品味與品牌,後者重快速與通用。

## 一句話總結

> BestSelf Co 創辦人 Cathryn Lavery 開發、MIT、4.5 個月衝上 ~29.8k 星的**大型跨 agent Claude 圖表 Skill(plugin)**:以「**刪除哲學 + 4px grid + 單一 accent + 六條連線鐵律 + anti-slop 清單**」把編輯設計品味編碼成規則,用 Markdown(1 個 SKILL.md + 53 個 references)驅動 agent 產出**自帶 inline-SVG 的單一 HTML** 圖表(39 種 × light/dark/full),可從網址套品牌、redraw draw.io/Mermaid、Playwright 匯出 PNG,並以跨平台幾何/像素級 CI 驗證品質——刻意站在「Mermaid slop / 通用圓角方塊 AI 圖」的對立面。
