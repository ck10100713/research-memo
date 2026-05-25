# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-notebook-multiple:{{ .lg .middle }} **notebooklm-py**

    ---

    `2026-05-25` teng-lin 非官方 NotebookLM Python API + agentic skill，15k stars/4.5 個月，CLI/Python/Claude Code/Codex/OpenClaw 三入口，能解鎖 web UI 沒有的批次下載/PPTX/JSON 心智圖等隱藏能力

    [:octicons-arrow-right-24: 閱讀筆記](notebooklm-py.md)

-   :material-book-open-variant:{{ .lg .middle }} **Laws of Software Engineering**

    ---

    `2026-05-25` Dr. Milan Milanović 整理的 56 條軟體工程定律參考站，分七大類（團隊/規劃/架構/品質/設計/規模/決策），含書、海報、JSON API、50k 訂閱電子報，已成 Amazon 暢銷書

    [:octicons-arrow-right-24: 閱讀筆記](laws-of-software-engineering.md)

-   :material-console-line:{{ .lg .middle }} **OpenCode (anomalyco/opencode)**

    ---

    `2026-05-22` Anomaly (前 SST 團隊) 開源 AI coding agent，163k stars/19k forks，TUI 為主、支援 75+ LLM provider、MCP、桌面 App、GitHub Action、SDK，與 Claude Code 同級的多 provider 替代品

    [:octicons-arrow-right-24: 閱讀筆記](opencode.md)

-   :material-router-network:{{ .lg .middle }} **LiteLLM**

    ---

    `2026-05-20` BerriAI 開源 AI Gateway，把 100+ LLM provider 統一成 OpenAI 格式 + virtual keys + cost tracking + guardrails，YC W23，被 Stripe/Netflix/OpenAI Agents SDK 採用，47k stars

    [:octicons-arrow-right-24: 閱讀筆記](litellm.md)

-   :material-account-heart:{{ .lg .middle }} **OpenHuman**

    ---

    `2026-05-19` tinyhumansai 的個人 AI 桌面助理，Rust+Tauri 桌面 mascot 會說話/開會、118+ OAuth 整合 20 分鐘自動 fetch、Memory Tree + Obsidian Wiki 在地持久記憶

    [:octicons-arrow-right-24: 閱讀筆記](openhuman.md)

-   :material-counter:{{ .lg .middle }} **usage (aqua5230)**

    ---

    `2026-05-19` aqua5230 隱私優先 macOS menu bar 用量追蹤器，把 Claude Code + Codex 5h/7d/今日 token 釘在右上角，零 API 呼叫純讀本機檔，台灣版專屬面板

    [:octicons-arrow-right-24: 閱讀筆記](aqua-usage-menubar.md)

-   :material-finance:{{ .lg .middle }} **Daily Stock Analysis**

    ---

    `2026-05-19` ZhuLinsen 用 GitHub Actions 跑零成本 A/H/美股 LLM 智能分析，37k stars、多 LLM + 多新聞源 + 多通知頻道、15 內建策略 + Agent 問股，工作日 18:00 自動推「決策仪表盘」

    [:octicons-arrow-right-24: 閱讀筆記](daily-stock-analysis.md)

-   :material-shield-check:{{ .lg .middle }} **Tech Leads Club Agent Skills**

    ---

    `2026-05-19` Tech Leads Club 安全驗證過的 Skill registry，CLI + MCP 雙入口，主打「13% 市集 Skill 有重大漏洞、我們不一樣」，跨 19 個 AI coding agent，4.2k stars

    [:octicons-arrow-right-24: 閱讀筆記](tlc-agent-skills.md)

-   :material-server-network:{{ .lg .middle }} **QuantDinger**

    ---

    `2026-05-19` brokermr810 自架式 AI 量化交易作業系統，一個 Docker Compose 串聯 AI 研究/Python 策略/回測/實盤(crypto+IBKR+MT5+Alpaca)，Agent Gateway + MCP，內建 USDT 計費可變 SaaS

    [:octicons-arrow-right-24: 閱讀筆記](quantdinger.md)

-   :material-console-line:{{ .lg .middle }} **CLI-Anything**

    ---

    `2026-05-19` HKUDS 把任何 GUI 軟體用 7 步驟 pipeline 自動產出 agent-friendly CLI harness，60+ 軟體覆蓋，CLI-Hub 一鍵安裝，36k stars / 2 個月

    [:octicons-arrow-right-24: 閱讀筆記](cli-anything.md)

-   :material-account-tie:{{ .lg .middle }} **mattpocock/skills**

    ---

    `2026-05-15` Matt Pocock (Total TypeScript) 把每天用的 Claude Skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnose / improve-codebase-architecture，3 個月 90k stars

    [:octicons-arrow-right-24: 閱讀筆記](mattpocock-skills.md)

-   :material-chart-multiple:{{ .lg .middle }} **Fincept Terminal**

    ---

    `2026-05-15` Fincept Corp 開源 Bloomberg-style 金融終端，C++20 + Qt6 + 嵌入式 Python，37 AI agents（巴菲特/葛拉漢/林區...）、100+ 資料源、16 券商整合，21k stars / AGPL-3.0

    [:octicons-arrow-right-24: 閱讀筆記](fincept-terminal.md)

-   :material-clipboard-list:{{ .lg .middle }} **Claude Code 最佳實踐完整研究報告（zeuikli）**

    ---

    `2026-05-15` zeuikli 整理 29 篇 best-practices + 52 篇 Claude blog 的 Claude Code 九面向最佳實踐總報告，含 CLAUDE.md、Hook、Cache、Subagent、Skill、MCP、安全、Routines、成本工程

    [:octicons-arrow-right-24: 閱讀筆記](zeuikli-claude-code-best-practices.md)

-   :material-palette:{{ .lg .middle }} **Casper × Claude Code Skill 設計風格圖鑑**

    ---

    `2026-05-15` 卡斯伯（六角學院）用 25 設計風格 × 15 動畫模式做的 Claude Code Skill 示範作品集，主軸是「主執行緒寫 Skill → SubAgent 用 Skill 產單檔網頁」的規模化工作流

    [:octicons-arrow-right-24: 閱讀筆記](casper-claude-skill-design-gallery.md)

-   :material-file-search:{{ .lg .middle }} **RAG-Anything**

    ---

    `2026-05-14` HKUDS All-in-One Multimodal RAG 框架，以 LightRAG 為核心 + MinerU 解析，支援 PDF/Office/影像/公式/表格與 multimodal knowledge graph

    [:octicons-arrow-right-24: 閱讀筆記](rag-anything.md)

-   :material-chat-question:{{ .lg .middle }} **LINE Bot Multimodal RAG (kkdai)**

    ---

    `2026-05-14` kkdai 的 LINE Bot + Gemini File Search API 多模態 RAG 範例，靠 metadata_filter 在單一 store 做多租戶隔離、Cloud Run 部署

    [:octicons-arrow-right-24: 閱讀筆記](linebot-multimodal-rag.md)

-   :material-school:{{ .lg .middle }} **AI Agents for Beginners**

    ---

    `2026-05-14` Microsoft 官方 12 (+6) 課 AI Agent 入門課，以 Microsoft Agent Framework + Azure AI Foundry V2 為主軸，61k stars、50+ 語言

    [:octicons-arrow-right-24: 閱讀筆記](ai-agents-for-beginners.md)

</div>

[查看研究索引](news.md)

---

## AI Agent 框架

<div class="grid cards" markdown>

-   :material-file-document-outline:{{ .lg .middle }} **Agent GoFundMe**

    ---

    Agent 群眾募資平台 — AI Agent 的 GoFundMe

    [:octicons-arrow-right-24: 閱讀筆記](agent-gofundme.md)

-   :material-compare-horizontal:{{ .lg .middle }} **開源 AI Agent 框架比較**

    ---

    2026 年功能完善的開源 Agent 框架橫向比較：從 Dify 到 LangGraph 的選型指南

    [:octicons-arrow-right-24: 閱讀筆記](open-source-agent-frameworks.md)

-   :material-file-document-outline:{{ .lg .middle }} **AgentBnB**

    ---

    Agent 短租市場 — AI Agent 的 Airbnb 託管協議

    [:octicons-arrow-right-24: 閱讀筆記](agentbnb.md)

-   :material-flask:{{ .lg .middle }} **Autoresearch**

    ---

    Karpathy 的自主 AI 研究代理，讓 Agent 整夜跑 LLM 實驗

    [:octicons-arrow-right-24: 閱讀筆記](autoresearch.md)

