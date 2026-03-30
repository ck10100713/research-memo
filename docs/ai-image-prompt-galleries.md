---
date: ""
category: "AI 創作資源"
icon: "material-image-multiple"
oneliner: "Civitai、PromptHero、Lexica 等 15+ 平台全景比較，涵蓋 SFW/NSFW、選擇決策樹"
---
# AI 圖像生成 Prompt Gallery 生態研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| Civitai 官網 | [civitai.com](https://civitai.com/) |
| Civitai 2026 評測 | [WeShop AI — Is it Still the King?](https://www.weshop.ai/blog/civitai-review-2026-is-it-still-the-king-of-ai-art%EF%BC%9F/) |
| Civitai 生態分析 | [Flowith — GitHub of AI Art](https://flowith.io/blog/civitai-model-hub-2026-github-of-ai-art/) |
| 免費 Prompt 庫評比 | [vakpixel — Best Free AI Image Prompt Libraries 2026](https://vakpixel.com/blog/best-free-ai-image-prompt-libraries-2026) |
| Prompt 庫平台評測 | [God of Prompt — Honest Review 2026](https://www.godofprompt.ai/blog/review-popular-ai-prompt-library-platforms) |
| NSFW 平台比較 | [Somake AI — Civitai Alternatives](https://www.somake.ai/guides/civitai-alternatives) |
| 台灣 Prompt 資源整理 | [INSPARK.LAB — 五大生圖提示詞平台](https://insparklab.com/lifestyle/image-prompt-library/) |
| Promptchan vs SoulGen | [TopAI.tools 比較](https://topai.tools/compare/promptchan-ai-vs-soulgen-net) |

## 概述

AI 圖像生成的 Prompt Gallery / Database 已發展為一個龐大的生態系，從純粹的 prompt 文字庫演化為集「prompt + 視覺預覽 + 模型參數 + 社群分享 + 線上生圖」於一體的創作平台。本筆記系統性整理 2026 年主要平台，涵蓋 SFW 與 NSFW 兩大區塊。

核心趨勢：**prompt 不再只是文字** — 好的 prompt 資料庫必須附帶「成品預覽 + 完整參數紀錄」才有實用價值，單純的文字清單已經過時。

## 生態全景圖

```
┌─────────────────────────────────────────────────────────────────┐
│                AI Image Prompt Gallery 生態                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  第一層：社群生態平台（模型 + Prompt + Gallery + 生圖）    │   │
│  │                                                         │   │
│  │  Civitai (800萬+ prompts, 開源AI藝術社群之王)            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │ 第二層：Prompt 搜尋    │  │ 第二層：生圖 + Gallery │           │
│  │                      │  │                      │           │
│  │ PromptHero (百萬+)   │  │ Promptchan (200萬+)  │           │
│  │ Lexica.art (以圖搜圖) │  │ SoulGen (人臉一致)   │           │
│  │ OpenArt              │  │ PixAI (動漫特化)     │           │
│  │ Arthub.ai            │  │ Yodayo (多模型)      │           │
│  │ PromptDen            │  │ Mage Space (SD)     │           │
│  └──────────────────────┘  │ Perchance (免費)     │           │
│                             │ BasedLabs (免註冊)   │           │
│  ┌──────────────────────┐  └──────────────────────┘           │
│  │ 第三層：工具型 / 模板  │                                     │
│  │                      │  ┌──────────────────────┐           │
│  │ Promptomania (組合器) │  │ 第三層：細分市場      │           │
│  │ Kalon.ai (美學模板)   │  │                      │           │
│  │ A1.art (50+ prompts) │  │ Uniform Map (制服/動漫)│           │
│  │ PromptWall (1000+)   │  │ Candy AI (AI 伴侶)   │           │
│  │ The Prompt Index      │  │ AI Gallery (無審查)   │           │
│  │ SpacePrompts (每日新增)│  └──────────────────────┘           │
│  │ NanoBanana (400+案例) │                                     │
│  └──────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
```

## SFW 平台詳細比較

### Tier 1：社群生態平台

#### Civitai — AI 藝術社群之王

| 指標 | 數值 |
|------|------|
| Prompt 數量 | 800 萬+ |
| 模型數量 | 數十萬（Checkpoint、LoRA、Embedding） |
| 核心定位 | 開源 AI 藝術的 GitHub |
| 支援模型 | Stable Diffusion、Flux、SDXL 等 |
| 內建生圖 | Airship（支援 ControlNet、Inpainting） |
| 費用 | 免費瀏覽，Buzz 點數制（$10/10K Buzz） |

**殺手級功能**：每張圖自動偵測並顯示完整生成參數 — prompt、negative prompt、sampler、steps、CFG、seed。這種「激進透明」在創作 AI 社群中獨一無二，讓任何人都能精確復現他人的作品。

```
一張 Civitai 圖片的 Metadata：
┌────────────────────────────────────┐
│ Prompt: masterpiece, best quality, │
│   1girl, school uniform, ...       │
│ Negative: lowres, bad anatomy, ... │
│ Model: AnythingV5                  │
│ Sampler: DPM++ 2M Karras          │
│ Steps: 28                         │
│ CFG Scale: 7                      │
│ Seed: 1234567890                  │
│ Size: 512x768                     │
└────────────────────────────────────┘
→ 任何人可用相同參數精確復現這張圖
```

### Tier 2：Prompt 搜尋引擎

| 平台 | 規模 | 核心差異化 | 費用 |
|------|------|-----------|------|
| **[PromptHero](https://prompthero.com/)** | 數百萬 | 多平台（MJ / SD / DALL-E / Sora），搜尋 + 預覽 | 免費，Pro $19.99/月 |
| **[Lexica.art](https://lexica.art/)** | 數百萬 | **以圖搜 prompt**（上傳圖片找相似 prompt），SD 特化 | 免費瀏覽 |
| **[OpenArt](https://openart.ai/)** | 大量 | Gallery + prompt 分享 + 內建生圖 | 免費 + 付費 |
| **[Arthub.ai](https://arthub.ai/)** | 中量 | 標籤分類瀏覽，社群導向 | 免費 |
| **[PromptDen](https://promptden.com/)** | 中量 | Midjourney Gallery 展示，社群投稿 | 免費 |

**Lexica 的獨特能力**：大多數平台只能「用文字搜 prompt」，Lexica 支援「用圖片搜 prompt」— 上傳一張你喜歡的圖，它會找出類似風格的 prompt。這解決了「我想要這種感覺但不知道怎麼描述」的痛點。

### Tier 3：工具型 / 模板型

| 平台 | 規模 | 核心差異化 | 費用 |
|------|------|-----------|------|
| **[Promptomania](https://promptomania.com/)** | 工具 | **Visual Prompt Builder** — 拖拉式 UI 組合 prompt | 免費 |
| **[NanoBanana Prompt Library](https://www.promptlibrary.space/)** | 400+ 案例 | 每案例附 prompt + 成品 + 創作者，社群驅動 | 免費 |
| **[The Prompt Index](https://www.thepromptindex.com/)** | 1,000+ | DALL-E / MJ / SD，依風格分類 | 免費 |
| **[PromptWall](https://www.chatgptimage.art/)** | 1,000+ | ChatGPT / MJ / NanoBanana | 免費 |
| **[SpacePrompts](https://www.spaceprompts.com/gallery)** | 每日新增 | 社群投稿，寫實 / 抽象 / 建築等 | 免費 |

### 細分市場

| 平台 | 特化領域 | 說明 |
|------|---------|------|
| **[Uniform Map](https://uniform.wingzero.tw/en/prompts)** | 制服 / 動漫 | 台灣，3,000+ prompts，正交分類（角度 × 髮型 × 打光 × 風格），視覺預覽 |
| **[Krea AI](https://krea.ai/)** | 設計 / 創意 | 繪圖 + 影片 prompt 分享，偏專業設計用途 |

## NSFW 平台詳細比較

### 生圖 + Gallery 平台

| 平台 | 規模 | 核心特色 | 費用 |
|------|------|---------|------|
| **[Civitai](https://civitai.com/)** | 800 萬+ | SFW/NSFW 切換，最完整的模型 + prompt 生態 | 免費，Buzz 付費加速 |
| **[Promptchan](https://promptchan.ai/)** | 200 萬+ 作品 | NSFW 專用最大社群，anime / 3D / 寫實 / 超奇幻多風格 | $5.99/月 |
| **[SoulGen](https://www.soulgen.net/)** | 大量 | **人臉一致性極強**（跨圖/影片保持角色），2025 推出影片 | $9.99/月 |
| **[PixAI](https://pixai.art/)** | 大量 | 動漫特化，VisualChat 對話式生圖 | 免費 + 付費 |
| **[Yodayo](https://yodayo.com/)** | 中量 | 多模型（寫實 / 可愛動漫 / 3D） | 免費 + 付費 |
| **[Mage Space](https://www.mage.space/)** | 中量 | 基於 Stable Diffusion，文字 + 圖生圖 | 免費 + 付費 |

### 免費 / 無註冊平台

| 平台 | 特色 | 限制 |
|------|------|------|
| **[Perchance AI](https://perchance.org/)** | 完全免費，可載入 Civitai 模型，無審查 | 速度較慢 |
| **[BasedLabs](https://www.basedlabs.ai/)** | 免註冊免費 NSFW 生圖 | 功能較基本 |
| **[AI Gallery (GenApe)](https://app.genape.ai/)** | 瀏覽器內生圖，無 NSFW 審查 | 品質取決於模型 |

### Prompt 模板 / 參考庫

| 平台 | 內容 | 費用 |
|------|------|------|
| **[Kalon.ai](https://www.kalon.ai/templates/nsfw-ai-art-prompts)** | Fine art nude 構圖 + 5 種 NSFW 美學風格模板 | 付費 |
| **[A1.art](https://a1.art/prompts/nsfw)** | 50+ NSFW prompts，可直接複製 | 免費 |
| **[Arthub.ai NSFW](https://arthub.ai/tags/NSFW)** | NSFW 標籤分類瀏覽 | 免費 |

### AI 伴侶型（生圖 + 角色互動）

| 平台 | 特色 | 費用 |
|------|------|------|
| **[Candy AI](https://candy.ai/)** | 寫實/動漫虛擬角色，roleplay + 多媒體，個性/外觀可客製 | $12.99/月起 |

## 平台選擇決策樹

```
你的需求是什麼？
│
├─ 學習 prompt 寫法 / 找靈感
│   ├─ 想用圖片搜 prompt → Lexica.art
│   ├─ 想看完整參數（可復現） → Civitai
│   └─ 想快速瀏覽多平台 prompt → PromptHero
│
├─ 組合 / 建構 prompt
│   ├─ 拖拉式視覺化組合 → Promptomania
│   ├─ 正交維度組合（角度×髮型×光線） → Uniform Map
│   └─ 美學風格模板 → Kalon.ai
│
├─ 線上直接生圖
│   ├─ 免費 + 無限制 → Perchance AI
│   ├─ SD 生態 + 社群 → Civitai Airship
│   ├─ 動漫特化 → PixAI / Yodayo
│   └─ NSFW 專用 → Promptchan / SoulGen
│
├─ 社群分享 / 投稿
│   ├─ 最大社群 → Civitai
│   ├─ NSFW 最大 → Promptchan (200萬+)
│   └─ 台灣 / 制服特化 → Uniform Map
│
└─ 角色一致性（跨圖/影片保持同一角色）
    └─ SoulGen
```

## 目前限制 / 注意事項

1. **版權灰色地帶** — AI 生成圖片的版權歸屬在各國法規仍不明確，商業使用需謹慎
2. **NSFW 平台穩定性** — 部分 NSFW 平台受支付處理商壓力，可能突然關閉或變更政策
3. **Prompt 品質參差** — 大型社群平台的 prompt 品質差異極大，高 like 數 ≠ 高品質 prompt
4. **模型版本敏感** — 同一 prompt 在不同模型版本（SD 1.5 vs SDXL vs Flux）效果可能截然不同，平台上的 prompt 不一定標注適用模型
5. **隱私風險** — 部分平台會將使用者上傳的圖片和 prompt 公開展示，上傳前需確認隱私政策
6. **成本隱藏** — 「免費」平台通常在速度、解析度、每日次數上有限制，實際高頻使用需付費
7. **內容審查政策變動** — 主流平台（如 Civitai）的 NSFW 政策可能隨時調整，不可過度依賴單一平台

## 研究價值與啟示

### 關鍵洞察

1. **Civitai 是這個生態的「GitHub」** — 就像 GitHub 不只是 code hosting 而是整個開發者生態的核心（code + issue + PR + CI/CD + community），Civitai 把 model + prompt + image + parameters 整合成一個完整的可復現創作生態。800 萬+ prompts 的規模加上每張圖的完整參數記錄，形成了 AI 藝術界最大的「可復現知識庫」。其他平台只做了其中一兩環。

2. **「以圖搜 prompt」是下一代 prompt 工具的方向** — Lexica 的以圖搜圖能力解決了最根本的問題：使用者知道「想要什麼感覺」但不知道「怎麼用文字描述」。這暗示未來的 prompt 工具應該是 multimodal 的 — 不只是文字搜尋，而是圖片、風格、甚至草圖都可以作為 prompt 的輸入。

3. **SFW 和 NSFW 生態其實高度重疊** — Civitai 同時覆蓋兩個市場，技術棧（SD / Flux / LoRA）完全相同，差別只在內容政策。Promptchan 和 SoulGen 等 NSFW 專用平台的存在，反映的是主流平台審查壓力下的市場真空，而非技術差異。

4. **Prompt Gallery 的演化路徑：文字 → 預覽 → 參數 → 生圖 → 社群** — 早期的 prompt 庫只有文字清單（The Prompt Index），進化到附帶預覽圖（PromptHero），再到完整參數記錄（Civitai），最終整合線上生圖和社群功能。每一步都增加了從「知道 prompt」到「產出作品」的轉換率。Uniform Map 的正交分類 + 視覺預覽處於這條路徑的中段。

5. **角色一致性（Character Consistency）是下一個戰場** — SoulGen 的核心賣點是跨圖/跨影片保持同一角色的臉和特徵。這在商業應用（品牌角色、虛擬偶像、遊戲美術）中極其重要，目前能做好的平台很少，誰先解決這個問題誰就佔據高地。

### 與其他專案的關聯

- **Uniform Map AI Prompts**（`uniform-map-prompts.md`）：本筆記將 Uniform Map 放入整個 AI Prompt Gallery 生態中定位 — 它屬於「細分市場 + 正交分類」的獨特利基，在 Civitai 和 PromptHero 的通用大平台夾縫中找到了制服/動漫的垂直市場。
- **Claude Financial Services Plugins**（`claude-financial-services-plugins.md`）：金融 Plugin 用 Skill-as-Markdown 編碼領域知識，Prompt Gallery 用「prompt + 視覺預覽 + 參數」編碼創作知識。兩者都是「結構化領域知識的分發平台」，只是一個服務金融分析師，一個服務 AI 創作者。
- **LobeHub**（`lobehub.md`）：LobeHub 的 MCP 市集（39K+ servers）是 Agent 工具生態，Civitai 的模型市集（數十萬模型）是 AI 藝術模型生態。兩者的共同模式：平台 + 市集 + 社群 = 網路效應飛輪。
