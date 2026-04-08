---
date: "2026-04-02"
category: "AI 應用"
card_icon: "material-briefcase-search"
oneliner: "Claude Code 驅動的 AI 求職系統 — 14 個 skill modes、A-F 評分、ATS 履歷生成、批次處理 740+ 職缺"
---

# Career-Ops 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [santifer/career-ops](https://github.com/santifer/career-ops) |
| 作者案例研究 | [Career-Ops: How I Built My Own AI Job Search Tool](https://santifer.io/career-ops-system) |
| DEV 文章 | [I Built a Multi-Agent Job Search System with Claude Code](https://dev.to/santifer/i-built-a-multi-agent-job-search-system-with-claude-code-631-evaluations-12-modes-2cd0) |
| Aakash Gupta 分析 | [The Claude Code Job Search OS](https://www.news.aakashg.com/p/job-search-os) |
| ToolHunter | [Career-Ops: Open-Source AI Job Search Pipeline](https://toolhunter.cc/tools/career-ops) |

## 專案概述

**Career-Ops** 是由 Santiago Fernández（前創辦人、現任 Head of Applied AI）開發的開源 AI 求職系統，基於 Claude Code 的 skill mode 架構。核心理念：

> **"Companies use AI to filter candidates. I gave candidates AI to *choose* companies."**

這**不是**自動海投工具（spray-and-pray），而是一個**篩選系統** — 幫你從數百個職缺中找到少數值得投遞的。系統永遠不會自動提交申請，人類做最終決策。

作者用它評估了 **740+ 職缺**、生成 **100+ 客製履歷**，最終拿到 Head of Applied AI 的 offer。

| 指標 | 數值 |
|------|------|
| Stars | ~20,700 |
| 語言 | JavaScript + Go |
| License | MIT |
| 建立日期 | 2026-04-04 |
| Skill Modes | 14 個 |
| 預設公司 | 45+ |
| 評估維度 | 10 個（A-F 評分） |

## 核心架構

### 自動化管線（Auto-Pipeline）

```
貼入職缺 URL
     │
     ▼
┌──────────────────┐
│  JD 擷取          │  Playwright 瀏覽器自動導航
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Archetype 偵測   │  6 種角色原型分類
│                   │  LLMOps / Agentic / PM / SA / FDE / Transformation
└────────┬─────────┘
         │
┌────────▼─────────┐
│  10 維度 A-F 評分  │  對比 cv.md + 作品集
└────────┬─────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Report  PDF  Tracker
  .md   .pdf   .tsv
```

### 10 維度評分系統

| 維度 | 說明 | 權重 |
|------|------|------|
| **Role Match** | 與 CV proof points 的對齊度 | Gate-pass（不通過直接淘汰） |
| **Skills Alignment** | 技術棧重疊度 | Gate-pass |
| **Seniority** | 職級拉伸適當性 | 高 |
| **Compensation** | 市場行情 vs 目標薪資 | 高 |
| **Interview Likelihood** | 回覆面試的機率 | 高 |
| **Geographic** | 遠端/混合可行性 | 中 |
| **Company Stage** | 新創/成長/企業的契合度 | 中 |
| **Product-Market Fit** | 領域共鳴度 | 中 |
| **Growth Trajectory** | 職涯升遷可見度 | 中 |
| **Timeline** | 招聘急迫性 | 低 |

> 實際數據：631 個職缺中 **74% 低於 4.0/5**，系統強烈建議不投遞低於 4.0 的職位。

### 14 個 Skill Modes

| Mode | 功能 |
|------|------|
| **auto-pipeline** | 完整流程：擷取 JD → 評估 → PDF → 追蹤 |
| **oferta** | 單一職缺評估（6 區塊報告） |
| **pdf** | ATS 優化履歷生成（Space Grotesk + DM Sans） |
| **scan** | 掃描 45+ 公司的求職入口 |
| **batch** | 並行批次處理 10+ 職缺 |
| **apply** | Playwright 自動填寫申請表 |
| **pipeline** | 處理待評估的 URL 隊列 |
| **tracker** | 查看申請狀態 |
| **contacto** | LinkedIn 外聯訊息生成 |
| **deep** | 深度公司研究 |
| **training** | 評估課程/證照的 ROI |
| **project** | 評估作品集專案 |
| **negotiation** | 薪資談判腳本（地區折扣反擊、competing offer 槓桿） |
| **_shared** | 共享上下文（原型定義、proof points） |

### 6 區塊評估報告

每個職缺生成一份完整報告：

1. **Role Summary** — 角色概述和原型分類
2. **CV Match** — 技能對齊分析和缺口識別
3. **Level Strategy** — 職級定位策略
4. **Comp Research** — 薪資市場研究
5. **Personalization** — 客製化投遞策略
6. **Interview Prep** — STAR+Reflection 故事庫（5-10 個 master stories 回答任何行為面試問題）

### 批次處理架構

```
Conductor（batch-runner.sh）
     │
     ├── Worker 1（claude -p）──→ claim URL → auto-pipeline → write result
     ├── Worker 2（claude -p）──→ claim URL → auto-pipeline → write result
     ├── Worker 3（claude -p）──→ claim URL → auto-pipeline → write result
     └── ...N workers
     
- Lock files 防止重複認領
- Worker 失敗不阻塞其他 worker
- 從已儲存狀態恢復
- 680 URLs 去重防止重複評估
```

### ATS 自適應履歷

不是發同一份 CV，而是每個職缺生成客製版本：

1. 從 JD 提取 15-20 個關鍵字
2. 偵測語言和地區（US → English/Letter, Europe → 當地語言/A4）
3. 識別原型（6 種 archetype）
4. 選出最相關的 3-4 個專案
5. 重排 bullet points — 最相關經歷移到最上面
6. Puppeteer 渲染 PDF（自託管字體、單欄 ATS 安全格式）

> **「履歷是論證（argument），不是文件（document）」** — 合法重組，非捏造。

## 技術棧

| 組件 | 技術 |
|------|------|
| Agent 引擎 | Claude Code（custom skills + modes） |
| 網頁互動 | Playwright（掃描求職入口、填表） |
| PDF 生成 | Puppeteer + HTML template |
| Dashboard | Go + Bubble Tea + Lipgloss（Catppuccin Mocha） |
| 資料格式 | Markdown tables + YAML config + TSV batch |
| 並行管理 | tmux + lock files |

## 快速開始

```bash
git clone https://github.com/santifer/career-ops.git
cd career-ops && npm install
npx playwright install chromium

# 檢查環境
npm run doctor

# 設定
cp config/profile.example.yml config/profile.yml   # 填入個人資料
cp templates/portals.example.yml portals.yml        # 自訂目標公司

# 建立 cv.md（你的 Markdown 履歷）

# 啟動 Claude Code，讓它幫你客製系統
claude
# "Change the archetypes to backend engineering roles"
# "Add these 5 companies to portals.yml"
```

## 實戰數據

| 指標 | 數值 |
|------|------|
| 評估報告 | 631 份 |
| 實際投遞 | 68 份（10.8% 投遞率） |
| 生成 PDF | 354 份 |
| 去重 URL | 680 個 |
| 重複評估 | 0 |
| 最終結果 | 拿到 Head of Applied AI offer |

## 目前限制 / 注意事項

- **高度個人化**：系統預設為作者的 AI Product/Engineering 角色配置，其他領域（如前端、資料工程）需大量自訂 archetypes 和 scoring weights
- **依賴 Claude Code**：核心引擎是 Claude Code，需要 Anthropic API 費用（批次處理 100+ 職缺的成本不低）
- **Playwright 脆弱性**：求職入口（Greenhouse, Lever 等）UI 頻繁變動，scraper 需要持續維護
- **法律灰色地帶**：自動掃描求職入口可能違反某些平台的 ToS，作者在 LEGAL_DISCLAIMER.md 中明確提醒
- **AI 幻覺風險**：評估報告可能誇大技能匹配度，作者強調「Always review AI-generated content for accuracy before submitting」
- **冷啟動問題**：作者坦言「the first evaluations won't be great — the system doesn't know you yet」，需要持續餵入個人 context
- **僅支援 Claude Code**：README 提到 OpenCode 和 Codex 支援即將到來，但目前僅 Claude Code

## 研究價值與啟示

### 關鍵洞察

1. **「Modes 優於單一巨型 Prompt」是可驗證的 Claude Code 使用模式** — 作者的核心經驗是：12 個專注的 mode（每個只載入必要 context）比一個 10,000 token 的 system prompt 效果更好。這與 gstack 的 29 個 slash command skill 設計哲學一致，證明了「分離關注點」在 LLM prompt 工程中同樣有效。

2. **「系統即作品集」是 AI 時代求職的元策略** — Career-Ops 本身就是最好的面試作品。如果你應聘 AI Product/Engineering 角色，展示一個用 Claude Code 建造的多 Agent 系統比任何傳統作品集都有說服力。這是一個自我指涉的設計 — 工具本身證明了使用者的能力。

3. **去重比評分更有 ROI** — 作者發現防止 680 個重複評估的基礎設施，比精煉評分邏輯帶來更高回報。這是一個反直覺的工程洞見：在大量候選中，排除已處理的比改善處理品質更重要。

4. **「人類做決策，AI 做分析」是正確的 HITL 邊界** — Career-Ops 刻意不自動提交申請。631 份評估中只投遞了 68 份（10.8%），系統的價值在於幫你「說不」而非「說是」。這與 gstack 的 `/review` gate 設計一致 — AI 提供建議，人類做最終決策。

5. **74% 低於門檻是系統真正的價值所在** — 大多數人會認為 AI 求職工具的價值在於「找到好工作」。但 Career-Ops 的實際數據顯示，它最大的價值是「過濾掉不值得投遞的工作」— 節省了投遞 74% 不匹配職位的時間。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [gstack](gstack.md) | 共享「Modes/Skills > 單一巨型 Prompt」的設計哲學；gstack 有 29 個 skill modes 管理開發流程，Career-Ops 有 14 個 modes 管理求職流程。兩者都是 Claude Code 的結構化工作流系統 |
| [Superpowers](superpowers.md) | Superpowers 的 brainstorming → plan → execute → verify 流程可對比 Career-Ops 的 scan → evaluate → pdf → apply 管線 |
| [Claude Code Showcase](claude-code-showcase.md) | Career-Ops 是 Claude Code 在非 coding 場景的典範應用 — 用 coding agent 解決求職問題 |
| [Claude Skills Guide](claude-skills-guide.md) | Career-Ops 的 14 個 mode 是 Claude Code skill 系統的深度實踐案例 |
| [Paperclip](paperclip.md) | Paperclip 管理多 Agent 公司運營，Career-Ops 管理個人求職管線；兩者都是 Agent 編排系統，但規模不同 |
