---
date: "2026-06-05"
category: "開發工具"
card_icon: "material-microsoft-windows"
oneliner: "微軟官方開源的 Windows 強化工具集：30+ 個生產力小工具，從 FancyZones 到 AI 剪貼簿"
tags:
  - desktop-app
  - automation
---

# Microsoft PowerToys 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/microsoft/PowerToys> |
| 官方文件 | <https://learn.microsoft.com/windows/powertoys/> |
| Command Palette 文件 | <https://learn.microsoft.com/en-us/windows/powertoys/command-palette/overview> |
| Advanced Paste（AI 剪貼簿） | <https://learn.microsoft.com/en-us/windows/powertoys/advanced-paste> |
| CmdPal 進入 Windows Run 對話框報導 | <https://www.xda-developers.com/microsoft-powertoys-command-palette-windows-11-run/> |

## 專案概述

Microsoft PowerToys 是微軟官方開源（MIT License）的 **Windows 生產力工具集**，在 GitHub 上有 **133k+ stars**，主要以 C# 開發、發布節奏約每月一版。「PowerToys」之名繼承自 Windows 95 時代的同名 power user 工具包；2019 年微軟以開源形式重啟這個品牌，由官方團隊與社群共同開發，至今已收錄 **30+ 個工具**。

它的定位是「Windows 缺的那些小功能」的官方補完計畫：視窗管理、批次改名、鍵盤重映射、取色器、OCR 文字擷取……每個工具都小而專注，統一裝在一個帶設定中心的程式裡。許多功能驗證成熟後會「畢業」進入 Windows 本體（如 Command Palette 的程式碼已成為 Windows 11 新版 Run 對話框的基礎），使 PowerToys 實質上扮演 **Windows shell 功能的公開孵化器**。

## 核心工具一覽（精選）

| 類別 | 工具 | 功能 |
|------|------|------|
| 視窗管理 | **FancyZones** | 自訂視窗吸附版面，遠超原生 Snap |
| | Always on Top / Crop And Lock / Workspaces | 視窗置頂、裁切鎖定、一鍵還原工作區佈局 |
| 啟動器 | **Command Palette**（CmdPal） | 新世代啟動器（Win+Alt+Space），可擴充外掛，取代舊的 PowerToys Run |
| 剪貼簿 | **Advanced Paste** | 貼上時即時轉格式（純文字/JSON/Markdown），可接 OpenAI API 做 AI 轉換與 OCR |
| 檔案 | PowerRename / File Locksmith / Peek / New+ | regex 批次改名、查誰鎖住檔案、空白鍵預覽、自訂新增檔案範本 |
| 輸入 | Keyboard Manager / Quick Accent / Mouse Without Borders | 鍵位重映射、重音字元、一套鍵鼠跨多台電腦 |
| 開發者 | Hosts File Editor / Environment Variables / Registry Preview | GUI 編輯 hosts、環境變數、registry 預覽 |
| 螢幕 | Text Extractor（OCR）/ Color Picker / Screen Ruler / ZoomIt | 截圖取字、取色、量測像素、簡報縮放標註 |
| 系統 | Awake / Light Switch / PowerDisplay | 防休眠、自動深淺色切換、顯示器控制 |

## 快速開始

```powershell
# WinGet（預設 user scope）
winget install Microsoft.PowerToys -s winget

# 機器層級安裝
winget install --scope machine Microsoft.PowerToys -s winget
```

也可從 [GitHub Releases](https://github.com/microsoft/PowerToys/releases) 下載 .exe（多數裝置選 x64 per-user）、Microsoft Store，或社群通道（Chocolatey、Scoop）。

## 目前限制 / 注意事項

- **僅支援 Windows 10/11**，無 macOS/Linux 版本
- 預設收集基本診斷遙測（telemetry），隱私敏感環境需留意
- Open issues 高達 7,000+：工具數量多、組合複雜，特定工具（如 Keyboard Manager 在部分遊戲/遠端桌面情境）有相容性邊角問題
- PowerToys Run 與 Command Palette 過渡期並存，外掛生態需逐步遷移到 CmdPal 擴充架構
- Advanced Paste 的 AI 功能需自備 OpenAI API key，按用量計費

## 研究價值與啟示

### 關鍵洞察

1. **「官方孵化器」是大平台演進的聰明模式**：PowerToys 讓微軟在不動 Windows 本體的前提下快速實驗 shell 功能，成熟後再合併（CmdPal → Win11 Run 對話框、之前的 Snap 改進亦受 FancyZones 影響）。這與瀏覽器的 flags/extension 先行、語言的 PEP/RFC 流程同構——**用低風險邊緣實驗餵養高風險核心**。
2. **30+ 工具共用一個外殼的架構值得借鏡**：統一的設定中心、更新通道與啟用開關，讓每個小工具的維護成本攤薄。對照 Claude Code 的 plugin/skill 生態：單一 harness + 多個小能力的組合，比 30 個獨立 app 的總和更有黏性。
3. **AI 功能以「升級既有動作」的方式切入最自然**：Advanced Paste 不是另開一個 AI 視窗，而是把 AI 藏進「貼上」這個既有動作裡（貼上時順手轉格式/摘要/OCR）。這是 AI 功能設計的好範式：**嵌入工作流，而非新增工作流**。
4. **開源作為品牌復興手段**：PowerToys 品牌沉寂 20 年後以 MIT 開源重生，社群貢獻（如 Mouse Without Borders、ZoomIt 皆來自既有工具的收編）讓它成為微軟對開發者社群示好的旗艦案例之一。

### 與其他專案的關聯

- [Mole](mole.md)：同屬「系統層生產力工具」，Mole 聚焦 macOS 清理，PowerToys 聚焦 Windows 強化，可對照兩平台工具生態
- [Awesome Free Apps](awesome-free-apps.md)：PowerToys 是該清單型資源中常見的 Windows 必裝項目
- [usage (aqua5230 menu bar tracker)](aqua-usage-menubar.md)：同為「小而專注的桌面常駐工具」設計哲學
