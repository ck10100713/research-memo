---
date: "2026-09-10"
category: "Coding Agent 工具"
card_icon: "material-file-presentation-box"
oneliner: "中國「大师的AI小灶」出品的 Claude / Codex Agent Skill:把一份文件丟給 agent,先整理成 goal.json 計畫,再用內建 React 生成器(非 reveal/Marp/Slidev)輸出 12 套視覺主題、可離線打開的 HTML 簡報。招牌是『產物即編輯器』——每頁自帶控制台(滑桿調模組數/換版式/換配色)+ 文字就地編輯 + 拖曳換圖,改動即時存回 index.html;能一鍵匯出 HTML 離線包、截圖式 PDF、與『逐節點保真、文字仍可編輯(無 OCR)』的真 PPTX。整包 AGPL-3.0、但導出引擎是專有授權;內容零上傳、本機優先;簡體介面 + 中英雙語編輯器,惟未內建 CJK 字型(靠系統字型)"
tags:
  - claude-code
  - skills
  - presentation
  - slides
  - design
---

# dashi-ppt-skill 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/chuspeeism/dashi-ppt-skill> |
| 作者 / 品牌 | **chuspeeism**(GitHub 顯示名 **Dashi AI Lab**),品牌 **大师的AI小灶 / Dashi**;bio 自述是「大师的AI小灶的 GitHub 延伸」,blog 掛小紅書(Xiaohongshu)個人頁——**中國大陸創作者、簡體中文語境**(非台灣繁中) |
| 協作者 | **jadon7**(上傳 README 演示素材的 collaborator,共 2 位 contributor) |
| skill 名稱 | `dashi-ppt`(repo 叫 `dashi-ppt-skill`;plugin 名 `dashi-ppt`,舊名 `dashiai-ppt`) |
| 一鍵安裝 | `npx dashi-ppt-skill@latest`(國內鏡像 `npx --registry=https://registry.npmmirror.com dashi-ppt-skill@latest`) |
| 姊妹作 | [dashi-taskboard](dashi-taskboard.md)(同品牌另一個 skill,另有 agent 在研究) |

> Metadata(**2026-09-10** 即時抓取,取自 GitHub API / `git clone` 原始碼):**7,918 stars / 731 forks / 15 open issues** · **AGPL-3.0**(但導出引擎子包是**專有授權**,見下)· 主語言 **JavaScript**(HTML/CSS 次之,另有少量 PowerShell/Shell)· 建立於 **2026-06-10**,最後 push 2026-09-08 · **25 subscribers** · repo size 約 **104 MB**(內含大量打包字型與主題 runtime)· 版本 `0.4.13` · **無正式 code release**(只有一個 `readme-assets-v1` 圖床 release,放 README 的 GIF/PNG,發布者是 jadon7)。topics:`agent-skill` / `ai-agent` / `ai-ppt` / `claude` / `claude-code` / **`dashial`** / `html-presentation` / `ppt` / `pptx` / `presentation` / `presentation-generator` / `skill` / `slide-generator` / `slides`。

