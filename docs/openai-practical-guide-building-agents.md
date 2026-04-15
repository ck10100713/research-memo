---
date: "2026-04-15"
category: "學習資源"
card_icon: "material-book-open-variant"
oneliner: "OpenAI 官方 34 頁 Agent 建構指南 — 定義、設計基礎、編排模式、護欄，從客戶部署提煉的最佳實踐"
---

# OpenAI: A Practical Guide to Building Agents 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原始 PDF | [OpenAI CDN](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| 官方頁面 | [openai.com](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) |
| DEV.to 摘要 | [OpenAI's Agent building guide - summary](https://dev.to/ivor/openais-agent-building-guide-summary-56jg) |
| Substack 深度分析 | [Rich Turrin 分析](https://richturrin.substack.com/p/openai-a-practical-guide-to-building) |
| Indie Hackers 分解 | [Breakdown](https://www.indiehackers.com/post/openais-a-practical-guide-to-building-agents-breakdown-c4255ce392) |
| 精簡版 Google Sheet | [cognizix.com](https://cognizix.com/openai-practical-guide-to-building-agents/) |

**發布者：** OpenAI · 34 頁 · 免費 PDF · 2025 年發布

## 文件概述

這是 OpenAI 官方發布的 **34 頁 AI Agent 建構實務指南**，從大量客戶部署經驗中提煉出最佳實踐，目標讀者是「探索如何建構第一個 Agent」的產品和工程團隊。

核心論點：Agent 與傳統軟體的根本差異在於——傳統軟體依賴人類處理非確定性決策點，**Agent 可以接管部分非確定性的詮釋步驟**。

> 雖然程式碼範例使用 OpenAI 模型，但概念適用於所有 LLM。

## 七大章節結構

### 1. 什麼是 Agent？

**定義：** Agent 是能「通過模糊性推理、跨工具採取行動、自主處理多步驟任務」的獨立系統。

**Agent 循環（Agentic Cycle）：**
```
評估當前知識 → 判斷是否需要更多上下文 → 採取行動 → 比較進度與目標 → 重複
```

**三大核心組件：**

| 組件 | 說明 |
|------|------|
| **Model** | 驅動推理和決策的 LLM |
| **Tools** | Agent 可呼叫的外部功能或 API |
| **Instructions** | 定義 Agent 行為的明確指引和護欄 |

### 2. 何時該建 Agent？

Agent 適合三種場景：

| 場景 | 為什麼需要 Agent |
|------|-----------------|
| **複雜決策** | 結果非二元對立，需在灰色地帶做判斷 |
| **難以維護的規則** | 規則龐大且頻繁更新，傳統自動化無法跟上 |
| **大量非結構化數據** | 需要推理和詮釋，而非簡單的規則匹配 |

### 3. 設計基礎

#### Model 選擇
- **先用最強模型**，再根據可量化結果向下優化
- 考量：context window、延遲、本地 vs 雲端、成本

#### Tool 設計（三類工具）

| 類型 | 說明 | 範例 |
|------|------|------|
| **Data Gathering** | 取得資訊 | 查資料庫、搜尋、讀檔 |
| **World-Affecting** | 改變外部狀態 | 發送訊息、更新記錄、下單 |
| **Orchestration** | 協調其他 Agent | 呼叫子 Agent、分派任務 |

**工具文件化原則：** 清晰的文件幫助 Agent 發現和正確使用工具，防止誤用。

#### Instructions 設計
- **減少模糊性** → 改善決策 → 更順暢的工作流 → 更少錯誤
- 明確指定動作
- 利用現有的業務文件
- 預先處理已知的邊界案例

### 4. 編排模式（Orchestration）

```
簡單 ────────────────────────────────────────── 複雜

Single Agent    →    Handoffs    →    Manager    →    Decentralized
（單一 Agent）     （交接模式）    （經理模式）     （去中心化）
```

| 模式 | 架構 | 適用場景 |
|------|------|---------|
| **Single Agent** | 一個 Agent 擁有所有工具 | 任務簡單，工具數量少 |
| **Handoffs** | Agent 間直接交接控制 | 明確的階段劃分 |
| **Manager** | 一個 supervisor 協調多個 specialist Agent | 需要綜合多個來源 |
| **Decentralized** | Agent 自主決定交接給誰 | 高度動態的工作流 |

**核心建議：**
> 「Start with a single agent and validate the use case. Progress to multi-agent orchestration only when necessary.」
>
> 偏好**簡單、聚焦的 Agent**，而非複雜的 Agent：
> - 降低認知負擔
> - 更容易驗證
> - 提升可組合性

### 5. 護欄（Guardrails）

#### 三層護欄

| 層級 | 護欄類型 | 功能 |
|------|---------|------|
| **Input** | Relevance Classifier | 過濾離題查詢（如「帝國大廈多高？」） |
| | Safety Classifier | 偵測 jailbreak、prompt injection |
| | PII Filter | 防止敏感資料洩漏 |
| | Moderation | 標記有害/不當內容 |
| **Output** | Output Validation | 確保回應符合品牌價值 |
| | Content Check | 防止品牌損害的輸出 |
| **Tool** | Risk Rating | 按存取類型/可逆性/權限/財務影響分級（低/中/高） |
| | Rules-based | Blocklist、輸入限制、regex 過濾 |

**關鍵設計原則：**
> 「Guards can run concurrently with some of the steps and only intervene when their conditions are breached.」
>
> 護欄**樂觀地與核心操作平行執行**，只在違反條件時介入——不拖慢正常流程。

#### 人類介入觸發點

| 觸發條件 | 範例 |
|---------|------|
| 超過失敗閾值 | Agent 重試次數達上限 |
| 高風險操作 | 取消訂單、大額退款、處理付款 |

### 6. 實作建議

| 原則 | 說明 |
|------|------|
| 從單一 Agent 開始 | 驗證用例後再擴展到多 Agent |
| 用確定性工具防幻覺 | 讓 Agent 呼叫確定性函式而非自由生成 |
| 護欄平行執行 | 樂觀執行，不阻塞主流程 |
| 先用最強模型 | 確認可行性後再降級優化成本 |
| 從通用到特定 | 護欄從通用保護開始，再加特定防護 |

## 目前限制 / 注意事項

- **OpenAI 中心化** — 程式碼範例和工具都基於 OpenAI API（Responses API、Agents SDK），但概念可推廣
- **偏重企業場景** — 從客戶部署經驗提煉，對個人開發者場景較少著墨
- **無開源範例** — 不像 Anthropic 的 Claude Code 有完整的開源 harness 設計
- **34 頁較淺** — 對複雜主題（如 multi-agent 協調、記憶管理）的深度有限
- **缺乏評估框架** — 提到需要 evaluation 但未給出具體方法論

## 研究價值與啟示

### 關鍵洞察

1. **「先單 Agent，再多 Agent」是最重要的建議。** 這與社群的炒作方向完全相反——大家急著做 multi-agent swarm，OpenAI 卻說「先證明一個 Agent 能解決問題」。Boris Cherny 的 Claude Code 經驗也印證了這點：他的主要工作流是一個 Claude 做規劃 + 一個 Claude 做 review，而非複雜的 Agent 網路。

2. **護欄平行執行（Optimistic Guards）是務實的工程選擇。** 不是先檢查再執行（同步），而是邊執行邊檢查（平行）——只在違規時介入。這大幅減少了延遲，且對多數正常請求零開銷。這個模式對任何需要安全檢查的 Agent 系統都有參考價值。

3. **工具的三分類（Data/World-Affecting/Orchestration）是實用的思考框架。** 區分「讀取」和「改變世界」的工具，直接影響護欄設計：Data 工具可以自由呼叫，World-Affecting 工具需要風險分級。Claude Code 的 permission 系統本質上就是這個框架。

4. **「Instructions 減少模糊性」比「更聰明的模型」更重要。** OpenAI 自己說好的 instructions 帶來的效益是「改善決策 → 更少錯誤」。這呼應了 tw-house-ops 和 Claude Ads 的經驗——精心設計的 prompt/mode 檔案（而非更大的模型）才是品質的決定因素。

5. **這份指南的定位是「OpenAI 版的 Agent 設計模式」。** 就像 GoF 的設計模式一樣，OpenAI 嘗試把 Agent 開發的最佳實踐標準化。不管你用哪家 LLM，Single Agent → Handoffs → Manager → Decentralized 的漸進式編排都是合理的路徑。

### 與其他專案的關聯

- **vs Boris Cherny 57 Tips：** Boris 的 tips 是 Claude Code 實戰技巧，OpenAI 指南是理論框架。Boris 的「先 plan mode 再執行」對應指南的「先單 Agent 驗證」；Boris 的「驗證迴圈」對應指南的「護欄」。
- **vs Multica：** Multica 實作了指南中「Manager 模式」的具體版本——一個平台管理多個 Coding Agent，每個 Agent 是 specialist。
- **vs wshobson/agents：** 77 個插件的四層模型策略（Opus/Inherit/Sonnet/Haiku）是指南中「先用最強模型，再降級」的具體實踐。
- **vs Harness Design（筆記庫中）：** Anthropic 的 harness 設計文件和 OpenAI 的 Agent 指南是兩大 LLM 廠商對 Agent 架構的不同詮釋——值得對照閱讀。
- **對 fluffy-agent-core 的啟示：** 指南的編排模式可以直接對應：fluffy-agent-core 目前適合 Single Agent → Handoffs 階段，未來擴展時再考慮 Manager 模式。
