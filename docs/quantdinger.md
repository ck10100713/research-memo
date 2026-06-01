---
date: "2026-05-19"
category: "量化交易"
card_icon: "material-server-network"
oneliner: "brokermr810 自架式 AI 量化交易作業系統，一個 Docker Compose 串聯 AI 研究/Python 策略/回測/實盤(crypto+IBKR+MT5+Alpaca)，Agent Gateway + MCP，內建 USDT 計費可變 SaaS"
tags:
  - quant
---

# QuantDinger 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（後端） | <https://github.com/brokermr810/QuantDinger> |
| 前端 repo | <https://github.com/brokermr810/QuantDinger-Vue> |
| 行動 app repo | <https://github.com/brokermr810/QuantDinger-Mobile> |
| 官方網站 | <https://www.quantdinger.com> |
| SaaS | <https://ai.quantdinger.com> |
| AWS Marketplace AMI | <https://aws.amazon.com/marketplace/pp/prodview-naanrb7d2mbc6>（ThinkCloud CentOS 9） |
| MCP server (PyPI) | <https://pypi.org/project/quantdinger-mcp/> |
| Telegram / Discord / YouTube | quantdinger / tyx5B6TChr / @quantdinger |
| 規模 | 5,858 stars / 1,278 forks / Apache 2.0 / 創建 2025-12-28（約 5 個月） |
| 版本 | v3.0.10 |
| 語言 / 部署 | Python 3.10+（Docker 3.12）+ Vue 前端 + Docker Compose + Postgres + Redis |
| 多語 README | EN / 簡中 / 日 / 韓 / 泰 / 越 / 阿拉伯（7 語） |

## 概述

**QuantDinger** 的 slogan：「**Your Private AI Quant Operating System**」。定位很明確——**自架式、本機優先的 AI 量化交易完整作業系統**。「OS」這個詞用得不誇張，因為它整合了：

```text
AI 研究（多 LLM 分析、機會雷達、watchlist）
   +
Python 原生策略撰寫（IndicatorStrategy + ScriptStrategy）
   +
伺服器端回測 + 績效指標 + 策略快照
   +
實盤交易（crypto、IBKR、MT5、Alpaca）
   +
通知（Telegram、Email、SMS、Discord、Webhooks）
   +
多使用者 + 角色 + Credits + USDT 計費（**可選的 operator primitive**）
```

→ **一個 Docker Compose 把這整套跑起來、用你自己的 API key、跑在你自己的機器**——而非把分散在 ChatGPT + TradingView + Notion + 各種 bot 的工作流拼湊起來。

特別值得注意的是 **operator 模式**：repo 內建 multi-user / credits / USDT 計費——意味著**你可以拿這個 repo 當基底自己開一個量化 SaaS**，不只是個人工具。

## 三 repo 架構

| Repo | 內容 |
|------|------|
| **QuantDinger** | Flask 後端 + Docker Compose stack + 文件 |
| **QuantDinger-Vue** | Vue 前端原始碼（tag `v*` 會自動發 `ghcr.io/brokermr810/quantdinger-frontend` 映像） |
| **QuantDinger-Mobile** | 開源行動 client，可配自架後端或 SaaS |

→ **前後端拆 repo 是個聰明的解耦**——一般使用者只 pull 前端 image，**不用裝 Node.js**。只有要改 UI 的人才碰前端 repo。

## 兩種策略寫法

| 類型 | 風格 | 適用 |
|------|------|------|
| **IndicatorStrategy** | DataFrame 訊號（向量化），含 chart overlay | 技術指標 / 因子型 / 適合畫圖 |
| **ScriptStrategy** | Event-driven（`on_bar` callback + 明確下單） | 多狀態 / 複雜訂單管理 / 需要 tick-level 控制 |

→ 一個 platform 同時支援**向量化思路**跟**事件驅動思路**是聰明的——對應到主流量化框架（zipline / backtrader 是事件驅動、vectorbt / bt 是向量化），讓兩派使用者都能上手。

