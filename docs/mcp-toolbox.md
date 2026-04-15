---
date: "2026-04-15"
category: "開發工具"
card_icon: "material-database-cog"
oneliner: "Google 官方 MCP Server — 讓 AI Agent 直連 42 種資料庫，Go 核心 + 4 語言 SDK"
---

# MCP Toolbox for Databases 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) |
| 官方文件 | [mcp-toolbox.dev](https://mcp-toolbox.dev/) |
| MCP 支援公告 | [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol) |
| Java SDK 公告 | [Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/announcing-the-mcp-toolbox-java-sdk) |
| Managed MCP Server | [Google Cloud Blog](https://cloud.google.com/blog/products/databases/managed-mcp-servers-for-google-cloud-databases) |
| LangChain 整合 | [LangChain Docs](https://python.langchain.com/docs/integrations/tools/toolbox/) |
| ADK 整合 | [ADK Docs](https://google.github.io/adk-docs/tools/google-cloud/mcp-toolbox-for-databases/) |

**專案狀態：** ⭐ 14.5K+ stars · Go · Apache 2.0 · v1.1.0 · 原名 Gen AI Toolbox for Databases

## 專案概述

MCP Toolbox for Databases 是 **Google 官方開源的 MCP Server**，讓 AI Agent、IDE（Gemini CLI、Claude Code、Codex 等）直接連接企業級資料庫。它同時扮演兩個角色：

1. **即用型 MCP Server** — 用 `--prebuilt=postgres` 一行指令啟動，立即讓 AI 查資料、探索 schema
2. **自訂工具框架** — 透過 `tools.yaml` 定義結構化查詢、語義搜尋、NL2SQL

支援 **42 種資料來源**，涵蓋 Google Cloud 資料庫和主流第三方資料庫。

## 支援的資料庫

### Google Cloud

| 資料庫 | 支援 |
|--------|------|
| AlloyDB | ✅ |
| BigQuery | ✅ |
| Cloud SQL（PostgreSQL/MySQL/SQL Server） | ✅ |
| Spanner | ✅ |
| Firestore | ✅ |
| Knowledge Catalog（原 Dataplex） | ✅ |

### 第三方 / 開源

| 資料庫 | 支援 |
|--------|------|
| PostgreSQL / MySQL / SQL Server | ✅ |
| Oracle / MongoDB / Redis | ✅ |
| Elasticsearch / Neo4j | ✅ |
| CockroachDB / ClickHouse | ✅ |
| Snowflake / Trino / TiDB | ✅ |
| Couchbase | ✅ |

## 技術架構

```
┌──────────────────────┐
│  AI Agent / IDE      │  Gemini CLI, Claude Code, Codex, ADK, LangChain...
│  (MCP Client)        │
└──────────┬───────────┘
           │ MCP 協定（HTTP）
           │ http://127.0.0.1:5000/mcp
           ▼
┌──────────────────────┐
│  MCP Toolbox Server  │  Go 核心，連線池管理，IAM 認證
│  (tools.yaml 設定)   │  OpenTelemetry 可觀測性
│                      │  動態重載（不需重啟）
└──────────┬───────────┘
           │ 各資料庫原生協定
           ▼
┌──────────────────────┐
│  42 種資料庫          │  PostgreSQL, BigQuery, MongoDB, Redis...
└──────────────────────┘
```

### 客戶端 SDK

| 語言 | 套件 |
|------|------|
| Python | `toolbox-core`、`toolbox-langchain`、`toolbox-llamaindex` |
| JS/TS | `@toolbox-sdk/core`、`@toolbox-sdk/server`、`@toolbox-sdk/adk` |
| Go | `mcp-toolbox-sdk-go` |
| Java | `mcp-toolbox-sdk-java`（2026-03 發布） |

### 核心功能

| 功能 | 說明 |
|------|------|
| Prebuilt Tools | `list_tables`、`execute_sql` 等通用工具，一行啟動 |
| 自訂工具 | `tools.yaml` 宣告式定義 source + tool + toolset + prompt |
| 連線池 | 自動管理資料庫連線池 |
| IAM 整合 | 內建 Google Cloud IAM 認證 |
| OpenTelemetry | 端到端 metrics + tracing |
| Toolbox UI | `--ui` 旗標啟動互動式測試介面 |
| Agent Skills 生成 | `skills-generate` 將 toolset 轉為可攜套件 |
| 動態重載 | 修改 `tools.yaml` 不需重啟 |

## 快速開始

### 方法一：Prebuilt（最快，以 PostgreSQL 為例）

MCP 客戶端設定檔加入：
```json
{
  "mcpServers": {
    "toolbox-postgres": {
      "command": "npx",
      "args": ["-y", "@toolbox-sdk/server", "--prebuilt=postgres"]
    }
  }
}
```

### 方法二：自訂工具

```yaml
# tools.yaml
kind: source
name: my-pg-source
type: postgres
host: 127.0.0.1
port: 5432
database: toolbox_db
user: toolbox_user
password: my-password
---
kind: tool
name: search-hotels-by-name
type: postgres-sql
source: my-pg-source
description: Search for hotels based on name.
parameters:
  - name: name
    type: string
    description: The name of the hotel.
statement: SELECT * FROM hotels WHERE name ILIKE '%' || $1 || '%';
```

```bash
# 啟動
npx @toolbox-sdk/server --config tools.yaml

# 或用 binary（生產環境推薦）
brew install mcp-toolbox
toolbox --config tools.yaml
```

### 方法三：Python SDK 整合

```python
from toolbox_core import ToolboxClient
async with ToolboxClient("http://127.0.0.1:5000") as client:
    tools = await client.load_toolset("toolset_name")
```

## 部署方式

| 方式 | 指令 |
|------|------|
| Homebrew | `brew install mcp-toolbox` |
| NPM | `npx @toolbox-sdk/server` |
| Docker | `docker pull us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox` |
| Binary | 支援 Linux AMD64、macOS Apple Silicon/Intel、Windows |
| 原始碼 | `go install` |

## 目前限制 / 注意事項

- **不是受管服務** — 開源版需自行部署。Google Cloud Managed MCP Server 是另一產品
- **NPM 模式非最佳效能** — 官方明確說 `npx` 方式是 convenience 優先，生產環境用 binary 或 container
- **tools.yaml 密碼明文** — 生產環境需搭配 Secret Manager
- **Prebuilt Tools 功能有限** — 只有通用工具，複雜查詢需自訂
- **Google Cloud 生態偏好** — IAM、Managed MCP 等功能明顯偏向 GCP 使用者
- **部分資料庫支援開發中** — KDB+、ArcadeDB、Spanner Admin 等仍在 PR 階段
- **版本快速迭代** — v0.x → v1.1.0，API 可能隨版本變動

## 研究價值與啟示

### 關鍵洞察

1. **Google 押注 MCP 作為 AI-Database 標準介面。** 14.5K stars + 官方維護 + 4 語言 SDK + Managed 版本——Google 對 MCP 的投入程度遠超「實驗性支援」。這暗示 MCP 正在成為 AI Agent 存取企業資料的事實標準，不只是 Anthropic 的專利。

2. **「Prebuilt → 自訂」的漸進式設計降低了門檻。** `--prebuilt=postgres` 一行搞定讓人先體驗價值，然後 `tools.yaml` 提供完整的自訂能力。這種「30 秒上手 → 逐步深入」的產品設計在開發者工具中非常有效。

3. **tools.yaml 宣告式配置是對的抽象層級。** 不用寫 Go/Python 程式碼就能定義資料庫工具——寫 SQL statement + 參數描述就好。這讓 DBA 和資料工程師（而非只有後端工程師）也能為 AI Agent 提供資料存取能力。

4. **42 種資料庫支援的策略意義。** 不只是 Google Cloud 資料庫——PostgreSQL、MongoDB、Redis、Snowflake、Oracle 都支援。這是 Google 的平台策略：讓 Toolbox 成為「不管你用什麼資料庫都好用」的中立層，然後透過 IAM 和 Managed 版本引導到 GCP。

5. **OpenTelemetry 內建說明這是生產級工具。** 大多數 MCP Server 是實驗性的，Google 直接把 metrics + tracing 作為內建功能——這是為企業生產環境設計的信號。

### 與其他專案的關聯

- **vs MCP CLI（筆記庫中）：** MCP CLI 是通用的 MCP 開發/除錯工具，Toolbox 是專門為資料庫設計的 MCP Server。兩者在 MCP 生態中的角色完全不同但互補。
- **對 Fluffy 生態的啟示：** fluffy-core 使用 Django + PostgreSQL，可以考慮用 Toolbox 為 AI Agent 提供直接的資料庫存取能力——不需要在 Django API 上額外包裝一層，Toolbox 直連 PostgreSQL 即可。特別是 `tools.yaml` 定義業務查詢的模式，可以讓 fluffy-agent-core 的 Agent 直接查商品資料、訂單記錄等。
