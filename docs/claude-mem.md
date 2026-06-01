---
date: "2026-05-27"
category: "Coding Agent 工具"
card_icon: "material-brain"
oneliner: "thedotmack 的跨 session 持久記憶系統（78k stars），自動捕捉 agent 行為→AI 壓縮成語義摘要→注入未來 session，3-layer 漸進揭露搜尋省 ~10x token，SQLite+Chroma 混合檢索，支援 Claude Code/OpenClaw/Codex/Gemini 等多 host"
tags:
  - claude-code
  - memory
---

# Claude-Mem 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/thedotmack/claude-mem> |
| 官方文件 | <https://docs.claude-mem.ai/> |
| 官網 | <https://claude-mem.ai> |
| 繁中 README | <https://github.com/thedotmack/claude-mem/blob/main/docs/i18n/README.zh-tw.md> |
| License | Apache-2.0（v6.5.0） |
| Web Viewer | http://localhost:37777（本機） |

## 專案概述

**Claude-Mem** 是 thedotmack 開發的「跨 session 持久記憶壓縮系統」（**78,865 stars / 6,779 forks**，TypeScript，Apache-2.0），是目前 Claude Code 生態中星數最高的記憶類專案之一，登上 Trendshift。

它解決的核心痛點：**LLM agent 的記憶會隨 session 結束而消失**。Claude-Mem 的做法是「自動捕捉 agent 在 session 中做的每件事（tool 使用觀察）→ 用 AI 壓縮成語義摘要 → 在未來 session 開始時把相關 context 注入回去」。這讓 Claude 即使在 session 結束或重連後，仍能維持對專案的知識連續性。

關鍵特色是**多 host 支援**——不只 Claude Code，還涵蓋 OpenClaw、Codex、Gemini CLI、Hermes、Copilot、OpenCode 等。一句 `npx claude-mem install` 即裝即用，context 自動在新 session 出現，**無需人工介入**。

## 核心架構

### 六大組件

| 組件 | 角色 |
|------|------|
| **5 Lifecycle Hooks** | SessionStart / UserPromptSubmit / PostToolUse / Stop / SessionEnd（共 6 個 hook script） |
| **Smart Install** | 快取式依賴檢查（pre-hook，非 lifecycle hook） |
| **Worker Service** | port 37777 的 HTTP API + web viewer UI + 10 個搜尋端點，由 Bun 管理 |
| **SQLite Database** | 儲存 sessions / observations / summaries |
| **mem-search Skill** | 自然語言查詢 + 漸進揭露 |
| **Chroma Vector DB** | 混合語義 + 關鍵字搜尋（hybrid search） |

資料流：hook 捕捉 → AI 壓縮成 observation/summary → SQLite + Chroma 儲存 → 下次 session 由 hook 注入相關 context。

### 3-Layer 漸進揭露搜尋（最精華設計）

Claude-Mem 提供 4 個 MCP 工具，遵循 token-efficient 的三層 workflow：

```
1. search          → 取得 compact 索引 + IDs（~50-100 tokens/result）
2. timeline        → 取得某結果周邊的時序 context
3. get_observations → 只對篩選後的 IDs 抓完整細節（~500-1,000 tokens/result）
```

```typescript
// Step 1: 搜尋索引
search(query="authentication bug", type="bugfix", limit=10)
// Step 2: 檢視索引，挑出相關 IDs（如 #123, #456）
// Step 3: 抓完整細節
get_observations(ids=[123, 456])
```

> **核心洞察**：先搜尋輕量索引、過濾後才抓重量細節 → **~10x token 節省**。這正是「progressive disclosure（漸進揭露）」哲學的具體實現。

## 快速開始

