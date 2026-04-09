---
date: "2026-04-09"
category: "Coding Agent 工具"
card_icon: "material-book-check"
oneliner: "Sahil Lavingia 將《The Minimalist Entrepreneur》轉為 10 個 Claude Code Skills"
---

# Slavingia Skills — 書本即 Skill 的先驅實驗

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [slavingia/skills](https://github.com/slavingia/skills) |
| 作者公告推文 | [Sahil Lavingia @shl (2026-03-23)](https://x.com/shl/status/2036162956761715096) |
| 技術分析 | [vibecoding.app](https://vibecoding.app/blog/sahil-lavingia-minimalist-entrepreneur-claude-skills) |
| Medium 報導 | [AI Engineering Trend](https://ai-engineering-trend.medium.com/sahil-lavingia-turns-bestseller-the-minimalist-entrepreneur-into-9-claude-ai-skills-3fb5da498556) |
| 書籍官網 | [minimalistentrepreneur.com](https://minimalistentrepreneur.com) |
| Skills 目錄 | [awesome-skills.com](https://awesome-skills.com/) |

## 專案概述

Gumroad 創辦人 Sahil Lavingia 將自己的暢銷書《The Minimalist Entrepreneur》拆解為 10 個 Claude Code skills，每個 skill 對應書中一個章節的核心框架，以 slash command 形式讓使用者在 Claude Code 中直接執行。

這不是「用 AI 摘要一本書」，而是**將書中的決策框架轉化為可互動的引導式工作流**。例如輸入 `/validate-idea`，Claude 不會給你泛泛的建議，而是依序走過「定義問題→手動驗證→收費測試→四個關鍵問題」的完整流程，並在最後給出明確判定（Validated / Needs more validation / Pivot）。

發布後的社群反應極為強烈：推文獲得 459K 觀看、5,858 書籤，GitHub repo 在數天內突破 4,800 stars，截至研究時已達 7,511 stars。

## 10 個 Skills 一覽

| Skill | 指令 | 對應書章 | 功能 |
|-------|------|---------|------|
| Find Community | `/find-community` | Ch.1 社群 | 找到你要為之服務的社群 |
| Validate Idea | `/validate-idea` | Ch.2 驗證 | 在寫任何程式碼前測試想法是否值得追 |
| MVP | `/mvp` | Ch.3 建造 | 指導在一個週末內 ship 出 MVP |
| Processize | `/processize` | Ch.4 流程化 | 先用手動流程交付價值，再寫程式碼 |
| First Customers | `/first-customers` | Ch.5 銷售 | 策略性取得前 100 個客戶 |
| Pricing | `/pricing` | Ch.6 定價 | 成本模型 vs 價值模型的定價引導 |
| Marketing Plan | `/marketing-plan` | Ch.7 行銷 | 內容導向的行銷策略（做粉絲，不做頭條） |
| Grow Sustainably | `/grow-sustainably` | Ch.8 成長 | 以獲利為核心的成長決策評估 |
| Company Values | `/company-values` | Ch.9 文化 | 在招聘前定義公司文化 |
| Minimalist Review | `/minimalist-review` | 全書 | 用極簡創業原則壓力測試任何商業決策 |

## Skill 技術結構

```
slavingia/skills/
├── .claude-plugin/
│   ├── plugin.json         ← 插件 metadata（name、version、author）
│   └── marketplace.json    ← 市集發布設定
├── skills/
│   ├── validate-idea/
│   │   └── SKILL.md        ← 單一 Markdown 檔案 = 一個 skill
│   ├── mvp/
│   │   └── SKILL.md
│   ├── pricing/
│   │   └── SKILL.md
│   └── ...（10 個子目錄）
└── README.md
```

**每個 SKILL.md 的結構：**

```yaml
---
name: validate-idea
description: Validate a business idea using the minimalist entrepreneur
             framework. Use when someone has a business idea and wants to
             test if it's worth pursuing before building anything.
---

（角色設定 → 核心原則 → 分步驟引導流程 → 紅旗/綠旗判斷 → 最終輸出格式）
```

### 安裝方式

```bash
# 方式 1：Plugin Marketplace（推薦）
/plugin marketplace add slavingia/skills
/plugin install minimalist-entrepreneur

# 方式 2：手動 clone
git clone https://github.com/slavingia/skills.git ~/.claude/plugins/skills
```

## Skill 內容範例：`/validate-idea`

以 `/validate-idea` 為例，展示「書本→Skill」的轉化方式：

| 步驟 | 框架內容 | 互動方式 |
|------|---------|---------|
| Step 1：定義問題 | 「誰有這個問題？現在怎麼解決？多痛？」 | 問使用者具體描述 |
| Step 2：手動驗證 | Sahil 的「processizing」概念——先手動做 | 引導使用者寫下手動步驟 |
| Step 3：收費測試 | 「至少跟 10 人談過？3 人願意付費？」 | 檢核清單式確認 |
| Step 4：四個關鍵問題 | 週末能 ship 嗎？客戶生活更好嗎？ | 是/否判斷 |
| 紅旗判斷 | 「沒人在解決這個問題」= 不要做 | 自動標記風險 |
| 最終輸出 | Validated / Needs more validation / Pivot | 明確判定 + 下一步 |

## 「書本即 Skill」模式分析

```
傳統書籍消費                          書本即 Skill
────────────                          ────────────
讀者 → 讀書 → 記住框架                  使用者 → /slash-command
     → 遇到決策 → 試著回想               → AI 引導走完完整框架
     → 可能記錯或簡化                    → 用使用者的真實情境套用
     → 斷裂的知識轉化                    → 即時輸出判定和建議

知識留存率：~10%                       知識應用率：~100%（每次使用都完整走完）
```

### 這個模式適合轉化的書籍類型

| 適合 | 不適合 |
|------|--------|
| 有明確框架/檢核清單的商業書 | 敘事型/傳記型書籍 |
| 決策導向（何時該X、何時不該Y） | 純理論/學術著作 |
| 分步驟的方法論 | 靈感型/散文型 |
| 「如果...那麼...」的條件邏輯 | 需要大量背景知識的專著 |

## 目前限制

| 限制 | 說明 |
|------|------|
| Claude Code 專屬 | SKILL.md 格式不相容 Cursor、Aider 等其他工具 |
| 無狀態 | 每次 `/validate-idea` 重新開始，不記得上次的結論 |
| 單向轉化 | 書→Skill 的過程仍需人工精煉，沒有自動化工具 |
| 英文內容 | Skills 內容為英文，但 Claude 會依使用者語言回覆 |
| 無資料整合 | 無法自動拉取市場數據、競品資訊等外部資料 |
| 品質依賴作者 | 框架的實用性完全取決於原書的品質 |

## 研究價值與啟示

### 關鍵洞察

1. **「書本即 Skill」開啟了知識產品的新形態**：Sahil 證明了一本書可以不只是被閱讀，而是被「執行」。這對所有方法論型的作者來說是一個全新的發行管道——你的書不再是 PDF 或紙本，而是一個可以在 Claude Code 裡被呼叫的互動式顧問。7,500+ stars 證明市場需求真實存在。

2. **Skill 的本質是「結構化 prompt + 決策樹」**：看完 SKILL.md 原始碼後會發現，每個 skill 其實就是一個精心設計的 prompt，包含角色設定、分步驟引導、條件判斷和輸出格式。沒有任何程式碼——純 Markdown。這意味著**任何有領域知識的人都能寫 skill**，不需要會寫程式。

3. **Plugin Marketplace 是 Claude Code 生態的關鍵拼圖**：`/plugin marketplace add slavingia/skills` 這個安裝流程，讓 Skill 從「手動複製檔案」進化到「一行指令安裝」。這是 Claude Code 建構第三方生態系的基礎——類似 VS Code Extension Marketplace 或 npm registry 的角色。

4. **Bootstrap vs VC 的哲學對比已內建於 Skill 生態**：Sahil 的 skills 走的是 bootstrap 路線（「Day 1 就收費」「手動先做再自動化」），而同類的 gStack 走的是 YC 路線（融資、pitch deck、hypergrowth）。Skill 不只是工具，它承載了作者的價值觀和世界觀。

5. **缺少狀態管理是最大的進化空間**：目前每次呼叫 skill 都是全新的 session。如果能記住「上次 /validate-idea 的結論是 Needs more validation」，然後在 `/mvp` 中自動帶入，整個 10 步旅程就能變成一個連貫的創業教練體驗。

### 與其他專案的關聯

- **Claude Skills Guide**：Slavingia Skills 是目前最成功的第三方 skill 套件，是 Claude Skills Guide 中「如何寫好 skill」的最佳範例
- **Superpowers**：Superpowers plugin 也使用 SKILL.md 格式，但專注於開發工作流而非商業決策——兩者展示了同一格式的不同應用面向
- **gStack**：直接競品，走 YC/VC 路線的創業 skill 套件，和 Slavingia 的 bootstrap 路線形成對比
- **Context Hub**：如果 Context Hub 提供「API 文件作為 Agent 知識」，Slavingia Skills 則提供「商業框架作為 Agent 知識」——都是在擴展 Agent 的知識邊界，但方向不同
