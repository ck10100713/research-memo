---
date: "2026-03-30"
category: "Coding Agent 工具"
card_icon: "material-suitcase"
oneliner: "MCP 萬用工具——TypeScript Runtime + CLI + Code-Gen，自動發現 IDE 設定、一行呼叫任何 MCP server（3.4K stars）"
---
# MCPorter 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [steipete/mcporter](https://github.com/steipete/mcporter) |
| 官方網站 | [mcporter.dev](http://mcporter.dev) |
| npm | [mcporter](https://www.npmjs.com/package/mcporter) |
| 作者 | [Peter Steinberger](https://steipete.me/) (PSPDFKit 創辦人，2021 exit 後全職做開源) |
| DeepWiki | [steipete/mcporter](https://deepwiki.com/steipete/mcporter) |

## 專案概述

MCPorter 是一套 **TypeScript runtime + CLI + code-gen 工具組**，讓開發者能直接從 TypeScript 程式碼或命令列呼叫任何 MCP (Model Context Protocol) server，不需要手動處理 JSON schema、OAuth、transport 細節。

核心價值：**把 MCP server 變成像一般 TypeScript 函式一樣好呼叫的 API**，或一鍵打包成獨立 CLI 工具。這對 AI Agent 工作流特別有用——Agent 可以透過 MCPorter 直接操作任何已註冊的 MCP server，省去 boilerplate。

| 指標 | 數值 |
|------|------|
| Stars | 3,466 |
| 語言 | TypeScript |
| 授權 | MIT |
| 建立日期 | 2025-11-05 |
| 最後更新 | 2026-03-30 |

## 核心功能

### 三層介面架構

```
┌─────────────────────────────────────────────┐
│  CLI（npx mcporter call / list / auth）      │  ← 人類直接使用
├─────────────────────────────────────────────┤
│  TypeScript Runtime（createRuntime）          │  ← Agent / 腳本程式化呼叫
├─────────────────────────────────────────────┤
│  Code Generator（generate-cli / emit-ts）    │  ← 產出獨立 CLI 或型別定義
└─────────────────────────────────────────────┘
         │ 自動合併設定來源 │
    Cursor / Claude Code / Claude Desktop /
    Codex / Windsurf / OpenCode / VS Code
```

### 功能矩陣

| 功能 | 說明 |
|------|------|
| **Zero-config discovery** | 自動偵測並合併 Cursor、Claude Code/Desktop、Codex、Windsurf、VS Code 等編輯器的 MCP 設定 |
| **Friendly call syntax** | 支援 function-call style `linear.create_issue(title: "Bug")` 與 flag style `title=Bug`，自動修正 typo |
| **Server proxy** | `createServerProxy()` 將 tool 映射為 camelCase 方法，結果包裝為 `CallResult`（`.text()` / `.json()` / `.images()`） |
| **CLI 生成** | `generate-cli` 將任意 MCP server 打包成獨立 CLI，支援 Bun 編譯成 binary |
| **型別生成** | `emit-ts` 產出 `.d.ts` 介面或完整 client wrapper，保持與 CLI 輸出同步 |
| **OAuth 內建** | 自動快取 token，`mcporter auth <url>` 一鍵完成 OAuth 流程 |
| **Daemon 模式** | 有狀態的 MCP server（如 chrome-devtools）可透過 daemon 保持連線，跨 Agent session 共用 |
| **Ad-hoc 連線** | 不需寫 config，直接 `--http-url` 或 `--stdio` 連接任何 MCP endpoint |

### 使用範例

**CLI 呼叫：**

```bash
# 列出所有 MCP server
npx mcporter list

# 呼叫 tool（function-call 語法）
npx mcporter call 'linear.create_comment(issueId: "ENG-123", body: "Looks good!")'

# 連接 ad-hoc server
npx mcporter list --http-url https://mcp.linear.app/mcp --name linear
```

**TypeScript Runtime：**

```ts
import { createRuntime, createServerProxy } from "mcporter";

const runtime = await createRuntime();
const linear = createServerProxy(runtime, "linear");

const docs = await linear.searchDocumentation({ query: "automations" });
console.log(docs.json());

await runtime.close();
```

**一次性呼叫（最簡用法）：**

```ts
import { callOnce } from "mcporter";

const result = await callOnce({
  server: "firecrawl",
  toolName: "crawl",
  args: { url: "https://anthropic.com" },
});
```

**產生獨立 CLI：**

```bash
npx mcporter generate-cli \
  --command "npx -y chrome-devtools-mcp@latest" \
  --compile  # 編譯成 Bun binary
```

## 設定管理

MCPorter 的設定解析順序：

1. `--config` 參數指定的路徑
2. `MCPORTER_CONFIG` 環境變數
3. `<root>/config/mcporter.json`（專案層級）
4. `~/.mcporter/mcporter.json`（全域層級）

設定檔格式兼容 Cursor/Claude 的 `mcpServers` 結構，支援 JSONC（含註解），可透過 `mcporter config` 子命令管理：

```jsonc
{
  "mcpServers": {
    "context7": {
      "baseUrl": "https://mcp.context7.com/mcp"
    }
  },
  "imports": ["cursor", "claude-code", "claude-desktop", "codex", "windsurf"]
}
```

## 目前限制 / 注意事項

- **Node.js 生態依賴**：需要 Node.js 或 Bun 環境，純 Python 工作流需要額外橋接
- **MCP 協議仍在演進**：MCP spec 尚未完全穩定，MCPorter 需要持續跟進上游變動
- **Daemon 限制**：Ad-hoc STDIO/HTTP target 尚不支援 daemon 管理，需先 persist 到 config
- **OAuth 複雜性**：某些 MCP server 的 OAuth 流程可能需要手動介入（browser login）
- **版本尚年輕**：目前 0.7.x，API 可能有 breaking changes

## 研究價值與啟示

### 關鍵洞察

1. **MCP 的 DX 問題被精準定位**：MCP 的價值在於標準化 LLM ↔ Tool 的溝通協議，但原始 MCP 呼叫需要處理 JSON schema、transport、auth 等底層細節。MCPorter 的核心洞見是：**MCP server 應該像普通 TypeScript 函式一樣好呼叫**。這個「API 糖衣」層是 MCP 生態成熟的必要基礎建設。

2. **「Config Discovery」解決碎片化痛點**：目前每個 IDE/Agent 都有自己的 MCP 設定格式（Cursor 一份、Claude Code 一份），MCPorter 自動合併所有來源的做法，等於建立了一個事實上的 MCP 設定聚合層。這個模式值得參考——我們的 fluffy-agent-core 也面臨多來源工具設定整合的問題。

3. **Code-gen 策略很聰明**：`emit-ts` 產出型別定義、`generate-cli` 產出獨立工具，這種「從 runtime 資訊生成靜態程式碼」的模式，讓 MCP 的動態性和 TypeScript 的靜態型別系統和平共存。特別是 `--compile` 能打包成 Bun binary，讓非技術使用者也能用。

4. **Daemon 模式預示 Agent 長駐架構**：MCPorter 的 daemon 讓 chrome-devtools 等有狀態 server 跨 session 存活，這暗示未來 Agent 工作流會越來越需要「persistent tool connection」，而不是每次都冷啟動。

5. **作者背景加分**：Peter Steinberger 是 PSPDFKit 創辦人（2021 成功出場），現已加入 OpenAI。他的「Ship beats perfect」哲學體現在 MCPorter 的快速迭代上——2025-11 建立，4 個月內已到 0.7.x 且累積 3.4K stars。

### 與其他專案的關聯

- **MCP CLI**（`docs/mcp-cli.md`）：MCPorter 可視為 MCP CLI 的「進階版」——MCP CLI 提供基本的 MCP server 互動，MCPorter 則加上了 config discovery、code-gen、daemon 等企業級功能
- **Claude Code 生態**（Everything Claude Code / Claude Skills）：MCPorter 的 import 機制直接讀取 Claude Code 的 MCP 設定，是 Claude Code 工作流的理想補充——特別是需要在 CI/CD 或非互動環境中呼叫 MCP tool 時
- **Agent Orchestrator**（`docs/agent-orchestrator.md`）：Composio 的 orchestrator 管理 Agent 流程，MCPorter 管理 Tool 呼叫，兩者是互補關係——orchestrator 決定「做什麼」，MCPorter 處理「怎麼呼叫」
