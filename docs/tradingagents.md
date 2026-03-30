---
date: "2024-12-28"
category: "量化交易"
icon: "material-chart-line"
oneliner: "多 Agent 協作的量化交易決策系統"
---
# TradingAgents 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) |
| arXiv 論文 | [2412.20138](https://arxiv.org/abs/2412.20138) |
| 論文 HTML 版 | [arxiv.org/html/2412.20138v5](https://arxiv.org/html/2412.20138v5) |
| Tauric Research 官網 | [tauric.ai](https://tauric.ai/) |
| Trading-R1 報告 | [2509.11420](https://arxiv.org/abs/2509.11420) |
| Discord 社群 | [TradingResearch](https://discord.com/invite/hk9PGKShPK) |

| 項目 | 數值 |
|------|------|
| Stars | 42.5K |
| Forks | 7.8K |
| Language | Python |
| License | Apache-2.0 |
| 建立日期 | 2024-12-28 |
| 最新版本 | v0.2.2（2026-03） |

## 專案概述

TradingAgents 是由 Tauric Research 開源的**多代理 LLM 金融交易框架**，模擬真實交易公司的組織架構——基本面分析師、情緒分析師、技術分析師、交易員、風控團隊各司其職，透過結構化辯論協作產出交易決策。

專案基於 **LangGraph** 建構，支援多家 LLM 供應商（OpenAI、Google、Anthropic、xAI、OpenRouter、Ollama），從 2024 年底發布以來快速成長至 42.5K stars，是目前 LLM + 量化交易領域 star 數最高的開源專案之一。

!!! warning "研究用途聲明"
    此框架僅供研究用途，不構成金融、投資或交易建議。交易績效受 backbone LLM、模型溫度、交易期間、資料品質等多重因素影響。

## 核心架構

```
┌─────────────────────────────────────────────────────────────────┐
│                        資料來源層                                │
│   yfinance (股價)  ·  Alpha Vantage (基本面/新聞)  ·  Local DB  │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        分析師團隊                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 基本面   │ │ 情緒     │ │ 新聞     │ │ 技術     │           │
│  │ Analyst  │ │ Analyst  │ │ Analyst  │ │ Analyst  │           │
│  │──────────│ │──────────│ │──────────│ │──────────│           │
│  │ 財報估值 │ │ 社群評分 │ │ 總經事件 │ │ MACD/RSI │           │
│  │ 紅旗偵測 │ │ 市場氛圍 │ │ 影響評估 │ │ 圖形辨識 │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        研究員團隊                                │
│          ┌──────────────┐  ←── 辯論 ──→  ┌──────────────┐      │
│          │ Bull 研究員  │               │ Bear 研究員  │      │
│          │ 評估潛在收益 │               │ 評估潛在風險 │      │
│          └──────────────┘               └──────────────┘      │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  交易員 Agent → 風險管理團隊 → 投資組合經理（批准/拒絕）→ 執行  │
└─────────────────────────────────────────────────────────────────┘
```

### 各層角色職責

| 層級 | 角色 | 職責 |
|------|------|------|
| 分析 | Fundamentals Analyst | 評估公司財報、估值、紅旗偵測 |
| 分析 | Sentiment Analyst | 社群情緒評分、短期市場情緒 |
| 分析 | News Analyst | 全球新聞、總經指標、事件影響 |
| 分析 | Technical Analyst | MACD、RSI 等技術指標與價格預測 |
| 研究 | Bull/Bear Researchers | 透過結構化辯論平衡收益與風險 |
| 執行 | Trader Agent | 綜合報告決定交易時機與規模 |
| 風控 | Risk Management Team | 評估波動性、流動性、調整策略 |
| 決策 | Portfolio Manager | 最終批准/拒絕交易提案 |

## 論文實驗結果

回測期間：**2024-01-01 ~ 2024-03-29**，標的：AAPL、GOOGL、AMZN

### 績效數據

| 指標 | AAPL | GOOGL | AMZN |
|------|------|-------|------|
| 累積報酬率 | 26.62% | 24.36% | 23.21% |
| 年化報酬率 | 30.5% | 27.58% | 24.90% |
| Sharpe Ratio | 8.21 | 6.39 | 5.60 |
| 最大回撤 | 0.91% | 1.69% | 2.11% |

### 對照基線

| 基線策略 | 說明 |
|---------|------|
| Buy & Hold | 買入持有 |
| MACD | 移動平均收斂發散 |
| KDJ & RSI | 技術指標策略 |
| ZMR | 零均值回歸 |
| SMA | 簡單移動平均 |

TradingAgents 在所有標的上均顯著優於上述基線，改善幅度 6.1%~28.43%。在 AAPL 的高波動期間，傳統方法表現不佳，但 TradingAgents 仍維持穩定獲利。

!!! note "Sharpe Ratio 說明"
    作者坦承 Sharpe Ratio 異常偏高（最高 8.21），歸因於回測期間回撤極少。且因 LLM 呼叫成本高，僅測試 3 個月，長期穩定性仍待驗證。

## 快速開始

### 安裝

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

conda create -n tradingagents python=3.13
conda activate tradingagents

pip install .
```

### API 金鑰設定

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage (金融數據)
```

也支援 Ollama 本地模型（設定 `llm_provider: "ollama"`）。

### CLI 使用

```bash
tradingagents          # 安裝後的指令
python -m cli.main     # 從原始碼執行
```

### Python API

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"       # 選擇 LLM 供應商
config["deep_think_llm"] = "claude-opus-4-6"  # 複雜推理用
config["quick_think_llm"] = "claude-haiku-4-5-20251001"  # 快速任務用
config["max_debate_rounds"] = 2            # 辯論輪數

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

### 支援的 LLM 供應商

| 供應商 | 模型範例 | 設定值 |
|--------|---------|--------|
| OpenAI | GPT-5.2, GPT-5-mini | `"openai"` |
| Google | Gemini 3.1 | `"google"` |
| Anthropic | Claude Opus 4.6, Haiku 4.5 | `"anthropic"` |
| xAI | Grok 4.x | `"xai"` |
| OpenRouter | 各家模型 | `"openrouter"` |
| Ollama | 本地模型 | `"ollama"` |

## 版本演進

| 版本 | 日期 | 重點更新 |
|------|------|---------|
| v0.2.2 | 2026-03 | GPT-5.4/Gemini 3.1/Claude 4.6 支援、五級評分量表、OpenAI Responses API、Anthropic effort control |
| v0.2.0 | 2026-02 | 多 LLM 供應商架構（OpenAI/Google/Anthropic/xAI）、系統架構改進 |
| v0.1.x | 2025 | 初始開源版本、LangGraph 架構、CLI 介面 |

**Trading-R1**：Tauric Research 於 2026-01 發布的新研究方向（[arXiv:2509.11420](https://arxiv.org/abs/2509.11420)），Terminal 工具預計近期釋出。

## 目前限制 / 注意事項

| 限制 | 說明 |
|------|------|
| **LLM 成本高** | 每次分析需多個 Agent 各呼叫 LLM，API 費用可觀 |
| **回測期短** | 論文僅測試 3 個月（受 LLM 成本限制），長期穩定性未知 |
| **Sharpe Ratio 偏高** | 作者自認數值超出合理經驗範圍，牛市期間回撤少所致 |
| **僅限規則基線比較** | 未與 ML-based 量化策略（如 RL agent）對比 |
| **非即時交易** | 回測框架，非生產級交易系統 |
| **資料依賴外部 API** | Alpha Vantage 免費版有呼叫限制 |
| **非確定性** | LLM 輸出隨溫度和版本變動，可重現性有限 |

## 研究價值與啟示

### 關鍵洞察

1. **「交易公司」隱喻的威力**：TradingAgents 成功之處不在演算法創新，而在**組織設計的忠實還原**。它把一家真實交易公司的部門架構（分析師 → 研究員 → 交易員 → 風控 → PM）直接映射為 Agent 拓撲，讓每個 Agent 的 prompt 和工具集自然受限於角色職責。這個「用組織模擬限制 Agent 行為」的模式，比單純的 prompt engineering 更具結構性。

2. **辯論機制是多 Agent 系統的殺手特性**：Bull/Bear 研究員的結構化辯論不只是噱頭——它強制系統產出對立觀點，避免單一 LLM 的確認偏誤（confirmation bias）。42.5K stars 的爆發性成長，很大程度源於這個直觀且可解釋的決策機制。

3. **誠實的侷限揭露反而增加可信度**：論文坦承 Sharpe Ratio 超出合理範圍、回測期短、成本限制等問題，這在量化金融 + AI 的炒作中非常少見。誠實揭露侷限 ≠ 軟弱，反而讓研究社群更願意投入改進。

4. **多 LLM 供應商支援是必要的生存策略**：v0.2.0 從 OpenAI-only 擴展到六家供應商，這不只是功能擴充，而是**降低對單一 API 的依賴風險**。在 LLM 價格戰持續的市場中，能隨時切換供應商 = 成本最佳化的能力。

5. **從 42.5K stars 看「金融 + AI Agent」的市場需求**：這個 2024 年底才建立的專案，15 個月內衝到 42.5K stars / 7.8K forks，反映了一個巨大的未被滿足需求——量化交易者想要「開箱即用」的 LLM Agent 框架，而非從零建構。

### 與其他專案的關聯

- **CrewAI / LangChain**：TradingAgents 建構於 LangGraph 之上，本質上是 LangChain 生態在金融垂直領域的最佳實踐範例。CrewAI 的角色定義模式與 TradingAgents 的 Agent 設計高度相似，但後者更專精於金融場景
- **多 Agent 辯論會**：TradingAgents 的 Bull/Bear 辯論機制與我們研究的多 Agent 辯論會架構不謀而合——兩者都驗證了「結構化辯論能提升 LLM 決策品質」的假設
- **MiroFish**：同為高 star 數的 AI Agent 預測系統，但 MiroFish 用群體智能、TradingAgents 用專家分工，代表兩種截然不同的多 Agent 決策哲學
- **OpenStock / StockStats**：可作為 TradingAgents 的資料來源補充，或與其技術分析模組做功能比較
