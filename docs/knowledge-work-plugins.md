---
date: "2026-05-27"
category: "Coding Agent 工具"
card_icon: "material-briefcase-variant"
oneliner: "Anthropic 官方開源的知識工作者 plugin 市集，為 Claude Cowork/Code 而生：~10 個職能 plugin（sales/finance/legal/data...）+ 數十個 partner-built，純 markdown+JSON 封裝 skills/commands/connectors，把 Claude 變成「你公司專屬的角色專家」"
tags:
  - claude-code
  - plugin
  - skills
---

# Knowledge Work Plugins 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/anthropics/knowledge-work-plugins> |
| Plugin 市集（Cowork） | <https://claude.com/plugins/> |
| Claude Cowork 產品頁 | <https://claude.com/product/cowork> |
| MCP 協定 | <https://modelcontextprotocol.io/> |
| License | Apache-2.0 |
| 維護方 | Anthropic 官方 |

## 專案概述

**Knowledge Work Plugins** 是 Anthropic 在 2026/01 開源的官方 plugin 市集（16,841 stars / 1,974 forks，Apache-2.0），主要為 **Claude Cowork** 設計、同時相容 **Claude Code**。

它的定位一句話講清楚：**「把 Claude 變成你的角色、團隊、公司的專家」**。Cowork 讓你「設定目標、Claude 交付完成的專業成果」；plugin 則讓你更進一步——告訴 Claude 你偏好的工作方式、要從哪些工具/資料拉資訊、如何處理關鍵 workflow、要暴露哪些 slash command，讓整個團隊得到更好、更一致的產出。

每個 plugin 把特定職能（job function）所需的 **skills、connectors、slash commands、sub-agents** 打包成一束。開箱即用就能給該角色一個強力起點；真正的威力來自**為你公司客製**——你的工具、你的術語、你的流程——讓 Claude 像是為你團隊量身打造的。

關鍵設計哲學：**「每個元件都是 file-based——純 markdown 與 JSON，無程式碼、無基礎設施、無 build step」**。貢獻 plugin 就只是 fork、改 markdown、發 PR。

## Plugin 生態（已成長到 49 個）

README 列的是最初 11 個 Anthropic 自家 plugin，但 marketplace.json 顯示生態已擴張到 **49 個**——約 10 個第一方職能 plugin + 大量 partner-built 整合。

### 第一方核心職能 Plugin

| Plugin | 功能 | 代表 Connectors |
|--------|------|----------------|
| **productivity** | 任務、行事曆、每日 workflow、個人 context 記憶 | Slack, Notion, Asana, Linear, Jira, Monday, ClickUp, M365 |
| **sales** | 研究潛客、call prep、pipeline review、outreach、competitive battlecard | HubSpot, Close, Clay, ZoomInfo, Fireflies, Notion |
| **customer-support** | Triage 工單、草擬回覆、打包 escalation、轉成知識庫文章 | Intercom, HubSpot, Guru, Jira, Notion |
| **product-management** | 寫 spec、規劃 roadmap、整合 user research、追競品 | Linear, Asana, Jira, Notion, Figma, Amplitude, Pendo |
| **marketing** | 草擬內容、規劃 campaign、品牌語調、競品 brief、跨渠道報表 | Canva, Figma, HubSpot, Amplitude, Ahrefs, Klaviyo |
| **legal** | 審約、NDA triage、compliance、風險評估、模板回覆 | Box, Egnyte, Jira, M365 |
| **finance** | 分錄、對帳、財報、變異分析、結帳、稽核支援 | Snowflake, Databricks, BigQuery, Slack, M365 |
| **data** | 寫 SQL、統計分析、建 dashboard、分享前驗證 | Snowflake, Databricks, BigQuery, Hex, Amplitude |
| **enterprise-search** | 跨 email/chat/docs/wiki 一次查詢全公司工具 | Slack, Notion, Guru, Jira, Asana, M365 |
| **bio-research** | 臨床前研究工具：文獻檢索、基因體分析、標靶優先排序 | PubMed, bioRxiv, ClinicalTrials.gov, ChEMBL, Benchling, Open Targets |
| **cowork-plugin-management** | 建立/客製組織專屬 plugin（meta-plugin） | — |

