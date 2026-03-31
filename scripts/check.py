#!/usr/bin/env python3
"""check.py — 檢查 docs/*.md frontmatter 完整性、nav 一致性，可自動修復缺失欄位。

用法：
  python3 scripts/check.py          # 只檢查，列出所有問題
  python3 scripts/check.py --fix    # 自動修復可修復的問題（目前：補 date from git log）
"""

import argparse
import re
import subprocess
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ── 設定 ──────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
SKIP_FILES = {"index.md", "news.md"}

REQUIRED_FIELDS = ["date", "category", "card_icon", "oneliner"]

# ANSI colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ── Frontmatter 解析 ─────────────────────────────────

def parse_frontmatter(filepath: Path) -> dict:
    """解析 YAML frontmatter，回傳 metadata dict"""
    text = filepath.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            try:
                return yaml.safe_load(text[3:end]) or {}
            except yaml.YAMLError:
                return {}
    return {}


def set_frontmatter_field(filepath: Path, field: str, value: str):
    """在既有 frontmatter 中設定或新增一個欄位"""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False

    end = text.find("---", 3)
    if end == -1:
        return False

    fm_text = text[3:end]
    rest = text[end:]  # 包含 closing ---

    # 檢查欄位是否已存在（空值）
    pattern = rf'^({field}:\s*)(""|\'\'|\s*)$'
    match = re.search(pattern, fm_text, re.MULTILINE)
    if match:
        # 替換空值
        fm_text = fm_text[:match.start()] + f'{field}: "{value}"' + fm_text[match.end():]
    else:
        # 新增欄位（加在最後一行之前）
        fm_text = fm_text.rstrip("\n") + f'\n{field}: "{value}"\n'

    filepath.write_text("---" + fm_text + rest, encoding="utf-8")
    return True


# ── Git 工具 ─────────────────────────────────────────

def git_first_commit_date(filepath: Path) -> str | None:
    """取得檔案首次 commit 的日期（ISO 格式）"""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", str(filepath)],
            capture_output=True, text=True, cwd=ROOT,
        )
        dates = result.stdout.strip().splitlines()
        if dates:
            # 取最早的日期，格式化為 YYYY-MM-DD
            return dates[-1][:10]
    except Exception:
        pass
    return None


