---
date: "2026-04-02"
category: "AI 應用"
card_icon: "material-head-lightbulb"
oneliner: "Milla Jovovich 的 AI 記憶宮殿系統 — 本地 ChromaDB 全文儲存 + 空間隱喻導航，96.6% LongMemEval"
---

# MemPalace 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [milla-jovovich/mempalace](https://github.com/milla-jovovich/mempalace) |
| 獨立深度分析 | [lhl/agentic-memory — ANALYSIS-mempalace.md](https://github.com/lhl/agentic-memory/blob/main/ANALYSIS-mempalace.md) |
| Hacker News 討論 | [MemPalace, the highest-scoring AI memory system](https://news.ycombinator.com/item?id=47672792) |
| Benchmark 方法論質疑 | [Issue #29: Multiple issues with benchmark methodology](https://github.com/milla-jovovich/mempalace/issues/29) |
| README 聲明 vs 程式碼差異 | [Issue #27: Multiple issues between README claims and codebase](https://github.com/milla-jovovich/mempalace/issues/27) |
| 獨立基準重現 | [Issue #39: Independent benchmark reproduction on M2 Ultra](https://github.com/milla-jovovich/mempalace/issues/39) |
| Bitcoin News 報導 | [Resident Evil Star Milla Jovovich Builds AI Memory Tool](https://news.bitcoin.com/resident-evil-star-milla-jovovich-builds-ai-memory-tool-with-engineer-ben-sigman/) |
| Substack 分析 | [An Unexpected Entry Into AI Memory](https://alexeyondata.substack.com/p/an-unexpected-entry-into-ai-memory) |

## 專案概述

MemPalace 是由女演員 **Milla Jovovich**（《乃莉亞：最終戰》系列）和工程師 **Ben Sigman** 使用 Claude Code 共同開發的開源 AI 記憶系統。核心理念是：**全部儲存原文，再用結構讓它可搜尋**，而不是讓 AI 決定什麼值得記住。

專案於 2026-04-05 開源（僅 7 個 commits），在 48 小時內獲得近千顆 stars，截至 2026-04-08 已達 ~20,700 stars。

| 指標 | 數值 |
|------|------|
| Stars | ~20,700 |
| 語言 | Python |
| License | MIT |
| 建立日期 | 2026-04-05 |
| Commits | 7（極早期） |
| LongMemEval R@5 | **96.6%**（raw mode） |
| 儲存 | 本地 ChromaDB，零雲端呼叫 |
| Wake-up context | ~170 tokens |

## 核心問題

> 每一次與 AI 的對話 — 每個決策、每個 debug session、每個架構辯論 — 在 session 結束時就消失了。6 個月的工作，歸零。

| 方案 | 載入 tokens | 年成本 |
|------|------------|--------|
| 全部貼入 | 19.5M（超過任何 context window） | 不可能 |
| LLM 摘要 | ~650K | ~$507/yr |
| **MemPalace wake-up** | **~170 tokens** | **~$0.70/yr** |
| **MemPalace + 5 次搜尋** | **~13,500 tokens** | **~$10/yr** |

## 記憶宮殿架構

靈感來自古希臘記憶術 — 把資訊放在想像建築的房間裡：

```
  ┌──────────────────────────────────────────┐
  │  WING: Person / Project                  │
  │                                          │
  │    ┌──────────┐  ──hall──  ┌──────────┐  │
  │    │  Room A  │            │  Room B  │  │
  │    └────┬─────┘            └──────────┘  │
  │         │                                │
  │         ▼                                │
  │    ┌──────────┐      ┌──────────┐        │
  │    │  Closet  │ ───▶ │  Drawer  │        │
  │    │ (摘要)    │      │ (原始全文) │        │
  │    └──────────┘      └──────────┘        │
  └──────────┼───────────────────────────────┘
             │ tunnel（跨翼連結）
  ┌──────────┼───────────────────────────────┐
  │  WING: Another Person / Project          │
  │          │                               │
  │    ┌─────┴────┐  ──hall──  ┌──────────┐  │
  │    │  Room A  │            │  Room C  │  │
  │    └──────────┘            └──────────┘  │
  └──────────────────────────────────────────┘
```

### 結構元素

| 元素 | 說明 |
|------|------|
| **Wing** | 一個人或專案，可以無限多個 |
| **Room** | 翼下的特定主題（auth、billing、deploy） |
| **Hall** | 同一翼內的記憶類型走廊（facts / events / discoveries / preferences / advice） |
| **Tunnel** | 跨翼連結 — 同一 Room 名出現在不同 Wing 時自動關聯 |
| **Closet** | 摘要，指向原始內容（目前是純文字，未來計畫用 AAAK） |
| **Drawer** | 原始逐字檔案，永不摘要 |

### 結構帶來的檢索提升

```
全搜所有 closets:         60.9%  R@10
限定 wing:               73.1%  (+12%)
限定 wing + hall:        84.8%  (+24%)
限定 wing + room:        94.8%  (+34%)
```

### 四層記憶載入

| 層級 | 內容 | Token 預算 | 觸發時機 |
|------|------|-----------|---------|
| **L0** | Identity — 這個 AI 是誰 | ~50 tokens | 永遠載入 |
| **L1** | 關鍵事實 — 團隊、專案、偏好 | ~120 tokens | 永遠載入 |
| **L2** | Room recall — 近期 session、當前專案 | 按需 | 話題出現時 |
| **L3** | Deep search — 跨所有 closets 語義搜尋 | 按需 | 明確要求時 |

## AAAK 壓縮方言（實驗性）

AAAK 是有損的縮寫系統 — 實體代碼、結構標記、句子截斷 — 設計用於在大規模重複實體場景下節省 tokens。**任何 LLM 都能直接讀取**，不需解碼器。

### 誠實現狀（2026 年 4 月）

| 聲明 | 實際 |
|------|------|
| 「30x 無損壓縮」 | ❌ 有損縮寫，非可逆壓縮 |
| 小規模省 tokens | ❌ 短文字 AAAK overhead 反而更多 |
| 大規模省 tokens | ⚠️ 重複實體多時可能有效，待驗證 |
| LongMemEval 分數 | ❌ AAAK mode **84.2%** vs raw mode **96.6%**（下降 12.4pp） |
| Token 計算 | ❌ 用 `len(text)//3` 而非真正的 tokenizer |

## 使用方式

```bash
pip install mempalace

# 初始化
mempalace init ~/projects/myapp

# 匯入資料
mempalace mine ~/projects/myapp                        # 專案（程式碼、文件）
mempalace mine ~/chats/ --mode convos                  # 對話（Claude、ChatGPT、Slack exports）
mempalace mine ~/chats/ --mode convos --extract general # 自動分類（決策、里程碑、問題）

# 搜尋
mempalace search "why did we switch to GraphQL"

# 接入 Claude Code（MCP）
claude mcp add mempalace -- python -m mempalace.mcp_server
```

三種 mining mode：**projects**（程式碼和文件）、**convos**（對話 exports）、**general**（自動分類為 decisions、preferences、milestones、problems、emotional context）。

接入 MCP 後，AI 會自動呼叫 `mempalace_search`，使用者不需手動下搜尋指令。

## 獨立程式碼分析：聲明 vs 實際

來自 [lhl/agentic-memory](https://github.com/lhl/agentic-memory/blob/main/ANALYSIS-mempalace.md) 的深度分析：

| README 聲明 | 程式碼實際 | 狀態 |
|------------|----------|------|
| 96.6% LongMemEval | 測的是 raw 未壓縮文字在 ChromaDB 的 embedding 效能，**宮殿結構未參與** | ⚠️ 歸因誤導 |
| +34% 宮殿結構提升 | 實際是 ChromaDB metadata filtering（wing/room 縮窄），標準 vector DB 技術 | ⚠️ 標籤誤導 |
| 矛盾偵測 | 程式碼只做完全相同 triple 攔截，衝突事實靜默累積 | ❌ 功能缺失 |
| 30x 無損壓縮 | 有損縮寫（regex + 截斷），benchmark 證實 12.4pp 品質下降 | ❌ 虛假聲明 |
| 100% with Haiku rerank | 不在公開 benchmark scripts 中，無法驗證 | ❌ 無法證實 |

### 技術實作細節

| 面向 | 實作 |
|------|------|
| 儲存 | 單一 ChromaDB collection（`mempalace_drawers`） |
| 知識圖譜 | SQLite，兩張表（entities + triples），**無圖遍歷** |
| 宮殿圖 | 按需掃描 ChromaDB metadata 計算，非預先儲存 |
| Embedding | all-MiniLM-L6-v2（ChromaDB 預設） |
| Chunk 大小 | 800 chars，100 chars overlap |
| 去重 | 僅 file-level（同 source_file 跳過），無內容去重 |
| 搜尋 | ChromaDB nearest-neighbor only，**無 BM25、無混合搜尋、無 re-ranking** |

## 值得採用的設計貢獻

根據獨立分析，以下設計模式值得學習：

1. **空間隱喻組織層** — Wing/Room/Hall/Tunnel 的比喻讓記憶結構對人類可理解、可導航
2. **四層漸進載入 + 嚴格 token 預算** — ~170 tokens wake-up，>95% context window 留給工作
3. **原文和壓縮版分別儲存** — 避免過早資訊損失
4. **零 LLM 寫入路徑** — ingestion 完全離線、確定性、零 API 成本
5. **MCP protocol embedding** — 在 status 工具輸出中嵌入 `PALACE_PROTOCOL`，強制 retrieval-before-response 紀律

## 公開勘誤（2026-04-07）

作者在社群發現問題後 48 小時內發佈了罕見的公開勘誤：

> "Brutal honest criticism is exactly what makes open source work, and it's what we asked for."

主要修正項：
- 用真正的 tokenizer 重寫 AAAK 範例
- 加入 `mode raw / aaak / rooms` 到 benchmark 文件
- 將 `fact_checker.py` 接入知識圖譜操作
- 修復 ChromaDB pinning (#100)、shell injection in hooks (#110)、macOS ARM64 segfault (#74)

## 目前限制 / 注意事項

- **極早期**：7 個 commits，4 個測試檔案覆蓋 21 個模組，顯然是 sprint 產物而非迭代驗證
- **Benchmark 歸因問題**：96.6% 實質上測的是 ChromaDB + all-MiniLM-L6-v2 的效能，不是宮殿架構
- **LongMemEval 本身的局限**：haystack ~115K tokens，50 個候選 session — 現代模型（Sonnet 200K、Gemini 1M）可以直接塞進 context window
- **無衰減/遺忘機制**：記憶只增不減，無 recency weighting
- **無內容去重**：相似記憶在不同 chunks 累積
- **無混合搜尋**：只有 ChromaDB vector search，無 BM25/FTS 後備
- **安全疑慮**：drawer 內容無 input sanitization（prompt injection 表面）
- **知識圖譜名不符實**：SQLite flat triple 查找，無真正的圖遍歷或多跳推理

## 研究價值與啟示

### 關鍵洞察

1. **「全部儲存，結構化導航」vs「摘要提取」是 AI 記憶的根本路線分歧** — MemPalace 選擇保留所有原文，用空間結構讓它可搜尋；Claude Code 的 MEMORY.md 和 Karpathy LLM Wiki 都讓 LLM 決定保留什麼。96.6% 來自 raw mode 這個事實，某種程度上驗證了「保留原文比摘要更準確」，但也暴露了「那宮殿結構的附加價值到底是什麼？」的問題。

2. **名人效應加速了技術批判的循環** — Milla Jovovich 的名氣讓專案在 48 小時內獲得近千 stars 和大量關注，但也吸引了更嚴格的技術審視。社群在兩天內就抓到 benchmark 方法論問題、AAAK 虛假聲明、程式碼與 README 不符。這種「高曝光 → 快速批判 → 公開修正」的循環，可能比低調發佈更有利於專案品質。

3. **~170 tokens wake-up 是真正的設計貢獻** — 在 context window 越來越大的時代，token 效率的價值可能被低估。但 MemPalace 的四層漸進載入（L0 身份 50 tokens → L1 關鍵事實 120 tokens → L2 按需 → L3 搜尋）是精巧的設計，讓 AI 帶著「地圖」而非「行李」醒來。

4. **「空間隱喻」的人類可理解性被低估了** — Wing/Room/Hall/Tunnel 的比喻讓技術架構變得直覺。即使底層只是 ChromaDB metadata filtering，這個 UI/UX 層的價值不應被忽視 — 使用者能理解自己的記憶在哪裡、怎麼組織的。

5. **公開勘誤是一種 trust signal** — 在 20K+ stars 的專案上承認「我們的壓縮聲明是假的、benchmark 數字來自不同 mode」，反而建立了比完美聲明更強的信任。這是開源社群的健康模式。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [Karpathy LLM Wiki](karpathy-llm-wiki.md) | 相反的設計哲學：Karpathy 讓 LLM 編譯摘要 wiki（有損但結構化），MemPalace 保留全文（無損但搜尋依賴 embedding）。Karpathy 的 index.md 對應 MemPalace 的 L1 層；Karpathy 的 Lint 操作對應 MemPalace 缺失的矛盾偵測 |
| [OpenHarness](open-harness.md) | OpenHarness 的 `memory/` 子系統實作 MEMORY.md 持久記憶，是 Claude Code 風格的「LLM 決定記什麼」路線，與 MemPalace 的「全部記住」路線形成對比 |
| [Everything Claude Code](everything-claude-code.md) | Claude Code 的 MEMORY.md 機制是極簡版的 AI 記憶 — 讓模型自行決定什麼值得記住，單一文件，無結構化空間 |
| [Analysis Claude Code](analysis-claude-code.md) | Claude Code 的 context compression（auto-compact）解決的是 session 內記憶；MemPalace 解決的是跨 session 記憶，兩者互補 |
