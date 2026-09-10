---
date: "2026-09-10"
category: "Coding Agent 工具"
card_icon: "material-view-column"
oneliner: "chuspeeism 出的『Codex Taskboard』:一個 local-first 的議題看板(七狀態 kanban + 三欄消費者視圖),同一套本機 HTTP API 同時餵 React UI 跟 taskctl CLI。招牌是『嵌進 coding agent 桌面 app 裡面』——用 CDP 注入把看板塞進 Codex(ChatGPT.app)側邊欄當 OOPIF,或用一個真正的 Cordis 插件(pnpm dsh plugin)塞進 DeepSeek Harness。附 bundled Codex Skill(manage-taskboard)讓 agent 自己搬卡、驗收、等你點頭才 done。Tauri 打包 macOS/Windows/Linux 桌面 app,自帶 Node runtime;Apache-2.0。注意:repo 叫 dashi-taskboard 但產品叫 Codex Taskboard,dsh 是 DeepSeek Harness 的 CLI 不是 Dashi 品牌"
tags:
  - claude-code
  - codex
  - taskboard
  - dashboard
  - agent
  - tauri
  - deepseek
---

# dashi-taskboard 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/chuspeeism/dashi-taskboard> |
| 作者 | **chuspeeism**(個人帳號,GitHub user id 70992554) |
| 產品實際名稱 | **Codex Taskboard**(`package.json` name = `codex-taskboard`、Tauri `productName` = `Codex Taskboard`、bundle identifier `com.chuspeeism.codex-taskboard`)。「dashi」只出現在 **repo slug** 和測試 fixture 的 checkout 路徑,不是產品品牌 |
| 最新 release | `v1.1.23-beta.2`(name = *Codex Taskboard v1.1.23-beta.2*,**prerelease**),macOS universal DMG `Codex.Taskboard_1.1.23_macOS-universal.dmg`(≈88 MB) |
| 姊妹作 | [dashi-ppt-skill](dashi-ppt-skill.md)(同作者的 `dashi-*` repo 家族) |

> Metadata(**2026-09-10** 即時抓取,取自 GitHub API + `git clone --depth 1` 原始碼):**3,020 stars / 433 forks / 33 open issues** · **Apache-2.0**(完整授權全文 LICENSE)· 建立於 **2026-07-24**,最後 push 2026-09-08 · 主分支 `main` · repo size ≈6.9 MB · **has_discussions / has_wiki 皆開**、subscribers 僅 14。語言組成:**JavaScript 1.33 M · TypeScript 875 K · CSS 227 K · Rust 102 K · HTML 544 bytes**——JS/TS/CSS 是 React 前端 + Node 後端,Rust 是 Tauri 桌面殼。**建立才約 1.5 個月就衝到 3,020 星**,成長極快,但版本仍是 `-beta`。topics:`claude-code / cli / codex / codex-app / codex-desktop / codex-plugin / dsh / dsh-plugin / skills`。

!!! warning "四個要先校正的判讀"
    - **它不叫「Dashi」,`dsh` 也不是它的品牌 CLI。** repo slug 是 `dashi-taskboard`,但打開原始碼,產品從頭到尾叫 **Codex Taskboard**。而 `dsh` 是 **DeepSeek Harness 的 CLI 指令**(`pnpm dsh plugin ...`),topic 的 `dsh-plugin` 指的是「一個 DeepSeek Harness 插件」,不是 Dashi 生態。把 `dsh` 當成 Dashi 品牌會整個誤讀。
    - **「任務面板」是給人看、也給 agent 用的雙面板——不是純監看儀表板。** 人這邊看到的是可拖曳的 kanban(七狀態、消費者三欄視圖);agent 那邊是透過 `taskctl` CLI + `manage-taskboard` Skill 讀寫同一份議題。它更像「給你的 coding agent 用的 Jira/Linear」,而不是 agent 進度監看牆。
    - **「可靈活嵌入」不是網頁 iframe widget。** 它是**專門嵌進兩個 coding agent 的桌面/網頁宿主**:用 CDP(Chrome DevTools Protocol)注入把自己塞進 Codex 桌面 app(ChatGPT.app)的側邊欄,或用 Cordis 插件塞進 DeepSeek Harness。「靈活」指的是**多重 fallback 宿主策略**(見下),不是能貼到任意網站。
    - **topics 掛了 `claude-code / skills`,但原始碼裡沒有 Claude Code 整合。** 實際整合對象是 **Codex(OpenAI)+ DeepSeek Harness**;Skill 目錄是 `~/.agents/skills/manage-taskboard`、agent 設定檔是 `agents/openai.yaml`。`claude-code` topic 比較像 SEO;唯一跟 Claude 生態相通的是「Agent Skill(SKILL.md)」這個檔案格式概念。

