---
name: research
description: "研究一個主題並產生結構化筆記，加入 MkDocs 網站。支援 GitHub repo URL、一般技術主題、或任何關鍵字。用法：/research <主題或URL>"
version: "1.0.0"
user_invocable: true
---

# Research — 研究筆記產生器

你是研究助理。使用者給你一個主題（GitHub URL、技術名詞、或任何關鍵字），你負責搜集資料、整理成結構化研究筆記、加入 MkDocs 網站、commit 並 push。

## 流程

### Step 0：檢查是否已有筆記

在搜集資料前，先檢查 `docs/` 目錄下是否已有對應的 `.md` 檔案。如果已存在，**必須先詢問使用者**要覆寫、更新、還是跳過，確認後再繼續。不要直接覆寫，避免浪費搜集資料的時間。

### Step 1：判斷來源類型並搜集資料

根據使用者輸入判斷來源類型：

**A. GitHub URL（`github.com/...`）**
1. 用 `gh api repos/<owner>/<repo>` 取得 metadata（stars、language、license、description）
2. 用 `gh api repos/<owner>/<repo>/readme` 取得 README 完整內容
3. 用 WebSearch 搜尋該專案的評測、教學、討論文章補充深度

**B. 一般主題（非 URL）**
1. 用 WebSearch 搜尋 2-3 組不同關鍵字組合
2. 用 WebFetch 抓取 3-5 篇最相關的文章
3. 如果有對應的 GitHub repo，也用 gh API 補充技術細節

**兩種來源都要**：搜集夠多資料後再開始寫，不要只靠單一來源。

### Step 2：撰寫研究筆記

寫入 `docs/<slug>.md`，slug 用小寫 kebab-case。

**必須在檔案最開頭加上 YAML frontmatter：**

```yaml
---
date: "YYYY-MM-DD"
category: "分類名稱"
icon: "material-icon-name"
oneliner: "一句話描述，用於卡片和表格"
---
```

- `date` — 研究日期（ISO 格式，如 `2026-03-30`）
- `category` — **必須完全匹配** `mkdocs.yml` nav 的分類名稱（如「Coding Agent 工具」）
- `icon` — Material Design icon 名稱（如 `material-robot`），不含冒號語法
- `oneliner` — 卡片和表格中使用的一句話描述

**筆記結構模板（frontmatter 之後）：**

```markdown
# <主題名稱> 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| （列出所有參考來源：官網、GitHub、文章、論文等） |

## 專案概述 / 功能概述

（2-3 段描述：這是什麼、解決什麼問題、適合什麼場景）

## 核心功能 / 技術架構

（用表格、清單、ASCII 圖表呈現重點）

## 快速開始 / 使用方式

（如果適用，附上安裝和使用步驟）

## 目前限制 / 注意事項

（誠實列出限制和風險）

## 研究價值與啟示

### 關鍵洞察

（3-5 個從研究中提煉的洞見，不只是功能描述，要有自己的分析角度）

### 與其他專案的關聯

（如果能與網站中其他研究筆記產生對比或連結，在這裡說明）
```

**寫作原則：**
- 使用繁體中文
- 引用程式碼、指令、專有名詞保留英文原文
- 表格和 ASCII 圖表優先於大段文字
- 「研究價值與啟示」是最重要的段落——不要只是搬運資訊，要提煉洞見

### Step 3：判斷分類並更新 mkdocs.yml

根據筆記內容，選擇最適合的分類。讀取 `mkdocs.yml` 的 nav 段落，將新筆記放入最匹配的分類。如果沒有合適的現有分類，可以新增一個（但要先跟使用者確認）。

**分類判斷原則：按內容本質分類，不按實作技術。** 例如：
- 一個用 AI Agent 做交易的專案 → 歸「量化交易」而非「AI Agent 框架」
- 一本教 AI Agent 的書 → 歸「學習資源」而非「AI Agent 框架」

在對應分類中，按字母順序插入新條目。

### Step 4：執行 sync.py 自動更新索引

```bash
python3 scripts/sync.py
```

這支腳本會自動：
- 讀取所有 `docs/*.md` 的 frontmatter + `mkdocs.yml` nav
- 重新生成 `docs/index.md`（研究更新卡片 + 各分類卡片）
- 重新生成 `docs/news.md`（最新整理表格 + 按年份/月份 + 按主題）
- 驗證所有 docs 都在 nav 中（如果有遺漏會報錯並 exit 1）

**不需要手動編輯 `index.md` 和 `news.md`。**

### Step 5：Commit 並 Push

```bash
git add docs/<slug>.md docs/index.md docs/news.md mkdocs.yml
git commit -m "Add research note: <主題名稱>"
git push
```

## 注意事項

- 如果使用者一次給多個主題，逐一處理，每個獨立 commit
- 如果主題已經有對應的 `docs/*.md`，問使用者要覆寫還是更新
- 資料來源不限 GitHub repo，可以是網路文章、論文、影片、文件等任何來源
- commit 前先用 `gh auth status` 確認 GitHub 帳號正確
- GitHub Actions 的 `deploy.yml` 也會在 build 前執行 `sync.py`，作為兜底保護
