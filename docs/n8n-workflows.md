---
date: "2026-04-13"
category: "AI 應用"
card_icon: "material-cog-transfer"
oneliner: "4,343 個免費 n8n 自動化工作流模板庫 — 從 AI Agent 到行銷自動化，一鍵匯入即用"
---

# n8n-workflows 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [Zie619/n8n-workflows](https://github.com/Zie619/n8n-workflows) |
| 線上瀏覽介面 | [zie619.github.io/n8n-workflows](https://zie619.github.io/n8n-workflows) |
| n8n 官方匯入教學 | [Export and import workflows](https://docs.n8n.io/workflows/export-import/) |
| n8n 官方模板庫 | [n8n Templates](https://docs.n8n.io/workflows/templates/) |
| Medium 介紹 | [2000+ Free n8n Workflows](https://medium.com/the-ai-bench/2000-free-n8n-workflows-for-every-use-case-you-can-imagine-265f8a49fa8c) |
| AI-BOM 安全掃描 | [Trusera/ai-bom](https://github.com/Trusera/ai-bom) |

**專案狀態：** ⭐ 53.7K+ stars · MIT License · Python · 2025-05 創建

## 專案概述

Zie619/n8n-workflows 是目前**最大的 n8n 工作流模板收藏庫**，包含 **4,343 個**可直接匯入使用的 JSON 工作流檔案，涵蓋 **365+ 個整合服務**、**29,445 個節點**，分為 **15 個分類**。

這些工作流從 n8n 官方網站、社群論壇、及網路各處收集而來，形成一個持續更新的自動化知識庫。專案提供線上搜尋介面（GitHub Pages）和本地安裝兩種使用方式，讓使用者不需要從零開始設計自動化流程。

> 使用者最關心的問題：**「如何免費取得並使用這些工作流？」** 答案很簡單——clone repo、挑選 JSON、匯入 n8n。以下是完整步驟。

## 如何取得和使用

### 方法一：線上瀏覽 + 直接下載（最簡單）

1. 開啟 [zie619.github.io/n8n-workflows](https://zie619.github.io/n8n-workflows)
2. 用搜尋或分類篩選找到想要的工作流
3. 點擊下載取得 JSON 檔案
4. 在 n8n 中匯入（見下方匯入步驟）

### 方法二：Clone 整個 Repo

```bash
git clone https://github.com/Zie619/n8n-workflows.git
cd n8n-workflows

# 工作流 JSON 檔案都在 workflows/ 目錄下，按分類組織
ls workflows/
```

### 方法三：本地搜尋伺服器

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動本地搜尋介面
python run.py

# 開啟 http://localhost:8000 搜尋和瀏覽
```

### 方法四：Docker

```bash
docker run -p 8000:8000 zie619/n8n-workflows:latest
# 開啟 http://localhost:8000
```

### 匯入 n8n 的步驟

```
┌─────────────────────────────────────────────────┐
│  n8n 匯入工作流（三步完成）                       │
│                                                   │
│  1. 開啟 n8n → 建立新工作流（或開啟空白工作流）    │
│  2. 右上角 ⋯ 選單 → "Import from File"           │
│     （或 "Import from URL"）                      │
│  3. 選擇下載的 JSON 檔案 → 工作流立即載入         │
│                                                   │
│  ⚠️  匯入後必做：                                 │
│  • 設定 Credentials（API keys、OAuth 等）         │
│  • 檢查各節點參數是否符合你的環境                  │
│  • 測試執行（先手動觸發確認正確再啟用排程）        │
└─────────────────────────────────────────────────┘
```

**重要提醒：** 匯入的工作流包含 credential 的「參照」但不包含實際的認證資訊。你需要在 n8n 的 Credentials 區段手動建立並連結對應的 API key / OAuth token。

## 工作流分類與數量

線上介面提供多維度篩選：

### 按複雜度

| 複雜度 | 節點數 | 適合對象 |
|--------|--------|---------|
| Low | ≤5 nodes | 初學者，快速上手 |
| Medium | 6-15 nodes | 有基礎的使用者 |
| High | 16+ nodes | 進階自動化需求 |

### 按觸發方式

| 類型 | 說明 |
|------|------|
| Manual | 手動觸發 |
| Webhook | HTTP 請求觸發 |
| Scheduled | 定時排程 |
| Complex | 多重觸發條件 |

### 15 個分類涵蓋的場景

涵蓋 AI Agent、Marketing、Sales、DevOps、HR、Finance 等 15 個主要業務領域，搭配 365+ 個整合服務（Slack、Google Sheets、Notion、Airtable、OpenAI、Anthropic 等）。

## 技術架構

```
n8n-workflows/
├── workflows/              # 4,343 個工作流 JSON（按分類組織）
│   └── [category]/
├── docs/                   # GitHub Pages 線上介面
├── src/                    # Python 原始碼
├── api_server.py           # FastAPI 後端
├── workflow_db.py          # SQLite FTS5 資料庫管理
├── run.py                  # 伺服器啟動器
└── requirements.txt

搜尋架構：
  User → Web Interface → FastAPI → SQLite FTS5 → Workflow DB
                                                → JSON Files
```

| 技術 | 說明 |
|------|------|
| Backend | Python + FastAPI |
| Database | SQLite + FTS5（全文搜尋） |
| Frontend | Vanilla JS + Tailwind CSS |
| 搜尋速度 | < 100ms |
| 記憶體使用 | < 50MB |

## 安全注意事項

專案維護者用 [AI-BOM](https://github.com/Trusera/ai-bom) 掃描了全部 4,343 個工作流，發現了：

- **硬編碼 API key** — 部分工作流直接寫死了 credential
- **未驗證的 AI Agent 節點** — Agent 連接 LLM 但缺乏存取控制
- **MCP client 連接未知 server** — 潛在的資安風險

```bash
# 建議在使用前掃描你挑選的工作流
pip install ai-bom
ai-bom scan ./workflows/
```

## 目前限制 / 注意事項

- **需要自己有 n8n 實例** — 這只是模板庫，你需要先安裝 n8n（自架或 n8n Cloud）
- **Credential 需手動設定** — 每個工作流用到的外部服務都要自己設定 API key
- **品質參差不齊** — 4,343 個工作流來自各種來源，部分可能過時或有 bug
- **安全風險** — 部分工作流含硬編碼 credential 或不安全的 Agent 設定，務必先審查
- **DMCA 合規** — 2025-08 曾因版權問題移除 8 個工作流，部分內容可能存在授權爭議
- **n8n 版本相容性** — 較舊的工作流可能不相容最新版 n8n 的節點格式

## 研究價值與啟示

### 關鍵洞察

1. **「工作流即知識」的複利效應。** 4,343 個工作流不只是模板——它們是自動化領域的集體知識庫。每個工作流封裝了「如何將 A 服務連接到 B 服務」的 know-how，這些 know-how 通常散落在文件、教學影片、論壇帖子中。集中後形成了一個可搜尋、可複製的自動化知識庫——概念上類似 Karpathy LLM Wiki 的「編譯」思路。

2. **53.7K stars 揭示了 no-code/low-code 的真實需求。** 這個 repo 的 star 數遠超多數 AI 框架專案，說明「能直接用的模板」比「能寫程式的工具」有更廣的受眾。大多數人需要的不是另一個 SDK，而是「解決我這個具體問題的現成方案」。

3. **GitHub Pages + SQLite FTS5 = 零成本搜尋引擎。** 不需要 Elasticsearch、不需要付費後端——純靜態 + SQLite 全文搜尋就能支撐 4,343 個工作流的即時搜尋。這個架構對任何中小型內容搜尋場景都有參考價值。

4. **AI-BOM 的發現是警示。** 掃描 4,343 個社群工作流後發現硬編碼 API key 和不安全的 Agent 設定——這不是個案，而是整個 no-code 生態的系統性安全問題。工作流分享的便利性與安全性之間存在根本張力。

5. **n8n 作為「AI Agent 的膠水層」正在崛起。** 這個模板庫中包含大量 AI Agent 相關工作流（OpenAI、Anthropic、向量資料庫整合），顯示 n8n 不再只是「Zapier 替代品」，而是成為連接 AI 能力與業務流程的關鍵中介層。

### 與其他專案的關聯

- **vs Karpathy LLM Wiki：** 兩者都體現了「預編譯知識」的理念。LLM Wiki 編譯的是研究知識，n8n-workflows 編譯的是自動化 know-how。差別在於 LLM Wiki 由 AI 持續維護，n8n-workflows 由社群貢獻。
- **vs Multica：** Multica 管理 Coding Agent 的執行，n8n 管理業務自動化的執行。兩者可以互補——用 n8n 觸發 webhook 啟動 Multica 的 Agent 任務，或用 Multica 的 Agent 自動生成 n8n 工作流。
- **對 Fluffy 生態的啟示：** n8n 可作為 fluffy-core 的外部自動化層——例如用 n8n 工作流自動化 ETL pipeline、定時觸發 AI Agent 任務、或串接外部服務通知。值得評估是否將部分 Django Celery 任務遷移到 n8n 以獲得更好的視覺化和可維護性。
