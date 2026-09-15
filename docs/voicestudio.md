---
date: "2026-09-15"
category: "AI 應用"
card_icon: "material-microphone-message"
oneliner: "29.5K★、AGPL-3.0 的「本機版 ElevenLabs」——聲音複製、聲音設計、影片配音、聽寫、轉錄、有聲書，16 個 TTS + 11 個 ASR 引擎、646 種語言，全程跑在自己機器上，不用帳號、金鑰、訂閱。Tauri v2 + React + FastAPI，預設接 loopback，內建 AudioSeal 浮水印與 MCP server。repo 本身也是 AI 輔助開發的樣本（CLAUDE.md 18KB、skills/、skills-lock.json）"
tags:
  - self-hosted
  - mcp
  - claude-code
  - desktop-app
---

# VoiceStudio 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★29,486 / 3,577 forks / AGPL-3.0） | <https://github.com/debpalash/VoiceStudio> |
| 官方站 | <https://voicestudio.sh> |
| 簡體中文 README | [README_CN.md](https://github.com/debpalash/VoiceStudio/blob/main/README_CN.md) |
| Colab 試用 | [OmniVoice_Studio_Colab.ipynb](https://colab.research.google.com/github/debpalash/VoiceStudio/blob/main/notebooks/OmniVoice_Studio_Colab.ipynb) |
| Agent skills 安裝 | `npx skills add debpalash/VoiceStudio`（[skills.sh](https://skills.sh) 相容） |

> **Metadata（2026-09-15 抓取）**：**29,486 stars / 3,577 forks / 82 open issues** · **AGPL-3.0** · 建立於 **2026-04-09**、最後 push **2026-09-14** · Python · repo size 約 83 MB · **CHANGELOG 有 290 KB**。前身叫 **OmniVoice-Studio**（`omnivoice` 這個名字還留在程式碼與 Docker image 裡）。

!!! warning "兩個要先知道的狀態"
    - **Active beta。** README 明講要用 [latest release](https://github.com/debpalash/VoiceStudio/releases/latest) 做正事，`main` 會在版本之間變動。
    - **桌面殼正在從 Tauri 改寫成 Electron。** README 最上方就掛著「Electron Rewrite Ongoing: Please don't create desktop app related issues and PR」——**現在不要提桌面 app 相關的 issue 或 PR**。下面寫的 Tauri 架構是改寫前的狀態。

## 一句話定位

> **開源、全本機的 ElevenLabs 替代品。** 本機工作流**不用帳號、不用 API key、不用訂閱、沒有用量計費**。

| | 內容 |
|---|---|
| **工作流** | 聲音複製、聲音設計、影片配音、聽寫、故事、有聲書、批次生成 |
| **語言** | **646 種 TTS 語言**（實際覆蓋與品質取決於選的引擎） |
| **引擎** | **16 個 TTS · 11 個 ASR**，在 Model Catalogue 或 <kbd>Ctrl/Cmd</kbd>+<kbd>E</kbd> 切換 |
| **平台** | macOS 13.3+（Apple Silicon）· Windows 10/11 x64 · Linux x86_64 (glibc 2.39+) · Docker |
| **算力** | CUDA · Apple Silicon MPS/MLX · Linux ROCm · CPU · 選配遠端 worker |
| **介面** | 桌面 app · 本機 REST/SSE/WebSocket API · **OpenAI 相容音訊 API** · **MCP Server** |
| **儲存** | 聲音、專案、設定、輸出預設留在本機 |

## 功能盤點

| 面向 | 內容 |
|------|------|
| **Voice Cloning** | 短樣本 zero-shot 合成，**3 秒可用、5–15 秒更好** |
| **Voice Design** | 用年齡、口音、音高、風格、演繹指示「設計」出一個聲音 |
| **Video Dubbing** | 轉錄 → 翻譯 → 保留說話者 → 合成 → 匯出影片；完成的配音會**標出時序問題供覆核** |
| **Stories / Audiobooks** | 多聲道腳本、EPUB/PDF 匯入、逐章渲染、`.m4b` 匯出 |
| **Dictation Widget** | 全系統快捷鍵、即時轉錄、**選配本機 LLM 清稿** |
| **Vocal Isolation** | Demucs 人聲／背景分離 |
| **Speaker Diarization** | Pyannote + WhisperX 說話者指派 |
| **Batch Queue** | 大量音訊／影片任務排隊，或**監看本機資料夾**自動處理新影片 |
| **AI Watermark** | **AudioSeal 嵌入與偵測** |
| **MCP Server** | 給 MCP client 用的合成與轉錄工具 |

## 架構

```text
Tauri v2 桌面殼 (Rust)
        │ IPC
React + Vite UI
        │ HTTP · SSE · WebSocket on localhost:3900
FastAPI 後端
        ├── TTS / ASR 引擎註冊表
        ├── 配音 / 音訊 / 長文本 pipeline
        ├── OpenAI 相容 API 與 MCP server
        └── SQLite + Alembic → omnivoice_data/
```

引擎放在 `backend/engines/`，是**隔離且選配的 adapter**；`backend/worker/` 處理認證過的遠端運算與任務傳輸。

### 網路邊界（這部分設計得很紮實）

- 桌面端只跟 **loopback-only 後端**（`localhost:3900`）講話
- **Loopback API 呼叫不需要 server key；遠端存取需要 share PIN 或 API key**
- 遠端 worker 與 OpenAI 相容 ASR **都是 opt-in**。Loopback ASR 可以用 HTTP 且音訊不離開機器；**非 loopback endpoint 強制 HTTPS，而且不跟隨 redirect**
- **Analytics 在同意之前是關的**。開啟後只送允許清單內、不含內容的使用中繼資料——**永不傳送文字、音訊、檔名或專案**

> 「非 loopback 強制 HTTPS 且不跟隨 redirect」這個細節很少見但很對——**跟隨 redirect 正是把加密連線降級成明文的常見路徑**。

## 兩個對 agent 使用者特別相關的入口

**MCP Server** 掛在 `http://localhost:3900/mcp`，工具有 `generate_speech`、`clone_voice`、`transcribe`：

```json
{ "mcpServers": { "voicestudio": { "url": "http://localhost:3900/mcp" } } }
```

需要 stdio transport 的 client 有內建 shim（`python -m backend.mcp_shim`）。

**Agent Skills** 可以直接裝進 Claude Code、Codex、Cursor：

```bash
npx skills add debpalash/VoiceStudio
```

- `omnivoice`：透過本機 VoiceStudio 合成語音與轉錄音訊
- `oss-maintainer`：**這個 repo 自己的開源維護工作流**

**OpenAI 相容音訊 API**：把 `base_url` 從 `https://api.openai.com/v1` 換成本機後端就能用——**現有程式碼幾乎不用改就從雲端切到本機**。

## repo 本身就是一個 AI 輔助開發的樣本

翻根目錄會看到一組很有時代感的檔案：

| 檔案／目錄 | 意義 |
|-----------|------|
| `CLAUDE.md`（**18 KB**） | 給 Claude Code 的專案指令 |
| `AGENTS.md`（4.5 KB） | 通用 agent 指令 |
| `.claude/` · `.agents/` | agent 設定 |
| `skills/` + `skills-lock.json` | **skill 有 lock file**——像鎖依賴一樣鎖技能版本 |
| `.coderabbit.yaml`（9.7 KB）· `greptile.json` | 兩套 AI code review 服務的設定 |
| `.gitleaks.toml` | 密鑰掃描 |
| `CHANGELOG.md`（**290 KB**） | 五個月累積的變更紀錄 |

> **`skills-lock.json` 這個東西值得單獨記一筆。** agent skill 生態現在多半是「把 markdown 丟進資料夾」，這個 repo 把它當成依賴管理——**有 lock file 就代表可重現、可稽核、可回滾**。這可能是 skill 生態成熟的一個早期訊號。

## 授權要看清楚（AGPL-3.0 的三層）

這是本專案最容易踩雷的地方：

1. **應用本體是 AGPL-3.0**。可以執行、修改、內部使用；但 AGPL 的網路條款意味著**如果你改了它並提供網路服務，要開源你的修改**。
2. **應用授權本身不限制你賣產出的音訊**，但——
3. **下載的模型與 tokenizer 有各自的條款**，可能會限制。`omnivoice/` 那包 Python 上游是 Apache-2.0，但**預設下載的權重與音訊 tokenizer 用的是另外的條款**。

**要商用的話，AGPL 只是第一關，真正要查的是你選的那個引擎的模型授權。**

## 目前限制

- **Active beta + 桌面殼正在改寫**。現在不是導入生產流程的好時機，除非你固定在某個 release。
- **82 個 open issue**，以 29.5K★ 的體量算是合理，但要注意處理速度。
- **Intel Mac 跑不了本機 Python 後端**，得用遠端後端。
- **Docker image 只有 `linux/amd64`**；Apple Silicon 要用原生 app 才有 GPU 加速。
- **Windows 的 AMD / Ryzen AI 只能用 CPU**；ROCm 只有 Linux 且 opt-in。
- **646 種語言是「目錄」數，不是「646 種都好用」**——README 自己註明「實際覆蓋與品質取決於選的引擎」。
- 最低需求 8 GB RAM / 10 GB 磁碟 / GPU 選配（用 GPU 時 4 GB VRAM 起跳）。

## 研究價值與啟示

### 關鍵洞察

1. **「換個 base_url 就從雲端切到本機」是本機優先工具最有效的採用策略。** VoiceStudio 提供 OpenAI 相容音訊 API，意味著現有接 ElevenLabs / OpenAI TTS 的程式碼幾乎不用改。**相容既有 API 比功能更強更能決定一個開源替代品會不會被用。**

2. **AudioSeal 浮水印預設開啟，是負責任的預設值。** 一個讓任何人都能 zero-shot 複製聲音的工具，**把合成語音標記做成預設而不是選項**，是把倫理責任寫進架構而不是寫進免責聲明。對照 README 的 Responsible use 章節（明確要求取得說話者同意），整體態度是一致的。

3. **網路邊界的三條規則可以直接抄**：loopback 免金鑰但遠端要 PIN／key、非 loopback 強制 HTTPS 且不跟隨 redirect、analytics 同意前不啟動且永不傳內容。**「本機優先」不是一句行銷話，是一組可以逐條檢查的設計約束。**

4. **`skills-lock.json` 可能是 agent skill 生態的下一步。** 現在的 skill 多半沒有版本管理，改了就改了。**把 skill 當依賴鎖起來**，代表有人開始把 agent 能力當成生產依賴在管——這件事遲早會變成標配。

5. **五個月 29.5K★，但這個 repo 最有趣的不是星數，是它把 AI 輔助開發的整套配置公開了**：18 KB 的 `CLAUDE.md`、兩套 AI code review 服務、skill lock file、290 KB 的 CHANGELOG。**想知道「用 agent 開發一個 29K★ 專案長什麼樣」，這個 repo 的根目錄就是答案。**

6. **AGPL + 模型授權的雙層結構，是所有本機 AI 工具的共同陷阱。** 應用開源不等於你能商用它的產出——**真正的限制在權重那一層**，而那一層通常沒寫在 README 的 License 章節裡。

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [abogen](abogen.md) | 同為 EPUB/PDF 轉有聲書；abogen 專精這一件事，VoiceStudio 是整套語音工作站 |
| [Deep-Live-Cam](deep-live-cam.md) | 同為「本機跑、有倫理爭議」的生成工具；VoiceStudio 的 AudioSeal 預設浮水印是比較負責任的處理方式 |
| [OpenHuman](openhuman.md) / [AI Avatar Bot](ai-avatar-bot.md) | 數位人／虛擬人方向，VoiceStudio 可以當它們的語音層 |
| [notebooklm-py](notebooklm-py.md) | 同樣涉及長文本轉語音；那個接雲端，這個全本機 |
| [反詐投資王](anti-gambling-trader-tw.md) / [Open SEO Advisor](open-seo-advisor-skill.md) | 共同點是 repo 裡都有 `.claude/` 與 agent 設定——**2026 年的開源專案結構正在長出新的一層** |
