---
date: ""
category: "AI 創作資源"
icon: "material-palette"
oneliner: "台灣制服地圖的 3,000+ AI 圖像生成 prompt 資料庫，視覺預覽 + 跨維度快速組合"
---
# Uniform Map AI Prompts Database 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| AI Prompts Database | [uniform.wingzero.tw/zh-TW/prompts](https://uniform.wingzero.tw/zh-TW/prompts) |
| 官方首頁 | [uniform.wingzero.tw](https://uniform.wingzero.tw/en) |
| AI Photo Gallery | [AI 相片集](https://uniform.wingzero.tw/en/ai-photos) |
| 起源故事 | [紅色死神 — Uniform Map 起源與故事](https://www.wingzero.tw/article/sn/19) |
| X (Twitter) | [@uniform_map](https://x.com/uniform_map) |
| Instagram | [@uniformmap](https://www.instagram.com/uniformmap/) |
| Facebook | [Uniform Map 制服地圖](https://www.facebook.com/uniform.map/) |

> ⚠️ 網站有 bot 防護（403），以下資料主要從搜尋引擎索引和社群資料彙整。

## 專案概述

**Uniform Map 制服地圖** 是台灣開發者「紅色死神」（wingzero）創建的專案，起源於研究所時期一個用 Google Maps 標示學校制服的作業，後來在 PTT 爆紅、媒體大幅報導。

專案從純粹的「制服地圖」逐步演化，加入 **AI Prompts Database** 和 **AI Photo Gallery** 功能，成為一個結合制服文化記錄與 AI 圖像生成 prompt 資源的獨特平台。

核心功能：收錄 **3,000+ 個 AI 圖像生成 prompt**，支援 Midjourney、Stable Diffusion、Gemini、ChatGPT、Grok 等多種平台，提供**視覺化參考對照**和**快速 prompt 組合**功能，完全免費使用。

## AI Prompts Database 功能

### Prompt 分類體系

從搜尋引擎索引可確認的分類與數量：

| 分類 | 確認數量 | URL slug | 說明 |
|------|---------|----------|------|
| **Camera Angle** | 17 prompts | `/prompts/camera-angle` | 鏡頭角度（俯視、仰視、特寫等） |
| **Anime/Manga Style** | 81 prompts | `/prompts/anime-manga-style` | 漫畫家/插畫家畫風差異 |
| **Uniform Style** | 多項 | `/prompts/uniform-style` | 制服類型（Race Queen、校服等） |
| **Fantasy** | 多項 | `/prompts/fantasy` | 奇幻角色（Succubus 等） |
| **Hairstyle** | — | 已確認存在 | 髮型參考 |
| **Lighting** | — | 已確認存在 | 打光效果 |
| **Expression** | — | 推測存在 | 表情 |
| **Body Type** | — | 推測存在 | 體型 |
| **合計** | **3,000+** | | 全站 prompt 總數 |

### 核心功能

```
┌─────────────────────────────────────────────────┐
│           Uniform Map AI Prompts Database        │
│                                                 │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ Prompt 分類  │  │ 視覺對照    │              │
│  │ 瀏覽         │  │ 每個 prompt │              │
│  │             │  │ 附參考圖    │              │
│  └──────┬──────┘  └──────┬──────┘              │
│         │                │                      │
│         ▼                ▼                      │
│  ┌──────────────────────────────┐              │
│  │   Quick Prompt Combination    │              │
│  │   快速組合多個 prompt 元素     │              │
│  │                              │              │
│  │   Camera + Hair + Lighting   │              │
│  │   + Style + Uniform + ...    │              │
│  └──────────────┬───────────────┘              │
│                 │                               │
│                 ▼                               │
│  ┌──────────────────────────────┐              │
│  │   一鍵複製完整 prompt          │              │
│  │   → Midjourney / SD / Gemini │              │
│  │   → ChatGPT / Grok / ...    │              │
│  └──────────────────────────────┘              │
└─────────────────────────────────────────────────┘
```

**三大核心能力：**

1. **視覺化參考對照** — 每個 prompt 附帶 AI 生成的參考圖，不用猜效果就能挑選
2. **快速 prompt 組合** — 從不同分類（角度 + 髮型 + 打光 + 風格）自由搭配，組成完整 prompt
3. **跨平台相容** — 支援 Midjourney、Stable Diffusion、Gemini、ChatGPT、Grok 等主流平台

### AI Photo Gallery（AI 相片集）

除了 prompt 資料庫，平台還有 AI 相片集功能：

| 功能 | 說明 |
|------|------|
| 圖片上傳 | 使用者可上傳 AI 生成的圖片 |
| Metadata 記錄 | 填寫繪圖引擎、模型名稱、完整 prompt |
| 自動 Tag 轉換 | Prompt 自動轉為標籤，方便其他使用者搜尋 |
| 平台篩選 | 可按生成平台（Gemini、Grok 等）瀏覽 |
| 社群參考 | 他人的 prompt + 成品 = 最佳學習素材 |

## 支援的 AI 圖像生成平台

| 平台 | 類型 |
|------|------|
| **Midjourney** | 付費文生圖服務 |
| **Stable Diffusion** | 開源文生圖模型 |
| **Gemini** | Google AI |
| **ChatGPT** (DALL-E) | OpenAI |
| **Grok** | xAI |

## 專案背景與演化

```
研究所作業（Google Maps + 制服照片）
    ↓
PTT 分享 → 爆紅 → 媒體報導 → 上線首日流量崩潰
    ↓
制服地圖 v1：全台學校制服蒐集與地圖標記
    ↓
加入航空公司制服、職業制服、ACG 角色
    ↓
加入 AI Prompts Database（3,000+ prompts）
    ↓
加入 AI Photo Gallery（使用者投稿 AI 生圖 + prompt）
    ↓
現在：制服文化記錄 × AI 圖像生成 prompt 資源平台
```

開發者「紅色死神」從這個專案中成長，從只會做網頁設計和互動效果，發展到後端開發、系統架構、社群經營、媒體管理的全方位能力。

## 目前限制 / 注意事項

1. **Bot 防護嚴格** — 網站全面阻擋自動化存取（403），無法用 WebFetch 或爬蟲抓取，研究資料只能從搜尋引擎快取和二手來源取得
2. **Prompt 數量細節不透明** — 除 Camera Angle（17）和 Anime/Manga Style（81）外，其他分類的確切數量無法從外部確認
3. **偏重二次元風格** — 從可見的分類（Anime/Manga Style、Uniform Style、Fantasy）判斷，prompt 庫偏重動漫風格，寫實風格或商業攝影類 prompt 可能較少
4. **無 API 或程式化存取** — 純網頁介面，無法批次下載或整合到工作流程中
5. **NSFW 邊界模糊** — Fantasy 分類中包含 Succubus 等內容，使用者應注意各平台的內容政策
6. **非開源** — 平台本身非開源（雖然有第三方爬蟲 `issaclin32/wz_uniform_crawler` 在 GitHub 上）

## 研究價值與啟示

### 關鍵洞察

1. **「Prompt + 視覺預覽」是 prompt 資料庫的殺手級組合** — 大多數 prompt 庫只有文字（如 PromptHero、PromptBase），Uniform Map 的差異化在於每個 prompt 都附帶視覺化參考圖。這解決了 AI 圖像生成中最大的痛點：「這個 prompt 到底會出什麼效果？」視覺預覽讓使用者從「猜測」變為「挑選」，大幅降低試錯成本。

2. **分類維度的正交設計值得學習** — Camera Angle × Hairstyle × Lighting × Style × Uniform/Fantasy 的多維度正交分類，讓使用者可以自由組合產出千變萬化的完整 prompt。這個設計思想類似 LangGraph 的 State channel — 每個維度獨立管理，組合時才產生最終結果。

3. **從制服地圖到 AI Prompt 庫的轉型路徑有啟示性** — 一個研究所作業演化為 3,000+ prompt 的 AI 資源平台，關鍵轉折是辨識出「制服 / 角色設計」的視覺分類知識可以直接遷移為 AI prompt 的組織架構。這提示我們：**任何領域的結構化視覺知識都有潛力成為 AI prompt 資料庫**（例如建築風格、食物擺盤、室內設計）。

4. **社群 UGC + Metadata 是 prompt 資料庫的成長引擎** — AI Photo Gallery 讓使用者上傳圖片時必須填寫引擎 / 模型 / prompt，這些 metadata 自動轉為標籤，形成 prompt → 成品的「可驗證知識」。這比純粹的 prompt 清單有價值得多，因為每個 prompt 都有實際產出作為佐證。

5. **台灣開發者的獨特利基** — 制服文化（特別是校園制服、航空制服）在東亞有高度文化共鳴，Uniform Map 佔據了一個全球性 AI prompt 庫（如 PromptHero）不會特別深耕的細分市場。這種文化特異性 + 技術通用性的結合，是小型專案找到生存空間的典型策略。

### 與其他專案的關聯

- **Claude Financial Services Plugins**（`claude-financial-services-plugins.md`）：兩者看似不相關，但共享一個核心設計模式 — 用結構化的 Markdown/文字檔案編碼領域知識。Financial Services Plugins 用 SKILL.md 編碼金融分析知識，Uniform Map 用分類化 prompt 編碼視覺設計知識。兩者都讓非工程師（分析師 / 設計師）能直接貢獻和使用。
- **LobeHub**（`lobehub.md`）：LobeHub 的 10K+ Skills 市集是通用的 Agent 能力模組化平台，如果要把 Uniform Map 的 prompt 知識整合到 AI Agent 工作流中，可以打包成一個 MCP Server 或 LobeHub Skill，讓 Agent 自動根據需求組合最佳 prompt。
