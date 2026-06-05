# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

<div class="stats-bar">
  <div class="stat"><div class="stat-num">191</div><div class="stat-label">研究筆記</div></div>
  <div class="stat"><div class="stat-num">11</div><div class="stat-label">主題分類</div></div>
  <div class="stat"><div class="stat-num">2026-06-05</div><div class="stat-label">最近更新</div></div>
</div>

## 分類導覽

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **AI Agent 框架**

    ---

    23 篇筆記

    [:octicons-arrow-right-24: 前往](topics/agent-frameworks.md)

-   :material-code-tags:{{ .lg .middle }} **Coding Agent 工具**

    ---

    65 篇筆記

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

    3 篇筆記

    [:octicons-arrow-right-24: 前往](topics/ai-creative.md)

-   :material-apps:{{ .lg .middle }} **AI 應用**

    ---

    16 篇筆記

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

    12 篇筆記

    [:octicons-arrow-right-24: 前往](topics/dev-tools.md)

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

-   :material-tune-variant:{{ .lg .middle }} **SkillOpt**

    ---

    `2026-06-05` Microsoft「文字空間優化器」：像訓練神經網路（epoch/batch/learning rate/validation gate）一樣訓練凍結 LLM agent 的自然語言技能，不動權重、產出可部署的 best_skill.md；52/52 評測格全勝，GPT-5.5 對 no-skill baseline +23.5 分，v0.1.0 已上 PyPI，arXiv:2605.23904

    [:octicons-arrow-right-24: 閱讀筆記](skillopt.md)

-   :material-sitemap:{{ .lg .middle }} **The System Design Primer**

    ---

    `2026-06-05` GitHub 35 萬星的系統設計入門聖經：可擴展系統原理 + 面試題解 + Anki 卡片

    [:octicons-arrow-right-24: 閱讀筆記](system-design-primer.md)

-   :material-server-network:{{ .lg .middle }} **HighScalability.com**

    ---

    `2026-06-05` 經營 17 年的大規模系統架構案例庫，2024 年由 ByteByteGo 收購接手

    [:octicons-arrow-right-24: 閱讀筆記](highscalability.md)

-   :material-microsoft-windows:{{ .lg .middle }} **Microsoft PowerToys**

    ---

    `2026-06-05` 微軟官方開源的 Windows 強化工具集：30+ 個生產力小工具，從 FancyZones 到 AI 剪貼簿

    [:octicons-arrow-right-24: 閱讀筆記](powertoys.md)

-   :material-speedometer:{{ .lg .middle }} **Codex Complexity Optimizer**

    ---

    `2026-06-01` Codex skill：掃描 codebase 複雜度熱點、產生「只報告不亂改」的安全優化報告

    [:octicons-arrow-right-24: 閱讀筆記](codex-complexity-optimizer.md)

-   :material-shaker-outline:{{ .lg .middle }} **Awesome OpenClaw Skills**

    ---

    `2026-05-29` VoltAgent 策展的 OpenClaw skill 精選清單（49.5k stars），從 ClawHub 官方 13,729 個社群 skill 中過濾出 5,211 個分 31 類，標註 spam/duplicate/低品質/crypto/惡意各排除多少，附 VirusTotal/Snyk 等安全工具，可看作「OpenClaw 生態的 App Store 看板」

    [:octicons-arrow-right-24: 閱讀筆記](awesome-openclaw-skills.md)

-   :material-trending-up:{{ .lg .middle }} **Trend Monitor**

    ---

    `2026-05-29` dongzhang84 個人專案，每日自動聚合 6 個 AI/科技趨勢來源（Product Hunt/Toolify/TAAFT/Chrome ExtensionStore/GitHub Trending/HN），email + GitHub Pages dashboard 雙輸出，亮點是「Indie Opportunity Analysis」對每個產品做 4 維評分 + 前 5 名 8 題深度分析

    [:octicons-arrow-right-24: 閱讀筆記](trend-monitor.md)

-   :material-school-outline:{{ .lg .middle }} **skillopt-qa**

    ---

    `2026-05-28` joshhu 對 Microsoft SkillOpt 的精簡忠實重現版，針對 HotpotQA 多跳問答，用 ~9 個檔案講清「文字空間優化器」全貌，含真實 Qwen3.6-27B 實驗結果（種子→優化 test F1 0.8424→0.8524），離線測試零網路

    [:octicons-arrow-right-24: 閱讀筆記](skillopt-qa.md)

