# Research Memo

研究與整理感興趣的技術專案、架構模式與工具鏈。

---

## 研究更新

最近新增或整理完成的研究筆記。

<div class="grid cards" markdown>

-   :material-chart-scatter-plot:{ .lg .middle } **Prediction Market Analysis**

    ---

    `2026-03-29` 2.92 億筆 Polymarket/Kalshi 交易的公開最大數據集，附學術研究框架與「財富轉移微結構」論文

    [:octicons-arrow-right-24: 閱讀筆記](prediction-market-analysis.md)

-   :material-robot-excited:{ .lg .middle } **NOFX**

    ---

    `2026-03-29` Go 撰寫的全自主 AI 交易助理，x402 USDC 微支付取代 API key，連接 9 個交易所執行真實訂單

    [:octicons-arrow-right-24: 閱讀筆記](nofx.md)

-   :material-bank:{ .lg .middle } **AI Hedge Fund**

    ---

    `2026-03-29` 12 位傳奇投資人 AI 分身協同分析股票的多 Agent 對沖基金模擬系統（49K stars）

    [:octicons-arrow-right-24: 閱讀筆記](ai-hedge-fund.md)

-   :material-source-branch:{ .lg .middle } **Agent Orchestrator**

    ---

    `2026-03-27` Composio 的多 agent 控制平面，為每個 issue 建立 worktree、branch、PR，並自動接住 CI 與 review feedback

    [:octicons-arrow-right-24: 閱讀筆記](agent-orchestrator.md)

-   :material-newspaper-variant-outline:{ .lg .middle } **Claude Cowork Dispatch**

    ---

    `2026-03-17` 用手機遠端遙控桌面 Claude Cowork，離開電腦也能派任務

    [:octicons-arrow-right-24: 閱讀筆記](dispatch.md)

-   :material-hammer-wrench:{ .lg .middle } **gstack**

    ---

    `2026-03-11` Garry Tan 的 Claude Code 工作流系統，將 AI coding agent 組織成虛擬工程團隊

    [:octicons-arrow-right-24: 閱讀筆記](gstack.md)

-   :material-office-building:{ .lg .middle } **Paperclip**

    ---

    `2026-03-02` 開源 AI Agent 編排控制平面，把多個 Agent 組織成一間零人公司

    [:octicons-arrow-right-24: 閱讀筆記](paperclip.md)

-   :material-finance:{ .lg .middle } **Claude Financial Services Plugins**

    ---

    `2026-02-23` Anthropic 官方金融服務 Plugin，覆蓋投行、股研、PE 與財管工作流

    [:octicons-arrow-right-24: 閱讀筆記](claude-financial-services-plugins.md)

</div>

[查看研究索引](news.md)

---

## AI Agent 框架

<div class="grid cards" markdown>

-   :material-flask:{ .lg .middle } **Autoresearch**

    ---

    Karpathy 的自主 AI 研究代理，讓 Agent 整夜跑 LLM 實驗

    [:octicons-arrow-right-24: 閱讀筆記](autoresearch.md)

-   :material-brain:{ .lg .middle } **AutoGPT**

    ---

    自主 AI Agent 先驅專案

    [:octicons-arrow-right-24: 閱讀筆記](autogpt.md)

-   :material-account-group:{ .lg .middle } **CrewAI**

    ---

    多 Agent 角色扮演協作框架

    [:octicons-arrow-right-24: 閱讀筆記](crewai.md)

-   :material-link-variant:{ .lg .middle } **LangChain**

    ---

    LLM 應用開發框架

    [:octicons-arrow-right-24: 閱讀筆記](langchain.md)

-   :material-state-machine:{ .lg .middle } **LangGraph State API**

    ---

    LangGraph 圖狀態機核心 API：State、Reducer、Channel、MessagesState 完整解析

    [:octicons-arrow-right-24: 閱讀筆記](langgraph-state-api.md)

-   :material-hub:{ .lg .middle } **LobeHub**

    ---

    74K stars 的 AI Agent 協作平台，Supervisor + Executor 多 Agent 架構、39K+ MCP 市集、White-Box Memory

    [:octicons-arrow-right-24: 閱讀筆記](lobehub.md)

-   :material-fishbowl:{ .lg .middle } **MiroFish**

    ---

    40K stars 群體智能預測引擎，用數千 AI Agent 模擬平行社會推演未來

    [:octicons-arrow-right-24: 閱讀筆記](mirofish.md)

-   :material-office-building:{ .lg .middle } **Paperclip**

    ---

    開源 AI Agent 編排控制平面，把多個 Agent 組織成「零人公司」

    [:octicons-arrow-right-24: 閱讀筆記](paperclip.md)

-   :material-cursor-default-click:{ .lg .middle } **Page Agent**

    ---

    阿里巴巴的網頁內嵌 GUI Agent，用自然語言控制網頁介面

    [:octicons-arrow-right-24: 閱讀筆記](page-agent.md)

