---
date: "2026-05-05"
category: "AI 應用"
card_icon: "material-airplane"
oneliner: "阿里巴巴飛豬出品的 Claude Code / OpenClaw skill，把 Fliggy 機票飯店景點門票庫存接到 coding agent，2 個月衝 590 stars"
---

# FlyAI Skill 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/alibaba-flyai/flyai-skill> |
| 官網 | <https://open.fly.ai/> |
| npm CLI 套件 | <https://www.npmjs.com/package/@fly-ai/flyai-cli> |
| ClawHub 收錄 | <https://clawhub.ai/alibaba-flyai/flyai-skill> |
| Fliggy（飛豬，阿里巴巴旅遊平台） | <https://www.fliggy.com/> |

## 專案概述

`flyai-skill` 是 **阿里巴巴飛豬（Fliggy）** 官方做的 Claude Code / OpenClaw skill，把飛豬整個旅遊平台庫存（機票、火車、飯店、景點門票、演唱會、簽證、SIM 卡、郵輪、跟團…）接到 coding agent 對話框裡，讓你**不用切瀏覽器、不用切 App、直接在 terminal 用自然語言搜可預訂的旅遊商品**。

repo 2026-03-19 建立、MIT、**590 stars / 43 forks**（不到 2 個月）、版本 1.0.14。沒有顯式 language（純 skill 定義 + 呼叫外部 npm CLI）。

它的角色不是「另一個 agent framework」，而是**一個垂直業務 skill**：背後是飛豬封裝的 MCP API，前端是 npm CLI `@fly-ai/flyai-cli`，中間用 Claude Code skill 格式包裝。每個搜尋結果都附**直接可預訂的連結**，從查到買打通。

## 八個指令

| 指令 | 用途 | 必填 |
|------|------|------|
| `keyword-search` | 全類別自然語言關鍵字搜（一句話跨機票/飯店/景點/簽證/郵輪…） | `--query` |
| `ai-search` | 語意搜尋，理解複雜旅遊意圖（含預算、地點、時間混合條件） | `--query` |
| `search-flight` | 結構化機票搜，深度過濾 | `--origin` |
| `search-train` | 結構化火車票搜，深度過濾 | `--origin` |
| `search-hotel` | 飯店搜（依目的地、星級、床型、附近 POI） | `--dest-name` |
| `search-poi` | 景點搜（依城市、類別、評級） | `--city-name` |
| `search-marriott-hotel` | 萬豪集團飯店搜 | `--dest-name` |
| `search-marriott-package` | 萬豪套裝（下午茶、SPA bundle 等） | `--keyword` |

機票 / 火車的 `--sort-type` 共 8 種（價低→高、推薦、時長、出發早/晚、直飛優先…），飯店有 `distance_asc / rate_desc / price_asc / price_desc / no_rank` 五種。

## 安裝與啟動

**Skill 三條安裝路徑：**

```bash
# OpenClaw（推薦，走 ClawHub）
clawhub install flyai

# OpenClaw（npx）
npx skills add alibaba-flyai/flyai-skill

# Claude Code（手動 copy）
cp -r /path/to/flyai-skill/skills/flyai ~/.claude/skills/flyai
```

**CLI（必裝）：**

```bash
npm i -g @fly-ai/flyai-cli
flyai keyword-search --query "things to do in Tokyo"
```

**API key 選用**：預設零設定可跑，要 enhanced 結果才設 `flyai config set FLYAI_API_KEY "your-key"`。

## 運作流程

```
You ask your agent ──→ FlyAI Skill 啟動 ──→ flyai-cli 執行 ──→ Fliggy MCP API
                                                                  │
You see rich results ←── Agent 格式化 markdown ←── JSON response ←┘
```

- **Runtime**：Node.js
- **輸出**：單行 JSON 到 stdout，錯誤/提示到 stderr
- **Context 隔離**：每個指令獨立執行 context
- **Intent-based activation**：skill 註冊在 priority 90，agent 自動把旅遊類查詢路由到 FlyAI

## 涵蓋場景

| 類別 | 範例 |
|------|------|
| **交通** | 機票、火車、機場接送、租車、包車 |
| **住宿** | 飯店、民宿、客棧、機+酒套裝 |
| **體驗** | 景點門票、一日遊、私導、跟團遊 |
| **活動** | 演唱會、體育賽事、表演藝術、動漫展 |
| **服務** | 簽證、旅平險、SIM 卡、Wi-Fi 租賃 |
| **行程** | 郵輪、週末小旅行、蜜月、親子、遊學 |

## 目前限制與注意事項

