---
date: "2026-07-28"
category: "量化交易"
card_icon: "material-flask-outline"
oneliner: "ACM TIST 論文的官方實作：用 LLM 多代理模擬股市，刻意不餵歷史行情以避開 test set leakage；核心結論是「換一個 LLM 就換一種市場」——GPT 交易少但單量大、個體分散，Gemini 頻繁交易且群體高度趨同。程式碼有多處已驗證的落差，預設參數下所有事件都不會觸發"
tags:
  - quant
  - multi-agent
  - finance
---

# StockAgent 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/MingyuJ666/Stockagent> |
| 論文（arXiv） | [When AI Meets Finance (StockAgent), arXiv:2407.18957](https://arxiv.org/abs/2407.18957)（v1 2024-07-15 → **v5 2026-06-23**，33 頁、10 圖） |
| 發表 | ACM Transactions on Intelligent Systems and Technology (TIST) |
| 相依工具 | [PromptCoder / procoder](https://github.com/dhh1995/PromptCoder)（prompt 組裝 DSL，需自行 clone 安裝） |

**作者群**：Chong Zhang（Liverpool）、Xinyi Liu（北大）、Zhongmou Zhang（上財）、Mingyu Jin（Rutgers）等 13 人，跨英美中三地七所學校，通訊作者 Yongfeng Zhang（Rutgers）。

**Repo 現況**（2026-07-28）：★ 684 / fork 162 / **無 LICENSE 檔** / Python / 建立 2024-02-02 / 最後 push 2026-06-16。程式碼本體只有 7 個 `.py`（約 60KB），其餘是 4 張架構圖與 `.idea/`、`__pycache__/`（未 gitignore）。

## 專案概述

StockAgent 問的是一個模擬問題而非預測問題：**如果讓一群 LLM 扮演散戶、在一個沒有歷史行情可查的虛構市場裡自由交易，外部因素（利率、財報、政策事件、論壇八卦）會怎麼改變他們的行為與價格？**

它的核心設計主張是「避開 test set leakage」。既有的 LLM 交易模擬多半直接餵真實歷史股價，於是模型可能是在回憶訓練資料而不是在決策——你分不出它是「判斷」還是「背答案」。StockAgent 的做法是造一個完全虛構的市場：公司 A/B（新版擴充到 A/B/C/D）、自編的財報數字、自編的政策事件，LLM 沒有任何先驗知識可用。

論文設定三個 research question：

| RQ | 問題 |
|----|------|
| **RQ1 — Simulation Effectiveness** | 換不同 LLM 驅動模擬，交易決策還可信嗎？ |
| **RQ2 — LLM Reliability** | 股票推薦與交易策略會被所選 LLM 的內在傾向影響嗎？ |
| **RQ3 — External Conditions** | 財務數據、市場指標、基準利率、突發事件、盤後 BBS 討論如何影響交易行為？ |

論文實驗用的是 **GPT-3.5-turbo-0125** 與 **Gemini-pro-1.0** 兩個模型。

## 模擬機制

### 四階段流程

```
Initial Phase        agent 隨機初始化（持股/現金/負債，性格四選一）
      ↓
Trading Phase        每日 N 個 session，隨機打亂交易順序，逐一問 LLM 下單
      ↓
Post-Trading Phase   Daily: 論壇發文 + 預測明日行動
                     Quarterly: 財報發布
      ↓
Special Events       隨機交易日觸發（降準降息 / 升息）
```

### 每個 agent 的一天

```python
# main.py 主迴圈（簡化）
for date in 1..TOTAL_DATE:
    agent.loan_repayment(date)              # 到期還本，cash<0 → is_bankrupt
    if date in REPAYMENT_DAYS: 付息
    if is_bankrupt: bankrupt_process()      # 強制賣股補現金，補不足則退場
    if date == EVENT_DAY: 改 LOAN_RATE + 往論壇塞一則官方訊息
    agent.plan_loan(...)                    # LLM 決定要不要借錢
    for session in 1..TOTAL_SESSION:
        random.shuffle(交易順序)
        for agent: action = agent.plan_stock(...)   # LLM 回一個 JSON 下單
                   handle_action(...)               # 撮合
        stock.update_price(date)            # 價格 = 該 session 最後一筆成交價
    agent.next_day_estimate()               # LLM 預測自己明天會不會買/賣/借
    agent.post_message()                    # LLM 發論壇文 → 成為所有人明天的輸入
```

**論壇（BBS）是這個模擬最關鍵的社會性設計**：每個 agent 收盤後發一則貼文，隔天所有 agent 的 prompt 裡都會看到全部人的貼文。這是唯一的 agent 間資訊通道，也是後面「群體趨同」現象的來源。

### Secretary：規則式格式守門員

`Secretary` 這個類別在論文裡聽起來像個 LLM 角色，但在釋出的程式碼裡它是**純 Python 的 JSON 驗證器**——`check_loan` / `check_action` / `check_estimate` 全是手寫的格式與額度檢查（大括號只能有一組、`loan` 只能 yes/no、買不能超過現金、賣不能超過持股）。驗證失敗就把錯誤訊息塞回 retry prompt，最多重試 3 次，仍失敗就當作「今天不動作」。

`Secretary.run_api()` 確實有一條 LLM 路徑，但它 `openai.api_key = ""` 寫死空字串，而且 `agent.py` 從頭到尾沒呼叫過 `get_response()`——是死程式碼。

### 撮合規則

`handle_action()` 的成交條件是**價格完全相等**（`if action["price"] == sell_action["price"]`），沒有價格穿越（買價 100 不會吃掉賣價 99 的單）。撮合不成的單留在當日 order book 裡，隔天全部清空。收盤價 = 該 session 最後一筆成交價；當日無成交則價格不變。

## 論文的實際結論

### 1. 換一個 LLM 就換一種市場（RQ1）

| | GPT-3.5 驅動 | Gemini-pro 驅動 |
|---|---|---|
| 交易頻率 | **較低** | 較高 |
| 單筆成交量 | **顯著較大** | 較小 |
| 對 Stock A | 更謹慎 | A 與 B 頻率相近，整體活躍 |
| 價格走勢 | ~1750 rounds，A 從 30 漲到 107 | ~470 rounds，A 從 30 漲到 48 |

論文對這件事的態度很直白：**「使用 StockAgent 做測試的使用者與交易所應注意，模擬結果可能因 LLM 選擇而產生偏差。」**

### 2. 群體行為的差異更值得注意（RQ2）

用 cluster analysis + t-SNE 看 agent 群體分布：

- **Gemini agents 彼此高度相似、群體行為一致** → 明顯的羊群效應（herding）與趨勢跟隨
- **GPT agents 在視覺化中分散** → 個體差異大、更獨立，論文形容為「能體現個人化的投資策略與風格」

這對「用 LLM multi-agent 模擬社會系統」是個一般性警訊：**你觀察到的「群體現象」有多少是被模擬對象的性質，有多少只是底層模型的性格？**

### 3. 外部條件消融實驗（RQ3）

論文逐一拿掉五種外部資訊，觀察價格與行為：

| 拿掉什麼 | 觀察到的效果 |
|---------|------------|
| **利率變動** | agent 對市場與公司表現**更樂觀**；Stock A 交易頻率顯著上升；部分 agent 由虧轉盈 |
| **BBS 論壇討論** | 心理估值轉保守、壓低股價；agent 行為更謹慎、避免大額交易 |
| **非首輪貸款** | agent 更保守 |
| **財報** | 部分 agent 由虧轉盈 |
| **任一種財務資訊** | **agent 之間的損益差距擴大（變異變大），市場競爭更激烈** |

另外 Stock B（新上市股）因為缺少 BBS 資訊流通，被 agent 壓到低於理想估值，並在第 21 個交易輪出現 flash crash。

### 4. 最重要的一句結論

> 儘管受外部因素影響，模型的**內在交易傾向在單步交易中依然明顯，顯示 context learning 並未顯著改變它們面對市場的根本取徑。**

換句話說：你可以用 prompt 改變 LLM 看到什麼，但改不掉它的交易性格。論文把「不同 LLM 能否可靠地擔任交易員」明確列為未解問題。

## 快速開始

```bash
conda create --name stockagent python=3.9 && conda activate stockagent

git clone https://github.com/dhh1995/PromptCoder && cd PromptCoder && pip install -e . && cd ..
git clone https://github.com/MingyuJ666/Stockagent && cd Stockagent
pip install -r requirements.txt

export OPENAI_API_KEY=...        # 或 export GOOGLE_API_KEY=...
python main.py --model gemini-pro
```

## 目前限制與注意事項

以下都是實際讀 HEAD（`e2a9c05`，2026-06-16）程式碼交叉比對後的發現，不是推測。

### A. 設定檔與執行程式碼已經對不上

2026-06-08 那兩個 commit（`Update util.py`、`Update agent_prompt.py`）把設定與 prompt 升級到一個**四檔股票、含非 LLM baseline、多 seed 的新實驗設計**，但 `main.py` / `agent.py` / `stock.py` 全部停在 2024 年版本：

| 檔案（新） | 宣告了什麼 | 檔案（舊） | 實際支援 |
|---|---|---|---|
| `util.py` | `STOCK_NAMES = ["A","B","C","D"]`、Table 3/5/7/9 財務常數、Table 10 理想價格區間、RQ1/RQ2/RQ3 run seeds | `main.py` | 只建立 `Stock("A")` 與 `Stock("B")` |
| `util.py` | `SUPPORTED_PROVIDER_MODELS = [gpt-5.5, Claude-4.6-Sonnet, gemini-3.1-flash-lite, DeepSeek-V4-flash, claude-haiku-4-5]` + YunWu gateway + `resolve_model_name()` | `agent.py` | `run_api()` 只認模型名含 `gpt` 或 `gemini`，其餘回傳 `None`；`resolve_model_name` 從未被呼叫 |
| `util.py` | `NON_LLM_BASELINES = [Fundamental Trader, Trend Follower, Noise Trader]` | — | 沒有任何 baseline 實作 |
| `util.py` | `import settings as local_settings` | — | repo 裡沒有 `settings.py`，也沒有 `settings.example.py` |
| `agent_prompt.py` | 模板需要 `{stock_c_price}`、`{stock_d_price}`、`{stock_c_deals}`、`{stock_d_deals}`、`{stock_c}`、`{stock_d}` | `agent.py` | `inputs` dict **完全沒提供這六個變數** |

最後一項最致命：`format_prompt(prompt, inputs)` 拿不到模板要求的變數。實際是 raise `KeyError` 還是留下未填佔位符取決於 procoder 的行為，但無論哪種，**四檔股票的模擬都不會正確運作**——`main.py` 只有兩檔股票、`buy_stock()` 裡還寫死 `stock_name not in ['A','B']`。

值得注意的是論文 v5（2026-06-23 修訂）附錄裡的 prompt 仍然是兩檔股票 A/B。所以 repo 的新設定是**為某個尚未發表的擴充版準備的半成品**，不是 v5 的對應實作。

### B. 預設參數下所有事件都不會觸發

```python
TOTAL_DATE = 10                                   # 模擬只跑 10 天
SEASON_REPORT_DAYS = [12, 78, 144, 210]           # 財報最早第 12 天
EVENT_1_DAY = 78 ; EVENT_2_DAY = 144              # 降準/升息
REPAYMENT_DAYS = [22, 44, 66, ...]                # 付息最早第 22 天
```

10 < 12 < 22 < 78 < 144。**用預設值跑一次，會得到一個沒有財報、沒有政策事件、沒有付息的十天市場**——也就是論文 RQ3 想研究的東西一個都不會出現。要重現論文結果必須自己把 `TOTAL_DATE` 調大。

### C. 兩處參數順序不符的呼叫

**1. 持股數量記成價格。** `main.py` 四個成交點都這樣呼叫：

```python
# main.py
get_agent(...).buy_stock(stock.name, close_amount, action["price"])
# agent.py — 簽章是 (stock_name, price, amount)
def buy_stock(self, stock_name, price, amount):
    self.cash -= price * amount          # 乘法可交換，現金正確
    if stock_name == 'A':
        self.stock_a_amount += amount    # ← amount 收到的是「價格」
```

現金因為乘法可交換所以算對了，但**持股張數增加的是成交價、不是成交量**。`sell_stock` 同樣。

**2. 貸款重試路徑。** `check_loan` 的簽章是 `(resp, max_loan)`，但重試分支呼叫 `self.secretary.check_loan(date, resp)`（`agent.py:208`）——把日期當成回應傳進去。

### D. 其他

| 項目 | 說明 |
|------|------|
| **無 LICENSE** | repo 沒有授權檔案。README 只給 citation，未授權任何使用條款。要在專案裡用它的程式碼需先聯繫作者 |
| 論文模型已過時 | 實驗用 GPT-3.5-turbo-0125 與 Gemini-pro-1.0（2024 年初）。今日模型的交易性格是否仍如論文所述，未經驗證 |
| 市場微結構極簡 | 撮合要求價格完全相等、無價格穿越、無做空、無流動性提供者、隔日清空所有掛單。價格由「最後一筆成交價」決定 |
| 無回測對照 | 虛構市場帶來的代價是**沒有 ground truth**。無法判斷 agent 的行為是否「合理」，只能做組間比較 |
| 版控衛生 | `.idea/`、`__pycache__/`（含 `.pyc`）都進了 git |
| `requirements.txt` 僅 95 bytes | 未鎖版本，2024 年的 `google.generativeai` 與 `openai` API 介面在今日環境可能已不相容 |

## 研究價值與啟示

### 關鍵洞察

**1. 「避開 test set leakage」這個設計動機，比模擬結果本身更重要。**
LLM 做金融預測的評測有一個結構性難題：你餵它 2023 年的行情問它明天怎麼走，它可能只是記得。StockAgent 的解法是把整個市場虛構掉——自編公司、自編財報、自編政策。這確實斷開了記憶通道，但代價也是結構性的：**沒有真實市場當基準，你只能做組間比較（GPT vs Gemini、有 BBS vs 無 BBS），永遠無法回答「哪一組更接近真實」。** 這是 LLM 社會模擬類研究的共同困境，StockAgent 把它擺得特別清楚。

**2. 「換一個 LLM 就換一種市場」對所有 LLM 社會模擬研究都是壞消息。**
論文最紮實的發現不是「利率影響交易」（這是常識），而是 GPT 群體分散、Gemini 群體趨同這個對比。如果你想用 multi-agent LLM 模擬任何社會現象——市場、輿論、組織——你觀察到的「湧現行為」有一部分只是底層模型的性格投影。**論文自己的結論「context learning 並未顯著改變模型面對市場的根本取徑」等於承認：prompt 改得動它看到什麼，改不動它是誰。** 這也直接反駁了「換個 prompt 就能讓 LLM 扮演任意投資人型態」的直覺。

**3. 消融實驗裡最反直覺的一條：拿掉利率資訊讓 agent 變樂觀。**
一般預期是「資訊變少 → 更保守」，但實驗結果相反——移除利率變動後 agent 對市場與公司表現更樂觀、Stock A 交易頻率顯著上升，部分 agent 甚至由虧轉盈。合理的解讀是：利率資訊在這個模擬裡主要扮演**風險提示**的角色，拿掉它等於拿掉了唯一會定期提醒 agent「借錢有成本」的訊號。相對地，拿掉 BBS 反而讓估值轉保守——**社群討論在這個系統裡是推升價格的力量，不是穩定力量。**

**4. Secretary 是規則式驗證器，而不是 LLM——這其實是正確的工程選擇，值得抄。**
論文架構圖裡 Secretary 看起來像個代理角色，實作卻是純 Python 的格式與額度檢查 + 最多 3 次帶錯誤訊息的重試。這比「再叫一個 LLM 來檢查前一個 LLM」便宜幾個數量級，而且格式驗證本來就是確定性問題。**任何要讓 LLM 輸出結構化動作的系統，都該把「格式合法性」與「額度合法性」放在確定性的守門員裡，不要浪費一次 API 呼叫。** 唯一的缺陷是它留了一條 `api_key = ""` 的死程式碼路徑沒清掉。

**5. 這個 repo 是「論文程式碼」這個品類的典型樣本，讀它要用不同的標準。**
684 star、162 fork、ACM TIST 接收，同時有：無 LICENSE、參數順序寫反、預設參數下事件全不觸發、設定檔比執行程式碼超前一整個實驗設計。這不是作者不用心——是**論文程式碼的目的是「支撐論文裡那組數字」，不是「讓別人跑」**。162 個 fork 裡有多少人真的跑成功過，是個有意思的問題。想引用它的結論可以放心（論文經過同儕審查）；想直接跑它的程式碼，得先自己修上面那幾處。

**6. 把「模擬」與「賺錢」分開看，這個專案的定位才成立。**
它不是交易系統、不預測任何真實標的、backtest 對它沒有意義。它是**一個用來研究「LLM 當投資人時是什麼樣子」的實驗裝置**。這個定位在 LLM 金融應用裡是少數派——多數專案在追報酬率，StockAgent 在追行為特徵。從風險管理角度看，後者可能更有用：**在你把 LLM 放進交易決策鏈之前，先知道它的內建偏誤長什麼樣。**

### 與其他專案的關聯

| 專案 | 關係 |
|------|------|
| [AI Hedge Fund](ai-hedge-fund.md) | 目的完全相反的鏡像。AI Hedge Fund 用多個 LLM 角色（各投資大師 agent）**追求報酬**，跑真實歷史資料；StockAgent 用多個 LLM 角色**觀察行為**，刻意避開真實資料。前者的 test set leakage 風險，正是後者要解決的問題 |
| [TradingAgents](tradingagents.md)、[AI-Trader](ai-trader.md)、[Vibe-Trading](vibe-trading.md) | 同屬 LLM × 交易，但都是「決策系統」；StockAgent 是「市場模擬器」。這四個放在一起可以看出這個領域的兩條分岔：**做決策 vs 研究決策者** |
| [多 Agent 辯論會](multi-agent-debate.md) | 同樣關心「多個 LLM 互動時會湧現什麼」。StockAgent 的 BBS 論壇機制就是一個受限的辯論場——差別是它有價格這個客觀後果，可以量測「說服」的實際影響 |
| [Prediction Market Analysis](prediction-market-analysis.md) | 都在研究「群體如何把資訊變成價格」。StockAgent 的優勢是可以做消融（拿掉 BBS 看會怎樣），真實預測市場做不到 |
| 本站量化交易分類的 Kelly / Drawdown 系列 | 那些是**規範性**研究（最優策略應該長怎樣）；StockAgent 是**描述性**研究（LLM 實際會怎麼做）。有意思的對照題：把 Kelly 準則寫進 system prompt，LLM agent 會遵守嗎？論文的「內在傾向不因 context learning 改變」暗示答案可能是否定的 |
| [i-have-adhd](i-have-adhd.md)、[BYOA Core](bring-your-own-agent.md) | 同樣提醒「模型選擇本身就是一個未受控變因」。BYOA 的 eval 用 `system_prompt_hash` 綁定提示詞版本；StockAgent 的教訓則是**連模型本身都該被當成實驗條件記錄下來**，因為 GPT 和 Gemini 跑出的是兩個不同的市場 |
