---
date: "2026-08-03"
category: "AI 應用"
card_icon: "material-file-search-outline"
oneliner: "Firecrawl 開源 Rust PDF 解析器 — 免 OCR 分類文字/掃描檔，200ms 內轉乾淨 Markdown"
tags:
  - rag
  - benchmark
  - self-hosted
---
# pdf-inspector 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/firecrawl/pdf-inspector> |
| 官方文件站 | <https://firecrawl.github.io/pdf-inspector/> |
| crates.io | <https://crates.io/crates/pdf-inspector> |
| npm | <https://www.npmjs.com/package/@firecrawl/pdf-inspector> |
| PyPI | <https://pypi.org/project/pdf-inspector/> |
| Firecrawl 部落格：Fire-PDF | <https://www.firecrawl.dev/blog/fire-pdf-launch> |
| Firecrawl 部落格：/parse | <https://www.firecrawl.dev/blog/introducing-parse> |
| Benchmark 語料庫 | <https://github.com/opendataloader-project/opendataloader-bench> |

> Metadata（擷取於 2026-08-03）：6,529 ★、Rust（含 Python/JS/WASM 綁定）、MIT License、最新版 `0.2.6`。由 [Firecrawl](https://firecrawl.dev) 維護，是其 `/parse` 文件解析服務的底層引擎之一。

## 專案概述

pdf-inspector 是一個用 **Rust** 寫的高速 PDF 解析函式庫，做三件事：**分類（classification）**、**位置感知文字擷取（text extraction）**、以及**轉乾淨 Markdown**——而且**完全不呼叫 OCR**。

它的核心命題來自一個觀察：在真實世界的 PDF 流水線中，約 **54% 的 PDF 本來就是文字型（text-based）**，根本不需要 OCR。既有做法卻常常無腦把每一份 PDF 都丟進昂貴又慢（2–10 秒/份）的 OCR 服務。pdf-inspector 的定位就是流水線最前端的「分流器」：先花 ~10–50ms 判斷這份 PDF 到底是文字型還是掃描型，**文字型就地在 200ms 內解析完，掃描型才轉送 OCR**，藉此把大多數文件的成本與延遲砍掉。

它刻意走「輕量」路線：**純 Rust、沒有 ML 模型、沒有外部服務**，PDF 解析只依賴單一套件 `lopdf`。這讓它可以編成 ~5–6MB 的原生 binary，甚至能編成 WebAssembly 在瀏覽器 / Web Worker 裡跑，不需要任何 server round trip。適合報告、論文、財報、發票、法律文件這類「原生文字 PDF」的結構化擷取場景。

## 核心功能

| 功能 | 說明 |
|------|------|
| **智慧分類** | 抽樣 content stream，在 ~10–50ms 內判斷 `TextBased` / `Scanned` / `ImageBased` / `Mixed`，回傳 0.0–1.0 信心分數，並給出**逐頁 OCR 路由**（`pages_needing_ocr`） |
| **位置感知文字擷取** | 帶字型資訊、X/Y 座標，自動處理多欄（newspaper-style）閱讀順序與 RTL |
| **Markdown 轉換** | H1–H4 標題（依字級比例）、項目/數字/字母清單、程式碼區塊（等寬字偵測）、表格、粗斜體、URL 連結、分頁標記 |
| **表格偵測** | 雙模式：從 PDF 繪圖指令的矩形偵測（union-find）＋ 從文字對齊的啟發式偵測；能處理財報表格、註腳、跨頁續表 |
| **CID 字型支援** | Type0/Identity-H 字型的 ToUnicode CMap 解碼，UTF-16BE / UTF-8 / Latin-1 編碼 |
| **編碼問題偵測** | 自動標記壞掉的字型編碼，讓呼叫端可以 fallback 到 OCR |
| **單次載入** | 文件只 parse 一次，偵測與擷取兩階段共用，避免重複 I/O |
| **瀏覽器 WASM** | 同一份 Rust parser 直接在瀏覽器本地跑，內嵌 CMap |

### 分類是怎麼運作的

1. 解析 xref table 與 page tree（**不做完整物件載入**）
2. 依 `ScanStrategy` 選頁（預設掃全部、遇非文字頁 early exit）
3. 在 content stream 找 `Tj`/`TJ`（文字運算子）與 `Do`（影像運算子）
4. 依「抽樣頁面是否有文字運算子」分類

因為不做完整載入，300+ 頁的 PDF 也能在毫秒級判完。結果附帶 `pages_needing_ocr` 清單，達成**逐頁 OCR 路由**，而非全有全無。

**ScanStrategy 策略：**

| 策略 | 行為 | 適用 |
|------|------|------|
| `EarlyExit`（預設） | 掃全部、遇第一個非文字頁就停 | 只想把 TextBased 分流到快速擷取的流水線 |
| `Full` | 掃全部、不 early exit | 需要準確區分 Mixed vs Scanned |
| `Sample(n)` | 均勻抽 n 頁（首/尾/中） | 超大 PDF，速度優先於精度 |
| `Pages(vec)` | 只掃指定頁碼 | 呼叫端已知要檢查哪幾頁 |

### 處理管線架構

```
PDF bytes
  ├─► detector    → PdfType（TextBased / Scanned / ImageBased / Mixed）
  └─► extractor
        ├─ fonts          → 字寬、編碼
        ├─ content_stream → 走訪 PDF 運算子 → TextItems + PdfRects
        ├─ xobjects       → Form XObject 文字、影像佔位
        ├─ links          → 超連結、AcroForm 欄位
        └─ layout         → 欄位偵測 → 分行 → 閱讀順序
              ├─► tables   → 矩形偵測 / 啟發式偵測 / 格線 / 格式化
              └─► markdown → 分析 → 前處理 → 轉換 → 分類 → 後處理
```

文件透過 `load_document_from_path` / `load_document_from_mem` **只載入一次**，偵測與擷取共用，沒有重複 parsing。

## Benchmark

在 [opendataloader-bench](https://github.com/opendataloader-project/opendataloader-bench) 語料庫（200 份 PDF）上評測，僅比較**不含 model-based 解析的本地引擎**，且**關閉 OCR**。分數 0–1，越高越好（更新於 2026-07-31，Apple M4 Pro）：

| 引擎 | 總分 | 閱讀順序 (NID) | 表格 (TEDS) | 標題 (MHS) | 速度（200 份） |
|------|------|------|------|------|------|
| **pdf-inspector** | **0.875** | **0.915** | **0.814** | 0.788 | **0.470s** |
| liteparse | 0.873 | 0.913 | 0.693 | **0.811** | 0.750s |
| opendataloader | 0.831 | 0.902 | 0.489 | 0.739 | 2.569s |
| pymupdf4llm | 0.735 | 0.886 | 0.401 | 0.424 | 17.117s |
| markitdown | 0.589 | 0.844 | 0.273 | 0.000 | 16.165s |

重點：**總分、閱讀順序、表格三項第一，且是全場最快**（比 pymupdf4llm 快約 36 倍、比 markitdown 快約 34 倍）。標題偵測略輸 liteparse。對「原生文字 PDF 要乾淨結構化 Markdown」這個場景，是很強的本地預設選項。

## 快速開始

```bash
# Rust
cargo add pdf-inspector

# Python（需 maturin 從原始碼建置）
pip install maturin && maturin develop --release

# Node.js
npm install @firecrawl/pdf-inspector

# 瀏覽器 WASM
npm install @firecrawl/pdf-inspector-wasm
```

```python
import pdf_inspector
result = pdf_inspector.process_pdf("document.pdf")
print(result.pdf_type)   # "text_based" / "scanned" / "image_based" / "mixed"
print(result.markdown)   # Markdown 字串或 None
```

**CLI（`cargo install pdf-inspector`）：**

```bash
pdf2md document.pdf                    # PDF → Markdown
pdf2md document.pdf --json             # JSON 輸出
pdf2md document.pdf --compact          # 省 token（收合長 dot leaders）
pdf2md document.pdf --select-pages 1,3,5-10
detect-pdf document.pdf --analyze --json   # 只偵測 + 版面分析
```

`--compact` 這種「省 token」旗標很值得注意：它是為了**餵給 LLM** 而設計的，會把 TOC 的長串點點、來源 padding 收成 " ... "。

## 目前限制 / 注意事項

- **不做 OCR**：這是設計取捨而非缺陷。掃描型 / 影像型 PDF 它只負責「認出來並標記」，實際文字還是得靠外部 OCR。它是分流器，不是全能解析器。
- **標題偵測靠字級啟發式**：H1–H4 依字級比例＋0.5pt 分群推斷，粗斜體靠字型名稱樣式（Bold/Italic/Oblique）。遇到不照排版慣例的 PDF 可能誤判（benchmark 上標題分數也確實略輸 liteparse）。
- **Python 需自行建置**：PyPI 有套件，但 README 的 Python 範例走 `maturin develop`，跨平台預編譯輪子的完整度需自行確認。
- **表格是啟發式**：矩形＋對齊雙模式已經很強，但複雜跨頁 / 合併儲存格表格仍是 PDF 解析的通病難題。
- 版本尚在 `0.x`（`0.2.6`），API 可能仍會變動。

## 研究價值與啟示

### 關鍵洞察

1. **「先分類再決定要不要花大錢」是被低估的架構槓桿。** 這個專案最聰明的地方不是解析本身，而是那個 ~20ms 的前置分流：與其優化 OCR，不如先判斷「這份根本不用 OCR」。用便宜的判斷擋掉昂貴的處理，是所有 AI 流水線都適用的成本控制心法。

2. **逐頁 OCR 路由 > 全有全無。** `pages_needing_ocr` 讓 Mixed 型 PDF（例如前面是文字報告、附錄夾了掃描圖）可以只把該掃描的幾頁送 OCR。這種 fine-grained routing 是把成本再壓一階的關鍵，很多解析器缺這一層。

3. **「不用 ML 模型」反而是賣點。** 在人人都上大模型的年代，它反其道而行——純 Rust、單一依賴、5–6MB binary、可編 WASM 在瀏覽器本地跑。對延遲敏感、要地端部署、或不想把文件外送第三方的場景（法律、財報、隱私資料），這種零外部依賴的輕量方案有結構性優勢。

4. **速度本身就是能力，不只是體驗。** 200 份文件 0.47 秒（比 pymupdf4llm 快 ~36 倍）意味著它可以放在「同步請求路徑」上即時判斷，而 16–17 秒級的解析器只能走非同步佇列。速度差一個數量級，架構位置就完全不同。

5. **為 LLM 而生的細節。** `--compact` 收合 dot leaders、分頁標記、乾淨 Markdown 輸出——這些都不是傳統 PDF 工具會在意的，而是「輸出要餵給 LLM」時才會冒出來的需求。它顯示 PDF 解析器正在從「給人看」重新定位成「給模型吃」。

### 與其他專案的關聯

- **[OpenDataLoader PDF](opendataloader-pdf.md)**：直接對照組。兩者都是開源 PDF→Markdown 解析器、都在 opendataloader-bench 上評測。差別在——OpenDataLoader 是 Java 生態、主打 LangChain 整合；pdf-inspector 是 Rust、主打**速度＋免 OCR 分流**，且在同一 benchmark 上總分（0.875 vs 0.831）與速度（0.47s vs 2.57s）都勝出。想做 RAG 前處理的人值得把兩者放一起比。
- **RAG 流水線**：它解決的是 RAG「文件攝取（ingestion）」階段最髒的一段——把任意 PDF 變成乾淨、有結構、省 token 的 Markdown。可視為 RAG chunking 之前的必要前處理層。
- **Firecrawl `/parse` 與 Fire-PDF**：pdf-inspector 是 Firecrawl 商業文件解析服務的開源底層引擎；`/parse` 在它之上再疊自家 OCR 模型（宣稱 0.002s/頁）。這是典型的「開源引擎 + 商業加值層」商業模式——核心開源換取採用與信任，OCR/雲端服務變現。

---

_研究日期：2026-08-03。Metadata（★ 數、版本）為擷取當下數值，可能隨時間變動。_