## 交易管道

| 通道 | 標的 |
|------|------|
| Crypto Exchange（直連） | 各大 CEX |
| **IBKR**（Interactive Brokers） | 全球股票 / ETF / 期貨 / 外匯 |
| **MT5**（MetaTrader 5） | 主要外匯 + 部分券商 |
| **Alpaca** | 美股 / ETF / Crypto |

→ 對台灣使用者，**IBKR 是最相關通道**（永豐 / 元大要自寫 adapter）；**MT5 對外匯交易者特別實用**。

## Agent Gateway + MCP（最有意思的設計）

### `/api/agent/v1` Agent Gateway

QuantDinger 內建一個 **Agent Gateway**，把整個平台暴露給 AI agent 用，**但完全不暴露你的 exchange key 或 admin JWT**：

```text
Cursor / Claude Code / Codex
      │ MCP
      ▼
quantdinger-mcp (PyPI)
      │ HTTP + Agent Token
      ▼
/api/agent/v1 (QuantDinger Agent Gateway)
      │
      ▼
讀市場 / 管理策略 / 跑回測 / 下單（paper only 預設）
```

**兩道安全閘**：

| 閘 | 預設 |
|---|------|
| Token 層 | `paper_only=true`（**只能紙上交易**） |
| Server 層 | `AGENT_LIVE_TRADING_ENABLED=false` |

→ **必須兩個 flag 同時開才能讓 AI agent 下實盤**。**所有 agent call 都會被 audit-log**。這是少見的「**對 AI 給予具備風險能力但預設關閉**」工程紀律。

### MCP client 設定

```json
{
  "mcpServers": {
    "quantdinger": {
      "command": "uvx",
      "args": ["quantdinger-mcp"],
      "env": {
        "QUANTDINGER_BASE_URL": "http://localhost:8888",
        "QUANTDINGER_AGENT_TOKEN": "qd_agent_xxxxxxxx"
      }
    }
  }
}
```

→ 用 `uvx` 跑 `quantdinger-mcp` PyPI 包，**Cursor / Claude Code / Codex 同一份 config**，唯一差異是 BASE_URL（SaaS vs 自架）。**這個跨環境一致性的設計是 production 級 MCP 整合的標準姿勢**。

## 兩條安裝路徑

### 1. 最輕（兩個檔案、不 clone）

```bash
curl -O https://raw.githubusercontent.com/brokermr810/QuantDinger/main/docker-compose.ghcr.yml
curl -o backend.env https://raw.githubusercontent.com/brokermr810/QuantDinger/main/backend_api_python/env.example
docker compose -f docker-compose.ghcr.yml pull
docker compose -f docker-compose.ghcr.yml up -d
```

`SECRET_KEY` 首次啟動自動產生。Open `http://localhost:8888`、登 `quantdinger / 123456`、**立刻改密碼**。

### 2. 標準（git clone）

```bash
git clone https://github.com/brokermr810/QuantDinger.git && cd QuantDinger \
  && cp backend_api_python/env.example backend_api_python/.env \
  && chmod +x scripts/generate-secret-key.sh && ./scripts/generate-secret-key.sh \
  && docker compose pull && docker compose up -d
```

**重要**：**不要用 `docker compose up --build`**——`--build` 會試圖在當前 repo build 前端，而前端在另一個 repo。預設 pull GHCR image 即可。

### AWS Marketplace AMI

對企業客戶：**AWS Marketplace 有預建好的 AMI（ThinkCloud CentOS 9）**，一鍵啟動，不用自己跑 Docker。對「想 PoC 但不想配環境」是極友善的入口。

## 系統架構圖（README 提供）

