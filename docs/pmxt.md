---
date: "2026-03-29"
category: "量化交易"
icon: "material-swap-horizontal-bold"
oneliner: "預測市場的 CCXT — 統一 API 連接 7 個交易所（Polymarket/Kalshi 等），Sidecar + OpenAPI 雙語言 SDK"
---
# pmxt 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [pmxt-dev/pmxt](https://github.com/pmxt-dev/pmxt) |
| 官網 | [pmxt.dev](https://pmxt.dev) |
| 歷史資料庫 | [archive.pmxt.dev](https://archive.pmxt.dev) |
| 作者 DEV.to 介紹文 | [CCXT for Prediction Markets: Introducing PMXT](https://dev.to/realfishsam/ccxt-for-prediction-markets-introducing-pmxt-130e) |
| 跨平台套利 Bot 教學 | [How I Built a "Risk-Free" Arbitrage Bot](https://dev.to/realfishsam/how-i-built-a-risk-free-arbitrage-bot-for-polymarket-kalshi-4f) |
| Show HN | [HN #46575615](https://news.ycombinator.com/item?id=46575615) |
| NPM (core) | `pmxt-core` |
| PyPI | `pmxt` |
| Zenodo DOI | 每個 release 自動發布，可學術引用 |

## 專案概述

**pmxt** 自稱為「The CCXT for Prediction Markets」—— 一個統一 API 函式庫，讓開發者透過單一介面同時存取多個預測市場交易所的資料與交易功能。正如 [CCXT](https://github.com/ccxt/ccxt) 標準化了加密貨幣交易所 API，pmxt 對預測市場做了同樣的事。

核心作者是 **Samuel EF. Tinnerholm**（`realfishsam`），新加坡國立大學（NUS）與瑞典烏普薩拉大學（Uppsala）的量化開發者。本質上是單人主力專案（439/533 commits），有約 12 名社群貢獻者。

截至 2026-03-29，擁有 **1,205 stars、123 forks**。從 2026-01-08 建立至今僅 2.5 個月，已從 v0.x 發展到 v2.22.1，幾乎每天更新，開發速度極快。

## 核心功能

### 支援的交易所（7 個）

| 交易所 | 類型 | 備註 |
|--------|------|------|
| **Polymarket** | 鏈上 CLOB（Polygon/EVM） | 最完整整合，3 個 API spec |
| **Kalshi** | 美國受監管 CFTC，傳統 REST | 最乾淨的參考實作 |
| **Limitless** | EIP-712 簽名 | |
| **Probable** | | |
| **Baozi** | Solana pari-mutuel | |
| **Myriad** | | |
| **Opinion** | 最新加入（2026-03-21） | |

另有 `kalshi-demo` 用於測試環境。

### Compliance Matrix（功能覆蓋）

| 類別 | 功能 | 覆蓋率 |
|------|------|--------|
| **市場資料** | `fetchMarkets`, `fetchEvents`, `fetchMarket`, `fetchEvent` | 7/7 |
| **公開資料** | `fetchOHLCV`, `fetchOrderBook` | 7/7 |
| | `fetchTrades` | 6/7 |
| **私有資料** | `fetchBalance`, `fetchPositions`, `fetchMyTrades` | 6-7/7 |
| **交易** | `createOrder`, `cancelOrder`, `fetchOrder`, `fetchOpenOrders` | 6-7/7 |
| **計算** | `getExecutionPrice`, `getExecutionPriceDetailed` | 7/7 |
| **即時** | `watchOrderBook`（WebSocket） | 7/7 |
| | `watchTrades` | 5/7 |

其他特色：
- **`buildOrder` / `submitOrder`**：兩步驟訂單工作流，允許建立但不送出（用於 Smart Order Router）
- **`watchAddress` / `unwatchAddress`**：鏈上地址活動監控（GoldSky GraphQL 訂閱）
- **`filterMarkets`**：客戶端市場篩選
- **Raw Mode**：保留原始交易所格式不轉換
- **14 種 Typed Error Classes**：Python/TypeScript 共用

## 技術架構

### Sidecar Pattern（最關鍵的設計決定）

```
Python SDK  ──┐
              ├──  HTTP  ──►  Sidecar Server (Node.js/Express v5)  ──►  Exchange APIs
TypeScript SDK ┘
```

- 交易所整合只在 TypeScript `core/` 實作一次
- SDK 是「瘦 HTTP 包裝器」，自動在背景啟動/管理 sidecar server
- 新增交易所 = 自動在所有 SDK 可用
- Server 使用 `~/.pmxt/server.lock` 管理生命週期與 access token
- **代價**：Python 使用者必須安裝 Node.js >= 18

### OpenAPI 驅動的 SDK 生成

```
BaseExchange.ts (JSDoc)
       │ AST parsing
       ▼
core/src/server/openapi.yaml  ← source of truth
       │ openapi-generator-cli
       ▼
sdks/python/generated/    sdks/typescript/generated/
```

CI 有 drift guard 確保 SDK 與 core 同步。

### Implicit API Pattern（二層 API 系統）

1. **Unified API** — 公開介面（`fetchMarkets`, `createOrder` 等），跨交易所統一
2. **Implicit API** — 從交易所自身 OpenAPI spec 自動生成的方法，為每個 `operationId` 建立可呼叫方法

統一方法內部透過 `callApi('OperationId', params)` 調用 implicit 方法。

### 目錄結構

```
core/
  specs/            交易所 OpenAPI YAML specs
  src/
    exchanges/      交易所實作（每個一個目錄）
      polymarket/   (3 個 api: CLOB, data, gamma)
      kalshi/
      limitless/
      probable/
      baozi/
      myriad/
      opinion/
    server/         Express sidecar server
    utils/          共用工具
    BaseExchange.ts 抽象基底類
    types.ts        統一資料型別
    errors.ts       錯誤類別層級
sdks/
  python/           pip install pmxt
  typescript/       npm install pmxtjs
tools/
  dome-to-pmxt/     Dome API 遷移工具（npx dome-to-pmxt ./src）
```

### 主要依賴

- `express` v5, `axios`, `cors`, `ethers` v5（Polymarket 簽名）
- `@polymarket/clob-client`, `@limitless-exchange/sdk`, `@prob/clob`
- `@opinion-labs/opinion-clob-sdk`, `@solana/web3.js`（Baozi）
- `ws`（WebSocket）, `esbuild`（bundling）

## 統一資料模型

階層：**Event** > **Market** > **Outcome**

```typescript
interface UnifiedEvent {
    id, title, description, slug,
    markets: UnifiedMarket[],
    volume24h, volume?, url, image?, category?, tags[]
}

interface UnifiedMarket {
    marketId, eventId?, title, description, slug?,
    outcomes: MarketOutcome[],
    resolutionDate, volume24h, volume?, liquidity, openInterest?,
    url, image?, category?, tags[], tickSize?,
    yes?, no?, up?, down?   // 便利 getters
}

interface MarketOutcome {
    outcomeId, marketId?, label, price, priceChange24h?, metadata?
}

interface Order {
    id, marketId, outcomeId, side, type, price?, amount,
    status: 'pending' | 'open' | 'filled' | 'cancelled' | 'rejected',
    filled, remaining, timestamp, fee?
}

interface Position {
    marketId, outcomeId, outcomeLabel, size,
    entryPrice, currentPrice, unrealizedPnL, realizedPnL?
}
```

## 使用範例

### Python — 查詢市場資料

```python
pip install pmxt

import pmxt

api = pmxt.Exchange()
events = api.fetch_events(query='Fed Chair')
market = events[0].markets.match('Kevin Warsh')
print(f"Price: {market.yes.price}")
```

### TypeScript — 查詢市場資料

```typescript
npm install pmxtjs

import pmxt from 'pmxtjs';

const api = new pmxt.Exchange();
const events = await api.fetchEvents({ query: 'Fed Chair' });
const market = events[0].markets.match('Kevin Warsh');
console.log(`Price: ${market.yes?.price}`);
```

### Python — 交易

```python
exchange = pmxt.Polymarket(
    private_key=os.getenv('POLYMARKET_PRIVATE_KEY'),
    proxy_address=os.getenv('POLYMARKET_PROXY_ADDRESS')
)
balance = exchange.fetch_balance()
order = exchange.create_order(
    outcome=markets[0].yes,
    side='buy', type='limit', price=0.33, amount=100
)
```

## 附帶資源

### pmxt Data Archive

- 網址：[archive.pmxt.dev](https://archive.pmxt.dev)
- 免費提供每小時預測市場 orderbook/trade 快照
- 格式：Parquet
- 覆蓋所有支援的交易所

### 跨平台套利 Bot 教學

作者在 DEV.to 示範用 pmxt 建構 Polymarket ↔ Kalshi 跨平台套利機器人：
- 捕獲 1.5%-4.5% 的價差
- 核心邏輯：比較同一事件在兩個平台的 Yes 價格，低買高賣

## 版本演進

| 版本 | 時間 | 重點 |
|------|------|------|
| v0.x | 2026-01 | 初始架構，Polymarket + Kalshi 整合 |
| v1.0 | 2026-01~02 | Sidecar 架構、Python/TS SDK、OpenAPI pipeline |
| v1.5-1.7 | 2026-02 | Hybrid ID、統一過濾、CCXT-style unified API |
| v2.0 | 2026-02 | Breaking changes，移除 deprecated methods |
| v2.17-2.22 | 2026-03 | 7 個交易所、WebSocket、typed errors、address watcher |
| **v3.0（計畫）** | 2027+ | Rust native bindings，零 Node.js 依賴，超低延遲 |

## 與替代方案比較

| 特性 | **pmxt** | **dr-manhattan** | **predmarket** | **Dome API** |
|------|----------|-------------------|----------------|-------------|
| Stars | **1,205** | 180 | ~70 | 商業服務 |
| 語言 | TS core + Python SDK | Python | Python | 商業 |
| 定位 | Library（統一 API） | Framework（Strategy 基底類） | Library | 付費 API |
| 交易所數 | **7** | ~5 | 較少 | 多 |
| SDK | Python + TypeScript | Python only | Python only | REST |
| WebSocket | 支援 | ? | 無 | 有 |
| 文件品質 | 完整 | 較弱 | 無 | 商業級 |
| 最後更新 | 2026-03-25 | 2026-02-25 | 不再維護 | 持續 |
| 授權 | MIT | MIT | — | 商業 |

pmxt 另提供 `npx dome-to-pmxt ./src` 自動遷移工具，定位自己為 Dome API 的開源替代。

## 外部討論

- **Show HN**（2026-01-25）：僅 2 points、2 comments，反響冷淡
  - 有人質疑 battle-tested 程度和速度
  - 作者回覆宣佈 WebSocket 與高測試覆蓋率
- **DEV.to**：作者自寫的兩篇介紹/教學文章
- **Medium**：作者自寫的比較文（pmxt vs dr-manhattan vs predmarket）
- 被列入 [Awesome Prediction Market Tools](https://github.com/aarora4/Awesome-Prediction-Market-Tools)
- Interexy 指南稱 pmxt 為「最有能力的預測市場聚合器」
- **贊助商**：ondb.ai
- **未來計畫**：Smart Order Router（private alpha 開發中）

## 風險與觀察

**優勢**：

- 架構設計成熟 — sidecar + OpenAPI 生成的工程水準很高
- 開發速度驚人 — 2.5 個月從零到 v2.22，7 個交易所
- 雙語言 SDK 降低使用門檻
- MIT 授權、Zenodo DOI 可學術引用
- 免費歷史資料庫（archive.pmxt.dev）

**風險**：

- **Bus factor = 1**：439/533 commits 來自同一人
- **Sidecar 摩擦**：Python 使用者必須安裝 Node.js >= 18，這是非自明的依賴
- **極短歷史**：僅 2.5 個月，生產環境穩定性未知
- **自我推銷為主**：比較文章、blog posts 全是作者自己寫的
- **商業模式不明**：Smart Order Router 似乎是未來付費產品
- **v3 Rust rewrite 遠期**：計畫 2027+ 才能移除 Node.js 依賴

## 與 Prediction Market Analysis 的互補性

本專案與先前研究的 [Prediction Market Analysis](prediction-market-analysis.md)（Jon Becker）形成互補：

| | pmxt | Prediction Market Analysis |
|---|------|---------------------------|
| 定位 | **即時交易 SDK** | **歷史研究數據集** |
| 強項 | 統一下單、即時報價、多交易所 | 2.92 億筆歷史交易、學術論文 |
| 數據格式 | API 回傳 JSON | Parquet 離線分析 |
| 適用場景 | 建造交易機器人、套利系統 | 回測策略、學術研究、市場微結構分析 |

兩者結合可覆蓋「歷史回測 → 即時執行」的完整工作流。
