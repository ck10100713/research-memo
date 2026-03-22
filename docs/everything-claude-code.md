# Everything Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) |
| Shorthand Guide | [X Thread](https://x.com/affaanmustafa/status/2012378465664745795) |
| Longform Guide | [X Thread](https://x.com/affaanmustafa/status/2014040193557471352) |
| Security Guide | [X Thread](https://x.com/affaanmustafa/status/2033263813387223421) |
| AgentShield（安全掃描） | [npm: ecc-agentshield](https://www.npmjs.com/package/ecc-agentshield) |
| GitHub App | [ecc-tools](https://github.com/marketplace/ecc-tools) |
| DeepWiki 分析 | [deepwiki.com](https://deepwiki.com/affaan-m/everything-claude-code) |
| 作者 | Affaan Mustafa（Anthropic Hackathon Winner） |
| Stars | **~97.3K**（Claude Code 生態最多星的專案） |
| Forks | ~12.7K |
| 授權 | MIT |
| 語言 | JavaScript / TypeScript / Python / Go / Java / Perl |
| 版本 | v1.9.0（2026-03） |
| 建立時間 | 2026-01-18 |

## 專案概述

Everything Claude Code（ECC）是一個 **AI Agent Harness 效能優化系統**，不只是設定檔合集，而是完整的系統：skills、instincts、memory optimization、continuous learning、security scanning、research-first development。

起源於 2026 年 2 月 Cerebral Valley × Anthropic 黑客松，目前已發展為跨平台（Claude Code、Codex、OpenCode、Cursor、Antigravity）的 Agent 配置生態系。

### 核心數字

| 項目 | 數量 |
|------|------|
| Agents | 28 |
| Skills | 116 |
| Commands | 59 |
| Rules | 多語言 × 多類別 |
| 支援語言 | 12（TS、Python、Go、Swift、Java、Kotlin、C++、Rust、PHP、Perl、Django、Laravel） |
| 測試 | 1,282 tests, 98% coverage |
| 靜態分析規則 | 102 |

## 系統架構

### 整體結構

```
everything-claude-code/
├── .claude-plugin/    # Plugin manifest
├── agents/            # 28 專業化 subagent
├── skills/            # 116 workflow 定義 + 領域知識
├── commands/          # 59 slash commands
├── rules/             # 按語言分類的規則
│   ├── common/        # 通用規則
│   ├── typescript/
│   ├── python/
│   ├── golang/
│   ├── swift/
│   └── php/
├── hooks/             # 觸發式自動化
├── scripts/           # 跨平台 Node.js 腳本
├── contexts/          # 動態 system prompt 注入
├── examples/          # 範例 CLAUDE.md
├── mcp-configs/       # MCP server 設定
└── tests/             # 測試套件
```

### 核心元件

#### 28 個專業 Agent

| 類別 | Agent 範例 |
|------|-----------|
| **規劃** | planner, architect, chief-of-staff |
| **程式碼** | code-reviewer, refactor-cleaner, security-reviewer |
| **語言專屬** | typescript-reviewer, python-reviewer, go-reviewer, java-reviewer, kotlin-reviewer, rust-reviewer, cpp-reviewer |
| **建置修復** | build-error-resolver, go-build-resolver, java-build-resolver, kotlin-build-resolver, cpp-build-resolver, rust-build-resolver, pytorch-build-resolver |
| **測試** | tdd-guide, e2e-runner |
| **運維** | loop-operator, harness-optimizer, doc-updater, docs-lookup |

#### 116 個 Skills（精選分類）

| 分類 | Skills |
|------|--------|
| **語言模式** | coding-standards, golang-patterns, python-patterns, django-*, laravel-*, springboot-*, cpp-*, perl-*, swift-* |
| **前端** | frontend-patterns, frontend-slides, liquid-glass-design |
| **後端** | backend-patterns, api-design, database-migrations, postgres-patterns, clickhouse-io, docker-patterns |
| **AI/LLM** | cost-aware-llm-pipeline, regex-vs-llm-structured-text, foundation-models-on-device |
| **持續學習** | continuous-learning, continuous-learning-v2, iterative-retrieval, strategic-compact |
| **驗證** | eval-harness, verification-loop, tdd-workflow, e2e-testing |
| **安全** | security-review, security-scan |
| **商業** | article-writing, content-engine, market-research, investor-materials, investor-outreach |
| **自主循環** | autonomous-loops（sequential、PR loop、DAG 編排） |

#### 關鍵 Commands

| 指令 | 功能 |
|------|------|
| `/plan` | 實作規劃 |
| `/tdd` | TDD 工作流 |
| `/code-review` | 品質審查 |
| `/build-fix` | 修復建置錯誤 |
| `/learn` | 中途提取模式 |
| `/evolve` | 將 instincts 聚類為 skills |
| `/security-scan` | AgentShield 安全掃描 |
| `/harness-audit` | Harness 配置評分 |
| `/multi-plan` | 多 Agent 任務分解 |
| `/multi-execute` | 編排式多 Agent 工作流 |
| `/pm2` | PM2 服務生命週期管理 |

### Continuous Learning v2（Instinct 系統）

自動從開發 session 中學習模式：

```
Session 中的行為模式
        ↓ /learn
  提取為 Instinct（含信心分數）
        ↓ /evolve
  聚類為可複用的 Skill
        ↓
  下一次 session 自動套用
```

| 指令 | 功能 |
|------|------|
| `/instinct-status` | 檢視已學習的 instincts 和信心度 |
| `/instinct-import` | 匯入他人的 instincts |
| `/instinct-export` | 匯出自己的 instincts |
| `/evolve` | 將相關 instincts 聚類為 skill |

### AgentShield — 安全掃描

掃描 Claude Code 配置的安全漏洞：

```bash
npx ecc-agentshield scan         # 快速掃描
npx ecc-agentshield scan --fix   # 自動修復
npx ecc-agentshield scan --opus  # 三個 Opus Agent 紅藍隊分析
npx ecc-agentshield init         # 從零生成安全配置
```

掃描 5 大類：secrets detection（14 patterns）、permission auditing、hook injection、MCP server risk、agent config review。

`--opus` 模式執行紅隊（攻擊）→ 藍隊（防禦）→ 審計（綜合）的三方對抗分析，非單純 pattern matching。

## 安裝方式

### Plugin 安裝（推薦）

```bash
# 加入 marketplace
/plugin marketplace add affaan-m/everything-claude-code

# 安裝 plugin
/plugin install everything-claude-code@everything-claude-code
```

> Rules 無法透過 plugin 自動安裝（Claude Code 上游限制），需手動：

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
./install.sh typescript    # 或 python / golang / swift / php
```

### Hook 控制

```bash
# Hook 嚴格度（minimal / standard / strict）
export ECC_HOOK_PROFILE=standard

# 停用特定 hook
export ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"
```

## 跨平台支援

| 平台 | 支援方式 |
|------|---------|
| Claude Code | Plugin（原生） |
| Codex | `AGENTS.md` + `/codex-setup` |
| OpenCode | Plugin system + custom tools |
| Cursor | `--target cursor` |
| Antigravity | `--target antigravity` |
| 作業系統 | Windows / macOS / Linux |

## 目前限制與注意事項

| 項目 | 說明 |
|------|------|
| **Rules 需手動安裝** | Claude Code plugin 系統不支援自動分發 rules |
| **Hook 重複偵測** | v2.1+ 自動載入 hooks.json，手動宣告會衝突（已是知名 bug） |
| **CLI 版本要求** | 最低 Claude Code CLI v2.1.0 |
| **體量龐大** | 116 skills + 28 agents 可能對小專案過於沉重，建議選擇性安裝 |
| **快速迭代** | v1.3 → v1.9 在兩個月內推出，API 可能不穩定 |

## 研究價值與啟示

### 關鍵洞察

1. **從「設定包」到「效能優化系統」的進化**：ECC 最初只是一個 CLAUDE.md 設定合集，但 v1.8 起明確定位為「harness performance system」。包含 continuous learning（自動提取模式）、instinct evolution（instinct → skill 演化）、harness audit（配置評分）等機制，已超越靜態設定的範疇

2. **Instinct → Skill 演化是最有創意的設計**：讓 AI 從每次 session 中學習行為模式（instinct），累積後自動聚類為可複用的 skill。這實現了「用越多越聰明」的正回饋循環，概念上類似人類的肌肉記憶 → 有意識的技能

3. **AgentShield 的紅藍隊對抗模式值得借鑑**：用三個 Opus Agent（攻擊者、防禦者、審計者）進行安全分析，比單純的 pattern matching 更能發現 exploit chain。這種「AI 審 AI」的模式可套用到其他安全場景

4. **12 語言生態的野心與代價**：從 TypeScript 擴展到 12 個語言生態是壯舉，但也意味著維護負擔。每個語言都有 patterns、testing、review、build-resolver 四件套，乘以 12 就是 48 個待維護的 skill/agent

5. **97K stars 背後的成功公式**：Anthropic 黑客松背書 + 三篇 X Thread 指南（shorthand / longform / security）+ 快速迭代 + 多語言翻譯 + 社群 PR。這是開源 AI 工具專案的行銷範本

### 與其他專案的關聯

| 對比專案 | 關聯 |
|---------|------|
| 本站 [Claude Skills Guide](claude-skills-guide.md) | ECC 是 Claude Skills 的最大規模實踐，116 skills 涵蓋各領域 |
| 本站 [Learn Claude Code](learn-claude-code.md) | ECC 的三篇指南（shorthand / longform / security）是最完整的 Claude Code 學習資源 |
| 本站 [App Store Preflight](app-store-preflight.md) | Preflight 是「規則即文件」的精簡範例，ECC 是同概念的超大規模版本 |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ECC 被列為頂級資源，但 awesome list 本身更適合探索生態全貌 |
| 本站 [Agency Agents](agency-agents.md) | 同為大規模 Agent 配置集，Agency 偏人格化，ECC 偏工程化 |
