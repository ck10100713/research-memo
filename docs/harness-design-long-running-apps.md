---
date: ""
category: "Coding Agent 工具"
icon: "material-cogs"
oneliner: "Anthropic 的 GAN 啟發三 Agent Harness 架構，讓 Claude 自主建構完整全端應用"
---
# Harness Design for Long-Running Apps 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原文 — Anthropic Engineering Blog | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| 前篇 — Effective Harnesses | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| 演化分析 | [Anthropic's Harness Design Philosophy — Evolution](https://www.working-ref.com/en/reference/anthropic-harness-design-philosophy-evolution) |
| Harness Engineering 趨勢 | [The Third Evolution: Why Harness Engineering Replaced Prompting in 2026](https://www.epsilla.com/blogs/harness-engineering-evolution-prompt-context-autonomous-agents) |
| Anthropic 官方推文 | [Twitter/X](https://x.com/AnthropicAI/status/2036481033621623056) |

## 專案概述

這是 Anthropic Labs 團隊成員 Prithvi Rajasekaran 於 2026-03-24 發表的工程文章，展示如何用**受 GAN 啟發的多 Agent Harness 架構**讓 Claude 在兩個領域達到更高品質：前端設計與全端應用開發。

核心問題：單一 Agent 在長時間任務中會遇到 **context 退化**（越寫越失焦）和 **自我評估失敗**（對自己的爛作品信心滿滿），僅靠 prompt 優化無法根治。解法是把「生成」和「評估」拆給不同 Agent — 就像 GAN 的 Generator 和 Discriminator。

## 核心架構：三 Agent 系統

```
┌──────────────────────────────────────────────────────┐
│                    Harness Orchestrator               │
│                                                      │
│  ┌──────────┐    spec    ┌───────────┐    code      │
│  │ Planner  │ ─────────► │ Generator │ ──────────►  │
│  │  Agent   │            │   Agent   │              │
│  └──────────┘            └─────┬─────┘              │
│       │                        │  ▲                  │
│       │ 1-4 句 prompt          │  │ bug reports     │
│       │ → 完整產品規格          │  │ + 修正要求       │
│       ▼                        ▼  │                  │
│  ┌──────────┐            ┌─────────────┐            │
│  │   User   │            │  Evaluator  │            │
│  │  Prompt  │            │    Agent    │            │
│  └──────────┘            │ (Playwright │            │
│                          │   MCP)      │            │
│                          └─────────────┘            │
└──────────────────────────────────────────────────────┘
```

### Planner Agent

- 將 1-4 句使用者 prompt 展開為**完整產品規格**
- 強調宏觀範圍和高階技術方向
- 主動建議加入 AI 功能
- **刻意迴避**過於細節的實作規格（避免錯誤級聯）

### Generator Agent

- 使用 React + Vite + FastAPI + SQLite/PostgreSQL 技術棧
- 一次實作一個功能（sprint model）
- 交給 Evaluator 前先自我檢查
- 維護 git 版本控制
- 在 Opus 4.6 上可以**不做 context reset** 持續跑 2+ 小時

### Evaluator Agent

- 用 **Playwright MCP** 像真實使用者一樣操作應用
- 測試 UI 功能、API endpoint、資料庫狀態
- 依硬性標準評分
- 產出**具體、可操作的 bug report**
- 與 Generator 談判 **Sprint Contract**（開發前先定義「完成」標準）

## 兩大核心問題與解法

### 問題一：Context 退化

| 症狀 | 說明 |
|------|------|
| Context Anxiety | Sonnet 4.5 接近 context 上限時會焦慮地草草收尾 |
| 品質衰退 | 隨著 context 填滿，產出的一致性和細節品質下降 |
| Compaction 不夠 | 摘要式壓縮（summarize in place）無法解決根本問題 |

**解法**：Context Reset — 清空重來而非壓縮。讓每個新 session 從乾淨的 slate 開始，搭配 `claude-progress.txt` 和 git log 來恢復上下文。

### 問題二：自我評估失敗

> "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre."

**解法**：將生成與評估拆給不同 Agent。訓練 Evaluator 保持懷疑態度需要**多輪 prompt 調校** — Claude 天生傾向讚美 LLM 生成的內容。

## Sprint Contract 模式

```
Generator                    Evaluator
    │                            │
    │  ── 提出實作範圍 ──────►   │
    │                            │
    │  ◄── 協商完成標準 ────     │
    │                            │
    │  ══ Sprint Contract ═══    │
    │  （雙方同意的 "done" 定義）  │
    │                            │
    │  ── 開始寫 code ──────►    │
    │      ...                   │
    │  ── 提交成果 ─────────►    │
    │                            │
    │  ◄── 依合約評分 ─────      │
    │  ◄── bug reports ─────     │
    │                            │
    │  ── 修復 ─────────────►    │
    │      ... (迴圈)            │
```

Sprint Contract 的價值：在 user story 和可測試的實作之間架橋，既不過度規格化，又讓雙方有明確的交付共識。

## 前端設計 Harness

### 四大評分標準

| 標準 | 權重 | 說明 |
|------|------|------|
| **Design Quality** | 高 | 一致的美學 — 配色、字型、版面、意象 |
| **Originality** | 高 | 有自主設計決策，而非模板預設或「AI slop」 |
| **Craft** | 中 | 技術執行力 — 層次、間距、色彩和諧、對比度 |
| **Functionality** | 中 | 使用者能否理解並完成任務 |

Harness 刻意加重 Design Quality 和 Originality，因為 Claude 天然擅長 Craft 和 Functionality。

### 迭代過程

- 每次生成跑 **5-15 輪迭代**，完整跑完約 4 小時
- Generator 根據 Evaluator 回饋**策略性微調或大幅轉向**
- 案例：荷蘭藝術博物館網站從傳統深色主題（第 9 輪）→ 3D 空間體驗（CSS perspective + 自由牆面藝術 + 門廊導航，第 10 輪）

## 實際成果數據

### Retro Game Maker 對比

| 指標 | 單一 Agent | 完整 Harness |
|------|-----------|-------------|
| 時間 | 20 分鐘 | 6 小時 |
| 成本 | $9 | $200 |
| 核心功能 | ❌ 遊戲實體不回應輸入 | ✅ 精緻 UI + sprite 編輯器 + 遊戲物理 + AI 輔助生成 |

### Browser DAW（數位音訊工作站）

| 階段 | 時間 | 成本 |
|------|------|------|
| Planner | 4.7 min | $0.46 |
| Build Round 1 | 2h 7min | $71.08 |
| QA Round 1 | 8.8 min | $3.24 |
| Build Round 2 | 1h 2min | $36.89 |
| QA Round 2 | 6.8 min | $3.09 |
| Build Round 3 | 10.9 min | $5.88 |
| QA Round 3 | 9.6 min | $4.06 |
| **合計** | **3h 50min** | **$124.70** |

QA 第一輪發現：clips 無法在 timeline 上拖曳、缺少樂器 UI、無視覺效果編輯器。第二輪發現：錄音功能仍是 stub、效果器是數字滑桿而非圖形化介面。最終產出包含完整的 arrangement view、mixer、transport，以及 AI 驅動的作曲功能。

## Harness 演化史：從複雜到簡化

```
Stage 1 (2025.11, Sonnet 4.5)    Stage 2 (Opus 4.5)         Stage 3 (Opus 4.6)
┌─────────────────┐              ┌──────────────────┐        ┌──────────────────┐
│ Initializer     │              │ Planner          │        │ Planner          │
│     ↓           │              │     ↓            │        │     ↓            │
│ Coding Agent    │              │ Generator ⇄      │        │ Generator ⇄      │
│ (context reset) │              │ Evaluator        │        │ Evaluator        │
│                 │              │ (sprint 合約)     │        │ (僅最終評估)      │
└─────────────────┘              │ (中間評估)        │        │ 無 sprint 拆分    │
                                 └──────────────────┘        │ 無 context reset  │
                                                             └──────────────────┘
```

每個被移除的組件都代表一個**關於模型能力不足的假設被推翻**：

| 移除的組件 | 為何不再需要 |
|-----------|------------|
| Context reset 間隔 | Opus 4.6 能持續 2+ 小時不失焦 |
| Sprint 分解 | 模型能自行規劃長期工作 |
| 中間評估輪次 | 只在最終交付時評估即可 |
| 多輪驗證 | 模型的自我檢查能力提升 |

## 前篇文章重點：Session 管理模式

前篇 "Effective harnesses for long-running agents" 建立的基礎模式：

### Session 啟動儀式

```
1. pwd — 確認工作目錄
2. git log + progress.txt — 恢復上下文
3. feature list (JSON) — 選擇下一個任務
4. init.sh — 啟動開發伺服器
5. E2E test — 驗證現有功能完整
6. 開始新功能開發
```

### 關鍵設計決策

| 決策 | 理由 |
|------|------|
| 用 JSON 而非 Markdown 記錄功能清單 | 模型較不易「不適當地修改或覆寫」JSON |
| 每 session 只做一個功能 | 避免一次 one-shot 整個專案 |
| 提供 Puppeteer/Playwright MCP | 沒有瀏覽器工具時 Agent 會「標記完成但未測試」 |
| git 不只版本控制 | 讓 Agent 能**自主 revert 壞掉的變更**恢復工作狀態 |

## 目前限制 / 注意事項

1. **成本高昂** — 完整 Harness 跑一次 $125-200，適合高價值場景而非日常開發
2. **非線性改進** — 後期迭代不一定比中期好，Generator 會越來越激進導致複雜度爆炸
3. **Evaluator 調校困難** — Claude 需要多輪 prompt iteration 才能學會懷疑性評估，而非反射性稱讚
4. **Prompt 措辭影響巨大** — 像「museum quality」這類詞會把所有模型輸出推向特定視覺風格的收斂
5. **Evaluator 並非永遠划算** — 任務難度在模型舒適區內時，Evaluator 變成純開銷
6. **尚未驗證跨領域通用性** — 目前只在全端 web 開發和前端設計驗證，科學研究或金融建模等場景未知

## 研究價值與啟示

### 關鍵洞察

1. **Harness Engineering 是第三代 AI 工程範式** — 從 Prompt Engineering（2022-2024）→ Context Engineering（2025）→ Harness Engineering（2026）。關鍵翻轉：同一模型、同一 prompt，僅改變 runtime 環境，程式基準測試從 42% 跳到 78%。**環境比指令更重要。**

2. **每個 Harness 組件都是一個「模型做不到」的假設** — 這是最深刻的設計哲學。隨著模型進步，應持續壓力測試每個組件的必要性，移除不再承重的假設。這讓 Harness 設計從「搭建複雜系統」轉為「持續簡化的紀律」。

3. **GAN 對抗思想遷移到軟體工程** — Generator-Evaluator 的分離不只是架構巧思，而是解決了 LLM 的根本缺陷：模型無法有效自我批評。這與人類軟體工程中 code review 和 QA 的角色天然對應，暗示成熟的人類工程實踐可能是 Agent Harness 設計的最佳靈感來源。

4. **約束反而提升生產力** — 反直覺發現：限縮 Agent 的解空間（明確的技術棧、sprint 合約、評分標準）反而讓產出品質和效率大幅提升。「用 linter 而非 prompt 來執行規則」— 讓違規在結構上不可能發生，而非靠指令「拜託」模型遵守。

5. **Harness 的有趣組合空間隨模型進步而移動，但不會縮小** — 不是說模型越強 Harness 越沒用，而是之前需要 Harness 處理的問題被模型內化後，新的更複雜問題又需要新型態的 Harness。AI 工程師的工作不會消失，只會持續轉型。

### 與其他專案的關聯

- **Everything Claude Code**（`everything-claude-code.md`）：文中的 Harness 架構正是 Claude Code 生態系中「Agent Harness」概念的具體實踐。28 agents、116 skills 的系統本身就是大型 Harness Engineering 的產物。
- **CrewAI**（`crewai.md`）：CrewAI 的多 Agent 角色扮演與本文的 Planner-Generator-Evaluator 異曲同工，但 CrewAI 的角色定義更自由，本文的角色分工更嚴格（特別是 Evaluator 必須用 Playwright 實際操作）。
- **LangGraph State API**（`langgraph-state-api.md`）：LangGraph 的 State reducer 機制可以用來實作本文的 Sprint Contract 狀態追蹤 — 例如用 `Annotated[list, add_messages]` 累積 QA 報告，用 `lambda x, y: y` 覆寫當前 sprint 目標。
- **Superpowers**（`superpowers.md`）：106K stars 的 agentic skills 框架同樣強調「約束即生產力」— 用心理學說服原則強制 coding agent 遵守紀律，與本文「用 linter 而非 prompt 執行規則」的理念相呼應。
- **前端設計 Harness** 中的「避免 AI slop」評分標準，可作為 `frontend-design` skill 的品質校準依據。
