---
date: "2026-09-08"
category: "AI Agent 框架"
card_icon: "material-robot-happy"
oneliner: "中國社群最紅的自架多平台 LLM 聊天機器人平台/框架(40.2K stars、Python、AGPL-3.0)。一套後端同時接 QQ/OneBot、Telegram、企業微信、飛書、釘釘、微信公眾號、Slack、Discord、LINE、KOOK 等十幾個 IM;LLM 支援 OpenAI/Anthropic/Gemini/DeepSeek/智譜/Kimi/Grok/Ollama 及 Dify/Coze/百煉 Agent 平台;插件叫「Star」,插件市場 1000+ 個一鍵裝;內建原生 Agent + MCP + 函式呼叫 + Anthropic 風格 Skills + Agent Sandbox(Docker 隔離跑程式碼)+ 混合式 RAG 知識庫 + STT/TTS 多模態 + Vue WebUI。uv/Docker/一鍵雲端都能裝,資料庫用 SQLite+FAISS"
tags:
  - chatbot
  - llm
  - plugins
  - self-hosted
  - python
  - mcp
---

# AstrBot 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/AstrBotDevs/AstrBot> |
| 官方網站 | <https://astrbot.app/> |
| 官方文件站 | <https://docs.astrbot.app/> |
| Blog / 路線圖 | <https://blog.astrbot.app/> ｜ <https://astrbot.featurebase.app/roadmap> |
| 組織 | **AstrBotDevs**(GitHub Organization,原作者 Soulter);Docker image `soulter/astrbot` |
| 生態周邊 | [AstrBot-desktop](https://github.com/AstrBotDevs/AstrBot-desktop)(桌面版)、[astrbot-launcher](https://github.com/Raven95676/astrbot-launcher)(啟動器) |

> Metadata(**2026-09-08** 即時抓取,取自 GitHub API 與 `git clone` 原始碼):**40,200 stars / 2,889 forks / 1,480 open issues** · License **AGPL-3.0-or-later**(另附一份 `EULA.md` 使用條款)· 建立於 **2022-12-08**,最後 push **2026-09-08**(每天都在動)· 預設分支 `master` · 約 **5,200 commits / 350+ contributors** · 最新 release **v4.28.0**(2026-09-07,另有 `v4.28.0-beta.1`)· repo size ≈ 73 MB · 主語言 **Python**(約 7.5M,佔絕大多數),`dashboard/` 前端是 **Vue**(約 2.3M)+ TypeScript · 需要 **Python 3.12+** · 插件市場號稱 **1000+** 個插件。README 有簡中/英/日/法/西/俄/繁中七種語言。

!!! warning "四個要先校正的判讀"
    - **「插件」在 v4.0 後官方改叫 `Star`**:原始碼裡 `astrbot/core/star/`、handler 叫 `star_handler`,但對外文件與插件市場仍講「插件」。看到 Star 就是插件,別以為是另一個概念。
    - **QQ 支援有灰色地帶,要分清楚**:AstrBot 官方只對接各家 IM 的**公開/官方接口**(EULA 明講沒逆向、沒破解)。但大家真正拿來玩「QQ 個人號」,是靠 `aiocqhttp`(OneBot v11 協議)去接 **NapCat / Lagrange / LLOneBot** 這類第三方 QQ 協議實作——那一段是非官方、有封號風險、也踩 QQ 使用條款的。**框架本身乾淨,風險在你搭的那顆 OneBot 實作**。QQ 官方 bot(qqofficial)則功能受限、群/頻道要審核。
    - **這是中國專案、原始碼是簡體中文**:程式碼註解、預設文案多為簡中(例:`# 交由 Stars 处理`)。官方有出繁中 README,但深入文件仍以簡中為主,詞彙要自己轉(訊息/伺服器/設定/外掛)。
    - **它跟 LangBot/NoneBot 不是同一種東西**:NoneBot 是「純框架、什麼都自己寫」;LangBot 是同類直接對手;AstrBot 是「電池全含」——WebUI、LLM、RAG、Agent、沙盒、1000+ 插件都幫你備好了(細節見〈與其他方案的差異〉)。

## 專案概述

AstrBot 自我定位是**「開源的一站式 Agent 聊天機器人平台」**,repo 描述更直白:*「AI Agent Assistant & development framework that integrates lots of IM platforms, LLMs, plugins and AI feature, and can be your openclaw alternative.」* 一句話:**一套後端,同時掛在你常用的十幾個即時通訊軟體上,把 LLM 對話 / Agent / 知識庫 / 多模態塞進去,再用插件無限擴充。**

它的核心價值有兩層:

- **拿來就用的一面**:`uv` 或 Docker 一鍵起,登入 Vue 做的 WebUI,填 API key、選模型、勾平台、從插件市場一鍵裝插件——不寫程式也能有一隻能對話、能查知識庫、會用工具的機器人。還內建 Web ChatUI(不接 IM 也能直接在網頁聊)。
- **開發框架的一面**:對外開放整套 `astrbot.api.*`,插件(Star)系統有幾十個裝飾器與生命週期鉤子,provider(模型)與 platform(IM)都用註冊機制可擴充,訊息走一條清楚的 pipeline。這一層才是它相對於「純聊天 App」的分野,也是本站把它歸類為 **AI Agent 框架** 的理由(它同時是可即用產品,但框架深度才是定義性特徵,方便與 [LobeHub](lobehub.md) 並列比較)。

配一句它 README 結尾的中二台詞很傳神:*「私は、高性能ですから!」*——作者刻意把「陪伴(能懂情緒)」跟「能力(可靠幹活)」兩件事綁在一起做。

## 七個看點

### 1. 支援平台:一套後端掛滿十幾個 IM(官方維護清單)

原始碼 `astrbot/core/platform/sources/` 底下每個資料夾就是一個平台適配器,官方維護的有:

| 分類 | 平台 |
|------|------|
| QQ 系 | `qqofficial` / `qqofficial_webhook`(QQ 官方 bot)、`aiocqhttp`(**OneBot v11**,接 NapCat 等第三方實作玩個人號) |
| 微信系 | `wecom`(企業微信應用)、`wecom_ai_bot`(企微智慧機器人)、`weixin_official_account` / `weixin_oc`(微信公眾號) |
| 國際 IM | `telegram`、`slack`、`discord`、`line`、`mattermost`、`misskey` |
| 中國協作 | `lark`(飛書)、`dingtalk`(釘釘)、`kook` |
| 通用/其他 | `satori`(通用協議)、`webchat`(內建 Web ChatUI) |

社群額外維護的還有 **Matrix、Rocket.Chat、VoceChat**(以插件形式),**WhatsApp 官方標示即將支援**。適配器用 `@register_platform_adapter` 註冊,寫一個新平台就是實作 `Platform` 介面 + 把收到的訊息轉成統一的 `AstrBotMessage`。

### 2. LLM / Provider:主流 + 一堆國產 + Agent 平台都收

`astrbot/core/provider/sources/` 把模型服務也做成可插拔的 source,而且不只文字模型,STT/TTS/embedding/rerank 全都是 provider:

- **對話 LLM**:OpenAI(及所有相容 endpoint,含 `openai_responses`)、**Anthropic**、Google **Gemini**、DeepSeek、Moonshot(Kimi,`kimi_code`)、智譜(`zhipu`)、xAI **Grok**(`xai`)、Groq、OpenRouter、LongCat、Xiaomi MiMo、以及一票 API 閘道(MiraRouter、AIHubMix、302.AI、矽基流動、PPIO、優雲、小馬算力、ModelScope、OneAPI)。
- **本機部署**:**Ollama**、**LM Studio**、vLLM(rerank)、Xinference。
- **Agent / LLMOps 平台**(當成「外部大腦」直接接):**Dify**、**Coze**、**阿里雲百煉**、**DeerFlow**——這幾個在 `astrbot/core/agent/runners/` 裡各有一個 runner,等於你可以不用 AstrBot 自己的 Agent,改把整段對話丟給 Dify/Coze 的工作流。
- **語音/向量**:STT 有 Whisper(API + self-host)、SenseVoice、Xiaomi MiMo Omni;TTS 有 OpenAI、Gemini、GPT-SoVITS、FishAudio、Edge TTS、Azure、Minimax、火山引擎、ElevenLabs、阿里雲百煉;embedding 有 OpenAI/Gemini/Dashscope/Ollama/NVIDIA;rerank 有百煉/NVIDIA/TEI/vLLM/Xinference。

### 3. 插件系統(Star):裝飾器風格 + 幾十個鉤子 + 1000+ 市場

這是 AstrBot 最像「框架」的部分。寫一個插件就是一個 `class Main(star.Star)`,方法上掛裝飾器。`astrbot/core/star/register/star_handler.py` 裡註冊得到的能力很齊:

- **指令/觸發**:`@filter.command`、`command_group`(子指令樹)、`event_message_type`(私聊/群聊/全部)、`regex`(正則觸發)、`platform_adapter_type`(只在某平台生效)、`permission_type`(權限,如管理員)。
- **生命週期鉤子**:`on_astrbot_loaded`、`on_platform_loaded`、`on_plugin_loaded/unloaded/error`。
- **LLM/Agent 攔截鉤子**(這組很關鍵):`on_llm_request` / `on_llm_response`(改寫進出 LLM 的內容)、`on_agent_begin` / `on_agent_done`、`on_using_llm_tool` / `on_llm_tool_respond`、`on_decorating_result`(改最終輸出)、`after_message_sent`。
- **給 LLM 用的工具**:`@filter.llm_tool`(或 `register_llm_tool`)把一個函式變成 function-calling 工具;`register_agent` 甚至能註冊自訂 Agent。

插件市場號稱 **1000+ 個**,WebUI 裡一鍵安裝。要注意 EULA 特別聲明:**第三方插件官方不審計、不背書、不擔保**,風險自負。

### 4. WebUI / 部署 / 資料庫

- **WebUI**:`dashboard/`(Vue + TypeScript)做的管理面板,後端用 Quart/FastAPI 提供;設定模型、平台、插件、對話、人格(persona)、看 log 全在網頁上。另有 **Web ChatUI**——不接任何 IM 也能直接在網頁跟機器人聊,而且內建 Agent Sandbox 與網頁搜尋。
- **部署**:①`uv tool install astrbot`(一鍵 CLI,官方主推);②**Docker / Docker Compose**(正式環境推薦);③一鍵雲端(雨雲 RainYun);④桌面版 App / Launcher(多開隔離);⑤面板化(寶塔 BT-Panel、1Panel、CasaOS NAS)。
- **資料庫**:預設 **SQLite**(`aiosqlite` + `sqlmodel`/SQLAlchemy),向量檢索用 **FAISS**(`faiss-cpu`)。**沒有強制 PostgreSQL**——這點跟 LobeHub 很不一樣,個人自架幾乎零維運。

### 5. Agent / MCP / 工具呼叫 / Skills / Agent Sandbox

這一區是 4.x 之後的重頭戲,也是它敢自稱「openclaw alternative」的底氣:

- **原生 Agent(tool-loop)**:`astrbot/core/agent/runners/tool_loop_agent_runner.py` 是自家的 function-calling 迴圈,搭 `ContextManager` + `ContextCompressor`(對話太長自動壓縮)。還有 `handoff.py`(多 Agent 交棒)和 `subagent_orchestrator.py`(子 Agent 編排)。
- **MCP**:`astrbot/core/agent/mcp_client.py` 是完整的 MCP client,支援 stdio 與 HTTP,還內建 stdio command allowlist(python/node/npx/uv…)做安全把關。等於 AstrBot 可以當 MCP host,把外部 MCP server 的工具餵給 LLM。
- **Skills(Anthropic 風格)**:`astrbot/builtin_stars/astrbot/skills/` 裡直接內建了 `documents`(docx)、`pdf`、`spreadsheets`、`skill-creator` 這幾個 **SKILL.md + scripts + references** 結構的技能——跟 Claude 的 Agent Skills 幾乎一模一樣的組織法。`neo_skill_sync.py` 負責同步。
- **Agent Sandbox**:`astrbot/core/computer/`(靠 `aiodocker`)提供隔離環境跑程式碼、呼叫 Shell,會話級資源複用;booter 有 `local`、`boxlite`、`shipyard`/`shipyard_neo`、`cua`(computer-use agent)。這讓機器人能安全地執行任意程式碼,不用把主機交出去。

### 6. 知識庫 / RAG / 多模態

- **知識庫 RAG**:`astrbot/core/knowledge_base/` 是一套完整的內建 RAG——parser 支援 PDF / EPUB / Markdown / 純文字 / URL(用 markitdown),chunking 有 fixed-size / markdown / recursive 三種,檢索是**混合式**:稀疏檢索(BM25,`rank-bm25` + 中文斷詞 + 停用詞表)＋ 稠密檢索(FAISS 向量)＋ `rank_fusion` 融合排序,還能接 rerank provider。知識庫存 SQLite。這比很多「只塞向量」的方案完整。
- **多模態**:圖片(多模態 LLM 輸入 + 結果階段的 text-to-image)、語音(STT 把語音轉文字進來、TTS 把回覆轉語音出去)。`ResultDecorateStage` 就負責把純文字結果加工成語音 / 圖片 / 加前綴。

### 7. Pipeline 架構:訊息事件怎麼流過 handler

AstrBot 用 **event bus + 分階段 pipeline** 處理每一則訊息,順序寫死在 `astrbot/core/pipeline/stage_order.py`:

```text
收到訊息(各平台適配器 → 統一 AstrBotMessage → EventBus)
  ↓
1. WakingCheck        判斷要不要被喚醒(@我 / 喚醒前綴 / 私聊)
2. WhitelistCheck     群聊/私聊白名單
3. SessionStatusCheck 這個會話有沒有整體啟用
4. RateLimit          頻率限制
5. ContentSafetyCheck 內容安全檢查
6. PreProcess         預處理
7. Process            ★ 交給 Stars(插件)或呼叫 LLM/Agent
8. ResultDecorate     加工結果(前綴 / text-to-image / 轉語音)
9. Respond            送回該平台
```

好處是責任分得很乾淨:白名單、限流、安全、喚醒判定這些「橫切關注點」都在插件之外統一處理,插件只需專注第 7 階段的業務邏輯。插件還能透過前面那些 LLM 鉤子插進第 7、8 階段中間改東西。

## 授權與商用可行性

- **License 是 AGPL-3.0-or-later**——這是最強的 copyleft 之一。自己內部用完全沒問題;但只要你**改了它、又拿去對外提供網路服務(SaaS)**,AGPL 會要求你把**修改後的完整原始碼**也對使用者公開。想閉源商用化要非常小心,這跟寬鬆的 MIT/Apache 完全不同。
- 另有一份 **`EULA.md`** 使用條款(最後更新 2026-01-12):明講①截至目前**團隊沒有任何收費服務**(有人跟你收錢請小心詐騙);②軟體「as is」不擔保;③**第三方插件與外部服務團隊一律不審計、不背書**,風險自負;④禁止拿去做違法/有害內容、禁止繞過內建安全機制。
- **實務結論**:個人、社群、企業內部自架 → 沒問題且免費。要包成對外商業產品 → 先把 AGPL 的開源義務跟第三方插件/OneBot 實作的合規風險搞清楚再說。

## 與其他方案的差異

| 面向 | **AstrBot** | LangBot | NoneBot2 | [LobeHub](lobehub.md) |
|------|-------------|---------|----------|---------|
| 定位 | 電池全含的 IM 機器人平台+框架 | 同類直接對手(中國 LLM IM bot) | 純 Python bot 框架 | Web 端多 Agent 協作工作空間 |
| 進入點 | **掛在你現有的 IM 裡** | 掛在 IM 裡 | 你自己寫 App | **獨立網頁 App** |
| 開箱即用 | WebUI + 1000+ 插件 + RAG + 沙盒全備 | 有 WebUI | 幾乎全靠自己寫 | 網頁產品即用 |
| 語言/資料庫 | Python 3.12,SQLite+FAISS(零維運) | Python | Python | TypeScript,常需 PostgreSQL |
| License | **AGPL-3.0**(強 copyleft) | AGPL-3.0 | MIT | 自訂(Other) |
| 社群規模 | 40.2K stars,中國社群最大 | 較小 | 大(框架老牌) | 74K stars |

一句話分野:

- **對比 NoneBot2**:NoneBot 是「給你螺絲起子」,LLM、WebUI、RAG 全要自己搭;AstrBot 是「整台車開走」。要高度客製、不要 LLM 包袱 → NoneBot;要快速有一隻能用的 AI bot → AstrBot。
- **對比 LangBot**:兩者最像(都是中國、都 AGPL、都 IM+LLM+WebUI+插件)。AstrBot 贏在**社群/插件生態規模、支援平台數、以及 Agent Sandbox + Skills + 原生 Agent 的深度**。
- **對比 [LobeHub](lobehub.md)**:LobeHub 是「你打開一個網頁跟 Agent 工作」;AstrBot 是「機器人住進你的 QQ/Telegram 群」。入口面完全不同——LobeHub 是 web 產品,AstrBot 是 IM-first 的自架後端。

## 注意事項與已知限制

1. **QQ 個人號的合規風險不在 AstrBot,在第三方 OneBot 實作**:NapCat/Lagrange 這類非官方協議實作有封號風險、踩 QQ 條款。要穩就用官方 bot 接口,但功能受限。
2. **AGPL 是雙面刃**:自架自用超讚,想閉源 SaaS 化要三思(見上一節)。
3. **插件市場品質參差**:1000+ 插件官方不審計,EULA 白紙黑字免責。裝第三方插件 = 給它跑你機器人的權限,尤其搭配 Agent Sandbox 能跑程式碼,要慎選來源。
4. **open issues 1,480 偏高**:專案很活躍(每天 push、release 到 v4.28)但迭代快、issue 累積多;4.x 相對 3.x 有過架構重整(`migra_3_to_4.py`),升級大版本要看 changelog。
5. **簡中為主**:深入設定與插件開發文件多為簡中,繁中使用者要自行轉詞。
6. **依賴外部模型 API**:本身不含推理能力,LLM/TTS/STT 的可用性與費用都看你接的 provider(這點所有這類平台都一樣)。

## 研究價值與啟示

### 關鍵洞察

1. **「一套後端 × N 個 IM」是被驗證的產品形態**:AstrBot 把「平台適配器」抽象成可註冊的 source,收到訊息一律轉成統一 `AstrBotMessage` 再走同一條 pipeline——這正是 [line-chatbot-boilerplate](line-chatbot-boilerplate.md) 那種「單一平台 boilerplate」放大 15 倍的樣子。想做跨平台 bot,這套「adapter → 統一事件 → pipeline」的分層值得照抄。

2. **分階段 pipeline 把「橫切關注點」抽離,是這類系統的架構共識**:喚醒判定、白名單、限流、內容安全都在插件之外統一做掉,插件只管業務。這跟 [LobeHub](lobehub.md) 的 chat pipeline、以及一般 web 框架的 middleware 是同一個思想——**先把「每個請求都要做的事」變成有序的 stage,再讓擴充點插進中間**。

3. **它把 Anthropic 的 Agent Skills 直接搬進 IM 機器人**:`builtin_stars` 裡那幾個 `SKILL.md + scripts + references` 幾乎是 Claude Skills 的翻版,加上 MCP client 與 Docker Agent Sandbox——等於「openclaw 那一套能力」被裝進了 QQ/Telegram。這條「把 coding-agent 的能力平移到 IM 聊天場景」的路線,跟本站一堆 Claude skills 筆記是同一股潮流的兩端。

4. **內建混合式 RAG(BM25 + 向量 + rerank)是它的隱藏強項**:很多 chatbot 的「知識庫」只是塞向量,AstrBot 的 `knowledge_base` 是稀疏+稠密+融合排序的完整管線,還帶中文斷詞。要研究 IM 場景的 RAG 落地,它比純 demo 實在。

5. **AGPL + EULA 的組合,是開源專案「防白嫖商用 + 免責」的教科書寫法**:用 AGPL 逼 SaaS 化的人開源,再用 EULA 把第三方插件/服務的責任撇清。做開源專案想兼顧「開放」與「保護自己」時,這個組合很值得參考。

### 與其他研究筆記的關聯

- **[LobeHub](lobehub.md)**:最直接的對照組——同樣是自架 LLM 平台,但 LobeHub 是 web-first 多 Agent 工作空間、TypeScript、常配 PostgreSQL;AstrBot 是 IM-first、Python、SQLite。並排讀能看清「自架 LLM 平台」的兩種產品形態。
- **[line-chatbot-boilerplate](line-chatbot-boilerplate.md)** 與 **[linebot-multimodal-rag](linebot-multimodal-rag.md)**:前者是單平台(LINE)bot 的起手式,後者是 LINE + 多模態 RAG——AstrBot 等於把這兩件事做成通吃 15 個平台的框架版,對照可看「單點方案 → 通用平台」的演化。
- **[ai-avatar-bot](ai-avatar-bot.md)**:同屬「自架、帶 RAG 的對話機器人」,可對比人格/陪伴向的設計取捨(AstrBot 也主打 persona + 陪伴)。
- **[rag-anything](rag-anything.md)** / **[graphrag](graphrag.md)**:想把 AstrBot 內建那套 RAG 換成更強的方案時,這兩篇是進階選項的參考。
- **[litellm](litellm.md)**:AstrBot 自己實作了一層 provider 抽象(統一各家 LLM),概念上跟 LiteLLM 解決同一問題,可對照兩種「多模型統一介面」的做法。
- **[mcp-for-beginners](mcp-for-beginners.md)**:AstrBot 是「MCP host」的實例,想理解它怎麼把外部 MCP 工具餵給 LLM,先讀這篇打底。
- **[gemma-4-local-llm](gemma-4-local-llm.md)**:AstrBot 支援 Ollama/LM Studio 本機模型,想做「全本地、不出網」的 bot 可搭這篇。
- **[n8n-workflows](n8n-workflows.md)**:另一種「把 AI 接進工作流」的思路(自動化編排 vs. IM 機器人),可對照兩種讓 AI 落地到日常的入口。

## 一句話總結

> AstrBot 是中國社群最紅、40.2K 星的**自架多平台 LLM 聊天機器人平台兼開發框架**:一套 Python 後端同時掛滿 QQ/OneBot、Telegram、企業微信、飛書、釘釘、微信公眾號、Slack、Discord、LINE、KOOK 等十幾個 IM,LLM 從 OpenAI/Anthropic/Gemini 到 DeepSeek/智譜/Kimi/Grok/Ollama 到 Dify/Coze/百煉全收;插件叫 Star、市場 1000+ 個一鍵裝,還內建原生 Agent + MCP + Anthropic 風格 Skills + Docker Agent Sandbox + 混合式 RAG + STT/TTS 多模態,配 Vue WebUI 與 SQLite+FAISS,uv/Docker/一鍵雲端都能起。要注意的是 AGPL-3.0 的 copyleft、以及「QQ 個人號」靠第三方 OneBot 實作的封號灰色地帶——框架乾淨,風險在你搭的那顆協議實作。
