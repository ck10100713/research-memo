---
date: "2026-05-25"
category: "軟體工程知識"
card_icon: "material-book-open-variant"
oneliner: "Dr. Milan Milanović 整理的 56 條軟體工程定律參考站，分七大類（團隊/規劃/架構/品質/設計/規模/決策），含書、海報、JSON API、50k 訂閱電子報，已成 Amazon 暢銷書"
---

# Laws of Software Engineering 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官網 | <https://lawsofsoftwareengineering.com/> |
| 書籍頁 | <https://lawsofsoftwareengineering.com/book/> |
| 作者 Newsletter | <https://newsletter.techworld-with-milan.com> |
| 完整 20 法則文章 | <https://newsletter.techworld-with-milan.com/p/the-20-software-engineering-laws> |
| Newsletter 介紹文 | <https://newsletter.techworld-with-milan.com/p/laws-of-software-engineering> |
| Amazon 紙本書 | <https://www.amazon.com/Laws-Software-Engineering-Milan-Milanovic/dp/9699893680> |
| Amazon 電子書 | <https://www.amazon.com/Laws-Software-Engineering-Milan-Milanovic-ebook/dp/B0GXH5JYVP> |
| 作者 Patreon | <https://www.patreon.com/posts/laws-of-software-155198996> |
| 第三方書評 | <https://www.blog.ajabbi.com/2026/04/laws-of-software-engineering.html> |

## 專案概述

**Laws of Software Engineering** 是塞爾維亞博士、軟體工程作家 **Dr. Milan Milanović** 維護的一個「軟體工程定律百科」網站，把職涯 20+ 年觀察到的、跨公司跨技術反覆出現的同一批模式，整理成 **56 條定律** 並開放免費瀏覽。

衍生產品：

- **書（300 頁、63+ 條定律）**：2026 上市，上線兩天賣 500+ 本，登 Amazon 該類別暢銷榜，序由 Rebecca Parsons（Thoughtworks CTO Emerita）、Addy Osmani（Google Cloud AI Engineering Director）撰寫，20 位 Google/Amazon/Uber/Oracle/Yelp/Nutanix/CodeScene 工程師審稿。
- **海報**：把 56 條定律印成單張海報，適合釘在 team space。
- **電子報「Tech World With Milan」**：50,000+ 訂戶。
- **JSON API + RSS**：把網站內容當成可程式化的資料來源。

### 網站特色

- **依等級過濾**：Junior / Mid / Senior，方便依資歷推薦該掌握的定律。
- **依分類過濾**：七大類（見下方）。
- **授權**：CC BY-NC-ND 4.0（可分享、不可商用、不可改作）。
- **Hacker News 1.1k 分數**，社群口碑強。

## 七大分類完整對照

> 以下完整收錄官網列出的 **56 條定律**，分七類，附原文聲明與一句中文解讀。

### 一、Teams（團隊，9 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 1 | **Conway's Law** | Organizations design systems mirroring their communication structure | 組織如何溝通，系統就會長成那個樣子 |
| 2 | **Brooks's Law** | Adding staff to delayed projects increases delays further | 給落後專案加人只會更晚 |
| 3 | **Dunbar's Number** | Cognitive limit ~150 stable relationships per person | 一個人能維持的穩定關係上限約 150 |
| 4 | **The Ringelmann Effect** | Individual productivity declines as group size expands | 團隊變大，每個人的產出反而下降 |
| 5 | **Price's Law** | Square root of participants produces 50% of output | √N 的人貢獻 50% 的產出 |
| 6 | **Putt's Law** | Tech experts don't manage it; managers don't understand it | 懂技術的不管理，管理的不懂技術 |
| 7 | **Peter Principle** | Employees rise until reaching incompetence level | 員工會被升遷到自己無能勝任的位置 |
| 8 | **Bus Factor** | Minimum team members whose departure threatens project viability | 多少人離職專案就停擺，數字越小越危險 |
| 9 | **Dilbert Principle** | Companies promote incompetent employees to management roles | 公司會把不適任者升上管理職以避免他們搞砸事 |

