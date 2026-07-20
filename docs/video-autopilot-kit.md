---
date: "2026-07-20"
category: "AI 創作資源"
card_icon: "material-movie-open-play-outline"
oneliner: "填問卷變成你的系統 — YouTube/短影音自動化框架，ffmpeg pipeline + CapCut 自動化，零私人數據"
tags:
  - automation
  - video
  - claude-code
---

# video-autopilot-kit 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [github.com/Hao0321/video-autopilot-kit](https://github.com/Hao0321/video-autopilot-kit) |
| README（中/英） | repo 內 `README.md` / `README.en.md` |
| 設定問卷 | repo 內 `SETUP.md` |
| 版本相容矩陣 | repo 內 `TROUBLESHOOTING.md` |
| 知識庫 | repo 內 `knowledge/`（M1–M106） |

**GitHub 數據**：1.3k stars、228 forks、Python、MIT License、2026-06 建立（很新）

## 專案概述

video-autopilot-kit 是一套**「框架 + 方法論模板」**的 YouTube / 短影音自動化工具。它的核心賣點不是「給你一套現成設定」，而是給你**經實戰的骨架程式碼**（ffmpeg pipeline + CapCut 自動化），再用一份 `SETUP.md` 問卷**一區一區問你關於自己頻道的問題**，用你的答案把模板填成「你的系統」。

最關鍵的設計聲明：**repo 不含任何原作者的私人數據** —— voice、策略、社群數字全是空白模板（`templates/*.template.md`）。作者的立場是「一套創作系統最值錢的是**結構與方法論**，不是某個人的私人數字」，所以抄別人的設定沒用、甚至誤導。

適合場景：想系統化、可重現地量產教學長片或直式 Shorts 的個人創作者 / 小團隊。

## 兩條 first-class Path（核心架構）

專案刻意設計成**兩條同等地位的路徑**，不是主次關係：

| 路徑 | 是什麼 | 平台 | 依賴 |
|------|--------|------|------|
| ⭐ **Path 1 — Programmatic**（採用者預設） | 純程式 ffmpeg pipeline + Python，全程可重現 | Win / Mac / Linux | Python + ffmpeg，**不碰 CapCut** |
| **Path 2 — CapCut-assisted**（作者本人主用） | CapCut 草稿 JSON 直改 + AI 助手 Computer Use 操作 CapCut 視窗 | Windows-first、**版本敏感** | CapCut Desktop + Computer Use |

> **誠實聲明**：作者私人流程以 Path 2 為主（因為素材、模板、肌肉記憶都在 CapCut），但開源採用者**多數應從 Path 1 開始** —— 跨平台、無 CapCut 版本風險、全程可重現。需要 CapCut 花字/雲端模板時再上 Path 2。

### 模組地圖

```
src/
├── longform_maker/      # 教學長片：fx_lib premium 動態引擎
│                        #   (亞像素 Ken Burns / 雙層 bloom / light sweep
│                        #    / easing / 合成 SFX)、字級時間字幕、螢幕錄影清理
├── silent_vlog_maker/   # 純 ffmpeg pipeline：直式 Shorts（多色字幕 /
│                        #   BGM 高光起點 / 正規化）、靜音 vlog、素材清理
├── capcut_helpers/      # Path 1 的 QA gates（delivery_qa / broll_audit /
│                        #   caption_broll_matcher，純 ffmpeg 不需 CapCut）
│                        # + Path 2 的 CapCut 草稿 JSON 直改 & Computer Use 自動化
└── platform_compat.py   # 跨平台路徑 / CJK 字型自動探測（不 hardcode）

knowledge/   # M1–M106 影片製作避坑大全 + 演算法 + SOP + 剪輯心法
templates/   # voice / 品牌 / 演算法 / 社群 的空白填寫模板
examples/    # 自包含可跑 demo（ffmpeg 合成素材，不用真素材/CapCut）
SETUP.md     # ⭐ 從這開始 —— 回答問題讓系統變成你的
```

### 交付前機械化 QA（兩條 path 共用）

不論走哪條 path，成品都該過 `delivery_qa` 這關 —— 純 ffmpeg/Python 檢查：

- **頻閃 / 死空檔 / caption-sync / 全幀掃描**（M91–M95）
- **b-roll 占比稽核**（`broll_audit`）
- **字幕與 b-roll 對位**（`caption_broll_matcher`，b-roll 用內容命名就自動對位）

## 快速開始

