---
date: "2026-05-14"
category: "學習資源"
card_icon: "material-school"
oneliner: "Microsoft 官方 12 (+6) 課 AI Agent 入門課，以 Microsoft Agent Framework + Azure AI Foundry V2 為主軸，61k stars、50+ 語言"
---

# AI Agents for Beginners 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/microsoft/ai-agents-for-beginners> |
| 官方課程入口 | <https://aka.ms/ai-agents-beginners> |
| 繁中翻譯 | <https://github.com/microsoft/ai-agents-for-beginners/tree/main/translations/zh-TW> |
| Microsoft Foundry Discord | <https://aka.ms/ai-agents/discord> |
| 配套技術 | Microsoft Agent Framework (MAF)、Azure AI Foundry Agent Service V2、MiniMax（替代 OpenAI-compatible） |
| 創建時間 | 2024-11-28 |
| 規模 | 61,394 stars / 20,790 forks / MIT / 主要語言 Jupyter Notebook（May 14 2026 抓取） |

## 專案概述

**AI Agents for Beginners** 是 Microsoft 官方推出的 Agent 入門課程，定位為「想開始造 Agent 必須知道的一切」。每堂課由短文 + 短影片 + Python 範例組成，範例放在 `code_samples/` 資料夾，以 **Microsoft Agent Framework (MAF) + Azure AI Foundry Agent Service V2** 為主要實作堆疊，部分課程支援其他 OpenAI-compatible provider（README 點名 **MiniMax**，因其支援 204K context）。

