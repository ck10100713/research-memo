# Reference 快速參考手冊 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/jaywcjlove/reference |
| 線上版 | https://jaywcjlove.github.io/reference |
| Docker | https://hub.docker.com/r/wcjiang/reference |
| 作者 | 小弟調調 (Wang Chujiang) |

## 專案概述

Reference 是一份專為中文開發者整理的技術棧速查清單，基於英文版 Reference 翻譯擴展而來，新增了更多實用內容。這個專案旨在提升查閱效率與使用體驗，涵蓋了程式語言、框架、工具、命令列等多個技術領域。

這個專案解決的問題是技術文件查閱效率低下的困境。透過結構化的速查表（Cheat Sheet）格式，開發者可以快速找到常用語法、命令和配置，而不需要翻閱冗長的官方文件。

適合場景：
- 需要快速查閱技術語法的開發者
- 學習新技術時需要速查表的學習者
- 想要建立自己的技術筆記系統的人
- 需要離線技術參考的開發環境

## 核心功能

1. **程式語言速查**：Bash、Python、Go、Rust、Java、JavaScript、TypeScript 等 30+ 語言
2. **前端技術**：React、Vue、HTML/CSS、Tailwind CSS、Next.js 等
3. **後端框架**：Express、Django、Flask、FastAPI、NestJS 等
4. **資料庫**：MongoDB、MySQL、PostgreSQL、Redis 等
5. **DevOps 工具**：Docker、Kubernetes、Nginx、CI/CD 等
6. **命令列工具**：Git、Vim、tmux、curl、awk、sed 等
7. **AI 工具**：ChatGPT、Claude Code 速查
8. **配置格式**：JSON、YAML、TOML、INI 等

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                    Reference 架構                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  docs/                  ← Markdown 速查表                    │
│  ├── bash.md           ← 各技術主題                          │
│  ├── python.md                                               │
│  ├── docker.md                                               │
│  ├── git.md                                                  │
│  └── ...                                                     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    分類架構                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ │
│  │ 程式語言   │  │ 前端技術   │  │ 後端框架   │  │ DevOps   │ │
│  │ ───────── │  │ ───────── │  │ ───────── │  │ ───────── │ │
│  │ Python    │  │ React     │  │ Django    │  │ Docker    │ │
│  │ Go        │  │ Vue       │  │ Flask     │  │ K8s       │ │
│  │ Rust      │  │ TypeScript│  │ Express   │  │ Nginx     │ │
│  │ Java      │  │ CSS       │  │ FastAPI   │  │ CI/CD     │ │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘ │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ │
│  │ 命令列    │  │ 配置格式   │  │ 資料庫    │  │ AI 工具   │ │
│  │ ───────── │  │ ───────── │  │ ───────── │  │ ───────── │ │
│  │ Git       │  │ JSON      │  │ MySQL     │  │ ChatGPT   │ │
│  │ Vim       │  │ YAML      │  │ MongoDB   │  │ Claude    │ │
│  │ tmux      │  │ TOML      │  │ Redis     │  │           │ │
│  │ curl      │  │ INI       │  │ PostgreSQL│  │           │ │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘ │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    部署方式                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • GitHub Pages（靜態網站）                              ││
│  │  • Docker 容器部署                                       ││
│  │  • 自架靜態伺服器                                        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 線上使用

直接訪問：https://jaywcjlove.github.io/reference

### Docker 部署

```bash
# 使用 Docker 執行
docker run --name reference \
  -p 9667:3000 \
  -d wcjiang/reference:latest
```

### 本地開發

```bash
# 克隆專案
git clone https://github.com/jaywcjlove/reference.git
cd reference

# 安裝依賴
npm install

# 開發模式
npm run dev

# 建構靜態網站
npm run build
```

### 貢獻內容

```bash
# 在 docs/ 目錄下新增或編輯 Markdown 檔案
# 遵循現有的格式規範

# 提交 PR 貢獻你的速查表
```

## 與其他工具的比較

| 特性 | Reference | DevDocs | Dash |
|------|-----------|---------|------|
| 中文支援 | ✅ 原生中文 | ⚠️ 有限 | ⚠️ 有限 |
| 開源 | ✅ | ✅ | ❌ (付費) |
| 離線使用 | ✅ | ✅ | ✅ |
| 速查表格式 | ✅ 精簡 | ❌ 完整文件 | ⚠️ 混合 |
| 自訂內容 | ✅ | ⚠️ | ⚠️ |
| 部署方式 | 靜態/Docker | 靜態 | 桌面App |

## 研究心得

Reference 是一個非常實用的開發者工具，特別是對於中文開發者社群。

**專案特色：**
1. **中文優先**：專門為中文開發者優化，避免英文文件的閱讀門檻
2. **速查格式**：精簡的 Cheat Sheet 格式，快速找到需要的資訊
3. **持續更新**：社群驅動，持續新增和更新內容
4. **多種部署**：支援線上訪問、Docker 部署和本地使用

**對開發者的價值：**
- 快速複習熟悉但偶爾忘記的語法
- 學習新技術時的快速入門參考
- 建立個人技術筆記系統的模板

**對 AI Agent 開發的參考價值：**
- 速查表格式可作為 Agent 知識庫的參考
- 文件組織方式可用於 Agent Skills 的結構設計
- Claude Code 速查表直接相關於 Agent 開發

**注意事項：**
- 部分內容標記為「建設中」，需要社群貢獻完善
- 速查表為簡化版，深入學習仍需官方文件

---
研究日期：2026-02-03
