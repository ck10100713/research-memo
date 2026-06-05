---
date: "2026-06-05"
category: "Agent Skills"
skill_type: "research"
card_icon: "material-text-box-search-outline"
oneliner: "本站自用的研究筆記產生器 skill：搜集資料 → 結構化筆記 → 更新索引 → 部署"
tags:
  - skills
  - knowledge-base
---

# research（研究筆記產生器）

## 資料來源

| 項目 | 連結 |
|------|------|
| Skill 檔案 | [`.claude/skills/research/SKILL.md`](https://github.com/ck10100713/research-memo/blob/main/.claude/skills/research/SKILL.md) |
| 作者 | 本站（ck10100713 / research-memo） |

## Skill 概述

`/research <主題或URL>` 是本站的核心工作流 skill：使用者給一個 GitHub repo、技術名詞或任何關鍵字，agent 負責搜集資料、寫成結構化繁中筆記、加入 MkDocs 網站並 commit 部署。它把「研究 → 寫作 → 發布」固化成五個步驟，確保每篇筆記的 frontmatter、分類、標籤與索引一致。

## 安全審查結果

- **審查日期**：2026-06-05
- **檢查範圍**：`SKILL.md` 全文（無 scripts/hooks 附件）
- **結果**：🟢 通過
- **備註**：skill 僅指示讀寫專案內檔案、呼叫 `gh api` 讀取公開 repo、執行專案內 `scripts/sync.py`、git commit/push 到自有 repo；無外部指令執行、無憑證存取。

## 工作流程（繁中原文整理）

| 步驟 | 內容 |
|------|------|
| Step 0 | 檢查 `docs/` 是否已有筆記，已存在必須先問使用者 |
| Step 1 | 判斷來源（GitHub URL 用 `gh api`；一般主題用 WebSearch/WebFetch），多來源搜集 |
| Step 2 | 撰寫筆記：YAML frontmatter（date/category/card_icon/oneliner/tags）+ 固定結構模板 |
| Step 3 | 按內容本質選分類、更新 `mkdocs.yml` nav；新分類需同步補三處 |
| Step 4 | 執行 `scripts/sync.py` 自動重建 index/news/topics |
| Step 5 | `gh auth status` 確認帳號 → commit → push |

設計重點：

- **tag hygiene**：標籤詞彙表集中維護在 skill 內，優先沿用、避免同義詞
- **分類三處同步**：nav topics 行 + `CATEGORY_SLUGS` + `CATEGORY_ICONS`，漏一處就會壞
- **生成頁不手編**：index/news/topics 全部由 sync.py 重建，人只寫 `docs/<slug>.md`

??? note "原文（繁體中文，節錄自 SKILL.md）"

    完整原文見 [`.claude/skills/research/SKILL.md`](https://github.com/ck10100713/research-memo/blob/main/.claude/skills/research/SKILL.md)。
