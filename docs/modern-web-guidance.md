---
date: "2026-11-12"
category: "Coding Agent 工具"
card_icon: "material-web"
oneliner: "Chrome 團隊（加上 Edge、Firefox、MDN）出的 coding agent skill：agent 寫前端前先用本機 CLI 搜 209 篇現代 Web 指南，拿到 dialog、popover、anchor positioning 這類原生寫法和 Baseline 相容資料，避免它照訓練資料寫舊式 JS；官方 eval 說能把通過率從五成多拉到八、九成"
tags:
  - agent-skill
  - frontend
  - web-platform
  - google
  - claude-code-plugin
---

# Modern Web Guidance（GoogleChrome/modern-web-guidance）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 發佈 repo（skill 本體） | [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) |
| 原始碼 repo（指南原稿、CLI、eval） | [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) |
| 官方文件 | [developer.chrome.com/docs/modern-web-guidance](https://developer.chrome.com/docs/modern-web-guidance) |
| Eval 儀表板 | [googlechrome.github.io/modern-web-guidance-src](https://googlechrome.github.io/modern-web-guidance-src/) |
| npm | [modern-web-guidance](https://www.npmjs.com/package/modern-web-guidance) |

| 指標 | 數值 |
|------|------|
| Stars / Forks | 發佈 repo ~5.4K / 180；src repo ~2K / 149（2026-11-12） |
| 建立 | src 2026-01-27、發佈 repo 2026-03-23，npm 首版 2026-04-30 |
| 最後更新 | 2026-11-10（幾乎天天在發） |
| 內容量 | `modern-web-guidance` 209 篇指南 + `chrome-extensions` 23 篇參考，涵蓋 250 個 web feature |
| License | 程式 Apache-2.0、指南內容 CC-BY 4.0 |
| 需求 | Node ≥ 22 |

## 一句話

LLM 的訓練資料裡舊式前端寫法太多，叫 agent 做個 modal 它就給你 `div` + z-index + 一堆 JS。這個 skill 讓 agent **動手前先查**：用 CLI 搜一篇對應的指南，拿到用 `<dialog>`、Popover API、anchor positioning、`@starting-style` 這類原生功能的寫法，連 fallback 和瀏覽器支援度一起塞進 context。

維護方是 Chrome 團隊，掛名的還有 Edge、Firefox、MDN，算是瀏覽器廠商官方背書的「前端版 [Context Hub](context-hub.md)」。

## 怎麼運作

```
agent 接到前端任務
   │  SKILL.md 寫著「MANDATORY: Execute FIRST」
   ▼
npx -y modern-web-guidance@latest search "light dismiss dialog"
   │  本機 hybrid 搜尋，回 10 筆 {id, description}
   ▼
npx -y modern-web-guidance@latest retrieve "<id>"
   │  吐出整篇指南 markdown（>9.5KB 自動寫到 /tmp 檔，叫 agent 自己讀）
   ▼
照指南寫 code → 回頭對照指南檢查 → 回覆最後加一段「### Modern Web Guidance」說明套了哪篇
```

SKILL.md 本身只有約 205 tokens 的 description，平常不佔 context，真的要用才去撈指南。

### 搜尋是完全離線的

`src/rag/` 做的是 dense + BM25 混合檢索，有幾個設計很細：

- **非對稱 embedding**：指南 chunk 在 build 時用 `gemini-embedding-001` 算好向量（256 維、int8 量化）直接打包進 npm；查詢端用從 Gemini 蒸餾出來的靜態詞表（Model2Vec 做法），一次查詢約 30 µs，不用跑 transformer、不用 API key。
- 他們實測過對稱做法會「cone collapse」：長文件平均後全擠在同一個方向，「best pizza in new york」跟 `<dialog>` 的 cosine 也有 0.899。所以才拆成文件用大模型、查詢用小詞表。
- 兩邊排名用 RRF（k=60）融合；BM25 零命中且 dense 分數 < 0.30 就直接回 `[]`，讓不相關的查詢乾淨地落空。
- 為了配合 Claude Code、Codex 會把 >10KB 的工具輸出從中間截斷，`retrieve` 超過 9.5KB 會自動寫到 `/tmp/mwg-guide-*.md`。這是專門針對 agent harness 行為調的。

### 指南長什麼樣

每篇指南有 frontmatter 標 `web-feature-ids`（對到 [web-features](https://web-platform-dx.github.io/web-features-explorer/) 的 ID）和相關指南，內文是 vanilla HTML/CSS/JS 的完整實作，加上「MANDATORY」註解標出 agent 最常漏的細節（例如 dialog 一定要有 accessible name）。

以 `navigation-drawer` 為例：用 `<dialog>` + `showModal()` 進 top layer，滑動手勢交給 CSS scroll-snap 的兩個停點，背景變暗用 scroll-driven animation 綁捲動位置，`IntersectionObserver` 判斷開關。整個沒有任何 pointer event 程式碼，還先教你判斷「只是 drawer」還是「寬螢幕會變 sidebar」要選不同元素。

分類大概是：

| 類別 | 篇數 | 類別 | 篇數 |
|------|-----:|------|-----:|
| ui-behaviors | 40 | security | 17 |
| performance | 26 | ui-atoms | 13 |
| ui-components | 22 | html | 8 |
| visual-design | 22 | built-in-ai | 5 |
| forms | 19 | js | 5 |
| css | 18 | 其他（a11y、pwa、wasm、webmcp…） | 14 |

### 相容性和實驗功能

- 預設假設 **Baseline Widely available** 的功能可以直接用，其他都要照指南寫 fallback。fallback 原則是「自己寫 < 50 行」或條件載入 polyfill，不塞大套件。
- 可以在 `AGENTS.md` / `CLAUDE.md` 寫自己的瀏覽器政策（例如「Safari 17.4+」或「不要 polyfill」），SKILL.md 有教 agent 怎麼依政策砍 fallback。
- Origin Trial 和「volatile」（單一引擎、三個月內才出）的功能，`search` 找得到但 `retrieve` 會擋，要在專案根目錄放 `.mwgrc` 開 `allowOriginTrials` / `allowVolatileFeatures` 才拿得到。

### legacy-scan

另一個用法是 `legacy-scan <path> --json` 掃整個 codebase 找舊寫法，每條結果附 `keepWhen` / `dropWhen` 判斷準則讓 agent 過濾誤判。只涵蓋約 20% 的指南（有確定性規則的那些），SKILL.md 也明講只有在使用者要「全面現代化」時才跑。

## Eval

這是整個專案最紮實的部分。流程是：

1. 拿兩個真實的 base app（`daily-grind`、`devtools-times`），出像「讓我的圖片載快一點」這種**不點名 API** 的任務。
2. 每個任務寫 Playwright grader，檢查原始碼、computed style、DOM 行為和 a11y 狀態。
3. grader 先校準：對多家 agent 寫的標準答案要 100% 通過，對沒改過的 base app 要 100% 失敗。
4. 跑 agent 有/沒有 skill 兩種模式比通過率。沒 skill 也能過的建議就砍掉，省 token。

最近一輪（2026-11-08，約 215 個任務、1,800 個 assertion）：

| Agent + 模型 | 沒 skill → 有 skill |
|------|------|
| Claude Code（opus-5-5） | 57% → 88%（+31pp） |
| Codex CLI（gpt-6.1-sol） | 54% → 82%（+28pp） |
| Antigravity（gemini-4-argon） | 58% → 94%（+36pp） |

提升幅度很一致，三家都在 +30pp 上下。要注意這是自己出題自己改，任務也是照指南涵蓋範圍設計的，數字代表「指南有寫到的地方 agent 會照做」，不代表一般前端任務都會好這麼多。

## 安裝

```bash
# 互動式安裝（會問要裝哪些 agent、哪些 skill pack）
npx modern-web-guidance@latest install

# Claude Code plugin
/plugin marketplace add GoogleChrome/modern-web-guidance
/plugin install modern-web-guidance@googlechrome

# 其他：npx skills add、gh skill install、Codex、Antigravity、Copilot CLI、Grok、Kimi 都有
```

## 要注意的地方

- **遙測預設開啟**：會送安裝次數、呼叫的 agent 名稱、retrieve 的指南 ID，還有 **agent 產生的搜尋字串**給 Google（說不收原始 prompt）。關掉要設 `DISABLE_TELEMETRY=1`。搜尋字串可能帶出你在做什麼功能，公司專案建議關。
- **每次都跑 `npx …@latest`**：好處是指南永遠最新，代價是每次查詢都執行 npm 上當下最新版的程式碼，等於信任 Google 的 npm 發佈流程。官方說套件零相依、16MB 全打包，供應鏈面相對單純，但要鎖版本得自己改 SKILL.md。
- **觸發很積極**：description 寫「MANDATORY: Execute FIRST for all HTML/CSS and clientside JS tasks」，裝了之後幾乎所有前端任務都會先跑一兩次 npx，第一次還要網路下載。小改動會多一點延遲。
- **回覆會多一段**：Step 4 規定 agent 回覆最後要加 `### Modern Web Guidance` 段落列出套了哪篇、引用原文。想要乾淨輸出的話要知道這是 skill 刻意的設計。
- 指南都是 vanilla 寫法，SKILL.md 有教怎麼搬到 React（`useId()` 產 anchor-name、新 HTML 屬性用 `as any` 塞），但框架整合仍要靠 agent 自己判斷。

## 我的看法

適合常叫 agent 寫前端的人，尤其是 modal、popover、表單驗證、view transition、CWV 優化這類「原生已經有解、但 agent 習慣自己刻」的東西。內容由瀏覽器廠商維護、有 Baseline 資料和 Playwright eval 撐著，可信度比一般社群 skill 高很多。

CLI 的檢索設計也值得參考：如果要做自己的「知識庫型 skill」，「文件端用大模型、查詢端用蒸餾詞表、全打包進 npm 離線跑」是個好模板，比接 vector DB 輕很多。

沒實際跑過 CLI（`npx` 執行在本機被擋），以上行為是讀 SKILL.md 和 `modern-web-guidance-src` 原始碼整理的。

## 相關筆記

- [Context Hub](context-hub.md)：同樣是「給 coding agent 查策展文件」，範圍是第三方 API
- [design-md-chrome](design-md-chrome.md)、[Awesome DESIGN.md](awesome-design-md.md)：前端設計面的 agent 素材
- [microsoft/skills](microsoft-skills.md)：另一家大廠官方出的 skill 集
