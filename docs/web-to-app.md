---
date: "2026-04-15"
category: "開發工具"
card_icon: "material-cellphone-link"
oneliner: "在手機上直接將任意網站/HTML/React 打包成 Android APK — 不需 Android Studio"
---

# WebToApp 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [shiahonb777/web-to-app](https://github.com/shiahonb777/web-to-app) |
| Telegram 群組 | [t.me/webtoapp777](https://t.me/webtoapp777) |

**作者：** shiahonb777

**專案狀態：** ⭐ 2,672 stars · Kotlin · Unlicense · 2025-11 創建 · 活躍開發中

## 專案概述

WebToApp 是一個原生 Android 應用，核心能力是**在手機上直接將任何網站 URL、HTML 檔案、或前端框架建置產出打包成獨立 APK**，完全不需要電腦或 Android Studio。

支援的輸入類型：
- **URL** — 任何網站直接包裝
- **媒體** — 圖片/影片打包成全螢幕 App
- **HTML** — React/Vue/Next.js/Nuxt/Svelte 等框架的 build 產出

## 技術棧

| 層級 | 技術 |
|------|------|
| 語言 | Kotlin 1.9+ |
| UI | Jetpack Compose + Material 3 |
| 架構 | MVVM + Repository |
| 瀏覽器 | WebView + GeckoView（Firefox 雙引擎） |
| 資料庫 | Room + DataStore |
| 加密 | AES-256-GCM + PBKDF2 |
| 簽名 | apksig（v1/v2/v3） |
| 原生層 | CMake C++17 / NDK |

## 核心功能

| 功能 | 說明 |
|------|------|
| 網站 → APK | 輸入 URL 即生成獨立 APK |
| HTML → APK | 支援 React/Vue/Next.js 等 build 產出 |
| 擴充模組 | 10 個內建 + 28 個範本，類 Tampermonkey 腳本注入 |
| APK 加固 | 防反編譯、Dex 加密、程式碼混淆、反除錯 |
| App 修改器 | 掃描已裝 App，改圖示/名稱，克隆安裝 |
| AI 輔助 | 自然語言開發模組、AI 圖示生成 |
| 安全隱私 | UA/指紋偽裝、Hosts 封鎖、隔離環境 |

### 內建擴充模組

影片下載器（通用/Bilibili/抖音/小紅書）、影片增強器（速度/子母畫面）、網頁分析器（元素檢查/網路監控）、深色模式、隱私保護（廣告封鎖/反追蹤）、內容增強（強制複製/翻譯/長截圖）、元素封鎖器。

## 有趣的觀察

專案的最多 commit 貢獻者是 **`claude`**（12 次），超過作者本人（2 次）——大量使用 AI 輔助開發。

## 目前限制 / 注意事項

- **僅支援 Android** — 無 iOS 版本
- **最低 Android 6.0（API 23）** — 較舊裝置才支援
- **雲端功能需付費** — Pro/Ultra 方案才有分析儀表板、雲端備份等
- **中國開發者生態** — QQ 群、Bilibili、小紅書整合為主
- **安全疑慮** — APK 加固和反編譯功能可能被用於惡意目的

## 研究價值與啟示

### 關鍵洞察

1. **「手機上打包 APK」是 no-code 的極端形式。** 把 Android 開發的門檻降到零——不需要電腦、不需要 IDE、不需要會寫程式。對非技術使用者（小商家、內容創作者）特別有吸引力。

2. **擴充模組系統是 WebView App 的差異化。** 單純的 URL → APK 包裝器很多，但內建腳本注入（影片下載、廣告封鎖、強制複製）讓生成的 App 比原始網頁更好用。

3. **APK 加固功能是雙刃劍。** 防反編譯和 Dex 加密對正規開發者保護智慧財產有用，但也可能被用來包裝惡意 App。Unlicense 授權意味著完全無使用限制。

### 與其他專案的關聯

- **vs tw-house-ops / Claude Ads：** 都是用 AI 輔助開發的應用。不同的是 tw-house-ops 運行在 Claude Code 之上，WebToApp 是用 Claude 協助開發但本身是獨立 App。
- **對行動開發的啟示：** 如果需要快速將 fluffy-core-internal-dashboard 包裝成行動 App 給非技術使用者，WebToApp 是一個零成本選項（雖然功能有限）。
