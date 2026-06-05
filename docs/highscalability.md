---
date: "2026-06-05"
category: "軟體工程知識"
card_icon: "material-server-network"
oneliner: "經營 17 年的大規模系統架構案例庫，2024 年由 ByteByteGo 收購接手"
tags:
  - system-design
  - software-engineering
  - knowledge-base
---

# HighScalability.com 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 網站 | <https://highscalability.com/> |
| 創辦人 Todd Hoff 作者頁 | <https://highscalability.com/author/toddhoff/> |
| ByteByteGo 收購公告（2024-03-15） | <https://x.com/alexxubyte/status/1768664948815904909> |
| 代表作：WhatsApp 架構（$19B 收購背後） | <https://highscalability.com/the-whatsapp-architecture-facebook-bought-for-19-billion/> |
| 代表作：WhatsApp 5 億用戶擴展史 | <https://highscalability.com/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an/> |

## 網站概述

HighScalability（標語：*Building bigger, faster, more reliable websites*）是分散式系統領域最具歷史地位的部落格之一，由分散式系統工程師 **Todd Hoff** 於 2007 年創辦並獨立經營 **17 年**，2024 年 3 月被 Alex Xu 的 **ByteByteGo**（《System Design Interview》作者、知名系統設計電子報）收購，目前以 Ghost 平台運行，持續發布真實世界系統架構文章。

它的核心價值在於「**真實案例**」：在工程部落格尚不普及的年代，它系統性地整理了各大公司如何擴展系統的第一手資料——Google、Amazon、Netflix、Uber、WhatsApp、Stack Overflow 等架構演進都有專文拆解。對一整個世代的工程師來說，它是系統設計的「案例教科書」。

## 內容類型與代表性系列

| 系列 / 類型 | 說明 |
|------------|------|
| **Real Life Architectures** | 招牌系列：拆解真實公司的架構（如 WhatsApp 用 Erlang/FreeBSD 做到單機 200 萬連線、32 名工程師支撐每日 500 億訊息） |
| **Stuff the Internet Says on Scalability** | 長年連載的週報式 link roundup，彙整當週擴展性相關文章與金句 |
| **概念解釋文** | 如 Gossip Protocol、Consistent Hashing、Kafka 101（收購後 ByteByteGo 風格的圖解文） |
| **事故 / 教訓分析** | 如 Swedbank 大當機與 change control 的反思、Meta 規模運行 Presto 的教訓 |
| **方法論經典** | 〈Google Pro Tip: Use Back-of-the-Envelope Calculations〉等，被 System Design Primer 等教材大量引用 |

### 收購前後的轉變

```
2007 ──────────────────────── 2024-03 ─────────────→
 Todd Hoff 時代                ByteByteGo 時代
 ├ 高頻更新、社群投稿           ├ 更新頻率較低（數週~數月一篇）
 ├ 長文深挖 + 週報彙整          ├ 圖解風格（ByteByteGo 式插圖)
 └ 原創案例訪談                └ 與付費電子報/課程生態整合
```

## 使用方式

- 無需註冊，全站文章免費閱讀；按 tag / 作者瀏覽歸檔
- 準備系統設計面試時，搭配教材使用：先學原理，再到這裡讀對應的真實案例（例如學完 sharding 後讀 Uber/Pinterest 的擴展史）
- 經典舊文（2010 年代）部分連結與圖片已失效，必要時配合 web.archive.org

## 目前限制 / 注意事項

- **更新頻率明顯下降**：收購後從高頻更新變為數週至數月一篇，新內容多與 ByteByteGo 電子報重疊
- **舊文時效性**：大量經典案例描述的是 2008–2016 年的技術選型（如 memcached、MySQL sharding），閱讀時要區分「不變的原則」與「過時的選型」
- **商業化脈絡**：現屬 ByteByteGo 內容生態的一環，文章導流至其付費課程，選題偏向面試導向

## 研究價值與啟示

### 關鍵洞察

1. **案例庫與教材是兩種互補的知識形態**：教材（如 System Design Primer）給框架，HighScalability 給「框架在真實世界長什麼樣」。WhatsApp 用 Erlang 單機扛 200 萬連線的故事，比任何 load balancer 章節都更能說明「先垂直優化、再水平擴展」的取捨。
2. **獨立部落格的退場模式**：17 年的個人經營最終以「被內容品牌收購」收尾——這是優質長尾內容資產化的典型案例，也說明 curation 型內容的價值可以被收購方量化（ByteByteGo 買的是 SEO 資產與品牌信任）。
3. **「小團隊 × 對的技術」的反規模敘事**：WhatsApp（32 工程師 / 4.5 億 DAU）、Stack Overflow（少量伺服器扛全站）這類案例是對「微服務 + 大團隊」主流敘事的重要平衡，提醒架構決策應從負載特性出發而非從流行趨勢出發。
4. **內容更新頻率是社群健康度的領先指標**：收購後更新放緩、原創案例減少，顯示這類站點的價值高度依賴主理人的人脈與訪談能力，品牌可轉移、network 難轉移。

### 與其他專案的關聯

- [System Design Primer](system-design-primer.md)：Primer 的附錄（real world architectures、back-of-the-envelope）大量引用本站文章，兩者是「教材 vs 案例庫」關係，建議搭配閱讀
- [Laws of Software Engineering](laws-of-software-engineering.md)：本站案例可作為各定律（如 Conway's Law、Gall's Law）的實證素材
