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
> for f in books/*.md; do
>   n=$(basename "$f" .md); t=$(head -1 "$f" | sed 's/^# //')
>   tail -n +2 "$f" | pandoc -s --toc --toc-depth=3 -M title="$t" -c book.css -o "/tmp/$n.html"
>   weasyprint "/tmp/$n.html" "books/pdf/$n.pdf"
> done
> ```
