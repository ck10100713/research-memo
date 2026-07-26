---
date: "2026-07-26"
category: "Coding Agent 工具"
card_icon: "material-view-dashboard-variant"
oneliner: "遠振資訊 solo 維護的 OpenClaw 營運儀表板——server-resident、瀏覽器內操作 VPS，含晨報/備份/第二大腦/LINE 客服 ops"
tags:
  - self-hosted
  - automation
  - taiwan
---

# Mission Control Center 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★8 / 4 forks / Apache-2.0 / TypeScript） | [github.com/YJ-Software/mission-control-center](https://github.com/YJ-Software/mission-control-center) |
| README（繁中，617 行，極完整） | [README.md](https://github.com/YJ-Software/mission-control-center/blob/main/README.md) |
| 開發者 | [遠振資訊 / YJ-Software](https://github.com/YJ-Software)（台灣） |
| 核心 runtime | [OpenClaw](https://openclaw.ai/)（agent runtime，dashboard 全靠它） |
| 靈感來源 | [tugcantopaloglu/openclaw-dashboard](https://github.com/tugcantopaloglu/openclaw-dashboard) |

## 專案概述

Mission Control Center（MCC）是台灣 **遠振資訊 (YJ-Software)** 個人開發者業餘維護的 **OpenClaw 任務控制面板**——用一個 Next.js 儀表板集中管理 AI Agent 團隊、任務排程、日報產出、備份、瀏覽器自動化與一整套 LINE 客服後台。★8 是小專案，但**功能密度與工程完整度遠超星數**（15 張 DB 表、15+ 頁面、60+ 元件、Playwright E2E 當 release gate）。

**核心設計前提：為遠端 VPS / headless Linux server 量身打造，不是 local desktop 工具。** 這個前提衍生出整套「**在瀏覽器裡操作整台伺服器**」的設計：終端機、Chrome、Docker、systemd 全部走 dashboard，不用 SSH 客戶端、不用 X11 forwarding。搭配 Tailscale 私網，從手機/平板都能像本機一樣操作一台 throwaway VPS 上的 agent 團隊。

> 這是本站少數的「**台灣自製 + OpenClaw 生態 + LINE 客服**」交集案例，與站上 OpenClaw 相關筆記（[awesome-openclaw-skills](awesome-openclaw-skills.md)、[openclaw-claude-proxy](openclaw-claude-proxy.md)、[claw-code](claw-code.md)）及 LINE 相關筆記（[line-chatbot-boilerplate](line-chatbot-boilerplate.md)、[linebot-multimodal-rag](linebot-multimodal-rag.md)）都能互連。

## 功能盤點

| 模組 | 重點 |
|------|------|
| **AI Agent 管理** | Agent 團隊（operators/developers/researchers 分類）、即時 Chat（串流 + 工具追蹤）、Sessions 歷史 + 成本分析、Live Feed 監控思考過程 |
| **晨報系統** | 主題管理 → `generate-prompts → 各主題執行 → finalize → podcast` 管線；URL 去重、edge-tts + ffmpeg 生 Podcast、自動同步為 OpenClaw cron（`mr-*`）、匯出 Obsidian |
| **Cron 排程** | 完整 CRUD；三種排程（cron / `at` / `every`）、兩種模式（`main` / `isolated` agent）、三種投遞（announce / webhook / none）、per-job timezone/timeout/model override |
| **備份系統** | 來源 + 目的地（FTP/local，S3/rsync coming）+ 排程 + 保留份數 + 還原；`X-Backup-Token` 外部呼叫 |
| **第二大腦** | NotebookLM 整合（wrap `nlm` CLI）+ Obsidian headless 安裝（Xvfb+Openbox+x11vnc）+ CouchDB LiveSync；兩個 capture skill（`link-capture`、`youtube-transcript`）自動抓取入 vault |
| **瀏覽器自動化** | Headless Chrome + noVNC 瀏覽器內遠端桌面 + CDP 9222 給腳本接；登入態/cookie 留在 server |
| **終端機 / Docker** | xterm.js + node-pty 多分頁、敏感資訊自動過濾；Docker container/image 管理 |
| **LINE 客服 Ops** | **功能最深的模組**（見下） |

### LINE 客服 Ops——最完整的模組

一整套 LINE Bot AI 客服後台，重點是「**operator 隨時能接手、看到 agent 內部過程、保證記憶累積**」：

- **operator 接手**：一鍵切「agent 回應中／我接手」，接手自動暫停 agent 30 分鐘（送訊息 reset 倒數）
- **接手 catch-up**：解除 pause 時自動掃 pause 期間對話，丟 LLM 萃取「值得長期記憶的客戶事實」寫入 mem0，不必手動整理
- **AI 自動建議 Quick Reply**：邊打字邊用 LLM 生客戶可能想點的回應（debounce 400ms）
- **Agent 時間軸 drawer**：列出該客戶所有 session 完整事件流，標記 `✅ 已送達 LINE` / `⚠️ 未送達`（偵測 openclaw 中途插話被吞的 race condition）
- **mem0 全自架堆疊**：Qdrant 向量庫 + Ollama `bge-m3` embedding + Gemini LLM，**免外部 API 依賴**；`customer-id-injector` plugin 自動把客戶 profile 注入 system prompt

## 技術棧

| 類別 | 技術 |
|------|------|
| 框架 | **Next.js 16 (App Router)** + 自訂 Server (`tsx server.ts`) |
| UI | Tailwind + Radix + shadcn/ui；Framer Motion、TipTap、FullCalendar、@dnd-kit |
| 狀態 | Zustand + TanStack Query |
| 即時 | WebSocket（Gateway 連線 + 瀏覽器即時更新） |
| DB | **SQLite via Drizzle ORM**（15 張表） |
| 多語系 | next-intl（zh-TW / zh-CN / en） |

即時架構是三層 WebSocket 中繼：

```
OpenClaw Gateway (ws://127.0.0.1:18789)
     ↕ WebSocket + Challenge-Response Auth
Mission Control Server (server.ts)   ← 事件中繼 + RPC 代理（10s timeout）
     ↕ WebSocket
Browser Client
```

## 工程亮點：release / openclaw 版本配對

這個小專案有一套**異常嚴謹的發版設計**，值得單獨記：

- **版本 = `<openclawVersion>-v<mccVersion>`**（例 `2026.6.1-v0.3.53`）。前綴不是裝飾，是**事實宣告**：「這個 MCC tarball 在 throwaway 環境上跑過完整 Playwright E2E，搭配的 openclaw 版本就是前綴」。
- **前綴 sticky / 後綴自由**：純 MCC 修補不重跑 E2E，前綴自動沿用上一筆；**換 openclaw 配對才必須重跑 E2E 全綠**——否則配對宣告就是說謊。
- **E2E 是 release gate**，不是 CI 裝飾。發版流程強制「E2E 通過才能 publish」。
- **部署 = tarball + symlink swap**：`current -> versions/vX.Y.Z` 原子切換，`upgrade.sh` 失敗自動回滾、比對 unit 內容有差才 `daemon-reload`。
- `/api/health` 同時暴露 `version`（組合字串顯示用）/ `mccVersion`（純 semver 比對用）/ `openclawVersion`——**升級比對統一用 `mccVersion`，避免 `split('.')` 被 openclaw 前綴拆爛**。

## 目前限制 / 注意事項

- **★8、solo 業餘維護、無 SLA**：不保證 issue/PR 回應。README 直說「想商用或客製，自己 fork 走比期待維護實際」。
- **僅 Ubuntu Linux**：macOS/Windows/其他發行版未驗證，systemd user unit、headless Chrome+VNC、apt 安裝流程會直接失敗。
- **0.x 可能 breaking**，升級前看 release notes。
- **高權限即高風險**：含終端機、Docker、瀏覽器自動化——**強烈建議只走 Tailscale 私網，別暴露公網**；一定要公網至少 強密碼 + fail2ban + reverse proxy + TLS。
- **wiki-person 記憶模式在 OpenClaw 4.29 無法運作**（plugin tool 不暴露給 agent），預設走 mem0，wiki-person UI 只是 scaffolding。

## 研究價值與啟示

### 關鍵洞察

1. **「server-resident、瀏覽器內操作整台伺服器」是被低估的 agent 運維範式**。多數 agent 工具假設你坐在 local 電腦前；MCC 反過來假設 agent 24/7 跑在 throwaway VPS 上，你只是偶爾用手機連進去看。終端機/Docker/Chrome 全塞進瀏覽器（xterm.js + noVNC + CDP），配 Tailscale 就是一個「隨身 agent 基地台」。這對「agent 要長跑、不能綁在你的筆電」的場景很對味。

2. **星數騙不了工程完整度**。8 stars 卻有 15 張 DB 表、E2E-as-release-gate、原子 symlink 部署、版本配對事實宣告——這是「**一人公司把內部運維工具開源**」的典型形態：不為 star，為自己的 VPS 車隊而寫。研究時看 star 之外的**工程慣性密度**更能判斷專案成熟度（對照本站對 [jezweb/claude-skills](jezweb-claude-skills.md) 文件漂移的觀察——這裡剛好相反，紀律極高）。

3. **LINE 客服 Ops 是「agent + human-in-the-loop」的完整落地樣本**。operator 接手自動暫停 agent、catch-up 自動萃取記憶、時間軸標記「已送達/未送達」偵測 race condition——這些是真正跑過生產客服才會長出來的細節。與站上 [linebot-multimodal-rag](linebot-multimodal-rag.md)、[line-chatbot-boilerplate](line-chatbot-boilerplate.md) 對照，MCC 補上了「**後台營運介面**」這一塊。

4. **openclaw 版本配對把「相容性」從 metadata 升級成 test-backed 契約**。多數專案的相容版本只是 README 上一句話；MCC 把它綁進「E2E 全綠才能改前綴」的流程，讓版本字串本身變成可驗證的宣稱。這個 pattern 可推廣到任何「wrap 快速更新的上游」的專案（對照 Vibe-Trading 的 provider 相容處理）。

5. **全自架記憶堆疊（Qdrant + Ollama + mem0）示範了「零外部 API 依賴」的客戶記憶**。對資料落地/隱私敏感的台灣中小企業客服場景，這個「embedding 用本地 bge-m3、向量庫自架」的組合是務實解。

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [awesome-openclaw-skills](awesome-openclaw-skills.md) / [openclaw-claude-proxy](openclaw-claude-proxy.md) / [claw-code](claw-code.md) | 同 OpenClaw 生態；MCC 是「OpenClaw 的營運儀表板」，補上 GUI 管理層 |
| [ai-usage-dashboard](ai-usage-dashboard.md) / [claude-hud](claude-hud.md) | 都是 agent 用量/狀態儀表板；MCC 範圍更廣（不只監控，還能操作終端/Docker/瀏覽器/客服） |
| [my-claude-devteam](my-claude-devteam.md) / [agent-orchestrator](agent-orchestrator.md) / [dispatch](dispatch.md) | 都是 agent 團隊管理；MCC 偏「單機 VPS 上的營運控制台」而非多機編排 |
| [line-chatbot-boilerplate](line-chatbot-boilerplate.md) / [linebot-multimodal-rag](linebot-multimodal-rag.md) | LINE bot 實作；MCC 補上「operator 接手 + mem0 長期記憶 + 時間軸」的後台 ops |
| [n8n-workflows](n8n-workflows.md) | 都做 automation；MCC 綁死 OpenClaw agent 生態，n8n 是通用 workflow |
