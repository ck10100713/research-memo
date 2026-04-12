---
date: "2026-03-29"
category: "量化交易"
card_icon: "material-chart-scatter-plot"
oneliner: "2.92 億筆 Polymarket/Kalshi 交易的公開最大數據集，附學術研究框架與「財富轉移微結構」論文"
---
# Prediction Market Analysis 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [Jon-Becker/prediction-market-analysis](https://github.com/Jon-Becker/prediction-market-analysis) |
| 研究論文 1 | [The Microstructure of Wealth Transfer in Prediction Markets](https://jbecker.dev/research/prediction-market-microstructure) |
| 研究論文 2 | [Decomposing Crowd Wisdom (arXiv:2602.19520)](https://arxiv.org/abs/2602.19520) |
| HackerNews 討論 | [HN #46680515](https://news.ycombinator.com/item?id=46680515) |
| Polymarket vs Kalshi 深度分析 | [tradetheoutcome.com](https://www.tradetheoutcome.com/polymarket-vs-kalshi-liquidity-volume-deep-dive-2026/) |
| Kalshi $22B 估值報導 | [Fortune](https://fortune.com/2026/03/20/kalshi-locks-in-22-billion-valuation-gaining-slight-edge-over-its-rival-polymarket/) |
| 數據集下載 | [Cloudflare R2 — data.tar.zst (36GiB)](https://s3.jbecker.dev/data.tar.zst) |

## 專案概述

**Prediction Market Analysis** 是 Jon Becker 建立的學術研究框架與數據集，提供目前**公開最大規模**的 Polymarket 和 Kalshi 交易數據。核心資產是一份 36GiB 壓縮、包含 **2.92 億筆交易**、涵蓋 327,000 個二元合約的 Parquet 格式資料集。

這個專案的定位是研究基礎設施：既有預先收集好的歷史數據可直接下載，也提供 indexer 框架讓研究者自行從 Polymarket API、Polymarket 鏈上數據（Polygon）和 Kalshi API 持續收集新數據。分析框架以可擴展的 script 架構輸出 PNG/PDF/CSV/JSON 格式的研究圖表。

截至 2026-03-29，擁有 **2,360 stars、317 forks**，已被至少兩篇學術論文引用，並催生了多個衍生研究和套利機器人專案。

## 核心功能 / 技術架構

### 專案結構

```
src/
├── analysis/
│   ├── kalshi/         # Kalshi 專項分析腳本
│   ├── polymarket/     # Polymarket 專項分析腳本
│   └── comparison/     # 跨平台比較分析
├── indexers/
│   ├── kalshi/         # Kalshi API 爬取器
│   └── polymarket/     # Polymarket API + 鏈上爬取器
└── common/             # 共用介面與工具

data/
├── kalshi/
│   ├── markets/        # 市場 metadata (Parquet)
│   └── trades/         # 交易記錄 (Parquet)
└── polymarket/
    ├── blocks/         # 鏈上區塊資料
    ├── markets/
    └── trades/
```

### 兩個平台的數據來源

| 平台 | 數據來源 | 特性 |
|------|---------|------|
| **Kalshi** | REST API | CFTC 合規；運動賽事主導（90%）；中心化 |
| **Polymarket** | REST API + Polygon 鏈上數據 | 去中心化（USDC）；政治/地緣政治主導；鏈上可查 |

### 數據規模

| 指標 | 數值 |
|------|------|
| 壓縮後大小 | 36 GiB（zstd 壓縮） |
| 總交易筆數 | 2.92 億筆 |
| 涵蓋合約數 | 327,000 個二元合約 |
| Kalshi 交易量 | $18.26B（72.1M 筆） |

## 快速開始

```bash
# 安裝（Python 3.9+，需要 uv）
uv sync

# 下載預收集數據集（36GiB 壓縮）
make setup

# 自行收集新數據（互動式選單）
make index

# 執行分析（互動式選單，輸出至 output/）
make analyze

# 重新打包壓縮
make package
```

## 目前限制 / 注意事項

| 限制 | 說明 |
|------|------|
| 數據量巨大 | 36GiB 壓縮，解壓後更大，需要足夠儲存空間 |
| Polymarket 鏈上爬取 | 須存取 Polygon RPC，有額度限制 |
| 靜態快照 | 預收集數據有截止時間，最新數據需自行 index |
| 分析框架偏學術 | 較適合研究用途，非即時交易信號 |

## 研究價值與啟示

### 關鍵洞察

**1. 「樂觀稅」（Optimism Tax）——市場系統性偏誤的量化證據**
Becker 的論文分析 7,210 萬筆 Kalshi 交易，發現流動性接受者（takers）對「YES」結果有系統性偏好，尤其在冷門合約（longshots）上，某些合約每下注 1 美元只能回收 43 美分。這不是個別行為偏差，而是規模化的系統性財富轉移——從散戶接受者流向專業做市商。這種「人類天生對好結果抱持過度樂觀」的心理，在 AI Agent 也可能出現類似偏差（對問題的答案傾向正向確認），值得注意。

**2. 做市商的優勢不來自更準的預測，而來自流量捕獲**
論文發現做市商在 YES/NO 的預測準確度差異僅 +0.77% 到 +1.25%——幾乎沒有「資訊優勢」。他們的獲利來自**捕獲 taker 流量的價差**，以及 taker 在不利價格下仍然積極進場的行為。這對量化策略設計有直接啟示：在有做市商主導的市場裡，作為 taker 長期而言注定不利。

**3. 政治市場的「校準壓縮」現象**
《Decomposing Crowd Wisdom》論文發現政治類合約存在持續的**低信心偏誤（underconfidence）**：市場價格長期被壓縮在 50% 附近，無論在 Kalshi 還是 Polymarket 都如此。換言之，「群眾智慧」在政治議題上普遍過於保守，極端結果（20% 以下或 80% 以上）被低估。這對自動化交易策略有套利空間的暗示，但也反映了真實世界事件的不確定性。

**4. 平台差異透露市場結構不同**
大額交易對校準的影響在 Kalshi 可複製、在 Polymarket 卻無法複製——兩個平台雖然交易同類商品，卻有截然不同的流動性結構和參與者組成。Kalshi 更機構化，Polymarket 更散戶化。這意味著「把一個平台的策略直接移植到另一個平台」風險很高。

**5. 公開數據集本身就是護城河**
這個 repo 最值錢的不是 Python 框架，而是那 36GiB 的歷史數據。學術論文引用它、套利機器人用它校準、研究者用它驗證假設——公開數據集吸引更多研究者，更多研究者帶來更多引用，更多引用又吸引更多數據貢獻者。這是「數據飛輪」效應的典型案例，適合借鑑到任何需要社群數據貢獻的 AI 服務設計。

### 與其他專案的關聯

- **AI Hedge Fund**（本站已有筆記）：ai-hedge-fund 使用 LLM 模擬傳奇投資人「感覺上如何決策」，而這個數據集提供的是**真實市場微結構的量化分析**——兩者的方法論差距極大
- **TradingAgents**（本站已有筆記）：TradingAgents 聚焦股票市場的 Agent 決策框架，本專案則是預測市場的學術數據基礎設施，可視為互補的研究工具
- **NOFX**（本站已有筆記）：NOFX 實際執行加密貨幣交易，本專案的 Polymarket 鏈上數據（USDC on Polygon）可作為 NOFX 策略研究的數據來源

### 市場背景（2026 年初）

| 指標 | Kalshi | Polymarket |
|------|--------|-----------|
| 2026-02 月交易量 | $9.8B | $7.0B |
| 2025 全年交易量 | $43.1B | $33.4B |
| 監管狀態 | CFTC 合規 | 鏈上（Polygon） |
| 主力品類 | 運動賽事（90%） | 政治、地緣政治、加密 |
| 最新估值 | ~$22B | ~$20B |
