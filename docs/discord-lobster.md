---
date: ""
category: "社群行銷"
icon: "material-robot-happy"
oneliner: "台灣一人公司的 Discord AI 社群管家——零依賴、$0/月、三支 cron 腳本管理 146 人社群"
---
# Discord Lobster 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原始文章 | [我們開源了 Discord 社群自動化機器人](https://ultralab.tw/blog/discord-lobster-open-source) |
| GitHub Repo | [ppcvote/discord-lobster](https://github.com/ppcvote/discord-lobster) |
| Ultra Lab 官網 | [ultralab.tw](https://ultralab.tw) |
| Discord 社群 | [一人公司實驗室](https://discord.gg/ewS4rWXvWk)（146+ 成員） |

## 專案概述

Discord Lobster（龍蝦）是台灣團隊 Ultra Lab 開源的 **Discord 社群 AI 自動管理機器人**。核心理念是讓一人公司 / solo founder 不需 24 小時在線，就能維持社群活躍度。

特色在於**極度簡約的架構**：三支獨立 Node.js 腳本 + cron 排程，零 npm 依賴、零資料庫、用 Gemini Flash 免費額度運行，月成本 $0。已在 Ultra Lab 自家 146 人 Discord 實戰驗證。

| 指標 | 數值 |
|------|------|
| Stars | 3（剛開源，2026-03-29） |
| 語言 | JavaScript |
| 授權 | MIT |
| 運行成本 | $0/月（Gemini Flash 免費額度） |
| 部署時間 | ~15 分鐘 |

## 核心功能

### 三隻獨立腳本架構

```
                    ┌─ cron 每 3 分鐘 ─┐
                    │  welcome.js       │  新人加入 → Gemini 讀 username
                    │  偵測 audit log   │  → 產生客製化歡迎訊息
                    └───────────────────┘

                    ┌─ cron 每 20 分鐘 ─┐
Discord Server ───→ │  vibes.js         │  讀最近 20 則訊息 → Gemini 判斷
                    │  #general 插嘴    │  是否值得回 → 60 分鐘冷卻
                    └───────────────────┘

                    ┌─ cron 每 10 分鐘 ─┐
                    │  memory.js        │  對話中擷取成員資訊
                    │  成員記憶建構     │  → 存入 JSON → 下次互動有記憶
                    └───────────────────┘
```

### 功能矩陣

| 功能 | 腳本 | 頻率 | 說明 |
|------|------|------|------|
| **自動歡迎** | `welcome.js` | 每 3 分鐘 | 讀取 audit log 偵測新成員，Gemini 根據 username 產生個性化歡迎語 |
| **聊天插嘴** | `vibes.js` | 每 20 分鐘 | 讀 #general 最近 20 則訊息，AI 判斷是否值得回覆，60 分鐘冷卻防洗版 |
| **回覆偵測** | `vibes.js` | 即時 | 有人回覆龍蝦訊息（5 分鐘內）→ 跳過冷卻直接回 |
| **成員記憶** | `memory.js` | 每 10 分鐘 | 從對話擷取職業/興趣/專案 → 存 `data/member-memory.json` |

### 技術特點

| 特性 | 做法 |
|------|------|
| **零依賴** | 只用 Node.js 內建模組（`https`、`fs`、`path`、`crypto`） |
| **無 daemon** | 純 cron 排程，不需要常駐程序 |
| **無資料庫** | JSON 檔案儲存記憶，git-friendly |
| **故障隔離** | 三支腳本完全獨立，一支掛掉不影響其他 |
| **免費運行** | Gemini Flash 免費額度 15 req/min，綽綽有餘 |

## 快速開始

```bash
git clone https://github.com/ppcvote/discord-lobster.git
cd lobster-kit
cp .env.example .env
# 編輯 .env：填入 Discord bot token、Gemini API key、channel ID、webhook URL
```

**前置需求：**

- Node.js 18+
- Discord bot（需開啟 Message Content Intent）
- Gemini API key（免費：[aistudio.google.com/apikeys](https://aistudio.google.com/apikeys)）
- Discord webhook

**Cron 排程：**

```cron
*/3 * * * * cd /path/to/lobster-kit && node welcome.js >> logs/welcome.log 2>&1
*/20 * * * * cd /path/to/lobster-kit && node vibes.js >> logs/vibes.log 2>&1
*/10 * * * * cd /path/to/lobster-kit && node memory.js >> logs/memory.log 2>&1
```

**個性化調教：** 搜尋原始碼中的 `Customize this prompt`，直接改 Gemini prompt 即可調整語氣（專業 / 搞笑 / 教學 / 中文回應）。

## 目前限制 / 注意事項

- **Stars 極少（3）**：2026-03-29 剛開源，社群採用度尚待觀察
- **功能簡單**：僅歡迎、插嘴、記憶三個功能，無法處理進階社群管理（踢人、分角色、排程活動）
- **單一 LLM 綁定**：硬編碼使用 Gemini Flash，若要換模型需自行改 code
- **記憶機制粗糙**：JSON 檔案儲存，成員數多時可能有效能問題，也缺乏語意搜尋
- **無 Web UI**：所有設定需改 `.env` 和 cron，對非工程師不友善
- **冷卻機制固定**：60 分鐘冷卻、5 分鐘回覆視窗是硬編碼，調整需改原始碼

## 研究價值與啟示

### 關鍵洞察

1. **「足夠好」的架構哲學**：Discord Lobster 最大的啟示不是技術，而是**架構決策的極簡主義**。三支獨立 cron 腳本、零依賴、JSON 當資料庫——這在工程美學上很「粗糙」，但它**真的跑了 146 人的社群而且有效**。這提醒我們：對一人公司而言，over-engineering 才是最大的風險。

2. **Gemini Flash 免費額度的商業模式啟示**：月成本 $0 是這個專案最吸引人的賣點。Google 的 Gemini Flash 免費額度（15 req/min）足以支撐一個中小型社群的 AI 互動需求。這意味著「AI 驅動的社群管理」已經不是成本問題，而是設計問題——如何讓 AI 介入得恰到好處、不過度打擾。

3. **「記憶」是社群 AI 的殺手功能**：三個功能中，member memory 最有潛力。一般 Discord bot 的回覆是 stateless 的，但 Lobster 能記住「你是物理治療師、對 AI 有興趣」，下次互動就能說「你上次提到復健，AI 能自動化你的預約系統」。這種 **cross-session personalization** 是讓 AI bot 感覺像「社群成員」而不是「工具」的關鍵。

4. **cron 取代 daemon 的取捨**：不跑常駐程序、用 cron 輪詢的模式犧牲了即時性（最多 3 分鐘延遲），但換來極高的穩定性和可維護性。一支腳本掛了不會拖垮其他功能。這種「無狀態、故障隔離」的設計模式，適合用在任何沒有專職 DevOps 的小團隊。

5. **台灣在地開源的 Open Source as Marketing 模式**：Ultra Lab 是台灣的一人 AI 工作室，開源 Lobster 的原因是「問的人太多了」。這是典型的 **open source → 建立信任 → 付費代設定服務** 商業模式。README 底部直接附「代客設定服務」連結，把開源當行銷漏斗。

### 與其他專案的關聯

- **Insta-Booster**（`docs/insta-booster.md`）：同屬「社群行銷」分類。Insta-Booster 專注 Instagram Reels 自動化，Lobster 專注 Discord 社群管理——兩者互補覆蓋不同平台的社群經營需求
- **LobeHub**（`docs/lobehub.md`）：LobeHub 有 39K+ MCP 市集和 Supervisor + Executor 架構，遠比 Lobster 複雜。但 Lobster 的極簡方案反過來說明：**不是每個社群 AI 需求都需要 enterprise-grade 框架**
- **Agency Agents**（`docs/agency-agents.md`）：144 個 AI Agent 人格庫。Lobster 的 prompt 自訂功能本質上就是在做「社群管理員人格設計」，只是更聚焦、更簡單
