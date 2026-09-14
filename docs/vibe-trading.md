---
date: "2026-09-14"
category: "量化交易"
card_icon: "material-robot-happy"
oneliner: "HKUDS 的『個人交易 Agent』——pip 一行裝起，自然語言驅動 90 skill / 107 agent tool / 462 alpha / 10 回測引擎 / 18 家券商，安全設計靠結構性 paper/live 護欄而非 config flag，另有一道 grounding gate 擋住模型沒抓過就講出來的數字。約 155 位貢獻者、每天合 5–8 個 PR。2026-09 已 33K★、v0.1.15"
tags:
  - quant
  - multi-agent
  - mcp
---

# Vibe-Trading（HKUDS）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★33,408 / 5,456 forks / MIT / Python 3.11+） | [github.com/HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) |
| 官網 / 文件 | [vibetrading.wiki](https://vibetrading.wiki/) · [Docs](https://vibetrading.wiki/docs/) |
| PyPI 套件 | [pypi.org/project/vibe-trading-ai](https://pypi.org/project/vibe-trading-ai/) |
| SECURITY.md（外部資安稽核、冒名警告） | [SECURITY.md](https://github.com/HKUDS/Vibe-Trading/blob/main/SECURITY.md) |
| HKUDS 實驗室（LightRAG / RAG-Anything / AI-Trader 同源） | [github.com/HKUDS](https://github.com/HKUDS) |
| 第三方索引 | [OpenSource-Hub](https://www.opensource-hub.com/en/library/hkuds-vibe-trading) |

> 本筆記初稿 2026-07-24（當時 ★27,073、v0.1.12），於 **2026-09-14 依 v0.1.15 更新**——數字、券商/引擎清單、以及一段新增的「v0.1.12 → v0.1.15 變化」。

## 專案概述

Vibe-Trading 是香港大學資料智能實驗室 **HKUDS**（LightRAG、[GraphRAG](graphrag.md)、[RAG-Anything](rag-anything.md)、[AI-Trader](ai-trader.md) 的同一實驗室）在 **2026-04 才建立**、五個月內衝到 **33K stars** 的開源專案。定位一句話：**「你的個人交易 Agent」**——把自然語言的金融問題轉成可執行的分析。

技術棧是 **FastAPI 後端 + React 19 前端 + ReAct agent core**，`pip install vibe-trading-ai` 一行裝起，同時提供 CLI（互動 TUI）、REST API、MCP server（74 tools）、Web UI 四個入口。核心迴圈是標準 ReAct，但外掛了一整套金融領域的 skill / tool / 回測 / 資料層。

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
| Finance skill 庫 | **90 skills / 9 類**（Data Source 10、Strategy 19、Analysis 23、Asset Class 9、Crypto 7、Flow 8、Tool 10、Research 3、Risk 1），每個一份 `SKILL.md`，可 CRUD 自建 |
| Agent tools | **107 個**自動探索工具（backtest、cross-session memory、skill CRUD、FTS5 session 搜尋、swarm、web search、bash、factor analysis…） |
| Alpha Zoo | **462 個因子 / 5 家族**：qlib158(154) + alpha101(101) + gtja191(191) + academic(12) + fundamental(4)；一行 `alpha bench` 出 IC + alive/reversed/dead 分類 |
| 回測引擎 | **10 個**（ChinaA T+1、GlobalEquity 美/港/加/英、IndiaEquity、KoreaEquity ±30% band、VietnamEquity T+2、Crypto 現貨/永續、China/Global Futures、Forex）+ options_portfolio + Composite 跨市場共用資金池 |
| 資料源 | **27 個**免費源 + 選配 QVeris premium；`source:"auto"` 依「**IP 封鎖風險**」排 fallback chain（永不封的公開源優先、限流/需金鑰的墊後） |
| 券商連接器 | **18 家**（IBKR、Robinhood、Scalable Capital、Tiger、Alpaca、OKX、Binance、Futu、eToro、MT5、KIS 한국투자증권、Longbridge、Dhan、Shoonya、Zerodha、Upbit、Trading212、Toss Securities）——每一家逐一標註 read / paper / bounded-live 能力邊界 |
| IM channel | **16 個** adapter（Telegram/Slack/Discord/WhatsApp/Signal/QQ/微信/飛書/Teams/email…）跑同一 session runtime |
| 驗證工具 | 15 metrics + benchmark、5 portfolio optimizer、3 驗證（Monte Carlo / Bootstrap / Walk-Forward） |
| Quant Library | **306 個經測試函式 / 23 模組**（`src/quantlib`）——skill 一律 import 這裡，README 明講「公式寫在 `SKILL.md` 裡是 bug 不是 pattern」 |

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

## 挖深一點：Grounding Gate——不准模型講出它沒抓過的數字

這是整個 repo 裡**最值得抄走的一個機制**，但 README 沒有專門一節介紹它，要從 News 一則一則拼出來。

金融 agent 最致命的失敗模式不是分析錯，是**編數字**——「該股收在 412.35」聽起來完全正常，而且沒有任何下游檢查會抓到。Vibe-Trading 的做法是加一道 **grounding gate**：模型答案裡的數值主張，要能對應到實際跑過的 tool 呼叫留下的證據，對不上就擋下來。

有趣的是這道閘門自己的 bug 史，每一個都在教你這種機制有多難做對：

| 日期 | 漏洞 |
|------|------|
| 2026-09-05 | 比對規則匹配 `close` 但**不匹配 `closed`**——於是英文的 `The stock closed at 412.35.` 在沒有任何 tool 呼叫的情況下直接放行，**而中文的同一句偽造主張（`该股收盘 412.35。`）被正確攔下**。同一個幻覺，換個語言就穿過去了 |
| 2026-09-08 | 一個寫成「Metric / Value 兩欄泛用表格」的數值主張，**繞過了會拒絕同樣主張寫成散文時的那道閘**。反過來的錯也有：`close/SMA50 > 1` 裡的 `close` 被讀成「被斷言的價格」而遭誤拒 |
| 2026-08-07 | 誤殺調校——閘門不再把信心分數、指標讀數、均線窗格、沒有年份的日期（`8/5`）、百分比區間、以及交易計畫自己的觸發價（`close ≥ 6.45` 是條件不是報價）當成價格主張 |

**目前還開著的洞**（2026-09 的 open issues，等於官方自曝的已知限制）：

- `[Bug] VaR / ES / CVaR tail-risk claims pass grounding completely unchecked` — **尾端風險數字完全沒被檢查**
- `[Bug] return_observations is ingested as return evidence and can validate a false return claim` — 證據種類搞混，可以拿來「認證」一個假的報酬率主張
- `[Bug] Spanish decimal comma and Unicode minus break analysis grounding` — 西班牙文的小數逗號、Unicode 負號會打爛整個比對
- `[Bug] Generic numeric tool fields can be misclassified as analysis evidence by metric-name`

> **可以直接抄走的想法**：任何會產出數字給人看的 agent，都該有一層「這個數字有沒有來源」的檢查。Vibe-Trading 的教訓同時給了你**兩件事**——這個機制值得做，以及它的實作會在斷詞、語言、數字格式、表格 vs 散文這些地方一直漏。**做這道閘的人要預期自己會被繞過，並且把「已知還沒補的洞」寫進 issue 而不是藏起來。**

## 挖深一點：專案實際長什麼樣

從 README 的 project structure 拆出來的幾個細節，比宣傳數字更能說明工程密度：

- **`factors/base.py` 只有 19 個 operator**（rank / scale / ts_* / delta / decay_linear / safe_div / vwap）就撐起 462 個 alpha——因子庫是**建立在一組小而正交的原語上**，不是 462 份各寫各的程式碼。這也是為什麼 NaN 守衛能一次搬到 registry 層解決 84 個 alpha 的問題。
- **`factors/registry.py` 用 AST-only 載入 metadata + lazy compute + sanity gate**——列出因子清單時不執行任何因子程式碼。
- **`loaders/` 明列 27 個來源**：`tushare`、`okx`、`nobitex`、`wallex`、`binance`、`yfinance`、`akshare`、`baostock`、`tencent`、`mootdx`、`ccxt`、`futu`、`pykrx`、`local`、`eastmoney`、`sina`、`stooq`、`yahoo`、`finnhub`、`alphavantage`、`tiingo`、`fmp`、`longbridge`、`mt5`、`qveris`、`india_broker`、`tickerall`。
- **`agent/loop.py` 做 5 層壓縮 + read/write tool batching**——這是讓多 agent swarm 不會把 context 燒光的關鍵。
- **`tools/ci_grep_gates.sh`**：repo 層級的 CI grep 閘，直接拒收 `yaml.load`、商標字串、逐股資料外洩。

> 小提醒：README 自己有處對不上——capabilities 章節寫「10 engines + options portfolio + composite」，project structure 的註解寫「9 engines + composite + options_portfolio」。引用時以 capabilities 那張表為準（它有逐一列出引擎名稱）。

## 挖深一點：社群規模與維護節奏

| 指標 | 數字 |
|------|------|
| 貢獻者 | **約 155 人**（GitHub contributors API 分頁到第 155 頁） |
| 合併 PR 節奏 | 最近一段時間 **每天 5–8 個**（2026-09-14 一天就合了 8 個） |
| 單一 release cycle | 0.1.14 → 0.1.15：**551 commits / 162 PR / 35 位貢獻者** |
| Open issue 品質 | 幾乎都是帶重現步驟的技術 bug report（grounding 漏洞、broker 連接器邊界、資料源行為） |

Issue tracker 本身就是訊號。**一個專案的 open issue 長什麼樣，比它的 star 數更能說明有沒有人真的在用它。**

### SECURITY.md 的兩個細節

- **回測子行程的環境變數是白名單制**：保留 OS/Python 基礎、proxy/憑證設定、允許的 run-root 設定、以及 loader 需要的唯讀行情憑證；**不轉發** LLM provider 金鑰、API server bearer token、shell 工具的 opt-in、券商交易密鑰、live/advisory 開關。但它也誠實寫明子行程**仍然有網路能力**（loader 要抓資料），所以「不要在有敏感檔案或你不信任本機程式碼存取的網路服務的環境裡跑未經審查的生成策略」。
- **2026-06-18 發生過冒名 Discord 事件**，SECURITY.md 直接寫明官方 Discord 只有一個、任何要你連錢包「驗證」的都是詐騙，還附上萬一已經簽了要去 revoke.cash 撤銷授權。**一個 33K★ 專案把詐騙應對寫進安全政策**，本身就說明開源專案紅到一定程度後多了哪一類維運負擔。

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

## v0.1.12 → v0.1.15 變化（2026-07-24 → 2026-09-14）

### 規模長大

| 面向 | 初稿時 | 現在 |
|------|--------|------|
| Stars / forks | 27,073 / 4,399 | **33,408 / 5,456** |
| 版本 | v0.1.12 | **v0.1.15**（2026-09-09） |
| Finance skills | 88 | **90** |
| Agent tools | 68 | **107** |
| MCP tools | 54 | **74** |
| 券商連接器 | 12 | **18** |
| 回測引擎 | 8 | **10** |
| 資料源 | 22–23 | **27** |
| 語系 | — | **8 種**（新增巴西葡萄牙文） |

新市場：**英國**（LSE `.L`/`.IL`，SDRT 只算買方——兩邊都收會把每趟來回成本高估一半）、**加拿大**、**韓國**（KRX ±30% 幅度在成交當下判定、2026 年 0.20% 交易稅）、**越南**（HOSE T+2、±7%、10/50/100 VND tick grid、100 股一手）。

新券商：Zerodha（第 14 家）、**KIS 한국투자증권**（少數有真正 broker-side 模擬投資沙盒、跑在獨立 host 上）、Upbit、Toss Securities、Scalable Capital。後三家因為沒有 runtime 的 paper/live 判別器或沒有沙盒，**直接被封頂在 read-only 或 paper**——這正是前面那套「安全靠結構」原則的落地。

新功能：唯讀 **多券商投資組合**（`/portfolio`，某個來源刷新失敗就算錯誤、排除在總額外，不拿舊 cache 頂）、**Quant Library +15**（Heston、Hierarchical Risk Parity、copula、VPIN/Roll/Amihud/Kyle 微結構、障礙選擇權有限差分 Greeks、ISDA CDS、Vasicek…）、`scheduled_research`（提案不碰 job store，要你在當下那個介面確認才寫入）、**offline evals harness**（缺少需要的 instrumentation 時吐 `NOT_EVALUABLE`，不會當成通過）。

### 真正值得讀的是這個 cycle 的 bug 主題

v0.1.15 的 release note 把整個 cycle 收斂成**一句話的 bug 類型**：「一個把缺失值悄悄換成合理值的預設，在下游跟真實觀測值無法區分」。三個大修其實是同一隻 bug 換衣服：

1. **Alpha Zoo 的 NaN 契約**：`np.where` 的比較碰到 NaN 得到的是 `False` 而不是 NaN，三元運算就掉到常數分支。把 462 個 alpha 的宣告輸入在某一根 K 棒全部清空，**84 個照樣吐出數字**——而 `dropna()` 正是把資料缺口擋在 IC 外的唯一機制，所以那些常數全被當成真訊號吃下去。修法是把守衛從個別 alpha 搬進 registry（只要宣告的依賴在那根缺了就把輸出遮成 NaN），同一個掃描再跑一次歸零。
2. **pandas `pct_change()` 預設 forward-fill**：缺一根收盤價就變成「一筆 0.0% 的報酬，而那根本沒發生」。先是四個 PR 一個呼叫點一個呼叫點修，後來窮舉掃出 **24 個呼叫點散在 10 個檔案**——其中兩個就在那幾個 PR 正在編輯的檔案裡。
3. **futures loader chain 掛著 `tushare` 和 `akshare`，這兩個根本沒實作期貨端點**，所以每張合約都掉到 A 股權益端點去定價。

還有 2026-09-14 那則：所有無分支的 A 股資料源（`local`/`tencent`/`eastmoney`/`baostock`/`mootdx`/`sina`）把純 A 股籃子路由到 **crypto 引擎**——不收印花稅、沒有 T+1、沒有漲跌停、沒有 100 股整手，還每 8 小時對部位扣一次永續資金費。**run 成功、指標內部一致，這正是它危險的地方**。

**誠實留白**：同一份 release note 明講「52 個 alpha 仍會在自己宣告的 `min_warmup_bars` 之內吐值」，並說明 registry 層的 warmup mask 會誤傷宣告過度保守的 alpha，所以這半邊「stays open and stated rather than quietly carried」——**開著並寫清楚，而不是默默扛著**。

### 自曝的安全問題

這個 cycle 也自己揭露了兩件事，值得任何做 broker 連接器的人抄筆記：

- **13 個存 API key 的 broker config 檔（`alpaca.json`、`zerodha.json` 等）漏在 `.gitignore` 之外**，而 `.gitignore` 的註解宣稱有涵蓋。把 `VIBE_TRADING_HOME` 設在 checkout 目錄的人，一個 `git add -A` 就把憑證送出去了。修法不只是補清單，而是**加一個測試從程式碼推導出這份清單**。
- **paper 取消單對任何 order id 都回 ack**：Zerodha / Dhan / Shoonya 的 paper connector 在本地模擬下單但讀真實帳戶，所以連真單的 id 也會回「已取消」——而那張單其實還活著。改成只接受模擬器自己發出的 id。

## 目前限制 / 注意事項

- **研究/模擬導向**：真實交易能力受限——18 家券商中多數只到 read + paper，bounded-live 僅少數支援；loader 只給 point-in-time 歷史 K 線，**即時 tick / 掛單簿深度不在範圍**。
- **極高活躍度＝高變動**：v0.x（現 v0.1.15，光 0.1.14→0.1.15 一個 cycle 就 551 commits / 162 PR / 35 位貢獻者），News 顯示幾乎每天數十個 PR、大量 reliability sweep——API/行為仍在快速變。引用版本務必對照 CHANGELOG。
- **33K stars 的名氣招來冒名詐騙**：已有假 token / 假 Discord 釣魚——**只信官方 repo 與其列出的官方頻道**。
- **不是「印鈔機」**：它反覆強調 correlation regime 是「descriptive risk context, not a signal」、Shadow Account 是診斷工具——**專案本身刻意壓低「賺錢」敘事**，把價值定位在研究嚴謹度與行為紀律。
- LLM 成本：swarm/autopilot 多 agent 跑起來 token 消耗可觀（有 `_microcompact` 壓縮但仍需自備 provider 金鑰）。

## 研究價值與啟示

### 關鍵洞察

1. **「安全靠結構、不靠設定」是這個專案最該被抄的設計**。paper/live 用執行期結構判定而非 config flag、下單工具不上 MCP、research 路徑結構性禁觸 live——這是「假設 agent 會被 prompt injection 或自己犯錯」的**縱深防禦**思路，遠比「加一個 `is_live=false` 開關」可靠。任何會下真單的 agent 都該照這個標準。

2. **Shadow Account 把行為金融學產品化**，避開了「預測市場」這個幾乎無法贏的戰場。它不賭方向，只量化「你 vs 你的紀律」的差距——這是一個**幾乎穩贏的價值命題**（每個散戶都有紀律漏洞），也是它和 [TradingAgents](tradingagents.md) / [AI Hedge Fund](ai-hedge-fund.md) 最大的差異化。

3. **它其實是一個「skill-based agent」**——88 個 `SKILL.md` + 可 CRUD 自建、swarm preset 用 YAML、user skill 同名覆蓋 bundled。這與本站大量 Agent Skills 筆記（[microsoft/skills](microsoft-skills.md)、[jezweb/claude-skills](jezweb-claude-skills.md)）是同一個 progressive-disclosure 範式，只是**垂直深耕到金融領域**。skill 不只是 Claude Code 的東西，是通用 agent 架構。

4. **研究嚴謹度是護城河**：PIT-safe 資料、operator 層 lookahead-ban、`alpha bench --strict`（same-universe random control + OOS gate）、Monte Carlo/Bootstrap/Walk-Forward、run cards 可重現。多數「AI 交易」專案敗在 look-ahead bias 與過擬合；這個專案把防過擬合當成一等公民。**這正好呼應本站量化交易分類反覆出現的主題**（drawdown 控制、robust optimization）。

5. **HKUDS 的「一實驗室多爆款」打法**：LightRAG → RAG-Anything → AI-Trader → Vibe-Trading，同一套「強 README + 高頻 PR + 多語系 + 生態互連（NanoBot/CLI-Anything/OpenSpace/ClawTeam）」的開源運營範式。**它們把開源專案當產品在運營**，README 本身就是一份極高品質的行銷+文件資產。

6. **「悄悄補上合理預設值」是資料密集型 agent 最陰險的 bug 類型**（v0.1.15 整個 cycle 的主題）。NaN 比較為 `False`、`pct_change()` 預設 forward-fill、fallback chain 指向沒實作的端點——三者的共同形狀是：**下游拿到一個看起來完全正常的數字，無法和真實觀測值區分**，而 `dropna()` 這類清理機制反而因此失效。任何會做回測或因子研究的系統都該問自己：把輸入清空，我的指標會報錯，還是會照樣給我一個漂亮的數字？

7. **Grounding gate 是這個專案第二個該被抄的設計**（第一個是結構性 paper/live 護欄）。「模型講出來的每個數字都要能追到一次 tool 呼叫」這個約束，把金融 agent 最致命的失敗模式——**編一個聽起來完全正常的價格**——從「無法察覺」變成「可攔截」。而它的 bug 史（`close` 匹配到但 `closed` 沒有、中文擋下英文放行、泛用表格繞過散文才擋的規則）也同時告訴你：**這種閘門一定會漏，重點是把漏掉的洞寫成 issue，而不是假裝它是密的。**

8. **Issue tracker 的品質是比 star 數可靠得多的專案訊號**。Vibe-Trading 現在開著的 issue 是「VaR/ES/CVaR 主張完全沒過 grounding 檢查」「西班牙文小數逗號打爛比對」這種等級的東西——**能寫出這種 issue 的人是真的在用它**。對照 [AutoHedge](autohedge.md) 那份 open 兩個月零回覆的驗證報告，兩個 tracker 擺在一起就是兩種專案生命狀態。

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [AI-Trader](ai-trader.md) | 同為 HKUDS；AI-Trader 偏「signal & copy trading 平台」，Vibe-Trading 偏「個人研究工作台」——同實驗室的兩條產品線 |
| [TradingAgents](tradingagents.md) / [AI Hedge Fund](ai-hedge-fund.md) | 都是 multi-agent 交易；差異：那兩者給你「一套 agent 團隊策略」，Vibe-Trading 給你「可組合的金融 agent 工作台 + 診斷自己的 Shadow Account」 |
| 量化分類的控制論筆記（[drawdown-modulated](drawdown-modulated-stock-trading.md)、[robust-optimal-linear-feedback](robust-optimal-linear-feedback-trading.md)） | 那些是「策略數學」，Vibe-Trading 是「能承載這些策略的工程平台 + 防過擬合驗證層」 |
| [jezweb/claude-skills](jezweb-claude-skills.md) / [microsoft/skills](microsoft-skills.md) | 同為 skill-based agent 架構；Vibe-Trading 證明 skill 範式可垂直深耕成一個 462-alpha / 88-skill 的領域系統 |
| [GraphRAG](graphrag.md) / [RAG-Anything](rag-anything.md) | 同 HKUDS 出品，可互相印證該實驗室的開源運營與工程品質風格 |
| [AutoHedge](autohedge.md) | 同樣主打「agent 可下真單」，但沒有任何護欄、免責聲明，執行工具甚至沒接到 agent 上。**和 Vibe-Trading 並排看就是同一問題的正反教材** |
