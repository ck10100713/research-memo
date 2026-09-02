---
date: "2026-08-07"
category: "AI Agent 框架"
card_icon: "material-book-open-variant"
oneliner: "O'Reilly《Building Applications with AI Agents》書籍配套碼:把「同一批企業場景」用 LangGraph / LangChain / Autogen / OpenAI 四種框架平行實作,再套上共用評測（LLM judge + drift 偵測）、可觀測性（Loki + Tempo）、fine-tuning（SFT/DPO/RLVR/GRPO）與三種分散式多 agent runtime（Ray / Redis Streams / Temporal）"
tags:
  - agent-framework
  - multi-agent
  - learning
  - mcp
  - llm-training
---

# Building Applications with AI Agents 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/michaelalbada/BuildingApplicationsWithAIAgents> |
| 作者 | Michael Albada（`michaelalbada`） |
| 配套書籍 | [Building Applications with AI Agents: Designing and Implementing Multi-Agent Systems](https://www.oreilly.com/library/view/building-applications-with/9781098176495/)（O'Reilly, ISBN 9781098176495） |

> Metadata（研究當下 2026-08-07）:**509 stars / 184 forks** · Python · **無 LICENSE 檔**(預設保留所有權利,商用/再散布前需先確認) · 最後 commit **2025-10-28**(最新 PR:`skill_selection_fine_tuning`) · 107 commits。

## 專案概述

這是 O'Reilly 書籍**《Building Applications with AI Agents》**的官方配套程式碼。它不是又一個「agent 框架」,而是一個**跨框架的參考實作平台**——核心設計理念是**把「場景定義」和「框架實作」拆開**:

- **一份場景 spec**（企業客服、IT help desk、金融、醫療、法務、SOC、供應鏈…)
- **多框架平行實作**(LangGraph / LangChain / Autogen / OpenAI 各做一遍)
- **一套共用評測 harness**,可跨框架比對輸出品質

它的價值在於**覆蓋了 production multi-agent 的完整生命週期**:設計 → 多框架實作 → 分散式編排 → 評測 → 可觀測性 → fine-tuning。README 只描述了理想化的資料夾結構,**實際 `src/` 內容比 README 豐富得多**(以下以實際程式碼為準)。

!!! note "定位對照"
    和站上 [AI Agents（黃佳）](ai-agents.md)、[AI Agents for Beginners](ai-agents-for-beginners.md) 這類**入門書配套碼**不同,本專案偏向 **production 工程參考**:重點在評測、可觀測性、分散式編排與模型微調,適合已經會寫單一 agent、想把它推上線的工程師。多 agent 編排部分可與 [LangGraph Multi-Agent](langgraph-multi-agent.md)、[qm](qm.md) 交叉參考。

## 六大支柱

### 1. 多框架平行實作（同場景、不同引擎）

`src/frameworks/` 下同一批場景用四種技術各實作一次,方便直接比較:

| 框架 | 內容 |
|------|------|
| **LangGraph**（`langgraph_agents/`,~2,930 LOC,最重) | 六大企業領域 agent:ecommerce 客服、financial services、healthcare 病患分流、IT help desk、legal 文件審閱、SOC 分析師;外加 reflexion、experiential learning、短期/語意記憶、MCP client、供應鏈多 agent |
| **LangChain**（~614 LOC) | tool use 範例(計算機、股價、Wikipedia)+ **三種 skill/tool selection 策略** |
| **Autogen**（~160 LOC) | MCP client、計算機 tool use、web surfer agent |
| **OpenAI**（~590 LOC) | **ADAS**（自動化 agentic 系統設計)、realtime 語音 agent |

### 2. 評測 harness（`src/common/evaluation/`)

這是本專案最實用的部分之一——把「agent 好不好」變成可量測:

- **`ai_judge.py`** — LLM-as-Judge,**支援有/無參考答案兩種模式**。用 rubric 對 `accuracy`（需 reference)、`coherence`、`clarity` 各打 0–1 分,可加權彙總;有 API 與 CLI 兩種介面。
- **`memory_evaluation.py`** — 針對 agent 記憶做 **precision / recall / F1**:分別評「記憶更新」是否命中預期,以及「記憶檢索」的召回品質。
- **`distribution_shifts.py`** — **資料漂移偵測**:KS 檢定(數值特徵,如 query 長度)+ KL divergence(token 分佈),用來抓 concept drift / 語言切換。
- **`batch_evaluation.py` + `metrics.py`** — 批次跑整個 eval set 並彙總指標。
- **`scenarios/*.jsonl`** — 七~八個領域的 gold evaluation set(ecommerce 客服、金融帳戶管理、醫療分流、IT help desk、法務文件審閱、SOC 分析師、供應鏈單/多 agent)。

### 3. 分散式多 agent 編排(本專案的招牌)

`langgraph_agents/supply_chain/` 把**同一個供應鏈多 agent 系統(庫存/物流/供應商/倉儲四個 specialist + supervisor)用三種分散式 runtime 各實作一遍**,直接示範 production 級 scaling 的取捨:

