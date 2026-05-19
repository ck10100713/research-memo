---
date: "2026-05-19"
category: "量化交易"
card_icon: "material-finance"
oneliner: "ZhuLinsen 用 GitHub Actions 跑零成本 A/H/美股 LLM 智能分析，37k stars、多 LLM + 多新聞源 + 多通知頻道、15 內建策略 + Agent 問股，工作日 18:00 自動推「決策仪表盘」"
---

# Daily Stock Analysis 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/ZhuLinsen/daily_stock_analysis> |
| 同系列姊妹專案 | <https://github.com/ZhuLinsen/alphasift>（多因子選股）、AlphaForge（策略進化） |
| Docker Hub | `zhulinsen/daily_stock_analysis` |
| Trendshift | <https://trendshift.io/repositories/18527> |
| HelloGitHub 精選 | rid=6daa16e405ce46ed97b4a57706aeb29f |
| 規模 | 37,207 stars / MIT / Python 3.10+ / 創建 2026-01-10（**4 個月衝到 37k stars**） |
| Topics | a-stock、ai-agent、llm、quant、quantitative-finance、quantitative-trading |

## 概述

**Daily Stock Analysis (DSA)** 是中國開發者 ZhuLinsen 推出的 **LLM 驅動 A/H/美股智能分析系統**，slogan：

> *「LLM 驱动的 A/H/美股智能分析：多数据源行情 + 实时新闻 + LLM 决策仪表盘 + 多渠道推送，**零成本定时运行，纯白嫖**」*

最核心的設計：**用 GitHub Actions 當 cron job runner，跑零成本量化分析**，每個工作日 18:00（北京時間）自動分析自選股 → 用 LLM 產生決策仪表盘 → 推到企業微信 / 飛書 / Telegram / Discord / Slack / 信箱。**不需要伺服器**，5 分鐘可上線。

整套系統解決的痛點：**散戶想要每天有 AI 分析報告，但不想自己跑伺服器 + 不想付 SaaS 訂閱費**。DSA 用 GitHub Actions 免費額度 + 多家有免費額度的 LLM provider，把這條 pipeline 變成「fork → 設 secrets → 啟用 Actions」三步驟。

## 功能矩陣

| 能力 | 內容 |
|------|------|
| 🎯 **AI 決策報告** | 核心結論、評分、趨勢、買賣點位、風險警報、催化因素、操作檢查清單 |
| 📊 **多市場數據** | A股、港股、美股、ETF；行情、K 線、技術指標、資金流、籌碼、新聞、公告、基本面 |
| 🖥️ **Web / 桌面工作台** | 手動分析、任務進度、歷史報告、Markdown 報告、回測、持倉、配置管理 |
| 🤖 **Agent 策略問股** | 多輪追問 + **15 種內建策略**（均線、纏論、波浪、趨勢、熱點、事件、成長、預期等） |
| 📥 **智能導入與補全** | 圖片 / CSV / Excel / 剪貼簿導入；股票代碼 / 名稱 / 拼音 / 別名補全 |
| 🚀 **自動化與推送** | GitHub Actions / Docker / 本地 cron / FastAPI + 6 通知頻道 |

## 技術選型

| 類別 | 支援 |
|------|------|
| **LLM** | Anspire（中國一站式）、AIHubMix、Gemini、OpenAI compat、DeepSeek、通義千問、Claude、Ollama |
| **行情** | TickFlow、AkShare、Tushare、Pytdx、Baostock、YFinance、Longbridge |
| **新聞搜索** | Anspire AI Search、SerpAPI、Tavily、Bocha、Brave、MiniMax、SearXNG |
| **社交輿情** | Adanos Stock Sentiment API（Reddit / X / Polymarket，美股 only） |
| **通知** | 企業微信、飛書、Telegram、Discord、Slack、Email |
| **部署** | GitHub Actions（推薦）、Docker、本地 cron、FastAPI server、Web UI |

→ **設計重點是「provider 多到一定有免費的能用」**——不依賴單一付費 API、不需要科學上網。

## GitHub Actions 零成本部署的關鍵

```yaml
# 大致流程（從 README 推敲）
1. Fork repo
2. Settings → Secrets → New secret
   - 至少配 1 個 LLM（推薦 Anspire 或 AIHubMix，免費額度足）
   - 至少配 1 個通知頻道
   - STOCK_LIST（自選股代碼，如 "600519,hk00700,AAPL,TSLA"）
   - 至少配 1 個新聞源（強烈推薦）
3. Actions → Enable
4. 手動觸發測試
5. 預設工作日 18:00 北京時間自動跑
```