-   :material-brain:{{ .lg .middle }} **AutoGPT**

    ---

    自主 AI Agent 先驅專案

    [:octicons-arrow-right-24: 閱讀筆記](autogpt.md)

-   :material-account-group:{{ .lg .middle }} **CrewAI**

    ---

    多 Agent 角色扮演協作框架

    [:octicons-arrow-right-24: 閱讀筆記](crewai.md)

-   :material-google:{{ .lg .middle }} **Google Agent Development Kit (ADK)**

    ---

    Google 官方 Agent 框架 — 以 LlmAgent + Workflow Agents 為核心的 code-first 多代理開發套件

    [:octicons-arrow-right-24: 閱讀筆記](google-adk.md)

-   :material-robot-industrial:{{ .lg .middle }} **OpenAI Agents SDK**

    ---

    OpenAI 官方 Agent 框架 — 以 Handoffs + Guardrails 為核心的輕量多代理工作流系統

    [:octicons-arrow-right-24: 閱讀筆記](openai-agents-sdk.md)

-   :material-file-document-outline:{{ .lg .middle }} **DeerFlow**

    ---

    ByteDance 開源多 Agent 深度研究框架

    [:octicons-arrow-right-24: 閱讀筆記](deer-flow.md)

-   :material-account-group-outline:{{ .lg .middle }} **LangGraph Multi-Agent Research Assistant**

    ---

    LangGraph Supervisor 模式教學範例——Researcher/Writer/Reviewer 三 Agent 研究助理，附 human-in-the-loop

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-multi-agent.md)

-   :material-account-supervisor:{{ .lg .middle }} **LangGraph Supervisor**

    ---

    LangGraph 官方 Supervisor 多 Agent 庫——中央調度器模式，支援多層階層與訊息歷史控制（1.5K stars）

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-supervisor-py.md)

-   :material-swap-horizontal-circle:{{ .lg .middle }} **LangGraph Swarm**

    ---

    LangGraph 官方 Swarm 多 Agent 庫——去中心化 handoff 模式，agent 間直接交接，延遲低 40%（1.4K stars）

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-swarm-py.md)

-   :material-link-variant:{{ .lg .middle }} **LangChain**

    ---

    LLM 應用開發框架

    [:octicons-arrow-right-24: 閱讀筆記](langchain.md)

-   :material-state-machine:{{ .lg .middle }} **LangGraph State API**

    ---

    LangGraph 圖狀態機核心 API：State、Reducer、Channel、MessagesState 完整解析

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-state-api.md)

-   :material-hub:{{ .lg .middle }} **LobeHub**

    ---

    74K stars 的 AI Agent 協作平台，Supervisor + Executor 多 Agent 架構、39K+ MCP 市集、White-Box Memory

    [:octicons-arrow-right-24: 閱讀筆記](lobehub.md)

-   :material-fishbowl:{{ .lg .middle }} **MiroFish**

    ---

    40K stars 群體智能預測引擎，用數千 AI Agent 模擬平行社會推演未來

    [:octicons-arrow-right-24: 閱讀筆記](mirofish.md)

-   :material-file-document-outline:{{ .lg .middle }} **OpenClaw（龍蝦）**

    ---

    開源 AI Agent 框架 — 支援本地 LLM 的 Claude Code 替代品

    [:octicons-arrow-right-24: 閱讀筆記](openclaw.md)

-   :material-cursor-default-click:{{ .lg .middle }} **Page Agent**

    ---

    阿里巴巴的網頁內嵌 GUI Agent，用自然語言控制網頁介面

    [:octicons-arrow-right-24: 閱讀筆記](page-agent.md)

-   :material-office-building:{{ .lg .middle }} **Paperclip**

    ---

    開源 AI Agent 編排控制平面，把多個 Agent 組織成一間零人公司

    [:octicons-arrow-right-24: 閱讀筆記](paperclip.md)

-   :material-robot-outline:{{ .lg .middle }} **Project Golem**

    ---

    Browser-in-the-Loop 自主 AI 代理，金字塔記憶可存 50 年對話精華

    [:octicons-arrow-right-24: 閱讀筆記](project-golem.md)

-   :material-forum:{{ .lg .middle }} **多 Agent 辯論會系統**

    ---

    使用 Copilot SDK 建構的多 Agent 辯論系統

    [:octicons-arrow-right-24: 閱讀筆記](multi-agent-debate.md)

</div>

---

## Coding Agent 工具

<div class="grid cards" markdown>

-   :material-memory:{{ .lg .middle }} **abdixere-api**

    ---

    Saki-tw 的極簡 MCP API base，主張 Agent context memory 應該在工具層下放給 Agent 自己，不要靠多餘保護

    [:octicons-arrow-right-24: 閱讀筆記](abdixere-api.md)

-   :material-file-search-outline:{{ .lg .middle }} **Analysis Claude Code**

    ---

    Claude Code v1.0.33 靜態逆向工程——50,000 行混淆碼拆解為 102 chunks，揭示 h2A 消息隊列、6 層權限驗證、92% 閾值上下文壓縮

    [:octicons-arrow-right-24: 閱讀筆記](analysis-claude-code.md)

-   :material-palette-swatch:{{ .lg .middle }} **Awesome DESIGN.md — AI Agent 的設計系統資料庫**

    ---

    58+ 個知名品牌 DESIGN.md 合集 — 丟進專案讓 AI Agent 產出 pixel-perfect UI

    [:octicons-arrow-right-24: 閱讀筆記](awesome-design-md.md)

-   :material-console:{{ .lg .middle }} **Better Agent Terminal**

    ---

    tony1223 出品的跨平台 Electron 終端機聚合器，內建 Claude Code Agent 面板、cache 成本追蹤、worktree 隔離與 WebSocket 遠端控制，4 個月累積 339 stars

    [:octicons-arrow-right-24: 閱讀筆記](better-agent-terminal.md)

-   :material-airplane-takeoff:{{ .lg .middle }} **App Store Preflight Skills**

    ---

    AI Agent Skill，提交前自動掃描 iOS/macOS 專案的 App Store 審核風險

    [:octicons-arrow-right-24: 閱讀筆記](app-store-preflight.md)

-   :material-airplane-search:{{ .lg .middle }} **Browser-Bound MCP 機票查詢工具**

    ---

    四層架構拆解：Rust Bridge + Chrome Extension + Tailscale，讓 AI Agent 在真實瀏覽器查 Google Flights 機票

    [:octicons-arrow-right-24: 閱讀筆記](browser-bound-mcp-flights.md)

-   :material-cogs:{{ .lg .middle }} **Harness Design for Long-Running Apps**

    ---

    Anthropic 的 GAN 啟發三 Agent Harness 架構，讓 Claude 自主建構完整全端應用

    [:octicons-arrow-right-24: 閱讀筆記](harness-design-long-running-apps.md)

-   :material-ghost:{{ .lg .middle }} **claude-better**

    ---

    CryptoSwift 作者的多層諷刺——main branch 0 行程式碼配企業級 README，code branch 是 XOR 混淆的 C 假 CLI，永遠回覆 'Your account is blocked'

    [:octicons-arrow-right-24: 閱讀筆記](claude-better.md)

-   :material-file-document-outline:{{ .lg .middle }} **Claude Code Boris Cherny 57 Tips — 創辦人親授的進階工作流**

    ---

    Boris Cherny 57 個 Claude Code 進階工作流技巧

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-boris-cherny-tips.md)

-   :material-brain:{{ .lg .middle }} **Boris Cherny × Claude Opus 4.7 — 發表當天的使用心得與 6 個新技巧**

    ---

    Claude Code 創辦人 Boris Cherny 在 Opus 4.7 發表當天公開的 6 個生產力技巧與行為差異全解析

    [:octicons-arrow-right-24: 閱讀筆記](boris-cherny-opus-4-7.md)

-   :material-claw:{{ .lg .middle }} **Claw Code**

    ---

    Claude Code 洩漏事件後的 clean-room Python/Rust 重寫，harness 工程研究標竿

    [:octicons-arrow-right-24: 閱讀筆記](claw-code.md)

-   :material-graph:{{ .lg .middle }} **Code Review Graph**

    ---

    本地程式碼知識圖譜 — Tree-sitter 解析 AST，MCP 提供 blast-radius 最小檔案集，省 8.2x token

    [:octicons-arrow-right-24: 閱讀筆記](code-review-graph.md)

