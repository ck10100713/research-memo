---
date: "2026-05-19"
category: "Coding Agent 工具"
card_icon: "material-shield-check"
oneliner: "Tech Leads Club 安全驗證過的 Skill registry，CLI + MCP 雙入口，主打「13% 市集 Skill 有重大漏洞、我們不一樣」，跨 19 個 AI coding agent，4.2k stars"
tags:
  - skills
  - security
  - mcp
---

# Tech Leads Club Agent Skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/tech-leads-club/agent-skills> |
| Skill registry 網站 | <https://agent-skills.techleads.club/> |
| GitHub Pages 索引 | <https://tech-leads-club.github.io/agent-skills/> |
| npm CLI | <https://www.npmjs.com/package/@tech-leads-club/agent-skills> |
| npm MCP | <https://www.npmjs.com/package/@tech-leads-club/agent-skills-mcp> |
| 安全掃描工具 | <https://github.com/snyk/agent-scan>（原 mcp-scan） |
| 規模 | 4,222 stars / 360 forks / 創建 2026-01-19（4 個月）/ TypeScript / Nx monorepo / Node ≥ 22 |

## 概述

**tech-leads-club/agent-skills** 是 Tech Leads Club 社群推出的 **「安全驗證過的 Skill registry」**，slogan：

> *"In an ecosystem where over 13% of marketplace skills contain critical vulnerabilities, Agent Skills stands apart as a hardened library of verified, tested, and safe capabilities."*

