---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-puzzle"
oneliner: "Li × Hsieh 2023：把 dynamic Black-Litterman + 因子模型 + Elastic Net + 動態 sliding window 整合成一個 adaptive portfolio 框架，S&P 500 前 100 大十年實證含 turnover 成本仍有效"
---

# On Unified Adaptive Portfolio Management

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2307.03391> |
| 投稿狀態 | Submitted（2023-07 首版、2024-04 大改） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chi-Lin Li、Chung-Han Hsieh |
| **首版** | 2023-07-07 |
| **資料** | S&P 500 前 100 大十年資料 |

## 一句話摘要

把 **dynamic Black-Litterman** + **general factor model** + **Elastic Net regression** + **動態 sliding window** 四個工具整合成統一的 adaptive portfolio 框架，系統性產生投資人觀點並降低估計誤差；S&P 500 前 100 大十年實證含 turnover 成本仍有 promising 績效。

## 核心貢獻

1. **四工具整合**：dynamic BL + factor model + Elastic Net + dynamic sliding window 一站式整合。
2. **動態視窗演算法**：依市場波動率調整視窗長度。
3. **系統性 view 生成**：取代 BL 中 subjective view 的人工輸入。

## 方法論

| 模組 | 角色 |
|------|------|
| Dynamic Black-Litterman | 主框架，整合先驗 + 觀點 |
| General factor model | 報酬建模 |
| Elastic Net regression | 因子估計，控過擬合 |
| Mean-variance optimization | 求最佳權重 |
| Dynamic sliding window | 動態調整視窗以反映市場波動 |

## 目前限制與注意事項

- 模組組合多，整體系統複雜度高，對中小型機構落地門檻不低。
- 各模組超參數需聯合調整。
- BL 需 tau、Omega 等參數設定。

## 研究價值與啟示

### 關鍵洞察

1. **「整合派」vs「結構派」是 Hsieh 的兩條學術線**：本篇代表「整合派」── 把現成工具兜起來解問題；其他 DLP / drawdown 路線是「結構派」── 從理論性質推策略。**整合派論文更快發表，結構派論文更深**。
2. **Black-Litterman 自動 view 生成是長期 open problem**：BL 一直被詬病「主觀 view 從哪來」，本篇用 factor model 系統化生成 ── 雖不是首創但配組合很好。
3. **Dynamic sliding window 與 frequency 系列呼應**：作者把 sliding window 概念從 log-optimal 移植到 BL，等於是把 Section 1 的「再平衡頻率」思維換體現在 BL 上。
4. **Turnover transaction cost 顯式處理**：實務派最在意，本篇沒迴避。
5. **十年 + S&P 500 前 100 大** 是實證強度：很多 paper 只用 30 檔 5 年，本篇規模比較有說服力。

### 與其他研究筆記的關聯

- **[Sliding Window Log-Optimal Portfolio](sliding-window-log-optimal-portfolio.md)** ── 同 sliding window 思維的 log-optimal 版本。
- **[Robust Trading in Lattice Market](robust-trading-lattice-market.md)** ── DLP 結構派代表作。
