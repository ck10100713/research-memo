---
date: "2026-05-15"
category: "Coding Agent 工具"
card_icon: "material-palette"
oneliner: "卡斯伯（六角學院）用 25 設計風格 × 15 動畫模式做的 Claude Code Skill 示範作品集，主軸是「主執行緒寫 Skill → SubAgent 用 Skill 產單檔網頁」的規模化工作流"
---

# Casper × Claude Code Skill 設計風格圖鑑 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 作品集首頁 | <https://www.casper.tw/claude-skill-design-gallery/> |
| 作者 | 卡斯伯（Wang Casper），六角學院創辦人 |
| 作者本站 | <https://www.casper.tw/>（卡斯伯 Blog · 前端，沒有極限） |
| 六角學院 | <https://www.hexschool.com/> |
| 抓取日期 | 2026-05-15 |

> 註：作品集本身是 Vite SPA，主要內容由前端動態渲染。本筆記的細節由直接解析 bundle 取得；如未來介面改版，slug 命名與分類可能微調。

## 專案概述

**「Claude Code Skill 設計風格圖鑑 · 島嶼共鳴 2026」** 是台灣前端教育者卡斯伯（六角學院）做的一個 Claude Code Skill 示範作品集。表面是一個虛構音樂節「島嶼共鳴 2026」（由虛構品牌「浪打文化」主辦，宣傳語：「在島嶼盡頭聽見彼此的迴聲」、25,000 人次、都蘭灣海邊舞台、來自島嶼與海的 12 組樂團）的活動網站圖鑑，**實際是一個 Claude Code Skill 系統的規模化工作流範本**。

核心訊息（首頁原文）：

> 「這是一個示範專案，展示**『主執行緒寫 Skill → SubAgent 透過 Skill 產出網頁』**的規模化工作流。
> 所有 Skill 都隨專案進 Git，可被自由下載、修改、套用至其他專案。」

→ 同一個音樂節主題、同一份內容素材，被 25 種設計風格 × 15 種動畫模式重新詮釋，**每一張作品卡片背後對應一個獨立 Skill**（`.claude/skills/<slug>/`），可被任意 Claude Code 專案 fork 走。

換句話說，這個作品集**同時是設計風格樣本書 + Skill 撰寫範本 + SubAgent 工作流示範**三件事。

## 工作流（核心方法論）

```text
主執行緒（Main Thread）
  │  撰寫 Skill：定義設計語言、版型結構、觸發詞
  ▼
.claude/skills/design-<slug>/
  ├── SKILL.md（含 frontmatter：description + triggers）
  └── 相關素材 / template
  │
  ▼
SubAgent（透過 Skill 觸發詞匹配）
  │  接收統一主題（島嶼共鳴 2026 + 12 樂團 + 25000 人次...）
  │  套用某個 Skill 的設計語言
  ▼
產出單檔 HTML（self-contained）
```

關鍵設計決策：

- **內容 / 風格分離**：主題、樂團、人次、場地都是固定 prompt 文本，風格差異全靠 Skill 提供。
- **單檔 HTML 輸出**：每個 Skill 的目標都是 single-file HTML page，**避免 build / 套件依賴**，可直接打開觀看。
- **Skill = git 資產**：所有 Skill 進 repo，可被剪貼複用，沒有 vendor lock-in。
- **Drawer 一鍵複製**：UI 設計成點作品卡片 → 開 drawer → 直接抄 Skill 內容（這是教學體驗的核心）。
- **觸發詞中英文並列**：每個 Skill 的 `description` 都列出中英文觸發詞，讓 Claude Code 的 skill activation 在兩種語言都能命中。

## Skill 觸發詞範例（從 bundle 直接抓）

每個 Skill 的 frontmatter 都嚴格遵循「Use when … Triggers on …」格式：

```yaml
description: Use when generating a single-file HTML page for the
  「島嶼共鳴 2026」music festival in Bauhaus (包浩斯) style.
  Triggers on Bauhaus、包浩斯、Herbert Bayer、Kandinsky、幾何構成、
  primary colors red blue yellow、circle square triangle.
```

```yaml
description: Use when generating a single-file HTML page for the
  「島嶼共鳴 2026」music festival in ASCII Terminal / CLI / Green Phosphor aesthetic.
  Triggers on ASCII、Terminal、CLI、80x24、green phosphor、retro computing、
  Curses TUI、boxdraw、Lynx.
```

→ **每個 Skill 都把該風格的歷史人物、視覺特徵、文化關聯詞一次列出**，讓 LLM 既靠關鍵字命中，也靠語義關聯命中。這個寫法值得當作 Skill description 撰寫範本。

## 25 種設計風格全清單

依 bundle 內 `category` 欄位分組：