## 專案概述

**Codex Taskboard 是一個 local-first(本機優先)的議題看板 / 任務面板**:一個跑在你機器上的 Node HTTP 服務(預設 port `47823`)+ SQLite(`.data/taskboard.sqlite`)+ React 19 前端。它被打包成 **Tauri 桌面 app**(macOS DMG/app、Windows NSIS、Linux deb/AppImage),桌面版**自帶 Node runtime、服務、Web UI、Skill、CLI、注入腳本**,目標機器只要裝了官方 Codex app 就能跑,不需要這個 repo、不需要系統 Node。

README 開宗明義:

> *「A local-first issue board that runs in a browser and can be embedded in Codex through the standalone CDP launcher or its injection script. The same HTTP API powers the React UI and the `taskctl` CLI used by the bundled Codex Skill.」*

這句話點出它的核心設計:**同一套本機 HTTP API,同時服務「人看的 React 看板」和「agent 用的 `taskctl` CLI」**。人把要做的事開成 issue,coding agent(Codex / DeepSeek)透過 CLI + 一個 bundled Skill 把 issue 從 `todo` 搬到 `in_progress`、驗收、留言、綁 Git 分支/worktree,**只有在你明確說「接受」之後才會搬到 `done`**。它把「人 ↔ coding agent 的工作交接」做成一塊共享白板。

領域模型是**七狀態**(`shared/domain.mjs`):`backlog / todo / in_progress / in_review / blocked / done / canceled`。消費者視圖(`docs/consumer-task-board-chatgpt-pro-review.md`)則固定顯示三欄——**待處理(todo)/ 處理中(in_progress)/ 等你確認(in_review)**,其餘狀態收進右側「其他任務」面板。

主要目錄:

```text
dashi-taskboard/
├── server/          # Node HTTP 服務(app.mjs / database.mjs / SSE 廣播 + AI chat + Jira 整合)
├── web/             # React 19 + Vite + TS 前端(93 檔;ProseMirror 編輯器、mermaid、gantt)
├── cli/taskctl.mjs  # 給 agent 用的 CLI(讀寫 issue/project/comment,吐 JSON)
├── shared/          # 前後端共用領域模型(domain.mjs 定義七狀態)
├── skills/manage-taskboard/     # bundled Codex Skill(SKILL.md + references/cli.md + agents/openai.yaml)
├── inject/codex-taskboard.user.js   # 1,968 行 document-start 注入腳本(塞進 Codex 桌面 app)
├── scripts/codex-injector.mjs       # CDP 啟動器 / 注入器
├── integrations/deepseek-harness/   # DeepSeek Harness 的 dsh 插件(Cordis)
├── src-tauri/       # Tauri 2 桌面殼(Rust)
├── cloud/ + wrangler.jsonc          # Cloudflare Worker + D1 + R2 雲端共享
└── AGENTS.md / README(.zh-CN).md / PRIVACY.md
```

## 6 個看點

### 1. Taskboard 到底是什麼:人 + agent 共用的一塊議題白板

不是 agent 進度監看牆,是**雙向工作交接板**:

