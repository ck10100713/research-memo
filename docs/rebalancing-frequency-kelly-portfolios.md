---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-sync"
oneliner: "Hsieh × Gubner × Barmish 2018 CDC：把再平衡頻率明確當參數放進 Kelly-optimal 框架，證明 dominant 條件下績效對頻率為常數函數，HFT 不必然改善"
---

# Rebalancing Frequency Considerations for Kelly-Optimal Stock Portfolios in a Control-Theoretic Framework

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1807.05265> |
| 會議 | IEEE CDC 2018, Miami Beach, pp. 5820–5825 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、John A. Gubner、B. Ross Barmish |
| **首版** | 2018-07 |

## 一句話摘要

把作者前一年 ACC 的 betting frequency 結論**從單押注場景擴張到多資產組合**：用控制理論視角，明確把「再平衡頻率」當作 Kelly-optimal 的決策參數，並證明 **dominant asset 存在時，績效是頻率的常數函數**（換言之，「再平衡頻率」此時不重要）。

## 核心貢獻

1. **頻率作為 Kelly 顯式參數**：control-theoretic 框架下把 rebalance frequency 拉成設計變數。
2. **Dominance 條件**：當存在 dominant asset，最佳組合單押該資產，頻率變得無關。
3. **HFT 不必然改善**：在零成本世界裡，更高頻不必然帶來更高 ELG。

## 目前限制與注意事項

- 仍假設 ELG / Kelly 標準。
- 多資產 dominance 條件的事前識別困難。
- Asymptotic 結論，有限樣本下偏差仍大。

## 研究價值與啟示

### 關鍵洞察

1. **「dominance → 頻率不重要」是被動投資的數學注釋**：被動派的「不要常常動」直覺，在 dominant asset 條件下被嚴格證明 ── 是反直覺也是強結論。
2. **這篇是 frequency 路線從 betting 推到 portfolio 的關鍵節點**：作者 2018 年另一篇 ACC 已處理單押注場景，本篇升級到多資產。
3. **Control-theoretic packaging 的賣點**：把投資視為 control system，論文容易被控制社群吸收，但也限制了財務社群的接觸面。
4. **與 Asymptotic Buy-and-Hold（2103.04898）形成連續論述**：dominant → 頻率無關（本篇）+ dominant → buy-and-hold 漸近最佳（2103.04898），兩篇結合構成「**有 dominant 就買進不動**」這條完整論述。

### 與其他研究筆記的關聯

- **[At What Frequency Should Kelly Bettor Bet](kelly-bettor-frequency.md)** ── 本篇的單押注前作。
- **[Asymptotic Log-Optimal Buy-and-Hold](asymptotic-log-optimal-buy-hold.md)** ── 從漸近最佳性角度給出同主題另一面。
- **[Frequency-Based Kelly Optimal Portfolio](frequency-based-kelly-portfolio.md)** ── 給出充分必要條件的延伸。
