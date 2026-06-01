---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-function-variant"
oneliner: "Hsieh 2020 CCTA：Kelly betting 用 Taylor 近似化為 quadratic programming，得到閉式近似解，並分析績效、變異數、survivability 等性質"
tags:
  - quant
  - kelly
  - control-theory
---

# On Feedback Control in Kelly Betting: An Approximation Approach

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2004.14048> |
| 會議 | IEEE Conference on Control Technology and Applications (CCTA) 2020, Montreal, pp. 903–908 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2020-04-29 |

## 一句話摘要

Kelly 押注最佳化原本是 concave program，本篇用 **Taylor 級數近似**把它**降為 quadratic programming**，得到**閉式近似解**；並分析此近似解的績效、變異數、與 survivability（破產防範）性質。

## 核心貢獻

1. **Taylor → QP 降階**：把 concave 的 log 目標換成 quadratic，直接得閉式解。
2. **近似解性質完整刻畫**：期望 gain/loss、變異數、survivability 全部給出。
3. **填補既有 Kelly 文獻空白**：過去近似法常被詬病「沒誠實分析誤差」，本篇正面回應。

## 目前限制與注意事項

- Taylor 在 log 報酬大時誤差大。
- QP 比閉式更貼近實作，但仍是近似，極端市況可能失準。

## 研究價值與啟示

### 關鍵洞察

1. **Approximation 不是放棄精度，是 trade-off 計算與洞察**：精確 Kelly 解需 numerical solver，閉式近似解可立刻看出參數效應。對策略設計階段更有用。
2. **與 Kelly Betting Limitations（2015）形成對話**：作者 2015 那篇就點出「Taylor 近似有問題」，本篇則展示「**正確使用 Taylor 近似仍有用**」── 自我延伸的研究脈絡。
3. **CCTA 場合定位**：CCTA 比 CDC 應用導向，本篇的閉式近似 + survivability 條件適合此會議。
4. **Survivability 在近似解下仍能保證**：這是 reviewers 最在意的 ── 近似解最怕「平均看起來好但極端會破產」，本篇排除這個風險。

### 與其他研究筆記的關聯

- **[On Kelly Betting: Some Limitations](kelly-betting-limitations.md)** ── 同作者 5 年前指出 Taylor 近似問題的反思。
- **[Kelly Betting Can Be Too Conservative](kelly-betting-too-conservative.md)** ── 對 Kelly 框架的另一面批評。
