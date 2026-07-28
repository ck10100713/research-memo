# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">216</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-07-28</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    25 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    76 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    44 篇筆記

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

    18 篇筆記

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

-   :material-flask-outline:{{ .lg .middle }} **StockAgent**

    ---

    `2026-07-28` ACM TIST 論文的官方實作：用 LLM 多代理模擬股市，刻意不餵歷史行情以避開 test set leakage；核心結論是「換一個 LLM 就換一種市場」——GPT 交易少但單量大、個體分散，Gemini 頻繁交易且群體高度趨同。程式碼有多處已驗證的落差，預設參數下所有事件都不會觸發

    [:octicons-arrow-right-24: 閱讀筆記](stockagent.md)

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

-   :material-microsoft:{{ .lg .middle }} **microsoft/skills**

    ---

    `2026-07-23` 微軟官方 Agent Skills 庫（175 skills）— 用 Skill/Custom Agent/AGENTS.md/MCP 把 coding agent 接地到 Azure SDK 與 Foundry，含官方 Agent Framework 建構 skill

    [:octicons-arrow-right-24: 閱讀筆記](microsoft-skills.md)

-   :material-graph-outline:{{ .lg .middle }} **GraphRAG**

    ---

    `2026-07-21` 微軟研究院的 graph-based RAG — 用 LLM 把文件抽成知識圖譜 + 社群摘要，回答向量 RAG 答不了的『全局性』問題

    [:octicons-arrow-right-24: 閱讀筆記](graphrag.md)

-   :material-movie-open-play-outline:{{ .lg .middle }} **video-autopilot-kit**

    ---

    `2026-07-20` 填問卷變成你的系統 — YouTube/短影音自動化框架，ffmpeg pipeline + CapCut 自動化，零私人數據

    [:octicons-arrow-right-24: 閱讀筆記](video-autopilot-kit.md)

-   :material-bridge:{{ .lg .middle }} **cc-to-antigravity-cli-bridge**

    ---

    `2026-07-20` 從 Claude Code 驅動 Google Antigravity CLI (agy) — 靠 Gemini 抗反爬搜尋做雙軌查證 + 共享 system prompt

    [:octicons-arrow-right-24: 閱讀筆記](cc-to-antigravity-cli-bridge.md)

-   :material-bridge:{{ .lg .middle }} **cc-to-grok-bridge**

    ---

    `2026-07-20` 把 Claude Code 的 rules/skills/hooks/memory 搬到 Grok Build — 靠 thin adapter 讓 CC 資安 hook 在 Grok 上真正 hard-block

    [:octicons-arrow-right-24: 閱讀筆記](cc-to-grok-bridge.md)

-   :material-robot-industrial:{{ .lg .middle }} **OpenAI Agents SDK**

    ---

    `2026-07-17` OpenAI 官方 Agent 框架 — Handoffs + Guardrails 起家，v0.18 補上 Sandbox Agents 與 Human-in-the-loop

    [:octicons-arrow-right-24: 閱讀筆記](openai-agents-sdk.md)

-   :material-heart-pulse:{{ .lg .middle }} **AI 使用量儀表板（danleetw/ai_usage_dashboard）**

    ---

    `2026-07-08` 本機執行的 AI 用量儀表板，以電玩血條顯示 Claude/Codex/MiniMax/Antigravity/Kiro 使用率，零執行期依賴

    [:octicons-arrow-right-24: 閱讀筆記](ai-usage-dashboard.md)

-   :material-head-lightbulb:{{ .lg .middle }} **Advisor Tool（顧問工具）**

    ---

    `2026-07-08` executor（Sonnet/Haiku）生成中途諮詢 advisor（Opus）取得策略指引，近 Opus 品質、Sonnet 成本的 Anthropic beta 工具

    [:octicons-arrow-right-24: 閱讀筆記](advisor-tool.md)

</div>

[查看研究索引](news.md)
