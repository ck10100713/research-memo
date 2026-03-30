---
date: ""
category: "AI Agent 框架"
icon: "material-robot-outline"
oneliner: "Browser-in-the-Loop 自主 AI 代理，金字塔記憶可存 50 年對話精華"
---
# Project Golem 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [Arvincreator/project-golem](https://github.com/Arvincreator/project-golem) |
| develop 分支 | [project-golem/tree/develop](https://github.com/Arvincreator/project-golem/tree/develop) |
| SkillsLLM 頁面 | [skillsllm.com/skill/project-golem](https://skillsllm.com/skill/project-golem) |
| Line 社群 | [Project Golem AI 系統代理群](https://line.me/ti/g2/wqhJdXFKfarYxBTv34waWRpY_EXSfuYTbWc4OA) |
| Discord 社群 | [Project Golem 官方頻道](https://discord.gg/bC6jtFQra) |
| 作者 | Arvincreator & @sz9751210 |
| Stars | ~309 |
| 授權 | MIT |
| 語言 | JavaScript (Node.js 20+) |
| 版本 | v9.1（develop 分支） |
| 建立時間 | 2026-01-30 |

## 專案概述

Project Golem 是一個**自主 AI 代理系統**，以 Web Gemini 的無限上下文為大腦、Puppeteer 為雙手。它不是普通的聊天機器人，而是一個能記住你、主動行動、自學技能的 OS 級 AI Agent。

### 核心定位

- **Browser-in-the-Loop 架構**：不依賴官方 API，直接用 Puppeteer 操控瀏覽器存取 Web Gemini，免費享有 1M+ token 無限上下文
- **金字塔式長期記憶**：5 層壓縮機制，理論上可保存 50 年對話精華，僅佔 3MB
- **自主行動能力**：閒置時主動瀏覽新聞、自省思考、向你發送訊息
- **多智能體圓桌討論**：一個指令召喚多個 AI 專家進行辯論，產出共識摘要
- **動態技能擴充**：熱載入 skill 模組，甚至讓 AI 在沙盒中自寫新技能

## 系統架構

### Browser-in-the-Loop 核心

```
👤 使用者（Telegram / Discord / Web Terminal）
        │
        ▼
┌─────────────────────────────────────────┐
│          UniversalContext                │  ← 跨平台抽象層
│          (防抖隊列)                       │
├─────────────────────────────────────────┤
│       ConversationManager               │  ← 對話狀態管理
├─────────────────────────────────────────┤
│          GolemBrain                      │  ← LLM 核心
│    (Puppeteer → Web Gemini)             │  ← 操控瀏覽器，非 API
├─────────────────────────────────────────┤
│        NeuroShunter                     │  ← 解析 GOLEM_PROTOCOL
│    ┌────────┬────────┬────────┐         │
│    │ REPLY  │ MEMORY │ ACTION │         │  ← 神經分流
│    │ →回覆  │ →記憶  │ →技能  │         │
│    └────────┴────────┴────────┘         │
└─────────────────────────────────────────┘
```

**關鍵設計**：GolemBrain 輸出結構化的 `GOLEM_PROTOCOL` 指令（Markdown 內嵌 JSON），由 `NeuroShunter` 解析，精準分流為「回覆」「記憶」「動作」三類。

### 原始碼結構（develop 分支）

```
src/
├── bridges/       # 平台橋接（Telegram、Discord）
├── config/        # 設定管理
├── core/          # 核心引擎（GolemBrain、NeuroShunter）
├── i18n/          # 國際化
├── managers/      # 對話管理、排程管理
├── mcp/           # MCP Server 整合
├── memory/        # 金字塔記憶系統
├── scripts/       # 自動化腳本
├── services/      # 服務層
├── skills/        # 技能膠囊（熱載入）
├── utils/         # 工具函式
└── views/         # Web Dashboard
```

## 金字塔式長期記憶

這是 Golem 最獨特的技術能力：

| 層級 | 名稱 | 壓縮觸發 | 內容 |
|------|------|---------|------|
| Tier 0 | 原始日誌 | 即時 | 每小時對話紀錄 |
| Tier 1 | 每日摘要 | 72 小時後 | ~1,500 字的當日精華 |
| Tier 2 | 每月亮點 | 90 天後 | 月度重點提煉 |
| Tier 3 | 年度回顧 | 5 年後 | 年度里程碑 |
| Tier 4 | 紀元里程碑 | 永久 | 最重要的長期記憶 |

**50 年儲存對比：**

| 方式 | 檔案數 | 儲存空間 |
|------|--------|---------|
| 傳統（無壓縮） | ~18,250 | 500 MB+ |
| Golem 金字塔 | ~277 | **3 MB** |

## 指令系統

### 系統管理指令

| 指令 | 功能 | 說明 |
|------|------|------|
| `/sos` | 輕量急救 | 清除元素快取，DOM Doctor 重新掃描修復，不需重啟 |
| `/new` | 物理重生 | 強制重新整理瀏覽器，開啟全新對話 |
| `/new_memory` | 徹底轉生 | 清空資料庫，Golem 變成白紙 |
| `/model` | 模型切換 | 切換 Gemini Fast / Thinking / Pro 模式 |
| `/learn <功能>` | 自學技能 | AI 自動生成新技能模組 |
| `/skills` | 技能列表 | 列出已安裝的技能 |

### Google Workspace 擴充指令

透過 Puppeteer 操控 Web Gemini 的擴充功能：

| 指令 | 對應服務 |
|------|---------|
| `/@Gmail` | 讀取、搜尋個人郵件 |
| `/@Google 雲端硬碟` | 搜尋 Google Drive |
| `/@Google 文件` | 讀取 Google Docs |
| `/@Google Keep` | 讀取筆記 |
| `/@Google Tasks` | 管理待辦事項 |
| `/@YouTube` | 搜尋影片 |
| `/@Google Maps` | 查詢地圖 |
| `/@Google 航班` | 查詢航班 |
| `/@Google 飯店` | 查詢住宿 |

> 首次需 `headless: false` 手動授權一次 Google Workspace 權限，之後可切回 `headless: true` 背景運行。

## 快速開始

### 環境需求

- Node.js v20+
- Google Chrome（Puppeteer 自動化）
- Telegram / Discord Bot Token（選用）

### 安裝

```bash
# Mac/Linux 一鍵安裝
chmod +x setup.sh
./setup.sh --magic

# 啟動
./setup.sh --start
```

Windows 用戶建議使用 Git Bash 執行。

## 目前限制與注意事項

| 項目 | 說明 |
|------|------|
| **安全風險** | 絕對避免以 root/admin 身份運行 |
| **隱私敏感** | `golem_memory/` 含 Google 登入 Cookie session，務必妥善保管 |
| **Google 依賴** | 整個系統綁定 Web Gemini，Google 若改版 UI 需靠 DOM Doctor 修復 |
| **Workspace 限制** | 擴充功能僅限個人 `@gmail.com` 帳號，企業 / 學校帳號通常被鎖 |
| **非 API 架構** | 繞過官方 API 的做法有違反 ToS 的風險，且 Google 可隨時封鎖 |
| **Stars 尚少** | 309 stars，專案成熟度和社群支持有限 |

## Web Dashboard

提供完整的 Web 管理介面：

- **戰術控制台**：Agent 狀態總覽、活躍進程、動態行為決策、效能監控
- **即時終端機**：網頁端直接與 Golem 對話，追蹤任務狀態
- **技能管理**：安裝/開啟/關閉技能模組，如插拔隨身碟
- **人格設定**：設定 Golem 的基本屬性與行為模式，含人格市場
- **記憶核心**：查看金字塔記憶內容
- **系統設定**：安全權限、API Keys、指令白名單管理

## 研究價值與啟示

### 關鍵洞察

1. **Browser-in-the-Loop 是雙面刃**：透過 Puppeteer 操控 Web Gemini 繞過 API 限制，免費獲得 1M+ token 上下文和 Google Workspace 整合，但高度依賴 Google 前端穩定性，且有違反 ToS 的法律風險。這種做法適合個人玩具專案，不適合正式產品

2. **金字塔記憶是真正有價值的創新**：5 層壓縮把 50 年記憶壓到 3MB，這個設計思路比大多數 Agent 框架的記憶管理都成熟。概念上類似人類記憶的遺忘曲線——細節隨時間淡化，但重要事件永久保留

3. **GOLEM_PROTOCOL 的結構化輸出設計**：讓 LLM 輸出結構化的 JSON 指令而非純文字，再由 NeuroShunter 分流處理。這種「LLM 輸出協定」的模式在多種 Agent 框架中都有類似實踐，但 Golem 的分流設計（REPLY / MEMORY / ACTION）特別清晰

4. **繁體中文原生是加分項**：README、文件、社群（Line 群）都以繁體中文為主，對台灣開發者特別友善。這在 AI Agent 開源專案中非常少見

5. **「AI 自學技能」的邊界**：`/learn` 讓 AI 在沙盒中寫新技能模組是很酷的概念，但實際執行的品質和安全性值得存疑。沙盒隔離做得如何？生成的程式碼品質能否保證？這些都是開放問題

### 與其他專案的關聯

| 對比專案 | 關聯 |
|---------|------|
| 本站 [AutoGPT](autogpt.md) | 同為自主 AI Agent，但 Golem 走 Browser-in-the-Loop 路線而非 API 路線 |
| 本站 [CrewAI](crewai.md) | 都有多智能體協作能力，CrewAI 更標準化，Golem 更野生 |
| 本站 [Page Agent](page-agent.md) | 都用瀏覽器操作網頁，但 Page Agent 是 client-side 嵌入，Golem 是 server-side Puppeteer |
| [Moltbot](https://github.com/moltbot/moltbot) | 類似定位的 OS 級 AI 助理，但更偏個人生產力工具 |
| 本站[多 Agent 辯論會](multi-agent-debate.md) | Golem 的圓桌討論功能與多 Agent 辯論概念相似 |
