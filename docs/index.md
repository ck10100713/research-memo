# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-robot-outline:{{ .lg .middle }} **Claude Agent SDK**

    ---

    `2026-03-31` Anthropic 官方 Agent SDK — 把 Claude Code 的工具與 Agent Loop 變成可程式化的 Python / TypeScript 函式庫

    [:octicons-arrow-right-24: 閱讀筆記](claude-agent-sdk.md)

-   :material-ghost:{{ .lg .middle }} **claude-better**

    ---

    `2026-03-31` CryptoSwift 作者的多層諷刺——main branch 0 行程式碼配企業級 README，code branch 是 XOR 混淆的 C 假 CLI，永遠回覆 'Your account is blocked'

    [:octicons-arrow-right-24: 閱讀筆記](claude-better.md)

-   :material-robot-industrial:{{ .lg .middle }} **OpenAI Agents SDK**

    ---

    `2026-03-31` OpenAI 官方 Agent 框架 — 以 Handoffs + Guardrails 為核心的輕量多代理工作流系統

    [:octicons-arrow-right-24: 閱讀筆記](openai-agents-sdk.md)

-   :material-google:{{ .lg .middle }} **Google Agent Development Kit (ADK)**

    ---

    `2026-03-31` Google 官方 Agent 框架 — 以 LlmAgent + Workflow Agents 為核心的 code-first 多代理開發套件

    [:octicons-arrow-right-24: 閱讀筆記](google-adk.md)

-   :material-code-braces-box:{{ .lg .middle }} **cloclo (claude-code-sdk)**

    ---

    `2026-03-31` 單檔 18,500 行的多 Provider Claude Code 替代品——13 個 LLM 後端 + Ink TUI + NDJSON Bridge + Skills Marketplace，npm 安裝即用

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-sdk.md)

-   :material-school:{{ .lg .middle }} **Learn Claude Code**

    ---

    `2026-03-31` 44K stars 的 Agent Harness 工程教科書——12 個漸進 Session 從 1 個 loop + Bash 到 worktree 隔離多 Agent 協作，附 Next.js 互動學習平台

    [:octicons-arrow-right-24: 閱讀筆記](learn-claude-code.md)

-   :material-school:{{ .lg .middle }} **LY Corp — Google ADK 入門：打造 AI Agent 與多代理人系統**

    ---

    `2026-03-31` LY Corporation 技術部落格 — Google ADK 入門系列，從單一 Agent 到多代理人系統的實戰教學

    [:octicons-arrow-right-24: 閱讀筆記](ly-corp-adk-agent.md)

-   :material-airplane-search:{{ .lg .middle }} **ITA Matrix 機票搜尋引擎**

    ---

    `2026-03-31` Google 旗下最強機票研究引擎——Routing Code + Extension Code + 日曆比價 + Open Jaw，Skyscanner 做不到的進階查詢全靠它

    [:octicons-arrow-right-24: 閱讀筆記](ita-matrix.md)

-   :material-file-search-outline:{{ .lg .middle }} **Analysis Claude Code**

    ---

    `2026-03-31` Claude Code v1.0.33 靜態逆向工程——50,000 行混淆碼拆解為 102 chunks，揭示 h2A 消息隊列、6 層權限驗證、92% 閾值上下文壓縮

    [:octicons-arrow-right-24: 閱讀筆記](analysis-claude-code.md)

-   :material-github:{{ .lg .middle }} **GitHub Copilot SDK**

    ---

    `2026-03-31` GitHub 官方 Agent SDK — 把 Copilot CLI 的 Agent 引擎以 JSON-RPC 暴露為可嵌入的多語言函式庫

    [:octicons-arrow-right-24: 閱讀筆記](github-copilot-sdk.md)

-   :material-magnify-scan:{{ .lg .middle }} **Claude Code Reverse Engineering**

    ---

    `2026-03-31` 2.3K stars 的 Claude Code 逆向工程——v2 基於 Runtime Monkey Patch 攔截 API 請求，附帶 Log 視覺化工具和完整 Prompt 解碼

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-reverse.md)