### 二、Planning（規劃，6 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 10 | **Premature Optimization** | "Premature optimization is the root of all evil" (Knuth) | 過早優化是萬惡之源 |
| 11 | **Parkinson's Law** | Work expands filling available completion time | 工作會自動膨脹填滿可用時間 |
| 12 | **Ninety-Ninety Rule** | First 90% takes 90% of time; last 10% takes another 90% | 前 90% 花 90% 時間，後 10% 再花 90% 時間 |
| 13 | **Hofstadter's Law** | Tasks take longer than expected, even accounting for this law | 任務總比預估長，連預估這件事都要算進去 |
| 14 | **Goodhart's Law** | Measures become poor targets when targeted | 一旦把指標當目標，指標就失效 |
| 15 | **Gilb's Law** | Quantifiable needs have measurable improvements over non-measurement | 能量化的需求才有可能改進 |

### 三、Architecture（架構，9 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 16 | **Hyrum's Law** | Sufficient API users depend on all observable system behaviors | API 用戶夠多時，所有可觀察的行為都會被人依賴 |
| 17 | **Gall's Law** | Working complex systems evolved from working simple ones | 能跑的複雜系統一定是從能跑的簡單系統演化來的 |
| 18 | **Law of Leaky Abstractions** | Non-trivial abstractions inherently leak details | 任何有用的抽象都會洩漏底層細節 |
| 19 | **Tesler's Law** | Irreducible complexity shifts, never eliminates | 必要的複雜度只能搬家，不能消滅 |
| 20 | **CAP Theorem** | Distributed systems guarantee only 2 of: consistency, availability, partition tolerance | 分散式系統三選二 |
| 21 | **Second-System Effect** | Successful small systems spawn overengineered replacements | 第一版成功的小系統，第二版往往會被過度設計毀掉 |
| 22 | **Fallacies of Distributed Computing** | 8 false assumptions novice designers make | 分散式系統新手會犯的 8 個假設錯誤 |
| 23 | **Law of Unintended Consequences** | Complex system changes produce surprises | 動複雜系統一定會冒出意料之外的副作用 |
| 24 | **Zawinski's Law** | Programs expand until reading mail capability | 所有程式最終都會膨脹到能收信為止 |

### 四、Quality（品質，11 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 25 | **Boy Scout Rule** | Leave code better than found | 走時讓 code 比來時更好 |
| 26 | **Murphy's Law** | Anything wrong will go wrong | 會出錯的就會出錯 |
| 27 | **Postel's Law** | Conservative outputs, liberal acceptance of inputs | 輸出嚴謹，輸入寬容 |
| 28 | **Broken Windows Theory** | Repair bad designs immediately; neglect enables decline | 壞設計不修就會墮落更快 |
| 29 | **Technical Debt** | Everything slowing development progress | 任何拖慢開發的東西都是技術債 |
| 30 | **Linus's Law** | Sufficient reviewers make bugs discoverable quickly | 眼睛多了 bug 就藏不住 |
| 31 | **Kernighan's Law** | Debugging difficulty doubles versus coding effort | 除錯比寫 code 難一倍，所以別寫太聰明的 code |
| 32 | **Testing Pyramid** | Many unit, fewer integration, minimal UI tests | 單元測試多、整合次之、UI 最少 |
| 33 | **Pesticide Paradox** | Repeated identical tests lose effectiveness | 同一組測試跑久了就抓不到新 bug |
| 34 | **Lehman's Laws of Software Evolution** | Real-world software must evolve predictably | 持續使用的軟體必須持續演化否則衰亡 |
| 35 | **Sturgeon's Law** | 90% of everything is poor quality | 萬物 90% 都是垃圾 |

