# books/

由 [ccc115a/se](https://github.com/ccc115a/se) 的 [`_more/mybook`](https://github.com/ccc115a/se/tree/main/_more/mybook)
合併而成的單檔書籍。原始內容一節一個 `.md`，這裡照各書 `README.md` 的目錄順序組成整本。

| 檔案 | 原始書名 | 節數 |
|---|---|---|
| `現代軟體工程.md` | 現代軟體工程：從基礎到 AI Agent 實踐 | 87 |
| `向淘寶學習網站架構演進.md` | 演進式架構實戰：從單體、微服務到 Docker、Kubernetes 與 AI 雲原生轉型 | 75 |
| `docker2k8s.md` | 從 Docker 到 Kubernetes：Rust 與多樣化 Web 架構（WebSocket / SSR / MPA）實戰 | 46 |

`pdf/` 是同樣內容的 A4 排版 PDF（pandoc → WeasyPrint）。

## 重新產生

```bash
python3 scripts/build_book.py <se-repo>/_more/mybook books/
```

## 授權

原著作者 **陳鍾誠**（金門大學資訊工程學系），採 **MIT License**，版權聲明見
<https://github.com/ccc115a/se/blob/main/LICENSE>。本目錄僅做格式合併，未修改內容。

研究筆記：[`docs/ccc115a-se-mybook.md`](../docs/ccc115a-se-mybook.md)

> `pdf/` 不進版控（見 `.gitignore`）。要產 PDF：
>
> ```bash
> ./scripts/build_pdf.sh          # 需要 pandoc、weasyprint、mermaid-cli（mmdc）
> ```
>
> PDF 帶側邊書籤與可點目錄，mermaid 圖會先渲染成 SVG。中間產物放 `books/build/`
> （也不進版控），圖以內容 hash 快取，只有改動過的會重畫。

### 三個排版上的坑

| 症狀 | 原因 | 作法 |
|---|---|---|
| 整份 PDF 顯示成方塊 | 蘋方在 PDF 裡的字型名是中文「蘋方-繁」，部分閱讀器認不得 | 改用 ASCII 名的 Noto Sans CJK TC |
| 圖上的字不見 | mermaid 預設用 SVG 的 `<foreignObject>` 包 HTML，WeasyPrint 不支援 | `htmlLabels: false` |
| 莫名拖進 Apple Color Emoji | 少數符號 Noto 沒有，或雖有但屬 `Emoji_Presentation=Yes` | `scripts/pdf_charfix.py` 換掉 |
