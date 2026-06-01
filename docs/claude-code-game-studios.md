---
date: "2026-05-26"
category: "Coding Agent 工具"
card_icon: "material-gamepad-variant"
oneliner: "Donchitos 將 Claude Code 改造成完整遊戲開發工作室：49 agents + 73 skills + 12 hooks + 11 rules，鏡像真實 studio 三層階層（Director/Lead/Specialist）"
tags:
  - claude-code
  - multi-agent
  - skills
---

# Claude Code Game Studios 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/Donchitos/Claude-Code-Game-Studios> |
| 作者 | [Donchitos](https://github.com/Donchitos) |
| License | MIT |
| Buy Me a Coffee | <https://www.buymeacoffee.com/donchitos3> |
| GitHub Sponsors | <https://github.com/sponsors/Donchitos> |
| Discussions | <https://github.com/Donchitos/Claude-Code-Game-Studios/discussions> |

## 專案概述

**Claude Code Game Studios** 是 Donchitos 在 2026/02 開源的 Claude Code 模板專案，目標是把「一個 Claude Code session」改造成「一間完整的遊戲開發工作室」。短短三個多月衝到 **19,998 stars / 2,906 forks**，是目前 game dev × AI agent 領域成長最快的 repo 之一。

它解決的痛點很具體：用 AI 單兵作戰時容易「沒人幫你把關」——沒人提醒你別 hardcode magic number、沒人做設計審查、沒人問「這真的符合遊戲核心 vision 嗎？」。Donchitos 的解法是把真實 game studio 的階層結構搬進 Claude Code：directors 守願景、leads 顧領域、specialists 動手做，每個 agent 都有明確職責、上呈路徑、品質門檻。

關鍵特色是**「Collaborative, Not Autonomous」**——不是 auto-pilot，每個 agent 都遵守「先問問題 → 提 2-4 個選項 → 使用者決定 → 草稿 → 簽核」的協作協議。User 永遠掌控決策權，agents 只提供結構與專業度。

## 核心功能

### 數字一覽

| 類別 | 數量 | 說明 |
|------|------|------|
| **Agents** | 49 | Design / Programming / Art / Audio / Narrative / QA / Production |
| **Skills** | 73 | Slash commands 涵蓋 7-phase pipeline |
| **Hooks** | 12 | Commit / Push / Asset / Session / Agent audit / Gap detection |
| **Rules** | 11 | Path-scoped coding standards（依檔案路徑自動套用） |
| **Templates** | 41 | GDD、UX spec、ADR、Sprint plan、HUD design、Accessibility |

### Studio Hierarchy（三層階層）

```
Tier 1 — Directors (Opus)
  creative-director  technical-director  producer

Tier 2 — Department Leads (Sonnet)
  game-designer  lead-programmer  art-director
  audio-director  narrative-director  qa-lead
  release-manager  localization-lead

Tier 3 — Specialists (Sonnet/Haiku)
  gameplay-programmer  engine-programmer  ai-programmer
  network-programmer   tools-programmer   ui-programmer
  systems-designer     level-designer     economy-designer
  technical-artist     sound-designer     writer
  world-builder        ux-designer        prototyper
  performance-analyst  devops-engineer    analytics-engineer
  security-engineer    qa-tester          accessibility-specialist
  live-ops-designer    community-manager
```

模型分配很值得注意：**Directors 用 Opus**（重決策、抽象 vision），**Leads 用 Sonnet**（領域專家），**Specialists 用 Sonnet/Haiku**（執行層）——這是直接把模型 cost/能力曲線對應到組織階層。

### 三大引擎專家組

| Engine | Lead Agent | Sub-Specialists |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript / Shaders / GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS / Shaders/VFX / Addressables / UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS / Blueprints / Replication / UMG/CommonUI |

### Skills 分組（73 個 slash commands）

| 階段 | 代表 Skills |
|------|------------|
| Onboarding | `/start` `/help` `/project-stage-detect` `/setup-engine` `/adopt` |
| Game Design | `/brainstorm` `/map-systems` `/design-system` `/quick-design` `/propagate-design-change` |
| Art & Assets | `/art-bible` `/asset-spec` `/asset-audit` |
| UX | `/ux-design` `/ux-review` |
| Architecture | `/create-architecture` `/architecture-decision` `/architecture-review` |
| Stories & Sprints | `/create-epics` `/create-stories` `/dev-story` `/sprint-plan` `/story-done` `/estimate` |
| Reviews | `/design-review` `/code-review` `/balance-check` `/scope-check` `/perf-profile` `/tech-debt` `/gate-check` `/security-audit` |
| QA & Testing | `/qa-plan` `/smoke-check` `/soak-test` `/regression-suite` `/test-flakiness` |
| Production | `/milestone-review` `/retrospective` `/bug-triage` `/playtest-report` |
| Release | `/release-checklist` `/launch-checklist` `/changelog` `/patch-notes` `/hotfix` `/day-one-patch` |
| **Team Orchestration** | `/team-combat` `/team-narrative` `/team-ui` `/team-release` `/team-polish` `/team-audio` `/team-level` `/team-live-ops` `/team-qa` |

「Team Orchestration」是亮點——一個指令就能召集多個 agent 協作完成單一 feature。

### 12 個 Hooks（自動安全網）

| Hook | 觸發時機 | 功能 |
|------|---------|------|
| `validate-commit.sh` | PreToolUse (Bash) | 檢查 hardcoded values、TODO 格式、JSON 有效性、GDD 章節 |
| `validate-push.sh` | PreToolUse (Bash) | Protected branch push 警告 |
| `validate-assets.sh` | PostToolUse (Write/Edit) | Assets 命名規範與 JSON 結構驗證 |
| `session-start.sh` | Session 開啟 | 顯示分支與最近 commits |
| `detect-gaps.sh` | Session 開啟 | 偵測新專案建議 `/start`、有 code 但缺設計文件時提醒 |
| `pre-compact.sh` | Compaction 前 | 保留 session 進度 |
| `post-compact.sh` | Compaction 後 | 提醒 Claude 從 `active.md` 還原 |
| `notify.sh` | Notification | Windows toast（PowerShell） |
| `session-stop.sh` | Session 關閉 | 歸檔 `active.md` 到 session log |
| `log-agent.sh` / `log-agent-stop.sh` | Subagent 起訖 | Agent audit trail |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | `.claude/skills/` 改動後提醒跑 `/skill-test` |

### Path-Scoped Rules（11 條依路徑自動生效）

| 路徑 | 強制規範 |
|------|---------|
| `src/gameplay/**` | Data-driven values、delta time、不可引用 UI |
| `src/core/**` | Hot path 零配置、thread safety、API 穩定性 |
| `src/ai/**` | 效能預算、可除錯、parameters data-driven |
| `src/networking/**` | Server-authoritative、訊息版本化、安全性 |
| `src/ui/**` | 不持有 game state、可在地化、無障礙 |
| `design/gdd/**` | 必填 8 sections、公式格式、edge cases |
| `tests/**` | Test 命名、覆蓋率、fixture 模式 |
| `prototypes/**` | 寬鬆標準、必須有 README 與 hypothesis |

## 快速開始

```bash
# 1. Clone 模板
git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git my-game
cd my-game

# 2. 開 Claude Code
claude

# 3. 跑 /start，它會問你在哪個階段（沒概念 / 模糊概念 / 明確設計 / 既有專案）
#    然後導向正確的 workflow
```

也可以直接跳到特定 skill：
- `/brainstorm` — 從零探索遊戲點子
- `/setup-engine godot 4.6` — 直接設定引擎
- `/project-stage-detect` — 分析既有專案

## 設計哲學基礎

模板背後是專業遊戲開發理論：

- **MDA Framework** — Mechanics / Dynamics / Aesthetics 三層分析
- **Self-Determination Theory** — Autonomy / Competence / Relatedness 玩家動機
- **Flow State Design** — Challenge-skill balance
- **Bartle Player Types** — 受眾類型驗證
- **Verification-Driven Development** — 先寫測試再實作

## 目前限制

- **主要在 Windows 10 + Git Bash 開發測試**——hooks 用 POSIX-compatible patterns（`grep -E` 而非 `-P`），有 fallback，但作者明說 macOS/Linux 跨平台還在持續測試
- **`notify.sh` 用 PowerShell**——macOS/Linux 上是 no-op，桌面通知未實作
- **`jq` 與 Python 3 是 optional**——缺了就只是失去驗證能力，不會中斷
- **Template 不是 framework**——所有東西都預期被使用者自己客製，不要當 black box 用
- **不是 auto-pilot**——強制使用者參與每個決策，想完全放手的人會覺得「太囉嗦」

## 研究價值與啟示

### 關鍵洞察

1. **「真實組織結構 → AI agent 階層」是被低估的設計模式**：大多數 Claude Code 模板把 agents 當「工具箱」（一堆 specialist 平鋪），這個專案直接搬「creative-director / technical-director / producer」三人組當頂層，再延伸 lead/specialist 兩層。這個結構讓 escalation path（誰找誰調解衝突）天然成立——design 衝突上呈 creative-director、技術衝突上呈 technical-director、跨部門變更交 producer 協調。「組織學」直接變成「prompt 架構」。

2. **模型分配（Opus/Sonnet/Haiku）對應組織階層是個聰明的 cost 設計**：Tier 1 directors 用 Opus（少數但需要 vision-level 抽象）、Tier 2 leads 用 Sonnet（領域深度但中等成本）、Tier 3 specialists 用 Sonnet/Haiku（高頻執行）。這是把「真實薪資結構」對應到「token cost」——讓 token 預算自然向決策層傾斜。

3. **Hooks 早退（early exit）是必要設計**：12 個 hook 中有 3 個（`validate-commit`、`validate-assets`、`validate-skill-change`）會在每次 Bash/Write 都觸發，作者特地在 README 強調「這些 hook 在不相關時會 exit 0 立即退出，是正常行為而非效能問題」。這提醒：寫 PreToolUse hook 一定要前置 guard，不然會被誤判成「拖慢 session」。

4. **「Collaborative, Not Autonomous」是反潮流但正確的定位**：在 autonomous agent 當紅的 2026 年，這個模板反其道而行——強調 agent 必須先問、再提選項、由 user 決定、最後簽核。對遊戲開發這種「品味驅動」的領域特別合適，因為遊戲沒有客觀正確答案，autonomous agent 會「自信地做出創意上錯的決定」。

5. **Path-Scoped Rules 是 prompt engineering 的進階形式**：傳統做法是「在 system prompt 寫 coding standards」，這專案改成「在 `src/gameplay/**` 自動載入 gameplay rules」——讓規範隨檔案路徑「就近啟動」，不污染全域 context、也不讓 agent 在改 UI 時還在記得 networking 的規範。這個模式可以複製到任何 Claude Code 專案。

6. **「Template 而非 Framework」的開源策略很值得學**：作者直接定義「這是模板，所有東西都該被你客製」——刪 agents、改 prompts、加 rules、調 hooks 都被鼓勵。這降低了使用者的心理門檻（不用「學一個框架」），也讓專案不會被使用者的「自定義需求」拉著走。3 個月衝到 20k stars 證明這條路線可行。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [my-claude-devteam](my-claude-devteam.md) | 同樣是「組 AI 團隊」概念，但 game-studios 階層更明確、領域更聚焦（遊戲開發），devteam 偏一般軟體開發 |
| vs [wshobson agents](wshobson-agents.md) | wshobson 是平鋪型 agent 集合（工具箱式），game-studios 加上了「階層+escalation path」這層組織學設計 |
| vs [Superpowers](superpowers.md) | Superpowers 強調 skill discipline（TDD、debugging 等紀律），game-studios 強調 organizational discipline（誰決策、誰簽核） |
| vs [Tech Leads Club Agent Skills](tlc-agent-skills.md) | TLC 是技術領袖視角的工程實踐，game-studios 是 studio 視角的跨職能協作 |
| vs [Casper Claude Skill Design Gallery](casper-claude-skill-design-gallery.md) | Casper 是 skill 設計範例集，game-studios 是把 skills 組成完整 workflow 的範例 |

**最大啟示**：如果你要把 AI agent 應用在「需要跨職能協作」的領域（不只遊戲——電影、音樂、產品設計、新創團隊都適用），與其讓單一 super agent 全包，不如**把組織結構搬進 prompt 架構**，讓 escalation path 與 quality gates 隨組織分工自然成立。這是 2026 年 agent 設計的一個重要演進方向。
