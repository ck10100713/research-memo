#!/usr/bin/env python3
"""stdin → stdout：把 Noto Sans CJK 沒有的字換掉。

這 7 個字元（共出現 14 次）會害 WeasyPrint 去抓 Apple Color Emoji 與 .SF-Compact，
前者是 sbix 點陣字型、後者是 Apple 內部字型，都有閱讀器讀不出來的紀錄。
清單用 scripts/build_pdf.sh 註解裡的 fontTools 掃描法重新產生。
"""
import sys

SUBS = {
    '️': '',        # variation selector-16，會逼出彩色 emoji 呈現
    '✅': '✓',  # ✅ → ✓
    '❌': '×',  # ❌ → ×（✗ U+2717 本身也不在 Noto CJK TC 裡，別拿它當替代）
    '⭐': '★',  # ⭐ → ★
    # 🆕 其實在 Noto CJK TC 的 cmap 裡，但它是 Emoji_Presentation=Yes，
    # Pango 照樣改派 emoji 字型 —— 所以「查得到字」不等於「不會 fallback」。
    '🆕': '[新]',
    '\U0001f534': '●',  # 🔴 → ●（TDD 圖，旁邊就有 Red 字樣）
    '\U0001f7e2': '●',  # 🟢 → ●
    '\U0001f535': '●',  # 🔵 → ●
}
TABLE = str.maketrans(SUBS)

def demo():
    assert '✅❌⭐'.translate(TABLE) == '✓×★'
    assert '⚠️'.translate(TABLE) == '⚠'
    assert '正常中文 abc'.translate(TABLE) == '正常中文 abc'
    print('charfix ok')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        sys.stdout.write(sys.stdin.read().translate(TABLE))