!!! warning "四個要先校正的判讀"
    - **這不是台灣繁中專案,是中國大陸簡體專案**:很容易跟 [slide-deck-skill](slide-deck-skill.md)(台灣林亞澤、全繁中)搞混——兩者都是「HTML 簡報 Agent Skill」,但 dashi-ppt 的 SKILL.md、README、plugin description **全簡體中文**,預設走 npmmirror 鏡像、實測平台含**豆包 / Marvis / Workbuddy / Dumate / Qclaw** 這些中國/國際 agent app,作者掛小紅書。定位、生態、語感都不同。
    - **AGPL-3.0 管的是「軟體」,不是「你做出來的簡報」**:你用它產出的 PPT/PPTX/PDF 是你自己的內容,**商用完全沒問題**。AGPL 的 copyleft 只在你「散布修改版」或「拿(修改版)架成對外網路服務(SaaS)」時才要求你公開對應原始碼。**但**導出引擎子包 `project/packages/html-deck-to-pptx` 是**專有授權(非 AGPL、非 MIT)**,只准當本 skill 的一部分用,不能單獨抽出來塞進別的產品——這是典型的 **open-core**:主體開源、值錢的導出引擎閉源。(該引擎 v0.2.7 以前曾以 MIT 發布,但只對那些歷史版本有效。)
    - **「瀏覽器可編輯」不是自由畫布**:它是「**鎖模板填內容**」+ 每頁一個**控制台**(滑桿調模組數量、下拉換版式/圖表/配色)+ **文字就地編輯** + **拖曳換圖**,不是 Figma 式隨意拖拉縮放。FAQ 明講「自訂樣式僅限特定範圍,是刻意的——穩定產出比自由選色重要」。要逐像素客製視覺,它自己都說「不合適」。
    - **「可編輯 PPTX」是盡力保真、不是 100%**:導出引擎自報基線 `editableFidelity 0.851`;複雜漸層/SVG 區域會截圖回退(但仍從即時 DOM 把文字抽回來保持可編輯,無 OCR)。而 **PDF 是逐頁截圖合成**(非向量文字層)。別預期 PPTX 跟 HTML 一模一樣。

## 專案概述

**dashi-ppt 是一套給 AI agent(Claude Code / Codex 等)用的 Agent Skill**,一句話說就是:**把文件丟給 agent → agent 先把需求整理成一份 `goal.json` 計畫 → 呼叫 skill 內建的本機 React 生成器,渲染出「可離線打開、每頁自帶編輯控制台」的 HTML 簡報 → 需要時再一鍵導出 PDF 或真 PPTX**。SKILL.md 開宗明義:

> *「Dashi PPT 生成静态 HTML 横向翻页 PPT。使用本 skill 时,先把用户的自然语言需求整理成 JSON 计划,再调用本地项目生成器输出 `index.html` 和 `assets/`。」*

它跟站上其他「AI 做簡報」工具最大的差異在於**規模與成品定位**:不是一頁 prompt、也不是「生一份漂亮 HTML 就交件」,而是**內建 12 套完整視覺主題、README 宣稱 1020 個版式頁面 / 8576 個可調控件**的產品級生成器,成品本身就是一台「網頁版 PPT 編輯器」。README 的自我定位是「一個真正適合職場人的 PPT Skill」,主打**行業研究 / 融資復盤 / 競品分析 / 趨勢報告 / 專案匯報 / 路演材料**這類「要結構完整、視覺統一、還能繼續改」的場景。

**它是一整包產品,不是單一 SKILL.md**。骨架大致是:

```text
dashi-ppt-skill/
├── .claude-plugin/marketplace.json   # Claude Code plugin marketplace 清單(v0.4.13)
├── npm-dist/install.mjs              # npx 安裝器:把 skill/ 複製到本機技能目錄
├── README.md / README.en.md         # 簡體中文主 README + 英文版
├── LICENSE                          # AGPL-3.0(整包)
└── skills/dashi-ppt/
    ├── SKILL.md                     # skill 主文件(frontmatter 只有 name/description)
    ├── agents/openai.yaml           # 給 Codex/OpenAI 吃的 skill interface 宣告
    ├── assets/skill/theme-style-grid.png   # 風格選擇提問要嵌的預覽總圖
    ├── scripts/                     # render_goal_deck.sh / .ps1、check_latest_version.mjs
    └── project/                     # ★ 本機生成器(React 元件 + 一堆 workflow 腳本)
        ├── package.json             # react/gsap/pptxgenjs/playwright-core/pdf-lib…
        ├── src/components/themes/theme01…theme12/   # 12 套主題(各自的 React 元件源)
        ├── dist/theme-runtime/                       # 12 套主題編譯後的 runtime
        ├── scripts/                 # layout:query / inspect:layout / goal:scaffold / validate:* / export-pptx…
        ├── packages/html-deck-to-pptx/   # ★ 專有導出引擎(只發 min 打包產物)
        └── assets/vendor/fonts/     # 一堆 Latin 顯示字型的 woff2(無 CJK 字型)
```