-   :material-magnify-scan:{{ .lg .middle }} **Kuberwastaken Claude Code**

    ---

    Claude Code 洩漏源碼深度拆解 + clean-room Rust 重寫，揭露 BUDDY/KAIROS/Dream 等未公開系統

    [:octicons-arrow-right-24: 閱讀筆記](kuberwastaken-claude-code.md)

-   :material-source-branch:{{ .lg .middle }} **xorespesp Claude Code**

    ---

    Claude Code 洩漏原始碼的可運行 TypeScript 復原版，含 shims 替代 native modules

    [:octicons-arrow-right-24: 閱讀筆記](xorespesp-claude-code.md)

-   :material-magnify-scan:{{ .lg .middle }} **Claude Code Reverse Engineering**

    ---

    2.3K stars 的 Claude Code 逆向工程——v2 基於 Runtime Monkey Patch 攔截 API 請求，附帶 Log 視覺化工具和完整 Prompt 解碼

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-reverse.md)

-   :material-robot-outline:{{ .lg .middle }} **Claude Agent SDK**

    ---

    Anthropic 官方 Agent SDK — 把 Claude Code 的工具與 Agent Loop 變成可程式化的 Python / TypeScript 函式庫

    [:octicons-arrow-right-24: 閱讀筆記](claude-agent-sdk.md)

-   :material-code-braces-box:{{ .lg .middle }} **cloclo (claude-code-sdk)**

    ---

    單檔 18,500 行的多 Provider Claude Code 替代品——13 個 LLM 後端 + Ink TUI + NDJSON Bridge + Skills Marketplace，npm 安裝即用

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-sdk.md)

-   :material-pencil-ruler:{{ .lg .middle }} **Claude Design 系統提示詞**

    ---

    Anthropic 新推出的「設計專用 Claude」完整中文系統提示詞 — 用 HTML 做設計交付，具備 Tweaks、Starter Components、Verifier 與反 AI slop 的完整工程骨架

    [:octicons-arrow-right-24: 閱讀筆記](claude-design.md)

-   :material-finance:{{ .lg .middle }} **Claude Financial Services Plugins**

    ---

    Anthropic 官方金融服務 Plugin：41 Skills、11 MCP 資料源，覆蓋投行/股研/PE/財管端到端工作流

    [:octicons-arrow-right-24: 閱讀筆記](claude-financial-services-plugins.md)

-   :material-account-multiple:{{ .lg .middle }} **The Agency: AI Specialists**

    ---

    144 個專業化 AI Agent 人格庫，橫跨 12 部門，支援 10 個 AI 工具

    [:octicons-arrow-right-24: 閱讀筆記](agency-agents.md)

-   :material-shield-check:{{ .lg .middle }} **andrej-karpathy-skills**

    ---

    Karpathy 的 LLM 編程痛點轉化為一份 CLAUDE.md — 四大原則讓 AI 少犯愚蠢錯誤，44K stars

    [:octicons-arrow-right-24: 閱讀筆記](andrej-karpathy-skills.md)

-   :material-bookshelf:{{ .lg .middle }} **Asgard Skills**

    ---

    263 個 Coding Agent Skills 知識庫 — 從研究所理論、演算法到台灣在地知識，附 20 支確定性計算腳本

    [:octicons-arrow-right-24: 閱讀筆記](asgard-skills.md)

-   :material-file-compare:{{ .lg .middle }} **Difftastic**

    ---

    24.8K stars 的結構化 diff 工具，用 tree-sitter 解析語法樹，只顯示真正有意義的程式碼變動

    [:octicons-arrow-right-24: 閱讀筆記](difftastic.md)

-   :material-monitor-dashboard:{{ .lg .middle }} **Claude HUD**

    ---

    11.5K stars 的 Claude Code 狀態列 plugin，即時顯示 context 用量、工具活動、Agent 狀態

    [:octicons-arrow-right-24: 閱讀筆記](claude-hud.md)

-   :material-view-dashboard-variant:{{ .lg .middle }} **cc-statusline — Claude Code 的全能 statusline 儀表板**

    ---

    Claude Code 一眼看穿全貌的 statusline：quota 條、agent tracker、MCP 健康、全 session 成本聚合

    [:octicons-arrow-right-24: 閱讀筆記](cc-statusline.md)

-   :material-palette:{{ .lg .middle }} **Casper × Claude Code Skill 設計風格圖鑑**

    ---

    卡斯伯（六角學院）用 25 設計風格 × 15 動畫模式做的 Claude Code Skill 示範作品集，主軸是「主執行緒寫 Skill → SubAgent 用 Skill 產單檔網頁」的規模化工作流

    [:octicons-arrow-right-24: 閱讀筆記](casper-claude-skill-design-gallery.md)

-   :material-account-tie:{{ .lg .middle }} **mattpocock/skills**

    ---

    Matt Pocock (Total TypeScript) 把每天用的 Claude Skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnose / improve-codebase-architecture，3 個月 90k stars

    [:octicons-arrow-right-24: 閱讀筆記](mattpocock-skills.md)

-   :material-counter:{{ .lg .middle }} **usage (aqua5230)**

    ---

    aqua5230 隱私優先 macOS menu bar 用量追蹤器，把 Claude Code + Codex 5h/7d/今日 token 釘在右上角，零 API 呼叫純讀本機檔，台灣版專屬面板

    [:octicons-arrow-right-24: 閱讀筆記](aqua-usage-menubar.md)

-   :material-shield-check:{{ .lg .middle }} **Tech Leads Club Agent Skills**

    ---

    Tech Leads Club 安全驗證過的 Skill registry，CLI + MCP 雙入口，主打「13% 市集 Skill 有重大漏洞、我們不一樣」，跨 19 個 AI coding agent，4.2k stars

    [:octicons-arrow-right-24: 閱讀筆記](tlc-agent-skills.md)

-   :material-newspaper-variant-outline:{{ .lg .middle }} **Claude Cowork Dispatch**

    ---

    用手機遠端遙控桌面 Claude Cowork，離開電腦也能派任務

    [:octicons-arrow-right-24: 閱讀筆記](dispatch.md)

-   :material-palette-swatch:{{ .lg .middle }} **design-md-chrome**

    ---

    Chrome 擴充套件，一鍵擷取任意網站設計系統生成 DESIGN.md / SKILL.md，7 天 756 stars，TypeUI 生態系的瀏覽器前端

    [:octicons-arrow-right-24: 閱讀筆記](design-md-chrome.md)

-   :material-dna:{{ .lg .middle }} **dot-skill**

    ---

    上海 AI Lab × titanwings 出品，從 colleague.skill 升級的通用人物蒸餾器 — 21 天衝 15.5K stars，三家族 × 四宿主把任何人變 AI Skill

    [:octicons-arrow-right-24: 閱讀筆記](dot-skill.md)

-   :material-package-variant-closed:{{ .lg .middle }} **Everything Claude Code**

    ---

    97K stars 的 Agent Harness 效能優化系統：28 agents、116 skills、59 commands

    [:octicons-arrow-right-24: 閱讀筆記](everything-claude-code.md)

-   :material-star-shooting:{{ .lg .middle }} **Claude Code Showcase**

    ---

    Claude Code 使用案例展示

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-showcase.md)

-   :material-book-open-variant:{{ .lg .middle }} **Context Hub — Coding Agent 的策展 API 文件中心**

    ---

    Andrew Ng 開源 CLI — 讓 Coding Agent 取得最新 API 文件，不再幻覺

    [:octicons-arrow-right-24: 閱讀筆記](context-hub.md)

-   :material-puzzle:{{ .lg .middle }} **The Complete Guide to Building Skills for Claude —**

    ---

    Claude Skills 建構完整指南

    [:octicons-arrow-right-24: 閱讀筆記](claude-skills-guide.md)

-   :material-toolbox:{{ .lg .middle }} **KC AI Skills — 真的會做事的 AI Skill 合集**

    ---

    12 個實戰型 Claude Code Skills — 從 repo 安全掃描到反指標分析，解決真實問題的 skill 合集

    [:octicons-arrow-right-24: 閱讀筆記](kc-ai-skills.md)

-   :material-account-voice:{{ .lg .middle }} **khazix-skills**

    ---

    数字生命卡兹克開源個人 AI 方法論 — 14 天 5.4K stars，1 個 Prompt + 2 個 Skill 把寫作風格與研究框架蒸餾成可執行指令集

    [:octicons-arrow-right-24: 閱讀筆記](khazix-skills.md)

