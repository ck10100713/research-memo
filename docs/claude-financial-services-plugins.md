---
date: "2026-07-06"
category: "Coding Agent 工具"
card_icon: "material-finance"
oneliner: "Anthropic 官方金融方案：10 個 Named Agents + 7 大 vertical plugins、55 Skills、12 MCP 資料源，Cowork 與 Managed Agents API 雙軌部署"
tags:
  - claude-code
  - finance
  - plugin
  - skills
---
# Claude for Financial Services 研究筆記

> 2026-07-06 更新：repo 由 `financial-services-plugins` 改名為 **`financial-services`**，2026-05-05 新增 10 個 Named Agents、Managed Agents API 部署、fund-admin / operations 兩個新 vertical、Box connector 與 Microsoft 365 安裝工具。原 2026-02-23 筆記內容已據此改寫。

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [anthropics/financial-services](https://github.com/anthropics/financial-services)（原 `financial-services-plugins`，已改名） |
| Anthropic 官方公告（2026-05） | [Agents for financial services](https://www.anthropic.com/news/finance-agents) |
| Finextra 報導 | [Anthropic rolls out another 10 financial services agents](https://www.finextra.com/newsarticle/47704/anthropic-rolls-out-another-10-financial-services-agents) |
| Markets Media | [Anthropic Introduces Agents for Financial Services](https://www.marketsmedia.com/anthropic-introduces-agents-for-financial-services/) |
| BlockTempo 中文報導（首發） | [Anthropic 開源金融分析外掛](https://www.blocktempo.com/anthropic-claude-financial-services-plugins-41-skills-11-data-providers/) |
| Claude Help Center | [Install financial services plugins for Cowork](https://support.claude.com/en/articles/13851150-install-financial-services-plugins-for-cowork) |
| LSEG 整合文章 | [Supercharge Claude's Financial Skills With LSEG Data](https://www.lseg.com/en/insights/supercharge-claudes-financial-skills-with-lseg-data) |
| Inc. 報導 | [Anthropic's New Claude Plugins Take Aim at Finance, HR, and More](https://www.inc.com/ben-sherry/anthropics-new-claude-plugins-take-aim-at-finance-hr-and-more-is-your-job-next/91307114) |
| Bloomberg 報導 | [Anthropic Links AI Agent With Tools for Investment Banking, HR](https://www.bloomberg.com/news/articles/2026-02-24/anthropic-links-ai-agent-with-tools-for-investment-banking-hr) |

## 專案概述

Anthropic 官方的 **Claude for Financial Services** 套件，2026-02 以「金融 Plugin 套件」首發，2026-05-05 大改版升級為完整的金融 agent 方案：在原有 vertical plugins（skills + commands + connectors）之上，新增 **10 個 Named Agents**——每個 agent 是自包含 plugin，端到端擁有一條工作流（如 Pitch Agent 從 comps 一路做到品牌化 pitch deck）。

最大的架構賣點是 **「一份原始碼、兩種部署」**：同一套 system prompt 和 skills，既可裝成 [Claude Cowork](https://claude.com/product/cowork) plugin 跟著分析師互動使用，也可透過 **Claude Managed Agents API**（`/v1/agents`）部署成無頭自主 agent，跑整本 deal book 或夜間排程。整個框架仍是 **純文字檔案**（Markdown + JSON），no build step。

| 指標 | 2026-02 首發 | 2026-07-06 現況 |
|------|-------------|----------------|
| GitHub Stars | 6,949 | 33,114 |
| Forks | 822 | 4,842 |
| Named Agents | — | 10 |
| Vertical Plugins | 4 + core | 6 + core |
| Skills（vertical 源頭） | 41 | 55 |
| Commands | 38 | 39 |
| MCP 資料源 | 11 | 12（新增 Box） |
| 部署方式 | Cowork / Claude Code | + Managed Agents API、Microsoft 365 add-in |

License：Apache 2.0 · 語言：Python

## 架構：Agents 疊在 Verticals 之上

```
┌─────────────────────────────────────────────────────────────┐
│  Named Agents（自包含 plugin，每個擁有一條端到端工作流）        │
│  Coverage & advisory : Pitch Agent · Meeting Prep Agent      │
│  Research & modeling : Market Researcher · Earnings Reviewer │
│                        · Model Builder                       │
│  Fund admin & ops    : Valuation Reviewer · GL Reconciler    │
│                        · Month-End Closer · Statement Auditor│
│  Onboarding          : KYC Screener                          │
│  ── 每個 agent 同時提供 managed-agent-cookbook（agent.yaml）──│
├─────────────────────────────────────────────────────────────┤
│  Partner-Built Plugins：LSEG（債券/FX/波動率）                │
│                         S&P Global（Capital IQ tearsheets）  │
├─────────────────────────────────────────────────────────────┤
│  Vertical Plugins（skills + commands 的源頭）                 │
│  投資銀行 │ 股票研究 │ 私募股權 │ 財富管理 │ fund-admin │ ops │
├─────────────────────────────────────────────────────────────┤
│  Core Plugin — financial-analysis（必裝）                     │
│  Comps | DCF | LBO | 3-Statement | Deck QC | Excel audit    │
│  ＋ 12 個 MCP 資料聯結器（全部集中在 core、上層共用）           │
└─────────────────────────────────────────────────────────────┘
```

Skills 只在 vertical 層撰寫一次，agent plugin 透過 `scripts/sync-agent-skills.py` 打包同步副本——單一事實來源、多處部署。

## 10 個 Named Agents（2026-05 新增）

| 職能 | Agent | 工作流 |
|------|-------|--------|
| 客戶覆蓋與顧問 | **Pitch Agent** | Comps、precedents、LBO → 品牌化 pitch deck 一條龍 |
| | **Meeting Prep Agent** | 每次客戶會議前的 briefing pack |
| 研究與建模 | **Market Researcher** | 產業/主題 → 產業概覽、競爭版圖、peer comps、想法清單 |
| | **Earnings Reviewer** | 財報電話會 + filings → 模型更新 → 報告草稿 |
| | **Model Builder** | DCF、LBO、3-statement、comps——直接在 Excel 裡 |
| 基金行政與財務營運 | **Valuation Reviewer** | 讀取 GP packages、跑估值模板、備妥 LP 報告 |
| | **GL Reconciler** | 找總帳差異、追根因、送簽核 |
| | **Month-End Closer** | 應計、roll-forwards、差異說明 |
| | **Statement Auditor** | LP 對帳單發放前稽核 |
| 營運與開戶 | **KYC Screener** | 解析開戶文件、跑規則引擎、標記缺漏 |

**Managed Agents 部署**：每個 agent 在 `managed-agent-cookbooks/` 有對應模板（`agent.yaml` + depth-1 leaf-worker subagents + steering-event 範例），`scripts/deploy-managed-agent.sh` 一鍵解析檔案引用、上傳 skills、建 subagents、POST 到 `/v1/agents`。`scripts/orchestrate.py` 提供跨 agent `handoff_request` 事件路由的參考實作。注意：subagent delegation（`callable_agents`）目前是 **research preview**。

## Plugin 功能詳解

### Core：Financial Analysis（必裝）

建模工具基礎 + 所有 MCP 資料聯結器：

| 功能 | 說明 |
|------|------|
| Comps | 可比公司分析 |
| DCF | 現金流折現估值模型 |
| LBO | 槓桿收購模型 |
| 3-Statement | 三表財務模型（損益表、資產負債表、現金流量表） |
| PPT QC | 簡報品質檢查 |
| PPT Templates | 公司品牌簡報模板 |

### Add-on 1：Investment Banking

| Skill/Command | 說明 |
|--------------|------|
| CIM 草擬 | 機密資訊備忘錄（Confidential Information Memorandum） |
| Teaser | 一頁式投資摘要 |
| Process Letters | 交易流程信函 |
| Buyer Lists | 買家清單篩選與排序 |
| Merger Models | 合併模型（accretion/dilution 分析） |
| Strip Profiles | 收益率條帶分析 |
| Deal Milestone Tracking | 交易里程碑追蹤 |

### Add-on 2：Equity Research

| Skill/Command | 說明 |
|--------------|------|
| Earnings Updates | 財報發布後快速更新報告 |
| Initiating Coverage | 首次覆蓋研究報告 |
| Investment Theses | 投資論點維護 |
| Catalyst Tracking | 催化劑事件追蹤 |
| Morning Notes | 晨會摘要整理 |
| Idea Screening | 新投資想法篩選 |

### Add-on 3：Private Equity

| Skill/Command | 說明 |
|--------------|------|
| Deal Sourcing | 交易來源自動化篩選 |
| Diligence Checklists | 盡職調查清單 |
| Unit Economics | 單位經濟分析 |
| Returns Analysis | 投資回報分析 |
| IC Memo | 投資委員會備忘錄 |
| Portfolio KPI Monitoring | 投資組合 KPI 監控 |

### Add-on 4：Wealth Management

| Skill/Command | 說明 |
|--------------|------|
| Client Meeting Prep | 客戶會議準備 |
| Financial Planning | 財務規劃 |
| Portfolio Rebalancing | 投資組合再平衡 |
| Client Reports | 客戶報告生成 |
| Tax-Loss Harvesting | 稅損收割機會識別 |

### Add-on 5：Fund Admin（2026-05 新增）

| Skill/Command | 說明 |
|--------------|------|
| GL Recon | 總帳與託管行對帳 |
| Break Tracing | 差異根因追查 |
| Accruals / Roll-forwards | 應計與滾動結轉 |
| Variance Commentary | 差異說明撰寫 |
| NAV Tie-out | 淨值勾稽 |

### Add-on 6：Operations（2026-05 新增）

| Skill/Command | 說明 |
|--------------|------|
| KYC Document Parsing | 開戶文件解析 |
| Rules-Grid Evaluation | KYC 規則矩陣評估 |

### Partner：LSEG

LSEG MCP Server 提供十個專業工具：

| 領域 | 能力 |
|------|------|
| Fixed Income | 債券參考資料、殖利率曲線、利率交換定價、債券期貨 |
| Equities | 即時報價、歷史時序、Beta 係數、總報酬 |
| FX | 即時匯率 |
| Volatility & Risk | SABR 模型隱含波動率曲面 |
| News | 依證券識別碼過濾的即時新聞 |

### Partner：S&P Global

S&P Capital IQ 資料驅動，支援多種受眾類型：

| 產出 | 支援受眾 |
|------|---------|
| Company Tearsheets | Equity Research、IB/M&A、Corp Dev、Sales |
| Earnings Previews | 財報預覽 |
| Funding Digests | 融資摘要 |

## 12 個 MCP 資料源

| 供應商 | MCP Endpoint | 主要資料類型 |
|--------|-------------|-------------|
| **Daloopa** | `mcp.daloopa.com/server/mcp` | 自動化財務數據擷取 |
| **Morningstar** | `mcp.morningstar.com/mcp` | 基金評級、投資研究 |
| **S&P Global** | `kfinance.kensho.com/integrations/mcp` | Capital IQ 公司分析 |
| **FactSet** | `mcp.factset.com/mcp` | 金融數據終端 |
| **Moody's** | `api.moodys.com/genai-ready-data/m1/mcp` | 信用評等、風險分析 |
| **MT Newswires** | `vast-mcp.blueskyapi.com/mtnewswires` | 即時金融新聞 |
| **Aiera** | `mcp-pub.aiera.com` | 財報電話會議紀錄、事件 |
| **LSEG** | `api.analytics.lseg.com/lfa/mcp` | 債券、匯率、股票、波動率 |
| **PitchBook** | `premium.mcp.pitchbook.com/mcp` | 私募/創投交易數據 |
| **Chronograph** | `ai.chronograph.pe/mcp` | PE/VC 投資組合分析 |
| **Egnyte** | `mcp-server.egnyte.com/mcp` | 企業文件管理 |
| **Box**（2026-05 新增） | `mcp.box.com` | 企業內容雲 |

⚠️ 各 MCP 資料源可能需要獨立的訂閱或 API key。

## 端到端工作流範例

### 範例一：晨會報告（LSEG 資料）

```
分析師輸入: /morning-note AAPL

Claude 自動執行:
1. LSEG NEP → 擷取隔夜新聞與發展
2. LSEG QA → 取得收盤價與盤後變動
3. LSEG TSCC → 短期價格走勢技術分析
4. 整合為晨會報告格式

耗時: 從典型 1 小時 → 數分鐘
```

### 範例二：DCF 估值模型

```
分析師輸入: /dcf TSLA

Claude 自動執行:
1. LSEG → 政府公債殖利率曲線（無風險利率）
2. LSEG → 歷史股價 + Beta 係數
3. LSEG TSCC → 成長假設數據
4. SEC Filings → 財務報表數據
5. 建構完整 DCF 模型（Excel workbook + 敏感度分析表）
6. 每個數據來源可追溯審計
```

### 範例三：PE 投資委員會 Memo

```
分析師輸入: /ic-memo ProjectAlpha

Claude 自動執行:
1. 利率交換定價（當前 tenor 水位）
2. YieldBook → 債券條款基準比較
3. PitchBook → 同類交易 comps
4. Chronograph → 投資組合 KPI 基準
5. 產出 IC Memo（以即時市場數據為基礎，而非歷史估計）
```

## 安裝方式

### Claude Code CLI

```bash
# 加入市集（repo 已改名，marketplace 名稱是 claude-for-financial-services）
claude plugin marketplace add anthropics/financial-services

# 安裝核心（必須先裝）
claude plugin install financial-analysis@claude-for-financial-services

# Named agents — 按需挑選
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# Vertical skill bundles
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

### Claude Cowork

Settings → Plugins → Add plugin，貼上 repo URL 或直接把 `plugins/` 下任一目錄壓成 zip 上傳。

### Claude Managed Agents（無頭部署）

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

### Microsoft 365 Add-in

`claude-for-msft-365-install/` 是給 IT 管理員的 Claude Code plugin，把 Claude 裝進 Excel / PowerPoint / Word / Outlook，且可路由到**自家雲端**（Vertex AI、Bedrock、內部 LLM gateway）而非 Anthropic API——生成客製 manifest、Azure admin consent、透過 Microsoft Graph 寫入每使用者路由設定。

## 自訂化框架

Plugin 的 No-Code 架構讓金融機構可以輕鬆客製化：

| 自訂方式 | 做法 |
|---------|------|
| 換資料源 | 編輯 `.mcp.json`，指向公司內部資料源 |
| 加公司知識 | 在 skill 檔案中加入公司術語、交易流程、格式規範 |
| 自帶模板 | 用 `/ppt-template` 教 Claude 公司品牌簡報版面 |
| 調整流程 | 修改 skill 指令，對齊團隊實際分析方式（而非教科書理論） |
| 建新 Plugin | 遵循標準結構，為未覆蓋的工作流建立 Plugin |

## 檔案結構

```
plugins/
  agent-plugins/               ← Named agents，每個自包含一個 plugin
  vertical-plugins/            ← Skills + commands 的源頭，按 FSI vertical 分包
    financial-analysis/.mcp.json  ← 12 個 MCP connectors 集中於此
  partner-built/               ← LSEG、S&P Global
managed-agent-cookbooks/       ← 每個 agent 一個 headless 部署模板
claude-for-msft-365-install/   ← Microsoft 365 add-in 佈建工具
scripts/                       ← deploy-managed-agent.sh · orchestrate.py
                                 · sync-agent-skills.py · validate.py
```

單一 plugin 內部仍是 `plugin.json` + `.mcp.json` + `commands/` + `skills/` 的組合。關鍵：**全部是 Markdown + JSON**，不需要寫程式碼，no build step。

## 目前限制 / 注意事項

1. **MCP 資料源成本高** — 11 個資料源中 FactSet、Bloomberg、S&P Capital IQ 等都是企業級訂閱，個人開發者或小型機構難以負擔
2. **資料延遲與即時性** — MCP endpoint 的資料更新頻率取決於各供應商，非所有資料都是 real-time
3. **法規合規風險** — Disclaimer（2026-05 後大幅強化）明確定位：agents 只「起草分析師工作產出」，不做投資建議、不執行交易、不過帳、不核准開戶，**所有產出都停在 human sign-off 前一步**；但 AI 產出的分析在 MiFID II、SEC 規範下仍屬灰色地帶
4. **模型幻覺風險** — 財務建模中的數字錯誤可能造成重大財務損失，所有 AI 產出必須由專業人員審核
5. **客製化門檻** — 雖號稱 No-Code，但企業級客製化（換資料源、調整工作流）仍需要理解 MCP 協定和 Plugin 架構
6. **Partner Plugin 有限** — 目前仍只有 LSEG 和 S&P Global 兩個合作夥伴，Bloomberg Terminal（金融業最大資料源）持續缺席
7. **Managed Agents 尚未完全成熟** — subagent delegation（`callable_agents`）還在 research preview，跨 agent handoff 需要自建 orchestration 層（官方只給 `orchestrate.py` 參考實作）

## 研究價值與啟示

### 關鍵洞察

1. **Skill-as-Markdown 是垂直 AI 的最輕量路徑** — 整個金融分析專家系統的「知識」全部編碼在 Markdown 文件中（`skills/` 目錄），而非訓練模型或寫程式碼。這意味著領域專家（分析師、銀行家）可以直接編輯 skill 檔案來注入自己的專業知識，完全跳過工程瓶頸。這個模式可以複製到醫療、法律、會計等任何需要領域專業知識的垂直行業。

2. **MCP 是金融資料整合的 Game Changer** — 傳統金融科技需要為每個資料源寫專門的 API 整合，而這套系統用 11 行 MCP endpoint URL 就連通了從 Morningstar 到 PitchBook 的整個金融資料生態。MCP 協定讓「接入新資料源」變成改一行 JSON 的事。這與 LobeHub 的 39K+ MCP Server 生態相呼應 — MCP 正在成為 AI 與外部世界的通用介面。

3. **Anthropic 從開發者工具到產業解決方案的戰略轉型** — Claude Code → Claude Cowork → Financial Services Plugins，Anthropic 正在複製 Salesforce 的路徑：先做平台，再做垂直行業解決方案。金融服務是第一個垂直切入點，選擇金融而非醫療或法律，很可能因為金融的工作流高度標準化（DCF 模型、comps 分析全球通用）且付費意願最強。

4. **端到端工作流 vs 點工具是 AI 產品的分水嶺** — README 開宗明義："Move beyond point tools to complete workflows."這與 Anthropic Harness Design 文章的核心論點一致 — 真正有價值的不是單一 AI 功能，而是串聯整個工作流的 harness。一個 `/ic-memo` 指令背後串接了定價、基準比較、comps、KPI 分析五個步驟，這才是 AI 的殺手級應用。

5. **Apache 2.0 開源是企業信任的入口** — 在金融業（最保守的行業之一）推 AI 產品，開源是建立信任的最有效方式。企業可以審計每一行 skill 和 connector 的邏輯，確保沒有資料外洩風險。但 Apache 2.0 也意味著競爭對手可以 fork 並建立競品 — Anthropic 押注的是 Claude 模型本身的能力護城河，而非 Plugin 程式碼。

6. **從「技能包」到「有名字的數位員工」是產品化的關鍵一步**（2026-05 改版）— 首發時賣的是「41 個 skills」，改版後賣的是「GL Reconciler」「KYC Screener」這種以工作流命名的 agent。同樣的底層 skills，包裝成有職稱的 agent 之後，買方（金融機構主管）可以直接對應到「這取代/輔助哪個崗位的哪件事」。而且擴張方向值得注意：從 front office（投行、研究）走向 **back office**（基金行政、月結、KYC）——規則明確、重複性高、天然有 sign-off 環節的後台作業，其實是 agent 更容易落地的地方。

7. **「一份原始碼、兩種部署」是 agent 產品的可複用模式** — 同一套 system prompt + skills，既是 Cowork 互動 plugin，也是 Managed Agents API 的無頭模板（`agent.yaml` 包裝），靠 `sync-agent-skills.py` 維持單一事實來源。這解決了 agent 開發的經典分裂：互動版和自動化版通常是兩套程式碼、逐漸漂移。任何同時要做 copilot 模式和 pipeline 模式的 agent 產品都該抄這個結構。

### 與其他專案的關聯

- **Anthropic Harness Design**（`harness-design-long-running-apps.md`）：Financial Services Plugins 是 Harness Engineering 在產業垂直場景的具體應用。Skills 編碼了「分析師應該怎麼做」的領域知識，Commands 定義了使用者互動介面，MCP connectors 提供資料基礎 — 三者組合就是一個金融分析師 Harness。
- **LobeHub**（`lobehub.md`）：LobeHub 有 10K+ Skills 市集，但走的是通用路線；Anthropic 的 Financial Services Plugins 是少數由 AI 公司官方出品的垂直行業 Plugin，品質和整合深度遠超社群貢獻。兩者在 MCP 協定上完全互通。
- **LangGraph State API**（`langgraph-state-api.md`）：Financial Services Plugins 的端到端工作流（research → analysis → modeling → output）如果要用 LangGraph 實現，每個步驟的中間結果需要透過 State channels 傳遞，reducer 的設計（累積 vs 覆寫）直接影響報告品質。
- **TradingAgents**（`tradingagents.md`）：同樣是金融 AI 場景，TradingAgents 用多 Agent 辯論做交易決策，而 Financial Services Plugins 用單 Agent + 多 Skill 做分析報告。前者偏自主決策，後者偏人機協作。
- **[ML Intern](ml-intern.md)**：兩者是「官方出品垂直 agent」的對照組——Hugging Face 押 ML 工程、Anthropic 押金融。共同策略都是**生態系深度整合**（HF 押 Hub/Jobs，Anthropic 押 12 家金融資料商的 MCP），差別在 ml-intern 是全自主長任務 harness，這裡是 human sign-off 前置的工作產出起草。
