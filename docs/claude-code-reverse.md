---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-magnify-scan"
oneliner: "2.3K stars 的 Claude Code 逆向工程——v2 基於 Runtime Monkey Patch 攔截 API 請求，附帶 Log 視覺化工具和完整 Prompt 解碼"
---
# Claude Code Reverse Engineering 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [Yuyz0112/claude-code-reverse](https://github.com/Yuyz0112/claude-code-reverse) |
| 視覺化工具 | [visualize.html](https://yuyz0112.github.io/claude-code-reverse/visualize.html) |
| 逆向結果（Prompts） | [results/prompts/](https://github.com/Yuyz0112/claude-code-reverse/tree/main/results/prompts) |
| 逆向結果（Tools） | [results/tools/](https://github.com/Yuyz0112/claude-code-reverse/tree/main/results/tools) |
| 作者 | [Yuyz0112](https://github.com/Yuyz0112) |

## 專案概述

| 指標 | 數值 |
|------|------|
| Stars | 2,302 |
| Forks | 378 |
| 語言 | JavaScript |
| 建立日期 | 2025-02-25 |

這個 repo 用**兩種方法**逆向工程 Claude Code，揭示其內部運作機制：

| 版本 | 方法 | 效果 |
|------|------|------|
| **v1**（已歸檔） | 用 LLM 分析 uglified JS 原始碼 | 能理解局部邏輯，但無法掌握整體架構 |
| **v2**（推薦） | Monkey Patch 攔截 API 請求/回應 | 直接看到 Claude Code 與 LLM 的完整對話 |

### v2 的核心洞見

> 如果你想開發一個跟 Claude Code 一樣強的 Agent，理論上你只需要在相同任務場景下構造類似的 API 請求。真正值得學習的不是 Claude Code 的內部實作，而是**它跟 LLM API 的對話內容**——這反映了它對 LLM 和 Agent 的理解。

## 技術方法：Runtime Monkey Patch

### 步驟

```bash
# 1. 找到 Claude Code 的 cli.js
which claude → $PATH → cli.js

# 2. 美化混淆程式碼
mv cli.js cli.bak
js-beautify cli.bak > cli.js

# 3. 找到 Anthropic TS SDK 的 beta.messages.create 方法
# 4. 加入 Monkey Patch（參見 cli.js.patch）
```

Patch 邏輯：
1. 每次 Claude Code 啟動時建立 `messages.log`
2. 每當 API 請求送出和收到回應時記錄 log

### Log 視覺化

提供 `parser.js` + `visualize.html`：
- 選擇 log 檔案即可檢視完整對話
- **自動識別共用 prompt**（根據出現頻率和位置）
- 區分 system prompt / user message / tool call / tool result

## 逆向工程發現

### Claude Code 內部流程全景

```
啟動
├── Quota Check（Haiku 3.5，輸入 "quota" 測試配額）
├── Summarize Previous Conversations（Haiku 3.5）
│
使用者輸入
├── Topic Detection（Haiku 3.5，判斷是否新主題）
├── Core Agent Workflow（Sonnet 4）
│   ├── System Workflow Prompt（定義 Agent 行為）
│   ├── System Reminder Start（動態環境資訊）
│   ├── System Reminder End（載入 Todo 短期記憶）
│   └── 所有工具常駐載入
│
上下文不足時
├── Context Compaction（Sonnet 4，壓縮為單一文字塊）
│
IDE 模式
├── IDE Integration（讀取開啟檔案路徑，MCP 工具）
│
任務管理
├── Todo Short-Term Memory（~/.claude/todos/ JSON 檔）
├── Task/Sub Agent（隔離 dirty context）
```

### 模型分工

| 流程 | 使用模型 | 原因 |
|------|---------|------|
| Quota Check | Haiku 3.5 | 輕量，只需要成功回應 |
| Topic Detection | Haiku 3.5 | 簡單分類，不需要強模型 |
| Summarize Previous | Haiku 3.5 | 摘要任務，成本敏感 |
| Core Agent Workflow | Sonnet 4 | 主力工作，需要強推理 |
| Context Compaction | Sonnet 4 | 需要理解完整上下文 |

### Sub Agent 的精妙設計

```
Main Agent (messages[])
    │
    │ 遇到獨立子任務（如「從 codebase 找某函式」）
    │
    ├── 提取任務 → Sub Agent (獨立 messages[])
    │       │
    │       ├── 搜尋 file A → 不是 → dirty context
    │       ├── 搜尋 file B → 不是 → dirty context
    │       ├── 搜尋 file C → 找到！→ 結果
    │       │
    │       └── 回傳「結果」給 Main Agent
    │           （dirty context 隨 Sub Agent 消失）
    │
    └── Main Agent 只看到精簡結果，上下文保持乾淨
```

## 目前限制 / 注意事項

- **需要修改 Claude Code 安裝檔案**：侵入式，更新後需重新 patch
- **v1 已證明無效**：純靜態分析 uglified JS 無法掌握整體架構
- **結果可能過時**：分析基於特定版本，Claude Code 持續更新
- **Anthropic 官方不支持逆向**：之前有 sourcemap 方式的 repo 被下架

## 研究價值與啟示

### 關鍵洞察

1. **「看 API 對話比看原始碼更有價值」**：v2 的核心洞見。Agent 的智慧不在程式碼裡，而在它如何跟 LLM 溝通。Prompt engineering > code engineering。

2. **三模型策略**：Claude Code 用 Haiku 做輕量任務（quota check, topic detection, summarize）、Sonnet 做主力工作。這種成本最佳化策略值得學習。

3. **Sub Agent 的真正目的是「上下文衛生」**：不是為了並行，而是為了隔離搜尋過程中的 dirty context，讓 main agent 保持清晰。

4. **Context Compaction 是無限對話的關鍵**：壓縮整個上下文為單一文字塊，作為下一輪對話的起點。

5. **視覺化工具的價值**：`visualize.html` 讓任何人都能直觀理解 Agent 的行為，比讀原始碼有效 10 倍。

### 與其他專案的關聯

- **analysis_claude_code**（`docs/analysis-claude-code.md`）：ThreeFish-AI 的靜態分析方法，與本專案的 v1 方法類似但更深入，兩者互補
- **Learn Claude Code**（`docs/learn-claude-code.md`）：教你從零建構 Agent harness，本專案則是從逆向角度理解已有的 harness
