---
date: "2026-03-31"
category: "學習資源"
card_icon: "material-school"
oneliner: "44K stars 的 Agent Harness 工程教科書——12 個漸進 Session 從 1 個 loop + Bash 到 worktree 隔離多 Agent 協作，附 Next.js 互動學習平台"
---
# Learn Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) |
| 作者 | shareAI-Lab (@baicai003) |
| 相關專案 | [Kode CLI](https://github.com/shareAI-lab/Kode-cli), [Kode Agent SDK](https://github.com/shareAI-lab/Kode-agent-sdk), [claw0](https://github.com/shareAI-lab/claw0) |
| 文件 | [English](https://github.com/shareAI-lab/learn-claude-code/tree/main/docs/en) / [中文](https://github.com/shareAI-lab/learn-claude-code/tree/main/docs/zh) / [日本語](https://github.com/shareAI-lab/learn-claude-code/tree/main/docs/ja) |
| 授權 | MIT |

## 專案概述

| 指標 | 數值 |
|------|------|
| Stars | **44,053** |
| Forks | 6,729 |
| 語言 | TypeScript (Web) + Python (Agents) |
| 建立日期 | 2025-06-29 |

Learn Claude Code 是目前 **GitHub 上最受歡迎的 AI Agent 教學專案**。核心理念：

> **The model IS the agent. The code IS the harness. Build great harnesses. The agent will do the rest.**

### 核心哲學：Harness Engineering

```
Agent = Model（已訓練好的 LLM）
Harness = Tools + Knowledge + Observation + Action + Permissions

你的工作不是「開發 Agent」，而是「建造 Harness」——
給模型工具、知識、觀察介面、行動能力和權限邊界，然後閃開。
```

這個專案**不是教你用框架**（LangChain, CrewAI），而是教你理解**為什麼 Claude Code 選擇不用框架**——因為 Agent 的核心只有一個 loop。

## 12 Session 學習路徑

```
Phase 1: THE LOOP              Phase 2: PLANNING & KNOWLEDGE
═══════════════════             ═══════════════════════════════
s01  Agent Loop         [1]     s03  TodoWrite              [5]
     while + stop_reason              規劃 + nag reminder
     │                                │
     └→ s02  Tool Use        [4]     s04  Subagents           [5]
              dispatch map               獨立 messages[] 隔離
                                         │
                                    s05  Skills               [5]
                                         SKILL.md via tool_result
                                         │
                                    s06  Context Compact       [5]
                                         三層壓縮策略

Phase 3: PERSISTENCE            Phase 4: TEAMS
═══════════════════             ═══════════════════════
s07  Tasks               [8]    s09  Agent Teams             [9]
     file-based CRUD + deps          teammates + JSONL mailboxes
     │                                │
s08  Background Tasks    [6]    s10  Team Protocols          [12]
     daemon threads + notify          shutdown + plan approval FSM
                                      │
                                 s11  Autonomous Agents       [14]
                                      idle cycle + auto-claim
                                      │
                                 s12  Worktree Isolation      [16]
                                      task coord + isolated lanes

                                 [N] = number of tools
```

### 每個 Session 的 Motto

| Session | 主題 | Motto |
|---------|------|-------|
| s01 | Agent Loop | *One loop & Bash is all you need* |
| s02 | Tool Use | *Adding a tool means adding one handler* |
| s03 | TodoWrite | *An agent without a plan drifts* |
| s04 | Subagents | *Break big tasks down; each subtask gets a clean context* |
| s05 | Skills | *Load knowledge when you need it, not upfront* |
| s06 | Context Compact | *Context will fill up; you need a way to make room* |
| s07 | Tasks | *Break big goals into small tasks, order them, persist to disk* |
| s08 | Background Tasks | *Run slow operations in the background; the agent keeps thinking* |
| s09 | Agent Teams | *When the task is too big for one, delegate to teammates* |
| s10 | Team Protocols | *Teammates need shared communication rules* |
| s11 | Autonomous Agents | *Teammates scan the board and claim tasks themselves* |
| s12 | Worktree Isolation | *Each works in its own directory, no interference* |

## 核心 Agent Loop（全部 12 Session 的不變基礎）

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return  # 模型決定停止

        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = TOOL_HANDLERS[block.name](**block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})
```

**每個 Session 只加一個 harness 機制，loop 本身永遠不變。**

## 專案結構

```
learn-claude-code/
├── agents/              # Python 實作（s01-s12 + s_full capstone）
├── docs/{en,zh,ja}/     # 三語文件
├── web/                 # Next.js 互動學習平台
├── skills/              # s05 的 Skill 檔案
└── .github/workflows/   # CI: typecheck + build
```

### 快速開始

```bash
git clone https://github.com/shareAI-lab/learn-claude-code
cd learn-claude-code
pip install -r requirements.txt
cp .env.example .env   # 設定 ANTHROPIC_API_KEY

python agents/s01_agent_loop.py        # 從這裡開始
python agents/s12_worktree_task_isolation.py  # 終點
python agents/s_full.py                # Capstone：所有機制合一
```

## 目前限制 / 注意事項

- **教學為主，非生產級**：刻意簡化了 event bus、permission governance、session lifecycle 等
- **Team JSONL mailbox 是教學實作**：不代表 Claude Code 的實際內部機制
- **需要 Anthropic API Key**：無法用本地模型
- **Scope 聲明明確**：README 清楚列出刻意省略的生產級功能

## 研究價值與啟示

### 關鍵洞察

1. **「Model IS the Agent」是這個時代最重要的認知轉換**：從 DQN 到 AlphaStar 到 LLM，agent 永遠是模型本身。框架和 pipeline 不是 agent，它們是 harness。大量「no-code AI agent platform」本質上是帶 LLM 的 Rube Goldberg machine。

2. **12 Session 的設計是教學天才**：每個 session 只加一個概念，loop 不變。這讓學習者清楚看到「哪些是 Agent 核心（loop），哪些是 Harness 擴展（其他一切）」。

3. **Sub Agent 的真正價值是 Context 衛生**（s04）：不是為了並行或分工，而是為了隔離 dirty context。搜尋 10 個檔案只為找一個函式——9 個無用結果不該污染 main context。

4. **Skills = Knowledge on demand**（s05）：不在 system prompt 塞所有知識，而是讓模型需要時才載入。這是 RAG 的 Agent 版本。

5. **從 s09 到 s12 的團隊演進**：s09 引入 teammates，s10 加協議，s11 讓 agent 自主認領任務，s12 用 worktree 隔離。這四步精確對應了 Claude Code 從單 agent 到 multi-agent 的演進。

### 與其他專案的關聯

- **analysis_claude_code**（`docs/analysis-claude-code.md`）：同一作者（ShareAI-Lab），analysis 是「拆解 Claude Code」，learn 是「從零重建」
- **claude-code-reverse**（`docs/claude-code-reverse.md`）：Runtime 逆向方法，與 learn 的「正向建構」互補
- **cloclo**（`docs/claude-code-sdk.md`）：learn 教原理，cloclo 給你一個可用的多 Provider 實作
- **LangChain**（`docs/langchain.md`）：learn 的立場是「框架隱藏了 Agent 的本質」，與 LangChain 的框架化路線形成對比