-   :material-account-supervisor:{{ .lg .middle }} **LangGraph Supervisor**

    ---

    `2026-03-30` LangGraph 官方 Supervisor 多 Agent 庫——中央調度器模式，支援多層階層與訊息歷史控制（1.5K stars）

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-supervisor-py.md)

-   :material-shield-star:{{ .lg .middle }} **Superpowers**

    ---

    `2026-03-30` 106K stars 的 agentic skills 框架，用心理學說服原則強制 coding agent 遵守開發紀律

    [:octicons-arrow-right-24: 閱讀筆記](superpowers.md)

-   :material-hammer-wrench:{{ .lg .middle }} **gstack**

    ---

    `2026-03-30` Garry Tan 的 Claude Code 工作流系統，將 AI coding agent 組織成虛擬工程團隊

    [:octicons-arrow-right-24: 閱讀筆記](gstack.md)

-   :material-account-group-outline:{{ .lg .middle }} **LangGraph Multi-Agent Research Assistant**

    ---

    `2026-03-30` LangGraph Supervisor 模式教學範例——Researcher/Writer/Reviewer 三 Agent 研究助理，附 human-in-the-loop

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-multi-agent.md)

-   :material-code-braces-box:{{ .lg .middle }} **Open SWE**

    ---

    `2026-03-30` LangChain 開源的企業內部 Coding Agent 框架——複製 Stripe/Ramp/Coinbase 的內部架構（8.8K stars）

    [:octicons-arrow-right-24: 閱讀筆記](open-swe.md)

-   :material-swap-horizontal-circle:{{ .lg .middle }} **LangGraph Swarm**

    ---

    `2026-03-30` LangGraph 官方 Swarm 多 Agent 庫——去中心化 handoff 模式，agent 間直接交接，延遲低 40%（1.4K stars）

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-swarm-py.md)

</div>

[查看研究索引](news.md)

---

## AI Agent 框架

<div class="grid cards" markdown>

-   :material-file-document-outline:{{ .lg .middle }} **Agent GoFundMe**

    ---

    

    [:octicons-arrow-right-24: 閱讀筆記](agent-gofundme.md)

-   :material-file-document-outline:{{ .lg .middle }} **AgentBnB**

    ---

    

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

-   :material-file-search-outline:{{ .lg .middle }} **Analysis Claude Code**

    ---

    Claude Code v1.0.33 靜態逆向工程——50,000 行混淆碼拆解為 102 chunks，揭示 h2A 消息隊列、6 層權限驗證、92% 閾值上下文壓縮

    [:octicons-arrow-right-24: 閱讀筆記](analysis-claude-code.md)

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

    

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-boris-cherny-tips.md)

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

-   :material-finance:{{ .lg .middle }} **Claude Financial Services Plugins**

    ---

    Anthropic 官方金融服務 Plugin：41 Skills、11 MCP 資料源，覆蓋投行/股研/PE/財管端到端工作流

    [:octicons-arrow-right-24: 閱讀筆記](claude-financial-services-plugins.md)

-   :material-account-multiple:{{ .lg .middle }} **The Agency: AI Specialists**

    ---

    144 個專業化 AI Agent 人格庫，橫跨 12 部門，支援 10 個 AI 工具

    [:octicons-arrow-right-24: 閱讀筆記](agency-agents.md)

-   :material-file-compare:{{ .lg .middle }} **Difftastic**

    ---

    24.8K stars 的結構化 diff 工具，用 tree-sitter 解析語法樹，只顯示真正有意義的程式碼變動

    [:octicons-arrow-right-24: 閱讀筆記](difftastic.md)

-   :material-monitor-dashboard:{{ .lg .middle }} **Claude HUD**

    ---

    11.5K stars 的 Claude Code 狀態列 plugin，即時顯示 context 用量、工具活動、Agent 狀態

    [:octicons-arrow-right-24: 閱讀筆記](claude-hud.md)

