---
date: "2026-04-21"
category: "Coding Agent 工具"
card_icon: "material-palette-swatch"
oneliner: "Chrome 擴充套件，一鍵擷取任意網站設計系統生成 DESIGN.md / SKILL.md，7 天 756 stars，TypeUI 生態系的瀏覽器前端"
---

# design-md-chrome 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/bergside/design-md-chrome> |
| Chrome Web Store（官方上架） | <https://chromewebstore.google.com/detail/designmd-style-extractor/ogpdnchdjiibhobphelbbkemnnemkfma> |
| TypeUI 官網 | <https://www.typeui.sh/> |
| DESIGN.md 格式規範 | <https://www.typeui.sh/design-md> |
| Design Skills 主題庫 | <https://www.typeui.sh/design-skills>（48 套精選設計） |
| TypeUI CLI（姊妹專案） | <https://github.com/bergside/typeui>（665⭐） |
| DEV.to 教學 | <https://dev.to/zoltanszogyenyi/generate-design-skill-files-for-your-agentic-tools-with-typeui-11ce> |
| Creative Tim 介紹文 | <https://www.creative-tim.com/blog/ai-agent/typeui-the-design-layer-for-ai-coding-agents/> |

## 專案概述

**design-md-chrome** 是 bergside 於 **2026-04-14** 開源的 Manifest v3 Chrome 擴充套件，定位是 **TypeUI 生態系的瀏覽器前端**——使用者打開任一網站、點一下 popup，擴充套件會把該頁面的 **typography / colors / spacing / radius / shadow / motion** 六大類樣式樣本抽出來，按照 **TypeUI DESIGN.md 標準格式** 生成一份可直接餵給 Claude Code / Codex / Cursor / Google Stitch / OpenCode / OpenClaw 的 `DESIGN.md` 或 `SKILL.md` 檔案。

解決的核心問題：**「AI coding agent 寫 UI 時長得都一樣」的 AI slop 問題**。原本你需要手寫設計系統文件餵給 agent，或在提示詞裡塞色碼與間距；現在你只要瀏覽一個你喜歡的網站，按一下就拿到結構化、帶 WCAG 2.2 AA 約束的設計規範 markdown，可直接 commit 到 repo 當 agent 的 context。

截至 **2026-04-21**（本筆記撰寫日，距首次 commit 僅 **7 天**）：**756 stars / 100 forks / Chrome Web Store 已上架**。同一組作者 bergside 另維護 TypeUI CLI（665⭐，2026-03-03 開源），本 repo 是 CLI 的「反向讀取」工具——**CLI 負責安裝預設 design skill，Chrome 擴充負責從真實網站萃取新 skill**，兩邊對接同一個 DESIGN.md 標準。

## 核心運作機制

### 架構（Manifest v3，零外部依賴）

```
┌──────────────────────────────────┐
│  popup/popup.html（UI）          │  ← 你按 Generate 的入口
└──────────────┬───────────────────┘
               │ RUN_EXTRACTION
               ▼
┌──────────────────────────────────┐
│  service-worker.js               │  ← 排版與下載協調者
│  ├─ inject content-script.js     │
│  ├─ normalize.mjs                │
│  ├─ generate-design-md.mjs       │
│  ├─ generate-skill-md.mjs        │
│  └─ validate.mjs                 │
└──────────────┬───────────────────┘
               │ TYPEUI_EXTRACT_STYLES
               ▼
┌──────────────────────────────────┐
│  content-script.js（注入目標頁） │  ← 真正抓 computed style
│  collectSampledElements(280)     │
│  getComputedStyle(el) × 6 token  │
└──────────────────────────────────┘
```

### 樣式擷取邏輯（核心演算法）

Content script 對目標頁面做**固定上限 280 個元素**的語意化取樣：

