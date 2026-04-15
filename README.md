# Research Memo

AI 與軟體工程的技術研究筆記網站，使用 MkDocs Material 建構，由 Claude Code 驅動自動化研究流程。

**[https://ck10100713.github.io/research-memo/](https://ck10100713.github.io/research-memo/)**

## 數據

| 指標 | 數值 |
|------|------|
| 研究筆記 | 111+ 篇 |
| 分類 | 11 個 |
| 自動化 | Claude Code `/research` skill |

## 分類

| 分類 | 筆記數 | 涵蓋主題 |
|------|--------|---------|
| AI Agent 框架 | 21 | CrewAI、LangGraph、Google ADK、OpenAI Agents SDK 等 |
| Coding Agent 工具 | 39 | Claude Code 生態、Copilot、MCP、Skills、Plugins |
| 量化交易 | 11 | AI 交易、K 線預測、量化分析工具 |
| 社群行銷 | 3 | 廣告審計、社群自動化 |
| AI 創作資源 | 3 | 設計系統、Prompt Gallery |
| AI 應用 | 11 | 知識庫、自動化工作流、看房管線 |
| OSINT / 情報工具 | 2 | 網路情報分析 |
| 開發工具 | 6 | MCP Server、Web Scraping、測試自動化 |
| 學習資源 | 12 | LLM 課程、AI 工程、Karpathy LLM Wiki |

## 架構

```
research-memo/
├── docs/                # 111+ 篇研究筆記（Markdown + YAML frontmatter）
├── mkdocs.yml           # 網站設定 + 導航結構
├── scripts/
│   └── sync.py          # 自動生成 index.md + news.md
└── .claude/
    └── skills/
        └── research/    # /research skill 定義
```

### 自動化流程

```
使用者輸入：/research <URL 或主題>
        │
        ▼
Claude Code 執行 /research skill
        │
        ├── 搜集資料（gh API + WebSearch + WebFetch）
        ├── 撰寫 docs/<slug>.md（含 frontmatter）
        ├── 更新 mkdocs.yml 導航
        ├── python3 scripts/sync.py（重建 index + news）
        └── git commit + push
        │
        ▼
GitHub Actions 自動部署至 GitHub Pages
```

### 筆記結構

每篇筆記遵循統一格式：

```yaml
---
date: "YYYY-MM-DD"
category: "分類名稱"
card_icon: "material-icon-name"
oneliner: "一句話描述"
---
```

```markdown
# 主題名稱 研究筆記

## 資料來源
## 專案概述
## 核心功能 / 技術架構
## 快速開始
## 目前限制
## 研究價值與啟示
### 關鍵洞察
### 與其他專案的關聯
```

## 技術棧

- **靜態網站** — [MkDocs Material](https://squidfunnel.github.io/mkdocs-material/)
- **託管** — GitHub Pages（免費）
- **CI/CD** — GitHub Actions
- **研究自動化** — Claude Code `/research` skill
- **索引生成** — `scripts/sync.py`

## 本地開發

```bash
pip install mkdocs-material
mkdocs serve    # http://localhost:8000
```

## License

研究筆記內容僅供個人學習參考。各專案的授權條款以原始專案為準。
