---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-format-vertical-align-bottom"
oneliner: "Hsieh × Barmish × Gubner 2016 CDC：跟主流「Kelly 太激進」相反，本篇證明 Kelly 常常太保守—Restricted Betting Theorem 顯示 unbounded support 分布下 Kelly 押注趨近 0、實證樣本反而更積極"
---

# Kelly Betting Can Be Too Conservative

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1710.01786> |
| 會議 | IEEE CDC 2016, Las Vegas, pp. 3695–3707 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish、John A. Gubner |
| **發表** | 2016（CDC proceedings）／ 2017 上 arXiv |

## 一句話摘要

主流文獻常批 Kelly 「太激進」（fractional Kelly 應運而生），本篇反過來證明 Kelly **常常太保守** ── 提出 **Restricted Betting Theorem**，並證明在 **unbounded support** 分布下 Kelly 理論押注會趨近 0，但用樣本估計出來的 empirical Kelly 反而押得更積極、實際更接近最佳。

## 核心貢獻

1. **Restricted Betting Theorem**：刻畫 Kelly 何時退化為「不押」。
2. **Unbounded support 下 Kelly → 0**：揭示理論 Kelly 失效的具體場景。
3. **Theoretical vs Empirical Kelly 對比**：樣本驅動的版本反而抓住獲利機會。

## 方法論

設定隨機向量 X 假設分布、抽 m 樣本得 empirical 對應；對兩版本比較 Kelly 押注大小，並把樣本數 m 當分析變數。

## 目前限制與注意事項

- 「太保守」結論依賴 unbounded support 假設。
- Empirical Kelly 在小樣本下變異大，論文需配合 sample size 條件討論。

## 研究價值與啟示

### 關鍵洞察

1. **「太激進 vs 太保守」雙向都對**：不同假設下兩種結論都會出現 ── 本篇等於告訴你「**沒分清楚假設前不要套 Kelly**」。實務上分布肥尾且 unbounded（如選擇權收益），這時純理論 Kelly 會給「不押」 ── 但實證告訴你應該押。
2. **Restricted Betting Theorem 是反直覺結論**：定理告訴你「即使期望為正、有正機率獲利，Kelly 也可能告訴你不要押」── 因為極端負尾把 expected log 拉到負無窮。
3. **這種「打臉自己領域」的論文難得**：作者敢正面挑戰 Kelly 主流，反映 control theory 學派看金融的獨立角度。
4. **與作者其他 Kelly 系列形成內部辯證**：Limitations（2015）→ Conservative（2016）→ Approximation（2020）→ Too Aggressive 文獻 ── 整條線是 Kelly 的多角度檢驗。

### 與其他研究筆記的關聯

- **[On Kelly Betting: Some Limitations](kelly-betting-limitations.md)** ── 前一年同團隊論文。
- **[Feedback Control in Kelly Betting Approximation](feedback-control-kelly-betting-approximation.md)** ── 給出可解閉式近似的後續論文。
