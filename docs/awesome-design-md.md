---
date: "2026-04-10"
category: "Coding Agent 工具"
card_icon: "material-palette-swatch"
oneliner: "58+ 個知名品牌 DESIGN.md 合集 — 丟進專案讓 AI Agent 產出 pixel-perfect UI"
---

# Awesome DESIGN.md — AI Agent 的設計系統資料庫

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) |
| 瀏覽網站 | [getdesign.md](https://getdesign.md/) |
| Google Stitch DESIGN.md 規格 | [stitch.withgoogle.com](https://stitch.withgoogle.com/docs/design-md/overview/) |
| MindStudio 教學 | [What Is Google Stitch's Design.md](https://www.mindstudio.ai/blog/what-is-google-stitch-design-md-file) |
| SimpleNews 報導 | [simplenews.ai](https://www.simplenews.ai/news/awesome-design-md-repository-hits-4385-stars-with-plain-text-design-systems-for-ai-coding-agents-k97b) |

## 專案概述

Awesome DESIGN.md 是由 VoltAgent 團隊維護的策展合集，收錄 58+ 個知名品牌的 `DESIGN.md` 檔案——一種由 Google Stitch 引入的純文字設計系統文件格式。核心用法極簡：**把一個 DESIGN.md 丟進你的專案根目錄，告訴 AI Agent「照這個風格做」，就能得到一致的 UI**。

`DESIGN.md` 的概念類似 `AGENTS.md`（告訴 Agent 怎麼建專案）和 `CLAUDE.md`（告訴 Agent 專案慣例），但專注於視覺設計：色彩、字型、元件樣式、佈局原則。Markdown 是 LLM 最擅長閱讀的格式，所以不需要 Figma 匯出、JSON design token 或特殊工具——就是一個 `.md` 檔案。

上線 3 天內累積 4,385 stars，截至研究時已達 38,975 stars。

## DESIGN.md 檔案結構

每個 DESIGN.md 遵循 [Google Stitch 格式](https://stitch.withgoogle.com/docs/design-md/format/)，包含 9 個標準區段：

| # | 區段 | 內容 |
|---|------|------|
| 1 | Visual Theme & Atmosphere | 整體氛圍、密度、設計哲學 |
| 2 | Color Palette & Roles | 語意化顏色名稱 + hex + 功能角色 |
| 3 | Typography Rules | 字型家族、完整層級表（H1-body-caption） |
| 4 | Component Stylings | Button、Card、Input、Nav 的各種狀態 |
| 5 | Layout Principles | 間距系統、grid、留白哲學 |
| 6 | Depth & Elevation | 陰影系統、表面層級 |
| 7 | Do's and Don'ts | 設計護欄與反模式 |
| 8 | Responsive Behavior | 斷點、觸控目標、收合策略 |
| 9 | Agent Prompt Guide | 快速色彩參考、即用型 prompt |

### 與其他 `.md` 慣例的對比

```
專案根目錄的 Agent 指令生態
─────────────────────────────────────────
  CLAUDE.md  → 告訴 Agent 專案的慣例和規則
  AGENTS.md  → 告訴 Agent 怎麼建造專案
  DESIGN.md  → 告訴 Agent 專案應該長什麼樣子
─────────────────────────────────────────
  三者互補，形成完整的 Agent 上下文
```

## 收錄品牌一覽（58+）

| 分類 | 品牌 |
|------|------|
| **AI & ML** | Claude、Cohere、ElevenLabs、Minimax、Mistral AI、Ollama、OpenCode AI、Replicate、RunwayML、Together AI、VoltAgent、xAI |
| **開發工具** | Cursor、Expo、Linear、Lovable、Mintlify、PostHog、Raycast、Resend、Sentry、Supabase、Superhuman、Vercel、Warp、Zapier |
| **基礎設施** | ClickHouse、Composio、HashiCorp、MongoDB、Sanity、Stripe |
| **設計 & 生產力** | Airtable、Cal.com、Clay、Figma、Framer、Intercom、Miro、Notion、Pinterest、Webflow |
| **金融 & 加密** | Coinbase、Kraken、Revolut、Wise |
| **企業 & 消費** | Airbnb、Apple、IBM、NVIDIA、SpaceX、Spotify、Uber |
| **汽車品牌** | BMW、Ferrari、Lamborghini、Renault、Tesla |

每個品牌的 DESIGN.md 都包含一句風格描述，例如：

- **Stripe** — Signature purple gradients, weight-300 elegance
- **Linear** — Ultra-minimal, precise, purple accent
- **Vercel** — Black and white precision, Geist font
- **Airbnb** — Warm coral accent, photography-driven, rounded UI
- **Ferrari** — Chiaroscuro black-white editorial, Ferrari Red with extreme sparseness

## 使用方式

```bash
# 方式 1：從 GitHub 直接複製
curl -o DESIGN.md https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/stripe/README.md

# 方式 2：從網站瀏覽並下載
# https://getdesign.md/stripe/design-md

# 方式 3：放進專案根目錄，告訴 Agent
# "Build me a landing page following the DESIGN.md spec"
```

**在 Google Stitch 中的運作方式：**

提交 prompt 時，Stitch 會同時把你的文字和完整 `DESIGN.md` 傳給 Gemini。模型將 DESIGN.md 視為「必須遵守的約束條件」，套用你指定的具體數值（`#1A73E8` 而非「一種可信賴的藍色」）。

**在 Claude Code 中的運作方式：**

把 `DESIGN.md` 放在專案根目錄，Claude Code 在產生前端程式碼時會自動讀取並遵循其中的設計規範——色彩、字型、元件樣式都會一致。

## DESIGN.md 撰寫最佳實踐

| 該做 | 不該做 |
|------|--------|
| 使用具體數值：`#1A73E8` | 使用模糊描述：「一種可信賴的藍色」 |
| 語意化命名：Primary、Error、Surface | 隨意命名：Blue1、Red2 |
| 只放 token 級資訊 | 放長篇設計哲學論述 |
| 存入 Git，審查變更後再合併 | 隨意修改不追蹤 |
| 保持精簡在 context window 內 | 塞入過多內容撐爆上下文 |

## 目前限制

| 限制 | 說明 |
|------|------|
| 只涵蓋 token 級資訊 | 不替代完整 design system（元件行為、UX 決策、互動模式不在範圍內） |
| 靜態快照 | 品牌網站改版後 DESIGN.md 不會自動更新 |
| 「inspired by」非官方 | 是從公開網站擷取的風格，非品牌官方提供的 design token |
| AI Agent 理解程度不一 | 不同 LLM 對同一份 DESIGN.md 的遵循程度有差異 |
| 無元件庫 | 只有設計規範，沒有可直接 import 的 React/Vue 元件 |
| 智財風險 | 複製品牌設計可能涉及商標/著作權，用於學習和靈感參考較安全 |

## 研究價值與啟示

### 關鍵洞察

1. **DESIGN.md 是 AI-native 設計系統的起點**：傳統 design system（Figma token、Style Dictionary JSON）是為人類和建置工具設計的。DESIGN.md 是第一個「為 LLM 設計的設計系統格式」——Markdown 是 LLM 最擅長的格式，不需要 parser、不需要 SDK。39K stars 證明了這個需求的真實性。

2. **Google Stitch 的標準化效應**：DESIGN.md 不是社群自發的格式，而是 Google Stitch 正式引入的標準。這代表「AI Agent 需要讀取設計規範」已經被大廠認可為正式需求，而非 hack。有了 Google 背書，DESIGN.md 可能成為 `package.json`、`tsconfig.json` 一樣的專案標配檔案。

3. **`CLAUDE.md` + `AGENTS.md` + `DESIGN.md` = 完整的 Agent 指令生態**：這三個檔案分別告訴 Agent「專案慣例」「怎麼建造」「應該長什麼樣」。放在專案根目錄，任何 Agent 都能快速理解一個專案的全貌。這是「Agent-native 專案架構」的雛形。

4. **策展價值 > 格式價值**：DESIGN.md 格式本身很簡單（就是 Markdown），但 Awesome DESIGN.md 的價值在於：有人幫你從 Stripe、Vercel、Linear 等知名品牌的網站中提取了完整的設計規範。這份策展工作（分析色彩系統、拆解字型層級、歸納元件樣式）才是耗時的部分。

5. **「Request a DESIGN.md」是聰明的社群增長策略**：使用者可以請求特定品牌的 DESIGN.md，甚至付費獲得「私人專屬」版本。這讓合集不斷成長，同時建立了商業化管道。

### 與其他專案的關聯

- **Context Hub**：Context Hub 提供「API 文件」讓 Agent 寫正確的後端程式碼，Awesome DESIGN.md 提供「設計規範」讓 Agent 寫正確的前端 UI——兩者是 Agent 知識生態的前後端
- **Slavingia Skills**：Slavingia 把書變成 skill，Awesome DESIGN.md 把品牌設計變成 Markdown——都是「把非結構化知識轉為 Agent 可消費的格式」
- **UI UX Pro Max Skill**：UI UX Pro Max 是教 Agent 「怎麼做好 UI/UX」的通用 skill，DESIGN.md 是告訴 Agent 「這個專案的 UI 長什麼樣」的具體規範——兩者組合使用效果最佳
- **Claude Skills Guide**：DESIGN.md 可視為一種特殊的「設計 skill」——不是 slash command，而是被動式的上下文檔案，Agent 自動讀取