```javascript
// content-script.js 裡的 selector 白名單
const selectors = [
  "body",
  "h1,h2,h3,h4,h5,h6",        // 標題層級
  "p", "a", "button",          // 互動元件
  "input,textarea,select",
  "label",
  "nav,header,footer,main,section,article,aside",  // semantic
  "ul li,ol li",
  // ...
];
```

對每個取樣元素呼叫 `window.getComputedStyle(el)` 收集 6 種 token：

| Token 類別 | 抓取欄位 |
|-----------|---------|
| `typography` | fontFamily / fontSize / lineHeight / fontWeight / letterSpacing |
| `colors` | textColor / backgroundColor / borderColor / outlineColor |
| `spacing` | margin × 4 方向 + padding × 4 方向 |
| `radius` | borderRadius |
| `shadows` | boxShadow |
| `motion` | transitionDuration / transitionTimingFunction / animationDuration / animationTimingFunction |

額外再收 `components`（元件數量統計）與 `siteSignals`（品牌相關 meta）。收完打包回 service worker，由 `normalize.mjs` 轉成 token 頻率統計，`generate-design-md.mjs` 或 `generate-skill-md.mjs` 生成 markdown，再經 `validate.mjs` 驗證結構完整度。

### 生成檔案的 11 個必備段落

| 段落 | 作用 |
|------|------|
| `Mission` | 一段話定義設計系統目標 |
| `Brand` | 品牌、受眾、產品型態（web app / marketing site / dashboard / mobile） |
| `Style Foundations` | 從樣本推論出的 token（顏色、字級、間距、圓角、陰影、動態） |
| `Accessibility` | **強制 WCAG 2.2 AA**、鍵盤優先、focus-visible、對比限制 |
| `Writing Tone` | 實作導向、精簡、自信的文案語氣 |
| `Rules: Do` | 必做實作規則（語意 token / 全狀態覆蓋 / 響應式） |
| `Rules: Don't` | 禁做模式（低對比、一次性間距、模糊標籤） |
| `Guideline Authoring Workflow` | 寫 guideline 的固定六步驟 |
| `Required Output Structure` | agent 必須輸出的結構 |
| `Component Rule Expectations` | 每個 component 必備的 state / variants / 邊界 |
| `Quality Gates` | 可測試的品質檢查 |

## 快速開始

### 方法 A：Chrome Web Store（零門檻）

直接到 <https://chromewebstore.google.com/detail/designmd-style-extractor/ogpdnchdjiibhobphelbbkemnnemkfma> 點安裝。

### 方法 B：Load unpacked（想改程式碼或審查原始碼時用）

```bash
git clone https://github.com/bergside/design-md-chrome ~/design-md-chrome
```

然後在 Chrome：

1. 打開 `chrome://extensions`
2. 開啟 **Developer mode**
3. 點 **Load unpacked**
4. 選 `~/design-md-chrome` 資料夾

### 操作流程

| 動作 | 說明 |
|------|------|
| **Auto-extract** | 讀取目前 tab 的樣式（自動） |
| **Generate `DESIGN.md`** | 產出設計系統文件 |
| **Generate `SKILL.md`** | 產出 agent 可讀的 skill markdown |
| **Refresh** | 重抓（頁面動態變化後用） |
| **Download** | 存成 `.md` 檔 |
| **Explain (`?`)** | 顯示檔案如何生成 + TypeUI reference |

v0.4.0（2026-04-17）新增 **Claude / Codex / Cursor 的一鍵安裝按鈕**，下載完可直接跳到對應工具的 skill 目錄引導。

### 搭配 Claude Code 使用

```bash
# 下載一個自己喜歡網站的 DESIGN.md 後
mv ~/Downloads/DESIGN.md ~/my-project/DESIGN.md

# 讓 Claude Code 在該專案永遠讀到它
echo "參考 DESIGN.md 作為設計系統來源" >> ~/my-project/CLAUDE.md
```

或放到 `~/.claude/skills/` 當全域 skill：

```bash
mkdir -p ~/.claude/skills/my-design-skill
mv ~/Downloads/SKILL.md ~/.claude/skills/my-design-skill/SKILL.md
```

