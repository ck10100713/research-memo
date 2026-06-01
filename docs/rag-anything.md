---
date: "2026-05-14"
category: "開發工具"
card_icon: "material-file-search"
oneliner: "HKUDS All-in-One Multimodal RAG 框架，以 LightRAG 為核心 + MinerU 解析，支援 PDF/Office/影像/公式/表格與 multimodal knowledge graph"
tags:
  - rag
---

# RAG-Anything 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/HKUDS/RAG-Anything> |
| 技術報告 (arXiv) | <https://arxiv.org/abs/2510.12323>（2025-10） |
| PyPI | <https://pypi.org/project/raganything/> |
| 上游核心 | <https://github.com/HKUDS/LightRAG> |
| 文件解析器 | <https://github.com/opendatalab/MinerU>（預設）/ docling / paddleocr |
| Discord | <https://discord.gg/yF2MmDJyGJ> |
| 規模 | 20,158 stars / 2,300 forks / MIT / Python 3.10（May 14 2026 抓取） |

## 專案概述

**RAG-Anything** 是港大 Data Intelligence Lab（HKUDS）在 [LightRAG](https://github.com/HKUDS/LightRAG) 之上推出的「All-in-One 多模態 RAG 框架」，主張**一個 framework 統一處理 text / image / table / equation / chart**，把過去需要拼接多個 specialised pipelines 才能做完的多模態 RAG 整成單一 query 介面。

論文於 2025-10 (arXiv 2510.12323) 公開，repo 2025-06 開張，截至 2026-05 已累積 20k stars，是 LightRAG 系列三件套（LightRAG → RAG-Anything → 多 vendor 整合）裡的旗艦版本。

整體定位：**用一個 Python package 把「文件解析 + 內容路由 + 多模態 KG 構建 + Hybrid retrieval」串完**，使用者只需準備 LLM / Vision / Embedding 三個函式，剩下交給 framework。論文以「multi-stage multimodal pipeline」描述其架構，但 codebase 維持 LightRAG 那種「lightweight、可塞進現有專案」的調性。

## 五階段 Pipeline

```text
PDF / Office / 影像 / Markdown
        │
        ▼
[1] Document Parsing
    │  MinerU / docling / paddleocr 抽結構（保留階層）
    │  自動拆 text block / 圖 / 表 / 公式 / 其他模態
    ▼
[2] Content Understanding & Routing
    │  Autonomous categorisation → 分流到專屬 pipeline
    │  Concurrent multi-pipeline（文字 / 多模態並行）
    │  保留 inter-element relationships
    ▼
[3] Multimodal Analysis Engine
    │  Visual Content Analyzer（VLM 自動生 caption + 空間關係）
    │  Structured Data Interpreter（表格 + statistical pattern）
    │  Mathematical Expression Parser（LaTeX 原生）
    │  Extensible Modality Handler（plugin 接新模態）
    ▼
[4] Multi-Modal Knowledge Graph Index
    │  Multimodal entity extraction
    │  Cross-modal relationship mapping
    │  belongs_to 階層保留
    │  Weighted relationship scoring
    ▼
[5] Modality-Aware Retrieval
    │  Vector ↔ Graph fusion
    │  Modality-aware ranking（依 query 偏好調整權重）
    │  Relational coherence maintenance
    ▼
LLM / VLM Answer
```

## 關鍵能力

| 能力 | 說明 |
|------|------|
| End-to-End Multimodal Pipeline | 從 ingestion 到 multimodal query 一條龍 |
| Universal Document Support | PDF / DOC / DOCX / PPT / PPTX / XLS / XLSX / 影像 |
| Specialised Content Analysis | 圖片、表格、公式、其他內容各自有 processor |
| Multimodal Knowledge Graph | entity + cross-modal relation 自動建構 |
| Adaptive Processing Modes | MinerU 解析 vs 直接注入 pre-parsed content list |
| Direct Content List Insertion | 可繞過解析、丟外部產的 content list 進來 |
| Hybrid Intelligent Retrieval | text 與 multimodal 混合檢索 |
| VLM-Enhanced Query（2025.08 新增） | 文件含圖時，自動把圖塞進 VLM 做多模態分析 |
| Context Configuration（2025.07 新增） | 把相關 context 智慧整合進多模態處理 |

## 快速開始

```bash
# 推薦 PyPI 安裝
pip install raganything                 # 基本
pip install 'raganything[all]'          # 全部 optional
pip install 'raganything[image]'        # BMP/TIFF/GIF/WebP（需 Pillow）
pip install 'raganything[text]'         # TXT/MD（需 ReportLab）

# 或從原始碼 + uv
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAG-Anything && uv sync
```

### Office 文件需 LibreOffice

`.doc / .docx / .ppt / .pptx / .xls / .xlsx` 需要本機安裝 LibreOffice：
- macOS：`brew install --cask libreoffice`
- Ubuntu/Debian：`sudo apt-get install libreoffice`

### 最小可用 Python 範例

```python
from raganything import RAGAnything, RAGAnythingConfig

config = RAGAnythingConfig(
    working_dir="./rag_storage",
    parser="mineru",          # mineru / docling / paddleocr
    parse_method="auto",      # auto / ocr / txt
    enable_image_processing=True,
    enable_table_processing=True,
    enable_equation_processing=True,
)

rag = RAGAnything(
    config=config,
    llm_model_func=llm_model_func,        # 自備
    vision_model_func=vision_model_func,  # 自備
    embedding_func=embedding_func,        # 自備
)

await rag.process_document_complete(
    file_path="paper.pdf",
    output_dir="./output",
    parse_method="auto",
)

# 純文字 query
text_result = await rag.aquery(
    "What are the main findings shown in the figures and tables?",
    mode="hybrid",
)

# 多模態 query（含公式）
multimodal_result = await rag.aquery_with_multimodal(
    "Explain this formula and its relevance to the document content",
    multimodal_content=[{
        "type": "equation",
        "latex": r"P(d|q) = \frac{P(q|d) \cdot P(d)}{P(q)}",
        "equation_caption": "Document relevance probability",
    }],
    mode="hybrid",
)
```

LLM / Vision / Embedding 函式皆由使用者注入，預設文檔範例用 `gpt-4o-mini` + `gpt-4o` + `text-embedding-3-large`，理論上可換任何 OpenAI-compatible provider。

## 目前限制與注意事項

- **強相依 MinerU + LibreOffice**：MinerU 須能下載模型（首次使用會自動拉），Office 解析需 LibreOffice。離線 / 受限環境部署成本不低。
- **三個解析器擇一**：mineru / docling / paddleocr 各有強弱，README 沒明列差異 benchmark，需自行測試。
- **OpenCV 安裝常 timeout**：repo 明確建議用 `UV_HTTP_TIMEOUT=120 uv sync`。
- **必須自備 LLM / VLM / Embedding 三組函式**：對只想跑 demo 的人門檻較高，沒有「一鍵連 Ollama / LM Studio」的內建捷徑。
- **Knowledge graph 儲存仍是 LightRAG 的方案**：跟隨 LightRAG 的儲存後端、ID 規則、graph backend 選項，要客製化需先理解 LightRAG。
- **論文發表於 arXiv（非同行評審期刊）**：技術報告為主，學術權威性低於 conference paper。
- **VLM-Enhanced Query 還新**（2025-08 上線）：成熟度可能不如純文字路徑。

## 研究價值與啟示

### 關鍵洞察

1. **「Knowledge Graph + Vector」回潮**：傳統 RAG 圈以 vector-only 為主流，RAG-Anything 把 KG 重新拉回核心位置——但**不是用 KG 取代 vector，而是 fusion**。Step 5 的 "Vector-Graph Fusion" + "Modality-Aware Ranking" 是這個流派的代表性架構，值得對照 [[ai-hedge-fund]] 那種純向量 RAG 思路。
2. **「多模態」在 RAG 已從加分題變必考題**：論文核心訊息是「現代文件本來就是多模態的（PDF + 表 + 公式 + 圖），純文字 RAG 結構性失能」。一個整合 framework 在 1 年內衝到 20k stars，反映社群已認可這個賽道。
3. **MinerU 成為「事實標準」文件解析器**：RAG-Anything、docling、paddleocr 三選一，預設 MinerU。OpenDataLab 的 MinerU 跟 LightRAG 兩個港大相關的開源工具形成事實上的 RAG-Anything 上游組合拳，把學術圈的解析能力打包成可商用的 pipeline。
4. **"belongs_to" 關係鏈是被低估的設計**：把「圖 → 章節 → 文件」這種 hierarchy 直接編碼進 KG，比單純存 chunk metadata 更能支援「這張圖在哪一節提到？」這類 query。是 Microsoft GraphRAG 之外另一個值得學的階層保留模式。
5. **VLM-Enhanced Query 把「圖也丟回 VLM」的決策放在 query time**：傳統做法是 ingestion 時把圖轉文字（caption），查詢時只看 text。RAG-Anything 在 query 時帶圖再進 VLM，**承認「caption 必有 loss、原圖才是真相」**——這個哲學差異對 retrieval quality 影響很大。
6. **Modality-Aware Ranking 是個值得拆解的小組件**：依 query 自動調整不同模態的 ranking 權重，比起單一固定 fusion score 更貼近真實使用。可以單獨抽出來研究其權重學習機制。

### 與其他研究的關聯

- 與 [[opendataloader-pdf]]、[[ai-hedge-fund]]：opendataloader-pdf 是純解析端，RAG-Anything 是整條 pipeline；ai-hedge-fund 走 vector-only RAG，本研究走 vector + graph fusion，兩條路線對 retrieval quality 取捨不同。
- 與 [[ai-agents-for-beginners]] 第 5 課 Agentic RAG：Microsoft 那邊把 RAG 當作一堂 Agent design pattern；RAG-Anything 是把這個 pattern 做成可獨立部署的 framework。**Agent + Multimodal RAG**是目前最熱的兩條主軸交集，這兩篇正好是兩端代表。
- 與 [[why-your-ai-is-dumbing-down]] 的 context engineering 議題：RAG-Anything 解決的是 "retrieval-side" 的 context construction，跟前者揭露的「context 在 runtime 被截斷」是同一光譜兩端——retrieval 把高品質 context 拿進來，runtime 又被 platform 截斷，兩個問題必須一起看才有完整對策。
- 與 LightRAG：LightRAG 是核心，但只到 text 層；RAG-Anything 等同 LightRAG 的多模態擴展版。投入學習成本時建議：**先理解 LightRAG 的 KG + retrieval 架構，再學 RAG-Anything 的多模態擴展層**——重複度高的部分學一次即可。
- 對企業文件平台選型：RAG-Anything 是少數同時支援 PDF + Office + 公式 + 表格的開源整合框架，對比 Unstructured.io、LlamaParse 這類商業方案，是 self-host 路線的強候選。
