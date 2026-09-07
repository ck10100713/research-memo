---
date: "2026-09-04"
category: "AI 應用"
card_icon: "material-book-music"
oneliner: "土耳其 Deniz Şafak 的 Python 有聲書工廠:把 EPUB/PDF/txt/markdown/字幕檔丟進去,用 Kokoro-82M(82M 參數、Apache-2.0)本機 TTS 生成自然語音,並同步吐出逐句/逐字字幕(SRT/ASS/VTT)。重點不在自研模型,而在完整 pipeline——章節解析、章節標記、M4B 封面/metadata、語音混音、佇列批次、離線下載,外加可插拔 TTS 引擎架構(Kokoro + Supertonic)與 PyQt6 桌面 + Flask Web UI 雙介面;Web UI 還接了 LLM 正規化、多角色配音、Audiobookshelf 整合"
tags:
  - tts
  - audiobook
  - python
  - kokoro
---

# abogen 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/denizsafak/abogen> |
| 作者 | **Deniz Şafak**(denizsafak,denizsafak98@gmail.com;英文非母語,見命名爭議一節) |
| PyPI 套件 | `abogen` — <https://pypi.org/project/abogen/> |
| 核心 TTS 模型 | **Kokoro-82M**（hexgrad,Apache-2.0）— <https://huggingface.co/hexgrad/Kokoro-82M> · repo <https://github.com/hexgrad/kokoro> |
| 語音清單 / 樣本 | Kokoro [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) · [SAMPLES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/SAMPLES.md) |
| 第二 TTS 引擎 | **Supertonic**（PyPI `supertonic>=0.1.0`,Web UI 才有） |
| G2P / phonemizer | **misaki[zh]**（Kokoro 的字音轉換,PyPI 依賴）+ 系統套件 **espeak-ng**（必裝外部相依） |

