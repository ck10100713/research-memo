---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-timer-sand"
oneliner: "Hsieh × Barmish × Gubner 2019 CDC：證明無延遲時 high-frequency trading 嚴格優於 buy-and-hold，但執行延遲存在時 buy-and-hold 反過來勝出 — 即使零成本"
tags:
  - quant
  - kelly
  - control-theory
---

# The Impact of Execution Delay on Kelly-Based Stock Trading: High-Frequency Versus Buy and Hold

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1907.08771> |
| 會議 | IEEE CDC 2019, Nice, France, pp. 2580–2585 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish、John A. Gubner |
| **首版** | 2019-07 |

## 一句話摘要

在 ELG（Expected Logarithmic Growth）標準下：
- **無執行延遲**時，HFT 嚴格優於 buy-and-hold（即使零成本）
- **存在執行延遲**時，**buy-and-hold 反而勝過 HFT**（仍是零成本）

延遲本身比交易成本更能逆轉策略優劣排序。

## 核心貢獻

1. **無延遲下 HFT 嚴格優於 B&H 的理論證明**（在 ELG 標準下）。
2. **延遲存在則翻轉**：用 binary lattice 模擬證明 buy-and-hold 反勝。
3. **與 self-financing 約束無關**：結論在含與不含此約束下都成立。

## 方法論

- 數學證明（無延遲情境）
- Binary lattice stock model 模擬（含延遲情境）

## 目前限制與注意事項

- Binary lattice 模型較粗，現代市場非二項式。
- 延遲建模單純（固定 lag），未含 latency 變動性。
- ELG 為 Kelly 標準，未涵蓋其他效用函數。

## 研究價值與啟示

### 關鍵洞察

1. **「執行延遲比交易成本更致命」是反直覺結論**：交易成本研究汗牛充棟，但執行延遲研究較少；本篇等於告訴你 ── 在某些情境下，**改善 latency 比降低成本更值得投資**。
2. **HFT vs B&H 的爭論被框成 ELG 命題**：把「主動派 vs 被動派」翻譯成 ELG 標準下的最佳化問題，是把哲學爭論變成可解的數學題。
3. **零成本世界裡 buy-and-hold 仍可勝出**：很多人以為「沒成本 = HFT 必贏」，本篇打破這個直覺，是給被動派的另一發數學彈藥。
4. **這是作者跟 Barmish 的早期合作**：Barmish 是 control theory + finance 的老牌人物，這條合作線後續延伸到 Kelly betting 系列、affine feedback、delay equation 等。

### 與其他研究筆記的關聯

- **[Asymptotic Log-Optimal Buy-and-Hold](asymptotic-log-optimal-buy-hold.md)** ── 從 dominant asset 角度給 B&H 另一個 asymptotic 優勢。
- **[Rebalancing Frequency for Kelly-Optimal Portfolios](rebalancing-frequency-kelly-portfolios.md)** ── 同 Hsieh × Barmish × Gubner 線的相關論文。
- **[At What Frequency Should Kelly Bettor Bet](kelly-bettor-frequency.md)** ── 從頻率角度切入的姊妹篇。