### 五、Design（設計，6 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 36 | **YAGNI** | You Aren't Gonna Need It — avoid unnecessary functionality | 還用不到就先別做 |
| 37 | **DRY** | Don't Repeat Yourself — single authoritative source | 同一份知識只該有一份權威表示 |
| 38 | **KISS** | Keep It Simple, Stupid | 設計越簡單越好 |
| 39 | **SOLID Principles** | 5 OO 設計原則（SRP/OCP/LSP/ISP/DIP） | 物件導向五大原則 |
| 40 | **Law of Demeter** | Objects interact only with immediate neighbors | 只跟直接鄰居說話，別跨層次拉扯 |
| 41 | **Principle of Least Astonishment** | Software behaves unsurprisingly | 別讓使用者/開發者驚訝 |

### 六、Scale（規模，3 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 42 | **Amdahl's Law** | Parallelization speedup limited by non-parallelizable work | 平行化的天花板是序列部分 |
| 43 | **Gustafson's Law** | Significant parallel speedup achievable through problem enlargement | 問題夠大平行化才划算 |
| 44 | **Metcalfe's Law** | Network value proportional to user count squared | 網路價值正比於用戶數平方 |

### 七、Decisions（決策，12 條）

| # | 定律 | 內容 | 一句解讀 |
|---|------|------|---------|
| 45 | **Dunning-Kruger Effect** | Less knowledge correlates with unwarranted confidence | 越不懂越自信 |
| 46 | **Hanlon's Razor** | Avoid malice attributions; consider incompetence first | 先想能力不足，再想惡意 |
| 47 | **Occam's Razor** | Simplest explanations typically prove most accurate | 最簡單的解釋通常最對 |
| 48 | **Sunk Cost Fallacy** | Continuing investments despite better alternatives | 不要為已經沉沒的成本繼續加碼 |
| 49 | **The Map Is Not the Territory** | Reality differs from representations | 地圖不是真實領土 |
| 50 | **Confirmation Bias** | Favoring information supporting existing beliefs | 人只信支持自己觀點的證據 |
| 51 | **Hype Cycle & Amara's Law** | Short-term overestimation, long-term underestimation | 短期高估，長期低估 |
| 52 | **Lindy Effect** | Longevity indicates continued use likelihood | 活越久未來會活越久 |
| 53 | **First Principles Thinking** | Decompose problems into basics, rebuild systematically | 拆到第一性原理重組 |
| 54 | **Inversion** | Solve problems considering opposite outcomes | 反向思考解問題 |
| 55 | **Pareto Principle** | 80% of problems stem from 20% of causes | 80/20 法則 |
| 56 | **Cunningham's Law** | Posting incorrect answers generates faster responses than asking | 想要正解，先 po 個錯解 |

## 七大分類分佈概覽

```
分類           條數    主題核心
─────────────────────────────────────────
Teams          9      組織、人、溝通結構
Planning       6      時程、估算、目標設定
Architecture   9      系統設計、抽象、分散式
Quality        11     程式碼健康、測試、演化  ← 最多
Design         6      物件導向與設計原則
Scale          3      平行化、網路效應
Decisions      12     認知偏誤、思考工具      ← 第二多
─────────────────────────────────────────
合計           56
```

值得注意：**Quality（11）+ Decisions（12）= 23 條，佔了 41%**。作者觀點：軟體工程的「重災區」不是設計、不是平行化，而是「程式碼會壞、人會誤判」這兩件事。

## 使用方式

### 1. 作為團隊文化字典

把網站連結放進 onboarding doc，新人遇到 PR review 時聽到「這違反 Hyrum's Law」「這是典型 second-system effect」可以即時查表。

### 2. 作為 Code Review 用語

把定律名當成 review 的 shorthand：

> 「這段違反 Law of Demeter，object 跨了三層」  
> 「這個 spec 在做 Premature Optimization，先實作再說」  
> 「警告 Hyrum's Law：這個內部 API 已經有人開始依賴 timing」

### 3. 用 JSON API 自動化

網站提供 JSON 端點，可以做：