- **人這邊**:React 看板,拖卡換狀態、開 issue、留言、看 Gantt。issue 描述與留言支援 GFM(表格、任務清單)、`mermaid` 圍欄圖(載入後渲染成唯讀圖)、`<!-- ... -->` HTML 註解隱藏。用 DOMPurify 消毒、不開 raw HTML。
- **agent 這邊**:`taskctl` CLI(吐 JSON)+ `manage-taskboard` Skill。**同一套 HTTP API 兩邊共用**,不是各接各的。
- **即時同步**:任務/留言/附件變更透過 **SSE(server-sent events)** 廣播給每個開著的 client;斷線重連會做一次完整刷新,不漏更新。
- **樂觀並發控制**:每個 issue 有 `version`,`taskctl` 用 `--if-version` 寫入,衝突就重讀 reconcile——這是為了「多個 agent + 人同時動同一塊板」設計的。
- **同網段多人**:`npm start` 會印出區網 URL,同一受信任網路的人開 LAN URL 就共用同一塊板。**但 LAN 模式完全沒有帳號驗證**(見注意事項)。

### 2. 嵌入機制:CDP 注入進 Codex 桌面 app,不是網頁 iframe

這是整個專案最有記憶點的工程。Codex 桌面 app(其實就是 **ChatGPT.app**,一個 Electron app)本身沒有插件 API 讓你塞面板,作者的解法是:

1. 用 `--remote-debugging-port` 把 Codex 開起來(或找到已開、有可用 CDP renderer 的 Codex)。
2. 透過 **CDP** 安裝一支 **document-start 注入腳本**(`inject/codex-taskboard.user.js`,1,968 行),在 Codex 側邊欄「Plugins」後面加一個原生外觀的 **Taskboard 入口**,把看板以 **OOPIF(out-of-process iframe)** 鋪滿整個主工作區(連上下文標題列區域都吃掉,才不會留空白條)。
3. Codex `26.715.52143` 的 renderer CSP 會擋任意 HTTP iframe,所以啟動器**啟用 CDP CSP bypass**、reload 一次 renderer、等 OOPIF 真的載入。
4. 「在對話中打開」會選對應的原生 Codex 專案,開一個未送出的 composer,預填 `e-taskboard` 指令 + issue 真實 ID——**Skill 由該指令隱式選中**,不用 `$manage-taskboard` mention。

README 特別強調它的**克制**:**不改 `ChatGPT.app` 或 `app.asar`、不 patch React、不換 `fetch`、不載私有 chunk、不動 Codex 資料檔**,只用 Codex 現有的專案/composer/route 標記。

「靈活」的真義是**一條命令多重 fallback**(`npm run codex`):有可用 CDP 的 Codex → 複用它注入;普通 Codex 沒 CDP → 開在它的原生瀏覽面板;完全沒開 Codex → 用獨立 profile + loopback-only port 開官方 Codex;要不然就純瀏覽器 / LAN 開。它會一直 watch 服務跟 renderer,replace 掉就重注入。

### 3. Codex 整合:注入 + bundled Skill + taskctl + thread 綁定

整合是**三件套**,不只是注入:

- **注入**(看點 2):把 UI 塞進 Codex。
- **bundled Skill `manage-taskboard`**:一份 SKILL.md,教 Codex 的標準流程——先 `issue get` + `comment list` 讀清楚 → `backlog` 視為「未核准不准動」→ 認領時把 `todo` 搬 `in_progress`(帶 `version`)→ 只做該 issue 綁定的 branch/worktree 內的事 → 驗證 → 留言寫變更+驗收結果+風險 → 搬 `in_review` → **只有使用者明確接受才搬 `done`**。Skill 裡有大量防呆:不准搶別的對話認領的 issue、不准 loop、身分欄位不齊就停手。
- **thread 綁定**:`taskctl` 讀 Codex 的 `CODEX_THREAD_ID`,把對話 ID 記到 issue/comment 上,之後可從 Codex 原生 route 點回去。每個 issue 可綁**一個 Git 分支或一個 worktree**,選項是從所選 Codex 專案的 repo **掃描**出來的,不是手打。

桌面 app 會讓 `~/.agents/skills/manage-taskboard` 跟內建 Skill 保持同步;啟動器把帶身分的服務地址寫進 `launcher-runtime.json`,`taskctl` 預設讀它,所以一般 shell 跟從面板開的 Codex 任務用的是同一個服務,不用手動設環境變數。

