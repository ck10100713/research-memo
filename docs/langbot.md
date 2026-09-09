---
date: "2026-09-09"
category: "AI Agent 框架"
card_icon: "material-forum-outline"
oneliner: "跟 AstrBot 同賽道的自架多平台 LLM IM 機器人平台(17.7K stars、Python、Apache-2.0),前身是 2022 年的 QChatGPT(mirai QQ bot),2024-11 的 v3.4.0 移除 Mirai、加 WebUI 後正式改名 LangBot。一套後端接 QQ/微信/企微/飛書/釘釘/Discord/Telegram/Slack/LINE/KOOK/Matrix;LLM 從 OpenAI/Anthropic/Gemini/DeepSeek/智譜/Kimi/Grok/Ollama 到一票聚合平台;最大特色是能把整段對話丟給 Dify/Coze/n8n/Langflow/DeerFlow/WeKnora/百煉/螞蟻TBox 當外部大腦(runner),插件跑在獨立 Plugin Runtime 進程(SDK 隔離),沙盒用 Box Runtime(nsjail/e2b),向量庫支援 6 種、資料庫可 PostgreSQL,還內建 /mcp server + 倉庫內 skills 讓 coding agent 直接操作機器人本身。Web 前端是 React(Vite),不是 AstrBot 的 Vue"
tags:
  - chatbot
  - llm
  - plugins
  - self-hosted
  - python
  - agent
---

