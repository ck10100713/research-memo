# Page Agent 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/alibaba/page-agent |
| 官方文件 | https://alibaba.github.io/page-agent/docs/introduction/overview |
| Demo | https://alibaba.github.io/page-agent/ |
| npm | https://www.npmjs.com/package/page-agent |
| HN 討論 | https://news.ycombinator.com/item?id=47264138 |
| 作者 | Alibaba |
| Stars | ~13.3K |
| 授權 | MIT |
| 語言 | TypeScript |

## 專案概述

Page Agent 是阿里巴巴開源的**網頁內嵌 GUI Agent**，讓你用自然語言控制網頁介面。與其他瀏覽器自動化工具（如 browser-use、Playwright）不同，Page Agent 不需要瀏覽器擴充套件、Python 環境或 headless browser——所有操作都在網頁內透過 JavaScript 完成。

### 核心特色

- **純前端整合**：不需要 browser extension、Python 或 headless browser，只需要 in-page JavaScript
- **文字型 DOM 操作**：不需要截圖、不需要多模態 LLM 或特殊權限
- **自帶 LLM**：支援接入自己的 LLM（Bring Your Own LLM）
- **Chrome 擴充套件**（選用）：跨頁面任務支援
- **MCP Server**（Beta）：從外部控制瀏覽器

## 使用場景

| 場景 | 說明 |
|------|------|
| **SaaS AI Copilot** | 幾行程式碼就能在產品中嵌入 AI 副駕駛，不需改後端 |
| **智慧表單填寫** | 把 20 次點擊的流程壓縮成一句話，適合 ERP、CRM、管理系統 |
| **無障礙存取** | 用自然語言操作任何 Web 應用，語音指令、螢幕閱讀器、零門檻 |
| **多頁面 Agent** | 搭配 Chrome 擴充套件，讓 Agent 跨瀏覽器分頁操作 |

## 快速開始

### 一行整合（Demo 模式）

最快速的體驗方式，使用免費的 Demo LLM：

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.6.1/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

> ⚠️ 僅供技術評估使用，使用免費測試 LLM API。

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

## 技術架構

### 與其他方案的差異

```
傳統瀏覽器自動化                     Page Agent
┌─────────────────────┐            ┌─────────────────────┐
│ 需要 Python 後端     │            │ 純前端 JavaScript    │
│ 需要 headless browser│            │ 直接在網頁內運行      │
│ 需要截圖 + 多模態 LLM│            │ 文字型 DOM 操作       │
│ 需要瀏覽器擴充套件    │            │ 擴充套件為選用        │
│ Server-side 自動化   │            │ Client-side 增強     │
└─────────────────────┘            └─────────────────────┘
```

### 核心設計

1. **DOM 處理**：將網頁 DOM 轉換為文字描述，傳給 LLM 理解頁面結構
2. **LLM 決策**：LLM 根據使用者指令和 DOM 描述，決定要執行的操作
3. **動作執行**：在網頁內直接執行點擊、輸入、捲動等操作

### 致謝

專案的 DOM 處理元件和 prompt 衍生自 [browser-use](https://github.com/browser-use/browser-use)，但定位完全不同：

- **browser-use**：server-side 瀏覽器自動化
- **Page Agent**：client-side 網頁增強

## 研究價值

### 輕量級 Web Agent 的新路線

Page Agent 代表了一種與主流不同的 Web Agent 思路：

| 面向 | 主流方案（browser-use 等） | Page Agent |
|------|-------------------------|------------|
| 運行環境 | Server-side | Client-side（瀏覽器內） |
| 視覺理解 | 截圖 + 多模態 LLM | 文字型 DOM 解析 |
| 部署方式 | 需要後端基礎設施 | 一行 `<script>` 標籤 |
| 適用場景 | 通用自動化 | SaaS 產品內嵌 |
| LLM 需求 | 多模態（視覺） | 純文字 LLM 即可 |

### 關鍵洞察

1. **不需要截圖**：文字型 DOM 操作夠用，大幅降低 LLM 成本和延遲
2. **前端優先**：把 Agent 嵌入產品本身，而非從外部控制，使用者體驗更自然
3. **漸進式整合**：從一行 script 到完整 NPM 套件，再到 Chrome 擴充套件和 MCP Server，按需選擇
4. **MCP 生態整合**：Beta 版 MCP Server 讓外部 Agent 也能控制網頁，連結更大的 Agent 生態
