---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-decision-tree"
oneliner: "Hsieh × Wong 2025 ACC：固定階段、含確定與隨機選項的 risk-sensitive 多階段決策，導出最佳性必要條件，示範用於最佳押注與庫存管理"
tags:
  - quant
  - control-theory
---

# On Risk-Sensitive Decision Making Under Uncertainty

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2404.13371> |
| 會議 | American Control Conference (ACC) 2025, Denver, Colorado |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、Yi-Shan Wong |
| **首版** | 2024-04-20 |

## 一句話摘要

把「**固定階段、混合確定與隨機選項**」的多階段決策問題**包成 stochastic control**，給出 **risk-sensitive** 設定下的**最佳性必要條件**；以最佳押注 + 庫存管理兩個案例示範。

## 核心貢獻

1. **混合確定/隨機選項建模**：每階段同時有 deterministic 與 stochastic alternatives 可選。
2. **必要最佳性條件**：在 risk-sensitive 框架下給出。
3. **跨應用示範**：betting + inventory，把同一個 control 框架推到兩個不同領域。

## 目前限制與注意事項

- 仍是必要條件，未必充分。
- 階段數固定，extension 到無窮階段仍 open。
- 缺實證資料。

## 研究價值與啟示

### 關鍵洞察

1. **「Risk-sensitive control」是 Kelly / log-utility 的廣義語言**：用 risk-sensitive 包裝後可調整 risk aversion 參數，把 Kelly 從「必須 log-utility」放鬆到「任何 exponential utility 級別」。
2. **「確定 + 隨機選項混合」反映實務**：投資人面對「下定存（確定）vs 買股票（隨機）」這種混合決策，本篇的建模比純隨機更貼實際。
3. **Betting + Inventory 雙案例是策略性安排**：把同一框架同時放進財務與營運兩個領域，論文受眾擴大、引用面增加。
4. **ACC 場合定位實作派**：較 CDC 應用導向，本篇的兩案例符合 ACC 喜好。

### 與其他研究筆記的關聯

- **[Frequency-Based Kelly Optimal Portfolio](frequency-based-kelly-portfolio.md)** ── 同 Kelly / risk-sensitive 路線。
- **[Kelly Betting Too Conservative](kelly-betting-too-conservative.md)** ── 對 Kelly 框架限制的反思。
