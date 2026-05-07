---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-alert-circle"
oneliner: "Hsieh × Barmish 2015 Allerton：Kelly 系列研究的開山批判篇—點出 Taylor 近似失準與 drawdown 過大兩個 Kelly 主結論的限制，定調作者後續整條 Kelly 研究線的問題清單"
---

# On Kelly Betting: Some Limitations

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1710.01787> |
| 會議 | Allerton Conference on Communication, Control, and Computing 2015, Monticello, pp. 165–172 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish |
| **發表** | 2015（Allerton）／ 2017 上 arXiv |

## 一句話摘要

不替 Kelly 辯護，反過來**列出 Kelly 的限制**：(1) 常見 Taylor 近似在某些情境誤差很大（後續 2020 Approximation 論文回應）；(2) Kelly 解的 drawdown 風險可能很大（後續 2017 Drawdown Modulation 論文回應）。**整條 Hsieh 學術線的問題清單就是從這篇生出來**。

## 核心貢獻

1. **批判 Taylor 近似濫用**：給具體例子展示誤差。
2. **點出 drawdown 大問題**：Kelly 解 drawdown 可能讓投資人受不了。
3. **指明研究方向**：建議從這兩個問題切入做後續工作。

## 方法論

數學分析 + 具體例子展示 Kelly 主結果的失效情境。

## 目前限制與注意事項

- 是純批判 / 概念論文，無新方法或定理。
- 例子驅動，缺一般化條件刻畫。

## 研究價值與啟示

### 關鍵洞察

1. **「先列限制再做後續工作」是聰明的研究發起策略**：本篇 = 整條 Hsieh 後續 publication 的「To-Do List」。把限制清單寫進論文，等於宣告未來幾篇要解什麼題目。
2. **「敢批自己用的工具」反映學術獨立性**：Kelly betting 在 control 社群是甜蜜區，敢正面說它有問題比起單純套用更可貴。
3. **Allerton 場合定位**：Allerton 是控制 / 通訊 / 計算的小而精會議，傳統上發表 conceptual 或先導性論文。本篇放這裡反映「先讓概念落地、後續才大力發表」的策略。
4. **與 Drawdown Modulation 系列直接相連**：本篇的「drawdown 問題」直接被 2017 IFAC（Drawdown-Modulated Stock Trading）回應，等於 self-citation 鏈。

### 與其他研究筆記的關聯

- **[Kelly Betting Too Conservative](kelly-betting-too-conservative.md)** ── 後續第二批 Kelly 批判。
- **[Feedback Control in Kelly Betting Approximation](feedback-control-kelly-betting-approximation.md)** ── 回應 Taylor 近似批判的續篇。
- **[Drawdown-Modulated Stock Trading](drawdown-modulated-stock-trading.md)** ── 回應 drawdown 批判的續篇。
- **[Markowitz Inefficiency Drawdown](markowitz-inefficiency-drawdown.md)** ── 把 drawdown 視角推到 portfolio 全層級。
