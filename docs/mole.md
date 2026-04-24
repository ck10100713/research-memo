---
date: "2026-04-24"
category: "開發工具"
card_icon: "material-broom"
oneliner: "tw93 打造的單一 binary Mac 深度清理工具，一條 `mo` 命令包辦 CleanMyMac + AppCleaner + DaisyDisk + iStat Menus，7 個月從 0 衝到 48.9K stars、MIT 開源"
---

# Mole 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/tw93/Mole> |
| Releases | <https://github.com/tw93/Mole/releases> |
| Homebrew Formula | <https://formulae.brew.sh/formula/mole> |
| 作者 Twitter | [@HiTw93](https://twitter.com/HiTw93) |
| Telegram 社群 | <https://t.me/+GclQS9ZnxyI2ODQ1> |
| 教學影片（PAPAYA 電腦教室） | <https://www.youtube.com/watch?v=UEe9-w4CcQ0> |
| Medium 評測（Nur Sabilly） | [I Just Switched to Mole](https://nursabilly.medium.com/i-just-switched-to-mole-a-lightweight-cleaning-tool-for-my-mac-aea1d69ac773) |
| 配套終端機（同作者） | [tw93/Kaku](https://github.com/tw93/Kaku) |

## 專案概述

**Mole** 是 [tw93](https://github.com/tw93)（同為知名跨平台打包工具 [Pake](https://github.com/tw93/Pake) 的作者）在 2025-09-23 開源的 **macOS 系統深度清理與優化工具**，核心哲學是「**一個 shell 寫的 binary，取代一串付費 App**」。7 個月內衝到 **48,989 stars、1,509 forks、126 subscribers**，幾乎是 2026 年上半年 macOS 工具類最亮眼的開源專案。

它用單一命令 `mo` 涵蓋：

- **CleanMyMac**（深度快取/日誌/瀏覽器殘留清理）
- **AppCleaner**（卸載 App + 抓殘留）
- **DaisyDisk**（磁碟空間可視化）
- **iStat Menus**（即時系統監控）
- 外加 **專案 build artifact 清理**（`node_modules` / `target` / `.venv`）和 **安裝檔掃除**（`.dmg` / `.pkg`）

定位：**純命令列、純 shell、純開源、純本地執行**。不需要掛 agent、不需要登入、不蒐集資料、沒有訂閱制。對於討厭 GUI 清理工具一直彈 upgrade 視窗、或懶得付 CleanMyMac 年費的使用者，Mole 是幾乎無痛的替代品。

## 核心功能

### 指令矩陣

| 指令 | 動作 | 破壞性 |
|------|------|--------|
| `mo` | 互動式主選單 | — |
| `mo clean` | 深度清除快取、日誌、瀏覽器殘留、已卸 App 殘檔 | ⚠️ 高 |
| `mo uninstall` | 移除 App + launch agents / preferences / 隱藏檔 | ⚠️ 高 |
| `mo optimize` | 重建系統快取 / 重啟 dynamic pager / 刷 Spotlight | 中 |
| `mo analyze` | 視覺化磁碟瀏覽器（檔案進 Trash 而非直刪） | 低 |
| `mo status` | 即時 CPU / Memory / Disk / Network / 溫度 / 電池 dashboard | 無 |
| `mo purge` | 清除專案 build artifact（node_modules 等） | ⚠️ 高 |
| `mo installer` | 找出 Downloads / Homebrew cache 裡的舊 .dmg / .pkg | 中 |
| `mo touchid` | 配置 Touch ID 給 sudo 用 | — |
| `mo completion` | 設定 shell tab completion | — |
| `mo update` / `mo update --nightly` | 更新 Mole（含 main 分支 nightly） | — |
| `mo remove` | 把 Mole 自己從系統移除 | — |

### 安全設計哲學（比功能更值得看的部分）

| 機制 | 說明 |
|------|------|
| `--dry-run` | 所有破壞性指令都支援預覽模式，看會刪什麼再決定 |
| `--debug` | 配合 `--dry-run` 查看詳細判斷邏輯 |
| `--whitelist` | `clean` / `optimize` 可設保護清單，永久排除某些路徑 |
| 操作日誌 | 所有檔案操作寫到 `~/Library/Logs/mole/operations.log`（可用 `MO_NO_OPLOG=1` 停用） |
| Trash-first | `mo analyze` 透過 Finder 送垃圾桶，不是直接 `rm`，可反悔 |
| 保守刪除邊界 | 遇到不確定狀態，Mole 選擇**跳過**而非擴大刪除範圍 |
| `IN_USE` 保護 | 清理 Xcode CoreSimulator 時，跳過標記為 `IN_USE` 的 Volume |
| 7 天新專案保護 | `mo purge` 預設不選取 7 天內還動過的專案 |
| Local Network 警告 | macOS 15+ 偵測到已卸 App 仍有 Local Network 權限殘留會警告，但不自動重設（因需 Recovery Mode） |
| 安全文件 | 附 `SECURITY.md` + `SECURITY_AUDIT.md` 說明已知風險與回報管道 |

### Machine-Readable 輸出

`mo analyze` 和 `mo status` 都支援 `--json`，而且 `mo status` 會**偵測到被 pipe**時自動切 JSON：

```bash
mo status | jq '.health_score'   # 自動 JSON
mo analyze --json ~/Documents    # 顯式 JSON
```

這對想把 Mole 包進腳本 / Raycast / CI 的人很友善。

### 輸出樣板（mo status 為例）

```
Mole Status  Health ● 92  MacBook Pro · M4 Pro · 32GB · macOS 14.5

⚙ CPU                                    ▦ Memory
Total   ████████████░░░░░░░  45.2%       Used    ███████████░░░░░░░  58.4%
Load    0.82 / 1.05 / 1.23 (8 cores)     Total   14.2 / 24.0 GB

▤ Disk                                   ⚡ Power
Used    █████████████░░░░░░  67.2%       Level   ██████████████████  100%
Read    ▮▯▯▯▯  2.1 MB/s                  Temp    58°C · 1200 RPM

⇅ Network                                ▶ Processes
Down    ▁▁█▂▁▁▇▆▅▂  0.54 MB/s             Code       ▮▮▮▮▯  42.1%
```

Health score 0–100 根據 CPU / 記憶體 / 磁碟 / 溫度 / I/O 綜合算出，顏色分級。可設 CPU 閾值做 process alert（`--proc-cpu-threshold`）。

## 快速開始

```bash
# Homebrew（推薦）
brew install mole

# 或一鍵腳本
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash

# 常用流程：先 dry-run，再實際執行
mo clean --dry-run           # 先看會刪什麼
mo clean                     # 確認後再動手
mo purge --paths             # 配置自訂專案掃描路徑
mo analyze /Volumes          # 只掃外接硬碟

# 用 Raycast / Alfred 快速啟動
curl -fsSL https://raw.githubusercontent.com/tw93/Mole/main/scripts/setup-quick-launchers.sh | bash
```

**前置**：macOS。Windows 有實驗性分支（[windows branch](https://github.com/tw93/Mole/tree/windows)），但不是主線。推薦先裝 `fd`（`brew install fd`）加速 `mo purge` 掃描。

**自訂掃描路徑**：編輯 `~/.config/mole/purge_paths`：

```
~/Documents/MyProjects
~/Work/ClientA
```

## 目前限制 / 注意事項

- **純 macOS**：Windows 仍是實驗分支，不建議生產用
- **破壞性指令多**：`clean` / `uninstall` / `purge` / `installer` / `remove` 都會實際刪檔，強烈建議先 `--dry-run`
- **iTerm2 有相容問題**：作者明示建議用自家的 [Kaku](https://github.com/tw93/Kaku)、或 Alacritty / kitty / WezTerm / Ghostty / Warp
- **Local Network 權限殘留無法自動清**：macOS 15+ 的這個 bug Mole 只能警告，要自己進 Recovery Mode 重設
- **以 shell 為主**：雖然穩定但除錯起來比 Go / Rust 寫的 CLI 稍吃力
- **外接硬碟預設跳過**：`mo analyze` 預設不掃 `/Volumes`（加速冷啟動），要掃需顯式指定

## 研究價值與啟示

### 關鍵洞察

1. **「替代一組付費 App」是極強的開源定位**
   Mole 的首頁一句話就把對手列清楚：`CleanMyMac + AppCleaner + DaisyDisk + iStat Menus`。這 4 套 App 加起來正式版每年要 US$100+。把這個對比攤開來，使用者不用猜它能做什麼——「那些東西能做的，我都做，還開源」。這是非常乾淨的開源定位公式：**對標一組有名的付費產品、用「一個 binary」當反面敘事**。值得任何想做「X 替代品」的開源專案抄這套文案結構。

2. **Shell 能撐到 48K stars，證明語言選擇不是關鍵**
   Mole 主語言是 Shell（MacOS 原生、無需 runtime、發佈零負擔），但能維持高速迭代和安全性——靠的是**嚴謹的 flag 設計**（`--dry-run` / `--whitelist` / `--debug` / `--json`）、**操作日誌**、**`SECURITY.md` + `SECURITY_AUDIT.md` 雙文件**、以及**保守優先**的刪除邊界。反例：很多 Go / Rust 寫的「清理工具」刪錯檔案後就沒救。Mole 證明**工程紀律 > 語言選擇**。

3. **`--json` + 自動偵測 pipe** 是極聰明的 UX 細節
   `mo status | jq '.health_score'` 可以直接用——因為 Mole 偵測到被 pipe 時自動切 JSON。這個小細節讓 CLI 工具從「人類互動工具」升級成「自動化基石」。任何 CLI 都應該學這招：**TTY 時給人看、pipe 時給機器看，不用多一個 flag**。

4. **「自我清理」的元設計**
   `mo remove` 可以把 Mole 自己從系統上完整移除——這對一個「負責清理的工具」是必要的誠意。代表作者的心態是「如果你不喜歡我，我該能讓你一鍵走人」，這比「下載容易、解除安裝隱晦」的商業軟體高明一級。

5. **tw93 的「工具產品化」連環**
   tw93 之前做過 [Pake](https://github.com/tw93/Pake)（把網頁一鍵打包成桌面 App，> 38K stars）、[Kaku](https://github.com/tw93/Kaku)（Mac 終端機），Mole 是他第三個衝破 3 萬 stars 的獨立作品。這些工具都遵循**「解決一個具體痛點、單一 binary、華美的 README + Twitter 行銷、深度整合作者自己的其他工具」**的公式。觀察這個連環是理解「東亞獨立開發者爆款公式」的好樣本。

6. **7 個月衝 48K stars 背後的傳播機制**
   - README 第一張圖就是「Freed 95.5GB」——**具體數字比功能列表有說服力**
   - 每個子指令都附 ASCII 輸出範例——**你能預見使用畫面，下載動機大增**
   - 作者親自維護 Telegram 群、推文 thread——**人格化社群 > 純 GitHub Issues**
   - 有 YouTube 中文教學影片（PAPAYA 電腦教室）——**打進非英文圈子**

### 與其他研究筆記的關聯

| 主題 | 關聯性 |
|------|--------|
| [Scrapling](scrapling.md) / [Optuna](optuna.md) / [MCP Toolbox for Databases](mcp-toolbox.md) | 同屬「開發者日常工具」類，但 Mole 是第一個 shell 語言為主、系統維運導向的 |
| [gstack](gstack.md) | 同屬「把一組工具整合成單一 CLI」的哲學，gstack 專注於 agent / browser，Mole 專注於系統維運 |
| [VirtEngine](virtengine.md) / [WebToApp](web-to-app.md) | 同為 macOS 生態的單一 binary 工具，可對比產品設計取捨 |
| [Context Hub](context-hub.md) / [Everything Claude Code](everything-claude-code.md) | 同為「aggregator」定位，但 Mole 整合的是系統功能，其他整合的是 AI 功能 |

**一句話結論**：Mole 是「**如果 CleanMyMac 有開源版本**」的答案。對 macOS 使用者無腦推薦 `brew install mole && mo clean --dry-run`；對獨立開發者，它是**「小而強、單一 binary、工程紀律勝過語言選擇」的當代樣板**。

Sources:

- [tw93/Mole — GitHub](https://github.com/tw93/Mole)
- [Mole Releases](https://github.com/tw93/mole/releases)
- [mole — Homebrew Formulae](https://formulae.brew.sh/formula/mole)
- [I Just Switched to Mole — Nur Sabilly (Medium)](https://nursabilly.medium.com/i-just-switched-to-mole-a-lightweight-cleaning-tool-for-my-mac-aea1d69ac773)
