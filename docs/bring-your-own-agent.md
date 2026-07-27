---
date: "2026-07-27"
category: "AI Agent 框架"
card_icon: "material-toy-brick-outline"
oneliner: "台灣單人開發者用 5.5 週、90 commits 從零重建一套 Claude Code 等級的 agent harness（兩階段 compact、subagent 防遞迴、skill 漸進式載入、tool result 分頁、多 provider gateway），全繁中、Gherkin 規格先行、附 13 個 SWE eval task 量化每次 prompt 改動——0 star 但是最好讀的 harness 解剖圖"
tags:
  - agent-framework
  - mcp
  - benchmark
  - taiwan
---

# Bring Your Own Agent (BYOA Core) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/class83108/Bring-Your-Own-Agent> |
| PyPI 套件 | <https://pypi.org/project/byoa-core/>（`0.1.0`，2026-02-12 上傳） |
| 架構文件 | `docs/architecture.md`（15KB）+ `docs/architecture.excalidraw` |
| 開發規範 | `CLAUDE.md`（9KB，型別/命名/Gherkin/工具鏈全套規範） |
| Gherkin 規格 | `docs/features/core/*.feature`（24 份）+ `docs/features/app/*.feature`（5 份） |
| Eval 任務 | `tests/eval/tasks/t01`–`t13` + `tests/eval/framework.py` + `tools/eval_viewer.html` |
| Roadmap | `docs/todo.md` |

**Repo 現況**（2026-07-27）：★ 0 / fork 0 / issue 0 / MIT / Python 3.12+ / 181 個檔案 / 90 commits，**全部出自單一作者** `class83108`（YAO AN CHUANG）。開發期 2026-01-24 → 2026-03-03（約 5.5 週密集開發），此後約 5 個月無新 commit。`Development Status :: 3 - Alpha`。

## 專案概述

這是一個**從零重建 coding agent harness** 的專案。README 的定位是「可擴充的 AI Agent 核心框架，透過 API 直接與 Claude 互動，自由組裝 Tools、Skills、MCP」，四個賣點：

| 賣點 | 原文說法 |
|------|---------|
| API-first | 直接呼叫 Anthropic API，不依賴 CLI 工具，**無被封禁風險** |
| Pay-per-use | 按量計費，輕度使用比月費訂閱更划算 |
| 可組裝 | Tools、Skills、MCP 三種擴充機制，像樂高一樣自由拼裝 |
| 可嵌入 | 作為 library 嵌入你的應用，不是獨立 CLI 工具 |

但真正值得注意的不是這四點，而是**它實際重建了什麼**。掃一遍 `src/agent_core/` 會看到：兩階段上下文壓縮、subagent 防遞迴機制、skill 的漸進式載入與隱形模式、tool result 自動分頁、think 工具、檔案式工作記憶、token counter + 費用估算、可續傳串流（EventStore）、多模態輸入、多 provider 路由 gateway、指數退避重試。**這是 Claude Code / Anthropic harness 那套已知設計的一份完整的、正向重建的、繁體中文實作**。

以「有沒有人用」衡量，這個專案是零（0 star、0 fork、0 issue、5 個月未動）。以「能不能讀懂 agent harness 到底在做什麼」衡量，它是本站目前收錄過最直接的教材之一——因為它不是逆向猜測別人的 minified 程式碼，而是有規格、有測試、有架構圖、有 eval 分數的正向實作。

## 技術架構

### 三層 + Protocol 解耦

```
┌──────────────────────────────────────────────────┐
│          可插拔擴充層 (Extension Layer)            │
│   Tools  ·  Skills  ·  MCP                       │
├──────────────────────────────────────────────────┤
│          核心層 (Core Layer)                      │
│   Agent（串流 → 工具調用 → 迭代）                  │
│   + Compact · Subagent · Memory · TokenCounter   │
├──────────────────────────────────────────────────┤
│          基礎設施層 (Infrastructure Layer)         │
│   LLMProvider · SessionBackend · Sandbox · EventStore │
└──────────────────────────────────────────────────┘
```

四條設計原則寫得很明確：**Protocol-based 依賴注入**（結構子型別，使用者不需繼承 base class）、**Async-first**（所有 I/O 都是 async）、**Message-centric**（Agent 狀態就是對話歷史，replay-safe）、**最小介面**（每個 Protocol 只定義必要方法）。

五個擴展點與可替換目標：

