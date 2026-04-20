---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-hammer-wrench"
oneliner: "Garry Tan 的 Claude Code 工作流系統，40 天衝到 77.7K stars，v1.3 新增 taste engine、context save/restore、10 個 host 支援"
---
# gstack 研究筆記

> **Repository:** [garrytan/gstack](https://github.com/garrytan/gstack)
> **作者:** Garry Tan（Y Combinator 總裁兼 CEO）
> **授權:** MIT
> **語言:** TypeScript (Bun)
> **最新版本:** v1.3.0.0（2026-04-19）
> **Stars:** 77.7K（截至 2026-04-20，40 天 +21K）
> **Forks:** 11.1K
> **建立日期:** 2026-03-11

---

## 一句話總結

gstack 是 Garry Tan 開源的 **Claude Code 工作流系統**，把 AI coding agent 組織成一個虛擬工程團隊（CEO、Eng Manager、Designer、QA Lead、CSO、Release Engineer、DX Lead），透過 **23 個 specialist skill + 10 個 power tool** 實現完整的軟體開發 sprint 流程，並支援 10 個 AI coding agent host。

> **"Not a copilot. That is a team."**

---

## 核心定位

gstack **是**：
- Claude Code（及其他 Agent）的 **結構化工作流 + 角色系統**
- 以 Markdown SKILL.md 為核心的 prompt 工程
- 一個內建 headless browser 的 QA / 瀏覽工具
- 一套開發流程方法論（Think → Plan → Build → Review → Test → Ship → Reflect）

gstack **不是**：
- Agent 框架或 orchestration 平台（那是 Paperclip 的定位）
- 獨立的 AI 產品
- SaaS 服務

---

## 作者背景

- **Garry Tan** — Y Combinator 現任總裁兼 CEO
- 曾任 Palantir 早期 eng manager/PM/designer，設計了 Palantir logo
- 共同創辦 Posterous（後被 Twitter 收購）
- 2013 年建造 Bookface（YC 內部社交網路）
- 聲稱使用 gstack 在 60 天內寫了 **60 萬行 production code**，每天 10,000~20,000 行可用程式碼
- 同時並行 10-15 個 sprint，搭配 [Conductor](https://conductor.build) 管理多個 Claude Code session

---

## 架構概覽

### 核心設計理念

> "gstack gives Claude Code a persistent browser and a set of opinionated workflow skills. The browser is the hard part — everything else is Markdown."

### 系統架構

```
Claude Code
    │
    │  invokes slash command (e.g. /qa)
    ▼
SKILL.md（Markdown prompt）
    │
    │  references $B commands
    ▼
Browse CLI（compiled Bun binary, ~58MB）
    │  HTTP POST to localhost:PORT
    ▼
Browse Server（Bun.serve()）
    │  CDP (Chrome DevTools Protocol)
    ▼
Chromium（headless, persistent daemon）
```

### 技術選擇

| 決策 | 選擇 | 原因 |
|------|------|------|
| Runtime | **Bun** (非 Node.js) | compiled binary（無需 node_modules）、原生 SQLite、原生 TypeScript、內建 HTTP server |
| Browser | **Playwright + Chromium** | persistent daemon 模式，首次 ~3s，之後 ~100-200ms |
| Skill 格式 | **Markdown SKILL.md** | Claude Code 原生支援，zero runtime dependency |
| 通訊 | **localhost HTTP** | 比 WebSocket 簡單，可用 curl 除錯 |
| 無 MCP | 刻意不用 | JSON schema overhead + persistent connection 不必要 |

### 專案結構

```
gstack/
├── browse/              # Headless browser 系統（核心技術）
│   ├── src/
│   │   ├── server.ts        # Bun.serve() HTTP server
│   │   ├── browser-manager.ts  # Playwright Chromium 管理
│   │   ├── commands.ts      # Command registry（唯一真相來源）
│   │   ├── snapshot.ts      # Accessibility tree snapshot
│   │   ├── cli.ts           # CLI entry point
│   │   ├── read-commands.ts # 無副作用的讀取指令
│   │   ├── write-commands.ts # 有副作用的寫入指令
│   │   └── meta-commands.ts # Server-level 操作
│   ├── test/            # 測試 + fixture
│   └── dist/            # Compiled binary
├── office-hours/        # /office-hours skill
├── plan-ceo-review/     # /plan-ceo-review skill
├── plan-eng-review/     # /plan-eng-review skill
├── plan-design-review/  # /plan-design-review skill
├── design-consultation/ # /design-consultation skill
├── design-review/       # /design-review skill
├── review/              # /review skill
├── investigate/         # /investigate skill
├── qa/                  # /qa skill
├── qa-only/             # /qa-only skill（只報告不修）
├── ship/                # /ship skill
├── canary/              # /canary skill
├── benchmark/           # /benchmark skill
├── document-release/    # /document-release skill
├── retro/               # /retro skill
├── codex/               # /codex skill（OpenAI second opinion）
├── careful/             # /careful skill（安全防護）
├── scripts/
│   └── gen-skill-docs.ts  # Template → SKILL.md 生成器
├── .agents/skills/      # Codex/Gemini/Cursor 相容的 skill 副本
├── SKILL.md.tmpl        # 模板（人寫的部分）
├── SKILL.md             # 生成的（自動化部分）
├── ETHOS.md             # 建造者哲學
└── ARCHITECTURE.md      # 架構文件
```

---

## 23 個 Specialist Skills（截至 2026-04-20，v1.3.0）

### Sprint 流程：Think → Plan → Build → Review → Test → Ship → Reflect

| 階段 | Skill | 角色 | 功能 |
|------|-------|------|------|
| **Think** | `/office-hours` | YC Office Hours | 六個 forcing questions 重新定義問題，挑戰前提，產生設計文件；v1.1.2 修復 builder 模式不再退化成 PRD |
| **Plan** | `/plan-ceo-review` | CEO / Founder | 重新思考問題，找出 10-star product，四種模式（擴展/選擇性擴展/維持/縮減）；v1.1.2 修復 SCOPE EXPANSION 不再被壓回診斷型 |
| **Plan** | `/plan-eng-review` | Eng Manager | 鎖定架構、資料流圖、邊界案例、測試矩陣 |
| **Plan** | `/plan-design-review` | Senior Designer | 每個設計維度 0-10 評分，說明 10 分長什麼樣，AI Slop 偵測 |
| **Plan** | `/plan-devex-review` | Developer Experience Lead | **v1.x 新增** — 互動式 DX 審計，3 模式（DX EXPANSION/POLISH/TRIAGE），20-45 個 forcing questions |
| **Plan** | `/design-consultation` | Design Partner | 從零建立完整設計系統；v1.3 新增 「人類設計師會不會覺得丟臉？」自我閘門 |
| **Plan** | `/autoplan` | Planner | 自動產生開發計畫 |
| **Review** | `/review` | Staff Engineer | 找 CI 過但 production 會爆的 bug，自動修簡單的，標記完整性缺口 |
| **Review** | `/design-review` | Designer Who Codes | 同 /plan-design-review 的審計，但會修改程式碼 |
| **Review** | `/devex-review` | DX Tester | **v1.x 新增** — 真的去測你的 onboarding，量 TTHW、截圖錯誤、與 plan-devex 比對 |
| **Design** | `/design-shotgun` | Design Explorer | 產生 4-6 組 AI mockup 變體 + 比較看板；v1.3 新增 anti-convergence（每個變體必須換 font + palette + layout）+ taste engine |
| **Design** | `/design-html` | Design Engineer | **v1.1 新增** — mockup 轉成可生產 HTML，30KB 零依賴，自動偵測 React/Svelte/Vue |
| **Debug** | `/investigate` | Debugger | 系統性根因除錯，Iron Law：不調查不修，3 次失敗後停止 |
| **Test** | `/qa` | QA Lead | 開真實瀏覽器測試，找 bug → 修復 → 產生回歸測試 → 驗證 |
| **Test** | `/qa-only` | QA Reporter | 同 /qa 但只報告不修 |
| **Test** | `/benchmark` | Performance Engineer | 頁面載入時間、Core Web Vitals、資源大小的基準測試 |
| **Test** | `/benchmark-models` | Multi-LLM Benchmark | **v1.3 新增** — Claude/GPT/Gemini 同 prompt 並行對比，可選 Sonnet judge 評分 |
| **Security** | `/cso` | Chief Security Officer | OWASP Top 10 + STRIDE 威脅建模，17 個 false positive 排除 + 8/10 信心閘門 |
| **Multi-Agent** | `/pair-agent` | Multi-Agent Coordinator | **v1.x 新增** — 把瀏覽器分享給 OpenClaw / Hermes / Codex / Cursor，每個 agent 自己的 tab，自動起 ngrok |
| **Ship** | `/ship` | Release Engineer | sync main → 跑測試 → 審計覆蓋率 → push → 開 PR；v1.1.1 修復 VERSION/package.json 飄移；v1.3 squash WIP commits |
| **Ship** | `/land-and-deploy` | Release Engineer | merge PR → 等 CI → 部署 → 驗證 production |
| **Monitor** | `/canary` | SRE | 部署後監控迴圈：console error、性能回歸、截圖異常偵測 |
| **Docs** | `/document-release` | Technical Writer | 更新所有文件以匹配剛發佈的內容 |
| **Reflect** | `/retro` | Eng Manager | 團隊感知的週回顧，per-person breakdown；支援 `/retro global` 跨 Agent 彙總 |
| **Learn** | `/learn` | Tutorial Mode | **v1.x 新增** — 教學模式 |
| **Browse** | `/browse` | QA Engineer | 真實 Chromium 瀏覽器，~100ms/command；v1.1 新增本地檔案 + retina 截圖 + setContent |
| **Cookies** | `/setup-browser-cookies` | Session Manager | 從 Chrome/Arc/Brave/Edge 匯入 cookies |

### 10 個 Power Tools

| Skill | 功能 |
|-------|------|
| `/codex` | OpenAI Codex CLI 獨立 review，跨模型分析 |
| `/context-save` | **v1.1.3 新增**（從 `/checkpoint` 改名，避開 Claude Code 內建衝突）— 把 session state 寫成 markdown 到 `~/.gstack/projects/$SLUG/checkpoints/`，可 grep / 編輯 / 搬機器 |
| `/context-restore` | **v1.1.3 新增** — 載入最近的 saved context，支援 fragment-match，可讀 WIP commit 的 `[gstack-context]` block |
| `/health` | **v1.x 新增** — 健康檢查 |
| `/careful` | 破壞性指令前警告（rm -rf, DROP TABLE, force-push） |
| `/freeze` | 鎖定編輯範圍到特定目錄 |
| `/guard` | /careful + /freeze 合一 |
| `/unfreeze` | 解除 /freeze |
| `/connect-chrome` | 連接 headed Chrome 處理 CAPTCHA/MFA |
| `/setup-deploy` | 一次性部署設定 |
| `/gstack-upgrade` | 自我更新；v1.3 新增升級後 feature discovery prompt |

---

## 關鍵技術深入

### 1. Headless Browser Daemon（核心技術差異化）

**問題：** 每次指令都啟動新瀏覽器 = 3-5 秒延遲 + 丟失所有狀態
**解決：** 長駐 Chromium daemon，透過 localhost HTTP 通訊

- 首次啟動 ~3 秒，之後每次指令 ~100-200ms
- 30 分鐘閒置自動關閉
- 隨機 port (10000-60000)，支援多 workspace 並行
- State file: `.gstack/browse.json`（pid, port, token）
- 版本自動重啟：binary version 不匹配時自動 kill + restart

### 2. Ref 系統（@e1, @e2, @c1）

Agent 用 ref 而非 CSS selector 或 XPath 來定位元素：

```
1. $B snapshot -i → Playwright accessibility tree → @e1, @e2, @e3...
2. 每個 ref 建立 Playwright Locator: getByRole(role, { name }).nth(index)
3. $B click @e3 → 解析 ref → locator.click()
```

**為何不用 DOM mutation (data-ref 注入)：**
- CSP 會擋 DOM 修改
- React/Vue/Svelte hydration 會剝掉注入的 attribute
- Shadow DOM 無法從外部觸及

**Ref 生命週期：**
- 導航時清除（framenavigated event）
- SPA 路由切換時透過 `resolveRef()` 的 `count()` 檢查偵測 stale ref（~5ms overhead）

### 3. SKILL.md Template 系統

```
SKILL.md.tmpl（人寫的 prose + placeholder）
      ↓  gen-skill-docs.ts（從原始碼 metadata 填入）
SKILL.md（committed，自動生成的段落）
```

Placeholder 從原始碼生成，確保文件永遠和程式碼同步：
- `{{COMMAND_REFERENCE}}` — 從 commands.ts
- `{{SNAPSHOT_FLAGS}}` — 從 snapshot.ts
- `{{PREAMBLE}}` — 更新檢查、session tracking、contributor mode
- `{{QA_METHODOLOGY}}` — /qa 和 /qa-only 共用
- `{{DESIGN_METHODOLOGY}}` — 設計審計共用

### 4. 安全模型

- **Localhost only** — server 綁定 localhost，非 0.0.0.0
- **Bearer token auth** — UUID token，state file mode 0o600
- **Cookie 安全** — Keychain 存取需使用者核准，記憶體內解密，不寫明文到 disk
- **Shell injection prevention** — 路徑從已知常數建構，不接受使用者輸入

### 5. 測試三層架構

| 層級 | 內容 | 成本 | 速度 |
|------|------|------|------|
| Tier 1 — Static | parse $B commands，驗證 registry | 免費 | <2s |
| Tier 2 — E2E | `claude -p` 真實 session | ~$3.85 | ~20min |
| Tier 3 — LLM Judge | Sonnet 評分文件品質 | ~$0.15 | ~30s |

---

## 建造者哲學（ETHOS.md）

### 1. Boil the Lake（煮沸湖泊）

> AI 輔助編程讓完整性的邊際成本趨近零。當完整實作只比捷徑多花幾分鐘 — 每次都做完整的。

- **Lake vs Ocean：** Lake 是可煮沸的（100% test coverage, 所有 edge cases）；Ocean 不是（重寫整個系統）
- 反模式：「選 B，90% 覆蓋用更少 code」→ 如果 A 只多 70 行，選 A
- 反模式：「測試留到下個 PR」→ 測試是最便宜的 lake

### 2. Search Before Building（先搜尋再建造）

三層知識體系：
1. **Layer 1 — Tried and true：** 標準模式，battle-tested
2. **Layer 2 — New and popular：** 當前最佳實踐，但群眾可能是錯的
3. **Layer 3 — First principles：** 原創觀察，最有價值

> **Eureka Moment：** 搜尋的最大價值不是找到可複製的方案，而是理解所有人在做什麼 + 為什麼，然後用第一原理發現傳統方法為什麼是錯的。

### AI 壓縮率表

| 任務類型 | 人類團隊 | AI 輔助 | 壓縮比 |
|---------|---------|---------|--------|
| 樣板/腳手架 | 2 天 | 15 分鐘 | ~100x |
| 寫測試 | 1 天 | 15 分鐘 | ~50x |
| 功能實作 | 1 週 | 30 分鐘 | ~30x |
| Bug fix + 回歸測試 | 4 小時 | 15 分鐘 | ~20x |
| 架構/設計 | 2 天 | 4 小時 | ~5x |
| 研究/探索 | 1 天 | 3 小時 | ~3x |

---

## 跨 Agent 相容性（v1.3：10 個 host）

gstack 不只限於 Claude Code，setup 會 auto-detect 已安裝的 agent：

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup        # 自動偵測
./setup --host <name>         # 指定特定 host
```

| Agent | Flag | Skills 安裝路徑 |
|-------|------|----------------|
| Claude Code | （預設） | `~/.claude/skills/gstack/` |
| OpenAI Codex CLI | `--host codex` | `~/.codex/skills/gstack-*/` |
| OpenCode | `--host opencode` | `~/.config/opencode/skills/gstack-*/` |
| Cursor | `--host cursor` | `~/.cursor/skills/gstack-*/` |
| Factory Droid | `--host factory` | `~/.factory/skills/gstack-*/` |
| Slate | `--host slate` | `~/.slate/skills/gstack-*/` |
| Kiro | `--host kiro` | `~/.kiro/skills/gstack-*/` |
| Hermes | `--host hermes` | `~/.hermes/skills/gstack-*/` |
| GBrain (mod) | `--host gbrain` | `~/.gbrain/skills/gstack-*/` |
| OpenClaw | （ACP 整合） | 透過 Claude Code session 自動載入 |

**OpenClaw 雙軌整合：**

1. **ACP spawn 模式** — OpenClaw 透過 ACP 起 Claude Code session，gstack skill 自動可用
2. **原生 ClawHub skills**（v1.x 新增）— 4 個方法論 skill 直接在 OpenClaw chat 跑：

```
clawhub install gstack-openclaw-office-hours \
                gstack-openclaw-ceo-review \
                gstack-openclaw-investigate \
                gstack-openclaw-retro
```

### Per-Model 行為 Overlay（v1.3 新增）

不同 LLM 需要不同 nudges。`bun run gen:skill-docs --model <model>` 套用對應 patch：

| Overlay | 針對問題 |
|---------|----------|
| `claude` | todo-list discipline |
| `gpt` | anti-termination + completeness |
| `gpt-5.4` | anti-verbosity（繼承 gpt） |
| `gemini` | conciseness |
| `o-series` | structured output |

Overlay 是純 markdown，編輯不需動程式碼。

---

## 與 Paperclip 的比較

| 面向 | gstack | Paperclip |
|------|--------|-----------|
| **層級** | 單 Agent 工作流強化 | 多 Agent 公司編排 |
| **核心問題** | 如何讓一個 AI Agent 按流程高效開發 | 如何讓多個 Agent 協作運營公司 |
| **角色系統** | 同一 Agent 扮演不同角色（slash command 切換） | 不同 Agent 有不同角色（org chart） |
| **技術核心** | Headless browser daemon + Markdown prompts | REST API + DB + WebSocket |
| **並行** | 靠 Conductor 管理多個 session | 內建多 Agent 編排 |
| **成本控制** | 無（依賴使用者自律） | Per-agent 預算硬限制 |
| **治理** | 內建 review gate（/review → /ship） | 完整審批流程 + 審計日誌 |
| **互補性** | 可以是 Paperclip 裡的一個 Agent 的工作流 | 可以編排多個跑 gstack 的 Agent |

**兩者是互補而非競爭的**：Paperclip 管「公司」，gstack 管「員工怎麼工作」。

---

## 與 Fluffy 的關聯

gstack 的幾個設計理念值得 Fluffy 生態系參考：

1. **SKILL.md template 系統** — 從原始碼自動生成 prompt 文件，避免文件與程式碼脫節
2. **Headless browser daemon 模式** — persistent state + sub-second latency 的瀏覽器互動
3. **Ref 系統** — 用 accessibility tree 而非 DOM selector 定位元素，更穩健
4. **Sprint 流程** — 結構化的 Think → Plan → Build → Review → Test → Ship 流程
5. **Boil the Lake 哲學** — AI 時代下完整性的邊際成本趨近零，應始終做完整實作
6. **測試三層架構** — 免費靜態驗證 + 付費 E2E + LLM 評判

---

## 成長數據

| 時間點 | Stars | 備註 |
|--------|-------|------|
| 前 48 小時（2026-03-13） | 10K | 上線爆紅 |
| 第 1 週（2026-03-18） | 23K | |
| 第 11 天（2026-03-22） | 39K | |
| 第 16 天（2026-03-27） | 50K | |
| 第 19 天（2026-03-30） | 56.1K | 第一版研究筆記時間點 |
| 第 38 天（2026-04-18） | ~73K | v1.1.x 連續 patch（VERSION sync、checkpoint 改名、ship 修復） |
| 第 39 天（2026-04-19） | ~76K | v1.3.0 發布（taste engine、context save/restore、benchmark-models） |
| 第 40 天（2026-04-20） | **77.7K** | 11.1K forks，467 watchers，351 open issues |

> Karpathy 在 2026-03 No Priors podcast 公開背書「12 月以來幾乎沒打過程式碼」，被寫進 gstack README 作為核心 hook。

## v1.3 重大架構升級（2026-04-19）

v1.3 是 gstack 從「結構化 prompt 集合」走向「**有狀態、會學習的工程系統**」的轉折版本。

### 1. Design Taste Engine — 設計品味會跨 session 累積

`/design-shotgun` 的每次 approve / reject 寫入 `~/.gstack/projects/$SLUG/taste-profile.json`，追蹤 font、color、layout、aesthetic direction 偏好，採用 **Laplace-smoothed confidence + 每週 5% 衰減**。下次 `/design-consultation` 跑時會根據過去偏好調整提案。

```
your taste profile (per project)
├── fonts: { "Geist Mono": 0.78, "Inter": 0.12 }
├── colors: { "neutral-warm": 0.65, "saturated-blue": 0.41 }
├── layouts: { "asymmetric-grid": 0.83, "centered-card": 0.22 }
└── decay: 5%/week (stale prefs fade)
```

### 2. Anti-AI-Slop 設計約束

| 機制 | 內容 |
|------|------|
| **Anti-convergence directive** | `/design-shotgun` 的 4-6 個變體必須換 font + palette + layout 三軸，否則 fail |
| **Embarrassment self-gate** | `/design-consultation` Phase 5 自問「人類設計師會不會覺得丟臉？」，fail 直接丟掉重生 |
| **Memorable forcing question** | Phase 1 必答「使用者會記得的那個唯一的東西是什麼？」 |
| **AI-slop font blacklist** | 從 ~8 fonts 擴到 10+，新增 Space Grotesk + system-ui |

### 3. Context Save/Restore — 你能 grep 的 session state

`/checkpoint` 因為被 Claude Code 內建 `/rewind` alias 遮蔽，v1.1.3 拆成 `/context-save` + `/context-restore`：

- 預設寫 markdown 到 `~/.gstack/projects/$SLUG/checkpoints/`
- 可選 **continuous mode**：`gstack-config set checkpoint_mode continuous`，自動 `WIP: <description>` commit + 結構化 `[gstack-context]` body 進 git log
- `/ship` 用 `git rebase --autosquash` 把 WIP commits 非破壞性壓掉，PR 保持乾淨可 bisect

> 設計理念：Claude Code 的內建 session 是 black box；gstack 的 context 是 plain text，可 grep / 編輯 / 跨機器 / 跨工具。

### 4. Per-Model Behavioral Overlays

5 個 overlay（claude / gpt / gpt-5.4 / gemini / o-series），純 markdown，針對各家 LLM 的行為缺陷寫對應 patch。Skill 生成時 `--model` flag 套用對應 overlay，preamble 印 `MODEL_OVERLAY: {model}` 供 debug。

### 5. Multi-Provider Benchmark CLI

`/benchmark-models` 同 prompt 跑 Claude / GPT / Gemini，比 latency / tokens / cost，可選 `--judge`（Sonnet 評分輸出品質，~$0.05/run）。**用資料而非 vibes 決定哪個模型適合哪個 skill。**

### 6. Mode-Posture Energy 修復（v1.1.2）

舊版 V1 writing-style 規則把所有輸出都壓回「診斷型疼痛」框架——`/plan-ceo-review` 的 SCOPE EXPANSION 變得乾巴巴，`/office-hours` 的 builder mode 退化成 PRD voice。v1.1.2 引入三軸 framing（pain reduction / capability unlocked / forcing-question pressure），cathedral language 終於能保留。

### 7. Token Ceiling 25K → 40K

200K-1M context window + prompt caching 已讓舊上限不再合理，重構為「失控成長的警示」而非強制壓縮。

## 與 Superpowers 的比較

| 面向 | gstack | Superpowers |
|------|--------|-------------|
| **Stars** | 56.1K（19 天） | 124K（6 個月） |
| **觸發方式** | 手動 slash command | 自動強制執行（1% Rule） |
| **TDD** | 可選（透過 `/qa`） | 強制（未測試的程式碼會被刪除） |
| **Planning** | 可選（`/office-hours`） | 強制（brainstorming 階段） |
| **Visual QA** | 真實 Chromium daemon + live 測試 | v5.0+ HTML mockup in browser |
| **安全** | `/cso` OWASP + STRIDE 掃描 | 非核心焦點 |
| **部署** | `/ship` 自動化發佈流程 | 手動 PR/merge |
| **Overhead** | 低：只呼叫需要的命令 | 高：10-20 分鐘規劃階段 |
| **Token 消耗** | 較低（按需呼叫） | 較高（每任務 50K+ tokens） |
| **最佳場景** | 產品思維 + visual QA + 完整 sprint | 強制 TDD + 長時間自主 session |

**互補使用**：gstack 負責 planning/QA/security/deploy 階段，Superpowers 負責 implementation 紀律。

## 關鍵洞察

1. **Markdown is all you need** — 除了 browser daemon，gstack 的核心就是精心撰寫的 Markdown prompt，證明 prompt engineering 的投資報酬率極高
2. **Browser 是真正的技術護城河** — daemon 模式、ref 系統、cookie 安全模型，這是非平凡的工程
3. **流程比工具重要** — gstack 的價值在於它定義了 sprint 流程，不是個別 skill 有多厲害
4. **40 天 77.7K stars** — 結合 Garry Tan 的個人品牌 + YC 背書 + Karpathy 公開站台 + 實際生產力數據（810× 2013 速率），成長曲線在 v1.3 後仍未轉平
5. **跨 10 個 host 的相容性是 Skills 生態的決定性能力** — 從 4 host（3 月）擴到 10 host（4 月），Slate / Kiro / Hermes / GBrain / Factory / OpenCode 一個月內全接上，證明 SKILL.md 標準正在贏
6. **First Principles > Best Practices** — ETHOS.md 的三層知識體系是值得深思的方法論
7. **安全 skill 是差異化亮點** — `/cso` 提供 OWASP + STRIDE 掃描 + 17 個 false positive 排除 + 8/10 信心閘門，早期使用者已報告找到真實 XSS 漏洞
8. **v1.3 的轉折：從「無狀態 prompt」進化成「有狀態系統」** — Taste Engine（設計品味會學）、Context Save/Restore（grep-able session state）、Model Overlays（每個 LLM 行為差異化）三件事合起來，gstack 從「結構化 prompt 集合」變成「會記憶、會適應、會跨工具的工程平台」。這是 Skills 生態下一個 12 個月的方向。
9. **Anti-AI-Slop 是高階 Skill 設計的試金石** — `/design-shotgun` 的「三軸必須換」+ `/design-consultation` 的「embarrassment self-gate」是把「品味」變成可機械驗證的閘門。對比 [khazix-skills](khazix-skills.md) 用「禁用詞 + 禁用標點」掃描來保證寫作品質，是同一思路在不同領域的展開——**用負面定義 + 機械閘門對抗 LLM 的回歸均值傾向**
10. **Context Save/Restore 是對 Claude Code 內建 session store 的對抗性設計** — 「Claude Code's own session store works fine on its own terms, but you can't grep it」是宣戰書。當官方工具的封閉性成為 friction，社群會用 plain text + git log 重建可審計的並行軌道

---

## 相關資源

- [GitHub Repo](https://github.com/garrytan/gstack)
- [Skill Deep Dives](https://github.com/garrytan/gstack/blob/main/docs/skills.md)
- [Builder Ethos](https://github.com/garrytan/gstack/blob/main/ETHOS.md)
- [Architecture](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md)
- [Browser Reference](https://github.com/garrytan/gstack/blob/main/BROWSER.md)
- [SitePoint Tutorial](https://www.sitepoint.com/gstack-garry-tan-claude-code/)
- [MarkTechPost 報導](https://www.marktechpost.com/2026/03/14/garry-tan-releases-gstack-an-open-source-claude-code-system-for-planning-code-review-qa-and-shipping/)
- [Medium 分析](https://agentnativedev.medium.com/garry-tans-gstack-running-claude-like-an-engineering-team-392f1bd38085)
- [Product Hunt](https://www.producthunt.com/products/gstack)
