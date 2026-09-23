# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">251</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-09-23</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    31 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    84 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    48 篇筆記

    [:octicons-arrow-right-24: 前往](topics/quant-trading.md)

-   :material-bullhorn-outline:{{ .lg .middle }} **社群行銷**

    ---

    5 篇筆記

    [:octicons-arrow-right-24: 前往](topics/social-marketing.md)

-   :material-palette-outline:{{ .lg .middle }} **AI 創作資源**

    ---

    5 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-creative.md)

-   :material-apps:{{ .lg .middle }} **AI 應用**

    ---

    25 篇筆記

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

    27 篇筆記

    [:octicons-arrow-right-24: 前往](topics/learning.md)

</div>

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-account-tie-voice:{{ .lg .middle }} **AI Engineering Interview Questions Company Wise**

    ---

    `2026-09-23` Outcome School 整理的 AI 工程師面試題庫，按 35 家公司分區(Anthropic、OpenAI、Cursor、Palantir…)，每家附面試流程；約 600 題、四成附答案，但答案全連回作者自家部落格，題目也沒標出處

    [:octicons-arrow-right-24: 閱讀筆記](ai-engineering-interview-questions-company-wise.md)

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

-   :material-magnify-scan:{{ .lg .middle }} **Open SEO Advisor（open-seo-advisor-skill）**

    ---

    `2026-09-15` 設計給 Claude Code 之類 AI coding agent 用的「全域行銷營運技能」，也能當 CLI 獨立跑。七大模式（SEO 顧問／工程師／資安／文章寫手／外掛開發／Meta 廣告／產圖）＋ 26 個 AI 角色的矩陣營運層，目前四個模式完整實作。設計原則是不綁定單一廠商、預設唯讀 dry-run、免金鑰可試玩。跟本站的反詐投資王同一位作者

    [:octicons-arrow-right-24: 閱讀筆記](open-seo-advisor-skill.md)

-   :material-brain:{{ .lg .middle }} **MiniMind**

    ---

    `2026-09-15` 61K★、Apache-2.0 的「從 0 訓練一個小 LLM」教學專案——單張 3090、約 2.3 小時、約 3 塊人民幣就能把 64M 參數的 minimind-3 從預訓練練到會對話。關鍵訓練演算法與核心模組全部從 0 實現不依賴框架封裝，但結構對齊 Qwen3 生態、可轉 transformers/llama.cpp/ollama。涵蓋 Pretrain→SFT→LoRA→DPO→RLAIF(PPO/GRPO/CISPO)→Tool Use→Agentic RL 完整鏈路

    [:octicons-arrow-right-24: 閱讀筆記](minimind.md)

-   :material-bee:{{ .lg .middle }} **AutoHedge**

    ---

    `2026-09-14` The Swarm Corporation 的「自主對沖基金 Agent」——6.1K★、Director→Quant→Risk→Execution 四 Agent + Solana 真單執行。但實際讀 code：整包約 22 KB Python、一半是 prompt 字串（還有一半是死的），會簽 Solana 交易的 execute_trade 沒接到任何 agent 上，.env 寫的私鑰變數名跟程式讀的不一樣，18 個 CI workflow 指向不存在的 tests/，repo 裡躺著 37 MB 時間戳壞掉的假交易紀錄，主線 2026-02 後停更。是「README 遠大於 code」的教材級案例

    [:octicons-arrow-right-24: 閱讀筆記](autohedge.md)

-   :material-robot-happy:{{ .lg .middle }} **Vibe-Trading（HKUDS）**

    ---

    `2026-09-14` HKUDS 的『個人交易 Agent』——pip 一行裝起，自然語言驅動 90 skill / 107 agent tool / 462 alpha / 10 回測引擎 / 18 家券商，安全設計靠結構性 paper/live 護欄而非 config flag，另有一道 grounding gate 擋住模型沒抓過就講出來的數字。約 155 位貢獻者、每天合 5–8 個 PR。2026-09 已 33K★、v0.1.15

    [:octicons-arrow-right-24: 閱讀筆記](vibe-trading.md)