-   :material-robot-outline:{ .lg .middle } **Project Golem**

    ---

    Browser-in-the-Loop 自主 AI 代理，金字塔記憶可存 50 年對話精華

    [:octicons-arrow-right-24: 閱讀筆記](project-golem.md)

-   :material-forum:{ .lg .middle } **多 Agent 辯論會**

    ---

    使用 Copilot SDK 建構的多 Agent 辯論系統

    [:octicons-arrow-right-24: 閱讀筆記](multi-agent-debate.md)

</div>

---

## Coding Agent 工具

<div class="grid cards" markdown>

-   :material-airplane-takeoff:{ .lg .middle } **App Store Preflight**

    ---

    AI Agent Skill，提交前自動掃描 iOS/macOS 專案的 App Store 審核風險

    [:octicons-arrow-right-24: 閱讀筆記](app-store-preflight.md)

-   :material-cogs:{ .lg .middle } **Anthropic Harness Design**

    ---

    Anthropic 的 GAN 啟發三 Agent Harness 架構，讓 Claude 自主建構完整全端應用

    [:octicons-arrow-right-24: 閱讀筆記](harness-design-long-running-apps.md)

-   :material-account-multiple:{ .lg .middle } **Agency Agents**

    ---

    144 個專業化 AI Agent 人格庫，橫跨 12 部門，支援 10 個 AI 工具

    [:octicons-arrow-right-24: 閱讀筆記](agency-agents.md)

-   :material-file-compare:{ .lg .middle } **Difftastic**

    ---

    24.8K stars 的結構化 diff 工具，用 tree-sitter 解析語法樹，只顯示真正有意義的程式碼變動

    [:octicons-arrow-right-24: 閱讀筆記](difftastic.md)

-   :material-monitor-dashboard:{ .lg .middle } **Claude HUD**

    ---

    11.5K stars 的 Claude Code 狀態列 plugin，即時顯示 context 用量、工具活動、Agent 狀態

    [:octicons-arrow-right-24: 閱讀筆記](claude-hud.md)

-   :material-finance:{ .lg .middle } **Claude Financial Services Plugins**

    ---

    Anthropic 官方金融服務 Plugin：41 Skills、11 MCP 資料源，覆蓋投行/股研/PE/財管端到端工作流

    [:octicons-arrow-right-24: 閱讀筆記](claude-financial-services-plugins.md)

-   :material-send:{ .lg .middle } **Claude Cowork Dispatch**

    ---

    用手機遠端遙控桌面 Claude Cowork，離開電腦也能派任務

    [:octicons-arrow-right-24: 閱讀筆記](dispatch.md)

-   :material-package-variant-closed:{ .lg .middle } **Everything Claude Code**

    ---

    97K stars 的 Agent Harness 效能優化系統：28 agents、116 skills、59 commands

    [:octicons-arrow-right-24: 閱讀筆記](everything-claude-code.md)

-   :material-star-shooting:{ .lg .middle } **Claude Code Showcase**

    ---

    Claude Code 使用案例展示

    [:octicons-arrow-right-24: 閱讀筆記](claude-code-showcase.md)

-   :material-puzzle:{ .lg .middle } **Claude Skills Guide**

    ---

    Claude Skills 建構完整指南

    [:octicons-arrow-right-24: 閱讀筆記](claude-skills-guide.md)

-   :material-school:{ .lg .middle } **Learn Claude Code**

    ---

    Claude Code 學習資源

    [:octicons-arrow-right-24: 閱讀筆記](learn-claude-code.md)

-   :material-lightning-bolt:{ .lg .middle } **Lightpanda Browser**

    ---

    用 Zig 從零打造的 headless browser，比 Chrome 快 11x、省 9x 記憶體，專為 AI Agent 設計

    [:octicons-arrow-right-24: 閱讀筆記](lightpanda-browser.md)

-   :material-console:{ .lg .middle } **GitHub Copilot CLI**

    ---

    GitHub Copilot 命令列工具

    [:octicons-arrow-right-24: 閱讀筆記](copilot-cli.md)

-   :material-cog:{ .lg .middle } **GitHub Copilot Configs**

    ---

    GitHub Copilot 設定與自訂指令

    [:octicons-arrow-right-24: 閱讀筆記](github-copilot-configs.md)

-   :material-code-braces:{ .lg .middle } **GitHub Copilot SDK**

    ---

    GitHub Copilot SDK 開發研究

    [:octicons-arrow-right-24: 閱讀筆記](github-copilot-sdk.md)

-   :material-refresh:{ .lg .middle } **Copilot Ralph**

    ---

    Copilot Ralph 自主迭代開發模式

    [:octicons-arrow-right-24: 閱讀筆記](copilot-ralph.md)

