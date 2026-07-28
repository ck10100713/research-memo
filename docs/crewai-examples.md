---
date: "2026-07-28"
category: "AI Agent 框架"
card_icon: "material-account-group-outline"
oneliner: "CrewAI 官方 30 個完整範例（16 crews + 6 flows + 3 integrations + 5 notebooks），新舊兩代專案骨架並存可直接對照框架演進；但安全性做過一輪硬化、功能正確性沒有——stock_analysis 有重複方法、寫死 AMZN、README 與程式碼互相矛盾，SEC 工具的正則還會把財報數字的小數點和負號洗掉"
tags:
  - agent-framework
  - multi-agent
  - learning
---

# crewAI-examples 研究筆記

> 本篇涵蓋整個 `crewAI-examples` collection，並對 **stock_analysis**、**landing_page_generator**、**instagram_post** 三個 crew 做逐檔解剖。

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/crewAIInc/crewAI-examples> |
| stock_analysis | [crews/stock_analysis](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/stock_analysis) |
| landing_page_generator | [crews/landing_page_generator](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/landing_page_generator) |
| instagram_post | [crews/instagram_post](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/instagram_post) |
| 姊妹 repo | [crewAI-cookbook](https://github.com/crewAIInc/crewAI-cookbook)（功能導向的短教學，與本 repo 的「完整應用」定位互補） |
| 框架本身 | 本站筆記 [CrewAI](crewai.md) |

**Repo 現況**（2026-07-28）：★ 6,120 / fork 2,169 / **repo 根目錄無 LICENSE 檔**（GitHub 顯示 `null`，但個別 crew 的 README 各自宣告 MIT）/ 建立 2023-12-19 / **最後 push 2026-04-20（約 3 個月未更新）** / open issues 75。原作者是 CrewAI 創辦人 [@joaomdmoura](https://x.com/joaomdmoura)。

## Collection 全貌

根 README 的定位很明確：這裡放**完整應用**，功能導向的短教學去 crewAI-cookbook。並聲明「所有範例使用 CrewAI 0.152.0 與 uv」——但下面會看到這句話並不成立。

### 🌊 Flows（6 個）— 有狀態的複雜編排

| 範例 | 重點 |
|------|------|
| Content Creator Flow | 多 crew 協作產出部落格 / LinkedIn / 研究報告 |
| Email Auto Responder Flow | 郵件監控與自動回覆 |
| **Lead Score Flow** | 潛在客戶評分，**含 human-in-the-loop 覆核** |
| Meeting Assistant Flow | 會議記錄處理 + Trello / Slack 整合 |
| **Self Evaluation Loop Flow** | 自我檢視的迭代改稿迴圈 |
| Write a Book with Flows | **平行章節生成**的自動寫書 |

### 👥 Crews（16 個）

| 分類 | 範例 |
|------|------|
| 內容與行銷 | Game Builder、**Instagram Post**、**Landing Page Generator**、Marketing Strategy、Screenplay Writer |
| 商業與生產力 | Job Posting、Prep for a Meeting、Recruitment、**Stock Analysis** |
| 資料與研究 | Industry Agents、Match Profile to Positions（CV 對職缺，向量搜尋）、Meta Quest Knowledge（PDF QA）、Markdown Validator |
| 旅遊規劃 | Surprise Trip、Trip Planner |
| 範本 | Starter Template |

### 🔌 Integrations（3 個）

CrewAI-LangGraph（跨框架整合）、Azure Model、NVIDIA Models。

### 📓 Notebooks（5 個）

Coding Assistant、Flows_101、Landing Page Flow、QA Agent、Simple QA Crew + Flow。

## 兩代專案骨架並存 — 這是意外的教學價值

repo 裡同時存在 CrewAI 的**新舊兩種專案結構**，而且可以直接並排比較：

```
【新骨架】stock_analysis / landing_page_generator      【舊骨架】instagram_post
src/<name>/                                            .
├── config/                                            ├── agents.py    # Agent 用 Python 建構
│   ├── agents.yaml   # 角色定義抽成 YAML                ├── tasks.py     # Task 用 Python 建構
│   └── tasks.yaml    # 任務描述抽成 YAML                ├── main.py      # 手動組 Crew(...)
├── crew.py           # @CrewBase / @agent / @task      └── tools/
├── main.py           # kickoff(inputs={...})
└── tools/
uv.lock                                                poetry（README 仍寫 poetry install）
```

新骨架的核心是三個 decorator：`@CrewBase` 標記類別、`@agent` / `@task` 標記方法，框架自動蒐集成 `self.agents` / `self.tasks`。**把角色與任務的自然語言描述抽進 YAML，程式碼只剩「誰用哪些工具」的接線**——這是 CrewAI 這兩年最重要的結構演進，而這個 repo 讓你能在同一次 clone 裡看到 before / after。

代價是文件沒跟上：根 README 說「全部用 0.152.0 + uv」，但 `instagram_post/README.md` 寫的是「crewAI==0.130.0」與 `poetry install`。

---

## 深入一：stock_analysis

### 設計

三個 agent、四個任務，`Process.sequential` 串接：

| Agent（`agents.yaml`） | 工具 |
|---|---|
| `financial_analyst` — The Best Financial Analyst | Scrape、WebsiteSearch、Calculator、SEC10Q、SEC10K |
| `research_analyst` — Staff Research Analyst | Scrape、SEC10Q、SEC10K |
| `investment_advisor` — Private Investment Advisor | Scrape、WebsiteSearch、Calculator |

| Task（`tasks.yaml`） | 內容 |
|---|---|
| `financial_analysis` | P/E、EPS 成長、營收趨勢、負債權益比 + 同業比較 |
| `research` | 新聞、新聞稿、市場情緒、分析師意見、將至的財報等事件 |
| `filings_analysis` | 從 EDGAR 抓最新 10-Q / 10-K，看 MD&A、財報、內部人交易、揭露風險 |
| `recommend` | 綜合前三者產出完整投資建議，須包含內部人交易與將至事件 |

`tasks.yaml` 的寫法值得注意：每個任務都拆成 `description`（做什麼）與 `expected_output`（產出長什麼樣），而 `expected_output` 裡塞了不少約束（「必須是給客戶的建議」「要漂亮、格式良好」「務必用最新資料」）。**這是 CrewAI 的核心提示工程介面——輸出契約寫在 YAML 而不是散在程式碼裡。**

### `calculator_tool.py` — 這個寫得很好

```python
if not re.match(r'^[0-9+\-*/().% ]+$', operation):   # 字元白名單
    raise ValueError("Invalid characters in mathematical expression")
tree = ast.parse(operation, mode='eval')             # AST 解析，不用 eval()
allowed_operators = {ast.Add: operator.add, ...}      # 運算子白名單
```

AST 解析 + 運算子白名單 + 字元前置檢查，**完全避開 `eval()`**。早期 CrewAI 範例的計算機工具是直接 `eval(operation)`，這份顯然做過安全硬化。想給 agent 一個安全計算器的人可以直接抄。

### 但同一個 crew 裡有數處明確問題

以下都是讀 HEAD 程式碼交叉比對的結果：

**1. `crew.py` 有重複定義的方法。** `financial_analysis` 這個 `@task` 方法被定義兩次，Python 的後者會覆蓋前者。同時有兩個 agent（`financial_agent` 與 `financial_analyst_agent`）綁到**同一個** config key `agents_config['financial_analyst']`，角色/目標/背景完全一樣，只有工具不同——典型的複製貼上殘留。

**2. 股票代號寫死成 AMZN。**

```python
tools=[..., SEC10QTool("AMZN"), SEC10KTool("AMZN")]   # crew.py，兩個 agent
inputs = {'query': '...', 'company_stock': 'AMZN'}     # main.py
```

README 說「執行後輸入要分析的公司」，但 `main.py` **從頭到尾沒有 `input()`**；`'query'` 欄位的值還直接是提示字串本身（`'What is the company you want to analyze?'`）。要換股票得改三個地方。

**3. README 與程式碼直接矛盾。** README 開頭寫「預設使用 GPT-4，所以你需要有 GPT-4 權限」並警告會花錢；程式碼第一行卻是：

```python
from langchain.llms import Ollama      # 已棄用的 import 路徑
llm = Ollama(model="llama3.1")         # 模組層級寫死，每個 agent 都吃這個
```

**4. README 指向不存在的檔案。** 說 key components 是 `./stock_analysis_tasks.py` 與 `./stock_analysis_agents.py`、安裝用 `poetry install --no-root`。實際結構是 `src/stock_analysis/` + YAML + `uv.lock`。這份 README 停在骨架遷移之前。

**5. `sec_tools.py` 的正則會把財報數字洗掉。**

```python
text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
```

註解說是「移除非英文字、錢字號、數字、換行以外的東西」，但這條規則會一併刪掉**小數點、逗號、負號、百分比符號**：

| 原文 | 洗完 |
|------|------|
| `1,234.56` | `123456` |
| `-5.2%` | `52` |
| `$(1,200)` | `$1200` |

**對一個「用來做財務分析」的工具而言，這等於把它要分析的數字全毀了。** 而且方向性資訊（負號、括號表示的負值）也一併消失。

**6. 其他。** SEC 請求的 User-Agent 寫死了某人的個人信箱（`"crewai.com bisan@crewai.com"`）；`__init__` 裡留著 `print("enter init")` 除錯輸出；`RagTool` 在**建構時**就下載並嵌入整份 10-K，所以光是組出這個 crew 就會觸發 4 次下載 + 4 次 embedding。

---

## 深入二：landing_page_generator

### 三個 crew 串成的流水線

單一 `crew.py`（8.8KB）裡定義了多個 `@CrewBase` 類別：

```
ExpandIdeaCrew          →  ChooseTemplateCrew        →  （內容編修）
├ Senior Idea Analyst      ├ Senior React Engineer      └ Senior Content Editor
└ Senior Comms Strategist    （+ FileManagementToolkit
   （Golden Circle 方法）      root_dir='workdir'）
```

四個角色定義在 `agents.yaml`，其中 Senior Communications Strategist 明確被要求用 **Golden Circle 方法**（Simon Sinek 的 why-how-what）來組織敘事——**把具體的方法論寫進 backstory，是比「你是一個很棒的文案」有效得多的角色設定。**

### 它跑不起來，而且作者明講

`main.py` 開頭就是：

```
! YOU MUST FORK THIS BEFORE USING IT !

Disclaimer: This will use gpt-4 unless you changed it not to,
and by doing so it will cost you money (~2-9 USD).
The full run might take around ~10-45m.
```

然後檢查 `./templates` 是否為空，空的就直接 `exit()`：

> Templates are not included as they are Tailwind templates. Place Tailwind individual template folders in `./templates`, if you have a license you can download them at <https://tailwindui.com/templates>

**這個範例依賴一份付費的 Tailwind UI 授權，範本不隨 repo 散布。** 換句話說它不是「clone 下來就能跑的 demo」，而是「你有 Tailwind UI 授權時的自動化骨架」。

值得肯定的是它**明碼標出成本與時間**（2–9 美元、10–45 分鐘）。多數 agent 範例對「跑一次要花多少錢」完全沉默，而這正是初學者最常踩的坑。

### 檔案工具做過完整的安全硬化

`file_tools.py` 的 `write_file` 有五層檢查：

```python
if not re.match(r'^[a-zA-Z0-9._/\-]+$', path): ...        # 字元白名單
if path.startswith("/"): return "絕對路徑不允許"
if ".." in relative_path: return "偵測到路徑穿越"
if not str(resolved_path).startswith(str(workdir)): ...    # resolve 後再確認包含關係
allowed_extensions = {'.jsx','.js','.tsx','.ts','.css',...} # 副檔名白名單
```

`template_tools.py` 同樣：範本名稱字元白名單、明確拒絕 `..` / `/` / `\`、來源與目的地雙向包含檢查、目的地已存在時拒絕覆寫。再加上 `FileManagementToolkit(root_dir='workdir')` 這層框架級的根目錄限制。

**讓 LLM 寫檔案是最危險的工具類型之一，這份實作可以當作硬化樣板直接參考。**

---

## 深入三：instagram_post

### 舊骨架 + 兩段式 crew 串接

五個角色（Lead Market Analyst、Chief Marketing Strategist、Creative Content Creator、Senior Photographer、Chief Creative Director），組成**兩個依序執行的 crew**，用 Python 手動接線：

```python
ad_copy = copy_crew.kickoff()            # 3 agents / 4 tasks：產品分析 → 競品分析 → 活動企劃 → 廣告文案
                                         #        ↓ ad_copy 當成輸入傳入下一段
take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, ...)
image = image_crew.kickoff()             # 2 agents / 2 tasks：攝影 → 創意總監覆核
```

這是在 Flows 出現之前，CrewAI 做多階段工作流的標準寫法：**crew 的輸出當成下一個 crew 的 task 參數手動傳遞。** 對照 `flows/` 目錄裡有狀態的 Flow 寫法，可以清楚看出框架為什麼要引入 Flows。

### 「Senior Photographer」不拍照，它寫 Midjourney prompt

程式最後印的是：

```python
print("'\n\nYour midjourney description:")
```

**這個誠實的設計值得一提**：LLM agent 不生成圖片，它生成「給圖像模型的提示詞」，然後由 Chief Creative Director agent 覆核這段提示詞。多代理系統在能力邊界上的正確做法就是這樣——**不要假裝 agent 能做它做不到的事，讓它產出交給下一個專門系統的輸入。**

### 工具裡藏著一個成本陷阱

`browser_tools.py` 的 `scrape_and_summarize_website`：

```python
content = [content[i:i + 8000] for i in range(0, len(content), 8000)]   # 切成 8000 字元塊
for chunk in content:
    agent = Agent(role='Principal Researcher', ...)   # 每塊都新建一個 agent
    task = Task(agent=agent, description=f'...{chunk}')
    summary = task.execute()                          # 每塊一次 LLM 呼叫
```

**一次網頁抓取 = N 次 LLM 呼叫**（N = 內容長度 / 8000）。抓一個 80KB 的頁面就是 10 次呼叫，而且每次都重新建構 Agent 物件。這個範例全跑本地 Ollama 所以感覺不出來，**但同樣的模式換成 GPT-4 就是帳單爆炸的來源**。想抄這段的人務必加快取與長度上限。

---

## 目前限制與注意事項

| 項目 | 說明 |
|------|------|
| **repo 根目錄沒有 LICENSE** | GitHub API 回傳 `license: null`。個別 crew 的 README 各自寫「MIT License」，但整個 collection 沒有頂層授權宣告。要商用引用前建議先確認 |
| **約 3 個月未更新** | 最後 push 2026-04-20，open issues 75 |
| **「全部用 0.152.0 + uv」不成立** | instagram_post 仍是 0.130.0 + poetry + 舊骨架 |
| **README 與程式碼普遍失同步** | stock_analysis 最嚴重（模型、檔名、安裝方式、輸入方式四項全錯）。**讀這個 repo 一律以程式碼為準** |
| **安全性硬化過，功能正確性沒有** | 三個 crew 的工具層都有明顯的安全 review 痕跡（AST 計算器、路徑穿越防護、副檔名白名單），但同一批檔案裡的重複方法、寫死 AMZN、洗掉小數點的正則都還在。**這強烈暗示曾經跑過一次自動化安全掃描的修補，而沒有人重跑過功能測試** |
| **無測試、無 CI 驗證** | 30 個範例沒有任何機制確認它們在當前 CrewAI 版本下還能跑 |
| landing_page_generator 需付費授權 | Tailwind UI 範本不隨附，沒有就直接 exit |
| stock_analysis 不適合當金融工具 | 除了上述 bug，它產出的是 LLM 生成的「投資建議」，沒有任何回測或驗證 |
| `uv.lock` 巨大 | instagram_post 的 lock 檔 610KB、landing_page 539KB、stock_analysis 433KB，佔了 repo 大部分體積 |

## 研究價值與啟示

### 關鍵洞察

**1. 官方範例集的真正價值是「輸出契約」的寫法，不是程式碼。**
`tasks.yaml` 裡 `description` 與 `expected_output` 的二分法，是 CrewAI 最值得學的介面設計。`description` 說做什麼，`expected_output` 說產出長什麼樣——而後者才是真正在約束 LLM 的地方（「必須是給客戶的完整報告」「務必包含內部人交易章節」「要漂亮、格式良好」）。**把輸出契約從程式碼裡抽出來變成可編輯的 YAML，讓非工程師也能調整 agent 行為**，這是 CrewAI 相對於「一切寫在 Python 裡」的框架最實際的優勢。

**2. 新舊骨架並存，意外成為框架演進的活教材。**
`instagram_post`（Python 建構 + 手動串接兩個 crew）與 `stock_analysis`（YAML + decorator）並排放在同一個 repo，正好展示 CrewAI 為什麼要走向宣告式：舊版把角色描述、工具接線、流程編排全混在 Python 裡，改一句 backstory 要動程式碼；新版把「說什麼」與「接什麼線」分離。**再對照 `flows/` 目錄，能看出第三階段的動機——crew 的手動串接（`ad_copy = copy_crew.kickoff()` 再傳給下一個）在超過兩段之後就不可維護了，於是需要有狀態的 Flow。** 三代寫法同時可見的框架 repo 不多。

**3. 「安全掃描修好了，功能沒人管」是官方範例集的典型腐化模式。**
這個 repo 最有意思的矛盾是：`calculator_tool.py` 從 `eval()` 改成 AST 白名單、`file_tools.py` 有五層路徑穿越防護、`template_tools.py` 連目的地覆寫都擋——顯然做過認真的安全審查。但同一批檔案裡，`crew.py` 有重複定義的方法、股票代號寫死成 AMZN、README 說用 GPT-4 而程式碼寫死 Ollama。**解釋只有一個：安全問題會被自動化工具掃出來並排進待辦，功能正確性不會。** 範例程式碼沒有測試、沒有人跑，壞掉了也沒有訊號。這對所有維護範例集的人都是警訊——[BYOA Core](bring-your-own-agent.md) 用 13 個 eval task、[i-have-adhd](i-have-adhd.md) 用 CI 真的裝一次 plugin，正是為了解決這個問題。

**4. `sec_tools.py` 那條正則是「LLM 時代的資料清洗」最好的反面教材。**
`re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)` 的動機可以理解——把 HTML 轉出來的雜訊清掉，讓 embedding 乾淨一點。但套在 SEC 財報上，它刪掉的是小數點、逗號、負號、百分比。**清洗規則是為「文字」設計的，套用對象卻是「數字密集的財務文件」。** 這類錯誤在 RAG 管線裡特別隱蔽：embedding 照樣產生、檢索照樣有結果、LLM 照樣給出看起來專業的分析——只是數字全錯，而且沒有任何一層會報錯。**任何要對數值型文件做 RAG 的人，都該把「清洗前後抽樣比對數字」列為必做步驟。**

**5. landing_page_generator 明碼標出「2–9 美元、10–45 分鐘」，這件小事應該變成慣例。**
Agent 範例最常見的隱藏成本是「跑一次到底要多少錢」。多代理 + 工具呼叫 + 網頁摘要，一次執行輕易上百次 LLM 呼叫。這個範例在 `main.py` 執行前就把成本與時間印出來，加上 `instagram_post` 那個「每 8000 字元一次 LLM 呼叫」的抓取工具（不標成本就會很痛），對比之下更顯得必要。**Agent 應用的 README 應該像 API 文件標 rate limit 一樣標成本區間。**

**6. 「Senior Photographer 產出 Midjourney prompt」是能力邊界處理的正確示範。**
與其讓 agent 假裝能拍照，不如讓它產出交給圖像模型的提示詞，再讓另一個 agent（Chief Creative Director）覆核這段提示詞。**多代理系統的價值不在於「每個角色都能做真事」，而在於把一個模糊任務拆成一串各自明確的文字產出**，最後由人或專門系統接手執行。這也解釋了為什麼 CrewAI 的範例大多集中在內容、行銷、研究、規劃——這些領域的「產出」本來就是文字。

### 與其他專案的關聯

| 專案 | 關係 |
|------|------|
| [CrewAI](crewai.md) | 框架本身的筆記。這份範例集是它的實作對照——想知道 `Process.sequential`、`@CrewBase`、`expected_output` 實際長什麼樣，看這裡比看文件快 |
| [GenAI Agents (NirDiamant)](genai-agents.md) | 最直接的對照。那份是**跨框架**教學集（三分之二 LangGraph），這份是**單框架**官方應用集。GenAI_Agents 裡 CrewAI 只有一個範例，想學 CrewAI 得來這裡 |
| [StockAgent](stockagent.md) | 都用多代理處理股票，但層次完全不同。StockAgent 模擬**市場**（一群投資人 agent 互相交易），stock_analysis crew 模擬**一間投顧公司**（分析師 + 研究員 + 顧問串接產出報告）。兩者放一起可以看出「多代理」這個詞在金融場景的兩種用法 |
| [AI Hedge Fund](ai-hedge-fund.md)、[TradingAgents](tradingagents.md) | 同樣是「多個角色 agent 產出投資建議」，但那些有回測與真實資料。stock_analysis 是骨架示範，沒有任何驗證機制——**不要把它當投資工具用** |
| [LangGraph Multi-Agent](langgraph-multi-agent.md) | `integrations/CrewAI-LangGraph` 是官方的跨框架整合範例。兩個框架的分工哲學不同：CrewAI 宣告角色與任務，LangGraph 宣告狀態與轉移 |
| [BYOA Core](bring-your-own-agent.md) | 對照「範例集如何腐化」與「單人專案如何用 eval 擋住腐化」。BYOA 的 13 個 eval task 正是這份 repo 缺的東西 |
| [Claude Cookbooks](claude-cookbooks.md) | 同為官方範例集。差別在維護節奏——Anthropic 有動機讓範例跟著 API 更新；這份 repo 停在 4 月，而 README 宣稱的版本與實際內容已經對不上 |