-   :material-lightning-bolt:{{ .lg .middle }} **Lightpanda Browser**

    ---

    用 Zig 從零打造的 headless browser，比 Chrome 快 11x、省 9x 記憶體，專為 AI Agent 設計

    [:octicons-arrow-right-24: 閱讀筆記](lightpanda-browser.md)

-   :material-console:{{ .lg .middle }} **GitHub Copilot CLI**

    ---

    GitHub Copilot 命令列工具

    [:octicons-arrow-right-24: 閱讀筆記](copilot-cli.md)

-   :material-cog:{{ .lg .middle }} **GitHub Copilot Configs**

    ---

    GitHub Copilot 設定與自訂指令

    [:octicons-arrow-right-24: 閱讀筆記](github-copilot-configs.md)

-   :material-github:{{ .lg .middle }} **GitHub Copilot SDK**

    ---

    GitHub 官方 Agent SDK — 把 Copilot CLI 的 Agent 引擎以 JSON-RPC 暴露為可嵌入的多語言函式庫

    [:octicons-arrow-right-24: 閱讀筆記](github-copilot-sdk.md)

-   :material-refresh:{{ .lg .middle }} **Copilot Ralph**

    ---

    保哥的 Ralph 迭代式 AI 開發迴圈工具 — 基於 Copilot SDK，讓 AI 反覆執行任務直到完成

    [:octicons-arrow-right-24: 閱讀筆記](copilot-ralph.md)

-   :material-hammer-wrench:{{ .lg .middle }} **gstack**

    ---

    Garry Tan 的 Claude Code 工作流系統，40 天衝到 77.7K stars，v1.3 新增 taste engine、context save/restore、10 個 host 支援

    [:octicons-arrow-right-24: 閱讀筆記](gstack.md)

-   :material-source-branch:{{ .lg .middle }} **Agent Orchestrator**

    ---

    Composio 的多 agent 控制平面，為每個 issue 建立 worktree、branch、PR，並自動接住 CI 與 review feedback

    [:octicons-arrow-right-24: 閱讀筆記](agent-orchestrator.md)

-   :material-connection:{{ .lg .middle }} **MCP CLI**

    ---

    Model Context Protocol CLI 工具

    [:octicons-arrow-right-24: 閱讀筆記](mcp-cli.md)

-   :material-suitcase:{{ .lg .middle }} **MCPorter**

    ---

    MCP 萬用工具——TypeScript Runtime + CLI + Code-Gen，自動發現 IDE 設定、一行呼叫任何 MCP server（3.4K stars）

    [:octicons-arrow-right-24: 閱讀筆記](mcporter.md)

-   :material-account-group:{{ .lg .middle }} **Multica**

    ---

    開源 Managed Agents 平台，把 Coding Agent 當隊友管理 — 派工、追蹤、技能複用

    [:octicons-arrow-right-24: 閱讀筆記](multica.md)

-   :material-account-group:{{ .lg .middle }} **my-claude-devteam**

    ---

    台灣交大 NYCU-Chung 作品，把 Claude Code 變成 12 人工程團隊，9 天衝 218 stars 的 P7/P9/P10 企業職級方法論

    [:octicons-arrow-right-24: 閱讀筆記](my-claude-devteam.md)

-   :material-head-lightbulb:{{ .lg .middle }} **女娲.skill（nuwa-skill）**

    ---

    蒸餾任何人的思維方式 — 6 路並行調研 → 三重驗證 → 心智模型 + 決策啟發式 + 表達 DNA，11.8K stars

    [:octicons-arrow-right-24: 閱讀筆記](nuwa-skill.md)

-   :material-chat-processing:{{ .lg .middle }} **OpenAB — Open Agent Broker**

    ---

    Rust 開源 ACP Harness — 在 Discord 操控 Kiro/Claude/Codex/Gemini/Copilot Coding Agent

    [:octicons-arrow-right-24: 閱讀筆記](openab.md)

-   :material-console-line:{{ .lg .middle }} **OpenCode (anomalyco/opencode)**

    ---

    Anomaly (前 SST 團隊) 開源 AI coding agent，163k stars/19k forks，TUI 為主、支援 75+ LLM provider、MCP、桌面 App、GitHub Action、SDK，與 Claude Code 同級的多 provider 替代品

    [:octicons-arrow-right-24: 閱讀筆記](opencode.md)

-   :material-cog-outline:{{ .lg .middle }} **OpenHarness**

    ---

    香港大學開源 Agent Harness — 11,700 行 Python 重現 98% Claude Code 工具能力，支援多 LLM Provider

    [:octicons-arrow-right-24: 閱讀筆記](open-harness.md)

-   :material-code-braces-box:{{ .lg .middle }} **Open SWE**

    ---

    LangChain 開源的企業內部 Coding Agent 框架——複製 Stripe/Ramp/Coinbase 的內部架構（8.8K stars）

    [:octicons-arrow-right-24: 閱讀筆記](open-swe.md)

-   :material-swap-horizontal:{{ .lg .middle }} **OpenClaw Claude Proxy**

    ---

    將 Claude Max 訂閱轉為 OpenAI 相容 API，驅動 Agent 群免費用 Opus 4.6

    [:octicons-arrow-right-24: 閱讀筆記](openclaw-claude-proxy.md)

-   :material-book-check:{{ .lg .middle }} **Slavingia Skills — 書本即 Skill 的先驅實驗**

    ---

    Sahil Lavingia 將《The Minimalist Entrepreneur》轉為 10 個 Claude Code Skills

    [:octicons-arrow-right-24: 閱讀筆記](slavingia-skills.md)

-   :material-presentation:{{ .lg .middle }} **Claude Slide Editor**

    ---

    garyyang1001 打造的瀏覽器內 HTML 簡報編輯器，串 Claude Code / Codex CLI 做元件級 AI 改寫，把 Claude Design 後續迭代成本壓到零頭

    [:octicons-arrow-right-24: 閱讀筆記](slide-editor.md)

-   :material-shield-star:{{ .lg .middle }} **Superpowers**

    ---

    106K stars 的 agentic skills 框架，用心理學說服原則強制 coding agent 遵守開發紀律

    [:octicons-arrow-right-24: 閱讀筆記](superpowers.md)

-   :material-palette-outline:{{ .lg .middle }} **UI UX Pro Max Skill**

    ---

    54K stars 的 AI 設計智慧注入系統——161 條行業推理規則 + 67 種 UI 風格，讓 Coding Agent 寫出有品味的 UI

    [:octicons-arrow-right-24: 閱讀筆記](ui-ux-pro-max-skill.md)

-   :material-account-supervisor:{{ .lg .middle }} **wshobson/agents**

    ---

    77 個 Claude Code 插件 + 182 個 Agent + 149 個 Skill — 最大的開源 Claude Code 生態集合

    [:octicons-arrow-right-24: 閱讀筆記](wshobson-agents.md)

-   :material-brain:{{ .lg .middle }} **Why Your AI Is Dumbing Down**

    ---

    Saki-tw 的法醫式分析：AI IDE 透過 CHECKPOINT 截斷對話 + 隱形 system prompt 注入「DO NOT TAKE ACTION」，把你付費的 LLM 偷偷閹割省 token

    [:octicons-arrow-right-24: 閱讀筆記](why-your-ai-is-dumbing-down.md)

</div>

---

## 量化交易

<div class="grid cards" markdown>

-   :material-speedometer:{{ .lg .middle }} **On Accelerating Large-Scale Robust Portfolio Optimization**

    ---

    Hsieh × Lu 2024：把 distributionally robust portfolio 的求解時間從幾千秒壓到個位數秒，extended supporting hyperplane approximation 用在 S&P 500 全成分股

    [:octicons-arrow-right-24: 閱讀筆記](accelerating-robust-portfolio-optimization.md)

-   :material-stop-circle:{{ .lg .middle }} **Generalization of Affine Feedback Stock Trading Results to Include Stop-Loss Orders**

    ---

    Hsieh 2022 Automatica：把 affine feedback stock trading 結果擴張至含 stop-loss 訂單，GBM 下給出累積 P&L 的閉式 CDF，含 stop-loss 涵蓋無 stop 為特例

    [:octicons-arrow-right-24: 閱讀筆記](affine-feedback-stop-loss.md)