## 目前限制與注意事項

- **取樣是靜態樣本**：固定上限 280 個元素，長頁面 / 大型 SPA 會遺漏深層元件（例如折疊選單、modal 裡的樣式）。
- **只抓 `getComputedStyle`，不認 CSS 變數**：抓出來的是最終值（`rgb(17, 24, 39)`）而非 `var(--gray-900)`；token 的語意命名需 AI 事後推論。
- **無法區分「設計語彙」與「偶發值」**：產品頁上一個臨時紅色 badge 會混進 palette，生成的 `Style Foundations` 可能帶雜訊。
- **對 Tailwind / 原子化 CSS 的還原有限**：原子化 class 的 token 意圖藏在 class name 裡，computed style 看不到。
- **Motion tokens 仰賴頁面當下有動畫在跑**：靜態截圖時若元素沒有 `transition`，該段會空白。
- **Manifest v3 權限涵蓋 `activeTab / scripting / storage / downloads`**：安裝前值得檢視 `manifest.json`，確認信任組織（bergside 為 Creative Tim 旗下，算商業背書）。
- **無 GitHub Release**：版號只寫在 `manifest.json`（v0.4.0），更新靠 Chrome Web Store 自動機制，手動 Load unpacked 的人要自己拉 main。
- **依賴 TypeUI 格式標準**：若 TypeUI 規範演化（例如 `typeui.sh/design-md` 更新欄位），擴充需要跟版。
- **不處理多 theme / dark mode**：只抓目前可視 theme，`prefers-color-scheme: dark` 的變體要手動切換頁面重抓一次。

## 研究價值與啟示

### 關鍵洞察

1. **「設計系統文件」是 AI coding agent 的缺失環節**：Claude Code、Cursor、Codex 已經很會寫元件，但寫出來的 UI 普遍像「generic Tailwind 預設樣」，原因是 agent 沒有**專案特化的設計 context**。design-md-chrome 把這塊從「要手寫 guideline」降到「瀏覽網頁按一下」，**把設計系統變成可被擷取的實體**，這是 2026 年 AI coding 工具鏈最重要的工作流修補之一。