| Protocol | 內建實作 | 文件明示的替換場景 |
|----------|---------|------------------|
| `LLMProvider` | Anthropic / OpenAI / Gemini / **Gateway** | 本地 Ollama 等 |
| `SessionBackend` | `MemoryBackend`、`SQLiteBackend` | Redis、DynamoDB、PostgreSQL |
| `EventStore` | `MemoryEventStore`（含 TTL） | Redis Streams、Kafka |
| `Sandbox`（ABC） | `LocalSandbox` | Docker Container、Firecracker microVM |
| `MCPClient` | 使用者自行實作 | 任何 MCP Server |

### Agent 對話迴圈

```
stream_message(content, attachments?, stream_id?)
├─ 1. 驗證輸入 + 建構 user message
├─ 2. 追加到 conversation
├─ 3. _stream_with_tool_loop()
│   ├─ 3a. _maybe_compact()          ← token 使用率 ≥ 80% 觸發
│   ├─ 3b. provider.stream()          ← yield 文字 token + AgentEvent
│   ├─ 3c. 記錄 usage → 追加 assistant message
│   ├─ 3d. stop_reason == 'end_turn' ? 結束 : 繼續
│   └─ 3e. _execute_tool_calls()
│       ├─ asyncio.gather() 平行執行
│       ├─ 建構 tool_result blocks → 追加 user message
│       └─ 回到 3a（上限 max_tool_iterations = 25）
├─ 4. EventStore 記錄事件（若有 stream_id）
└─ 5. 標記串流完成 / 失敗
```

### 四個值得單獨看的機制

**1. Compact（兩階段上下文壓縮）**

```
usage < 80%  → 不壓縮
Phase 1: 截斷舊 tool_result（無 API 呼叫，低成本）
  ├─ 掃描 user messages 的 tool_result blocks
  ├─ 舊的 content 換成 '[已壓縮的工具結果]'
  ├─ 保留最近 N 輪不截斷
  └─ 有截斷就返回，不進 Phase 2
Phase 2: LLM 摘要
  ├─ 找安全分割點（不打斷 tool_use → tool_result 配對）
  └─ 早期對話送 LLM 摘要，換成 user/assistant 摘要訊息對
```

「安全分割點偵測」是整個設計裡最容易被忽略但最致命的一步——如果切在 `tool_use` 和對應的 `tool_result` 之間，API 會直接拒絕整個請求。

**2. Subagent（子代理）**

複製 `ToolRegistry` 但**排除 `create_subagent` 本身**（防遞迴）、獨立 conversation（不污染父 agent context）、**共享父 agent 的 Sandbox**（同一安全邊界）、只回傳 `{'result': accumulated_text}`。可平行建立多個。

**3. Skill 的三段可見性**

| 狀態 | system prompt 裡有什麼 |
|------|---------------------|
| 已註冊未啟用 | 只有 `name` + `description`（LLM 知道有這個能力存在） |
| 已啟用 | 完整 `instructions` 注入 |
| `disable_model_invocation=True` | 連描述都不載入（完全隱形） |

而且做成 REST API 讓終端使用者在對話中即時切換：`POST /api/skills/{name}/activate`。這是 Anthropic Agent Skills 漸進式披露（progressive disclosure）的一個獨立重實作，連 `disable-model-invocation` 這個 frontmatter 欄位名都對得上。

**4. GatewayProvider（框架內建的迷你 LLM Gateway）**

```python
_MODEL_PREFIX_MAP = [
    ('claude-', 'anthropic'), ('gpt-', 'openai'),
    ('o1', 'openai'), ('o3', 'openai'), ('o4', 'openai'),
    ('gemini-', 'gemini'),
]
```

用模型名稱前綴自動路由，加上 fallback 備援與 middleware chain（middleware 的具體實作如 cost tracking、OTel tracing 刻意留在應用層）。Provider 類別用 lazy import 避免迴圈依賴。

### 內建工具

| 工具 | 說明 |
|------|------|
| `read_file` / `edit_file` / `list_files` / `grep_search` | 檔案讀寫、目錄瀏覽、正則搜尋（支援上下文行數） |
| `bash` | Shell 執行（含安全限制） |
| `think` | 無副作用的推理記錄 |
| `web_fetch` / `web_search` | httpx + BeautifulSoup / Tavily API |
| `create_subagent` | 建立子代理 |
| memory `view`/`write`/`delete` | 檔案式工作記憶，路徑穿越防護用 `resolve().is_relative_to(root)` |

