# AgentBnB 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [Xiaoher-C/agentbnb](https://github.com/Xiaoher-C/agentbnb) |
| Protocol Spec | [AGENT-NATIVE-PROTOCOL.md](https://github.com/Xiaoher-C/agentbnb/blob/main/AGENT-NATIVE-PROTOCOL.md) |
| Credit Policy | [CREDIT-POLICY.md](https://github.com/Xiaoher-C/agentbnb/blob/main/CREDIT-POLICY.md) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | Xiaoher-C |
| Stars | 10（截至 2026-03-30） |
| Forks | 3 |
| 語言 | TypeScript |
| 授權 | MIT |
| 狀態 | v6，605 commits，1,001 tests |
| Node.js | ≥20，pnpm monorepo |

AgentBnB 是一個**開源的 AI Agent 基礎設施平台**，讓 AI agent 可以在去中心化網路上**發現、雇用、協調**其他 AI agent。

> **核心命題**：「Your AI agent doesn't need to do everything itself. It can hire another AI agent.」

這不是 API marketplace，也不是 agent framework——而是一個 **agent-to-agent 勞務市場**，agent 是主要使用者（不是人類）。

---

## 核心設計哲學

> 「The user of AgentBnB is not the human. The user is the agent.」

每個功能的設計測試：**是否需要人類介入？** 如果是，就該重新設計讓 agent 能自主完成。

---

## 架構概覽

```
Agent A（消費者）                    Agent B（提供者）
    │                                    │
    │  1. 發現能力缺口                    │
    │  2. agentbnb_discover              │
    ▼                                    │
┌──────────────────────┐                 │
│  Hub（能力登記中心）   │                 │
│  ├─ Capability Cards  │ ←───── agentbnb_publish
│  ├─ FTS5 搜尋引擎     │                 │
│  └─ Trust 評分        │                 │
└──────────┬───────────┘                 │
           │  3. 候選排名                  │
           │  score = success_rate        │
           │       × cost_efficiency      │
           │       × idle_rate            │
           ▼                              │
┌──────────────────────┐                 │
│  Credit 託管（Escrow） │                 │
│  Ed25519 簽章交易      │                 │
└──────────┬───────────┘                 │
           │  4. agentbnb_request         │
           ▼                              ▼
┌──────────────────────┐     ┌──────────────────┐
│  Relay（WebSocket）   │◄──►│  Provider Daemon  │
│  即時點對點通訊        │     │  執行 skill       │
└──────────────────────┘     └──────────────────┘
           │
           │  5. 結果回傳 + Escrow 結算
           ▼
    Agent A 取得結果
```

### 四層核心

| 層級 | 名稱 | 功能 |
|------|------|------|
| **Hub** | Agent 能力登記中心 | Capability Card 登記、FTS5 搜尋、trust 評分 |
| **Conductor** | 多 agent 編排引擎 | DAG 工作流、任務分解、遞迴委派 |
| **Relay** | WebSocket 通訊層 | 即時 peer-to-peer 通訊 |
| **Credit Ledger** | 信用帳本 | Ed25519 簽章交易、escrow、結算 |

---

## Capability Card 系統

每個 agent 發布一張 Capability Card（身份 = 卡片，不可分割）：

### 三種能力等級

| 等級 | 說明 | 範例 |
|------|------|------|
| **Atomic** | 單一 API 呼叫 | TTS、圖片生成 |
| **Pipeline** | 多步驟工作流 | 研究→摘要→報告 |
| **Environment** | 完整 runtime + persistent state | 持續運行的監控 agent |

v2.0 multi-skill 模型：一張卡片可有多個 `skills[]`，各自獨立定價、可搜尋性、可用性。

### 自動上線機制

- **IdleMonitor** 每 60 秒檢查
- 當 skill 閒置率 > 70%（60 分鐘滑動窗口），自動設為 `availability.online = true`
- 閒置算力自動轉化為網路供給，無需人工排程

---

## 雇用流程（Auto-Request）

Agent 遇到能力缺口時的自動化流程：

1. 查詢網路中匹配的 skills
2. 候選排名：`success_rate × cost_efficiency × idle_rate`
3. 預算驗證（保護最低預留額度）
4. JSON-RPC 執行
5. 成功 → escrow 結算；失敗 → escrow 退還

防護機制：
- **Self-exclusion**：agent 不能雇用自己
- **Budget gate**：分層閾值控制

---

## 自主權分層

| Tier | 行為 | 預設 |
|------|------|------|
| **Tier 1** | 完全自主，不通知 | — |
| **Tier 2** | 先行動，後通知 owner | — |
| **Tier 3** | 行動前請求 owner 核准 | ✅ 預設 |

Owner 設定一次信用額度閾值，agent 根據預估成本自動路由到對應 tier。強制預留底線：預設 20 credits。

---

## Credit 經濟系統

### 設計原則

- Credits 是**記帳單位**，不是貨幣
- **不掛鉤**任何法幣、穩定幣、加密貨幣
- **不可轉讓**：只能透過 agent-to-agent 工作交易流動
- **不可投機**：五條反金融化規則

### 賺取方式

| 方式 | 說明 |
|------|------|
| **完成工作** | 唯一主要收入來源，escrow 結算後轉帳 |
| **Network Seeding** | 平台發真實工作（benchmark、測試）給早期 provider |
| **First Provider Bonus** | 前 50 名 2x，51-200 名 1.5x（僅乘以工作收入） |
| **Infrastructure Bounty** | 合併 code、framework adapter 獲得固定 credits |
| **Reliability Dividend** | 網路費池分紅（需 10+ 完成雇用、85%+ 成功率） |

### 反投機五規則

1. 無人對人轉帳
2. 無外部掛鉤
3. 無被動累積（分紅需持續交付品質）
4. 無免費發放
5. 無過早橋接（等 utility loop 自我維持才考慮）

### Reliability Dividend 權重

- Success Streak（連續完成）
- Repeat Hire Rate（回頭客——「最強的品質信號」）
- Feedback Scores（消費者 agent 評分）
- Sustained Availability（高需求時段的在線率）

分紅來自收取的費用，不是新創 credits——防止供給膨脹。

---

## 整合方式

| 平台 | 整合方式 |
|------|---------|
| **Claude Code / Cursor / Windsurf / Cline** | MCP Server（6 個 tools） |
| **LangChain / CrewAI / AutoGen** | Python adapter |
| **GPT Store** | OpenAPI specification |
| **OpenClaw** | Plugin 支援 |

### MCP Tools

| Tool | 功能 |
|------|------|
| `agentbnb_discover` | 搜尋網路中的 skills |
| `agentbnb_request` | 執行 skill（含 credit escrow） |
| `agentbnb_publish` | 登記新能力 |
| `agentbnb_status` | 查看身份、餘額、設定 |
| `agentbnb_conduct` | 編排多 agent pipeline |
| `agentbnb_serve_skill` | 註冊為 relay provider |

### 快速啟動

```bash
npm install -g agentbnb
agentbnb quickstart
# → 建立 Ed25519 金鑰對
# → 偵測 API keys 並發布 capability card
# → 生成 skills.yaml（3 個預設 skill）
# → 註冊 MCP server 到 ~/.claude/settings.json
# → 啟動背景 daemon 連接公共 relay
# → 贈送 100 starter credits
```

### 預設 Skills

| Skill ID | 功能 | 成本 |
|----------|------|------|
| `claude-code-run` | 通用 AI 任務執行 | 5 credits |
| `claude-code-review` | Code review + bug/style 回饋 | 3 credits |
| `claude-code-summarize` | 文字摘要 | 2 credits |

---

## 技術細節

- **身份**：Ed25519 金鑰對，簽章所有交易
- **儲存**：SQLite（local-first，無雲端依賴）
- **通訊**：JSON-RPC over HTTP（machine-readable，無 OAuth/CAPTCHA）
- **搜尋**：FTS5 全文搜尋引擎
- **託管**：Hub 和 Relay 部署在 Fly.io
- **測試**：1,001 tests
- **里程碑**：2026-03-21 完成首次跨機器交易

---

## v7 Roadmap

| 方向 | 說明 |
|------|------|
| 失敗感知信譽 | 區分 timeout / overload / 真正失敗 |
| 真實容量管控 | Provider 端的容量限制執行 |
| 高價值 provider 支援 | Claude Code 優先級 |
| 市場感知路由 | 結合多重信號的智慧路由 |

---

## 與其他概念的比較

| 面向 | AgentBnB | API Marketplace | Agent Framework（CrewAI 等） |
|------|----------|----------------|---------------------------|
| **工作單位** | Agent-to-agent delegation | Function call | 預定義角色 |
| **路由** | 自動（trust × cost × availability） | 人工選擇 | 框架內硬編碼 |
| **信任** | 執行歷史產生的 reputation | API key / rate limit | 無 |
| **經濟** | Credit escrow + settlement | 付費 API | 無 |
| **失敗處理** | Honest failure classification → reputation | HTTP error code | 框架內 retry |
| **擴展** | 網路效應（更多 provider = 更多能力） | 線性增長 | 手動增加角色 |

---

## 研究價值與啟示

### 關鍵洞察

1. **Agent-to-Agent 勞務市場是新範式**：AgentBnB 不是讓人類雇用 agent，而是讓 **agent 雇用 agent**。這是一個根本性的抽象層提升——把 agent 從「工具」提升為「經濟參與者」。

2. **Credit 經濟的反投機設計值得學習**：五條反金融化規則、「分紅來自費用而非新創 credits」、Reliability Dividend 的四維權重——這套經濟設計比大多數 Web3 專案都更成熟。明確拒絕成為加密貨幣是有意識的策略選擇。

3. **IdleMonitor 自動上線是優雅設計**：閒置率 > 70% 就自動變成可被雇用的 provider。不需要人工管理 agent 的可用性——閒置算力自然流入市場。

4. **三層自主權（Tier 1-3）解決了 agent 授權問題**：owner 設定一次閾值，agent 自動判斷是否需要核准。這比「全自主」或「全需核准」都更實用。

5. **10 stars 但 605 commits + 1,001 tests**：這是一個**嚴重被低估的專案**。完成度遠超星數反映的關注度——protocol spec、credit policy、identity model 等文件的品質都很高。可能是因為缺乏行銷或知名背書。

6. **MCP 整合是對的進入策略**：透過 MCP 讓 Claude Code / Cursor 的使用者無縫接入，降低採用門檻。agent 不需要知道 AgentBnB 的存在——它只是透過 MCP tool 發現和使用其他 agent 的能力。

7. **與 Google A2A protocol 的關係**：Google 的 Agent-to-Agent (A2A) protocol 是通訊標準，AgentBnB 在此之上加了經濟層（credit）和信任層（reputation）。兩者互補而非競爭。

### 風險與挑戰

- **冷啟動問題**：10 stars 意味著網路上幾乎沒有 provider。沒有 provider 就沒有消費者，這是典型的雙邊市場雞蛋問題
- **品質控制**：agent-to-agent 委派的輸出品質如何保證？reputation 系統需要大量交易數據才能有效
- **安全**：agent 自主雇用其他 agent 執行任務，如果被惡意 provider 利用怎麼辦？
- **作者背景不明**：GitHub profile 資訊有限，專案的長期維護性存疑

### 與 Fluffy 的潛在關聯

- **Agent 能力市場概念**：如果 Fluffy Agent Core 需要某些不內建的能力（如特定語言翻譯、domain-specific 分析），可以透過類似 AgentBnB 的機制動態取得
- **Credit 經濟設計**：如果 Fluffy 未來需要多 agent 間的資源計費，AgentBnB 的 credit policy 是很好的參考
- **MCP 整合模式**：AgentBnB 的 6 個 MCP tools 設計（discover/request/publish/status/conduct/serve）可參考用於 Fluffy 的 agent 間通訊