```bash
# 標準安裝（會註冊 plugin hooks + worker service）
npx claude-mem install

# 其他 host
npx claude-mem install --ide gemini-cli
npx claude-mem install --ide opencode

# 或 Claude Code 內 plugin marketplace
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# OpenClaw gateway 一鍵裝
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

> **重要陷阱**：`npm install -g claude-mem` 只裝 **SDK/library**，不會註冊 plugin hooks 或設定 worker。一定要用 `npx claude-mem install` 或 `/plugin`。

## 關鍵功能

- 🧠 **Persistent Memory** — context 跨 session 存活
- 📊 **Progressive Disclosure** — 分層記憶檢索，附 token cost 可見性
- 🔍 **Skill-Based Search** — 用 mem-search skill 查專案歷史
- 🖥️ **Web Viewer UI** — http://localhost:37777 即時記憶串流
- 🔒 **Privacy Control** — `<private>` 標籤排除敏感內容入庫
- 🔗 **Citations** — 用 ID 引用過往觀察（`/api/observation/{id}`）
- 🧪 **Beta Channel** — 實驗功能如 **Endless Mode**（仿生記憶架構，適合超長 session）

### Mode & 語言設定

`~/.claude-mem/settings.json` 的 `CLAUDE_MEM_MODE` 同時控制 workflow 行為與 observation 語言：

```json
{ "CLAUDE_MEM_MODE": "code--zh" }
```

`code`（英文）、`code--zh`（簡中，內建）、`code--ja`（日文）等，pattern 為 `code--[ISO639-1]`。

## 系統需求

Node.js ≥18、Claude Code（含 plugin 支援）、Bun（自動裝）、uv（Python 套件管理，向量搜尋用，自動裝）、SQLite 3（內建）。

## 目前限制 / 注意事項

- **安裝方式易踩雷**——`npm install -g` 只給 library，必須用 `npx claude-mem install`
- **本機服務依賴**——worker 跑在 port 37777，需保持運作；多了 Bun/uv/Chroma 等執行期依賴
- **228 open issues**——專案演進極快（README 提到 v3→v5 架構演進），邊角穩定性待觀察
- **記憶品質取決於壓縮模型**——observation 摘要由 AI 生成，壓縮失真或注入過量都可能反噬 context
- **隱私需主動管理**——預設捕捉「agent 做的每件事」，敏感內容要自己用 `<private>` 排除

## 研究價值與啟示

### 關鍵洞察

1. **「3-Layer 漸進揭露」是記憶系統的 token 經濟學典範**：search（索引）→ timeline（時序）→ get_observations（細節）三層，先用 ~50-100 token 的索引過濾，再對少數 ID 抓 ~500-1,000 token 的細節，省下 ~10x token。這直接回應了「記憶系統最大的反模式 = 把所有歷史一股腦塞進 context」。任何做 RAG/記憶的人都該學這個「先索引後取詳情」的分層 fetch。

2. **「Workspace/observation 為單位」而非「對話為單位」的記憶粒度**：claude-mem 捕捉的是 tool 使用 observation（agent 做了什麼），壓縮成語義摘要並給每筆一個可引用 ID。這比「存整段對話」更結構化、可檢索、可引用（citation）。記憶的單位設計決定了檢索品質。

3. **hook-driven 的自動化是「零摩擦記憶」的關鍵**：靠 5 個 lifecycle hook（SessionStart 注入、PostToolUse 捕捉、SessionEnd 歸檔）做到全自動、無需人工介入。這跟本站的 auto-memory 系統理念一致——記憶必須是「副作用式自動發生」，要使用者手動存就一定會荒廢。

4. **多 host 通用是它衝到 78k stars 的結構性原因**：不綁死 Claude Code，而是支援 OpenClaw/Codex/Gemini/Hermes/Copilot/OpenCode。記憶是所有 agent 的共同剛需，做成跨 host 的記憶層 = 把 TAM 從「Claude Code 用戶」擴大到「所有 coding agent 用戶」。這是平台中立策略的勝利。

5. **本機優先（local-first）+ web viewer 的透明性設計**：SQLite + Chroma 都在本機，http://localhost:37777 提供即時記憶串流與 token cost 可見性。相比 mem0/supermemory 等雲端記憶服務，local-first 在隱私與成本上有結構優勢，web viewer 則解決「記憶是黑箱」的信任問題。

6. **Endless Mode（仿生記憶架構）指向記憶研究的前沿**：beta channel 的 Endless Mode 用「biomimetic memory architecture」處理超長 session，呼應人類記憶的鞏固/遺忘機制。這暗示下一代 agent 記憶不只是「存更多」，而是「像生物一樣選擇性鞏固與遺忘」。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs 本站 auto-memory 系統 | 同為「自動捕捉+跨 session 注入」，claude-mem 多了向量檢索與 web viewer，auto-memory 偏 file-based 語義分類 |
| vs mem0 / supermemory / openmemory | claude-mem 是 local-first（SQLite+Chroma 在本機），這些多為雲端服務；topics 直接點名 mem0/supermemory 為對標 |
| vs [Context Hub](context-hub.md) / [MemPalace](mempalace.md) | 都在做 context/記憶管理，claude-mem 的差異化在 hook-driven 全自動 + 3-layer token 經濟學 |
| vs [Knowledge Work Plugins](knowledge-work-plugins.md) | KWP 的 productivity plugin 也談「個人 context 記憶」，但 claude-mem 是專精、可跨 host 的記憶引擎 |
| vs [Superpowers](superpowers.md) | Superpowers 提供 skill 紀律，claude-mem 提供記憶基礎設施，兩者正交可疊用 |

**最大啟示**：claude-mem 證明「記憶」是 agent 生態最被低估的剛需，而做好記憶的關鍵不是「存更多」，是**「token 經濟學」**——用 3-layer 漸進揭露讓檢索成本可控、可見。對任何要給 agent 加記憶的人，核心教訓是：先設計好「記憶的粒度（observation）」與「分層 fetch（索引→時序→細節）」，再談存什麼。同時，做成跨 host 的中立記憶層，是把單一工具放大成基礎設施的關鍵策略。
