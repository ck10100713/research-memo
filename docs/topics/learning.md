# 學習資源

本分類收錄 27 篇研究筆記。

| 日期 | 筆記 | 摘要 |
| --- | --- | --- |
| 2026-09-23 | [AI Engineering Interview Questions Company Wise](../ai-engineering-interview-questions-company-wise.md) | Outcome School 整理的 AI 工程師面試題庫，按 35 家公司分區(Anthropic、OpenAI、Cursor、Palantir…)，每家附面試流程；約 600 題、四成附答案，但答案全連回作者自家部落格，題目也沒標出處 |
| 2026-09-16 | [ccc115a/se `_more/mybook` 三本書](../ccc115a-se-mybook.md) | 金門大學資工系陳鍾誠教授 115 學年上學期《現代軟體工程》課程 repo（MIT、30★）裡藏的 `_more/mybook`——三本各自寫完整的繁體中文技術書草稿，共 216 個分節 Markdown、約 198K 漢字、256 個 mermaid 圖：《現代軟體工程：從基礎到 AI Agent 實踐》（87 節，三篇 14 章 + 附錄 ABC，明講參考李博杰 agent-book）、《演進式架構實戰》（75 節，用淘寶 14 次架構演進當問題驅動主線）、《從 Docker 到 Kubernetes：Rust × WebSocket/SSR/MPA 實戰》（46 節）。每節一檔、靠 README 當目錄，本筆記附上把它們合併成單一本書的方法與腳本 |
| 2026-09-15 | [《深入理解 AI Infra》(ai-infra-book)](../ai-infra-book.md) | 李博杰《深入理解 AI Agent》的姊妹作《深入理解 AI Infra：量化分析與系統設計》——開站 3.5 週 2.6K★、Apache-2.0 全書開源。核心命題：模型成了 LLM 時代的作業系統，AI Infra 成了 LLM 時代的計算機體系結構。方法論明著對標《計算機體系結構：量化研究方法》，12 章都從硬體約束量化推導系統設計，全書追問同五個問題：搬什麼、搬多少、搬幾次、經過哪裡、誰必須等它。附一個只靠 Python 標準庫、不用 GPU 就能複算全書數字的 CLI |
| 2026-09-15 | [MiniMind](../minimind.md) | 61K★、Apache-2.0 的「從 0 訓練一個小 LLM」教學專案——單張 3090、約 2.3 小時、約 3 塊人民幣就能把 64M 參數的 minimind-3 從預訓練練到會對話。關鍵訓練演算法與核心模組全部從 0 實現不依賴框架封裝，但結構對齊 Qwen3 生態、可轉 transformers/llama.cpp/ollama。涵蓋 Pretrain→SFT→LoRA→DPO→RLAIF(PPO/GRPO/CISPO)→Tool Use→Agentic RL 完整鏈路 |
| 2026-09-11 | [《深入理解 AI Agent》(ai-agent-book)](../ai-agent-book.md) | 前華為『天才少年』、Pine AI 首席科學家李博杰寫的《深入理解 AI Agent:設計原理與工程實踐》——45.7K★、Apache-2.0『整本書免費開源』(正文 + PDF/EPUB + 109 個配套實驗全放 GitHub)。以核心公式 Agent = LLM + 上下文 + 工具 用十章從原理講到生產:上下文工程(KV Cache/Skills/壓縮)、用戶記憶與 RAG、工具與 MCP、Coding Agent、語音/Computer Use/機器人交互、評估、模型後訓練(SFT/RL)、持續進化、multi-agent。用 whisper coding 口述式協作寫成,15 種語言,含繁體中文台灣版 |
| 2026-08-20 | [awesome-agentic-ai-zh](../awesome-agentic-ai-zh.md) | 繁中為 canonical 的 AI Agent 學習地圖：8 階段 + 雙軌（CLI 使用者 / Agent 建構者）+ 240+ 資源策展 + 23 個動手練習，6k stars |
| 2026-07-28 | [GenAI Agents (NirDiamant)](../genai-agents.md) | 23.5k ★、53 本可跑的 agent 教學 notebook，從對話機器人到多代理系統——但授權是「非商業限定 + 投稿者交出商業權利」的自訂條款，不是開源；且 requirements.txt 凍結在 2024-09，約三分之二內容其實是 LangGraph 應用集 |
| 2026-06-05 | [The System Design Primer](../system-design-primer.md) | GitHub 35 萬星的系統設計入門聖經：可擴展系統原理 + 面試題解 + Anki 卡片 |
| 2026-05-28 | [skillopt-qa](../skillopt-qa.md) | joshhu 對 Microsoft SkillOpt 的精簡忠實重現版，針對 HotpotQA 多跳問答，用 ~9 個檔案講清「文字空間優化器」全貌，含真實 Qwen3.6-27B 實驗結果（種子→優化 test F1 0.8424→0.8524），離線測試零網路 |
| 2026-05-15 | [Claude Code 最佳實踐完整研究報告（zeuikli）](../zeuikli-claude-code-best-practices.md) | zeuikli 整理 29 篇 best-practices + 52 篇 Claude blog 的 Claude Code 九面向最佳實踐總報告，含 CLAUDE.md、Hook、Cache、Subagent、Skill、MCP、安全、Routines、成本工程 |
| 2026-05-14 | [AI Agents for Beginners](../ai-agents-for-beginners.md) | Microsoft 官方 12 (+6) 課 AI Agent 入門課，以 Microsoft Agent Framework + Azure AI Foundry V2 為主軸，61k stars、50+ 語言 |
| 2026-04-24 | [MCP for Beginners](../mcp-for-beginners.md) | 微軟官方 MCP 入門課程，12 模組 × 6 種語言 (.NET / Java / JS / TS / Python / Rust)，對齊 MCP 規範 2025-11-25，模組 11 含 13 個 PostgreSQL 整合實作實驗室，20 天衝到 15.9K stars |
| 2026-04-17 | [Anthropic Claude Cookbooks — 40.8K stars 的官方範例庫](../claude-cookbooks.md) | Anthropic 官方 40.8K stars 的 Claude 食譜庫，從 RAG 到 Managed Agents 的完整可執行範例 |
| 2026-04-16 | [reverse-SynthID](../reverse-synthid.md) | 逆向工程 Google SynthID 圖像浮水印 — 頻譜分析發現載波結構，90% 偵測率 + 91% 相位去除 |
| 2026-04-15 | [AI Engineering from Scratch](../ai-engineering-from-scratch.md) | 從零學 AI 工程 — 20 Phases、260+ 課、290 小時，從數學到多 Agent Swarm 全覆蓋 |
| 2026-04-15 | [dotLLM](../dotllm.md) | 用純 C#/.NET 10 從零打造 LLM 推論引擎 — Zero-GC、SIMD、CUDA、Paged KV-cache |
| 2026-04-15 | [OpenAI: A Practical Guide to Building Agents](../openai-practical-guide-building-agents.md) | OpenAI 官方 34 頁 Agent 建構指南 — 定義、設計基礎、編排模式、護欄，從客戶部署提煉的最佳實踐 |
| 2026-04-12 | [Claude Code from Source — 逆向工程架構全書](../claude-code-from-source.md) | 18 章深度逆向工程 Claude Code 架構 — 從 npm source map 解析 2,000 個 TypeScript 檔案 |
| 2026-04-09 | [DeepTutor](../deep-tutor.md) | 港大 HKUDS 開源 AI 學習助理 — RAG 知識庫 + 多 Agent 解題 + TutorBot 自主家教 + CLI 原生 |
| 2026-04-02 | [Gemma 4 與 Local LLM](../gemma-4-local-llm.md) | Google Gemma 4 模型全解析 + 2026 Local LLM 推論工具對比（Ollama / llama.cpp / vLLM / LM Studio） |
| 2026-04-02 | [Karpathy LLM Wiki](../karpathy-llm-wiki.md) | Karpathy 提出的 LLM 知識庫模式 — 用 AI Agent 編譯、維護持久化 Markdown Wiki，取代傳統 RAG |
| 2026-03-31 | [Learn Claude Code](../learn-claude-code.md) | 44K stars 的 Agent Harness 工程教科書——12 個漸進 Session 從 1 個 loop + Bash 到 worktree 隔離多 Agent 協作，附 Next.js 互動學習平台 |
| 2026-03-31 | [LY Corp — Google ADK 入門：打造 AI Agent 與多代理人系統](../ly-corp-adk-agent.md) | LY Corporation 技術部落格 — Google ADK 入門系列，從單一 Agent 到多代理人系統的實戰教學 |
| 2026-03-30 | [Claude Use Cases Gallery](../claude-use-cases.md) | Anthropic 官方 Use Cases 資料庫——13 行業 × 7 功能 × 4 產品線，從 Cowork 桌面代理到法務合約紅線的全景案例集 |
| 2026-03-23 | [AI Agents (黃佳)](../ai-agents.md) | 《動手做AI Agent》書籍配套程式碼與教學 |
| 2026-03-23 | [LLM Course](../llm-course.md) | LLM 學習課程資源 |
| 2026-03-23 | [Reference 快速參考手冊](../reference.md) | 常用參考手冊 |
