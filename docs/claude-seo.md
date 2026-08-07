---
date: "2026-08-07"
category: "社群行銷"
card_icon: "material-magnify"
oneliner: "Claude Code SEO skill：25 sub-skills + 18 專家 agent 並行跑技術 SEO、E-E-A-T、Schema、GEO/AI 搜尋、本地/電商/國際 SEO；每條建議都附『怎麼知道它失敗了』的可證偽檢查"
tags:
  - skills
  - marketing
  - claude-code
  - automation
---

# Claude SEO（claude-seo）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/AgriciDaniel/claude-seo> |
| 官方首頁 | <https://claude-seo.md> |
| 作者 | Daniel Agrici（Rankenstein / AI Marketing Hub） |
| 同作者姊妹工具 | [Claude Ads](claude-ads.md)（廣告審計）· [Codex SEO](https://github.com/AgriciDaniel/codex-seo)（Codex 版移植） |
| 社群（Pro，私有 mirror） | <https://www.skool.com/ai-marketing-hub-pro> |
| Demo | [YouTube](https://www.youtube.com/watch?v=COMnNlUakQk) |

> Metadata（研究當下）：**13,531 stars / 1,974 forks** · Python · MIT · 建立於 2026-02-07 · 410 tests passing。需 Claude Code 1.0.33+。

## 專案概述

**Claude SEO 是一個開源的 Claude Code SEO 分析 plugin/skill**。它把一次 SEO 稽核拆成 **25 個 sub-skill + 18 個專家 agent**,在技術 SEO、內容品質（E-E-A-T）、Schema.org、AI 搜尋優化（GEO）、本地 SEO、電商、國際 SEO 等面向**並行**跑（全站稽核可同時 spawn 到 **15 個 agent**,分鐘級完成本來要數小時的工作）。最終產出一份**排序過的行動計畫**,每條建議都以 Google 一手指引為依據。

它是本站同作者 [Claude Ads](claude-ads.md)（250+ 項跨平台廣告審計）的**姊妹作**——同一套「把某個行銷專業領域打包成 Claude Code skill」的思路,這次做的是 SEO。並有 [Codex SEO](https://github.com/AgriciDaniel/codex-seo)（Codex-first 移植,TOML agent + deterministic runner）。

**兩個版本**:公開開源版（`AgriciDaniel/claude-seo`,MIT、無會員門檻）與社群私有 mirror（`AI-Marketing-Hub/claude-seo`,早期功能 + 社群協作,需會員）——一種 open-core + 付費社群的變體。

## 核心賣點

| 賣點 | 內容 |
|------|------|
| **AI-search first** | 對齊 Google 的 AI Optimization Guide；做 question-based citability 評分、llms.txt 的一手證據立場、AI 生成圖的 IPTC `TrainedAlgorithmicMedia` 標記、agent-friendly 頁面檢查 |
| **並行執行** | 全站稽核 fan out 到 15 個專家 agent 同時跑,分鐘級 |
| **可證偽而非推銷** | 每條建議都帶:它立足的 first-principle 觀察、與其他建議的依賴關係、一個「how would we know this failed?」檢查、一個 leading indicator |
| **本地優先** | 預設不呼叫任何第三方 API（只抓你指定的目標 URL）；資料不離開機器；輸出是本地 markdown/PDF/JSON;無 lock-in |

### 32 個 `/seo` 指令(節選)

`/seo audit`（全站並行）、`page`、`technical`（9 類）、`content`（E-E-A-T）、`content-brief`、`schema`（偵測/驗證/生成 JSON-LD）、`geo`（AI Overviews/GEO）、`local`（GBP/citations/reviews）、`maps`（geo-grid 排名、競品半徑）、`hreflang`（國際化）、`google`（GSC/PageSpeed/CrUX/Indexing/GA4）、`backlinks`（Moz/Bing/Common Crawl）、`cluster`（SERP 語意分群）、`sxo`、`drift`（SQLite 快照做回歸監測）、`ecommerce`、`programmatic`…，外加 8 個 MCP 擴充（Firecrawl、DataForSEO、Ahrefs、SE Ranking、Profound、Bing、Unlighthouse、Banana 圖片生成）。

## 技術架構

- **遵循 Agent Skills 標準的 3 層架構**（directive → orchestration → execution）；skill 與 agent 從 `skills/seo-*/` 與 `agents/seo-*.md` **自動探索**。
- **orchestrator**（`skills/seo/SKILL.md`）負責:產業偵測（SaaS / local / ecommerce / publisher / agency）→ 最多 15 個 sub-agent 並行派發 → 用 10-principle 框架 synthesize → 產出行動計畫。
- **隔離 runtime**:`/seo setup` 在 Claude 的持久 plugin data 裡建**獨立 Python 環境 + Playwright Chromium**,不動全域 Python、不建 PATH shim;`/seo doctor` 檢查健康。
- **憑證分層（Tier 0–3）**:Tier 0 只要 API key（PageSpeed/CrUX/25 週趨勢）；Tier 1 加 OAuth（Search Console + Indexing）；Tier 2 加 GA4；Tier 3 加 Ads token（Keyword Planner）。憑證存 `~/.config/claude-seo/`、`0o600` 權限、不進 repo。
- **報告產出**:markdown 為主（`FULL-AUDIT-REPORT.md`、`SCHEMA-REPORT.md`、`GEO-ANALYSIS.md`…）+ WeasyPrint + matplotlib 生 A4 PDF（全站稽核約 32 頁）。

### 10-principle 方法論(四階段)

| 階段 | 原則 | 做什麼 |
|------|------|--------|
| **PERCEIVE** | OBSERVE(外/內) · LISTEN | 收原始訊號、審自己的假設、讀 SERP/品牌/社群真正在說什麼 |
| **ANALYZE** | THINK · CONNECT(lateral/system) | 化約到 first principles、找跨 skill 的非顯性連結、排成依賴圖 |
| **VALIDATE** | FEEL · ACCEPT | 對 UX/品牌/團隊產能壓測、浮現可證偽性 |
| **ACT** | CREATE · GROW | 產出成品、設下一輪稽核的回饋迴路 |

## 值得注意的「時效性正確」細節

這個 repo 對 SEO 領域的**時效知識更新**做得異常認真,反映在很多硬編的日期事實:

- **Core Web Vitals 只認 LCP/INP/CLS**;INP 於 2024-03-12 取代 FID、2024-09-09 從 Chrome field 工具移除,**全程不提 FID**。
- **FAQPage**:Google 於 **2026-05-07** 對所有站點停止顯示 FAQ rich results → 標記為無 Google 效益。
- **已淘汰 schema**:HowTo（2023-09）、SpecialAnnouncement（2025-07）、ClaimReview、CourseInfo carousel 等（2025-06 退場）**一律不推薦**。
- **E-E-A-T** 對齊 2025-09 版 Search Quality Rater Guidelines（YMYL 已擴及政治/社會議題）。
- **GEO/AEO = SEO 的 reframe**:直接引用 Google 說法「AEO/GEO 只是 SEO 的改名」,並用一手證據破三個迷思（llms.txt 目前非 citation 槓桿、不需 content chunking、不需 AI 專用關鍵字改寫）。

## 目前限制 / 注意事項

- **重度 client-side hydration 的頁面**:headless renderer 多數 SPA 可處理（`--render auto` 偵測空 `<div id="root">` 就切 Playwright），但「滾動到 fold 以下才 hydrate」「互動後才抓內容」「第三方 widget race condition」等 edge case 仍會有雜訊,需手動觸發 `seo-visual` subagent 比對。
- **免費層無 enrichment**:預設不呼叫第三方 API,沒有 Google 憑證時 Core Web Vitals 只是 lab 估計、indexation 靠頁面訊號推斷;競品/AI-citation 資料要各自的 Ahrefs/DataForSEO 等帳號。
- **仍需 Claude Code 訂閱 + Python/Playwright 環境**:雖然 skill 免費,底層算力與環境門檻仍在。
- **開源版 vs 私有社群版**:最新功能先進私有 mirror,公開版是穩定落後版;要早期功能需付費會員。
- **成效圖表是作者自站案例**:README 的 GSC 成長圖來自作者自己的站,屬 anecdote 而非對照實驗,別當普適保證。

## 研究價值與啟示

### 關鍵洞察

1. **「可證偽性」被做成每條建議的強制欄位,是 SEO 工具裡罕見的科學態度**——每個 recommendation 都要回答「how would we know this failed?」並附 leading indicator。多數 SEO 稽核工具給的是「wall of findings」清單;把**否證條件**與**先行指標**綁進輸出,等於逼工具（和使用者）區分「有依據的判斷」與「推銷式廢話」。這是任何 AI 分析類工具都該抄的輸出契約。

2. **並行 sub-agent 是「稽核從季度變週度」的關鍵槓桿**——把一次稽核拆成 25 skill / 15 並行 agent,把時間從 4–8 小時（人工）壓到 10–15 分鐘。這讓「稽核頻率」而非「單次深度」成為新的競爭維度:同樣人力做到 4× cadence,再配 `/seo drift` 的 SQLite 快照做回歸監測,對話從「看這張快照」變成「這週變了什麼」。

3. **對「時效知識」的執著,是 LLM 領域工具的護城河**——SEO 規則變動極快（FID→INP、FAQ rich result 下架、schema 大量退場）。這個 repo 把日期級事實硬編進 skill 並附一手來源,正好對抗 LLM「知識停在訓練截止日」的通病。**skill 的價值不只是流程,更是把易腐的領域知識持續更新並落地**——這點與 [gs-quant](gs-quant.md) 用 skill 打包「怎麼正確用 SDK」異曲同工。

4. **GEO/AEO = SEO 的 reframe,是難得的「反炒作」立場**——當市場瘋炒 GEO/AEO/llms.txt,這個工具引用 Google 一手說法指出它們只是 SEO 改名、並用證據破迷思。在充斥「AI 搜尋新紀元」行銷話術的領域,**敢說「這其實沒變」比追新名詞更可信**。

5. **「把一個行銷專業打包成 Claude Code skill」正在成為一種產品範式**——同作者的 [Claude Ads](claude-ads.md)（廣告）、Claude SEO（SEO）、Codex SEO（跨 harness 移植）構成一個系列。對照 [mattpocock-skills](mattpocock-skills.md)（工程）、[gs-quant](gs-quant.md)（量化）,可見 **skill 不再只服務 coding,而是各垂直專業把「專家工作流」商品化的載體**;而「開源版 + 付費社群早期版」則是這類 skill 作者常見的變現路徑。

6. **本地優先 + 明確的憑證分層,是對「資料主權」的產品化回應**——預設零外呼、資料不離機、輸出是你的本地檔案、MIT 無 lock-in,並用 Tier 0–3 讓使用者**自行決定用多少外部資料換多少能力**。相較把資料上傳 vendor dashboard 的商業 SEO 工具,這是把信任邊界交回使用者手上;與 [qm](qm.md) 的 posture 分層、[headroom](headroom.md) 的本地壓縮同屬「資料主權即賣點」的一脈。

### 與其他專案的關聯

- **與 [Claude Ads](claude-ads.md)（同作者）**:一個做廣告審計、一個做 SEO,同一套「行銷專業 → Claude Code skill」方法論的兩個實例,建議並讀理解作者的產品套路。
- **與 [mattpocock-skills](mattpocock-skills.md)、[gs-quant](gs-quant.md) 的 skill 生態**:三者分別代表 skill 在**行銷 / 工程 / 量化**三個垂直的落地;Claude SEO 的「orchestrator + 自動探索 sub-skill + 並行 agent」架構,是本站看過**單一領域內最龐大**的 skill 集合。
- **與 [qm](qm.md)、[headroom](headroom.md) 的資料主權對照**:三者都把「資料留在本地/使用者掌控」當顯性賣點,反映一條與「上傳到 vendor」相反的產品哲學。
- **與 AI 搜尋/RAG 主題**:`/seo geo` 對 AI Overviews 的 citability 評分,與本站 RAG/AI 搜尋類筆記可對讀——它是從「被 LLM 引用」這端反推內容該長什麼樣。
