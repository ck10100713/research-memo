---
date: "2026-04-02"
category: "學習資源"
card_icon: "material-brain"
oneliner: "Karpathy 提出的 LLM 知識庫模式 — 用 AI Agent 編譯、維護持久化 Markdown Wiki，取代傳統 RAG"
---

# Karpathy LLM Wiki 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原始 Gist | [karpathy/llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
| Antigravity 完整解析 | [Karpathy's LLM Wiki: The Complete Guide](https://antigravity.codes/blog/karpathy-llm-wiki-idea-file) |
| VentureBeat 報導 | [Karpathy shares 'LLM Knowledge Base' architecture](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an) |
| Analytics India | [Karpathy Moves Beyond RAG](https://analyticsindiamag.com/ai-news/andrej-karpathy-moves-beyond-rag-builds-llm-powered-personal-knowledge-bases) |
| Medium 分析 | [Karpathy Stopped Using AI to Write Code](https://medium.com/neuralnotions/andrej-karpathy-stopped-using-ai-to-write-code-hes-using-it-to-build-a-second-brain-instead-cddceadc5df5) |
| MindStudio 教學 | [How to Build a Personal Knowledge Base With Claude Code](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code) |

## 專案概述

**Andrej Karpathy**（OpenAI 共同創辦人、前 Tesla AI 負責人、「vibe coding」一詞的創造者）於 2026 年 4 月發佈了一個 GitHub Gist，描述了一種用 LLM Agent 建立和維護個人知識庫的模式，稱為 **LLM Wiki**。

核心理念：**LLM 的正確用法不是 Q&A，而是編譯（compilation）。** 不要每次查詢都重新從原始文件檢索（RAG），而是讓 LLM 一次性將原始資料「編譯」成結構化的 Markdown Wiki，並持續維護和更新。

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."

Karpathy 報告他的一個研究 wiki 已成長到約 **100 篇文章、40 萬字**，完全不需要向量資料庫或 embedding 檢索 — LLM 用自己維護的 index 檔案就能導航。

### 「Idea File」格式

這個 Gist 刻意不分享程式碼，而是分享**概念藍圖**：

> "There is less point in sharing specific code/apps; just share the idea, then the other person's agent customizes it."

使用者把 Gist 內容貼給自己的 LLM Agent（Claude Code、Codex 等），Agent 就會根據個人需求實例化。

## 核心架構

### 三層架構

```
Layer 1: Raw Sources（raw/）
    原始資料：文章、論文、圖片、資料集
    不可變；LLM 只讀不寫
    作為事實驗證的真相來源
         │
         │  LLM 讀取 + 編譯
         ▼
Layer 2: Wiki（wiki/）
    LLM 生成並維護的 Markdown 檔案
    概念頁、實體頁、來源摘要、比較頁、綜合概覽
    交叉引用和反向連結
    使用者讀；LLM 寫
         │
         │  結構和規則由 Schema 定義
         ▼
Layer 3: Schema（CLAUDE.md / AGENTS.md）
    定義 Wiki 結構約定
    指定頁面格式、frontmatter 要求、工作流程
    跨 session 持久記憶
```

### 三大操作

| 操作 | 說明 | 觸發時機 |
|------|------|---------|
| **Ingest** | 新增原始資料 → LLM 讀取 → 討論重點 → 建立/更新多個 wiki 頁面 → 更新 index 和 log | 加入新資料時（一個來源可能觸及 10-15 個現有頁面） |
| **Query** | 搜尋 wiki → LLM 綜合回答（附引用）→ 有價值的洞見歸檔為新 wiki 頁面 | 提問時（知識持續複利） |
| **Lint** | 健康檢查：矛盾、孤立頁面、提到但未建立的概念、過時聲明、調查缺口 | 定期維護 |

### 索引與日誌

| 檔案 | 用途 | 格式 |
|------|------|------|
| `index.md` | 按分類組織的內容目錄，每頁一行摘要 | 在 ~100 篇來源規模下可取代 embedding RAG |
| `log.md` | 時間序的操作記錄 | Append-only，可解析前綴（如 `## [2026-04-02] ingest \| Article Title`） |

## LLM Wiki vs 傳統 RAG

| 維度 | 傳統 RAG | LLM Wiki |
|------|---------|----------|
| 處理時機 | 每次查詢都重新檢索 | 每個來源只編譯一次 |
| 交叉引用 | 臨時發現 | 預先建立並維護 |
| 知識累積 | 無（每次查詢獨立） | 複利效應（每次 ingest 強化全局） |
| 輸出持久性 | 對話蒸發 | 持久化檔案 |
| 透明度 | 黑盒 | 可編輯、可審閱的 Markdown |
| 成本 | 每次查詢都付費 | 編譯一次，查閱免費 |

## 工具鏈

| 工具 | 角色 | 說明 |
|------|------|------|
| **Obsidian** | Wiki IDE | 瀏覽 wiki 結構、graph view 視覺化連結 |
| **Obsidian Web Clipper** | 來源擷取 | 將網頁文章轉為 Markdown |
| **qmd** | 本地搜尋引擎 | BM25 + 向量混合搜尋 + LLM re-ranking，完全本地（node-llama-cpp + GGUF） |
| **Marp** | 簡報產生 | 從 wiki 內容生成投影片 |
| **Dataview** | 中繼資料查詢 | Obsidian plugin，查詢 frontmatter |
| **Git** | 版本控制 | 追蹤 wiki 演化歷史 |

### 工作流

> "I have the LLM agent open on one side and Obsidian on the other."

```
使用者                          LLM Agent
  │                               │
  │  策展來源、提問、審閱          │  摘要、交叉引用、歸檔、
  │  探索、做決策                  │  記帳、矛盾標記
  │                               │
  └──── Obsidian（左） ◄──────── Agent（右）────► raw/ + wiki/
```

## 人機分工

| 使用者負責 | LLM 負責 |
|-----------|---------|
| 策展來源（決定讀什麼） | 摘要和歸檔 |
| 探索和提問 | 交叉引用維護 |
| 審閱 LLM 的輸出 | 一致性記帳 |
| 做最終決策 | 矛盾偵測和標記 |

## 快速開始

```bash
# 1. 建立目錄結構
mkdir -p my-wiki/{raw,wiki/{concepts,entities,sources,comparisons}}
cd my-wiki && git init

# 2. 撰寫 Schema（CLAUDE.md 或 AGENTS.md）
#    定義頁面格式、frontmatter 規範、工作流程

# 3. 設定 Obsidian + Web Clipper

# 4. 把 Karpathy 的 Gist 貼給你的 LLM Agent
#    Agent 會根據 Schema 開始工作

# 5. Ingest 前 10 篇來源，同時調整 Schema

# 6. 開始 Query — 有價值的洞見歸檔為 wiki 頁面

# 7. 定期 Lint（每週一次）
```

### 接入 Claude Code

```bash
# 把 Gist 內容放入 CLAUDE.md
# Claude Code 會自動讀取並依照 Schema 操作

# 如需本地搜尋，加入 qmd MCP server
claude mcp add qmd -- npx qmd --mcp
```

## 目前限制 / 注意事項

- **規模瓶頸**：index.md 超過 context window 時需要 qmd 等搜尋工具輔助，但具體閾值未明確定義
- **幻覺風險**：LLM 編譯 wiki 時可能引入錯誤，需要使用者定期審閱（Lint 只能抓部分問題）
- **單人模式**：目前設計偏向個人知識庫，團隊協作場景需額外考慮衝突解決
- **沒有具體程式碼**：Gist 是概念藍圖，每個人的實作會不同，入門門檻較高
- **Obsidian 依賴**：雖非強制，但工具鏈高度圍繞 Obsidian 生態
- **去重和品質控制**：社群回饋指出大量筆記（4,000+）時，去重和 MMR re-ranking 是關鍵挑戰

## 研究價值與啟示

### 關鍵洞察

1. **「編譯」vs「檢索」是根本性的思維轉變** — RAG 每次查詢都重新從原始文件推導，像是每次都從頭編譯程式碼。LLM Wiki 將知識「編譯」成持久化的中間表示（Markdown），之後只需「連結」而非「重新編譯」。這不只是效率提升，而是從「無狀態查詢」到「有狀態知識庫」的範式轉移。

2. **Karpathy 選擇分享「idea file」而非程式碼，本身就是洞見** — 在 Agent 時代，可複製的不再是程式碼，而是概念。把 Gist 貼給 Agent，Agent 會自動實例化。這暗示了一個趨勢：未來的「開源」可能越來越多是分享概念而非 implementation。

3. **LLM 最擅長的不是思考，而是記帳** — Karpathy 的核心觀察是：維護知識庫的痛點不在閱讀或思考，而在記帳（更新交叉引用、保持一致性、歸檔）。這正是 LLM 的甜蜜點 — 不容易出錯且不會疲倦的機械性工作。

4. **Vannevar Bush 的 Memex（1945）終於可行** — Bush 80 年前就構想了個人化知識庫+關聯文件路徑，但「誰來做維護？」一直無解。LLM 填補了這個缺口。這個歷史連結說明 LLM Wiki 不是 hack，而是長期願景的自然實現。

5. **知識複利是殺手特性** — 每次 Ingest 不只新增內容，還強化全局（更新連結、修正綜合、標記矛盾）。每次 Query 的有價值回答也被歸檔為新頁面。這種複利效應是傳統 RAG 和筆記工具都無法做到的。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [MemPalace](https://github.com/milla-jovovich/mempalace) | 同樣解決 AI 記憶問題，但走「全部儲存原文 + 空間結構」路線；LLM Wiki 走「LLM 編譯摘要 + 交叉引用」路線。MemPalace 的 96.6% recall 來自 raw mode，某種程度驗證了 Karpathy「保留原始資料」的 Layer 1 設計 |
| [gstack](gstack.md) | gstack 的 ETHOS.md「Search Before Building」三層知識體系（Tried and true → New and popular → First principles）可與 LLM Wiki 的 Ingest → Query → Lint 流程對應 |
| [Everything Claude Code](everything-claude-code.md) | Claude Code 的 CLAUDE.md + MEMORY.md 機制本質上就是 Karpathy Schema 層的簡化版本 |
| [Claude Skills Guide](claude-skills-guide.md) | Skills 的 on-demand knowledge loading 與 LLM Wiki 的 L2 room recall 概念相似 |
| 本研究網站 | 本站的 `docs/` + `mkdocs.yml` + `scripts/sync.py` 架構，本身就是 LLM Wiki 模式的一個實例 — raw sources 是網路搜尋結果，wiki 是研究筆記，schema 是 research skill 的流程定義 |