## 七個看點

### 1. 觸發與 SKILL.md:frontmatter 極簡,重量全在 body

SKILL.md 的 frontmatter **只有 `name` 和 `description` 兩欄、沒有 `allowed-tools`**(逐字):

```yaml
---
name: dashi-ppt
description: 制作 PPT、演示文稿、幻灯片、汇报材料时使用。Dashi PPT 基于预置视觉主题组合页面,生成可离线打开、可在浏览器编辑的 HTML 演示,支持导出 PPTX / PDF 文件。
---
```

觸發語就是中文的「**制作 PPT / 演示文稿 / 幻灯片 / 汇报材料**」。真正的重量在 SKILL.md 的 body——它是一份**極長、極規範**的作業指令(約 270 行),把「怎麼問使用者風格、怎麼選版式、怎麼寫 goal.json、怎麼渲染、怎麼驗收、怎麼導出」全部寫死成流程。核心是它反覆強調的 **3+1 生成原則**:每個邏輯頁生成 **3 個「鎖模板填文案」的模板方案**(保留原始視覺/結構/配色/圖表類型,只換可見文字)+ **1 個由 agent 在主題視覺語言內定制的 bespoke 方案**(在 12×8 網格上擺 text/metric/list/quote/media/shape/chart 元素,不新增事實、不寫自由 HTML)。它還內建「**成果驗收與返工**」機制:預設最多修正 2 輪,驗收只有「通過/待修正/阻塞」三態,連「輸出裡若殘留 AI Capital / SoundWave / End of Report 這類預設 demo 文案就必須重做」都寫進規則。

### 2. 12 套視覺主題:每套是一組獨立 React 元件,不是換 CSS 變數

主題有 `theme01`～`theme12`,各有中文風格名(SKILL.md 內建對照):

`theme01` 輕擬態風、`theme02` 炫光紫綠風、`theme03` 深淺代碼風、`theme04` 玻璃糖果風、`theme05` 色譜圖表風、`theme06` 深色圖譜風、`theme07` 冷白調研風、`theme08` 黑金實驗風、`theme09` 深藍雜誌風、`theme10` 金色指數風、`theme11` 高能增長風、`theme12` 聲波霓虹風。

關鍵是主題**不是「同一套版型換色票」**,而是 `project/src/components/themes/themeXX/` 底下**各自一組 React/JSX 元件源 + metadata.js**(有些主題還帶自己的 `theme.css`、3D preset、icon set),再編譯成 `dist/theme-runtime/themeXX.module.mjs`。部分主題(如炫光/聲波類)會用 `unicorn-background.jsx` + `assets/vendor/unicornstudio.umd.js` 掛 **WebGL 動態背景**(repo 內有 `automations` / `goey_balls` / `tech_background` 等 remix scene JSON)。內建圖表/分析模型很齊:雷達圖、瀑布圖、矩形樹圖、漏斗、熱力圖、桑基圖、甘特圖,加上 SWOT、波特五力、PEST、商業模式畫布、雙鑽模型等版式。skill 規定 agent 選版式要先跑 `layout:query`(帶 `--theme --role --seed`),同一邏輯頁的 3 個模板方案必須「結構指紋不同」。

### 3. 「產物即編輯器」:編輯器烘進 HTML,改動即時存回 index.html

這是它跟 [slide-editor](slide-editor.md) / [open-slidex](open-slidex.md) 最不一樣的地方——**編輯能力不是靠外部工具,而是直接烘進渲染出來的 `index.html`**(`src/components/themes/client-runtime.jsx` 這條 client runtime)。打開成品網頁就是一台 PPT 編輯器:

- **文字就地編輯**:點任意文字直接改,裝飾元素隨字數自適應。
- **每頁一個控制台**:滑桿增減模組數量(目錄/表格/多項式/圖片數)、下拉換版式、換圖表類型、風格內配色切換、調頁面邏輯重點——README 稱「20 多個維度的編輯空間」。
- **媒體槽**:點擊或拖曳換圖/換影片,上傳自動壓縮。
- **左側縮圖目錄**可拖拽重排、跳過/刪除/複製頁;頂欄可進放映模式、切明暗主題、重置全部改動;翻頁動畫有 9 種可選。

