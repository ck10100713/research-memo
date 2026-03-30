#!/usr/bin/env python3
"""sync.py — 從 docs/*.md frontmatter + mkdocs.yml nav 自動生成 index.md 和 news.md"""

import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ── 設定 ──────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
INDEX_MD = DOCS / "index.md"
NEWS_MD = DOCS / "news.md"

RECENT_CARDS_LIMIT = 17  # 研究更新區塊顯示的最大卡片數

# 不需要 frontmatter 的特殊頁面
SKIP_FILES = {"index.md", "news.md"}

# ── Frontmatter 解析 ─────────────────────────────────

def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """解析 YAML frontmatter，回傳 (metadata_dict, h1_title)"""
    text = filepath.read_text(encoding="utf-8")
    meta = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(text[3:end]) or {}
            except yaml.YAMLError:
                pass
            text = text[end + 3:].lstrip("\n")

    # 提取 H1 title
    title = ""
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
        # 移除尾部「研究筆記」
        title = re.sub(r"\s*研究筆記$", "", title)
    return meta, title


# ── mkdocs.yml nav 解析 ──────────────────────────────

def parse_nav(mkdocs_yml: Path) -> list[tuple[str, list[tuple[str, str]]]]:
    """用 regex 解析 mkdocs.yml nav 段落（避免 !!python/name 標籤問題）。
    回傳 [(category_name, [(title, slug), ...])]，跳過首頁和研究更新。"""
    text = mkdocs_yml.read_text(encoding="utf-8")

    # 擷取 nav: 到下一個頂層 key（如 extra:）之間的文字
    nav_match = re.search(r"^nav:\s*\n((?:[ \t].*\n)*)", text, re.MULTILINE)
    if not nav_match:
        return []

    nav_text = nav_match.group(1)
    categories = []
    current_cat = None
    current_docs = []

    for line in nav_text.splitlines():
        # 分類標題行：「  - AI Agent 框架:」（2 空格縮排）
        cat_match = re.match(r"^  - (.+):$", line)
        if cat_match:
            # 儲存前一個分類
            if current_cat and current_docs:
                categories.append((current_cat, current_docs))
            current_cat = cat_match.group(1).strip()
            current_docs = []
            continue

        # 頂層頁面行：「  - 首頁: index.md」（2 空格，值是 .md）
        top_match = re.match(r"^  - .+:\s+\S+\.md$", line)
        if top_match:
            # 儲存前一個分類
            if current_cat and current_docs:
                categories.append((current_cat, current_docs))
            current_cat = None
            current_docs = []
            continue

        # 子條目行：「      - Title: slug.md」（6 空格縮排）
        doc_match = re.match(r"^      - (.+?):\s+(\S+\.md)$", line)
        if doc_match and current_cat:
            title = doc_match.group(1).strip()
            slug = doc_match.group(2).strip()
            current_docs.append((title, slug))

    # 最後一個分類
    if current_cat and current_docs:
        categories.append((current_cat, current_docs))

    return categories


# ── 驗證 ─────────────────────────────────────────────

def validate(categories, all_docs_meta):
    """驗證 nav 和 docs 的一致性，回傳 errors 列表"""
    errors = []
    warnings = []

    # nav 中所有 slug
    nav_slugs = set()
    for _, docs_in_cat in categories:
        for _, slug in docs_in_cat:
            nav_slugs.add(slug)

    # 實際 docs 檔案
    actual_files = {f.name for f in DOCS.glob("*.md") if f.name not in SKIP_FILES}

    # 檢查 nav 指向不存在的檔案
    for slug in nav_slugs:
        if slug not in actual_files:
            errors.append(f"NAV ERROR: {slug} 在 mkdocs.yml nav 中但檔案不存在")

    # 檢查檔案不在 nav 中
    for fname in actual_files:
        if fname not in nav_slugs:
            errors.append(f"ORPHAN: {fname} 存在於 docs/ 但不在 mkdocs.yml nav 中（會 404）")

    # 檢查缺少 frontmatter
    for slug, (meta, _) in all_docs_meta.items():
        if not meta.get("date"):
            warnings.append(f"WARNING: {slug} 缺少 frontmatter date")
        if not meta.get("category"):
            warnings.append(f"WARNING: {slug} 缺少 frontmatter category")
        if not meta.get("card_icon"):
            warnings.append(f"WARNING: {slug} 缺少 frontmatter icon")
        if not meta.get("oneliner"):
            warnings.append(f"WARNING: {slug} 缺少 frontmatter oneliner")

    return errors, warnings


# ── index.md 生成 ────────────────────────────────────

