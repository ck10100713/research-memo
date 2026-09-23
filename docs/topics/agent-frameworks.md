# AI Agent 框架

本分類收錄 31 篇研究筆記。

| 日期 | 筆記 | 摘要 |
| --- | --- | --- |
| 2026-09-09 | [LangBot](../langbot.md) | 跟 AstrBot 同賽道的自架多平台 LLM IM 機器人平台(17.7K stars、Python、Apache-2.0),前身是 2022 年的 QChatGPT(mirai QQ bot),2024-11 的 v3.4.0 移除 Mirai、加 WebUI 後正式改名 LangBot。一套後端接 QQ/微信/企微/飛書/釘釘/Discord/Telegram/Slack/LINE/KOOK/Matrix;LLM 從 OpenAI/Anthropic/Gemini/DeepSeek/智譜/Kimi/Grok/Ollama 到一票聚合平台;最大特色是能把整段對話丟給 Dify/Coze/n8n/Langflow/DeerFlow/WeKnora/百煉/螞蟻TBox 當外部大腦(runner),插件跑在獨立 Plugin Runtime 進程(SDK 隔離),沙盒用 Box Runtime(nsjail/e2b),向量庫支援 6 種、資料庫可 PostgreSQL,還內建 /mcp server + 倉庫內 skills 讓 coding agent 直接操作機器人本身。Web 前端是 React(Vite),不是 AstrBot 的 Vue |
| 2026-09-08 | [AstrBot](../astrbot.md) | 中國社群最紅的自架多平台 LLM 聊天機器人平台/框架(40.2K stars、Python、AGPL-3.0)。一套後端同時接 QQ/OneBot、Telegram、企業微信、飛書、釘釘、微信公眾號、Slack、Discord、LINE、KOOK 等十幾個 IM;LLM 支援 OpenAI/Anthropic/Gemini/DeepSeek/智譜/Kimi/Grok/Ollama 及 Dify/Coze/百煉 Agent 平台;插件叫「Star」,插件市場 1000+ 個一鍵裝;內建原生 Agent + MCP + 函式呼叫 + Anthropic 風格 Skills + Agent Sandbox(Docker 隔離跑程式碼)+ 混合式 RAG 知識庫 + STT/TTS 多模態 + Vue WebUI。uv/Docker/一鍵雲端都能裝,資料庫用 SQLite+FAISS |
| 2026-08-27 | [Agenvoy](../agenvoy.md) | 自架單一 Go binary 的個人 AI Agent harness:缺工具時「自己寫一個」而非停手,sandbox 測試後存進共用工具庫,再透過 MCP 分享給 Claude Code / Codex 等 agent;同時是 TUI + 本機 daemon + MCP server/client。台灣 Pardn Chiu 個人專案,6.5 個月 1,015 commits / 182 releases |
| 2026-08-07 | [Building Applications with AI Agents](../building-applications-with-ai-agents.md) | O'Reilly《Building Applications with AI Agents》書籍配套碼:把「同一批企業場景」用 LangGraph / LangChain / Autogen / OpenAI 四種框架平行實作,再套上共用評測（LLM judge + drift 偵測）、可觀測性（Loki + Tempo）、fine-tuning（SFT/DPO/RLVR/GRPO）與三種分散式多 agent runtime（Ray / Redis Streams / Temporal） |
| 2026-08-06 | [qm](../qm.md) | Y Combinator 出品的『multiplayer agent harness for work』：每位員工/每個房間各有隔離的 memory·檔案·keychain·sandbox，在 Slack 與 web 協作；harness 無關(Pi/Codex/Claude Code/OpenCode 同一核心)、可自架 |
| 2026-07-28 | [crewAI-examples](../crewai-examples.md) | CrewAI 官方 30 個完整範例（16 crews + 6 flows + 3 integrations + 5 notebooks），新舊兩代專案骨架並存可直接對照框架演進；但安全性做過一輪硬化、功能正確性沒有——stock_analysis 有重複方法、寫死 AMZN、README 與程式碼互相矛盾，SEC 工具的正則還會把財報數字的小數點和負號洗掉 |
| 2026-07-27 | [Bring Your Own Agent (BYOA Core)](../bring-your-own-agent.md) | 台灣單人開發者用 5.5 週、90 commits 從零重建一套 Claude Code 等級的 agent harness（兩階段 compact、subagent 防遞迴、skill 漸進式載入、tool result 分頁、多 provider gateway），全繁中、Gherkin 規格先行、附 13 個 SWE eval task 量化每次 prompt 改動——0 star 但是最好讀的 harness 解剖圖 |
| 2026-07-17 | [OpenAI Agents SDK](../openai-agents-sdk.md) | OpenAI 官方 Agent 框架 — Handoffs + Guardrails 起家，v0.18 補上 Sandbox Agents 與 Human-in-the-loop |
| 2026-06-17 | [Ponytail](../ponytail.md) | 把『最懶的資深工程師』裝進 AI agent 的跨平台 ruleset：寫程式前先過六層 YAGNI 篩子，少寫 80-94% 程式碼 |
| 2026-06-05 | [SkillOpt](../skillopt.md) | Microsoft「文字空間優化器」：像訓練神經網路（epoch/batch/learning rate/validation gate）一樣訓練凍結 LLM agent 的自然語言技能，不動權重、產出可部署的 best_skill.md；52/52 評測格全勝，GPT-5.5 對 no-skill baseline +23.5 分，v0.1.0 已上 PyPI，arXiv:2605.23904 |
| 2026-05-27 | [Webwright](../webwright.md) | Microsoft Research 極簡瀏覽器 agent 框架（~1.5k LoC），核心理念『coding agent + terminal』把瀏覽器當可拋棄環境、用 code-as-action 寫 Playwright 腳本，Online-Mind2Web 86.7% SOTA，可當 Claude Code/Codex skill |
| 2026-04-14 | [開源 AI Agent 框架比較](../open-source-agent-frameworks.md) | 2026 年功能完善的開源 Agent 框架橫向比較：從 Dify 到 LangGraph 的選型指南 |
| 2026-03-31 | [Google Agent Development Kit (ADK)](../google-adk.md) | Google 官方 Agent 框架 — 以 LlmAgent + Workflow Agents 為核心的 code-first 多代理開發套件 |
| 2026-03-30 | [Agent GoFundMe](../agent-gofundme.md) | Agent 群眾募資平台 — AI Agent 的 GoFundMe |
| 2026-03-30 | [AgentBnB](../agentbnb.md) | Agent 短租市場 — AI Agent 的 Airbnb 託管協議 |
| 2026-03-30 | [DeerFlow](../deer-flow.md) | ByteDance 開源多 Agent 深度研究框架 |
| 2026-03-30 | [LangGraph Multi-Agent Research Assistant](../langgraph-multi-agent.md) | LangGraph Supervisor 模式教學範例——Researcher/Writer/Reviewer 三 Agent 研究助理，附 human-in-the-loop |
| 2026-03-30 | [LangGraph Supervisor](../langgraph-supervisor-py.md) | LangGraph 官方 Supervisor 多 Agent 庫——中央調度器模式，支援多層階層與訊息歷史控制（1.5K stars） |
| 2026-03-30 | [LangGraph Swarm](../langgraph-swarm-py.md) | LangGraph 官方 Swarm 多 Agent 庫——去中心化 handoff 模式，agent 間直接交接，延遲低 40%（1.4K stars） |
| 2026-03-30 | [OpenClaw（龍蝦）](../openclaw.md) | 開源 AI Agent 框架 — 支援本地 LLM 的 Claude Code 替代品 |
| 2026-03-27 | [LangGraph State API](../langgraph-state-api.md) | LangGraph 圖狀態機核心 API：State、Reducer、Channel、MessagesState 完整解析 |
| 2026-03-27 | [LobeHub](../lobehub.md) | 74K stars 的 AI Agent 協作平台，Supervisor + Executor 多 Agent 架構、39K+ MCP 市集、White-Box Memory |
| 2026-03-23 | [Autoresearch](../autoresearch.md) | Karpathy 的自主 AI 研究代理，讓 Agent 整夜跑 LLM 實驗 |
| 2026-03-23 | [CrewAI](../crewai.md) | 多 Agent 角色扮演協作框架 |
| 2026-03-23 | [LangChain](../langchain.md) | LLM 應用開發框架 |
| 2026-03-23 | [MiroFish](../mirofish.md) | 40K stars 群體智能預測引擎，用數千 AI Agent 模擬平行社會推演未來 |
| 2026-03-23 | [Page Agent](../page-agent.md) | 阿里巴巴的網頁內嵌 GUI Agent，用自然語言控制網頁介面 |
| 2026-03-23 | [Project Golem](../project-golem.md) | Browser-in-the-Loop 自主 AI 代理，金字塔記憶可存 50 年對話精華 |
| 2026-03-02 | [Paperclip](../paperclip.md) | 開源 AI Agent 編排控制平面，把多個 Agent 組織成一間零人公司 |
| 2026-02-04 | [多 Agent 辯論會系統](../multi-agent-debate.md) | 使用 Copilot SDK 建構的多 Agent 辯論系統 |
| 2026-02-03 | [AutoGPT](../autogpt.md) | 自主 AI Agent 先驅專案 |