**自動保存機制**:改動不是存瀏覽器 localStorage,而是本機**預覽伺服器**(`serve-preview-https.mjs` / `start-preview-server.mjs`,跑在 `127.0.0.1`、埠段 5200–5999)提供 `POST /api/save-deck-state` 端點,把編輯**即時寫回 `index.html` 本體**。所以 SKILL.md 硬性規定:交付一定要走這個預覽服務(不准用 `python -m http.server` / `npx serve` 代替,因為那些沒有存檔與導出端點);用 `file://` 雙擊打開的檔案**不會自動保存**,交付前得先導出。編輯器介面本身**中英雙語**(`i18n/zh-en.json`),自動跟隨打開者的系統語言、右上角可手動切。

### 4. 三種匯出各自怎麼實作:HTML 離線包 / 截圖 PDF / 保真可編輯 PPTX

| 產物 | 怎麼做 | 底層 |
|------|--------|------|
| **HTML 離線包** | 就是渲染出的 `ppt/` 目錄(`index.html` + `assets/`),雙擊即開、離線可用 | 純靜態,零上傳 |
| **PDF** | `npm run export:pdf`(= `export-pptx.mjs --pdf`)→ `exportScreenshotPdfFromUrl`:用 Playwright **逐頁截圖**,再用 `pdf-lib` 合成 | **截圖式**,非向量文字 |
| **可編輯 PPTX** | 瀏覽器內按「導出」打 `/api/export-editable-pptx`,或 CLI `npm run export:pptx`;都是驅動 `html-deck-to-pptx` 引擎 → `exportEditablePptxFromUrl`:Playwright 走訪 DOM,**逐節點保真回退鏈**——能對應的形狀/文字映射成原生 pptx 物件(`pptxgenjs`),對應不了的區域截圖但**從即時 DOM 把文字重新抽回來保持可編輯(無 OCR)**,再加 alpha-matte 透明背景捕捉 | `pptxgenjs` + `playwright-core`,自報 `editableFidelity 0.851` |

三種都需要 **Node 20+**;PDF/PPTX 額外需要本機有 **Chrome / Chromium / Edge**(可用 `CHROME_PATH` 指定)。CLI 版(`export-pptx.mjs`)聰明的地方:它自己起一個隨機回環埠的預覽伺服器來 serve 靜態檔、導出完再關掉,**繞過**瀏覽器導出流程那套 Origin/Referer 同源檢查——所以「無瀏覽器會話 / 腳本直呼 / 導出端點回 403」時可直接用 CLI 出檔。

### 5. 底層技術:自製 React 元件簡報引擎,跟 reveal.js / Marp / Slidev 沒關係

成品是**靜態 HTML 橫向翻頁簡報**,但底層**不是** reveal.js / Marp / Slidev,而是**作者自製的 React 元件簡報引擎**:`package.json` 相依 `react` / `react-dom` / `gsap`(動畫)/ `html-to-image` / `pptxgenjs`,dev 相依 `tsx` / `esbuild`(把 JSX 主題編譯成 runtime)/ `playwright-core` / `pdf-lib` / `pngjs`。整條 pipeline 是:**goal.json(schema v2,唯一業務事實源在 `slide.content.presentation`)→ scaffold 產結構投影 → React 元件按 `contentMap + projection` 即時生成 props → 渲染成帶 client runtime 的 HTML**。跟 [OpenSlideX](open-slidex.md) 的 MotionDoc MDX 是「兩種結構化真相源」的不同答案:OpenSlideX 用 MDX 標籤,dashi-ppt 用 JSON 計畫 + 鎖版式。

### 6. 安裝與跨 agent:npx 安裝器 + Claude Code marketplace,實測一票 agent

**兩條安裝路**:

- **npx 安裝器**(主推):`npx dashi-ppt-skill@latest` 把包內 `skill/` 複製到本機技能目錄。安裝器會自動探測 `~/.claude/skills`、`~/.codex/skills`、`~/.config/agents/skills`,以及共用的 `~/.agents/skills`;可 `--dir` 指定、`--all` 全裝、`--list` 只列。安裝=更新同一條命令(重跑原地更新、保留已裝依賴)。
- **Claude Code plugin marketplace**:repo 根有 `.claude-plugin/marketplace.json`,可當 plugin 掛。

同時給兩種 agent 生態吃:帶 `agents/openai.yaml`(宣告 display name / icon / default prompt 給 Codex/OpenAI 用),對齊 [mattpocock skills](mattpocock-skills.md) 記過的 `.agents/` 跨 agent 格式。README 的「平台支援」表列出**已實測**:Claude Code、Codex(可調生圖能力補配圖)、豆包(需辦公模式)、Marvis / Workbuddy / Dumate / Qclaw(把 SKILL.md 放任意位置讀取即可)、Cursor / 其他本地 agent(需能讀寫檔 + 跑 shell);**普通網頁 chatbot 不推薦**(生成器需要本機 Node 環境)。每次交付前 SKILL.md 要求跑 `check_latest_version.mjs` 做**靜默版本檢查**(有輸出才提醒更新)。

### 7. 內容零上傳、本機優先,但導出端點有做防濫用

隱私模型清楚:**內容層面零上傳**——文件與簡報內容不送任何伺服器,生成/編輯/導出全在本機、成品離線可開。會聯網的只有兩件:首次生成時 npm 裝依賴、完成後的靜默版本檢查(只拉版本號、不上傳內容)。**安全細節有想過**:本機預覽服務**預設同一區域網內可存取(僅供瀏覽)**,但**導出端點只對本機開放**——`preview-export-auth.mjs` 會檢查 Origin/Referer 是否在允許列表,curl/腳本這種「都沒有」的請求只在伺服器綁回環時放行、綁 LAN 時拒絕(因為導出會啟 headless Chromium 並寫檔,要防跨站/區網濫用)。token 成本:README 實測「一套 10 頁 PPT 約 10 萬 token」。

## 授權與商用可行性

- **整包 AGPL-3.0**:OSI 認證裡 copyleft 效力最強的授權之一。你可以自由使用、修改、散布(**含商用**);但**散布修改版**、或**拿本專案(及其修改版)透過網路對外提供服務(SaaS)**,就必須以 AGPL-3.0 對使用者公開完整對應原始碼。
- **你產出的簡報 = 你的內容,不受 AGPL 拘束**:AGPL 約束的是「軟體本身」,不是「用軟體做出來的 PPT/PPTX/PDF」。拿去客戶提案、商業路演、賣簡報服務都沒問題——這點跟 slide-deck-skill(MIT,更寬鬆)實務上對「產出物」的結論一致,差別在「你改軟體去架服務」時 AGPL 才咬人。
- **導出引擎是專有授權(關鍵例外)**:`project/packages/html-deck-to-pptx` 明文「**licensed, not open-sourced**」,只准當 Dashi PPT skill 的一部分用,**禁止單獨提取/複製/再分發、禁止用於其他軟體、禁止逆向與衍生**。而且安裝版只發**構建產物**(`dist/editable.min.mjs`,源碼 `src/editable.mjs` 只是 re-export 那個 min 檔)。這是刻意的 **open-core**:想把「HTML→可編輯 PPTX」這塊值錢能力抽去自用,得另外跟作者談商業授權。
- 需 AGPL 之外的商業授權,README 要你直接聯絡作者。

## 與其他簡報方案的差異

