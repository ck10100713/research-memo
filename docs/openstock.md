# OpenStock 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/Open-Dev-Society/OpenStock |
| 社群 | Open Dev Society |
| Demo | HelloGitHub Featured |
| 授權 | AGPL-3.0 |

## 專案概述

OpenStock 是一個開源的股票市場追蹤平台，作為昂貴市場平台的替代方案。它提供即時價格追蹤、個人化警報和詳細的公司資訊，專為個人投資者打造，完全免費且永久開源。

這個專案的核心理念來自 Open Dev Society 宣言：「技術應該屬於每個人，知識應該開放、免費且可存取」。OpenStock 不是券商平台，市場數據可能會因提供者規則而有延遲。

適合場景：
- 需要免費股票追蹤工具的個人投資者
- 想學習現代 Web 應用架構的開發者
- 需要 AI 整合股票應用範例的研究者
- 尋找開源 Next.js 專案參考的開發者

## 核心功能

1. **身份驗證**：使用 Better Auth + MongoDB 實作 Email/Password 驗證
2. **全域搜尋**：Command + K 搜尋面板，支援 Finnhub 股票搜尋
3. **自選清單**：每個使用者獨立的 Watchlist，存於 MongoDB
4. **股票詳情**：TradingView 圖表、K線圖、技術指標、公司基本面
5. **市場總覽**：熱力圖、報價、新聞頭條（TradingView widgets）
6. **個人化 Onboarding**：收集投資目標、風險偏好、產業偏好
7. **AI 郵件**：使用 Gemini 產生個人化歡迎信與每日新聞摘要
8. **深色主題**：預設深色模式，使用 shadcn/ui 元件

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                    前端 (Next.js 15)                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  React 19 + TypeScript + Tailwind CSS v4               ││
│  │  shadcn/ui + Radix UI + Lucide icons                   ││
│  │  next-themes + cmdk (Command Palette)                  ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    認證 & 數據                               │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ Better Auth   │  │   MongoDB     │  │   Finnhub API   │ │
│  │ ───────────── │  │ ───────────── │  │ ─────────────── │ │
│  │ Email/Password│  │ 使用者資料    │  │ 股票資料       │ │
│  │ Protected     │  │ Watchlist     │  │ 公司資訊       │ │
│  │ Routes        │  │ 偏好設定      │  │ 市場新聞       │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    圖表 & 視覺化                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  TradingView Embeddable Widgets                        ││
│  │  • Symbol Info      • Candlestick Charts               ││
│  │  • Technical Charts • Company Fundamentals             ││
│  │  • Market Heatmap   • Top Stories                      ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    自動化 & 通知                             │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │   Inngest     │  │ Google Gemini │  │  Nodemailer     │ │
│  │ ───────────── │  │ ───────────── │  │ ─────────────── │ │
│  │ Events/Cron   │  │ AI 內容生成   │  │ Gmail SMTP      │ │
│  │ AI Inference  │  │ 個人化郵件    │  │ 郵件發送        │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 前置需求

- Node.js 20+ 和 pnpm 或 npm
- MongoDB 連線（Atlas 或本地 Docker）
- Finnhub API 金鑰
- Gmail 帳號（用於郵件發送）
- 可選：Google Gemini API 金鑰

### 安裝方式

```bash
# 克隆專案
git clone https://github.com/Open-Dev-Society/OpenStock.git
cd OpenStock

# 安裝依賴
pnpm install
# 或
npm install

# 設定環境變數
cp .env.example .env
# 編輯 .env 設定各項 API 金鑰
```

### 環境變數

```env
# Database
MONGODB_URI=mongodb+srv://<user>:<pass>@<cluster>/<db>

# Better Auth
BETTER_AUTH_SECRET=your_secret
BETTER_AUTH_URL=http://localhost:3000

# Finnhub
NEXT_PUBLIC_FINNHUB_API_KEY=your_key
FINNHUB_BASE_URL=https://finnhub.io/api/v1

# AI (Gemini)
GEMINI_API_KEY=your_key

# Email
NODEMAILER_EMAIL=your@gmail.com
NODEMAILER_PASSWORD=your_app_password
```

### 執行

```bash
# 開發模式
pnpm dev

# Inngest 本地執行（工作流程、排程、AI）
npx inngest-cli@latest dev

# 建構與部署
pnpm build && pnpm start
```

### Docker 部署

```bash
# 啟動 MongoDB 和應用
docker compose up -d mongodb && docker compose up -d --build
```

## 與其他工具的比較

| 特性 | OpenStock | Yahoo Finance | TradingView |
|------|-----------|---------------|-------------|
| 開源 | ✅ AGPL-3.0 | ❌ | ❌ |
| 自架 | ✅ | ❌ | ❌ |
| 即時數據 | ⚠️ 可能延遲 | ✅ | ✅ |
| AI 整合 | ✅ Gemini | ❌ | ❌ |
| 個人化 | ✅ | ⚠️ 有限 | ✅ |
| 費用 | 免費 | 部分付費 | 部分付費 |

## 研究心得

OpenStock 是一個展示現代 Web 應用最佳實踐的優秀範例，特別是在 Next.js 15 + AI 整合方面。

**技術亮點：**
1. **現代技術棧**：Next.js 15 App Router、React 19、Tailwind CSS v4
2. **Better Auth**：比傳統 NextAuth 更輕量的認證方案
3. **Inngest**：優雅的事件驅動架構和排程任務
4. **AI 整合**：Gemini 生成個人化內容

**對 AI Agent 開發的參考價值：**
- 展示如何將 AI (Gemini) 整合到實際應用中
- Inngest 的事件驅動架構可作為 Agent 任務調度參考
- 使用者偏好收集流程可用於 Agent 個人化

**限制與注意：**
- 使用 AGPL-3.0 授權，修改或部署需開源
- 不是券商，僅供追蹤和研究
- 市場數據可能延遲

---
研究日期：2026-02-03
