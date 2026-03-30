---
date: ""
category: "AI Agent 框架"
card_icon: "material-fishbowl"
oneliner: "40K stars 群體智能預測引擎，用數千 AI Agent 模擬平行社會推演未來"
---
# MiroFish 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [666ghj/MiroFish](https://github.com/666ghj/MiroFish) |
| 官網 | [mirofish.ai](https://mirofish.ai) |
| 線上 Demo | [mirofish-live-demo](https://666ghj.github.io/mirofish-demo/) |
| DEV Community 技術解析 | [The Open Source Swarm Intelligence Engine](https://dev.to/beitroot/mirofish-the-open-source-swarm-intelligence-engine-that-simulates-the-future-2h21) |
| 博客園深度評論 | [從 MiroFish 看群體智能預測的可能與不可能](https://www.cnblogs.com/informatics/p/19704252) |
| 知乎討論 | [如何評價登頂 GitHub 趨勢榜的 MiroFish？](https://www.zhihu.com/question/2014290448701679302) |
| Medium 分析 | [Swarm-Intelligence with 1M Agents](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | 666ghj / 盛大集團（陳天橋）孵化 |
| Stars | 40K+ |
| 語言 | Python (後端) + Vue.js (前端) |
| 授權 | AGPL-3.0 |
| 建立 | 2025-11-26 |
| 融資 | 3000 萬人民幣（~$4.1M），24 小時內完成 |

MiroFish 是一款基於**多智能體群體模擬**的 AI 預測引擎。核心概念：提取現實世界的「種子資訊」（新聞、政策、金融訊號、甚至小說），自動建構一個平行數位世界，在其中部署成千上萬具備獨立人格、長期記憶與行為邏輯的 AI Agent，透過自由交互產生**群體湧現行為**，從而推演未來走向。

簡單說：**不是用一個大模型直接預測，而是用一群小 Agent 模擬整個社會系統的演化，讓預測從互動中自然浮現。**

2026 年 3 月 7 日登頂 GitHub Trending 全球榜首，兩週內累積超過 25K stars。

## 核心架構：五階段 Pipeline

```
使用者上傳種子材料（報告、新聞、小說...）
    │
    ▼
┌──────────────────────┐
│ 1. 圖譜構建            │ ← GraphRAG 提取實體與關係
│    Knowledge Graph     │   建構結構化知識圖譜（非純文字）
│                        │   注入個體與群體記憶
└──────────┬─────────────┘
           ▼
┌──────────────────────┐
│ 2. 環境搭建            │ ← Environment Config Agent
│    World Building      │   生成 Agent 人設（人口結構、權力關係）
│                        │   注入仿真參數
└──────────┬─────────────┘
           ▼
┌──────────────────────┐
│ 3. 模擬執行            │ ← 雙平台並行（Twitter / Reddit 模擬）
│    Simulation          │   Agent 自主交互（23 種社交動作）
│                        │   可中途注入變數（上帝視角）
│                        │   動態更新時序記憶
└──────────┬─────────────┘
           ▼
┌──────────────────────┐
│ 4. 報告生成            │ ← Report Agent 分析湧現模式
│    Report Generation   │   結構化預測報告
└──────────┬─────────────┘
           ▼
┌──────────────────────┐
│ 5. 深度互動            │ ← 與模擬世界中任意 Agent 對話
│    Deep Interaction    │   與 Report Agent 追問細節
└──────────────────────┘
```

## 技術棧

| 層 | 技術 | 說明 |
|----|------|------|
| 前端 | Vue.js + Vite | 五步驟引導式 UI |
| 後端 | Python + FastAPI | API 服務 |
| 模擬引擎 | [OASIS](https://github.com/camel-ai/oasis) (CAMEL-AI) | 開源多 Agent 社會模擬框架，支援百萬級 Agent |
| 知識圖譜 | GraphRAG | 從種子材料提取實體關係 |
| Agent 記憶 | [Zep Cloud](https://app.getzep.com/) | 長期記憶服務，每個 Agent 攜帶人格 + 累積記憶 + 世界狀態 |
| LLM | OpenAI SDK 相容 API | 推薦阿里百煉 qwen-plus |
| 部署 | Docker / 原始碼 | Node.js 18+ / Python 3.11-3.12 |

## 模擬能力：23 種社交動作

Agent 在模擬平台上可執行：follow、comment、repost、like、mute、search 等 23 種社交行為。這些行為不是預設腳本，而是 Agent 根據人設、記憶和當前情境自主決定，形成**由下而上的群體湧現**。

## 應用場景與適用度

| 場景 | 適用度 | 說明 |
|------|--------|------|
| 輿情推演 | ★★★★★ | 資訊流傳播模型貼切，最強項 |
| 危機公關沙盤 | ★★★★ | 壓力測試與方案驗證 |
| 創意推演 | ★★★★ | 小說結局預測、腦洞探索 |
| 金融分析 | ★★★ | 情緒模型有局限，非量化預測 |
| 政策模擬 | ★★★★ | 群體反應推演，但缺乏經濟模型 |

### 實際案例

- **武漢大學輿情推演**：模擬校園事件的輿情擴散路徑與群體反應
- **《紅樓夢》失傳結局**：輸入前 80 回數十萬字，預測後續角色走向
- **Polymarket 交易**：有開發者接入 Polymarket 交易機器人，模擬 2,847 個數位人，338 筆交易獲利 $4,266

## 快速開始

```bash
# 1. 配置環境變數
cp .env.example .env
# 編輯 .env：填入 LLM_API_KEY、ZEP_API_KEY

# 2. 安裝依賴
npm run setup:all

# 3. 啟動（前端 :3000 / 後端 :5001）
npm run dev
```

Docker 部署：

```bash
cp .env.example .env
docker compose up -d
```

## 目前限制 / 注意事項

### 三大根本性問題

1. **AI 幻覺鏈式傳播**：錯誤資訊在 Agent 間逐級放大，產生「誤差雪崩」——一個 Agent 的幻覺輸出成為另一個 Agent 的輸入事實

2. **資訊盲區無法補全**：「你不知道你不知道什麼」——種子材料未涵蓋的變數超出預測範圍，而現實中的黑天鵝事件正是這類未知變數

3. **思維同質化**：所有 Agent 共用同一 LLM 底層，缺乏真實的異質性思維。LLM Agent 比真人更容易出現羊群效應，模擬群體極化速度快於現實

### 其他限制

- **Token 消耗巨大**：每個 Agent 每輪攜帶人格 + 累積記憶 + 世界狀態，隨模擬輪數增長成本急劇上升
- **缺乏基準測試**：團隊尚未公布預測結果與實際結果的對照基準
- **AGPL-3.0 授權**：商業使用需注意開源義務
- **Zep Cloud 依賴**：Agent 記憶依賴第三方雲端服務（雖有免費額度）

## 研究價值與啟示

### 關鍵洞察

1. **「模擬演化」vs「直接預測」是根本性的範式轉換**：傳統 AI 預測是「一個模型吃資料吐結果」，MiroFish 的方法是「建立一個微型社會讓它自己跑」。這不是增量改進，而是從 function approximation 轉向 emergent simulation 的典範轉移。即使預測精度不高，這個思路本身就值得深入研究。

2. **GraphRAG + Agent 記憶是「接地」的關鍵**：MiroFish 最重要的設計決策是用 GraphRAG 將種子材料轉化為結構化知識圖譜，而非直接丟給 Agent 一段文字。這確保了 Agent 的行為錨定在現實實體關係上，防止「幻覺漂移」。這個 pattern 值得在其他多 Agent 系統中借鑑。

3. **「探索工具」定位比「預言機」更誠實也更有價值**：如博客園評論所言，MiroFish 的真正價值不在於「預測萬物」（這是行銷口號），而在於「幫助人類更好地思考萬物」——發現盲點、推演因果鏈、壓力測試決策。把它當決策輔助而非決策替代才是正確用法。

4. **盛大集團入局驗證了「Agent 社會模擬」的商業潛力**：24 小時內 3000 萬人民幣的融資速度，加上 40K stars 的社群熱度，說明市場認為 multi-agent simulation 有真實的商業場景，特別是在輿情管理和公關風險評估領域。

5. **同質化問題是所有 LLM multi-agent 系統的阿基里斯腱**：當所有 Agent 共用同一個 LLM，所謂的「獨立人格」只是 prompt 層面的差異。真正的群體智慧需要認知多樣性，而這恰恰是當前 LLM 架構最難提供的。這個問題不只是 MiroFish 的，而是整個 multi-agent simulation 領域的根本挑戰。

### 與其他專案的關聯

- **vs TradingAgents**：TradingAgents 用多 Agent 做量化交易決策，但走的是「專業分工」路線（分析師、交易員等角色）；MiroFish 走的是「群體湧現」路線（模擬整個市場參與者）。兩者代表了 multi-agent 在預測領域的兩種哲學。
- **vs Project Golem**：Golem 的「金字塔記憶」和 MiroFish 的 Zep 記憶系統都在解決 Agent 長期記憶問題，但目標不同——Golem 服務單一 Agent 的持續對話，MiroFish 服務數千 Agent 的平行演化。
- **vs CrewAI / LangChain**：這些是通用 Agent 框架，MiroFish 則是專門化的模擬引擎。MiroFish 底層用了 OASIS（CAMEL-AI 的框架），但上層的知識圖譜 → 人設生成 → 社會模擬 → 報告產出的完整 pipeline 是它的核心差異化。
