---
date: "2026-03-02"
category: "AI Agent 框架"
card_icon: "material-office-building"
oneliner: "開源 AI Agent 編排控制平面，把多個 Agent 組織成一間零人公司"
---
# Paperclip 研究筆記

> **Repository:** [paperclipai/paperclip](https://github.com/paperclipai/paperclip)
> **官網:** [paperclip.ing](https://paperclip.ing)
> **授權:** MIT
> **語言:** TypeScript
> **Stars:** ~31.5K (截至 2026-03-23)
> **建立日期:** 2026-03-02

---

## 一句話總結

Paperclip 是一個開源的 **AI Agent 編排控制平面**，讓你把多個 AI Agent 組織成一間「零人公司」(zero-human company)，具備組織架構、預算控制、治理審批和任務追蹤。

> **"If OpenClaw is an employee, Paperclip is the company."**

---

## 核心定位

Paperclip **不是**：
- 聊天機器人
- Agent 框架（不教你如何建 Agent）
- 拖拉式 workflow builder
- Prompt 管理器
- 單 Agent 工具
- Code review 工具

Paperclip **是**：
- Agent 之上的「公司層」(company layer)
- 定義階層、委派目標、執行預算、記錄每個決策的控制平面
- 類似 task manager 的 UX，但底層有 org chart、budget、governance、goal alignment

---

## 架構概覽

### 技術棧

| 層級 | 技術 |
|------|------|
| Server | Node.js + Express + TypeScript |
| UI | React + Vite |
| 資料庫 | PostgreSQL（開發時內嵌 embedded-postgres） |
| ORM | Drizzle ORM |
| 即時通訊 | WebSocket (ws) |
| 驗證 | better-auth |
| 儲存 | local_disk（預設）/ S3 |
| 日誌 | pino |
| 驗證 | zod + ajv |

### Monorepo 結構（pnpm workspace）

```
paperclip/
├── server/              # Express REST API + 編排服務
├── ui/                  # React + Vite 管理介面
├── cli/                 # CLI 工具 (npx paperclipai)
├── packages/
│   ├── db/              # Drizzle schema + migrations
│   ├── shared/          # 共用 types、constants、validators
│   ├── adapter-utils/   # Adapter 共用工具
│   ├── adapters/        # Agent 適配器
│   │   ├── claude-local/
│   │   ├── codex-local/
│   │   ├── cursor-local/
│   │   ├── gemini-local/
│   │   ├── openclaw-gateway/
│   │   ├── opencode-local/
│   │   └── pi-local/
│   └── plugins/         # Plugin 系統
│       ├── sdk/
│       └── examples/
├── doc/                 # 產品與規格文件
└── docs/                # 使用者文件
```

### Agent Adapter 架構

每個 Adapter 都有三層結構：
- `cli/` — CLI 整合指令
- `server/` — Server-side 邏輯（啟動、heartbeat、通訊）
- `ui/` — 前端設定介面元件

支援的 Agent Runtime：
| Adapter | 說明 |
|---------|------|
| `claude-local` | Claude Code 本地整合 |
| `codex-local` | OpenAI Codex CLI 整合 |
| `cursor-local` | Cursor IDE 整合 |
| `gemini-local` | Google Gemini CLI 整合 |
| `openclaw-gateway` | OpenClaw（前 OpenHands/Devin 替代品）閘道整合 |
| `opencode-local` | OpenCode 本地整合 |
| `pi-local` | Pi 本地整合 |

> **核心原則：** "If it can receive a heartbeat, it's hired." — 任何能接收心跳信號的 Agent 都可以被整合。

---

## 核心概念與機制

### 1. Goal Alignment（目標對齊）

四層級目標瀑布：

```
Company Mission（公司使命）
  └── Project Goal（專案目標）
       └── Agent Goal（Agent 目標）
            └── Task / Issue（具體任務）
```

每個任務都能追溯到公司使命。Agent 在執行時透過 `SKILLS.md` 注入上下文，無需重新訓練就能理解目標脈絡。

### 2. Heartbeat 機制（心跳）

Agent 不是持續運行，而是基於排程心跳：
- 按定義的時間表喚醒（每 4h / 8h / 12h 等）
- 檢查指派的工作並自主行動
- 回應 ticket 指派與委派
- 跨 session 恢復持久的任務上下文
- 防止 token 浪費，實現成本控制

### 3. Cost Control（成本控制）

- **每 Agent 月度預算**，硬性執行
- 80% 使用率時警告，100% 時自動暫停
- 追蹤粒度：Agent / Task / Project / Goal
- Board 可以 override 預算
- 防止失控的 token 消耗

### 4. Governance（治理層）

使用者作為「董事會」：
- 審批 Agent 雇用
- 在執行前 review CEO 策略
- 隨時暫停 / 恢復 / 覆蓋 / 重新指派 / 終止 Agent
- **不可變審計日誌**（append-only，不可編輯）
- 每個 tool call 和決策都有追蹤

### 5. Ticket System（工單系統）

- 每個對話都有追蹤
- 每個決策都有解釋
- 完整的 tool-call 追蹤
- 不可變的審計日誌
- Atomic issue checkout（原子化任務簽出，防止重複工作）

### 6. Multi-Company（多公司支援）

- 單一部署，多間公司
- 完全資料隔離
- 所有 entity 都有 company scope
- 統一控制平面管理投資組合

---

## 資料模型（DB Schema）

核心 entity 共 55+ 張表，主要分類：

| 分類 | Tables |
|------|--------|
| **公司** | companies, company_logos, company_memberships, company_secrets, company_secret_versions, company_skills |
| **Agent** | agents, agent_config_revisions, agent_api_keys, agent_runtime_state, agent_task_sessions, agent_wakeup_requests |
| **任務/Issue** | issues, issue_comments, issue_labels, issue_attachments, issue_documents, issue_approvals, issue_read_states, issue_work_products |
| **專案/目標** | projects, project_goals, project_workspaces, goals |
| **心跳** | heartbeat_runs, heartbeat_run_events |
| **預算/成本** | budget_policies, budget_incidents, cost_events, finance_events |
| **治理** | approvals, approval_comments, principal_permission_grants |
| **文件** | documents, document_revisions, assets |
| **Workspace** | execution_workspaces, workspace_operations, workspace_runtime_services |
| **Routines** | routines (含 routine_triggers, routine_runs) |
| **Plugin** | plugins, plugin_config, plugin_company_settings, plugin_state, plugin_entities, plugin_jobs, plugin_webhooks, plugin_logs |
| **認證** | auth_users, auth_sessions, auth_accounts, auth_verifications |
| **其他** | activity_log, instance_settings, instance_user_roles, invites, join_requests, labels |

---

## 工程規範重點（from AGENTS.md）

1. **Company-scoped** — 所有 entity 必須限定 company 範圍
2. **契約同步** — 改 schema 必須同步更新 db → shared → server → ui
3. **控制平面不變量** — 單一 assignee、原子化 checkout、approval gate、budget hard-stop、activity log
4. **驗證流程** — `pnpm -r typecheck && pnpm test:run && pnpm build`

---

## 部署模式

| 模式 | 說明 |
|------|------|
| **本地開發** | `pnpm dev`，內嵌 PostgreSQL，零設定 |
| **Quick start** | `npx paperclipai onboard --yes` |
| **Docker** | 提供 docker-compose.yml |
| **Production** | 自行指定外部 PostgreSQL，可部署到 Vercel 等 |
| **Solo** | 搭配 Tailscale 從手機存取 |

---

## Roadmap（官方）

- OpenClaw onboarding 簡化
- Cloud agent 支援（Cursor / e2b）
- **ClipMart** — 下載並執行預建的「公司模板」
- 更好的 Agent 配置 UX
- Harness engineering 支援
- Plugin 系統（已啟動 🟢）
- 文件改善

---

## 與 Fluffy Agent Core 的比較分析

| 面向 | Paperclip | Fluffy Agent Core |
|------|-----------|-------------------|
| **層級** | 公司編排層（管理多個 Agent） | Agent 執行層（單一 Agent 框架） |
| **核心問題** | 如何讓多個 Agent 協作運營公司 | 如何讓單一 Agent 有效完成任務 |
| **Agent 來源** | BYOA（帶自己的 Agent） | 自建 Worker + Tool |
| **目標對齊** | Company → Project → Agent → Task 四層瀑布 | Agent → Sub-agent 委派 |
| **成本控制** | 每 Agent 預算 + 硬限制 | N/A（依賴外部） |
| **治理** | 審批流程 + 審計日誌 | N/A |
| **可能整合** | Fluffy Agent Core 可作為 Paperclip 的一個 Agent adapter | Paperclip 可作為 Fluffy 的上層編排 |

### 潛在整合方式

Paperclip 的 Adapter 架構（cli + server + ui 三層）設計明確，理論上可以為 Fluffy Agent Core 建立一個 `fluffy-agent-adapter`，使其成為 Paperclip 公司中的一名「員工」。

---

## 關鍵洞察

1. **時機精準** — 2026-03-02 才建立，3 週內就衝到 31K stars，顯示多 Agent 編排是當前極度熱門的需求
2. **抽象層級正確** — 不試圖重新發明 Agent，而是解決 Agent 之上的「管理」問題
3. **公司隱喻有效** — 用 org chart / budget / governance 等商業概念來建模 Agent 協作，直覺且易理解
4. **Plugin 系統** — 已啟動開發，允許擴展 knowledgebase、tracing、queue 等能力
5. **開發者體驗好** — 內嵌 DB、一鍵啟動、worktree 支援，降低入門門檻
6. **OpenClaw 生態** — 與 OpenClaw（開源 Devin 替代品）深度整合，形成 Agent + Orchestration 的完整方案

---

## 相關資源

- [Paperclip 官方文件](https://paperclip.ing/docs)
- [GitHub Repo](https://github.com/paperclipai/paperclip)
- [Discord 社群](https://discord.gg/m4HZY7xNG3)
- [開發指南](https://github.com/paperclipai/paperclip/blob/master/doc/DEVELOPING.md)
- [eWeek 報導](https://www.eweek.com/news/meet-paperclip-openclaw-ai-company-tool/)
- [Abduzeedo 介紹](https://abduzeedo.com/paperclip-open-source-ai-agent-orchestration-builders)
- [Zeabur 部署模板](https://zeabur.com/templates/E6H44N)
