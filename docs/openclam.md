# OpenClam 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [aaaddress1/OpenClam](https://github.com/aaaddress1/OpenClam) |
| 作者 GitHub | [aaaddress1 (Sheng-Hao Ma)](https://github.com/aaaddress1) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | **Sheng-Hao Ma（馬聖豪）** — 台灣資安研究員，TXOne Networks |
| Stars | 13（截至 2026-03-30） |
| Forks | 3 |
| 語言 | Python 100% |
| 授權 | MIT |
| Commits | 8（早期階段） |

OpenClam 是一套 **Windows 桌面浮動 AI 啟動器**，整合搜尋、翻譯、本地 AI 助手於一體。類似 macOS Spotlight 的 Windows 替代品，但內建 AI 對話和翻譯功能。

> **注意**：這是一個非常早期的個人專案（8 commits, 13 stars），但作者背景值得關注。

---

## 核心功能

### 1. 浮動搜尋列

- **啟動**：按 Alt 鍵呼出
- **搜尋範圍**：應用程式、檔案、資料夾、視窗、瀏覽器歷史、系統設定
- **目錄限縮**：輸入路徑如 `~\Desktop` + Tab，限縮搜尋範圍
- **Detail Pane**：右側面板顯示檔案 metadata、操作按鈕、預覽

### 2. 本地 AI 模式

- **啟動**：在搜尋列輸入 `?` 進入 AI 模式
- **模型**：qwen2.5:0.5b（首次啟動自動下載）
- **不需要 Ollama**：完全獨立運行
- **完全離線**：所有 AI 推理在本地執行

### 3. 翻譯面板

- **啟動**：選取文字後雙按 Ctrl+C
- **引擎**：Meta NLLB + CTranslate2
- **風格**：類似 DeepL 的翻譯彈出視窗
- **離線**：翻譯引擎也是本地運行

---

## 技術架構

| 組件 | 技術 |
|------|------|
| 語言 | Python 3.12 |
| AI 模型 | qwen2.5:0.5b（0.5B 參數，極輕量） |
| 翻譯 | Meta NLLB + CTranslate2 |
| 本地狀態 | `.openclam/` 目錄 |
| 平台 | Windows only |

### 安裝

```bash
winget install Python.Python.3.12
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install git+https://github.com/aaaddress1/OpenClam.git
openclam ui
```

模型在首次啟動時自動下載。

---

## 作者背景：Sheng-Hao Ma（馬聖豪）

這是理解 OpenClam 的重要脈絡——作者不是一般的 AI 開發者，而是**台灣知名資安研究員**：

| 項目 | 內容 |
|------|------|
| 公司 | **TXOne Networks**（工控資安公司，趨勢科技子公司） |
| 專長 | Windows Reversing、Exploit、x86、Malware |
| GitHub | 1.5K followers、278 repos |
| 成就 | Arctic Code Vault Contributor、Starstruck ×3 |
| 演講 | HITCON 2018（vtMal — Malware Sandbox Emulation） |

### 知名開源專案

| 專案 | Stars | 說明 |
|------|-------|------|
| RunPE-In-Memory | 941 | PE 載入器，在記憶體中執行執行檔 |
| PR0CESS | 617 | Windows process 工具集 |
| Skrull | 458 | Malware DRM，防止 AV 自動提交樣本 |
| Windows-APT-Warfare | 418 | 《Windows APT 戰爭》一書的技術實作 |
| wowInjector | 167 | 利用 WOW64 繞過防毒的 PoC |

> **意涵**：一個深耕 Windows 底層和資安的研究員開始做 AI 桌面工具，說明 AI 應用已擴散到資安社群。OpenClam 的 Windows 整合深度（搜尋系統設定、瀏覽器歷史等）可能得益於作者對 Windows 內部機制的深度理解。

---

## 與類似工具比較

| 面向 | OpenClam | Flow Launcher | Raycast | macOS Spotlight |
|------|----------|--------------|---------|-----------------|
| 平台 | Windows | Windows | macOS | macOS |
| AI 對話 | 內建（qwen2.5:0.5b） | 插件 | 內建 | 無 |
| 翻譯 | 內建（NLLB） | 插件 | 插件 | 無 |
| 離線 | 完全離線 | 部分 | 需網路 | 部分 |
| 開源 | MIT | MIT | 閉源 | 閉源 |
| AI 模型大小 | 0.5B（極輕量） | — | 雲端 | — |

---

## 研究價值與啟示

### 關鍵洞察

1. **0.5B 參數模型就夠用**：OpenClam 選擇 qwen2.5:0.5b（5 億參數）做桌面 AI 助手，而非 7B/13B 大模型。對於搜尋輔助和快速問答，極小模型已經足夠，且不需要 GPU。

2. **「不需要 Ollama」是差異化**：直接打包模型、首次啟動自動下載。降低了「安裝 Ollama → 下載模型 → 設定 API」的多步驟門檻。

3. **Meta NLLB + CTranslate2 是輕量翻譯的好選擇**：不需要雲端 API（如 DeepL/Google Translate），完全離線的 NLP 翻譯。CTranslate2 是高效推理引擎。

4. **資安研究員跨界 AI 的信號**：當像馬聖豪這樣的 Windows 底層專家開始做 AI 工具，代表 AI 開發工具鏈已經成熟到讓非 ML 專家也能快速產出。也暗示未來 AI 桌面工具可能有更深的系統整合。

5. **極早期但值得追蹤**：8 commits / 13 stars，但作者的背景和技術深度意味著如果他持續投入，這個專案可能發展出其他 launcher 難以複製的 Windows 深度整合。

### 限制

- **Windows only**：無 macOS/Linux 支援
- **極早期**：8 commits，功能和穩定性都在初期
- **AI 能力有限**：0.5B 模型只能做簡單問答，無法處理複雜任務
- **社群極小**：13 stars，幾乎沒有外部貢獻者
- **官網 openclam.tw 無法連線**
