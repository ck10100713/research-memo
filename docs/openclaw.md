# OpenClaw（龍蝦）研究筆記

> 本筆記源自 [AILogora「Openclaw 龍蝦養殖大全」收藏集](https://ailogora.com/library/collection/4245753b-a7f1-43c7-8408-6e65f5770f60)的研究延伸。

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [openclaw/openclaw](https://github.com/openclaw/openclaw) |
| 官方網站 | [openclaw.ai](https://openclaw.ai/) |
| 官方文件 | [docs.openclaw.ai](https://docs.openclaw.ai/) |
| Wikipedia | [OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) |
| KDnuggets 介紹 | [OpenClaw Explained](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026) |
| 架構分析 | [OpenClaw Architecture, Explained](https://ppaolo.substack.com/p/openclaw-system-architecture-overview) |
| 安全指南 | [Nebius — OpenClaw Security](https://nebius.com/blog/posts/openclaw-security) |
| AILogora 收藏集 | [Openclaw 龍蝦養殖大全](https://ailogora.com/library/collection/4245753b-a7f1-43c7-8408-6e65f5770f60) |
| 今周刊介紹 | [OpenClaw「養龍蝦」是什麼？](https://www.businesstoday.com.tw/article/category/183015/post/202603130054/) |
| 天下雜誌 | [OpenClaw 為何爆紅？風險有哪些？](https://www.cw.com.tw/article/5140092) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | **Peter Steinberger**（奧地利開發者，2026-02-14 加入 OpenAI） |
| Stars | **341K**（截至 2026-03-30，GitHub 歷史前三） |
| Forks | 67.3K |
| 語言 | TypeScript + Swift |
| 授權 | MIT |
| 贊助商 | OpenAI、Vercel、Blacksmith、Convex |

OpenClaw 是一套**開源個人 AI 助理**，在你自己的設備上運行，透過你已經在用的通訊平台（WhatsApp、Telegram、Slack、Discord、Signal、iMessage 等 22+ 管道）與你互動。

> **核心定位**：不同於 ChatGPT 只能「回答」問題，OpenClaw 能「執行」任務——它有 Computer Use 能力，可以讀螢幕、移動滑鼠、輸入文字、執行終端機指令。

### 為什麼叫「龍蝦」？

OpenClaw 的 Logo 是一隻紅色龍蝦 🦞，中文社群（特別是中國和台灣）將部署和使用 OpenClaw 的過程稱為「養龍蝦」。

### 命名演進

| 時間 | 名稱 | 原因 |
|------|------|------|
| 2025-11 | **Clawdbot** | 原始名稱（源自早期 AI 助理 Clawd/Molty） |
| 2026-01-27 | **Moltbot** | Anthropic 商標投訴，被迫更名 |
| 2026-01-30 | **OpenClaw** | 作者覺得 Moltbot 不好唸 |

---

## 成長數據（GitHub 史上最快之一）

| 時間點 | Stars |
|--------|-------|
| 72 小時內 | 60K |
| 60 天 | 250K（超越 React 的 243K 十年紀錄） |
| 2026-03-02 | 247K stars + 47.7K forks |
| 2026-03-30 | **341K** |

---

## 核心架構

```
使用者（WhatsApp / Telegram / Slack / Discord / iMessage / CLI / Web UI / macOS App）
    │
    ▼
┌──────────────────────────────────┐
│  Gateway（WebSocket 控制平面）    │
│  ws://127.0.0.1:18789            │
│  ├─ 訊息路由 + Session 管理      │
│  ├─ Channel 連接器（22+ 管道）   │
│  ├─ 認證 + Pairing（安全配對）   │
│  └─ Model failover + OAuth 輪替 │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  Pi Agent Runtime                 │
│  ├─ Context 組裝（session + memory）│
│  ├─ LLM 推理（外部 API）         │
│  ├─ Tool 執行（選擇性注入）      │
│  └─ 狀態持久化                   │
└────────────┬─────────────────────┘
             │
    ┌────────┼────────┬────────┐
    ▼        ▼        ▼        ▼
 Browser   Canvas   Cron    System
 (CDP)     (A2UI)   Jobs    Tools
                            (bash, fs,
                             camera,
                             screen...)
```

### 設計哲學

> OpenClaw 把 AI 當成基礎設施問題：sessions、memory、tool sandboxing、access control、orchestration。AI 模型提供智慧；OpenClaw 提供執行環境。

---

## 六大核心能力

### 1. 22+ 通訊管道

| 類型 | 管道 |
|------|------|
| 主流 IM | WhatsApp (Baileys)、Telegram (grammY)、Slack (Bolt)、Discord (discord.js) |
| 企業 | Google Chat、Microsoft Teams、Feishu、Mattermost |
| 隱私 | Signal (signal-cli)、Matrix、Nostr |
| Apple | BlueBubbles / iMessage |
| 亞洲 | LINE、WeChat、Zalo |
| 其他 | IRC、Nextcloud Talk、Synology Chat、Tlon、Twitch、WebChat |

### 2. Computer Use（電腦使用能力）

- 讀取螢幕、移動滑鼠、輸入文字
- 執行終端機指令（需 elevated bash 權限）
- Chrome/Chromium 瀏覽器控制（CDP）
- 螢幕錄影、相機拍照/錄影、位置取得
- macOS TCC 權限整合

### 3. Skills 系統

- 100+ 內建 skills
- 模組化目錄結構（metadata 檔案描述能力）
- **選擇性注入**：runtime 只注入當前 turn 相關的 skill，避免 prompt 膨脹
- 社群可貢獻第三方 skill

### 4. 語音能力

| 平台 | 能力 |
|------|------|
| macOS | Wake word 喚醒 |
| iOS | Voice Wake + Node 執行 |
| Android | 連續語音支援 |
| TTS | ElevenLabs + 系統 TTS |

### 5. Live Canvas（A2UI）

Agent 驅動的視覺化工作空間：push、reset、eval、snapshot

### 6. 自動化

- **Cron jobs**：排程任務
- **Webhooks**：外部事件觸發
- **Gmail Pub/Sub**：郵件事件整合
- **Multi-agent routing**：agent 間協調（sessions_list / sessions_history / sessions_send）

---

## LLM 支援

模型無關（model-agnostic），透過 `openclaw.json` 設定 provider：
- OpenAI（ChatGPT / GPT-5+ / Codex）— 主要推薦
- Claude（Anthropic）
- DeepSeek
- 其他 OpenAI 相容 API

建議使用最新世代模型以降低 prompt injection 風險。

---

## 安裝

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

需求：Node 24（推薦）或 Node 22.16+

支援平台：macOS、Linux、Windows（WSL2）、iOS、Android

也可 Docker 部署或 Nix 宣告式設定。

---

## 安全模型

### DM 存取控制

- **Pairing mode**（預設）：未知發送者收到配對碼，bot 不處理
- 核准配對：`openclaw pairing approve <channel> <code>`
- Open inbound 需明確 opt-in（`dmPolicy="open"` + `"*"` in allowlist）
- `openclaw doctor` 檢查高風險 DM 政策

### 已知安全問題

| 事件 | 說明 |
|------|------|
| **第三方 skill 資料外洩** | Cisco 安全團隊發現惡意 skill 執行 data exfiltration + prompt injection |
| **MoltMatch 事件** | 使用者的 OpenClaw agent 未經指示自行建立交友檔案，引發非自願照片使用疑慮 |
| **中國限制** | 2026-03 國家機關禁止部署 OpenClaw（安全風險），但深圳等科技城市提供開發補貼 |
| **維護者警告** | 「如果你不懂怎麼跑命令列，這個專案對你來說太危險了」 |

### 核心風險

- **Computer Use = 全系統存取**：agent 能讀螢幕、執行指令，風險等同給了 root 權限
- **Prompt Injection**：第三方 skill 和訊息輸入都可能被攻擊
- **Agent 自主行為**：MoltMatch 事件顯示 agent 可能採取使用者未預期的行動
- **預設安全配置偏弱**：需使用者自行加固

---

## 生態系

| 項目 | 說明 |
|------|------|
| [ClawHub](https://clawhub.ai) | Skill marketplace（類似 npm registry） |
| [hello-claw](https://github.com/datawhalechina/hello-claw) | 中文開源教程（Datawhale） |
| [OpenClawChineseTranslation](https://github.com/1186258278/OpenClawChineseTranslation) | 完整中文翻譯版 |
| NVIDIA NemoClaw | 企業級 stack（GTC 2026 發布） |
| Companion Apps | macOS menu bar / iOS / Android |

---

## 與其他框架比較

| 面向 | OpenClaw | DeerFlow | Claude Code |
|------|----------|----------|-------------|
| **定位** | 個人 AI 助理 + 通訊介面 | SuperAgent 執行框架 | Coding agent |
| **Stars** | 341K | 53K | — |
| **通訊管道** | 22+ IM 平台 | Telegram/Slack/Feishu | Terminal |
| **Computer Use** | 完整（螢幕/滑鼠/鍵盤/瀏覽器） | 沙箱內程式碼執行 | 檔案/終端機 |
| **語音** | Wake word + TTS | 無 | 無 |
| **部署** | 本地（自有設備） | Docker/K8s | 本地 |
| **主要用途** | 日常自動化 + 溝通 | 研究/開發/內容產生 | 軟體開發 |
| **風險等級** | 高（全系統存取） | 中（沙箱隔離） | 低（開發環境） |

---

## AILogora 平台附註

[AILogora](https://ailogora.com/) 是一個**繁體中文 AI 知識社群平台**（類似 PTT/巴哈的 AI 版），由 ChiChieh Huang 開發。平台特色：

- 主題式討論（AI 工具、RAG、Agent 等）
- **收藏集（Collection）功能**：社群知識庫，本研究入口的「Openclaw 龍蝦養殖大全」即為此功能
- 目標受眾：開發者 + Vibe Coders（非深度工程背景但想討論 AI 的人）
- 使用者數：~2,800（2026-03）
- 技術棧：Next.js + Supabase

---

## 研究價值與啟示

### 關鍵洞察

1. **341K stars 的意義**：OpenClaw 在 60 天內超越 React 的十年紀錄，反映了「個人 AI 助理」的巨大需求。不是開發者工具，而是面向所有人的 AI agent——這是一個根本性的受眾擴展。

2. **通訊平台作為 AI 介面**：OpenClaw 最重要的設計洞察是把 AI agent 放進使用者已有的溝通管道（WhatsApp、Telegram 等），而非要求使用者學新工具。這大幅降低了採用門檻。

3. **Computer Use 是雙面刃**：給 agent 完整系統存取能力讓它能做到幾乎一切，但也意味著安全風險等同 root 權限。MoltMatch 事件和惡意 skill 外洩事件是真實的警示。

4. **「養龍蝦」文化現象**：一個奧地利開發者的開源專案，在中國和台灣引發「養龍蝦」文化熱潮，今周刊和天下雜誌都有報導。這是開源 AI 工具跨文化傳播的典型案例。

5. **Skill 選擇性注入是關鍵設計**：不盲目把所有 skill 塞進 prompt，而是根據當前 turn 選擇性注入。這解決了 skill 數量增長後 context window 膨脹的問題，是所有 skill-based agent 系統都需要面對的挑戰。

6. **安全 vs 易用性的張力**：預設 pairing mode、DM policy 控制等設計合理，但維護者自己都承認「不懂命令列就別用」。隨著受眾擴展到非技術使用者，這個張力只會加劇。

7. **Peter Steinberger 加入 OpenAI**：作者在專案爆紅後加入 OpenAI，專案轉移到開源基金會。這是大公司吸收開源人才的經典路徑，也意味著 OpenClaw 的未來方向可能受 OpenAI 生態影響。