> Metadata（**2026-09-04** 即時抓取,均取自 GitHub API 與 `git clone` 原始碼）:**5,846 stars / 440 forks / 45 open issues** · **MIT**（Kokoro 另為 Apache-2.0,兩者皆允許商用) · 建立於 **2025-04-24**,最後 push 2026-08-29 · 預設分支 `main`、共 5 分支 · **約 862 commits / 17 contributors / 27 tags** · 最新 release **v1.3.1（2026-02-06)** · repo size ≈ 7.2 MB · 主語言 **Python(2.34 MB)**,其後 JavaScript 274 KB、HTML 252 KB、CSS 80 KB(全來自 Web UI 前端)。上過 Trendshift(repo #14433)。

!!! warning "五個要先校正的判讀"
    - **它不是「自研 TTS 模型」,而是 pipeline / 編排工具**:語音品質全來自 **Kokoro-82M**(和選配的 Supertonic),abogen 本體不含聲學模型。它的價值在把「解析文件 → 切塊 → 章節/metadata → 呼叫 TTS → 對齊字幕 → 輸出多格式 → GUI」串成一條龍。看待它要用「有聲書生產線」而非「新模型」的角度。
    - **兩個介面功能集不同,別預設桌面版 = 完整版**:`abogen`(PyQt6 桌面)只有「穩定核心功能」;`abogen-web`(Flask Web UI)才有 **Supertonic 引擎、LLM 文字正規化、多角色配音、Audiobookshelf/Calibre 整合、EPUB3 read-along 匯出**。Web UI 是社群貢獻者 @jeremiahsb 一筆 **>55,000 行** 的 PR(#120)帶進來的,官方正逐步回填桌面版。
    - **逐字(word-level)字幕只有英文**:因為 [Kokoro 只對英文吐 per-word timestamp token](https://github.com/hexgrad/kokoro/blob/6d87f4ae7abc2d14dbc4b3ef2e5f19852e861ac2/kokoro/pipeline.py#L383)。其他語言退回「以音訊長度估算」的段落級(`FakeToken`),只支援 Line / Sentence / Sentence + Comma。這是設計限制,不是 bug。
    - **中文 = 簡體普通話,且無繁中/中文 GUI**:Kokoro 的 `z` 是 Mandarin Chinese,樣本文字是簡體「这是所选语音的示例」,靠 `misaki[zh]` 做 G2P;**沒有針對繁體中文的處理**,GUI 亦僅英文(roadmap 上「GUI 多語」還沒打勾)。繁中文本要唸,實務上多半得先轉簡體。且 Supertonic 那條(~35 語)**根本不含中文**。
    - **`watchers_count` 5,846 是 stars 的鏡像**(真正 `subscribers_count` 只有 30);另外 **espeak-ng 是必裝的系統級外部相依**(非 pip 能解),許多「日文沒聲音 / DLL 初始化失敗」的 issue 都跟它與 PyTorch 有關。

## 專案概述

**abogen** 是一套 Python 寫的 **文字轉語音(TTS)有聲書產生器**:把 **ePub / PDF / 純文字 / Markdown / 字幕檔** 丟進去,幾秒內產出「高品質語音 + 同步字幕」。定位是做有聲書,也做 YouTube/TikTok/Instagram 的旁白配音。名稱來自 "**a**udio**bo**ok **gen**erator"。作者 Deniz Şafak 於 2025-04 建立,一年多累積 **5.8k stars / 440 forks / 862 commits / 17 貢獻者**,active development,授權 **MIT**。

它的骨幹是 **Kokoro-82M**——一個只有 8,200 萬參數、卻在盲測排行名列前茅、**Apache-2.0** 可商用的開源 TTS 模型。abogen 把它包成「一鍵有聲書」,並補上 Kokoro 本身沒有的所有工程:文件解析、章節切分、字幕對齊、封面/metadata 嵌入、語音混音、佇列批次、離線下載。

README 一句話定位:

> *「Abogen is a powerful text-to-speech conversion tool that makes it easy to turn ePub, PDF, text, markdown, or subtitle files into high-quality audio with matching subtitles in seconds.」*

專案結構清楚地做了 **domain / application / infrastructure 分層**(受 @jeremiahsb 的 PR 重構影響),核心邏輯放 `abogen/domain/`(約 40 個模組:conversion_pipeline、subtitle_generation、chunk_utils、voice_resolution…),UI 分 `abogen/pyqt/` 與 `abogen/webui/`,兩者共用同一個 core。全 repo 有 **89 個測試檔** + GitHub Actions CI,工程密度不低,還附了一份 `AGENTS.md` 作為「斷句/字幕系統契約」文件(見下)。

## 八個看點

### 1. TTS pipeline 怎麼跑:文件 → 切塊 → Kokoro → 對齊 → 多格式

一趟轉換大致是:

```
輸入檔(EPUB/PDF/MD/TXT/字幕)
  → text_extractor 抽文字(EbookLib 讀 EPUB、PyMuPDF 讀 PDF)
  → 章節偵測,插入 <<CHAPTER_MARKER:...>> 標記,存進 cache 的 .txt(可手動編輯)
  → split_pattern / spaCy 依「語言 × 字幕模式」切成 engine 段落(見看點 6 的契約表)
  → TTS 引擎(Kokoro / Supertonic)逐段合成 24kHz 音訊 + token 時間軸
  → subtitle_generation 把 token 組成字幕條目(SRT/ASS/VTT)
  → audio_buffer / audio_sink 合併、加章節間靜音、轉檔(static_ffmpeg)
  → 輸出 wav/mp3/opus/flac/m4b + 字幕 +(選配)專案資料夾/metadata
```

作者示範:一台 **RTX 2060 Mobile** 低階筆電 GPU,約 3,000 字文字 11 秒生成 3 分 28 秒音訊;README 的 demo 更是 5 秒生成約 1 分鐘、字幕完美同步。速度來自 Kokoro 模型極小(82M)。

### 2. 支援輸入格式:EPUB / PDF / txt / markdown / 字幕檔 / 帶時間戳文字

`SUPPORTED_INPUT_FORMATS = epub, pdf, txt, srt, ass, vtt`,markdown(.md)另由 PR #75 加入。三個進階輸入機制值得記:

- **章節標記 `<<CHAPTER_MARKER:標題>>`**:處理 EPUB/PDF/MD 時自動插入(依你勾選的章節);也可手打進純文字。用途是「每章存成獨立音檔」與「只重跑出錯的某章」。
- **M4B metadata 標籤 `<<METADATA_TITLE/ARTIST/ALBUM/YEAR/COVER_PATH...>>`**:寫在文字檔開頭,產 M4B 時嵌入;EPUB/PDF 的封面會自動抽出來當 `COVER_PATH`。
- **反向:字幕檔 / 帶時間戳文字 → 語音**:丟 `.srt/.ass/.vtt` 進去可「照字幕時間軸配音」;純文字裡若出現 `HH:MM:SS[.ms]` 時間戳,abogen 會問要不要照時間戳生成——等於一個「定時旁白」產生器。要對齊時間時提供兩種對策:`TTS Regeneration`(重新以較快語速生成,音質好)或 `FFmpeg Time-stretch`(直接變速,快)。

### 3. 字幕同步機制:英文 per-word token,其餘語言段落級 fallback

這是全案最精巧、也最容易誤解的部分。Kokoro 合成時**只對英文**回傳每個詞的 `start_ts / end_ts`(timestamp token),abogen 據此做出逐字/逐詞字幕與「Sentence + Highlighting」逐詞高亮。非英文語言 Kokoro 不給 token,abogen 就用 `abogen/domain/tokens.py` 的 **`FakeToken`**——以整段音訊長度反推、產段落級假 token,讓字幕仍能對齊到「句」而非「詞」。

字幕模式:`Disabled / Line / Sentence / Sentence + Comma / Sentence + Highlighting / 1~N words`。其中 **N words 系列僅英文**;非英文只有 Line/Sentence/Sentence+Comma(v1.2.4 起「所有語言都能生字幕」即指這條 duration-based fallback)。字幕格式除 SRT 外,ASS 提供 wide / narrow / centered wide / centered narrow 五種版面,方便直接壓進影片。

### 4. 支援語言與語音:Kokoro 9 語系 54 個聲音 + Supertonic ~35 語

**Kokoro(兩介面皆有)** 支援 9 個語系,voice ID 前綴第一碼是語言、第二碼是性別(`a`merican `f`emale = `af_`):

| 碼 | 語言 | 靜態聲音數 |
|----|------|-----------|
| `a` / `b` | 美式 / 英式英語 | 20 / 8 |
| `z` | **中文(簡體普通話)** | 8(zf_×4、zm_×4) |
| `j` | 日語(需 `misaki[ja]`) | 5 |
| `e` `f` `h` `i` `p` | 西 / 法 / 印地 / 義 / 巴西葡 | 各 1~4 |

程式碼 `plugins/kokoro/__init__.py` 內建 **54 個** 靜態 voice manifest。**Voice Mixer(語音混音)**:可用「voice formula」把多個聲音加權混成自訂音色(含 `*`/`+` 運算)、存成 profile,並提供試聽。

**Supertonic(僅 Web UI)** 走另一套語言碼,支援約 **35 種**歐洲 + 亞洲語言(en/de/fr/es/ja/ko/ru/vi/tr…),**但不含中文**。它是較新的引擎,主打 GPU 加速。

### 5. 可插拔 TTS 引擎架構(工程亮點)

abogen 沒把 Kokoro 寫死,而是設計了一層 **TTS Plugin 架構**(`abogen/tts_plugin/`):定義 `Engine` / `EngineSession` protocol、`PluginManifest`(含 semver 的 `api_version`、`capabilities`、`VoiceLister`)、`plugin_manager` 與 loader。實際引擎放在獨立的 `plugins/kokoro/` 與 `plugins/supertonic/`,各自把「Language enum ↔ 引擎內部語言碼」的轉換封在引擎內部(呼叫端永遠看不到 kokoro 的 `a/b/z` 或 Supertonic 的 ISO 碼)。這讓「新增第三個 TTS 引擎」變成寫一個 plugin 的事,是這個專案少見的「為擴充而設計」的架構決策,也附了 `tests/plugins/` 一整套針對 plugin 載入失敗情境的測試。

### 6. `AGENTS.md`:把「斷句/字幕」寫成一份契約(給 AI 改碼用)

repo 根目錄的 `AGENTS.md` 不是行銷文,而是一份**工程契約**:一張表格窮舉「字幕模式 × 語言(英/非英 spaCy 開關/CJK)」該用哪個 split pattern 餵給 TTS 引擎。它明說是在一個 bug(sentence 模式把全文當成一整段 → 一條巨大字幕)之後寫的,並要求「**改這行為前必須先更新這張表**」。對 CJK(ja/zh)特別列了 `(?<=[.!?؟。！？।])\s*|\n+` 這類「用標點斷句、字元間不需空格」的規則。這份文件本身就是一個很好的「如何用文件把易錯領域知識固化、避免 AI/貢獻者改壞」的範例。

### 7. GPU/CPU/離線、安裝與輸出格式

- **算力後端**:PyTorch,支援 NVIDIA CUDA 12.6 / 12.8 / 13.0、AMD ROCm 6.4(**僅 Linux**,Windows 無 ROCm)、Apple Silicon MPS(裝 Kokoro dev 版)、以及 **CPU fallback**(慢但可跑)。用 optional-dependencies(`abogen[cuda]` / `[cuda126]` / `[cuda130]` / `[rocm]`)+ uv 的多 index 對應不同 wheel。
- **離線**:設定選單有「Pre-download models and voices for offline use」一次抓齊 Kokoro 模型/聲音/spaCy 模型,再配「Disable Kokoro's internet access」即可完全離線;所有推論本機跑,文字不外流(唯一會連外的是 Web UI 的選配 LLM 正規化)。
- **安裝**:`uv tool install abogen`(推薦)/ `pip install abogen` / Windows 的 `WINDOWS_INSTALL.bat`(內含 embedded Python,免另裝 Python,但仍要自行裝 espeak-ng)/ Docker(Web UI,`abogen-web` 開 8808 埠)。Python 3.10–3.12。
- **輸出格式**:音訊 **WAV / MP3 / OPUS / FLAC / M4B(含章節)**;字幕 **SRT / ASS / VTT**。另有佇列批次(Queue Mode)可一次排多檔、各自保留設定。

### 8. Web UI 專屬的「進階 AI 功能」(與本研究站的關聯)

Web UI(v1.3.0 起)加了幾個和 LLM/自動化沾邊、對本站較有意思的功能:

- **LLM 輔助文字正規化**:把難唸的縮寫/所有格撇號交給 **OpenAI-compatible 端點**(Ollama、OpenAI proxy…)改寫,設定在 Settings → LLM,支援 sentence/paragraph/document 三種 context 視窗與自訂 prompt,可用 `.env` 的 `ABOGEN_LLM_*` 預先注入。`abogen/llm_client.py` 是自己用標準庫 urllib 手刻的極簡 client(含 tool-call 資料結構),不綁 SDK。
- **專有名詞發音覆寫**:`entity_analysis.py` 用 spaCy 抽出人名/地名等實體,配 `pronunciation_store.py` 讓使用者對特定專有名詞指定發音。
- **多角色「劇場化」配音**:`speaker_analysis.py` 用對白動詞(said/asked/whispered…)與 `Name:` 冒號格式,把台詞歸屬到角色,再指派不同聲音,做出多角色有聲劇。
- **整合**:Calibre **OPDS** 匯入、推送到 **Audiobookshelf** 有聲書伺服器;**EPUB 3 media-overlay** 匯出(帶時間軸的 read-along 電子書)。
- **JSON API**:`GET /api/jobs/<id>` 等端點可程式化查狀態,適合接自動化流程。

## 授權與商用可行性

- **abogen 本體:MIT**;**Kokoro-82M:Apache-2.0**——兩者都明確允許商用、修改、再散布與私用。README 特別點出這點,對想拿它做商業有聲書/配音的人是綠燈。
- 相依裡 **PyQt6** 為 GPL/商業雙授權(桌面 GUI);若要閉源商用桌面版需注意其授權,但 **Web UI(Flask)這條沒有 PyQt 的顧慮**。espeak-ng 為 GPL,但是外部系統程式、非連結進來,一般以「工具相依」看待。
- 隱私上是 **local-first**:預設全本機推論,可完全離線;唯一外連是 Web UI 選配的 LLM 正規化(可不用)。

## 與其他有聲書/TTS 工具的差異

README 自陳受這些專案啟發:[audiblez](https://github.com/santinic/audiblez)、[autiobooks](https://github.com/plusuncold/autiobooks)、[pdf-narrator](https://github.com/mateogon/pdf-narrator)、[epub_to_audiobook](https://github.com/p0n1/epub_to_audiobook)、[ebook2audiobook](https://github.com/DrewThomasson/ebook2audiobook)。abogen 的差異點:

- **「同步字幕」是一等公民**:多數 epub→有聲書工具只出音訊,abogen 把字幕(逐句/逐字/高亮、多版面 ASS)做成核心賣點,適合影片旁白而不只是聽書。
- **雙介面 + 可插拔引擎 + 89 測試**的工程完整度,高於多數同類單檔腳本。
- **Kokoro-82M** 這個「小而強、Apache-2.0」的模型選型,讓它在低階 GPU 甚至 CPU 上都能實用,和動輒吃大模型的方案不同。
- 相對地,它**不做語音克隆**(voice cloning),這點不如 ebook2audiobook;客製音色只能靠 voice mixer 混既有聲音。

## 注意事項與已知限制

- **espeak-ng 是最常見的坑**:必須先自行安裝(Windows 下 .msi、mac `brew`、Linux 套件管理器);日文還要 `misaki[ja]`。相關 issue(日文沒聲音、`WinError 1114` DLL、`CUDA not available`)多半繞著 espeak-ng 與 PyTorch/CUDA 版本打轉。
- **桌面版 ≠ Web UI 功能**:新功能先進 Web UI 再回填桌面,想要 Supertonic/LLM/ABS 就得用 `abogen-web`。
- **繁中/中文在地化弱**:GUI 只有英文;中文語音是簡體普通話(靠 misaki[zh]),無繁中專屬處理;Supertonic 不支援中文。
- **命名爭議**:作者在 [HN 討論](https://news.ycombinator.com/item?id=44853064)後於 README 說明,"abo" 前綴在澳洲/紐西蘭可能被理解為對原住民的蔑稱,強調命名純為技術縮寫(audiobook generator)、無冒犯之意。屬需知悉的社群脈絡。
- Roadmap 尚未完成項:PDF 的 OCR(docling/tesseract)、GUI 多語、kokoro-onnx。

## 研究價值與啟示

### 關鍵洞察

1. **「薄模型 + 厚 pipeline」是開源 AI 應用的甜蜜點**:abogen 幾乎不碰模型訓練,全部力氣花在「把一個現成的小而強模型(Kokoro-82M)產品化」——文件解析、章節、字幕對齊、多格式、GUI、離線。它的 5.8k 星證明:**在一個好用的開源模型外面,補齊真實使用者要的所有工程瑣事,本身就是巨大的價值**。這和 [Koharu](koharu.md) 用 staged pipeline 組合多個專用模型是同一種產品哲學的兩面——一個組合多模型,一個把單模型做深。

2. **為擴充而設計的 plugin 架構,是它跟同類單檔腳本的分野**:多數 epub→有聲書工具把 TTS 呼叫寫死;abogen 抽出 `Engine`/`EngineSession` protocol + `PluginManifest`(帶 semver api_version),把引擎語言碼封裝在引擎內,於是「Kokoro → 再加 Supertonic」只是加一個 plugin。**當一個工具想從個人腳本長成社群專案,這種介面抽象幾乎是必經之路**,也直接讓那筆 5.5 萬行的社群 PR 有地方落地。

3. **用文件(`AGENTS.md`)把易錯領域知識固化,是防止 AI/貢獻者改壞的實務手法**:斷句規則是這種「改一個 regex 就默默壞掉、且很難用單元測試全覆蓋」的地雷。作者的做法是把「語言 × 模式 → pattern」寫成一張契約表 + 「改前先更新此表」的規範。這與本站 [slide-deck-skill](slide-deck-skill.md) 把「頁數=備註數」設成硬契約、用機器可驗證標準守住品質,是同一種工程直覺:**把只有踩過雷才知道的知識,寫成後人(含 AI)必須遵守的顯性契約**。

4. **字幕同步暴露了「模型能力邊界決定產品功能邊界」**:逐字字幕只有英文,純粹因為上游 Kokoro 只對英文吐 timestamp token。abogen 的處理不是硬幹,而是誠實地用 `FakeToken` 做段落級 fallback,並在 UI/README 明講限制。這是很好的一課:**當你的產品建立在別人的模型上,你的功能矩陣會被上游能力直接切割,老實標示邊界比假裝支援更可信**。

### 與其他研究筆記的關聯

- **[Koharu](koharu.md)**:同為「local-first、多階段 ML pipeline、可完全離線」的桌面 AI 應用。差別在 Koharu 組合多個專用模型(偵測/OCR/inpaint/翻譯)、還內建 agent;abogen 是把單一 TTS 模型做深、做全。兩者並讀可看「組合 vs 深化」兩種 pipeline 策略。
- **[slide-deck-skill](slide-deck-skill.md)**:兩者都用「顯性契約 + 機器可驗證標準」守品質(前者頁數=備註、溢出偵測;後者 `AGENTS.md` 斷句表)。是本站兩個最好的「用契約防退化」對照。
- **LLM 正規化那條**:abogen Web UI 接 OpenAI-compatible / Ollama 端點只為「改寫難唸的縮寫」,是「把 LLM 當文字前處理小工具」的輕量用法,和把 LLM 當主角的 agent 型專案形成有趣對比。

## 一句話總結

> 土耳其開發者 Deniz Şafak 的 Python 有聲書生產線:核心是拿 82M 參數、Apache-2.0 可商用的 **Kokoro-82M** 本機 TTS,外面補齊 EPUB/PDF/MD/字幕解析、章節標記、M4B metadata、語音混音、多格式輸出與**逐句/逐字同步字幕**,並用可插拔引擎架構接上第二個引擎 Supertonic。MIT 授權、5.8k 星、862 commits、89 測試,工程完整;PyQt6 桌面與 Flask Web UI 雙介面(Web UI 另有 LLM 正規化、多角色配音、Audiobookshelf 整合)。真正的護城河不是模型,而是把一個好模型徹底產品化的所有瑣碎工程——以及一張把斷句規則寫死的契約表。中文僅簡體普通話、GUI 無繁中。