-   :material-apps:{{ .lg .middle }} **Awesome Free Apps**

    ---

    `2026-05-27` Axorax 維護的跨平台免費軟體 curated list（5.4k stars），涵蓋瀏覽器/音訊/開發/影音/安全等數十類別，每條附 Windows/macOS/Linux/開源/推薦 圖示標記，另有獨立 MOBILE.md 與多種 filter 視圖

    [:octicons-arrow-right-24: 閱讀筆記](awesome-free-apps.md)

-   :material-web:{{ .lg .middle }} **Webwright**

    ---

    `2026-05-27` Microsoft Research 極簡瀏覽器 agent 框架（~1.5k LoC），核心理念『coding agent + terminal』把瀏覽器當可拋棄環境、用 code-as-action 寫 Playwright 腳本，Online-Mind2Web 86.7% SOTA，可當 Claude Code/Codex skill

    [:octicons-arrow-right-24: 閱讀筆記](webwright.md)

-   :material-brain:{{ .lg .middle }} **Claude-Mem**

    ---

    `2026-05-27` thedotmack 的跨 session 持久記憶系統（78k stars），自動捕捉 agent 行為→AI 壓縮成語義摘要→注入未來 session，3-layer 漸進揭露搜尋省 ~10x token，SQLite+Chroma 混合檢索，支援 Claude Code/OpenClaw/Codex/Gemini 等多 host

    [:octicons-arrow-right-24: 閱讀筆記](claude-mem.md)

-   :material-briefcase-variant:{{ .lg .middle }} **Knowledge Work Plugins**

    ---

    `2026-05-27` Anthropic 官方開源的知識工作者 plugin 市集，為 Claude Cowork/Code 而生：~10 個職能 plugin（sales/finance/legal/data...）+ 數十個 partner-built，純 markdown+JSON 封裝 skills/commands/connectors，把 Claude 變成「你公司專屬的角色專家」

    [:octicons-arrow-right-24: 閱讀筆記](knowledge-work-plugins.md)

-   :material-gamepad-variant:{{ .lg .middle }} **Claude Code Game Studios**

    ---

    `2026-05-26` Donchitos 將 Claude Code 改造成完整遊戲開發工作室：49 agents + 73 skills + 12 hooks + 11 rules，鏡像真實 studio 三層階層（Director/Lead/Specialist）

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-game-studios.md)

-   :material-notebook-multiple:{{ .lg .middle }} **notebooklm-py**

    ---

    `2026-05-25` teng-lin 非官方 NotebookLM Python API + agentic skill，15k stars/4.5 個月，CLI/Python/Claude Code/Codex/OpenClaw 三入口，能解鎖 web UI 沒有的批次下載/PPTX/JSON 心智圖等隱藏能力

    [:octicons-arrow-right-24: 閱讀筆記](notebooklm-py.md)

-   :material-translate:{{ .lg .middle }} **軟體工程 56 大定律（完整中文版）**

    ---

    `2026-05-25` 56 條軟體工程定律完整中文版，每條附背景、實例、應用建議，搭配 laws-of-software-engineering.md 原版作為中文受眾學習資源

    [:octicons-arrow-right-24: 閱讀筆記](laws-of-software-engineering-zh.md)

-   :material-book-open-variant:{{ .lg .middle }} **Laws of Software Engineering**

    ---

    `2026-05-25` Dr. Milan Milanović 整理的 56 條軟體工程定律參考站，分七大類（團隊/規劃/架構/品質/設計/規模/決策），含書、海報、JSON API、50k 訂閱電子報，已成 Amazon 暢銷書

    [:octicons-arrow-right-24: 閱讀筆記](laws-of-software-engineering.md)

-   :material-console-line:{{ .lg .middle }} **OpenCode (anomalyco/opencode)**

    ---

    `2026-05-22` Anomaly (前 SST 團隊) 開源 AI coding agent，163k stars/19k forks，TUI 為主、支援 75+ LLM provider、MCP、桌面 App、GitHub Action、SDK，與 Claude Code 同級的多 provider 替代品

    [:octicons-arrow-right-24: 閱讀筆記](opencode.md)

</div>

[查看研究索引](news.md)