→ 直接拿 [Snyk Agent Scan 報告](https://github.com/snyk/agent-scan/blob/main/.github/reports/skills-report.pdf) 點名「**現有 marketplace 13.4% Skill 有重大漏洞**」當行銷論據，把自己定位成「**企業可信任的 skill 來源**」——這是 2026 Skill 生態系第一次有人**明確以 supply chain security 為主賣點**。

整個專案是 **Skill registry + CLI + MCP server** 三件套，跨 **19 個 AI coding agent** 通用。

## 三層產品架構

```text
                    Skill Catalog（社群貢獻、CI 嚴格驗證）
                            │
                            ▼
              ┌──────────────────────────────┐
              │  agent-skills.techleads.club │   ← 瀏覽介面
              │  GitHub Pages 索引           │
              └──────────────┬───────────────┘
                             │
              ┌──────────────┴───────────────┐
              ▼                              ▼
      ┌───────────────┐              ┌────────────────────┐
      │ CLI (npx)     │              │ MCP server         │
      │ 互動式安裝   │              │ progressive        │
      │ Copy/Symlink │              │ disclosure         │
      │ Global/Local │              │ search-first       │
      └───────────────┘              └────────────────────┘
              │                              │
              └──────────────┬───────────────┘
                             ▼
              19 個 AI Coding Agent (Claude Code / Cursor / Antigravity ...)
```

## 19 個支援的 Agent（三層級分類）

| Tier 1 (Popular) | Tier 2 (Rising) | Tier 3 (Enterprise) |
|------------------|-----------------|---------------------|
| Claude Code | Aider | Amazon Q |
| Cline | Antigravity (Google IDX) | Augment |
| Cursor | Gemini CLI | Droid (Factory.ai) |
| GitHub Copilot | Kilo Code | OpenCode |
| Windsurf | Kiro | Sourcegraph Cody |
| | OpenAI Codex | Tabnine |
| | Roo Code | |
| | TRAE | |

→ **19 個 agent first-class 支援**，是目前所有 Skill registry 裡覆蓋面最廣的。對比 [[mattpocock-skills]] 只專注 Claude Code、[[cli-anything]] 支援 7 個 agent，這個 registry 的**跨平台普世性是它的核心競爭力**。

## 安全設計（核心差異化）

README 把安全當第一賣點，做了 6 層防禦：

| 層 | 機制 |
|---|------|
| **0. 透明性** | 100% open source、**沒有任何 binary**（純文字 + script，可被 audit） |
| **1. CI 靜態分析** | Snyk Agent Scan 掃每個 Skill 才能 publish |
| **2. 完整性** | Lockfile + content hashing，內容竄改會被偵測 |
| **3. 人工審查** | 不是純自動化 marketplace，每個 prompt 經過人類 curation |
| **4. CLI 防禦** | sanitization、path isolation、symlink guards |
| **5. 原子操作** | atomic lockfile（中途失敗不會留半套狀態） |
| **6. 稽核** | audit trail（`agent-skills audit` 看歷史操作） |

→ 對比一般 `npx some-skills` 直接拿到的東西，這個 registry **把 supply chain security 做到了 OS package manager 等級**（apt / pacman / brew 那種完整性檢查）。

## Featured Skills（旗艦 5 個）

| Skill | 類別 | 用途 |
|-------|------|------|
| **tlc-spec-driven** | Development | **4 階段 Spec → Design → Tasks → Implement** 工作流，原子任務 + 跨 session 持久記憶 |
| **aws-advisor** | Cloud | AWS 架構設計 / 安全審查，整合 AWS MCP tools 給有出處的回答 |
| **playwright-skill** | Automation | 完整 Playwright 瀏覽器自動化（測頁面、填表、截圖、UX 驗證） |
| **figma** | Design | 從 Figma 拉設計 context、轉成 production code（design-to-code） |
| **security-best-practices** | Security | 各語言 / 框架的安全 review，偵測弱點、產報告、給 secure-by-default 修法 |

→ **`tlc-spec-driven` 是這個 registry 的招牌**——把「**規格驅動開發**」打包成可被任何 agent 載入的 skill，跟 [[mattpocock-skills]] 的 `grill-with-docs` 同類但走更結構化的 4 階段路線。

## CLI 設計（值得學習的細節）

```bash
# 互動精靈（最常用）
npx @tech-leads-club/agent-skills

# 列清單 / 安裝 / 更新 / 移除
agent-skills list
agent-skills install -s tlc-spec-driven
agent-skills install -s aws-advisor coding-guidelines docs-writer    # ← 一次裝多個
agent-skills install -s my-skill -a cursor claude-code               # ← 指定 target agent
agent-skills install -s my-skill -g                                  # ← 全域裝
agent-skills install -s my-skill --symlink                           # ← 用 symlink 不 copy
agent-skills install -s my-skill --force                             # ← 跳過 cache 重抓

agent-skills update -s my-skill         # 更新單個
agent-skills update                     # 更新全部已裝

agent-skills remove -s s1 s2 s3         # 一次移除多個
agent-skills remove -s my-skill -a cursor windsurf  # 只從特定 agent 移除

# 快取管理
agent-skills cache --clear              # 清快取
agent-skills cache --clear-registry     # 只清 registry index
agent-skills cache --path               # 看快取在哪

# 稽核
agent-skills audit                      # 看最近操作
agent-skills audit -n 20                # 最近 20 筆
agent-skills audit --path               # audit log 在哪
```

**設計亮點**：

| 設計 | 為什麼好 |
|------|---------|
| 互動精靈每步都有 **← Back** 選項 | 不會逼使用者整個重來 |
| 互動 + 命令列雙模式 | 新手用精靈、CI / 自動化用 flag |
| **支援 Copy / Symlink 兩種安裝** | symlink 給開發者改 skill 即時生效、Copy 給穩定使用 |
| **Global vs Local scope** | 個人偏好 vs 專案綁定兩種需求都覆蓋 |
| 一次裝多個 skill / 多個 agent | 批次操作友善 |
| **lockfile 保護**：`remove` 預設要過 lockfile 才放行，`--force` 才能繞過 | 防止誤刪正在被別處依賴的 skill |
| **audit log 內建** | 對 compliance / 企業是必要 |

→ 這份 CLI 設計**直接抄就能用**——比手刻一個 skill installer 強很多。

## MCP Server 變體：`@tech-leads-club/agent-skills-mcp`

第二個 npm 包是 **MCP server**，把整個 catalog 暴露給 agent 用 **progressive disclosure**：

| MCP Tool | 用途 |
|----------|------|
| `list_skills` | 瀏覽全部 skill（依分類） |
| `search_skills` | fuzzy search 找 skill |
| `read_skill` | 載入某個 skill 主說明 |
| `fetch_skill_files` | 抓特定 reference 檔案 |

關鍵設計：**`list_skills` 只有使用者明確要求「列清單」才該被呼叫**——平常 agent 自己用 `search_skills` 先搜，找到目標再 `read_skill`，**避免一次拉整個 catalog 進 context**。

```json
{
  "mcpServers": {
    "agent-skills": {
      "command": "npx",
      "args": ["-y", "@tech-leads-club/agent-skills-mcp"]
    }
  }
}
```

→ **CLI（離線安裝）+ MCP（runtime 即時搜尋）雙路線**，是同一個 catalog 的兩種消費模式，使用者可以同時用。

## How It Works（流程）

```text
1. Browse — CLI 拉 catalog 索引（~45 KB）
2. Select — 你選想裝的
3. Download — 從 CDN 抓內容，cache 在 ~/.cache/agent-skills/
4. Install — 寫進對應 agent 的 config（.claude / .cursor / .codex / ...）
```

**Offline 友善**：cache 在後不需要網路也能用。CI 環境設計：可以設 `--force` bypass cache 拿最新版。

## Repo 結構

```
agent-skills/
├── packages/
│   ├── skills-catalog/skills/      ← 所有 skill 內容
│   │   └── (category)/skill/
│   │       ├── SKILL.md
│   │       ├── templates/
│   │       └── references/
│   ├── agent-skills/ (CLI 本體)
│   └── agent-skills-mcp/ (MCP server)
├── libs/                            ← 共用程式碼
├── tools/                           ← 開發 / build 工具
└── .claude-plugin/ + .cursor-plugin/ ← 雙 IDE plugin
```

Nx monorepo + semantic-release + Nx Cloud——**重量級 enterprise-grade 工程設置**，對個人 fork 來改門檻略高。

## 目前限制與注意事項

- **License 標為 "Other"**：repo 有 LICENSE 但 GitHub 無法分類成已知授權，**商用前必須讀 LICENSE 全文**。
- **「13% 漏洞」數據來自 Snyk 自家報告**：Snyk 也是 agent-scan 工具的擁有者，**有利益關係**。數據可信但要意識到行銷脈絡。
- **「Verified」程度仍是相對性的**：人工 curation 跟自動掃描都不是零風險，**新手不該因此完全信任所有 skill**。
- **Nx monorepo 對個人貢獻者門檻高**：跑起 nx + jest + semantic-release 一整套 toolchain 對非 enterprise dev 學習曲線陡。
- **Featured skills 仍少（5 個）**：4 個月、4k stars、但 skill 數量遠不如 [[mattpocock-skills]] 的 15+ 或 [[cli-anything]] 的 60+。**「品質高但量少」是這個 registry 目前的狀態**。
- **Node.js ≥ 22 要求高**：很多 Linux 發行版預設 node 還在 20，要先升。
- **「Spec-driven」哲學跟 [[mattpocock-skills]] 的「real engineering」立場相近**，但 spec-driven 路線比 Matt 的 grilling + tdd 路線更重——**團隊 / 多人開發較適合，個人開發者可能 overkill**。
- **每個 agent 的 plugin path 不同**：CLI 要適配 19 個 agent 的 config layout 是巨大維護成本，**新 agent 加入支援會有延遲**。

## 研究價值與啟示

### 關鍵洞察

1. **「Skill supply chain security」是 2026 浮現的新議題**：Snyk 提的 13% 漏洞率報告是個 wake-up call——隨著 Skill 從個人 dotfile 走向 enterprise dependency，**它們需要 npm / PyPI 等級的 supply chain security**。Tech Leads Club 是第一個明確抓住這個 positioning 的 registry。
2. **「CLI + MCP 雙入口」是 Skill registry 的正確架構**：CLI 解決「離線安裝」，MCP 解決「runtime 即時搜尋」。**兩個入口同一個 catalog**——這個 pattern 是 [[cli-anything]] 的 CLI-Hub 也走的路。**Skill registry 的事實標準正在浮現**。
3. **`list_skills` 不該預設被呼叫**這個 MCP 設計細節很重要：absent intentional user request，**agent 應該用 `search_skills` 先精準找，不要拉整個 catalog 進 context**——這是 progressive disclosure 的具體實踐，對保 context 預算極為關鍵。
4. **19 個 agent 的清單本身就是研究素材**：第一次有人把 Tier 1/2/3 整理出來——**Tier 1 是市場已驗證、Tier 2 是新興、Tier 3 是企業專用**。看哪個工具進哪一 tier，就能看出當下 agent 市場格局。**Antigravity 被歸到 Tier 2（Google IDX）值得注意**。
5. **lockfile + audit log + `--force` 繞過**：這套機制是「**包管理器級嚴謹度**」搬到 Skill 場景。對比一般「下載 .md 檔丟進 .claude/ 完事」的隨意做法，這套設計**為企業合規開了門**——AICPA / SOC2 audit 場景能直接用 audit log 證明可追溯性。
6. **「13% 漏洞」當行銷武器是個聰明的差異化策略**：當 Skill marketplace 開始爆量（Anthropic 自家、Claude marketplace、Cursor marketplace、各種社群 registry），**「安全」會成為購買決策因素**。Tech Leads Club 比同業早 6-12 個月卡這個 positioning。
7. **Tier 3 (Enterprise) 的存在反映 B2B 市場分歧**：Amazon Q、Augment、Droid (Factory.ai)、OpenCode、Sourcegraph Cody、Tabnine 都進 Tier 3——**這些工具的使用者預算 / 合規需求顯著不同於 Tier 1 個人開發者**。對想做 B2B Skill 生意的人，這個分類是市場地圖。
8. **`tlc-spec-driven` 4 階段 (Specify → Design → Tasks → Implement) 跟業界其他 spec-first 路線收斂**：對應 [[mattpocock-skills]] 的 grill-with-docs、Sequoia Capital 的 spec-driven dev 倡議、Amazon Kiro 的 spec-first agent——**spec-driven 已成 2026 agent 工作流的主流之一**。

### 與其他研究的關聯

- 與 [[mattpocock-skills]]、[[casper-claude-skill-design-gallery]]、[[cli-anything]]：**Skill 生態系四強各據一方**——Matt 走 workflow 哲學、Casper 走 design output、CLI-Anything 走 tool wrapping、**Tech Leads Club 走 enterprise security**。對「Skill 該怎麼定位」這個問題，四個案例就是四個答案。
- 與 [[abdixere-api]]：abdixere 主張「context memory 應該在 Skill 層」，本 registry 是「**那 Skill 從哪來、怎麼確保可信**」這個下游問題的答案。
- 與 [[zeuikli-claude-code-best-practices]] 第 5 章 Skill 撰寫：zeuikli 列了「描述要寫 Do NOT use for」等原則，本 registry 是這些原則的工程化執行單位——**所有進入 catalog 的 skill 都已通過這套規範審查**。
- 與 [[ai-agents-for-beginners]]、[[mcp-for-beginners]]：Microsoft 教材講原理，本 registry 是學完後**找成熟 skill 立即生產用**的去處。
- 與 [[fincept-terminal]]、[[daily-stock-analysis]] 等量化工具：可以**寫一個 quant-research skill 上傳到 Tech Leads Club catalog**——同時被 19 個 agent 使用、有 audit log、過 Snyk 掃描。對「想分享自己量化方法」的人是 distribution 通路。
- 與 [[claude-financial-services-plugins]]：Anthropic 官方 plugin 是 vendor-locked，本 registry 是 vendor-neutral——**「跨 agent skill」vs「綁定 vendor skill」**是兩種未來方向的對比。
- 對台灣開發者：可以**把 [[aqua-usage-menubar]] 的「台灣用量監控」面板選擇邏輯封裝成 skill 上傳**，讓任何 agent 可以呼叫——這是把在地工具走向國際的可行路徑。