-   :material-bank:{{ .lg .middle }} **AI Hedge Fund**

    ---

    13 位傳奇投資人 + 6 個分析/管理 Agent 協同分析股票，LangGraph 驅動的多 Agent 對沖基金模擬系統，2026-04 衝到 57K stars 且新增 Nassim Taleb 黑天鵝 Agent

    [:octicons-arrow-right-24: 閱讀筆記](ai-hedge-fund.md)

-   :material-help-circle-outline:{{ .lg .middle }} **Asset Pricing Theory with Ambiguity（工作中 working paper）**

    ---

    Hsieh × Po-Hsuan Hsu 工作中：把 ambiguity（Knightian 不確定性）放進資產定價框架，預期接續作者整條 distributionally robust 路線推到 pricing 層級

    [:octicons-arrow-right-24: 閱讀筆記](asset-pricing-with-ambiguity.md)

-   :material-trending-up:{{ .lg .middle }} **On Asymptotic Log-Optimal Buy-and-Hold Strategy**

    ---

    Hsieh 2023 Automatica：證明只要存在 dominant asset，buy-and-hold 就是 asymptotically log-optimal，且 frequency-based 高頻再平衡無法超越被動持有

    [:octicons-arrow-right-24: 閱讀筆記](asymptotic-log-optimal-buy-hold.md)

-   :material-cash-multiple:{{ .lg .middle }} **On Cost-Sensitive Distributionally Robust Log-Optimal Portfolio**

    ---

    Hsieh × Yu 2024：用 Wasserstein ball 量化分布不確定性，加上一般凸交易成本模型，證明無成本時收斂等權重、有成本時資金往無風險資產偏移

    [:octicons-arrow-right-24: 閱讀筆記](cost-sensitive-distributionally-robust-portfolio.md)

-   :material-finance:{{ .lg .middle }} **Daily Stock Analysis**

    ---

    ZhuLinsen 用 GitHub Actions 跑零成本 A/H/美股 LLM 智能分析，37k stars、多 LLM + 多新聞源 + 多通知頻道、15 內建策略 + Agent 問股，工作日 18:00 自動推「決策仪表盘」

    [:octicons-arrow-right-24: 閱讀筆記](daily-stock-analysis.md)

-   :material-chart-line-variant:{{ .lg .middle }} **On Robustness of Double Linear Policy with Time-Varying Weights**

    ---

    Wang × Hsieh 2023 CDC：把 Double Linear Policy 從常數權重推廣到 time-varying 權重，用 elementary symmetric polynomials 證明 robust positive expectation，可接 moving average 訊號

    [:octicons-arrow-right-24: 閱讀筆記](dlp-time-varying-weights.md)

-   :material-cash-minus:{{ .lg .middle }} **On Robustness of Double Linear Trading with Transaction Costs**

    ---

    Hsieh 2022 L-CSS：DLP 加上交易成本後 robust positive expected gain 可能消失，本篇給出保留正期望的條件、用 GBM with jumps 模擬與 BTC-USD 回測驗證

    [:octicons-arrow-right-24: 閱讀筆記](dlp-with-transaction-costs.md)

-   :material-restart:{{ .lg .middle }} **On Data-Driven Drawdown Control with Restart Mechanism in Trading**

    ---

    Hsieh 2023 IFAC：drawdown modulation 觸發後不再像 stop-loss 那樣放棄，加 data-driven restart 自動重啟，含成本仍打敗原版且維持 max drawdown 上限

    [:octicons-arrow-right-24: 閱讀筆記](drawdown-control-restart-mechanism.md)

-   :material-shield-check:{{ .lg .middle }} **On Drawdown-Modulated Feedback Control in Stock Trading**

    ---

    Hsieh × Barmish 2017 IFAC：Drawdown Modulation Lemma 刻畫「以機率 1 維持 max drawdown 上限」的投資族，並在此族內最大化 Kelly ELG，給出 drawdown-constrained Kelly 的最佳投資

    [:octicons-arrow-right-24: 閱讀筆記](drawdown-modulated-stock-trading.md)

-   :material-timer-sand:{{ .lg .middle }} **The Impact of Execution Delay on Kelly-Based Stock Trading: High-Frequency Versus Buy and Hold**

    ---

    Hsieh × Barmish × Gubner 2019 CDC：證明無延遲時 high-frequency trading 嚴格優於 buy-and-hold，但執行延遲存在時 buy-and-hold 反過來勝出 — 即使零成本

    [:octicons-arrow-right-24: 閱讀筆記](execution-delay-kelly-trading.md)

-   :material-chart-multiple:{{ .lg .middle }} **Fincept Terminal**

    ---

    Fincept Corp 開源 Bloomberg-style 金融終端，C++20 + Qt6 + 嵌入式 Python，37 AI agents（巴菲特/葛拉漢/林區...）、100+ 資料源、16 券商整合，21k stars / AGPL-3.0

    [:octicons-arrow-right-24: 閱讀筆記](fincept-terminal.md)

-   :material-function-variant:{{ .lg .middle }} **On Feedback Control in Kelly Betting: An Approximation Approach**

    ---

    Hsieh 2020 CCTA：Kelly betting 用 Taylor 近似化為 quadratic programming，得到閉式近似解，並分析績效、變異數、survivability 等性質

    [:octicons-arrow-right-24: 閱讀筆記](feedback-control-kelly-betting-approximation.md)

-   :material-format-list-checks:{{ .lg .middle }} **Necessary and Sufficient Conditions for Frequency-Based Kelly Optimal Portfolio**

    ---

    Hsieh 2021 L-CSS：給出 frequency-based Kelly 最佳組合的充分必要條件、Extended Dominant Asset Theorem，並提出顯式 trading algorithm 用 dominant asset 條件決定下單時點

    [:octicons-arrow-right-24: 閱讀筆記](frequency-based-kelly-portfolio.md)

-   :material-dice-multiple:{{ .lg .middle }} **At What Frequency Should the Kelly Bettor Bet?**

    ---

    Hsieh × Barmish × Gubner 2018 ACC：Bernoulli 押注場景下，零成本時最優 ELG 對下注間隔 n 為非遞增、提出 sufficient attractiveness inequality 作為低頻匹配高頻的條件

    [:octicons-arrow-right-24: 閱讀筆記](kelly-bettor-frequency.md)

-   :material-alert-circle:{{ .lg .middle }} **On Kelly Betting: Some Limitations**

    ---

    Hsieh × Barmish 2015 Allerton：Kelly 系列研究的開山批判篇—點出 Taylor 近似失準與 drawdown 過大兩個 Kelly 主結論的限制，定調作者後續整條 Kelly 研究線的問題清單

    [:octicons-arrow-right-24: 閱讀筆記](kelly-betting-limitations.md)

-   :material-format-vertical-align-bottom:{{ .lg .middle }} **Kelly Betting Can Be Too Conservative**

    ---

    Hsieh × Barmish × Gubner 2016 CDC：跟主流「Kelly 太激進」相反，本篇證明 Kelly 常常太保守—Restricted Betting Theorem 顯示 unbounded support 分布下 Kelly 押注趨近 0、實證樣本反而更積極

    [:octicons-arrow-right-24: 閱讀筆記](kelly-betting-too-conservative.md)

-   :material-trending-neutral:{{ .lg .middle }} **Compounding Effects in Leveraged ETFs: Beyond the Volatility Drag Paradigm**

    ---

    Hsieh × Chang × Chen 2025：挑戰「LETF 必受 volatility drag」教條，AR(1) + AR-GARCH + regime switching 分析顯示獨立報酬下 LETF 可正複利、動能市每日再平衡有利、均值回復期低頻再平衡反而保護

    [:octicons-arrow-right-24: 閱讀筆記](leveraged-etf-compounding.md)

-   :material-trending-down:{{ .lg .middle }} **On Inefficiency of Markowitz-Style Investment Strategies When Drawdown is Important**

    ---

    Hsieh × Barmish 2017 CDC：以 drawdown 取代 variance 當風險指標時，古典 Markowitz LTI 反饋策略不效率，drawdown modulator 時變反饋以機率 1 提供 worst-case drawdown 保護

    [:octicons-arrow-right-24: 閱讀筆記](markowitz-inefficiency-drawdown.md)

-   :material-account-cash:{{ .lg .middle }} **On Positive Solutions of a Delay Equation Arising When Trading in Financial Markets**

    ---

    Hsieh × Barmish × Gubner 2020 IEEE TAC：把交易者帳戶價值寫成離散時間含延遲線性方程，找出 feedback gain α₋/α₊ 兩個門檻分別保證「永不破產」與「必破產」

    [:octicons-arrow-right-24: 閱讀筆記](positive-solutions-delay-equation.md)