- **生態以中國 / 亞洲為主**：飛豬是阿里巴巴旗下平台，飯店與火車庫存集中於中國境內，國際機票 / 飯店可搜但價格與訂位流程偏向中國使用者；**境外使用者要付款訂購可能會卡支付方式**（飛豬主要走支付寶）。
- **仍是商業漏斗的入口**：所有「booking link」最終會把你導去飛豬平台完成預訂，不是純粹的中立比價工具。
- **POI 類別僅中文 token**：`search-poi --category` 只接受 `自然风光 / 山湖田园 / 历史古迹 …` 等簡中固定詞彙，非中文 agent prompt 要先翻譯。
- **無 LICENSE 顯式版權年標示外的限制**：MIT 授權，但實際 API 用量受飛豬服務條款約束（README 沒明說 rate limit）。
- **依賴外部 npm CLI**：skill 本身只是 manifest + 路由設定，真正幹活的是 `@fly-ai/flyai-cli`（Node.js），少了 npm install 就不能跑。

## 研究價值與啟示

### 關鍵洞察

1. **大廠開始把 vertical inventory 包成 Claude Code skill**：飛豬 = 阿里旗下 OTA，這個 repo 等於是「阿里官方第一次把消費級旅遊商品庫存正式接到 coding agent」。當 OTA、訂餐、訂車、票務、電商都把自家 API 包成 skill 進駐 Claude Code / OpenClaw，coding agent 就會從「寫程式工具」演化成「可預訂任何東西的通用 client」── **terminal 直接變成下單入口**這個趨勢值得追蹤。

2. **Skill 是「intent router + thin CLI wrapper」的最佳示範**：FlyAI 自己幾乎不寫邏輯 ── skill manifest 寫 8 個指令的觸發 pattern（priority 90 自動 route），重活全部丟給 `@fly-ai/flyai-cli` 跑，CLI 再呼叫飛豬封裝的 MCP API。**這個分層讓 skill 本體小到可以 `cp -r` 安裝**，所有業務邏輯改動只要 `npm i -g @fly-ai/flyai-cli` 升級。比起把整套搜尋邏輯硬寫進 skill，這個架構升級代價低很多。

3. **`keyword-search` 與 `ai-search` 並存的設計值得學**：前者是廣度查詢（一句話跨類別），後者是語意查詢（理解「Labor Day 三天兩夜杭州西湖人均 2000 預算」這種混合條件）。**廣度 vs 深度兩條路徑同時開**，使用者依需求選一條，不用強迫所有查詢都走最貴的 LLM 路徑。對比之下很多「AI 搜尋」工具只開語意路徑、把簡單查詢也丟去做 embedding，是浪費。

4. **Bookable result 是這類 skill 的護城河**：很多 travel search agent 只給「資訊」（時刻表、價格、評論），但 FlyAI 每筆結果附直接 booking 連結 ── **背後是阿里既有的訂位 / 支付系統**。一個沒有底層 inventory + payment 的新創想做同樣的事，就要重新接航空公司、PMS、刷卡通道，門檻高到嚇人。這也是為什麼這類大廠 skill 即使 2 個月就 590 stars，仍然很難被獨立開發者複製。

5. **「priority 90 intent activation」反映 skill 路由戰場開始白熱化**：當 Claude Code / OpenClaw 上有 N 個 skill 都想接「我要訂機票」這條 prompt，誰的 priority 高、誰的 trigger pattern 寫得準，就贏走流量。**Skill 排序與 trigger 設計會變成下一個 SEO**，這個現象目前還沒被廣泛討論但會很快發生。

### 與其他研究筆記的關聯

- **[Slide Editor](slide-editor.md)** / **[design-md-chrome](design-md-chrome.md)** / **[Better Agent Terminal](better-agent-terminal.md)**：都是「把 Claude Code / Codex 包進垂直工作流」的小工具，但 FlyAI 是**大廠官方版** ── 同樣的 skill 形式、十倍以上的 stars、背後是真實 OTA inventory。
- **[Asgard Skills](asgard-skills.md)** / **[Slavingia Skills](slavingia-skills.md)** / **[KC AI Skills](kc-ai-skills.md)** / **[khazix-skills](khazix-skills.md)**：個人開發者的 skill 集，主題以開發 / 效率為主；FlyAI 把同樣的 skill 形式應用在 **B2C 旅遊預訂** 這個完全不同的領域。
- **[OpenClaw](openclaw.md)** / **[OpenClaw Claude Proxy](openclaw-claude-proxy.md)**：FlyAI 的另一個主要載體，README 把 OpenClaw 與 Claude Code 並列為一等公民。
- **[ITA Matrix](ita-matrix.md)**：另一個機票搜尋工具研究，但 ITA 是專業 power user 的「裸 fare construction」介面，FlyAI 走完全相反的路 ── 把搜尋包成自然語言問句、把結果格式化成 agent 對話 chunk。
