---
date: "2026-09-03"
category: "Coding Agent 工具"
card_icon: "material-projector-screen"
oneliner: "台灣林亞澤打造的 Claude Agent Skill:從零手刻的 16:9 純網頁(HTML/CSS/原生 JS)簡報系統,非 Marp/Slidev/reveal.js。內建雙螢幕講者主控台 + 手機無線遙控(雷射筆/螢光筆,走 Cloudflare Worker 或離線區網)+ PACE 超時變紅計時器 + Playwright 驗收(頁數=備註契約、排版溢出偵測)+ 16:9/A4 PDF 匯出。繁中優先"
tags:
  - claude-code
  - skills
  - taiwan
  - design
---

# slide-deck-skill 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/yazelin/slide-deck-skill> |
| 作者 | **林亞澤(YAZE LIN)** — Taipei, Taiwan;公司 ChingTech 擎添工業;blog <https://yazelin.github.io>(個人非組織帳號,176 public repos) |
| skill 名稱 | `slide-deck`(repo 叫 `slide-deck-skill`,但 SKILL.md `name` 與 symlink 目標都是 `slide-deck`) |

> Metadata(**2026-09-03** 即時抓取,均取自 GitHub API / `git clone` 原始碼):**11 stars / 0 forks / 0 open issues** · **MIT**(有明確 LICENSE,©2026 林亞澤) · 建立於 **2026-08-26**,最後 push 2026-09-02 · 單一分支 `master` · **36 commits / 1 contributor** · **無 release / tag**(`package.json` 標 1.0.0)· repo size 670KB。整個 repo(README、SKILL.md、程式碼註解、UI 文案、commit message)幾乎**全繁體中文**。

!!! warning "兩個要先校正的判讀"
    - **主語言不是「JavaScript 做的工具」那麼單純**:GitHub 標 JavaScript,但 TS 全來自 `worker/src/index.ts`(Cloudflare Worker 中繼),HTML/CSS/原生 JS 才是簡報「產品本體」(模板),而 SKILL.md/README 這類 Markdown 不列入主語言——所以「這是一份 **Agent Skill 文件包**」在語言長條圖上看不出來。
    - **watchers 11 = stars 的 legacy 鏡像**(`subscribers_count` = 0);且 repo 建立僅一週多,11 星是「很新、剛起步」而非冷門。

## 專案概述

**這是一套給 AI agent(Claude Code / Codex / Antigravity)使用的 Claude Agent Skill**,用來「**建立 / 編輯 / 驗收 / 匯出**」專業的 16:9 **純網頁簡報**與配套講義。關鍵在於:輸出**不是** Reveal.js / Marp / Slidev / PPTX,而是**從零手刻、零框架、瀏覽器雙擊即播的 HTML/CSS/原生 JS 簡報**,再透過 Playwright 匯出 16:9 PDF。

SKILL.md 開頭自述:

> *「這是一套經過實戰驗證的 16:9 網頁簡報系統。支援雙螢幕跨視窗同步主控台、PACE 節奏計時、逐頁排版溢出檢查、高解析度截圖轉 PDF、與配套講義生成。」*

**觸發此 skill 的 frontmatter(逐字,只有兩欄、無 `allowed-tools`)**:

```yaml
---
name: slide-deck
description: Use when the user wants to create, edit, verify, or export professional 16:9 HTML presentations, dual-screen synchronized slide decks, speaker notes, or printable companion handouts. Supports Windows, macOS, and Linux.
---
```

**目標使用者**:需要在**線上直播 / 會議室提案 / 錄影課程**做長時間、可重用簡報的講者;以及用 AI coding agent 產簡報的人。README 明講這套骨架是「**為線上直播長期使用累積出來的**」——它的價值不在漂亮樣式,而在「一次次直播現場的疼痛」沉澱成的臨場功能。

**它是完整套件,不是單一 SKILL.md**——約 14 個檔:

```text
slide-deck-skill/
├── SKILL.md              # 90 行;skill 主文件(frontmatter + 規格 + 指令)
├── README.md             # 173 行;人類向說明 + 「一段 prompt 就夠」發包單
├── deck.mjs              # 316 行;跨平台 CLI(init / serve / verify / export / handout)
├── scripts/smoke.mjs     # 172 行;煙霧測試(npm test)
├── templates/            # deck.mjs init 複製進使用者專案的樣板
│   ├── deck.html         # 559 行;簡報主檔(主控台/手機遙控/PACE/雷射筆全部前端邏輯)
│   ├── deck.css          # 357 行;16:9 響應式樣式(:root 16 個色彩變數)
│   ├── deck-tools.mjs    # 279 行;Playwright 驗收 + 縮圖 + 16:9 PDF 匯出
│   ├── handout.html / handout-to-pdf.mjs  # A4 學員講義 + 轉 PDF
│   ├── qrcode.min.js     # 純前端 QR(離線用)
│   └── deck.pdf          # 4 頁預先產好的範例輸出
└── worker/               # Cloudflare Worker 手機遙控中繼(index.ts + wrangler.toml)
```