| Runtime | 做法 | 適用情境 |
|---------|------|---------|
| **Ray**（actor) | 每個 specialist 是 Ray actor,**per-session 隔離**(以 `operation_id` 區分),每個 session 有自己的 actor 實例、狀態隔離、序列化執行 | 需要平行 + 狀態隔離 |
| **Redis Streams** | supervisor 把任務發到共用 stream,specialists **非同步消費**、把結果發回另一條 stream(pub/sub 解耦) | 事件驅動、鬆耦合 |
| **Temporal** | 用 Temporal workflow 做**耐久編排**:自動 retry、持久化狀態、失敗恢復 | 長時間執行、需容錯的流程 |

這種「同一問題、三種基礎設施」的對照,在教學型 repo 裡相當少見。

### 4. 可觀測性（`src/common/observability/`)

一整套本地 Grafana 觀測 stack(附 `docker-compose.yaml`):

- **Loki**（`loki_logger.py`)— 結構化 log 推到 `localhost:3100`,配 promtail。
- **OpenTelemetry / Tempo**（`instrument_tempo.py`)— OTLP exporter,parent/child span 追蹤 agent 執行,推到 `localhost:3200`。

### 5. Fine-tuning(`src/fine_tuning/`,~1,494 LOC,最新加入)

以 **IT help desk function-calling** 為題,把主流微調法各做一遍:

- **SFT** — supervised fine-tuning。
- **DPO**（`direct_preference_optimization.py`)— Phi-3-mini + **LoRA + 4-bit 量化**(bitsandbytes)。
- **RLVR**(`reinforcement_learning_with_verifiable_rewards.py`)— 用 **GRPO** + **可驗證獎勵**:針對 tool call 品質給分梯度(正確 tool 名 + 合法 JSON + 必填參數 = +1.0;缺參數 +0.5;JSON 非法 +0.2;錯 tool -0.3;沒呼叫 -1.0)。
- **Production GRPO**（`skill_selection_fine_tuning/grpo_production.py`)— 在完整 Glaive function-calling 資料集上訓 Qwen2-0.5B,含 wandb 監控、8-bit AdamW、驗證切分,附 `run_jobs.sh` / `env_setup.sh`。

### 6. 協定與基礎設施

- **MCP servers**（`src/common/mcp/`)— FastAPI 實作的 math server 與 weather server,示範 Model Context Protocol 端點;各框架都有對應的 MCP client。
- **A2A**（`src/common/a2a/`)— Agent-to-Agent 協定:`agent_server.py` 提供 **Agent Card**(`/.well-known/agent.json` 描述 identity / capabilities / schemas / endpoint / auth),`agent_client.py` 做發現與呼叫。
- **GraphRAG**（`graph_rag.py`)— networkx + `cdlib` 社群偵測 + OpenAI,做 graph-based RAG。
- **Skill / tool selection**(`langchain/`)— 當工具數量變多時如何選對工具:**semantic**(FAISS embedding 相似度)、**embedding-based**、**hierarchical**(先選 tool group 再選 tool)三種策略。
- **Agent 學習模式** — **Reflexion**(從失敗經驗反思、產出新計畫)、**Experiential Learning**(`InsightAgent`,對 insight 做 promote/demote)。

## 技術棧與版本

`requirements.txt` 釘在**較舊的版本**:`langchain==0.1.20`、`langchain-openai==0.1.4`、`langgraph==0.0.28`(2024 年份的 API,與現行 LangGraph 差異大)。fine-tuning 另用 `transformers` / `trl`(GRPO/DPO)/ `peft`(LoRA)/ `bitsandbytes`(量化)/ `datasets` / `wandb`。分散式部分需 `ray` / `redis` / `temporalio`。評測用 `scipy` / `scikit-learn` / `numpy`。

環境檔有兩份:`environment.yml`(主環境)與 `langgraph_env.yml`。測試用 pytest(`tests/` 下涵蓋 ai_judge、memory evaluation、langgraph 客服 agent、observability)。

## 誰該看這個 repo

| 適合 | 理由 |
|------|------|
| 想比較 LangGraph / LangChain / Autogen / OpenAI 差異的工程師 | 同場景平行實作,直接對照寫法 |
| 要把 multi-agent 推上 production 的人 | Ray / Redis / Temporal 三種分散式編排 + Grafana 觀測 stack 是現成範本 |
| 需要「agent 評測」方法論的團隊 | LLM-as-Judge、記憶 P/R/F1、資料漂移偵測都有可用實作 |
| 想微調小模型做 function calling 的人 | SFT→DPO→RLVR→GRPO 一條龍,含可驗證獎勵設計 |

## 注意事項

- **無授權條款**:repo 未附 LICENSE,依 GitHub 預設為「保留所有權利」。作為學習/內部參考沒問題,但**商用、再散布或大段複製前務必先向作者確認授權**。
- **依賴版本偏舊**:LangGraph/LangChain 釘在 2024 年的版本,照抄到新專案前要留意 API 變動。
- **README 與實作有落差**:README 描述的資料夾結構(`scenarios/<name>/spec.md` 等)是理想化版本,實際場景 spec 以 `evaluation/scenarios/*.jsonl` 與各框架目錄為準。
- 大量範例需要 `OPENAI_API_KEY`;分散式範例還需自架 Ray / Redis / Temporal 服務。

## 一句話總結

> 一本 O'Reilly 書的配套碼,難得地把 production multi-agent 的**六個面向(多框架、評測、分散式編排、可觀測性、fine-tuning、協定)**都用可跑的程式碼收在同一個 repo——最大看點是「**同一個供應鏈多 agent,用 Ray / Redis Streams / Temporal 各寫一遍**」的分散式對照。
