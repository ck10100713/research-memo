---
date: "2026-04-14"
category: "開發工具"
card_icon: "material-cloud-sync"
oneliner: "去中心化 Serverless 雲端市場（Akash fork）+ Bosun AI Agent 協調器"
---

# VirtEngine 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [virtengine/virtengine](https://github.com/virtengine/virtengine) |
| Bosun AI Agent | [virtengine/bosun](https://github.com/virtengine/bosun) |
| 專利 | [AU2024203136B2](https://patents.google.com/patent/AU2024203136B2/) |
| 官網 | [virtengine.com](https://virtengine.com/) |
| 基礎：Akash Network | [akash.network](https://akash.network/) |

**專案狀態：** ⭐ 15 stars（VirtEngine）+ 256 stars（Bosun）· Go + JavaScript · Apache 2.0 · 2021 創建

## 專案概述

VirtEngine 是一個**去中心化的 Serverless 雲端計算市場**，連接需要算力的租戶（tenants）和擁有閒置算力的供應商（providers）。技術上是 [Akash Network](https://akash.network/) 的 fork，使用 Cosmos SDK + CometBFT（Tendermint 後繼）構建區塊鏈節點，透過加密代幣實現算力交易。

專案有兩個主要組成部分：

1. **VirtEngine Protocol** — 去中心化交易所 + 區塊鏈節點（Go 單一二進制）
2. **Bosun** — AI Agent 自主協調器，管理 Codex/Copilot/Claude 等 Coding Agent 的生命週期

## 核心架構

### VirtEngine Protocol

```
┌──────────────┐      ┌──────────────────────┐      ┌──────────────┐
│   Tenant     │─────>│   VirtEngine Node    │<─────│   Provider   │
│  (需要算力)   │      │  (CometBFT 區塊鏈)   │      │  (提供算力)   │
└──────────────┘      │                      │      └──────────────┘
                      │  • 去中心化交易所      │
                      │  • Proof-of-Identity  │
                      │  • 加密代幣結算        │
                      └──────────────────────┘
```

| 組件 | 技術 |
|------|------|
| 區塊鏈引擎 | CometBFT（Tendermint fork） |
| SDK | Cosmos SDK |
| 身份驗證 | VEID — 0-100 分身份評分系統 |
| ML 引擎 | TensorFlow（臉部辨識、生物特徵） |
| 工作排程 | SLURM + Kubernetes |
| 語言 | Go 1.21+ |

### 專利核心：VEID 身份系統

專利 AU2024203136B2 描述的核心創新是去中心化系統中的**身份驗證機制**（VEID）：

- 用 0-100 分量化使用者身份可信度（0=未知、100=完全驗證）
- 多重驗證方式：臉部辨識、生物特徵感測器、文件上傳、SSO、Email/SMS
- 資料加密傳輸和儲存，只有授權帳戶可存取

> ⚠️ **專利注意事項：** 雖然程式碼是 Apache 2.0，但專利授權僅限於此專案的貢獻範圍。在此專案之外重現專利方法可能需要另外授權。

### Bosun — AI Agent 協調器

Bosun 是 VirtEngine 生態中的 **AI Coding Agent 自主管理工具**，256 stars，比主專案更受關注：

```bash
npm install -g bosun
bosun --daemon
```

| 功能 | 說明 |
|------|------|
| Fleet 管理 | 監管多個 Coding Agent（Codex、Copilot、Claude） |
| Failover | Agent 失敗時自動切換 |
| Crash 分析 | 自動分析崩潰原因 |
| Auto-restart | 自動重啟失敗的 Agent |
| 通知 | Telegram / WhatsApp 即時通知 |

## 快速開始

### 安裝 VirtEngine

```bash
# Homebrew
brew tap virtengine/tap
brew install virtengine

# 或用安裝腳本
curl -sSfL https://raw.githubusercontent.com/virtengine/virtengine/main/install.sh | sh
```

### 從原始碼編譯

```bash
# 需要 Go 1.21+、gcc/clang（C 依賴：libusb/libhid）
make virtengine
# 二進制輸出至 .cache/bin
```

### 安裝 Bosun

```bash
npm install -g bosun
bosun --daemon
```

## 版本與分支策略

| 分支 | 用途 | 版本號 |
|------|------|--------|
| `main` | 新功能開發（不穩定） | 奇數 minor（v0.9.0） |
| `mainnet/main` | 穩定發行版 | 偶數 minor（v0.8.0） |

## 目前限制 / 注意事項

- **極小社群** — 主 repo 僅 15 stars，開發活躍度和長期維護存疑
- **專利風險** — Apache 2.0 授權但有專利限制，商用需謹慎評估 AU2024203136B2 的範圍
- **Akash fork** — README 明確標示衍生自 Akash Network，原創性有限
- **Windows 僅實驗性支援** — 主要支援 macOS/Linux
- **文件不足** — Quick Start Guide 被提及但在 repo 中不易找到
- **Bosun 與主專案分離** — 兩者 star 數差異大（256 vs 15），Bosun 可能比 VirtEngine 本身更有獨立價值

## 研究價值與啟示

### 關鍵洞察

1. **Bosun 比 VirtEngine 本身更有研究價值。** 256 stars vs 15 stars 的巨大落差說明社群真正需要的不是「另一個去中心化雲端」，而是 **AI Agent 的 fleet 管理工具**。Bosun 的 failover + crash 分析 + auto-restart 正好解決了 Coding Agent 規模化的運維痛點。

2. **VEID 身份評分系統是有趣的設計模式。** 用 0-100 分量化身份可信度，結合臉部辨識和生物特徵——這在去中心化場景中解決了「你怎麼知道對方是誰」的根本問題。雖然隱私爭議很大，但這種分級信任模型對任何需要身份驗證的 P2P 系統都有參考價值。

3. **專利 + 開源的混合策略值得警惕。** Apache 2.0 看似友善，但專利條款實際限縮了使用範圍。這種模式在開源社群中越來越常見（如 MongoDB 的 SSPL、Redis 的 dual license），理解專利授權範圍比只看 License 檔案更重要。

4. **Akash fork 的市場定位不明確。** Akash Network 本身已有成熟生態（8.7K stars），VirtEngine 的差異化主要是 Proof-of-Identity（VEID）和 Bosun。但 15 stars 說明市場對此差異化的認可度有限。

### 與其他專案的關聯

- **vs Multica：** 兩者都在解決「多 Agent 管理」問題。Multica 用看板 UI + Skill 複用，Bosun 用 daemon + failover + 通知。Multica 偏「專案管理」，Bosun 偏「運維監控」——互補的兩個面向。
- **vs Agent Orchestrator / OpenAB：** Bosun 的 fleet 管理（failover、crash 分析）補充了 OpenAB 缺少的高可用性能力。OpenAB 做 Discord → Agent 橋接，Bosun 做 Agent 的生命週期管理。
- **去中心化算力的趨勢：** VirtEngine/Akash 代表的「用區塊鏈做算力市場」模式，可能對 GPU 匱乏時代的 AI 訓練有實際價值——但目前仍是早期階段。