-   :material-book-open-page-variant:{{ .lg .middle }} **《深入理解 AI Agent》(ai-agent-book)**

    ---

    `2026-09-11` 前華為『天才少年』、Pine AI 首席科學家李博杰寫的《深入理解 AI Agent:設計原理與工程實踐》——45.7K★、Apache-2.0『整本書免費開源』(正文 + PDF/EPUB + 109 個配套實驗全放 GitHub)。以核心公式 Agent = LLM + 上下文 + 工具 用十章從原理講到生產:上下文工程(KV Cache/Skills/壓縮)、用戶記憶與 RAG、工具與 MCP、Coding Agent、語音/Computer Use/機器人交互、評估、模型後訓練(SFT/RL)、持續進化、multi-agent。用 whisper coding 口述式協作寫成,15 種語言,含繁體中文台灣版

    [:octicons-arrow-right-24: 閱讀筆記](ai-agent-book.md)

-   :material-file-presentation-box:{{ .lg .middle }} **dashi-ppt-skill**

    ---

    `2026-09-10` 中國「大师的AI小灶」出品的 Claude / Codex Agent Skill:把一份文件丟給 agent,先整理成 goal.json 計畫,再用內建 React 生成器(非 reveal/Marp/Slidev)輸出 12 套視覺主題、可離線打開的 HTML 簡報。招牌是『產物即編輯器』——每頁自帶控制台(滑桿調模組數/換版式/換配色)+ 文字就地編輯 + 拖曳換圖,改動即時存回 index.html;能一鍵匯出 HTML 離線包、截圖式 PDF、與『逐節點保真、文字仍可編輯(無 OCR)』的真 PPTX。整包 AGPL-3.0、但導出引擎是專有授權;內容零上傳、本機優先;簡體介面 + 中英雙語編輯器,惟未內建 CJK 字型(靠系統字型)

    [:octicons-arrow-right-24: 閱讀筆記](dashi-ppt-skill.md)

-   :material-view-column:{{ .lg .middle }} **dashi-taskboard**

    ---

    `2026-09-10` chuspeeism 出的『Codex Taskboard』:一個 local-first 的議題看板(七狀態 kanban + 三欄消費者視圖),同一套本機 HTTP API 同時餵 React UI 跟 taskctl CLI。招牌是『嵌進 coding agent 桌面 app 裡面』——用 CDP 注入把看板塞進 Codex(ChatGPT.app)側邊欄當 OOPIF,或用一個真正的 Cordis 插件(pnpm dsh plugin)塞進 DeepSeek Harness。附 bundled Codex Skill(manage-taskboard)讓 agent 自己搬卡、驗收、等你點頭才 done。Tauri 打包 macOS/Windows/Linux 桌面 app,自帶 Node runtime;Apache-2.0。注意:repo 叫 dashi-taskboard 但產品叫 Codex Taskboard,dsh 是 DeepSeek Harness 的 CLI 不是 Dashi 品牌

    [:octicons-arrow-right-24: 閱讀筆記](dashi-taskboard.md)

-   :material-forum-outline:{{ .lg .middle }} **LangBot**

    ---

    `2026-09-09` 跟 AstrBot 同賽道的自架多平台 LLM IM 機器人平台(17.7K stars、Python、Apache-2.0),前身是 2022 年的 QChatGPT(mirai QQ bot),2024-11 的 v3.4.0 移除 Mirai、加 WebUI 後正式改名 LangBot。一套後端接 QQ/微信/企微/飛書/釘釘/Discord/Telegram/Slack/LINE/KOOK/Matrix;LLM 從 OpenAI/Anthropic/Gemini/DeepSeek/智譜/Kimi/Grok/Ollama 到一票聚合平台;最大特色是能把整段對話丟給 Dify/Coze/n8n/Langflow/DeerFlow/WeKnora/百煉/螞蟻TBox 當外部大腦(runner),插件跑在獨立 Plugin Runtime 進程(SDK 隔離),沙盒用 Box Runtime(nsjail/e2b),向量庫支援 6 種、資料庫可 PostgreSQL,還內建 /mcp server + 倉庫內 skills 讓 coding agent 直接操作機器人本身。Web 前端是 React(Vite),不是 AstrBot 的 Vue

    [:octicons-arrow-right-24: 閱讀筆記](langbot.md)

</div>

[查看研究索引](news.md)
