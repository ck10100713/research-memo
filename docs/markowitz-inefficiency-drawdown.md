---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-trending-down"
oneliner: "Hsieh × Barmish 2017 CDC：以 drawdown 取代 variance 當風險指標時，古典 Markowitz LTI 反饋策略不效率，drawdown modulator 時變反饋以機率 1 提供 worst-case drawdown 保護"
tags:
  - quant
  - drawdown
  - control-theory
---

# On Inefficiency of Markowitz-Style Investment Strategies When Drawdown is Important

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1710.01501> |
| 會議 | IEEE CDC 2017, Melbourne, pp. 3075–3080 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish |
| **首版** | 2017-10 |

## 一句話摘要

「保守投資人最在意的是 drawdown 而非 variance」── 換用 drawdown + 平均報酬當作風險-報酬框架後，**古典 Markowitz LTI 投資策略變得不效率**；本篇提出 **drawdown modulator**（時變線性反饋），dominate Markowitz 並以**機率 1** 給出 worst-case drawdown 保護。

## 核心貢獻

1. **Markowitz 在 drawdown 框架下不效率**：等同於說 MV 不適合風險厭惡的長期投資人。
2. **Drawdown modulator**：時變線性反饋機制，dominate 古典 LTI。
3. **機率 1 worst-case 保護**：不僅是平均，是 almost-surely 的保證。

## 目前限制與注意事項

- Drawdown 度量本身有多種定義（最大 drawdown vs 平均 drawdown vs underwater duration），結論依度量不同會變。
- LTI vs 時變反饋的對比建立在 control-theoretic 抽象上，與實務 portfolio strategy 還有距離。

## 研究價值與啟示

### 關鍵洞察

1. **「Variance ≠ Risk」對保守派而言是常識，但能用數學嚴格證明 MV 不效率的不多**：本篇給出明確結論 ── **如果你在意 drawdown，MV 是錯的工具**。對 robo-advisor、退休基金的配置思維會是衝擊。
2. **時變反饋勝過 LTI 在 control 學界很自然，但在 finance 還是新意**：投資界的「rebalance」本質上就是時變反饋，但少有 paper 從 control 角度給嚴格 dominance 結果。
3. **「機率 1」的承諾很強**：很多風控結論是「機率上界」、「期望意義」、「99% VaR」── 機率 1 worst-case 是更強的保證，雖然代價可能是犧牲報酬。
4. **這是 Hsieh × Barmish 合作早期奠基論文**：drawdown modulation 後續成為作者整條 drawdown 子線（2017→2023→...）的核心概念。

### 與其他研究筆記的關聯

- **[On Drawdown-Modulated Stock Trading](drawdown-modulated-stock-trading.md)** ── 同年 IFAC 姊妹論文，把 drawdown modulator 用 lemma 形式完整化。
- **[Drawdown Control with Restart Mechanism](drawdown-control-restart-mechanism.md)** ── 後續加 restart 的進化版本。