### 🎨 mainstream（主流現代 UI）
| Slug | 風格 |
|------|------|
| `design-material-3` | Material You / Material Design 3（Google Android） |
| `design-minimalism` | 極簡 / editorial whitespace |
| `design-dark-mode` | Immersive Dark / Netflix-like cinematic |
| `design-editorial` | 雜誌排版（Monocle / Wallpaper / Kinfolk） |
| `design-swiss-international` | 瑞士國際風格（Helvetica + grid） |

### ✨ decorative（裝飾性 UI）
| Slug | 風格 |
|------|------|
| `design-glassmorphism` | 玻璃擬態（frosted glass） |
| `design-neumorphism` | 新擬物化 / Soft UI / Claymorphism |
| `design-gradient-mesh` | Gradient Mesh / Aurora（Linear / Stripe） |
| `design-isometric-3d` | Isometric 3D 等距視角 |

### 🕹️ retro（懷舊復古）
| Slug | 風格 |
|------|------|
| `design-synthwave` | 80s Synthwave / Outrun |
| `design-vaporwave` | Vaporwave 蒸氣波 |
| `design-y2k` | Y2K（千禧年金屬 + Bubble） |
| `design-web1` | Web 1.0 GeoCities 風 |
| `design-american-retro-print` | 美式復古印刷 / Saul Bass / Aaron Draplin |
| `design-bauhaus` | 包浩斯（紅黃藍 / 幾何） |
| `design-constructivism` | 俄國構成主義（Rodchenko / Lissitzky） |
| `design-cyberpunk` | Cyberpunk / Blade Runner / Akira |

### 🧪 experimental（實驗性 / anti-design）
| Slug | 風格 |
|------|------|
| `design-brutalism` | Brutalist Web（raw HTML / anti-design / Balenciaga） |
| `design-glitch` | Glitch Art / databending / VHS noise |
| `design-ascii-terminal` | ASCII Terminal 80x24 green phosphor |

### 🌏 cultural（文化／地域）
| Slug | 風格 |
|------|------|
| `design-chinoiserie` | 中國風國潮（紅黑金 / 水墨 / 宋體） |
| `design-wabi-sabi` | 侘寂 |
| `design-taiwan-temple` | 台灣廟宇美學（Casper 在地化亮點） |
| `design-scandinavian` | 北歐 / Hygge / Finn Juhl / Aalto |
| `design-hand-drawn` | 手繪塗鴉 / indie zine |

→ 這 25 個分類橫跨「主流 UI 風潮 → 歷史設計運動 → 文化美學」，**特別把『台灣廟宇美學』放進去，是這份作品集的在地特色**——多數英文 design system 都不會涵蓋這條。

## 15 種動畫 / 互動模式（motion-*）

| Slug | 模式 |
|------|------|
| `motion-parallax-layers` | 多層視差捲動 |
| `motion-sticky-stack` | sticky 堆疊（每段 `position: sticky; min-height: 100vh`） |
| `motion-horizontal-scroll` | 橫向捲動 |
| `motion-scroll-snap-acts` | scroll-snap 分幕 |
| `motion-scroll-progress` | 捲動進度指示 |
| `motion-marquee-band` | 跑馬燈帶 |
| `motion-fade-stagger` | 錯位淡入 |
| `motion-typewriter` | 打字機效果 |
| `motion-counter-burst` | 數字爆發計數 |
| `motion-aurora-flow` | 極光流動背景 |
| `motion-floating-orbs` | 浮動光球 |
| `motion-noise-grain` | 雜訊顆粒疊加 |
| `motion-cursor-spotlight` | 游標 spotlight |
| `motion-tilt-cards` | 卡片傾斜（3D tilt） |
| `motion-magnetic-cta` | 磁吸 CTA 按鈕 |

→ 這 15 條動畫**是可以橫向 mix-and-match 進任何設計風格的「副 Skill」**。例如「Bauhaus + scroll-snap-acts + counter-burst」就能變出有現代互動感的包浩斯網站。

## 主執行緒寫 Skill / SubAgent 用 Skill 的意義

這個專案在 Skill engineering 上的真正貢獻，不是「列出 25 種設計風格」（那只是 UI 教材），而是**示範了一個 N=1（主執行緒）+ N=N（SubAgent 並行）的工作流模式**：

```
       傳統 Claude Code 用法              本作品集示範
       ────────────────────              ───────────────
       人類在主執行緒                     人類在主執行緒
       直接請 Claude 寫頁面               請 Claude 寫 Skill（一次性）
                                          │
                                          ▼
       每換一個風格都要重新                Skill 進 Git 後
       輸入完整需求                       N 個 SubAgent 各拿一個 Skill
                                          並行產 N 個頁面
       Token 消耗 ∝ 頁面數                Token 消耗 ≈ Skill 數 + 各頁面執行
```

→ 對於「同一個內容、要產出 N 種樣式」的場景（網站樣板、簡報、報告書），**主執行緒寫 Skill、SubAgent 套 Skill** 是顯著比「重複 prompt」更省 token、且結果更一致的工作流。

## 目前限制與注意事項

