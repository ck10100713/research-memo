---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-format-list-checks"
oneliner: "Hsieh 2021 L-CSS：給出 frequency-based Kelly 最佳組合的充分必要條件、Extended Dominant Asset Theorem，並提出顯式 trading algorithm 用 dominant asset 條件決定下單時點"
---

# Necessary and Sufficient Conditions for Frequency-Based Kelly Optimal Portfolio

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/pdf/2004.12099> |
| 期刊 | IEEE Control Systems Letters, vol. 5, no. 1, pp. 349–354（2021） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2020-04-25 |

## 一句話摘要

把 frequency-based Kelly portfolio 的最佳性條件從「只證充分」推到「**充分必要**」；同時給出 **Extended Dominant Asset Theorem**：「某資產為 dominant ⇔ 最佳組合只含該資產」，並提出實作演算法。

## 核心貢獻

1. **充分必要條件**：對 frequency-based Kelly 給出完整刻畫（expected ratio optimality + asymptotic relative optimality）。
2. **Extended Dominant Asset Theorem**：dominant asset 與全押解的 iff 等價。
3. **Survivability + bankruptcy 處理**：在 frequency-based 框架顯式處理破產風險。
4. **實用演算法**：用 dominant asset 條件決定何時交易、何時不動。

## 目前限制與注意事項

- 仍以離散時間 + 機率模型為基礎，需要分布假設。
- 「Dominant」事前識別困難。
- 短篇 L-CSS，細節推導需配合作者其他文章。

## 研究價值與啟示

### 關鍵洞察

1. **「充分必要」是論文價值的金字招牌**：給出充要條件意味著「這就是答案，不會有別的更好的解被遺漏」── 對控制 / 最佳化社群的引用價值很高。
2. **Dominant Asset Theorem 與 buy-and-hold 結論呼應**：本篇 + Asymptotic Log-Optimal Buy-and-Hold（2103.04898）合在一起就是 ── 「**有 dominant 就全押，沒 dominant 才談分散**」。這個視角顛覆 mean-variance 分散教條。
3. **Survivability 處理是實務派強項**：很多 Kelly 文章把破產問題輕輕帶過，本篇直接放進框架。
4. **演算法包裝讓論文易落地**：給「何時下單」的具體條件，不只是理論存在性。

### 與其他研究筆記的關聯

- **[Asymptotic Log-Optimal Buy-and-Hold](asymptotic-log-optimal-buy-hold.md)** ── 給 dominant asset 的 buy-and-hold asymptotic optimality。
- **[Frequency-Based Optimal Portfolio with Costs](frequency-based-optimal-portfolio-costs.md)** ── 加上交易成本的延伸。