- Slack/Discord bot：每天推送一條定律
- IDE 外掛：寫 code 時跳出相關定律提示
- LLM agent 工具：給 AI agent 一個「software-engineering-laws」工具，code review 時自動引用

### 4. 牆面海報

辦公室印一張，每週固定討論一條。

## 目前限制

- **不是研究級別文獻**：每條定律的描述非常短（一兩句），想深究需要自己再去查原始出處。
- **CC BY-NC-ND 授權限制商用 + 改作**：不能直接把內容塞進付費產品或自製衍生海報。
- **網站 56 條 vs 書 63+ 條**：書裡多了至少 7 條，網站是免費試用版的概念。
- **個人經驗為主**：作者主觀挑選，不是學術 survey；有些「定律」（如 Putt's Law、Dilbert Principle）偏諷刺幽默，認真使用要注意語境。
- **英文為主**：目前沒有官方繁中翻譯。

## 研究價值與啟示

### 關鍵洞察

1. **「定律命名」本身就是一種抽象壓縮工具**
   把「給落後專案加人會更晚」壓縮成「Brooks's Law」三個字，是團隊溝通成本最低的共識協定。一個有 56 條共同字彙的團隊，PR review 速度會比沒有的團隊快非常多——這跟設計模式（Design Patterns）給類別命名的價值是同源的。

2. **AI 時代「命名定律」反而更重要**
   LLM 在 review code 或寫 PR 評論時，用「違反 Hyrum's Law」比用 200 字解釋更省 token 也更易讀。**這個網站可以做成 LLM agent 的 system prompt 附錄**，讓 agent 用業界共識的語言溝通。可結合 [Skill Creator](skill-creator) 模式，做成一個 `swe-laws` skill，每次 review 時自動引用最相關的 3 條。

3. **單人 + Newsletter + 書 + 海報 + JSON API 是 2026 知識付費標準堆疊**
   Milan 一個人經營：免費網站做 SEO 漏斗 → 5 萬訂戶 newsletter 經營信任 → 書收一次性費用 → 海報賣周邊 → JSON API 開放給開發者→ Patreon 收訂閱。這個堆疊比傳統「寫部落格賣課程」高一層級，值得想做 dev content 的人研究。

4. **定律分佈洩漏業界共識：Quality + Decisions 最多條**
   11 條 Quality + 12 條 Decisions 暗示業界已經共識——**軟體工程的瓶頸不是技術，是「程式碼會壞、人會誤判」**。對比之下 Scale 只有 3 條，反映「scale 問題已被 cloud / k8s / CAP 之類框架解決得差不多」的時代心情。

5. **與 [Why Your AI Is Dumbing Down](why-your-ai-is-dumbing-down.md) 形成對照**
   兩者都在處理「為什麼程式越寫越爛」，但角度不同：
   - 本站從**人與組織結構**找原因（Conway、Brooks、Peter、Ringelmann）
   - WYAIDD 從**AI 工具行為**找原因
   合起來看：**程式變爛 = 組織問題 + 工具問題**，兩者乘積。

### 與其他研究筆記的關聯

- **[Awesome DESIGN.md](awesome-design-md.md) / [Awesome Design Systems](awesome-design-systems.md)**：同樣是「策展型」資源，但本站策展的是抽象原則而非具體實作。
- **[Claude Skills Guide](claude-skills-guide.md) / [Casper Claude Skill Design Gallery](casper-claude-skill-design-gallery.md)**：如果把 56 條定律打包成 Claude Code skill，會是個高 ROI 的小專案——每次 review 時 LLM 自動引用最相關定律。
- **[Why Your AI Is Dumbing Down](why-your-ai-is-dumbing-down.md)**：從「人」角度互補本站的「工具」視角。
- **[Boris Cherny × Opus 4.7 心得](boris-cherny-opus-4-7.md) / [Claude Code Boris Cherny 57 Tips](claude-code-boris-cherny-tips.md)**：Boris Cherny 的 tips 是「實戰技巧」、本站是「抽象定律」，互為樓上樓下的兩層知識。
