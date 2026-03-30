---
date: "2026-02-04"
category: "AI Agent 框架"
icon: "material-forum"
oneliner: "使用 Copilot SDK 建構的多 Agent 辯論系統"
---
# 多 Agent 辯論會系統

使用 Python + GitHub Copilot SDK 建構的多 Agent 辯論會系統，讓來自不同 LLM 提供者的 AI 就用戶指定議題進行辯論。

## 專案概述

此系統利用 GitHub Copilot SDK 的多模型支援功能，建立多個獨立的 AI Agent Session，模擬辯論會場景。每個辯論代表使用不同的 LLM 提供者，展現不同模型的思考方式與論述風格。

## 模型配置

| 角色 | 模型 | 提供者 |
|------|------|--------|
| 辯論代表 A | gpt-4o | OpenAI |
| 辯論代表 B | claude-3-5-sonnet-20241022 | Anthropic |
| 辯論代表 C | gemini-1.5-pro | Google |
| 仲裁者 | claude-3-5-sonnet-20241022 | Anthropic |

> **注意**：實際模型識別碼可能需要根據 Copilot SDK 支援情況調整。

## 專案結構

```
multi-agent-debate/
├── README.md                    # 專案說明
├── requirements.txt             # 依賴套件
├── .env.example                 # 環境變數範本
├── config/
│   ├── __init__.py
│   ├── providers.py             # Provider 設定
│   └── debate_config.py         # 辯論設定
├── agents/
│   ├── __init__.py
│   ├── base_agent.py            # Agent 基礎類別
│   ├── debater.py               # 辯論代表
│   └── arbitrator.py            # 仲裁者
├── debate/
│   ├── __init__.py
│   ├── context_manager.py       # 上下文管理
│   └── engine.py                # 辯論引擎
└── main.py                      # 主程式入口
```

## 安裝需求

- Python 3.8+
- GitHub Copilot CLI 已安裝並認證
- GitHub Copilot 訂閱（或使用 BYOK）

## 安裝步驟

```bash
# 1. 進入專案目錄
cd research/multi-agent-debate

# 2. 建立虛擬環境（建議）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 複製環境變數範本
cp .env.example .env

# 5. 編輯 .env 設定（可選）
```

## 使用方式

```bash
# 執行預設辯論
python main.py

# 指定議題
python main.py --topic "AI 是否會取代人類工作？"

# 指定辯論輪數
python main.py --rounds 5

# 啟用詳細輸出
python main.py --verbose
```

## 辯論流程

```
1. 初始化
   └─ 建立 CopilotClient → 建立 4 個 Session

2. 開場階段
   └─ 仲裁者宣布議題 → 各代表開場陳述（A→B→C）

3. 辯論輪次（重複 N 輪）
   ├─ 代表 A 發言（含前輪上下文）
   ├─ 代表 B 發言（含前輪上下文）
   ├─ 代表 C 發言（含前輪上下文）
   └─ 仲裁者輪次評論

4. 最終裁決
   └─ 仲裁者匯總所有發言 → 宣布結果與見解

5. 清理
   └─ 銷毀 Sessions → 產生逐字稿
```

## 輸出範例

系統會產生辯論逐字稿，格式如下：

```
============================================================
                    AI 辯論會逐字稿
============================================================
議題：AI 是否會取代人類工作？
日期：2026-02-04
辯論輪數：3

============================================================
                       開場陳述
============================================================

【仲裁者】（claude-3-5-sonnet）：
歡迎各位參與今天的辯論會...

【辯論代表 A】（gpt-4o）：
作為 OpenAI 的代表，我認為...

...
```

## 研究日期

2026-02-04
