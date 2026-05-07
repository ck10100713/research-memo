---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-stop-circle"
oneliner: "Hsieh 2022 Automatica：把 affine feedback stock trading 結果擴張至含 stop-loss 訂單，GBM 下給出累積 P&L 的閉式 CDF，含 stop-loss 涵蓋無 stop 為特例"
---

# Generalization of Affine Feedback Stock Trading Results to Include Stop-Loss Orders

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2004.12848> |
| 期刊 | Automatica, vol. 136, pp. 11051:1–11051:7（2022） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2020-04-27 |

## 一句話摘要

把 **affine feedback stock trading** 的既有結果擴張到含 **stop-loss 訂單**：用 GBM 當價格模型，導出**含 stop-loss 的累積 P&L 的閉式 CDF**；無 stop-loss 的舊結果是本篇特例。

## 核心貢獻

1. **Affine feedback + stop-loss 統一處理**：給出含 stop 的閉式分布。
2. **回收舊結果為特例**：stop-loss 上限放鬆 → 退化為經典結果。
3. **顯式刻畫 survivability、cash-financing、long-only、期望 P&L 下界**等實務關注議題。

## 方法論

GBM 隨機微積分 + control theory feedback 設計 + stop-loss order 的結束時刻刻畫；給出 P&L CDF 閉式表達。

## 目前限制與注意事項

- GBM 假設限制（無跳躍、波動性常數）。
- 連續時間設定，與離散下單實務有 gap。

## 研究價值與啟示

### 關鍵洞察

1. **Stop-loss 在控制論的學術處理一直不夠完整**：實務人天天用 stop-loss，但學術上常被當「外加規則」而非內生策略；本篇把它放進 affine feedback，理論層級補強。
2. **閉式 CDF 是金字招牌**：能給出 P&L 的完整分布閉式 = 任何下檔風險指標（VaR、CVaR、機率破產）都可直接導出。
3. **Automatica 期刊位置反映重視**：Automatica 是控制論頂刊，把 stop-loss + affine feedback 推到 Automatica 等於在控制社群打標。
4. **連續時間 GBM 是雙刃**：給漂亮閉式但離實務遠；後續論文（DLP 系列）轉離散時間就是為了更貼近實務。

### 與其他研究筆記的關聯

- **[Positive Solutions of Delay Equation](positive-solutions-delay-equation.md)** ── 同主題（trader account positivity）的姊妹篇。
- **[Robust Optimal Linear Feedback Trading](robust-optimal-linear-feedback-trading.md)** ── 同 affine / linear feedback 控制路線的 robust 版本。
