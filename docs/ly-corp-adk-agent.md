---
date: "2026-03-31"
category: "學習資源"
card_icon: "material-school"
oneliner: "LY Corporation 技術部落格 — Google ADK 入門系列，從單一 Agent 到多代理人系統的實戰教學"
---

# LY Corp — Google ADK 入門：打造 AI Agent 與多代理人系統

## 資料來源

| 項目 | 連結 |
|------|------|
| 入門 (1): 打造 AI Agent 與多代理人系統 | [techblog.lycorp.co.jp/zh-hant/adk-1-agent](https://techblog.lycorp.co.jp/zh-hant/adk-1-agent) |
| Agent LINEBot 系列 (1): 透過 ADK 打造 Agent LINE Bot | [techblog.lycorp.co.jp/zh-hant/google-adk-linebot](https://techblog.lycorp.co.jp/zh-hant/google-adk-linebot) |
| Agent LINEBot 系列 (2): Function Call → Agent 模式 | [techblog.lycorp.co.jp/zh-hant/function-agent](https://techblog.lycorp.co.jp/zh-hant/function-agent) |
| Google ADK 官方文件 | [google.github.io/adk-docs](https://google.github.io/adk-docs/) |

## 專案概述

LY Corporation（LINE 母公司）技術部落格發布的 Google ADK 入門教學系列，以繁體中文撰寫，從基礎的單一 Agent 建構到多代理人系統（Multi-Agent System），最終延伸到實際的 LINE Bot 整合應用。

這系列文章的價值在於：

1. **繁體中文技術文件稀缺**——Google ADK 的官方文件為英文，這是少數以繁體中文深度解說的教學
2. **從概念到產品的完整路徑**——不只是 SDK 教學，還展示如何整合到 LINE 的產品生態
3. **大廠工程師視角**——LY Corp 作為 LINE 的母公司，文章反映了大型服務公司如何評估和採用 Agent 框架

## 系列文章結構

### 入門 (1)：打造 AI Agent 與多代理人系統

本文為系列首篇，涵蓋：

- **ADK 核心概念**：Agent、Tools、Session、State 的關係
- **LlmAgent 使用方式**：定義 instruction、配置 tools、設定 model
- **多代理人架構**：使用 `sub_agents` 建立 Agent 階層
- **共享狀態**：`output_key` 與 `session.state` 的白板通訊模式
- **實作範例**：建構一個多步驟的專案管理 Agent 系統

### Agent LINEBot 系列：ADK × LINE Bot

- 展示如何將 ADK Agent 包裝為 LINE Bot webhook handler
- 從傳統 Function Call 模式升級為完整 Agent 模式的遷移路徑
- 整合 LINE Messaging API + Google ADK + Gemini 模型

## 核心教學內容

### ADK 的四大核心概念

根據系列文章整理的 ADK 核心概念（與[官方文件](google-adk.md)對照）：

```
Agent（代理人）
  │
  ├── LlmAgent — LLM 驅動的推理 Agent
  │     ├── instruction（系統提示詞）
  │     ├── tools（工具清單）
  │     ├── sub_agents（子代理人）
  │     └── output_key（輸出到共享狀態）
  │
  └── Workflow Agents — 確定性控制流
        ├── SequentialAgent（依序執行）
        ├── ParallelAgent（平行執行）
        └── LoopAgent（迴圈執行）
```

### 多代理人系統設計

文章展示的多代理人系統架構模式：

| 模式 | 說明 | 範例 |
|------|------|------|
| 階層委派 | 父 Agent 依 description 路由到子 Agent | Coordinator → Specialist A / B |
| 序列管線 | 每個 Agent 處理一個階段 | 解析 → 分析 → 報告 |
| 共享狀態 | 所有 Agent 讀寫同一個 state dict | `output_key` = 寫，`{var}` = 讀 |

### LINE Bot 整合

```
使用者 → LINE → Webhook → ADK Agent → Gemini → 回覆
                              │
                              ├── Tools (搜尋、計算、API)
                              └── Sub-agents (分工處理)
```

## 目前限制 / 注意事項

- **文章可能未涵蓋最新 ADK 版本**——ADK 更新快速（雙週發布），部落格文章的 API 範例可能與最新版有差異
- **LINE Bot 整合為 LY Corp 特定場景**——需要 LINE 開發者帳號和 Messaging API 設定
- **部落格為 JS 渲染（SPA）**——無法透過一般 WebFetch 取得全文，需直接瀏覽器訪問

## 研究價值與啟示

### 關鍵洞察

1. **「大廠採用 = 框架驗證」信號**——LY Corporation 作為 LINE 的母公司，願意為 Google ADK 撰寫技術部落格，代表 ADK 至少通過了大型服務公司的技術評估。這比單純的 GitHub stars 更能反映框架的生產準備度。

2. **繁體中文技術內容的生態價值**——Google ADK 的中文教學資源極少，LY Corp 的系列文章填補了繁中社群的知識缺口。對台灣開發者來說，這是最直接可用的入門資源。

3. **Function Call → Agent 的遷移路徑有參考價值**——系列第二篇展示了如何從傳統的 LLM Function Call 模式升級為完整 Agent 模式，這個遷移路徑適用於所有正在考慮導入 Agent 框架的團隊。

4. **LINE Bot × Agent 的組合展示了 Agent 落地的一種路徑**——不是「Agent 取代一切」，而是「Agent 增強現有產品」。把 Agent 嵌入已有的 LINE Bot，比從零建構 Agent 產品風險更低。

### 與其他專案的關聯

- **直接關聯 [Google ADK](google-adk.md)**：本系列是 Google ADK 的繁體中文教學資源
- **vs [Learn Claude Code](learn-claude-code.md)**：類似定位，一個教 ADK，一個教 Claude Code
- **vs [AI Agents (黃佳)](ai-agents.md)**：黃佳的書教 Agent 通用概念，LY Corp 系列教特定框架（ADK）的實作