後續還新增了 **engineering / human-resources / design / operations / small-business** 等職能 plugin。

### Partner-Built Plugin（廠商官方整合，部分）

`apollo`、`common-room`、`slack-by-salesforce`、`zoominfo`、`figma`、`miro`、`prisma`、`planetscale`、`cockroachdb`、`brightdata-plugin`、`zapier`（8,000+ apps）、`intercom`、`cloudinary`、`sanity-plugin`、`vanta-mcp-plugin`、`box`、`adobe-for-creativity`、`mintlify`、`sp-global`、`lseg`、`daloopa`、`bigdata-com` 等——涵蓋 CRM、資料庫、設計工具、web scraping、金融資料、合規平台。

## Plugin 結構（統一規範）

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest（清單）
├── .mcp.json                    # Tool connections（MCP server 設定）
├── commands/                    # 你顯式呼叫的 slash command
└── skills/                      # Claude 自動取用的領域知識
```

- **Skills** — 編碼領域專業、最佳實踐、step-by-step workflow。相關時 Claude 自動取用。
- **Commands** — 顯式觸發的動作，如 `/finance:reconciliation`、`/product-management:write-spec`、`/sales:call-prep`、`/data:write-query`。
- **Connectors** — 透過 MCP server 接外部工具（CRM、專案追蹤、資料倉儲、設計工具）。

以 `sales` plugin 為例，`skills/` 下有 `account-research`、`call-prep`、`call-summary`、`competitive-intelligence`、`daily-briefing`、`draft-outreach`、`forecast`、`pipeline-review` 等子技能，外加 `CONNECTORS.md`、`.mcp.json`。

## 快速開始

```bash
# Claude Code：先加市集，再裝特定 plugin
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install sales@knowledge-work-plugins
```

安裝後自動啟用——skill 在相關時觸發，slash command 在 session 中可用（如 `/sales:call-prep`、`/data:write-query`）。Cowork 則直接從 [claude.com/plugins](https://claude.com/plugins/) 安裝。

## 客製化（Making Them Yours）

官方明說這些是「通用起點」，客製後才真正有用：

- **Swap connectors** — 改 `.mcp.json` 指向你的工具棧
- **Add company context** — 把你的術語、組織結構、流程塞進 skill 檔
- **Adjust workflows** — 改 skill 指令貼合團隊實際做法（而非教科書做法）
- **Build new plugins** — 用 `cowork-plugin-management` plugin 或照結構自建

## 目前限制 / 注意事項

- **連接器依賴 MCP server**——多數職能 plugin 要真正發揮，得接上對應 SaaS 的 MCP（需各自授權、可能有費用）
- **「通用起點」≠ 開箱即最佳**——官方反覆強調 plugin 是 generic starting point，不客製就只是「textbook 做法」
- **主場是 Cowork**——雖相容 Claude Code，但部分能力（如完整的 connector 體驗）以 Cowork 為主要載體
- **partner-built plugin 品質與維護由廠商負責**——非 Anthropic 直接背書，使用前需評估
- **127 open issues**——生態擴張快、整合多，邊角問題不少

## 研究價值與啟示

### 關鍵洞察

1. **這是 Anthropic 對「skill/plugin 經濟」的官方下注**：相較社群的 Superpowers、Casper Skill Gallery 等是「個人/社群整理」，這個 repo 是 Anthropic 親自下場、定義 plugin 的標準結構（`.claude-plugin/plugin.json` + `.mcp.json` + `commands/` + `skills/`），並拉進數十家 SaaS 廠商做官方整合。它在為「plugin 成為 Claude 生態的分發單位」鋪路——類似 app store 之於手機。

2. **「純 markdown + JSON、零程式碼」是刻意的低門檻設計**：把整個 plugin 拆成「skills（自動取用的領域知識）+ commands（顯式動作）+ connectors（MCP 接線）」三類純文字檔，意味著**非工程師也能寫 plugin**。這是 Anthropic 對「knowledge worker 自己客製 AI」這個願景的具體實現——把 prompt engineering 民主化成「編輯 markdown」。

3. **plugin 的真正價值在「公司 context 的固化」**：最值得品味的一句是「The context you define gets baked into every relevant interaction, so leaders and admins can spend less time enforcing processes and more time improving them」。plugin 不只是工具集，而是**把公司流程/術語/最佳實踐編碼進 AI**，讓「流程執行」從人治變成 context-driven。這對組織的隱性知識管理是新範式。

4. **「Skill 自動觸發 vs Command 顯式呼叫」的二分很清晰**：skill 靠 description 自動 fire（Claude 判斷相關性），command 靠使用者主動 `/plugin:action`。這個分法跟本站研究過的 Superpowers、Andrej Karpathy Skills 等一脈相承，但這裡是把它制度化成「每個職能 plugin 都遵守同一結構」。

5. **職能（role）而非技術是分類軸**：plugin 按 sales/finance/legal/data/HR 等**工作職能**切分，而非按技術能力切。這反映 Cowork 的產品定位——目標客戶是「各部門的知識工作者」，不是開發者。這也是它與「Coding Agent 工具」最大的差異：它把 AI agent 的應用面從工程師擴展到全公司。

6. **生態從 11 → 49 的擴張速度說明 connector 才是護城河**：核心職能 plugin 約 10 個就飽和，但 partner-built（Apollo、ZoomInfo、Figma、Prisma、Zapier...）持續湧入。這顯示 plugin 競爭的關鍵不是 skill 本身（markdown 易複製），而是**誰能接上獨家資料源/工具**——connector（MCP 整合）才是真正的差異化與護城河。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [Superpowers](superpowers.md) / [Casper Skill Gallery](casper-claude-skill-design-gallery.md) | 社群整理的通用工程 skill，KWP 是 Anthropic 官方、按職能分、含 connector 與廠商整合 |
| vs [Claude Code Game Studios](claude-code-game-studios.md) | 都是「角色化 agent 集合」，但 Game Studios 是單一垂直領域（遊戲開發）的深度階層，KWP 是橫跨全公司職能的廣度市集 |
| vs [Claude Financial Services Plugins](claude-financial-services-plugins.md) | 同為 Anthropic 官方 plugin，但金融服務版聚焦單一行業，KWP 涵蓋通用知識工作職能 |
| vs [Claude Use Cases Gallery](claude-use-cases.md) | Use Cases 是「能做什麼」的展示，KWP 是「直接給你可裝的工具」的可執行版本 |
| vs [Webwright](webwright.md) | Webwright 是專精瀏覽器任務的單一強 skill（可跨 host），KWP 是按職能組織的廣度 plugin 市集 |
| vs [Zapier](https://github.com/...) 類整合 | KWP 內含 zapier plugin（接 8,000+ apps），顯示它定位為「整合的整合」——connector 的聚合層 |

**最大啟示**：Knowledge Work Plugins 標誌著 AI agent 應用從「開發者工具」向「全公司知識工作」的擴散。它的賭注是——**未來每家公司都會把自己的流程、術語、工具接線編碼成一套 plugin，讓 AI 成為「為這家公司量身打造」的跨職能專家**。而其中真正稀缺、可防禦的不是 skill（markdown 人人能寫），而是 connector（接上獨家資料與工具的 MCP 整合）。對任何想在 Claude 生態做產品的團隊，這指出一條清晰路徑：別只做 prompt/skill，要去擁有資料接點。
