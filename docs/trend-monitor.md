---
date: "2026-05-29"
category: "AI 應用"
card_icon: "material-trending-up"
oneliner: "dongzhang84 個人專案，每日自動聚合 6 個 AI/科技趨勢來源（Product Hunt/Toolify/TAAFT/Chrome ExtensionStore/GitHub Trending/HN），email + GitHub Pages dashboard 雙輸出，亮點是「Indie Opportunity Analysis」對每個產品做 4 維評分 + 前 5 名 8 題深度分析"
tags:
  - github-actions
  - automation
---

# Trend Monitor 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/dongzhang84/trend-monitor> |
| Live Dashboard | <https://dongzhang84.github.io/trend-monitor/> |
| License | MIT |
| 維護者 | [dongzhang84](https://github.com/dongzhang84) |
| 建立 / 更新 | 2026-01-31 建立，每日自動執行 |

## 專案概述

**Trend Monitor** 是 dongzhang84 開發的個人趨勢監控工具（6 stars / 4 forks，Python，MIT），看似小專案但設計頗具參考價值。定位是「**每日商業機會發現工具**」——從 6 個 AI/科技趨勢來源自動聚合資料，每天早上把整理好的 digest 寄到信箱、同時更新公開 dashboard。

最大的差異化在於它不只是「聚合+顯示」，而是內建一套**「Indie Opportunity Analysis」**——對每個產品做 4 維評分，挑出前 5 名做 8 題深度商業分析，並給出「💡 First Step」一句具體可執行的驗證動作。換言之，它把「看趨勢」這件事做成「為獨立開發者找下個產品點子的研究助理」。

關鍵特色是 **零成本架構**：免費 API + GitHub Actions + GitHub Pages，不用付任何雲端服務費。

## 6 大資料來源

| 來源 | 收集欄位 |
|------|---------|
| **Product Hunt** | 產品名、tagline、連結 |
| **Toolify.ai** | 最新 + 趨勢工具（含月訪問量、成長率） |
| **There's An AI For That** | AI 工具名、描述、分類、連結 |
| **Chrome Extensions** | 擴充功能名、描述、使用者數、評分 |
| **GitHub Trending** | repo 名、描述、當日 star 增量 |
| **Hacker News** | 標題、作者、score、評論數 |

Toolify 用 **Playwright**（繞 Cloudflare），其他多為一般爬蟲/API。

## 雙 Dashboard + Email 三輸出

每次執行產出 4 個檔案：

| 檔案 | 角色 |
|------|------|
| `report.md` | Markdown digest（本地參考） |
| `docs/index.html` | 深色主題產品 dashboard（GitHub Pages） |
| `docs/indie.html` | Indie 商機 dashboard（GitHub Pages） |
| `analysis/daily/{date}-indie.md` | Indie 分析 Markdown（CI 自動 commit） |

兩個 dashboard 互相連結（index ↔ indie）。

## Indie Opportunity Analysis（最有趣的設計）

針對「獨立開發者找商機」的痛點，做了一條完整的篩選 → 評分 → 深度分析 pipeline：

### Step 1: Filter（先剔除不適合單兵的）

排除：B2B（enterprise / churn / SSO / CRM）、過於複雜領域（區塊鏈 / 硬體）、機構性工具、GitHub libraries（用 `npm install` 等安裝指令判別）。

### Step 2: Score（4 維度 1-5 分）

| 維度 | 意義 |
|------|------|
| `tech_difficulty` | 建造難度 |
| `user_acquisition` | 自然擴散程度 |
| `revenue_potential` | 利基貨幣化潛力 |
| `indie_friendly` | 單人能否出貨並維護 |

### Step 3: Deep-dive（前 5 名做 8 題分析）

| # | 題目 |
|---|------|
| 1 | 誰是用戶？（persona + B2C/B2B） |
| 2 | 他們為什麼需要？（pain point + 產品自述） |
| 3 | 它如何找到用戶？（distribution channel） |
| 4 | 賺不賺錢？多少？（model + 收入估計） |
| 5 | 我能學到什麼？（positioning insights） |
| 6 | 一句話 pitch |
| 7 | 我能不能做？（技術可行性） |
| 8 | 我如何找用戶？（具體戰術） |

每篇分析以 **💡 First Step** 收尾——一個具體可執行的驗證/起步動作。

### Domain Awareness

分析器從產品描述偵測 **14 個產品領域**（占卜、瀏覽器擴充、圖像生成、開發者工具、生產力等），針對該領域給出**領域特定**建議——而非通用陳腔。

## 週報設計

每週日 22:00 PST 自動跑 `weekly_report.py`：
- **Repeated Items** — 一週內多次出現的產品（持續熱度）
- **New Discoveries** — 只出現一次的獨家發現
- **Keyword Analysis** — 跨來源前 10 熱門關鍵字
- **Category Statistics** — 分類分佈

`--days 14` 可分析自訂時長。

## 自動化排程（GitHub Actions）

- **Daily Reports**：每天 7:00 AM PST → email + HTML dashboard + commit 回 repo
- **Weekly Reports**：每週日 22:00 PST → 趨勢分析 email

Repository Secrets：`EMAIL_SENDER`、`EMAIL_PASSWORD`（Gmail App Password）、`EMAIL_RECEIVER`、`SMTP_SERVER`、`SMTP_PORT`。

## 專案結構

```
trend-monitor/
├── main.py                 # Daily report 入口
├── weekly_report.py        # Weekly report 入口
├── collectors/             # 6 個來源各一個爬蟲模組
│   ├── github_trending.py
│   ├── product_hunt.py
│   ├── hackernews.py
│   ├── theresanaiforthat.py
│   ├── chrome_extensions.py
│   └── toolify.py          # Playwright（繞 Cloudflare）
├── reporters/              # Markdown / Weekly / HTML 三種報表
└── senders/email_sender.py
```

## 目前限制 / 注意事項

- **個人專案、6 stars** — 維護由單人，無社群保證；建議當「設計藍圖」而非「直接套用」
- **依賴 Gmail SMTP + App Password** — 換信箱要改設定，且 Gmail App Password 是專屬機制
- **Toolify 用 Playwright 繞 Cloudflare** — 對方更新反爬蟲機制可能失效
- **TAAFT / Product Hunt 等網站結構變動會壞** — 沒有 API 的來源都有此風險
- **「Indie 評分」由 LLM 完成（推測）但 README 未明說模型** — 評分品質取決於底層 LLM 與 prompt
- **是「個人 dashboard」而非 SaaS** — 多帳號分發、共享、付費版皆無

## 研究價值與啟示

### 關鍵洞察

1. **「Aggregator + Opinionated Analysis Layer」是個人工具勝過商業 dashboard 的範式**：純聚合（看 Product Hunt + GitHub Trending）大家都會，但這個專案在聚合上**疊加一層獨立開發者視角的篩選 + 評分 + 深度分析**。這是個人工具的勝場——商業 dashboard 為了通用會避免主觀立場，個人工具反而能放心地說「B2B 我不看、需要 `npm install` 的 library 不算商機」。

2. **「8 題深度分析」本質是 YC/IndieHackers 框架的程式化封裝**：誰是用戶 / 為何需要 / 怎麼找用戶 / 賺多少錢 / 一句話 pitch / 我能不能做——這是 YC office hours 與 IndieHackers 社群長年累積的「驗證問題清單」，被作者壓縮成可批次跑的提示。**把成熟的人類框架封裝成 LLM prompt 是 AI 時代知識工人的核心技能**。

3. **「💡 First Step」一句話收尾是 actionable 設計的精髓**：分析報告最大的失敗模式是「讀完很有道理但不知道要做什麼」。強制每篇以「一個具體可執行的驗證/起步動作」收尾，把 insight 變成 next action。任何做 AI 顧問/分析工具的人都該抄這條設計。

4. **Domain Awareness 是 generic LLM 答案的解藥**：偵測 14 個產品領域並給「領域特定建議」，避免「每個分析看起來都一樣」的陳腔病。這呼應本站 [Knowledge Work Plugins](knowledge-work-plugins.md) 的 path-scoped rules、[Claude Code Game Studios](claude-code-game-studios.md) 的 path-scoped 規範——**讓 prompt 隨情境就近啟動，比全域萬用 prompt 更精準**。

5. **「零成本架構（免費 API + Actions + Pages）」是個人 SaaS 的範本**：每日跑批次 + 公開 dashboard + email 推送，整套不花錢。這是 GitHub 生態最被低估的隱形 SaaS 平台——對任何「想自動化又不想付雲端費」的人，這個 stack 值得學起來。

6. **「Repeated Items 顯示持續性 vs New Discoveries 顯示新意」是時間維度的雙視角**：週報同時呈現「一週內多次出現＝市場驗證」與「只出現一次＝獨家信號」，避免陷入單一視角。這個資料切法值得抄到任何趨勢/監控類產品。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [Awesome OpenClaw Skills](awesome-openclaw-skills.md) | 都在做「資訊過載時的策展層」，但本專案是**動態自動**策展（每日跑 LLM 分析）、後者是人工 awesome-list |
| vs [Daily Stock Analysis](daily-stock-analysis.md) | 同樣「每日自動批次 + email + 結構化分析」，但領域不同（股票 vs 商機） |
| vs [Office Hours skill (gstack)](https://github.com/...) / YC 框架 | 同樣是「驗證商機的問題清單」，但這個專案是把人類框架封裝成自動化 pipeline |
| vs [Career-Ops](career-ops.md) | 都是個人化自動化工具，本專案聚焦商機發現，Career-Ops 聚焦職涯運維 |

**最大啟示**：Trend Monitor 是「個人化 AI 工具」的優秀範本——技術上沒有複雜創新，但在**「聚合 + 立場明確的篩選 + 框架化深度分析 + actionable next step」**這個產品設計鏈條上做得到位。它證明，AI 時代知識工人的核心競爭力不是「能寫 LLM 程式」，而是**「能把成熟的人類分析框架（YC / IndieHackers / 商機評估）程式化、自動化、並注入領域感知」**。任何想做「個人 SaaS / 知識自動化」的人，這 6-stars 的小專案是值得細讀的參考設計。
