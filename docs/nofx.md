---
date: ""
category: "量化交易"
icon: "material-robot-excited"
oneliner: "Go 撰寫的全自主 AI 交易助理，x402 USDC 微支付取代 API key，連接 9 個交易所執行真實訂單"
---
# NOFX 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [NoFxAiOS/nofx](https://github.com/NoFxAiOS/nofx) |
| 官網 | [nofxai.com](https://nofxai.com) |
| x402 協議官網 | [x402.org](https://www.x402.org/) |
| Coinbase x402 文件 | [docs.cdp.coinbase.com/x402](https://docs.cdp.coinbase.com/x402/welcome) |
| Claw402 AI Gateway | [claw402.ai](https://claw402.ai/) |
| SlowMist 安全漏洞分析 | [Medium - NOFX AI Automated Trading Vulnerability](https://slowmist.medium.com/threat-intelligence-analysis-of-the-nofx-ai-automated-trading-vulnerability-e4f4664ad1e6) |
| 股權糾紛報導 | [Phemex News](https://phemex.com/news/article/nofx-ai-trading-system-faces-equity-and-opensource-dispute-47300) |
| CoinDesk x402 採用現況 | [Coinbase-backed AI payments protocol](https://www.coindesk.com/markets/2026/03/11/coinbase-backed-ai-payments-protocol-wants-to-fix-micropayment-but-demand-is-just-not-there-yet) |

## 專案概述

**NOFX** 是一個開源的全自主 AI 交易助理，以 Go 撰寫後端、React + TypeScript 建構前端。核心主張是「Any market. Any model. Pay with USDC, not API keys」——AI 自行決定要呼叫哪個 LLM、抓哪些市場資料、何時下單，使用者只需設定策略並存入 USDC 錢包。

截至 2026-03-29，擁有 **11,356 stars、2,867 forks**，創立於 2025-10-28，成長相當快速。

與 ai-hedge-fund 的「純模擬」不同，NOFX **實際連接交易所並執行真實訂單**，支援 Binance、Bybit、OKX、Hyperliquid 等 9 個交易所（含 3 個 Perp-DEX）。官方雖加了風險警告，但這是一個真實可交易的自動化系統。

## 核心功能

### 系統架構

```
┌──────────────────────────────────────────┐
│          Web Dashboard                    │
│   React + TypeScript + TradingView        │
├──────────────────────────────────────────┤
│            API Server (Go)                │
├─────────────┬──────────────────────────┤
│  Strategy   │      Telegram Agent        │
│  Engine     │   (chat / tool calling)    │
├─────────────┴──────────────────────────┤
│          MCP AI Client Layer              │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │  API Key 模式  │  │   x402 模式       │ │
│  │ DeepSeek/GPT │  │  Claw402 Gateway  │ │
│  │ Claude/Gemini│  │  USDC 按次付費    │ │
│  └──────────────┘  └──────────────────┘ │
├──────────────────────────────────────────┤
│          Exchange Connectors              │
│  Binance · Bybit · OKX · Bitget · KuCoin │
│  Gate · Hyperliquid · Aster DEX · Lighter │
└──────────────────────────────────────────┘
```

### 主要功能模組

| 模組 | 說明 |
|------|------|
| **Strategy Studio** | 視覺化策略建構器，設定選股條件、技術指標、風控參數 |
| **AI Competition** | 多個 AI model 同時競跑，排行榜即時追蹤績效 |
| **Telegram Agent** | 以聊天方式操控 AI trader，支援 streaming 與 tool calling |
| **Dashboard** | 即時部位、P/L、AI Chain of Thought 決策日誌 |
| **Backtester** | 歷史回測引擎（依賴 TA-Lib） |

### x402 支付模式：核心差異化設計

傳統 LLM API 流程：
```
註冊帳號 → 購買額度 → 取得 API key → 管理配額 → 定期輪換 key
```

x402 流程：
```
Request → 402 (這個請求需要 X USDC) → 錢包簽名 → retry → 完成
```

**錢包即身份**——不需要帳號、不需要 API key、不需要預付額度。每次請求按實際用量從 USDC 錢包扣除，由 [Claw402](https://claw402.ai) 路由到 15+ 個 LLM 模型。

### 支援的 AI 模型

| 模式 | 可用模型 |
|------|---------|
| API Key 模式 | DeepSeek、Qwen、GPT、Claude、Gemini、Grok、Kimi |
| x402 模式（Claw402） | 15+ 模型，按 USDC 按次付費 |

## 快速開始

```bash
# Linux / macOS（一行安裝）
curl -fsSL https://raw.githubusercontent.com/NoFxAiOS/nofx/main/install.sh | bash
# 開啟 http://127.0.0.1:3000

# Docker
curl -O https://raw.githubusercontent.com/NoFxAiOS/nofx/main/docker-compose.prod.yml
docker compose -f docker-compose.prod.yml up -d

# 從原始碼編譯（需要 Go 1.21+、Node.js 18+、TA-Lib）
git clone https://github.com/NoFxAiOS/nofx.git && cd nofx
go build -o nofx && ./nofx
cd web && npm install && npm run dev
```

設定流程：AI（API key 或 x402 錢包）→ 交易所 → 策略 → Trader 組合 → 啟動交易。

## 目前限制 / 注意事項

| 類別 | 風險 |
|------|------|
| **安全漏洞（已知）** | SlowMist 發現預設開啟 admin mode 會暴露 API key 與私鑰（commit 517d0caf 之前的版本） |
| **創辦人糾紛** | 開發者之間爆發股權糾紛（50% 股份 + 500,000 USDT 索求），影響專案可信度 |
| **x402 採用率低** | Coinbase 的 x402 協議每日實際交易量僅 ~$28,000，大量為測試交易 |
| **AGPL-3.0** | 若用於商業衍生產品，須開放源碼 |
| **真實金融風險** | 不像 ai-hedge-fund 純模擬，本系統會執行真實下單，虧損即真實虧損 |
| **TA-Lib 依賴** | 從原始碼編譯需要系統安裝 TA-Lib，增加環境複雜度 |

## 研究價值與啟示

### 關鍵洞察

**1. MCP 被用在 AI Model 路由層，而非只是工具呼叫**
NOFX 架構圖顯示有一層「MCP AI Client Layer」——他們把 MCP（Model Context Protocol）用來統一抽象不同 LLM provider 的介面。這是一個值得關注的設計：MCP 不只是讓 AI 呼叫外部工具，也可以讓系統在執行時動態切換不同的 AI model 提供者。這個模式可以直接借鑑到 fluffy-agent-core 的 provider 抽象層設計。

**2. x402 是「Agent 原生支付」的第一個可運行方案**
x402 由 Coinbase 於 2025 年 5 月推出，用 HTTP 402 狀態碼實現 USDC 微支付。理念是讓 AI Agent 能自主付款取得資源，不需要人類介入處理 API key。這解決了一個真實問題：當你有 100 個 Agent 同時運行，管理 100 組 API key 是噩夢。但現實是 x402 每日交易量仍只有 ~$28K，距離真正普及還很遠。

**3. 「AI Competition」模式是差異化設計**
讓多個 AI model 同時用相同策略競跑，排行榜追蹤績效——這不只是工程 feature，更是產品思維：讓使用者可以「對比不同 AI 的決策品質」，而不是盲目相信單一模型。這個概念可以應用到任何 AI 決策系統的評估框架。

**4. 開源貢獻者空投計畫是新型激勵模型**
NOFX 承諾當平台產生收益時，所有 contributor 會收到空投，並按貢獻類型給予不同權重（Pinned Issue PR ★★★★★★ > 一般 PR ★★★★★）。這是 DeFi 與開源協作的混合激勵模型，比傳統的名譽制或 bounty 制更有長期綁定效果——但前提是平台確實產生收益，且團隊不陷入股權糾紛。

**5. 安全事件暴露「自動交易 + 開源」的信任危機**
SlowMist 的漏洞報告指出 admin mode 預設開啟會暴露私鑰，加上創辦人股權糾紛——對於一個直接操作真實資金的工具，這類事件的殺傷力遠大於純工具類專案。**任何連接真實錢包的 AI 自動化工具，安全審計應列最高優先級。**

### 與其他專案的關聯

- **AI Hedge Fund**（本站已有筆記）：純教育模擬 vs. NOFX 真實交易，前者適合學習 multi-agent 設計，後者有真實財務風險
- **TradingAgents**（本站已有筆記）：學術研究框架，不執行真實交易；NOFX 是面向個人用戶的生產工具
- **OpenClaw Claude Proxy**（本站已有筆記）：ClawRouter / Claw402 與 OpenClaw 概念相似，都在做 LLM 請求的路由與代理層，值得對比架構設計