```text
Trader / Operator / Researcher
        │
        ▼
[Frontend]  Vue Web App  →  Nginx Delivery
                                  │
                                  ▼
[Application]  Flask API Gateway
                ├─ AI Analysis Services
                ├─ Strategy & Backtest Engine
                ├─ Execution & Quick Trade
                └─ Billing & Membership
                              │
                              ▼
[State]  PostgreSQL 16  +  Redis 7  +  Logs/Runtime
                              │
                              ▼
[External]
    LLM Providers
    Crypto Exchanges  ↔  IBKR / MT5 / Alpaca
    Market Data / News
    TronGrid / USDT Payment
    Telegram / Email / SMS / Webhook
```

**Crypto 市場資料管道跟下單管道是分離的**——這個架構決策跟所有 production-grade 交易系統一致，**failure isolation 必要**。

## 7 個語言 i18n（少見的覆蓋面）

EN / 簡中 / 日 / 韓 / 泰 / 越 / 阿拉伯——**涵蓋亞洲 + 中東**，但**沒繁中、沒西語**。這個語言組合反映目標市場——**東南亞 + 中東 + 中日韓 retail quant**，避開歐美 / 拉美主場（那些有 Bloomberg、QuantConnect、Alpaca SaaS 等大廠卡位）。

## 目前限制與注意事項

- **License Apache 2.0 但 TRADEMARKS.md 限制商標使用**：fork 改名做白牌 SaaS 沒問題，但**不能用 "QuantDinger" 名稱繼續發**。
- **預設密碼 `quantdinger/123456`**：首次登入務必改——很多人會忘，**部署上網前必改**。
- **沒繁中 README**：對台灣使用者要看英文或簡中。
- **「Operator-ready」雙刃**：內建 credits / USDT billing 讓你能變 SaaS，但**也意味著 codebase 比純個人工具複雜很多**。個人使用者可能用不到的功能會增加維護負擔。
- **AI agent 加入 live trading 必須兩道 flag 同開**：保護機制好，**但意味著從零開始用 MCP 做實盤需要明確意識**——不是預設能跑的，要主動啟用。
- **5.8k stars / 5 個月 / 1.3k forks**：成長速度快、社群驗證度中等，**但仍是相對年輕的專案**。production 用實盤要慎重。
- **CN 使用者拉 Docker image 可能慢**：repo 提供 `IMAGE_PREFIX=docker.m.daocloud.io/library/` 鏡像替代——表示作者考慮了 GFW 場景。
- **強相依 Docker**：不像 [[fincept-terminal]] 走 native binary、不像 [[daily-stock-analysis]] 走 GitHub Actions——QuantDinger 走「Docker Compose 一套 stack」路線，**對 Docker 不熟的使用者門檻較高**。
- **「AI 分析」≠「AI 決策」**：跟 [[daily-stock-analysis]] 一樣，AI agent 出的建議是輔助分析，**不是回測過的策略訊號**，跟單風險高。

## 研究價值與啟示

### 關鍵洞察

