---
date: "2026-04-15"
category: "社群行銷"
card_icon: "material-bullhorn"
oneliner: "Claude Code Skill — 250+ 項廣告審計，跨 Google/Meta/YouTube/LinkedIn/TikTok/Apple 7 大平台"
---

# Claude Ads 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) |
| 作者部落格 | [Claude Code Replaced Your Ad Agency](https://agricidaniel.com/blog/claude-code-ad-agency) |
| GIGAZINE 報導 | [claude-ads 介紹](https://gigazine.net/gsc_news/en/20260301-claude-ads/) |
| 同作者 SEO 工具 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) |
| AI Marketing Hub 社群 | [Skool 社群](https://www.skool.com/ai-marketing-hub)（2,800+ 成員） |

**作者：** [Agrici Daniel](https://agricidaniel.com/about) — AI Marketing Systems Architect

**專案狀態：** ⭐ 2,510 stars · Python · MIT · 2026-02 創建 · 活躍開發中

## 專案概述

Claude Ads 是一個**建構在 Claude Code 之上的付費廣告審計與優化 Skill**，涵蓋 **7 大廣告平台、250+ 項審計檢查**，產出 0-100 的 Ads Health Score 和優先行動計畫。

跟 tw-house-ops 一樣，它不是獨立應用——而是一組安裝到 Claude Code 的 skill + agent 檔案。使用者在 Claude Code 中輸入 `/ads audit`，系統自動 spawn 6 個平行 subagent 同時審計不同平台，最終產出統一報告。

**實際案例：** 作者在 B2B SaaS 場景做的 5 天 AI 輔助審計發現 35% 預算浪費在不轉換的流量上，結構優化後 CPC 降低 35%。

> 「人類審計師通常檢查 15-20 項，Claude Ads 檢查 250+ 項，在幾分鐘內完成需要數週的工作。」

## 核心功能

### 指令一覽

| 指令 | 功能 |
|------|------|
| `/ads audit` | 全平台審計（6 個平行 subagent） |
| `/ads google` | Google Ads 深度分析（Search、PMax、AI Max、Demand Gen、CTV） |
| `/ads meta` | Meta Ads 分析（Pixel/CAPI、Andromeda creative diversity） |
| `/ads youtube` | YouTube Ads 分析（Skippable、Shorts、Demand Gen） |
| `/ads linkedin` | LinkedIn Ads B2B 分析（TLA、Lead Gen） |
| `/ads tiktok` | TikTok Ads 分析（Creative-first、Smart+、GMV Max） |
| `/ads microsoft` | Microsoft/Bing Ads 分析（Copilot、Google import safety） |
| `/ads apple` | Apple Ads 分析（CPPs、Maximize Conversions、TAP） |
| `/ads creative` | 跨平台素材品質審計 + 疲勞偵測 |
| `/ads landing` | Landing page 品質評估 |
| `/ads budget` | 預算分配 + 出價策略審查 |
| `/ads plan <type>` | 產業別廣告策略規劃（11 種模板） |
| `/ads competitor` | 競爭對手廣告情報 |
| `/ads math` | PPC 財務計算機（CPA、ROAS、break-even、LTV:CAC） |
| `/ads test` | A/B 測試設計（假設框架、顯著性、樣本量） |
| `/ads report` | 產生 PDF 審計報告 |

### 平台覆蓋與檢查項目

| 平台 | 檢查數 | 重點領域 |
|------|--------|---------|
| Google Ads | 80 | Search, PMax, AI Max, Demand Gen, CTV, YouTube |
| Meta Ads | 50 | Pixel/CAPI, Andromeda creative diversity, 受眾 |
| Apple Ads | 35+ | CPPs, Maximize Conversions, AdAttributionKit |
| TikTok Ads | 28 | Creative-first, Smart+, GMV Max, Events API |
| LinkedIn Ads | 27 | B2B targeting, TLA, Lead Gen, CRM 整合 |
| Microsoft Ads | 24 | Google import safety, Copilot, CTV, LinkedIn targeting |
| 跨平台 | 3 | 隱私基礎設施, creative diversity, 更新頻率 |

### Ads Health Score（0-100）

| 等級 | 分數 | 意義 |
|------|------|------|
| A | 90-100 | 只需微調 |
| B | 75-89 | 有改善空間 |
| C | 60-74 | 需注意的問題 |
| D | 40-59 | 嚴重問題 |
| F | <40 | 需要緊急介入 |

### Quality Gates（硬性規則）

- 禁止在沒有 Smart Bidding 的情況下推薦 Broad Match（Google）
- **3x Kill Rule**：CPA 超過目標 3 倍立即暫停
- 預算充足性：Meta ≥5x CPA/ad set、TikTok ≥50x CPA/ad group
- Learning phase 保護：學習期間禁止編輯
- 隱私基礎設施閘門：先驗證追蹤堆疊（Consent Mode V2、CAPI、Events API）再給優化建議

## 技術架構

```
~/.claude/skills/ads/              # 主 Orchestrator
~/.claude/skills/ads/references/   # 25 個 RAG 參考檔案
~/.claude/skills/ads-*/            # 19 個 sub-skills
~/.claude/skills/ads-plan/assets/  # 12 個產業模板
~/.claude/agents/                  # 10 個 agents（6 審計 + 4 素材）
```

```
/ads audit 的執行流程
─────────────────────────────────────────
  /ads audit
       │
       ▼
  Orchestrator 路由
       │
       ├─→ audit-google    (80 checks)  ─┐
       ├─→ audit-meta      (50 checks)  ─┤
       ├─→ audit-creative  (21+ checks) ─┤  6 個平行 subagent
       ├─→ audit-tracking  (8+ checks)  ─┤
       ├─→ audit-budget    (24 checks)  ─┤
       └─→ audit-compliance(18+ checks) ─┘
                                          │
                                          ▼
                                   統一 Health Score
                                   + 優先行動計畫
                                   + PDF 報告（可選）
```

**資料處理方式：**
- **預設：** 使用者提供匯出資料（CSV、截圖、貼上指標）
- **可選 MCP 整合：** 直接連接廣告平台 API
  - Google Ads: [mcp-google-ads](https://github.com/cohnen/mcp-google-ads)
  - Meta Ads: [Adspirer MCP](https://www.adspirer.com)
  - LinkedIn Ads: [GrowthSpree MCP](https://www.growthspreeofficial.com)

**隱私：** 所有分析在本機執行，不傳輸至外部伺服器。MCP 時資料直接在你的機器和廣告平台 API 之間流動。

### 產業模板（/ads plan）

支援 11 種業務類型：

| 類型 | 重點 |
|------|------|
| `saas` | Trial/demo、Google + LinkedIn |
| `ecommerce` | Shopping/PMax、ROAS 導向 |
| `local-service` | Search + LSA、來電追蹤、地理範圍 |
| `b2b-enterprise` | LinkedIn ABM、長銷售週期 |
| `info-products` | Meta + YouTube、webinar/VSL |
| `mobile-app` | Meta + Google UAC、MMP、LTV:CPI |
| `real-estate` | Special Ad Category（住房） |
| `healthcare` | HIPAA、LegitScript |
| `finance` | Special Ad Category（信用） |
| `agency` | 多客戶管理 |
| `generic` | 通用模板 |

## 快速開始

```bash
# 方法一：Plugin 安裝（推薦）
/plugin marketplace add AgriciDaniel/claude-ads
/plugin install claude-ads@agricidaniel-claude-ads

# 方法二：一鍵安裝
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/install.sh | bash

# 使用
claude
/ads audit          # 全平台審計
/ads google         # 單平台深度分析
/ads plan saas      # SaaS 產業策略
/ads report         # 產生 PDF 報告
```

## 目前限制 / 注意事項

- **不自動連接廣告平台** — 預設需手動提供匯出資料，MCP 整合為可選
- **不建立或修改廣告** — 純審計和策略工具，執行仍需手動
- **benchmark 是平均值** — 基於 WordStream、Triple Whale 等 16,000+ 廣告系列，但你的結果會因產業/預算/帳戶成熟度而異
- **需提供上下文** — 不告訴 Claude 預算和產業，建議品質會大打折扣
- **PDF 報告需 reportlab** — 額外 Python 依賴
- **Landing page 分析需 Playwright** — 額外安裝

## 研究價值與啟示

### 關鍵洞察

1. **Claude Code Skill 作為「虛擬顧問」的商業模式。** Claude Ads 本質上是把一個資深廣告顧問的知識體系（250+ 檢查項、11 種產業模板、25 份參考資料）封裝成 Skill。這不是「AI 取代廣告人」，而是「AI 把頂級顧問的方法論民主化」——月付幾十美元的 Claude 訂閱取代數千美元的顧問費。

2. **平行 Subagent 是 Skill 架構的正確實踐。** `/ads audit` spawn 6 個平行 subagent 同時審計不同平台——這直接應用了 Boris Cherny 的「並行化是最大生產力提升」原則。每個 agent 專注一個領域，最終合併成統一報告。

3. **Quality Gates 是防止 AI 犯致命錯誤的關鍵設計。** 「3x Kill Rule」（CPA 超標 3 倍立即暫停）、「Learning phase 禁止編輯」等硬性規則，確保 AI 的建議不會踩到廣告投放的地雷。這種「AI 建議 + 硬規則約束」的模式，適用於任何高風險決策場景。

4. **RAG 模式的巧妙應用。** 25 份 reference 檔案按需載入（而非全部塞進 context），這是 LLM Wiki 理念的具體實踐——預編譯的領域知識，在需要時才載入。比起讓 AI 每次都搜尋最新 benchmark，預載入的 2026 年資料更可靠。

5. **2,510 stars 說明「垂直領域 Skill」的市場需求巨大。** 跟通用的 Claude Code tips 不同，claude-ads 針對一個非常具體的職業需求（廣告投放），卻獲得了比很多通用工具更高的關注度。這暗示 **Claude Code Skill marketplace 的最大機會在垂直領域**。

### 與其他專案的關聯

- **vs tw-house-ops：** 同為「建構在 Claude Code 之上」的領域應用，但架構更成熟。tw-house-ops 用 modes/ 目錄分模式，claude-ads 用完整的 skills + agents + references 三層架構。claude-ads 的 plugin 安裝方式也更接近 Claude Code 生態的標準實踐。
- **vs Boris Cherny 57 Tips：** claude-ads 是 Boris 原則的最佳實踐範例——平行 subagent（Tips #1）、/simplify 品質審查（對應 Quality Gates）、CLAUDE.md 複合知識（對應 25 份 references）。
- **vs Slavingia Skills / KC AI Skills：** 同屬 Claude Code Skill 生態，但 claude-ads 的規模（250+ checks、19 sub-skills、10 agents）遠超一般 skill，更接近一個完整的「Skill 平台」。
- **對行銷團隊的啟示：** 如果團隊有多平台廣告投放需求，claude-ads 可以作為日常審計工具——特別是 `/ads audit` 的自動化全面檢查，能發現人工審計容易遺漏的問題。