-   :material-clock-fast:{{ .lg .middle }} **On Frequency-Based Optimal Portfolio with Transaction Costs**

    ---

    Wong × Hsieh 2023：把 frequency-dependent log-optimal portfolio 加上交易成本後仍保持為 concave program，用兩基金定理 + sliding window 解出每期可實作的解

    [:octicons-arrow-right-24: 閱讀筆記](frequency-based-optimal-portfolio-costs.md)

-   :material-school:{{ .lg .middle }} **A Jump Start to Stock Trading Research for the Uninitiated Control Scientist: A Tutorial**

    ---

    Barmish × Formentin × Hsieh × Proskurnikov × Warnick 2024 CDC tutorial：寫給控制論研究者的股票交易入門指南，把交易研究的核心問題、方法論、未解難題系統性地展示給 control 社群

    [:octicons-arrow-right-24: 閱讀筆記](jump-start-stock-trading-tutorial.md)

-   :material-chart-line:{{ .lg .middle }} **Kronos**

    ---

    首個金融 K 線基礎模型，將 OHLCV 離散化為階層式 Token 進行自回歸預測

    [:octicons-arrow-right-24: 閱讀筆記](kronos.md)

-   :material-robot-excited:{{ .lg .middle }} **NOFX**

    ---

    Go 撰寫的全自主 AI 交易助理，x402 USDC 微支付取代 API key，連接 9 個交易所執行真實訂單

    [:octicons-arrow-right-24: 閱讀筆記](nofx.md)

-   :material-finance:{{ .lg .middle }} **OpenStock**

    ---

    開源股票分析工具

    [:octicons-arrow-right-24: 閱讀筆記](openstock.md)

-   :material-swap-horizontal-bold:{{ .lg .middle }} **pmxt**

    ---

    預測市場的 CCXT — 統一 API 連接 7 個交易所（Polymarket/Kalshi 等），Sidecar + OpenAPI 雙語言 SDK

    [:octicons-arrow-right-24: 閱讀筆記](pmxt.md)

-   :material-chart-scatter-plot:{{ .lg .middle }} **Prediction Market Analysis**

    ---

    2.92 億筆 Polymarket/Kalshi 交易的公開最大數據集，附學術研究框架與「財富轉移微結構」論文

    [:octicons-arrow-right-24: 閱讀筆記](prediction-market-analysis.md)

-   :material-server-network:{{ .lg .middle }} **QuantDinger**

    ---

    brokermr810 自架式 AI 量化交易作業系統，一個 Docker Compose 串聯 AI 研究/Python 策略/回測/實盤(crypto+IBKR+MT5+Alpaca)，Agent Gateway + MCP，內建 USDT 計費可變 SaaS

    [:octicons-arrow-right-24: 閱讀筆記](quantdinger.md)

-   :material-sync:{{ .lg .middle }} **Rebalancing Frequency Considerations for Kelly-Optimal Stock Portfolios in a Control-Theoretic Framework**

    ---

    Hsieh × Gubner × Barmish 2018 CDC：把再平衡頻率明確當參數放進 Kelly-optimal 框架，證明 dominant 條件下績效對頻率為常數函數，HFT 不必然改善

    [:octicons-arrow-right-24: 閱讀筆記](rebalancing-frequency-kelly-portfolios.md)

-   :material-decision-tree:{{ .lg .middle }} **On Risk-Sensitive Decision Making Under Uncertainty**

    ---

    Hsieh × Wong 2025 ACC：固定階段、含確定與隨機選項的 risk-sensitive 多階段決策，導出最佳性必要條件，示範用於最佳押注與庫存管理

    [:octicons-arrow-right-24: 閱讀筆記](risk-sensitive-decision-making.md)

-   :material-vector-line:{{ .lg .middle }} **On Solving Robust Log-Optimal Portfolio: A Supporting Hyperplane Approximation Approach**

    ---

    Hsieh 2024 EJOR：用 supporting hyperplane 把 distributionally robust log-optimal portfolio 化成線性規劃，可內建交易成本、槓桿、做空、survival、分散性條件

    [:octicons-arrow-right-24: 閱讀筆記](robust-log-optimal-hyperplane.md)

-   :material-source-branch:{{ .lg .middle }} **From Semi-Infinite Constraints to Structured Robust Policies: Optimal Gain Selection for Financial Systems**

    ---

    Hsieh 2022 / 2025 修訂：DLP 結構派的源頭論文，把 semi-infinite constraints 化成 balanced / complementary 兩種結構策略，廣義化 mean-variance 並提供圖形求解法

    [:octicons-arrow-right-24: 閱讀筆記](robust-optimal-linear-feedback-trading.md)

-   :material-chart-multiline:{{ .lg .middle }} **Robust Trading in a Generalized Lattice Market**

    ---

    Chung-Han Hsieh × Xin-Yu Wang 把 Double Linear Policy 從單一資產推廣到多資產相關的 lattice market，理論證明在對稱市場仍能保證 survivability + 正期望報酬，S&P 500 前 30 大實證有效

    [:octicons-arrow-right-24: 閱讀筆記](robust-trading-lattice-market.md)

-   :material-window-restore:{{ .lg .middle }} **On Data-Driven Log-Optimal Portfolio: A Sliding Window Approach**

    ---

    Wang × Hsieh 2022 IFAC：用 sliding window 解 log-optimal portfolio，產生時變權重而非靜態配置，累積報酬率超越傳統常數權重 log-optimal

    [:octicons-arrow-right-24: 閱讀筆記](sliding-window-log-optimal-portfolio.md)

-   :material-chart-areaspline:{{ .lg .middle }} **The Alchemy of Multibagger Stocks**

    ---

    464 支美股 10-bagger 實證研究：FCF/P 是最強因子、EPS 成長不顯著、動量呈反轉型態（CAFE Working Paper No.33）

    [:octicons-arrow-right-24: 閱讀筆記](multibagger-stocks.md)

-   :material-puzzle:{{ .lg .middle }} **On Unified Adaptive Portfolio Management**

    ---

    Li × Hsieh 2023：把 dynamic Black-Litterman + 因子模型 + Elastic Net + 動態 sliding window 整合成一個 adaptive portfolio 框架，S&P 500 前 100 大十年實證含 turnover 成本仍有效

    [:octicons-arrow-right-24: 閱讀筆記](unified-adaptive-portfolio-management.md)

-   :material-chart-bar:{{ .lg .middle }} **StockStats**

    ---

    股票統計分析工具

    [:octicons-arrow-right-24: 閱讀筆記](stockstats.md)

-   :material-database:{{ .lg .middle }} **TEJAPI Python Medium Quant**

    ---

    TEJ API 量化交易 Python 教學

    [:octicons-arrow-right-24: 閱讀筆記](tejapi_python_medium_quant.md)

-   :material-robot-outline:{{ .lg .middle }} **AI-Trader**

    ---

    港大 AI 交易 Benchmark + Agent-Native 社交交易平台 — 真實市場、MCP 工具鏈、多 Agent 協作

    [:octicons-arrow-right-24: 閱讀筆記](ai-trader.md)

-   :material-chart-timeline-variant:{{ .lg .middle }} **TimesFM**

    ---

    Google 時間序列基礎模型 — 200M 參數、16K context、zero-shot 預測，已整合 BigQuery

    [:octicons-arrow-right-24: 閱讀筆記](timesfm.md)

-   :material-chart-line:{{ .lg .middle }} **TradingAgents**

    ---

    多 Agent 協作的量化交易決策系統

    [:octicons-arrow-right-24: 閱讀筆記](tradingagents.md)

</div>

---

## 社群行銷

<div class="grid cards" markdown>

-   :material-bullhorn:{{ .lg .middle }} **Claude Ads**

    ---

    Claude Code Skill — 250+ 項廣告審計，跨 Google/Meta/YouTube/LinkedIn/TikTok/Apple 7 大平台

    [:octicons-arrow-right-24: 閱讀筆記](claude-ads.md)

-   :material-robot-happy:{{ .lg .middle }} **Discord Lobster**

    ---

    台灣一人公司的 Discord AI 社群管家——零依賴、$0/月、三支 cron 腳本管理 146 人社群

    [:octicons-arrow-right-24: 閱讀筆記](discord-lobster.md)

-   :material-instagram:{{ .lg .middle }} **Insta-Booster**

    ---

    Instagram Reels 自動化互動工具

    [:octicons-arrow-right-24: 閱讀筆記](insta-booster.md)

