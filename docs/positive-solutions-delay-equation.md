---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-account-cash"
oneliner: "Hsieh × Barmish × Gubner 2020 IEEE TAC：把交易者帳戶價值寫成離散時間含延遲線性方程，找出 feedback gain α₋/α₊ 兩個門檻分別保證「永不破產」與「必破產」"
tags:
  - quant
  - control-theory
---

# On Positive Solutions of a Delay Equation Arising When Trading in Financial Markets

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/1901.02480> |
| 期刊 | IEEE Transactions on Automatic Control, vol. 65, no. 7, pp. 3143–3149（2020） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh、B. Ross Barmish、John A. Gubner |
| **首版** | 2019-01-08 |
| **修訂** | 2019-10-16 |

## 一句話摘要

把交易者帳戶價值寫成 **離散時間、線性、含延遲的狀態方程**，分析其正解條件 ── 對 feedback gain 找到兩個門檻 **α₋** 與 **α₊**：低於 α₋ 時所有報酬序列都不會破產；高於 α₊ 時某些序列必破產；中間區間則提出 conjecture。

## 核心貢獻

1. **帳戶價值 delay equation 模型**：把 trader account 寫成標準 control 形式，可動用整套 delay system 工具。
2. **α₋ / α₊ 兩個 robust 門檻**：給出 feedback gain 的安全 / 危險區間。
3. **Indefinite continuability**：找出讓帳戶價值永恆為正的條件。
4. **Conjecture for intermediate range**：提出中間區間的猜想，邀請後續研究。

## 方法論

離散時間線性方程 + 延遲建模 + 數學分析 + 計算實驗。

## 目前限制與注意事項

- 線性帳戶模型限制（無交易成本、無凸 / 凹 utility）。
- Conjecture 仍未證。

## 研究價值與啟示

### 關鍵洞察

1. **「破產 / 不破產」翻譯成 delay equation 正解問題**是聰明的問題重塑。把行為金融問題（誰會破產）放回控制論的成熟工具，立刻有 Lyapunov、stability、positivity 等可用。
2. **TAC 期刊位置反映重要性**：IEEE Transactions on Automatic Control 是控制論頂刊，本篇 = 控制社群對「financial market 是 control problem」的正式背書。
3. **α₋ < α₊ 的 gap 啟發後續研究**：兩個門檻之間的「無人區」是研究機會 ── 後續 DLP 系列、drawdown 系列都在這條 gap 裡找答案。
4. **延遲建模呼應 1907.08771（execution delay）**：同一作者群把延遲思維貫穿到帳戶模型 + 交易頻率兩個層級。

### 與其他研究筆記的關聯

- **[Affine Feedback Stop-Loss](affine-feedback-stop-loss.md)** ── 從 affine feedback 角度處理同主題的姊妹篇。
- **[Execution Delay on Kelly Trading](execution-delay-kelly-trading.md)** ── 延遲建模思維的 Kelly 版本。
