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
> ./scripts/build_pdf.sh
> ```
>
> 字型刻意用 Noto Sans CJK TC 而非蘋方：蘋方在 PDF 裡的字型名是中文（「蘋方-繁」），
> 部分閱讀器認不得，整份文件會顯示成方塊。`scripts/pdf_charfix.py` 另外把 Noto 沒有的
> 符號換掉，避免拖進 Apple Color Emoji（sbix 點陣字型，相容性同樣不好）。
