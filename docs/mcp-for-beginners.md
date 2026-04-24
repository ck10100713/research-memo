---
date: "2026-04-24"
category: "學習資源"
card_icon: "material-school"
oneliner: "微軟官方 MCP 入門課程，12 模組 × 6 種語言 (.NET / Java / JS / TS / Python / Rust)，對齊 MCP 規範 2025-11-25，模組 11 含 13 個 PostgreSQL 整合實作實驗室，20 天衝到 15.9K stars"
---

# MCP for Beginners 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/microsoft/mcp-for-beginners> |
| 繁中 README | <https://github.com/microsoft/mcp-for-beginners/blob/main/translations/zh-TW/README.md> |
| MCP 官方文件 | <https://modelcontextprotocol.io/> |
| MCP 規範 2025-11-25 | <https://modelcontextprotocol.io/specification/2025-11-25> |
| Discord 社群 | [Microsoft Foundry Discord](https://discord.gg/nTYy5BXMWG) |
| 翻譯工具 | [Azure Co-op Translator](https://github.com/Azure/co-op-translator) |
| 姊妹課程 | [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners), [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners), [AZD for Beginners](https://github.com/microsoft/AZD-for-beginners) |

## 課程概述

**MCP for Beginners** 是微軟 Foundry 團隊的官方 **Model Context Protocol (MCP) 入門課程**，2025-04-04 建立，到 2026-04-24 已累積 **15,932 stars / 5,200 forks**，屬於微軟「`X for beginners`」系列（Generative AI、AI Agents、ML、Data Science、Web Dev 等等）裡面新加入但成長最快的一員。

課程特色是：

1. **對齊最新穩定 MCP 規範 `2025-11-25`**（MCP 採用 `YYYY-MM-DD` 格式做版本號）
2. **跨 6 種程式語言同步提供範例**：C# (.NET) / Java / JavaScript / TypeScript / Python / Rust
3. **12 個模組（0–11），從「什麼是 MCP」一路到「生產級 PostgreSQL 整合」的 13 個 hands-on 實驗室**
4. **靠 Azure Co-op Translator 做多語言自動翻譯**，繁中版的 README 即是機翻產物，由 GitHub Action 持續同步

定位：完全不需要 MCP 背景、只要會其中一種主流程式語言（+ client-server / REST / HTTP 概念）就能上手。適合**第一次接觸 MCP 的開發者**、**想把 MCP 整合進企業應用的工程師**、**想用官方課程快速教團隊 MCP 的技術主管**。

## 課程結構

### 學習路徑分段

| 階段 | 模組 | 學習目標 |
|------|------|---------|
| 🌱 **基礎** | 0–2 | 搞懂「MCP 是什麼 / 為什麼要用 / 安全威脅」 |
| 🔨 **建置** | 3（含 3.1–3.15，15 個子單元） | 自己寫第一個 server / client，整合 VS Code、Cursor、Claude Desktop、Cline |
| 🚀 **成長** | 4–5 | 分頁、多模態、OAuth2、Entra ID、Azure Foundry、對抗性多代理推理 |
| 🌟 **精通** | 6–11 | 社群貢獻、最佳實踐、案例研究、AI Toolkit workshop、**13 個 PostgreSQL lab** |

### 模組 3「快速入門」的 15 個子單元（最實用的部分）

| # | 主題 | 學到什麼 |
|---|------|----------|
| 3.1 | 第一個伺服器 | 最小可跑的 MCP server |
| 3.2 | 第一個客戶端 | 基礎 MCP client |
| 3.3 | 搭配 LLM 的客戶端 | 接 OpenAI / Claude |
| 3.4 | VS Code 整合 | MCP server 掛 VS Code |
| 3.5 | stdio 伺服器 | stdio transport |
| 3.6 | HTTP 串流 | HTTP streaming transport |
| 3.7 | AI 工具組 | 搭配 Microsoft AI Toolkit |
| 3.8 | 測試 | MCP server 的測試策略 |
| 3.9 | 部署 | 丟到生產環境 |
| 3.10 | 進階伺服器 | 架構優化 |
| 3.11 | 簡單驗證 | 從零教 auth + RBAC |
| 3.12 | **MCP Hosts** | Claude Desktop、Cursor、Cline 等 host 設定 |
| 3.13 | **MCP Inspector** | 官方除錯工具用法 |
| 3.14 | 取樣（Sampling） | Client 反向餵 LLM 給 server |
| 3.15 | MCP Apps | 把 MCP 包成應用 |

### 模組 5「進階」亮點

- `5.3` **OAuth2 示範** + `5.12` **Microsoft Entra ID** ——企業導入必學
- `5.13` **Azure AI Foundry 整合** ——微軟把自家 Foundry 和 MCP 綁起來的官方 showcase
- `5.14` **上下文工程（Context Engineering）** ——這個詞 2026 年才流行起來，微軟課程已收錄
- `5.15` **自訂傳輸（Custom Transport）** ——超出 stdio / HTTP 的實作
- `5.17` **對抗性多代理推理** ——兩個 agent 用同一個 MCP toolset 辯論，由裁判 agent 評分（研究味很重）

### 模組 11「PostgreSQL Hands-On Labs」（13 個實驗室）

這是整個課程**最扎實的畢業專案**，跟著做就能產出一個生產級 MCP server：

```
11.1  介紹（零售分析案例）
11.2  核心架構（server / DB layer / 安全模式）
11.3  Row-Level Security、驗證、多租戶資料存取
11.4  環境設置（Docker + Azure 資源部署）
11.5  PostgreSQL 安裝、零售架構設計、範例資料
11.6  用 FastMCP 寫結合資料庫的 server
11.7  資料庫查詢工具 + schema profiler
11.8  Azure OpenAI + pgvector 做語意搜尋
11.9  測試 / 除錯 / 驗證
11.10 VS Code MCP 整合 + AI chat
11.11 Docker + Azure Container Apps 部署
11.12 Application Insights 監控
11.13 效能優化 / 安全加固 / 生產建議
```

### 程式碼範例矩陣

| 難度 | C# | Java | JavaScript | TypeScript | Python | Rust |
|------|----|----|----|----|----|----|
| 基礎計算機 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 進階 / 容器化 | ✅ | ✅（Spring） | ✅ | ✅（Container） | ✅ | — |

## 使用方式

```bash
git clone https://github.com/microsoft/mcp-for-beginners.git
cd mcp-for-beginners

# 直接從 README 開始，一路照著 Module 00 → 11 做
open translations/zh-TW/README.md
```

**專屬教學系列「Lets Learn MCP」**（每個語言都有獨立 aka.ms 短網址）：

| 語言 | 短網址 |
|------|--------|
| C# | <https://aka.ms/letslearnmcp-csharp> |
| Java | <https://aka.ms/letslearnmcp-java> |
| JavaScript | <https://aka.ms/letslearnmcp-javascript> |
| Python | <https://aka.ms/letslearnmcp-python> |

**學習地圖** 在 `study_guide.md`，附視覺化課程地圖 + 分技能層級路徑建議。

## 目前限制 / 注意事項

- **繁中版是 AI 機翻**（README 最後有 disclaimer）：由 Azure Co-op Translator 產出，品質不錯但術語偶爾不一致，遇到關鍵定義請回查英文原文
- **偏微軟生態**：模組 5 的 Azure Foundry、Entra ID、Application Insights 對非 Azure 用戶價值較低
- **規範會演進**：MCP 是活的協議（用日期版號），目前對齊 `2025-11-25`，未來半年規範變動時課程需同步更新，追 `changelog.md` 確認版本差異
- **部分進階主題深度有限**：課程廣度覆蓋很完整，但像 `5.15 Custom Transport`、`5.17 對抗性多代理`更多是 showcase 性質，做研究級應用仍需回讀 [MCP 官方 SDK](https://github.com/modelcontextprotocol) 原始碼
- **CLA 需求**：貢獻 PR 需簽 Microsoft CLA（只需一次、所有微軟 repo 共用）
- **Jupyter Notebook 是 primary language**：GitHub 標記主語言是 `Jupyter Notebook`，代表很多範例是 notebook 形式，terminal-only 使用者要多花工具配置

## 研究價值與啟示

### 關鍵洞察

1. **「MCP 是活的協議」這件事被正面處理**
   用 `YYYY-MM-DD` 格式做版本號、README 直接標示「本課程對齊 2025-11-25」、有獨立 `changelog.md` 追蹤變動——這是微軟教育團隊把「協議會動、教材會過時」當第一等公民設計出來的做法。對比其他 MCP 教程常常只寫「基於 MCP」卻不標版本，這是品質保證的一個關鍵。任何想做「追快速變動規範」的文件/教材都值得抄這套方法。

2. **跨語言範例矩陣背後的工程決策**
   同時維護 6 種語言的完整範例（C# / Java / JS / TS / Python / Rust）並不容易，微軟的做法是**讓每種語言都獨立成模組、各自有 README + aka.ms 短網址**，而不是寫一個語言當主、其他當譯本。這反映「MCP 是真的跨語言協議」，也避免讓某種語言變二等公民。對於做 SDK 文件的團隊是很好的範本。

3. **Azure Co-op Translator 是微軟教材全球化的基礎建設**
   README 底部註明繁中版是 AI 翻譯，但這個 AI 翻譯是靠 **GitHub Action 自動持續同步**，不是一次性翻完就不管。這個 pipeline 對任何想做「跟著原版 README 同步翻譯」的 open source 教材都值得研究——[Co-op Translator repo](https://github.com/Azure/co-op-translator) 本身就是一個可復用工具。

4. **模組 11 的 13 個 PostgreSQL lab 是隱藏金礦**
   很多人看到 15K stars 以為只是又一個介紹性教程，但模組 11 其實是個完整的「MCP + pgvector + Azure OpenAI + 語意搜尋 + RLS 多租戶 + Docker + ACA 部署 + App Insights 監控」的生產級範例。比起一堆 blog post 片段教程，這是微軟把「怎麼上線一個真的能給人用的 MCP server」一次寫清楚。

5. **對比 Anthropic 的 MCP 官方文件**
   [modelcontextprotocol.io](https://modelcontextprotocol.io/) 是協議規範和 SDK 文件為主，適合已經懂 MCP 的人查 API。微軟這套則是**從「你第一次聽到 MCP」的角度重新組織內容**，有類比、有 learning path、有 hands-on lab、有 host 設定教學。兩者互補——官方是 reference，微軟是 tutorial。

6. **模組 5.17「對抗性多代理推理」是研究味最重的單元**
   兩個 agent 共用一組 MCP 工具、針對同一問題辯論對立觀點、再由裁判 agent 評分——這其實是 [多 Agent 辯論會](multi-agent-debate.md) 那類 debate-based reasoning 的 MCP 實作版。可以看作是「把 debate 的 tool 存取層標準化」的示範。

### 與其他研究筆記的關聯

| 主題 | 關聯性 |
|------|--------|
| [MCP CLI](mcp-cli.md) / [MCPorter](mcporter.md) / [MCP Toolbox for Databases](mcp-toolbox.md) | 這些工具要配合 MCP 使用，本課程提供 host 設定 + 協議理解的基礎 |
| [Claude Agent SDK](claude-agent-sdk.md) / [Claude Code SDK (cloclo)](claude-code-sdk.md) | Claude 系列 SDK 底層也走 MCP；學完本課程再回看 Claude SDK 會清楚 host/server 分工 |
| [多 Agent 辯論會](multi-agent-debate.md) | 課程 5.17「對抗性多代理」是這類 debate 架構的 MCP 標準化版本 |
| [Browser-Bound MCP Flights](browser-bound-mcp-flights.md) | 屬於 MCP 應用；學完本課程能看懂它的 transport / auth 選型理由 |
| [Karpathy LLM Wiki](karpathy-llm-wiki.md) / [LLM Course](llm-course.md) | 同屬「大廠 / 大神開的 X for beginners」系列，對比不同廠商的教育敘事風格 |
| [OpenAI Agent 建構指南](openai-practical-guide-building-agents.md) | OpenAI 的 agent 教程 vs 微軟的 MCP 教程，代表不同陣營對「AI + tool」標準化的策略 |

**一句話總結**：如果你需要「**微軟官方、對齊最新 MCP 規範、跨 6 種語言、有 13 lab 畢業專案、有持續更新 pipeline**」的入門教材——這就是目前市面上最完整的一份，免費。對於要教團隊、寫 blog post 或準備企業導入 MCP 的人，這是第一個該讀的 repo。
