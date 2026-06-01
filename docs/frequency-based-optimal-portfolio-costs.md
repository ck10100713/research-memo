---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-clock-fast"
oneliner: "Wong × Hsieh 2023：把 frequency-dependent log-optimal portfolio 加上交易成本後仍保持為 concave program，用兩基金定理 + sliding window 解出每期可實作的解"
tags:
  - quant
  - portfolio-optimization
---

# On Frequency-Based Optimal Portfolio with Transaction Costs

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2301.02754> |
| 期刊 | IEEE Control Systems Letters, vol. 7, pp. 3489–3494（2023） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Yi-Shan Wong、Chung-Han Hsieh |
| **首版** | 2023-01 |
| **資料** | 日內 + 日頻歷史價格 |

## 一句話摘要

把 log-optimal portfolio 加上**再平衡頻率**這個維度，再放回**真實交易成本** ── 證明問題仍是 concave program、給出含成本的 dominance theorem、並用 sliding window 把它變成可線上跑的版本。

## 核心貢獻

1. **Concave program 等價**：頻率相依 log-optimal + 成本 ≡ concave 最佳化問題。
2. **Dominance theorem with costs**：含成本下的最佳資產配置判定條件。
3. **指出 bankruptcy 風險**：成本累積可能讓策略破產，需要主動防範。
4. **Quadratic concave 近似 + 最優條件**：給出可解形式與最優性條件。
5. **Two-fund theorem 變體**：最佳權重的凸組合仍是最佳。
6. **Sliding window 線上化**：把 stochastic dynamic programming 換成連續解 concave program。

## 目前限制與注意事項

- 仍假設成本為凸函數，bid-ask spread + market impact + slippage 不一定凸。
- Sliding window 長度需經驗選擇。
- 破產條件給出但避免方式仰賴策略限制。

## 研究價值與啟示

### 關鍵洞察

1. **「頻率」是 log-optimal 文獻長期忽略的維度**：Kelly / log-optimal 經典文獻多假設連續或固定頻率，本系列把「再平衡頻率本身」當決策變數，視角更接近實務。
2. **Concave 性質保留是好理論的指標**：加上成本後仍是 concave program ── 等於數學結構沒崩，可以繼續用既有 LP / convex solver 解。
3. **Bankruptcy 風險顯式提出**：不少 Kelly 文章假裝沒事，本篇直接點出 ── **任何 log-utility 系列方法都應該先檢查破產條件**，這是實務人最在意的點。
4. **Sliding window 等於把離線最佳化變成線上**：sliding window 是 control theory + online learning 的經典工具，套到 portfolio 上就是「滾動式 log-optimal」，比傳統 monthly rebalance 更貼近高頻場景。

### 與其他研究筆記的關聯

- **[Sliding Window Log-Optimal Portfolio](sliding-window-log-optimal-portfolio.md)** ── 同條 sliding window 路線的另一篇。
- **[Robust Log-Optimal Hyperplane](robust-log-optimal-hyperplane.md)** ── 處理「分布不確定」的姊妹問題。
