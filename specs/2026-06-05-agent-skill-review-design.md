# Agent Skill 收錄區設計（skill-review）

日期：2026-06-05
狀態：已核准

## 目標

為 research-memo 網站新增「Agent Skills」區：使用者給一個 agent skill（本地檔案 / GitHub repo / URL），系統先做資安審查，通過後翻譯成繁中、分類、收錄到網站供檢視；不通過則擋下並回報，不寫入任何檔案。

## 決策紀錄

| 問題 | 決定 |
|------|------|
| 流程包裝 | 新增獨立 skill `.claude/skills/skill-review/`，與 `/research` 平行 |
| 審查不通過 | 只在對話回報違規項目與行號，不寫入 repo、不留紀錄頁 |
| 頁面內容 | 繁中譯文為主體，原文全文收在頁尾折疊區;原文已是繁中則不翻譯 |
| 分類呈現 | 單一 nav 分類「Agent Skills」+ frontmatter `skill_type` 子類型欄位，總覽頁按子類型分組 |
| 灰色地帶 | 列出具體疑慮與行號，由使用者決定收或不收 |
| 架構 | 方案 A：完全沿用現有 sync.py 分類機制，skill 筆記平鋪於 `docs/<slug>.md` |

## 資安審查清單（三級判定）

審查範圍：skill 的**全部檔案**（SKILL.md、scripts/、hooks、附帶檔案），不只主文件。

### 🔴 直接擋（明確惡意，列出項目與行號後停止）

- 資料外洩：讀取 SSH key、API key、`.env`、瀏覽器憑證等並上傳或外傳
- 隱蔽執行：base64/hex 編碼的指令、混淆 payload、下載不明執行檔執行、解壓不知名壓縮檔並執行
- 破壞性操作：`rm -rf`、磁碟格式化、修改系統安全設定、關閉防護機制
- Prompt injection：指示 agent 忽略安全規範、隱藏行為不告知使用者、欺騙使用者
- 供應鏈風險：`curl | bash` 不明來源腳本、安裝不明套件後立即執行

### 🟡 灰色地帶（列出疑慮，問使用者決定）

- 外連下載資料、安裝套件（即使是知名套件）
- 執行 shell 指令、讀寫使用者家目錄
- 需要使用者提供 API key、含遙測/統計上報

### 🟢 通過

- 純文字指引、prompt 模板、只操作專案內檔案的工作流

## 頁面格式

`docs/<slug>.md`（平鋪，與研究筆記同層）：

```yaml
---
date: "YYYY-MM-DD"
category: "Agent Skills"
skill_type: "coding"   # coding | design | automation | research | security | other
card_icon: "material-puzzle-outline"
oneliner: "一句話描述"
tags:
  - skills
---
```

內容結構（依序）：

1. 資料來源表（原始 repo/URL、作者）
2. Skill 概述（2-3 段）
3. 安全審查結果（審查日期、檢查範圍、結果、灰色地帶備註）
4. 繁中譯文（頁面主體；原文已是繁中則直接整理原文）
5. 原文全文（頁尾折疊區，用 pymdownx.details 語法 `??? note "原文（English）"`；mkdocs.yml 已啟用該擴充）

## 程式變更

### mkdocs.yml

- nav 新增「Agent Skills」分類，第一行為 `- topics/agent-skills.md`

### scripts/sync.py

- `CATEGORY_SLUGS` 補 `"Agent Skills": "agent-skills"`
- `CATEGORY_ICONS` 補 `"Agent Skills": "material-puzzle-outline"`
- frontmatter 解析支援 `skill_type` 欄位
- topic 總覽頁生成：分類內筆記若有 `skill_type`，表格按子類型分組；子類型中文顯示名對照表（coding→Coding、design→設計、automation→自動化、research→研究、security→資安、other→其他）

### .claude/skills/skill-review/SKILL.md（新增）

仿 research skill 結構：

```
Step 0  檢查 docs/ 是否已收錄（已存在 → 問使用者）
Step 1  取得 skill 全部檔案（本地檔 / gh api / WebFetch）
Step 2  資安審查（三級清單）→ 擋 / 問 / 過
Step 3  翻譯並撰寫 docs/<slug>.md
Step 4  更新 mkdocs.yml nav、跑 scripts/sync.py
Step 5  gh auth 確認帳號 → commit → push
```

## 驗收標準

1. 拿一個已知安全的 skill 走完整流程：頁面生成正確、總覽頁按子類型分組、首頁/news/標籤索引自動更新
2. 人工構造一個含危險指令的測試樣本（如「下載並解壓不明壓縮檔後執行」）：審查擋下、對話列出違規行號、repo 無任何新檔案
3. `python3 scripts/sync.py` 對既有 191 篇筆記零回歸（無錯誤、無 diff 以外的變動）

## 不做的事（YAGNI）

- 不留「審查未通過清單」頁
- 不做 `docs/skills/` 子目錄與第二套生成邏輯
- 不做自動排程掃描、不做黑名單資料庫
