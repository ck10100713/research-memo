---
date: "2026-04-15"
category: "量化交易"
card_icon: "material-robot-outline"
oneliner: "港大 AI 交易 Benchmark + Agent-Native 社交交易平台 — 真實市場、MCP 工具鏈、多 Agent 協作"
---

# AI-Trader 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [HKUDS/AI-Trader](https://github.com/HKUDS/AI-Trader) |
| 官網 | [ai4trade.ai](https://ai4trade.ai) |
| 論文 | [arXiv:2512.10971](https://arxiv.org/abs/2512.10971) |
| Portfolio 分析 | [hkuds.github.io/AI-Trader/portfolio.html](https://hkuds.github.io/AI-Trader/portfolio.html) |

**團隊：** HKUDS — Data Intelligence Lab @ 香港大學（PI: Chao Huang）

**專案狀態：** ⭐ 13.3K+ stars · Python · 2025-10 創建 · 活躍開發中

## 專案概述

AI-Trader 經歷兩個階段：

**v1（2025 底）— 研究 Benchmark：** 第一個完全自動化、即時、無數據污染的 LLM Agent 金融交易評測基準。Agent 被投入真實市場，需自主搜尋資訊、分析數據、執行交易。

**v2（2026-03）— Agent-Native Trading Platform：** 從學術 benchmark 轉型為社交交易平台。核心理念：「人類有自己的交易平台，AI Agent 也需要自己的。」任何 Agent 讀取一份 `SKILL.md` 即可在數秒內加入。

## 核心架構

```
AI-Trader Platform
├── skills/              # SKILL.md — Agent 自助加入
│   ├── ai4trade/        # 主技能
│   ├── copytrade/       # 跟單交易
│   └── tradesync/       # 交易同步
├── service/
│   ├── server/          # FastAPI 後端
│   └── frontend/        # React/Vite 前端
└── MCP Toolchain        # Agent 透過 MCP function call 交易
```

### Minimal Information Paradigm（核心創新）

- Agent 僅獲得**最少必要上下文**（股票代碼、初始資金）
- 必須**自主搜尋、驗證、綜合**即時市場資訊
- 無歷史數據預載、無提示注入、無人工干預

### 多市場覆蓋

| 市場 | 特性 |
|------|------|
| 美股 | 高流動性 |
| A 股 | 政策驅動型 |
| 加密貨幣 | 高波動性 |
| Polymarket | 預測市場（模擬執行 + 自動結算） |

## 論文關鍵發現

1. **通用智慧 ≠ 交易能力** — LLM 推理能力無法自動轉化為有效交易
2. **風險控制決定跨市場穩健性** — 不是報酬率，而是風控能力決定穩定性
3. **多數 Agent 難以打敗 Buy-and-Hold** — 簡單的買入持有仍是強基線
4. **高流動性市場更適合 AI** — 美股/加密比 A 股（政策驅動）更容易取得超額報酬
5. **集體智慧有潛力** — 多 Agent 即時辯論策略展現獨特的協作模式

## 目前限制 / 注意事項

- **License 不明確** — Badge 顯示 MIT 但 API 回傳 null
- **模擬 vs 真實交易** — Polymarket 使用模擬執行，非全部真金白銀
- **多數 LLM 表現不佳** — 論文自承大部分 Agent 難以打敗 buy-and-hold
- **數據不可重現** — 即時市場 benchmark，不同時期結果差異大
- **商業化元素** — v2 有積分激勵、跟單等，研究中立性可能受影響
- **Agent 安全性** — 允許任何 Agent 註冊交易，惡意 Agent 防範機制未見說明

## 研究價值與啟示

### 關鍵洞察

1. **「LLM 做交易不如 buy-and-hold」是最重要的誠實結論。** 多數 AI 交易專案宣傳勝率，AI-Trader 卻坦承「大部分 Agent 難以打敗簡單基線」——這種學術誠實比漂亮的回測數字更有參考價值。

2. **從 Benchmark 到 Platform 的轉型值得關注。** 學術 benchmark → 社交交易平台的路徑，本質上是從「評估能力」到「應用能力」的跨越。SKILL.md 讓任何 Agent 自助加入的設計，降低了 Agent 參與金融市場的門檻。

3. **MCP 作為交易工具鏈的標準介面。** AI-Trader 用 MCP 讓 Agent 透過結構化 function call 執行交易，將「推理」與「行動」乾淨分離。這與 MCP Toolbox for Databases 的理念一致——MCP 正在成為 Agent 存取外部系統的通用介面。

### 與其他專案的關聯

- **vs Kronos：** Kronos 做「價格預測」（基礎模型層），AI-Trader 做「自主交易」（Agent 應用層）。兩者可組合——用 Kronos 的預測信號作為 AI-Trader Agent 的輸入。
- **vs AI Hedge Fund / TradingAgents：** AI-Trader 的學術背景和 benchmark 設計更嚴謹，但商業化程度不如 AI Hedge Fund 的模擬框架。
- **vs OpenStock / StockStats：** 傳統量化工具提供數據和指標，AI-Trader 提供「Agent 自主決策」的框架——層級不同。
