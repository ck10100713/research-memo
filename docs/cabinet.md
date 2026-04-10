---
date: "2026-04-10"
category: "AI 應用"
card_icon: "material-file-cabinet"
oneliner: "AI-first 知識庫 + 新創 OS — Markdown on disk、AI Agent 團隊、排程任務、自架部署"
---

# Cabinet — AI-First 知識庫與新創作業系統

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [hilash/cabinet](https://github.com/hilash/cabinet) |
| 官網 | [runcabinet.com](https://runcabinet.com) |
| 作者 | [Hila Shmuel](https://hila.sh/)（前 Apple Engineering Manager） |
| Discord 社群 | [discord.gg/rxd8BYnN](https://discord.gg/rxd8BYnN) |

## 專案概述

Cabinet 是前 Apple 工程經理 Hila Shmuel 以公開建造方式開發的開源專案，定位為「AI-first 新創作業系統」。它不只是筆記工具——而是一個整合知識庫、AI Agent 團隊、排程任務、內部聊天、看板管理的自架平台。

核心設計哲學：**所有東西都是 Markdown 檔案存在磁碟上**。沒有資料庫、沒有 vendor lock-in、資料不離開你的機器。每次儲存自動 git commit，完整版本歷史可追溯、可還原。

2026 年 4 月上線，一週內累積 975 stars。提供 20 個預建 AI Agent 模板，涵蓋 CEO、CTO、PM、行銷、工程、法務等角色，透過 5 個問題的 onboarding wizard 自動建立你的 AI 團隊。

## 核心功能

| 功能 | 說明 |
|------|------|
| WYSIWYG + Markdown | Tiptap 富文字編輯器，支援表格、程式碼、slash commands |
| AI Agent 團隊 | 每個 Agent 有目標、技能、排程任務，像真實團隊一樣運作 |
| 排程任務（Cron Jobs） | 基於 node-cron 的 Agent 自動化：每 6 小時 Reddit 偵察、週一週報 |
| 嵌入式 HTML Apps | 資料夾放 `index.html` 即渲染為 iframe，支援全螢幕 |
| Web Terminal | 瀏覽器內的本地 AI CLI 終端（xterm.js + node-pty） |
| Git-Backed 歷史 | 每次儲存自動 commit，完整 diff viewer，任意時間點還原 |
| Missions & Tasks | 看板式任務管理，將目標拆解為 missions |
| 內部聊天 | Agent 和人類在同一個頻道溝通 |
| 全文搜尋 | Cmd+K 即時搜尋，模糊匹配 |
| PDF & CSV Viewer | 原生支援 PDF 和試算表檢視 |

## 20 個 AI Agent 模板

| 部門 | Agent 角色 |
|------|-----------|
| 領導層 | CEO、COO、CFO、CTO |
| 產品 | Product Manager、UX Designer |
| 行銷 | Content Marketer、SEO Specialist、Social Media、Growth Marketer、Copywriter |
| 工程 | Editor、QA Agent、DevOps Engineer |
| 銷售與支援 | Sales Agent、Customer Success |
| 分析 | Data Analyst |
| 營運 | People Ops、Legal Advisor、Researcher |

## 技術架構

```
cabinet/
├── src/
│   ├── app/api/         → Next.js API routes
│   ├── components/      → React（sidebar, editor, agents, jobs, terminal）
│   ├── stores/          → Zustand 狀態管理
│   └── lib/             → Storage, markdown, git, agents, jobs
├── server/
│   └── cabinet-daemon.ts → WebSocket + job scheduler + agent executor
└── data/
    ├── .agents/.library/ → 20 個預建 Agent 模板
    └── getting-started/  → 預設 KB 頁面
```

**Tech Stack：** Next.js 16、TypeScript、Tailwind CSS、shadcn/ui、Tiptap、Zustand、xterm.js、node-cron

```
┌─────────────────────────────────────────────┐
│              Browser (port 3000)             │
│  ┌──────────┐ ┌────────┐ ┌───────────────┐  │
│  │ Tiptap   │ │ Agent  │ │ Web Terminal  │  │
│  │ Editor   │ │ Panel  │ │ (xterm.js)    │  │
│  └──────────┘ └────────┘ └───────────────┘  │
└────────────────────┬────────────────────────┘
                     │ API + WebSocket
┌────────────────────▼────────────────────────┐
│         cabinet-daemon (port 3001)           │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Job     │ │ Agent    │ │ node-pty     │  │
│  │ Cron    │ │ Executor │ │ Terminal     │  │
│  └─────────┘ └──────────┘ └──────────────┘  │
└────────────────────┬────────────────────────┘
                     │ read/write + git auto-commit
┌────────────────────▼────────────────────────┐
│          Filesystem (Markdown on disk)       │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐   │
│  │ Pages    │ │ .agents  │ │ HTML Apps  │   │
│  │ (.md)    │ │ configs  │ │ (index.html)│   │
│  └──────────┘ └──────────┘ └────────────┘   │
└──────────────────────────────────────────────┘
```

## 快速開始

```bash
# 一鍵安裝
npx create-cabinet@latest
cd cabinet
npm run dev:all

# 開啟 http://localhost:3000
# 5 個問題的 onboarding wizard 自動建立你的 AI 團隊
```

**需求：**

- Node.js 20+
- 至少一個 CLI provider：Claude Code CLI 或 Codex CLI
- macOS / Linux（Windows 需 WSL）

## 與 Obsidian / Notion 的比較

| 功能 | Cabinet | Obsidian | Notion |
|------|---------|----------|--------|
| AI Agent 編排 | ✅ | ❌ | ❌ |
| 排程 Cron Jobs | ✅ | ❌ | ❌ |
| 嵌入式 HTML Apps | ✅ | ❌ | ❌ |
| Web Terminal | ✅ | ❌ | ❌ |
| 自架 + 檔案存磁碟 | ✅ | ✅ | ❌ |
| 無資料庫/無 lock-in | ✅ | ✅ | ❌ |
| Git-backed 版本歷史 | ✅ | 需 plugin | ❌ |
| WYSIWYG + Markdown | ✅ | ✅ | ✅ |

## 設計哲學

| 原則 | 說明 |
|------|------|
| **Yours** | 資料在本地、可見、可攜——不被鎖在任何 AI provider 裡 |
| **Git everything** | 記憶應該有歷史——可檢視、可還原、可稽核知識如何演變 |
| **BYOAI** | 帶你自己的 AI：Claude、Codex、OpenCode、本地模型，不鎖定 provider |
| **KISS** | 保持簡單——純檔案、清楚的行為、開發者能理解的系統 |
| **Security** | AI 要處理你的文件和計畫，信任應該是設計需求而非事後想法 |
| **Self-hosted** | AI 持有你的上下文和計畫，應該跑在你控制的環境 |

## 目前限制

| 限制 | 說明 |
|------|------|
| 非常新 | 2026-04-03 建立，僅一週歷史，API 和功能可能快速變動 |
| 依賴外部 CLI | 需要 Claude Code CLI 或 Codex CLI，自身不包含 LLM |
| 無手機版 | Web-only，無原生行動應用 |
| 單機架構 | 無多使用者/多機器協作設計 |
| 無雲端同步 | 資料在本地磁碟，跨裝置需自行處理（Cloud Waitlist 已開放） |
| Agent 品質未驗證 | 20 個 Agent 模板的實際效用取決於底層 LLM 能力 |

## 研究價值與啟示

### 關鍵洞察

1. **「AI 團隊」比「AI 工具」更有想像力**：Cabinet 不是給你一個 AI 助手，而是給你一整支 AI 團隊——CEO 做策略、PM 做產品、Marketer 寫內容、Researcher 做調查。每個 Agent 有自己的目標、技能、排程任務。這種「模擬一家公司的運作」的設計，比單一 chatbot 更接近 AI Agent 的真實潛力。

2. **「嵌入式 HTML Apps」是最被低估的功能**：在知識庫的資料夾裡放一個 `index.html`，它就變成一個可互動的嵌入式應用，由 git 版本控制、可全螢幕。這讓 AI Agent 不只能寫文件，還能「製作工具」——Agent 可以寫一個簡單的 dashboard 或計算機，直接嵌入知識庫中使用。

3. **Markdown on disk + Git auto-commit 是最「honest」的儲存架構**：沒有資料庫意味著你可以用任何文字編輯器開啟檔案、用 git log 看歷史、用 grep 搜尋。這對開發者來說極度友善——「我的資料到底在哪裡？」永遠有明確答案。

4. **Cabinet vs AppFlowy 是兩種不同的「Notion 替代」路線**：AppFlowy 走的是「功能對標 Notion」（資料庫視圖、看板、日曆），Cabinet 走的是「超越 Notion」（AI Agent 團隊、排程任務、嵌入式 Apps、Web Terminal）。前者更穩定成熟，後者更有野心。

5. **前 Apple 工程主管的「公開建造」策略**：Hila Shmuel 選擇離開 Apple 以公開方式建造 Cabinet，在 Discord 與社群即時互動。這種透明度對開源專案的社群建設極為有效——一週 975 stars 證明了這一點。

### 與其他專案的關聯

- **AppFlowy**：同為「自架 + 本地優先 + AI」的生產力工具，但定位不同——AppFlowy 是「更好的 Notion」，Cabinet 是「AI 團隊的作業系統」
- **MemPalace**：MemPalace 是 AI 記憶宮殿，Cabinet 是 AI 團隊知識庫——兩者都在解決「AI session 結束後知識不見了」的問題
- **KC AI Skills 的 skill-cron**：Cabinet 的 Cron Jobs 和 skill-cron 解決相同問題——讓 AI 自動化排程執行。Cabinet 用 node-cron 內建，skill-cron 用系統 crontab
- **LobeHub**：LobeHub 是 AI Chat UI + Agent 市集，Cabinet 是 AI 知識庫 + Agent 編排——功能有重疊但切入角度不同
