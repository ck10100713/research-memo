---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-dice-multiple"
oneliner: "Hsieh × Barmish × Gubner 2018 ACC：Bernoulli 押注場景下，零成本時最優 ELG 對下注間隔 n 為非遞增、提出 sufficient attractiveness inequality 作為低頻匹配高頻的條件"
tags:
  - quant
  - kelly
---

# At What Frequency Should the Kelly Bettor Bet?

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1801.06737> |
| 會議 | American Control Conference (ACC) 2018, Milwaukee, pp. 5485–5490 |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish、John A. Gubner |
| **首版** | 2018-01-20 |
| **修訂** | 2018-08-21 |

## 一句話摘要

回答「Kelly 賭徒應該多頻繁下注？」── 在 Bernoulli 報酬（±1）場景下，**最優 ELG 對下注間隔 n 為非遞增**（無成本時頻率越高越好），並提出 **sufficient attractiveness inequality** 作為「低頻是否能匹配高頻」的充分（也接近必要）條件。

## 核心貢獻

1. **Bernoulli 報酬全分析**：完整刻畫 -1/+1 報酬下的最優頻率行為。
2. **兩個 conjecture**：
   - 最優績效隨頻率下降而下降
   - 「Sufficient attractiveness inequality」條件下低頻可匹配高頻
3. **零成本下 g_n* 對 n 為非遞增**：給出嚴格證明。

## 方法論

動態 game 框架：賭徒每 n 步更新部位，用 Kelly ELG 評比；理論分析 + 多種機率分布測試。

## 目前限制與注意事項

- Bernoulli 報酬假設窄。
- Conjecture 仍是猜想，後續論文（如 1907.08771 加入延遲）部分回應。
- 純理論，無實證資料。

## 研究價值與啟示

### 關鍵洞察

1. **「無成本時越高頻越好」是 Kelly betting 的直覺結論**：本篇給出嚴格證明，後續延遲 / 成本論文則處理「為什麼實務上不能無腦高頻」。
2. **Sufficient attractiveness inequality 是有趣的條件名稱**：把「市場 attractiveness」量化成不等式，可以拿來判斷某個賭局值不值得加倍下注。
3. **這篇是整條 frequency / delay 路線的源頭**：作者 2018 → 2019（延遲）→ 2020 → 2021 → 2023（含成本）一路發展，本篇是底層。
4. **ACC 場合定位**：ACC 比 CDC 更應用導向，本篇用 betting 包裝吸引控制社群。

### 與其他研究筆記的關聯

- **[Rebalancing Frequency for Kelly Portfolios](rebalancing-frequency-kelly-portfolios.md)** ── 本篇從單押注推到多資產的 CDC 後作。
- **[Execution Delay on Kelly Trading](execution-delay-kelly-trading.md)** ── 加入延遲後的翻轉論文。
- **[Kelly Betting Can Be Too Conservative](kelly-betting-too-conservative.md)** ── 同 Kelly betting 論述線。