def git_last_commit_date(filepath: Path) -> str | None:
    """取得檔案最近 commit 的日期（ISO 格式）"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(filepath)],
            capture_output=True, text=True, cwd=ROOT,
        )
        date = result.stdout.strip()
        if date:
            return date[:10]
    except Exception:
        pass
    return None


# ── mkdocs.yml nav 解析 ──────────────────────────────

def parse_nav_categories(mkdocs_yml: Path) -> dict[str, str]:
    """回傳 {slug: category_name} 的 mapping"""
    text = mkdocs_yml.read_text(encoding="utf-8")
    nav_match = re.search(r"^nav:\s*\n((?:[ \t].*\n)*)", text, re.MULTILINE)
    if not nav_match:
        return {}

    slug_to_cat = {}
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
            slug_to_cat[doc_match.group(1).strip()] = current_cat

    return slug_to_cat


# ── 主檢查邏輯 ───────────────────────────────────────

def check_all(fix: bool = False) -> int:
    """執行所有檢查，回傳問題數量"""
    nav_map = parse_nav_categories(MKDOCS_YML)
    nav_slugs = set(nav_map.keys())
    actual_files = {f.name for f in DOCS.glob("*.md") if f.name not in SKIP_FILES}

    errors = []      # 會導致 404 或功能異常
    fixed = []       # 自動修復的項目

    # ── 1. Nav 一致性 ──

    # 孤兒檔案（在 docs/ 但不在 nav）
    for fname in sorted(actual_files - nav_slugs):
        errors.append(f"ORPHAN  {fname} — 在 docs/ 但不在 mkdocs.yml nav（會 404）")

    # 幽靈條目（在 nav 但檔案不存在）
    for slug in sorted(nav_slugs - actual_files):
        errors.append(f"GHOST   {slug} — 在 mkdocs.yml nav 但檔案不存在")

    # ── 2. Frontmatter 完整性 ──

    missing_by_field = defaultdict(list)

    for fname in sorted(actual_files):
        filepath = DOCS / fname
        meta = parse_frontmatter(filepath)

        for field in REQUIRED_FIELDS:
            val = meta.get(field)
            if not val or (isinstance(val, str) and not val.strip()):
                missing_by_field[field].append(fname)

                if fix and field == "date":
                    # 嘗試從 git log 補日期
                    git_date = git_first_commit_date(filepath)
                    if not git_date:
                        git_date = git_last_commit_date(filepath)
                    if git_date:
                        if set_frontmatter_field(filepath, "date", git_date):
                            fixed.append(f"date    {fname} ← {git_date} (from git log)")
                            missing_by_field[field].remove(fname)

    # ── 3. Category 一致性 ──

    cat_mismatches = []
    for fname in sorted(actual_files & nav_slugs):
        meta = parse_frontmatter(DOCS / fname)
        fm_cat = meta.get("category", "")
        nav_cat = nav_map.get(fname, "")
        if fm_cat and nav_cat and fm_cat != nav_cat:
            cat_mismatches.append((fname, fm_cat, nav_cat))

    # ── 輸出報告 ──

    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  Research Memo — Docs 健康檢查{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    total_docs = len(actual_files)
    total_issues = 0

    # Nav 問題
    if errors:
        print(f"{RED}{BOLD}NAV 問題（會 404）{RESET}")
        for e in errors:
            print(f"  {RED}✗{RESET} {e}")
        print()
        total_issues += len(errors)

    # Frontmatter 缺失
    for field in REQUIRED_FIELDS:
        missing = missing_by_field[field]
        if missing:
            severity = RED if field in ("date", "oneliner") else YELLOW
            print(f"{severity}{BOLD}缺少 {field}（{len(missing)} 篇）{RESET}")
            for fname in missing:
                print(f"  {severity}✗{RESET} {fname}")
            print()
            total_issues += len(missing)

    # Category 不一致
    if cat_mismatches:
        print(f"{YELLOW}{BOLD}Category 不一致（frontmatter ≠ nav）{RESET}")
        for fname, fm_cat, nav_cat in cat_mismatches:
            print(f"  {YELLOW}✗{RESET} {fname}: frontmatter={fm_cat!r} nav={nav_cat!r}")
        print()
        total_issues += len(cat_mismatches)

    # 自動修復結果
    if fixed:
        print(f"{GREEN}{BOLD}已自動修復（{len(fixed)} 項）{RESET}")
        for f in fixed:
            print(f"  {GREEN}✓{RESET} {f}")
        print()

    # 摘要
    healthy = total_docs - len(set(
        f for files in missing_by_field.values() for f in files
    ) | {e.split()[1] for e in errors} | {m[0] for m in cat_mismatches})

    print(f"{BOLD}{'─' * 60}{RESET}")
    print(f"  總計 {total_docs} 篇文件")
    print(f"  {GREEN}✓ {healthy} 篇完全健康{RESET}")
    if total_issues > 0:
        print(f"  {RED}✗ {total_issues} 個問題待修復{RESET}")
    if fixed:
        print(f"  {GREEN}⚡ {len(fixed)} 個已自動修復（需 commit）{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    if total_issues > 0 and not fix:
        print(f"{CYAN}提示：執行 python3 scripts/check.py --fix 可自動補上缺失的 date（from git log）{RESET}\n")

    return total_issues


# ── Entry point ──────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="檢查 docs frontmatter 完整性與 nav 一致性")
    parser.add_argument("--fix", action="store_true", help="自動修復可修復的問題（date from git log）")
    args = parser.parse_args()

    issues = check_all(fix=args.fix)
    sys.exit(1 if issues > 0 else 0)


if __name__ == "__main__":
    main()