### 4. DeepSeek Harness 整合與 `dsh-plugin` 結構:一個真正的 Cordis 插件

跟 Codex 的「注入 hack」不同,**DeepSeek Harness 這邊是走正規插件 API**。`integrations/deepseek-harness/` 就是一個可安裝的 **dsh(DeepSeek Harness CLI)插件**,npm name 叫 `dsh-codex-taskboard`,底層是 **Cordis 插件框架**(`ctx.effect` / `ctx.slots` / `ctx.webServer`、`window.__ModuleLoader__.load`、`cordis.patch.yml`)。安裝:

```sh
pnpm dsh plugin --profile web add /absolute/path/to/codex-taskboard/integrations/deepseek-harness
```

結構分兩半:

- **`index.js`(server 端)**:註冊一個 `/integrations/codex-taskboard` 路由,handler 讀 launcher runtime 檔拿到當前 Codex Taskboard 的 URL,回 `307` redirect 過去(服務沒開就回 `503`)。**因為讀 runtime 檔,所以不綁死 port。**
- **`client.js`(web UI 端)**:一個 React 元件,`inject` 到 DeepSeek 的 `sidebar.footer.action` slot,加一個「任务面板」按鈕,點開一個 `position:fixed` 的 aside,裡面 iframe 那個 redirect 路由。整個 UI 貼齊 DeepSeek 的設計 token(`--dsw-alias-*`),看起來像原生功能。

換句話說:**同一塊本地看板,對 Codex 用 CDP 注入、對 DeepSeek 用官方插件機制**,兩邊都指向 launcher runtime 檔裡那個唯一的本地服務。

### 5. 前端 / 後端 / 打包技術棧

滿完整的一套現代 stack:

- **前端**:**React 19 + Vite 8 + TypeScript 7**(`web/`,93 檔,含 i18n 中英)。富文本編輯器用 **ProseMirror**(prosemirror-markdown/model/state/view + example-setup),渲染走 markdown-it / react-markdown / remark-gfm / remark-breaks,圖表用 **mermaid**,消毒用 **DOMPurify**,還內建 **dhtmlx-gantt**(甘特圖視圖)。
- **後端**:Node(`server/index.mjs` / `app.mjs`)、**SQLite** 落地、**SSE** 即時廣播、`ws`(WebSocket)。另有 **built-in AI chat**(`server/ai-chat*.mjs`,會實際 spawn Codex 進程、載 slash commands / catalog)跟 **Jira 整合**(`server/jira-integration.mjs`,把 issue 對到 Jira 欄位)——這兩塊是看板之外的附加能力。
- **桌面殼**:**Tauri 2**(Rust,`src-tauri/`),把 Node runtime + 服務 + Web UI + Skill + CLI + 注入腳本全包進一個 app。
- **雲端**:**Cloudflare Worker + D1(權威業務 DB)+ R2(附件)**,`wrangler.jsonc` 部署,HTTPS Basic Auth。

### 6. 安裝與部署:桌面 app 一包到底,或原始碼三步走

四條路:

1. **下載桌面 app(最省事)**:從 GitHub Releases 抓 DMG(macOS universal)/ NSIS(Windows)/ deb·AppImage(Linux Ubuntu 24.04 x64)。目標機器只要有官方 Codex app,不用 repo、不用系統 Node、不用另裝 Codex CLI。資料存 `~/Library/Application Support/Codex Taskboard`。
2. **原始碼跑本機**:`npm install && npm run build && npm start` → 開 `http://127.0.0.1:47823`;開發模式 `npm run dev`(Vite 5173 proxy 到本地服務)。
3. **裝 Skill**:把 `skills/manage-taskboard` symlink 到 `~/.agents/skills/manage-taskboard`。
4. **Cloudflare 雲端共享(限「兩位受信任協作者」)**:Worker Static Assets + D1 + R2 + Basic Auth。每台設備仍各自跑**本地 companion**(device-local loopback 服務,負責 Codex/Git/worktree/Skill/MCP 能力與路徑映射),雲端模式**不會回退或雙寫本地 SQLite**。作者在 SKILL.md 甚至明文要求:`companion` **不准譯成「伴侶」**、普通 Taskboard HTTP API 不准叫「伴侶 API」。

