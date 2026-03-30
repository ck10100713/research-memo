---
date: "2026-03-30"
category: "Coding Agent 工具"
card_icon: "material-hammer-wrench"
oneliner: "Garry Tan 的 Claude Code 工作流系統，將 AI coding agent 組織成虛擬工程團隊"
---
# gstack 研究筆記

> **Repository:** [garrytan/gstack](https://github.com/garrytan/gstack)
> **作者:** Garry Tan（Y Combinator 總裁兼 CEO）
> **授權:** MIT
> **語言:** TypeScript (Bun)
> **Stars:** 56.1K（截至 2026-03-30）
> **Forks:** 7.3K
> **建立日期:** 2026-03-11

---

## 一句話總結

gstack 是 Garry Tan 開源的 **Claude Code 工作流系統**，把 AI coding agent 組織成一個虛擬工程團隊（CEO、Eng Manager、Designer、QA Lead、CSO、Release Engineer），透過 29 個 slash command skill 實現完整的軟體開發 sprint 流程。

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

## 29 個 Specialist Skills（截至 2026-03-30）

### Sprint 流程：Think → Plan → Build → Review → Test → Secure → Ship → Reflect

| 階段 | Skill | 角色 | 功能 |
|------|-------|------|------|
| **Think** | `/office-hours` | YC Office Hours | 六個 forcing questions 重新定義問題，挑戰前提，產生設計文件 |
| **Plan** | `/plan-ceo-review` | CEO / Founder | 重新思考問題，找出 10-star product，四種模式（擴展/選擇性擴展/維持/縮減） |
| **Plan** | `/plan-eng-review` | Eng Manager | 鎖定架構、資料流圖、邊界案例、測試矩陣 |
| **Plan** | `/plan-design-review` | Senior Designer | 每個設計維度 0-10 評分，說明 10 分長什麼樣，AI Slop 偵測 |
| **Plan** | `/plan-design-consultation` | Design Partner | 從零建立完整設計系統，研究市場、提出創意風險 |
| **Plan** | `/autoplan` | Planner | 自動產生開發計畫（新增） |
| **Review** | `/review` | Staff Engineer | 找 CI 過但 production 會爆的 bug，自動修簡單的，標記完整性缺口 |
| **Review** | `/design-review` | Designer Who Codes | 同 /plan-design-review 的審計，但會修改程式碼 |
| **Review** | `/design-shotgun` | Design Explorer | 產生多組 AI 設計方案供比較（新增） |
| **Debug** | `/investigate` | Debugger | 系統性根因除錯，Iron Law：不調查不修，3 次失敗後停止 |
| **Test** | `/qa` | QA Lead | 開真實瀏覽器測試，找 bug → 修復 → 產生回歸測試 → 驗證 |
| **Test** | `/qa-only` | QA Reporter | 同 /qa 但只報告不修 |
| **Test** | `/benchmark` | Performance Engineer | 頁面載入時間、Core Web Vitals、資源大小的基準測試 |
| **Security** | `/cso` | Chief Security Officer | OWASP Top 10 + STRIDE 威脅建模（新增） |
| **Ship** | `/ship` | Release Engineer | sync main → 跑測試 → 審計覆蓋率 → push → 開 PR |
| **Ship** | `/land-and-deploy` | Release Engineer | merge PR → 等 CI → 部署 → 驗證 production |
| **Monitor** | `/canary` | SRE | 部署後監控迴圈：console error、性能回歸、截圖異常偵測 |
| **Docs** | `/document-release` | Technical Writer | 更新所有文件以匹配剛發佈的內容 |
| **Reflect** | `/retro` | Eng Manager | 團隊感知的週回顧，per-person breakdown；支援 `/retro global` 跨 Agent 彙總 |
| **Browse** | `/browse` | QA Engineer | 真實 Chromium 瀏覽器，~100ms/command |
| **Cookies** | `/setup-browser-cookies` | Session Manager | 從 Chrome/Arc/Brave/Edge 匯入 cookies |

### 8 個 Power Tools

| Skill | 功能 |
|-------|------|
| `/codex` | OpenAI Codex CLI 獨立 review，跨模型分析 |
| `/careful` | 破壞性指令前警告（rm -rf, DROP TABLE, force-push） |
| `/freeze` | 鎖定編輯範圍到特定目錄 |
| `/guard` | /careful + /freeze 合一 |
| `/unfreeze` | 解除 /freeze |
| `/connect-chrome` | 連接 headed Chrome 處理 CAPTCHA/MFA（新增） |
| `/setup-deploy` | 一次性部署設定 |
| `/gstack-upgrade` | 自我更新 |

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

## 跨 Agent 相容性

gstack 不只限於 Claude Code：

```bash
# Codex
git clone https://github.com/garrytan/gstack.git ~/.codex/skills/gstack
cd ~/.codex/skills/gstack && ./setup --host codex

# Auto-detect
./setup --host auto  # 自動偵測已安裝的 agent
```

支援的 Agent Host：
- Claude Code (`~/.claude/skills/`)
- Codex (`~/.codex/skills/`)
- Gemini CLI
- Cursor

使用 [SKILL.md 標準](https://github.com/anthropics/claude-code) 和 `.agents/skills/` 目錄結構。

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

| 時間點 | Stars |
|--------|-------|
| 前 48 小時（2026-03-13） | 10K |
| 第 1 週（2026-03-18） | 23K |
| 第 11 天（2026-03-22） | 39K |
| 第 16 天（2026-03-27） | 50K |
| 第 19 天（2026-03-30） | 56.1K |

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
4. **19 天 56K stars** — 結合 Garry Tan 的個人品牌 + YC 背書 + 實際生產力數據，成長速度驚人
5. **跨 Agent 相容** — `.agents/skills/` 標準讓 skill 可在 Claude/Codex/Gemini/Cursor/Factory Droid 間共用
6. **First Principles > Best Practices** — ETHOS.md 的三層知識體系是值得深思的方法論
7. **安全 skill 是差異化亮點** — `/cso` 提供 OWASP + STRIDE 掃描，早期使用者已報告找到真實 XSS 漏洞，這是 Superpowers 缺乏的面向

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
