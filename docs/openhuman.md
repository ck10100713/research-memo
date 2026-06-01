---
date: "2026-05-19"
category: "AI 應用"
card_icon: "material-account-heart"
oneliner: "tinyhumansai 的個人 AI 桌面助理，Rust+Tauri 桌面 mascot 會說話/開會、118+ OAuth 整合 20 分鐘自動 fetch、Memory Tree + Obsidian Wiki 在地持久記憶"
tags:
  - desktop-app
  - memory
---

# OpenHuman 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/tinyhumansai/openhuman> |
| 官網 | <https://tinyhumans.ai/openhuman> |
| GitBook 文件 | <https://tinyhumans.gitbook.io/openhuman/> |
| Discord | <https://discord.tinyhumans.ai/> |
| 創作者 | senamakel（X: @senamakel） |
| Trendshift | <https://trendshift.io/repositories/23680> |
| 規模 | 17,553 stars / GPL-3.0 / 創建 2026-02-18（**3 個月 17.5k stars / Early Beta**） |
| 語言 | Rust + TypeScript（pnpm workspace + Tauri 桌面 shell） |
| 工具鏈 | Node.js 24+ / pnpm 10.10.0 / Rust 1.93.0 / CMake / Ninja / ripgrep |

## 概述

**OpenHuman** 是 tinyhumansai（個人開發者 senamakel）的開源 **個人 AI 超智能桌面助理**，slogan：

> *"Your Personal AI super intelligence. Private, Simple and extremely powerful."*

跟絕大多數「coding agent」不同，OpenHuman 把 LLM **塞進你的日常生活** —— 不是「給開發者用的 ReAct loop」，而是「**會說話的桌面 mascot + 自動連你 118 個服務 + 持續累積對你的理解**」。

最核心的差異化是 **「在最短時間建立 personal context」**：

> *Most agents start cold. Hermes learns by watching you work; OpenClaw waits for plugins. Either way, you spend days or weeks before the agent knows enough.*
> *OpenHuman skips the wait. Connect your accounts, let auto-fetch pull data locally on a 20-minute loop, and then have Memory Trees compress everything into Markdown files stored in a Karpathy-style Obsidian wiki.*

→ 設計靈感是 **Karpathy 的 LLM Knowledgebase / obsidian-wiki workflow**（X post 2039805659525644595）。

## 核心模組

| 模組 | 內容 |
|------|------|
| 🎭 **Desktop Mascot** | 桌面有「臉」的代理人，會說話、回應環境、**會以真實 participant 身份加入你的 Google Meet**、跨週記得你、即使你停打字也在背景思考 |
| 🔌 **118+ OAuth Integrations** | Gmail、Notion、GitHub、Slack、Stripe、Google Calendar、Drive、Linear、Jira... **一鍵 OAuth**，每 20 分鐘自動 walk 連線拉新資料 |
| 🌳 **Memory Tree** | 連進來的資料 canonicalize 成 ≤ 3k token Markdown chunks → 評分 → 折成階層摘要樹 → **SQLite 存本機** |
| 📚 **Obsidian Wiki** | 同樣 chunks 落地成 `.md` 在 Obsidian-compatible vault，你可以打開、瀏覽、編輯 |
| 🔋 **Batteries Included** | Web search、scraper、coder toolset (filesystem/git/lint/test/grep)、**native voice (STT in + ElevenLabs TTS out + mascot lip-sync)** |
| 🧠 **Model Routing** | 自動把任務分派到對的 LLM（reasoning / fast / vision），**一個訂閱搞定** |
| 🤖 **Optional Local AI via Ollama** | 想全離線的可以走本機 |
| 🗜️ **TokenJuice** | 把每個 tool call / scrape / email / search 在送進 LLM 前先壓縮：HTML → Markdown、URL 縮短、verbose dedupe + summarise。**CJK / emoji 逐 grapheme 保留**，**降低成本/延遲達 80%** |
| 📨 **Messaging Channels** | inbound / outbound 跨各種頻道 |
| 🔒 **Privacy & Security** | workflow data on-device、加密本機 |

