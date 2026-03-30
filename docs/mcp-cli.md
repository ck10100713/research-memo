---
date: ""
category: "Coding Agent 工具"
card_icon: "material-connection"
oneliner: "Model Context Protocol CLI 工具"
---
# MCP CLI 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/chrishayuk/mcp-cli |
| PyPI | https://pypi.org/project/mcp-cli/ |
| 相關專案 | [CHUK Tool Processor](https://github.com/chrishayuk/chuk-tool-processor), [CHUK-LLM](https://github.com/chrishayuk/chuk-llm) |

## 專案概述

MCP CLI 是一個功能豐富的命令列介面工具，用於與 Model Context Protocol (MCP) 伺服器進行互動。它整合了 CHUK Tool Processor 和 CHUK-LLM，提供工具使用、對話管理和多種操作模式。

這個專案的核心價值在於讓開發者能夠透過統一的 CLI 介面，與各種 LLM 提供者（如 Ollama、OpenAI、Anthropic、Azure 等）進行互動，同時支援 MCP 伺服器提供的工具擴展功能。預設使用 Ollama 搭配 gpt-oss 推理模型，可在本地運行，無需 API 金鑰。

適合場景：
- 本地開發與測試 AI Agent 功能
- 與 MCP 伺服器整合的自動化腳本
- 多 LLM 提供者的統一存取介面
- 命令列驅動的 AI 輔助開發工作流程

## 核心功能

1. **多種操作模式**：Chat Mode（對話式）、Interactive Mode（命令驅動）、Command Mode（腳本自動化）
2. **串流回應**：即時回應生成與 UI 更新，支援推理過程可視化
3. **多 LLM 提供者支援**：Ollama、OpenAI (GPT-5)、Anthropic (Claude 4.5)、Azure、Gemini、Groq 等
4. **工具系統**：自動探索伺服器提供的工具，支援並行執行與中介軟體（重試、斷路器、限流）
5. **OAuth 認證**：完整的 OAuth 流程支援，包含多種 token 儲存後端
6. **跨平台支援**：Windows、macOS、Linux，具備平台特定最佳化
7. **主題系統**：8 種內建主題，包含 Markdown 渲染與語法高亮
8. **配置管理**：環境變數、YAML/JSON 配置檔、使用者偏好設定

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP CLI                               │
│              (命令協調與整合層 - 本專案)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Chat Mode  │  │ Interactive │  │ Command Mode│          │
│  │   (預設)    │  │    Mode     │  │  (腳本化)   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│               依賴的底層模組                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ CHUK Tool       │  │   CHUK-LLM      │  │ CHUK-Term   │  │
│  │ Processor       │  │                 │  │             │  │
│  │ ─────────────── │  │ ─────────────── │  │ ─────────── │  │
│  │ • 非同步工具執行 │  │ • 統一 LLM 介面 │  │ • 終端 UI   │  │
│  │ • 中介軟體      │  │ • 動態模型發現  │  │ • 主題系統  │  │
│  │ • 重試/斷路器   │  │ • llama.cpp     │  │ • 跨平台    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     MCP Server                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  server_config.json → SQLite / 自訂工具 / 其他服務       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**架構說明：**
- **MCP CLI**：最上層的命令協調層，提供使用者介面
- **三種模式**：Chat（自然語言對話）、Interactive（命令驅動）、Command（Unix 友善的腳本化）
- **CHUK 模組群**：Tool Processor 負責工具執行，LLM 負責模型整合，Term 負責終端 UI
- **MCP Server**：底層伺服器，透過配置檔定義可用工具

## 安裝與使用

### 安裝方式

```bash
# 使用 uvx（推薦）
uvx mcp-cli --help

# 使用 pip
pip install mcp-cli

# 從原始碼安裝
git clone https://github.com/chrishayuk/mcp-cli
cd mcp-cli
pip install -e "."
```

### 前置需求

```bash
# 安裝 Ollama（預設 LLM 提供者）
curl -fsSL https://ollama.ai/install.sh | sh

# 下載預設推理模型
ollama pull gpt-oss
```

### 基本使用範例

```bash
# 使用預設模式（Ollama/gpt-oss）
mcp-cli --server sqlite

# 切換到其他本地模型
mcp-cli --model llama3.3
mcp-cli --model qwen2.5-coder

# 使用雲端提供者（需要 API 金鑰）
mcp-cli --provider openai --model gpt-5
mcp-cli --provider anthropic --model claude-4-5-sonnet

# 命令模式（適合腳本）
mcp-cli cmd --server sqlite --prompt "分析資料" --input data.txt
```

### 環境變數配置

```bash
# 預設提供者設定
export LLM_PROVIDER=ollama
export LLM_MODEL=gpt-oss

# 雲端提供者 API 金鑰
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GEMINI_API_KEY=...

# 工具執行逾時設定
export MCP_TOOL_TIMEOUT=120
```

## 與其他工具的比較

| 特性 | MCP CLI | LangChain | GitHub Copilot CLI |
|------|---------|-----------|-------------------|
| MCP 協議支援 | ✅ 原生支援 | ❌ 需額外整合 | ❌ 不支援 |
| 本地 LLM 支援 | ✅ Ollama 預設 | ⚠️ 需配置 | ❌ 僅雲端 |
| 工具中介軟體 | ✅ 斷路器/重試 | ⚠️ 需自行實作 | ❌ 無 |
| 多提供者支援 | ✅ 8+ 提供者 | ✅ 多提供者 | ⚠️ 有限 |
| Unix 腳本整合 | ✅ Command Mode | ⚠️ 需開發 | ⚠️ 有限 |

## 研究心得

MCP CLI 是一個設計精良的 CLI 工具，特別適合需要與 MCP 伺服器互動的開發者。其模組化架構（分離為 CHUK Tool Processor、CHUK-LLM、CHUK-Term）展現了良好的軟體工程實踐。

**優點：**
1. 預設使用本地 Ollama，隱私保護且無需 API 費用
2. 多種操作模式滿足不同使用場景
3. 工具中介軟體提供生產級的可靠性

**觀察：**
1. 依賴多個 CHUK 系列套件，學習曲線較陡
2. 需要額外設定 MCP Server（server_config.json）
3. 文件豐富但分散在多個檔案中

**適用場景：**
- 開發 MCP 協議相關應用
- 需要本地 LLM + 工具整合的專案
- 建構 CLI 驅動的 AI Agent 工作流程

---
研究日期：2026-02-03
