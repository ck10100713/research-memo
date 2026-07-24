---
date: "2026-07-24"
category: "量化交易"
card_icon: "material-robot-happy"
oneliner: "HKUDS 的『個人交易 Agent』——pip 一行裝起，自然語言驅動 88 skill / 462 alpha / 8 回測引擎，安全設計靠結構性 paper/live 護欄而非 config flag"
tags:
  - quant
  - multi-agent
  - mcp
---

# Vibe-Trading（HKUDS）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★27,073 / 4,399 forks / MIT / Python 3.11+） | [github.com/HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) |
| 官網 / 文件 | [vibetrading.wiki](https://vibetrading.wiki/) · [Docs](https://vibetrading.wiki/docs/) |
| PyPI 套件 | [pypi.org/project/vibe-trading-ai](https://pypi.org/project/vibe-trading-ai/) |
| SECURITY.md（外部資安稽核、冒名警告） | [SECURITY.md](https://github.com/HKUDS/Vibe-Trading/blob/main/SECURITY.md) |
| HKUDS 實驗室（LightRAG / RAG-Anything / AI-Trader 同源） | [github.com/HKUDS](https://github.com/HKUDS) |
| 第三方索引 | [OpenSource-Hub](https://www.opensource-hub.com/en/library/hkuds-vibe-trading) |

## 專案概述

Vibe-Trading 是香港大學資料智能實驗室 **HKUDS**（LightRAG、[GraphRAG](graphrag.md)、[RAG-Anything](rag-anything.md)、[AI-Trader](ai-trader.md) 的同一實驗室）在 **2026-04 才建立**、四個月內衝到 **27k stars** 的開源專案。定位一句話：**「你的個人交易 Agent」**——把自然語言的金融問題轉成可執行的分析。

技術棧是 **FastAPI 後端 + React 19 前端 + ReAct agent core**，`pip install vibe-trading-ai` 一行裝起，同時提供 CLI（互動 TUI）、REST API、MCP server（54 tools）、Web UI 四個入口。核心迴圈是標準 ReAct，但外掛了一整套金融領域的 skill / tool / 回測 / 資料層。

**定位釐清**：它**不持有資金、預設不下真單**。主力場景是**研究、模擬、回測**；真實交易是選配——透過你自己授權的券商（如 Robinhood Agentic Trading），且被你設的限額框死、可即時停止。

> 本站已有多個「AI Agent 做交易」的筆記（[TradingAgents](tradingagents.md)、[AI Hedge Fund](ai-hedge-fund.md)、[AI-Trader](ai-trader.md)）。Vibe-Trading 的差異在於**它不是一套固定策略，而是一個「金融能力齊全的 agent 工作台」**——資料、回測、因子庫、swarm、記憶、skill 全部可組合。

## 四大特色

| 特色 | 內容 |
|------|------|
| 🔍 **Self-Improving Trading Agent** | 自然語言市場研究、策略草稿、檔案/網頁分析、記憶回填的可重用 workflow；useful routine 可存成 editable skill |
| 🐝 **Multi-Agent Trading Teams** | investment / quant / crypto / risk 團隊；**30 個 swarm preset**（如 `investment_committee`：多空辯論→風控→PM 拍板）；worker 都用抓來的真實市場資料 grounding |
| 📊 **Cross-Market Data & Backtesting** | A股/港股/美股/加密/期貨/外匯；資料 fallback + 複合回測；**PIT 資料 + 驗證 + run cards** |
| 👥 **Shadow Account** | **本專案最獨特的功能**——從你自己的券商交割單出發，不是通用策略模板 |

### Shadow Account——行為診斷才是差異化

多數 AI 交易專案是「給你一套策略」；Shadow Account 反過來——**診斷你自己的交易行為**：

```
1. 讀交割單   解析 同花顺/東方財富/富途/通用 CSV
2. 剖析行為   持有天數、勝率、盈虧比、回撤，並檢測
              disposition effect（處置效應）、overtrading、追高、錨定
3. 抽取規則   把反覆出現的進出場變成「明確策略 profile」而非模糊總結
4. 跑影子帳戶 回測抽出的規則，標出你的 rule break、太早出場、錯過訊號、反事實交易路徑
5. 產出報告   8 段式 HTML/PDF——「你到底把多少錢留在桌上」
```

> 這把「行為金融學」直接產品化：不是預測市場，而是**量化你和你自己紀律之間的差距**。

## 技術盤點（實測 main 分支數字）

| 面向 | 規模 |
|------|------|
| Finance skill 庫 | **88 skills / 9 類**（Data Source 10、Strategy 19、Analysis 22、Asset Class 9、Crypto 7、Flow 8、Tool 10、Research 2、Risk 1），每個一份 `SKILL.md`，可 CRUD 自建 |
| Agent tools | **68 個**自動探索工具（backtest、cross-session memory、skill CRUD、FTS5 session 搜尋、swarm、web search、bash、factor analysis…） |
| Alpha Zoo | **462 個因子 / 5 家族**：qlib158(154) + alpha101(101) + gtja191(191) + academic(12) + fundamental(4)；一行 `alpha bench` 出 IC + alive/reversed/dead 分類 |
| 回測引擎 | **8 個**（ChinaA T+1、GlobalEquity T+0、IndiaEquity、Crypto 現貨/永續、China/Global Futures、Forex、options_portfolio）+ Composite 跨市場共用資金池 |
| 資料源 | **22–23 個**免費源 + 選配 QVeris premium；`source:"auto"` 依「**IP 封鎖風險**」排 fallback chain（永不封的公開源優先、限流/需金鑰的墊後） |
| 券商連接器 | **12 家**（IBKR、Robinhood、Tiger、Alpaca、OKX、Binance、Futu、MT5、Longbridge、Dhan、Shoonya、Trading212） |
| IM channel | **16 個** adapter（Telegram/Slack/Discord/WhatsApp/Signal/QQ/微信/飛書/Teams/email…）跑同一 session runtime |
| 驗證工具 | 15 metrics + benchmark、5 portfolio optimizer、3 驗證（Monte Carlo / Bootstrap / Walk-Forward） |

## 安全設計（最值得學的部分）

一個「會下真單、接你券商」的開源 agent，最大風險就是安全。Vibe-Trading 的做法異常紮實：

- **結構性 paper/live 護欄，不是 config flag**：paper vs live 靠「帳號 ID 格式 / host 分離 / demo 旗標 / 交易環境」等**執行期結構**判定，agent **無法用設定翻轉**。券商若沒有這種判別器 → 直接封頂在 paper + 唯讀（如 Trading212 連 paper 下單都 hard-refuse）。
- **Mandate gate（授權閘）**：真單被 symbol allowlist、單量/曝險上限、每日交易次數上限、即時 kill switch 框死；**永不持有資金**（券商執行）。
- **下單工具不上 MCP**（只在 agent + CLI）；**research/backtest 路徑在結構上被禁止觸及任何 live endpoint**。
- **AST 強化的回測沙箱**：擋掉 network / subprocess / eval / `os.environ` / 不安全 open（連巢狀函式內都擋）。
- **通過外部資安稽核**：2026-07-10 外部稽核的 **10 項發現全部關閉**（Docker digest-pin、SSE 短期單次票券、read-only rootfs、hash-locked 依賴…）。
- **TAP mode（選配）**：接 [Tool Authorization Protocol](https://tap.human.tech) 憑證代理——agent 進程**完全不持有券商金鑰**（用 `<CREDENTIAL:alpaca.key_id>` 佔位、TAP 伺服器端注入）；**寫入操作卡在人類核准**，連被 prompt injection 的「立即買進」都會被攔住。誠實列出「approval race」已知限制。
- **CI grep gate**：`tools/ci_grep_gates.sh` 直接拒收 `yaml.load` / 商標 / 逐股資料外洩。
- **反冒名聲明**：README 頂端就警告有假 X 帳號 / 假 token 冒用其名——「我們從未發行任何 token 或 memecoin」。

## 快速開始

```bash
pip install vibe-trading-ai

# 自然語言研究
vibe-trading run -p "Backtest a BTC-USDT 20/50 moving-average strategy for 2024, \
  summarize return and drawdown, then export the report"

# 一行 bench 整個 alpha zoo
vibe-trading alpha bench --zoo gtja191 --universe csi300 --period 2018-2025 --top 20

# Shadow Account：診斷你自己的交易
vibe-trading --upload trades_export.csv
vibe-trading run -p "Analyze my trading behavior, extract my shadow strategy, \
  and compare it with my actual trades"
```

其餘部署路徑：Docker（零設定）、本地安裝、MCP plugin、ClawHub 一鍵。

## 目前限制 / 注意事項

- **研究/模擬導向**：真實交易能力受限——12 家券商中多數只到 read + paper，bounded-live 僅少數支援；loader 只給 point-in-time 歷史 K 線，**即時 tick / 掛單簿深度不在範圍**。
- **極高活躍度＝高變動**：v0.x（現 v0.1.12），News 顯示幾乎每天數十個 PR、大量 reliability sweep——API/行為仍在快速變。引用版本務必對照 CHANGELOG。
- **27k stars 的名氣招來冒名詐騙**：已有假 token / 假 Discord 釣魚——**只信官方 repo 與其列出的官方頻道**。
- **不是「印鈔機」**：它反覆強調 correlation regime 是「descriptive risk context, not a signal」、Shadow Account 是診斷工具——**專案本身刻意壓低「賺錢」敘事**，把價值定位在研究嚴謹度與行為紀律。
- LLM 成本：swarm/autopilot 多 agent 跑起來 token 消耗可觀（有 `_microcompact` 壓縮但仍需自備 provider 金鑰）。

## 研究價值與啟示

### 關鍵洞察

1. **「安全靠結構、不靠設定」是這個專案最該被抄的設計**。paper/live 用執行期結構判定而非 config flag、下單工具不上 MCP、research 路徑結構性禁觸 live——這是「假設 agent 會被 prompt injection 或自己犯錯」的**縱深防禦**思路，遠比「加一個 `is_live=false` 開關」可靠。任何會下真單的 agent 都該照這個標準。

2. **Shadow Account 把行為金融學產品化**，避開了「預測市場」這個幾乎無法贏的戰場。它不賭方向，只量化「你 vs 你的紀律」的差距——這是一個**幾乎穩贏的價值命題**（每個散戶都有紀律漏洞），也是它和 [TradingAgents](tradingagents.md) / [AI Hedge Fund](ai-hedge-fund.md) 最大的差異化。

3. **它其實是一個「skill-based agent」**——88 個 `SKILL.md` + 可 CRUD 自建、swarm preset 用 YAML、user skill 同名覆蓋 bundled。這與本站大量 Agent Skills 筆記（[microsoft/skills](microsoft-skills.md)、[jezweb/claude-skills](jezweb-claude-skills.md)）是同一個 progressive-disclosure 範式，只是**垂直深耕到金融領域**。skill 不只是 Claude Code 的東西，是通用 agent 架構。

4. **研究嚴謹度是護城河**：PIT-safe 資料、operator 層 lookahead-ban、`alpha bench --strict`（same-universe random control + OOS gate）、Monte Carlo/Bootstrap/Walk-Forward、run cards 可重現。多數「AI 交易」專案敗在 look-ahead bias 與過擬合；這個專案把防過擬合當成一等公民。**這正好呼應本站量化交易分類反覆出現的主題**（drawdown 控制、robust optimization）。

5. **HKUDS 的「一實驗室多爆款」打法**：LightRAG → RAG-Anything → AI-Trader → Vibe-Trading，同一套「強 README + 高頻 PR + 多語系 + 生態互連（NanoBot/CLI-Anything/OpenSpace/ClawTeam）」的開源運營範式。**它們把開源專案當產品在運營**，README 本身就是一份極高品質的行銷+文件資產。

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [AI-Trader](ai-trader.md) | 同為 HKUDS；AI-Trader 偏「signal & copy trading 平台」，Vibe-Trading 偏「個人研究工作台」——同實驗室的兩條產品線 |
| [TradingAgents](tradingagents.md) / [AI Hedge Fund](ai-hedge-fund.md) | 都是 multi-agent 交易；差異：那兩者給你「一套 agent 團隊策略」，Vibe-Trading 給你「可組合的金融 agent 工作台 + 診斷自己的 Shadow Account」 |
| 量化分類的控制論筆記（[drawdown-modulated](drawdown-modulated-stock-trading.md)、[robust-optimal-linear-feedback](robust-optimal-linear-feedback-trading.md)） | 那些是「策略數學」，Vibe-Trading 是「能承載這些策略的工程平台 + 防過擬合驗證層」 |
| [jezweb/claude-skills](jezweb-claude-skills.md) / [microsoft/skills](microsoft-skills.md) | 同為 skill-based agent 架構；Vibe-Trading 證明 skill 範式可垂直深耕成一個 462-alpha / 88-skill 的領域系統 |
| [GraphRAG](graphrag.md) / [RAG-Anything](rag-anything.md) | 同 HKUDS 出品，可互相印證該實驗室的開源運營與工程品質風格 |