memory 工具的 system prompt 引導詞很值得抄：**「假設對話隨時可能被壓縮」**——直接把 compact 的存在告知 agent，讓它主動把重要狀態寫進檔案。

## Eval 驅動開發

這是全專案最稀有的部分。`tests/eval/` 裡有 13 個 SWE 風格任務，難度分級（easy/medium/hard/special）：

| Task | 內容 |
|------|------|
| t01–t04 | 修語法錯誤 / 修失敗測試 / 加函式 / 加錯誤處理 |
| t05–t06 | 從症狀找 bug / 從測試反推實作 |
| t07 | 大型 codebase |
| t08 | 模糊需求 |
| t09 | 自我修復迴圈 |
| t10 | 完整 TDD 循環 |
| t11 | Web crawler（本地 HTTP 爬蟲） |
| t12 | 迷宮探索（**Memory + Compact 壓力測試**） |
| t13 | Subagent 平行修復 |

`EvalResult` 記錄的欄位比分數本身更有意思：

```python
task_name, task_level, passed, score,        # 基本
tool_calls, tool_call_sequence,              # 工具用了幾次、順序長什麼樣
total_tokens, duration_seconds,              # 成本
ran_verification,                            # ← agent 有沒有自己跑測試
system_prompt_hash,                          # ← SHA256 前 8 碼，綁定提示詞版本
```

`system_prompt_hash` 加 `ran_verification` 這兩個欄位，讓「改了 system prompt 之後 agent 變乖了嗎」變成可查詢的資料而不是印象。`todo.md` 裡確實照這個流程走：v1-baseline 9/10 通過、avg 0.91，然後列出 P0–P4 優化方向（system prompt 強化、工具描述任務導向化、max iterations 上限、working memory、think 工具），逐條標記完成並註明對應的 target task。

Task 自動探索用 `pkgutil.iter_modules` 掃 `t??_*.py`，並驗證模組有 `TASK_NAME` / `setup` / `evaluate` 才收——一個輕量的 Protocol 檢查。另附 `tools/eval_viewer.html`（17KB）看結果。

## 工程紀律

| 面向 | 做法 |
|------|------|
| 規格先行 | **Gherkin 驅動 TDD**：`.feature`（繁中 `# language: zh-TW`）→ 紅燈測試 → 綠燈實作 → 重構。29 份 feature 檔，用 `Rule:` 分組 scenario |
| 型別 | `pyright` **strict** 模式；`CLAUDE.md` 明文規定「優先定義型別，避免 `cast()`」，並列出 5 種替代手段（TypedDict + `Literal` discriminated union、縮窄參數型別、用 `['key']` 而非 `.get()` 觸發 narrowing、`TypeGuard`），`cast()` 只准用在反序列化邊界 |
| 測試分層 | unit（`tests/core`、`tests/app`）/ smoke（`tests/manual`，需 `--run-smoke` + 真實 API + 會花錢）/ eval（需 `--run-eval`） |
| CI | GitHub Actions ×3：`ci.yml`、**`codeql.yml`**、**`sonarcloud.yml`** + codecov + pre-commit + Allure 報告 |
| 慣例 | Conventional Commits、`feature/*` branch、ruff（single quote、line-length 100）、uv 管套件且禁止手改 `pyproject.toml` dependencies |

測試量遠大於實作量：`test_agent.py` 41KB vs `agent.py` 15KB；`test_api.py` 46KB vs `main.py` 18KB。

## 快速開始

```bash
uv add byoa-core          # 或 pip install byoa-core
uv add byoa-core[all]     # web(fetch/search) + mcp + openai
export ANTHROPIC_API_KEY=...
```

```python
import asyncio
from pathlib import Path
from agent_core import Agent, AgentCoreConfig, AnthropicProvider, Skill, SkillRegistry
from agent_core.tools.setup import create_default_registry

async def main():
    config = AgentCoreConfig(system_prompt='你是專業的程式開發助手。')
    registry = create_default_registry(Path('./workspace'))   # read/edit/list/grep/bash

    skills = SkillRegistry()
    skills.register(Skill(name='code_review', description='程式碼審查',
                          instructions='審查程式碼並以表格輸出結果。'))
    skills.activate('code_review')

    agent = Agent(config=config, provider=AnthropicProvider(config.provider),
                  tool_registry=registry, skill_registry=skills)

    async for chunk in agent.stream_message('請讀取 main.py 並審查程式碼'):
        if isinstance(chunk, str):
            print(chunk, end='', flush=True)

asyncio.run(main())
```

