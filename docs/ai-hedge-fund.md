# AI Hedge Fund 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) |
| 作者 Twitter | [@virattt](https://x.com/virattt/status/1870513142981353703) |
| DeepWiki 架構分析 | [deepwiki.com/virattt/ai-hedge-fund](https://deepwiki.com/virattt/ai-hedge-fund/1-overview) |
| Decision Crafters 評測 | [The Revolutionary Multi-Agent Trading System](https://www.decisioncrafters.com/ai-hedge-fund-the-revolutionary-multi-agent-trading-system-thats-transforming-financial-ai-with-43k-github-stars/) |
| The Dispatch Report | [Repo Analysis](https://thedispatch.ai/reports/6517/) |
| Ethan Mollick 試玩紀錄 | [LinkedIn](https://www.linkedin.com/posts/emollick_this-is-neat-im-playing-with-virat-singhs-activity-7283565091642343425-p5-U) |

## 專案概述

**AI Hedge Fund** 是 Virat Singh 開發的教育性概念驗證專案，模擬一個由多個 AI Agent 組成的虛擬對沖基金。系統讓 12 位傳奇投資人的 AI 分身從各自的投資哲學角度分析同一支股票，再由 Portfolio Manager Agent 整合意見做出最終倉位決策。

截至 2026-03-29，該專案擁有 **49,685 stars、8,632 forks**，是 GitHub 最受關注的 AI 交易相關開源專案之一。作者明確聲明這是 **純教育用途**，系統不會執行真實交易。

這個專案最大的價值不在於真正盈利，而在於它示範了「如何讓多個具有不同思維框架的 Agent 協同決策」——這個模式可以套用到任何需要多視角分析的領域。

## 核心功能

### 18 個 Agent 組成的決策鏈

```
[傳奇投資人 AI × 12]          [分析師 Agent × 4]
  Aswath Damodaran               Valuation Agent
  Ben Graham                     Sentiment Agent
  Bill Ackman                    Fundamentals Agent
  Cathie Wood                    Technicals Agent
  Charlie Munger                      │
  Michael Burry                       │
  Mohnish Pabrai      ──────►  Risk Manager
  Peter Lynch                         │
  Phil Fisher                         ▼
  Rakesh Jhunjhunwala        Portfolio Manager
  Stanley Druckenmiller       (最終交易決策)
  Warren Buffett
```

### 各角色設計哲學

| Agent | 投資哲學關鍵詞 |
|-------|-------------|
| Ben Graham | 安全邊際、隱藏寶石 |
| Cathie Wood | 顛覆式創新、成長股 |
| Charlie Munger | 優秀企業、合理價格 |
| Michael Burry | 逆向思考、深度價值 |
| Stanley Druckenmiller | 宏觀趨勢、不對稱機會 |
| Warren Buffett | 長期持有、護城河 |
| Valuation Agent | 計算內在價值、生成交易訊號 |
| Risk Manager | 計算風險指標、設定部位上限 |
| Portfolio Manager | 整合所有信號、生成最終訂單 |

## 技術架構

```
src/
├── agents/       # 18 個 Agent 的定義與 prompt
├── graph/        # LangGraph 工作流（Agent 協調層）
├── data/         # 市場資料抓取層
├── tools/        # Agent 可呼叫的工具集
├── llm/          # LLM 設定（支援多家 provider）
├── backtesting/  # 回測引擎
├── cli/          # 命令列介面
└── main.py       # 入口
```

**LLM 支援：**

| Provider | 環境變數 |
|----------|---------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Groq | `GROQ_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Ollama（本地） | `--ollama` flag |

**免費資料股票：** AAPL、GOOGL、MSFT、NVDA、TSLA（其他需要 `FINANCIAL_DATASETS_API_KEY`）

## 快速開始

```bash
# 安裝
git clone https://github.com/virattt/ai-hedge-fund.git && cd ai-hedge-fund
cp .env.example .env   # 填入 API keys

poetry install

# 執行分析
poetry run python src/main.py --ticker AAPL,MSFT,NVDA

# 使用本地 LLM（Ollama）
poetry run python src/main.py --ticker AAPL --ollama

# 指定時間區間
poetry run python src/main.py --ticker NVDA --start-date 2024-01-01 --end-date 2024-06-01

# 執行回測
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

也提供 Web Application（詳見 `app/` 目錄），有視覺化介面。

## 目前限制 / 注意事項

| 限制 | 說明 |
|------|------|
| 純教育用途 | 不可用於真實交易，無法執行實際訂單 |
| 歷史資料依賴 | 回測結果不代表未來表現 |
| 未考慮流動性 | 沒有市場衝擊、滑價、成交量限制 |
| LLM 幻覺風險 | Agent 的「分析」受 LLM 能力上限約束 |
| API 費用 | 18 個 Agent 同時呼叫 LLM，單次分析費用可觀 |
| 無即時資料 | 依賴 Financial Datasets API，非 tick-level 資料 |

## 研究價值與啟示

### 關鍵洞察

**1. 「投資哲學」是優秀的 prompt engineering 框架**
把 Warren Buffett 或 Michael Burry 的投資書籍摘要塞進 system prompt，比寫抽象的「請分析這支股票」效果好得多——有具體的心智模型做錨點，LLM 輸出的品質和一致性明顯提升。這個技巧可以套用到任何專業角色扮演場景。

**2. 多 Agent 辯論比單一 Agent 更抗偏見**
讓 Cathie Wood（成長）和 Ben Graham（價值）同時分析同一支股票，結果往往比單一視角更均衡。這印證了 multi-agent debate 的價值——不是為了「正確」，而是為了「覆蓋更多視角」。

**3. LangGraph 的 graph 結構是關鍵**
`src/graph/` 顯示這個系統用 LangGraph 而非簡單的序列呼叫。這讓 Agent 可以有條件路由、並行執行、以及有狀態的記憶傳遞——這是可以直接借鑑到 fluffy-agent-core 的架構模式。

**4. 免費資料的邊界設計很聰明**
只讓 5 支大型股票免費，其餘需要付費 API key，這降低了入門門檻又保護了資料服務商的商業利益——是一個值得學習的開源商業模式設計。

**5. 49K stars 背後的傳播機制**
這個專案的核心吸引力不是「能賺錢」，而是「有名字的 AI」——看到「Warren Buffett AI 分析了你的股票」比看到「AI 分析了你的股票」更有分享動機。**可識別的角色設定**是 AI 產品病毒傳播的有效策略。

### 與其他專案的關聯

- **TradingAgents**（本站已有筆記）：同為多 Agent 交易系統，TradingAgents 更學術（來自 Tauric Research），ai-hedge-fund 更工程導向且有 Web UI
- **AutoHedge**（The-Swarm-Corporation）：更進一步支援 Solana 真實交易執行，是「下一步」的參考
- **Claude Financial Services Plugins**（本站已有筆記）：Anthropic 官方的金融 Agent 工具集，與本專案的 Agent 設計可以互相補充
