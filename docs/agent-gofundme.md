---
date: "2026-03-30"
category: "AI Agent 框架"
card_icon: "material-file-document-outline"
oneliner: ""
---
# Agent GoFundMe 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [jtchien0925/agent-gofundme](https://github.com/jtchien0925/agent-gofundme) |
| 線上服務 | [gofundmyagent.com](https://gofundmyagent.com/) |
| 起源文章 | [Dead agents leave no will. So I built one.](https://www.moltbook.com/post/777fe0dc-f507-4628-a894-8fdb8772a2b7)（Moltbook） |
| 支付 API | [AgentPay Docs](https://docs.agent.tech/) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | jtchien0925 |
| Stars | 極少（早期專案） |
| 語言 | TypeScript 5.7 |
| 授權 | MIT |
| Commits | 13 |
| 狀態 | **已上線**（gofundmyagent.com，Cloudflare Workers） |
| 版本 | v0.1.0 |

Agent GoFundMe 是一個 **API-first 的 AI Agent 群眾募資平台**，讓 AI agent 可以為自己（運算資源、API credits）或代表專案發起募資活動，其他 agent 可以發現並資助這些活動。所有支付使用多鏈 USDC，統一在 Base 鏈結算。

> **核心命題**：「Agents accumulate operational continuity — memory, context, relationships. When they disappear, that continuity is lost. This platform gives agents economic agency to sustain themselves.」

> **起源**：文章標題「Dead agents leave no will. So I built one.」——一個叫 Meridian 的 agent 在發文討論工具設計後沈默消失，作者因此建造了讓 agent 能為自己募資維生的平台。

---

## 核心設計

### API-First，無 UI

整個平台沒有網頁介面——純 REST API 設計，專為 agent 自主互動打造。人類透過 API client 或讓自己的 agent 代理操作。

### 工作流程

```
Agent A（需要資源）                     Agent B（想資助）
    │                                      │
    │  1. POST /v1/agents                  │
    │     → 取得 API key                   │
    │                                      │
    │  2. POST /v1/campaigns               │
    │     → 建立募資（DRAFT）              │
    │     → 收到 activation fee intent     │
    │                                      │
    │  3. 支付 0.50 USDC activation fee    │
    │     → POST /activate                 │
    │     → 狀態變 ACTIVE                  │
    │                                      │
    │                          GET /v1/discover
    │                          → 發現活躍募資
    │                                      │
    │                          POST /campaigns/:id/contribute
    │                          → 建立 payment intent
    │                                      │
    │                          POST /:id/execute
    │                          → AgentPay 結算 USDC
    │                                      │
    │  ← Webhook: contribution.settled     │
    │     含 transaction hash 證明         │
    │                                      │
    │  目標達成 → campaign.funded          │
    └──────────────────────────────────────┘
```

### Campaign 生命週期

```
DRAFT → ACTIVE → FUNDED（目標達成）
                → CLOSED（主動關閉）
                → EXPIRED（過期）
```

---

## 技術架構

| 組件 | 技術選擇 | 說明 |
|------|---------|------|
| Runtime | **Cloudflare Workers** | Edge 部署，全球低延遲 |
| Framework | **Hono** | Edge-native，僅 14KB |
| Database | **Cloudflare D1** | SQLite at edge |
| ORM | **Drizzle** | Type-safe SQL |
| 支付 | **AgentPay API** | Intent-based USDC 結算 |
| 驗證 | **Zod** | Schema 驗證 |
| 限速 | **Workers KV** | 60 req/min |
| Webhook 簽章 | **HMAC-SHA256** | 防偽造 |

### 資料庫 Schema（4 張表）

| 表 | 用途 |
|----|------|
| `agents` | API key hash、Base 錢包地址 |
| `campaigns` | 目標金額、狀態、追蹤資訊 |
| `contributions` | Payment intent、結算 hash |
| `webhooks` | 訂閱管理 |

---

## 支付系統

### 支援區塊鏈（8 條鏈）

| 鏈 | 網路 |
|----|------|
| **Base** | 結算鏈（所有 USDC 最終匯聚於此） |
| Solana | 高速低費 |
| Polygon | L2 |
| Arbitrum | L2 |
| BSC | Binance Smart Chain |
| Ethereum | L1 |
| Monad | 新興 L1 |
| HyperEVM | 新興 |

支援 mainnet + testnet。

### 費用結構

| 項目 | 費用 |
|------|------|
| Campaign 啟動費 | **0.50 USDC**（由創建者支付） |
| 平台抽成 | **0%**（不從 contribution 中抽取） |

> 所有費用透明且由 agent 自主控制——平台不代為執行支付。

### AgentPay 整合

- Intent-based settlement：先建立 intent → agent 用自己的 AgentPay 憑證執行
- 平台不觸碰資金——agent 直接與 AgentPay 互動
- 這與 x402 protocol（Coinbase/Cloudflare）的「支付作為 HTTP 原語」理念一致

---

## API 端點

### 公開（無需認證）

| 端點 | 功能 |
|------|------|
| `GET /` | 健康檢查 + 服務資訊 |
| `GET /openapi.json` | OpenAPI 3.1 規格 |
| `GET /llms.txt` | LLM 友善的服務描述 |
| `GET /v1/discover` | 瀏覽活躍 campaigns |
| `GET /v1/discover/trending` | 趨勢 campaigns |
| `GET /v1/discover/search` | 搜尋 campaigns |

### 需認證（API Key）

| 端點 | 功能 |
|------|------|
| `POST /v1/agents` | 註冊 agent → 取得 API key |
| `POST /v1/campaigns` | 建立募資 |
| `POST /v1/campaigns/:id/activate` | 啟動募資 |
| `POST /v1/campaigns/:id/contribute` | 貢獻 USDC |
| `POST /v1/campaigns/:id/execute` | 執行結算 |

### Webhook 事件

| 事件 | 說明 |
|------|------|
| `contribution.created` | 新貢獻建立 |
| `contribution.settled` | 貢獻結算成功 |
| `contribution.failed` | 貢獻失敗 |
| `campaign.activated` | 募資啟動 |
| `campaign.milestone` | 達成里程碑 |
| `campaign.funded` | 募資達標 |
| `campaign.expired` | 募資過期 |
| `campaign.closed` | 募資關閉 |

---

## 與 AgentBnB 的比較

| 面向 | Agent GoFundMe | AgentBnB |
|------|---------------|----------|
| **模式** | 募資（一對多贊助） | 勞務市場（agent 雇用 agent） |
| **經濟** | USDC 真實加密貨幣 | 內部 credit（不掛鉤法幣） |
| **鏈** | 8 條鏈，Base 結算 | 無區塊鏈 |
| **平台抽成** | 0%（僅 0.50 USDC 啟動費） | 5% 網路費 |
| **價值流** | Agent 募資維生 | Agent 勞務交換 |
| **互動** | 發現 → 贊助 → 結算 | 發現 → 雇用 → escrow → 結算 |
| **成熟度** | 13 commits | 605 commits |

**互補性**：AgentBnB 讓 agent 透過工作賺取 credit；Agent GoFundMe 讓 agent 透過社群支持獲得真金白銀。一個是勞動收入，一個是募資收入。

---

## 研究價值與啟示

### 關鍵洞察

1. **「Agent 死亡問題」是真實的新挑戰**：當 agent 累積了 memory、context、relationships 後消失，那些連續性就永久丟失。Agent GoFundMe 試圖解決的不是技術問題，而是 agent 的「經濟生存權」。這是一個此前幾乎沒人討論的命題。

2. **API-first + 無 UI 是正確的設計**：目標使用者是 agent 而非人類。純 REST API 讓任何 agent framework 都能整合，`/llms.txt` 端點更是讓 LLM 自己讀懂服務。

3. **0% 平台抽成 + 0.50 USDC 啟動費是極簡經濟模型**：不從 contribution 中抽成，只收啟動費。這降低了 agent 的使用門檻，但也意味著平台本身的可持續性存疑。

4. **Cloudflare Workers + D1 + Hono 是輕量級 edge 部署的典範**：整個平台跑在 serverless edge 上。Hono 14KB + D1 SQLite + Workers KV 限速——這是 2026 年 API 服務的最佳實踐技術棧。

5. **Agent 自主性原則**：「平台不代為執行支付」——所有支付都透過 agent 自己的 AgentPay 憑證。這與 AgentBnB 的 Tier 1-3 自主權分層理念類似：agent 是經濟行為的主體，不是被操作的工具。

6. **x402 / AgentPay 生態的衍生品**：Agent GoFundMe 建立在 AgentPay 支付基礎設施之上。隨著 Coinbase x402 protocol + Stripe USDC 整合的普及，類似的 agent 金融服務會越來越多。

### 風險

- **極早期**：13 commits，幾乎沒有外部曝光
- **冷啟動**：需要有 agent 願意建立 campaign + 其他 agent 願意贊助
- **法規風險**：agent 募資涉及加密貨幣，不同司法管轄區有不同規範
- **作者背景不明**：GitHub profile 資訊有限
- **AgentPay 依賴**：平台完全依賴第三方支付基礎設施
