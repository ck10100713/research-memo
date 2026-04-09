---
date: "2026-04-09"
category: "Coding Agent 工具"
card_icon: "material-chat-processing"
oneliner: "Rust 開源 ACP Harness — 在 Discord 操控 Kiro/Claude/Codex/Gemini Coding Agent"
---

# OpenAB — Open Agent Broker

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [openabdev/openab](https://github.com/openabdev/openab) |
| Helm Chart 文件 | [openabdev.github.io/openab](https://openabdev.github.io/openab/) |
| ACP 官方協定 | [agentclientprotocol.com](https://agentclientprotocol.com/) |
| ACP 開發者介紹 | [A Developer's Intro to ACP](https://www.calummurray.ca/blog/intro-to-acp) |
| 競品：OpenACP | [Open-ACP/OpenACP](https://github.com/Open-ACP/OpenACP) |
| 靈感來源：sample-acp-bridge | [aws-samples/sample-acp-bridge](https://github.com/aws-samples/sample-acp-bridge) |

## 專案概述

OpenAB（Open Agent Broker）是一個用 Rust 寫的輕量級 ACP harness，將 Discord 聊天介面橋接到任何 [Agent Client Protocol](https://github.com/agentclientprotocol/agent-client-protocol) 相容的 Coding CLI。使用者在 Discord 頻道中 @mention 機器人，OpenAB 自動建立 thread、spawn CLI 子程序、透過 stdio JSON-RPC 雙向通訊，並以 edit-streaming 即時更新回覆。

核心定位：**讓團隊成員在 Discord 中直接使用 Kiro CLI、Claude Code、Codex、Gemini 等 Coding Agent**，不需要每個人都安裝 CLI 或設定開發環境。特別適合部署在 Kubernetes 上作為團隊共享的 Agent 服務。

## 核心架構

```
┌──────────────┐  Gateway WS   ┌──────────────┐  ACP stdio    ┌──────────────┐
│   Discord    │◄─────────────►│   OpenAB     │──────────────►│  Coding CLI  │
│   使用者      │               │   (Rust)     │◄── JSON-RPC ──│  (ACP mode)  │
└──────────────┘               └──────────────┘               └──────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │ Session Pool │ ← 每個 Discord thread 一個 CLI process
                               │ max=10, TTL  │
                               └──────────────┘
```

### 原始碼結構

| 檔案 | 職責 |
|------|------|
| `src/main.rs` | 進入點：tokio + serenity + cleanup + shutdown |
| `src/config.rs` | TOML 設定 + `${ENV_VAR}` 展開 |
| `src/discord.rs` | Discord bot：@mention、thread 建立、edit-streaming |
| `src/format.rs` | 訊息切割（Discord 2000 字元限制） |
| `src/reactions.rs` | 狀態 emoji 控制器（debounce、stall 偵測） |
| `src/acp/protocol.rs` | JSON-RPC types + ACP event 分類 |
| `src/acp/connection.rs` | spawn CLI、stdio JSON-RPC 通訊 |
| `src/acp/pool.rs` | thread_id → AcpConnection map |

## 支援的 Agent 後端

| Agent Key | CLI | ACP Adapter | 認證方式 |
|-----------|-----|-------------|---------|
| `kiro`（預設） | Kiro CLI | 原生 `kiro-cli acp` | `kiro-cli login --use-device-flow` |
| `codex` | Codex | [@zed-industries/codex-acp](https://github.com/zed-industries/codex-acp) | `codex login --device-auth` |
| `claude` | Claude Code | [@agentclientprotocol/claude-agent-acp](https://github.com/agentclientprotocol/claude-agent-acp) | `claude setup-token` |
| `gemini` | Gemini CLI | 原生 `gemini --acp` | Google OAuth 或 `GEMINI_API_KEY` |

## 核心功能

| 功能 | 說明 |
|------|------|
| @mention 觸發 | 在允許的頻道中 @bot 啟動對話 |
| Thread 多輪對話 | 自動建立 thread，後續回覆不需 @mention |
| Edit-streaming | 每 1.5s 更新 Discord 訊息，即時顯示生成內容 |
| Emoji 狀態反應 | 👀→🤔→🔥/👨‍💻/⚡→👍 + 隨機表情，視覺化 Agent 狀態 |
| Session Pool | 每個 thread 一個 CLI process，自動生命週期管理 |
| 權限自動回覆 | ACP tool call 的 permission 請求自動處理 |
| Kubernetes-ready | Dockerfile + k8s manifests + Helm chart，PVC 持久化認證 |

## 快速開始

```bash
# 1. 設定
cp config.toml.example config.toml
# 編輯 bot_token 和 allowed_channels

# 2. 開發模式
export DISCORD_BOT_TOKEN="your-token"
cargo run

# 3. 生產模式
cargo build --release
./target/release/openab config.toml
```

**Helm 安裝（推薦）：**

```bash
helm repo add openab https://openabdev.github.io/openab
helm repo update

# 單一 Agent（Kiro CLI）
helm install openab openab/openab \
  --set agents.kiro.discord.botToken="$DISCORD_BOT_TOKEN" \
  --set-string 'agents.kiro.discord.allowedChannels[0]=YOUR_CHANNEL_ID'

# 多 Agent（Kiro + Claude 同時運行）
helm install openab openab/openab \
  --set agents.kiro.discord.botToken="$KIRO_BOT_TOKEN" \
  --set agents.claude.discord.botToken="$CLAUDE_BOT_TOKEN" \
  ...
```

## ACP 協定簡介

Agent Client Protocol（ACP）是由 Zed 編輯器團隊推動的標準化協定，定義 **編輯器/客戶端** 與 **Coding Agent** 之間的通訊方式：

```
ACP 協定定位
─────────────────────────────────────────
  MCP = Agent ↔ 工具/資料（Tool Protocol）
  ACP = Client ↔ Agent（Agent Protocol）
  兩者正交，可組合使用
─────────────────────────────────────────

通訊方式：JSON-RPC 2.0 over stdio（本地）/ HTTP（遠端，開發中）
Session 模型：Client spawn Agent 為子程序 → 建立 session → prompt → streaming response
```

OpenAB 的創新在於：**將 ACP 的 client 角色從「編輯器」替換為「Discord bot」**，使得 ACP Agent 可以在聊天平台上被使用。

## 與 OpenACP 的比較

| 比較項目 | OpenAB | OpenACP |
|----------|--------|---------|
| 語言 | Rust | Node.js |
| 聊天平台 | Discord only | Telegram + Discord + Slack |
| 支援 Agent 數 | 4（Kiro/Claude/Codex/Gemini） | 28+（含 Cursor、Cline、goose 等） |
| 部署方式 | Kubernetes / Helm | npm + daemon mode |
| 特色功能 | Emoji 狀態反應、edit-streaming | Monaco Editor、語音訊息、REST API |
| 專案成熟度 | 新專案（180 stars） | 較成熟（58 stars, 1,410 commits） |
| 設計哲學 | 輕量、單一用途、Rust 效能 | 功能全面、Plugin 系統 |

## 目前限制

| 限制 | 說明 |
|------|------|
| 僅支援 Discord | 不像 OpenACP 支援 Telegram/Slack |
| 無 License 檔案 | README 寫 MIT 但 repo 無 LICENSE 文件 |
| 新專案風險 | 2026-04-03 建立，僅一週歷史 |
| 單機 Session | Session pool 綁定單一 Pod，無跨 Pod 分散 |
| 認證需手動 | 首次需 `kubectl exec` 進 Pod 做 OAuth 登入 |
| 無多使用者隔離 | 所有頻道使用者共享同一個 Agent 身份 |

## 研究價值與啟示

### 關鍵洞察

1. **ACP 正在成為 Coding Agent 的「USB 介面」**：就像 LSP 統一了編輯器與語言伺服器的溝通，ACP 正在統一 Client 與 Coding Agent 的溝通。OpenAB 證明了 ACP 的 client 不一定是編輯器——任何能 spawn process 的程式都能成為 ACP client，包括 Discord bot、Telegram bot、甚至 CI/CD pipeline。

2. **Discord 作為 Coding Agent 介面的價值**：團隊中不是每個人都需要（或想要）在終端機裡跑 Coding Agent。Discord 提供了低門檻的存取方式——PM 可以叫 Agent 解釋程式碼、QA 可以叫 Agent 跑測試、設計師可以叫 Agent 調 CSS。這是 Agent 民主化的一步。

3. **Rust 用於 Agent Harness 的合理性**：Agent harness 需要處理 WebSocket（Discord Gateway）+ stdio（ACP）+ 高並發 session pool。Rust 的 tokio async runtime + 零成本抽象在這裡有實際優勢，特別是部署在 Kubernetes 上時，記憶體和 CPU 效率直接影響成本。

4. **Emoji 狀態反應是低成本但高價值的 UX 設計**：OpenAB 用 emoji reaction 即時呈現 Agent 狀態（思考中、呼叫工具中、寫程式碼中），讓使用者不用等到完整回覆就能知道 Agent 在做什麼。這個模式值得在其他 Agent 介面中借鏡。

5. **OpenAB vs OpenACP 反映兩種設計哲學**：OpenAB 選擇「做好一件事」（Rust、Discord only、輕量），OpenACP 選擇「做所有事」（Node.js、3 平台、28+ agent、Plugin 系統）。兩者都有市場，但 OpenAB 的 Helm chart + K8s 原生設計更適合企業團隊部署。

### 與其他專案的關聯

- **OpenClaw / OpenClaw Claude Proxy**：OpenAB 的 StatusReactionController 直接受 OpenClaw 啟發，同屬 ACP 生態系的不同切面
- **Agent Orchestrator / Dispatch**：OpenAB 是「聊天介面→Agent」的橋接，Dispatch 是「Agent→Agent」的協作——兩者可以組合使用
- **Claude Agent SDK**：OpenAB 使用 `claude-agent-acp` adapter 連接 Claude Code，底層依賴 Claude 的 ACP 實作
- **sample-acp-bridge（AWS）**：OpenAB 的直接靈感來源，ACP protocol + process pool 架構從此衍生
