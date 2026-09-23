---
date: "2026-09-23"
category: "社群行銷"
card_icon: "material-magnify-scan"
oneliner: "設計給 Claude Code 之類 AI coding agent 用的「全域行銷營運技能」，也能當 CLI 獨立跑。七大模式（SEO 顧問／工程師／資安／文章寫手／外掛開發／Meta 廣告／產圖）＋ 26 個 AI 角色的矩陣營運層，v0.4 起加了 SEO/AEO 引導式建站。設計原則是不綁定單一廠商、預設唯讀 dry-run、免金鑰可試玩。注意核心健檢有個 robots/sitemap 必定誤報的 bug 拖了兩個月，v0.4.6 才修。跟本站的反詐投資王同一位作者"
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
| GitHub repo（★301 / 31 forks / Apache-2.0） | <https://github.com/mars-tw/open-seo-advisor-skill> |
| 能力地圖 | [`docs/capability-map.md`](https://github.com/mars-tw/open-seo-advisor-skill/blob/main/docs/capability-map.md) |
| Skill 規格 | [`SKILL.md`](https://github.com/mars-tw/open-seo-advisor-skill/blob/main/SKILL.md)（24 KB） |
| 同作者的另一個專案（本站已有筆記） | [反詐投資王](anti-gambling-trader-tw.md) |

> **Metadata（2026-09-23 更新）**：**301 stars / 31 forks / 6 open issues** · **Apache-2.0** · 建立於 **2026-07-01**、最後 push **2026-09-21** · Python · 最新 **v0.4.6** · 分析 commit `05b464a` · 39 個 commit 全部出自作者一人。
>
> 初版筆記寫於 2026-09-15，當時基於 7 月的 `ada1a52`(v0.3.5)。本次更新補上 v0.4.0～v0.4.6 的變化，並實際安裝跑過。

## 一句話定位

> **把「資深 SEO 顧問 / 技術 SEO 工程師 / 資安人員 / SEO 內容編輯 / WordPress 外掛工程師」五種角色的方法論，蒸餾成可執行的檢查清單、報告格式與程式碼。**

它是設計給 [Claude Code](https://claude.com/claude-code) 這類 AI coding agent 用的 **Skill**，同時也可以當獨立 CLI。新手路徑只有一個指令：

```bash
seo-advisor auto https://你的網站.com
```

自動分析，產出白話懶人包 + 待辦清單。**預設只做分析、不花錢、不會改動你的網站。**

## 七大模式

| 模式 | 做什麼 | 狀態 |
|------|--------|:----:|
| **Consultant 顧問** | 全站 SEO 健檢，產出診斷報告與 P0–P3 優先順序 | ✅ |
| **Content Writer 文章寫手** | 呼叫 LLM（Anthropic / OpenAI / 本地模型皆可）產出符合 E-E-A-T 的內容 | ✅ |
| **Meta Ads 廣告優化** | 診斷 Meta 廣告帳戶，產出優化建議與 dry-run 行動計畫 | ✅ |
| **Image Material 產圖素材** | 為廣告／社群／文章產生圖像素材，provider 可換，有合規前置檢查 | ✅ |
| **Engineer 工程師** | 直接修 sitemap、robots.txt、canonical、hreflang、結構化資料、Core Web Vitals | ⚠️ |
| **Security 資安** | 檢查 SEO 相關資安風險（外洩檔案、過時 CMS、垃圾內容注入、惡意重導、HTTPS） | ⚠️ |
| **Plugin Dev 外掛開發** | 為 WordPress 等 CMS 開發 SEO 外掛 | ⚠️ |

!!! warning "三個 ⚠️ 模式的實作狀態，repo 裡有三種說法"
    初版筆記照 README 寫「七個做完四個」。這次裝起來實測(v0.4.6)，發現說法彼此矛盾：

    | 來源 | 說法 |
    |------|------|
    | README | 完整實作 Consultant、Content Writer、Meta Ads、Image Material 四個 |
    | CLI 的 `seo-advisor mode <名稱>` | 只有 consultant 和 content_writer 完整實作，其他「僅提供 prompt 模板」 |
    | CHANGELOG 與實際指令 | v0.2.1 Security、v0.3.5 Plugin Dev 標「正式上線」；`fix engineer`、`security audit`、`plugin dev` 指令都存在也能執行 |

    實際程式碼比文件走得快。README 和 `mode` 指令都沒跟上，要知道某個模式能不能用，直接看 `--help` 最準。

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

## v0.4 新增：SEO/AEO 引導式建站

2026-09-18 起的 v0.4.x 在原本的健檢、修復、寫文之外，多了一條「幫你蓋網站」的路線，指令是 `seo-advisor website`：

| 子指令 | 做什麼 |
|--------|--------|
| `init` | 回答四個問題，產出預設 noindex 的網站草稿 |
| `build` | 依 JSON brief 產出靜態網站，只寫進不存在的目錄 |
| `demo` | 虛構的「山嵐茶屋」示範，不呼叫 API、不付費生圖 |
| `check` | 離線檢查 SEO/AEO 基線；exit 0 代表通過、2 代表草稿待補、1 代表驗證失敗 |

網站分 sales、shop、experience 三型，會產出語意 HTML、metadata、JSON-LD、robots.txt、sitemap，還有 Cloudflare Workers、Firebase Hosting、GCP Cloud Run 的部署設定，但**不會自動部署也不會收款**。GPT 生圖、接金流、登入雲端這些都交給 agent 在使用者自己的帳號上做，CLI 本身不碰。

我實跑 `website demo` 加 `website check` 的結果：

- 產出的 `public/` 只有 60 KB，沒有外部 script，預設 `noindex,follow`。
- `check` 回 exit 2，15 項離線檢查全過，另外列出 5 項待補(canonical、GPT 素材、品牌事實確認等)。回報裡明講「不驗 DNS、不驗收錄、不驗無障礙」，沒有誇大自己檢查的範圍。

另一個賣點是「沉浸式捲動故事」頁：用宣告式的場景、角色路徑、原圖座標描述多幕敘事，支援倒帶、跳章、減少動態模式和無 JS 的靜態降級。附了兩個公開範例，一個是茶葉《一片葉的回家路》，一個是工筆媽祖畫像《一筆敬意》，都部署在 Cloudflare。

v0.4.5 也加了 [OpenCode](https://opencode.ai) 的安裝指南和可選的 `/seo-website` command 模板。CHANGELOG 註明是用 OpenCode 1.18.31 實測技能發現和指令解析，「未以付費推論驗證」，誠實程度跟前面一致。

!!! note "v0.4.0 CHANGELOG 的奇怪措辭"
    v0.4.0 標題寫「本地衍生版」，內文寫「此版本為使用者需求的衍生改作，未代表 upstream 已合併或發布」，`UPGRADE-REPORT.md` 也說「以 upstream `ada1a52` 為基礎」。但這就是作者自己的 upstream repo，commit 也都是作者本人推的。比較可能的解讀是作者讓 coding agent 做這輪改版，agent 產出的報告原封不動進了 repo。不影響功能，但讀文件時會有點困惑。

## 實測驗證(2026-09-23，v0.4.6)

| 項目 | 結果 |
|------|------|
| `pip install -e '.[dev]'` | 成功 |
| 完整 pytest | **1038 passed / 1 skipped**，37.7 秒 |
| `website demo` + `website check` | 正常，見上節 |
| `security audit` 掃本機 | 被擋下 |

`security audit` 有兩道防線值得一提。第一，必須用 `--confirm-authorized` 打出指定的確認字串，宣告你有權掃這個站。第二，預設不准掃私有網段、localhost 和雲端 metadata IP，避免被當成 SSRF 跳板，要掃自己內網得在程式裡明確打開 `allow_private_network`。我對本機示範站跑就被第二道擋下，這正是它該有的行為。

## 目前限制

- **核心健檢曾長期誤報。** Consultant 模式抓 robots.txt 和 sitemap.xml 時會把非 `text/html` 的回應內容丟掉，結果**任何正確設定這兩個檔的網站都會被誤報**，其中一項是 P1，分數還比沒放這兩個檔更低([#7](https://github.com/mars-tw/open-seo-advisor-skill/issues/7)、[#9](https://github.com/mars-tw/open-seo-advisor-skill/issues/9))。外部貢獻者 7-18 就送了修正 PR [#5](https://github.com/mars-tw/open-seo-advisor-skill/pull/5)，8-08 又有 [#8](https://github.com/mars-tw/open-seo-advisor-skill/pull/8)，作者到 9-21 的 v0.4.6 才用自己的實作修掉，兩個 PR 到現在還開著沒關。**v0.4.6 之前跑出的健檢報告，robots/sitemap 那兩項不能信。**
- **文件跟不上程式碼。** 模式實作狀態有三種說法，見上面的警告框。
- **維護節奏是一陣一陣的。** 7 月密集開發三週，7-13 之後停了兩個多月，9-18 又一口氣推了 v0.4.0～v0.4.6。初版筆記寫「之後停了」，現在看來只是暫停。dependabot 的 PR 也堆著沒處理。
- **一人專案。** 39 個 commit 全是作者本人，外部 PR 至今沒有被合併過。
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
| [OpenCode](opencode.md) | v0.4.5 起官方支援的第二個 agent 宿主 |
