#!/usr/bin/env python3
"""migrate_frontmatter.py — 一次性腳本：為現有 docs 加上 YAML frontmatter

從 mkdocs.yml、index.md、news.md 提取 category、icon、oneliner、date，
然後 prepend 到每個 doc 的開頭。

用法：python scripts/migrate_frontmatter.py [--dry-run]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
INDEX_MD = DOCS / "index.md"
NEWS_MD = DOCS / "news.md"

SKIP_FILES = {"index.md", "news.md"}


def parse_nav_categories(mkdocs_yml: Path) -> dict[str, str]:
    """用 regex 解析 mkdocs.yml nav，回傳 {slug: category_name}"""
    text = mkdocs_yml.read_text(encoding="utf-8")
    nav_match = re.search(r"^nav:\s*\n((?:[ \t].*\n)*)", text, re.MULTILINE)
    if not nav_match:
        return {}

    result = {}
    current_cat = None
    for line in nav_match.group(1).splitlines():
        cat_match = re.match(r"^  - (.+):$", line)
        if cat_match:
            current_cat = cat_match.group(1).strip()
            continue
        top_match = re.match(r"^  - .+:\s+\S+\.md$", line)
        if top_match:
            current_cat = None
            continue
        doc_match = re.match(r"^      - .+?:\s+(\S+\.md)$", line)
        if doc_match and current_cat:
            result[doc_match.group(1).strip()] = current_cat
    return result


def parse_index_cards(index_md: Path) -> dict[str, dict]:
    """從 index.md 的 grid cards 提取 icon 和 oneliner。
    回傳 {slug: {"icon": ..., "oneliner": ...}}"""
    text = index_md.read_text(encoding="utf-8")
    result = {}

    # 逐塊解析：每張卡片以 `-   :` 開頭，到下一張卡片或 </div> 結束
    cards = re.split(r'\n(?=-\s+:)', text)

    for card in cards:
        # 提取 icon
        icon_m = re.search(r':([\w-]+):\{\s*\.lg\s+\.middle\s*\}', card)
        if not icon_m:
            continue
        icon = icon_m.group(1)

        # 提取 slug
        slug_m = re.search(r'\[:octicons-arrow-right-24:\s*閱讀筆記\]\((.+?\.md)\)', card)
        if not slug_m:
            continue
        slug = slug_m.group(1)

        # 提取 oneliner：在 --- 和 [:octicons 之間的文字
        desc_m = re.search(r'---\s*\n\s*\n\s*(.*?)\s*\n\s*\n\s*\[:octicons', card, re.DOTALL)
        oneliner = ""
        if desc_m:
            raw = desc_m.group(1).strip()
            # 移除開頭的日期標記 `2026-03-30`
            raw = re.sub(r'^`[\d-]+`\s*', '', raw)
            oneliner = raw

        if slug not in result or len(oneliner) > len(result[slug].get("oneliner", "")):
            result[slug] = {"icon": icon, "oneliner": oneliner}

    return result


def parse_news_dates(news_md: Path) -> dict[str, str]:
    """從 news.md 的「最新整理」表格提取日期。
    回傳 {slug: date_string}"""
    text = news_md.read_text(encoding="utf-8")
    result = {}

    # 匹配表格行：| 2026-03-30 | ... | [...](slug.md) |
    pattern = re.compile(r'\|\s*([\d-]+)\s*\|[^|]+\|\s*\[.+?\]\((.+?\.md)\)')
    for m in pattern.finditer(text):
        date = m.group(1)
        slug = m.group(2)
        # 保留最早的日期（如果同一個 slug 出現多次，例如更新條目）
        if slug not in result:
            result[slug] = date

    # 也從「按年份/月份」區塊提取
    pattern2 = re.compile(r'`([\d-]+)`\s*\[.+?\]\((.+?\.md)\)')
    for m in pattern2.finditer(text):
        date = m.group(1)
        slug = m.group(2)
        if slug not in result:
            result[slug] = date

    return result


def has_frontmatter(filepath: Path) -> bool:
    """檢查檔案是否已有 frontmatter"""
    text = filepath.read_text(encoding="utf-8")
    return text.startswith("---")


def add_frontmatter(filepath: Path, meta: dict, dry_run: bool = False):
    """在檔案開頭加入 YAML frontmatter"""
    text = filepath.read_text(encoding="utf-8")

    fm_lines = ["---"]
    fm_lines.append(f'date: "{meta.get("date", "")}"')
    fm_lines.append(f'category: "{meta.get("category", "")}"')
    fm_lines.append(f'icon: "{meta.get("icon", "material-file-document-outline")}"')
    # oneliner 可能含引號，用 YAML block scalar 或轉義
    oneliner = meta.get("oneliner", "").replace('"', '\\"')
    fm_lines.append(f'oneliner: "{oneliner}"')
    fm_lines.append("---")
    fm_lines.append("")

    new_text = "\n".join(fm_lines) + text

    if dry_run:
        print(f"  [DRY RUN] Would add frontmatter to {filepath.name}")
        for line in fm_lines:
            print(f"    {line}")
    else:
        filepath.write_text(new_text, encoding="utf-8")
        print(f"  ✓ {filepath.name}")


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE ===\n")

    # 1. 從 mkdocs.yml 取得 category
    slug_to_cat = parse_nav_categories(MKDOCS_YML)
    print(f"從 mkdocs.yml 取得 {len(slug_to_cat)} 個 nav 條目")

    # 2. 從 index.md 取得 icon 和 oneliner
    slug_to_card = parse_index_cards(INDEX_MD)
    print(f"從 index.md 取得 {len(slug_to_card)} 個卡片資料")

    # 3. 從 news.md 取得 date
    slug_to_date = parse_news_dates(NEWS_MD)
    print(f"從 news.md 取得 {len(slug_to_date)} 個日期")

    print()

    # 4. 遷移
    migrated = 0
    skipped = 0
    missing_info = []

    for f in sorted(DOCS.glob("*.md")):
        if f.name in SKIP_FILES:
            continue

        if has_frontmatter(f):
            skipped += 1
            continue

        slug = f.name
        meta = {
            "date": slug_to_date.get(slug, ""),
            "category": slug_to_cat.get(slug, ""),
            "icon": slug_to_card.get(slug, {}).get("icon", "material-file-document-outline"),
            "oneliner": slug_to_card.get(slug, {}).get("oneliner", ""),
        }

        # 記錄缺少資訊的
        missing = [k for k, v in meta.items() if not v]
        if missing:
            missing_info.append((slug, missing))

        add_frontmatter(f, meta, dry_run=dry_run)
        migrated += 1

    print(f"\n遷移完成：{migrated} 已處理，{skipped} 已跳過（已有 frontmatter）")

    if missing_info:
        print(f"\n⚠ 以下 {len(missing_info)} 個檔案有缺少的欄位（需手動補充）：")
        for slug, fields in missing_info:
            print(f"  {slug}: 缺少 {', '.join(fields)}")


if __name__ == "__main__":
    main()
