---
date: "2026-09-11"
category: "學習資源"
card_icon: "material-book-open-page-variant"
oneliner: "前華為『天才少年』、Pine AI 首席科學家李博杰寫的《深入理解 AI Agent:設計原理與工程實踐》——45.7K★、Apache-2.0『整本書免費開源』(正文 + PDF/EPUB + 109 個配套實驗全放 GitHub)。以核心公式 Agent = LLM + 上下文 + 工具 用十章從原理講到生產:上下文工程(KV Cache/Skills/壓縮)、用戶記憶與 RAG、工具與 MCP、Coding Agent、語音/Computer Use/機器人交互、評估、模型後訓練(SFT/RL)、持續進化、multi-agent。用 whisper coding 口述式協作寫成,15 種語言,含繁體中文台灣版"
tags:
  - learning
  - multi-agent
  - rag
  - mcp
  - memory
  - context-engineering
  - llm-training
---

# 《深入理解 AI Agent》(ai-agent-book) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/bojieli/ai-agent-book> |
| 書名 | 《深入理解 AI Agent:設計原理與工程實踐》 |
| 作者 | **李博杰(Bojie Li)** — 前華為首批「天才少年」、現 Pine AI 首席科學家 |
| 作者個人站 / blog | <https://01.me>、<https://bojieli.github.io> |
| 線上閱讀(MkDocs Material) | <https://bojieli.github.io/ai-agent-book/> |
| PDF / EPUB(中文原版) | [Releases → AI-Agents-in-Depth-zh-CN.pdf / .epub](https://github.com/bojieli/ai-agent-book/releases) |
| 繁體中文(台灣)版 | 社群翻譯 by [@tigercosmos](https://github.com/tigercosmos),原始碼在 `book-zhtw/`,PDF 為 `...-zh-TW.pdf` |
| 作者背景報導 | [華為首批「天才少年」李博杰:放棄百萬年薪,投身 AI 創業(騰訊新聞)](https://news.qq.com/rain/a/20250107A02UDW00)、[蜗壳进阶联盟专访(01.me)](https://01.me/2024/12/wokejinjie-interview-1/) |

> **Metadata(2026-09-11 即時抓取,取自 GitHub API 與 `git clone` 原始碼):**
> **45,723 stars / 5,095 forks / 20 open issues** · **Apache-2.0**(有明確 LICENSE 檔) · 主語言 **Python**(約 14.9 MB;其餘依序為 JavaScript / TeX / HTML / MDX / Shell / TypeScript / Lua / CSS)· 建立於 **2025-09-09**,最後 push **2026-09-10**(剛好上線約一年、**極度活躍**,commit 數逾 1,700)· 預設分支 `main` · repo size **約 794 MB**(含全書 SVG 配圖、15 語系正文與建置工具鏈)· subscribers 166 · topics:`agent` / `agent-memory` / `ai-agent` / `book` / `coding-agent` / `context-engineering` / `large-language-models` / `llm` / `mcp` / `multi-agent` / `multimodal` / `rag` / `reinforcement-learning`。書稿目前為 **2.0 版**(由 1.4 升級,把原第 4 章「異步交互」與原第 9 章「多模態」合併重組為新的第 6 章「交互」)。

!!! warning "五個要先校正的判讀"
    - **這是「一本書」,不是框架/工具/SDK。** GitHub 標主語言 Python,但 Python 是「配套實驗」的碼;真正的產品是那本十章的技術書(正文在 `book/chapter1.md`~`chapter10.md`)。TeX/Lua 是 LaTeX(ElegantBook)+ pandoc 的 PDF 建置鏈,MDX/HTML/CSS/JS 是線上閱讀站,語言長條圖看不出「這是書」。
    - **45.7K★ 是「一本書」的星,不是程式庫的星。** 這個量級在技術書開源史上非常罕見——它衝上過 GitHub Trending「Project of the Day」。星數反映的是內容價值,不是「多少人拿它當 dependency」。
    - **Apache-2.0 罕見地蓋在「整本書正文 + PDF」上,不只是程式碼。** 一般技術書就算開源程式碼,正文仍是出版社版權;這本連正文都用 Apache-2.0 開放,是刻意選擇(見下「授權與商用可行性」)。
    - **原文是簡體中文,本筆記已轉繁體 + 台灣用詞。** 官方另有社群維護的繁體中文(台灣)版(`book-zhtw/`),但社群譯本可能落後於簡中原版。
    - **「109 個實驗」不等於「109 個能一鍵跑的 demo」。** 官方數字含三類:✅ 可獨立執行、📖 需自行 clone 外部倉庫的「複現指南」、🚧 仍在完善的「設計文件」。早期評測文常說「60 多個可跑 demo」,兩個數字並不矛盾——差在「可獨立跑」與「含外部複現軌道」的口徑。

## 專案概述

這是 **《深入理解 AI Agent:設計原理與工程實踐》** 的開源主倉庫——一本由**前華為「天才少年」、Pine AI 首席科學家李博杰**撰寫的中文 AI Agent 技術書。它把「全書正文 + 編譯版 PDF/EPUB + 按章配套程式碼」全部用 **Apache-2.0 免費開源**,同時提供 15 種語言與線上閱讀站。

全書只圍繞**一條核心公式**展開:

> **Agent = LLM + 上下文 + 工具**(直覺層:大腦 + 眼睛 + 手腳;學術層:Policy + Observation Space + Action Space)

書的來歷很特別:它以李博杰 2025 年 8–10 月在**圖靈《AI Agent 實戰營》**的課程講義、以及他 2024–2026 年在**國科大(中國科學院大學)**開的 AI Agent 實踐課為底稿,整理重構而成。作者本人在引言裡強調,書中的架構原則來自 **Pine AI 的真實生產場景**(讓 Agent 代表用戶跟真人溝通、處理帳單協商/退款投訴/退訂等涉及真實金錢的長流程任務)——也就是「**實踐在前,命名在後**」:Skill、harness、loop engineering 這些後來流行的術語,對應的工程做法其實更早出現在領先系統裡。

它的定位不是「跑通一個 demo」,而是**解釋每個設計決策背後「為什麼」與其能力邊界/工程取捨**,主打「好的架構原則能穿越模型迭代週期」。

## 全書章節總覽(第 1–10 章)

全書分兩部分:**第一部分「如何構建 Agent」(第 1–6 章)** 從概念、上下文、記憶、工具、Coding Agent 到交互;**第二部分「如何提升 Agent 能力」(第 7–10 章)** 從評估、後訓練、持續進化到多 Agent 協作(分別對應模型參數、單體系統、群體系統三個層面)。

| 章 | 主題 | 一句話核心 | 實驗數 |
|:--:|------|-----------|:--:|
| 1 | **AI Agent 入門** | Agent = LLM + 上下文 + 工具;三層理解(實現/直覺/學術)、ReAct 循環、從工作流到自主 Agent 的編排光譜;**Harness 工程才是競爭力** | 4 |
| 2 | **上下文工程**(作者稱全書最關鍵一章) | 上下文決定能力上限:訊息列表結構、**KV Cache** 底層原理、提示工程 vs 提示注入攻防、**Agent Skills** 按需載入、狀態栏(system hint)、上下文壓縮 | 10 |
| 3 | **用戶記憶和知識庫** | 跨會話持久化:用戶記憶四種漸進式策略、**RAG** 完整技術棧(dense/sparse embedding、contextual retrieval、rerank)、結構化索引、知識圖譜、**Agentic RAG**、多模態記憶 | 12 |
| 4 | **工具** | **MCP** 互操作標準 + 五類工具(感知/執行/協作/事件觸發/用戶溝通)、多模態感知三路線、執行工具**安全機制**、主動工具發現 | 5 |
| 5 | **Coding Agent 與通用 Agent** | 論證「Coding Agent + 檔案系統」是所有通用 Agent 的技術基礎;以 **OpenClaw** 架構為主線,代碼作為「能創造新工具的工具」、Agent 自舉 | 16 |
| 6 | **交互:觀察與動作空間的擴展** | 從**模態 × 時序**兩維度擴展:異步/事件驅動、**語音交互**、**Computer Use**、**機器人操作**;共享喚醒/安全點/取消/搶佔/快慢路徑分離等原語 | 14 |
| 7 | **Agent 的評估** | 把表現變可比信號:評估環境(工具型/人機互動型/仿真)、資料集設計、**LLM-as-a-Judge**、統計顯著性、評估驅動選型 | 14 |
| 8 | **模型後訓練** | 預訓練/SFT/RL 三階段全景;「SFT 記憶、RL 泛化」「資料與環境比演算法更重要」;獎勵設計、單/多輪 RL 演算法、樣本效率 | 19 |
| 9 | **Agent 的持續進化** | 從運行軌跡取得學習信號;比較四種更新載體(知識文檔 / Prompt+Skills / 程式+Harness / 模型參數),含驗證、灰度發布、回滾 | 9 |
| 10 | **多 Agent 協作** | 協作分類框架(上下文共享/獨立 × 對等/管理者/去中心化)、翻譯 Agent、電話+電腦協同、生成式 Agent 小鎮;「Agent 社會/經濟」展望 | 6 |

> 合計 **109 個實驗**(4+10+12+5+16+14+14+19+9+6)。實驗編號為「實驗 X-Y」,難度以星級標注:★ 入門 / ★★ 中等 / ★★★ 進階。另有引言、後記與思考題。

## 6 個看點

### 1. 章節結構:一條「構建 → 提升」主線,且穿越模型迭代

十章不是主題大雜燴,而是一條清楚的敘事線:先用第 1 章的核心公式建立座標系,第 2–6 章沿「眼睛(上下文/記憶)→ 手腳(工具/代碼/交互)」把 Agent「造出來」,再用第 7–10 章沿「評估 → 後訓練 → 持續進化 → 多 Agent」把它「變強」。後記〈兩朵烏雲〉點出作者眼中的兩個未解難題:**(1) Agent 如何流式/實時地與環境交互**(快慢路徑分離 vs 把推理做快)、**(2) Agent 如何像人一樣從成敗中持續積累經驗**(小世界 vs 大世界假設),並提出「**模型會一層一層吃掉 Harness,但永遠吃不完**」的飛輪論。這種「原則優先、抗過時」的寫法是它跟一般「教你用某框架」教材最大的氣質差異。

### 2. 109 個配套實驗:能真跑、可復現、還接真實(國產)模型

配套碼不是玩具:

- **統一環境**:Python 3.11–3.13,倉庫根目錄用 **`uv.lock`** 提供可復現的**分章環境**(`uv sync --locked --extra ch1`~`ch10`,另有 `vllm`/`unsloth` 等 extra);也支援 `pip install -e ".[ch1]"`。
- **每章一個 `README.md` + `EXPERIMENT_LEDGER.md`**:後者記錄逐項「正文驗收、真實 API 狀態與證據路徑」——很誠實地標明哪些實驗實測通過、哪些被配額卡住、哪些結論沒能複現(例如第 1 章「去掉 reasoning 必然退化」在該次運行未複現)。
- **接真實模型**:實驗大量走國產/開源模型(Kimi / GLM / DeepSeek / Qwen / Doubao 等)與 OpenAI 相容介面,務實面向中國大陸讀者的取用性。
- **外部複現軌道**:第 6/7/8/10 章有 22 個外部倉庫映射(如評測基準 **SWE-bench / GAIA / OSWorld / tau2-bench / terminal-bench / android_world**、訓練框架 **verl / minimind / AWorld / SimpleVLA-RL**),**釘死到不可變 commit SHA** 並附校驗;部分是作者 fork 的 `bojieli/*` 適配分支。這些「不內建、需自行 clone」是出於體積與版權考量。

### 3. 定位與深度:進階「工程」書,不是入門手冊

**理論 vs 工程的比重明顯偏工程實踐**,但每個工程決策都追問原理。適合對象(作者在引言明列):

- **前置必需**:會 Python、用過 LLM 產品、熟悉至少一款 AI Coding 工具(Claude Code / Codex / Cursor…)、有軟工常識(CLI/Git/JSON/REST)。
- **前置推薦**:機器學習基礎(第 8 章)、線代與機率直覺(第 2/3/8 章)、Web 基礎(第 6 章)。
- 除第 8 章後訓練外,全書對數學/ML 要求很低。**核心受眾是想把 Agent 推上生產的工程師與研究者**,而非純新手;但第 1–2 章也可當入門起點。全書約 400 多頁。

### 4. 作者李博杰:少年班 → MSRA → 華為天才少年 → Pine AI 首席科學家

一個關鍵背書是作者本人的來歷(可靠來源交叉確認):

- 1992 年生,**中科大少年班**(高中拿過 NOI 資訊競賽銅牌)。
- 2014 年進 **中科大—微軟亞洲研究院(MSRA)聯合培養博士**,研究資料中心網路與 FPGA;2019 年獲博士,拿過 **ACM China 優秀博士論文獎**、微軟學者獎學金;在 SIGCOMM / SOSP / NSDI / ATC / PLDI 等頂會發表論文。
- **華為首批「天才少年」**,曾任華為計算機網路與協議實驗室助理/副首席科學家。
- 後**放棄百萬年薪投身 AI 創業**,現任 **Pine AI 首席科學家**——書中的架構原則正是來自 Pine 這種「代表用戶跟真人談判、涉及真實金錢、長流程高風險」的產品實戰。

### 5. 涵蓋的關鍵主題:幾乎把 Agent 生產全景收齊

一本書把這些主題用「可跑的實驗」串起來,覆蓋面在同類教材裡罕見:**context engineering**(KV Cache / Skills / 壓縮 / 提示注入)、**agent memory**(四級策略 + 評估)、**RAG**(dense/sparse/contextual/rerank/agentic/GraphRAG 式知識圖譜)、**MCP** 與工具設計、**Coding Agent**(OpenClaw 主線)、**多模態 / 語音 / Computer Use / 機器人**、**評估**(LLM-as-Judge / 統計顯著性 / benchmark)、**模型後訓練**(SFT vs RL、獎勵設計、verl/GRPO/ReTool 配方)、**持續進化**(自我修改、軌跡驗證)、**multi-agent**(協作分類框架、生成式 Agent 小鎮)。這對應 repo 的 topics 一字不差。

### 6. 寫作與出版模式:whisper coding 寫成、全開源、15 種語言

- **AI 深度參與寫作**:作者自述用 **whisper coding(口述式協作)**——口述章節提綱 → 語音 Agent 調研成草稿 → 結合學員反饋反覆核查修訂。這本書「不只討論 Agent,也記錄了一種由 Agent 深度參與的知識生產方式」。
- **15 種語言**:中文原版 + 14 種社群翻譯(英/西/印尼/阿/**繁中台灣**/俄/泰米爾/越/日/土/韓/匈/希伯來/葡巴),各語系正文放在 `book-<lang>/`,線上站可切換。
- **持續更新**:每次 push 自動重建線上站與 PDF/EPUB;書稿已迭代到 2.0 版,contributors 逾 70 人(勘誤、新實驗、配圖、翻譯皆走 PR)。

## 授權與商用可行性

- **授權**:**Apache-2.0**,而且蓋在「**整本書正文 + 編譯版 PDF/EPUB + 全部配套碼**」上。這意味著你可以自由閱讀、複製、修改、再散布,甚至商用/二創,只需保留授權與著作權聲明(Apache-2.0 另含專利授權條款)。README 註明:部分子專案(尤其外部倉庫)可能有各自授權,以子專案為準。
- **「真的全書免費開放嗎?」——是。** 正文、PDF、EPUB、109 個實驗全部在 GitHub 免費取得,無付費牆、無「僅程式碼開源、正文閉源」的常見拆分。這正是它最反常之處。
- **與實體出版的關係**:本書以圖靈《AI Agent 實戰營》課程講義為底稿,引言/致謝也感謝了**圖靈(人民郵電出版社圖靈教育)的編輯**,並提到姊妹作《圖解大模型》(圖靈出版)。但**截至 2026-09,查無這本書的實體/付費版在售**——目前它就是「開源免費電子書 + 配套碼」的形態。是否會出紙本尚未確認;即便日後出版,現有開源正文仍免費。
- **實務提醒**:配套實驗需要各家 LLM 的 **API Key**(部分僅支援特定 provider);外部複現軌道(訓練/機器人/瀏覽器)另需自備 GPU、模擬器、瀏覽器等系統依賴,且「clone 成功 ≠ 實驗已跑通」(作者用 `EXPERIMENT_LEDGER.md` 明確區分)。

## 與其他 AI agent 書/教材的差異

| 專案 | 形式 | 語言 | 授權 | 深度定位 | 最大特色 |
|------|------|------|------|---------|---------|
| **本書 ai-agent-book(李博杰)** | 技術書 + 109 實驗 | 簡中(+14 語系) | **Apache-2.0(連正文)** | 進階工程,原理→生產 | 全書正文都開源;涵蓋 context/memory/RAG/MCP/coding/交互/評估/**後訓練 RL**/進化/multi-agent 全景;作者是華為天才少年 + Pine AI 首席科學家 |
| [AI Agents(黃佳《動手做 AI Agent》)](ai-agents.md) | 入門書配套碼 | 中文 | 書籍付費 | 入門實作 | 系統性中文入門;正文在**付費紙本**,repo 只是配套碼 |
| [Building Applications with AI Agents](building-applications-with-ai-agents.md) | O'Reilly 書配套碼 | 英文 | **無 LICENSE**(保留權利) | 生產工程參考 | 同場景用 LangGraph/LangChain/Autogen/OpenAI 平行實作 + 分散式編排(Ray/Redis/Temporal) |
| [AI Engineering from Scratch](ai-engineering-from-scratch.md) | 課程式教材 | 英文 | — | 從數學到多 Agent 全覆蓋 | 20 Phases、260+ 課、290 小時的長跨度課綱 |
| [GenAI Agents](genai-agents.md) | 53 本 notebook | 英文 | **非商業自訂條款** | 範例集 | 可跑 notebook 多,但約 2/3 是 LangGraph 應用集、授權非開源 |
| [AI Agents for Beginners(微軟)](ai-agents-for-beginners.md) | 官方入門課 | 多語 | 開源 | 入門 | 綁 Microsoft Agent Framework + Azure AI Foundry |

**一句話抓差異**:別的多半是「入門書的付費正文 + 免費碼」「英文的框架範例集」或「入門課」;**這本是唯一把「進階、覆蓋到後訓練/RL/持續進化的整本工程書正文」也 Apache 開源、且由頂級一線實戰者(華為天才少年 + Pine AI 首席科學家)親筆的中文書**。深度與主題廣度上,它更像把 [building-applications-with-ai-agents](building-applications-with-ai-agents.md) 的工程野心 + [ai-agents](ai-agents.md) 的中文系統性,再加上「模型後訓練」這塊多數 agent 書不碰的內容,合為一冊。

## 注意事項與已知限制

- **簡繁差異**:官方原版簡中;繁中(台灣)為社群譯本,可能落後於原版。閱讀最新內容建議看簡中或線上站。
- **「109 實驗」口徑**:含 ✅ 可跑 / 📖 需 clone 外部倉庫的複現指南 / 🚧 設計文件三類;不是每個都能一鍵跑通。以 `chapterX/EXPERIMENT_LEDGER.md` 的驗收狀態為準。
- **依賴取用**:多數實驗需 API Key(且部分綁特定 provider,如國產模型);外部訓練/機器人/瀏覽器實驗需 GPU/模擬器/瀏覽器等重依賴,並非人人跑得動。
- **repo 很大(約 794 MB)**:含全書 SVG 配圖、多語系正文、LaTeX/pandoc 建置鏈與資產;`git clone` 檔案數上萬,只想讀書可直接下 PDF/EPUB 或看線上站。
- **內容時效**:主題緊貼 2025–2026 前沿(DeepSeek R1、Manus、Claude Code、OpenClaw、GRPO/ReTool 等),模型與 API 細節會過時——作者也在後記主動承認「一本書追不上所有變化」,強調帶走的應是判斷力而非某個 API 用法。
- **商業味**:README 有贊助商(Krill AI)與帶邀請碼的優惠連結,屬正常開源專案商業化,不影響內容開放性,但引用時可留意。

## 研究價值與啟示

### 關鍵洞察

1. **「整本書正文都用 Apache-2.0 開源」本身就是一個罕見的事件。** 技術書通常「碼開源、正文閉源」;這本連 400 多頁正文、PDF、EPUB 全開放,配上一線實戰者的深度,是「知識共享」在技術書領域的極端案例——也解釋了 45.7K★ 這種「書」不該有的星數量級。
2. **它把「模型後訓練(SFT/RL)」納入 Agent 書,補上多數 agent 教材的缺口。** 大部分 agent 書止步於「用 API 拼 Agent」;這本一路講到 SFT vs RL、獎勵設計、verl/GRPO/ReTool,把「應用層 harness」與「模型層訓練」接成一條飛輪(後記的「模型會一層層吃掉 Harness」論證正是這條主線)。
3. **「實踐在前,命名在後」是很有價值的方法論姿態。** 作者反覆強調 Skill/harness/loop engineering 這些術語背後的工程做法更早出現在生產系統——這提醒讀者別把「流行詞」當起點,而要回到「Agent 與世界交互的基本問題:看到什麼、能做什麼、如何驗證做得對」。
4. **whisper coding 寫書,是「Agent 深度參與知識生產」的活體示範。** 這本書既是教材,也是它自己所講方法的產物。

### 與其他研究筆記的關聯

- **中文 agent 書對照**:與 [AI Agents(黃佳)](ai-agents.md) 並讀,可看「中文 agent 書」的兩種形態——一本入門付費紙本 + 免費碼,一本進階全開源電子書。
- **工程深度對照**:與 [Building Applications with AI Agents](building-applications-with-ai-agents.md) 是最佳工程對照(同樣重評估、分散式、後訓練),差在授權(Apache vs 無 LICENSE)與語言(中 vs 英)。
- **主題級延伸**:第 3 章 RAG/知識圖譜可延伸讀 [RAG-Anything](rag-anything.md)、[GraphRAG](graphrag.md);第 4 章 MCP 可接 [MCP for Beginners](mcp-for-beginners.md);第 10 章 multi-agent 可對照站上多 agent 相關筆記。
- **教材光譜**:與 [AI Engineering from Scratch](ai-engineering-from-scratch.md)、[GenAI Agents](genai-agents.md)、[AI Agents for Beginners](ai-agents-for-beginners.md) 一起,構成「入門課 → 範例集 → 進階工程書」的學習資源光譜,本書坐在「最進階、最工程化」那端。

## 一句話總結

> 前華為「天才少年」、Pine AI 首席科學家**李博杰**寫的《深入理解 AI Agent:設計原理與工程實踐》——**45.7K★、Apache-2.0 把「整本書正文 + PDF/EPUB + 109 個配套實驗」全免費開源**(技術書裡極罕見)。以 **Agent = LLM + 上下文 + 工具** 一條公式,用十章從原理講到生產,涵蓋上下文工程、記憶與 RAG、MCP 與工具、Coding Agent、語音/Computer Use/機器人交互、評估、**模型後訓練(SFT/RL)**、持續進化與 multi-agent——比多數 agent 書更深、更廣,還是用 whisper coding 口述式協作寫成、支援 15 種語言(含繁中台灣版)的中文一線實戰之作。
