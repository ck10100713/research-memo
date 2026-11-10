# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">264</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-11-10</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    31 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    87 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    49 篇筆記

    [:octicons-arrow-right-24: 前往](topics/quant-trading.md)

-   :material-bullhorn-outline:{{ .lg .middle }} **社群行銷**

    ---

    5 篇筆記

    [:octicons-arrow-right-24: 前往](topics/social-marketing.md)

-   :material-palette-outline:{{ .lg .middle }} **AI 創作資源**

    ---

    7 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-creative.md)

-   :material-apps:{{ .lg .middle }} **AI 應用**

    ---

    27 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-apps.md)

-   :material-radar:{{ .lg .middle }} **OSINT / 情報工具**

    ---

    2 篇筆記

    [:octicons-arrow-right-24: 前往](topics/osint.md)

-   :material-book-open-variant:{{ .lg .middle }} **軟體工程知識**

    ---

    4 篇筆記

    [:octicons-arrow-right-24: 前往](topics/software-engineering.md)

-   :material-wrench-outline:{{ .lg .middle }} **開發工具**

    ---

    14 篇筆記

    [:octicons-arrow-right-24: 前往](topics/dev-tools.md)

-   :material-puzzle-outline:{{ .lg .middle }} **Agent Skills**

    ---

    3 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-skills.md)

-   :material-star-outline:{{ .lg .middle }} **資源彙整 / Awesome List**

    ---

    5 篇筆記

    [:octicons-arrow-right-24: 前往](topics/awesome-lists.md)

-   :material-school-outline:{{ .lg .middle }} **學習資源**

    ---

    30 篇筆記

    [:octicons-arrow-right-24: 前往](topics/learning.md)

</div>

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-clock-alert-outline:{{ .lg .middle }} **AI On-Duty（AI 自動化工作流：困難部分）**

    ---

    `2026-11-10` 繁中策展影片課，主題是排程與 CI/CD：GitHub Actions、Cloudflare Cron Triggers、把 Claude Code 放進 CI。13 章 49 單元 201 支影片，每個單元對照 2026 官方文件標時效（49 單元查 29 個，17 個已飄移），repo 本身用週排程驗連結、死了自動開 issue

    [:octicons-arrow-right-24: 閱讀筆記](ai-onduty.md)

-   :material-file-check-outline:{{ .lg .middle }} **MUSE Evidence Review Core**

    ---

    `2026-11-05` 黑客松作品：拿 Meta muse-wonder-1.0 逐句審稿，每句判 SUPPORTED / CONTRADICTED / NOT_ESTABLISHED / NEEDS_HUMAN_REVIEW，引文在本機逐字對回原文；改稿後舊審查自動變 STALE。純 Python 標準函式庫，對 API 金鑰、送出同意、網路出口的防護做得很重

    [:octicons-arrow-right-24: 閱讀筆記](muse-evidence-review-core.md)

-   :material-format-list-bulleted-type:{{ .lg .middle }} **Agent Use Cases 全目錄（1872 筆）**

    ---

    `2026-11-05` agentusecases.ai 收錄的 1872 筆 AI agent 實際用例,翻成中文、依 11 個主題分類,每筆一句話說明做了什麼,點標題連回原頁看結果和 prompt

    [:octicons-arrow-right-24: 閱讀筆記](agentusecases-catalog.md)

-   :material-sync:{{ .lg .middle }} **Harness²（google-research/harness2）**

    ---

    `2026-11-05` Google Research 的遞迴 harness 優化框架：不動模型權重，每遇到新任務就自己改 prompt / skill / script / hook 再跑，沒有標準答案也能挑出更好的 harness，並把學到的教訓存成跨任務經驗庫

    [:octicons-arrow-right-24: 閱讀筆記](harness2.md)

-   :material-lightbulb-on-outline:{{ .lg .middle }} **Agent Use Cases(agentusecases.ai)**

    ---

    `2026-11-05` Alex Finn 經營的 AI agent 實際用例目錄,每天從網路、X、Reddit、HN 掃描,目前收錄 1,872 筆。每筆都寫了做了什麼、結果如何(包含失敗)、要注意什麼,並附一段可以直接複製的 prompt。依 28 個 agent、11 個主題、數十個具體工作分類,Claude Code 以 256 筆居冠。適合找 agent 能做什麼的靈感,但很多筆來源只有一則貼文,沒有驗證

    [:octicons-arrow-right-24: 閱讀筆記](agentusecases.md)

