---
date: "2026-03-29"
category: "量化交易"
card_icon: "material-chart-areaspline"
oneliner: "464 支美股 10-bagger 實證研究：FCF/P 是最強因子、EPS 成長不顯著、動量呈反轉型態（CAFE Working Paper No.33）"
---
# The Alchemy of Multibagger Stocks 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 論文原文 (PDF) | [CAFE Working Paper No.33 — Birmingham City University](https://www.open-access.bcu.ac.uk/16180/1/The%20Alchemy%20of%20Multibagger%20Stocks%20-%20Anna%20Yartseva%20-%20CAFE%20Working%20Paper%2033%20%282025%29.pdf) |
| 作者 | Anna Yartseva, Birmingham City Business School |
| 發表日期 | February 2025 |
| 授權 | Creative Commons Attribution Non-commercial Share Alike |

## 論文概述

**The Alchemy of Multibagger Stocks** 是一篇來自 Birmingham City University CAFE（Centre for Applied Finance and Economics）的工作論文，對美國股市的 **multibagger stocks**（股價至少翻 10 倍的股票）進行了系統性的實證研究。

作者分析 **464 支** 2009-2024 年間在 NYSE/NASDAQ 上市、股價增長至少 10 倍的股票，建立動態面板數據模型（dynamic panel data model），找出驅動這些異常報酬的關鍵因子。研究跨度 25 年（2000-2024），涵蓋牛熊市、升降息、COVID 等多種市場環境。

這篇論文最大的價值在於：它用嚴格的計量經濟學方法**驗證（也推翻）了許多投資界的「常識」**——例如「強勁的 EPS 成長是必要條件」這個被奉為圭臬的觀點，在計量檢驗下並不顯著。

## 核心發現

### 一、Fama-French 因子在 Multibagger 上的表現

傳統 Fama-French 五因子模型的四個因子在 multibagger 上全部有效，但**投資因子的方向相反**：

| 因子 | 效果 | 在 Multibagger 的表現 |
|------|------|---------------------|
| **Size (規模)** | 小型股跑贏 | 小型股（<$250M）年超額報酬 37.7%，大型股 9.7% |
| **Value (價值)** | 高 B/M 跑贏 | 高價值組年超額 34.7%，低價值組 12.8% |
| **Profitability (獲利能力)** | 高獲利跑贏 | 高獲利組 40.9% vs 低獲利組 9.6% |
| **Investment (投資)** | 積極投資跑贏 :warning: | **與 Fama-French 預測相反**：積極擴張資產的公司在 100% 的配對比較中跑贏保守投資的公司 |

**關鍵洞察**：Fama-French 模型的截距項高達 83.9（p=0.000），代表五因子模型**無法完全解釋** multibagger 的報酬，需要額外因子。

### 二、最終模型的顯著因子（7 個模型比較）

作者用 Hendry 的 **general-to-specific** 方法，從 150+ 個變數篩選出最終的簡約模型。七個模型（靜態 FE、動態 IV FE、FD、差分 GMM、系統 GMM 等）的共同顯著因子：

| 因子 | 方向 | 係數範圍 | 解讀 |
|------|------|---------|------|
| **S&P 500 報酬** | + | 0.54 ~ 0.93 | Multibagger 與大盤同向但 beta > 1 |
| **ln(TEV)** | - | -5.3 ~ -49.0 | 公司規模越大，未來報酬越低 |
| **ROA** | + | 0.4 ~ 1.9 | 獲利能力正相關但係數不大 |
| **B/M (帳面市值比)** | + | 7.2 ~ 42.4 | **最重要的因子之一**：價值型 multibagger 更佳 |
| **FCF/P (自由現金流收益率)** | + | 46.4 ~ 51.9 | **最大影響因子**：1% 增幅帶來 7-52% 報酬增加 |
| **Inv dummy** | - | -4.1 ~ -11.0 | 資產成長超過 EBITDA 成長時，報酬降低 4-11 個百分點 |
| **Price range** | - | -0.86 ~ -0.92 | 股價越接近 12 個月高點，未來報酬越低 |
| **6 個月動量** | - | -0.09 ~ -0.81 | 反轉效應：近 6 個月漲越多，下一年報酬越低 |
| **利率環境 dummy** | - | -7.9 ~ -12.1 | Fed 升息期間報酬降低 ~10 個百分點 |
| **滯後報酬 Y(t-1)** | + | 0.12 ~ 0.49 | 存在動態持續性（momentum inertia） |