## 六個看點

### 1. 生成 → 驗收 → 匯出管線(skill 指示 Claude 走的流程)

1. `node <skill 根>/deck.mjs init <專案> --title "主題"` → 建骨架(複製模板、換標題)
2. 使用者照 `deck.css` 既有 class 填內容(**規定勿自創樣式**)
3. `node deck-tools.mjs` 跑全套驗收(見下)
4. `node handout-to-pdf.mjs` 另出 **A4 講義 PDF**
5. `node deck.mjs serve 8080 .` 起 **100% 離線區網伺服器**(斷網現場用)

### 2. Playwright 驗收:抓「機器看不出、台下卻看得到」的溢出(最有記憶點)

`deck-tools.mjs` 用無頭 Chromium(1600×900、deviceScaleFactor 2、locale zh-TW)做的檢查**超越一般 `scrollHeight` 比對**:

- **頁數 = 備註數,硬性契約**:`<section class="slide">` 數必須等於 `#notes > div` 數,否則直接 `exit 1` 中斷。
- **自動翻頁模擬**:逐頁按 `ArrowRight`,驗證 `#counter` 為 `i / n`、`.slide.active` 恰為 1。
- **排版溢出偵測**:不只看頁面溢出,還量「內容離頁首/底部留白(<16px 警告)」與「**pre/table/ul/.points 這種自身 overflow 被捲掉、投影機看不到的部分**」——程式碼註解直言 2026-09-02 因第 15 頁被切掉 236px 才補上這條。
- **無損 16:9 PDF**:用高畫質 JPEG 截圖(quality 88)合成(`@page size:1600px 900px; margin:0`),**刻意避開 CSS `@media print` 跑版**。

把「投影機上內容被切掉」這種只有現場才發現的問題,自動化擋在匯出前——這是本 skill 最工程化、也最實用的一環。

### 3. 雙螢幕講者主控台 + PACE 超時變紅計時器

按 `P`:筆電看講稿備註 + 縮圖清單 + 超時警示,投影機開全螢幕,兩視窗透過 **localStorage 即時雙向同步**(另含「開播前檢查」與「常見問答」區塊)。

**PACE 陣列**在 `<script>` 內定義每頁「累積目標分鐘數」(例:30 頁 90 分鐘 → `[2,5,8,...,90]`);講到某頁若超過目標,主控台計時器**自動由白轉紅**提醒加速。這是把「時間掌控」直接編進骨架的設計。

### 4. 手機無線遙控:線上/離線同一份 UI(雷射筆 + 螢光筆繪圖)

按 P →「手機遙控」→ 手機掃 QR → 手機變遙控器,三分頁:**翻頁(大按鈕 + 觸控震動)**、**雷射光點 / 螢光筆繪圖觸控板**、**完整講稿 + 縮圖跳頁**。座標經 WebSocket 廣播回投影機端 canvas 繪製。

雙模式共用同一份遙控面板 HTML:

- **線上**:Cloudflare **Worker + Durable Object(SQLite-backed)** 做同房 WebSocket 廣播中繼
- **離線**:`deck.mjs serve` 自己當中繼(現場斷網也能用)

### 5. 零依賴播放,Playwright 只做驗收

播放端是純 HTML5 + CSS + 原生 JS,**任何瀏覽器雙擊即播、播放不需 Node/Playwright**;Playwright 僅是唯一的 devDependency,只在驗收與 PDF 匯出時用。內建版型:重點清單 `.points`、雙/三欄 `.cols`、代碼區塊、統計大數字 `.stats`;頁面模式有暗底頁(預設,琥珀金 + 墨黑)、淺色頁 `.light`、宣言頁 `.statement`。換風格只改 `deck.css` 最上面 16 個 `:root` 變數。

**完全自製,沒有用 marp-cli / reveal.js / decktape / pandoc / libreoffice / Slidev。**

### 6. 「一段 prompt 就夠」的發包單:方法論也一起交付

README 附一段發包單,強迫使用者先回答四題(**講給誰聽 / 聽完要做什麼 / 在哪講 / 講多久**),並把取捨與驗收標準寫成 `spec.md` 再開工。這把「怎麼想清楚一場簡報」也納入交付,是純程式模板少見的定位。不想 clone/裝 Node 的人,可直接把這段貼給 agent,要它讀 raw `deck.html`/`deck.css` 照 class 產出。

## 成熟度與活躍度

