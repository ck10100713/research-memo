#!/usr/bin/env bash
# books/*.md → books/pdf/*.pdf（mermaid → SVG、pandoc → HTML、WeasyPrint → PDF）
#
# 三個不明顯但必要的選擇：
#   1. 字型用 ASCII 名的 Noto CJK。蘋方在 PDF 裡的字型名是中文「蘋方-繁」，部分閱讀器認不得，整份變方塊。
#   2. mermaid 關掉 htmlLabels。預設會用 SVG 的 <foreignObject> 包 HTML，WeasyPrint 不支援，圖上的字會消失。
#   3. 書內那份純文字目錄砍掉改用 pandoc --toc，因為 pandoc 會自己算錨點，目錄在 PDF 裡才點得動。
set -euo pipefail
cd "$(dirname "$0")/.."

MMDC=${MMDC:-mmdc}
CHROME=${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}
build=books/build            # mermaid 產物放這，下次沒改就不重畫（256 張圖要跑好幾分鐘）
mkdir -p "$build" books/pdf
cp books/book.css "$build/"

for f in books/*.md; do
  n=$(basename "$f" .md); [ "$n" = README ] && continue
  t=$(head -1 "$f" | sed 's/^# //')
  src="$build/$n.src.md"; rendered="$build/$n.md"

  # 書名抽成 metadata；awk 砍掉書內目錄（留到第一個「# 篇」為止）；再換掉 Noto 沒有的字元
  tail -n +2 "$f" | awk '/^# /{p=1} p' | python3 scripts/pdf_charfix.py > "$src"

  if [ ! -f "$rendered" ] || [ "$src" -nt "$rendered" ]; then
    echo "  ${n}：$(grep -c '^```mermaid' "$src" || true) 張圖"
    MMDC="$MMDC" CHROME="$CHROME" python3 scripts/render_mermaid.py "$src" "$rendered" "$build/svg" "$MMDC"
  fi

  pandoc "$rendered" -s --toc --toc-depth=3 -M title="$t" -c book.css -o "$build/$n.html"
  weasyprint "$build/$n.html" "books/pdf/$n.pdf" 2>/dev/null
  echo "books/pdf/$n.pdf  $(du -h "books/pdf/$n.pdf" | cut -f1)"
done
