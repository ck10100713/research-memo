# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">223</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-08-06</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    27 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    77 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    45 篇筆記

    [:octicons-arrow-right-24: 前往](topics/quant-trading.md)

-   :material-bullhorn-outline:{{ .lg .middle }} **社群行銷**

    ---

    3 篇筆記

    [:octicons-arrow-right-24: 前往](topics/social-marketing.md)

-   :material-palette-outline:{{ .lg .middle }} **AI 創作資源**

    ---

    5 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-creative.md)

-   :material-apps:{{ .lg .middle }} **AI 應用**

    ---

    21 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-apps.md)

-   :material-radar:{{ .lg .middle }} **OSINT / 情報工具**

    ---

    2 篇筆記

    [:octicons-arrow-right-24: 前往](topics/osint.md)

-   :material-book-open-variant:{{ .lg .middle }} **軟體工程知識**

    ---

    3 篇筆記

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

    2 篇筆記

    [:octicons-arrow-right-24: 前往](topics/awesome-lists.md)

-   :material-school-outline:{{ .lg .middle }} **學習資源**

    ---

    21 篇筆記

    [:octicons-arrow-right-24: 前往](topics/learning.md)

</div>

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-account-tie:{{ .lg .middle }} **mattpocock/skills**

    ---

    `2026-08-06` Matt Pocock (Total TypeScript) 把每天用的 agent skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnosing-bugs / improve-codebase-architecture，半年衝到 205k stars

    [:octicons-arrow-right-24: 閱讀筆記](mattpocock-skills.md)

-   :material-bank:{{ .lg .middle }} **GS Quant（gs-quant）**

    ---

    `2026-08-06` Goldman Sachs 官方量化金融 Python 工具包：把 GS 自家衍生品定價／風險引擎、跨資產回測、時間序列分析包成統一 API；近期加碼官方 MCP server 與 agent skills

    [:octicons-arrow-right-24: 閱讀筆記](gs-quant.md)

-   :material-account-group:{{ .lg .middle }} **qm**

    ---

    `2026-08-06` Y Combinator 出品的『multiplayer agent harness for work』：每位員工/每個房間各有隔離的 memory·檔案·keychain·sandbox，在 Slack 與 web 協作；harness 無關(Pi/Codex/Claude Code/OpenCode 同一核心)、可自架

    [:octicons-arrow-right-24: 閱讀筆記](qm.md)

-   :material-notebook-edit:{{ .lg .middle }} **lecture-to-notes**

    ---

    `2026-08-04` 演講／研習錄影 → 結構化「可溯源」筆記 + 影片-逐字稿-摘要三向同步的 HTML 檢視器；本機 GPU pipeline(Whisper·投影片抽取·OCR·VLM),Claude Code skill + CLI

    [:octicons-arrow-right-24: 閱讀筆記](lecture-to-notes.md)

-   :material-arrow-collapse-horizontal:{{ .lg .middle }} **Headroom**

    ---

    `2026-08-04` AI Agent 的 context 壓縮層：在 tool 輸出、log、RAG chunk 進入 LLM 前壓縮，JSON 省 60–95%、coding agent 省 15–20%，且可逆還原

    [:octicons-arrow-right-24: 閱讀筆記](headroom.md)

-   :material-file-search-outline:{{ .lg .middle }} **pdf-inspector**

    ---

    `2026-08-03` Firecrawl 開源 Rust PDF 解析器 — 免 OCR 分類文字/掃描檔，200ms 內轉乾淨 Markdown

    [:octicons-arrow-right-24: 閱讀筆記](pdf-inspector.md)

-   :material-home-search-outline:{{ .lg .middle }} **AI Real Estate Assistant**

    ---

    `2026-07-28` 單人（1314/1400 commits）做出 6 萬行、7000 測試、13 個 LLM provider 的房產 RAG 搜尋平台，MIT 授權 + 明碼標價的 open-core 漏斗（Pro $29/mo）；最值得看的是它把「Render 免費層 512MB 逼出的 lazy import hack」連同「這不是最佳實踐」一起寫進 README

    [:octicons-arrow-right-24: 閱讀筆記](ai-real-estate-assistant.md)

-   :material-flask-outline:{{ .lg .middle }} **StockAgent**

    ---

    `2026-07-28` ACM TIST 論文的官方實作：用 LLM 多代理模擬股市，刻意不餵歷史行情以避開 test set leakage；核心結論是「換一個 LLM 就換一種市場」——GPT 交易少但單量大、個體分散，Gemini 頻繁交易且群體高度趨同。程式碼有多處已驗證的落差，預設參數下所有事件都不會觸發

    [:octicons-arrow-right-24: 閱讀筆記](stockagent.md)

