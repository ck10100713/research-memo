---
date: "2026-04-10"
category: "AI 應用"
card_icon: "material-note-edit"
oneliner: "開源 Notion 替代品 — Flutter + Rust 打造，支援本地 AI、自架部署、資料自主"
---

# AppFlowy — 開源 AI 協作工作區

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [AppFlowy-IO/AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) |
| 官網 | [appflowy.com](https://appflowy.com) |
| Notion vs AppFlowy | [appflowy.com/compare](https://appflowy.com/compare/notion-vs-appflowy) |
| StackAlts 對比分析 | [stackalts.com](https://stackalts.com/appflowy-vs-notion.html) |
| Self-Hosting 指南 | [appflowy.com/docs](https://appflowy.com/docs/Step-by-step-Self-Hosting-Guide---From-Zero-to-Production) |
| It's FOSS 評測 | [itsfoss.com/appflowy](https://itsfoss.com/appflowy/) |

## 專案概述

AppFlowy 是目前最受歡迎的開源 Notion 替代品（69,400+ GitHub stars），由 Flutter（前端）+ Rust（後端）打造，主打**資料自主權**和**本地優先**架構。使用者的資料預設儲存在本機，同步功能為可選項，也可以自架 AppFlowy Cloud 實現團隊協作。

專案始於 2021 年，核心理念是：Notion 很好用，但你的資料不屬於你、離線不能用、也不能自架。AppFlowy 要在保持類似體驗的前提下，解決這三個問題。截至 2026 年，它已覆蓋 Notion 約 85% 的核心功能，擁有超過 400 位貢獻者和遍及 215 個國家的社群。

## 核心功能

### 功能矩陣

| 類別 | 功能 | 說明 |
|------|------|------|
| 文件 | 富文字編輯器 | Block-based，支援 Markdown |
| 資料庫 | Grid / Kanban / Calendar | 多視圖資料庫，類似 Notion Database |
| 任務 | 看板管理 | Kanban board + 屬性標籤 |
| AI | 內建 AI 助手 | 寫作輔助、腦力激盪、表格自動填充 |
| AI | 本地模型支援 | Ollama 整合，支援 Mistral 7B、Llama 3 等 |
| AI | 雲端模型 | GPT-5、Gemini 2.5、Claude 3.7 |
| 協作 | 即時同步 | AppFlowy Cloud 或自架伺服器 |
| 發布 | AppFlowy Sites | 將文件發布為網站 |
| 客製 | 主題/字型/佈局 | 可調整外觀與體驗 |

### 技術架構

```
┌─────────────────────────────────────────────┐
│              AppFlowy 客戶端                  │
│  ┌─────────────────┐  ┌──────────────────┐  │
│  │   Flutter UI     │  │   Rust Core      │  │
│  │   (跨平台前端)    │  │   (資料處理引擎)  │  │
│  │   Desktop/Mobile │  │   離線優先邏輯    │  │
│  └────────┬────────┘  └────────┬─────────┘  │
│           │                    │             │
│           └────────┬───────────┘             │
│                    │                         │
│           ┌────────▼─────────┐               │
│           │  本地 SQLite 儲存  │               │
│           └────────┬─────────┘               │
└────────────────────┼─────────────────────────┘
                     │ 可選同步
          ┌──────────▼──────────┐
          │  AppFlowy Cloud     │
          │  (官方雲 or 自架)    │
          │  Docker Compose     │
          └─────────────────────┘
```

### 平台支援

| 平台 | 管道 | 狀態 |
|------|------|------|
| macOS | 官網 / GitHub Releases | 穩定 |
| Windows | 官網 / GitHub Releases | 穩定 |
| Linux | Flathub / Snapcraft / 官網 | 穩定 |
| iOS | App Store | 可用（較不成熟） |
| Android | Play Store（≥ Android 10） | 可用（較不成熟） |

## 與 Notion 的比較

| 比較項目 | AppFlowy | Notion |
|----------|----------|--------|
| 費用 | 免費（個人/小型團隊） | $16/月/人 |
| 資料位置 | 本機優先，可選同步 | 雲端伺服器 |
| 離線支援 | 完整離線功能 | 需要網路連線 |
| 自架 | Docker 部署，完整控制 | 不支援 |
| AI | 內建 + 本地模型（Ollama） | Notion AI（雲端） |
| 手機體驗 | 早期階段，明顯不如 Notion | 成熟流暢 |
| 整合 | 生態系較小 | 100+ 原生整合 |
| 效能 | Rust 編譯，啟動快、大量資料流暢 | JavaScript，大型資料庫可能卡頓 |
| 開源 | AGPL-3.0 | 閉源 |

### 與其他開源替代品的定位

| 專案 | 架構 | 特色 | GitHub Stars |
|------|------|------|-------------|
| **AppFlowy** | Flutter + Rust | 本地優先、Notion 功能對標 | 69K+ |
| **AFFiNE** | Web（React） | 白板 + 文件融合 | ~45K |
| **Anytype** | Go + Electron | P2P 加密、無伺服器同步 | ~25K |

## 快速開始

```bash
# 方式 1：直接下載
# https://github.com/AppFlowy-IO/AppFlowy/releases

# 方式 2：Linux via Flathub
flatpak install flathub io.appflowy.AppFlowy

# 方式 3：自架 AppFlowy Cloud（團隊協作）
# 參考：https://appflowy.com/docs/Step-by-step-Self-Hosting-Guide---From-Zero-to-Production

# 方式 4：從原始碼建置
git clone https://github.com/AppFlowy-IO/AppFlowy.git
# 參考：https://docs.appflowy.io/docs/documentation/appflowy/from-source
```

**本地 AI 設定（Ollama）：**

AppFlowy 支援透過 Ollama 執行本地 LLM，實現完全離線的 AI 功能——AI 推論不離開你的機器。

## 目前限制

| 限制 | 說明 |
|------|------|
| 手機體驗不成熟 | iOS/Android app 明顯落後 Notion 的流暢度 |
| 整合生態弱 | 沒有 Slack、GitHub、Google Drive 等原生整合 |
| AI 功能不及 Notion AI | 跨文件 Q&A、自動摘要等進階功能尚未到位 |
| 自架有門檻 | Docker Compose 部署對非技術使用者不友善 |
| AGPL 授權 | 對企業內部修改有開源義務，可能影響商用決策 |
| 無 API / Webhook | 第三方自動化整合受限 |
| 匯入功能有限 | 從 Notion 遷移不完美，部分資料庫結構會遺失 |

## 研究價值與啟示

### 關鍵洞察

1. **「資料自主權」正在從小眾需求變成主流期待**：AppFlowy 的 69K+ stars 不只是因為它是「免費的 Notion」，更因為「資料存在我的機器上」這個承諾。在 GDPR、資料主權法規越來越嚴格的趨勢下，local-first 架構從技術偏好變成合規需求。

2. **Flutter + Rust 是跨平台原生應用的最佳組合之一**：Flutter 提供跨 6 個平台的統一 UI，Rust 提供高效能的資料處理核心。這比 Electron（笨重）或純 Web（效能差）都更適合做需要離線能力的生產力工具。AppFlowy 是這個技術組合的旗艦展示案例。

3. **本地 AI（Ollama 整合）是殺手級差異化**：Notion AI 只能用雲端模型，而 AppFlowy 讓你用 Ollama 跑 Mistral、Llama 等本地模型。對於處理敏感資料的團隊（法律、醫療、金融），「AI 推論不離開機器」是無法用 Notion 做到的。

4. **85% 功能覆蓋率是「夠用」的門檻**：大多數使用者不需要 Notion 的 100+ 整合和進階 AI。AppFlowy 覆蓋了文件+資料庫+看板+AI——對個人和小團隊來說，這就是全部。剩下的 15% 是 Notion 的護城河（手機體驗、整合生態、企業功能），但不是每個人都需要。

5. **AGPL 授權是雙面刃**：AGPL 保證了專案的開源性（任何修改都必須開源），但也嚇退了一些想在內部深度客製的企業。相比之下，AFFiNE 用 MIT 授權，Anytype 也是較寬鬆的授權。這是 AppFlowy 在企業市場的潛在障礙。

### 與其他專案的關聯

- **LobeHub**：同樣是開源 AI 應用的代表，LobeHub 專注於 Chat UI + Agent 生態，AppFlowy 專注於工作區 + 文件協作——兩者展示了開源 AI 應用的不同切入點
- **MemPalace**：MemPalace 是 AI 記憶系統，AppFlowy 是 AI 工作區——如果 AppFlowy 能整合類似 MemPalace 的跨文件記憶能力，會成為更強大的知識管理工具
- **OpenDataLoader PDF**：AppFlowy 的文件能力可以和 PDF 處理工具互補，形成「匯入 PDF → AppFlowy 整理 → AI 分析」的工作流
