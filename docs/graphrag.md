---
date: "2026-07-21"
category: "開發工具"
card_icon: "material-graph-outline"
oneliner: "微軟研究院的 graph-based RAG — 用 LLM 把文件抽成知識圖譜 + 社群摘要，回答向量 RAG 答不了的『全局性』問題"
tags:
  - rag
  - knowledge-base
---

# GraphRAG 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag) |
| 官方文件 | [microsoft.github.io/graphrag](https://microsoft.github.io/graphrag/) |
| 論文 | [arXiv:2404.16130](https://arxiv.org/pdf/2404.16130) |
| 研究院部落格 | [GraphRAG: Unlocking LLM discovery on narrative private data](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) |
| LazyGraphRAG 公告 | [LazyGraphRAG sets a new standard for quality and cost](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) |

**GitHub 數據**：34.6k stars、3.6k forks、Python、MIT License、2024-03 建立、最新 **v3.1.1**（2026-07-18）

## 專案概述

GraphRAG 是微軟研究院提出的**graph-based RAG 系統**：用 LLM 把非結構化文件抽成一張**知識圖譜**（entities + relationships），再用社群偵測把圖分群、對每群生成摘要，最後在查詢時利用圖結構與社群摘要來回答問題。

它解決的核心痛點是傳統向量 RAG 的盲點——**「全局性 / 需要跨整份語料歸納」的問題**。向量 RAG 靠語意相似度撈 top-k chunk，很擅長「文件裡關於 X 說了什麼」，但答不了「整份語料的主要主題是什麼」「這些事件之間的整體關係為何」——因為答案不在任何單一 chunk，而是散在全文、要靠歸納。GraphRAG 用「社群摘要 + map-reduce」把這種歸納能力補上。

> ⚠️ 官方明講：這是**展示方法論的 demo，非 Microsoft 官方支援產品**；且 **indexing 很貴**，務必先讀文件、從小資料集開始。

## 索引 Pipeline（離線、昂貴的那一半）

```
原始文件
   │
   ▼ ① 切塊（TextUnits）
文字塊
   │
   ▼ ② LLM 逐塊抽取 entities + relationships（+ claims）  ← 成本主要來源
知識圖譜（節點=實體、邊=關係）
   │
   ▼ ③ Leiden 演算法做階層式社群偵測（community detection）
社群階層（大群 → 子群）
   │
   ▼ ④ LLM 為每個社群生成 community report（摘要）
社群摘要
   │
   ▼ ⑤ 產生 embeddings（實體 / 文字塊 / 社群摘要）
輸出：一組 parquet（documents / text_units / entities / relationships / communities / community_reports）
```

關鍵：步驟②和④**對每個 chunk / 每個社群都要呼叫 LLM**，這是 indexing 昂貴的根源。

## 查詢方法（線上）

| 方法 | 做什麼 | 怎麼運作 | 何時用 |
|------|--------|---------|--------|
| **Local Search** | 回答特定實體的問題 | 把知識圖譜的相關資料 + 原始文字塊結合 | 實體導向（「洋甘菊有什麼療效？」） |
| **Global Search** | 全資料集層級的歸納洞察 | 對**所有社群摘要**做 map-reduce 綜合 | 需要整體理解（「最重要的草藥價值是什麼？」）；耗資源 |
| **DRIFT Search** | 強化版 local search | local + 社群脈絡，並把 query **拆成後續追問**擴大檢索範圍 | 需要比 local 更豐富脈絡的細緻實體問題 |
| **Basic Search** | 基礎向量 RAG | 陽春 vector RAG，指定 `k` 個文字塊做摘要 | 當 baseline 對照各方法 |
| **Question Generation** | 從 query 自動生成追問 | — | 深入探索資料集 / 對話延續 |

## 快速開始

```bash
pip install graphrag
graphrag init --root ./ragtest            # 產生 config + prompts
# 放文件到 ./ragtest/input，設定 API key
graphrag index --root ./ragtest           # 建索引（會呼叫大量 LLM）
graphrag query --root ./ragtest --method global --query "整份語料的主要主題？"
```

> 強烈建議做 **Prompt Tuning**（`graphrag prompt-tune`）——out-of-the-box 的 prompt 對你的領域資料通常不是最佳。跨 minor 版本要 `graphrag init --force` 更新 config 格式。

## 成本問題與 LazyGraphRAG

indexing 貴到什麼程度？社群整理的數據：**2024 初，索引一個資料集要 ~$33,000**；一本 32,000 字的書約 **$7**，放大到 5 萬份文件就是嚴肅的預算議題。到 2025 年中，微軟把成本壓到約原本的 0.1%。

微軟因此另推 **LazyGraphRAG**：

| | 完整 GraphRAG | LazyGraphRAG |
|---|---|---|
| 索引階段 | LLM 逐塊抽取 + 預先生成社群摘要 / embedding | **不預先摘要、不預生 embedding**；改用 NLP 名詞片語抽取 + 共現關係 + 圖統計 |
| 索引成本 | 高 | 與**向量 RAG 相同**（≈ 完整 GraphRAG 的 0.1%） |
| 查詢品質 | 高 | global 查詢品質**與 GraphRAG Global Search 相當** |
| 查詢成本 | 高 | 低 **700 倍以上** |

核心差異：GraphRAG 把功夫花在**索引時預先計算**，LazyGraphRAG 把功夫**延遲到查詢時才做**（lazy），因此省掉巨大的前期成本。

## 目前限制 / 注意事項

- **索引成本高**：LLM 逐塊抽取是主要開銷；大語料前先估算成本、從小做起
- **非官方支援產品**：定位是研究 demo / 方法論，非生產級 SLA
- **需要 Prompt Tuning**：預設 prompt 對特定領域效果有限，要調校才好
- **版本破壞性變更**：v3.x 期間 config 格式會變，跨版本需 `init --force` 或跑 migration notebook
- **Global Search 耗資源**：map-reduce 掃所有社群摘要，查詢成本與延遲都高（LazyGraphRAG / Basic Search 是較省的替代）

## 研究價值與啟示

### 關鍵洞察

1. **GraphRAG 補的是向量 RAG 的「歸納盲點」，不是取代它**——向量 RAG 擅長「答案在某幾個 chunk 裡」的問題；GraphRAG 擅長「答案要跨整份語料歸納」的問題（主題、趨勢、整體關係）。兩者是互補而非替代。選型的第一問應該是**「這個問題的答案存在於單一段落，還是要靠全局歸納？」**

2. **「預先計算 vs 延遲計算」是 RAG 成本工程的主軸**——完整 GraphRAG 把成本壓在索引期（預先建圖、預先摘要），LazyGraphRAG 把成本延到查詢期。這組對照是所有檢索系統的通用權衡：**你想在寫入時付錢還是在讀取時付錢？** 資料常變、查詢稀疏 → lazy 划算；資料穩定、查詢密集 → 預先計算划算。

3. **社群摘要 + map-reduce 是「讓 LLM 讀完整本書」的可擴充解**——LLM context window 裝不下整份語料，GraphRAG 用 Leiden 分層社群 + 逐群摘要，把「全局理解」拆成可平行、可 map-reduce 的子問題。這個「分群摘要再聚合」的模式，對任何「要對超長內容做整體歸納」的任務都可借鑑。

4. **成本從 $33,000 → $33 揭示這領域迭代之快**——18 個月內索引成本降三個數量級，靠的是演算法改良（LazyGraphRAG 的名詞片語 + 共現取代 LLM 逐塊抽取）而非等模型變便宜。這提醒：**在 GenAI 應用裡，「現在太貴」往往是暫時的工程問題**，架構選型要預留成本會快速下降的空間。

5. **知識圖譜作為 LLM 的「結構化記憶」**——GraphRAG 的本質是把非結構化文本轉成可查詢的圖結構記憶。這與 agent 領域的 memory 系統、知識庫是同一個母題：**如何把散落的資訊組織成 LLM 能有效檢索與推理的結構**。

### 與其他專案的關聯

- **vs [RAG-Anything](rag-anything.md)**：RAG-Anything 以 LightRAG 為核心、主打 multimodal（PDF/Office/影像/公式/表格）解析；GraphRAG 更聚焦純文字的知識圖譜建構與全局查詢。兩者都走「圖 + RAG」路線，但 RAG-Anything 偏多模態輸入、GraphRAG 偏查詢方法學（global/local/DRIFT）
- **vs [LINE Bot Multimodal RAG](linebot-multimodal-rag.md)**：後者是輕量的向量/檔案檢索 RAG 應用範例，正好對照 GraphRAG「重索引、重歸納」的另一端——大多數應用其實用不到 GraphRAG 的全局歸納，向量 RAG 就夠
- **記憶 / 知識庫母題**：與 agent memory、知識庫類專案共享「把資訊結構化成可檢索記憶」的核心問題，只是 GraphRAG 用的是圖 + 社群摘要這條路