## 與其他 Agent Harness 的對比表（OpenHuman 自己列的）

| | Claude Cowork | OpenClaw | Hermes Agent | OpenHuman |
|---|---|---|---|---|
| Open-source | 🚫 Proprietary | ✅ MIT | ✅ MIT | ✅ GNU GPLv3 |
| Simple to start | ✅ Desktop + CLI | ⚠️ Terminal-first | ⚠️ Terminal-first | ✅ Clean UI, minutes |
| Cost | ⚠️ Sub + add-ons | ⚠️ BYO models | ⚠️ BYO models | ✅ One sub + TokenJuice |
| Memory | ✅ Chat-scoped | ⚠️ Plugin-reliant | ✅ Self-learning | 🚀 **Memory Tree + Obsidian vault + optional agentmemory backend** |
| Integrations | ⚠️ Few connectors | ⚠️ BYO | ⚠️ BYO | 🚀 **118+ via OAuth** |
| Auto-fetch | 🚫 None | 🚫 None | 🚫 None | ✅ **20-min sync into memory** |
| API sprawl | 🚫 Extra keys | 🚫 BYOK | 🚫 Multi-vendor | ✅ One account |
| Model routing | 🚫 Single model | ⚠️ Manual | ⚠️ Manual | ✅ Built-in |
| Native tools | ✅ Code-only | ✅ Code-only | ✅ Code-only | ✅ **Code + search + scraper + voice** |

→ 主要競爭定位：**「不是 coding agent，是日常生活 agent」**。

## 與 agentmemory 整合