2. **TypeUI 的雙邊策略**：bergside 同時維護 [typeui CLI](https://github.com/bergside/typeui)（安裝 48 套精選 design skill）與本 repo（從任意網站萃取 skill）。一邊**供應**（從精選庫下載），一邊**生產**（從野外擷取），兩邊共用同一個 DESIGN.md 標準。這個「工具鏈閉環」是很聰明的 ecosystem play——**標準化 markdown 格式是護城河**，工具只是入口。

3. **Chrome 擴充是分發 AI tooling 最被低估的管道**：相較於要寫 CLI 或 Plugin，Chrome 擴充的「看見 → 安裝 → 用」摩擦極低。7 天 756 stars 不只是專案本身好，更是**分發通路選對**——開發者已經在瀏覽器看範例網站，「按一下抓設計」的使用場景跟他們已有習慣完全對齊。這對所有 AI 工具作者都是啟示：**把入口搬到使用者已經在的地方，不是要他們來你的地方**。

4. **Manifest v3 + 純 ES Module 是可複製的乾淨樣本**：整份擴充**零 npm 依賴**（`scripts/` 只有一支 `generate-icons.sh`，測試用 `tests/run-tests.mjs` 原生 Node），service-worker / content-script / popup 三層分工明確。對想自己寫 AI 工具 Chrome 擴充的人來說，這是 400 多行就能讀完的最小完整樣本。

5. **WCAG 2.2 AA 內建是聰明的「合規綁定」**：生成的 DESIGN.md **強制** accessibility 區塊為 WCAG 2.2 AA、要求 focus-visible、鍵盤優先、對比約束。這不是 feature，而是**把合規要求寫進 AI context 裡**——agent 讀了這份文件，寫 code 時會自動滿足可及性，不用開發者另外提醒。**合規 by context** 比 **合規 by linter** 門檻低很多。

6. **7 天 756 stars 的成長訊號**：對照同期熱門 Claude 專案（[my-claude-devteam](my-claude-devteam.md) 9 天 218⭐、[cc-statusline](cc-statusline.md) 8 天 82⭐），design-md-chrome 的增速明顯更快。差異在於 **它不只是 Claude 工具**——跨 Claude / Codex / Cursor / Google Stitch / OpenClaw 多個陣營，受眾面擴大 5 倍以上。**不綁單一 agent 廠牌的工具**在 2026 年這個多陣營並存的時間點是關鍵紅利。

### 與其他專案的關聯

| 對比對象 | 差異 / 啟示 |
|----------|------------|
| [Awesome DESIGN.md](awesome-design-md.md) | Awesome DESIGN.md 是**精選 DESIGN.md 清單**（靜態 curation），design-md-chrome 是**動態生成器**；兩者互補：前者提供範本靈感，後者從任意網站現抓。 |
| [Awesome Design Systems](awesome-design-systems.md) | 同為設計系統資源，但 Awesome Design Systems 針對**人類設計師**，design-md-chrome 針對 **AI agent**。2026 年「design system for LLM」是新興賽道，值得與人類導向做語彙比較。 |
| [khazix-skills](khazix-skills.md) / [Andrej Karpathy Skills](andrej-karpathy-skills.md) | 都是 skill 生產源。khazix 是方法論 skill、karpathy 是 LLM 教學 skill、design-md-chrome 是**設計 skill 自動化**。三者代表 Claude Skill 生態的不同供應源：人類手寫 / 教學匯整 / 機器萃取。 |
| [UI UX Pro Max Skill](ui-ux-pro-max-skill.md) | UI UX Pro Max 是通用 UI/UX 設計 skill（設計理論），design-md-chrome 產出的是**特定網站的實體規範**。前者教「什麼是好設計」，後者答「這個網站的設計是什麼」。組合用效果最大：先套 UI UX Pro Max 定基準，再用 design-md-chrome 注入品牌特化。 |
| [frontend-design](https://www.typeui.sh/design-skills)（內建於 Anthropic Skills） | Anthropic 官方 frontend-design skill 的定位類似，但 TypeUI / design-md-chrome 提供**可客製、可擷取、可版本化**的替代方案。若你想把某一家公司的設計系統綁進 Claude Code（例如「永遠用我們官網的風格」），這條路線比官方 skill 可行。 |
| [claude-skills-guide](claude-skills-guide.md) | skills-guide 教你寫 skill，design-md-chrome **幫你自動生成設計類 skill**。讀完 skills-guide 了解結構後，用 design-md-chrome 為各種 design style 批次產出 skill.md，效率倍增。 |

### 值得追蹤的後續

- **v0.5+ 是否支援 dark mode / CSS variable 還原**：目前抓不到 `var(--token)`，如果後續整合 CSS OM 或 `document.styleSheets` 解析，token 品質會大升級。
- **TypeUI 48 套精選 design skill 的授權模式**：目前開放下載，若未來推商業方案，本擴充可能變成「免費版的野外採集器 + 付費版的精選庫」二分策略。
- **是否擴展到 Firefox / Edge / Arc**：Manifest v3 跨瀏覽器相容度高，Arc 的 AI 使用者是一塊沒人吃的蛋糕。
- **會否加入「反向生成」能力**：餵一份 DESIGN.md 回擴充套件，把 agent 產出的頁面對照驗證是否符合規範——這會是 design QA 新賽道。
- **是否和 [frontend-design skill](https://www.typeui.sh/design-skills) 或 [Figma Code Connect](https://www.typeui.sh/) 整合**：設計源頭（Figma）→ 擷取（Chrome 擴充）→ 實作（Claude Code）的全鏈自動化，是下一階段明顯的產品版圖。
