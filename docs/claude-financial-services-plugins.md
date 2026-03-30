---
date: "2026-02-23"
category: "Coding Agent 工具"
card_icon: "material-finance"
oneliner: "Anthropic 官方金融服務 Plugin：41 Skills、11 MCP 資料源，覆蓋投行/股研/PE/財管端到端工作流"
---
# Claude Financial Services Plugins 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| BlockTempo 中文報導 | [Anthropic 開源金融分析外掛](https://www.blocktempo.com/anthropic-claude-financial-services-plugins-41-skills-11-data-providers/) |
| GitHub Repo | [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) |
| Claude Help Center | [Install financial services plugins for Cowork](https://support.claude.com/en/articles/13851150-install-financial-services-plugins-for-cowork) |
| LSEG 整合文章 | [Supercharge Claude's Financial Skills With LSEG Data](https://www.lseg.com/en/insights/supercharge-claudes-financial-skills-with-lseg-data) |
| Inc. 報導 | [Anthropic's New Claude Plugins Take Aim at Finance, HR, and More](https://www.inc.com/ben-sherry/anthropics-new-claude-plugins-take-aim-at-finance-hr-and-more-is-your-job-next/91307114) |
| Bloomberg 報導 | [Anthropic Links AI Agent With Tools for Investment Banking, HR](https://www.bloomberg.com/news/articles/2026-02-24/anthropic-links-ai-agent-with-tools-for-investment-banking-hr) |

## 專案概述

Anthropic 官方發布的 **金融服務 Plugin 套件**，將 Claude 從通用 AI 助手轉化為投資銀行、股票研究、私募股權、財富管理四大領域的專業分析師。全套件包含 **41 個 Skills**（自動觸發的領域知識）、**38 個 Commands**（使用者主動呼叫的斜線指令）、**11 個 MCP 資料源整合**。

核心價值：不是做單點工具，而是實現 **端到端工作流** — 從研究 → 分析 → 建模 → 產出報告/簡報，無需 context switching。整個框架是 **純文字檔案**（Markdown + JSON），無需寫程式碼或搭建基礎設施。

| 指標 | 數值 |
|------|------|
| GitHub Stars | 6,949 |
| Forks | 822 |
| 語言 | Python |
| License | Apache 2.0 |
| 發布日期 | 2026-02-23 |
| Skills | 41 |
| Commands | 38 |
| MCP 資料源 | 11 |

## 三層架構

```
┌─────────────────────────────────────────────────────────────┐
│  第三層：Partner-Built Plugins                               │
│  ┌────────────────────┐  ┌────────────────────┐             │
│  │ LSEG               │  │ S&P Global         │             │
│  │ 債券定價、殖利率曲線 │  │ 公司分析、財報預覽  │             │
│  │ FX、選擇權、宏觀    │  │ Capital IQ 資料     │             │
│  └────────────────────┘  └────────────────────┘             │
├─────────────────────────────────────────────────────────────┤
│  第二層：四大功能 Add-on Plugins                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │投資銀行   │ │股票研究   │ │私募股權   │ │財富管理   │       │
│  │CIM       │ │財報更新   │ │Deal      │ │客戶會議   │       │
│  │買家清單   │ │報告生成   │ │Sourcing  │ │財務規劃   │       │
│  │合併模型   │ │催化劑追蹤 │ │盡職調查   │ │組合再平衡 │       │
│  │Deal Track │ │晨會整理   │ │IC Memo   │ │稅務優化   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│  第一層：Core Plugin — financial-analysis（必裝）             │
│                                                             │
│  Comps | DCF | LBO | 3-Statement | PPT QC | 模板           │
│  ＋ 11 個 MCP 資料聯結器（所有 Add-on 共用）                  │
└─────────────────────────────────────────────────────────────┘
```

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

## 11 個 MCP 資料源

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
# 加入市集
claude plugin marketplace add anthropics/financial-services-plugins

# 安裝核心（必須先裝）
claude plugin install financial-analysis@financial-services-plugins

# 按需安裝功能模組
claude plugin install investment-banking@financial-services-plugins
claude plugin install equity-research@financial-services-plugins
claude plugin install private-equity@financial-services-plugins
claude plugin install wealth-management@financial-services-plugins
```

### Claude Cowork

直接從 [claude.com/plugins](https://claude.com/plugins/) 一鍵安裝。

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
plugin-name/
├── .claude-plugin/plugin.json   ← 清單（名稱、版本、描述）
├── .mcp.json                    ← MCP 連接設定
├── commands/                    ← 斜線指令（使用者主動觸發）
│   ├── comps.md
│   ├── dcf.md
│   └── ...
└── skills/                      ← 領域知識（自動觸發）
    ├── valuation-principles.md
    ├── financial-modeling.md
    └── ...
```

關鍵：**全部是 Markdown + JSON**，不需要寫程式碼，不需要基礎設施。

## 目前限制 / 注意事項

1. **MCP 資料源成本高** — 11 個資料源中 FactSet、Bloomberg、S&P Capital IQ 等都是企業級訂閱，個人開發者或小型機構難以負擔
2. **資料延遲與即時性** — MCP endpoint 的資料更新頻率取決於各供應商，非所有資料都是 real-time
3. **法規合規風險** — Disclaimer 明確聲明「不提供金融/投資建議」，但 AI 自動產出的分析報告在法規監管灰色地帶（特別是 MiFID II、SEC 規範下）
4. **模型幻覺風險** — 財務建模中的數字錯誤可能造成重大財務損失，所有 AI 產出必須由專業人員審核
5. **客製化門檻** — 雖號稱 No-Code，但企業級客製化（換資料源、調整工作流）仍需要理解 MCP 協定和 Plugin 架構
6. **Partner Plugin 有限** — 目前只有 LSEG 和 S&P Global 兩個合作夥伴，Bloomberg Terminal（金融業最大資料源）缺席
7. **Claude Cowork 綁定** — 主要為 Claude Cowork 設計，雖相容 Claude Code，但企業部署可能需要 Anthropic Enterprise 方案

## 研究價值與啟示

### 關鍵洞察

1. **Skill-as-Markdown 是垂直 AI 的最輕量路徑** — 整個金融分析專家系統的「知識」全部編碼在 Markdown 文件中（`skills/` 目錄），而非訓練模型或寫程式碼。這意味著領域專家（分析師、銀行家）可以直接編輯 skill 檔案來注入自己的專業知識，完全跳過工程瓶頸。這個模式可以複製到醫療、法律、會計等任何需要領域專業知識的垂直行業。

2. **MCP 是金融資料整合的 Game Changer** — 傳統金融科技需要為每個資料源寫專門的 API 整合，而這套系統用 11 行 MCP endpoint URL 就連通了從 Morningstar 到 PitchBook 的整個金融資料生態。MCP 協定讓「接入新資料源」變成改一行 JSON 的事。這與 LobeHub 的 39K+ MCP Server 生態相呼應 — MCP 正在成為 AI 與外部世界的通用介面。

3. **Anthropic 從開發者工具到產業解決方案的戰略轉型** — Claude Code → Claude Cowork → Financial Services Plugins，Anthropic 正在複製 Salesforce 的路徑：先做平台，再做垂直行業解決方案。金融服務是第一個垂直切入點，選擇金融而非醫療或法律，很可能因為金融的工作流高度標準化（DCF 模型、comps 分析全球通用）且付費意願最強。

4. **端到端工作流 vs 點工具是 AI 產品的分水嶺** — README 開宗明義："Move beyond point tools to complete workflows."這與 Anthropic Harness Design 文章的核心論點一致 — 真正有價值的不是單一 AI 功能，而是串聯整個工作流的 harness。一個 `/ic-memo` 指令背後串接了定價、基準比較、comps、KPI 分析五個步驟，這才是 AI 的殺手級應用。

5. **Apache 2.0 開源是企業信任的入口** — 在金融業（最保守的行業之一）推 AI 產品，開源是建立信任的最有效方式。企業可以審計每一行 skill 和 connector 的邏輯，確保沒有資料外洩風險。但 Apache 2.0 也意味著競爭對手可以 fork 並建立競品 — Anthropic 押注的是 Claude 模型本身的能力護城河，而非 Plugin 程式碼。

### 與其他專案的關聯

- **Anthropic Harness Design**（`harness-design-long-running-apps.md`）：Financial Services Plugins 是 Harness Engineering 在產業垂直場景的具體應用。Skills 編碼了「分析師應該怎麼做」的領域知識，Commands 定義了使用者互動介面，MCP connectors 提供資料基礎 — 三者組合就是一個金融分析師 Harness。
- **LobeHub**（`lobehub.md`）：LobeHub 有 10K+ Skills 市集，但走的是通用路線；Anthropic 的 Financial Services Plugins 是少數由 AI 公司官方出品的垂直行業 Plugin，品質和整合深度遠超社群貢獻。兩者在 MCP 協定上完全互通。
- **LangGraph State API**（`langgraph-state-api.md`）：Financial Services Plugins 的端到端工作流（research → analysis → modeling → output）如果要用 LangGraph 實現，每個步驟的中間結果需要透過 State channels 傳遞，reducer 的設計（累積 vs 覆寫）直接影響報告品質。
- **TradingAgents**（`tradingagents.md`）：同樣是金融 AI 場景，TradingAgents 用多 Agent 辯論做交易決策，而 Financial Services Plugins 用單 Agent + 多 Skill 做分析報告。前者偏自主決策，後者偏人機協作。
