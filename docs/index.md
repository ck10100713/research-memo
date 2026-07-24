# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">211</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-07-24</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    24 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    74 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    43 篇筆記

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

    20 篇筆記

    [:octicons-arrow-right-24: 前往](topics/learning.md)

</div>

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

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

-   :material-school:{{ .lg .middle }} **ML Intern**

    ---

    `2026-07-06` Hugging Face 官方開源的自主 ML 工程師 agent：讀論文、訓練模型、上架模型，GPQA 表現超越 Claude Code

    [:octicons-arrow-right-24: 閱讀筆記](ml-intern.md)

-   :material-finance:{{ .lg .middle }} **Claude for Financial Services**

    ---

    `2026-07-06` Anthropic 官方金融方案：10 個 Named Agents + 7 大 vertical plugins、55 Skills、12 MCP 資料源，Cowork 與 Managed Agents API 雙軌部署

    [:octicons-arrow-right-24: 閱讀筆記](claude-financial-services-plugins.md)

-   :material-content-cut:{{ .lg .middle }} **Ponytail**

    ---

    `2026-06-17` 把『最懶的資深工程師』裝進 AI agent 的跨平台 ruleset：寫程式前先過六層 YAGNI 篩子，少寫 80-94% 程式碼

    [:octicons-arrow-right-24: 閱讀筆記](ponytail.md)

-   :material-message-processing-outline:{{ .lg .middle }} **LINE Chatbot Boilerplate**

    ---

    `2026-06-12` 用 decorator 註冊指令、Redis 存對話狀態的早期 LINE chatbot Python boilerplate（Wit.ai NLU、Yeoman 產生器）

    [:octicons-arrow-right-24: 閱讀筆記](line-chatbot-boilerplate.md)

-   :material-view-grid-outline:{{ .lg .middle }} **LINE Rich Menus Manager**

    ---

    `2026-06-12` 用滑鼠拖拉就能建/管 LINE Rich Menu 的本機 GUI 工具（Angular + Express，npm 一鍵啟動）

    [:octicons-arrow-right-24: 閱讀筆記](line-richmenus-manager.md)

-   :material-palette-swatch:{{ .lg .middle }} **Open Design**

    ---

    `2026-06-11` 本地優先、開源的 Claude Design 替代品：原生桌面 app，不自帶 agent——用你 PATH 上既有的 Claude Code/Codex/Cursor 等 21 種 CLI 當設計引擎，讀 DESIGN.md 品牌契約串出網頁/簡報/圖/影片，支援 HTML/PDF/PPTX/MP4 匯出，Apache-2.0，兩週衝破 6 萬星

    [:octicons-arrow-right-24: 閱讀筆記](open-design.md)

</div>

[查看研究索引](news.md)
