---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-refresh"
oneliner: "保哥的 Ralph 迭代式 AI 開發迴圈工具 — 基於 Copilot SDK，讓 AI 反覆執行任務直到完成"
---

# Copilot Ralph 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub 儲存庫 | [github.com/doggy8088/copilot-ralph](https://github.com/doggy8088/copilot-ralph) |
| npm 套件 | [npmjs.com/package/@willh/copilot-ralph](https://www.npmjs.com/package/@willh/copilot-ralph) |
| 運作流程詳解 | `docs/運作流程詳解.md`（repo 內） |
| 保哥部落格 | [blog.miniasp.com](https://blog.miniasp.com/) |

**GitHub 數據**：194 stars、TypeScript、最後更新 2026-03-28

## 專案概述

**Copilot Ralph** 是由保哥（Will 保哥, doggy8088）開發的 Node.js CLI 工具，名稱來自《乃乃家族》的角色 Ralph Wiggum，實作了一種「**自我參照式 AI 開發迴圈**」——讓 AI 依照同一個任務反覆迭代，直到偵測到完成短語、達到最大迭代次數、或超過時間限制。

核心設計理念：**不是一次性給 AI 指令，而是讓 AI 持續自主迭代修正**，類似 TDD 的紅-綠-重構循環，但由 AI 自動驅動。

Copilot Ralph 建構在 [GitHub Copilot SDK](github-copilot-sdk.md) 之上，是 Copilot SDK 的一個高品質應用範例。

## 技術架構

```
┌─────────────────────────────────────────────────────────┐
│                    Copilot Ralph CLI                      │
│                   (src/cli-entry.ts)                      │
├─────────────────────────────────────────────────────────┤
│  ┌───────────┐   ┌───────────┐   ┌───────────────┐      │
│  │ Commander  │──▶│LoopConfig │──▶│  LoopEngine   │      │
│  │ (參數解析) │   │ (設定組裝) │   │  (迴圈引擎)   │      │
│  └───────────┘   └───────────┘   └───────┬───────┘      │
│                                          │               │
│  ┌───────────┐   ┌───────────┐   ┌───────▼───────┐      │
│  │TUI Output │◀──│AsyncQueue │◀──│  Copilot SDK  │      │
│  │ (終端輸出) │   │ (事件佇列) │   │  (AI 互動)    │      │
│  └───────────┘   └───────────┘   └───────────────┘      │
├─────────────────────────────────────────────────────────┤
│  Copilot SDK  →  Copilot CLI (Server)  →  AI Models     │
└─────────────────────────────────────────────────────────┘
```

### 核心檔案結構

```
src/
├── cli-entry.ts              # CLI 入口點
├── cli/commands/             # CLI 指令定義
├── core/
│   ├── loop-engine.ts        # 核心迴圈引擎
│   ├── loop-config.ts        # 設定結構
│   └── completion-detector.ts # 完成偵測器
├── sdk/
│   └── copilot-client.ts     # Copilot SDK 封裝
├── tui/
│   └── display-events.ts     # 終端輸出處理
└── utils/
    └── async-queue.ts        # 非同步事件佇列
```

## 安裝

### 獨立可執行檔（免安裝 Node/Bun）

```bash
# macOS Apple Silicon
curl -L -o copilot-ralph https://github.com/doggy8088/copilot-ralph/releases/latest/download/copilot-ralph-macos-arm64
chmod +x copilot-ralph
sudo mv copilot-ralph /usr/local/bin/

# macOS Intel
curl -L -o copilot-ralph https://github.com/doggy8088/copilot-ralph/releases/latest/download/copilot-ralph-macos-x64

# Linux x64
curl -L -o copilot-ralph https://github.com/doggy8088/copilot-ralph/releases/latest/download/copilot-ralph-linux-x64
```

### npm 全域安裝

```bash
npm i -g @willh/copilot-ralph
```

**前置需求**：Node.js 18+、GitHub Copilot CLI 已安裝、有效的 Copilot 訂閱（或 BYOK）

## 運作流程

```
┌────────────────────────────────────────────────┐
│                 LoopEngine                      │
├────────────────────────────────────────────────┤
│  while (未完成 && 未超時 && 未達上限) {         │
│    1. 發送 prompt 到 Copilot SDK               │
│    2. 監聽事件串流（文字、工具呼叫、錯誤）     │
│    3. 即時輸出到終端 (TUI)                     │
│    4. 偵測完成短語 <promise>...</promise>       │
│  }                                              │
│  輸出摘要 + 退出碼                              │
└────────────────────────────────────────────────┘
```

### 完成偵測

AI 回應中必須精確包含：

```
<promise>任務完成！🥇</promise>
```

可透過 `--promise` 自訂短語。大小寫與字元必須完全一致。

## CLI 使用方式

### 基本指令

```bash
copilot-ralph run "請建立一個 Hello World 程式"
copilot-ralph run ./prompts/my-task.md   # 從檔案讀取 prompt
```

### 完整參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--max-iterations` | 最大迭代次數 | `10` |
| `--timeout` | 執行時限 | `30m` |
| `--promise` | 完成判定短語 | `任務完成！🥇` |
| `--model` | 使用的模型 | `gpt-5-mini` |
| `--working-dir` | 工作目錄 | `.` |
| `--streaming` | 是否串流 | `true` |
| `--system-prompt` | 自訂系統提示（文字/Markdown/.txt） | — |
| `--system-prompt-file` | 系統提示模板檔案（支援 `{{PROMISE}}`） | — |
| `--system-prompt-mode` | `append` 或 `replace` | — |
| `--session-id` | 延續上次 session 上下文 | — |
| `--dry-run` | 僅顯示設定，不執行 | — |
| `--log-level` | `debug`/`info`/`warn`/`error` | — |

### 退出狀態碼

| 碼 | 說明 |
|----|------|
| `0` | 成功（偵測到完成短語） |
| `1` | 失敗（執行錯誤） |
| `2` | 取消（使用者中斷） |
| `3` | 超時 |
| `4` | 達到最大迭代次數 |

## BYOK（自帶金鑰）多 Provider 支援

Copilot Ralph 支援四種 AI Provider，不一定要有 GitHub Copilot 訂閱：

### CLI 用法

=== "Azure OpenAI"

    ```bash
    export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
    export AZURE_OPENAI_API_KEY="your-api-key"
    copilot-ralph run --model your-deployment-name "請幫我加上單元測試"
    ```

=== "OpenAI"

    ```bash
    copilot-ralph run \
      --openai-base-url "https://api.openai.com/v1" \
      --openai-api-key "sk-..." \
      --model gpt-4o \
      "你的任務"
    ```

=== "Anthropic"

    透過 SDK 程式碼用法支援（見下方）

=== "Ollama（本地）"

    ```bash
    copilot-ralph run \
      --openai-base-url "http://localhost:11434/v1" \
      --model "llama3.2" \
      "你的任務"
    ```

### SDK 程式碼用法

Copilot Ralph 也可作為 SDK 在程式碼中使用：

```typescript
import { newCopilotClient, withModel, withProvider } from "@willh/copilot-ralph";

// Azure OpenAI
const azureClient = newCopilotClient(
  withModel("your-deployment-name"),
  withProvider({
    type: "azure",
    baseUrl: "https://your-resource.openai.azure.com/",
    apiKey: "your-api-key",
    wireApi: "completions",  // 或 "responses"
    azure: { apiVersion: "2024-10-21" }
  })
);

// OpenAI
const openaiClient = newCopilotClient(
  withModel("gpt-4o"),
  withProvider({
    type: "openai",
    baseUrl: "https://api.openai.com/v1",
    apiKey: "sk-your-key"
  })
);

// Anthropic
const anthropicClient = newCopilotClient(
  withModel("claude-sonnet-4-20250514"),
  withProvider({
    type: "anthropic",
    baseUrl: "https://api.anthropic.com",
    apiKey: "your-anthropic-key"
  })
);

// Ollama（本地，apiKey 可省略）
const ollamaClient = newCopilotClient(
  withModel("llama3.2"),
  withProvider({
    type: "openai",
    baseUrl: "http://localhost:11434/v1"
  })
);
```

### ProviderConfig 完整參數

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `type` | `"openai"` \| `"azure"` \| `"anthropic"` | 否 | Provider 類型，預設 `"openai"` |
| `baseUrl` | `string` | 是 | API 端點 URL |
| `apiKey` | `string` | 否 | API 金鑰（本地模型可省略） |
| `bearerToken` | `string` | 否 | Bearer Token，優先於 `apiKey` |
| `wireApi` | `"completions"` \| `"responses"` | 否 | API 格式，預設 `"completions"` |
| `azure.apiVersion` | `string` | 否 | Azure API 版本，預設 `"2024-10-21"` |

### 環境變數對照

| 環境變數 | CLI 參數 | 說明 |
|----------|----------|------|
| `AZURE_OPENAI_ENDPOINT` | `--azure-endpoint` | Azure 端點 URL |
| `AZURE_OPENAI_API_KEY` | `--azure-api-key` | Azure API 金鑰 |
| `AZURE_OPENAI_API_VERSION` | `--azure-api-version` | API 版本 |
| `AZURE_OPENAI_WIRE_API` | `--azure-wire-api` | `completions` 或 `responses` |

## 與 Copilot SDK 的關係

```
┌─────────────────────────────────┐
│       Copilot Ralph             │  ← 應用層（迴圈引擎 + TUI）
├─────────────────────────────────┤
│     @github/copilot-sdk         │  ← SDK 層（JSON-RPC client）
├─────────────────────────────────┤
│       Copilot CLI               │  ← Runtime 層（Agent 引擎）
├─────────────────────────────────┤
│   AI Models (GPT/Claude/...)    │  ← 模型層
└─────────────────────────────────┘
```

## 目前限制 / 注意事項

- **依賴 Copilot CLI**：底層需要已安裝的 Copilot CLI 作為 Agent Runtime
- **完成偵測機制依賴 LLM 配合**：如果 LLM 不按格式輸出 `<promise>...</promise>`，可能永遠無法觸發完成
- **macOS Gatekeeper**：獨立執行檔可能被系統阻擋，需手動移除 quarantine 屬性
- **Session 延續**：`--session-id` 可跨次執行延續上下文，但前提是 Copilot CLI 的 session 仍存在

## 研究價值與啟示

### 關鍵洞察

1. **「迭代式 AI 迴圈」是簡單但有效的 Agent 模式**——不需要複雜的多 Agent 架構，只要一個迴圈 + 完成偵測，就能讓 AI 自主修正直到任務完成。這個模式已被多個專案獨立發現和實作（Copilot Ralph、superpowers 的 ralph-loop skill），說明它是一個基礎的 Agent 設計原語。

2. **`<promise>` 完成偵測是巧妙的設計**——用特定格式的 XML tag 作為 AI 自我宣告完成的信號，比分析 AI 回覆的語義來判斷「是否完成」更可靠。這個 pattern 值得在其他 Agent 專案中借用。

3. **BYOK 多 Provider 支援大幅擴展了適用範圍**——原本只能用 GitHub Copilot，現在支援 Azure OpenAI、OpenAI、Anthropic、Ollama。特別是 Azure OpenAI 的支援（包括 Completions 和 Responses 兩種 API 格式），讓企業環境可以直接使用。

4. **SDK 程式碼用法讓 Ralph 不只是 CLI**——`newCopilotClient` + `withProvider` 的 functional options 模式讓 Ralph 可以嵌入其他 TypeScript 應用中，變成一個可程式化的迭代執行引擎。

5. **跨平台獨立可執行檔降低採用門檻**——提供 macOS（ARM/x64）、Linux、Windows 的獨立執行檔，不需要 Node.js 環境。這對 DevOps/CI/CD 場景特別有價值。

### 與其他專案的關聯

- **基於 [GitHub Copilot SDK](github-copilot-sdk.md)**：Ralph 是 Copilot SDK 最成熟的第三方應用範例
- **vs [Superpowers ralph-loop skill](superpowers.md)**：Superpowers 的 ralph-loop 是 Claude Code 內建的類似概念，但 Copilot Ralph 是獨立的 CLI 工具，支援更多 Provider
- **靈感來源相同**：Ralph Wiggum 迴圈概念已成為 AI Agent 社群的通用模式，多個專案獨立實作
