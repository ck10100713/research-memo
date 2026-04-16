---
date: "2026-04-16"
category: "Coding Agent 工具"
card_icon: "material-bookshelf"
oneliner: "263 個 Coding Agent Skills 知識庫 — 從研究所理論、演算法到台灣在地知識，附 20 支確定性計算腳本"
---

# Asgard Skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [asgard-ai-platform/skills](https://github.com/asgard-ai-platform/skills) |
| Skill Template | [asgard-ai-platform/skill-template](https://github.com/asgard-ai-platform/skill-template) |
| MCP Servers | [asgard-ai-platform/mcp-*](https://github.com/orgs/asgard-ai-platform/repositories?q=mcp-) |

**專案狀態：** ⭐ 69 stars · Python · MIT · 2026-04-07 創建 · 263 個 skills 已完成

## 專案概述

Asgard Skills 是一個開源的 **263 個 coding agent skills 知識庫**，分成 21 個主題類別。每個 skill 是獨立的 `SKILL.md` 檔案，遵循 Claude Agent Skills 規範。這是 [Asgard AI Platform](https://github.com/asgard-ai-platform) 的「原料庫」，Skills 會與 MCP servers 組合，打包成針對特定使用者情境的 plugin（如台股分析師、電商營運、政策研究者）。

核心理念：**每個 skill 封裝的是某個明確任務的「方法論 + 判斷 + 陷阱」——那些 LLM agent 若沒有提示就會重新摸索、或直接做錯的東西。**

與 wshobson/agents（77 個插件，偏軟體開發）不同，Asgard 聚焦在**商業、學術、分析**領域——研究所理論模型、商學院框架、統計方法、台灣在地知識。

## 21 個分類（263 個 Skills）

| 前綴 | 數量 | 主題 | 重點 |
|------|:----:|------|------|
| `grad-` | 87 | 研究所級理論模型 | RBV、CAPM、SEM、DID、Affordance... |
| `algo-` | 62 | 演算法 | PageRank、BM25、ARIMA、EOQ、風險模型... |
| `biz-` | 22 | 商學院框架 | SWOT、Porter 五力、DCF、損益兩平... |
| `tw-` | 9 | 台灣在地知識 | 股市、稅務、電子發票... |
| `hum-` | 9 | 人文 / 批判性推理 | |
| `ecom-` | 7 | 電商實務 | RFM、定價彈性... |
| `soc-` | 7 | 社會科學 | Cialdini、認知偏誤、創新擴散... |
| `econ-` | 6 | 經濟學基礎 | |
| `meta-` | 6 | 跨領域思維模型 | |
| `ops-` | 6 | 企業營運 | OKR、合約審查、pitch deck... |
| `law-` | 5 | 法律框架 | |
| `pr-` | 5 | 公關 / 品牌傳播 | |
| `cs-` | 4 | 客戶服務 | SOP、通知策略... |
| `data-` | 4 | 資料分析 | Cohort、Dashboard、SQL 優化... |
| `mfg-` | 4 | 製造業 | OEE、預測性維護、MPS/MRP... |
| `mkt-` | 4 | 數位行銷 | A/B 測試、廣告優化、SEO... |
| `stat-` | 4 | 統計方法論 | 因果推論、假設檢定、EDA... |
| `tech-` | 4 | 一般技術 | API、MCP server、prompt engineering... |
| `ux-` | 4 | 設計 / UX 方法論 | Design Thinking、JTBD、Nielsen... |
| `fin-` | 2 | 金融實務 | 財務模型、法說會摘要... |
| `xborder-` | 2 | 跨境電商 | 物流策略、東南亞進入... |

## Skill 結構模板

```markdown
---
name: "{category}-{skill-name}"
description: "[祈使句 WHAT + WHEN，< 1024 字元]"
metadata:
  category: "WP-XX Topic Label"
  tags: [...]
---

# {Skill 顯示名稱}

## Overview / Framework
## When to Use (and When NOT to Use)
## Methodology（Phase-Gate 或 Hub-and-Spoke）
## IRON LAW：{非顯而易見的約束}      ← 核心設計
## Output Format
## Gotchas
## Scripts（若適用）
## References
```

## 確定性計算腳本（20 支）

LLM 常算錯的計算用 Python 腳本處理（純 stdlib、無外部依賴）：

| 領域 | Skills |
|------|--------|
| 財務 | `biz-cac-ltv`、`biz-breakeven`、`biz-dcf`、`biz-dupont`、`grad-capm`、`fin-modeling` |
| 風險/統計 | `algo-risk-altman-z`、`algo-risk-var`、`mkt-ab-testing` |
| 供應鏈 | `algo-sc-eoq`、`algo-sc-safety-stock`、`algo-sc-newsvendor` |
| 排名 | `algo-rank-wilson`、`algo-rank-elo`、`algo-rank-bayesian` |
| 電商/搜尋 | `ecom-rfm-analysis`、`algo-price-elasticity`、`algo-seo-tfidf`、`algo-ecom-bm25` |

```bash
# 每支腳本都支援 --help、--input、--verify（自我測試）
python biz-cac-ltv/scripts/cac_ltv.py \
  --marketing-cost 100000 --new-customers 500 \
  --arpu 50 --gross-margin 0.70 --monthly-churn 0.05
```

## 設計原則

| 原則 | 說明 |
|------|------|
| **Iron Law** | 每個 skill 定義一條非顯而易見的約束，agent 不提示就會踩雷 |
| **Hub-and-Spoke** | SKILL.md 精簡（< 200 行），冗長內容外掛到 `references/` |
| **Phase-Gate** | 演算法類 skill 明確步驟 + 步驟間驗證關卡 |
| **具體驗證** | 範例必須可精確計算，不接受模糊範圍 |
| **不過度教學** | 假設 agent 已懂基礎，只強調它會**做錯**的地方 |

## 品質狀態

| 階段 | 狀態 |
|------|:----:|
| Phase 1：263 個 skills 生成 | ✅ |
| Phase 1.5：自動 lint | ✅ 263/263 |
| Phase 1.7：with/without skill 評估 | ✅ 4/4 with_skill 勝 |
| Phase 2-3：品質審計（抽樣 28 份） | ✅ 14 PASS / 13 MINOR / 1 MAJOR |
| Phase 4：description 最佳化 | ✅ |
| 確定性腳本 `--verify` | ✅ 全部通過 |
| Plugin 打包（Phase 5） | 🟡 規劃中 |

## 目前限制 / 注意事項

- **尚未打包為 Plugin** — Phase 5 規劃中，目前需手動安裝個別 SKILL.md
- **品質審計覆蓋率低** — 263 個只抽樣 28 個（~10%），其餘未經人工審查
- **新專案風險** — 2026-04-07 建立，不到兩週歷史
- **87 個 grad- skills 的實用性** — 研究所理論模型對多數實務場景可能過於學術
- **台灣在地 skills 僅 9 個** — `tw-` 前綴的覆蓋面有限

## 研究價值與啟示

### 關鍵洞察

1. **「Iron Law」設計是 Skill 品質的決定性差異。** 大多數 skill 只告訴 agent「怎麼做」，Asgard 的每個 skill 額外定義「做錯會踩什麼雷」。這比正面指引更有價值——LLM 最常犯的錯是它「不知道自己不知道」的邊界案例。

2. **確定性腳本解決了 LLM 的致命弱點。** LLM 做 DCF 估值、A/B 測試統計、安全庫存計算常算錯。Asgard 用純 Python stdlib 腳本處理這些——讓 LLM 做推理和決策，把計算交給確定性程式碼。這是「AI + 傳統程式」的正確分工。

3. **「原料庫 + MCP + Plugin」的三層架構值得借鑑。** Skills 是原料（方法論知識），MCP servers 是資料管道（連接外部系統），Plugin 是組合包（針對特定角色打包）。這種解耦設計讓同一個 skill 可以在不同 plugin 中復用。

4. **263 個 skills 的廣度反映了「AI 顧問化」趨勢。** 從 SWOT 分析到 CAPM 模型、從客服 SOP 到預測性維護——Asgard 本質上是把 MBA + 研究所 + 產業實務的方法論封裝給 AI Agent。這跟 Claude Ads 封裝廣告顧問知識的模式一致，但覆蓋面更廣。

5. **`tw-` 前綴是差異化的起點。** 台灣稅務、電子發票、股市規則——這些在地知識是英文世界的 skill 庫完全沒有的。雖然目前只有 9 個，但這個方向（在地化 skills）有巨大的擴展空間。

### 與其他專案的關聯

- **vs wshobson/agents（33.6K stars）：** wshobson 聚焦軟體開發（77 個 plugin、182 個 agent），Asgard 聚焦商業分析（263 個 skill、21 個主題）。兩者幾乎零重疊，可以同時安裝。wshobson 的四層模型策略和 PluginEval 在工程面更成熟，Asgard 的 Iron Law 和確定性腳本在知識面更深入。
- **vs Claude Ads：** Claude Ads 是廣告審計的「深度垂直」（250+ checks 只在廣告領域），Asgard 是跨領域的「廣度覆蓋」（263 skills 橫跨 21 個主題）。Asgard 的 `mkt-ad-optimization` skill 可能和 Claude Ads 有功能重疊。
- **vs KC AI Skills / Slavingia Skills：** 同屬 Claude Code Skill 生態，但 Asgard 的學術深度（grad- 87 個研究所理論）和確定性腳本是獨特差異。
- **vs OpenAI Agent 建構指南：** 指南說「用確定性工具防幻覺」——Asgard 的 20 支計算腳本就是這個建議的最佳實踐。
- **對 Fluffy 生態的啟示：** `tw-` 前綴的台灣在地知識 skills 可以直接參考。如果 fluffy-agent-core 需要處理台灣電商場景（稅務、發票、物流），這些 skills 是現成的知識來源。
