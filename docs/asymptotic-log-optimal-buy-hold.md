---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-trending-up"
oneliner: "Hsieh 2023 Automatica：證明只要存在 dominant asset，buy-and-hold 就是 asymptotically log-optimal，且 frequency-based 高頻再平衡無法超越被動持有"
tags:
  - quant
  - portfolio-optimization
  - control-theory
---

# On Asymptotic Log-Optimal Buy-and-Hold Strategy

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2103.04898> |
| 期刊 | Automatica, vol. 151, pp. 110901:1–110901:11（2023） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2021-03-08 |
| **領域** | Optimization and Control、Mathematical Finance |

## 一句話摘要

理論告訴你「全押 dominant asset」可獲最高 log growth，但這風險太大。本篇證明：**只要市場上存在 dominant asset，無論你怎麼 ad hoc 地配權重做 buy-and-hold，都會以次線性速率收斂到 log-optimal**；含每檔資產非零權重的 market portfolio 也是 asymptotically log-optimal。

## 核心貢獻

1. **Buy-and-hold asymptotic optimality**：dominant asset 存在時，「全押該資產做 buy-and-hold」是 asymptotically log-optimal。
2. **Model-robust extension**：交易者沒有機率模型 / 不信歷史資料時，結論仍成立。
3. **Market portfolio 也達標**：含每檔資產非零權重的 market portfolio 同樣 asymptotically log-optimal（有 dominant asset 前提下）。
4. **High-Frequency Maximality Conjecture**：在無交易成本情境下，**任何再平衡策略在 log-growth 意義下都不會超越 buy-and-hold**。
5. **再平衡時機指引**：給出何時應該（不該）再平衡的原則。

## 方法論

- 多資產 frequency-based portfolio 框架（m ≥ 2 assets）
- 識別 dominant asset 與漸近收斂率分析
- 理論證明 + 歷史資料模擬

## 目前限制與注意事項

- **「Dominant asset 存在」是強假設**：實務上難以事前識別誰會 dominate。
- **無交易成本前提**：High-Frequency Maximality 的結論依賴此假設，含成本後再平衡仍可能有價值（作者其他論文處理）。
- **Asymptotic 結論**：有限樣本下偏差可能很大。

## 研究價值與啟示

### 關鍵洞察

1. **「Buy-and-hold = asymptotically log-optimal」是被動投資派的理論彈藥**：散戶 / 主動派 vs 被動派的爭論裡，本篇給被動派一個強學術結論：**長期看，誰是 dominant asset、你 ad hoc 配的 buy-and-hold 就會逼近最佳**。等於把 Bogle 的 1/N 直覺升級為定理。
2. **「High-Frequency Maximality Conjecture」翻譯成白話**：「在沒有交易成本的世界裡，再平衡是浪費」── 這個直覺很多人有，但放進嚴格 frequency-based 框架做出來才有引用價值。conjecture 也意味著作者後續論文可能朝證明 / 反證這條走。
3. **Dominant asset 前提反映實務智慧**：歷史上股市裡 nVidia / Apple / 美元 / 比特幣等都曾是某段時期的 dominant asset，事後看買誰都對。本篇等於說「**只要你有眼光買到一個會 dominant 的標的，怎麼配權重都不會偏離最佳太遠**」── 這是 Munger / Buffett 的選股哲學的數學化版本。
4. **「Model-robust」延伸有實務意義**：交易者多半不信任歷史機率模型（樣本不足、結構斷裂），本篇結論在「沒有模型」場景仍成立 ── 等於 robust trading 的非機率派論述。
5. **Automatica 期刊位置定位**：本篇登在控制論頂刊，把投資組合問題包裝成系統理論問題。**控制論社群把財務當應用領域開拓**這條路線值得追蹤。

### 與其他研究筆記的關聯

- **[Robust Log-Optimal Hyperplane](robust-log-optimal-hyperplane.md)** ── distributionally robust 求解版本。
- 後續 Kelly betting / drawdown 系列依此基礎再延伸。