-   :material-image-filter-hdr:{{ .lg .middle }} **napali**

    ---

    `2026-11-03` 用 Claude Code(Opus 5.5)跑 13 輪 agent 做出來的 Na Pali 海岸無人機空拍,沒有任何貼圖、模型或圖片,地形侵蝕、FFT 海浪、浪花、礁岩、一棵棵 SDF 樹、體積雲全部在一個 5,273 行的 index.html 裡用 WebGL2 shader 算。做法是水/天/地形/植被各派一個 specialist 平行改、再合併、最後由 judge 對照實景照片打分。MIT,129★

    [:octicons-arrow-right-24: 閱讀筆記](napali.md)

-   :material-broom:{{ .lg .middle }} **ub-mode**

    ---

    `2026-10-30` Uncle Bob(Robert C. Martin)把 poteto-mode 的原則砍到只剩一份約 140 行的 SKILL.md:Make it Work → Make it Right → Practice 三段,每條原則壓成兩三句祈使句,並強制 TDD;最大差異是把『寫得好不好』交給自己寫的三個確定性工具把關(crapper 的 CRAP < 10、dryer 的重複度 < 0.8、mutator 的突變測試)。5 天 4.8k★,但 repo 沒有授權檔

    [:octicons-arrow-right-24: 閱讀筆記](ub-mode.md)

-   :material-timer-sand:{{ .lg .middle }} **hftbacktest**

    ---

    `2026-10-28` nkaz001 的高頻交易 / 造市回測框架:用逐筆 L2/L3 訂單簿重建市場,模擬掛單在佇列中的位置、行情與下單兩種延遲,讓回測結果盡量對得上實盤;Rust 核心 + Python(Numba njit)介面,同一份 Rust 策略能直接接 Binance Futures / Bybit 實盤。5k★、MIT,但 master 自 2025-12 後沒有新 commit

    [:octicons-arrow-right-24: 閱讀筆記](hftbacktest.md)

-   :material-crown-outline:{{ .lg .middle }} **poteto-mode(pstack)**

    ---

    `2026-10-28` Lauren Tan(@poteto,React core、Cursor)的 pstack plugin 入口 skill:一句 /poteto-mode 把任務對到 23 份 playbook 之一、步驟原文抄成 todolist,主控只負責設計 / 審查 / 驗證,實作派給 subagent;配 24 條 principle skill、多模型對抗審查(只收跑得出失敗的 finding)、能實驗就不問人。Cursor 原生,Claude Code 有官方對照表,社群另有多個移植版

    [:octicons-arrow-right-24: 閱讀筆記](poteto-mode.md)

-   :material-scale-balance:{{ .lg .middle }} **HowToLiveBetter(高性价比人生指南)**

    ---

    `2026-10-27` 簡中《高性价比人生指南》:34 節 767 條人生建議(健康、急救、省錢、法律紅線、勞保醫保、婚育、創業合規),每條寫明成本、收益、證據等級 A/B/C 和原始文獻;純 Markdown 當資料庫,靜態檢索頁 + CI 檢查寫作規範,附一個讓 Claude Code 照書回答的 skill。兩個月 7 萬星,法規部分只適用中國大陸

    [:octicons-arrow-right-24: 閱讀筆記](howtolivebetter.md)

-   :material-palette:{{ .lg .middle }} **storytold(ArtCraft)**

    ---

    `2026-10-23` ArtCraft 團隊(前身是 FakeYou / vo.codes 語音生成)的 GitHub org:主力產品 ArtCraft 是「給藝術家的 IDE」,在 2D/3D 場景裡組好構圖再丟給 62 個圖像/影片/3D 模型生成;2026-09-30 起又用 AI agent 大量產出一整套純 Rust 的 clean-room 辦公/創作軟體(PhotoCraft 對標 Photoshop、WordCraft 對標 Word 等 13 個 app),PhotoCraft 三週 7.1 萬星、66 萬行 Rust、每個動作都能透過 CLI / JSON / MCP 讓 agent 操作

    [:octicons-arrow-right-24: 閱讀筆記](storytold.md)

