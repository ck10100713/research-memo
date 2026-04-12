---
date: "2026-03-23"
category: "Coding Agent 工具"
card_icon: "material-swap-horizontal"
oneliner: "將 Claude Max 訂閱轉為 OpenAI 相容 API，驅動 Agent 群免費用 Opus 4.6"
---
# OpenClaw Claude Proxy 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub（Enhanced 版） | [ppcvote/openclaw-claude-proxy](https://github.com/ppcvote/openclaw-claude-proxy) |
| GitHub（原版） | [51AutoPilot/openclaw-claude-proxy](https://github.com/51AutoPilot/openclaw-claude-proxy) |
| OpenClaw 官方文件 | [Claude Max API Proxy](https://docs.openclaw.ai/providers/claude-max-api-proxy) |
| 封鎖事件分析 | [The End of the Claude Subscription Hack](https://augmentedmind.substack.com/p/the-end-of-the-claude-subscription-hack) |
| 增強者 | [Ultra Lab](https://ultralab.tw)（台灣 AI 產品公司） |
| Stars | ~33（Enhanced）/ ~13（原版） |
| 授權 | MIT |
| 語言 | JavaScript (Node.js 18+) |
| 建立時間 | 2026-03-21（非常新） |

## 專案概述

OpenClaw Claude Proxy 是一個本地代理伺服器，將 Claude Max 訂閱（$200/月）透過 `claude --print` CLI 指令轉換為 **OpenAI 相容的 API endpoint**，讓你的 Agent 群（OpenClaw、LangChain 等）免費使用 Opus 4.6 / Sonnet 4.6 / Haiku 4.5。

```
Your Agents → Proxy (localhost:3456) → claude --print → Claude Max 訂閱
                                                          ↓
                                          Opus 4.6 / Sonnet 4.6 / Haiku 4.5
```

核心價值主張：如果你的 Agent 每天產生超過 ~89K tokens，用這個 proxy 比直接購買 API 便宜。

!!! danger "重大合規風險"
    Anthropic 在 **2026 年 2 月**已封鎖第三方工具使用 Claude 訂閱 token。`claude --print` 方式目前仍可運作，但明確處於 ToS 灰色地帶。詳見下方「合規風險」段落。

## 技術架構

### 核心機制

Proxy 接收 OpenAI 格式的 API 請求，轉換為 `claude --print` CLI 呼叫：

```
POST /v1/chat/completions
        │
        ▼
┌─────────────────────────────────┐
│  Claude Code Proxy              │
│                                 │
│  1. [pre] Plugin 預處理         │
│     └─ language-enforcer        │
│  2. 排隊（MAX_CONCURRENT=3）    │
│  3. spawn: claude --print       │
│     └─ --model sonnet|haiku     │
│  4. [post] Plugin 後處理        │
│     ├─ content-filter           │
│     └─ cost-tracker             │
│  5. 轉換回 OpenAI 格式回傳     │
└─────────────────────────────────┘
```

### 增強功能（vs 原版）

| 功能 | 原版 | Enhanced（ppcvote） |
|------|------|-------------------|
| 使用統計 | 無 | `GET /stats` — 請求數、token、省下費用 |
| 多模型 | 僅 Opus | Opus / Sonnet / Haiku 切換 |
| 重試 | 無 | CLI 失敗自動重試（`MAX_RETRIES`） |
| Plugin 系統 | 無 | pre/post 處理 hooks |
| 內容過濾 | 無 | 自動遮蔽 API keys、token、IP |
| 費用追蹤 | 無 | 每日節省報告 |
| 語言強制 | 無 | 自動偵測 zh-TW 並強化語言指示 |

### Plugin 系統

在 `plugins/` 目錄放入 `.js` 檔案即可：

```javascript
module.exports = {
  name: 'my-plugin',
  preProcess(messages, model) { return { messages, model }; },
  postProcess(text, model) { return text; }
};
```

**內建 Plugin：**

| Plugin | 類型 | 功能 |
|--------|------|------|
| `content-filter.js` | post | 遮蔽 API keys、Bearer tokens、IP、密碼等敏感資訊 |
| `cost-tracker.js` | post | 追蹤每日節省費用（vs API 定價），寫入 JSON |
| `language-enforcer.js` | pre | 偵測中文內容時自動加入繁中語言指示 |

### 成本對比

| | Anthropic API | Claude Max + Proxy |
|---|---|---|
| Opus 4.6 定價 | $15/M input, $75/M output | $200/月吃到飽 |
| 100K tokens/天 | ~$225/月 | $200/月 |
| 500K tokens/天 | ~$1,125/月 | $200/月 |
| **損益平衡** | ~89K tokens/天 | 超過即省錢 |

## 快速開始

```bash
git clone https://github.com/ppcvote/openclaw-claude-proxy.git
cd openclaw-claude-proxy
npm install
cp .env.example .env  # 編輯 .env 設定 API_KEY
node server.js
```

前置需求：Claude Code CLI 已安裝認證 + Claude Max 訂閱。

### 連接 OpenClaw

```json
{
  "models": {
    "providers": {
      "claude-proxy": {
        "baseUrl": "http://127.0.0.1:3456",
        "api": "openai",
        "apiKey": "YOUR_API_KEY",
        "models": [{
          "id": "claude-opus-4-6",
          "name": "Claude Opus 4.6 (via Max)",
          "contextWindow": 200000,
          "cost": { "input": 0, "output": 0 }
        }]
      }
    }
  }
}
```

## 合規風險與現況

### Anthropic 封鎖時間線

| 時間 | 事件 |
|------|------|
| 2025 下半年 | 社群發現可用 Claude 訂閱 OAuth token 驅動 OpenClaw 等工具，套利嚴重 |
| **2026 年 2 月** | Anthropic 部署三重封鎖：Token Binding、Telemetry 驗證、Pattern Detection |
| 2026 年 2-3 月 | OpenClaw 官方轉向 OpenAI 整合，社群修補 patch 持續被封堵 |

### Anthropic 的三重封鎖機制

1. **Token Binding**：OAuth token 現在只在 Anthropic 驗證呼叫者是正版 Claude Code 客戶端時才生效
2. **Telemetry 要求**：官方工具會傳送 debugging/safety telemetry，第三方 proxy 無法偽造
3. **Pattern Detection**：自動標記高量循環呼叫等 agentic 自動化模式

### 當前狀態

`claude --print` 方式（本 proxy 使用的方法）與 OAuth token 方式不同，是直接呼叫 CLI binary。目前仍可運作，但：

- **OpenClaw 官方文件明確標註**：「Anthropic has blocked some subscription usage outside Claude Code in the past」
- **非官方支援**：社群工具，非 Anthropic 或 OpenClaw 官方認可
- **帳號風險**：過去有使用者因違反 ToS 被封帳號的案例
- **隨時可能失效**：Anthropic 可在任何更新中封堵 `claude --print` 管道

## 目前限制

| 限制 | 說明 |
|------|------|
| **ToS 灰色地帶** | 最大風險，帳號可能被封 |
| **僅限本地** | Proxy 只能在本機運行（安全考量） |
| **CLI 瓶頸** | 依賴 `claude --print` 的回應速度，非原生 API 效能 |
| **非真正 streaming** | SSE 是模擬的，非原生 streaming |
| **並行限制** | 預設 MAX_CONCURRENT=3，受 CLI 程序限制 |
| **Token 估算** | 用字元數 ÷ 4 估算 token 數，不精確 |

## 研究價值與啟示

### 關鍵洞察

1. **訂閱套利的經濟學**：$200/月 Max 訂閱 vs 按量計費 API 之間存在巨大價差。當每天 >89K tokens 時，proxy 路線省錢。這解釋了為何社群持續嘗試繞過封鎖——經濟誘因太強

2. **`claude --print` 是當前唯一存活的管道**：OAuth token 路線已死，但 CLI `--print` flag 仍可用。Proxy 的生命週期完全取決於 Anthropic 何時決定封堵這條路

3. **Plugin 架構是可複用的設計**：content-filter（遮蔽敏感資訊）、cost-tracker（費用追蹤）、language-enforcer（語言強制）這三個 plugin 的設計模式，即使不用於 proxy，也可套用到任何 LLM 中間層

4. **台灣團隊的增強版值得關注**：Ultra Lab 加入的多模型路由、Plugin 系統、統計追蹤等功能，讓原本簡陋的單檔 proxy 變成一個有模有樣的中間層。`language-enforcer.js` 自動偵測繁中也是貼心設計

5. **這類工具的半衰期極短**：從建立（3/21）到現在不到一週，Anthropic 隨時可能封堵。研究價值在於理解 proxy 架構和 plugin 模式，而非長期依賴

### 與其他專案的關聯

| 對比專案 | 關聯 |
|---------|------|
| 本站 [Project Golem](project-golem.md) | 同樣繞過官方 API 的思路（Golem 用 Puppeteer + Web Gemini），面臨類似的 ToS 風險 |
| [OpenClaw](https://github.com/openclaw) | Proxy 的主要消費端，OpenClaw 是 2026 初最火的開源 AI 助理 |
| [Moltbot](https://github.com/moltbot/moltbot) | OpenClaw 的前身，曾因商標爭議更名 |
| 本站 [MCP CLI](mcp-cli.md) | 同為 AI 工具鏈的中間層，但 MCP 是官方協定路線 |
