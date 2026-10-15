---
date: "2026-10-15"
category: "學習資源"
card_icon: "material-chart-bell-curve"
oneliner: "前私募 QR 寫的簡中 Quant Research 面試筆記：55 題八股文全附答案，加上項目復盤 8 問、策略方向論文清單和工具書單；內容紮實，但有幾處文獻張冠李戴、一個資訊洩漏例子寫錯"
tags:
  - learning
  - quant
  - finance
---

# Awesome Quant Interview 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/SoYuCry/awesome-quant-interview> |
| 維護者 | YuCry([@0xYuCry](https://x.com/0xYuCry))，自述社招面過 30+ 家量化私募、拿到數家百億級私募 QR offer、做過實盤產品創業 |
| 分析 commit | `6aaeaa9`(2026-08-25) |

> Metadata(2026-10-15 抓取):**786 stars / 94 forks** · MIT · 建立於 2026-03-27，共 23 個 commit，全部同一個作者。整個 repo 就一份 1,776 行的 `README.md`、一張 logo、一份 LICENSE。內文標示 "Last reviewed: 2026-06"。

## 專案概述

一份簡體中文的 **Quant Research(QR)** 面試準備筆記，主場是**中國量化私募**。作者明講範圍只做 QR(因子研究、資產定價、時間序列、ML、回測、組合優化、論文閱讀)，QD(開發)和 Trader 只當延伸背景。

README 全部用 `<details>` 摺疊，分成兩大塊：

1. **前半是「怎麼準備」**：國內面試現況、A/B/C/D 四種起點的讀法路線、數理速查索引、項目復盤 8 問
2. **後半是資源和題庫**：開源工具、按策略方向分的論文清單、研究前沿、書單/社群/A 股資料源，最後是 55 題八股文

跟上一份看的 [AI 工程面試題庫](ai-engineering-interview-questions-company-wise.md) 很不一樣：那份按公司分、四成附答案、答案導流回自家部落格；這份**不分公司**、**55 題全部附完整答案**直接寫在 README 裡，沒有導流。作者也在免責聲明寫了「不含公司原題」，所以「真實追問」都是抽象化過的。

## 內容結構

### 1. 55 題八股文的分布

| 區塊 | 題號 | 題數 | 重點 |
|------|------|------|------|
| 機率論 | Q1–Q4 | 4 | 貝氏、LLN vs CLT、鞅、常見分布 |
| 數理統計 | Q5–Q7 | 3 | MLE vs GMM、p 值誤解、協方差矩陣估計 |
| 線性代數 | Q8–Q9 | 2 | EVD/SVD、半正定 |
| 時間序列 | Q10–Q12 | 3 | 平穩性、ARIMA/GARCH、協整 |
| 隨機微積分 | Q13–Q14 | 2 | 布朗運動、Itô、GBM |
| Python | Q15–Q21 | 7 | 資料結構、深淺拷貝、Pandas 效能、GIL、SettingWithCopy、裝飾器、生成器 |
| C++(標為延伸) | Q22–Q26 | 5 | 指標/參考、虛函數、move、STL、模板 |
| NumPy | Q27–Q28 | 2 | 廣播、滾動視窗 |
| 因子投資 | Q29–Q34 | 6 | Alpha/Beta、FF 三/五因子、量價因子、IC/IR、共線性、因子擁擠 |
| 組合優化 | Q35–Q36 | 2 | MVO、風險平價 |
| 回測評估 | Q37–Q40 | 4 | 回測偏差、評估指標、過擬合、衝擊成本 |
| ML 基礎 | Q41–Q45 | 5 | 偏差-方差、正則化、時序 CV、GBDT、特徵工程 |
| 深度學習 | Q46–Q49 | 4 | RNN/LSTM/Transformer、AE/VAE、GAN、GNN |
| 強化學習 | Q50 | 1 | RL 應用與挑戰 |
| 實戰 | Q51–Q55 | 5 | 標籤不平衡、資訊洩漏、Attention 選股、集成、LLM |

每題固定格式：**標準答案 → 直覺 → 量化應用/陷阱**，常配 LaTeX 公式、表格或一小段 Python/C++。偏「能在 2 分鐘講完」的口徑，深度大概是教科書章節摘要。

### 2. 項目復盤 8 問(整份最有價值的部分)

作者認為面試的鑑別度集中在項目追問，所以給了一份自查清單：Alpha 假設 → 預測目標 → 資料口徑 → 驗證方式 → 評價指標 → 失敗案例 → 實盤落差 → 下一步改進。

再加一張「追問層次」表，把面試官的意圖拆成五層：

| 層次 | 面試官想確認 |
|------|-------------|
| 概念層 | 定義、假設、適用條件 |
| 驗證層 | 知不知道金融資料的坑(前視、洩漏、交易成本) |
| 項目層 | 有沒有真的跑過研究閉環 |
| 生產層 | 懂不懂回測和實盤之間的距離 |
| 反思層 | 有沒有研究判斷力 |

這張表其實不只適用量化面試，任何「做過模型」的面試都可以拿來套。

### 3. 策略方向與論文

按 9 個方向列奠基論文：CTA、中低頻趨勢、截面選股、基本面量化、統計套利、市場中性、高頻(延伸)、做市(延伸)、期權與波動率。每個方向開頭有一段白話介紹，例如市場中性那段直接提到 2024 年 2 月國內量化踩踏。🌟 標記「繞不開的經典」。

研究前沿另外分四塊：時序預測、ML 與資產定價(Gu-Kelly-Xiu 2020 為核心)、深度學習量價、因子工廠(101 Alphas、多重檢定)。

### 4. 資源清單

工具(Backtrader、NautilusTrader、vnpy、Qlib、RD-Agent、FinRL…)、書單(綠皮書、Shreve、de Prado、Grinold & Kahn、石川《因子投資》)、公眾號、A 股資料源(Tushare、AKShare、BaoStock、Wind)、券商金工研報團隊、刷題站(QuantGuide、QuantVault、Brainstellar、Jane Street Puzzles)、競賽。偏中國市場，台灣讀者用得到的主要是書單和英文刷題站。

## 抽查發現的問題

我把 55 題和論文清單抽查了一遍，大方向都對，但有幾個值得注意的錯：

| 位置 | README 寫的 | 實際上 |
|------|------------|--------|
| Q6 多重檢定修正 | 「Bailey-López de Prado-Marcos 的 Haircut 校正」 | Haircut Sharpe 是 **Harvey & Liu(2015)** 提的；Bailey & López de Prado 的是 Deflated Sharpe Ratio(Q39 有寫對) |
| Q38 t 統計量門檻 | 「Bailey-López de Prado 建議 t > 3」 | t > 3 出自 **Harvey, Liu & Zhu(2016)**《…and the Cross-Section》，README 自己的論文清單也有列這篇 |
| Q40 衝擊成本 | 把 $\sigma \gamma (V/ADV)^\delta$ 稱為 Almgren-Chriss 模型 | Almgren-Chriss(2000)原始模型是線性的暫時/永久衝擊，冪次形式比較接近 Almgren et al.(2005)的實證估計 |
| Q52 標籤洩漏例子 | 「用 t-20~t 的均值預測 t~t+5，但 t-20~t 已包含部分 t+5 的資訊」 | 這個例子本身沒有洩漏。真正的問題是**相鄰樣本的標籤視窗重疊**(t 和 t+1 的 5 日報酬共用 4 天)，在 CV 切分時會漏過去 |
| Q43 Embargo | 「Embargo 至少設為標籤前瞻窗口」 | 這比較像 **purging** 的職責；de Prado 的 embargo 是在測試集**之後**再丟一段，處理序列相關。兩者被混在一起講 |
| Q35 風險平價 | 寫成 $w_i \propto 1/\sigma_i$ | 那是 inverse-volatility，只有在資產兩兩相關係數相同時才等於風險平價。Q36 的定義才是對的 |
| 論文清單 | Zhang, Zohren & Roberts(2020)標 JFE | 刊在 *Journal of Financial Data Science* |
| 論文清單 | Xu et al.(2021)Stock Movement Prediction…, ACL | 是 **Xu & Cohen(2018)**, ACL |

其他小地方：Moskowitz et al. *Time Series Momentum* 和 Baz et al. 在兩個區塊重複出現；C++ 五題放在「QR 主線」的八股文裡，跟作者自己說的範圍有點衝突。

這些錯誤在面試時可能剛好會被追問(尤其 Q6、Q38 引用出處)，拿來背的話建議對照原論文。

## 跟這個 memo 其他筆記的關係

- 想實作 README 提到的工具：[GS Quant](gs-quant.md)、[CZSC](czsc.md)、[Vibe-Trading](vibe-trading.md)、[TradingAgents](tradingagents.md)
- 組合優化題(Q35–Q36)想往下挖：memo 裡一系列 Kelly / log-optimal 論文筆記，例如 [Markowitz Inefficiency Drawdown](markowitz-inefficiency-drawdown.md)、[Accelerating Robust Portfolio](accelerating-robust-portfolio-optimization.md)
- 同類型面試題庫：[AI 工程面試題庫(按公司分)](ai-engineering-interview-questions-company-wise.md)

## 總結

**適合誰**：準備中國量化私募 QR 面試、或想用一份文件把「量化研究需要懂什麼」攤開看的人。項目復盤 8 問和追問層次表是最有用的部分，題庫本身是不錯的速查表。

**不適合誰**：要準備海外 quant(Jane Street、Citadel 那種偏機率腦筋急轉彎)的人，這份幾乎沒有 brainteaser，要回去刷綠皮書和 QuantGuide。想要深度的人也會覺得每題都只講到教科書摘要的程度。

**可信度**：答案整體正確，但文獻出處有好幾處張冠李戴，引用論文時要自己查證。作者的「30+ 家私募」經歷沒辦法驗證，「真實追問」也都抽象化過，看不出是哪家問的。
