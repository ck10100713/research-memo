#!/usr/bin/env bash
# books/*.md → books/pdf/*.pdf（pandoc → HTML → WeasyPrint）
# 字型刻意用 ASCII 名的 Noto CJK：蘋方等系統字型的名字是中文，部分 PDF 閱讀器認不得會顯示成方塊。
set -euo pipefail
cd "$(dirname "$0")/.."
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cp books/book.css "$work/"
mkdir -p books/pdf
for f in books/*.md; do
  n=$(basename "$f" .md); [ "$n" = README ] && continue
  t=$(head -1 "$f" | sed 's/^# //')
  # 書名抽成 metadata 後從正文移除；不用 --toc，書內第一節已經是自己的目錄
  # 先換掉 Noto CJK 沒有的字元，否則 WeasyPrint 會去抓 Apple Color Emoji（sbix 點陣字型）。
  # 缺字清單怎麼重新掃：用 fontTools 讀 NotoSansCJK.ttc 的 cmap，跟 books/*.md 的字元集取差集。
  tail -n +2 "$f" | python3 scripts/pdf_charfix.py \
    | pandoc -f markdown -s -M title="$t" -c book.css -o "$work/$n.html"
  weasyprint "$work/$n.html" "books/pdf/$n.pdf" 2>/dev/null
  echo "books/pdf/$n.pdf  $(du -h "books/pdf/$n.pdf" | cut -f1)"
done
echo "--- 內嵌字型（應全為 ASCII 名）---"
pdffonts books/pdf/*.pdf 2>/dev/null | awk 'NR>2 && $1!="" {sub(/^[A-Z]{6}\+/,"",$1); print $1}' | sort -u
