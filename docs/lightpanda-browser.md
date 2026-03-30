---
date: ""
category: "Coding Agent 工具"
card_icon: "material-lightning-bolt"
oneliner: "用 Zig 從零打造的 headless browser，比 Chrome 快 11x、省 9x 記憶體，專為 AI Agent 設計"
---
# Lightpanda Browser 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [lightpanda-io/browser](https://github.com/lightpanda-io/browser) |
| 官網 | [lightpanda.io](https://lightpanda.io) |
| 效能基準測試 | [lightpanda-io/demo](https://github.com/lightpanda-io/demo) |
| CDP vs Playwright vs Puppeteer | [官方部落格](https://lightpanda.io/blog/posts/cdp-vs-playwright-vs-puppeteer-is-this-the-wrong-question) |
| Linuxiac 評測 | [Lightpanda Promises a Faster Alternative to Headless Chrome](https://linuxiac.com/lightpanda-promises-a-faster-lightweight-alternative-to-headless-chrome/) |
| emelia.io 深度分析 | [Everything You Need to Know](https://emelia.io/hub/lightpanda-headless-browser) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 團隊 | Lightpanda (法國) |
| Stars | 24K+ |
| 語言 | Zig |
| 授權 | AGPL-3.0 |
| 建立 | 2023-02-07 |
| 狀態 | Beta |

Lightpanda 是一款**從零打造的 headless browser**，專為 AI Agent 和自動化場景設計。**不是 Chromium fork、不是 WebKit patch**，而是用系統級語言 Zig 從空白頁面開始寫的全新瀏覽器。

核心設計哲學：砍掉所有人類不需要看的東西（CSS 排版、圖片解碼、GPU 合成、字型渲染、無障礙樹），只保留自動化需要的核心——DOM 樹、JavaScript 執行、網路請求。

## 效能基準

> 基準環境：AWS EC2 m5.large，Puppeteer 請求 100 頁本地網站

| 指標 | Headless Chrome | Lightpanda | 差距 |
|------|----------------|------------|------|
| 執行時間（100 頁） | 25.2 秒 | **2.3 秒** | **11x 快** |
| 峰值記憶體 | 207 MB | **24 MB** | **9x 少** |
| 100 tabs 並行（933 頁） | > 1 小時 | **< 5 秒** | 數量級差距 |
| 並行擴展 | 5 tabs 後退化 | 線性擴展至 ~25 processes | — |
| 同等 RAM 可開啟 sessions | ~9 | **~80** | **9x 多** |

## 技術架構

```
┌─────────────────────────────────────────────────┐
│              Lightpanda Browser                  │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ libcurl  │  │ html5ever│  │ V8 (zig-js)   │  │
│  │ HTTP 層  │  │ HTML 解析│  │ JavaScript 引擎│  │
│  └────┬─────┘  └────┬─────┘  └───────┬───────┘  │
│       │              │                │          │
│       ▼              ▼                ▼          │
│  ┌──────────────────────────────────────────┐    │
│  │              DOM Tree                     │    │
│  │  (無 CSS layout / 無圖片 / 無 GPU 合成)    │    │
│  └──────────────────┬───────────────────────┘    │
│                     │                            │
│  ┌──────────────────▼───────────────────────┐    │
│  │         CDP WebSocket Server              │    │
│  │     (Chrome DevTools Protocol)            │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────┘
                      │ ws://
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
   Puppeteer     Playwright      chromedp
```

### 關鍵元件

| 元件 | 技術 | 說明 |
|------|------|------|
| HTTP 載入器 | [libcurl](https://curl.se/libcurl/) | 成熟穩定的 HTTP 實作 |
| HTML 解析器 | [html5ever](https://github.com/servo/html5ever) | Mozilla Servo 的 HTML5 解析器 |
| JS 引擎 | [V8](https://v8.dev/) (via zig-js-runtime) | 與 Chrome 相同的 JS 引擎 |
| 協議 | CDP (Chrome DevTools Protocol) | 300+ 指令，WebSocket + JSON |

### 刻意省略的元件

- CSS layout engine
- 圖片解碼器
- GPU 合成器
- 字型渲染器
- 無障礙樹 (Accessibility tree)

這些是 Chrome headless 仍然執行的步驟。Lightpanda 直接跳過，這就是 11x 速度差距的來源。

## 已支援功能

| 功能 | 狀態 |
|------|------|
| JavaScript 執行 | ✅ |
| DOM APIs | ✅ |
| XHR / Fetch API | ✅ |
| CDP WebSocket Server | ✅ |
| Click / Input form | ✅ |
| Cookies | ✅ |
| 自訂 HTTP Headers | ✅ |
| Proxy 支援 | ✅ |
| Network interception | ✅ |
| `robots.txt` 遵守 | ✅ (`--obey_robots`) |
| Web APIs（部分） | 🚧 進行中 |

## 快速開始

```bash
# macOS 安裝
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos
chmod a+x ./lightpanda

# 擷取頁面
./lightpanda fetch --obey_robots --log_format pretty https://example.com

# 啟動 CDP server（供 Puppeteer/Playwright 連接）
./lightpanda serve --host 127.0.0.1 --port 9222
```

Docker：

```bash
docker run -d --name lightpanda -p 9222:9222 lightpanda/browser:nightly
```

Puppeteer 連接（零程式碼修改，只改 endpoint）：

```js
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});
// 其餘 script 完全不變
```

## Puppeteer vs Playwright 搭配差異

| 項目 | Puppeteer | Playwright |
|------|-----------|------------|
| CDP 通訊量（等效任務） | 11 KB WebSocket messages | 326 KB |
| 策略 | 原生 CDP 指令為主 | 大量 JavaScript 執行以跨瀏覽器 |
| 搭配 Lightpanda 效能 | **快 15-20%** | 略慢（JS 執行層更重） |
| 相容穩定度 | 較佳（CDP native） | 可能因新增 Web API 觸發未實作路徑 |

> Playwright 會根據瀏覽器回報的功能選擇執行策略。當 Lightpanda 新增 Web API 時，Playwright 可能切換到嘗試使用尚未實作功能的程式碼路徑。

## 目前限制 / 注意事項

- **Beta 狀態**：仍可能遇到錯誤或當機，複雜 SPA（React/Vue 重度框架）可能有 edge cases
- **Web API 覆蓋不完整**：數百個 Web API 中僅支援部分，coverage 持續增加中
- **無渲染能力**：需要截圖、視覺測試、PDF 生成的場景不適用
- **Playwright 相容性風險**：版本更新可能觸發未實作的 code path
- **AGPL-3.0 授權**：商業 SaaS 使用需注意開源義務
- **預設遙測**：需手動設 `LIGHTPANDA_DISABLE_TELEMETRY=true` 關閉
- **CLA 要求**：貢獻需簽署 Contributor License Agreement

## 研究價值與啟示

### 關鍵洞察

1. **Headless browser 的「過度渲染」問題終於被正面挑戰**：Chrome headless 仍執行完整渲染管線（CSS layout → paint → composite），即使沒有人在看。Lightpanda 的 11x 速度提升證明了對 AI Agent 和爬蟲而言，90% 的瀏覽器工作是浪費的。這不是漸進優化，而是重新定義「headless browser 到底需要什麼」。

2. **Zig 語言在基礎設施層的驗證**：選擇 Zig 而非 Rust/C++ 是大膽的技術賭注。Zig 的零成本抽象 + 無 GC + 手動記憶體控制，讓 Lightpanda 在同等功能下實現 9x 記憶體優勢。這為 Zig 在高效能基礎設施領域提供了有力的實戰驗證。

3. **CDP 協議是 headless browser 生態的通用語言**：Lightpanda 不用自己發明新的自動化協議，直接實作 CDP 就能讓現有 Puppeteer/Playwright script 無縫遷移。這個策略避免了生態系統冷啟動問題——使用者不需要學新東西，只需要改一行 endpoint。

4. **AI Agent 爬蟲場景的基礎設施瓶頸正在被解決**：當一台機器能跑 80 個 Lightpanda session（vs 9 個 Chrome session），AI Agent 的「眼睛」（瀏覽器）成本直接降到 1/9。這對需要大量網頁互動的 Agent 系統（如 Project Golem、Page Agent）是基礎性的賦能。

5. **「不做什麼」比「做什麼」更重要**：Lightpanda 的核心競爭力不是它做了什麼新功能，而是它勇敢地砍掉了 Chrome 80% 的功能。這是一個優秀的產品設計案例——為特定用例極度優化，而非試圖成為通用瀏覽器。

### 與其他專案的關聯

- **vs Project Golem**：Golem 是 Browser-in-the-Loop 的 AI Agent，依賴完整瀏覽器能力。Lightpanda 可以作為 Golem 類 Agent 的輕量化替代——在不需要視覺渲染的任務中，用 Lightpanda 替代 Chrome 可以大幅降低資源消耗。
- **vs Page Agent**：阿里巴巴的 Page Agent 需要 GUI 互動能力，Lightpanda 目前不適合（無渲染）。但對於 Page Agent 的資料擷取前處理階段，Lightpanda 是理想選擇。
- **對 AI Agent 生態的影響**：任何使用 Puppeteer/Playwright 的 Agent 框架都能直接受益——只需換 endpoint，無需改程式碼。這使得 Lightpanda 成為 AI Agent 基礎設施層的重要一環。
