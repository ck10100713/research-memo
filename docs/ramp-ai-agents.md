---
date: "2026-03-30"
category: "AI 應用"
card_icon: "material-file-document-outline"
oneliner: ""
---
# Ramp AI Agents — $32B 公司如何讓 AI Agent 主導一切

## 資料來源

| 項目 | 連結 |
|------|------|
| YouTube | [Inside Ramp, the $32B Company Where AI Agents Run Everything](https://www.youtube.com/watch?v=RBqT2PHWdBg) |
| 文字版 + PM Skill | [Creator Economy — Inside Ramp](https://creatoreconomy.so/p/inside-ramp-the-32b-company-ai-agents-geoff-charles) |
| Podcast (Spotify) | [Behind the Craft — Inside Ramp](https://open.spotify.com/episode/1bsmIFPjrqFkP8AZTLUZny) |
| 筆記摘要 | [Shaun Abram 評論](https://www.shaunabram.com/podcast-review-behind-the-craft-inside-ramp/) |
| Ramp 內部 Agent | [Why We Built Our Own Background Agent](https://builders.ramp.com/post/why-we-built-our-background-agent) |
| InfoQ 報導 | [Ramp Coding Agent Powers 30% of PRs](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/) |

## 影片概述

| 項目 | 內容 |
|------|------|
| 頻道 | **Peter Yang**（Behind the Craft） |
| 來賓 | **Geoff Charles** — Ramp CPO（Chief Product Officer） |
| 公司 | **Ramp** — $32B 估值的企業支出管理平台 |
| 主題 | Ramp 如何成為最 AI-native 的組織之一 |

---

## 核心數據

| 指標 | 數據 |
|------|------|
| AI 生成程式碼佔比 | **50%**（預計很快達 80%） |
| 去年出貨功能數 | **500+ features**，僅 25 個 PM |
| Inspect agent PR 佔比 | 前後端合併 PR 的 **30%** |
| 研究壓縮比 | 8 天研究 → **8 分鐘** |

---

## 三個內部 AI Agent Demo

### 1. Voice of Customer Agent（客戶之聲）

> 8 天研究壓縮到 8 分鐘

- 自動掃描客戶回饋（Gong 通話、Zendesk 工單等）
- 彙整成結構化 insight
- PM 不再手動翻閱數百筆回饋

### 2. Analyst Agent（分析師）

- 用**自然語言**查詢數據
- 直接對內部數據庫下 query
- 非技術人員也能拉數據、產生 insight
- 取代「跟數據團隊排隊等報表」的流程

### 3. Inspect Agent（內部 coding agent）

> 5 分鐘建立 production feature

- Ramp 自建的**背景 coding agent**
- 比標準 AI 助手更強：有完整 agency、context、存取工程工具的權限
- 已達前後端 **30% PR 合併量**
- 非工程師也能用它出貨 production code

---

## Claude Code PM Skill（三階段產品規格流程）

Geoff 展示了 Ramp 內部使用的 Claude Code PM skill，已移除公司特定資訊，任何人/公司都能採用。

### Phase 1：Frame the Problem（定義問題）

Claude 用 **7 個關鍵問題**挑戰 PM：

- What's the customer job to be done?
- Why now?
- What does success look like?
- If we build this, what does it unlock?
- ...

**如果 PM 答不好，Claude 會反駁**——不是橡皮圖章，而是嚴格的 sparring partner。

### Phase 2：Parallel Research（並行研究）

啟動 **6-10 個並行 agent** 同時掃描：

- 競品分析
- Gong 銷售通話記錄
- Zendesk 客服工單
- 現有 codebase

每個 agent 產出一份 markdown 摘要，Claude 彙整成關鍵 pattern。

### Phase 3：Shape the Spec（收斂規格）

最終產出一份 **2 分鐘可讀的規格文件**：

- Context（背景）
- Design principles（設計原則）
- Requirements grounded in evidence（有證據支撐的需求）
- Alternatives considered（考慮過的替代方案）
- Open questions（待解問題）

> **25 個 PM 出 500+ features 的秘密**：不是 PM 更努力，而是 AI 接管了研究和規格撰寫的勞動密集部分。

---

## L0-L3 AI 熟練度框架

Ramp 用四個等級推動全公司 AI 採用：

| 等級 | 描述 | 範例 |
|------|------|------|
| **L0** | 偶爾用 ChatGPT 當搜尋替代品 | 「幫我查一下...」 |
| **L1** | 使用和調整 custom GPTs、Notion agent、Claude Code | 實驗性使用，但未自動化真正工作 |
| **L2** | **建造應用來自動化自己的工作** | 非工程師用 AI 寫工具取代重複性任務 |
| **L3** | **設計 AI-first 系統** | 從根本用 AI 架構重新設計工作流程 |

### 採用策略（5 個戰術）

1. **移除約束**：不限制工具存取、API token、預算
2. **識別瓶頸**：優先找出工作流中最痛的點
3. **自動化自己的工作**：「Our job is to automate our jobs」
4. **減少 1-on-1 會議**：把時間還給 hands-on building
5. **招聘門檻**：所有候選人必須展示 AI 工具熟練度

### 淘汰訊號

> 「The people who are still in L0, they will most likely not be at the company.」
> 「If you're not a self-starter and you don't have that growth mindset, it's going to be very, very hard to train.」

---

## PM 角色的兩個分裂方向

Geoff 認為 PM 角色正在分裂成兩個方向：

| 方向 | 描述 |
|------|------|
| **Builder PM** | 自己能寫 code / 用 AI 出貨，從 idea 到 production 一人完成 |
| **Strategy PM** | 專注產品策略、市場洞察、客戶研究，但必須能指揮 AI agent 做執行 |

兩個方向都需要 AI 熟練度，差別在於 hands-on building vs. strategic direction。

---

## 爭議性觀點

| 觀點 | 引述 |
|------|------|
| Claude Code 是必要條件 | 「If you're not using Claude Code, you're probably underperforming.」 |
| 管理已死 | 「Management is probably dead. Optimize to be the best builder in the world.」 |
| 50%→80% AI code | 「50% of Ramp's code is written by AI. It'll probably be 80% soon.」 |
| PM 技術不足才選管理 | 暗示部分 PM 選管理路線是因為技術能力不足（引發爭議） |
| 取消 1-on-1 | 與傳統團隊管理原則矛盾 |

---

## 研究價值與啟示

### 關鍵洞察

1. **AI Agent 不是未來，是現在**：Ramp 已經有 50% AI code + 30% agent PR + 8 分鐘取代 8 天研究。這不是概念驗證，是 $32B 公司的日常。

2. **PM Skill 的三階段設計是可複製的**：Frame → Research（並行 agent）→ Spec。這個模式適用於任何產品團隊，且已公開。最關鍵的是 Phase 2 的並行研究——同時掃描競品/通話/工單/codebase，這是人類物理上無法做到的。

3. **L0-L3 框架是企業 AI 採用的實用路線圖**：不是「全員學 AI」的口號，而是有具體等級定義和淘汰標準。L0 留在 ChatGPT 搜尋的人「most likely not be at the company」——這是嚴厲但明確的訊號。

4. **「Builder PM」是新的職涯方向**：PM 不再只寫 PRD 然後交給工程師。Ramp 的 PM 用 Claude Code 直接從 idea 到 production。這根本性改變了 PM 的價值定義。

5. **「Management is dead」的深層含義**：不是說不需要領導力，而是傳統的「管人」角色正在被「管 agent」取代。真正的價值在於能 build，不在於能 manage。

6. **Inspect Agent 的啟示**：Ramp 自建 coding agent 而非只用 Copilot/Claude Code，因為它需要完整的內部工具存取和 context。這暗示通用 coding agent 對大型組織可能不夠——他們需要 domain-specific agent。

### 與 Fluffy 的關聯

- **PM Skill 模式**：三階段（定義→研究→規格）可直接參考用於 Fluffy 的產品開發流程
- **並行 agent 研究**：Phase 2 的 6-10 個並行 agent 掃描不同資料源，是 Fluffy Agent Core 可實作的模式
- **L0-L3 框架**：可作為團隊 AI 能力評估和提升的參考
- **內部 coding agent**：Ramp 的 Inspect agent 驗證了「自建比通用工具更有效」的假設