```bash
# 60 秒看它真的會動（不用 CapCut、不用真素材）
python examples/01_vertical_short.py       # 合成素材 → 1080x1920 直式 Short
python examples/02_caption_broll_match.py  # 零設定字幕自動對位 b-roll
```

正式採用流程：

1. 讀 `SETUP.md` → 照問題把 `templates/*.template.md` 填成 `profiles/*.md`
   （或把整個 repo 丟給 Claude / ChatGPT，說「照 SETUP.md 問我問題，幫我生成 profiles/」）
2. `cp config.example.py config.py` → 填素材/匯出路徑
3. 選 Path 1（Python + ffmpeg）或 Path 2（額外裝 CapCut Desktop + Computer Use）
4. 用 `src/` 的工具開始產片

需求：Python 3.9+ 與 `ffmpeg`/`ffprobe`。

## 目前限制 / 注意事項

- **Path 2 版本敏感**：CapCut 草稿 JSON 直改對版本有相容矩陣，**剪映 CN 6.0+ 已加密不可直改**；動手前先讀 `TROUBLESHOOTING.md`，用 `detect_draft_format()` 驗明文
- **Computer Use GUI 自動化僅 Windows**：套雲端模板 / 匯出需 AI 助手的 Computer Use，**Mac 上沒有可用等效機制**（CapCut Mac 無 AppleScript dictionary）
- **CapCut 草稿自動化未在 Mac 實測**：路徑已支援（`CAPCUT_USER_DATA` env override），但自動化只在 Windows 親測
- **需要自備素材與判斷**：這是框架不是「一鍵生成」——腳本、選題、voice 仍要你自己填
- **很新的專案**：2026-06 才建立，API 與模組可能仍在變動

## 研究價值與啟示

### 關鍵洞察

1. **「空白模板 + 問卷」是可複製的開源方法論**——多數 creator 工具賣的是「某個成功者的設定」，抄了對你沒用還可能誤導。這個 kit 反其道而行：**只給結構，逼你用自己的數據填滿**。這種「框架式開源」（ship 骨架、留白讓使用者注入 domain 知識）比「ship 一套死參數」更誠實，也更難被時效淘汰。

2. **把 LLM 當 onboarding 引擎，而非生成引擎**——`SETUP.md` 明確建議「把整個 repo 丟給 Claude / ChatGPT，讓它照問卷問你、幫你生成 profiles/」。LLM 在這裡的角色不是「生成影片」，而是**把使用者腦中的隱性知識結構化成設定檔**。這是 agent 應用中被低估的一種用法：用對話把 tacit knowledge 轉成 config。

3. **Computer Use 落地在真實桌面軟體的樣本**——Path 2 用 Claude 的 Computer Use 實際操作 CapCut 視窗（套模板、匯出）。它誠實揭露了現實限制：**版本敏感、平台綁定（Windows-only）、GUI 自動化脆弱**。這是研究「AI 操作既有桌面 App」時很有價值的踩坑實錄，而非 demo。

4. **機械化 QA gate 是量產品質的關鍵**——`delivery_qa`（頻閃/死空檔/caption-sync/全幀掃描）把「交付品質」變成純 ffmpeg 可驗證的關卡，兩條 path 共用。這呼應了工程界的「品質內建於 pipeline」思維：量產內容要穩定，靠的不是人工檢查而是**自動化 gate**。

5. **「純程式 vs GUI 輔助」雙軌是務實的過渡設計**——作者承認自己主用 CapCut（Path 2），卻把跨平台可重現的 Path 1 設為採用者預設。這反映了創作自動化的現實張力：**GUI 工具有特效紅利但脆弱且綁平台，純程式可重現但要犧牲部分視覺花俏**。雙軌並存讓使用者按需求選擇，而非強推一種。

### 與其他專案的關聯

- **方法論對照**：與「賣現成 prompt/設定」的 creator 產品相反，走的是 [ai-agents-for-beginners](ai-agents-for-beginners.md) 這類「教你搭骨架」的路線，只是領域換成影音生產
- **Computer Use 角度**：Path 2 用 Claude Computer Use 操作 CapCut，可與研究 [page-agent](page-agent.md)、[better-agent-terminal](better-agent-terminal.md) 等「AI 操作既有介面」的專案對照——共同課題都是「GUI 自動化的脆弱性與版本相容」
- **LLM as onboarding**：用 LLM 把使用者隱性知識轉成 config 的模式，與 Claude/OpenAI Agent SDK 的 structured output 應用是同一思路的輕量版
