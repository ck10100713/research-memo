---
date: "2026-06-12"
category: "開發工具"
card_icon: "material-view-grid-outline"
oneliner: "用滑鼠拖拉就能建/管 LINE Rich Menu 的本機 GUI 工具（Angular + Express，npm 一鍵啟動）"
tags:
  - chatbot
  - design
---

# LINE Rich Menus Manager 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/kenakamu/line-richmenus-manager> |
| npm 套件 | `line-richmenus-manager`（`npm i -g` 後直接執行） |
| 作者 | Kenichiro Nakamura（中村憲一郎，微軟，日本） |
| LINE Rich Menu 官方文件 | <https://developers.line.me/en/docs/messaging-api/using-rich-menus/> |
| UI 元件庫 | [Ignite UI for Angular](https://www.infragistics.com/products/ignite-ui-angular)（INFRAGISTICS） |

> Repo 統計：⭐ 28、TypeScript、MIT License、topics: `line` `messaging-api` `richmenu`。最後更新 2025-10。提供英／日雙語 README。

## 專案概述

`line-richmenus-manager` 是一套**本機執行的圖形化工具**，專門用來管理 LINE bot 的 **Rich Menu**（聊天室下方那塊可點擊的圖文選單）。

問題背景：LINE 的 Rich Menu **沒有官方後台 GUI**。要建立一個 Rich Menu，開發者得手動呼叫 Messaging API——先用 JSON 定義每個可點區域的座標（x / y / width / height）與動作，再上傳一張底圖，最後把選單綁到使用者身上。座標全靠人工算、要反覆試錯，開發體驗很差。

這個工具把整套流程搬進瀏覽器：**上傳底圖後直接用滑鼠在圖上拖拉框選可點區域**，或用文字框做 pixel 級微調，省去手算座標與裸寫 API 呼叫。本質是一個架在 LINE Messaging API 之上的 **CRUD GUI**。

## 核心功能

| 功能 | 說明 |
|------|------|
| **List** | 列出該 bot 的所有 Rich Menu |
| **Find by user** | 查某個使用者目前綁定的 Rich Menu |
| **Detail / Link / Unlink** | 看選單細節、把選單綁定或解綁到特定 user |
| **Create** | 上傳底圖 → 拖拉框選可點區域 → 設定動作 → 建立 |
| **Delete** | 刪除 Rich Menu |
| **拖拉 + 數值雙模式** | 滑鼠拉框做粗調，文字框輸入 x/y/w/h 做 pixel 級精修 |

## 技術架構

```
┌─────────────────────────────┐
│  Browser (Chrome only)      │  Angular 2 + Ignite UI for Angular
│  拖拉框選 / 數值微調 UI       │
└──────────────┬──────────────┘
               │  proxy.conf.json 轉發
               ▼
┌─────────────────────────────┐
│  Express server (Node.js)   │  代理呼叫 LINE Messaging API
└──────────────┬──────────────┘
               ▼
        LINE Messaging API (Rich Menu endpoints)
```

- 前端：**Angular 2**，UI 元件用 INFRAGISTICS 的 **Ignite UI for Angular**
- 後端：**Express**，透過 `proxy.conf.json` 把前端請求代理到 LINE API（也避開瀏覽器 CORS）
- 啟動後開在 `localhost:3000`，**僅在 Chrome 測過**
- 開發除錯流程綁定 **VSCode**（Launch Node + Launch Chrome）與 Debugger for Chrome

## 快速開始

```bash
# 最簡單：從 npm 全域安裝後直接跑
npm install -g line-richmenus-manager
line-richmenus-manager                 # 開瀏覽器，服務跑在 :3000
line-richmenus-manager --port:3200     # 指定埠號

# macOS 可能需 sudo
sudo npm install -g line-richmenus-manager
sudo line-richmenus-manager
```

從原始碼跑（開發用）：

```bash
git clone https://github.com/kenakamu/line-richmenus-manager
npm install
ng serve --aot --progress=false --proxy-config proxy.conf.json
```

## 目前限制 / 注意事項

- **僅支援 Chrome**：作者明言只在 Chrome 測過，其他瀏覽器自負風險。
- **技術棧偏舊**：Angular 2（2016 年代）。對現代 Angular（v17+ standalone components）而言已是古早版本，從原始碼維護的門檻較高。
- **需自帶 Channel Access Token**：工具本身只是 API 前端，仍需 LINE bot 的 token 才能操作；token 在本機輸入、本機代理，使用前要確認執行環境可信。
- **依賴商用 UI 元件**：Ignite UI 為 INFRAGISTICS 商業產品，二次開發或商用需留意授權。
- **功能聚焦單一**：只做 Rich Menu，不涉及訊息推播、webhook、其他 bot 設定。
- **小眾、低活躍**：28 stars、更新緩慢，遇到問題多半得自己讀程式碼。

## 研究價值與啟示

### 關鍵洞察

1. **「給沒有官方後台的 API 補一個 GUI」是極具槓桿的工具切入點。** LINE Rich Menu 的痛點不在功能，而在「手算座標 + 裸寫 JSON」的開發體驗。這個工具不發明任何新能力，只是把既有 API 包成所見即所得的介面——**價值全在 DX（開發者體驗）**。任何「只有 API、沒有 dashboard」的服務，都存在同類型的工具機會。

2. **拖拉 + 數值雙輸入，是座標編輯類 UI 的黃金組合。** 滑鼠拉框快速但不精準、數值輸入精準但繁瑣，兩者並存讓使用者依情境切換。這個模式在 Figma、影像標註工具、地圖框選等場景反覆出現，是處理「空間座標輸入」的成熟解法。

3. **「本機 Express 代理 + 瀏覽器前端」是 API 工具的經典架構，且順手解掉兩個問題。** 一是 **CORS**（瀏覽器無法直接打 LINE API），二是 **token 不外洩**（憑證留在本機 server，不進公開雲端）。這個「local-first 代理」模式至今仍是開發者工具（如各種 API explorer、本機 dashboard）的主流選擇。

4. **npm 全域安裝 + 一行啟動，是 Node 生態「工具即指令」的 DX 範本。** `npm i -g` 後敲一個指令就開瀏覽器，把「安裝 → 設定 → 啟動」壓成兩步。這正是 CLI 工具降低上手門檻的標準做法，與本站收錄的多數 CLI 工具同一思路。

5. **技術棧會過時，但「補足官方缺的後台」這個需求不會。** Angular 2 已老，但工具解決的核心問題（缺 Rich Menu GUI）依然存在。這提醒：工具的長期價值取決於它對應的**需求是否持久**，而非實作技術是否時髦——必要時用現代框架重寫即可延續價值。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [LINE Chatbot Boilerplate](line-chatbot-boilerplate.md) | 同為 LINE bot 開發工具鏈：boilerplate 解決「程式骨架」，本工具解決「Rich Menu 視覺設定」，互補 |
| [LINE Bot Multimodal RAG (kkdai)](linebot-multimodal-rag.md) | 同屬 LINE 生態；前者做對話智能，本工具做選單介面，合起來是一個完整 bot 的兩端 |
| [WebToApp](web-to-app.md) | 同為「把某種能力包成可立即使用的 GUI/App」的工具思路，DX 導向相通 |
