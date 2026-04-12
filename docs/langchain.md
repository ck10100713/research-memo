---
date: "2026-03-23"
category: "AI Agent 框架"
card_icon: "material-link-variant"
oneliner: "LLM 應用開發框架"
---
# LangChain 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/langchain-ai/langchain |
| 官方文件 | https://docs.langchain.com |
| API 參考 | https://reference.langchain.com/python |
| 論壇 | https://forum.langchain.com |
| 學習資源 | https://academy.langchain.com |

## 專案概述

LangChain 是一個用於建構 AI Agent 和 LLM 驅動應用程式的框架。它幫助開發者串連可互通的元件和第三方整合，簡化 AI 應用程式開發，同時確保技術演進時決策的彈性。

### 解決的問題

- **即時資料增強**：輕鬆連接 LLM 到各種資料來源和內外部系統
- **模型互通性**：快速切換不同模型，適應產業前沿演進
- **快速原型開發**：模組化、元件式架構，加速開發週期
- **生產就緒功能**：內建監控、評估和除錯支援

## 技術架構

```
┌─────────────────────────────────────────────────────────────────┐
│                     LangChain 生態系統                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │   LangChain   │  │   LangGraph   │  │   LangSmith   │       │
│  │   (核心框架)   │  │ (Agent 編排)  │  │  (可觀測性)   │       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
│          │                  │                  │                │
│          └──────────────────┼──────────────────┘                │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────┐       │
│  │                    整合層 (Integrations)              │       │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │       │
│  │  │  模型   │ │ 向量庫  │ │  工具   │ │ 檢索器  │    │       │
│  │  │ Models  │ │ Vector  │ │ Tools   │ │Retrievers│   │       │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │                    應用層                            │       │
│  │  • Chains (鏈式調用)                                 │       │
│  │  • Agents (自主代理)                                 │       │
│  │  • RAG (檢索增強生成)                                │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 核心元件

1. **LangChain** - 核心框架，提供標準介面
2. **LangGraph** - 低階 Agent 編排框架，支援複雜工作流程
3. **LangSmith** - 評估和可觀測性工具
4. **Deep Agents** - 可規劃、使用子 Agent 的進階 Agent

## 安裝與使用

### 安裝

```bash
pip install langchain
```

### 基本使用範例

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 建立模型
llm = ChatOpenAI(model="gpt-4")

# 建立提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個有幫助的助手。"),
    ("user", "{input}")
])

# 建立鏈
chain = prompt | llm

# 執行
response = chain.invoke({"input": "什麼是 AI Agent？"})
print(response.content)
```

### Agent 範例

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# 定義工具
tools = [
    Tool(
        name="Search",
        func=lambda x: "搜尋結果...",
        description="用於搜尋資訊"
    )
]

# 建立 Agent
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 執行
result = agent_executor.invoke({"input": "搜尋最新的 AI 新聞"})
```

## 研究重點

### Agent 架構

- 使用 ReAct 模式（Reasoning + Acting）
- 支援多種 Agent 類型：OpenAI Functions、ReAct、Plan-and-Execute
- LangGraph 提供更細緻的控制和狀態管理

### Tool 定義方式

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """將兩個數字相乘"""
    return a * b
```

### 與其他工具整合

- 支援 100+ 種整合（模型、向量庫、工具）
- 可與 LangSmith 整合進行監控
- 支援 LangGraph 進行複雜工作流程

## 研究日期

2026-02-03