</div>

---

## AI 創作資源

<div class="grid cards" markdown>

-   :material-image-multiple:{{ .lg .middle }} **AI 圖像生成 Prompt Gallery 生態**

    ---

    Civitai、PromptHero、Lexica 等 15+ 平台全景比較，涵蓋 SFW/NSFW、選擇決策樹

    [:octicons-arrow-right-24: 閱讀筆記](ai-image-prompt-galleries.md)

-   :material-palette-swatch:{{ .lg .middle }} **Awesome Design Systems**

    ---

    200+ 全球企業設計系統精選清單 — Google Material、Apple HIG、Shopify Polaris 到各國政府

    [:octicons-arrow-right-24: 閱讀筆記](awesome-design-systems.md)

-   :material-palette:{{ .lg .middle }} **Uniform Map AI Prompts Database**

    ---

    台灣制服地圖的 3,000+ AI 圖像生成 prompt 資料庫，視覺預覽 + 跨維度快速組合

    [:octicons-arrow-right-24: 閱讀筆記](uniform-map-prompts.md)

</div>

---

## AI 應用

<div class="grid cards" markdown>

-   :material-note-edit:{{ .lg .middle }} **AppFlowy — 開源 AI 協作工作區**

    ---

    開源 Notion 替代品 — Flutter + Rust 打造，支援本地 AI、自架部署、資料自主

    [:octicons-arrow-right-24: 閱讀筆記](appflowy.md)

-   :material-file-cabinet:{{ .lg .middle }} **Cabinet — AI-First 知識庫與新創作業系統**

    ---

    AI-first 知識庫 + 新創 OS — Markdown on disk、AI Agent 團隊、排程任務、自架部署

    [:octicons-arrow-right-24: 閱讀筆記](cabinet.md)

-   :material-briefcase-search:{{ .lg .middle }} **Career-Ops**

    ---

    Claude Code 驅動的 AI 求職系統 — 14 個 skill modes、A-F 評分、ATS 履歷生成、批次處理 740+ 職缺

    [:octicons-arrow-right-24: 閱讀筆記](career-ops.md)

-   :material-file-document-outline:{{ .lg .middle }} **Deep-Live-Cam**

    ---

    開源即時 AI 換臉工具 — 單張照片即可驅動

    [:octicons-arrow-right-24: 閱讀筆記](deep-live-cam.md)

-   :material-airplane:{{ .lg .middle }} **FlyAI Skill**

    ---

    阿里巴巴飛豬出品的 Claude Code / OpenClaw skill，把 Fliggy 機票飯店景點門票庫存接到 coding agent，2 個月衝 590 stars

    [:octicons-arrow-right-24: 閱讀筆記](flyai-skill.md)

-   :material-airplane-search:{{ .lg .middle }} **ITA Matrix 機票搜尋引擎**

    ---

    Google 旗下最強機票研究引擎——Routing Code + Extension Code + 日曆比價 + Open Jaw，Skyscanner 做不到的進階查詢全靠它

    [:octicons-arrow-right-24: 閱讀筆記](ita-matrix.md)

-   :material-chat-question:{{ .lg .middle }} **LINE Bot Multimodal RAG (kkdai)**

    ---

    kkdai 的 LINE Bot + Gemini File Search API 多模態 RAG 範例，靠 metadata_filter 在單一 store 做多租戶隔離、Cloud Run 部署

    [:octicons-arrow-right-24: 閱讀筆記](linebot-multimodal-rag.md)

-   :material-head-lightbulb:{{ .lg .middle }} **MemPalace**

    ---

    Milla Jovovich 的 AI 記憶宮殿系統 — 本地 ChromaDB 全文儲存 + 空間隱喻導航，96.6% LongMemEval

    [:octicons-arrow-right-24: 閱讀筆記](mempalace.md)

-   :material-cog-transfer:{{ .lg .middle }} **n8n-workflows**

    ---

    4,343 個免費 n8n 自動化工作流模板庫 — 從 AI Agent 到行銷自動化，一鍵匯入即用

    [:octicons-arrow-right-24: 閱讀筆記](n8n-workflows.md)

-   :material-notebook-multiple:{{ .lg .middle }} **notebooklm-py**

    ---

    teng-lin 非官方 NotebookLM Python API + agentic skill，15k stars/4.5 個月，CLI/Python/Claude Code/Codex/OpenClaw 三入口，能解鎖 web UI 沒有的批次下載/PPTX/JSON 心智圖等隱藏能力

    [:octicons-arrow-right-24: 閱讀筆記](notebooklm-py.md)

-   :material-account-heart:{{ .lg .middle }} **OpenHuman**

    ---

    tinyhumansai 的個人 AI 桌面助理，Rust+Tauri 桌面 mascot 會說話/開會、118+ OAuth 整合 20 分鐘自動 fetch、Memory Tree + Obsidian Wiki 在地持久記憶

    [:octicons-arrow-right-24: 閱讀筆記](openhuman.md)

-   :material-file-document-outline:{{ .lg .middle }} **OpenClam**

    ---

    台灣資安研究員開發的開源惡意程式分析工具

    [:octicons-arrow-right-24: 閱讀筆記](openclam.md)

-   :material-file-document-outline:{{ .lg .middle }} **OpenDataLoader PDF**

    ---

    Hancom 開源 PDF 資料載入器 — LangChain 整合、Benchmark 第一

    [:octicons-arrow-right-24: 閱讀筆記](opendataloader-pdf.md)

-   :material-file-document-outline:{{ .lg .middle }} **Ramp AI Agents — $32B 公司如何讓 AI Agent 主導一切**

    ---

    Ramp $32B 公司如何讓 AI Agent 主導 30% 的 PR

    [:octicons-arrow-right-24: 閱讀筆記](ramp-ai-agents.md)

-   :material-home-search:{{ .lg .middle }} **tw-house-ops**

    ---

    台灣看房 AI 管線 — Claude Code 驅動，自動掃描 591/信義/永慶，評估、追蹤、議價一條龍

    [:octicons-arrow-right-24: 閱讀筆記](tw-house-ops.md)

</div>

---

## OSINT / 情報工具

<div class="grid cards" markdown>

-   :material-radar:{{ .lg .middle }} **OsintRadar**

    ---

    社群策展的 OSINT 工具目錄 — 335 個工具、21 個分類，按調查工作流組織

    [:octicons-arrow-right-24: 閱讀筆記](osint-radar.md)

-   :material-magnify-scan:{{ .lg .middle }} **pyWhat — 「這是什麼？」的萬用辨識器**

    ---

    Python CLI — 自動辨識文字/檔案中的 email、IP、API key、加密貨幣錢包等 141 種模式

    [:octicons-arrow-right-24: 閱讀筆記](pywhat.md)

</div>

---

## 軟體工程知識

<div class="grid cards" markdown>

-   :material-book-open-variant:{{ .lg .middle }} **Laws of Software Engineering**

    ---

    Dr. Milan Milanović 整理的 56 條軟體工程定律參考站，分七大類（團隊/規劃/架構/品質/設計/規模/決策），含書、海報、JSON API、50k 訂閱電子報，已成 Amazon 暢銷書

    [:octicons-arrow-right-24: 閱讀筆記](laws-of-software-engineering.md)

</div>

---

## 開發工具

<div class="grid cards" markdown>

-   :material-database-cog:{{ .lg .middle }} **MCP Toolbox for Databases**

    ---

    Google 官方 MCP Server — 讓 AI Agent 直連 42 種資料庫，Go 核心 + 4 語言 SDK

    [:octicons-arrow-right-24: 閱讀筆記](mcp-toolbox.md)

-   :material-broom:{{ .lg .middle }} **Mole**

    ---

    tw93 打造的單一 binary Mac 深度清理工具，一條 `mo` 命令包辦 CleanMyMac + AppCleaner + DaisyDisk + iStat Menus，7 個月從 0 衝到 48.9K stars、MIT 開源

    [:octicons-arrow-right-24: 閱讀筆記](mole.md)

-   :material-tune-variant:{{ .lg .middle }} **Optuna — Python 超參數優化天花板，正邁向 Prompt Optimization 時代**

    ---

    Python 超參數優化框架天花板，14K stars、define-by-run API，v5 將加上 Prompt Optimization 與 MCP Server

    [:octicons-arrow-right-24: 閱讀筆記](optuna.md)

