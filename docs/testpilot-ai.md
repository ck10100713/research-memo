---
date: "2026-04-14"
category: "開發工具"
card_icon: "material-test-tube"
oneliner: "用 GitHub Copilot SDK 分析網站並自動產生完整 Playwright 測試套件"
---

# TestPilot.AI 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [fugazi/testpilot-ai](https://github.com/fugazi/testpilot-ai) |
| 作者 LinkedIn | [Douglas Urrea Ocampo](https://www.linkedin.com/in/douglasfugazi) |
| 同作者的 QA Agent 技能庫 | [fugazi/test-automation-skills-agents](https://github.com/fugazi/test-automation-skills-agents) |
| GitHub Next TestPilot（不同專案） | [githubnext/testpilot](https://githubnext.com/projects/testpilot/) |
| Copilot SDK 文件 | [GitHub Copilot SDK](https://github.com/features/copilot) |

**作者：** Douglas Urrea Ocampo — SDET（Software Developer Engineer in Test），來自哥倫比亞

**專案狀態：** ⭐ 10 stars · TypeScript · MIT · 2026-01 創建 · Phase 2 開發中

## 專案概述

TestPilot.AI 是一個 AI 驅動的自動化測試平台，核心能力是：**輸入一個 URL，自動分析網站結構，然後產生完整的 Playwright 測試套件**（含測試策略文件、Page Object Models、測試腳本、`package.json`）。

它使用 **GitHub Copilot SDK** 作為 AI 引擎，不只是簡單的程式碼生成——而是先爬取目標頁面、分析 HTML 結構（表單、按鈕、連結、accessibility tree），再透過專門的 QA System Prompt 讓 Copilot 產生結構化的測試方案。生成的程式碼還會經過 TypeScript Compiler API 驗證語法正確性。

這不是企業級產品，而是一位 SDET 工程師的個人專案——但它展示了用 Copilot SDK 構建垂直 AI 工具的完整模式。

## 核心工作流程

```
使用者輸入 URL（例如 https://example.com）
       │
       ▼
┌─────────────────────────────────┐
│  1. Crawl — 伺服器端抓取 HTML   │
│     Cheerio 解析表單、按鈕、連結 │
│     提取 accessibility tree      │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  2. Agent — 資料送給 Copilot    │
│     使用專用 QA System Prompt   │
│     產生測試策略 + 程式碼        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  3. Validate — TS Compiler API  │
│     驗證語法和型別正確性         │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  4. Output — 結構化測試套件     │
│     • Test Strategy 文件        │
│     • Page Object Models        │
│     • Playwright 測試腳本        │
│     • package.json              │
│     → 打包為 ZIP 一鍵下載       │
└─────────────────────────────────┘
```

## 技術架構

| 層級 | 技術 |
|------|------|
| Frontend | Next.js 16 (App Router) + React 19 |
| AI Engine | GitHub Copilot SDK |
| UI | Tailwind CSS 4 + Radix UI + Lucide React |
| HTML 解析 | Cheerio |
| 程式碼驗證 | TypeScript Compiler API |
| 打包 | JSZip |
| 測試 | Vitest |

### 專案結構

```
src/
├── app/api/agent/          # Copilot Agent 邏輯 + QA System Prompt
├── components/
│   ├── dashboard/          # 分析結果、CodeViewer、StrategyView
│   ├── landing/            # Landing page
│   └── ui/                 # Radix/Shadcn 基礎元件
├── lib/
│   ├── parser.ts           # 網站爬蟲和解析
│   ├── validator.ts        # TypeScript 語法驗證
│   ├── mdParser.ts         # AI 回應的 Markdown 解析
│   └── metrics.ts          # 效能追蹤
```

## 快速開始

```bash
# 前置條件：Node.js 20+、pnpm、GitHub Copilot 訂閱

# 1. Clone
git clone https://github.com/fugazi/testpilot-ai.git
cd testpilot-ai

# 2. 安裝依賴
pnpm install

# 3. 安裝 Copilot CLI 並認證
npm install -g @github/copilot-cli @github/copilot
copilot auth login

# 4. 啟動
pnpm dev
# 開啟 http://localhost:3000
```

**使用方式：** 在 Dashboard 輸入目標網站 URL → 等待分析（有即時進度指示）→ 瀏覽 Test Strategy 和 Code → 下載 ZIP。

## 開發路線圖

| Phase | 狀態 | 內容 |
|-------|------|------|
| Phase 1 | ✅ 完成 | MVP：核心 Agent 整合 |
| Phase 2 | 🚧 進行中 | UI/UX 改進 + Artifact 驗證 |
| Phase 3 | 📅 規劃中 | Playwright MCP Integration（動態探索） |

> Phase 3 的 Playwright MCP 整合值得關注——目前只做靜態 HTML 分析，加入 MCP 後可以讓 Agent 實際操作瀏覽器探索 SPA 和動態內容。

## 目前限制 / 注意事項

- **需要 GitHub Copilot 付費訂閱** — SDK 需要認證，Free tier 可能不足
- **僅靜態分析** — 目前只爬取 HTML，無法處理 SPA/CSR 的動態內容（Phase 3 才會改善）
- **小型專案** — 10 stars、單人開發，生產環境使用需謹慎評估
- **測試品質取決於 Copilot** — 生成的測試可能需要人工修改，特別是複雜業務邏輯
- **無 CI/CD 整合** — 目前是獨立 Web 應用，未提供 CLI 或 GitHub Action 整合

## 研究價值與啟示

### 關鍵洞察

1. **「URL → 完整測試套件」是 AI 測試的理想 UX。** TestPilot.AI 把整個 QA 工作流壓縮成一步操作——不需要了解 Playwright API、不需要手寫 selector、不需要設計測試策略。雖然生成品質仍需驗證，但這個「零配置」的使用體驗是正確的產品方向。

2. **GitHub Copilot SDK 作為垂直 AI 工具的引擎。** 這是少見的 Copilot SDK 實際應用案例——不是在 IDE 裡補全程式碼，而是用 SDK 構建一個獨立的 Web 應用。這展示了 Copilot SDK 的另一種用法：作為 AI backbone 驅動特定領域的工具。

3. **TypeScript Compiler API 驗證是關鍵的品質閘門。** 大多數 AI 程式碼生成工具只管生成不管驗證。TestPilot.AI 用 TS Compiler API 自動檢查語法和型別錯誤——這讓生成的程式碼至少在語法層面是正確的，大幅降低了使用者的修正成本。

4. **Page Object Model 的自動生成比測試腳本更有價值。** 寫測試的最大痛點往往不是測試邏輯，而是 POM 的建立（找 selector、封裝操作）。TestPilot.AI 自動從 HTML 結構生成 POM，這部分的 ROI 可能比測試腳本本身更高。

5. **Phase 3 的 Playwright MCP 是質的飛躍。** 目前的靜態 HTML 分析對現代 SPA 幾乎無用（React/Vue 渲染前的 HTML 往往是空的）。加入 Playwright MCP 後，Agent 可以實際點擊、填表、導航——從「看網頁結構」升級為「實際使用網站」，這才是真正的 AI QA。

### 與其他專案的關聯

- **vs GitHub Next TestPilot：** 同名但不同專案。GitHub Next 的 TestPilot 聚焦於 unit test 生成（從程式碼產生），fugazi 的 TestPilot.AI 聚焦於 E2E test 生成（從網站 URL 產生）。兩者互補。
- **vs Boris Cherny 的驗證迴圈理念：** Boris 強調「讓 Claude 能驗證自己的產出」。TestPilot.AI 的 TS Compiler 驗證步驟就是這個理念的實踐——AI 生成 → 自動驗證 → 回饋修正。
- **對 Fluffy 生態的啟示：** fluffy-core-internal-dashboard（Next.js）可以考慮用類似方式自動生成 E2E 測試。特別是 Phase 3 的 Playwright MCP 模式——如果成熟的話，可以對 Dashboard 的每個頁面自動生成測試，大幅降低 QA 成本。