-   :material-newspaper-variant-outline:{{ .lg .middle }} **Claude Cowork Dispatch**

    ---

    用手機遠端遙控桌面 Claude Cowork，離開電腦也能派任務

    [:octicons-arrow-right-24: 閱讀筆記](dispatch.md)

-   :material-package-variant-closed:{{ .lg .middle }} **Everything Claude Code**

    ---

    97K stars 的 Agent Harness 效能優化系統：28 agents、116 skills、59 commands

    [:octicons-arrow-right-24: 閱讀筆記](everything-claude-code.md)

-   :material-star-shooting:{{ .lg .middle }} **Claude Code Showcase**

    ---

    Claude Code 使用案例展示

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-showcase.md)

-   :material-puzzle:{{ .lg .middle }} **The Complete Guide to Building Skills for Claude —**

    ---

    Claude Skills 建構完整指南

    [:octicons-arrow-right-24: 閱讀筆記](claude-skills-guide.md)

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

    Copilot Ralph 自主迭代開發模式

    [:octicons-arrow-right-24: 閱讀筆記](copilot-ralph.md)

-   :material-hammer-wrench:{{ .lg .middle }} **gstack**

    ---

    Garry Tan 的 Claude Code 工作流系統，將 AI coding agent 組織成虛擬工程團隊

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

-   :material-code-braces-box:{{ .lg .middle }} **Open SWE**

    ---

    LangChain 開源的企業內部 Coding Agent 框架——複製 Stripe/Ramp/Coinbase 的內部架構（8.8K stars）

    [:octicons-arrow-right-24: 閱讀筆記](open-swe.md)

-   :material-swap-horizontal:{{ .lg .middle }} **OpenClaw Claude Proxy**

    ---

    將 Claude Max 訂閱轉為 OpenAI 相容 API，驅動 Agent 群免費用 Opus 4.6

    [:octicons-arrow-right-24: 閱讀筆記](openclaw-claude-proxy.md)

-   :material-shield-star:{{ .lg .middle }} **Superpowers**

    ---

    106K stars 的 agentic skills 框架，用心理學說服原則強制 coding agent 遵守開發紀律

    [:octicons-arrow-right-24: 閱讀筆記](superpowers.md)

-   :material-palette-outline:{{ .lg .middle }} **UI UX Pro Max Skill**

    ---

    54K stars 的 AI 設計智慧注入系統——161 條行業推理規則 + 67 種 UI 風格，讓 Coding Agent 寫出有品味的 UI

    [:octicons-arrow-right-24: 閱讀筆記](ui-ux-pro-max-skill.md)

</div>

---

## 量化交易

<div class="grid cards" markdown>

-   :material-bank:{{ .lg .middle }} **AI Hedge Fund**

    ---

    12 位傳奇投資人 AI 分身協同分析股票，LangGraph 驅動的多 Agent 對沖基金模擬系統

    [:octicons-arrow-right-24: 閱讀筆記](ai-hedge-fund.md)

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

-   :material-chart-areaspline:{{ .lg .middle }} **The Alchemy of Multibagger Stocks**

    ---

    464 支美股 10-bagger 實證研究：FCF/P 是最強因子、EPS 成長不顯著、動量呈反轉型態（CAFE Working Paper No.33）

    [:octicons-arrow-right-24: 閱讀筆記](multibagger-stocks.md)

-   :material-chart-bar:{{ .lg .middle }} **StockStats**

    ---

    股票統計分析工具

    [:octicons-arrow-right-24: 閱讀筆記](stockstats.md)

-   :material-database:{{ .lg .middle }} **TEJAPI Python Medium Quant**

    ---

    TEJ API 量化交易 Python 教學

    [:octicons-arrow-right-24: 閱讀筆記](tejapi_python_medium_quant.md)

-   :material-chart-line:{{ .lg .middle }} **TradingAgents**

    ---

    多 Agent 協作的量化交易決策系統

    [:octicons-arrow-right-24: 閱讀筆記](tradingagents.md)

