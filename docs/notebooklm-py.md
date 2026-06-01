---
date: "2026-05-25"
category: "AI 應用"
card_icon: "material-notebook-multiple"
oneliner: "teng-lin 非官方 NotebookLM Python API + agentic skill，15k stars/4.5 個月，CLI/Python/Claude Code/Codex/OpenClaw 三入口，能解鎖 web UI 沒有的批次下載/PPTX/JSON 心智圖等隱藏能力"
tags:
  - rag
  - skills
---

# notebooklm-py 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/teng-lin/notebooklm-py> |
| PyPI 套件 | <https://pypi.org/project/notebooklm-py/> |
| SKILL.md | <https://github.com/teng-lin/notebooklm-py/blob/main/SKILL.md> |
| AGENTS.md（Codex 引導） | <https://github.com/teng-lin/notebooklm-py/blob/main/AGENTS.md> |
| Trendshift 趨勢 | <https://trendshift.io/repositories/19116> |
| Asciinema demo | <https://asciinema.org/a/767284> |

## 專案概述

`notebooklm-py` 是 **非官方** 的 Google NotebookLM Python SDK，作者 [teng-lin](https://github.com/teng-lin) 在 **2026-01-07** 開源，到 2026-05 已累積 **15,016 stars、2,063 forks**（4.5 個月內），是過去幾個月最快速躥升的 AI 工具 wrapper 之一。

它解決的問題是：**NotebookLM 沒有官方 API**。Google 的 NotebookLM 內部用了一套未公開的 RPC endpoint，這個專案逆向出協定，再包成 Python 函式庫 + CLI + Agent Skill 三種介面。

定位特殊：

- **不是另一個 RAG 工具**——它包的是 NotebookLM 本身的 source 管理 / chat / 內容生成能力。
- **解鎖 web UI 看不到的功能**——批次下載、PPTX 投影片、心智圖 JSON、quiz/flashcard 結構化匯出等都是 UI 不提供的。
- **同時鎖定三類使用者**：寫 Python 的開發者、寫 shell script 的人、用 Claude Code/Codex/OpenClaw 的 AI agent 使用者。

> ⚠️ **使用風險**：完全依賴 undocumented Google API，Google 隨時可以改 endpoint 讓它失效。作者明確標註「適合原型、研究、個人專案」，不建議用於 production。

## 三種使用方式

| 介面 | 適合場景 |
|------|---------|
| **Python API** | 應用整合、async pipeline、客製化流程 |
| **CLI** | shell script、快速任務、CI/CD 自動化 |
| **Agent Integration** | Claude Code / Codex / OpenClaw / 任何 LLM agent，用自然語言下指令 |

## NotebookLM 全功能覆蓋

### 核心操作

| 類別 | 能力 |
|------|------|
| **Notebooks** | 建立、列出、改名、刪除 |
| **Sources** | URL、YouTube、檔案（PDF、txt、Markdown、Word、EPUB、音訊、影片、圖片）、Google Drive、貼上文字；refresh、取得 guide/fulltext |
| **Chat** | 問答、對話歷史、自訂 persona |
| **Research** | Web/Drive research agent（fast/deep 兩種模式），自動匯入結果 |
| **Sharing** | 公開/私人連結、user 權限（viewer/editor）、view level |

### 內容生成（9 種 artifact）

| 類型 | 選項 | 下載格式 |
|------|------|---------|
| **Audio Overview** | 4 種格式（deep-dive、brief、critique、debate）、3 種長度、50+ 語言 | MP3/MP4 |
| **Video Overview** | 3 種格式、9 種視覺風格、`cinematic-video` 專屬 CLI alias | MP4 |
| **Slide Deck** | detailed/presenter 兩種，可改個別 slide | PDF / **PPTX** |
| **Infographic** | 3 種方向、3 種詳細度 | PNG |
| **Quiz** | 數量、難度可調 | JSON / Markdown / HTML |
| **Flashcards** | 數量、難度可調 | JSON / Markdown / HTML |
| **Report** | briefing doc、study guide、blog post、custom prompt | Markdown |
| **Data Table** | 用自然語言描述結構 | CSV |
| **Mind Map** | 階層視覺化 | **JSON** |

### Web UI 沒有的隱藏能力

| 功能 | Web UI | API/CLI |
|------|--------|---------|
| 批次下載所有 artifact | ❌ | ✅ |
| Quiz/Flashcard 匯出 JSON/MD/HTML | ❌（只給互動式） | ✅ |
| Mind map JSON 匯出 | ❌ | ✅ |
| Data table CSV 匯出 | ❌ | ✅ |
| Slide deck 匯出 **PPTX** | ❌（只給 PDF） | ✅ |
| 個別 slide 用自然語言改稿 | ❌ | ✅ |
| Report 模板附加自訂指令 | ❌ | ✅ |
| 把 chat 答案存成 notebook note | ❌ | ✅ |
| Source 取得 fulltext | ❌ | ✅ |
| 程式化 sharing 權限 | ❌ | ✅ |
| 多 Google 帳號 profile 切換 | ❌ | ✅ |
| 從現有瀏覽器 cookie 匯入登入態 | ❌ | ✅ |

## 快速開始

### 安裝

```bash
# CLI 使用者 + AI agent（含 Playwright 瀏覽器自動化）
pip install "notebooklm-py[browser]"
playwright install chromium      # ~170MB，沒有進度條，等 30-90 秒
notebooklm login                  # 開瀏覽器登入 Google
notebooklm auth check --test --json   # 驗證：應該看到 "status": "ok"

# 純函式庫（embedded 到自己 App，不裝 Playwright/Chromium）
pip install notebooklm-py         # ~10MB；需自備 storage_state.json
```

### CLI 範例（完整工作流）

```bash
# 1. 登入（也可用 Edge 給 SSO 機關用、或從現有瀏覽器借 cookie）
notebooklm login
notebooklm login --browser msedge
notebooklm login --browser-cookies chrome
notebooklm login --browser-cookies 'chrome::Profile 1'

# 2. 建 notebook + 加來源
notebooklm create "My Research"
notebooklm use <notebook_id>
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add "./paper.pdf"

# 3. 問問題
notebooklm ask "What are the key themes?"
notebooklm ask --prompt-file ./long_question.txt

# 4. 生成 artifact（--wait 等到完成）
notebooklm generate audio "make it engaging" --wait
notebooklm generate video --style whiteboard --wait
notebooklm generate cinematic-video "documentary-style summary" --wait
notebooklm generate quiz --difficulty hard
notebooklm generate flashcards --quantity more
notebooklm generate slide-deck
notebooklm generate infographic --orientation portrait
notebooklm generate mind-map
notebooklm generate data-table "compare key concepts"

# 5. 下載
notebooklm download audio        ./podcast.mp3
notebooklm download video        ./overview.mp4
notebooklm download cinematic-video ./documentary.mp4
notebooklm download quiz         --format markdown ./quiz.md
notebooklm download flashcards   --format json    ./cards.json
notebooklm download slide-deck   ./slides.pdf
notebooklm download infographic  ./infographic.png
notebooklm download mind-map     ./mindmap.json
notebooklm download data-table   ./data.csv
```

### Python API 範例

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        # 建 notebook 加來源
        nb = await client.notebooks.create("Research")
        await client.sources.add_url(nb.id, "https://example.com", wait=True)

        # 問答
        result = await client.chat.ask(nb.id, "Summarize this")
        print(result.answer)

        # 生 podcast
        status = await client.artifacts.generate_audio(nb.id, instructions="make it fun")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.mp3")

        # 生 quiz 並匯出 JSON
        status = await client.artifacts.generate_quiz(nb.id)
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_quiz(nb.id, "quiz.json", output_format="json")

        # 生心智圖匯出 JSON
        await client.artifacts.generate_mind_map(nb.id)
        await client.artifacts.download_mind_map(nb.id, "mindmap.json")

asyncio.run(main())
```

### Agent Skill 安裝

```bash
# 方案 1：CLI 內建安裝
notebooklm skill install
# → 安裝到 ~/.claude/skills/notebooklm 與 ~/.agents/skills/notebooklm

# 方案 2：npx skills 生態系
npx skills add teng-lin/notebooklm-py
```

實際運用：在 Claude Code 中輸入「幫我把這幾個 PDF 變成 podcast 跟簡報」，agent 會自動：

1. 建 notebook
2. 上傳 PDF 為 source
3. `generate audio` + `generate slide-deck`
4. `wait_for_completion` 輪詢
5. 下載到本機指定路徑

## 架構特色

從 repo 根目錄結構看得出工程品質：

```
├── SKILL.md             # 給 AI agent 的 skill 規格
├── AGENTS.md            # 給 Codex 的 repo-level 指引
├── CLAUDE.md            # 給 Claude Code 的 repo-level 指引
├── src/                 # 主程式
├── tests/               # 測試
├── examples/            # 範例
├── docs/                # 完整文件
│   ├── installation.md (六種 persona 安裝指南)
│   ├── cli-reference.md
│   ├── python-api.md
│   ├── architecture.md
│   ├── rpc-development.md  # 協定逆向開發指南
│   ├── rpc-reference.md    # payload 結構
│   └── stability.md
├── pyproject.toml
└── uv.lock              # uv 依賴管理
```

幾個亮點：

- **同時放 `SKILL.md` + `AGENTS.md` + `CLAUDE.md`**：作者把 Claude Code 與 Codex 視為一等公民。
- **公開 RPC 開發文件**：`docs/rpc-development.md` + `docs/rpc-reference.md` 告訴貢獻者怎麼用 Playwright 抓 Google 內部 endpoint、怎麼解 payload。
- **跨平台、跨 Python 版本**：macOS / Linux / Windows + Python 3.10-3.14 全測。
- **`uv.lock`**：用 [uv](https://github.com/astral-sh/uv) 做依賴管理，Modern Python 標準配備。

## 目前限制

- **依賴 undocumented Google API**：endpoint 可能無預警改變或被風控。
- **可能被限速 / 封 IP**：高頻自動化使用者要自己處理 rate limit。
- **需要 storage_state.json**：作為純函式庫使用時必須先以 Playwright 模式取得登入 cookie。
- **不適合 production**：作者明確列為「prototype / research / 個人專案用」。
- **Google 帳號風險**：濫用可能導致個人 Google 帳號異常，建議用次要帳號。

## 研究價值與啟示

### 關鍵洞察

1. **「給 AI agent 用的 API」是新興市場區隔**
   傳統 wrapper（OAuth 帳密 + REST）目標客群是「寫 App 的工程師」；`notebooklm-py` 額外把 SKILL.md / AGENTS.md / CLAUDE.md 設計成一等公民，目標客群擴大到「Claude Code 使用者」「Codex 使用者」「OpenClaw 使用者」。**同樣的 SDK，三個入口三個市場**，是 2026 年 AI 工具 packaging 的新標準範式。

2. **「web UI 沒給的功能」才是真正的賣點**
   Quiz JSON、PPTX、心智圖 JSON、批次下載——這些 NotebookLM 官方刻意藏起來、留給未來收費的功能，反而成了非官方 SDK 的差異化武器。這暗示 **官方產品的功能斷捨離 = 第三方 SDK 的市場機會**。

3. **逆向 SaaS 的工程文件可以公開**
   `docs/rpc-development.md` 完整公開「怎麼抓 Google 的 RPC」「怎麼解 payload 結構」。這在以前的「灰色地帶」專案會被視為敏感資訊，現在反而成為吸引貢獻者的核心競爭力。Google 顯然容忍這種程度的逆向（畢竟還在用人家 NotebookLM 的算力）。

4. **15k stars / 4.5 個月 = 用戶痛點極度真實**
   NotebookLM 是 Google 過去 18 個月最受歡迎的 AI 產品之一（podcast 功能爆紅），但 Google 始終不開放 API。這個 gap 一旦有人填上，star 量就是真實需求的證明。**「熱門 SaaS + 沒 API + 有 LLM agent 場景」= 開源高潛力專案的公式**。

5. **多 profile 切換是企業使用者的隱藏門檻**
   `notebooklm profile switch work` 命令背後是 Google 多帳號（工作 / 個人 / 學校）的常見痛點。Web UI 切帳號要重登，CLI 內建 profile management 反而比官方好用——這是「程式介面戰勝 GUI」的典型場景。

### 與其他研究筆記的關聯

- **[CLI-Anything](cli-anything.md)** / **[LiteLLM](litellm.md)**：同樣是「把某類 AI 能力包成 SDK + CLI」的範式，但 LiteLLM 包多家 LLM provider，`notebooklm-py` 包單一 SaaS 產品。
- **[OpenClaw](openclaw.md)**：repo topic 直接寫了 `openclaw-skills`，暗示作者把 OpenClaw 與 Claude Code、Codex 並列為三大 agent host。
- **[OpenCode](opencode.md)**：兩者都示範了「在 AI agent 生態做 SDK」的新打法——OpenCode 是 agent 本身，`notebooklm-py` 是給 agent 用的工具。
- **[Casper Claude Skill Design Gallery](casper-claude-skill-design-gallery.md)** / **[dot-skill](dot-skill.md)**：研究 skill 設計時，`notebooklm-py` 的 `SKILL.md` + `notebooklm skill install` CLI 是「SDK 同時是 skill」的最佳實作參考。
- **[RAG-Anything](rag-anything.md)**：兩者都處理「多模態 source → 知識萃取」，但 RAG-Anything 是自建 pipeline、`notebooklm-py` 是借用 NotebookLM 的閉源能力——典型「自己做 vs 站在巨人肩膀上」對比。
