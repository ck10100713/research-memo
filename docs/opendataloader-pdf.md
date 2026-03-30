---
date: "2026-03-30"
category: "AI 應用"
icon: "material-file-document-outline"
oneliner: ""
---
# OpenDataLoader PDF 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [opendataloader-project/opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) |
| 官方網站 | [opendataloader.org](https://opendataloader.org/) |
| PR Newswire | [Hancom Tops Open-Source PDF Benchmarks with v2.0](https://www.prnewswire.com/news-releases/hancom-tops-open-source-pdf-benchmarks-with-opendataloader-pdf-v2-0--302713091.html) |
| PDF Association | [v2.0 Tops Open-Source PDF Benchmarks](https://pdfa.org/opendataloader-pdf-v20-tops-open-source-pdf-benchmarks-in-pdf-data-loading/) |
| Medium | [OpenDataLoader PDF v2.0 is out!](https://medium.com/data-and-beyond/opendataloader-pdf-v2-0-is-out-bb233a668ca8) |
| Hacker News | [HN 討論](https://news.ycombinator.com/item?id=45347147) |
| LangChain 整合 | [langchain-opendataloader-pdf](https://github.com/opendataloader-project/langchain-opendataloader-pdf) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 開發公司 | **Hancom**（韓國，1990 年創立，韓文文書處理器 Hangul 開發商） |
| 合作夥伴 | PDF Association、Dual Lab（veraPDF 開發團隊） |
| Stars | 10.7K（截至 2026-03-30） |
| Forks | 800 |
| 語言 | Java（核心）+ Python/Node.js/Java SDK |
| 授權 | Apache 2.0（從 MPL 2.0 轉換） |
| 版本 | v2.0（2026-03-13 發布） |

OpenDataLoader PDF 是一套**為 AI/RAG 管線設計的開源 PDF 解析器**。核心問題：PDF 格式為「頁面渲染一致性」而設計，不是為了結構化資料擷取——表格會斷裂、閱讀順序會錯亂、缺乏語義標籤。

專案提供兩種模式：

1. **Deterministic 模式**（預設）：純規則引擎，本地 CPU 執行，無 GPU 需求，0.05s/page
2. **Hybrid 模式**：複雜頁面路由到 AI 後端（OCR、表格、公式），0.43s/page，精確度 #1

v2.0 發布一週內登上 GitHub Trending 全語言第一名。

---

## 核心能力

### 資料擷取

| 能力 | 說明 |
|------|------|
| 閱讀順序 | XY-Cut++ 演算法，正確處理多欄排版 |
| 元素偵測 | 標題、段落、表格、列表、圖片、公式、圖說 |
| Bounding Box | 每個元素都有 PDF 座標 `[left, bottom, right, top]`，可回溯原始位置 |
| Tagged PDF | 原生支援 PDF 結構標籤（`use_struct_tree=True`） |
| OCR | 80+ 語言，hybrid 模式支援掃描文件 |
| 公式 | LaTeX 格式輸出（hybrid 模式） |
| 圖表描述 | SmolVLM 輕量視覺模型產生 AI 描述（hybrid 模式） |

### 輸出格式

| 格式 | 用途 |
|------|------|
| **JSON** | 結構化資料 + bounding box + 語義類型，適合 RAG 管線 |
| **Markdown** | 乾淨文字，保留標題/表格/列表，適合 LLM context window |
| **HTML** | 網頁展示 |
| **Annotated PDF** | 視覺化除錯，標記偵測到的結構 |
| **Text** | 純文字擷取 |

### JSON 輸出範例

```json
{
    "type": "heading",
    "id": 42,
    "level": "Title",
    "page number": 1,
    "bounding box": [72.0, 700.0, 540.0, 730.0],
    "heading level": 1,
    "font": "Helvetica-Bold",
    "font size": 24.0,
    "content": "Introduction"
}
```

### AI 安全功能

- **Prompt Injection 過濾**：偵測隱藏文字、零大小字型、頁面外內容
- **資料淨化**：可選將 email/URL/電話號碼替換為 placeholder

---

## Benchmark 排名（#1）

| 引擎 | Overall | Reading Order | Table | Heading | Speed (s/page) |
|------|---------|---------------|-------|---------|----------------|
| **opendataloader [hybrid]** | **0.90** | **0.94** | **0.93** | **0.83** | 0.43 |
| opendataloader | 0.72 | 0.91 | 0.49 | 0.76 | **0.05** |
| docling | 0.86 | 0.90 | 0.89 | 0.80 | 0.73 |
| marker | 0.83 | 0.89 | 0.81 | 0.80 | 53.93 |

**關鍵觀察**：

- Hybrid 模式的表格精確度（0.93）大幅領先，解決了純規則引擎的最大弱點（0.49）
- 純 deterministic 模式速度是 marker 的 **1000 倍**（0.05 vs 53.93 s/page）
- 測試資料集 200 份真實 PDF（學術論文、財報、多欄文件），benchmark code 已公開可重現

---

## 多語言 SDK

### Python

```bash
pip install -U opendataloader-pdf
# Hybrid: pip install "opendataloader-pdf[hybrid]"
```

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["file1.pdf", "file2.pdf", "folder/"],
    output_dir="output/",
    format="markdown,json"
)
```

### Node.js

```bash
npm install @opendataloader/pdf
```

```typescript
import { convert } from '@opendataloader/pdf';

await convert(['file1.pdf', 'file2.pdf', 'folder/'], {
    outputDir: 'output/',
    format: 'markdown,json'
});
```

### Java

```xml
<dependency>
  <groupId>org.opendataloader</groupId>
  <artifactId>opendataloader-pdf-core</artifactId>
</dependency>
```

需求：Java 11+

### LangChain 整合

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader

loader = OpenDataLoaderPDFLoader(
    file_path=["file1.pdf", "file2.pdf", "folder/"],
    format="text"
)
documents = loader.load()
```

---

## Hybrid 模式架構

```
PDF 輸入
    │
    ▼
Deterministic Engine（Java, veraPDF 基礎）
    │  XY-Cut++ 閱讀順序 + 邊框分析 + 文字聚類
    │
    ├─ 簡單頁面 → 直接輸出 JSON/Markdown
    │
    └─ 複雜頁面（無邊框表格/掃描/公式）→ 路由到 AI 後端
                                              │
                                              ▼
                                    Hybrid Server（localhost:5002）
                                    ├─ OCR（80+ 語言）
                                    ├─ 表格結構推理
                                    ├─ 公式辨識 → LaTeX
                                    └─ SmolVLM 圖表描述
```

```bash
# Terminal 1: 啟動 hybrid server
opendataloader-pdf-hybrid --port 5002 \
    --force-ocr \           # 掃描 PDF
    --ocr-lang "ko,en" \    # 指定語言
    --enrich-formula \       # 公式辨識
    --enrich-picture-description  # 圖表 AI 描述

# Terminal 2: 處理檔案
opendataloader-pdf --hybrid docling-fast file1.pdf file2.pdf folder/
```

---

## 與競品比較

| 面向 | OpenDataLoader | Docling (IBM) | Marker | PyMuPDF |
|------|---------------|---------------|--------|---------|
| **精確度** | 0.90 (hybrid) | 0.86 | 0.83 | — |
| **速度** | 0.05s/page (local) | 0.73s/page | 53.93s/page | 極快 |
| **GPU 需求** | 無 | 無 | 需要 | 無 |
| **Bounding Box** | 每個元素都有 | 無 | 無 | 有 |
| **AI 安全** | Prompt injection 過濾 | 無 | 無 | 無 |
| **Tagged PDF** | 原生支援 | 部分 | 無 | 部分 |
| **SDK** | Python + Node.js + Java | Python | Python | Python |
| **授權** | Apache 2.0 | MIT | GPL | AGPL |
| **本地部署** | 完全本地 | 完全本地 | 完全本地 | 完全本地 |

---

## 企業版功能

| 功能 | 說明 |
|------|------|
| Hancom Data Loader | 自訂 AI 模型，30+ 元素類型 |
| PDF/UA 匯出 | PDF/UA-1 和 PDF/UA-2 無障礙標準合規 |
| Accessibility Studio | 視覺化編輯器 |
| HWP/HWPX | 韓國 Hangul 文件格式支援（規劃中） |

---

## Roadmap

| 時程 | 功能 |
|------|------|
| 已發布 | PDF 審計功能 |
| Q2 2026 | **Auto-tag 引擎**（免費，Apache 2.0）— 自動將未標籤 PDF 轉為 Tagged PDF |
| 規劃中 | HWP/HWPX 原生支援 |

Auto-tag 是開源 PDF 工具的首創功能，與 PDF Association 和 Dual Lab 合作開發。

---

## 限制與注意事項

- **僅支援 PDF**：不處理 Word、Excel、PowerPoint
- **Java 依賴**：核心引擎是 Java，C/C++ 整合需跨程序通訊（HN 使用者反饋延遲問題）
- **Hybrid 模式需額外伺服器**：本地 localhost 但仍需啟動獨立 process
- **企業功能閉源**：PDF/UA 匯出、視覺化編輯器需另外授權
- **Hancom 為韓國公司**：文件和社群以英文為主，但部分資源可能偏向韓文生態

---

## 研究價值與啟示

### 關鍵洞察

1. **Deterministic + AI Hybrid 是最佳架構**：純規則引擎速度快但表格弱（0.49），純 AI 慢且貴。OpenDataLoader 的「簡單頁面走規則、複雜頁面走 AI」策略在精確度和速度間取得最佳平衡。

2. **Bounding Box 是 RAG 的差異化關鍵**：每個元素都有座標，意味著 RAG 回答可以直接指向原始 PDF 位置——這是 docling 和 marker 缺乏的能力，對企業級 RAG 應用至關重要。

3. **AI 安全內建是趨勢**：prompt injection 過濾在 PDF 解析層就做掉，不把風險留給下游 LLM。隨著 PDF 成為 RAG 主要輸入來源，這類防禦將成為標配。

4. **Apache 2.0 授權是商業友善的選擇**：相比 marker 的 GPL 和 PyMuPDF 的 AGPL，Apache 2.0 讓企業整合無授權顧慮。從 MPL 2.0 轉換也顯示 Hancom 刻意降低採用門檻。

5. **韓國大廠的開源策略**：Hancom 是韓國文書軟體龍頭，透過開源 PDF 解析器建立生態系，企業版功能（PDF/UA、auto-tag）作為商業模式。類似 Elastic 的 open core 模式。

### 與 Fluffy 的潛在關聯

- **RAG 管線整合**：如果 Fluffy Agent Core 需要處理 PDF 文件，OpenDataLoader 的 LangChain 整合可直接使用
- **Bounding Box 引用**：JSON 輸出的座標資訊可用於「指向原始文件位置」的引用功能
- **AI 安全**：prompt injection 過濾可作為 Fluffy 處理使用者上傳 PDF 時的防護層
