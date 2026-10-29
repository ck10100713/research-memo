# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">257</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-10-28</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    30 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    86 篇筆記

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

    6 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-creative.md)

-   :material-apps:{{ .lg .middle }} **AI 應用**

    ---

    26 篇筆記

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

    3 篇筆記

    [:octicons-arrow-right-24: 前往](topics/awesome-lists.md)

-   :material-school-outline:{{ .lg .middle }} **學習資源**

    ---

    29 篇筆記

    [:octicons-arrow-right-24: 前往](topics/learning.md)

</div>

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

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

-   :material-eye-lock:{{ .lg .middle }} **Argus**

    ---

    `2026-09-16` 台灣開發者 nathawu 寫的「確認優先（Confirm-First）」閘門外掛，同時支援 Claude Code 與 OpenAI Codex——AI 先用白話文覆述最多 5 點需求重點（自己補的假設要標「（假設）」），你按下「正確，開始執行」之前，PreToolUse hook 硬性擋掉除提問工具外的所有工具呼叫。實作只有 148 行核心 + 83 行 Codex adapter，測試卻有 487 行（33 個 case，實測 32 pass / 1 skip）。設計上刻意 fail-open：hook 自己出錯就放行，絕不卡住正常使用。目前 5★、3 個 commit、**沒有 LICENSE 檔**

    [:octicons-arrow-right-24: 閱讀筆記](argus.md)

-   :material-chip:{{ .lg .middle }} **《深入理解 AI Infra》(ai-infra-book)**

    ---

    `2026-09-15` 李博杰《深入理解 AI Agent》的姊妹作《深入理解 AI Infra：量化分析與系統設計》——開站 3.5 週 2.6K★、Apache-2.0 全書開源。核心命題：模型成了 LLM 時代的作業系統，AI Infra 成了 LLM 時代的計算機體系結構。方法論明著對標《計算機體系結構：量化研究方法》，12 章都從硬體約束量化推導系統設計，全書追問同五個問題：搬什麼、搬多少、搬幾次、經過哪裡、誰必須等它。附一個只靠 Python 標準庫、不用 GPU 就能複算全書數字的 CLI

    [:octicons-arrow-right-24: 閱讀筆記](ai-infra-book.md)

-   :material-chart-timeline-variant:{{ .lg .middle }} **CZSC（纏中說禪技術分析工具）**

    ---

    `2026-09-15` 纏中說禪（纏論）技術分析工具，6.2K★、2019 年至今維護六年。1.0 版把分型／筆／中樞等纏論核心演算法全部改用 Rust 重寫，透過 PyO3 以 czsc._native 暴露給 Python，底層 9 個 crate、220+ 個信號函數。定義了「信號—事件—交易」三層邏輯體系，把中文技術分析理論做成可回測的工程系統

    [:octicons-arrow-right-24: 閱讀筆記](czsc.md)

-   :material-database-search:{{ .lg .middle }} **awesome-data**

    ---

    `2026-09-15` AKShare 作者維護的金融資料源清單——把中國與國際的開源資料工具、官方 SDK、公開資料源與商業資料庫分四類列出。697★ 但 2025-03 後就沒更新，內容偏中國市場。價值在於它是 AKShare 生態的「資料源地圖」，不在於清單本身的完整度

    [:octicons-arrow-right-24: 閱讀筆記](awesome-data.md)

-   :material-microphone-message:{{ .lg .middle }} **VoiceStudio**

    ---

    `2026-09-15` 29.5K★、AGPL-3.0 的「本機版 ElevenLabs」——聲音複製、聲音設計、影片配音、聽寫、轉錄、有聲書，16 個 TTS + 11 個 ASR 引擎、646 種語言，全程跑在自己機器上，不用帳號、金鑰、訂閱。Tauri v2 + React + FastAPI，預設接 loopback，內建 AudioSeal 浮水印與 MCP server。repo 本身也是 AI 輔助開發的樣本（CLAUDE.md 18KB、skills/、skills-lock.json）

    [:octicons-arrow-right-24: 閱讀筆記](voicestudio.md)

-   :material-shield-alert-outline:{{ .lg .middle }} **反詐投資王（anti-gambling-trader-tw）**

    ---

    `2026-09-15` 台灣人做的「反詐投資王」——把交易紀錄丟進去，用期望值、t 檢定＋置中 Bootstrap、樣本外驗證判斷你的獲利是可重複的優勢還是運氣＋倖存者偏差，並內建詐騙話術掃描、假績效鑑識、假老師機率檢驗。核心引擎純 Python 標準庫零依賴、全程本機執行。最特別的是它刻意「誠實到不討喜」：五級裁決有四級是勸退，資料不完整時直接 fail closed 拒算而不是猜

    [:octicons-arrow-right-24: 閱讀筆記](anti-gambling-trader-tw.md)

-   :material-brain:{{ .lg .middle }} **MiniMind**

    ---

    `2026-09-15` 61K★、Apache-2.0 的「從 0 訓練一個小 LLM」教學專案——單張 3090、約 2.3 小時、約 3 塊人民幣就能把 64M 參數的 minimind-3 從預訓練練到會對話。關鍵訓練演算法與核心模組全部從 0 實現不依賴框架封裝，但結構對齊 Qwen3 生態、可轉 transformers/llama.cpp/ollama。涵蓋 Pretrain→SFT→LoRA→DPO→RLAIF(PPO/GRPO/CISPO)→Tool Use→Agentic RL 完整鏈路

    [:octicons-arrow-right-24: 閱讀筆記](minimind.md)

</div>

[查看研究索引](news.md)
