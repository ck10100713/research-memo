# Learn Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/shareAI-lab/learn-claude-code |
| 作者 | shareAI Lab (@baicai003) |
| 相關專案 | [Kode CLI](https://github.com/shareAI-lab/Kode), [Agent Skills Spec](https://agentskills.io/specification) |
| 授權 | MIT |

## 專案概述

Learn Claude Code 是一個教育性專案，透過從零開始建構 AI Agent 來教導現代 AI Agent 的運作原理。這個專案的核心理念是「Bash is all you & agent need」— 展示 AI coding agent 的核心其實非常簡單。

這個專案解決的問題是讓開發者理解「為什麼 Claude Code 這麼強大」。透過 5 個版本的漸進式學習（v0 到 v4），從最簡單的 50 行程式碼 Bash Agent 開始，逐步加入工具、規劃、子代理和技能系統。

適合場景：
- 想理解 AI Agent 運作原理的開發者
- 希望從零建構 Agent 的學習者
- 需要教學案例的 AI 教育者
- 想擴展 Claude Code/Kode CLI 功能的使用者

## 核心功能

1. **Agent Loop 核心模式**：展示所有 AI coding agent 的基本運作迴圈
2. **工具設計**：教導如何讓 AI 模型與真實世界互動
3. **顯式規劃**：使用約束讓 AI 行為可預測
4. **上下文管理**：透過子代理隔離保持 Agent 記憶乾淨
5. **知識注入**：無需重新訓練即可載入領域專業知識
6. **完整的學習路徑**：從 16 行到 550 行的漸進式學習

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                    學習路徑概覽                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                            │
│  │ v0: Bash     │ ────▶ "One tool is enough"                │
│  │ Agent        │       ~16-50 行，1 個工具                  │
│  │ (起點)       │       遞迴子代理                           │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                            │
│  │ v1: Basic    │ ────▶ "The complete agent pattern"        │
│  │ Agent        │       ~200 行，4 個工具                    │
│  │              │       bash, read, write, edit              │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                            │
│  │ v2: Todo     │ ────▶ "Make plans explicit"               │
│  │ Agent        │       ~300 行，+TodoManager                │
│  │              │       結構化規劃                           │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                            │
│  │ v3: Subagent │ ────▶ "Divide and conquer"                │
│  │              │       ~450 行，+Task tool                  │
│  │              │       上下文隔離                           │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                            │
│  │ v4: Skills   │ ────▶ "Domain expertise on-demand"        │
│  │ Agent        │       ~550 行，+Skill tool                 │
│  │ (終點)       │       SkillLoader                          │
│  └──────────────┘                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    核心 Agent Loop                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   while True:                                                │
│       response = model(messages, tools)                      │
│       if response.stop_reason != "tool_use":                 │
│           return response.text                               │
│       results = execute(response.tool_calls)                 │
│       messages.append(results)                               │
│                                                              │
│   # 就這樣。模型呼叫工具直到完成。                             │
│   # 其他所有東西都只是改進。                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 安裝方式

```bash
# 克隆專案
git clone https://github.com/shareAI-lab/learn-claude-code
cd learn-claude-code

# 安裝依賴
pip install -r requirements.txt

# 設定 API 金鑰
cp .env.example .env
# 編輯 .env 設定 ANTHROPIC_API_KEY
```

### 執行各版本

```bash
# v0: 最小化 Bash Agent（從這裡開始！）
python v0_bash_agent.py

# v1: 核心 Agent Loop
python v1_basic_agent.py

# v2: + Todo 規劃
python v2_todo_agent.py

# v3: + 子代理
python v3_subagent.py

# v4: + Skills
python v4_skills_agent.py
```

### 環境設定

```bash
# .env 檔案
ANTHROPIC_API_KEY=sk-ant-xxx      # 必要
ANTHROPIC_BASE_URL=https://...    # 可選：API 代理
MODEL_ID=claude-sonnet-4-5-20250929  # 可選：模型選擇
```

## 與其他教學資源的比較

| 特性 | Learn Claude Code | LangChain 教學 | AutoGPT 文件 |
|------|------------------|---------------|--------------|
| 學習曲線 | ✅ 極低（50行起步） | ⚠️ 中等 | ⚠️ 較陡 |
| 程式碼量 | ✅ 16-550 行 | ❌ 複雜框架 | ❌ 大型專案 |
| 核心原理 | ✅ 清晰展示 | ⚠️ 被框架包裝 | ⚠️ 被框架包裝 |
| 漸進學習 | ✅ 5 個版本 | ⚠️ 有限 | ❌ 無 |
| 生產就緒 | ⚠️ 教育為主 | ✅ 生產級 | ✅ 生產級 |

## 研究心得

Learn Claude Code 是目前最好的 AI Agent 原理教學資源之一，展示了「Model as Agent」的核心理念。

**核心洞見：**
1. **Agent 本質很簡單**：核心 loop 只有 5 行程式碼
2. **模型占 80%**：現代 agent 之所以強大是因為模型被訓練成 agent
3. **工程占 20%**：我們的工作是給模型工具，然後閃開

**學習價值：**
1. 從 v0 的 16 行程式碼理解 Agent 核心
2. 透過比較各版本理解工具、規劃、子代理的價值
3. 最終理解 Skills 機制如何提供領域專業知識

**對 Agent 開發的啟示：**
- 不要過度工程化，保持簡單
- 工具設計是關鍵（bash, read, write, edit 就夠了）
- 子代理用於上下文隔離，避免記憶污染
- Skills 用於注入領域知識，不需要微調模型

**中文資源價值：**
- 提供 README_zh.md 中文說明
- 對於中文開發者理解 Agent 原理非常有幫助

---
研究日期：2026-02-03
