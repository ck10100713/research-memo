---
date: ""
category: "Coding Agent 工具"
icon: "material-airplane-search"
oneliner: "四層架構拆解：Rust Bridge + Chrome Extension + Tailscale，讓 AI Agent 在真實瀏覽器查 Google Flights 機票"
---
# Browser-Bound MCP 機票查詢工具 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 架構截圖 | 7 張截圖拆解（Claude Code / Kiro CLI chat session） |
| 相關概念：WebMCP | [Chrome for Developers Blog](https://developer.chrome.com/blog/webmcp-epp) |
| 相關專案：Google Flights MCP (Fli) | [punitarani/fli](https://github.com/punitarani/fli) |
| 相關專案：Rust Browser MCP | [EmilLindfors/rust-browser-mcp](https://github.com/EmilLindfors/rust-browser-mcp) |
| ITA Matrix | [matrix.itasoftware.com](https://matrix.itasoftware.com) |

## 專案概述

這是一個**自建的 Browser-Bound MCP 工具**，讓 AI Agent（Kiro、Claude 等）能透過 MCP 協議呼叫 Google Flights 搜尋機票。不是公開的 GitHub repo，而是從截圖中拆解出的架構模式研究。

核心創新在於 **「Browser-Bound MCP」架構**：不用 headless browser 或逆向 API，而是直接操控真實瀏覽器（Brave）的 DOM——帶著使用者的 cookies、登入狀態、語言偏好，結果與人工操作完全一致。

使用場景：在 Kiro CLI chat（persona「諸葛亮」）中，一句話查詢多段機票，Agent 自動拆解需求、組合最便宜的航線。

## 技術架構

### 四層架構圖

```
┌──────────────────────────────────────────────┐
│  AI Agent (任何 Tailnet 上的裝置)              │
│  e.g. Kiro CLI, Claude Code, etc.            │
└──────────────┬───────────────────────────────┘
               │ HTTP SSE (MCP protocol)
               │ http://100.115.238.40:3000/sse
               ▼
┌──────────────────────────────────────────────┐
│  Rust Bridge (0.0.0.0:3000)                  │
│  ┌──────────┐ ┌────────────┐ ┌────────────┐ │
│  │SSE Server│↔│MCP Handler │↔│WS Forwarder│ │
│  │ (axum)   │ │            │ │            │ │
│  └──────────┘ │search_flts │ └─────┬──────┘ │
│               │scrape_res  │       │        │
│               └────────────┘       │        │
└────────────────────────────────────┼────────┘
               │ WebSocket ws://127.0.0.1:9222
               │ (localhost only!)
               ▼
┌──────────────────────────────────────────────┐
│  Chrome Extension (MV3, in Brave)            │
│  ┌──────────────┐    ┌────────────────────┐  │
│  │background.js │───→│content.js          │  │
│  │• WS client   │chrome│(Google Flights tab)│  │
│  │• keep-alive  │.tabs │• buildFlightsUrl()│  │
│  │  (25s alarm) │.send │• scrapeResults()  │  │
│  │• auto-reconn │Msg  │• CAPTCHA detect   │  │
│  └──────────────┘    └─────────┬──────────┘  │
└────────────────────────────────┼──────────────┘
               │ DOM scraping
               ▼
┌──────────────────────────────────────────────┐
│  google.com/travel/flights                   │
│  (真實 Brave session, cookies/login)          │
└──────────────────────────────────────────────┘
```

### 安全設計要點

| 設計 | 說明 |
|------|------|
| **WebSocket localhost-only** | Extension 只在 `127.0.0.1:9222` 監聽，永不暴露到網路 |
| **SSE 走 Tailnet** | MCP endpoint `100.115.238.40:3000` 只在 Tailscale VPN 內可達 |
| **Browser 不離開本機** | 只有結構化的 MCP tool call 跨網路傳輸，瀏覽器操作完全在本地 |
| **故障隔離** | Extension keep-alive (25s alarm) + auto-reconnect，斷線自動恢復 |

### MCP 暴露的 Tools

```
1. search_flights — 導航 Google Flights 並爬取結果
   ├── origin (required)         — 機場代碼或城市名
   ├── destination (required)    — 機場代碼或城市名
   ├── departure_date (required) — YYYY-MM-DD
   ├── return_date (optional)    — YYYY-MM-DD, 省略 = 單程
   └── passengers (optional)     — 預設 1

2. scrape_results — 重新爬取當前 Google Flights 頁面（不重新導航）
```

## 實戰 Demo：台北→首爾→東京→台北

截圖展示了一次多段機票查詢的完整流程：

### Round-trip 查詢（Agent 自動分段）

| 段 | 航線 | 日期 | 航空公司 | 時間 | 票價 |
|---|------|------|----------|------|------|
| 1 | TPE→ICN | 4/6 | Scoot | 6:10→9:45 PM | NT$7,257 |
| 2 | ICN→NRT | 4/8 | Jeju Air | 1:20→3:50 PM | NT$9,671 |
| 3 | NRT→TPE | 4/11 | Scoot | 12:30→3:05 PM | NT$11,270 |
| | | | **三段最低總價** | | **NT$28,198** |

### 單程改查（Agent 發現價差洞察）

Agent 發現上述「單程」其實查的是 round-trip 價格，改用真正的 one-way 搜尋後：

| 段 | 航空公司 | 時間 | 單程價 |
|---|----------|------|--------|
| TPE→ICN 4/6 | Scoot | 6:10→9:45 PM | NT$3,891 |
| ICN→NRT 4/8 | ZIPAIR | 12:55→3:30 PM | NT$4,153 |
| NRT→TPE 4/11 | Thai Lion Air | 5:40→8:20 PM | NT$6,464 |
| **三段總計** | | | **NT$14,508** |

!!! tip "關鍵洞察"
    Round-trip 查 NT$28,198 vs. 真正 one-way 組合 NT$14,508 = **省 NT$13,690（近一半）**。
    這是 Agent 自己發現的，人工操作很難想到逐段改查 one-way。

### 機票搜尋策略（ITA Matrix + Google Flights）

```
┌─────────────────────┐     ┌──────────────────────┐
│  ITA Matrix          │     │  Google Flights       │
│  = Discovery         │ ──→ │  = Validation         │
│  (理論最低價)         │     │  (實際可訂)            │
│                      │     │                       │
│  • 搜所有 fare class │     │  • 確認是否可買         │
│  • hidden city combo │     │  • 取得預訂連結         │
│  • open jaw 組合     │     │  • 台灣在地支援好       │
└─────────────────────┘     └──────────────────────┘
```

## 架構的通用性

截圖明確指出：**架構本身是通用的**。目前只為 Google Flights 寫了 content script，但 `bridge ↔ WebSocket ↔ extension ↔ content script ↔ DOM` 這個模式可以適用於任何網站。

新增一個網站只需要：

1. 新的 `content.js`（該網站的 DOM 爬取邏輯）
2. `background.js` 加新的 message type
3. Rust Bridge 加新的 MCP tool

Bridge 和 WebSocket 管線完全不用改。

## 目前限制 / 注意事項

- **非公開專案**：沒有 GitHub repo，無法直接使用，僅供架構參考
- **Google Flights DOM 脆弱性**：DOM 結構隨時可能改版，content.js 需持續維護
- **CAPTCHA 風險**：雖有偵測邏輯，但高頻率查詢仍可能觸發 Google 反爬
- **單機限制**：需要在本機跑 Brave + Extension + Rust Bridge，不能 serverless 部署
- **Tailscale 依賴**：跨裝置使用需要 Tailscale VPN，增加一層基礎建設
- **手動維護成本**：Rust Bridge + Chrome Extension MV3 + content script 三個元件需同步維護

## 研究價值與啟示

### 關鍵洞察

1. **「真實瀏覽器」是最被低估的 AI 工具連接策略**：大多數 Google Flights MCP 工具（如 Fli、SerpApi）選擇逆向 API 或 headless browser，但這個專案選擇操控**真實瀏覽器 session**。好處是：帶著使用者的 cookies/語言/幣別設定、結果與人工操作一致、不觸發 headless 偵測。這個 tradeoff 在「查機票」這種高價值低頻率場景特別合理。

2. **「Browser-Bound MCP」是一個可複製的架構模式**：`Rust Bridge (SSE/MCP) ↔ WebSocket ↔ Chrome Extension ↔ DOM` 這個四層架構是通用的。只要替換 content script，就能讓 AI Agent 操作任何網站——銀行、政府網站、需要登入的服務。這比 Playwright/Puppeteer 更適合需要「帶身份操作」的場景。

3. **AI Agent 的「價差發現」能力**：最有價值的 demo 不是查機票本身，而是 Agent 自己發現 round-trip vs. one-way 的價差（省 NT$13,690）。人類查機票通常只查一種方式，但 Agent 能平行查多種組合、自動比較。這暗示 **AI Agent 在消費者決策場景的真正價值不是自動化，是發現人類看不到的選項**。

4. **Tailscale 作為 Agent 網路層的巧妙用法**：用 Tailscale 讓遠端 Agent（在任何裝置上）透過 VPN 存取本機的 MCP server，解決了「瀏覽器必須在本機」和「Agent 可能在遠端」的矛盾。這個模式值得在其他 browser-bound 工具中複製。

5. **ITA Matrix + Google Flights 雙引擎策略**：截圖揭示了旅遊高手的進階策略——ITA Matrix 當 discovery（理論最低價、hidden city combo、open jaw），Google Flights 當 validation（可訂性確認）。如果把這個 MCP 工具擴展到也支援 ITA Matrix 爬取，就能實現完整的自動化機票搜尋漏斗。

### 與其他專案的關聯

- **MCPorter**（`docs/mcporter.md`）：MCPorter 管理 MCP server 的 discovery 和呼叫，Browser-Bound MCP 則是一種特化的 MCP server 實現。兩者可以組合——用 MCPorter 管理多個 browser-bound tool
- **Lightpanda Browser**（`docs/lightpanda-browser.md`）：Lightpanda 是為 AI Agent 設計的 headless browser（快 11x、省 9x 記憶體）。但 Browser-Bound MCP 走的是相反路線——不用 headless，而是操控真實瀏覽器。兩者的取捨在於：headless 適合大規模 stateless 爬取，real browser 適合需要登入/cookies 的高價值場景
- **Page Agent**（`docs/page-agent.md`）：阿里巴巴的 GUI Agent 用視覺理解操控網頁，Browser-Bound MCP 用 DOM selector 操控。視覺方式更通用但更慢，DOM 方式更快但需要為每個網站寫 content script
