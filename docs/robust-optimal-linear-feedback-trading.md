---
date: "2026-05-07"
category: "量化交易"
card_icon: "material-source-branch"
oneliner: "Hsieh 2022 / 2025 修訂：DLP 結構派的源頭論文，把 semi-infinite constraints 化成 balanced / complementary 兩種結構策略，廣義化 mean-variance 並提供圖形求解法"
tags:
  - quant
  - control-theory
  - portfolio-optimization
---

# From Semi-Infinite Constraints to Structured Robust Policies: Optimal Gain Selection for Financial Systems

## 資料來源

| 項目 | 連結 |
|------|------|
| arXiv | <https://arxiv.org/abs/2202.02300> |
| 投稿狀態 | Submitted（2022 首版、2025 大改） |

## 論文基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Chung-Han Hsieh（單作者） |
| **首版** | 2022-02-04 |
| **大改** | 2025-01-17 |

## 一句話摘要

把 robust optimal **gain selection**（DLP 系列權重設定問題）的 semi-infinite constraints 化成兩種結構化策略 ── **balanced** 與 **complementary** ── 並設計圖形求解法降低計算量；廣義化 mean-variance 並引入 robustness。

## 核心貢獻

1. **Semi-infinite → 兩類結構策略**：把無窮維約束問題降為 balanced / complementary 兩種顯式 policy。
2. **圖形解法**：用幾何方法降低計算量。
3. **MV 廣義化**：把 mean-variance 框架擴張為 robust 版本。

## 方法論

- DLP 框架做資金配置
- Robust optimization 用 bounded uncertainty set 描述報酬參數
- Constraint transformation 取得顯式最優解

## 目前限制與注意事項

- Bounded uncertainty set 假設不一定貼合肥尾市場。
- Balanced / complementary 兩類策略名稱在後續論文（CDC 2023）才完整實證化。
- 仍是 submitted 階段。

## 研究價值與啟示

### 關鍵洞察

1. **這是 DLP 整條結構派的「設計起點」**：「balanced / complementary」這兩個名詞被作者後續論文反覆引用，本篇等於是**整個 DLP 設計語彙的字典**。
2. **Semi-infinite optimization 在 finance 不常見**：semi-infinite 來自 control / optimization 經典文獻（連續性 robust constraints），把它搬到財務交易系統是技術橋接。
3. **圖形解法是 reviewer-friendly**：許多 optimization 論文求解過程是黑盒，本篇用圖形說明，論文可讀性 / 引用率都會提高。
4. **MV 廣義化是學術話術但實質有限**：「廣義化 mean-variance」常被當賣點，但實務上 MV 早已不是主流配置工具，廣義化的引用價值更多在 OR / control 社群而非投資實務。

### 與其他研究筆記的關聯

- **[DLP with Time-Varying Weights](dlp-time-varying-weights.md)** / **[DLP with Transaction Costs](dlp-with-transaction-costs.md)** / **[Robust Trading in Lattice Market](robust-trading-lattice-market.md)** ── 都站在本篇的 balanced / complementary 結構上延伸。
