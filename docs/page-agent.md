# Page Agent 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [alibaba/page-agent](https://github.com/alibaba/page-agent) |
| 官方文件 | [Overview](https://alibaba.github.io/page-agent/docs/introduction/overview) |
| Demo | [Live Demo](https://alibaba.github.io/page-agent/) |
| npm | [page-agent](https://www.npmjs.com/package/page-agent) |
| Chrome 擴充套件 | [Page Agent Ext](https://chromewebstore.google.com/detail/page-agent-ext/akldabonmimlicnjlflnapfeklbfemhj) |
| HN 討論 | [Hacker News](https://news.ycombinator.com/item?id=47264138) |
| DEV.to 文章 | [PageAgent: The GUI Agent Living in Your Web Page](https://dev.to/simon_luv_pho/pageagent-the-gui-agent-living-in-your-web-page-1cda) |
| 作者 | Alibaba（[@simonluvramen](https://x.com/simonluvramen)） |
| Stars | ~13.3K |
| 授權 | MIT |
| 語言 | TypeScript |
| 建立時間 | 2025-09-23 |

## 專案概述

Page Agent 是阿里巴巴開源的**網頁內嵌 GUI Agent**，讓你用自然語言控制網頁介面。與主流瀏覽器自動化方案（browser-use、Playwright、Selenium）從外部控制瀏覽器不同，Page Agent 直接在網頁內以 JavaScript 執行，是一種「由內而外」（inside-out）的架構。

不需要 browser extension、Python 環境、headless browser，也不需要截圖或多模態 LLM。所有操作都是**文字型 DOM 操作**，LLM 只需處理文字即可，大幅降低成本與延遲。

因為運行在使用者實際的瀏覽器 session 中，Page Agent 天然繼承使用者的登入狀態——不需要管理密碼、cookie 或 OAuth，這是企業內部工具（ERP、CRM、採購系統）最大的痛點解決方案。

## 核心架構

### 運作原理

```
使用者指令 (自然語言)
        │
        ▼
┌──────────────────────┐
│   PageAgent (JS)     │
│                      │
│  1. DOM 解析         │──→ 將頁面 DOM 轉換為文字描述
│  2. LLM 請求         │──→ 傳給 LLM 理解頁面 + 決策
│  3. 動作執行         │──→ 在頁面內執行點擊/輸入/捲動
│  4. 迴圈至完成       │
└──────────────────────┘
        │
        ▼
  直接操作 DOM（無截圖、無 OCR）
```

### 與傳統方案的差異

| 面向 | 傳統方案（browser-use 等） | Page Agent |
|------|-------------------------|------------|
| 運行位置 | Server-side（外部程序） | Client-side（網頁內） |
| 視覺理解 | 截圖 + 多模態 LLM / OCR | 文字型 DOM 解析 |
| 部署方式 | 需後端基礎設施 | 一行 `<script>` 標籤 |
| 登入狀態 | 需管理 cookie / credential | 繼承瀏覽器 session |
| LLM 需求 | 多模態（視覺）模型 | 純文字 LLM 即可 |
| 資料流向 | 頁面 → 後端 → LLM | 頁面 → LLM（直連） |
| 適用場景 | 通用自動化 | SaaS 產品內嵌 AI Copilot |

### 模組化架構

Page Agent 提供分層的模組化套件：

| 套件 | 用途 |
|------|------|
| `page-agent` | 完整整合套件（turnkey） |
| `@page-agent/core` | Headless 核心引擎 |
| `@page-agent/llms` | LLM 客戶端抽象層 |
| `@page-agent/page-controller` | DOM 控制器 |
| `@page-agent/ui` | UI 面板（思考過程視覺化） |
| `@page-agent/extension` | Chrome 擴充套件 |
| `@page-agent/mcp` | MCP Server（Beta） |

## 支援的 LLM

採用 **Bring Your Own LLM** 架構，無後端依賴，資料直接從頁面傳到你配置的 LLM：

| 供應商 | 模型範例 |
|--------|---------|
| Alibaba Qwen | qwen3.5-plus |
| OpenAI | GPT 系列 |
| Anthropic | Claude |
| Google | Gemini |
| DeepSeek | DeepSeek |
| xAI | Grok |
| 本地推論 | Ollama（需 ≥ 9B 參數） |

!!! warning "小模型限制"
    作者在 HN 討論中確認：「小於 9B 參數的模型無法處理 Page Agent 複雜的 tool call schema」。

## 使用場景

| 場景 | 說明 |
|------|------|
| **SaaS AI Copilot** | 幾行程式碼在產品中嵌入 AI 副駕駛，不需改後端 |
| **智慧表單填寫** | 把 20 次點擊的流程壓縮成一句話，適合 ERP、CRM、管理系統 |
| **無障礙存取** | 用自然語言操作任何 Web 應用，語音指令、螢幕閱讀器、零門檻 |
| **多頁面 Agent** | 搭配 Chrome 擴充套件，跨瀏覽器分頁操作 |
| **企業內部工具** | 導航供應商入口網站、內部差旅預訂系統等，保留使用者認證 |

## 快速開始

### 一行整合（Demo 模式）

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.6.1/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

> ⚠️ 僅供技術評估。Demo CDN 使用免費測試 LLM API，資料會傳至阿里雲。

### NPM 安裝

```bash
npm install page-agent
```

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_API_KEY',
    language: 'en-US',
})

await agent.execute('Click the login button')
```

### Chrome 擴充套件（多頁面）

```javascript
const result = await window.PAGE_AGENT_EXT.execute(
  'Compare top 3 results for "wireless keyboard" on Amazon',
  { /* config */ }
)
```

## 擴充功能

- **Custom Tools**：註冊自訂工具擴展 Agent 能力
- **Lifecycle Hooks**：掛載生命週期事件
- **Prompt 自訂**：覆寫系統 prompt
- **Data Masking**：敏感資料遮罩功能
- **Thinking Panel**：內建思考面板，視覺化 Agent 推理過程，使用者可在執行前介入

## 目前限制與注意事項

### 技術限制

| 限制 | 說明 |
|------|------|
| **Shadow DOM** | 不支援，作者刻意排除 |
| **Canvas / WebGL** | 不支援，WebGL2 相依可能導致停用 WebGL 的系統崩潰 |
| **巢狀 iframe** | DOM 序列化的邊界案例 |
| **CAPTCHA** | 文字型方法無法處理視覺驗證碼 |
| **長按 / 拖曳** | 尚未支援 |
| **Firefox** | 尚未支援（計畫中） |
| **小型 LLM** | < 9B 參數的模型無法處理複雜 tool call schema |

### 安全考量

根據 HN 社群討論，主要安全疑慮：

1. **CSP（Content Security Policy）障礙**：許多企業網站的 CSP 會阻擋外部腳本注入，需要明確白名單
2. **權限與認證**：Agent 以 JavaScript 標準權限運行，等同於任何第三方腳本的權限層級
3. **資料隱私**：免費測試 LLM API 託管於中國大陸，正式使用建議配置自有 LLM 或本地 Ollama
4. **跨分頁存取**：Chrome 擴充套件的跨分頁操作需要使用者明確授權

### DOM 序列化挑戰

HN 上有經驗豐富的嵌入式腳本開發者指出：

> HTML dehydration 的複雜度會隨時間增長，Shadow DOM、canvas、巢狀 iframe 的邊界案例會持續浮現。Serialization fidelity 直接影響任務成功率。

## 致謝與淵源

Page Agent 的 DOM 處理元件和 prompt 衍生自 [browser-use](https://github.com/browser-use/browser-use)（MIT 授權），但定位完全不同：

- **browser-use**：server-side 瀏覽器自動化
- **Page Agent**：client-side 網頁增強

## 研究價值與啟示

### 關鍵洞察

1. **「由內而外」是更務實的路線**：對於 SaaS 產品內嵌 AI 功能，Page Agent 的 inside-out 架構比傳統的 outside-in 自動化更合理——不需要後端基礎設施、天然繼承認證狀態、部署成本極低
2. **文字型 DOM > 截圖型**：不需要多模態 LLM 是巨大優勢，純文字 LLM 更便宜、更快、選擇更多（甚至可以用本地 Ollama），但代價是無法處理 Canvas/WebGL 等非 DOM 內容
3. **漸進式整合策略值得借鑑**：從一行 `<script>` → NPM 套件 → Chrome 擴充套件 → MCP Server，每一層都是可選的，降低採用門檻
4. **MCP 生態連結是戰略佈局**：Beta 版 MCP Server 讓外部 Agent（如 Claude Code）也能控制網頁，把 Page Agent 從「產品內嵌工具」提升為「Agent 生態的網頁介面層」
5. **9B 參數是實用門檻**：作者明確指出小模型無法處理複雜 tool call schema，這對選型有直接指導意義

### 與其他專案的關聯

| 對比專案 | 關聯 |
|---------|------|
| [browser-use](https://github.com/browser-use/browser-use) | Page Agent 的 DOM 處理衍生自此，但從 server-side 轉為 client-side |
| [Playwright](https://playwright.dev/) / [Selenium](https://www.selenium.dev/) | 傳統 outside-in 自動化，Page Agent 是完全不同的 inside-out 路線 |
| MCP 生態 | Page Agent 的 MCP Server 讓它能被 Claude Code 等外部 Agent 控制 |
| 本站 [CrewAI](crewai.md) / [LangChain](langchain.md) | 後端 Agent 框架可透過 MCP 與 Page Agent 協作，形成前後端 Agent 組合 |