-   :material-hammer-wrench:{ .lg .middle } **gstack**

    ---

    Garry Tan (YC CEO) 的 Claude Code 工作流系統

    [:octicons-arrow-right-24: 閱讀筆記](gstack.md)

-   :material-source-branch:{ .lg .middle } **Agent Orchestrator**

    ---

    Composio 的多 agent 控制平面，為每個 issue 建立 worktree、branch、PR，並自動處理 CI 與 review feedback

    [:octicons-arrow-right-24: 閱讀筆記](agent-orchestrator.md)

-   :material-connection:{ .lg .middle } **MCP CLI**

    ---

    Model Context Protocol CLI 工具

    [:octicons-arrow-right-24: 閱讀筆記](mcp-cli.md)

-   :material-swap-horizontal:{ .lg .middle } **OpenClaw Claude Proxy**

    ---

    將 Claude Max 訂閱轉為 OpenAI 相容 API，驅動 Agent 群免費用 Opus 4.6

    [:octicons-arrow-right-24: 閱讀筆記](openclaw-claude-proxy.md)

-   :material-shield-star:{ .lg .middle } **Superpowers**

    ---

    106K stars 的 agentic skills 框架，用心理學說服原則強制 coding agent 遵守開發紀律

    [:octicons-arrow-right-24: 閱讀筆記](superpowers.md)

</div>

---

## 量化交易

<div class="grid cards" markdown>

-   :material-bank:{ .lg .middle } **AI Hedge Fund**

    ---

    12 位傳奇投資人 AI 分身協同分析股票，LangGraph 驅動的多 Agent 對沖基金模擬系統

    [:octicons-arrow-right-24: 閱讀筆記](ai-hedge-fund.md)

-   :material-robot-excited:{ .lg .middle } **NOFX**

    ---

    Go 撰寫的全自主 AI 交易助理，x402 USDC 微支付取代 API key，連接 9 個交易所執行真實訂單

    [:octicons-arrow-right-24: 閱讀筆記](nofx.md)

-   :material-finance:{ .lg .middle } **OpenStock**

    ---

    開源股票分析工具

    [:octicons-arrow-right-24: 閱讀筆記](openstock.md)

-   :material-chart-bar:{ .lg .middle } **StockStats**

    ---

    股票統計分析工具

    [:octicons-arrow-right-24: 閱讀筆記](stockstats.md)

-   :material-database:{ .lg .middle } **TEJAPI Python Quant**

    ---

    TEJ API 量化交易 Python 教學

    [:octicons-arrow-right-24: 閱讀筆記](tejapi_python_medium_quant.md)

-   :material-chart-scatter-plot:{ .lg .middle } **Prediction Market Analysis**

    ---

    2.92 億筆 Polymarket/Kalshi 公開數據集，揭示預測市場財富轉移微結構

    [:octicons-arrow-right-24: 閱讀筆記](prediction-market-analysis.md)

-   :material-chart-line:{ .lg .middle } **TradingAgents**

    ---

    多 Agent 協作的量化交易決策系統

    [:octicons-arrow-right-24: 閱讀筆記](tradingagents.md)

</div>

---

## 社群行銷

<div class="grid cards" markdown>

-   :material-instagram:{ .lg .middle } **Insta-Booster**

    ---

    Instagram Reels 自動化互動工具

    [:octicons-arrow-right-24: 閱讀筆記](insta-booster.md)

</div>

---

## 學習資源

<div class="grid cards" markdown>

-   :material-robot:{ .lg .middle } **AI Agents (黃佳)**

    ---

    《動手做AI Agent》書籍配套程式碼與教學

    [:octicons-arrow-right-24: 閱讀筆記](ai-agents.md)

-   :material-book-open-variant:{ .lg .middle } **LLM Course**

    ---

    LLM 學習課程資源

    [:octicons-arrow-right-24: 閱讀筆記](llm-course.md)

-   :material-bookmark:{ .lg .middle } **Reference 快速參考**

    ---

    常用參考手冊

    [:octicons-arrow-right-24: 閱讀筆記](reference.md)

</div>

---

## AI 創作資源

<div class="grid cards" markdown>

-   :material-image-multiple:{ .lg .middle } **AI 圖像 Prompt Gallery 生態**

    ---

    Civitai、PromptHero、Lexica 等 15+ 平台全景比較，涵蓋 SFW/NSFW、選擇決策樹

    [:octicons-arrow-right-24: 閱讀筆記](ai-image-prompt-galleries.md)

-   :material-palette:{ .lg .middle } **Uniform Map AI Prompts**

    ---

    台灣制服地圖的 3,000+ AI 圖像生成 prompt 資料庫，視覺預覽 + 跨維度快速組合

    [:octicons-arrow-right-24: 閱讀筆記](uniform-map-prompts.md)

</div>