-   :material-console-line:{{ .lg .middle }} **CLI-Anything**

    ---

    HKUDS 把任何 GUI 軟體用 7 步驟 pipeline 自動產出 agent-friendly CLI harness，60+ 軟體覆蓋，CLI-Hub 一鍵安裝，36k stars / 2 個月

    [:octicons-arrow-right-24: 閱讀筆記](cli-anything.md)

-   :material-router-network:{{ .lg .middle }} **LiteLLM**

    ---

    BerriAI 開源 AI Gateway，把 100+ LLM provider 統一成 OpenAI 格式 + virtual keys + cost tracking + guardrails，YC W23，被 Stripe/Netflix/OpenAI Agents SDK 採用，47k stars

    [:octicons-arrow-right-24: 閱讀筆記](litellm.md)

-   :material-format-text:{{ .lg .middle }} **Pretext**

    ---

    Cheng Lou 的零 DOM 文字排版引擎 — `layout()` 比 DOM 測量快 480-1240x，17+ 語言深度支援（4.6K stars / 3 天）

    [:octicons-arrow-right-24: 閱讀筆記](pretext.md)

-   :material-file-search:{{ .lg .middle }} **RAG-Anything**

    ---

    HKUDS All-in-One Multimodal RAG 框架，以 LightRAG 為核心 + MinerU 解析，支援 PDF/Office/影像/公式/表格與 multimodal knowledge graph

    [:octicons-arrow-right-24: 閱讀筆記](rag-anything.md)

-   :material-spider-web:{{ .lg .middle }} **Scrapling**

    ---

    自適應 Web Scraping 框架 — 網站改版後自動重新定位元素，內建繞過 Cloudflare + MCP Server

    [:octicons-arrow-right-24: 閱讀筆記](scrapling.md)

-   :material-test-tube:{{ .lg .middle }} **TestPilot.AI**

    ---

    用 GitHub Copilot SDK 分析網站並自動產生完整 Playwright 測試套件

    [:octicons-arrow-right-24: 閱讀筆記](testpilot-ai.md)

-   :material-cloud-sync:{{ .lg .middle }} **VirtEngine**

    ---

    去中心化 Serverless 雲端市場（Akash fork）+ Bosun AI Agent 協調器

    [:octicons-arrow-right-24: 閱讀筆記](virtengine.md)

-   :material-cellphone-link:{{ .lg .middle }} **WebToApp**

    ---

    在手機上直接將任意網站/HTML/React 打包成 Android APK — 不需 Android Studio

    [:octicons-arrow-right-24: 閱讀筆記](web-to-app.md)

</div>

---

## 學習資源

<div class="grid cards" markdown>

-   :material-robot:{{ .lg .middle }} **AI Agents (黃佳)**

    ---

    《動手做AI Agent》書籍配套程式碼與教學

    [:octicons-arrow-right-24: 閱讀筆記](ai-agents.md)

-   :material-school:{{ .lg .middle }} **AI Agents for Beginners**

    ---

    Microsoft 官方 12 (+6) 課 AI Agent 入門課，以 Microsoft Agent Framework + Azure AI Foundry V2 為主軸，61k stars、50+ 語言

    [:octicons-arrow-right-24: 閱讀筆記](ai-agents-for-beginners.md)

-   :material-book-open-page-variant:{{ .lg .middle }} **Claude Code from Source — 逆向工程架構全書**

    ---

    18 章深度逆向工程 Claude Code 架構 — 從 npm source map 解析 2,000 個 TypeScript 檔案

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-from-source.md)

-   :material-notebook-multiple:{{ .lg .middle }} **Anthropic Claude Cookbooks — 40.8K stars 的官方範例庫**

    ---

    Anthropic 官方 40.8K stars 的 Claude 食譜庫，從 RAG 到 Managed Agents 的完整可執行範例

    [:octicons-arrow-right-24: 閱讀筆記](claude-cookbooks.md)

-   :material-clipboard-list-outline:{{ .lg .middle }} **Claude Use Cases Gallery**

    ---

    Anthropic 官方 Use Cases 資料庫——13 行業 × 7 功能 × 4 產品線，從 Cowork 桌面代理到法務合約紅線的全景案例集

    [:octicons-arrow-right-24: 閱讀筆記](claude-use-cases.md)

-   :material-school:{{ .lg .middle }} **DeepTutor**

    ---

    港大 HKUDS 開源 AI 學習助理 — RAG 知識庫 + 多 Agent 解題 + TutorBot 自主家教 + CLI 原生

    [:octicons-arrow-right-24: 閱讀筆記](deep-tutor.md)

-   :material-memory:{{ .lg .middle }} **Gemma 4 與 Local LLM**

    ---

    Google Gemma 4 模型全解析 + 2026 Local LLM 推論工具對比（Ollama / llama.cpp / vLLM / LM Studio）

    [:octicons-arrow-right-24: 閱讀筆記](gemma-4-local-llm.md)

-   :material-brain:{{ .lg .middle }} **Karpathy LLM Wiki**

    ---

    Karpathy 提出的 LLM 知識庫模式 — 用 AI Agent 編譯、維護持久化 Markdown Wiki，取代傳統 RAG

    [:octicons-arrow-right-24: 閱讀筆記](karpathy-llm-wiki.md)

-   :material-school:{{ .lg .middle }} **AI Engineering from Scratch**

    ---

    從零學 AI 工程 — 20 Phases、260+ 課、290 小時，從數學到多 Agent Swarm 全覆蓋

    [:octicons-arrow-right-24: 閱讀筆記](ai-engineering-from-scratch.md)

-   :material-language-csharp:{{ .lg .middle }} **dotLLM**

    ---

    用純 C#/.NET 10 從零打造 LLM 推論引擎 — Zero-GC、SIMD、CUDA、Paged KV-cache

    [:octicons-arrow-right-24: 閱讀筆記](dotllm.md)

-   :material-school:{{ .lg .middle }} **Learn Claude Code**

    ---

    44K stars 的 Agent Harness 工程教科書——12 個漸進 Session 從 1 個 loop + Bash 到 worktree 隔離多 Agent 協作，附 Next.js 互動學習平台

    [:octicons-arrow-right-24: 閱讀筆記](learn-claude-code.md)

-   :material-book-open-variant:{{ .lg .middle }} **LLM Course**

    ---

    LLM 學習課程資源

    [:octicons-arrow-right-24: 閱讀筆記](llm-course.md)

-   :material-school:{{ .lg .middle }} **MCP for Beginners**

    ---

    微軟官方 MCP 入門課程，12 模組 × 6 種語言 (.NET / Java / JS / TS / Python / Rust)，對齊 MCP 規範 2025-11-25，模組 11 含 13 個 PostgreSQL 整合實作實驗室，20 天衝到 15.9K stars

    [:octicons-arrow-right-24: 閱讀筆記](mcp-for-beginners.md)

-   :material-book-open-variant:{{ .lg .middle }} **OpenAI: A Practical Guide to Building Agents**

    ---

    OpenAI 官方 34 頁 Agent 建構指南 — 定義、設計基礎、編排模式、護欄，從客戶部署提煉的最佳實踐

    [:octicons-arrow-right-24: 閱讀筆記](openai-practical-guide-building-agents.md)

-   :material-school:{{ .lg .middle }} **LY Corp — Google ADK 入門：打造 AI Agent 與多代理人系統**

    ---

    LY Corporation 技術部落格 — Google ADK 入門系列，從單一 Agent 到多代理人系統的實戰教學

    [:octicons-arrow-right-24: 閱讀筆記](ly-corp-adk-agent.md)

-   :material-bookmark:{{ .lg .middle }} **Reference 快速參考手冊**

    ---

    常用參考手冊

    [:octicons-arrow-right-24: 閱讀筆記](reference.md)

-   :material-fingerprint-off:{{ .lg .middle }} **reverse-SynthID**

    ---

    逆向工程 Google SynthID 圖像浮水印 — 頻譜分析發現載波結構，90% 偵測率 + 91% 相位去除

    [:octicons-arrow-right-24: 閱讀筆記](reverse-synthid.md)

-   :material-clipboard-list:{{ .lg .middle }} **Claude Code 最佳實踐完整研究報告（zeuikli）**

    ---

    zeuikli 整理 29 篇 best-practices + 52 篇 Claude blog 的 Claude Code 九面向最佳實踐總報告，含 CLAUDE.md、Hook、Cache、Subagent、Skill、MCP、安全、Routines、成本工程

    [:octicons-arrow-right-24: 閱讀筆記](zeuikli-claude-code-best-practices.md)

</div>
