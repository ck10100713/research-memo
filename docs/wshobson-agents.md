---
date: "2026-04-15"
category: "Coding Agent 工具"
card_icon: "material-account-supervisor"
oneliner: "77 個 Claude Code 插件 + 182 個 Agent + 149 個 Skill — 最大的開源 Claude Code 生態集合"
---

# wshobson/agents 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [wshobson/agents](https://github.com/wshobson/agents) |
| 作者網站 | [sethhobson.com](https://sethhobson.com) |
| Claude Marketplaces | [claudemarketplaces.com](https://claudemarketplaces.com/plugins/wshobson-agents) |

**作者：** Seth Hobson

**專案狀態：** ⭐ 33.6K+ stars · Python + C# · MIT · 2025-07 創建 · 活躍開發中

## 專案概述

wshobson/agents 是目前**最大的 Claude Code 插件生態集合**，包含 **77 個聚焦型插件、182 個 Agent、149 個 Skill、16 個工作流協調器、96 個 Commands**。每個插件遵循單一職責原則，平均僅 3.6 個元件，符合 Anthropic 建議的 2-8 模式。

核心設計理念：**粒度化 + 漸進式揭示**。安裝一個插件只載入該插件的元件（~1000 tokens），不會拉入整個市集。

## 規模一覽

| 類型 | 數量 | 說明 |
|------|------|------|
| Plugins | 77 | 單一職責、可組合 |
| Agents | 182 | 涵蓋架構、語言、基礎設施、品質、AI、文件、SEO |
| Skills | 149 | 三層漸進式揭示 |
| Workflows | 16 | 全端、安全、ML pipeline、事件回應 |
| Commands | 96 | 專案建置、安全掃描、測試 |

## 四層模型策略

| Tier | Model | Agent 數 | 用途 |
|------|-------|---------|------|
| Tier 1 | Opus 4.6 | 42 | 架構、安全、code review、生產環境 |
| Tier 2 | Inherit | 42 | 複雜任務，繼承使用者設定 |
| Tier 3 | Sonnet | 51 | 文件、測試、除錯 |
| Tier 4 | Haiku | 18 | SEO、部署、簡單文件 |

## 三層漸進式揭示（Skills）

1. **Metadata** — 名稱 + 啟動條件（永遠載入）
2. **Instructions** — 核心指引（啟動時載入）
3. **Resources** — 範例與模板（按需載入）

## 24 個插件分類

涵蓋 Development、Documentation、Workflows、Testing、Quality、AI & ML、Data、Database、Operations、Performance、Infrastructure、Security、Languages（10 種）、Blockchain、Finance、Payments、Gaming、Creative、Accessibility、Marketing、Business、API、Utilities、Modernization。

## 亮點功能

| 功能 | 說明 |
|------|------|
| **PluginEval** | 三層品質評估（靜態分析 / LLM 裁判 / Monte Carlo）、10 維度、品質徽章 |
| **Agent Teams** | 7 種預設（review/debug/feature/fullstack/research/security/migration） |
| **Conductor** | Context-Driven Development 工作流（Context → Spec → Implement） |

## 快速開始

```bash
# 加入市集
/plugin marketplace add wshobson/agents

# 安裝需要的插件
/plugin install python-development
/plugin install security-scanning
/plugin install full-stack-orchestration
```

## 目前限制 / 注意事項

- **規模龐大** — 77 個插件全裝會很混亂，需要根據需求精選
- **單人主導** — Seth Hobson 佔 228/250+ commits
- **品質參差** — 雖有 PluginEval 評估，但 77 個插件的維護品質不均
- **C# 偏重** — 29K 行 C# 程式碼，部分插件偏向 .NET 生態

## 研究價值與啟示

### 關鍵洞察

1. **33.6K stars 說明 Claude Code Plugin 生態的爆發式需求。** 這是一個「插件市集」級別的 repo，而非單一工具。社群對「即插即用的 Agent 能力擴展」的渴望遠超預期。

2. **四層模型策略是成本控制的最佳實踐。** 不是所有任務都用 Opus——安全和架構用 Opus，文件和測試用 Sonnet，簡單操作用 Haiku。這種分層策略可以顯著降低 API 成本。

3. **PluginEval 品質框架值得借鑑。** 靜態分析 + LLM 裁判 + Monte Carlo 模擬的三層評估，比單純的 star 數更能反映插件品質。品質徽章系統也為使用者選擇提供了依據。

### 與其他專案的關聯

- **vs Claude Ads / Slavingia Skills / KC AI Skills：** 這些是「垂直領域 Skill」，wshobson/agents 是「全域插件市集」——層級不同。Claude Ads 是一個深入的廣告 skill，wshobson 是 77 個淺但廣的插件集合。
- **vs Superpowers：** Superpowers 聚焦工作流方法論（brainstorming、TDD、plan mode），wshobson 聚焦具體工具能力（語言支援、安全掃描、基礎設施）。兩者可以同時安裝。
- **vs Boris Cherny Tips：** Boris 教你「如何用 Claude Code」，wshobson 給你「Claude Code 能做什麼」的 182 個具體答案。