**節假日邏輯內建**：預設非交易日（A/H/US 各自節假日）不執行；交易日檢查、強制執行、斷點續傳都有對應 flag。

## 決策仪表盘範例（README 直接抄）

```text
🎯 2026-02-08 决策仪表盘
共分析3只股票 | 🟢买入:0 🟡观望:2 🔴卖出:1

📊 分析結果摘要
⚪ 中钨高新(000657): 观望 | 评分 65 | 看多
⚪ 永鼎股份(600105): 观望 | 评分 48 | 震荡
🟡 新莱应材(300260): 卖出 | 评分 35 | 看空

⚪ 中钨高新 (000657)
📰 重要信息速览
💭 舆情情绪: 市场关注其 AI 属性与业绩高增长...
📊 业绩预期: 2025 年前三季度业绩同比大幅增长...

🚨 风险警报：
风险点 1：2 月 5 日主力资金大幅净卖出 3.63 亿元...
风险点 2：筹码集中度高达 35.15%...
风险点 3：历史违规记录及重组相关风险...

✨ 利好催化：
利好 1：AI 服务器 HDI 核心供应商...
利好 2：扣非净利润同比暴涨 407.52%...

📢 最新动态: ...
```

→ 報告結構**設計成手機可讀的「卡片化」格式**（標題 emoji + 短段落 + bullet），不是把 LLM 原始輸出貼出來。

## 三件套姊妹專案