### 三、顛覆傳統認知的發現

#### EPS 成長**不顯著**
> 盈餘成長——不論是 EPS、營收、毛利、淨利、現金流——無論是年增率或 5 年 CAGR，在動態模型中**全部統計不顯著**。

這直接推翻了 Phelps、Lynch、Mayer 等投資大師「持續的盈餘成長是 multibagger 的必要條件」的說法。

#### P/E 不是好的估值指標
P/E 在迴歸中**不顯著**且會扭曲其他係數。原因：
1. 虧損公司的 P/E 無法解讀
2. 盈餘趨近零時 P/E 趨近無窮

取而代之的是 **B/M** 和 **FCF/P** 作為更好的估值代理變數。

#### 投資因子方向相反
Fama-French 認為保守投資的公司跑贏，但在 multibagger 中：
- 積極投資是**必要的**（100% 配對一致）
- 但投資必須有 EBITDA 支撐——資產增長率 > EBITDA 增長率時，報酬反而下降 4-11%

#### 動量效應是**反轉型**的
- 1 個月動量微弱正向（僅在一個模型顯著）
- 3 個月和 6 個月動量**顯著為負**
- Price range（接近 52 週高點的程度）**顯著為負**

→ 最佳進場點是股價**接近 12 個月低點**且**近 6 個月有明顯下跌**時。

## 研究方法

### 樣本篩選
- 數據來源：S&P Capital IQ
- 期間：2009/1/1 ~ 2024/1/1（分析期間含回溯至 2000 年）
- 篩選條件：15 年間股價至少增長 10 倍（900% 報酬）且**持續維持**（排除暫時性 10-bagger）
- 排除：基本面數據缺失的公司
- 最終樣本：464 家公司，10,740 company-years

### 建模流程

```
1. Fama-French 五因子排序 → 36 個投資組合
2. FF5 迴歸估計 → 升級版 FF5（替換代理變數）
3. General-to-specific → 從 150+ 變數篩選至簡約模型
4. 靜態模型 → 動態面板模型（加入滯後被解釋變數）
5. Granger 因果確認 → 樣本外預測評估
```

### 估計方法比較

| 模型 | 估計方法 | 特性 |
|------|---------|------|
| Model 1 | FE (levels) | 靜態固定效果 |
| Model 2 | FE (first differences) | 靜態一階差分 |
| Model 3 | IV FE Within (Wooldridge) | 動態、組內轉換 |
| Model 4 | IV FD (Anderson-Hsiao) | 動態、一階差分 |
| Model 5 | Difference GMM 2-step (Arellano-Bond) | 動態、差分 GMM |
| Model 6 | System GMM 2-step (Roodman) | 動態、系統 GMM |
| Model 7 | System GMM 1-step (Blundell-Bond) | 動態、系統 GMM |

所有模型均通過 Arellano-Bond 自相關檢定（AR(1) 顯著、AR(2) 不顯著），使用 cluster() 修正異質變異與自相關。

## 樣本描述統計

### Multibagger 的典型輪廓（2009 年起點中位數）

| 指標 | 數值 |
|------|------|
| 市值 | $348M（小型股） |
| 營收 | $702M |
| 15 年平均增長 | 26 倍（21.4% CAGR） |
| 含 100-bagger 數量 | 24 支 |
| 營收 CAGR | 11.1% |
| 毛利 CAGR | 12.0% |
| 營業利益 CAGR | 17.3% |
| 淨利 CAGR | 22.9% |
| EPS CAGR | 20.0% |
| 起始估值 (P/S) | 0.6 |
| 起始估值 (P/B) | 1.1 |
| 起始估值 (Forward P/E) | 11.3 |
| 起始 PEG | 0.8 |
| 毛利率 | 34.8% |
| 營業利益率 | 3.9% |
| ROE | 9.0% |
| ROC | 6.5% |

### 達到 10 倍所需時間

