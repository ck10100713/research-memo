---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-cash-minus"
oneliner: "Hsieh 2022 L-CSS：DLP 加上交易成本後 robust positive expected gain 可能消失，本篇給出保留正期望的條件、用 GBM with jumps 模擬與 BTC-USD 回測驗證"
tags:
  - quant
  - control-theory
---

# On Robustness of Double Linear Trading with Transaction Costs

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2209.12383> |
| 期刊 | IEEE Control Systems Letters, vol. 7, pp. 679–684（2022） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2022-09 |
| **資料** | GBM with jumps 模擬 + BTC-USD 歷史 |

## 一句話摘要

DLP 在無摩擦市場可以保證 robust positive expected gain，但**交易成本可以把這個保證吃掉**；本篇給出**在何種條件下正期望仍能保留**的判定條件，並用 GBM with jumps 與比特幣回測驗證。

## 核心貢獻

1. **點出 cost 可吃掉 DLP 結構紅利**：清楚展示 transaction cost 何時讓 DLP 失效。
2. **保留正期望的條件**：給出顯式不等式，把成本上限與權重設定關聯起來。
3. **GBM with jumps 模擬**：超越 vanilla BM，模擬肥尾事件下的表現。
4. **BTC-USD 歷史回測**：實際資料驗證理論。

## 目前限制與注意事項

- 成本模型仍簡化（線性 / 比例式）。
- BTC 單一資產，多資產含成本版本要看 multi-DLP 系列。
- L-CSS 篇幅短，理論細節需配合作者其他文章。

## 研究價值與啟示

### 關鍵洞察

1. **任何「結構性正期望」都該先過 cost 那關**：學術上常見「無成本世界裡某策略期望為正」，本篇直接告訴你「**成本一進來，這個保證可能立刻消失**」── 是個對 DLP 主結果的誠實警示。
2. **Cost-aware 條件給策略上線提供 sanity check**：實作時可以拿論文不等式當作「我設定的權重 + 我估的成本，是否仍能維持正期望」的檢核。
3. **GBM with jumps 是更貼近現實的模擬**：純 GBM 對加密貨幣不適用（肥尾、跳躍頻繁），加 jump 後才有意義。
4. **BTC 是好的 stress-test**：高波動 + 高成本 + 24/7 = 對任何策略都是嚴格考驗。

### 與其他研究筆記的關聯

- **[DLP with Time-Varying Weights](dlp-time-varying-weights.md)** ── 同 DLP 系列。
- **[Robust Trading in Lattice Market](robust-trading-lattice-market.md)** ── DLP 多資產延伸（沒處理成本）。
- **[Robust Optimal Linear Feedback Stock Trading](robust-optimal-linear-feedback-trading.md)** ── DLP 早期理論基礎。