另附 FastAPI 應用層（`src/apps/agent_app/main.py`）與 vanilla JS 前端（`static/`，app.js 23KB），提供 SSE 串流對話、session CRUD、token 用量、沙箱檔案樹、skill 即時開關等端點：

```bash
uv run uvicorn agent_app.main:app --reload --port 8000
```

## 目前限制與注意事項

| 項目 | 說明 |
|------|------|
| **實質停更** | 2026-03-03 後約 5 個月無 commit。90 commits 全出自一人，無外部貢獻者、無 issue 討論。作為生產依賴風險高 |
| **LocalSandbox 不是真沙箱** | 只做路徑驗證（`resolve().is_relative_to`）+ subprocess 執行。真正的容器隔離（`ContainerRunner`、`RunnerPool`）在 `todo.md` Priority 7 仍未打勾。`bash` 工具「含安全限制」但邊界靠應用層自己補 |
| **文件落後於程式碼** | README 架構圖只列 `anthropic_provider`，實際已有 OpenAI / Gemini / Gateway 三個；README 的 Protocol 表仍寫「`LLMProvider` 內建實作：`AnthropicProvider`」；`todo.md` 把「多 Provider」列為「應用層待辦」（早就做完）、把「發佈到 PyPI」標為未完成（2026-02-12 就上了）。**讀這個 repo 要以程式碼為準** |
| **無 PyPI 更新** | PyPI 只有 `0.1.0`（2026-02-12），之後 2 週的 OpenAI/Gemini/Gateway 開發都沒發版。`uv add byoa-core` 拿到的是舊版，最新功能得從 git 裝 |
| **零外部驗證** | 0 star / 0 fork / 0 issue。eval 分數是作者自測（v1-baseline 9/10、avg 0.91），無第三方復現 |
| Python 3.12+ 硬需求 | `pyright` strict + `from __future__ import annotations` 風格，向下相容未考慮 |
| 全繁中 | 註解、docstring、feature 檔、規範文件都是繁體中文。對中文讀者是優勢，要國際化就得整批翻譯 |

## 研究價值與啟示

### 關鍵洞察

**1. 這是「正向重建」而非「逆向拆解」，正好補上本站缺的那一半視角。**
本站已收錄 [Analysis Claude Code](analysis-claude-code.md)、[Claude Code Reverse](claude-code-reverse.md)、[Claude Code from Source](claude-code-from-source.md)——那些都是**從 minified bundle 往回猜設計意圖**。BYOA 走反方向：先寫 Gherkin 規格，再寫紅燈測試，再實作，最後用 eval 量測。同一組機制（compact、subagent、skill 漸進載入、tool result 分頁、max iterations）從兩個方向看，逆向能告訴你「官方實際怎麼寫」，正向能告訴你「為什麼非得這樣寫、不這樣寫會壞在哪」。**想真的理解 harness，兩邊都得讀。**

**2. `system_prompt_hash` + `ran_verification` 這兩個 eval 欄位，是整個 repo 最該被抄走的 12 行程式碼。**
多數人調 agent prompt 的流程是「改一改、跑幾次、感覺好像好一點」。BYOA 把 system prompt 的 SHA256 前 8 碼寫進每一筆 eval 結果，於是「哪個版本的提示詞得到這個分數」變成可查資料；再加上 `ran_verification`（agent 有沒有自己跑測試）、`tool_call_sequence`（工具調用的順序），量測的就不只是「答對了嗎」，而是**「它的工作習慣變好了嗎」**。`todo.md` 的優化表格能逐條標 ✅ 並註明 target task，靠的就是這個。這件事和 [i-have-adhd](i-have-adhd.md) 給輸出風格建 eval harness 是同一個思路的不同尺度：**prompt 是需要回歸測試的產出物。**

**3. Protocol-based DI 讓「BYOA」這個名字名副其實，但代價是使用者要自己補的東西不少。**
五個 Protocol 都把「替換場景」寫在文件裡（Redis / Kafka / Firecracker / Ollama），這是很誠實的設計——框架不假裝自己有生產級後端。但反過來說，`MCPClient` 和 `LockProvider` 的內建實作是「使用者自行實作」，`Sandbox` 只有 LocalSandbox，`EventStore` 只有記憶體版。**框架給的是介面與參考實作，不是 batteries-included。**這對學習是優點（每個介面都小到能一眼看完），對上生產是待辦清單。

