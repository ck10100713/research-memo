---
date: "2026-06-05"
category: "學習資源"
card_icon: "material-sitemap"
oneliner: "GitHub 35 萬星的系統設計入門聖經：可擴展系統原理 + 面試題解 + Anki 卡片"
tags:
  - learning
  - software-engineering
  - system-design
---

# The System Design Primer 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/donnemartin/system-design-primer> |
| 作者 | Donne Martin（前 Facebook 工程師） |
| 姊妹專案（Coding 面試） | <https://github.com/donnemartin/interactive-coding-challenges> |
| 與其他面試資源比較 | [Grokking vs Alex Xu 比較](https://www.grokkingsystemdesign.com/blog/grokking-the-system-design-interview-vs-alex-xu)、[Pragmatic Engineer 書評](https://blog.pragmaticengineer.com/system-design-interview-an-insiders-guide-review/) |

## 專案概述

The System Design Primer 是 GitHub 上最具代表性的系統設計學習資源（**351k+ stars、56k+ forks**，2017 年創建至今持續維護），目標是「學會設計大規模系統」與「準備系統設計面試」兩件事。它不是一本教科書，而是把散落在網路各處的系統設計資源**有組織地彙整**成一條學習路徑：每個主題都附上優缺點分析（核心信條是 *Everything is a trade-off*）與延伸閱讀連結。

repo 主語言標為 Python，是因為它附有 8 道系統設計面試題的完整解答（含 Python 實作碼、架構圖）以及 6 道 OOD（物件導向設計）題的 Jupyter Notebook 解答。另外提供 3 套 **Anki 字卡牌組**（System Design、System Design Exercises、OO Design），用間隔重複幫助記憶。社群翻譯涵蓋日文、簡中、繁中等 4 種完成語言與 16+ 種進行中語言。

## 內容架構

整個 repo 可分為四大塊：

```
system-design-primer
├── 學習指南（Study Guide）
│   └── 按準備時間（短/中/長）建議的學習廣度與深度
├── 面試方法論（4 步驟框架）
│   ├── Step 1: 釐清 use cases、約束、假設
│   ├── Step 2: 畫出 high-level 設計
│   ├── Step 3: 深入核心元件
│   └── Step 4: 擴展設計（找瓶頸 → 加 LB/cache/sharding）
├── 系統設計主題索引（知識主體，~20 個主題）
│   └── 每個主題：原理 + 優缺點 + 延伸閱讀
└── 題解（solutions/）
    ├── 8 道系統設計題（Pastebin、Twitter timeline、爬蟲、
    │   Mint.com、社交圖譜、KV store、Amazon 銷售排行、AWS 百萬用戶）
    └── 6 道 OOD 題（hash map、LRU cache、call center...）
```

### 知識主題涵蓋範圍

| 層面 | 主題 |
|------|------|
| 基礎觀念 | Performance vs Scalability、Latency vs Throughput、CAP 定理 |
| 一致性/可用性模式 | Weak / Eventual / Strong consistency；Fail-over、Replication、可用性數字（99.9% vs 99.99%） |
| 網路入口 | DNS、CDN（Push vs Pull）、Load Balancer（L4 vs L7、active-passive vs active-active）、Reverse Proxy |
| 應用層 | Microservices、Service Discovery |
| 資料庫 | RDBMS（master-slave、master-master、federation、sharding、denormalization、SQL tuning）、NoSQL 四型（KV / document / wide column / graph）、SQL or NoSQL 抉擇 |
| 快取 | 六個層級（client → CDN → web server → DB → application）+ 四種更新策略（cache-aside、write-through、write-behind、refresh-ahead） |
| 非同步 | Message queues、Task queues、Back pressure |
| 通訊 | TCP vs UDP、RPC vs REST 比較 |
| 附錄 | 2 的冪次表、**Latency numbers every programmer should know**、真實世界架構（公司架構案例 + 工程部落格清單） |

### 面試準備的時間軸建議

| 準備時間 | 策略 |
|----------|------|
| 短 | 廣度優先，做**部分**題目 |
| 中 | 廣度 + 部分深度，做**多數**題目 |
| 長 | 廣度 + 更多深度，做**全部**題目 |

## 快速開始

不需安裝任何東西，建議路徑：

1. 看 [Harvard Scalability Lecture](https://www.youtube.com/watch?v=-W9F__D3oY4)（垂直/水平擴展、快取、LB、複寫、分區）
2. 讀 Scalability for Dummies 系列文章（Clones → Databases → Caches → Asynchronism）
3. 按主題索引逐一閱讀，配 Anki 卡片複習
4. 用 4 步驟框架練習 `solutions/` 內的題目

## 目前限制 / 注意事項

- **OOD 章節標註 under development**，部分題目仍缺解答；repo 創建近十年，部分外部連結已失效（README 中多處已改用 web.archive.org 快照）
- **內容偏「經典」**：聚焦 2010 年代的擴展性問題（LAMP 式架構演進），對 Kubernetes、serverless、stream processing（Kafka/Flink）、向量資料庫等近年主題著墨少
- **深度有限**：每個主題是摘要 + 連結的形式，適合建立框架，不適合取代 DDIA（*Designing Data-Intensive Applications*）這類深度書籍
- 它是**面試導向**的資源；實際工作中的系統設計還需要考慮成本、團隊、漸進遷移等面向，這些不在範圍內

## 研究價值與啟示

### 關鍵洞察

1. **「組織」本身就是價值**：這個 repo 沒有多少原創內容，它做的是把散落的演講、文章、論文組織成學習路徑——351k stars 證明在資訊過載時代，curation + 結構化是獨立的價值來源。這與本站（research-memo）做的事本質相同。
2. **Everything is a trade-off 是貫穿全書的方法論**：每個主題都用「優點/缺點」對照呈現（如 CP vs AP、cache-aside vs write-through），訓練的是決策思維而非背誦。這個格式值得本站筆記借鏡——「目前限制」段落正是同樣精神。
3. **4 步驟面試框架其實是通用設計流程**：釐清需求 → high-level 設計 → 深入元件 → 找瓶頸擴展。把它套在 AI Agent 系統設計上同樣成立（例如設計 multi-agent pipeline 時先估 token 流量與延遲預算）。
4. **back-of-the-envelope 估算被低估**：附錄的 latency 數字表（L1 cache 0.5ns → 跨洋 RTT 150ms，數量級差 10^8）是做容量規劃的基本功；對 LLM 應用同樣適用（token 生成速度、context window 成本估算）。
5. **定位是「免費的廣度起點」**：與付費資源相比（Grokking 是結構化課程、Alex Xu 是深度參考書），Primer 適合當第一站建立全景圖，再用其他資源補深度。

### 與其他專案的關聯

- [Laws of Software Engineering](laws-of-software-engineering.md)：同屬「軟體工程經典知識」彙整，Primer 提供架構面、Laws 提供原則面，互補
- [HighScalability](highscalability.md)：Primer 附錄大量引用 highscalability.com 的真實架構案例（back-of-the-envelope 估算一文即出自該站），兩者是「教材 vs 案例庫」的關係
- [AI Agents for Beginners (Microsoft)](ai-agents-for-beginners.md)：同為「有組織的免費學習路徑」模式，一個教分散式系統、一個教 Agent 系統