驗證:`npm run check`(typecheck + 前端 build + 元件測試 + server/CLI/注入測試套件);test 目錄有 32 個測試檔,涵蓋注入、CLI、雲端遷移、skill 契約等。

## 授權與商用可行性

- **Apache-2.0**(repo 有完整授權全文,11 KB LICENSE)。相對寬鬆:可商用、可閉源二次開發、可修改再散布,附帶**專利授權條款**與商標保留,只要保留授權與 NOTICE。以「自己的程式碼」而言商用無虞。
- **但真正的可行性瓶頸不在授權,而在它嵌入的宿主**:它是靠 **CDP 注入到 OpenAI 的 Codex(ChatGPT.app)** 這種未公開介面工作的。Apache 只管 Taskboard 自己的碼,**管不到 ChatGPT.app 的使用條款**;拿去做商業產品前,得自己確認「用 CDP 注入官方桌面 app」在對方 ToS 下的風險。DeepSeek Harness 那條路是正規插件,風險低很多。
- **仍是 `-beta`**:版本 `v1.1.23-beta.2`、prerelease,Windows CI 產物「刻意未簽名、不自動更新」,公開 macOS 下載還需要 Developer ID 簽名 + Apple notarization。要當生產工具得自己補這些。

## 與其他方案的差異

- **它不是「agent 監看儀表板」(對比 [dispatch](dispatch.md) / [mission-control-center](mission-control-center.md))**:那類東西是「人在旁邊盯多個 agent 的進度/輸出」;Codex Taskboard 是**工作項(issue)本身的生命週期管理**,agent 是「執行者」而非「被監看對象」,而且**收斂在 issue 狀態機 + 人工驗收 gate** 上。
- **它把「議題板」直接嵌進 agent 宿主**,而不是要你切出去開另一個網站/app。這點跟一般 Kanban SaaS(Jira/Linear/Trello)最大的差別——**面板長在 coding agent 的側邊欄裡**,agent 能用 CLI 直接動它。
- **人工驗收 gate 是設計核心**:Skill 明訂「只有使用者明確接受才 `done`」,這跟 [humanlayer-skills](humanlayer-skills.md) 那種「human-in-the-loop 審批」是同一個思路——都在解「別讓 agent 自己宣布完成」。
- **與 [qm](qm.md)(YC 的 multiplayer agent harness)**:同樣想解「多個 agent + 人一起工作」的協調問題,但 qm 是 harness 層,Codex Taskboard 是**在既有 harness(Codex/DeepSeek)旁邊掛一塊共享議題板**,兩者可對照「協調層要做多厚」。

## 注意事項與已知限制

- **安全:CDP 對本機其他進程無驗證。** README 明講:啟動器活著時,同機任何進程都能碰那個 CDP port,**只在此時跑受信任的本地程式碼**。這是把 debug 通道當生產通道用的固有風險。
- **LAN 模式零驗證,且預設對外。** `CODEX_TASKBOARD_HOST` **預設 `0.0.0.0`**(綁全網卡),受信任網路上任何人碰得到 URL 就能讀寫整塊板;要關 LAN 得手動設 `127.0.0.1`。公網/雲端才有 Basic Auth 邊界。
- **綁死特定 Codex 版本行為。** 注入依賴 Codex renderer 的 DOM/CSP 細節(README 直接寫死 `Codex 26.715.52143`);官方 app 一改版,注入很可能就得跟著修。這是「注入第三方閉源 app」的長期維護成本。
- **雲端只支援「兩位協作者」**,不是多人團隊方案;還是走 Basic Auth 共享密碼。
- **仍在 beta、簽名未齊、star 成長與成熟度不對稱**:1.5 個月 3,020 星、但版本 `-beta`、Windows 未簽名、macOS 公開下載還缺 notarization。用它得自己補生產化的最後一哩。
- **命名/topic 有誤導性**:repo slug `dashi-taskboard`、topics 掛 `claude-code`/`skills`,但產品叫 Codex Taskboard、實際整合是 Codex + DeepSeek。第一次看很容易誤判(見開頭 warning)。

