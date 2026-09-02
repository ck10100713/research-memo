---
date: "2026-08-20"
category: "學習資源"
card_icon: "material-map"
oneliner: "繁中為 canonical 的 AI Agent 學習地圖：8 階段 + 雙軌（CLI 使用者 / Agent 建構者）+ 240+ 資源策展 + 23 個動手練習，6k stars"
tags:
  - learning
  - agent-framework
  - mcp
---

# awesome-agentic-ai-zh 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/WenyuChiou/awesome-agentic-ai-zh> |
| 線上文件站 | <https://wenyuchiou.github.io/awesome-agentic-ai-zh/> |
| 三語版本 | 繁中（canonical）/ 简中（README.zh-Hans.md）/ English（README.en.md） |
| 維護者 | [@WenyuChiou](https://github.com/WenyuChiou)（Wenyu Chiou，博士生；顧問聯絡 wenyuchiou12@gmail.com） |
| 創建時間 | 2026-05-04（約 3.5 個月累積 6k stars） |
| 規模 | 6,047 stars / 807 forks / 25 watchers / MIT / 主要語言 Python（2026-08-20 抓取，最後 push 2026-08-19） |
| 靈感來源 | Datawhale [hello-agents](https://github.com/datawhalechina/hello-agents)（章節結構）、[liyupi/ai-guide](https://github.com/liyupi/ai-guide)（廣度資源庫） |

## 專案概述

**awesome-agentic-ai-zh** 是一份**結構化 AI Agent 學習地圖**，作者自己把定位講得很清楚：**學習路線圖 + 240+ 資源策展 + 簡單 illustrative 案例**三件事為核心，目標是帶人從「不知道從哪開始」走到「能設計多 agent 系統、能寫自己的 MCP server」。

跟一般 `awesome-*` 清單最大的不同是**它有學習順序**——不是一堆連結攤平列出，而是把散落的高品質專案、教材、必修閱讀，按「從零開始、循序漸進」編成 **8 個階段（Stage 0-8）+ 2 條學習路徑 + 5 條延伸路線**。作者在致謝裡直接對比：`wong2/awesome-mcp-servers`、`hesreallyhim/awesome-claude-code` 是「純清單、看到再挑」，本 repo 的差異點是「**從 Stage 0 一路走到 production 的學習順序**」。

最值得台灣讀者注意的一點：**繁體中文是 canonical 版本**，簡中與英文都是從繁中衍生而非反過來。中文圈的 AI 教材（Datawhale、liyupi/ai-guide 等）幾乎清一色簡中優先，這份是少見「繁中母本 + 三語皆完整維護、英文非薄翻譯」的資源。

### 中英術語處理

刻意保留領域常見英文術語（Prompt Engineering / Context Engineering / Harness / MCP / Skills / RAG），每個重要概念給 **中文理解名 + 英文正式術語 + 一句白話定位**，完整對照放 `resources/glossary.md`（30+ 詞）。理由是官方文件、paper、API 文件多以英文為主，先懂概念再對接英文生態。

## 學習地圖：雙軌設計

走完 **Stage 0-2（共用基礎）** 後，依目的選一條 track，兩條不互斥：

### 共用基礎（Stage 0-2）

| Stage | 主題 | 關鍵內容 | 時程 |
|---|---|---|---|
| **0** | 基礎準備 Foundations | Python · CLI · git · API · JSON | 1-2 週 |
| **1** | LLM 基礎 | token · API · 各家 LLM 比較 · 本地 LLM | 1 週 |
| **2** | Prompt 設計 | 系統 prompt · few-shot · CoT | 1-2 週 |

### Track A — CLI Power User（想「用」現成 CLI agent）

| Stage | 主題 | 關鍵內容 |
|---|---|---|
| **A1** | 選一個 CLI Agent 開始用 | 8 主流 CLI 比較 · 安裝 · 第一次跑 |
| **A2** | 可重複的 CLI 工作流程 | CLAUDE.md · slash command · 多步驟拆解 |
| **A3** | 接進真實工作流程 | MCP 接 CLI · CI 自動化 · cost / observability |

> **Track A 總時程 ≈ 8-10 週**（含 Stage 0-2 + A1-A3 + 兩個共用 hub Stage 5、Stage 8）

### Track B — Agent Builder（從零「打造」agent）

| Stage | 主題 | 關鍵內容 |
|---|---|---|
| **3** ⭐ | 工具使用與第一個 Agent | function calling · ReAct · 5 個動手練習 |
| **4** | Agent 框架 | LangGraph · AutoGen · CrewAI · Smolagents |
| **5** ⭐⭐ | **Claude Code 生態系（共用 hub）** | MCP · Skills · Plugins · Subagents |
| **6** | 上下文管理：RAG 與 Memory | vector DB · long-term memory · contextual retrieval |
| **7** | 多 Agent 系統與穩定運作 | orchestration · eval · observability · SDK 進階 |
| **7.5** | 進階 Agentic 概念（reading map，不寫 code）| 工作邊界 · PAR loop · agent-as-judge · 12 概念 |
| **8** ⭐⭐ | **Agent 操作介面（共用 hub）** | Computer Use · Browser Use · Code Sandbox |

> **Track B 主幹 ≈ 16-22 週、現實 5-7 個月**（每週 5-8 hr 兼職）

**兩個共用 hub 是設計亮點**：Stage 5（Claude Code 生態）與 Stage 8（Agent Interfaces）在兩條 track 都會用到,但**視角不同**——Track A 學「怎麼用」委派任務,Track B 學「怎麼 build」embed 進 agent,內文分視角撰寫。

### 5 條延伸路線（走完主幹後依身分分流）

研究人員 · 開發者 · 教師 · 知識工作者 · **日常使用者**（這條不必走完主幹即可讀，給「想用 AI 但不寫 code」的人）。

## 內容規模與資源

| 類型 | 規模 | 位置 |
|---|---|---|
| 精選 projects | **240+**（附星等、適合誰、教什麼、怎麼跑，含 Ollama / llama.cpp / LocalAI / MLX 本地執行） | 各 stage 內 |
| MCP / Skill 目錄 | **79+ 條、16 大分類**（含 DeepSeek / Zhipu / Kimi 等中文 AI 生態） | `resources/mcp-skills-catalog.md` |
| 動手練習 folder | **23 個**（70-150 行 starter + dual-path Ollama/Anthropic SDK 對照 + mock-based test） | `examples/` |
| 術語表 | 30+ 詞 | `resources/glossary.md` |
| Cookbook recipe | 6 個 step-by-step（Skill / MCP server / 接 Word / Zotero / 本機 LLM，各 30-50 分） | `resources/cookbook.md` |
| Subagent 派工 recipe | 15 個複製貼上即用 + 進階 composition/debug | `resources/subagent-cookbook.md` |
| 跨 stage 完整範例 | 「7 步打造第一個 AI Agent」（同一個 Paper Summary Bot 從 Stage 1 寫到 Stage 7，~300 行） | `walkthroughs/` |

## 研究價值與啟示

### 關鍵洞察

1. **「路線圖」而非「清單」是這份的核心差異化**：AI 資源類 repo 早已飽和（awesome-mcp-servers、awesome-claude-code 遍地都是），這份靠「**有學習順序 + 時程估計 + 練習 gate**」殺出——它賣的不是連結,是「該用什麼順序讀這些連結」。這是**資源型內容產品**在 2026 的分水嶺:單純聚合已無價值,策展順序與 learning path 才是護城河。

2. **雙軌（用 vs 建）分流精準命中真實使用者結構**：多數 agent 教材預設「你要從零寫 agent」，但現實中絕大多數人只想把 Claude Code / Codex / Gemini CLI 用順（Track A）。把「CLI Power User」獨立成一條 8-10 週的完整 track、還配 5 條含「日常使用者」的延伸路線，反映作者看清了「**會用 > 會建**」才是市場多數。值得對照 [[ai-agents-for-beginners]]（Microsoft，預設你要 build）的教法差異。

3. **5 層工程分工是全 repo 最有價值的心智模型**：`prompt engineering`（Stage 2，單一 prompt）→ `context engineering`（Stage 3+，動態組 system prompt + memory + retrieved chunks + tool schema）→ `harness engineering`（Stage 7，agent loop / eval / observability / deploy 包成 production）→ 2026 後再往外接 `loop`（讓它自己跑完）與 `graph`（把流程攤開）。這條分層直接呼應 [[harness-design-long-running-apps]] 與 [[why-your-ai-is-dumbing-down]] 的核心論點——context 操作已從「prompt 工程副題」升格為獨立工程層。

4. **繁中 canonical 是稀缺定位**：中文 AI 教材幾乎都是簡中母本（Datawhale、liyupi/ai-guide），這份反過來以繁中為母本、英文非薄翻譯。對台灣 / 香港的自學者與教育者，這是少數能直接用母語讀、術語又對得上英文生態的路線圖。

5. **練習設計的反模式提醒很誠實**：作者明說 `starter.py` 是**完整解答不是 TODO skeleton**，若 clone 下來直接 `cat + python test.py` pass 會誤以為學會了；正確用法是 `mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫。這種「防止 passive learning」的方法論（`docs/HOW_TO_USE.md`）在教材裡很少見。

6. **維護基建像產品在做**：新增 project 連結有 GitHub Action 自動留言 star/license/封存/最後更新並對照策展標準；`CHANGELOG.md` 記最近 14 天 ship；有 style-guide、CONTRIBUTORS 分 stage/branch maintainer。對「想把知識庫做成可持續開源專案」的人是可對標的運營範本——本 [[skill-research]] 研究筆記產生器與 research-memo 本身都可借鏡其策展自動審核流程。

### 與其他研究的關聯

- 與 [[ai-agents-for-beginners]]（Microsoft）：兩者都是 8+ 階段 agent 入門，但取向相反——Microsoft 綁 MAF + Azure Foundry、預設你要 build；這份繁中母本、雙軌含「只想用 CLI」的 Track A。並排讀可看「雲端原生派 vs 開源中立派」的教法差異。
- 與 [[ai-agents]]（黃佳）、[[genai-agents]]（NirDiamant）：三份都是 agent 入門教材，這份的獨特處是「學習順序 + 時程 + 練習 gate」而非章節書或範例集。
- 與 [[mcp-for-beginners]]、[[claude-agent-sdk]]：Stage 5 的 Claude Code 生態（MCP / Skills / Plugins / Subagents）是這兩者的入口與導覽層，深入版轉去對應官方教材。
- 與 [[open-source-agent-frameworks]]、[[langgraph-multi-agent]]、[[crewai]]：Stage 4 框架巡覽（LangGraph / AutoGen / CrewAI / Smolagents）是這些深入筆記的上游地圖。
- 與 [[rag-anything]]、[[graphrag]]：Stage 6（RAG 與 Memory）是這兩份 RAG 框架研究的概念前置。
- 與 [[opencode]]、[[copilot-cli]]、[[claude-code-showcase]]：Track A 的「8 家 CLI agent 對照」（`resources/cli-agents-guide.md`）是這些 CLI 工具筆記的橫向比較框架。
- 與 [[harness-design-long-running-apps]]、[[why-your-ai-is-dumbing-down]]：Stage 7 的 harness engineering 與 5 層工程分工，是這兩份 context/harness 論述的教學化落地版本。
