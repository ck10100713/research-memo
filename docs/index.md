# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">205</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">12</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-07-20</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    24 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    70 篇筆記

    [:octicons-arrow-right-24: 前往](topics/coding-agent-tools.md)

-   :material-chart-line:{{ .lg .middle }} **量化交易**

    ---

    42 篇筆記

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

    13 篇筆記

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

-   :material-movie-open-play-outline:{{ .lg .middle }} **video-autopilot-kit**

    ---

    `2026-07-20` 填問卷變成你的系統 — YouTube/短影音自動化框架，ffmpeg pipeline + CapCut 自動化，零私人數據

    [:octicons-arrow-right-24: 閱讀筆記](video-autopilot-kit.md)

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

-   :material-account-voice:{{ .lg .middle }} **AI 虛擬人 Widget（ai-avatar-bot）**

    ---

    `2026-06-11` 一行 <script> 嵌入任何網站的右下角 Live2D 語音 AI 虛擬人 widget：皮（角色模型）／肉（引擎）／內容（知識庫）三分離，預設純前端、零後端、零金鑰，語音用瀏覽器內建、可選配神經語音

    [:octicons-arrow-right-24: 閱讀筆記](ai-avatar-bot.md)

-   :material-shield-check-outline:{{ .lg .middle }} **soplint**

    ---

    `2026-06-11` 為 AI agent 的「紀律」而非「程式碼」設計的 linter：用外部 belief-revision 稽核日誌、每日 CI discipline checks、PreToolUse AST gate 三機制，檢查 agent 是否真的遵守了你跟它定下的工作協議——把一年真實事故沉澱成可每日跑的回歸測試，PowerShell 零依賴

    [:octicons-arrow-right-24: 閱讀筆記](soplint.md)

-   :material-bullhorn-outline:{{ .lg .middle }} **social-post**

    ---

    `2026-06-11` 駱君昊（Hao）的 Claude Code skill：學使用者 FB 語氣 → 排 14 天內容日曆 → 透過 Claude in Chrome MCP 自動發到 FB/IG/Threads/X；內建「發佈前必打『確認』」硬安全閘，首發即 72K 觸及的實證 viral 框架（v1.0.1：R1-R35 規則 + F1-F27 公式 + 4 種 Mode）

    [:octicons-arrow-right-24: 閱讀筆記](skill-social-post.md)

-   :material-book-arrow-right-outline:{{ .lg .middle }} **book-to-skill（書轉 Skill 產生器）**

    ---

    `2026-06-08` 把任何技術書/文件（PDF、EPUB、DOCX…）轉成結構化 Claude Code skill，隨用隨查

    [:octicons-arrow-right-24: 閱讀筆記](skill-book-to-skill.md)

-   :material-tune-variant:{{ .lg .middle }} **SkillOpt**

    ---

    `2026-06-05` Microsoft「文字空間優化器」：像訓練神經網路（epoch/batch/learning rate/validation gate）一樣訓練凍結 LLM agent 的自然語言技能，不動權重、產出可部署的 best_skill.md；52/52 評測格全勝，GPT-5.5 對 no-skill baseline +23.5 分，v0.1.0 已上 PyPI，arXiv:2605.23904

    [:octicons-arrow-right-24: 閱讀筆記](skillopt.md)

-   :material-sitemap:{{ .lg .middle }} **The System Design Primer**

    ---

    `2026-06-05` GitHub 35 萬星的系統設計入門聖經：可擴展系統原理 + 面試題解 + Anki 卡片

    [:octicons-arrow-right-24: 閱讀筆記](system-design-primer.md)

</div>

[查看研究索引](news.md)
