---
date: "2026-04-14"
category: "AI 應用"
card_icon: "material-home-search"
oneliner: "台灣看房 AI 管線 — Claude Code 驅動，自動掃描 591/信義/永慶，評估、追蹤、議價一條龍"
---

# tw-house-ops 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [kylinfish/tw-house-ops](https://github.com/kylinfish/tw-house-ops) |
| 靈感來源 | [santifer/career-ops](https://github.com/santifer/career-ops) |
| 依賴工具 | [agent-browser](https://www.npmjs.com/package/agent-browser)（網頁爬取） |
| 作者贊助 | [ko-fi/kylinwin](https://ko-fi.com/kylinwin) |

**作者：** kylinfish（台灣開發者）

**專案狀態：** ⭐ 83 stars · JavaScript · 2026-04-08 創建 · 活躍開發中

## 專案概述

tw-house-ops 是一個**建構在 Claude Code 之上的台灣看房 AI 管線**，把找房、評估、追蹤、試算、議價準備全部自動化。支援三種使用者：**租屋族**、**首購族**、**換屋族**。

核心概念是 **ops-style approach**（靈感來自 career-ops）：把找房當成一個可重複執行的 pipeline 來管理，而不是零散的手動搜尋。你在 Claude Code 裡貼上物件 URL 或輸入 `scan`，AI 就會自動爬取 591、樂屋網、信義、永慶、東森、住商等平台，產出結構化的評估報告。

> 使用原則：「以精準找房為目標，非大量瀏覽。Claude 不會代替你送出 offer、簽約或送出任何申請。」

## 核心工作流

```
scan                        ← 掃描目標區域各平台新物件
  │
  ▼
pipeline                    ← 批次評估 data/pipeline.md 中的 URL
  │
  ├─ agent-browser 爬取頁面
  ├─ 判斷租屋 / 買屋
  ├─ 比對實價登錄行情
  ├─ 計算通勤時間
  ├─ 五維度評分（0-5 分）
  │
  ▼
reports/                    ← 每間物件一份完整報告
  │
  ├─ compare 001, 003       ← 並列比較
  ├─ prepare visit for 001  ← 看屋清單 + 議價策略
  ├─ affordability           ← 可負擔房價試算（首購族）
  └─ upgrade plan            ← 換屋財務規劃（換屋族）
  │
  ▼
data/tracker.md             ← 全部物件的結構化追蹤表
```

## 操作指令

| 輸入 | 動作 |
|------|------|
| 貼上物件 URL | 自動判斷租/買 → 評估 → 產生報告 |
| `scan` | 掃描目標區域各平台新物件 |
| `pipeline` | 批次處理所有待評估 URL |
| `compare 001, 003` | 並列比較兩間物件 |
| `prepare visit for 001` | 看屋清單 + 議價策略 |
| `affordability` | 可負擔房價試算（首購族） |
| `upgrade plan` | 換屋財務規劃（換屋族） |
| `tracker` | 所有物件追蹤摘要 |

## 評分系統

五維度加權評分，租屋與買屋權重不同：

| 維度 | 租屋權重 | 買屋權重 |
|------|----------|----------|
| 價格合理性 | 30% | 35% |
| 空間與格局 | 20% | 20% |
| 區域生活機能 | 25% | 20% |
| 物件條件 | 15% | 15% |
| 風險與潛力 | 10% | 10% |

**判讀：** ≥4.0 推薦看屋 · 3.5–3.9 保留 · <3.5 建議跳過

## 物件追蹤狀態機

```
Scanned → Evaluated → Visit → Visited → Offer → Negotiating → Signed → Done
                 ↘ Skip        ↘ Pass                              
                                         → Expired（物件下架）
```

## 技術架構

```
tw-house-ops/
├── CLAUDE.md                 # 入口：模式路由 + 初始設定 + 資料合約
├── config/
│   └── profile.yml           # 個人設定（不會被系統覆寫）
├── portals.yml               # 各平台 URL 與掃描設定
├── modes/                    # Claude Code 的各模式指令
│   ├── _shared.md            # 評分維度 + 台灣市場知識
│   ├── _profile.md           # 個人情境（每次注入）
│   ├── scan.md               # 平台掃描器
│   ├── rent.md / buy.md      # 租屋 / 購屋評估
│   ├── afford.md             # 可負擔試算
│   ├── switch.md             # 換屋規劃
│   ├── compare.md            # 多物件比較
│   ├── visit.md              # 看屋清單
│   └── pipeline.md           # 批次處理器
├── data/
│   ├── pipeline.md           # 待評估 URL 收件匣
│   ├── tracker.md            # 物件追蹤主表
│   └── scan-history.tsv      # 去重紀錄
├── reports/                  # 各物件評估報告
└── *.mjs                     # 輔助腳本（合併、驗證、去重）
```

**關鍵設計：CLAUDE.md 作為路由器**

整個系統的入口是 `CLAUDE.md`，它定義了：
- 模式路由：根據使用者輸入自動選擇對應的 mode 檔案
- 初始設定流程：7 步驟自動化設定（約 5 分鐘）
- 資料合約：明確區分「使用者層」（不覆寫）和「系統層」（可更新）

**資料合約（保護使用者資料）：**

| 層級 | 檔案 | 自動更新？ |
|------|------|-----------|
| 使用者層 | `config/profile.yml`、`modes/_profile.md`、`data/*`、`reports/*` | ❌ 永不覆寫 |
| 系統層 | mode 檔案、`CLAUDE.md`、`*.mjs`、`templates/*` | ✅ 隨版本更新 |

## 快速開始

```bash
# 1. 安裝 agent-browser（爬取網頁必備）
npm install -g agent-browser
agent-browser --version

# 2. Clone 並在 Claude Code 開啟
git clone https://github.com/kylinfish/tw-house-ops.git
cd tw-house-ops
claude  # 開啟 Claude Code

# 3. Claude 自動偵測缺少設定 → 啟動 7 步初始設定（約 5 分鐘）
# 4. 設定完成後：
#    - 貼上 591/信義/永慶 URL → 自動評估
#    - 輸入 scan → 掃描目標區域
```

## 目前限制 / 注意事項

- **依賴 Claude Code** — 不是獨立應用，必須在 Claude Code 環境中執行
- **依賴 agent-browser** — 未安裝則無法爬取真實頁面，評估結果不可信
- **無 License** — 未宣告授權條款，使用與修改前需確認
- **台灣限定** — 評分維度、平台整合、法規知識都針對台灣市場
- **AI 評估 ≠ 專業鑑價** — 分數僅供參考，實價登錄比對有延遲，重大決策仍需專業意見
- **各平台反爬風險** — 頻繁掃描可能被 591 等平台封鎖

## 研究價值與啟示

### 關鍵洞察

1. **「Ops-style」是 AI Agent 應用的強力設計模式。** career-ops 把求職當 pipeline，tw-house-ops 把找房當 pipeline。核心思路是：**把原本零散的人工決策流程，結構化為可重複執行的自動化管線**。這個模式可以推廣到任何有「搜尋 → 評估 → 比較 → 決策」流程的場景（選車、選校、選投資標的等）。

2. **CLAUDE.md 作為路由器的設計非常優雅。** 不是把所有邏輯塞在一個巨大的 prompt 裡，而是用 CLAUDE.md 作為入口路由到不同的 mode 檔案（scan.md、buy.md、rent.md 等）。每個 mode 專注一件事，`_shared.md` 和 `_profile.md` 作為共享上下文注入——這是**模組化 prompt engineering** 的最佳實踐。

3. **資料合約（Data Contract）解決了 AI 系統最常見的痛點。** 明確區分「使用者層」（永不覆寫）和「系統層」（可更新），讓系統升級不會破壞使用者的個人設定和歷史資料。這個設計對任何需要持久化資料的 Claude Code 專案都有參考價值。

4. **五維度加權評分 + 狀態機追蹤 = 結構化決策。** 不是讓 AI 給一個模糊的「推薦/不推薦」，而是用具體的維度和權重產生可解釋的分數，再用狀態機追蹤每個物件的生命週期。這把 AI 從「回答問題」提升為「管理決策流程」。

5. **agent-browser 作為 Claude Code 的「眼睛」。** Claude Code 本身無法瀏覽網頁，agent-browser 補上了這個能力——讓 AI 可以實際爬取 591 等平台的物件頁面。這個模式（CLI tool 擴展 Agent 能力）在 MCP 生態中會越來越常見。

### 與其他專案的關聯

- **vs Career-Ops：** 直接靈感來源。career-ops 管理求職 pipeline（職缺搜尋、面試準備、offer 追蹤），tw-house-ops 管理找房 pipeline。兩者證明了 ops-style 模式的可移植性。
- **vs Karpathy LLM Wiki：** 兩者都是「用 AI 管理結構化知識」，但方向不同。LLM Wiki 編譯研究知識，tw-house-ops 編譯房屋物件資訊。tracker.md 就是一種領域特化的 wiki index。
- **vs Boris Cherny Tips 的 CLAUDE.md 設計：** Boris 建議用 CLAUDE.md 記錄 Claude 的錯誤行為。tw-house-ops 更進一步——用 CLAUDE.md 作為整個應用的路由器和架構定義，展示了 CLAUDE.md 的「框架級」用法。
- **對 Fluffy 生態的啟示：** modes/ 目錄的模組化 prompt 設計可以借鑑到 fluffy-agent-core——把不同的 Agent 能力分拆為獨立的 mode 檔案，用共享上下文注入個人化設定。
