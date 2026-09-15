---
date: "2026-09-15"
category: "資源彙整 / Awesome List"
card_icon: "material-database-search"
oneliner: "AKShare 作者維護的金融資料源清單——把中國與國際的開源資料工具、官方 SDK、公開資料源與商業資料庫分四類列出。697★ 但 2025-03 後就沒更新，內容偏中國市場。價值在於它是 AKShare 生態的「資料源地圖」，不在於清單本身的完整度"
tags:
  - quant
  - knowledge-base
---

# awesome-data 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★697 / 81 forks / MIT） | <https://github.com/akfamily/awesome-data> |
| 維護者 | **akfamily** — 也就是 [AKShare](https://github.com/akfamily/akshare) 的作者群 |

> **Metadata（2026-09-15 抓取）**：**697 stars / 81 forks / 8 open issues** · **MIT** · 建立於 **2020-03-02**、最後 push **2025-03-27**（**已一年半沒更新**）· repo size 僅 48 KB（就是一份 README）· topics：`data` / `data-science`。

## 這是什麼

一份**單頁的金融資料源清單**，分四類：

| 類別 | 收錄內容 |
|------|---------|
| **Open Data Tools** | AKShare、Tushare、yfinance、pandas-datareader、wbdata、Quandl、investpy、Financial Data |
| **Financial Data SDK** | WindPy（Wind）、JQData（聚寬）、RQData（米筐）、TQSDK（天勤，**期貨 tick 與分鐘資料免費**） |
| **Public Data Source** | Investing.com、新浪財經、東方財富、中國指數研究院（房價）、World Bank Open Data、中國商務數據中心、**FRED（美國聯準會）** |
| **商業資料源** | CSMAR、CNRDS、RESSET、蘿蔔投研（通聯）、恆有數（恆生電子）、BankScope（BvD + 惠譽）、ChinaScope、CnOpenData、預測者網、米筐資料商城 |

## 老實說：它的價值在哪、不在哪

**不在於清單本身。** 47 個條目、一年半沒更新、每條只有一句英文簡介、沒有標註免費/付費/資料覆蓋範圍/更新頻率/API 限流——以「awesome list」的標準來說，這份做得相當薄。而且 `awesome-` 開頭的 repo 通常會有徽章、貢獻指南、分類索引，這份都沒有，README 第一行就是「想加你喜歡的資料源請開 issue」。

**價值在於它是誰維護的。** akfamily 就是 **AKShare** 的作者群——AKShare 是中文圈最常用的免費財經資料介面庫之一。這份清單等於是**AKShare 生態自己畫的資料源地圖**：他們知道自己的 loader 在跟哪些源打交道、哪些商業資料庫是學術研究的標配。

幾個**單看清單容易漏掉、但實際有用**的條目：

- **TQSDK（天勤）** — 期貨 tick 與分鐘資料免費，中國期貨研究少見的免費高頻來源
- **FRED（St. Louis Fed）** — 美國總經資料的權威免費源，做宏觀因子一定會用到
- **CSMAR / CNRDS / RESSET** — 中國財金學術論文的三大標配資料庫，看中文量化論文時知道這三個名字很有幫助
- **CnOpenData** — 專門收另類／小眾資料，找不到的資料可以去翻

## 目前限制

- **2025-03 後未更新**。這一年半裡資料源的 API、定價、可用性都變了不少，清單只能當起點不能當現況。
- **重中國市場**。四類裡三類以中國資料源為主，做台股／美股的參考價值有限。
- **沒有標註任何篩選維度**：免費/付費、是否需要實名、資料覆蓋起訖、更新頻率、限流政策全都沒有。實際要選資料源還是得自己一個一個試。
- **8 個 open issue 沒處理**，其中應該包含社群提交的新資料源。

## 研究價值與啟示

### 關鍵洞察

1. **「誰維護」比「清單多完整」更決定一份 awesome list 的價值。** 這份只有 47 條、一年半沒更新，但因為出自 AKShare 作者之手，它反映的是**一個真的在處理這些資料源的團隊的視野**。相對地，很多上千條目的 awesome list 是爬蟲堆出來的，看起來完整但沒有判斷力。

2. **一份 awesome list 缺什麼欄位，往往就是它沒被真正使用的證據。** 資料源清單最該標的是**免費/付費、覆蓋範圍、更新頻率、限流**——這四欄任一缺席，使用者就還是得自己試一輪。**清單的實用性不在條目數，在於它幫你省掉多少次試錯。** 這一點對本站自己的資源彙整筆記也適用。

3. **對照本站的 [Vibe-Trading](vibe-trading.md) 更有意思**：那個專案的 27 個 loader 是把這類清單「做進程式碼」的結果，而且每一個都標註了 auth 需求、市場覆蓋與 IP 封鎖風險排序。**從清單到可執行的 fallback chain，中間那段工作才是真的難的部分。**

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [AKShare](https://github.com/akfamily/akshare) | 同一團隊的主力專案；這份清單是它的生態地圖 |
| [Vibe-Trading](vibe-trading.md) | 把同類資料源做成 27 個帶 fallback chain 的 loader——**清單的「已實作版」** |
| [CZSC](czsc.md) | 其 connector 接的正是 Tushare、天勤這類清單上的源 |
| [awesome-agentic-ai-zh](awesome-agentic-ai-zh.md) | 同為中文圈 awesome list；那份有 GitHub Action 自動檢查 star/license/封存狀態，**是這份可以對標的策展自動化範本** |
