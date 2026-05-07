---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-window-restore"
oneliner: "Wang × Hsieh 2022 IFAC：用 sliding window 解 log-optimal portfolio，產生時變權重而非靜態配置，累積報酬率超越傳統常數權重 log-optimal"
---

# On Data-Driven Log-Optimal Portfolio: A Sliding Window Approach

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2206.12148> |
| 期刊 | IFAC-PapersOnLine, vol. 55, no. 30, pp. 474–479（2022） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Pei-Ting Wang、Chung-Han Hsieh |
| **首版** | 2022-06 |

## 一句話摘要

把 log-optimal portfolio 從**離線一次解出常數權重**改成**滾動視窗解**，每期重新最佳化得到時變權重；歷史回測累積報酬率超越傳統 log-optimal。

## 核心貢獻

1. **Sliding window 架構**：每期只用最近 N 期資料解一次 log-optimal，得到當期權重。
2. **時變權重 vs 常數權重對比**：累積報酬率顯著改善。
3. **資料驅動 + 線上化**：不需要事前知道分布，用最近樣本不斷更新。

## 目前限制與注意事項

- 視窗長度 N 是超參數，缺一般化選擇規則。
- 高頻資料下計算負荷高（每期都要重解）。
- 沒有顯式處理 transaction cost。

## 研究價值與啟示

### 關鍵洞察

1. **「靜態最佳 → 滾動最佳」是 log-optimal 走向實務的必經之路**：傳統 Kelly / log-optimal 的詬病就是「假設知道真實分布」，sliding window 用「最近 N 期經驗分布」替代，是實作的合理妥協。
2. **與 frequency-based optimal portfolio 互補**：作者另一條 frequency 路線把「再平衡頻率」當變數，本篇把「視窗長度」當變數 ── 兩條都是把單一靜態解變多參數可調的表現體。
3. **每期重解 = online learning**：等於把 log-optimal 接到 online optimization / online learning 框架，可以期待引入 adaptive 學習率、regret bound 等工具。
4. **IFAC 的小篇幅短暫**：6 頁論文做核心 idea POC，後續 frequency-based with cost（2301.02754）才把這條路線完整化。

### 與其他研究筆記的關聯

- **[Frequency-Based Optimal Portfolio with Costs](frequency-based-optimal-portfolio-costs.md)** ── 同 sliding window 主題的後續完整版（含成本）。
- **[Robust Log-Optimal Hyperplane](robust-log-optimal-hyperplane.md)** ── distributionally robust 的姊妹解法。
