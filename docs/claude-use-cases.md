---
date: "2026-03-30"
category: "學習資源"
icon: "material-clipboard-list-outline"
oneliner: "Anthropic 官方 Use Cases 資料庫——13 行業 × 7 功能 × 4 產品線，從 Cowork 桌面代理到法務合約紅線的全景案例集"
---
# Claude Use Cases Gallery 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方 Use Cases 首頁 | [claude.com/resources/use-cases](https://claude.com/resources/use-cases) |
| 探索頁 | [Explore what Claude can do for you](https://claude.com/resources/use-cases/explore-what-claude-can-do-for-you) |
| Cowork 分類 | [claude.com/resources/use-cases-category/cowork](https://claude.com/resources/use-cases-category/cowork) |
| Legal 分類 | [claude.com/resources/use-cases-category/legal](https://claude.com/resources/use-cases-category/legal) |
| Marketing 分類 | [claude.com/resources/use-cases-category/marketing](https://claude.com/resources/use-cases-category/marketing) |
| Nonprofits 分類 | [claude.com/resources/use-cases-category/nonprofits](https://claude.com/resources/use-cases-category/nonprofits) |
| The Four Claude Features (深度分析) | [smithstephen.com](https://www.smithstephen.com/p/the-four-claude-features-that-turn) |
| Claude Cowork 77 Use Cases | [aiblewmymind.substack.com](https://aiblewmymind.substack.com/p/claude-cowork-use-cases-guide) |
| Everything Claude Shipped 2026 | [the-ai-corner.com](https://www.the-ai-corner.com/p/everything-claude-shipped-2026-complete-guide) |
| Anthropic Clio 用量分析 | [constellationr.com](https://www.constellationr.com/insights/news/anthropic-outlines-most-popular-claude-use-cases) |

## 功能概述

Anthropic 在 `claude.com/resources/use-cases` 建立了一個**官方 Use Cases Gallery**——以互動式卡片牆呈現 Claude 各產品線的應用場景，涵蓋 13 個行業分類與 7 個功能標籤，是目前最完整的 Claude 實戰案例集。

這個頁面的定位不是技術文件，而是**銷售賦能 + 使用者教育**：讓潛在用戶看到「Claude 能幫我做什麼」，讓現有用戶發現「原來還能這樣用」。每個 use case 卡片都附上所用的模型（如 Sonnet 4.5）和功能標籤（如 Extended Thinking、Connectors），形成一個可篩選的案例資料庫。

## 分類架構

### 行業分類（13 類）

| 分類 | 代表場景 |
|------|---------|
| **Cowork** | 桌面檔案整理、散落文件合規準備、跨資料來源分析圖表 |
| **Custom Visuals** | 品牌名片/傳單生成 |
| **Education** | 課程材料整理、複雜概念解說 |
| **Finance** | 支出分析、預算規劃、銀行對帳 |
| **HR** | 人才流程自動化 |
| **Legal** | 合約紅線標註談判、合規文件準備、discovery 時間線追蹤 |
| **Life Sciences** | 醫療 HIPAA 合規、臨床資料分析 |
| **Marketing** | 跨平台內容改寫、行銷活動績效分析與預算重分配 |
| **Nonprofits** | 募款金字塔試算、捐款留存率 vs 新募比較、預算情境模擬 |
| **Personal** | 夢境解讀、災難準備、填字遊戲提示 |
| **Professional** | 客戶研究綜整、策略壓力測試、競品拆解 |
| **Research** | 學術論文分析、假說形成、資料集探索 |
| **Sales** | 客戶訪談模式發現、case interview 練習 |

### 功能標籤（7 種）

| 功能 | 說明 |
|------|------|
| **Artifacts** | 可交付成果：文件、試算表、互動式清單、簡報 |
| **Connectors** | Google Drive 等外部資料源串接 |
| **Extended Thinking** | 深度推理模式，適合多步驟分析 |
| **Projects** | 持久化工作區，檔案 + 指令跨對話保存 |
| **Research** | 網路搜尋 + 深度研究模式 |
| **Skills** | 可重複使用的自訂工作流 |
| **Web Search** | 即時網路搜尋能力 |

### 產品線篩選（4 種）

| 產品 | 定位 |
|------|------|
| **Claude.ai** | 瀏覽器/行動裝置聊天介面 |
| **Cowork** | 桌面端自主代理，直接操作本機檔案 |
| **Claude in Chrome** | 瀏覽器擴充套件，直接在網頁上操作 |
| **Claude in Excel** | 試算表內建 AI 助手 |

## Claude 四大模式與功能堆疊

```
┌─────────────────────────────────────────────────────────┐
│  Claude 產品矩陣（2026 年 3 月）                          │
├──────────┬──────────┬──────────┬─────────────────────────┤
│  Chat    │  Cowork  │  Code    │  Projects               │
│  瀏覽器   │  桌面代理  │  終端工具  │  持久工作區              │
│  快速問答  │  自主檔案  │  程式碼庫  │  跨對話記憶              │
│  草稿撰寫  │  多步驟    │  git 管理  │  檔案+指令持久化          │
├──────────┴──────────┴──────────┴─────────────────────────┤
│  底層能力：                                               │
│  • 1M token context（600 頁 PDF / 圖片）                   │
│  • Memory（自動記憶 + 可編輯）                               │
│  • Extended Thinking（深度推理）                            │
│  • Skills + Plugins（可重複工作流 + 角色工具包）               │
│  • Artifacts（可交付成果生成）                               │
│  • Connectors（Google Drive 等外部資料源）                   │
│  • Computer Use（螢幕操作）                                 │
│  • Dispatch（離開電腦後的遠端任務派送）                        │
└─────────────────────────────────────────────────────────┘
```

## 實際用量分布（Anthropic Clio 數據）

Anthropic 透過匿名化分析系統 Clio 揭示了 Claude 的實際使用分布：

### 企業端 Top 5 用途

| 排名 | 用途 | 佔比 |
|------|------|------|
| 1 | Web/Mobile App 開發輔助 | 10.4% |
| 2 | 內容創作與溝通 | 9.2% |
| 3 | 學術研究與寫作 | — |
| 4 | 職涯發展 | — |
| 5 | AI 與商業策略優化 | — |

### 語言別差異（有趣發現）

| 語言 | 偏好用途 |
|------|---------|
| 西班牙語 | 經濟學、兒童健康、環保 |
| 中文 | 犯罪/驚悚/推理小說寫作、長照 |
| 日文 | 動漫、經濟學、長照 |

## 重點 Use Case 深入

### Cowork（桌面代理）

Cowork 是最能展示 Claude 差異化的產品線——它不只是聊天，而是**直接操作你的電腦檔案**：

| Use Case | 做什麼 |
|----------|--------|
| 桌面檔案整理 | 讀取散亂的桌面檔案，自動辨識內容並分類到資料夾 |
| 跨來源分析 | 從 board deck 抓營收 + 從 FRED 抓 GDP，生成比較圖表 |
| 合規文件準備 | 散落的政策文件、合約、記錄 → 統一命名、組織好待審 |
| 銀行對帳 | 比對帳單與發票，分類支出，標記遺漏 |
| 照片辨識分類 | 用參考照片辨識寵物，自動分入標記資料夾 |
| 大型資料集報告 | 49,000+ 筆問卷回應 → 多 tab 試算表 + 圖表 |
| 影片剪輯 | 不用專業軟體就能拼接、裁切、編輯影片 |

### Legal（法務）

| Use Case | 做什麼 |
|----------|--------|
| 合約紅線標註 | 分析協議條款，標記影響工作的條款，建議修改與談判策略 |
| Projects 管理法務流程 | 上傳 playbook 一次，自動套用到數百份合約審查 |
| Discovery 時間線 | 大量文件產出中建立時間序列，辨識文件模式 |

### 企業四功能堆疊（Skills → Plugins → Projects → Artifacts）

Stephen Smith 提出的法律事務所類比特別精闢：

```
Skills    = 教新人格式規範        → 可重複的工作流指令
Plugins   = 發給他整組工具包      → Skills + MCP + 工具的打包安裝
Projects  = 指派到特定案件        → 隔離的工作區（AI 的 ethical wall）
Artifacts = 交出客戶端成品        → 文件、試算表、簡報的最終交付物
```

## 目前限制與注意事項

1. **Gallery 是動態載入** — 頁面用 Finsweet CMS + JS 動態渲染，無法被搜尋引擎完整索引，也難以程式化抓取
2. **案例深度不均** — 部分分類（如 Cowork、Legal、Nonprofits）有具體場景描述，其他（如 HR、Education）僅有標題級內容
3. **缺乏量化效果** — 大多數 use case 只描述「能做什麼」，缺乏「效果提升多少」的數據佐證
4. **產品線割裂** — Chat / Cowork / Code / Chrome / Excel 各自獨立，使用者需要自行判斷哪個產品適合哪個場景
5. **Clio 數據有限** — 實際用量分布只公開了 Top 5 和語言差異，細粒度數據未揭露

## 研究價值與啟示

### 關鍵洞察

1. **「Gallery as Sales Playbook」策略** — Anthropic 把 use case gallery 做成了一個多維度篩選的互動式資料庫（行業 × 功能 × 產品），這不是技術文件，而是 sales enablement 工具。讓銷售團隊能快速找到「你的行業 + 你的痛點 → Claude 怎麼解」的答案。這個策略值得任何 B2B SaaS 借鑒。

2. **Cowork 是真正的護城河** — 從 use case 分布可以看到，Cowork（桌面代理）佔據了最多的獨特場景——檔案整理、對帳、照片分類這些都是 ChatGPT 做不到的。Anthropic 把 Claude 從「聊天機器人」推向「桌面作業系統的一部分」，這是和 OpenAI 拉開差距的關鍵。

3. **四功能堆疊模型是企業採用的真正框架** — Skills → Plugins → Projects → Artifacts 不只是功能列表，而是一套「新人培訓」隱喻：先教規範（Skills），再給工具包（Plugins），指派案件（Projects），最後交成品（Artifacts）。這套框架解決了企業最大的疑慮：「AI 怎麼融入我們現有的工作流」。

4. **語言別差異揭示文化需求鴻溝** — 中文用戶偏好犯罪小說寫作、日文用戶偏好動漫——這些「非生產力」用途暗示 Claude 在亞洲市場的定位可能需要和歐美截然不同。Anthropic 公開這些數據是罕見的透明度。

5. **Use Case 的「反面」同樣重要** — Gallery 沒有列出的領域也很有意義：沒有「自主交易」、沒有「醫療診斷」、沒有「法律判決建議」——Anthropic 刻意迴避了高風險決策場景，這與他們的 responsible AI 定位一致。

### 與其他專案的關聯

- **vs. [Claude Code Showcase](claude-code-showcase.md)** — Showcase 展示 Claude Code（終端開發工具）的案例，Use Cases Gallery 則涵蓋全產品線。兩者互補：Showcase 面向開發者，Gallery 面向企業用戶。
- **vs. [Claude Skills Guide](claude-skills-guide.md)** — Skills Guide 教你「怎麼建 Skill」，Use Cases Gallery 展示「建好的 Skill 能做什麼」。Gallery 是 Skills 的消費端案例。
- **vs. [Everything Claude Code](everything-claude-code.md)** — Everything 是 Claude Code 生態的全方位強化，而 Use Cases Gallery 提醒我們 Claude 的版圖遠不止 coding——桌面代理、法務、非營利組織都是戰場。
- **vs. [Ramp AI Agents](ramp-ai-agents.md)** — Ramp 是單一公司的 AI 實戰案例，Gallery 是 Anthropic 官方收集的跨行業案例集。可以把 Ramp 看作 Gallery 中 Finance 分類的深度版本。
- **vs. [Claude Financial Services Plugins](claude-financial-services-plugins.md)** — Financial Services Plugins 是 Gallery 中 Finance 分類的底層實作。Gallery 展示場景，Plugins 提供工具。
