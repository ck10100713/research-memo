---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-vector-line"
oneliner: "Hsieh 2024 EJOR：用 supporting hyperplane 把 distributionally robust log-optimal portfolio 化成線性規劃，可內建交易成本、槓桿、做空、survival、分散性條件"
tags:
  - quant
  - portfolio-optimization
---

# On Solving Robust Log-Optimal Portfolio: A Supporting Hyperplane Approximation Approach

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2202.03858> |
| 期刊 | European Journal of Operational Research, vol. 313, no. 3, pp. 1129–1139（2024） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2022-02-08 |
| **領域** | Optimization and Control、Computational Finance、Portfolio Management、Risk Management |

## 一句話摘要

報酬分布部分已知時，把 **distributionally robust log-optimal portfolio** 用 supporting hyperplane approximation **降為線性規劃**；同時給出「給定容忍誤差，求最少 hyperplane 數」的演算法，並能直接擴充到含交易成本、槓桿、做空、survival 與分散性限制的版本。

## 核心貢獻

1. **Supporting hyperplane 線性化**：將原本困難的 distributionally robust log-optimization 化為可解的 LP。
2. **誤差驅動的 hyperplane 數選擇**：給定可接受逼近誤差，演算法自動決定需要幾條 hyperplane。
3. **框架彈性**：同一框架自然容納 transaction costs、leverage、shorting、survival、diversification constraints，無須重新證明。

## 方法論

`log` 是凹函數，可由有限條 supporting hyperplane 從上方逼近。把每條 hyperplane 視為一個線性不等式約束，原本「最大化期望 log return 在最差分布下」的 worst-case 問題就被線性化，丟給 LP solver 即可求解。

## 目前限制與注意事項

- **逼近誤差需事前估**：選太少 hyperplane 解失準、太多計算量大。
- **distributional ambiguity 用多面體 set**：Wasserstein ball 等需另一條技術路線（見作者 2410.23536）。
- **Log-optimal 在實務上偏激進**：log utility 等於 Kelly criterion，下檔風險仍可能很大，需配合 drawdown 控制（見作者 2303.02613）。

## 研究價值與啟示

### 關鍵洞察

1. **Supporting hyperplane 是 Hsieh 整條 robust 路線的鑰匙**：從本篇（2022）→ lattice market（2310.11023）→ scaling（2408.07879），同一招反覆放大覆蓋更複雜場景。**研究方法論的「主武器專精」勝過「樣樣都摸」**。
2. **「框架自然容納限制」是好理論的指標**：交易成本、槓桿、做空、survival 不需要修改主結果就能掛上去 ── 這意味著抽象層級對了。實務上設計策略時也該追求這種「核心一個、限制可插拔」的架構。
3. **EJOR 期刊位置反映受眾**：論文落在 OR 期刊不是純財務期刊，意味著作者把這條線當「最佳化方法論貢獻」推銷，財務應用是 case study。研究路線定位的選擇會影響引用社群。
4. **與 Kelly betting 系列接得很順**：log-optimal = Kelly，本篇 + 作者更早的 Kelly betting limitations（2015–2018）+ approximation approach（2020）構成完整理論線。

### 與其他研究筆記的關聯

- **[Accelerating Robust Portfolio](accelerating-robust-portfolio-optimization.md)** ── 本篇的 scale-up 版本。
- **[Robust Trading in Lattice Market](robust-trading-lattice-market.md)** ── 同作者另一條 DLP 路線。
