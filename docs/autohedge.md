---
date: "2026-09-14"
category: "量化交易"
card_icon: "material-bee"
oneliner: "The Swarm Corporation 的「自主對沖基金 Agent」——6.1K★、Director→Quant→Risk→Execution 四 Agent + Solana 真單執行。但實際讀 code：整包約 22 KB Python、一半是 prompt 字串（還有一半是死的），會簽 Solana 交易的 execute_trade 沒接到任何 agent 上，.env 寫的私鑰變數名跟程式讀的不一樣，18 個 CI workflow 指向不存在的 tests/，repo 裡躺著 37 MB 時間戳壞掉的假交易紀錄，主線 2026-02 後停更。是「README 遠大於 code」的教材級案例"
tags:
  - quant
  - multi-agent
  - agent-framework
  - finance
---

# AutoHedge 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★6,082 / 877 forks / MIT / Python） | [github.com/The-Swarm-Corporation/AutoHedge](https://github.com/The-Swarm-Corporation/AutoHedge) |
| PyPI 套件（最新 0.1.6，2026-02-18） | [pypi.org/project/autohedge](https://pypi.org/project/autohedge/) |
| 底層 agent 框架 Swarms | [swarms.ai](https://swarms.ai) · [github.com/kyegomez/swarms](https://github.com/kyegomez/swarms) |
| 執行用的 Jupiter Ultra Swap API | [dev.jup.ag](https://dev.jup.ag) |

> 本筆記的判斷全部來自**實際讀 repo 原始碼**（`autohedge/` 全部檔案 + `.env.example` + `pyproject.toml`），不是轉述 README。數據抓取時間 2026-09-14。

## 專案概述

AutoHedge 自稱「enterprise-grade autonomous agent hedge fund that trades on your behalf」——用 swarm intelligence 跑完整的市場分析 → 風控 → 下單閉環，**目前支援 Solana 全自動交易**，Coinbase 與其他交易所「coming soon」。

作者是 Kye Gomez（The Swarm Corporation），底層用他自己的 [Swarms](https://github.com/kyegomez/swarms) agent 框架。專案 2024-12-10 建立，累積 6,082 stars。

聽起來很猛。但這個筆記的重點是：**把 README 講的跟 code 實際做的擺在一起看**。

## README 說的 vs. code 實際做的

| README 宣稱 | 實際 code |
|------------|-----------|
| Director → Quant → Risk → Execution **四階段 pipeline**（還附 mermaid 流程圖） | `AutoHedge.run()` 只做一件事：`director_agent.run(task)`。Director 是一個 `handoffs=[sentiment, risk, execution, quant]` 的 Swarms Agent——要不要 handoff、handoff 給誰，**由模型自己決定**。沒有確定性的四階段管線 |
| **Full autonomous trading on Solana** | `execute_trade`（Jupiter Ultra Swap、會用 `solders` 簽真交易）確實寫在 `tools/ultra_tools.py`，也收在 `tools/tools_registry.py` 的 `get_tools()` 裡——但 **`get_tools` 在整個 package 沒有被任何檔案 import**。`workers.py` 裡唯一掛上工具的是 sentiment agent 的 `tools=[exa_search]`。Quant / Risk / **Execution 三個 agent 的 `tools` 是空的** |
| Execution Agent「generates and executes orders」 | prompt 要它輸出 order type / quantity / entry / stop loss / take profit / TIF——**純文字輸出**，沒有工具可呼叫，不會真的送單 |
| Real-Time Market Analysis：整合即時行情 | `tools/` 下有 `jupiter_price`、`polygon_api`、`yahoo_api`，但同樣**沒掛到任何 agent 上** |
| Risk-First Design：下單前先做風控 | Risk agent 存在，但 Director 的 handoff 順序由模型決定，**架構上沒有任何東西保證 risk 在 execution 之前跑** |
| `.env.example` 要你填 `WALLET_PRIVATE_KEY` | `ultra_tools.py` 讀的是 **`SOLANA_PRIVATE_KEY`**。照 README 設定，簽章一定拋 `ValueError` |
| `ANTHROPIC_API_KEY` 列在 `.env.example` | 五個 agent 的 `model_name` 全部寫死 `gpt-4.1` / `gpt-4o-mini`，**Anthropic key 沒有任何地方讀** |
| Basic Usage 程式碼範例 | README 的 python code block 裡只有一行字：`autohedge`。不是程式碼 |

## 程式碼盤點

整個 `autohedge/` package（不含 `tools/`）約 **22 KB**：

| 檔案 | 大小 | 內容 |
|------|------|------|
| `prompts.py` | 10,099 B | **最大的檔案**——五個 agent 的 system prompt 字串 |
| `cli.py` | 5,830 B | rich 做的 ASCII banner + 互動 REPL |
| `workers.py` | 2,808 B | 五個 `swarms.Agent` 的宣告 |
| `main.py` | 2,095 B | `AutoHedge` class，`run()` 本體約 20 行 |
| `env_loader.py` | 867 B | 讀 `.env` |
| `__init__.py` / `__main__.py` | 238 B | entry point |

五個 agent：

| Agent | 模型 | 工具 | 角色 |
|-------|------|------|------|
| Trading-Director | gpt-4.1 | 無（只有 handoffs） | 產生交易論點、決定分派給誰 |
| Sentiment-Agent | gpt-4o-mini | `exa_search` | 唯一真的能查外部資料的 agent |
| Quant-Analyst | gpt-4.1 | 無 | 輸出 technical/volume/trend/probability 分數（0–1） |
| Risk-Manager | gpt-4.1 | 無 | 輸出部位大小、最大回撤、風險分數 |
| Execution-Agent | gpt-4.1 | 無 | 輸出訂單參數（文字） |

`tools/` 另有 8 個檔案（exa_search、jupiter_price、jupiter_search、polygon_api、yahoo_api、ultra_tools、tools_registry），**除了 exa_search 之外都是孤兒**。`experimental/` 還放了 `btc_agent.py`、`market_making.py`、`crypto_agent_wrapper.py`。

## 挖深一點（一）：CI 是演的

`.github/workflows/` 底下有 **18 個 workflow 檔**。對一個 22 KB 的 package 來說已經很奇怪，實際讀完更奇怪——**其中 4 個是測試 workflow，而 repo 根本沒有 `tests/` 目錄**：

| Workflow | 它想做什麼 | 為什麼跑不起來 |
|----------|-----------|---------------|
| `run_test.yml` | `pytest tests/` | 沒有 `tests/`，每次 push 都會失敗 |
| `testing.yml` | `pytest tests/` | 同上，而且 trigger 是 `branches: [master]`——**這個 repo 的預設分支是 `main`**，永遠不會觸發 |
| `test.yml` | `make test` / `make extended_tests`，用 `./.github/actions/poetry_setup` | **沒有 Makefile、沒有 `.github/actions/` 目錄**，trigger 也是 `master` |
| `unit-test.yml` | `python3 -m unittest tests/` + `docker build . --file Dockerfile` | **沒有 Dockerfile**；而且 `python3 -m unittest tests/` 傳一個目錄給 unittest，本身就不是合法用法 |

另外還有 5 個各自獨立的 lint / 品質 workflow（`lints.yml`、`ruff.yml`、`pylint.yml`、`quality.yml`、`code_quality_control.yml`）。

`test.yml` 裡的 `extended_testing` extra、`poetry_setup` composite action、`make test` / `make extended_tests` 這組合是 **LangChain 倉庫 CI 的特徵形狀**——這 18 個檔案是從別的 repo 整包複製過來的模板，沒有一個被改成對得上這個專案。

> **重點不是「沒寫測試」**，是 repo 首頁掛著一排 CI badge 的視覺份量，跟實際跑起來的東西完全脫鉤。看 repo 別只看 Actions 有沒有綠勾，要點進去看它到底跑了什麼。

## 挖深一點（二）：repo 裡躺著 37 MB 的假交易紀錄

`logs/` 目錄被 commit 進 repo，裡面兩個檔案：

```
30,294,201 bytes  logs/trades_20250305_193100.csv
 6,855,831 bytes  logs/trades_20250305_193129.csv
```

**37 MB 的交易紀錄，在一個功能性程式碼只有 22 KB 的 repo 裡。** 打開看內容：

```
2025-03-05 11:31:29.f,BTCUSDT,BUY,Price:667.8219070853885,Quantity:2.906810641961535,PnL:0
2025-03-05 11:31:29.f,BTCUSDT,SELL,Price:667.9554848245795,Quantity:4.855816776771281,PnL:0.6486290269661324
```

三個問題，每一個都能單獨說明這份檔案的性質：

1. **時間戳最後是字面上的 `.f`**。有人把 `%f`（微秒）寫成 `.f`，於是整份 37 MB 檔案的每一行都帶著兩個沒被格式化的字元。**沒有人讀過這份輸出**——讀過一眼就會看到。
2. **BTCUSDT 的價格是 $667**。2025 年 3 月的比特幣在 $80,000 上下。這是模擬資料，不是任何真實市場的紀錄。
3. **價格幾乎不動**。11:31:29 的所有成交都在 667.82 / 667.95 這兩個價位之間，六秒後（11:31:35）漂到 665.72 / 665.87。這是一個對著近乎凍結的價格跑的造市模擬迴圈。

再往下追一層更妙：`experimental/market_making.py` 寫出來的檔名格式是 `market_making_{pair}_{timestamp}.csv`——**跟 `trades_*.csv` 對不上**。也就是說，這 37 MB 是由一支**不在 repo 裡的腳本**產生的，然後被 commit 進來留到今天。

## 挖深一點（三）：有人照 README 做了，然後沒人回他

[Issue #42](https://github.com/The-Swarm-Corporation/AutoHedge/issues/42)（2026-07-06，**至今 open、0 則回覆**）是一份寫得極為完整的驗證報告，結論跟本筆記讀 code 得到的完全一樣：

- 環境：Windows + Python 3.11 + `pip install -U autohedge` → 0.1.6
- **有效**：CLI REPL 起得來、Director → handoffs → 子 agent 的多 agent 流程會跑、`EXA_API_KEY` 讓 Sentiment agent 的 `exa_search` 成功執行
- **找不到**：「fully autonomous Solana execution」的任何一條有文件的路徑
- 他自己也注意到了：「Jupiter-related **code exists** in `autohedge/tools/`」——**程式碼存在，但沒有路徑通到它**

他問的是「Solana 自動交易到底是 production-ready、roadmap、還是需要自己接？」。**兩個多月過去，沒有人回答。**

其他 open issue 也透露生態樣貌：[#40](https://github.com/The-Swarm-Corporation/AutoHedge/issues/40) 抱怨只支援 OpenAI/Anthropic 兩家（對照 code：模型還是寫死的）；[#30](https://github.com/The-Swarm-Corporation/AutoHedge/issues/30) 是一篇掛著 Telegram 頻道連結和另一個 repo 的「我跑了 $100k 實盤」推廣文。

## 挖深一點（四）：6,085★ 在自己的 org 裡是 34 倍離群值

The Swarm Corporation 這個 org 有 **160 個 public repo**、448 個 followers。把 star 數排開：

| Repo | Stars | 最後 push |
|------|-------|----------|
| **AutoHedge** | **6,085** | 2026-05-11 |
| ClawSwarm | 178 | 2026-09-14 |
| swarms-rs | 177 | 2025-12-15 |
| AI-CoScientist | 130 | 2026-07-13 |
| swarms-examples | 83 | 2026-07-13 |

同一個作者、同一套工程習慣、同一個框架，**第二名只有 178★，AutoHedge 是它的 34 倍**。程式碼份量沒有 34 倍的差距——差在題材。「autonomous hedge fund that trades on your behalf」這個 hook 本身就是那 6,000 顆星。

## 挖深一點（五）：prompts.py 有一半是死的

`prompts.py` 定義了 **11 個 prompt 常數**，`workers.py` 只 import 其中 **5 個**。死掉的六個是 `RISK_ASSESSMENT_PROMPT`、`EXECUTION_ORDER_PROMPT`、`DIRECTOR_THESIS_PROMPT`、`QUANT_ANALYSIS_PROMPT`、`DIRECTOR_DECISION_PROMPT`、`DIRECTOR_TICKER_DISCOVERY_PROMPT`。

從命名看得出來，它們屬於一個**更早期、更確定性的架構**——有明確的 thesis → quant analysis → risk assessment → execution order 階段，還有一個 `DIRECTOR_DECISION_PROMPT`（`"According to the thesis, {thesis}, should we execute this order: {task}"`）做明確的執行決策閘。這正是 README 的 mermaid 圖畫的那個東西。

2026-02-17 的 commit「[New tools] [Jupiter, polygon, massive] [Remove ticker agent]」之後，架構改成 Swarms 的 `handoffs`，**那個確定性管線被拆掉了，但 README 沒改**。所以 README 描述的不是幻想，是**上一個版本的架構**——只是沒人回來更新文件。

## 專案健康度

| 指標 | 狀況 |
|------|------|
| 最後一次功能性 commit | **2026-02-18**（之後只有 3 筆 dependabot merge，到 2026-03-05） |
| PyPI 最新版 | 0.1.6，2026-02-18（共 10 個版本） |
| GitHub Releases | **0 個** |
| 測試 | repo 根目錄**沒有 `tests/`**，但 `.github/workflows/` 有 **18 個 workflow**、其中 4 個在跑 `pytest tests/` 之類的指令（兩個還綁在不存在的 `master` 分支上） |
| `logs/` 目錄 | **被 commit 進 repo**：兩個 CSV 共 **37 MB**，時間戳帶著沒格式化的字面 `.f`、BTCUSDT 標價 $667、產生它的腳本不在 repo 裡 |
| 版本號一致性 | `pyproject.toml` 寫 0.1.5，`cli.py` fallback 寫 `"0.1.2"`，PyPI 是 0.1.6 |
| 免責聲明 | **完全沒有**。一個會簽 Solana 交易、要你把私鑰放進 `.env` 的專案，README 裡沒有任何風險、法遵或績效免責 |
| 死碼 | `prompts.py` 的 11 個 prompt 常數只有 **5 個**被 import |
| Issue 回應 | 一份詳盡的「照 README 做不出來」驗證報告（[#42](https://github.com/The-Swarm-Corporation/AutoHedge/issues/42)）open 兩個多月、**0 回覆** |
| org 內對照 | 母 org 有 160 個 repo，AutoHedge 6,085★，**第二名 178★** |
| GitHub topics | `blackrock`、`goldmansachs`、`jpmorgan`——這三個跟專案內容零關係，是**純 SEO 塞關鍵字** |

## 還是有可取之處

不是全無價值，以下兩點值得看：

1. **Swarms `handoffs` 的極簡參考實作**。`workers.py` 不到 100 行就示範了「一個 Director agent 帶一組 specialist，用 `handoffs=` 做動態轉交」的寫法。想快速理解 Swarms 框架的 handoff 模式，這是個好起點——就 30 秒的閱讀量。

2. **`ultra_tools.py` 的 Jupiter Ultra Swap 串接是能用的程式碼**。base58 私鑰 → `Keypair` → `VersionedTransaction` 簽章 → 送 `/ultra/v1` 的流程完整，要自己做 Solana swap agent 的話可以直接抄這段（記得環境變數是 `SOLANA_PRIVATE_KEY`）。

## 研究價值與啟示

### 關鍵洞察

1. **6.1K stars 完全不代表 code 的份量**。這個 repo 的 star 數比很多紮實的量化框架都高，但功能性程式碼不到 22 KB，其中最大的檔案是 prompt 字串。**評估開源 AI 專案時，README 的說服力和 star 數都是雜訊，`git log` 的最後日期、有沒有測試、核心模組多大才是訊號**。這一條對整個「AI Agent 做交易」的賽道特別重要，因為這個題材天生容易衝 star。

2. **「工具寫了但沒掛上 agent」是 agent 專案最容易出現、也最難從外面看出的斷點**。AutoHedge 把 `execute_trade` 寫好、放進 registry，然後 registry 沒人 import——README 於是可以誠實地說「我們有 Solana 執行能力」，而跑起來的 agent 其實碰不到它。**看 agent 專案一定要追一條線：工具函式 →(誰 import) → agent 的 `tools=` 參數**。追不到就是沒接上。

3. **和 [Vibe-Trading](vibe-trading.md) 對照，能看出「會下真單的 agent」該長什麼樣**。Vibe-Trading 用結構性 paper/live 判別器（帳號 ID 格式 / host 分離 / demo 旗標）、mandate gate（allowlist + 部位上限 + kill switch）、下單工具不上 MCP、research 路徑結構性禁觸 live endpoint，還有一份明確的免責聲明。AutoHedge 的對應設計是：**沒有**。同一件事（自主下單）的兩種做法擺在一起，就是最好的教材。

4. **Prompt 不是架構**。這個專案把「風控優先」寫在 Risk agent 的 system prompt 裡，但 Director 的 handoff 順序由模型自由決定——**寫在 prompt 裡的保證，在架構上等於沒有保證**。要讓風控真的先跑，得用確定性的程式流程，不是靠提示詞拜託模型。

5. **免責聲明的缺席本身就是訊號**。金融 + 會簽私鑰交易 + 沒有任何免責與風險說明，通常代表專案沒被當成真的要有人拿去用的東西在維護。

6. **README 描述的常常不是幻想，而是「上一版的架構」**。AutoHedge 的 mermaid 四階段管線、`DIRECTOR_DECISION_PROMPT` 這種明確的執行決策閘，在 2026-02 改成 Swarms `handoffs` 之前是真的存在的。**重構拆掉了確定性流程，文件留在原地。** 這比「作者在吹牛」更常見、也更難察覺——看到 README 和 code 對不上，先去翻 git log，通常能找到那個沒有回頭改文件的 commit。

7. **CI badge 的視覺份量跟實際執行完全可以脫鉤**。18 個 workflow、4 個測試 job、5 個 lint job，指向不存在的 `tests/`、不存在的 `Makefile`、不存在的 `Dockerfile`，兩個還綁在不存在的 `master` 分支。**看 repo 要點進 Actions 看實際跑了什麼，不是看首頁有幾個綠勾。**

8. **commit 進 repo 的產出物是最誠實的證據**。那 37 MB CSV 誰都沒看過——看過一眼就會發現時間戳壞了、BTC 標價 $667。**一個專案的「沒被讀過的輸出」比它的 README 更能說明它被使用的真實程度。**

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [Vibe-Trading](vibe-trading.md) | 同為「agent 可下真單」；Vibe-Trading 把安全做進結構、18 家券商逐一標註 paper/live 能力邊界，AutoHedge 沒有任何護欄。**兩者是同一問題的正反範例** |
| [AI Hedge Fund](ai-hedge-fund.md) | 該筆記把 AutoHedge 列為「支援 Solana 真實執行、是下一步的參考」——**本筆記的結論是需要修正這個說法**：執行能力寫了但沒接上 agent |
| [TradingAgents](tradingagents.md) | 同為多 Agent 交易團隊；TradingAgents 有論文與可重現流程，AutoHedge 只有 prompt |
| [CrewAI](crewai.md) / [OpenAI Agents SDK](openai-agents-sdk.md) | 同屬 multi-agent 框架的 handoff 範式；AutoHedge 是 Swarms 框架的一個薄應用層 |
| [StockAgent](stockagent.md) | 同為 LLM 交易 agent 研究；StockAgent 走學術驗證路線，對照之下更凸顯 AutoHedge 缺少任何驗證層 |
