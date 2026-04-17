---
date: "2026-04-17"
category: "學習資源"
card_icon: "material-notebook-multiple"
oneliner: "Anthropic 官方 40.8K stars 的 Claude 食譜庫，從 RAG 到 Managed Agents 的完整可執行範例"
---
# Anthropic Claude Cookbooks — 40.8K stars 的官方範例庫

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) |
| Claude Agent SDK（本 repo 子目錄） | [claude_agent_sdk/](https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk) |
| Managed Agents Tutorials | [managed_agents/](https://github.com/anthropics/claude-cookbooks/tree/main/managed_agents) |
| Skills Cookbook | [skills/](https://github.com/anthropics/claude-cookbooks/tree/main/skills) |
| Agent Patterns | [patterns/agents/](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents) |
| 姊妹 repo（Claude Agent SDK Python） | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) |
| Anthropic 官方文件 | [docs.claude.com](https://docs.claude.com/claude/docs/guide-to-anthropics-prompt-engineering-resources) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 維護方 | **Anthropic 官方** |
| Stars / Forks | **40,841 / 4,503** |
| 語言 | Jupyter Notebook（Python） |
| License | MIT |
| 建立日期 | 2023-08-15 |
| 最近更新 | **2026-04-17**（本筆記建立當日仍在活躍維護） |
| 先前名稱 | `anthropic-cookbook`（README 內許多連結仍指向舊名） |

**Claude Cookbooks** 是 Anthropic 官方維護的可執行範例合集，以 Jupyter Notebook 為主，每個資料夾都是一個主題的「食譜」。README 本身已經落後 repo 實際結構，**最新的價值集中在最近半年內新增的資料夾**：`managed_agents/`、`claude_agent_sdk/`、`skills/`、`patterns/agents/`、`tool_use/context_engineering/` 等。

適合場景：
- 想學 Claude 新 API 時 **避開過時教學**，直接看官方 canonical 寫法
- 把 notebook 當成 prompt / workflow 的「可執行文件」
- 找一個類似場景的起手式複製修改

---

## 資料夾全景（2026-04-17 snapshot）

```
claude-cookbooks/
├── capabilities/          # 基礎能力：classification, RAG, summarization, text_to_sql, knowledge_graph
├── claude_agent_sdk/      # Claude Agent SDK 六個主題 tutorial（新）
├── coding/                # coding 專屬範例（目前只有 frontend aesthetics prompt）
├── extended_thinking/     # Extended Thinking + Tool Use
├── finetuning/            # Fine-tuning 範例
├── managed_agents/        # Claude Managed Agents（CMA）完整教學（最新，2026-04 大批新增）
├── misc/                  # prompt caching / JSON mode / moderation / PDF / evals
├── multimodal/            # Vision、圖表判讀、crop tool
├── observability/         # usage_cost_api（新）
├── patterns/agents/       # Anthropic "Building Effective Agents" 三種模式實作
├── skills/                # Claude Skills（Excel / PPT / PDF / 自製 skill）
├── third_party/           # Pinecone / Voyage / Wikipedia / ElevenLabs
├── tool_evaluation/       # Tool 評估方法
└── tool_use/              # Tool use 進階（PTC、tool search embedding、context engineering）
```

---

## 核心重點分類

### 1. `managed_agents/` — Claude Managed Agents 完整教學（2026-04 最新）

這是 Anthropic 2026 年 4 月推出的 **CMA（Claude Managed Agents）** 託管執行環境，「定義 agent + sandbox environment 一次，後續 session 保留檔案、工具狀態、對話」。

**應用範例（applied cookbooks）**：

| Notebook | 做什麼 |
|---------|-------|
| `data_analyst_agent.ipynb` | CSV → pandas + plotly → 互動式 HTML 敘事報告 |
| `slack_data_bot.ipynb` | Slack bot 版 data analyst（mention 機器人上傳 CSV，thread 內回報告；後續回覆延續同一 session） |
| `sre_incident_responder.ipynb` | 告警 → agent 讀 log 和 runbook → 找根因 → 開 PR → 等待 human 核准 |

**指南式教學（guided tutorials）**：

| Notebook | 教什麼 |
|---------|-------|
| **`CMA_iterate_fix_failing_tests.ipynb`** | **建議入門** — agent / environment / session、file mounts、streaming event loop，透過修 3 個被植入的 bug 串起全流程 |
| `CMA_orchestrate_issue_to_pr.ipynb` | issue → fix → PR → CI → review → merge（透過 mock gh CLI） |
| `CMA_explore_unfamiliar_codebase.ipynb` | 用 agent 探索不熟悉的 codebase（有植入 stale-doc 陷阱） |
| `CMA_gate_human_in_the_loop.ipynb` | 人工審批：custom-tool `decide()` / `escalate()`、`requires_action` idle bounce |
| `CMA_prompt_versioning_and_rollback.ipynb` | server-side prompt 版控：v1 → 評估 → v2 → 檢出 regression → 回滾 |
| `CMA_operate_in_production.ipynb` | 生產環境：vault-backed MCP credentials、`session.status_idled` webhook（HITL without long-lived connections）、resource lifecycle CRUD |

> Anthropic 把 streaming event loop 抽成 `utilities.stream_until_end_turn` 供其他 notebook 重用，但 gate notebook 保留 inline 版因為 custom-tool agent 要額外處理 `requires_action`。這個「何時抽、何時不抽」的決策很值得學。

### 2. `claude_agent_sdk/` — Claude Agent SDK 六個主題 tutorial

從研究 agent 一路做到多 agent 協作。**假設你已在用 Claude Code 做軟體工程**，目標是教你把它用在非 coding 領域。

| 編號 | 主題 | 核心概念 |
|------|------|---------|
| **00** | The One-Liner Research Agent | `query()` async 迴圈、WebSearch、`ClaudeSDKClient`、系統 prompt 專化 |
| **01** | The Chief of Staff Agent | CLAUDE.md 持久化指示、Output Styles、Plan Mode、Custom Slash Commands、Hooks、Subagent Orchestration、Bash Tool |
| **02** | The Observability Agent | （配合 GitHub token + Docker） |
| **03** | The Site Reliability Agent | SRE agent |
| **04** | Migrating from OpenAI Agents SDK | 從 OpenAI Agents SDK 遷移到 Claude Agent SDK |
| **05** | Building a Session Browser | 自建 session 瀏覽器 |

### 3. `skills/` — Claude Skills 實戰（Progressive Disclosure）

| Notebook | 內容 |
|---------|-----|
| `01_skills_introduction` | Skills 架構、beta headers、首個 Excel、PPT、PDF |
| `02_skills_financial_applications` | 財務 dashboard、投資組合分析、CSV→Excel→PPT→PDF 跨格式 workflow |
| `03_skills_custom_development` | 自製 skill：財務比率計算器、品牌指南 skill、financial modeling suite |

核心概念：**Progressive Disclosure Architecture** — skill 只在需要時載入，節省 token。

### 4. `patterns/agents/` — "Building Effective Agents" 經典模式

這是 Anthropic 公認文章《Building Effective Agents》的**官方參考實作**：

| Notebook | 模式 |
|---------|------|
| `basic_workflows.ipynb` | Prompt chaining、parallelization、routing |
| `evaluator_optimizer.ipynb` | Evaluator-Optimizer：一個 LLM 評估、另一個 LLM 優化，迭代改進 |
| `orchestrator_workers.ipynb` | Orchestrator-Workers：中央 LLM 動態分派子任務給 worker |

> 想懂 agent 設計模式不用再到處找，**從這三個 notebook 入門就對了**。

### 5. `tool_use/` — 工具使用進階

最近更新的幾個值得收藏：

| Notebook | 要點 |
|---------|------|
| `programmatic_tool_calling_ptc.ipynb` | **PTC** — 讓 Claude 寫 code 在 code execution 環境裡呼叫 tool，降低延遲 + token |
| `tool_search_with_embeddings.ipynb` | 用語意 embedding 動態發現工具，**scale 到上千個工具** |
| `automatic-context-compaction.ipynb` | 長 agentic workflow 的對話自動壓縮 |
| `context_engineering/context_engineering_tools.ipynb` | 比較 memory / compaction / tool clearing 三種 context 工程策略 |
| `threat_intel_enrichment_agent.ipynb` | IOC 調查 + MITRE ATT&CK 映射 |

### 6. 其他高價值 Notebooks

| 分類 | 重點 Notebook |
|------|------|
| `extended_thinking/` | `extended_thinking.ipynb`、`extended_thinking_with_tool_use.ipynb` |
| `multimodal/` | `best_practices_for_vision`、`crop_tool`（給 Claude 一個裁切工具做細節分析） |
| `capabilities/` | `knowledge_graph/guide.ipynb`（2026-03）、`contextual-embeddings`（RAG 加 context 後再 embed） |
| `observability/` | `usage_cost_api.ipynb` |
| `misc/` | `prompt_caching`、`building_evals`、`how_to_enable_json_mode`、`building_moderation_filter` |
| `third_party/ElevenLabs/` | `low_latency_stt_claude_tts.ipynb`（低延遲語音助理） |

---

## 官方 CLAUDE.md 中的開發規範（值得抄的慣例）

Repo 的 `CLAUDE.md` 是 Anthropic 自己的貢獻者指南，包含 **官方認為的最佳實踐**：

### 環境

```bash
uv sync --all-extras            # 裝依賴
uv run pre-commit install       # 裝 pre-commit
cp .env.example .env            # 設 ANTHROPIC_API_KEY
```

### Makefile 指令

```
make format        # ruff format
make lint          # ruff check
make check         # format-check + lint
make fix           # auto-fix + format
make test          # pytest
```

### 風格

- Line length **100 字元**
- **Double quotes**
- Formatter **Ruff**
- Notebook 放寬 E402 / F811 / N803 / N806（import 位置、重定義、變數命名）

### Commit 慣例（Conventional Commits）

```
feat(scope): add new feature
fix(scope): fix bug
docs(scope): update documentation
```

Branch：`<username>/<feature-description>`

### **模型 ID 規範（2026 年當下 canonical）**

| 模型 | 直接 API | Bedrock |
|------|---------|---------|
| Sonnet | `claude-sonnet-4-6` | `anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Haiku | `claude-haiku-4-5` | `anthropic.claude-haiku-4-5-20251001-v1:0` |
| Opus | `claude-opus-4-6` | `anthropic.claude-opus-4-6-v1` |

> 注意：**不要用帶日期的 ID**（如 `claude-sonnet-4-6-20250514`）；Bedrock 可加 `global.` prefix 走 global endpoint。
> 本 CLAUDE.md 寫於 Opus 4.7 發表前，4.7 的規範需對照 [`best-practices-for-using-claude-opus-4-7-with-claude-code`](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code)。

### 官方定義的 Slash Commands

- `/notebook-review` — 檢查 notebook 品質
- `/model-check` — 驗證 Claude model 引用
- `/link-review` — 檢查變更檔案內連結

---

## 使用建議

### 依學習階段選路徑

| 階段 | 建議路徑 |
|------|---------|
| 剛接觸 Claude API | `capabilities/` RAG + `misc/prompt_caching` + `misc/building_evals` |
| 想懂 agent 設計 | `patterns/agents/` 三個 notebook → `claude_agent_sdk/` 00 → 01 |
| 要做 coding agent | `claude_agent_sdk/` 01-03 + `coding/prompting_for_frontend_aesthetics` |
| 要上生產 | `managed_agents/CMA_operate_in_production` + `observability/usage_cost_api` |
| 工具規模化 | `tool_use/tool_search_with_embeddings` + `tool_use/programmatic_tool_calling_ptc` |
| 長任務 context | `tool_use/context_engineering/context_engineering_tools` + `tool_use/automatic-context-compaction` |
| 多模態 | `multimodal/best_practices_for_vision` + `multimodal/crop_tool` |
| 文檔自動化 | `skills/` 三個 notebook |

### 注意事項

- **README 比實際 repo 落後** — `claude_agent_sdk/`、`managed_agents/`、`patterns/`、`observability/` 都不在 README 的 Table of recipes。認真看 `registry.yaml` + 資料夾結構才知道最新內容
- repo 先前叫 `anthropic-cookbook`，README 內大量連結仍指向舊名（`github.com/anthropics/anthropic-cookbook/...`），會 redirect，但 watch / contribute 時要注意新名
- CLAUDE.md 中寫的模型 ID 是 Opus 4.6 時期；4.7（2026-04-16 發表）之後要改為 `claude-opus-4-7`
- Jupyter Notebook 執行需要 `ANTHROPIC_API_KEY`；Notebook 02 還要 `GITHUB_TOKEN` + Docker

---

## 研究價值與啟示

### 關鍵洞察

1. **Cookbook 是 Anthropic 官方「activity log」的公開版本**
   - 新功能發表後幾天內，對應 notebook 一定會進來（CMA 2026-04-07、Knowledge Graph 2026-03-23）
   - 比 `docs.claude.com` 更新得快，是看 Anthropic 下一步的「前置指標」
   - **追蹤 `registry.yaml` 的 commit 比看 release note 更有用**

2. **`patterns/agents/` 是最被低估的部分**
   - 三個 notebook 精確對應《Building Effective Agents》部落格的三種模式
   - 「先選模式、再選工具」是 Anthropic 強推的 agent 設計哲學，比直接跳 LangGraph / CrewAI 更務實

3. **Managed Agents 是比 SDK 更上層的抽象**
   - Claude Agent SDK 要你自己管 session 狀態；**CMA 把 state / file mount / streaming 都託管**
   - `CMA_operate_in_production` 揭露了 **生產 agent 的真正痛點**：vault-backed credentials、idle webhook、resource CRUD —— 這些在 SDK 教學裡通常被跳過
   - 適合對 DevOps 熟但不想自己管 agent state 的團隊

4. **CLAUDE.md 是「Anthropic 自己怎麼管理 AI 輔助開發」的參考案**
   - Line 100、double quotes、Ruff、Conventional Commits —— 這是 Anthropic 內部認可的 AI-friendly code style
   - 模型 ID 規範（**用 alias 不用 dated ID**）值得直接抄到自己的 CLAUDE.md
   - 三個 slash command（`/notebook-review`、`/model-check`、`/link-review`）示範了**怎麼把 review 自動化**

5. **README 與 repo 不同步的意義**
   - 表示 Anthropic 把 `registry.yaml` 當 source of truth，README 是 SEO 入口
   - 對使用者：**看目錄樹和 registry.yaml**，別太信任 README
   - 對貢獻者：新增 notebook 只要改 `registry.yaml` 和 `authors.yaml`

### 與其他筆記的關聯

| 相關筆記 | 關聯點 |
|---------|-------|
| [Claude Agent SDK](claude-agent-sdk.md) | `claude_agent_sdk/` 是該 SDK 的官方 tutorial |
| [Claude Use Cases Gallery](claude-use-cases.md) | Cookbooks 是「可執行版」的 use cases gallery |
| [Claude Skills Guide](claude-skills-guide.md) | `skills/` 是 Skills 系統的官方入門 |
| [Boris Cherny × Opus 4.7 心得](boris-cherny-opus-4-7.md) | CLAUDE.md 模型規範 + 4.7 行為差異兩份合看更完整 |
| [OpenAI Agent 建構指南](openai-practical-guide-building-agents.md) | `claude_agent_sdk/04_migrating_from_openai_agents_sdk` 與之直接對照 |
| [LangGraph Multi-Agent](langgraph-multi-agent.md) | `patterns/agents/orchestrator_workers` 是 LangGraph 類似模式的極簡官方版 |
| [Learn Claude Code](learn-claude-code.md) | Cookbook 是 Learn Claude Code 的進階續作 |
| [AI Engineering from Scratch](ai-engineering-from-scratch.md) | 兩者對照：from-scratch 是底層原理，cookbook 是高層 canonical 寫法 |

### 可直接抄的做法

```
追蹤 cookbook 的方式：
1. watch repo，但過濾到 registry.yaml 的 commit 即可
2. 每次看到新日期出現 → 對照資料夾結構找對應 notebook
3. 把 CLAUDE.md 的 Ruff 設定、Conventional Commits、模型 alias 規範抄到自己專案
4. 把 /notebook-review、/model-check、/link-review 三個 slash command 植入自己的 CI
```