OpenHuman 還可以選用 [agentmemory](https://github.com/rohitg00/agentmemory) backend：

```toml
# config.toml
[memory]
backend = "agentmemory"
```

→ **同一份 durable store 可以被 OpenHuman / Claude Code / Cursor / Codex / OpenCode 共用**。對「跨 agent 共享我的記憶」是個重要 pattern。

## 安裝

```bash
# macOS / Linux x64
curl -fsSL https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.sh | bash

# Windows
irm https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.ps1 | iex

# 或下載 DMG / EXE：tinyhumans.ai/openhuman
```

## 目前限制與注意事項

- **Early Beta**：repo 自陳「expect rough edges」，**production 用要謹慎**。
- **GPL-3.0**：商用 / fork 必須沿用 GPL，比 MIT / Apache 嚴格——對企業整合是限制。
- **OAuth 信任成本高**：要把 Gmail / Notion / GitHub / Stripe 都接給一個桌面 app，**就算 on-device 加密，依然要評估 token 洩漏風險**。
- **每 20 分鐘自動 fetch 的 quota 消耗**：每連線都會被 walked，**對 quota 緊的服務（Gmail API、Notion API）要小心**。
- **Mascot 加入 Google Meet 的隱私 / 合規問題**：作為「real participant」進會議，**對方 / 公司是否允許 AI 參加會議是法律灰區**，在某些司法管轄下可能違反錄音同意法。
- **作者個人 repo**：tinyhumansai 看似個人專案（senamakel），無公司背書；雖 17.5k stars 但**可持續性依賴一個人**。
- **「Tomorrow's users will be agents」反向應用**：跟 [[cli-anything]] 的 "Making ALL Software Agent-Native" 是**相反方向**——OpenHuman 把「人類使用者的所有服務」灌進 agent；CLI-Anything 把「所有軟體」變 agent 可用。兩者是補集。

## 研究價值與啟示

### 關鍵洞察

1. **「Personal AI = 把 agent 變成自己的 superset」是 2026 的新範式**：傳統 agent 是「給定任務、回答」；OpenHuman 是「持續自動拉資料、無問也在累積對你的理解」。這是 Karpathy 提的 **LLM Knowledgebase** 概念第一次有 production-grade 開源實作。
2. **Auto-fetch 20 分鐘 loop 是被低估的 UX 變革**：絕大多數 agent 是 pull-on-demand（你問才查），**OpenHuman 是 push-into-memory（agent 已經知道）**。對「what's on my calendar tomorrow」「what did Jane email me yesterday」這類 query，**沒有等資料的時間**——資料已經在 Memory Tree 裡了。
3. **Memory Tree + Obsidian Wiki 雙寫設計很聰明**：SQLite 給 agent 快查、`.md` 給人類可讀。**「資料一份、兩種介面」**，使用者隨時可以打開 Obsidian 編輯，agent 下次 walk 自動撿回——這個雙向同步是 LLM 知識庫的關鍵設計。
4. **TokenJuice 是 [[zeuikli-claude-code-best-practices]] 「caveman rules」的工程化版**：規則式壓縮（HTML → Markdown、URL 縮短、dedupe）+ **CJK grapheme 保留**。對比 LLMLingua 對 CJK 有 25% 衰退，TokenJuice 路線（規則式而非 token-pruning）是**正確方向**。
5. **「跟 agentmemory 整合」開啟了「跨 agent 共享記憶」可能**：你的 Claude Code 可以讀到你 OpenHuman 累積的 personal context。這指向**未來會有 "memory layer" 從 agent 中抽離出來成獨立元件**——就像 vector DB 從 RAG 系統抽離一樣。
6. **Mascot 加入會議是「具身化 AI」的早期實驗**：把 AI 從聊天框拉到「實體在場」（會議參與者），降低「AI 是工具」的隔閡感——但這也帶來社會 / 法律的全新邊界問題（會議錄音同意法、AI 是否該揭露身分）。
7. **個人 GPL 專案 vs HKUDS 機構級 Apache 的對比**：[[cli-anything]] / [[rag-anything]] 是 HKUDS 機構級開源（Apache 2.0，鼓勵商用）；OpenHuman 是個人 GPL（防 fork 套殼）。**兩種授權策略反映兩種社群成長路徑**——機構走廣泛採用、個人走守住主導權。
8. **「Agent 起步成本」是個未被充分討論的概念**：作者反覆強調「cold start」問題——Claude / Cursor / Codex 開新對話都不認識你。OpenHuman 主張 **「agent should know me before I ask」**，這個論點若被市場驗證，會改變 agent 產品設計（**從 chat-first 變成 context-first**）。

### 與其他研究的關聯

- 與 [[cli-anything]]：方向**相反互補**。CLI-Anything 把所有軟體變 agent 可用；OpenHuman 把所有「我的資料」灌進 agent。兩者搭起來就是「**agent 認識所有軟體 + agent 認識我**」。
- 與 [[abdixere-api]]：abdixere 主張「context memory 應該在 Skill 層」、OpenHuman 主張「context memory 應該在 Memory Tree + Obsidian Wiki 層」——**兩者都同意 context 不該在 system prompt 裡**，差異在於存放位置。
- 與 [[zeuikli-claude-code-best-practices]] 第 3 章 Prompt Caching：TokenJuice 是 caching 的補集——caching 解「重複 context 不要重傳」，TokenJuice 解「context 本身要先壓縮」。
- 與 [[why-your-ai-is-dumbing-down]]：那篇揭露 IDE 平台**截斷 context**，OpenHuman 主張**主動累積 context**。兩者是「被動失憶 vs 主動記憶」的兩端。
- 與 [[karpathy-llm-wiki]]：OpenHuman 是 Karpathy obsidian-wiki workflow 的最完整實作版。看過 Karpathy 原概念的人，可以看 OpenHuman 怎麼把它工程化。
- 與 [[fincept-terminal]]：兩者都是 native desktop app + 嵌入式腳本語言（Fincept Qt+C+++Python、OpenHuman Tauri+Rust+TS）。**native 桌面是個重新回歸的趨勢**，對抗 Electron 的疲勞。
- 與 [[ramp-ai-agents]]、[[appflowy]]：同屬「AI-powered desktop tool」族群，但 OpenHuman 是首個把 **「持續自動 fetch 個人資料」** 寫成核心賣點的開源專案。