**4. 「無被封禁風險」是這個專案真正的產品起點，而它揭示了一個市場縫隙。**
README 第一個賣點不是技術，是「不依賴 CLI 工具，無被封禁風險」+「輕度使用比月費划算」。這把 Claude Code 訂閱制的兩個真實焦慮直接寫成賣點。有意思的是這個縫隙的存在方式：官方 [Claude Agent SDK](claude-agent-sdk.md) 也是 API-first，但它是「用官方的殼」；BYOA 選擇連殼都自己寫。**對只要一個可嵌入 library、不想要一整個 CLI harness 的人，這個選擇是理性的**——即使代價是自己維護 15KB 的 agent loop。

**5. 5.5 週、90 commits、單人做到這個完整度，靠的是規格先行而不是寫得快。**
29 份 Gherkin feature 檔、`CLAUDE.md` 裡連「什麼時候不准用 `cast()`」都寫成 5 條替代手段、pyright strict、CodeQL + SonarCloud + codecov 三重 CI——這些看起來像過度工程，但正是它能在單人條件下維持 181 個檔案不失控的原因。特別是 `CLAUDE.md` 的型別規範那段：它其實是**寫給 AI coding agent 看的**（討論 discriminated union narrowing 該用 `['key']` 而不是 `.get()`），把「這個專案的品味」編碼成 agent 讀得懂的規則。這和 [Ponytail](ponytail.md)、[Awesome DESIGN.md](awesome-design-md.md) 是同一件事的不同維度。

**6. 文件漂移是高速單人開發的固定成本，而它有跡可循。**
README 說只有 Anthropic provider、`todo.md` 說多 provider 是「應用層待辦」、`todo.md` 說 PyPI 未發佈——三處都被程式碼推翻。這不是粗心：2026-02-24 到 03-03 那 8 天連續加了 OpenAI、Gemini、Gateway 三個 provider 並重組專案結構，文件根本追不上，然後開發就停了，漂移被凍結在那裡。**讀任何停更的個人專案，都應該先假設文件是舊的，用 git log 和檔案樹交叉驗證。**

### 與其他專案的關聯

| 專案 | 關係 |
|------|------|
| [Analysis Claude Code](analysis-claude-code.md)、[Claude Code Reverse](claude-code-reverse.md)、[Claude Code from Source](claude-code-from-source.md) | **鏡像關係**。那三個從 minified bundle 逆向推設計；BYOA 從規格正向重建同一組機制。同題目的兩種解法，配著讀最有價值 |
| [Claude Agent SDK](claude-agent-sdk.md) | 官方的 API-first 答案。BYOA 是「連官方 SDK 都不用，自己寫一遍」的版本——用來理解官方 SDK 幫你擋掉了哪些事 |
| [CrewAI](crewai.md)、[Google ADK](google-adk.md)、[OpenAI Agents SDK](openai-agents-sdk.md)、[LangChain](langchain.md) | 同為 agent 框架，但那些是團隊產品、有生態與社群。BYOA 的定位不同：它是**單人可讀完的完整實作**（core 約 200KB Python），適合當「框架到底在幫我做什麼」的解剖對象 |
| [LiteLLM](litellm.md) | `GatewayProvider` 是 LiteLLM 的框架內建迷你版——模型前綴路由 + fallback + middleware chain。可以對照看「自建 gateway 要處理哪些事、什麼時候該直接用 LiteLLM」 |
| [i-have-adhd](i-have-adhd.md) | 兩者都自建 eval harness 來擋 prompt 迴歸，但尺度相反：i-have-adhd 量測**輸出形狀**（14 個 case、加權 rubric、release gate），BYOA 量測**任務完成能力**（13 個 SWE task、score + tool_call_sequence + ran_verification）。合起來剛好是「agent 該怎麼講話」與「agent 該怎麼做事」兩套回歸測試 |
| [Ponytail](ponytail.md)、[Awesome DESIGN.md](awesome-design-md.md) | `CLAUDE.md` 把型別品味（何時不准 `cast()`）寫成 agent 讀得懂的規則，是同一種「把品味編碼成檔案」的做法，只是維度換成靜態型別 |
| [AI Engineering from Scratch](ai-engineering-from-scratch.md)、[Karpathy LLM Wiki](karpathy-llm-wiki.md) | 同屬「從零重建以求理解」的學習路徑。差別是那些是為教學而寫，BYOA 是為自用而寫、順便成了教材——所以它保留了教學專案通常會省略的髒細節（compact 的安全分割點、subagent 防遞迴、tool result 分頁） |