- **活躍但很新**:36 commits 全集中在 2026-08-26 ~ 09-02(約一週),單人開發。8/26 首日密集初版 → 8/31 起再密集修 bug。
- **commit message 是工程日誌式的坦白**(全繁中),每條記錄真實踩雷,例如「手機遙控永遠卡『連線中』——inline onerror 的單引號在模板字串裡是語法錯」。
- **有煙霧測試**(`scripts/smoke.mjs`,`npm test`):驗腳本語法、`init` 產骨架、驗收跑得起來、離線 serve 的 WebSocket 握手/跨端同步/錯 PIN 被擋。
- **README/SKILL.md 品質高**,指令、目錄、快捷鍵表、手機遙控步驟、換色說明齊備;宣稱與實作大致相符,無明顯灌水。

## 注意事項

- **安裝靠手動 `git clone` + `ln -s` 到 `~/.claude/skills/slide-deck`**——**非 plugin、非 marketplace**(repo 內無 `plugin.json`)。skill 依賴 CLI 實體路徑,Claude 需知道安裝位置才能跑 `init`。
- **線上手機遙控預設打作者託管的 `deck-sync.yazelinj303.workers.dev`**;`wrangler.toml` 內含作者 Cloudflare `account_id`(**公開識別碼、非密鑰**,但已 commit)。要完全自主需自部署該 Worker,或改用離線 serve。`file://` 雙擊 + 手機遙控時,中繼會走作者 Worker(README 稱該 Worker 零資料庫、零隱私,但仍是預設外部依賴)。
- **無 release/tag**(`package.json` 標 1.0.0,但仍在密集修 bug 階段);**README 無截圖/封面圖**,範例輸出僅 `templates/deck.pdf`(4 頁)。
- **無明列 roadmap/TODO**。

## 研究價值與啟示

### 關鍵洞察

1. **「驗收」才是這份 skill 的護城河,不是「生成」**:市面 AI 簡報工具多到「HTML/`.tex` 看起來對」就交件,這裡最花力氣的是**用 Playwright 把『投影機上會被切掉、只有現場才發現』的排版問題自動擋在匯出前**,還把「頁數 = 備註數」設成硬契約。這呼應站上 [ai-job-search](ai-job-search.md) 的同一心得:**LLM 產品的品質常不在生成那一步,而在『產完後拿什麼可機器驗證的硬標準去驗它』**——簡報是頁數/溢出/留白,履歷是 PDF 頁數/ATS 文字層。

2. **把「講者臨場工作流」編進骨架,是它跟一般簡報模板的分野**:雙螢幕同步、PACE 超時變紅、開播前檢查、預錄備援影片、可拖曳縮放的即時內嵌——每一個都是「直播現場疼過一次」的產物。價值不在樣式庫,而在**領域知識(長期直播)被固化進工具**。這類「作者自己的真實工作流 → 開源工具」的路線,與 [Agenvoy](agenvoy.md)「垂直整合自己的需求」同源。

3. **Agent Skill 也可以是「一個完整前端系統 + CLI + 方法論」,而非一頁 prompt**:多數 skill 只是 SKILL.md 指令;這份把 559 行的 HTML 播放器、Playwright 驗收、Cloudflare Worker 中繼、發包單方法論全包進一個 skill。示範了 **Agent Skill 的規模上限可以很高**——它更像「把一套產品交給 agent 當工具用」。

4. **繁中優先 + 台灣作者的原生考量**:文件、UI、程式碼註解、講義襯線字體堆疊(Noto Serif TC / Songti TC / PingFang TC…)全 zh-TW。對中文簡報場景(字體 fallback、襯線講義)有母語級處理,是繁中生態少見的完整簡報 skill。

### 與其他研究的關聯

- 與 [OpenSlideX](open-slidex.md)、[Slide Editor](slide-editor.md):三者都是「本機/網頁優先」的簡報工具,但**介面契約不同**——OpenSlideX 走 MCP、Slide Editor 是編輯器,本篇走 **Agent Skill(SKILL.md 觸發)** + 手刻 HTML 播放器 + Playwright 驗收。並排讀可看「同一個『AI 做簡報』需求的三種產品形態」。
- 與 [FlyAI Skill](flyai-skill.md):另一個台灣作者的 Claude Skill,可對照繁中 skill 生態的做法。
- 與 [Claude Skills 指南](claude-skills-guide.md):本篇是「skill 規模上限」的極端案例,適合當該指南的進階實例。
- 與 [ai-job-search](ai-job-search.md):同屬「把可機器驗證的硬標準(PDF/排版/ATS)做成驗收迴圈」的工程思路,是本站兩個最好的對照。

## 一句話總結

> 台灣林亞澤為「線上直播長期使用」累積出來、從零手刻的 16:9 網頁簡報 Claude Agent Skill——非 Marp/Slidev,而是純 HTML/CSS/原生 JS 播放器 + Node CLI + **Playwright 驗收(頁數=備註契約、抓投影機上被切掉的溢出)** + 16:9/A4 PDF 匯出;招牌是雙螢幕主控台、PACE 超時變紅、跨裝置手機遙控(雷射筆/螢光筆,線上走 Cloudflare Worker、離線走自架區網)。很新(建立一週多、11 星),但工程密度與繁中完整度都高。
