---
date: "2026-03-30"
category: "Coding Agent 工具"
icon: "material-palette-outline"
oneliner: "54K stars 的 AI 設計智慧注入系統——161 條行業推理規則 + 67 種 UI 風格，讓 Coding Agent 寫出有品味的 UI"
---
# UI UX Pro Max Skill 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| 官網 | [uupm.cc](https://uupm.cc) |
| npm CLI | [uipro-cli](https://www.npmjs.com/package/uipro-cli) |
| DEV Community 專題 | [Open Source Project of the Day (Part 7)](https://dev.to/wonderlab/open-source-project-of-the-day-part-7-uiux-pro-max-skill-ai-design-intelligence-for-building-4bd5) |
| Snyk 推薦 | [Top 8 Claude Skills for UI/UX Engineers](https://snyk.io/articles/top-claude-skills-ui-ux-engineers/) |
| DeepWiki | [UI/UX Pro Max Skill](https://deepwiki.com/nextlevelbuilder/ui-ux-pro-max-skill/3-uiux-pro-max-skill) |

## 專案概述

| 項目 | 數值 |
|------|------|
| Stars | 54,602 |
| Forks | 5,294 |
| Language | Python |
| License | MIT |
| 最新版本 | v2.5.0 |
| 最近 commit | 2026-03-28 |
| 創建日期 | 2025-11-30 |

UI UX Pro Max Skill 是一個**為 AI Coding Agent 注入設計智慧**的 Skill 系統。它不是一個 UI 元件庫，也不是一個 Figma 插件——它是一套結構化的設計知識資料庫，讓 Claude Code、Cursor、Windsurf 等 20+ AI 程式助手在產生 UI 程式碼時，能自動套用專業等級的設計系統（配色、字體、佈局模式、反模式偵測）。

核心解決的問題：AI Coding Agent 寫出的 UI 通常缺乏設計品味——配色不協調、字體搭配不對、間距混亂、缺少 hover 動效。UUPM 透過一套 161 條行業推理規則 + 67 種 UI 風格 + 161 組配色方案，讓 AI 在寫 code 之前先「推理」出最適合的設計系統。

## 核心功能與技術架構

### v2.0 旗艦功能：Design System Generator

```
使用者請求 → 多維度搜尋（5 平行查詢）→ 推理引擎（BM25 排序）→ 完整設計系統輸出
```

| 維度 | 資料量 | 說明 |
|------|--------|------|
| 行業推理規則 | 161 條 | 按產品類型推薦 pattern + style + color + font |
| UI 風格 | 67 種 | Glassmorphism、Brutalism、Neumorphism、Bento Grid 等 |
| 配色方案 | 161 組 | 與 161 個行業規則 1:1 對應 |
| 字體搭配 | 57 組 | Google Fonts 搭配，附 mood 標籤 |
| Landing Page 模式 | 24 種 | Hero-Centric、Conversion-Optimized 等 |
| 圖表類型 | 25 種 | Dashboard 與 analytics 推薦 |
| UX 準則 | 99 條 | Best practices + anti-patterns + accessibility |
| 支援技術棧 | 15 個 | React、Next.js、Vue、Nuxt、Svelte、SwiftUI、Flutter 等 |

### 設計系統輸出格式

針對每個請求，推理引擎產出完整的設計規格：

- **Pattern** — Landing page 區塊結構與順序
- **Style** — UI 風格關鍵字、適用場景、效能/無障礙評級
- **Colors** — Primary / Secondary / CTA / Background / Text 完整配色
- **Typography** — 標題 + 內文字體搭配，附 Google Fonts 連結
- **Effects** — Shadow、transition、hover 動效建議
- **Anti-patterns** — 該行業不該做的事（如銀行 app 不該用 AI purple/pink 漸層）
- **Pre-delivery Checklist** — SVG icon、cursor-pointer、對比度、響應式斷點等

### 架構：Template-Based Generation

```
src/ui-ux-pro-max/
├── data/          ← CSV 格式的設計知識庫（styles、colors、fonts、rules）
├── scripts/       ← Python 搜尋引擎 + BM25 排序 + 設計系統生成器
└── templates/     ← 各平台 skill 設定模板（Claude、Cursor、Windsurf...）

cli/               ← npm CLI (uipro-cli)，從 templates 動態生成各平台檔案
```

Python `search.py` 是核心：

- `--design-system` 模式：5 平行搜尋 → BM25 ranking → 組合輸出
- `--domain` 模式：單一維度搜尋（style / typography / chart）
- `--stack` 模式：技術棧特定的 guideline
- `--persist` 模式：輸出寫入 `design-system/MASTER.md`，支援 page-level override

## 安裝與使用方式

### CLI 安裝（推薦）

```bash
npm install -g uipro-cli
cd /path/to/your/project

# 選擇你的 AI 助手
uipro init --ai claude       # Claude Code
uipro init --ai cursor       # Cursor
uipro init --ai all          # 一次裝全部

# 全域安裝（所有專案共用）
uipro init --ai claude --global
```

### Claude Marketplace 安裝

```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### 使用模式

**Skill Mode（自動啟動）**：直接描述需求，Skill 自動觸發

```
Build a landing page for my SaaS product
```

**直接呼叫設計系統**：

```bash
# 產生完整設計系統
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Serenity Spa"

# 持久化設計系統（Master + Page Overrides）
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp"
```

### 支援平台（20+）

| 類別 | 平台 |
|------|------|
| **Anthropic** | Claude Code |
| **IDE 內建** | Cursor、Windsurf、Kiro、Trae |
| **GitHub** | Copilot |
| **CLI** | Codex CLI、Gemini CLI、OpenCode |
| **其他** | Antigravity、Roo Code、Continue、CodeBuddy、Droid、KiloCode、Warp、Augment、Qoder |

## 目前限制與注意事項

1. **依賴 Python 3.x** — 搜尋引擎用 Python 撰寫，沒裝 Python 的環境無法使用設計系統生成
2. **知識庫品質不透明** — 161 條規則是否真正反映業界最佳實踐，缺乏獨立驗證
3. **CSV 資料庫天花板** — 所有設計知識存在 CSV 檔案中，擴展性和查詢效率有上限
4. **不處理設計 token 輸出** — 產出的是 ASCII/Markdown 格式的設計規格，不是 Figma token 或 Style Dictionary，無法直接匯入設計工具
5. **高度依賴 AI 助手的遵守度** — 設計系統只是「建議」，最終 AI 是否忠實執行取決於 LLM 的 instruction following 能力
6. **69 個 open issues** — 社群活躍但有一定的未解決問題積壓

## 研究價值與啟示

### 關鍵洞察

1. **「AI Coding Agent 的品味問題」是真實痛點** — 54K+ stars 證明市場需求存在。AI 寫的 code 功能正確但缺乏設計品味，這個 gap 用「結構化設計知識庫 + 行業推理規則」來補，是一個聰明的切入角度。

2. **Skill 作為「知識注入」的價值** — UUPM 的核心不是程式碼，是知識。161 條行業規則 + 67 種風格 + 161 組配色，本質是把資深 UI 設計師的經驗壓縮成可查詢的 CSV，再透過 Skill 機制注入 AI 的 context window。這比訓練一個「懂設計的 LLM」成本低得多。

3. **Cross-platform Skill 的先驅案例** — 同時支援 20+ AI 助手（從 Claude 到 Cursor 到 Gemini CLI），用 template-based generation 解決各平台格式差異。這是目前看到最野心勃勃的跨平台 Skill 分發策略。

4. **Anti-pattern 比 Best Practice 更有價值** — 設計系統輸出中最獨特的部分是「該行業不該做的事」（如銀行 app 避免 AI purple/pink gradients）。相比正面建議，負面約束更容易被 AI 遵守，也更能避免災難性的設計錯誤。

5. **Design System as Code 的輕量路線** — 沒有用 Figma API、沒有用 Style Dictionary、沒有用 Design Token——就是 CSV + Python script + Markdown 輸出。這條「夠用就好」的路線讓它能在 4 個月內從 0 衝到 54K stars。

### 與其他專案的關聯

- **vs. [Superpowers](superpowers.md)** — 同屬「Coding Agent Skill」生態，但 Superpowers 偏向開發紀律與流程控制，UUPM 專注 UI/UX 設計品質。兩者可以疊加使用：Superpowers 管流程，UUPM 管設計。
- **vs. [Claude Skills Guide](claude-skills-guide.md)** — UUPM 是 Claude Skills 機制的頂級實作案例，可作為「如何建構一個好的 Skill」的範本研究。
- **vs. [Agency Agents](agency-agents.md)** — Agency Agents 提供「人格」（144 個角色），UUPM 提供「專業知識」（設計系統）。一個解決 AI「是誰」，一個解決 AI「懂什麼」。
- **vs. [Everything Claude Code](everything-claude-code.md)** — Everything 是全方位 harness 效能強化，UUPM 是垂直領域的知識注入。在 Claude Code 生態中屬於互補關係。