</div>

---

## 社群行銷

<div class="grid cards" markdown>

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

-   :material-palette:{{ .lg .middle }} **Uniform Map AI Prompts Database**

    ---

    台灣制服地圖的 3,000+ AI 圖像生成 prompt 資料庫，視覺預覽 + 跨維度快速組合

    [:octicons-arrow-right-24: 閱讀筆記](uniform-map-prompts.md)

</div>

---

## AI 應用

<div class="grid cards" markdown>

-   :material-file-document-outline:{{ .lg .middle }} **Deep-Live-Cam**

    ---

    

    [:octicons-arrow-right-24: 閱讀筆記](deep-live-cam.md)

-   :material-airplane-search:{{ .lg .middle }} **ITA Matrix 機票搜尋引擎**

    ---

    Google 旗下最強機票研究引擎——Routing Code + Extension Code + 日曆比價 + Open Jaw，Skyscanner 做不到的進階查詢全靠它

    [:octicons-arrow-right-24: 閱讀筆記](ita-matrix.md)

-   :material-file-document-outline:{{ .lg .middle }} **OpenClam**

    ---

    

    [:octicons-arrow-right-24: 閱讀筆記](openclam.md)

-   :material-file-document-outline:{{ .lg .middle }} **OpenDataLoader PDF**

    ---

    

    [:octicons-arrow-right-24: 閱讀筆記](opendataloader-pdf.md)

-   :material-file-document-outline:{{ .lg .middle }} **Ramp AI Agents — $32B 公司如何讓 AI Agent 主導一切**

    ---

    

    [:octicons-arrow-right-24: 閱讀筆記](ramp-ai-agents.md)

</div>

---

## 開發工具

<div class="grid cards" markdown>

-   :material-format-text:{{ .lg .middle }} **Pretext**

    ---

    Cheng Lou 的零 DOM 文字排版引擎 — `layout()` 比 DOM 測量快 480-1240x，17+ 語言深度支援（4.6K stars / 3 天）

    [:octicons-arrow-right-24: 閱讀筆記](pretext.md)

</div>

---

## 學習資源

<div class="grid cards" markdown>

-   :material-robot:{{ .lg .middle }} **AI Agents (黃佳)**

    ---

    《動手做AI Agent》書籍配套程式碼與教學

    [:octicons-arrow-right-24: 閱讀筆記](ai-agents.md)

-   :material-clipboard-list-outline:{{ .lg .middle }} **Claude Use Cases Gallery**

    ---

    Anthropic 官方 Use Cases 資料庫——13 行業 × 7 功能 × 4 產品線，從 Cowork 桌面代理到法務合約紅線的全景案例集

    [:octicons-arrow-right-24: 閱讀筆記](claude-use-cases.md)

-   :material-school:{{ .lg .middle }} **Learn Claude Code**

    ---

    44K stars 的 Agent Harness 工程教科書——12 個漸進 Session 從 1 個 loop + Bash 到 worktree 隔離多 Agent 協作，附 Next.js 互動學習平台

    [:octicons-arrow-right-24: 閱讀筆記](learn-claude-code.md)

-   :material-book-open-variant:{{ .lg .middle }} **LLM Course**

    ---

    LLM 學習課程資源

    [:octicons-arrow-right-24: 閱讀筆記](llm-course.md)

-   :material-school:{{ .lg .middle }} **LY Corp — Google ADK 入門：打造 AI Agent 與多代理人系統**

    ---

    LY Corporation 技術部落格 — Google ADK 入門系列，從單一 Agent 到多代理人系統的實戰教學

    [:octicons-arrow-right-24: 閱讀筆記](ly-corp-adk-agent.md)

-   :material-bookmark:{{ .lg .middle }} **Reference 快速參考手冊**

    ---

    常用參考手冊

    [:octicons-arrow-right-24: 閱讀筆記](reference.md)

</div>