1. **「Self-hosted Quant OS」是個被低估的賽道**：QuantConnect / TradingView 是雲端 SaaS、Bloomberg 是企業桌面、[[fincept-terminal]] 是個人桌面、[[daily-stock-analysis]] 是 cron job——**「自架完整 stack、可變白牌 SaaS」這個生態位之前少有強參與者**。QuantDinger 5 個月 5.8k stars 證明這個空缺真實存在。
2. **`paper_only=true` + 雙 flag 才能 live trade 是「對 AI 給力但預設關掉」的範式**：對比 ChatGPT plugin 開放後不少人讓 AI 直接下單翻車，QuantDinger 的設計可以當作「**AI 工具該如何給予危險權限**」的標竿。對應到 [[zeuikli-claude-code-best-practices]] 第 7.2 章「Permission 系統 deny → ask → allow」原則完全一致。
3. **「Agent Gateway」是把 AI agent 變成 API client 的範式**：不直接給 admin JWT、發專用 agent token、加 audit log、加 rate limit、限制 scope——**是 production 級「Agent as API consumer」的標準姿勢**。任何把 AI agent 接進既有系統的人都該抄這個 pattern。
4. **「operator primitive」是個體開發者用 OSS 變現的新路徑**：repo 內建 multi-user + credits + USDT 計費——**意味著作者鼓勵你拿這個 repo 開自己的 SaaS、不需要從零實作付費系統**。這個策略 vs 純 OSS 策略形成有趣對比——**「給工具」+「給做生意的腳手架」**是更完整的 OSS 變現觀。
5. **MCP server 走 PyPI 而非自架**：`quantdinger-mcp` 上 PyPI 用 `uvx` 跑——**對 Claude Code / Cursor 使用者來說零摩擦**。對比 [[cli-anything]] 的 CLI-Hub 自架 registry，QuantDinger 直接用 PyPI 作為發布通路是更輕量的設計。
6. **多 LLM 分析 + 多通道執行 + 多語言 i18n** 三個「多」是 SaaS 量化平台的基本盤：對應 [[daily-stock-analysis]] 也走多 provider 路線——**「不綁定單一 vendor」已是 2026 量化開源工具的 hard requirement**。
7. **AWS Marketplace AMI 揭示開源 + 企業通路雙軌策略**：對 retail 走 GitHub OSS + Docker self-host、對企業走 AWS Marketplace ThinkCloud AMI。**這條雙軌變現路線**對任何想做嚴肅 OSS 商業化的個人 dev 是個值得抄的範本。
8. **「Crypto 市場資料管道 vs 下單管道分離」**是個關鍵架構決策：失敗隔離（market data 中斷不該影響下單）、安全（市場資料公開、下單需 key），任何 production 交易系統都該如此。

### 與其他研究的關聯

- 與 [[fincept-terminal]]：兩者都是「Bloomberg Terminal 的開源版」野心——**Fincept 走 native C++/Qt 桌面 app**，QuantDinger 走 **Docker Compose 自架 stack + Web UI**。**桌面 vs Web stack 的兩極對照**。
- 與 [[daily-stock-analysis]]：兩者都是 LLM 驅動量化——**DSA 走 GitHub Actions 零成本 cron 路線、QuantDinger 走完整自架 stack + 可變 SaaS 路線**。對「個人散戶 vs 小型量化 operator」兩種使用者各有對應。
- 與 [[ai-hedge-fund]]、[[tradingagents]]、[[ai-trader]]：這些是 framework / research 性質，**QuantDinger 是同類技術的 production product 化**——從 lab repo 變成「能拿來營運」的完整平台。
- 與 [[tlc-agent-skills]]：QuantDinger 的 `quantdinger-mcp` 可以**寫成一個 Skill 上傳到 Tech Leads Club registry**，被 19 個 agent 通用呼叫。兩者是 orthogonal 的 distribution layer。
- 與 [[abdixere-api]]、[[cli-anything]]：abdixere 主張「工具乾淨小巧」、CLI-Anything 把所有軟體變 agent-native——**QuantDinger 走的是「給 AI 一個完整 API gateway + audit + scope token」的中重路線**，跟 CLI 風格不同但都解「agent 怎麼安全用工具」這個議題。
- 與 [[openhuman]]：兩者都用 MCP server + token-based access 給 agent——**OpenHuman 是個人生活 agent、QuantDinger 是金融交易 agent**，但**架構幾乎一致**（gateway + token + audit + paper/safe default）。這個 pattern 正在成為「Agent 連進已有系統」的事實標準。
- 對台灣 retail quant：可以**直接 fork QuantDinger、用 backend_api_python 內 broker adapter 樣板加上永豐 / 元大 / 富邦 API**——比從零起步快非常多。
- 對 startup 機會：**台灣沒有對應的「open-source quant OS」**——目前都是純粹個人工具或券商 API wrapper。QuantDinger 的「**operator-ready + 雙軌變現 + 開源**」模板，可以做台版 / 繁中版本，搭配台股本土券商整合。
