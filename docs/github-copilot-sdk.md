# GitHub Copilot SDK 研究筆記

## 資料來源

| 來源 | 連結 | 說明 |
|------|------|------|
| 官方儲存庫 | https://github.com/github/copilot-sdk | 主要程式碼與文件 |
| Python SDK | https://github.com/github/copilot-sdk/tree/main/python | Python 專屬文件 |
| 入門指南 | https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md | 官方教學 |
| 官方部落格 | https://github.blog/news-insights/company-news/build-an-agent-into-any-app-with-the-github-copilot-sdk/ | SDK 發布公告 |
| Microsoft 教學 | https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-agents-with-github-copilot-sdk-a-practical-guide-to-automated-tech-upda/4488948 | 實戰應用案例 |

## 專案概述

GitHub Copilot SDK 是 GitHub 官方發布的多平台 SDK（目前為**技術預覽版**），讓開發者能夠將 AI Agent 工作流程嵌入到任何應用程式中。它提供了與 Copilot CLI 相同的生產級 Agent 執行引擎。

### 核心價值

- **無需自建編排系統**：直接使用 GitHub 的生產級 Agent Runtime
- **多語言支援**：Node.js、Python、Go、.NET
- **彈性模型選擇**：支援 BYOK（Bring Your Own Key）

## 主要功能

| 功能 | 說明 |
|------|------|
| 智能規劃 | Agent 自動進行多步驟任務規劃與決策 |
| 工具調用 | 支援檔案系統、Git 操作、網路請求等工具 |
| 程式碼編輯 | 直接進行檔案修改 |
| 即時串流 | 支援 streaming 漸進式回應 |
| MCP 整合 | 支援 Model Context Protocol 伺服器 |
| 自訂擴展 | 可定義自訂 Agent、技能和工具 |
| 多模型支援 | 相容多種 AI 模型 |
| BYOK 支援 | 可使用自帶 API 金鑰（OpenAI、Azure、Anthropic、Ollama 等） |

## 架構說明

```
┌─────────────────┐
│   應用程式       │
└────────┬────────┘
         │ JSON-RPC
┌────────▼────────┐
│  Copilot SDK    │
│  (Python/TS/Go) │
└────────┬────────┘
         │ stdio/TCP
┌────────▼────────┐
│  Copilot CLI    │
│  (Agent Runtime)│
└────────┬────────┘
         │
┌────────▼────────┐
│   AI Models     │
│ (GPT/Claude/...) │
└─────────────────┘
```

### 通訊協定

- SDK 透過 **JSON-RPC** 與 Copilot CLI 通訊
- 支援 **stdio** 和 **TCP** 兩種傳輸方式
- SDK 自動管理 CLI 程序的生命週期

## Python SDK 詳細說明

### 安裝需求

- Python 3.8+
- GitHub Copilot CLI 已安裝並認證
- GitHub Copilot 訂閱（或使用 BYOK）

### 安裝指令

```bash
pip install github-copilot-sdk
```

### CopilotClient 設定選項

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `cli_path` | CLI 執行檔路徑 | "copilot" |
| `cli_url` | 連接現有伺服器 | None |
| `port` | TCP 模式端口 | None |
| `use_stdio` | 使用 stdio 傳輸 | True |
| `log_level` | 日誌等級 | "info" |
| `auto_start` | 自動啟動伺服器 | True |
| `auto_restart` | 崩潰時自動重啟 | True |
| `github_token` | GitHub 認證 Token | None |
| `use_logged_in_user` | 使用系統憑證 | True |

### Session 設定選項

| 參數 | 說明 |
|------|------|
| `model` | 模型識別碼（BYOK 時必填） |
| `reasoning_effort` | 推理模型的努力程度 |
| `streaming` | 啟用漸進式回應 |
| `tools` | 自訂工具列表 |
| `system_message` | 自訂系統提示 |
| `infinite_sessions` | Context 管理設定 |
| `on_user_input_request` | Agent 請求輸入時的處理器 |
| `hooks` | 生命週期事件處理器 |
| `provider` | 自訂 API Provider 設定 |

### 事件類型

| 事件 | 說明 |
|------|------|
| `assistant.message` | 完整訊息回應 |
| `assistant.message_delta` | 串流訊息片段 |
| `assistant.reasoning_delta` | 推理過程片段 |
| `session.idle` | Session 閒置（可發送下一個請求） |

## Cookbook 範例主題

官方 Cookbook 包含以下實用範例：

1. **Error Handling** - 錯誤處理最佳實踐
2. **Multiple Sessions** - 多會話管理
3. **Managing Local Files** - 本地檔案操作
4. **PR Visualization** - Pull Request 視覺化
5. **Persisting Sessions** - 跨重啟持久化會話

## 實際應用案例

根據官方部落格，開發者已使用 SDK 建構：

- YouTube 章節產生器
- 自訂 Agent GUI
- 語音轉指令工作流程
- AI 競賽遊戲

## 範例專案

本資料夾的 `examples/` 目錄包含以下範例：

| 檔案 | 說明 | 難度 |
|------|------|------|
| `01_basic_chat.py` | 基本對話範例 | ⭐ 入門 |
| `02_streaming.py` | 串流回應範例 | ⭐ 入門 |
| `03_custom_tool.py` | 自訂工具範例（使用 Pydantic） | ⭐⭐ 基礎 |
| `04_byok_ollama.py` | 使用本地 Ollama / 自訂 Provider | ⭐⭐ 基礎 |
| `05_image_attachment.py` | 圖片附件與視覺分析 | ⭐⭐ 基礎 |
| `06_hooks_and_permissions.py` | Hooks 與權限控制 | ⭐⭐⭐ 進階 |
| `07_user_input_handler.py` | 使用者輸入處理 | ⭐⭐⭐ 進階 |
| `08_multi_session.py` | 多 Session 管理與 Session 池 | ⭐⭐⭐ 進階 |

### 執行範例

```bash
cd examples
pip install -r requirements.txt
python 01_basic_chat.py
```

## 注意事項

⚠️ **技術預覽版**：此 SDK 目前處於技術預覽階段，API 可能會有破壞性變更。

## 研究日期

2026-02-03