- **網頁是 SPA、無靜態內容**：bundle 內容必須執行 JS 才呈現，對搜尋引擎、archive 工具不友善；想離線複習得自己 dump bundle。
- **GitHub repo 未公開連結**：bundle 內找不到 git 倉庫位置（可能在文字介紹中、但未直接寫出）；要拿 Skill 內容須從網頁 drawer 複製。
- **「島嶼共鳴 2026」是虛構活動**：所有素材（樂團、25,000 人次、都蘭灣場地）都是虛構，是為了示範統一主題下的多風格產出，不是真實活動。
- **單檔 HTML 限制**：所有 Skill 都鎖死「single-file output」，不示範框架（React/Vue）或 CMS 整合，是樣本書而非可直接 deploy 的 starter template。
- **內容深度未驗證**：bundle 抓不到每個 Skill 的完整 SKILL.md 內文，描述觸發詞之外的細節（layout 規則、token system、字型選擇）需點開作品集 drawer 逐一查看。

## 研究價值與啟示

### 關鍵洞察

1. **「主執行緒寫 Skill、SubAgent 用 Skill」是規模化 LLM 工作流的關鍵 pattern**：對需要「同主題、多變體」的設計／文件／報告產出，這個分層比起反覆 prompt 顯著更有效率。對應的場景可以延伸到：用 Skill 產 N 種簡報模板、N 種 README 風格、N 種程式碼註解語氣。
2. **Skill description 的「Triggers on …」設計值得仿造**：作品集裡每個 Skill 的觸發詞**同時列中英文 + 歷史人物 + 視覺特徵 + 文化關聯詞**，這比起只放「Bauhaus style」一個關鍵字命中率高很多。可以抽出成 [[claude-skills-guide]] 級別的撰寫規範。
3. **設計風格 25 × 動畫 15 = 375 種組合，是隱性的 design system 字典**：對前端開發者來說，這份目錄本身就是一份「我能挑哪些風格給客戶看」的參考菜單；對 Skill 撰寫者來說，是「我可以把哪些設計運動編碼成 LLM 可執行知識」的清單。
4. **在地文化納入**：「design-taiwan-temple」放在跟 Bauhaus / Swiss 同樣 first-class 的位置，這是少見的非西方 design vocabulary 進入 LLM Skill 系統的具體例子。值得當作「本地化設計 Skill」的範本，去做台灣老牌餐廳、香港霓虹、日本居酒屋等等。
5. **內容 / 風格分離是 Skill 抽象化的核心**：把「島嶼共鳴 2026 + 12 樂團 + 25000 人次」固定下來、讓風格自由變化，這個約束才讓「Skill 是設計 DNA、SubAgent 是執行者」的分工成立。如果連內容都要 Skill 提供，Skill 會肥大而難以複用。
6. **單檔 HTML 是「給 LLM 用的設計 deliverable」最聰明的格式**：沒 build、沒 framework、沒 dependency，**Claude 寫完 = 使用者可以立刻打開看 = 結果可被儲存進 git**。對比常見的「教 Claude 寫 React」陷阱（生成出來但跑不起來），單檔 HTML 是真正的 LLM-friendly 產出格式。

### 與其他研究的關聯

- 與 [[claude-skills-guide]]、[[andrej-karpathy-skills]]、[[asgard-skills]]：本作品集是 Skill 撰寫的**實戰範本**，前述三份是觀念整理。建議用本研究的 Skill description 寫法回頭優化觀念整理裡列出的範本。
- 與 [[abdixere-api]]：abdixere-api 主張「Skill 是 Agent context memory 的主要載體」，本作品集就是這個哲學在「設計領域」的具體落地——把設計運動的歷史知識編成 Skill 後，Agent 不需要 RAG 也能寫對風格。
- 與 [[ai-agents-for-beginners]]、[[mcp-for-beginners]]：Microsoft 教材教「Agent design patterns」，本作品集示範「Multi-Agent Design Pattern」中「同主題並行產出」的最直接案例。可作為閱讀 Microsoft 教材後的實作練習。
- 與 [[awesome-design-md]]、[[claude-design]]、[[design-md-chrome]]：這幾份都圍繞「Claude + 設計」主題，本研究**走得更遠**：不只是給 Claude 一份 DESIGN.md，而是把每個設計運動拆成獨立可呼叫的 Skill，讓 Agent 用觸發詞自選風格。
- 對 [[ralph-loop:ralph-loop]] 或自主迭代開發場景：可以用本作品集當「設計樣本書」，讓 ralph loop 自己挑風格 → 用 SubAgent 套 Skill → 產出 → 自評（用第 4 個 Skill 比如 design-review）→ 換風格再來。是把「設計也納入自主迭代」的可行性 PoC。
- 對 Casper 本人的教學體系（六角學院）：這份作品集是少見的「前端教育者用 Claude Code 做的教材」，值得對照 [[learn-claude-code]] 等學習資源觀察「教育者如何把 Skill 系統重新教給前端工程師」。