def generate_index(categories, all_docs_meta):
    """生成 index.md 內容"""
    lines = []
    lines.append("# Research Memo")
    lines.append("")
    lines.append("研究與整理感興趣的技術專案、架構模式與工具鏈。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 研究更新（最近 N 篇）──
    lines.append("## 研究更新")
    lines.append("")
    lines.append("最近新增或整理完成的研究筆記。")
    lines.append("")
    lines.append('<div class="grid cards" markdown>')
    lines.append("")

    # 收集所有有日期的 docs，按日期降序
    dated_docs = []
    for slug, (meta, title) in all_docs_meta.items():
        if meta.get("date") and meta.get("card_icon") and meta.get("oneliner"):
            dated_docs.append((meta["date"], slug, meta, title))
    dated_docs.sort(key=lambda x: x[0], reverse=True)

    for date, slug, meta, title in dated_docs[:RECENT_CARDS_LIMIT]:
        lines.append(f'-   :{meta["card_icon"]}:{{{{ .lg .middle }}}} **{title}**')
        lines.append("")
        lines.append("    ---")
        lines.append("")
        lines.append(f'    `{date}` {meta["oneliner"]}')
        lines.append("")
        lines.append(f"    [:octicons-arrow-right-24: 閱讀筆記]({slug})")
        lines.append("")

    lines.append("</div>")
    lines.append("")
    lines.append("[查看研究索引](news.md)")
    lines.append("")

    # ── 各分類區塊 ──
    for cat_name, docs_in_cat in categories:
        lines.append("---")
        lines.append("")
        lines.append(f"## {cat_name}")
        lines.append("")
        lines.append('<div class="grid cards" markdown>')
        lines.append("")

        for doc_title, slug in docs_in_cat:
            meta, title = all_docs_meta.get(slug, ({}, doc_title))
            icon = meta.get("card_icon", "material-file-document-outline")
            oneliner = meta.get("oneliner", "")
            display_title = title or doc_title

            lines.append(f"-   :{icon}:{{{{ .lg .middle }}}} **{display_title}**")
            lines.append("")
            lines.append("    ---")
            lines.append("")
            lines.append(f"    {oneliner}")
            lines.append("")
            lines.append(f"    [:octicons-arrow-right-24: 閱讀筆記]({slug})")
            lines.append("")

        lines.append("</div>")
        lines.append("")

    return "\n".join(lines)


# ── news.md 生成 ─────────────────────────────────────

def generate_news(categories, all_docs_meta):
    """生成 news.md 內容"""
    lines = []
    lines.append("# 研究更新")
    lines.append("")
    lines.append("這頁是研究資料庫的更新索引，提供最新整理、按年份 / 月份、按主題三種入口。")
    lines.append("")
    lines.append("> 日期以文章內標註的「建立日期 / 研究日期 / 發布日期」為主；"
                 "若文章保留的是專案建立日，也依原文收錄。尚未標註日期的文章，統一收在下方的主題索引。")
    lines.append("")

    # 收集所有有日期的 docs
    dated_docs = []
    undated_docs = []
    for slug, (meta, title) in all_docs_meta.items():
        if meta.get("date"):
            dated_docs.append((meta["date"], slug, meta, title))
        else:
            undated_docs.append((slug, meta, title))
    dated_docs.sort(key=lambda x: x[0], reverse=True)

    # ── 最新整理 ──
    lines.append("## 最新整理")
    lines.append("")
    lines.append("| 日期 | 類型 | 文章 |")
    lines.append("| --- | --- | --- |")
    for date, slug, meta, title in dated_docs:
        cat = meta.get("category", "未分類")
        lines.append(f"| {date} | {cat} | [{title}]({slug}) |")
    lines.append("")

    # ── 按年份 / 月份 ──
    lines.append("## 按年份 / 月份")
    lines.append("")

    # 分組
    by_year_month = defaultdict(list)
    for date, slug, meta, title in dated_docs:
        parts = date.split("-")
        if len(parts) >= 2:
            year, month = parts[0], parts[1]
            by_year_month[(year, month)].append((date, slug, meta, title))

    current_year = None
    for (year, month), items in sorted(by_year_month.items(), reverse=True):
        if year != current_year:
            lines.append(f"### {year} 年")
            lines.append("")
            current_year = year
        lines.append(f"#### {month} 月")
        lines.append("")
        for date, slug, meta, title in items:
            oneliner = meta.get("oneliner", "")
            if oneliner:
                lines.append(f"- `{date}` [{title}]({slug})  ")
                lines.append(f"  {oneliner}")
            else:
                lines.append(f"- `{date}` [{title}]({slug})")
        lines.append("")

    # ── 按主題 ──
    lines.append("## 按主題")
    lines.append("")

    for cat_name, docs_in_cat in categories:
        lines.append(f"### {cat_name}")
        lines.append("")
        links = []
        for doc_title, slug in docs_in_cat:
            _, title = all_docs_meta.get(slug, ({}, doc_title))
            display = title or doc_title
            links.append(f"[{display}]({slug})")
        lines.append("、".join(links))
        lines.append("")

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────

def main():
    # 1. 解析 nav
    categories = parse_nav(MKDOCS_YML)

    # 2. 解析所有 docs 的 frontmatter
    all_docs_meta = {}
    for f in DOCS.glob("*.md"):
        if f.name in SKIP_FILES:
            continue
        meta, title = parse_frontmatter(f)
        all_docs_meta[f.name] = (meta, title)

    # 3. 驗證
    errors, warnings = validate(categories, all_docs_meta)
    for w in warnings:
        print(w, file=sys.stderr)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"\n{len(errors)} error(s) found. Fix them before building.", file=sys.stderr)
        sys.exit(1)

    # 4. 生成 index.md
    index_content = generate_index(categories, all_docs_meta)
    INDEX_MD.write_text(index_content, encoding="utf-8")
    print(f"✓ Generated {INDEX_MD.relative_to(ROOT)}")

    # 5. 生成 news.md
    news_content = generate_news(categories, all_docs_meta)
    NEWS_MD.write_text(news_content, encoding="utf-8")
    print(f"✓ Generated {NEWS_MD.relative_to(ROOT)}")

    print(f"✓ {len(all_docs_meta)} docs processed, 0 errors")


if __name__ == "__main__":
    main()