# LangBot 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/langbot-app/LangBot> |
| 官方網站 | <https://langbot.app/> |
| 官方文件站 | <https://docs.langbot.app/> ｜ 特性頁 <https://langbot.app/docs/zh/insight/features> |
| 組織 | **langbot-app**(GitHub Organization);原作者 **RockChinQ**（GitCode 仍在 <https://gitcode.com/RockChinQ/LangBot>） |
| 前身 QChatGPT | 改名公告見 [Release v3.4.0](https://github.com/langbot-app/LangBot/releases/tag/v3.4.0)（2024-11-17，內文明講「从 3.4.0 版本开始，QChatGPT 更名为 LangBot」）；[一週年討論 #627](https://github.com/langbot-app/LangBot/discussions/627)（2023-12-06） |
| 插件 SDK | [langbot-plugin-sdk](https://github.com/langbot-app/langbot-plugin-sdk)（獨立 repo，PyPI 套件 `langbot-plugin`） |
| 插件/技能市集 | LangBot Space <https://space.langbot.app> ｜ 雲端版 <https://space.langbot.app/cloud> |

> Metadata（**2026-09-09** 即時抓取，取自 GitHub API 與 `git clone` 原始碼）：**17,688 stars / 1,586 forks / 119 open issues** · License **Apache-2.0**（寬鬆授權）· 建立於 **2022-12-07**（前身 QChatGPT），最後 push **2026-09-08**（每天都在動）· 預設分支 `master` · 約 **3,880 commits / 98 contributors** · 最新 release **v4.10.10**（2026-09-04；發版極頻繁，8 月底到 9 月初就跳了好幾個 patch）· repo size ≈ 57 MB · 主語言 **Python**（約 7.7M）+ **TypeScript**（約 3.1M，`web/` 前端）· 需 **Python 3.11–3.13** · README 有英/簡中/繁中/日/西/法/韓/俄/越 九種語言。官方定位改成「Production-grade platform for building **agentic** IM bots」。

!!! warning "五個要先校正的判讀"
    - **前身 QChatGPT 很容易搞混沿革**：2022-12 建立時它叫 **QChatGPT**，是一隻基於 **Mirai（YiriMirai）** 的 ChatGPT QQ 機器人。真正改名是在 **v3.4.0（2024-11-17）**——同一版**移除了 Mirai**（因為 Mirai 協議被 QQ 嚴重風控）、**加入 WebUI 管理面板**，才正式變成今天這個多平台 Agent 平台。看到網路上「QChatGPT / RockChinQ/QChatGPT / rockchin/qchatgpt(Docker)」都是它的舊身分。
    - **它跟 AstrBot 是同賽道直接對手，但授權天差地遠**：兩者都是中國、都是「自架 × 多 IM × LLM × 插件 × WebUI」。但 **LangBot 是 Apache-2.0（寬鬆，可閉源商用）**，AstrBot 是 **AGPL-3.0（強 copyleft）**——這是實務上最大的差別，想包成閉源商業產品的人幾乎只能選 LangBot。細節見〈與 AstrBot 及其他方案的差異〉。
    - **熱度 vs 定位不要混為一談**：以 star 數論，AstrBot（~40K）明顯比 LangBot（~17.7K）紅；但 LangBot 主打「生產級 / 企業級 / Agent-native」，在多租戶、獨立插件進程、PostgreSQL、多向量庫這些「上生產」的點著墨更深。star 少不等於比較弱，是兩條路線。
    - **QQ / 個人微信仍是灰色地帶**：QQ 個人號走 `aiocqhttp`（OneBot v11）接第三方協議實作、個人微信走 `wechatpad` / `openclaw_weixin` 掃碼登入——這些都非官方接口，有封號風險、踩平台條款。**框架本身乾淨，風險在你搭的那顆協議實作**。
    - **這是中國專案、原始碼與深入文件多為簡體**：程式碼註解、預設文案多是簡中（例：`# 处理器`、`# 封禁会话检查`）。官方有繁中 README，但深入設定/插件開發文件仍以簡中為主，詞彙要自己轉（訊息/伺服器/設定/外掛）。

## 專案概述

LangBot 自我定位是**「開源的生產級 AI 即時通訊機器人開發平台」**（Production-grade platform for building agentic IM bots）。一句話：**一套 Python 後端，同時掛在你常用的十幾個 IM 上，把 LLM 對話 / Agent / 知識庫 / 多模態塞進去，再用插件與外部工作流平台無限擴充——而且整包 Apache-2.0，商用門檻低。**

它的產品重心跟同賽道的 [AstrBot](astrbot.md) 有微妙差異，可以拆成三層看：

- **拿來就用的一面**：`uvx langbot` 或 Docker Compose 一鍵起，開瀏覽器進 **React 做的 WebUI**（`http://localhost:5300`），填 API key、選模型、勾平台、裝插件——不寫程式也能有一隻能對話、查知識庫、會用工具的機器人。甚至有官方 **LangBot Cloud** 免部署版與線上 demo。
- **「外部大腦」轉接器的一面**：LangBot 很強調「**不一定要用自己的 Agent**」——它可以把整段對話**原封不動丟給 Dify / Coze / n8n / Langflow / DeerFlow / WeKnora / 阿里雲百煉 / 螞蟻 TBox** 的工作流去處理，自己只當「IM 接入 + 訊息路由 + 回覆」的殼。這是它跟很多同類最不一樣的賣點：**把 LLMOps / workflow 平台當一等公民接進 IM**。
- **Agent-native 的一面**：LangBot 內建 **`/mcp` MCP Server** 與**倉庫內 `skills/` 目錄**，明確設計成「讓你的 coding agent（Claude Code / Codex / Cursor）一等公民般地操作、擴充、部署 LangBot 本身」。這層在同類專案裡相當少見（見看點 6）。

本站把它跟 AstrBot 一起歸在 **AI Agent 框架**，方便並排比較這兩個「自架多平台 LLM IM bot」龍頭。

## 8 個看點

### 1. 支援平台:一套後端掛滿十幾個 IM

原始碼 `src/langbot/pkg/platform/sources/` 底下每個檔案就是一個平台適配器（adapter），每個 adapter 都繼承 SDK 的 `AbstractMessagePlatformAdapter`，把平台事件轉成統一的 `MessageChain`。官方維護的清單：

| 分類 | 平台（原始碼檔名） |
|------|------|
| QQ 系 | `qqofficial` / `qqofficial_webhook`（QQ 官方 bot：頻道/私聊/群聊）、`aiocqhttp`（**OneBot v11**，接第三方實作玩個人號） |
| 微信系 | `wecom`（企業微信應用）、`wecombot`（企微智能機器人）、`wecomcs`（企微對外客服）、`officialaccount`（微信公眾號）、`wechatpad` / `openclaw_weixin`（**個人微信**，掃碼登入） |
| 國際 IM | `telegram`、`discord`、`slack`、`line`、`mattermost` |
| 中國協作 | `lark`（飛書）、`dingtalk`（釘釘）、`kook` |
| 通用/橋接 | `satori`（通用協議）、`matrix`（可再橋接 Signal/WhatsApp/iMessage/IRC/XMPP…）、`http_bot`（自訂 HTTP bot，有簽章）、`websocket_adapter`、`web_page_bot`（內建網頁聊天） |

README 表格另外標了 **Email（限 Matrix/Satori 橋接）**、**WhatsApp 開發中**。要新增平台就是實作 adapter 介面——這套「adapter → 統一 MessageChain → pipeline」的分層跟 AstrBot 幾乎同構。

### 2. LLM / Provider:主流 + 一票國產聚合平台都收

模型服務放在 `pkg/provider/modelmgr/requesters/`，做成可插拔的 requester（多半是 OpenAI-compatible 的 `chatcmpl` 變體）：

- **對話 LLM**：OpenAI、**Anthropic**、Google **Gemini**、DeepSeek、Moonshot（Kimi，含 `moonshotcn`）、智譜（`zhipuai`，GLM）、xAI **Grok**、Groq、Mistral、豆包（`doubao`）、火山方舟（`volcark`）、百度（`baidu`）、騰訊混元（`tencent`）、訊飛（`iflytek`）、零一萬物（`yi`）、小米 MiMo（`mimo`）、MiniMax。
- **本機部署**：**Ollama**、**LM Studio**。
- **統一閘道**：內建 **LiteLLM**（`litellmchat`）與 OpenRouter，等於「LiteLLM 支援的模型」它全吃；另有一票聚合/GPU 平台：矽基流動、阿里雲百煉、ModelScope、GiteeAI、PPIO、優雲智算、勝算雲、接口 AI、302.AI、七牛、Together、new-api 等。
- **向量 / rerank / 其他**：embedding 有 OpenAI/Chroma/seekdb 等；rerank 有 Cohere/Jina/VoyageAI；還藏了一個 `codex` requester（接 Codex）。

一句話：**主流模型 + 幾乎所有中國聚合平台 + 本地模型 + LiteLLM 兜底**，選擇面比 AstrBot 更偏「中國 API 閘道」齊全。

### 3. 與 Dify / n8n / Coze 等外部平台的整合:runner 機制(招牌賣點)

這是 LangBot 最有辨識度的設計。`pkg/provider/runners/` 裡每個檔案是一個 **RequestRunner**，pipeline 的核心處理階段會挑一個 runner 來跑對話。runner 分兩種：

- **`localagent`（原生 Agent）**：LangBot 自家的 function-calling **tool-loop**（硬上限 `MAX_TOOL_CALL_ROUNDS = 128`），會注入 RAG context、掛 `sandbox_exec`（Box 沙盒執行程式碼）等工具。
- **外部平台 runner（把對話整段轉包出去）**：`difysvapi`（**Dify**）、`cozeapi`（**Coze**）、`n8nsvapi`（**n8n**）、`langflowapi`（**Langflow**）、`deerflowapi`（**DeerFlow**）、`weknoraapi`（騰訊 **WeKnora** RAG）、`dashscopeapi`（阿里雲**百煉** App）、`tboxapi`（螞蟻 **Ant TBox**）。

也就是說——**你可以完全不用 LangBot 的 Agent，把 IM 收到的訊息丟給 Dify 的工作流、n8n 的自動化、Coze 的 bot、Langflow 的流程去處理，回覆再由 LangBot 送回 IM**。Dify runner 甚至實作了工作流「暫停等表單填寫再續跑」的狀態管理（`_PENDING_FORMS`）。這把 LangBot 變成「**任何 LLMOps / workflow 平台的多 IM 前台**」，是它跟 AstrBot 分野最清楚的一塊（AstrBot 也有 Dify/Coze/百煉/DeerFlow runner，但 LangBot 多了 n8n / Langflow / WeKnora / TBox，且把它擺在 README 最顯眼處當招牌）。

### 4. 插件系統:跑在「獨立 Plugin Runtime 進程」,不是同進程

LangBot 的插件架構跟 AstrBot 有一個關鍵不同——**插件不在主進程裡跑**。整套 API 拆到獨立 repo **`langbot-plugin-sdk`**（PyPI 套件 `langbot-plugin`，在 `pyproject.toml` 釘死版本 `0.5.7`）：

- **Plugin Runtime（`lbp rt`）**：插件在**獨立的 Runtime 進程**裡執行，主程式透過 `pkg/plugin/connector.py` 用 **stdio 或 WebSocket** 跟它通訊。本地直跑通常 stdio 起子進程；容器化/獨立部署可用 `--standalone-runtime` 走 WebSocket（`plugin.runtime_ws_url`）。
- **好處**：進程隔離 → 插件崩潰/更新不拖垮主程式，可熱重載，也比較好做資源與安全邊界。**代價**是架構較重（跨 repo、跨進程協議），開發插件要理解 SDK 的 component/action 協議。
- 插件能提供的 component：對 LLM 暴露 **Tool**（function calling）、掛 pipeline 事件（normal-message、prompt-processing…）、**KnowledgeEngine**（自訂知識庫）等。
- **插件市集**：**LangBot Space**（`space.langbot.app`），官方說法是「**數百個**社群插件」，WebUI 一鍵裝。規模上目前**小於 AstrBot 號稱的 1000+**。

### 5. Agent / 知識庫 / RAG / MCP / Box 沙盒

4.x 的重頭戲，也是它敢自稱 agentic 的底氣：

- **原生 Agent**：`localagent` runner 的 tool-loop（見看點 3），工具來源由 `pkg/provider/tools/toolmgr.py` 匯總——**原生工具 + 插件工具 + 外部 MCP server 工具 + skill 工具**四路合一。
- **MCP（兩個方向別搞混）**：① **MCP client**——`tools/loaders/mcp.py`、`mcp_stdio.py` 讓 LangBot 連外部 MCP server，把工具餵給 LLM；② **MCP server**——`/mcp` 端點（見看點 6）是給 coding agent 操作 LangBot 本身用的。ARCHITECTURE.md 特別提醒這兩個是不同 surface。
- **Box Runtime（沙盒）**：`pkg/box/` + SDK 的 `lbp box`（跑在 `:5410`）提供隔離環境跑程式碼、跑 stdio MCP server、做 skill 開發。後端有 **`nsjail_backend`（Linux namespace jail）** 與 **`e2b_backend`（E2B 雲沙盒）**——這是它對應 AstrBot「Agent Sandbox」的東西，但後端選擇更偏生產（nsjail / E2B，而非直接 Docker）。
- **知識庫 / RAG**：`pkg/rag/` + `pkg/vector/`。文件解析用 langchain 的 text-splitter + PyPDF2/python-docx/ebooklib/html2text（PDF/docx/EPUB/HTML/Markdown）。**向量庫支援 6 種**：Chroma、Milvus、pgvector、Qdrant、seekdb、Valkey Search——這點明顯比 AstrBot 的 FAISS 單一選項「更企業級」。
- **多模態**：多模態 LLM 輸入 + 圖片/語音（TTS 走插件如 FishAudio/海豚/AzureTTS，文生圖走百煉插件）。

### 6. Agent-native:內建 /mcp server + 倉庫內 skills,把「機器人平台」交給 coding agent

這是 LangBot 相當獨特、AstrBot 沒有對應物的一層。README 有整段「**為 AI Agent 而生**」：

- **`/mcp` MCP Server**：`pkg/api/mcp/server.py`，跟 HTTP API 對齊，暴露一組「curated 的 agent 專用子集」，讓 coding agent **程式化管理機器人、流水線、插件、模型**——用同一把 `api.global_api_key` 鑑權，不用登入流程。
- **倉庫內 `skills/`**：這裡的 skill **不是**給 bot 執行期用的（跟 AstrBot 那種 Anthropic 風格 documents/pdf skills 不同），而是給 **Claude Code / Codex / Cursor（以及 LangBot 自己的 Local Agent）開發與維運 LangBot 本身**用的——`langbot-dev`、`langbot-plugin-dev`、`langbot-deploy`、`langbot-testing`、`langbot-mcp-ops`、`langbot-space-ops`、`langbot-eba-adapter-dev` 等 9 個，號稱「使用 LangBot 的**唯一事實來源**」。
- **`AGENTS.md`（軟連結到 `CLAUDE.md`）+ `ARCHITECTURE.md` + `llms.txt`**：把架構、規範、「API 改了就要同步更新 MCP server 與 skills」的約定寫給 agent 看。ARCHITECTURE.md 甚至白紙黑字寫「API、MCP tools、skills 是一個系統，drift 就是 bug」。

換句話說，LangBot 不只是「能跑 Agent 的機器人」，還把**專案本身工程化成「可被 coding agent 操作的對象」**。這條思路跟本站一堆 Claude Code / skills 筆記是同一股潮流。

### 7. WebUI / 部署 / 資料庫 / 多租戶

- **WebUI**：`web/` 是 **Vite + React Router 7 + shadcn/ui + Tailwind CSS + pnpm** 的 SPA（ARCHITECTURE.md 特別澄清「**不是 Next.js**，別被歷史檔名騙了」）。後端用 **Quart + Hypercorn**（ASGI）在 `:5300` 同時提供 HTTP API、MCP server 與打包好的前端。**這跟 AstrBot 的 Vue 前端是明顯技術棧差異。**
- **部署**：①`uvx langbot`（一鍵 CLI）；②**Docker / Docker Compose**（`--profile all`）；③一鍵雲端 **Zeabur / Railway**；④手動 / 寶塔面板 / **Kubernetes**；⑤官方託管 **LangBot Cloud**。
- **資料庫**：預設 **SQLite**（`aiosqlite` + SQLAlchemy/SQLModel + **Alembic** migration），**正式支援 PostgreSQL**（`asyncpg` + `pgvector`）。這點跟 AstrBot（SQLite-only）不同，是為「上規模」準備的。
- **多租戶 / 多流水線**：原始碼有 `pkg/workspace/`、`docs/multi-tenant/`、service 層的 `TenantContext` / `require_workspace_uuid`——LangBot 支援 **Workspace 多租戶** 與 **多流水線（一個實例跑多條 pipeline、不同機器人用不同場景）**，明顯往企業/SaaS 場景鋪路。

### 8. Pipeline 架構:訊息事件怎麼流過各階段

LangBot 用 **QueryPool + Controller + 責任鏈式 pipeline** 處理每則訊息。訊息從 adapter 進來 → `RuntimeBot`（套路由規則）→ `MessageAggregator`（批次/正規化）→ `QueryPool` → `Controller`（控全域與 per-session 併發）→ `RuntimePipeline` 依設定跑各 stage。預設階段順序寫在 `pkg/api/http/service/pipeline.py::default_stage_order`：

```text
收到訊息(adapter → 統一 MessageChain → QueryPool → Controller)
  ↓
1. GroupRespondRuleCheckStage   群響應規則(要不要回)
2. BanSessionCheckStage         封禁/黑名單會話檢查
3. PreContentFilterStage        內容過濾(前置)
4. PreProcessor                 預處理
5. ConversationMessageTruncator 會話訊息截斷(控 context 長度)
6. RequireRateLimitOccupancy    佔用限流額度
7. MessageProcessor             ★ 核心:挑 runner 呼叫 LLM/Agent/外部平台、發插件事件
8. ReleaseRateLimitOccupancy    釋放限流額度
9. PostContentFilterStage       內容過濾(後置)
10. ResponseWrapper             回應包裝
11. LongTextProcessStage        長文本處理(轉圖片/檔案)
12. SendResponseBackStage       送回原平台
```

責任分得很乾淨：群回應判定、黑名單、內容安全、限流這些「橫切關注點」都在核心處理之外統一做掉，插件只需專注第 7 階段。**這條 pipeline 跟 AstrBot 的分階段 pipeline 是同一個架構思想**（先把「每個訊息都要做的事」排成有序 stage，再讓擴充點插進中間），差別在 LangBot 每條 pipeline 是**設定驅動、可多條並存**。

## 授權與商用可行性

- **License 是 Apache-2.0**——寬鬆授權。**可以閉源、可以商用、可以改了不開源、可以包成 SaaS**，只要保留授權聲明與 NOTICE、標示改動即可。**這跟 AstrBot 的 AGPL-3.0（改了拿去做網路服務就要開放完整原始碼）是本質差異**，也是「想拿它做商業產品」時 LangBot 幾乎是唯一合理選擇的原因。
- `pyproject.toml` 的 classifiers 直接標 **`Development Status :: 5 - Production/Stable`**，官方也說「已被多家企業採用」——它是刻意往「可商用、可上生產」定位的。
- **實務結論**：個人、社群、企業內部、對外商業產品自架 → **授權上全部 OK 且免費**。真正要留意的合規風險不在 License，而在**你接的那些平台**：QQ 個人號（第三方 OneBot 實作）、個人微信（掃碼登入）都非官方接口，有封號與踩條款風險；插件市集的第三方插件也是自負風險。

## 與 AstrBot 及其他方案的差異

先講最重要的一句：**LangBot 與 [AstrBot](astrbot.md) 是同一賽道最像的一對直接對手**（都是中國、都自架、都「多 IM × LLM × 插件 × WebUI」）。真正要選邊，看下面這張表：

| 面向 | **LangBot** | [AstrBot](astrbot.md) | NoneBot2 | [LobeHub](lobehub.md) |
|------|-------------|-----------------------|----------|-----------------------|
| 定位 | 生產級 IM bot 平台，強調 agentic / 多租戶 / 可商用 | 電池全含、社群生態最大 | 純 Python bot 框架 | Web 端多 Agent 工作空間 |
| **License** | **Apache-2.0（寬鬆，可閉源商用）** | **AGPL-3.0（強 copyleft）** | MIT | 自訂(Other) |
| Stars / 熱度 | ~17.7K | **~40.2K（更紅）** | 大(老牌) | ~74K |
| 資歷 | 2022-12 建立（前身 **QChatGPT**，Mirai QQ bot），2024-11 v3.4 改名 | 2022-12 建立 | 更老 | 較新 |
| 招牌能力 | **把對話轉包給 Dify/n8n/Coze/Langflow/DeerFlow/WeKnora/百煉/TBox**；**/mcp + 倉庫內 skills 讓 coding agent 操作 bot 本身** | 1000+ 插件、Agent Sandbox、Anthropic 風格 Skills、混合式 RAG | 什麼都自己寫 | 網頁多 Agent 協作 |
| 插件架構 | **獨立 Plugin Runtime 進程**（SDK 隔離，stdio/WS） | in-process **Star**（同進程） | 純框架 | — |
| 插件市集規模 | LangBot Space「數百個」 | **1000+（更大）** | — | — |
| 沙盒 | Box Runtime（**nsjail / E2B** 後端） | Agent Sandbox（aiodocker） | — | — |
| 向量庫 | **6 種**（Chroma/Milvus/pgvector/Qdrant/seekdb/Valkey） | FAISS | — | — |
| 資料庫 | SQLite 預設，**正式支援 PostgreSQL** | SQLite | — | 常需 PostgreSQL |
| Web 前端 | **React（Vite + React Router 7 + shadcn/ui）** | **Vue + TypeScript** | — | Next.js |
| 多租戶 | **有（Workspace）+ 多流水線** | 單租戶為主 | — | 有 |

三個最關鍵的分野：

1. **授權（最重要）**：LangBot **Apache-2.0** vs AstrBot **AGPL-3.0**。要閉源、要包商業產品、要做 SaaS 又不想開源 → 幾乎只能選 LangBot。純自架自用兩者都免費，這時授權差異對你無感。
2. **Agent-native「向內」的程度**：LangBot 把**平台自己**工程化成 coding agent 可操作的對象（`/mcp` server + 倉庫內 dev/ops skills + `AGENTS.md`）；AstrBot 的 Agent/Skills 主要是**讓 bot 在執行期更能幹活**。一個是「讓 AI 幫你維運這台機器人」，一個是「讓這台機器人更會用 AI」。
3. **路線取向**：LangBot 偏「**生產/企業**」——獨立插件進程、多租戶、PostgreSQL、6 種向量庫、把 workflow 平台當一等公民；AstrBot 偏「**社群/生態最大、電池全含**」——插件與平台數量、Sandbox+Skills 深度、star 熱度都領先。

跟其他方案：**對比 NoneBot2**——NoneBot 給你螺絲起子（LLM/WebUI/RAG 全自己搭），LangBot 是整台車開走。**對比 [LobeHub](lobehub.md)**——LobeHub 是「打開網頁跟 Agent 工作」，LangBot 是「機器人住進你的 QQ/Telegram 群」，入口面完全不同。

## 注意事項與已知限制

1. **QQ 個人號 / 個人微信的合規風險在第三方協議**：走 `aiocqhttp`(OneBot) 接第三方實作、或 `wechatpad`/`openclaw_weixin` 掃碼登入的個人號，都非官方接口，有封號與踩條款風險。要穩就用官方 bot（QQ 官方、企微、公眾號、飛書、釘釘），但功能受限。
2. **插件生態與熱度目前小於 AstrBot**：星數約一半、插件市集「數百 vs 1000+」。要「裝現成插件解決需求」的廣度，AstrBot 目前佔優。
3. **架構較重**：插件跨 repo（`langbot-plugin-sdk`）、跨進程協議、Box Runtime、多租戶——功能強大但心智負擔高，寫插件/改核心要先讀 `ARCHITECTURE.md` 與 SDK。
4. **發版極快、跨大版本有重整**：從 QChatGPT 3.x → LangBot 3.4（移除 Mirai）→ 4.x，架構重整過數次（persistence 有「凍結的 3.x legacy migration baseline + Alembic」兩段式 migration）。升級大版本要看 changelog。
5. **第三方插件不背書**：市集插件官方不審計，裝 = 給它跑你機器人的權限，尤其搭 Box 沙盒能執行程式碼，要慎選來源。
6. **簡中為主 + 依賴外部模型 API**：深入文件多簡中；本身不含推理能力，LLM/TTS/STT 的可用性與費用都看你接的 provider。

## 研究價值與啟示

### 關鍵洞察

1. **「IM 前台 × 外部 workflow 大腦」是被驗證、且比自寫 Agent 更務實的產品形態**：LangBot 的 runner 機制讓你**把對話整段轉包給 Dify/n8n/Coze/Langflow/DeerFlow**——很多團隊本來就在這些平台上編排流程，LangBot 直接把它們接到十幾個 IM 上。想做「讓現有工作流長出聊天入口」，這套 runner 抽象非常值得抄。可搭 [n8n-workflows](n8n-workflows.md)、[deer-flow](deer-flow.md) 一起看。

2. **同一個「adapter → 統一訊息 → 分階段 pipeline」架構，被 LangBot 與 [AstrBot](astrbot.md) 各自獨立驗證了一遍**：兩個龍頭的核心分層幾乎同構（平台適配器統一成內部訊息模型、責任鏈 pipeline 把橫切關注點抽離、擴充點插在核心處理階段）。這幾乎是「跨平台 IM bot 平台」的架構共識——這正是把 [line-chatbot-boilerplate](line-chatbot-boilerplate.md) 那種單平台 boilerplate 放大十幾倍的樣子。

3. **Apache-2.0 vs AGPL-3.0，是同賽道兩強最現實的差異化槓桿**：LangBot 用寬鬆授權 + 「Production/Stable」+ 多租戶 + PostgreSQL，明確卡「可商用/企業/SaaS」這一格，跟 AGPL 的 AstrBot 做出區隔。做開源專案在選授權時，這組對照是很好的教材：**授權不只是法律問題，是產品定位與目標客群的選擇**。

4. **把「專案本身」做成 coding agent 可操作的對象，是一條正在成形的新工程實踐**：`/mcp` server + 倉庫內 dev/ops skills + `AGENTS.md` + 「API/MCP/skills 是一個系統、drift 就是 bug」的約定——LangBot 等於示範了「**agent-friendly repo**」該長什麼樣。這跟本站大量 Claude Code / skills 筆記是同一股潮流的另一端（不是用 agent 寫別的專案，而是**把自己的專案交給 agent**）。

5. **插件跑獨立進程 vs 同進程，是「隔離/穩定」對「輕量/生態」的經典取捨**：LangBot 選了較重的獨立 Plugin Runtime（隔離、熱重載、好上生產），AstrBot 選了同進程 Star（輕、生態大、上手快）。要設計外掛系統時，這一對是很好的正反面案例。

### 與其他研究筆記的關聯

- **[AstrBot](astrbot.md)**：**最直接的對照組**，同賽道最像的對手。務必並排讀——授權（Apache vs AGPL）、熱度、插件架構（獨立進程 vs 同進程）、向量庫（6 種 vs FAISS）、前端（React vs Vue）、多租戶有無，都是清楚的分歧點。
- **[n8n-workflows](n8n-workflows.md)** / **[deer-flow](deer-flow.md)**：LangBot 的招牌是把對話轉包給這類 workflow / research agent 平台；想理解「外部大腦」那端在做什麼，讀這兩篇。
- **[line-chatbot-boilerplate](line-chatbot-boilerplate.md)** 與 **[linebot-multimodal-rag](linebot-multimodal-rag.md)**：單平台（LINE）bot 的起手式與多模態 RAG 版——LangBot/AstrBot 是把這件事做成通吃十幾個平台的框架版，對照可看「單點方案 → 通用平台」的演化。
- **[litellm](litellm.md)**：LangBot 直接把 LiteLLM 當成一個 requester 內建進來（統一各家 LLM），可對照「多模型統一介面」的兩種落地（自建抽象 vs 直接用 LiteLLM）。
- **[mcp-for-beginners](mcp-for-beginners.md)**：LangBot **同時是 MCP client（連外部工具）與 MCP server（讓 agent 操作自己）**，是理解 MCP 雙向角色的好實例。
- **[rag-anything](rag-anything.md)** / **[graphrag](graphrag.md)**：想把 LangBot 內建那套（6 種向量庫）RAG 換成更強方案時的進階參考。
- **[gemma-4-local-llm](gemma-4-local-llm.md)**：LangBot 支援 Ollama/LM Studio 本機模型，想做「全本地、不出網」的 bot 可搭這篇。
- **[lobehub](lobehub.md)**：另一種「自架 LLM 平台」的產品形態（web-first 多 Agent 工作空間），跟 LangBot/AstrBot 的 IM-first 並排看能看清入口面差異。

## 一句話總結

> LangBot 是跟 [AstrBot](astrbot.md) 同賽道、17.7K 星的**自架多平台 LLM IM 機器人平台**：前身是 2022 年的 **QChatGPT**（Mirai QQ bot），2024-11 的 **v3.4.0** 移除 Mirai、加 WebUI 後正式改名。一套 Python 後端掛滿 QQ/微信/企微/飛書/釘釘/Discord/Telegram/Slack/LINE/KOOK/Matrix，LLM 從 OpenAI/Anthropic/Gemini 到 DeepSeek/智譜/Kimi/Grok/Ollama 再到一票中國聚合平台與 LiteLLM 兜底。它最有辨識度的兩件事：**能把整段對話轉包給 Dify/Coze/n8n/Langflow/DeerFlow/WeKnora/百煉/TBox 當外部大腦**，以及**內建 `/mcp` server + 倉庫內 skills 讓 coding agent 直接操作機器人本身**。插件跑在獨立 Plugin Runtime 進程、沙盒用 Box（nsjail/E2B）、向量庫支援 6 種、資料庫可上 PostgreSQL、前端是 React（不是 AstrBot 的 Vue）。跟 AstrBot 最關鍵的差別是 **Apache-2.0（可閉源商用）vs AGPL-3.0**——這也是它主打「生產級 / 企業級 / 可商用」的底氣所在。
