---
date: "2026-06-11"
category: "AI 應用"
card_icon: "material-account-voice"
oneliner: "一行 <script> 嵌入任何網站的右下角 Live2D 語音 AI 虛擬人 widget：皮（角色模型）／肉（引擎）／內容（知識庫）三分離，預設純前端、零後端、零金鑰，語音用瀏覽器內建、可選配神經語音"
tags:
  - self-hosted
  - rag
---

# AI 虛擬人 Widget（ai-avatar-bot）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/YuriCrystal/ai-avatar-bot> |
| 線上 Demo | <https://ai-avatar-bot-two.vercel.app>（須用 Chrome 桌機） |
| License | MIT（專案自身程式碼；第三方資產另有授權） |
| 語言 / 規模 | HTML/JS，42 stars |

## 專案概述

**ai-avatar-bot** 是一個「一行 `<script>` 嵌入任何網站」的右下角 **Live2D 語音 AI 虛擬人**元件。訪客可以對她說話，她會聽懂（STT）、檢索知識庫回答、開口說話（TTS）並依音量即時對嘴。整個元件透過 `embed.js` 動態建立 iframe，不干擾宿主網站。

它最核心的設計理念是**「皮肉分離」三層架構**：**肉（引擎）**＝通用核心邏輯、**皮（角色模型）**＝可換的 Live2D `.model3.json`、**內容（知識庫）**＝可換的 FAQ JSON。三者用 `data-*` 屬性各自抽換，核心程式不動。這讓同一套引擎可以套不同角色、餵不同領域知識，變成完全不同的虛擬人。

最務實的賣點是**預設純前端、免後端、不依賴任何外部網域**：語音辨識與合成都用瀏覽器內建 API（zh-TW），知識庫檢索與可選的瀏覽器內 LLM（WebLLM）都在訪客瀏覽器裡跑——**零後端、零金鑰、零雲端成本**。只有想要更自然的「神經語音」時，才需選配一支 Vercel serverless function。

## 核心功能 / 技術架構

| 檔案 | 角色 | 說明 |
|------|------|------|
| `widget.html` | **肉** | iframe 內的虛擬人本體：Live2D／STT／TTS／對嘴／LLM／檢索 |
| `embed.js` | 載入器 | 建 iframe ＋ `postMessage` 父子溝通 ＋ 對外 `window.AvatarWidget` API |
| `knowledge.js` | **內容** | 知識庫（FAQ 範例，可替換） |
| `api/tts.js` | 選配 | Vercel serverless function，取神經語音 MP3 |
| `index.html` / `demo-host.html` | 示範 | landing 頁 / 模擬客戶網站 |

**能力堆疊**：
- **Live2D 動畫** ＋ 即時對嘴（依實際音量驅動嘴型，pixi.js / pixi-live2d-display）
- **STT**：`webkitSpeechRecognition`（僅 Chromium 桌機）
- **TTS**：神經語音（自然女聲）失敗自動退回瀏覽器內建語音
- **大腦**：知識庫檢索（即時、零金鑰）＋ 可選 WebLLM（瀏覽器內 LLM，需 WebGPU / Chrome 113+，首次下載約 1GB 模型，問答不外傳）

### 一行嵌入 + 設定

```html
<script src="/path/embed.js"
        data-model="你的-live2d.model3.json"
        data-knowledge="你的-faq.json"></script>
```

| `data-*` 屬性 | 作用 | 預設 |
|---|---|---|
| `data-model` | **皮**：Live2D `.model3.json` 網址 | 內建 Haru 範例 |
| `data-knowledge` | **內容**：知識庫 JSON（`[{q,kw,a}]`） | 內建 `knowledge.js` |
| `data-api` | **肉**：神經語音端點，不設＝純瀏覽器語音 | 試同站 `api/tts` |
| `data-voice` | 神經語音聲線 | `zh-TW-HsiaoChenNeural` |
| `data-open` | 是否一進站就展開 | `true` |

對外 JS API：`window.AvatarWidget.open() / close() / say(text)`。

## 快速開始（三種方式）

1. **自帶安裝（推薦）**：把 `widget.html`、`embed.js`、`knowledge.js` 放進自己網站，貼一行 script。全在訪客瀏覽器跑，零後端零金鑰。
2. **託管一行（最快試玩）**：直接引用別人部署好的 `embed.js`（⚠ 運算/流量算在該部署者頭上）。
3. **完整版含神經語音**：`npm install && vercel --prod`，需 `api/tts.js`。沒設 `data-api` 時 widget 會自動試同站 `api/tts`，抓不到退回瀏覽器語音。

**瀏覽器需求**：Chrome/Chromium 桌機（STT 限制）；WebLLM 需 WebGPU；TTS/LLM 需 HTTPS 或 localhost。