這份教材是 Microsoft「for Beginners」系列的最新一員，跟 [MCP for Beginners](https://github.com/microsoft/mcp-for-beginners)、Generative AI for Beginners、Edge AI for Beginners、AZD for Beginners 同屬一個生態系。短短一年多累積 61k stars，是目前 GitHub 上最受歡迎的 AI Agent 入門教材之一。

特別值得注意的是**多語支援機制**：repo 透過 Azure 自家的 [co-op-translator](https://github.com/Azure/co-op-translator) GitHub Action 自動同步 50+ 種語言翻譯（含繁中-台灣 / 香港 / 澳門三版分支），但這也讓 clone size 暴增到近 3.7GB。README 提供 `--filter=blob:none --sparse` + `sparse-checkout set --no-cone '/*' '!translations' '!translated_images'` 的範例命令，是 ML/AI 教材中少見、值得學習的處理方式。

## 課程地圖

| # | 課名 | 核心概念 |
|---|------|---------|
| 01 | Intro to AI Agents and Agent Use Cases | Agent 定義與適用場景 |
| 02 | Exploring AI Agentic Frameworks | 框架巡覽 |
| 03 | Understanding AI Agentic Design Patterns | 設計模式總覽 |
| 04 | Tool Use Design Pattern | 工具呼叫模式 |
| 05 | Agentic RAG | 帶決策的檢索 |
| 06 | Building Trustworthy AI Agents | 信任與安全 |
| 07 | Planning Design Pattern | 規劃 |
| 08 | Multi-Agent Design Pattern | 多 Agent 協作 |
| 09 | Metacognition Design Pattern | 反思 / 元認知 |
| 10 | AI Agents in Production | 上線實務 |
| 11 | Using Agentic Protocols (MCP, A2A and NLWeb) | 三種 agent 互通協定 |
| 12 | Context Engineering for AI Agents | context 工程 |
| 13 | Managing Agentic Memory | Agent 記憶管理 |
| 14 | Exploring Microsoft Agent Framework | MAF 深入 |
| 15 | Building Computer Use Agents (CUA) | 電腦操作 Agent（browser-use 範例） |
| 16 | Deploying Scalable Agents | （Coming Soon） |
| 17 | Creating Local AI Agents | （Coming Soon） |
| 18 | Securing AI Agents | 安全 |

→ 已公開 14 堂 + 1 堂 CUA + 1 堂 Security，2 堂未發布，**實際課數已超過題目宣傳的 12 堂**，內容仍在擴充。

## 技術選型重點

- **Microsoft Agent Framework (MAF)** 是 Microsoft 整合 AutoGen 與 Semantic Kernel 之後的新代 SDK（topics 仍標 `autogen` / `semantic-kernel`，反映歷史脈絡）。
- **Azure AI Foundry Agent Service V2** 為主要執行環境，需 Azure 帳號。
- **MiniMax** 被特別點名作為 OpenAI-compatible 替代 provider，主打 204K context window——對於只想學概念但不想開 Azure 的學員是現成解法。
- **MCP / A2A / NLWeb 三協定**：第 11 課把三個橫向互通 protocol 並列教學，反映 Microsoft 對「Agent 間通訊」標準的下注（NLWeb 是 Microsoft 自家提案）。

## 快速開始

```bash
# 不要拉 3.7GB 全部翻譯
git clone --filter=blob:none --sparse https://github.com/microsoft/ai-agents-for-beginners.git
cd ai-agents-for-beginners
git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'

# 進入課程
cd 00-course-setup
# 依 README 設定 Azure AI Foundry 或 MiniMax API key
```

## 目前限制與注意事項

- **強烈綁定 Azure 生態系**：預設範例需要 Azure 帳號 + Foundry 額度；雖然 MiniMax 是替代方案，但 14 課 MAF 深入課大概率只在 Azure 環境完整可跑。
- **Repo 體積**：3.7GB（含 50+ 語言 + translated_images）。沒用 sparse checkout 直接 clone 會卡很久。
- **主要語言被 GitHub 判定為 Jupyter Notebook**：實際範例為 Python，但 ipynb 形式比例高，要看完整 source 須在 notebook 內 scroll。
- **2 堂課仍 Coming Soon**：scaling deployment 與 local AI agents 都是熱門題，但目前缺貨。
- **CLA 要求**：所有 PR 需簽 Microsoft CLA。
- **WT.mc_id tracking**：所有外部連結帶 `WT.mc_id=academic-105485-koreyst` query string，是 Microsoft 內部歸因參數，並非追蹤學員行為。

## 研究價值與啟示

### 關鍵洞察

1. **微軟把「教材」當作 SDK 採用率推進工具**：MCP for Beginners、AI Agents for Beginners、Edge AI for Beginners 共用 co-op-translator 翻譯流水線、共用 Discord 社群、共用 `WT.mc_id` 歸因系統。這條 for Beginners 系列已成微軟對抗 LangChain / LlamaIndex 等開源敘事的核心通路——值得對標研究**「教材 → SDK 採用 → 雲端服務付費」**的完整漏斗設計。
2. **第 11 課 (MCP + A2A + NLWeb) 是少見的「三協議並列」教學**：MCP 是 Anthropic 提的 Agent ↔ Tool 標準、A2A 是 Google 提的 Agent ↔ Agent 標準、NLWeb 是 Microsoft 提的 web ↔ agent 標準。一堂課把三者並排教，相當於 Microsoft 在說：**這三個是 Agent 互通的「標準層」候選，全要學**。值得對照 [[mcp-for-beginners]] 的深入版。
3. **Context Engineering 與 Agentic Memory 被獨立成兩課**：呼應 [[why-your-ai-is-dumbing-down]] 的核心觀察——context 操作已從「prompt 工程的副題」升格為「Agent 工程的兩大支柱」。Microsoft 願意把這兩件事各給一整課，反映業界共識已經移動。
4. **MAF = AutoGen + Semantic Kernel 的整併**：topics 同時保留 `autogen` 與 `semantic-kernel`，但教材以 MAF 為主。對長期關注 Microsoft Agent 棧的人，這是個明確訊號：之前學 AutoGen 或 Semantic Kernel 的人需要重新對齊到 MAF 的 API 表面。
5. **co-op-translator 是真正的隱藏寶藏**：50+ 語言翻譯由 Azure 自家 LLM-based translator pipeline 維護，是其他 AI 教材罕見能達到的覆蓋率。對教育內容創作者來說，這個 pipeline 比課程本身更值得 fork 來用。
6. **sparse-checkout 寫進 README 是正確示範**：絕大多數含翻譯的開源教材 README 不提這件事，新手 clone 直接卡爆。Microsoft 把命令寫進 quick start 是給其他多語 repo 的範本。

### 與其他研究的關聯

- 與 [[mcp-for-beginners]]：同系列、相鄰主題，11 課的 MCP 內容是這份的精華版，深入版要轉去 MCP for Beginners。
- 與 [[ai-agents]]（黃佳 / 動手做 AI Agent）：兩本都是入門書，但取向完全不同——黃佳走 LangChain 為主，Microsoft 這份綁 MAF + Azure Foundry。**並排讀可看到「開源派 vs 雲端原生派」對同一概念的不同教法**。
- 與 [[openai-practical-guide-building-agents]]、[[ly-corp-adk-agent]]、[[claude-agent-sdk]]：四個 vendor（Microsoft / OpenAI / Google ADK 經 LY / Anthropic）的官方 Agent 入門材料齊備，可做橫向比較研究：誰把 memory 講最清楚？誰把 multi-agent 講最清楚？誰把 tool use 講最清楚？
- 與 [[context-hub]]、[[why-your-ai-is-dumbing-down]]：第 12 課 context engineering、第 13 課 agentic memory，是業界主流敘事的官方版本；對照 Saki-tw 對 CHECKPOINT 的批判，可看到「平台說的 context engineering」與「平台實際做的 context replacement」之間的差距。