## 研究價值與啟示

### 關鍵洞察

1. **「把面板長進 agent 宿主裡」是這專案真正的創新點**:大多數 AI 任務工具是「另開一個網站/app 讓你切過去」;它反過來,用 CDP 注入 / Cordis 插件**把議題板塞進 Codex、DeepSeek 的側邊欄**,讓 agent 用 CLI 直接動同一塊板。這示範了「當宿主沒有插件 API 時,怎麼用 CDP + document-start script 硬擠出一個嵌入點」——是很實用、但也很吃維護的一條路。

2. **同一套 HTTP API 同時餵人跟 agent,是乾淨的架構決策**:React UI 跟 `taskctl` CLI 打的是同一組路由,加上 `version` 樂觀鎖 + SSE 廣播,才撐得起「多 agent + 人同時改同一塊板」。這比「UI 一套 API、agent 一套 API」省掉大量一致性問題,值得抄。

3. **人工驗收 gate 寫進 Skill,而不是靠人自律**:Skill 硬性規定 `backlog=未核准`、認領要帶 version、**沒你點頭不准 `done`**。把「交接協定」固化進 SKILL.md,是「怎麼讓 agent 守規矩」的一個具體範本——比在 prompt 裡拜託有效。

4. **dogfooding 到近乎透明**:`docs/consumer-task-board-chatgpt-pro-review.md` 把「用 ChatGPT Pro 生 patch → 獨立驗收(密鑰掃描、逐檔比對、`git apply --check`、測試通過數)」整套記錄公開,連 SHA-256 都貼。這種「連自己怎麼用 AI 改自己」都攤開的做法,本身就是研究素材。

### 與其他研究筆記的關聯

- **[dashi-ppt-skill](dashi-ppt-skill.md)(姊妹作)**:同作者 chuspeeism 的 `dashi-*` repo 家族。兩者都走「**把工具嵌進 coding agent 的工作流**」路線(一個是任務板、一個是簡報 skill),可並讀看同一個作者對「agent 周邊工具」的產品觀。注意兩者**產品品牌與 repo slug 不一定一致**,別被 `dashi-` 前綴誤導成同一個品牌。
- **[dispatch](dispatch.md) / [mission-control-center](mission-control-center.md)**:同屬「agent + 儀表板」空間,但那兩個偏**監看**、本篇偏**議題狀態機 + 人工驗收**,並排讀可分清「監看 agent」vs「管理工作項」兩種定位。
- **[humanlayer-skills](humanlayer-skills.md)**:同樣在解「human-in-the-loop 審批/驗收」,可對照「驗收 gate」的不同做法。
- **[slide-deck-skill](slide-deck-skill.md)**:另一個「Agent Skill = 一整套產品(不只一頁 prompt)」的極端案例——本篇把 Skill、CLI、注入腳本、桌面 app 全包成一坨,是同一個「skill 規模上限很高」現象的另一個樣本。
- **[qm](qm.md) / [harness-design-long-running-apps](harness-design-long-running-apps.md)**:協調多 agent / 長時運行 app 的設計討論,可當本篇「協調層」的理論背景。

## 一句話總結

> chuspeeism 的 **Codex Taskboard**(repo 叫 `dashi-taskboard`)——一個 local-first、人跟 coding agent 共用的議題看板:同一套本機 HTTP API 同時餵 React 看板跟 `taskctl` CLI,靠七狀態機 + 樂觀鎖 + SSE 撐起多人多 agent 協作,並把「沒你點頭不准 done」的驗收 gate 寫進 bundled Skill。招牌是**嵌入機制**:對 Codex 桌面 app 用 CDP 注入把面板塞進側邊欄(不改 app.asar、不 patch React),對 DeepSeek Harness 用正規 Cordis 插件(`pnpm dsh plugin`);Tauri 打包成自帶 Node runtime 的桌面 app,Apache-2.0。1.5 個月衝 3,020 星、但還是 beta,而且要小心 `dsh` 是 DeepSeek Harness 的 CLI、不是「Dashi 品牌」。
