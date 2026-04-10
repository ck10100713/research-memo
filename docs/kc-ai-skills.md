---
date: "2026-04-10"
category: "Coding Agent 工具"
card_icon: "material-toolbox"
oneliner: "12 個實戰型 Claude Code Skills — 從 repo 安全掃描到反指標分析，解決真實問題的 skill 合集"
---

# KC AI Skills — 真的會做事的 AI Skill 合集

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [KerberosClaw/kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) |
| 中文 README | [README_zh.md](https://github.com/KerberosClaw/kc_ai_skills/blob/main/README_zh.md) |
| 相關專案：kc_job_radar | [KerberosClaw/kc_job_radar](https://github.com/KerberosClaw/kc_job_radar) |
| 相關專案：kc_openclaw_local_llm | [KerberosClaw/kc_openclaw_local_llm](https://github.com/KerberosClaw/kc_openclaw_local_llm) |
| CTF 搭配 skill | [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills) |

## 專案概述

KC AI Skills 是台灣開發者 KerberosClaw 打造的 12 個 Claude Code skill 合集，主打「解決真實問題」——不是「摘要 PDF」那種 skill，而是「推 code 前幫我掃機敏資訊」「安裝套件前幫我做安全掃描」「幫我追蹤反指標女神的 Threads 然後做台股分析」這種 skill。

遵循 [Claude Code skill 規範](https://code.claude.com/docs/en/skills)（SKILL.md + scripts/），但設計為框架無關——可以用在 Claude Code、OpenClaw、或任何支援 prompt 載入的 LLM 客戶端。每個 SKILL.md 都是獨立的 markdown 指令文件，複製貼上就能用。

## 12 個 Skills 完整解析

### 開發工作流類

#### 1. prep-repo — 推 GitHub 前的 Checklist

推 code 前的「我是不是忘了什麼」自動檢查，涵蓋 7 大面向：

| 檢查項目 | 內容 |
|----------|------|
| README | 雙語（EN + zh-TW）、badges、Security Notice |
| Docs | 中文文件附 English summary、內部連結有效 |
| Naming | 命名一致性、prefix 慣例 |
| Git Commits | 分類式 commit message（`Core:` `fix:` `Docs:` 等） |
| Files | `.gitignore`、LICENSE、無垃圾檔 |
| **機敏資訊掃描** | IP、API token、Telegram ID、SSH path — 掃 tracked files + git history |
| Co-Authored-By | 移除 AI 共同作者標記 |

**亮點**：不只掃現有檔案，還掃 git history——很多人只顧 `.gitignore` 但忘了 key 曾經被 commit 過。

#### 2. spec — Spec-Driven 開發流程

從模糊想法到驗收結案的完整流程引導：

```
/spec 做一個 Markdown loader
    │
    ▼ Stage Detection（自動判斷狀態）
    │
    ├─ 小需求 → Spec Stage
    │   └─ requirements.md → plan.md → tasks.md → 實作 → check → report
    │
    └─ 大需求 → Discovery Stage
        └─ DESIGN.md（整體架構）→ 拆成多個 spec → 逐一實作
```

**自動判斷規模**：「這個需求能拆成 5-10 項 checklist 就做完嗎？」能→單一 spec；不能→先做 Discovery。

#### 3. md2pdf — Markdown 轉 PDF

不只是 `pandoc` 的 wrapper，而是處理了所有詭異 edge case 的完整 pipeline：

| 處理 | 說明 |
|------|------|
| ASCII Art → Mermaid | 自動辨識流程圖結構並轉換 |
| CJK 字型 | 正確處理繁中/日文字型 |
| `$` 符號 | pandoc 會把 `NT$1` 解讀為 LaTeX math，自動 escape |
| 3 種 CSS 風格 | Professional / Technical / Minimal |
| 不修改原檔 | 所有操作在 `_pdf.md` 副本上進行 |

#### 4. rewrite-tone — 技術文件語氣改寫

把乾巴巴的技術文件變成「踩坑故事」風格：

- 「問題描述」→ 用情境 hook 讀者
- 「設計決策」→ 「被現實教訓出來的決策」
- 被動語態 → 第一人稱（「我們」）
- **不改 code blocks、Mermaid、表格** — 只改文字段落

### 安全與分析類

#### 5. repo-scan — GitHub Repo 安全掃描

安裝開源套件前的安全評估，6 階段掃描：

```
Phase 1：專案概覽（stars、license、最後 commit）
Phase 2：依賴分析（package.json / requirements.txt / go.mod / Cargo.toml）
Phase 3：靜態弱點掃描（硬編碼 credentials、危險函數、注入風險）
Phase 4：供應鏈風險（typosquatting、鬆散版本約束、可疑 post-install）
Phase 5：GitHub Issues 安全回報（搜尋 security/vulnerability 相關 issue）
Phase 6：維護者健康度（commit 頻率、contributor 數、response time）
```

**實用性**：`npm install random-package` 不該是一場賭博。

#### 6. ctf-kit — CTF 逆向工程工具箱

聚焦 **Windows 應用程式驗證繞過** 的實戰 playbook，從 67+ 次失敗中淬煉：

| 涵蓋範圍 | 說明 |
|----------|------|
| 保護殼 | VMProtect、Themida、UPX、自製殼 |
| 驗證類型 | 網路驗證、本地驗證、時間驗證、混合驗證 |
| 工具 | Frida recon scripts（即用型）、零依賴 PE 分析器 |
| 準則 | 「對齊目標，反覆確認」「先驗證再行動，不猜測」 |

**範圍界定清晰**：不覆蓋的場景（Linux ELF、.NET、Web）會導向 [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills)。

### 求職類

#### 7. job-scout — 求職前公司調查

投履歷前的 due diligence，4 階段調查：

| Phase | 內容 | 搜尋來源 |
|-------|------|---------|
| 1. 公司基本資料 | 統一編號、資本額、員工數、上市櫃狀態 | findbiz、twincn |
| 2. 財務與營運 | 營收趨勢、裁員/減資紀錄、融資狀況 | 新聞、財報 |
| 3. 員工評價 | 薪資行情、面試經驗、工作環境 | salary.tw、interview.tw、Qollie、PTT |
| 4. 職位行情分析 | 該職位的市場薪資、技術棧需求 | 104、CakeResume |

**台灣本地化**：搜尋來源完全對準台灣求職生態（104、比薪水、面試趣、PTT Tech_Job）。

#### 8. job-radar — 求職自動化遙控台

搭配 [kc_job_radar](https://github.com/KerberosClaw/kc_job_radar) Docker 容器，在 Telegram 遙控求職流程：

| 指令 | 功能 |
|------|------|
| 「寫信」 | 讀取 JD → 批量產生客製化求職信 → zip → Telegram 傳送 |
| 「整理雷達」 | 封存「沒興趣」+ 搬移「想投遞」+ 產生 context |
| 「搜尋職缺」 | 搜尋 104 新職缺 → 篩選 → 去重 → 寫入 Google Sheet |
| 「評估雷達」 | 一鍵標記「想投遞/沒興趣」 |
| 「刷新追蹤」 | 抓取 104 職缺最新狀態更新 |

### 本地 LLM 與搜尋類

#### 9. llm-benchmark — 本地 LLM 效能評測

在下載模型前先搞清楚你的 GPU 能跑什麼：

```
Step 0：環境檢查（Ollama 安裝/運行）
Step 0.5：VRAM 清空（停 OpenClaw、重啟 Ollama、確認 nvidia-smi）
Step 1：GPU/VRAM 偵測 → 推薦模型大小
Step 2：下載推薦模型
Step 3：Benchmark 跑分（回應速度、token/s、記憶體使用）
Step 4：與現有模型比較 → Markdown 報告
```

**細節到位**：benchmark 前會停掉 OpenClaw 釋放 VRAM，完成後自動還原——這種「考慮到使用者環境」的設計是手工 skill 的價值。

#### 10. searxng — 隱私搜尋

讓本地 LLM 透過自架的 SearXNG 實例搜尋網路，不把搜尋紀錄送給 Google：

```bash
uv run scripts/searxng.py search "query"              # 基本搜尋
uv run scripts/searxng.py search "query" --category news   # 新聞
uv run scripts/searxng.py search "query" --format json     # JSON 輸出
```

### 台股與排程類

#### 11. banini — 反指標女神追蹤器

追蹤台灣知名「反指標」投資人巴逆逆（banini31）的 Threads 貼文，用 Claude 做反指標分析：

| 她的狀態 | 反指標解讀 |
|---------|-----------|
| 買入/加碼 | 該標的可能下跌 |
| 被套/持有中 | 可能繼續跌（她還沒認輸） |
| 停損/賣出 | 可能反彈（她認輸 = 底部訊號） |
| 看多/喊買 | 可能下跌 |
| 空單/買 put | 可能飆漲 |

**技術實作**：Playwright 本地抓 Threads → Claude 做分析 → 零 API 成本（原版用 Apify + LLM API 要 $11/月）。

#### 12. skill-cron — 排程推播管理器

解決 `claude -p` 不支援 `/skill` 語法的問題，讓任何 skill 都能排程 + Telegram 推播：

```
/skill-cron
┌─ 排程管理器 ──────────────┐
│ 1. 列出排程與狀態         │
│ 2. 新增排程               │
│ 3. 移除/啟停排程          │
│ 4. Telegram 設定          │
│ 5. 手動執行一次           │
└───────────────────────────┘
```

**核心解法**：skill 的 frontmatter 加入 `headless-prompt` 欄位 → skill-cron 掃描 → 自然語言轉 cron 表達式 → 註冊 crontab → 執行結果推播 Telegram。

## 安裝方式

```bash
# Clone 整個合集
git clone https://github.com/KerberosClaw/kc_ai_skills.git

# 只裝你要的（Claude Code）
cp -r kc_ai_skills/prep-repo ~/.claude/skills/

# 或裝到 OpenClaw
cp -r kc_ai_skills/searxng ~/.openclaw/workspace/skills/

# 或直接複製 SKILL.md 內容貼到任何 AI 的 system prompt
```

## Skill 結構規範

```
skill-name/
├── SKILL.md          # Frontmatter（name, description, version）+ 完整指令
└── scripts/          # 可執行腳本（選用）
    └── script.py
```

每個 SKILL.md 都是自包含的——不依賴外部 SDK、不需要 API key（除了各自功能需要的外部服務）。

## 目前限制

| 限制 | 說明 |
|------|------|
| 本地開發環境導向 | 設計給本地和受信任內網使用，非生產環境部署 |
| 部分 skill 有硬依賴 | job-radar 需要 Docker + kc_job_radar、banini 需要 Playwright |
| 台灣本地化強 | job-scout、banini 深度綁定台灣資料來源（104、比薪水、Threads） |
| 小專案規模 | 41 stars，單一作者維護 |
| 無 Plugin Marketplace | 需手動 `cp -r` 安裝，不支援 `/plugin marketplace add` |

## 研究價值與啟示

### 關鍵洞察

1. **「實戰型 skill」vs「展示型 skill」的差距**：和 Slavingia Skills（書→skill、概念框架）不同，KC AI Skills 每個 skill 都附帶 scripts/、處理 edge case、考慮環境差異（停 OpenClaw 釋放 VRAM、Docker 內操作 Google Sheet 而非直接打 API）。這代表兩種 skill 設計哲學——一種是「引導你思考」，一種是「幫你做事」。

2. **`headless-prompt` 是 skill 排程化的關鍵設計**：skill-cron 透過 frontmatter 的 `headless-prompt` 欄位實現「非互動模式執行 skill」。這解決了 `claude -p` 不支援 `/skill` 的限制，是目前 Claude Code 生態中少數處理「skill 排程」問題的方案。

3. **台灣本地化 skill 是藍海**：job-scout 對準台灣求職生態（104、比薪水、面試趣、PTT），banini 追蹤台灣投資圈的梗（反指標女神）。全球化的 skill 合集（如 awesome-claude-skills）不會做這些——本地化 skill 的價值就在於它知道使用者的上下文。

4. **repo-scan 是被低估的安全實踐**：在 `npm install` 或 `pip install` 前先做 6 階段安全掃描（靜態分析、供應鏈、維護者健康度），這應該是每個開發者的標準流程——但幾乎沒人做。把它變成一個 slash command 大幅降低了執行門檻。

5. **spec skill 展示了「AI 引導式開發」的模式**：不是 AI 幫你寫 code，而是 AI 引導你走完「需求→spec→plan→tasks→實作→驗收→報告」的完整流程。這比純 code generation 更有價值——它幫你避免「先寫再說→之後全部重寫」的循環。

### 與其他專案的關聯

- **Slavingia Skills**：兩者是 skill 設計哲學的兩極——Slavingia 是「概念框架→互動引導」，KC 是「實戰腳本→自動執行」。前者 7,500 stars 靠的是名人效應和書本品牌，後者 41 stars 但每個 skill 都能實際跑起來做事
- **Superpowers**：KC 的 spec skill 和 Superpowers 的 writing-plans / executing-plans 功能重疊，但 spec 更完整（含 Discovery Stage 和結案報告）
- **Context Hub**：searxng skill 讓本地 LLM 能搜尋網路，Context Hub 讓 Agent 能取得 API 文件——都在解決「Agent 怎麼取得外部知識」的問題
- **Career-Ops**：job-scout + job-radar 組合和 Career-Ops 解決同一個問題（AI 驅動的求職流程），但 KC 版本更深度本地化（台灣 104、比薪水等）
- **OsintRadar / pyWhat**：repo-scan 的安全掃描能力和 OSINT 工具互補——repo-scan 專注於開源套件的供應鏈安全