-   :material-account-group-outline:{{ .lg .middle }} **crewAI-examples**

    ---

    `2026-07-28` CrewAI 官方 30 個完整範例（16 crews + 6 flows + 3 integrations + 5 notebooks），新舊兩代專案骨架並存可直接對照框架演進；但安全性做過一輪硬化、功能正確性沒有——stock_analysis 有重複方法、寫死 AMZN、README 與程式碼互相矛盾，SEC 工具的正則還會把財報數字的小數點和負號洗掉

    [:octicons-arrow-right-24: 閱讀筆記](crewai-examples.md)

-   :material-notebook-multiple:{{ .lg .middle }} **GenAI Agents (NirDiamant)**

    ---

    `2026-07-28` 23.5k ★、53 本可跑的 agent 教學 notebook，從對話機器人到多代理系統——但授權是「非商業限定 + 投稿者交出商業權利」的自訂條款，不是開源；且 requirements.txt 凍結在 2024-09，約三分之二內容其實是 LangGraph 應用集

    [:octicons-arrow-right-24: 閱讀筆記](genai-agents.md)

-   :material-format-list-numbered:{{ .lg .middle }} **i-have-adhd**

    ---

    `2026-07-27` 6.8KB 的 10 條輸出規則讓 coding agent 停止把答案埋在廢話裡（動作優先、步驟編號、砍掉「Hope this helps!」），2.5 個月 10.6k stars；真正值得抄的是它把一段 prompt 包成有 eval harness、release gate、8 平台安裝指南的工程專案

    [:octicons-arrow-right-24: 閱讀筆記](i-have-adhd.md)

-   :material-toy-brick-outline:{{ .lg .middle }} **Bring Your Own Agent (BYOA Core)**

    ---

    `2026-07-27` 台灣單人開發者用 5.5 週、90 commits 從零重建一套 Claude Code 等級的 agent harness（兩階段 compact、subagent 防遞迴、skill 漸進式載入、tool result 分頁、多 provider gateway），全繁中、Gherkin 規格先行、附 13 個 SWE eval task 量化每次 prompt 改動——0 star 但是最好讀的 harness 解剖圖

    [:octicons-arrow-right-24: 閱讀筆記](bring-your-own-agent.md)

-   :material-view-dashboard-variant:{{ .lg .middle }} **Mission Control Center**

    ---

    `2026-07-26` 遠振資訊 solo 維護的 OpenClaw 營運儀表板——server-resident、瀏覽器內操作 VPS，含晨報/備份/第二大腦/LINE 客服 ops

    [:octicons-arrow-right-24: 閱讀筆記](mission-control-center.md)

-   :material-palette-swatch:{{ .lg .middle }} **Awesome DESIGN.md — AI Agent 的設計系統資料庫**

    ---

    `2026-07-26` 73+ 個知名品牌 DESIGN.md 合集 — 丟進專案讓 AI Agent 產出 pixel-perfect UI（★104k，含超跑與 90 年代懷舊系列）

    [:octicons-arrow-right-24: 閱讀筆記](awesome-design-md.md)

-   :material-robot-happy:{{ .lg .middle }} **Vibe-Trading（HKUDS）**

    ---

    `2026-07-24` HKUDS 的『個人交易 Agent』——pip 一行裝起，自然語言驅動 88 skill / 462 alpha / 8 回測引擎，安全設計靠結構性 paper/live 護欄而非 config flag

    [:octicons-arrow-right-24: 閱讀筆記](vibe-trading.md)

-   :material-toolbox:{{ .lg .middle }} **jezweb/claude-skills**

    ---

    `2026-07-23` Jezweb 的 63-skill / 10-plugin 生產型 skill 市集——核心價值在兩份把官方規範編輯化的 authoring 準則（SKILL_SHAPE.md / CLAUDE.md）

    [:octicons-arrow-right-24: 閱讀筆記](jezweb-claude-skills.md)

-   :material-hammer-wrench:{{ .lg .middle }} **建構型 Agent SDK Skills 對照**

    ---

    `2026-07-23` 『建構型 skill』對照 — 教 coding agent 用 SDK 把 agent 寫出來：Claude Agent SDK（雙語第三方最成熟）、OpenAI、Microsoft Agent Framework 三方現況

    [:octicons-arrow-right-24: 閱讀筆記](agent-sdk-builder-skills.md)

</div>

[查看研究索引](news.md)
