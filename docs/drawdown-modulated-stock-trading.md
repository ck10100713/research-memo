---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-shield-check"
oneliner: "Hsieh × Barmish 2017 IFAC：Drawdown Modulation Lemma 刻畫「以機率 1 維持 max drawdown 上限」的投資族，並在此族內最大化 Kelly ELG，給出 drawdown-constrained Kelly 的最佳投資"
---

# On Drawdown-Modulated Feedback Control in Stock Trading

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1710.01503> |
| 期刊 | IFAC-PapersOnLine, vol. 50, no. 1, pp. 952–958（IFAC World Congress 2017, Toulouse） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish |
| **首版** | 2017-10 |

## 一句話摘要

提出 **Drawdown Modulation Lemma**，刻畫「**以機率 1 維持 max drawdown 上限**」的投資族；在這個族內進一步最大化 Kelly ELG，得到 **drawdown-constrained Kelly Optimization Problem** 的最佳投資；當 drawdown 上限放寬到極大時，回收經典 Kelly 結果為特例。

## 核心貢獻

1. **Drawdown Modulation Lemma**：刻畫所有「機率 1 滿足 drawdown 上限」的投資族。
2. **Drawdown-Modulated Feedback Control**：給出具體反饋控制方案。
3. **Drawdown-Constrained Kelly**：最大化 ELG 同時受限 max drawdown。
4. **回收 Kelly 為特例**：drawdown 上限趨近最大值時退化為原始 Kelly。

## 方法論

把 control system 的 feedback 概念套到投資 ── 部位大小依目前 drawdown 水位調整，drawdown 接近上限時自動縮部位。歷史股價資料驗證。

## 目前限制與注意事項

- 仍假設機率模型已知（後續論文逐步放寬）。
- Lemma 給出族但策略選擇仍需設計。

## 研究價值與啟示

### 關鍵洞察

1. **「先刻畫滿足約束的整個族、再在族內最佳化」是聰明的兩階段方法論**：不是先解最佳化再事後加約束，而是**先把可行集做小到肯定滿足約束**，再在這個更小的集合上最佳化。這是 control 學派慣用的兩階段思路。
2. **Drawdown-Constrained Kelly 是實務人最在意的**：原始 Kelly 大家都怕（會破產），加上 drawdown 約束後變成可上線版本，本篇給出最佳解形式。
3. **「上限放寬退化為 Kelly」是好理論的指標**：新框架要能 recover old as special case，本篇做到了。
4. **IFAC 場合有 control 社群關注**：本篇配 CDC 那篇（1710.01501）形成 drawdown 主題的 1+1 cluster，發表策略上一年兩篇互引也是常用做法。

### 與其他研究筆記的關聯

- **[Markowitz Inefficiency Drawdown](markowitz-inefficiency-drawdown.md)** ── 同年 CDC 兄弟篇。
- **[Drawdown Control with Restart Mechanism](drawdown-control-restart-mechanism.md)** ── 2023 年 restart 升級版。
