---
date: "2026-09-15"
category: "社群行銷"
card_icon: "material-magnify-scan"
oneliner: "設計給 Claude Code 之類 AI coding agent 用的「全域行銷營運技能」，也能當 CLI 獨立跑。七大模式（SEO 顧問／工程師／資安／文章寫手／外掛開發／Meta 廣告／產圖）＋ 26 個 AI 角色的矩陣營運層，目前四個模式完整實作。設計原則是不綁定單一廠商、預設唯讀 dry-run、免金鑰可試玩。跟本站的反詐投資王同一位作者"
tags:
  - skills
  - marketing
  - automation
  - claude-code
---

# Open SEO Advisor（open-seo-advisor-skill）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★172 / 16 forks / Apache-2.0） | <https://github.com/mars-tw/open-seo-advisor-skill> |
| 能力地圖 | [`docs/capability-map.md`](https://github.com/mars-tw/open-seo-advisor-skill/blob/main/docs/capability-map.md) |
| Skill 規格 | [`SKILL.md`](https://github.com/mars-tw/open-seo-advisor-skill/blob/main/SKILL.md)（24 KB） |
| 同作者的另一個專案（本站已有筆記） | [反詐投資王](anti-gambling-trader-tw.md) |

> **Metadata（2026-09-15 抓取）**：**172 stars / 16 forks / 8 open issues** · **Apache-2.0** · 建立於 **2026-07-01**、最後 push **2026-07-22** · Python · **CHANGELOG 有 88 KB**（三週內開發密度極高）。

## 一句話定位

> **把「資深 SEO 顧問 / 技術 SEO 工程師 / 資安人員 / SEO 內容編輯 / WordPress 外掛工程師」五種角色的方法論，蒸餾成可執行的檢查清單、報告格式與程式碼。**

它是設計給 [Claude Code](https://claude.com/claude-code) 這類 AI coding agent 用的 **Skill**，同時也可以當獨立 CLI。新手路徑只有一個指令：

```bash
seo-advisor auto https://你的網站.com
```

自動分析，產出白話懶人包 + 待辦清單。**預設只做分析、不花錢、不會改動你的網站。**

## 七大模式（四個已完整實作）

| 模式 | 做什麼 | 狀態 |
|------|--------|:----:|
| **Consultant 顧問** | 全站 SEO 健檢，產出診斷報告與 P0–P3 優先順序 | ✅ |
| **Content Writer 文章寫手** | 呼叫 LLM（Anthropic / OpenAI / 本地模型皆可）產出符合 E-E-A-T 的內容 | ✅ |
| **Meta Ads 廣告優化** | 診斷 Meta 廣告帳戶，產出優化建議與 dry-run 行動計畫 | ✅ |
| **Image Material 產圖素材** | 為廣告／社群／文章產生圖像素材，provider 可換，有合規前置檢查 | ✅ |
| **Engineer 工程師** | 直接修 sitemap、robots.txt、canonical、hreflang、結構化資料、Core Web Vitals | 🚧 |
| **Security 資安** | 檢查 SEO 相關資安風險（外洩檔案、過時 CMS、垃圾內容注入、惡意重導、HTTPS） | 🚧 |
| **Plugin Dev 外掛開發** | 為 WordPress 等 CMS 開發 SEO 外掛 | 🚧 |

**七個講了四個做完**——README 誠實標出來，沒有把未完成的當成賣點。

### 上層：AI 矩陣營運系統

七大模式之上還有 `seo-advisor matrix`：提一句目標，**NORA 總控**判斷情境、派工給 **26 位 AI 工作夥伴角色**（策略／行銷／銷售／產品／營運／財務／人資／法務／行政）協作，各角色接到已實作的模式引擎，最後整合成一份可執行交付物。

```bash
seo-advisor matrix demo                                        # 免金鑰試玩
seo-advisor matrix run --goal "推廣新產品增加詢價" --industry 製造業
```

> **任何高風險任務（發布／花錢／部署）會被強制升級為需人工確認且只產計畫。** 這道閘是整個 matrix 層最重要的設計——26 個 agent 自由派工的系統，如果沒有這層，第一個意外就是有人的廣告帳戶被燒錢。

## 設計原則（這部分最值得抄）

- **不綁定單一廠商**：所有付費 API（Search Console、GA4、PageSpeed Insights、OpenAI、Anthropic、Cloudflare…）**都是 optional adapter，核心功能不依賴任何一個**。
- **預設唯讀、預設 dry-run**：任何寫入或部署動作都需要人工確認。成效分析的 Google 資料源（GA4 / GSC / Google Ads）**一律 read-only，無憑證時用 mock**。
- **可攜**：SSH、本地原始碼包／zip、Git repo、WordPress REST API、Cloudflare API、cPanel 都能接，透過統一的 `WebsiteConnector` 介面。
- **免金鑰可試玩**：幾乎每個模式都有 `demo` 子指令。

## 其他模組

**成長行銷**（`seo-advisor growth`）：UTM 歸因、CRO 落地頁優化、跨渠道成效分析，全部免金鑰可試玩。

**電商 Listing 健檢 + 行銷方法論知識庫**：內建**中性化蒸餾**的方法論知識庫（電商／付費廣告漏斗／內容品牌／成長駭客四領域共 **50 條**可執行檢核原則），用電商領域原則做 Amazon / 電商平台的 listing 健檢。

> **合規說明值得注意**：知識庫「萃取業界公開、廣泛認可的通用原則，轉成**不具名、不含課程名或商標**的檢核清單，不宣稱與任何特定專家有關聯或代言」。目的是讓任何人**免費**就能用這些方法論自我健檢，不需買課或代操。**這是一個處理『把付費課程方法論開源』這個灰色地帶的謹慎做法**——去識別化 + 明確聲明不代言。

## 輸出

掃描完產出四份報告：`report-beginner.md`（白話懶人包）、`report.md`（完整技術報告）、`report.json`（機器可讀）、`report.html`（含 Impact × Effort matrix、URL 狀態分布、hreflang 矩陣等圖表，可列印成 PDF）。

**同一份分析出四種受眾的格式**——老闆看懶人包、工程師看技術報告、程式讀 JSON、簡報用 HTML。

## 目前限制

- **七個模式只實作四個**，Engineer / Security / Plugin Dev 還沒完成——而 Engineer 模式（直接修技術 SEO 問題）恰好是很多人最想要的那個。
- **172★、最後 push 2026-07-22**，之後沒動。CHANGELOG 顯示 7 月那三週開發極密集，之後停了。
- **Meta Ads 模式動用真實預算的操作預設全鎖**，要自己解鎖——安全但也代表實際自動化程度有限。
- **內容以繁中為主**，有 `README.en.md` 但深度文件多半只有中文。
- 沒有 topics 標籤、star 數不高，**發現性差**——這類工具的價值往往要用過才知道。

## 研究價值與啟示

### 關鍵洞察

1. **「把專業角色的方法論蒸餾成可執行清單」是 agent skill 最實在的形態。** 這個專案沒有試圖讓 LLM「變成 SEO 專家」，而是把顧問實際會做的檢查步驟、報告格式、優先順序規則寫成程式與清單，**LLM 只負責需要語言能力的那部分**。這比「寫一個超長 system prompt 叫它扮演 SEO 專家」可靠得多。

2. **「不綁定單一廠商」做成 optional adapter，而不是寫在 README 裡的承諾。** 所有付費 API 都可以不接，核心功能照跑、沒憑證就用 mock——**這讓工具在「還沒決定要買哪家服務」的階段就能用**，而那正是大多數人開始評估 SEO 工具的時間點。

3. **26 個 agent 的矩陣層，真正的設計重點是那道強制人工確認的閘。** 多 agent 系統的風險不在協作品質，在於**某個 agent 在沒人看著的時候花了錢或發布了東西**。把「發布／花錢／部署」無條件升級為需確認且只產計畫，是這類系統該有的預設。對照本站 [Vibe-Trading](vibe-trading.md) 的 mandate gate、[AutoHedge](autohedge.md) 的完全沒有護欄，同一個問題的三種答案排在一起很清楚。

4. **「中性化蒸餾」是處理付費課程方法論的一個可參考做法。** 去掉姓名、課程名與商標，只留通用原則，並明確聲明不代言——既讓知識可用，又避開了冒用他人品牌的問題。**這個做法值得任何想把業界 know-how 開源的人參考。**

5. **同一位作者（mars-tw）的兩個專案共享同一種產品哲學**：[反詐投資王](anti-gambling-trader-tw.md) 是「預設你沒有優勢，要你舉證」＋ fail closed；這個是「預設唯讀、預設 dry-run，要花錢先問過」。**兩者都把『預設不做危險的事』寫進架構，而不是寫進說明書。**

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [反詐投資王](anti-gambling-trader-tw.md) | 同作者、同哲學（預設保守、危險動作要人工確認），不同領域 |
| [Claude SEO](claude-seo.md) | 同為 SEO 導向的 Claude 生態工具；那個是 25 個 sub-skill 的集合，這個是單一 CLI + 七模式架構 |
| [Vibe-Trading](vibe-trading.md) | mandate gate vs. 強制人工確認閘——**都在解「agent 可能花你的錢」這個問題** |
| [社群自動發文 skill](skill-social-post.md) | 同屬行銷自動化 agent skill；可與本專案的 Content Writer 模式串接 |