## 目前限制 / 注意事項

作者在 README 對風險揭露相當誠實，這幾點務必注意：

- **TTS 走非官方端點**：`/api/tts` 透過 `msedge-tts` 連到微軟 Edge 朗讀的**非官方**語音服務（免金鑰）。**可能違反微軟服務條款、隨時失效或被封鎖**。正式環境應改接官方 Azure Speech。失效時自動退回瀏覽器語音。
- **`/api/tts` 是公開端點且無完整限流**：只做同網域來源檢查 ＋ 長度上限。自架者**務必在 Vercel 開用量上限（Spend Management）/ Firewall**，否則可能被當免費 TTS proxy 灌爆帳單。可用 `TTS_ALLOWED_HOSTS` 加白名單。
- **語音辨識會上雲**：`webkitSpeechRecognition` 在 Chrome 下會把**麥克風音訊上傳 Google** 處理，並非本機辨識，須告知使用者。
- **第三方授權不在 MIT 範圍**：**Live2D Cubism Core 是專有授權**（非開源，商用/再散佈須自行確認 Live2D 條款）；Haru 範例模型僅供範例，正式上線要換成自有合法授權模型（repo 不夾帶模型檔，採 CDN 引用）。
- **平台綁定 Chromium 桌機**：STT 不支援非 Chromium 與行動裝置。

### 隱私資料流向

| 功能 | 資料去哪 |
|------|---------|
| STT | 麥克風音訊 → 瀏覽器廠商雲端（Chrome=Google） |
| TTS | 文字 → 你的 `/api/tts` → 微軟非官方端點 |
| LLM／檢索 | **本機**，不外傳 |

## 研究價值與啟示

### 關鍵洞察

1. **「皮／肉／內容三分離」是把通用元件產品化的關鍵抽象**：大多數虛擬人 demo 把角色、引擎、知識寫死在一起，換個用途要改程式。ai-avatar-bot 用 `data-model` / `data-knowledge` / `data-api` 把三軸外部化，使「同引擎 × 不同皮 × 不同知識」成為配置而非開發。這個分離原則對任何想做「可複用嵌入式元件」的人都直接適用。

2. **「預設零後端」是降低採用門檻的高明取捨**：把語音、檢索、LLM 全塞進瀏覽器（Web Speech API + WebLLM），讓最小可用版本完全不需伺服器、不需金鑰、不產生雲端成本。神經語音這種「較好但有成本/風險」的能力被刻意設計成**選配且自動降級**——這是 progressive enhancement 思維的好範例：基礎版人人可跑，進階版自己承擔成本。

3. **誠實的風險揭露本身就是專案品質訊號**：README 主動點明 TTS 走非官方微軟端點、STT 音訊會上傳 Google、Live2D 核心是專有授權、公開端點可能被灌爆帳單。這種「先講壞處」的態度，比多數只秀 demo 的專案更值得信任，也是評估開源元件能否上正式環境的範本——**真正的限制往往不在功能而在授權與資料流向**。

4. **iframe + postMessage 是嵌入第三方網站的安全邊界**：用 iframe 隔離 widget、靠 `postMessage` 與宿主溝通、對外只暴露 `window.AvatarWidget` 精簡 API，避免污染宿主網站的 CSS/JS 全域。這是嵌入式 widget（如客服、聊天泡泡）的標準安全模式。

5. **「demo 讓虛擬人自己當說明書」是聰明的內容設計**：`knowledge.js` 內建內容就是「這個元件本身的使用教學」，訪客問虛擬人怎麼用，她直接答——用產品演示產品，零額外文件成本。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [Deep-Live-Cam](deep-live-cam.md) / [OpenHuman](openhuman.md) | 同屬「數位人／虛擬人」應用，但 ai-avatar-bot 主打**網頁嵌入式語音互動**（Live2D + 對嘴），而非換臉/全身生成 |
| vs [LINE Bot Multimodal RAG](linebot-multimodal-rag.md) | 都用知識庫檢索回答，但本專案是**純前端零後端**的網頁 widget，前者是 LINE 平台後端 bot |
| WebLLM 路線 | 把 LLM 推到瀏覽器端（零金鑰、隱私本機），與多數依賴雲端 API 的 AI 應用是相反的成本/隱私取捨 |

**最大啟示**：ai-avatar-bot 示範了「**把 AI 能力做成可嵌入元件**」時，真正困難的不是接 API，而是**架構分離（皮肉內容）＋ 降級策略（神經語音→瀏覽器語音）＋ 誠實的授權與資料流向揭露**。它是一個小而完整的範本：技術上不複雜，但在「如何讓別人能安全地用上你的元件」這件事上想得很周到。