| 維度 | **dashi-ppt**(本篇) | [slide-deck-skill](slide-deck-skill.md) | [OpenSlideX](open-slidex.md) | [Slide Editor](slide-editor.md) |
|------|------|------|------|------|
| 形態 | Agent Skill(SKILL.md 觸發)+ React 生成器 | Agent Skill + 手刻 HTML 播放器 | MCP tool + MDX 格式 + 專案內 skills | 單檔 Python 瀏覽器內編輯器 |
| 底層 | 自製 React 元件 + GSAP | 純 HTML/CSS/原生 JS(零框架) | React + MotionDoc MDX | 注入 JS 到既有 deck |
| 真相源 | `goal.json`(schema v2)+ 鎖版式 | 手填 `deck.html` 的 class | `presentation.mdx` | 直接改 HTML slide |
| 編輯機制 | 產物即編輯器(控制台滑桿 + 就地改字),存回 index.html | 雙螢幕主控台 + 手機遙控(側重演講) | agent 透過 MCP tool 帶版本鎖改 | hover 就地改 + 元素級 AI 改寫 |
| 匯出 | HTML / **截圖 PDF** / **保真可編輯 PPTX** | 16:9 / A4 **PDF**(Playwright 截圖) | 渲染到 `dist/renders/`(算圖+品質閘) | 存回 HTML(不主打匯出) |
| 主題 | **12 套內建**(各自 React 元件) | 改 `:root` 16 個色彩變數 | 敘事/視覺方向靠 skill 引導 | 對齊好事發生 design system |
| 授權 | **AGPL-3.0**(導出引擎專有) | MIT | MIT | MIT |
| 語言 | **簡體中文**(中英雙語編輯器) | **繁體中文**(台灣) | 英文為主 | 繁中(台灣) |
| 規模/星數 | 大;**7,918★** | 小而精;11★ | 早期;8★ | 早期;5★ |

一句話：**同樣是「AI 做簡報」,dashi-ppt 走的是「產品級、鎖模板、內建 12 主題、能導真 PPTX」的重裝路線**,而 slide-deck-skill 走「輕、零框架、側重演講臨場」、OpenSlideX 走「MDX + MCP 交易式編輯」、slide-editor 走「單檔 Python 補 Claude Design 迭代」。

## 注意事項與已知限制

- **未內建 CJK 字型**:`assets/vendor/fonts/` 打包的全是 **Latin 顯示字型**(Anton / Archivo / Inter / IBM Plex Sans·Mono / JetBrains Mono / Newsreader / Space Grotesk·Mono / Caveat),**沒有任何中日韓字型**。一個簡體中文為主的專案,中文字其實是**靠系統字型**渲染——換機器 / 換 OS 時中文字型 fallback 可能不一致,導出 PPTX/PDF 的中文呈現要留意。
- **可編輯 PPTX 非全保真**:`editableFidelity 0.851`,複雜漸層/SVG 會截圖回退;PDF 是截圖合成、非向量。要「PPTX 跟 HTML 100% 一樣」會失望。
- **依賴本機環境**:Node 20+ + npm 必備;PDF/PPTX 還要 Chrome/Chromium/Edge。純網頁 chatbot 跑不動。首次生成會在 skill 內建 `project/` 裝依賴(需要能對外裝 npm 套件)。
- **自由度是刻意收窄的**:鎖模板填文案、自訂樣式僅限特定範圍(FAQ 明說「穩定產出 > 自由選色」);要逐像素客製,官方自己標「不合適」。
- **導出引擎閉源**:想學/改「HTML→可編輯 PPTX」核心邏輯的人會碰壁——只發 min 打包產物,且授權禁止逆向與衍生。
- **無正式 code release / 版本仍在快速迭代**:只有圖床 release,version `0.4.13`,SKILL.md 反覆提「不用舊 token/舊主題/舊媒體槽」暗示格式契約還在收斂。
- **預覽服務預設 LAN 可瀏覽**:雖然導出端點鎖回環、內容零上傳,但在公司/公共網路要意識到「同網段的人預設看得到你的預覽簡報」。

## 研究價值與啟示

### 關鍵洞察