-   :material-movie-open-play:{{ .lg .middle }} **Wan2GP(WanGP)**

    ---

    `2026-10-22` DeepBeepMeep 一人主導的「GPU 窮人」本機生成超級 app:從 Wan2.1 fork 起家,現在一個 Gradio 介面塞進 Wan 2.1/2.2、LTX-2.x、Hunyuan Video、MiniMax H3、Flux、Qwen Image、TTS、音樂、3D 等 277 個模型定義;靠自家 mmgp 做分塊 offload、量化與 VRAM 配置,部分模型 6 GB VRAM 就能跑。內建 Python API + MCP server + 官方 agent skill,Claude Code / Codex 可以直接當遙控器。授權從 Apache-2.0 一路改成自訂的 WanGP Community License 2.0

    [:octicons-arrow-right-24: 閱讀筆記](wan2gp.md)

-   :material-chart-bell-curve:{{ .lg .middle }} **Awesome Quant Interview**

    ---

    `2026-10-15` 前私募 QR 寫的簡中 Quant Research 面試筆記：55 題八股文全附答案，加上項目復盤 8 問、策略方向論文清單和工具書單；內容紮實，但有幾處文獻張冠李戴、一個資訊洩漏例子寫錯

    [:octicons-arrow-right-24: 閱讀筆記](awesome-quant-interview.md)

-   :material-account-tie-voice:{{ .lg .middle }} **AI Engineering Interview Questions Company Wise**

    ---

    `2026-09-23` Outcome School 整理的 AI 工程師面試題庫，按 35 家公司分區(Anthropic、OpenAI、Cursor、Palantir…)，每家附面試流程；約 600 題、四成附答案，但答案全連回作者自家部落格，題目也沒標出處

    [:octicons-arrow-right-24: 閱讀筆記](ai-engineering-interview-questions-company-wise.md)

-   :material-magnify-scan:{{ .lg .middle }} **Open SEO Advisor（open-seo-advisor-skill）**

    ---

    `2026-09-23` 設計給 Claude Code 之類 AI coding agent 用的「全域行銷營運技能」，也能當 CLI 獨立跑。七大模式（SEO 顧問／工程師／資安／文章寫手／外掛開發／Meta 廣告／產圖）＋ 26 個 AI 角色的矩陣營運層，v0.4 起加了 SEO/AEO 引導式建站。設計原則是不綁定單一廠商、預設唯讀 dry-run、免金鑰可試玩。注意核心健檢有個 robots/sitemap 必定誤報的 bug 拖了兩個月，v0.4.6 才修。跟本站的反詐投資王同一位作者

    [:octicons-arrow-right-24: 閱讀筆記](open-seo-advisor-skill.md)

-   :material-language-rust:{{ .lg .middle }} **Copilot runtime 搬到 Rust**

    ---

    `2026-09-18` Stephen Toub 寫的 65 分鐘長文：GitHub Copilot agent runtime 從 TypeScript/Node 整包換成 Rust，43 萬行 TS 換出 83 萬行production Rust，2026-05-12 到 08-21 約 14 週，主要由一個人 + 大量 agent 完成，128 個 PR 邊搬邊出貨。有硬數字：單次 turn 從 5.25 秒降到 292 毫秒（18 倍）、session 生命週期吞吐從 7.55/秒 到 120/秒。更值得看的是 agent 使用數據——工具呼叫 185 萬次裡探索類是編輯類的 10 倍、prompt cache 命中率 96.22%、壓縮 5,116 次、borrow checker 只佔編譯錯誤的 1.7%。還有兩個真實事故：agent 之間互相併吞分支、以及用一個 chat session 當「agentic mutex」擋建置塞車

    [:octicons-arrow-right-24: 閱讀筆記](copilot-runtime-rust-port.md)

-   :material-book-multiple:{{ .lg .middle }} **ccc115a/se `_more/mybook` 三本書**

    ---

    `2026-09-16` 金門大學資工系陳鍾誠教授 115 學年上學期《現代軟體工程》課程 repo（MIT、30★）裡藏的 `_more/mybook`——三本各自寫完整的繁體中文技術書草稿，共 216 個分節 Markdown、約 198K 漢字、256 個 mermaid 圖：《現代軟體工程：從基礎到 AI Agent 實踐》（87 節，三篇 14 章 + 附錄 ABC，明講參考李博杰 agent-book）、《演進式架構實戰》（75 節，用淘寶 14 次架構演進當問題驅動主線）、《從 Docker 到 Kubernetes：Rust × WebSocket/SSR/MPA 實戰》（46 節）。每節一檔、靠 README 當目錄，本筆記附上把它們合併成單一本書的方法與腳本

    [:octicons-arrow-right-24: 閱讀筆記](ccc115a-se-mybook.md)

</div>

[查看研究索引](news.md)
