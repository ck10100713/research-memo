---
date: "2026-10-23"
category: "AI 創作資源"
card_icon: "material-palette"
oneliner: "ArtCraft 團隊(前身是 FakeYou / vo.codes 語音生成)的 GitHub org:主力產品 ArtCraft 是「給藝術家的 IDE」,在 2D/3D 場景裡組好構圖再丟給 62 個圖像/影片/3D 模型生成;2026-09-30 起又用 AI agent 大量產出一整套純 Rust 的 clean-room 辦公/創作軟體(PhotoCraft 對標 Photoshop、WordCraft 對標 Word 等 13 個 app),PhotoCraft 三週 7.1 萬星、66 萬行 Rust、每個動作都能透過 CLI / JSON / MCP 讓 agent 操作"
tags:
  - image-generation
  - video-generation
  - rust
  - mcp
  - ai-coding
---

# storytold(ArtCraft)研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub org | <https://github.com/storytold>(顯示名稱 ArtCraft,68 個 public repo) |
| 官網 | <https://getartcraft.com> |
| 主力 repo | [artcraft](https://github.com/storytold/artcraft)、[photocraft](https://github.com/storytold/photocraft) |
| 共用層 | [craft-libs](https://github.com/storytold/craft-libs)、[craft-ai-integrations](https://github.com/storytold/craft-ai-integrations)、[craft-launcher](https://github.com/storytold/craft-launcher) |
| 第三方報導 | [AI Weekly](https://aiweekly.co/alerts/photocraft-ships-rust-photoshop-clone-with-mcp-agent-server)、[ecosistemastartup](https://ecosistemastartup.com/?p=115272) |

數字都是 2026-10-23 從 GitHub API 和 README 抓的,這個 org 每天都在變,過幾天就會過時。

## 一句話

一間做 AI 創作工具的新創,同時在做兩件事:**ArtCraft**(把 AI 生圖/生影片包成有 3D 場景、構圖工具的桌面 app),以及 **Crafting Apps**(用 AI agent 從零重寫 Photoshop、Word、Excel、Premiere 等十幾套軟體,全部純 Rust、開源、可被 agent 操控)。

## 團隊背景

org 2021 年建立,舊 repo 透露出前身:

- `redirect-vocodes`:「Netlify redirect vo.codes → fakeyou.com」,也就是當年的名人語音 TTS 網站 FakeYou
- `storyteller-ml`(Tacotron)、`vits-finetuning`、`realtime-voice-conversion`:語音模型
- `HyperJail`、`cloudcam`、`LiveScan3D` fork、一堆 Unreal Engine plugin:VTuber / 即時動捕實驗
- PhotoCraft 的 Flatpak ID 還是 `ai.storyteller.photocraft`

路線是 語音生成 → 虛擬人/3D → AI 影像創作 IDE → 整套創作軟體。commit 裡發 release 的是 Brandon Thomas,contributor 帳號 `echelon` 看起來是同一人,但我沒有找到明確對應,這點不確定。

## ArtCraft:給藝術家的 AI IDE

- repo 2022 年建立,3.5 萬星,Rust(桌面 app 加上 `frontend/` 前端),MIT/Apache-2.0 雙授權
- 核心想法:**先搭場景再生成**。在 2D 畫布或 3D 場景裡擺角色、姿勢、相機、道具,把這些當成控制條件丟給模型,比純打 prompt 更能重現同一個角色、同一個房間
- 功能:Image to Location(同一場景多鏡頭)、2D/3D 合成、圖轉 3D mesh、角色擺姿、kitbash 場景、角色身份轉移、去背、inpainting、圖轉影片
- 模型:自家「ArtCraft」供應商轉接 62 個模型,另外可接你自己的 Grok、Midjourney、Sora、World Labs 帳號

| 類別 | 數量 | 代表 |
|------|------|------|
| 圖像 | 16 | Nano Banana Pro、GPT Image 2.x、FLUX、Seedream 5 |
| 影片 | 25 | Seedance 2.0、Kling、Veo 3.1、Sora 2、Vidu Q3、MiniMax H3 |
| 音樂/音效 | 5 | Suno、Seed Audio |
| 3D mesh | 11 | Hunyuan 3D 3.1、Tripo、Meshy、Rodin |
| 世界/Gaussian splat | 5 | Marble(World Labs)、TripoSplat |

商業模式看起來是:app 開源免費,生成走他們的雲端點數(`artcraft-services` 是後端)。

## Crafting Apps:用 agent 重寫整套軟體

2026-09-30 一口氣開了 photocraft、pdfcraft、filmcraft,之後每隔幾天多一個:

| App | 對標 | 星數 |
|-----|------|------|
| PhotoCraft | Photoshop | 71,429 |
| PdfCraft | Acrobat | 17,240 |
| FilmCraft | 非線性剪輯 | 15,763 |
| WordCraft | Word | 15,559 |
| LightCraft | Lightroom | 14,341 |
| VectorCraft | Illustrator | 10,452 |
| EffectCraft | After Effects | 7,705 |
| CADCraft | AutoCAD | 6,477 |
| GridCraft | Excel | 6,264 |
| DesignCraft | InDesign | 4,674 |
| DeckCraft | PowerPoint | 4,131 |
| SoundCraft | Pro Tools | 3,585 |
| FigCraft | Figma | 3,157 |
| AniCraft | 2D 動畫 | 剛開 |

共同原則(寫在各 repo 的 `AGENTS.md`):

- **純 Rust**,UI 用 egui + wgpu,不准 Electron / Tauri / webview;同一份程式碼編成 WebAssembly 就是網頁版
- **Clean-room**:只看公開規格和觀察到的行為,不碰對方原始碼
- **Never crash 優先於功能**:非測試碼禁止 `unwrap`/`expect`/`panic!`,`unsafe` 全面 forbid,來自檔案的數字一律當敵意輸入
- **每個動作都是 command**,UI、CLI、JSON control channel、MCP server 共用同一個 registry

### PhotoCraft 細看

- 3 週:5,301 個 commit、66 萬行 Rust、24 個 crate、1,700+ 測試、issue+PR 編號已到 #8760
- 最近 100 個 commit 有 16 個帶 `Co-Authored-By: Claude Opus 5.5`,ROADMAP 的剩餘工時直接用「**Opus 5.5 agent-hours**」估(到 ~95% 完成度還要 2,300–4,100 小時)
- 自評:選單 628/628、工具 56/68、面板 30/35,「功能廣度 ~76%」「可實際工作 ~45%」,README 自己講 **還不能取代 Photoshop 做日常專業工作**,缺口是 AI 生成功能、部分工具、排版深度、plug-in 相容
- PSD:獨立 crate 依 Adobe 公開規格實作,psd-tools 測試集 309 個檔重存後 307 個渲染一致
- 架構分層用 `cargo xtask layers` 在 build 時強制檢查;CPU compositor 當 oracle,wgpu compositor 跟它對測
- Agent 介面:

```sh
photocraft-cli run wave.psd \
  --cmd filter.sharpen.smartSharpen --params '{"amount":80}' \
  --out wave-final.png
photocraft-cli batch --actions grade.json --in ./raw --out ./graded
photocraft-cli mcp      # 給 agent 用的 MCP server
photocraft --control    # 本機 loopback、有認證的 JSON 控制通道
```

README 裡每張截圖都是透過 control channel 離屏渲染出來的,等於 agent 自己幫自己拍文件截圖。

### 共用層

- **craft-libs**:跨 app 共用的 crate,ICC 色彩管理(`craft-cms`)、PDF、MP4/MKV 容器、列印、原子寫檔、設定檔、i18n、egui UI 元件
- **craft-ai-integrations**:「一次設定、所有 app 共用」的 AI 連線層。provider 有 OpenAI 相容、BFL FLUX、Vertex Gemini、Seedance、ComfyUI、SAM 3,本機推論引擎有 Candle / rten / burn;API key 存 OS keychain,有 consent 流程。目前標註是 first draft
- **craft-launcher**:類似 Adobe Creative Cloud 的安裝器,抓各 app 的 GitHub release、驗 SHA-256、自動更新

## 怎麼使用

以下整理自 2026-10-27 的 README 和 Release 頁,沒有實際安裝驗證。

### ArtCraft

**安裝**

- 一般人從 <https://getartcraft.com> 下載,有 Windows 和 macOS 版
- GitHub [Releases](https://github.com/storytold/artcraft/releases) 有最新版(v0.41.0,2026-09-26):`ArtCraft_0.41.0_universal.dmg`、`.msi`、`-setup.exe`
- Linux 沒有現成安裝檔,要照 `_docs/dev_setup.md` 自己 build

**流程**(先搭場景再生成)

1. 開 2D 畫布或 3D 場景,擺背景、道具、角色;素材可以先用「圖轉 3D mesh」或「去背」做出來
2. 調角色姿勢和相機;要固定同一個角色,就先擺木頭人,再用 Character Identity Transfer 把角色套上去
3. 選模型生成,圖、影片、音樂、3D、Gaussian splat 都在同一個介面

**費用**

- 選「ArtCraft」provider 就是走他們的雲端,應該是點數制,但 README 沒寫價格,要登入才知道
- 已經有 Grok、Midjourney、Sora、World Labs 帳號的,可以直接接自己的帳號

### Craft Apps(PhotoCraft 等)

**安裝**

- 最省事是先裝 [ArtCraft Launcher](https://github.com/storytold/craft-launcher/releases/latest)(v0.8.1),13 個 app 一鍵安裝、自動更新,下載後會驗 SHA-256
- 只要 PhotoCraft:從 <https://getartcraft.com/apps/photocraft> 下載,或在 GitHub Release 抓 `photocraft-<ver>-macos-universal.dmg`(v0.16.0,2026-10-25)。Mac 版有簽章和 notarize;Windows 有 x64/arm64/x86 的 msi 和免安裝 zip;Linux 有 AppImage、Flatpak、deb、rpm

**操作**

- 照 Photoshop 的習慣用,選單和快捷鍵(⌘J、⇧⌘D)刻意做成一樣,⌘F 開 command palette
- 能開 PSD/PSB、分層 TIFF、Krita、GIMP、OpenRaster、Paint.NET;Affinity 和 iPhone HEIC 唯讀

**給 agent / 腳本用**:另外下載 `photocraft-cli-<ver>-macos-universal.zip`

```sh
photocraft-cli run wave.psd --cmd filter.sharpen.smartSharpen --params '{"amount":80}' --out out.png
photocraft-cli batch --actions grade.json --in ./raw --out ./graded   # 批次處理
photocraft-cli mcp        # 當 MCP server 掛進 Claude Code
```

**從原始碼跑**:`cargo run --release -p photocraft -- image.psd`;要日文字型就另外 clone `craft-fonts` 並設 `CRAFT_FONTS_DIR`。

### 怎麼選

- 做 AI 影像創作用 ArtCraft,比較成熟
- PhotoCraft 自評「可實際工作 ~45%」,比較適合試 CLI + MCP 的批次修圖,正式工作先別拿來取代 Photoshop

## 值得注意的地方

1. **這是「agent 大量寫軟體」目前最誇張的公開案例之一**。三週 66 萬行、以 agent-hours 規劃 roadmap、AGENTS.md 寫得比給人看的文件還細(parity 清單、scorecard、gap 排序都是給 agent 挑工作用的)。想研究大型 agent 開發流程的,`photocraft/AGENTS.md` 和 `docs/target-app-parity.md` 很值得看
2. **星數成長快到要打個問號**。PhotoCraft 10/8 約 2.37 萬星(第三方報導),10/23 到 7.1 萬;stargazer API 對這麼大的 repo 我這邊拿不到,沒辦法檢查是不是有灌星。不過 8 千多個 issue/PR 和一堆外部 contributor 是真的活動
3. **品質要自己驗**。自評 45% 可用、alpha 階段,13 個 app 同時開工,大部分應該還很早期。拿來當「agent 能把 clean-room 重寫推到哪」的觀察對象比較合適,先別拿來取代正式工具
4. **授權乾淨**:MIT/Apache-2.0 雙授權,但 ArtCraft 名稱和 logo 不在授權範圍內

## 跟其他筆記的關係

- 跟 [Wan2GP](wan2gp.md) 互補:Wan2GP 是本機跑開源模型,ArtCraft 偏向串商用雲端模型、重點在構圖控制
- 「每個動作都是 command + MCP」的設計,跟這個 repo 裡收的各種 agent-ready 工具思路一樣