1. **Agent Skill 的規模上限可以很高——這是「把一整套產品交給 agent 當工具」的極端案例**:12 套 React 主題 + 1020 版式 + 一整條 layout:query→scaffold→validate→render→export 的 workflow + 專有導出引擎,全包進一個 skill。跟 [slide-deck-skill](slide-deck-skill.md) 一樣示範「skill 不必是一頁 prompt」,但 dashi-ppt 把規模推得更大、更接近商業產品。適合當 [Claude Skills 指南](claude-skills-guide.md) 的「重量級 skill」實例。
2. **「鎖模板填文案 + bespoke 定制」的 3+1 是控制 AI 產出品質的好模式**:前三案完全鎖死視覺、只換文字(agent 不會亂改結構),第四案才放手讓 agent 在主題語言內定制——**既要穩定又要有創意的取捨,用「3 穩 + 1 活」切開**。這跟 OpenSlideX 的「收窄標籤契約」、slide-deck-skill 的「規定勿自創樣式」是同一種「用約束換可靠」的工程直覺。
3. **open-core 的清楚示範**:主體 AGPL 開源建立信任與傳播,唯一值錢的「HTML→可編輯 PPTX」引擎閉源收費。對照 [OpenSlideX](open-slidex.md) 用 MIT 全開源、把商業功能留在雲端,dashi-ppt 是「把商業護城河留在**本機的一個閉源子包**」——同樣 open-core、不同切法,並讀能看清兩種商業化邊界。
4. **「產物即編輯器」把交付與迭代合一**:成品 HTML 本身就是編輯器 + 本機服務負責存回檔案,使用者不必回頭找 agent 改小地方——正好補上 [Claude Design](claude-design.md)「生第一版強、迭代貴」的痛點,和 [slide-editor](slide-editor.md) 是「同一個痛點的兩種解法」(一個把編輯器烘進成品,一個外掛編輯器到既有 deck)。
5. **「成果驗收是默認流程」呼應站上反覆出現的主題**:SKILL.md 花大篇幅寫驗收/返工(目標一致性、內容覆蓋、逐頁檢查、敘事完整性、交付完整性,最多返工 2 輪),跟 [ai-job-search](ai-job-search.md)、slide-deck-skill 的「用可機器/可核對的硬標準去驗 LLM 產出」是同一條心得——**LLM 產品的品質常不在生成那一步,而在產完後拿什麼標準去驗它**。

### 與其他研究筆記的關聯

- **[slide-deck-skill](slide-deck-skill.md)**:最容易混淆、也最值得並讀的對照——同是「HTML 簡報 Agent Skill」,一個台灣繁中/MIT/零框架/側重演講,一個中國簡體/AGPL/React/側重產品化導出。
- **[OpenSlideX](open-slidex.md)**、**[Slide Editor](slide-editor.md)**:三種「AI 生 deck + 可迭代」的產品形態;dashi-ppt 是其中最重、最主打「導真 PPTX」的一個。
- **[dashi-taskboard](dashi-taskboard.md)**:同品牌「大师的AI小灶」的姊妹 skill,可對照同一作者的 skill 設計語彙。
- **[mattpocock skills](mattpocock-skills.md)**:`.agents/` + `openai.yaml` 跨 agent(Claude + Codex)skill 格式的先例,dashi-ppt 也採用。
- **[Claude Design](claude-design.md)**:「AI 從零生 deck」的上游生成端;dashi-ppt 把「生成 + 可編輯 + 可導出」收在同一個本機 skill 裡。

## 一句話總結

> 中國「大师的AI小灶」出品、7,918★ 的重量級 Agent Skill:把文件丟給 Claude Code / Codex,先整理成 goal.json,再用內建 React 生成器(非 reveal/Marp/Slidev)輸出 12 套視覺主題、可離線打開的 HTML 簡報;招牌是「產物即編輯器」——每頁自帶控制台(滑桿調模組/換版式/換配色)+ 文字就地編輯 + 拖曳換圖,改動即時存回 index.html,並能一鍵導出 HTML 離線包、截圖式 PDF、與「逐節點保真、文字仍可編輯(無 OCR)」的真 PPTX。整包 AGPL-3.0、導出引擎專有(open-core),內容零上傳、本機優先;惟簡體語境、未內建 CJK 字型(靠系統字型),自由度也刻意收窄。