| 分組 | 總增長 (%) | 增長倍數 | CAGR | 達標月數 |
|------|-----------|---------|------|---------|
| Top 10 | 12,143.9 | 122.4x | 37.6% | 7.5 |
| Top 25 | 5,340.0 | 54.4x | 30.5% | 11.0 |
| Top 50 | 4,283.8 | 43.8x | 28.7% | 20.0 |
| Top 100 | 3,433.0 | 35.3x | 28.8% | 40.5 |
| 全樣本 | 1,725.1 | 18.3x | 21.4% | 107.0 |
| 基準 Nasdaq 100 | 1,277.0 | 13.8x | 19.1% | 140.0 |

### 產業分佈

| 產業 | 佔比 |
|------|------|
| Information Technology | 20% |
| Industrials | 19% |
| Consumer Discretionary | 18% |
| Health Care | 14% |
| Financials | 9% |
| Consumer Staples | 6% |
| Materials | 5% |
| Communication Services | 4% |
| Real Estate | 2% |
| Energy | 2% |
| Utilities | 1% |

## 預測能力

### 樣本外預測（2023-2024）

- 所有模型成功預測了 2023 年投資組合的**下跌方向**和 2024 年的**回升方向**
- 模型有系統性**偏保守**（平均預測誤差 -6.63%），對投資人而言反而是好事（內建安全邊際）
- 升息環境下預測最準確（平均誤差僅 -1.68%）
- 降息/平穩環境下偏保守更嚴重（平均誤差 -9.92%）
- 沒有任何一年出現「模型預測上漲但實際下跌」的情況

## 實務選股公式（根據論文推導）

根據所有顯著因子，作者暗示的 multibagger screener 邏輯：

```
篩選條件（精簡版）：
1. 規模小    → TEV 或市值偏低（small cap 優先）
2. 價值低估  → B/M > 0.4，FCF/P 高（free cash flow yield 高）
3. 有獲利    → ROA > 0，EBITDA margin 正
4. 積極投資  → 資產成長率高，但 ≤ EBITDA 成長率
5. 近期回調  → 股價接近 12 個月低點，近 6 個月有下跌
6. 利率環境  → Fed 非升息期間進場更佳（或已升到頂）
```

**避開信號**：
- B/M ≤ 0，負權益
- 營業利潤率為負
- 保守投資（資產萎縮）
- 股價在 52 週高點附近

## 文獻脈絡

論文追溯了 multibagger 研究的主要里程碑：

| 年代 | 作者 | 貢獻 |
|------|------|------|
| 1931 | Wyckoff | 價量分析、市場心理學 |
| 1934 | Graham & Dodd | 內在價值、安全邊際 |
| 1970 | Fama | 效率市場假說 |
| 1972 | Phelps | 首次系統研究 100-bagger（1932-1971，365 支） |
| 1985 | De Bondt & Thaler | 過度反應假說 |
| 1988 | Peter Lynch | 「以合理價格買成長」GARP 策略 |
| 1993 | Fama & French | 三因子模型 |
| 2014 | Oswal | 印度市場 100-bagger（47 支），提出 QGLP 框架 |
| 2014 | Martelli | 美國 10x 股票的規模模式 |
| 2015 | Fama & French | 五因子模型 |
| 2018 | Mayer | 100-bagger（1962-2014），coffee-can 投資法 |

本研究的獨特貢獻：
1. **首次**以嚴格計量方法（而非描述統計）分析 multibagger
2. 涵蓋 2009-2024 最近期，包含 AI、疫情、升息等新環境
3. 建立可操作的量化框架（非定性建議）
4. 推翻了多個未經驗證的「業界共識」

## 研究限制與未來方向

- **地理侷限**：僅美國市場，新興市場的驅動因子可能不同
- **產業差異**：科技 vs 金融 vs 工業可能需要不同模型
- **技術創新衝擊**：AI 等顛覆性技術可能改變因子的有效性
- **散戶影響**：COVID 後散戶佔美國交易量 25%+，meme stock 等社群行為未納入
- **AI/ML 擴展**：本研究以可解釋性為優先選擇線性面板模型；未來可用 neural network、random forest 等提升預測精度
- **替代數據**：社群情緒、新聞情緒分析可能增強模型
