# Claude Cowork Dispatch 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方說明 | [Claude Help Center — Assign tasks to Claude from anywhere](https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork) |
| 功能解析 | [Claude Dispatch Explained — LowCode Agency](https://www.lowcode.agency/blog/claude-dispatch-explained) |
| 實測評價 | [Hands-On with Claude Dispatch — MacStories](https://www.macstories.net/stories/hands-on-with-claude-dispatch-for-cowork/) |
| 設定教學 | [Claude Dispatch: Control Cowork From Your Phone — FindSkill.ai](https://findskill.ai/blog/claude-dispatch-remote-cowork/) |
| 產業分析 | [AINews: Claude Cowork Dispatch — Latent Space](https://www.latent.space/p/ainews-claude-cowork-dispatch-anthropics) |
| 使用心得 | [How Claude Dispatch turns your phone into an AI agent remote control](https://www.howdoiuseai.com/blog/2026-03-19-how-claude-dispatch-turns-your-phone-into-an-ai-ag) |
| Product Hunt | [Claude Dispatch — Product Hunt](https://www.producthunt.com/products/claude-dispatch) |
| 發布日期 | 2026-03-17（Research Preview） |
| 發布者 | Anthropic |

## 功能概述

Claude Cowork Dispatch 是 Anthropic 於 2026 年 3 月 17 日推出的 **Research Preview** 功能，內建於 Claude Cowork（Claude Desktop 的 Agent 模式）。核心概念：**用手機遠端遙控桌面上的 Claude Cowork session**。

> "Assign Claude a task, go do something else, and come back to the finished work."

你可以從手機傳訊息給桌面的 Claude，Claude 在你的電腦上執行任務（讀檔案、操作應用程式、使用 connectors），你回來時工作已經完成。

### 一句話定位

**手機是遙控器，桌面是執行者。** 不是雲端運算，是遠端操控。

## 運作架構

```
手機（Claude Mobile App）          桌面（Claude Desktop — Cowork）
┌──────────────────────┐          ┌──────────────────────────────┐
│ 傳送指令              │ ──────▶ │ 接收指令                      │
│ 接收結果              │ ◀────── │ 本地執行任務                   │
│ 回答權限請求           │ ◀─────▶ │ 存取檔案、connectors、外掛     │
│                      │          │ 全部在本地處理，資料不離開電腦   │
└──────────────────────┘          └──────────────────────────────┘
        │                                    │
        └──── 持續對話線程（跨裝置保留 context）──┘
```

### 關鍵設計

| 特性 | 說明 |
|------|------|
| **本地執行** | 所有處理都在桌面電腦上進行，檔案不會上傳到 Anthropic 伺服器 |
| **持續對話** | 跨裝置保留上下文，不需每次重新說明 |
| **端對端加密** | 手機與桌面之間的通訊使用 E2E 加密 |
| **權限閘門** | 破壞性操作（如刪除檔案）會暫停並推送通知到手機請求確認 |
| **單一線程** | 目前只支援一個對話線程，無法建立多個 |

## 設定方式

設定僅需約 2 分鐘：

1. **更新 Claude Desktop**（macOS 或 Windows x64）至最新版
2. **更新 Claude 行動 App**（iOS 或 Android）至最新版
3. 打開 Claude Desktop → 進入 **Cowork** 模式 → 點擊 **Dispatch**
4. 用手機掃描 **QR Code** 配對
5. 完成，開始使用

**不需要** API key、複雜設定或額外安裝。

### 系統需求

- Claude Desktop（macOS / Windows x64）
- Claude Mobile App（iOS / Android）
- Pro（$20/月）或 Max（$100-200/月）訂閱
- 兩台裝置皆需網路連線
- **桌面電腦必須保持喚醒狀態**

## 可以做什麼

### 成功率較高的任務

- 從本地試算表提取數據並生成摘要報告
- 搜尋 Slack / Email 並整理重點
- 查詢 Notion 資料庫內容
- 在 Google Drive 建立格式化簡報
- 快速檔案搜尋與資訊檢索
- 晨間郵件分類、會議準備

### 目前失敗率較高的任務

- 遠端開啟 Mac 應用程式
- 透過 iMessage 傳送檔案
- 存取 Safari 分頁資訊
- 部分第三方服務授權
- Terminal 存取

## Connectors 生態

Dispatch 繼承 Cowork 的 connector 生態，透過 **MCP（Model Context Protocol）** 連接 38+ 個工具：

| 類別 | 工具 |
|------|------|
| 通訊 | Slack、Gmail |
| 專案管理 | Jira、Trello、Asana、Linear |
| 文件 | Notion、Google Drive、Dropbox |
| 開發 | GitHub、GitLab |
| CRM | Salesforce、HubSpot |
| 設計 | Figma |
| 資料 | Snowflake |
| 行事曆 | Google Calendar |

搭配 Zapier MCP 可擴展到 8,000+ 應用程式。

## 目前限制

| 限制 | 說明 |
|------|------|
| **電腦必須保持開機** | 筆電休眠或 app 關閉就停止運作，這是遙控器不是雲端 |
| **成功率約 50%** | 複雜任務成功率不高，簡單任務（搜尋、摘要）較可靠 |
| **單一對話線程** | 無法同時建立多個 dispatch 線程 |
| **無完成通知** | 任務完成不會主動推播，需要手動回去查看 |
| **不支援排程** | 無法設定定時任務 |
| **Claude 不會主動聯繫** | 僅被動回應訊息 |
| **Research Preview** | 功能仍在早期階段，持續迭代中 |

## 安全考量

Anthropic 官方明確警告：

> "Instructions from your phone can trigger real actions on your computer — including reading, moving, or deleting local files."

### 安全機制

- **E2E 加密**：手機與桌面之間的通訊
- **權限閘門**：破壞性操作前推送通知請求確認
- **資料夾限制**：僅存取明確授權的資料夾和應用程式

### 需注意

- Dispatch 可以觸發 Cowork 有權限的任何操作
- 存在 prompt injection 風險
- 啟用前應確認信任所有已連接的應用程式和服務

## 訂閱方案

| 方案 | 價格 | Dispatch 支援 |
|------|------|--------------|
| Pro | $20/月 | 有（稍後開放） |
| Max | $100-200/月 | 有（首批開放） |
| Enterprise / Team | 未定 | 預計後續支援 |

## 與同類功能的比較

| 特性 | Claude Dispatch | OpenClaw（OpenAI） | Claude Code Background |
|------|----------------|-------------------|----------------------|
| 定位 | 手機遙控桌面 Agent | 雲端 coding agent | CLI 背景任務 |
| 執行環境 | 本地桌面 | 雲端沙箱 | 本地終端機 |
| 資料位置 | 不離開電腦 | 上傳到雲端 | 不離開電腦 |
| 介面 | 手機 App | Web UI | CLI |
| 連接器 | 38+ 本地 connectors | GitHub 整合 | 無（直接檔案存取） |
| 適用場景 | 離開桌面時的非同步任務 | 持續運行的 coding 任務 | 平行開發任務 |

## 研究價值與啟示

### 關鍵洞察

1. **「離開桌面」是真實的使用場景**：不是所有 AI 工作都發生在螢幕前，Dispatch 填補了「想到一件事但不在電腦旁」的空白
2. **本地優先的安全取捨**：資料不離開電腦是賣點也是限制——你的電腦必須開著。這與 OpenClaw 的雲端路線形成對比
3. **50% 成功率是誠實的現狀**：Research Preview 的定位讓使用者有正確期待，比起過度承諾更健康
4. **Connectors 是護城河**：38+ 個 MCP connectors 讓 Dispatch 不只是 chat，而是能操作真實工作流的 agent
5. **手機作為 Agent 遙控器**：這個 UX 範式可能比「開一個 web dashboard 看 agent 跑」更自然——因為手機是人類最常隨身攜帶的裝置

### 產業意義

Latent Space 將 Dispatch 定位為 Anthropic 對 OpenClaw 的回應。但兩者路線不同：

- **OpenClaw**：雲端優先，程式碼上傳到沙箱，持續運行
- **Dispatch**：本地優先，電腦是執行環境，手機是遙控器

這反映了 AI Agent 部署的兩大路線之爭：**雲端沙箱** vs **本地 Agent**。
