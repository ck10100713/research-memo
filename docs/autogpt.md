---
date: "2026-02-03"
category: "AI Agent 框架"
card_icon: "material-brain"
oneliner: "自主 AI Agent 先驅專案"
---
# AutoGPT 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/Significant-Gravitas/AutoGPT |
| 官方文件 | https://docs.agpt.co |
| Discord | https://discord.gg/autogpt |
| Twitter | https://twitter.com/Auto_GPT |

## 專案概述

AutoGPT 是一個強大的平台，允許使用者建立、部署和管理持續運行的 AI Agent，以自動化複雜的工作流程。

### 解決的問題

- **自主任務執行**：AI Agent 可以自主規劃和執行多步驟任務
- **持續運行**：Agent 可以被外部觸發並持續運行
- **視覺化建構**：提供低程式碼介面設計和配置 Agent
- **工作流程自動化**：將複雜商業流程轉化為智慧自動化

### 託管選項

- **自託管**：免費下載並自行部署
- **雲端託管**：等待清單中的 Beta 版本

## 技術架構

```
┌─────────────────────────────────────────────────────────────────┐
│                     AutoGPT 平台架構                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    AutoGPT Frontend                      │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │   │
│  │  │ Agent       │ │ Workflow    │ │ Deployment  │        │   │
│  │  │ Builder     │ │ Management  │ │ Controls    │        │   │
│  │  │ (低程式碼)   │ │ (工作流程)   │ │ (部署控制)  │        │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │   │
│  │  │ Ready-to-Use│ │ Agent       │ │ Monitoring  │        │   │
│  │  │ Agents      │ │ Interaction │ │ & Analytics │        │   │
│  │  │ (預設Agent) │ │ (Agent互動) │ │ (監控分析)  │        │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    AutoGPT Server                        │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │   │
│  │  │ Source Code │ │Infrastructure│ │ Marketplace │        │   │
│  │  │ (核心邏輯)  │ │ (基礎設施)   │ │ (市場)      │        │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    AutoGPT Classic                       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │   │
│  │  │  Forge  │ │Benchmark│ │   UI    │ │   CLI   │        │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 核心元件

1. **AutoGPT Frontend** - 使用者互動介面
   - Agent Builder：低程式碼設計介面
   - Workflow Management：工作流程管理
   - Deployment Controls：部署生命週期管理

2. **AutoGPT Server** - 運行 Agent 的核心引擎
   - 核心邏輯
   - 基礎設施
   - Marketplace

3. **AutoGPT Classic** - 經典版本工具
   - Forge：Agent 開發框架
   - Benchmark：效能測試工具
   - UI：使用者介面
   - CLI：命令列工具

## 系統需求

### 硬體需求
- CPU：建議 4+ 核心
- RAM：最低 8GB，建議 16GB
- 儲存：至少 10GB 可用空間

### 軟體需求
- 作業系統：Linux (Ubuntu 20.04+), macOS (10.15+), Windows 10/11 with WSL2
- Docker Engine (20.10.0+)
- Docker Compose (2.0.0+)
- Git (2.30+)
- Node.js (16.x+)
- npm (8.x+)

## 安裝與使用

### 快速安裝（macOS/Linux）

```bash
curl -fsSL https://setup.agpt.co/install.sh -o install.sh && bash install.sh
```

### 快速安裝（Windows PowerShell）

```powershell
powershell -c "iwr https://setup.agpt.co/install.bat -o install.bat; ./install.bat"
```

### 使用 CLI

```bash
$ ./run
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Commands:
  agent      Commands to create, start and stop agents
  benchmark  Commands to start the benchmark and list tests
  setup      Installs dependencies needed for your system
```

## 範例應用場景

### 1. 從熱門話題生成病毒式影片
- Agent 讀取 Reddit 上的話題
- 辨識熱門趨勢
- 自動建立短影片

### 2. 從影片中提取社群媒體素材
- 訂閱 YouTube 頻道
- 新影片上傳時自動轉錄
- 使用 AI 找出最具影響力的引言
- 自動發布到社群媒體

## 授權說明

- **autogpt_platform 資料夾**：Polyform Shield License
- **其他部分**：MIT License

## 研究重點

### 自主 Agent 架構

AutoGPT 的核心特色是「自主性」：
- Agent 可以自行規劃任務步驟
- 支援持續運行和外部觸發
- 透過區塊（Blocks）連接建構工作流程

### 任務規劃機制

- 使用視覺化區塊編輯器
- 每個區塊執行單一動作
- 支援條件分支和迴圈
- 可建立自訂區塊擴展功能

## 研究日期

2026-02-03
