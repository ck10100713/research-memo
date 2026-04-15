---
date: "2026-04-15"
category: "Coding Agent 工具"
card_icon: "material-graph"
oneliner: "本地程式碼知識圖譜 — Tree-sitter 解析 AST，MCP 提供 blast-radius 最小檔案集，省 8.2x token"
---

# Code Review Graph 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) |
| 官網 | [code-review-graph.com](https://code-review-graph.com) |
| Hacker News 討論 | [HN #47314090](https://news.ycombinator.com/item?id=47314090) |
| DeepWiki 文件 | [deepwiki.com](https://deepwiki.com/tirth8205/code-review-graph) |
| PyPI | [code-review-graph](https://pypi.org/project/code-review-graph/) |

**專案狀態：** ⭐ 10K+ stars · Python + TypeScript · MIT · v2.3.2 · 23+ 語言支援

## 專案概述

Code Review Graph 解決一個核心問題：**AI coding 工具每次任務都重新讀取整個 codebase，浪費大量 token。**

解法：用 Tree-sitter 將程式碼解析為 AST，建立知識圖譜（函式/類別為節點、呼叫/繼承為邊），存於本地 SQLite。Review 時透過 MCP 只提供 **blast radius 內的最小檔案集**。

**關鍵數據：** Token 平均節省 **8.2x**，monorepo 場景最高 **49x**。Impact 分析 Recall 100%（從未漏掉受影響檔案）。

## 核心架構

```
Git Repo
  │  Tree-sitter 解析
  ▼
AST → 知識圖譜（SQLite）
  │    節點：函式、類別、模組
  │    邊：呼叫、繼承、import、測試覆蓋
  │
  │  git commit / file save 自動增量更新（<2s）
  ▼
28 個 MCP Tools
  │    blast-radius、review context、semantic search
  │    hub/bridge 偵測、knowledge gap 分析
  ▼
AI Agent（Claude Code / Codex / Cursor / ...）
  只讀需要的最小檔案集
```

## 支援平台與語言

**一鍵安裝**自動偵測並配置：Claude Code、Codex、Cursor、Windsurf、Zed、Continue、OpenCode、Antigravity、Kiro、Qwen Code

**23+ 語言：** Python、TypeScript/TSX、JavaScript、Vue、Svelte、Go、Rust、Java、Scala、C#、Ruby、Kotlin、Swift、PHP、Solidity、C/C++、Dart、R、Perl、Lua、Zig、PowerShell、Julia、Elixir、Bash

## 核心功能

| 功能 | 說明 |
|------|------|
| Blast-radius 分析 | 追蹤每個 caller、dependent、test 的影響範圍 |
| 28 個 MCP Tools | build/update、impact、review context、semantic search、graph traversal |
| 5 個 MCP Prompts | review_changes、architecture_map、debug_issue、onboard_developer、pre_merge_check |
| 增量更新 + Hook | git commit 或 file save 自動更新，<2s（2,900 檔案） |
| Semantic Search | sentence-transformers / Gemini / MiniMax 向量嵌入 |
| 視覺化 | D3.js force-directed graph + GraphML / Neo4j / Obsidian 匯出 |
| Hub & Bridge 偵測 | 找出架構瓶頸和高耦合節點 |
| Community Detection | Leiden 演算法聚類 |
| Refactoring 工具 | rename preview、dead code detection、dry-run |
| Graph Diff | 跨時間比較圖譜快照 |

## 效能數據

| 指標 | 數值 |
|------|------|
| Token 節省 | 平均 8.2x，最高 49x |
| Impact Recall | 100%（從未漏掉） |
| 平均 F1 | 0.54 |
| 增量更新 | <2s（2,900 檔案） |
| 初始 Build | ~10s（500 檔案） |
| 測試 | 788 tests pass |

## 快速開始

```bash
pip install code-review-graph
code-review-graph install    # 自動偵測 IDE 並配置 MCP
code-review-graph build      # 建立圖譜
```

## 目前限制 / 注意事項

- **小型單檔變更** — graph context 可能比直接讀檔案更大
- **Search MRR 0.35** — 語義搜尋排名仍需改進
- **Flow Detection 33% recall** — 僅在 Python framework pattern 上可靠
- **偏保守** — 刻意多抓（false positives）以確保不漏

## 研究價值與啟示

### 關鍵洞察

1. **「只給 AI 需要的」比「讓 AI 更聰明」更有效。** 8.2x token 節省不是靠更好的 LLM，而是靠圖譜精準定位——減少噪音比增加能力更實際。

2. **Tree-sitter + SQLite 是輕量級程式碼理解的最佳組合。** 不需要 LSP、不需要雲端服務——本地 AST 解析 + SQLite 就能建立有效的程式碼知識圖譜。

3. **Blast-radius 概念應該成為所有 AI code review 的標配。** 知道「改這一行會影響哪些檔案」是 code review 的核心問題，圖譜讓這個問題有了精確答案。

### 與其他專案的關聯

- **vs Karpathy LLM Wiki：** 兩者都是「用結構化知識減少 AI 的工作量」。LLM Wiki 編譯研究知識，Code Review Graph 編譯程式碼結構。
- **對 Fluffy 生態的啟示：** fluffy-core（Django）跨多個 app 的依賴關係可以用 Code Review Graph 視覺化和追蹤，特別是在重構時理解 blast-radius。
