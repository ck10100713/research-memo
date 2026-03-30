# claude-better 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [krzyzanowskim/claude-better](https://github.com/krzyzanowskim/claude-better) |
| 作者 | [Marcin Krzyzanowski](https://krzyzanowskim.com)（CryptoSwift 作者、前 PSPDFKit 工程師） |

## 專案概述

claude-better 自稱是 Claude CLI 的「compatibility-first reimplementation」，號稱達到 **73% 更快啟動、80% 更少記憶體、100% 相容性**。README 寫得極為專業——benchmark 方法論、conformance matrix、30-run batch 統計、p95 jitter 數據一應俱全。

**然而，這個 repo 完全沒有原始碼。**

整個 repo 只有兩個檔案：`LICENSE`（GPL-3.0）和 `README.md`。語言欄位是 `null`。README 最後一行寫著：

> The source code is available upon request, and provided for selected high profile customers only.

這是一個**精心製作的開發者諷刺作品**，用完美的企業級技術文案包裝一個不存在的產品。

| 指標 | 數值 |
|------|------|
| Stars | 369 |
| Forks | 40 |
| 程式碼行數 | **0** |
| 實際檔案 | `LICENSE` + `README.md` |
| 授權 | GPL-3.0（授權了...空氣） |
| 建立日期 | 2026-03-27 |

## 諷刺手法解構

### README 的「完美」技術文案

整份 README 的寫法完全符合高端技術產品的行銷慣例，每一段都精準模仿了某種常見的 tech marketing 套路：

| README 段落 | 模仿對象 | 諷刺點 |
|------------|----------|--------|
| "Why" — 列出 CLI 常見痛點 | 問題定義式開場 | 痛點都是真的，但解法不存在 |
| "Positioning" — 三個量化目標 | OKR 風格定位 | 精確到小數點的 % 數，來自不存在的 benchmark |
| "Headline Results" — 6 行表格 | 效能對比表 | `182ms → 49ms` 這種精確數字令人信服，但沒有可驗證的程式碼 |
| "Compatibility Study" — 1,200 invocations, 87 flag combos | 測試覆蓋率報告 | 連 `98.7% byte-for-byte output parity` 都寫了 |
| "Benchmark Methodology" — 30-run batches, p95 jitter | 學術級方法論 | Apple Silicon、32 GB RAM、APFS SSD 的測試環境 |
| "Why The Numbers Look Good" — 技術原理 | 白皮書式深度分析 | zero-copy streaming、precomputed registry 都是真技術名詞 |
| 最後一行：source code upon request | Enterprise sales 套路 | 最終揭曉的笑點 |

### 作者背景讓諷刺更有分量

Marcin Krzyzanowski 不是路人。他是：

- **CryptoSwift** 作者（Swift 生態最知名的加密庫之一）
- **前 PSPDFKit 工程師**（與 MCPorter 作者 Peter Steinberger 是同事）
- iOS/macOS 社群的資深開發者

由一個有真實技術背景的人寫出這個 repo，諷刺效果遠比匿名帳號更強——他完全有能力做出 README 描述的東西，但他選擇只寫 README。

## 目前限制 / 注意事項

- **沒有程式碼**：這不是一個可以使用的工具
- **可能被誤讀**：369 stars 中有多少人真的看了 repo 內容？
- **GPL-3.0 授權空 repo**：法律上無意義，但增添了諷刺的荒誕感

## 研究價值與啟示

### 關鍵洞察

1. **「README-Driven Hype」的完美解剖標本**：AI 工具生態充斥著誇張的 benchmark 和精美的 README，但使用者很少驗證背後是否有真正的實作。claude-better 用歸謬法暴露了這個問題——如果一份沒有程式碼的 README 能拿到 369 stars，那那些有程式碼但 benchmark 同樣無法獨立驗證的專案，其 star 數又能說明什麼？

2. **「Synthetic Benchmark」的可信度危機**：README 中反覆強調數據來自「synthetic benchmark results from the evaluation harness」。這正是許多 AI 工具（包括 LLM 本身）被詬病的問題——自己跑自己的 benchmark，永遠看起來很棒。claude-better 把這個諷刺推到極致：benchmark harness 也不存在。

3. **Enterprise 銷售話術的解構**：最後一行「available upon request, provided for selected high profile customers only」是整個 repo 的點睛之筆。這句話在真實的企業軟體世界中無處不在——它的功能是讓你無法驗證產品、但又給你一種「別人能拿到、你拿不到」的 FOMO。

4. **開發者社群的自我反省能力**：369 stars 和 40 forks 說明社群看懂了這個笑話，而且覺得它值得傳播。這表明開發者對 AI hype cycle 是有批判意識的——只是這種意識通常以 meme 和諷刺的形式表達，而不是認真的技術批評。

5. **「Same interface, less overhead」的真實需求**：諷刺之下，README 描述的痛點（CLI 啟動慢、記憶體膨脹、long session 效能下降）是真實的。如果有人真的做出 claude-better 描述的東西，它會是一個有價值的專案。這也是好諷刺的特徵——它嘲笑的不是需求本身，而是回應需求的方式。

### 與其他專案的關聯

- **MCPorter**（`docs/mcporter.md`）：作者 Peter Steinberger 是 Krzyzanowski 在 PSPDFKit 的前同事。MCPorter 是有真實程式碼的 MCP 工具（3.4K stars），兩人的專案風格形成鮮明對比——一個是認真造輪子，一個是諷刺造輪子文化
- **Everything Claude Code**（`docs/everything-claude-code.md`）：97K stars 的 Claude Code 擴展系統。claude-better 諷刺的正是這類專案的行銷語言——精確的 agent/skill/command 數字、impressive 的 benchmark、但使用者體驗是否真如數字所示？
- **Superpowers**（`docs/superpowers.md`）：106K stars 的 agentic skills 框架。同樣以精確數字行銷（「200+ skills」），claude-better 作為對照組提醒我們：數字本身不等於價值
