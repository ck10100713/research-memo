---
date: ""
category: "Coding Agent 工具"
icon: "material-refresh"
oneliner: "Copilot Ralph 自主迭代開發模式"
---
# Copilot Ralph 研究筆記

## 資料來源

| 來源 | 連結 | 說明 |
|------|------|------|
| 官方儲存庫 | https://github.com/doggy8088/copilot-ralph | 主要程式碼 |
| 運作流程文件 | `docs/運作流程詳解.md` | 詳細架構說明 |
| npm 套件 | https://www.npmjs.com/package/@willh/copilot-ralph | npm 發布 |

## 專案概述

**Copilot Ralph** 是由保哥（Will 保哥）開發的 Node.js CLI 工具，名稱來自《乃乃家族》的角色 Ralph Wiggum，實作了一種「自我參照式 AI 開發迴圈」技術。

### 核心概念

讓 AI 依照同一個任務**反覆迭代**，直到：
1. 達成完成條件（偵測到完成短語）
2. 達到最大迭代次數
3. 超過時間限制

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                     Copilot Ralph CLI                        │
│                    (src/cli-entry.ts)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ Commander   │───▶│ LoopConfig  │───▶│ LoopEngine  │      │
│  │ (參數解析)   │    │ (設定組裝)   │    │ (迴圈引擎)  │      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘      │
│                                               │              │
│  ┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐      │
│  │ TUI Output  │◀───│ AsyncQueue  │◀───│ Copilot SDK │      │
│  │ (終端輸出)   │    │ (事件佇列)   │    │ (AI 互動)   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 核心檔案結構

```
src/
├── cli-entry.ts          # CLI 入口點
├── cli/
│   └── commands/         # CLI 指令定義
├── core/
│   ├── loop-engine.ts    # 核心迴圈引擎
│   ├── loop-config.ts    # 設定結構
│   └── completion-detector.ts  # 完成偵測器
├── sdk/
│   └── copilot-client.ts # Copilot SDK 封裝
├── tui/
│   └── display-events.ts # 終端輸出處理
└── utils/
    └── async-queue.ts    # 非同步事件佇列
```

## 運作流程

### 1. 參數解析階段
```
copilot-ralph run "任務描述" --max-iterations 5
                    │
                    ▼
            ┌───────────────┐
            │ createRunCommand() │
            │ 解析 CLI 參數      │
            └───────────────┘
```

### 2. Prompt 組裝階段
- `resolvePrompt()`: 判斷輸入是檔案路徑還是字串
- `buildSystemPrompt()`: 組裝 System Prompt

### 3. 迴圈執行階段
```
┌────────────────────────────────────────┐
│            LoopEngine                   │
├────────────────────────────────────────┤
│  while (未完成 && 未超時 && 未達上限)   │
│  {                                      │
│    1. 發送 prompt 到 Copilot SDK       │
│    2. 監聽事件串流                      │
│    3. 即時輸出到終端                    │
│    4. 偵測完成短語                      │
│  }                                      │
└────────────────────────────────────────┘
```

### 4. 完成偵測
偵測 AI 回應中是否包含：
```
<promise>任務完成！🥇</promise>
```
（大小寫敏感）

## CLI 使用方式

### 基本指令
```bash
copilot-ralph run "請建立一個 Hello World 程式"
```

### 完整參數
```bash
copilot-ralph run "任務描述" \
  --max-iterations 10 \        # 最大迭代次數（預設 10）
  --timeout 30m \              # 執行時限（預設 30 分鐘）
  --promise "完成！" \          # 完成判定短語
  --model gpt-5 \              # 使用的模型
  --system-prompt "你是..." \  # 自訂 System Prompt
  --no-color                   # 關閉彩色輸出
```

### 使用 Prompt 檔案
```bash
copilot-ralph run ./prompts/my-task.md
```

## BYOK（自訂 Provider）

### Azure OpenAI
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_KEY="your-api-key"

copilot-ralph run "任務" \
  --azure-endpoint $AZURE_OPENAI_ENDPOINT \
  --azure-api-key $AZURE_OPENAI_API_KEY \
  --azure-deployment "gpt-4o" \
  --azure-api-version "2024-02-15-preview"
```

### OpenAI 直連
```bash
copilot-ralph run "任務" \
  --openai-base-url "https://api.openai.com/v1" \
  --openai-api-key "sk-..."
```

### 本地 Ollama
```bash
copilot-ralph run "任務" \
  --openai-base-url "http://localhost:11434/v1" \
  --model "llama3.2"
```

## 退出狀態碼

| 狀態碼 | 說明 |
|--------|------|
| 0 | 成功（偵測到完成短語） |
| 1 | 失敗（執行錯誤） |
| 2 | 取消（使用者中斷） |
| 3 | 超時 |

## 與 GitHub Copilot SDK 的關係

Copilot Ralph 是建構在 GitHub Copilot SDK 之上的應用範例：

```
┌─────────────────────────────────────┐
│         Copilot Ralph               │  ← 應用層
├─────────────────────────────────────┤
│       @github/copilot-sdk           │  ← SDK 層
├─────────────────────────────────────┤
│         Copilot CLI                 │  ← Runtime 層
├─────────────────────────────────────┤
│      AI Models (GPT/Claude/...)     │  ← 模型層
└─────────────────────────────────────┘
```

## 本地安裝資訊

- **安裝路徑**: `~/.local/bin/copilot-ralph`
- **版本**: v0.3.2
- **原始碼**: `research/github-copilot-sdk/copilot-ralph/`

### 執行測試
```bash
# 確保 PATH 包含 ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

# 測試執行
copilot-ralph version
copilot-ralph run "請用繁體中文說 Hello"
```

## 學習重點

1. **迭代式 AI 執行** - 如何讓 AI 反覆修正直到完成
2. **事件串流處理** - 使用 AsyncQueue 處理非同步事件
3. **完成偵測機制** - 設計 AI 任務的終止條件
4. **CLI 工具架構** - Commander.js + TypeScript 建構 CLI

## 相關連結

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk) - 底層 SDK
- [保哥的技術部落格](https://blog.miniasp.com/) - 作者部落格

## 研究日期

2026-02-03
