# Agent Orchestrator 研究筆記

> **Repository:** [ComposioHQ/agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator)
> **官網:** [platform.composio.dev](https://platform.composio.dev/)
> **授權:** MIT
> **語言:** TypeScript（Node.js + Next.js monorepo）
> **Stars:** ~5.5K（截至 2026-03-27）
> **建立日期:** 2026-03-27

---

## 資料來源

| 項目 | 連結 | 備註 |
|------|------|------|
| 官方 README | [README.md](https://github.com/ComposioHQ/agent-orchestrator/blob/main/README.md) | 產品定位、Quick Start、Plugin 架構 |
| Setup Guide | [SETUP.md](https://github.com/ComposioHQ/agent-orchestrator/blob/main/SETUP.md) | 安裝需求、設定、故障排除 |
| Development Guide | [docs/DEVELOPMENT.md](https://github.com/ComposioHQ/agent-orchestrator/blob/main/docs/DEVELOPMENT.md) | Monorepo 結構、plugin pattern、核心服務 |
| Architecture Plan | [ARCHITECTURE.md](https://github.com/ComposioHQ/agent-orchestrator/blob/main/ARCHITECTURE.md) | Hash-based namespacing 設計稿 |
| CLI Reference | [docs/CLI.md](https://github.com/ComposioHQ/agent-orchestrator/blob/main/docs/CLI.md) | `ao` 指令分工 |

---

## 一句話總結

Agent Orchestrator 是一個面向 **平行 coding agent fleet** 的 orchestration layer：把 issue、git worktree、branch、PR、CI、review comment 和 notification 串成一個自動閉環，讓你用 dashboard 監督一整隊 AI 工程師。

> 如果 gstack 偏向「Claude Code 的 workflow 系統」，Agent Orchestrator 更像「幫多個 agent 同時開工、接 CI、接 review 的控制平面」。

---

## 核心定位

Agent Orchestrator **不是**：
- 單一 coding agent CLI
- 通用聊天式 AI assistant
- 視覺化 workflow builder
- 組織治理導向的公司層平台（那比較接近 Paperclip）

Agent Orchestrator **是**：
- 多個 AI coding agent 的 **編排層 / 控制平面**
- 以 **issue → branch → PR → CI → review → merge** 為中心的自動化系統
- 以 plugin slot 設計成的可替換架構
- 一個讓人類只在「卡住、需要判斷、準備合併」時再介入的監督介面

---

## 系統架構

### Monorepo 切分

根據開發文件，它的 monorepo 主要分成四層：

| 套件 | 角色 |
|------|------|
| `packages/core` | 型別、session manager、lifecycle manager、config、prompt builder |
| `packages/cli` | `ao` 指令列工具 |
| `packages/web` | Next.js dashboard |
| `packages/plugins` | 各種 runtime / agent / tracker / notifier / terminal plugin |

### 8 個 Plugin Slots

這是整個專案最重要的抽象化設計：

| Slot | 預設值 | 可替換項 |
|------|--------|----------|
| Runtime | `tmux` | `process`、`docker`、`k8s`、`ssh`、`e2b` |
| Agent | `claude-code` | `codex`、`aider`、`opencode` |
| Workspace | `worktree` | `clone` |
| Tracker | `github` | `linear` |
| SCM | `github` | 其他 SCM 尚未成熟 |
| Notifier | `desktop` | `slack`、`webhook`、`composio` |
| Terminal | `iterm2` | `web` |
| Lifecycle | core | 不可替換 |

核心介面都集中在 `packages/core/src/types.ts`，plugin 只要實作對應 interface 並 export `PluginModule` 即可接進系統。

### Session Lifecycle

官方定義的 session 狀態大致如下：

```text
spawning -> working -> pr_open -> ci_failed
                           -> review_pending -> changes_requested
                           -> approved -> mergeable -> merged
                                              |
                                           cleanup -> done
```

另外還有與 lifecycle 分離的 activity state，例如 `active`、`ready`、`idle`、`waiting_input`、`blocked`、`exited`。

這個分層很合理，因為「PR 狀態」和「agent 目前有沒有在跑」是兩件不同的事。

---

## 核心工作流程

### 人類只需要做的事

官方把使用者入口壓得很小，重點是：

```bash
ao start https://github.com/your-org/your-repo
```

或在現有 repo 內直接：

```bash
ao start
```

`ao start` 會自動做幾件事：
- 偵測 git remote、default branch、可用 agent runtime
- 產生 `agent-orchestrator.yaml`
- 啟動 dashboard
- 啟動 orchestrator agent

### Orchestrator 幫你做的事

真正的價值在後面的閉環：

1. Orchestrator 啟動後，針對 issue 生成 worker session
2. 每個 worker 都拿到自己的 git worktree、branch、PR
3. Agent 在隔離 workspace 中寫碼、測試、送 PR
4. CI fail 時，reaction engine 會自動把錯誤送回同一個 agent
5. reviewer 留 comment 時，也能再送回 agent 修正
6. PR 綠燈且 approved 後，系統通知你，或在設定下自動 merge

這讓它不像「幫你寫程式的 agent」，而像「管理一整條 AI 開發流水線的班長」。

---

## CLI 與 Dashboard 分工

CLI 文件明講，大部分 `ao` 指令其實是給 orchestrator agent 自己用的，不是給人類天天敲的。

### 人類常用指令

```bash
ao start
ao stop
ao status
ao dashboard
```

### Orchestrator 常用指令

```bash
ao spawn [issue]
ao batch-spawn 101 102 103
ao send <session> "Fix the tests"
ao session ls
ao session kill <session>
ao session restore <session>
```

這種分工很合理，代表產品思路是 **dashboard-first, operator-second**，不是把所有責任都丟回 terminal user。

---

## 設定模型

README 中的最小設定大致是這樣：

```yaml
port: 3000

defaults:
  runtime: tmux
  agent: claude-code
  workspace: worktree
  notifiers: [desktop]

projects:
  my-app:
    repo: owner/my-app
    path: ~/my-app
    defaultBranch: main

reactions:
  ci-failed:
    auto: true
    action: send-to-agent
```

比較有意思的是它還支援：
- `orchestrator.agent` 與 `worker.agent` 分開指定
- `agentRules` / `agentRulesFile` 把 repo 規則注入每個 agent prompt
- `reactions` 自動處理 CI fail、review changes requested、approved-and-green
- notifier routing，依 `urgent / action / warning / info` 分流通知

這些都說明它不是單純 session manager，而是有 **policy layer** 的 orchestration system。

---

## 亮點

### 1. 真正把 Git / PR / CI / Review 串成閉環

很多 agent 工具只做到「幫你在 terminal 裡寫碼」，Agent Orchestrator 則把後續流程也納入：
- branch 隔離
- PR 建立與追蹤
- CI 失敗回送
- review comment 回送
- merge readiness 檢查

這是從「agent 使用工具」跨到「agent 操作軟體交付流程」的差別。

### 2. Plugin slot 抽象做得很清楚

它不是寫死 Claude Code + tmux + GitHub。

理論上你可以替換：
- agent：Claude Code / Codex / Aider / OpenCode
- runtime：tmux / Docker / K8s
- tracker：GitHub / Linear
- notifier：desktop / Slack / webhook

這讓它更像一個本地可部署的 orchestration kernel。

### 3. Local-first，沒有重 SaaS 鎖定

預設工作模式是：
- 本機 repo
- 本機 tmux session
- 本機 dashboard
- GitHub / Linear 當外部系統

這種設計對技術團隊很務實，不需要先把整個開發流程搬到某個雲端平台。

---

## 限制與風險

### 1. 前置條件偏重

官方 Quick Start 明列需要：
- Node.js 20+
- Git 2.25+
- tmux
- `gh` CLI

如果你團隊本來沒有 tmux / gh CLI / 本地 agent runtime 的操作習慣，導入成本不低。

### 2. GitHub 與 tmux 仍是最成熟路徑

雖然抽象上是 plugin-based，但目前實際文件最完整、最成熟的仍是：
- `github` tracker / SCM
- `tmux` runtime
- 本地 terminal / dashboard 工作流

也就是說，它的「agnostic」更多是架構目標，不代表每個替代選項都同等成熟。

### 3. 文件顯示架構仍在演進中

這是我覺得最值得注意的一點：

- `ARCHITECTURE.md` 與 `docs/DEVELOPMENT.md` 描述的是 **hash-based namespacing**，強調所有 runtime data path 由 config 位置自動推導
- 但 `agent-orchestrator.yaml.example` 與 `SETUP.md` 仍然出現 `dataDir`、`worktreeDir` 這類舊式顯式欄位

這代表 repo 文件裡同時存在「新設計方向」與「目前範例設定」兩套語意。實際使用時，應該以 **目前的 config schema / example / CLI 行為** 為準，不要只看 architecture doc 就假設所有欄位都已落地。

---

## 適合的使用場景

Agent Orchestrator 特別適合：
- 同時有很多 issue / PR 要並行處理的 repo
- 已經有 CI、code review 流程的工程團隊
- 已在用 Claude Code / Codex / Aider，想把多 session 管理系統化
- 想讓 agent 自己處理「修 CI、回 review comment、更新 PR」這些重複雜務

不太適合：
- 只有單一 agent、偶爾手動跑一次任務的個人工作流
- 沒有 GitHub PR / CI 流程的小型腳本專案
- 想找的是一般 AI agent framework，而不是 coding workflow orchestration

---

## 研究結論

Agent Orchestrator 的關鍵價值，不在於「又一個可以寫 code 的 agent」，而在於它試圖把 **多 agent 並行開發** 這件事產品化。

它最強的地方是：
- 用 worktree / branch / PR 建立清楚隔離
- 用 reactions 把 CI 和 review feedback 關回原 agent
- 用 plugin slots 把 runtime、agent、tracker、notifier 抽象化

對我來說，它更接近：

> **AI 工程團隊的本地控制平面**

而不是單純的 CLI 工具或聊天 agent。