| 專案 | 定位 |
|------|------|
| **daily_stock_analysis（本研究）** | **日常分析** — 每日自動產報告 |
| [AlphaSift](https://github.com/ZhuLinsen/alphasift) | **選股** — 多因子全市場掃描 |
| AlphaForge（README 提到） | **策略進化** — 策略驗證與優化 |

→ 作者明確說「當前獨立維護，**後續會優先探索與 DSA 的候選股導入、回測驗證、報告聯動**」——三件套未來會打通。

## Agent 策略問股（15 內建策略）

Web `/chat` 介面支援多輪問股，內建策略：

```text
均線金叉、纏論、波浪理論、多頭趨勢、熱點題材、事件驅動、
成長質量、預期重估、…（共 15 種）
```

每個策略本質是 **system prompt + tool 組合**——LLM 在 strategy frame 下做分析，呼叫實時行情 / K 線 / 技術指標 / 新聞 / 風險工具。

支援功能：
- 多輪追問
- 會話導出
- 發送到通知頻道
- 後台執行
- 自訂策略檔案
- 多 Agent 編排（實驗性）

## 目前限制與注意事項

- **「LLM 分析」不是「LLM 決策」**：報告產出評分 / 觀望 / 買賣建議，**但這是基於新聞 + 指標的綜合 LLM 判斷，不是 backtest 過的策略訊號**。實盤跟單風險高。
- **資料源品質參差**：AkShare / Tushare / Baostock 對 A 股強，**台股不支援**；YFinance 對美股 OK 但延遲較大。
- **新聞源是關鍵變數**：README 自陳「新聞源會顯著影響輿情、公告、事件和催化因素質量」——免費 tier 配額有限，**production 用得買額度**。
- **強相依「中國新聞源 + 中國 LLM」**：Anspire / AIHubMix / 博查 / 通義千問是中國服務，**台灣使用者需要評估資料合規性**；Gemini / OpenAI / Claude 路線完全可行，但要科學上網或 AIHubMix 中轉。
- **GitHub Actions 公開倉庫每月 2000 分鐘額度**：超過會被收費；Fork 後務必確認**不要把 secrets 設成 public**。
- **零成本是免費 tier 撐起來的脆弱平衡**：免費 LLM 額度、免費 GitHub Actions、免費新聞源——**任一收緊就會破功**。
- **「贊助商」是 Anspire / SerpAPI**：README 顯著推薦這兩個服務，使用前要意識到**這是商業合作而非中立技術選擇**。
- **無 Agent 風控**：報告產生後直接推給使用者，**沒有「風險過高拒絕推送」的 guardrail**——可能在極端市況推出誤導性建議。

## 研究價值與啟示

### 關鍵洞察

1. **「GitHub Actions 當零成本 cron runner」是被低估的部署模式**：對個人量化 / 小型 SaaS，**Actions 免費額度（公開倉庫每月 2000 分鐘）足以跑大部分日頻 / 週頻任務**。免費、無 server 維護、有完整 secret 管理 + 日誌——是 retail quant 開發最佳的 starter platform。值得**完全抄這個 deploy 路線**到你的策略 backtest / 訊號通知系統。
2. **「決策仪表盘」這個資訊架構值得學**：把 LLM 原始輸出 **強制套進固定模板**（核心結論 + 評分 + 趨勢 + 買賣點位 + 風險警報 + 利好催化 + 操作清單）——對使用者可讀、對 LLM 易產出、對下游可解析。比起讓 LLM 自由發揮，**模板化輸出是 production-grade LLM 應用的關鍵紀律**。
3. **多 provider 策略是抗風險核心**：8+ LLM、7+ 行情、7+ 新聞源、6 通知頻道——**沒有單點故障**。對個人用戶降低 vendor lock-in、對極端時刻（某家 API 掛掉）有兜底。**這個架構應該是任何 production LLM 應用的預設姿勢**。
4. **「白嫖」哲學的開源策略**：作者直接在 description 寫「**纯白嫖**」——這個定位在中國開源圈是強有力的 positioning。對台灣 retail 同樣適用——多數人不會付 ChatGPT Plus 訂閱、不會租伺服器，但會願意 fork 一個免費跑的 repo。
5. **15 種策略 = 15 個 system prompt**：呼應 [[fincept-terminal]] 的 37 AI agents（Buffett / Graham / Lynch），**「投資策略 = 角色 prompt + tool 組合」已是 retail quant 的標配 UI pattern**。差異是 Fincept 用大師人物、DSA 用技術指標流派。
6. **三件套姊妹專案揭示完整 retail quant agent stack**：選股（AlphaSift）→ 日常分析（DSA）→ 策略進化（AlphaForge）。對台灣有志做類似系統的人，這是個值得抄的完整切分。
7. **CJK 報告 + 卡片化排版**：報告大量 emoji + 短段落 + 標題鮮明——是適合手機推播閱讀的設計，**比英文長文更貼合通訊軟體場景**。
8. **GitHub Actions 上跑 LLM 還有個 hidden benefit**：每次運行的 log 全部留在 Actions tab，**自帶 trace + debug**——這是「免費 observability」。

### 與其他研究的關聯

- 與 [[fincept-terminal]]：兩者都是 retail quant + 多 LLM provider + AI agents，但**部署模型完全不同**——Fincept 是 native desktop app（C++ + Qt6），DSA 是 GitHub Actions 排程任務。**「桌面 app vs 雲端 cron」是 retail quant 的兩個主要部署路線**。
- 與 [[ai-hedge-fund]]、[[tradingagents]]、[[ai-trader]]：四者都是 LLM agents 做交易分析，DSA 是**唯一全 production-ready 的「每日自動推 → 使用者讀」消費端產品**；其他三者更偏 framework / research。
- 與 [[openstock]]、[[stockstats]]、[[tejapi_python_medium_quant]]：純資料層 vs 整合產品層的對照。DSA 是後者最完整的例子。
- 與 [[openhuman]]：兩者都是「定時 fetch + LLM 分析 + 通知」架構——OpenHuman 是個人生活版（Gmail / Notion / Calendar），DSA 是金融版（行情 / 新聞 / 自選股）。**核心架構幾乎一致**，差異只在 data domain。
- 與 [[cli-anything]]、[[rag-anything]]：DSA 沒用 MCP / CLI 抽象層，**直接寫死 provider 整合**。對應的設計取捨：DSA 為了 simplicity、CLI-Anything 為了 generality。
- 對台灣 retail quant 的應用：**直接 fork DSA，把 AkShare / Tushare 換成 yfinance/TWSE + 永豐 API 即可變成「台股 DSA」**。所有「LLM + 新聞 + 通知頻道」邏輯都能保留。
- 與 [[zeuikli-claude-code-best-practices]] 第 8 章 Routines：DSA 的 GitHub Actions cron 本質就是 routine——對比 Anthropic 自家 Routines（Pro 5 次 / Max 15 次 / Team 25 次 / 日），**GitHub Actions 每月 2000 分鐘**是更慷慨的免費資源。
