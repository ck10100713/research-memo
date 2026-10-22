---
date: "2026-10-22"
category: "AI 應用"
card_icon: "material-movie-open-play"
oneliner: "DeepBeepMeep 一人主導的「GPU 窮人」本機生成超級 app:從 Wan2.1 fork 起家,現在一個 Gradio 介面塞進 Wan 2.1/2.2、LTX-2.x、Hunyuan Video、MiniMax H3、Flux、Qwen Image、TTS、音樂、3D 等 277 個模型定義;靠自家 mmgp 做分塊 offload、量化與 VRAM 配置,部分模型 6 GB VRAM 就能跑。內建 Python API + MCP server + 官方 agent skill,Claude Code / Codex 可以直接當遙控器。授權從 Apache-2.0 一路改成自訂的 WanGP Community License 2.0"
tags:
  - video-generation
  - image-generation
  - self-hosted
  - mcp
---

# Wan2GP(WanGP)研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo(已改名 WanGP,舊網址會轉址) | <https://github.com/deepbeepmeep/WanGP> |
| 作者 | **DeepBeepMeep**(GitHub [deepbeepmeep](https://github.com/deepbeepmeep),X [@deepbeepmeep](https://x.com/deepbeepmeep);使用者原本拼成 "leepbeepmeep") |
| 官方網站 | <https://wangp.ai/>(README 另認可 wan2gp.ai) |
| Discord | <https://discord.gg/g7efUW9jGV> |
| 授權全文 | [LICENSE.txt](https://github.com/deepbeepmeep/WanGP/blob/main/LICENSE.txt)(WanGP Community License 2.0) |
| 官方文件 | repo 內 [`docs/`](https://github.com/deepbeepmeep/WanGP/tree/main/docs):INSTALLATION / CLI / API / LORAS / DEEPY / REMOTE_LLMS / CHANGELOG 等 25 份 |
| 記憶體管理函式庫 mmgp | <https://github.com/deepbeepmeep/mmgp> · PyPI <https://pypi.org/project/mmgp/> |
| 上游模型 | [Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1)(17.3k★,Apache-2.0)· [Wan-Video/Wan2.2](https://github.com/Wan-Video/Wan2.2)(18.1k★,Apache-2.0)· [HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo) · [LTX-2](https://github.com/Lightricks/LTX-2) |
| 雲端對照 | [OpenRouter Wan 2.7](https://openrouter.ai/alibaba/wan-2.7) · [OpenRouter Video API 文件](https://openrouter.ai/docs/features/multimodal/video-generation) · [fal.ai Wan 2.2 微調指南](https://fal.ai/learn/devs/how-to-fine-tune-wan-with-the-api) |
| 研究方法 | `gh api` 抓 metadata + `git clone --depth 50` 讀原始碼與 docs(未執行任何程式碼) |

> Metadata(**2026-10-22** 即時抓取,GitHub API + clone):**10,900 stars / 1,749 forks / 1,308 open issues(含 PR)/ 116 watchers** · GitHub 判讀授權為 `NOASSERTION`(實為自訂 **WanGP Community License 2.0**)· 建立於 **2025-02-27**(GitHub 上標記為 `Wan-Video/Wan2.1` 的 fork),最後 push **2026-10-22** · **1,871 commits / 31 位具名貢獻者**(deepbeepmeep 1,416、Tophness 311、0xDELUXA 34)· **沒有 GitHub Release 也沒有 tag**,版本只寫在 README / CHANGELOG,最新 **v18.21(2026-10-21)** · repo ≈ 101 MB,主語言 Python。

!!! warning "先校正幾個常見誤解"
    - **Wan 是模型,Wan2GP 是跑模型的本機外殼**:Wan 2.1/2.2 是阿里巴巴 Wan-Video 團隊開源的影片模型(Apache-2.0);Wan2GP 不訓練模型,它做的是低 VRAM 推論、UI、佇列、外掛和 agent 介面。名字裡的 "GP" = **GPU Poor**。
    - **它早就不只是 Wan**:repo 已改名 **WanGP**,README 自稱 "one-stop super app",`defaults/` 有 **277 個模型定義 JSON、約 161 種 architecture**,涵蓋影片、圖片、TTS、音樂、3D。把它當「Wan 專用工具」會低估它。
    - **它不是 Apache-2.0 也不是 OSI 開源**:最早(2025-02)繼承 Wan 的 Apache-2.0,2025-08-07 改成「Non-Commercial Evaluation License 1.0」,2026-04-05 再改成 **WanGP Community License 2.0**。現行條款:本機免費用(公司內也可)、輸出可以賣;但**不准賣 WanGP 本身、包進付費產品、提供付費 API/SaaS/託管**,要另簽商業授權。第三方模型權重另依各自授權。
    - **「6 GB VRAM 就能跑」只對部分模型成立**:README 原話是 "run select models with as little as 6 GB"。14B 等級的 Wan 官方建議 12 GB 以上,而且系統 RAM 也要夠(mmgp 是用 RAM 換 VRAM)。目前沒找到獨立第三方的系統性 benchmark,速度/VRAM 數字都是作者自報。
    - **Claude 本身不會生影片**:網路上說「用 Claude Code 生影片」,實際上是 Claude 當指揮,透過 MCP 或 Python API 叫本機的 WanGP(或雲端 API、Remotion 等工具)去產生。詳見下方「用 Claude Code 驅動 Wan2GP」。

## 專案概述

**WanGP**(原名 Wan2GP / Wan2.1GP)是 DeepBeepMeep 做的本機 AI 生成 app,口號是 "The best Open Source Generative Models Accessible to the GPU Poor"。2025-02-25 阿里開源 Wan2.1,兩天後作者就 fork 出來,2025-03-02 發布 "Wan2.1GP v1",主打記憶體用量砍半、RTX 4090 能生 720p 超過 10 秒、12 GB 以下能生 480p 10 秒([CHANGELOG](https://github.com/deepbeepmeep/WanGP/blob/main/docs/CHANGELOG.md))。

之後它一路把新出的開源模型吞進來:Hunyuan Video、LTX Video、Flux、Qwen Image、VACE、MultiTalk/InfiniteTalk、LTX-2.x、MiniMax H3、各家 TTS 與音樂模型,2026-10 的 v18.00 還加了 3D 生成(Hunyuan3D 2.1、TRELLIS.2 等)。20 個月從 v1 走到 v18.21,幾乎每週都有新版。

它的定位很清楚:ComfyUI 是給想自己接 node 的人,WanGP 是「選模型、打 prompt、按生成」的一體化 Gradio 介面,背後把記憶體管理、量化格式、加速 kernel 全包掉。有中文社群作者評論它「對大多數人比 ComfyUI 合適,但易用性還是有些問題」([cnb.cool 鏡像頁](https://cnb.cool/huyuefeitool/Wan2GP),屬第三方意見)。

## 核心功能

### 支援模型(依 README Highlights 與 `defaults/`、`models/` 目錄交叉確認)

| 類型 | 模型(節錄) | 備註 |
|------|------------|------|
| 影片 | **Wan 2.1 / 2.2** 及衍生(VACE、Animate、MultiTalk、InfiniteTalk、Fun Camera、SkyReels DF、Phantom、Lynx…)、**MiniMax H3**、**LTX-2 / 2.3 / 2.5**、**Hunyuan Video 1 / 1.5**、LongCat、Kandinsky 5/6、LTXV、MagiHuman | Wan 只有 2.1/2.2(開源權重);**WanGP 裡找不到 Wan 2.5 以後的定義** |
| 圖片 | Krea 2、Qwen Image、Z-Image、Flux 1/2/3(Klein、Kontext、Chroma)、SenseNova、Ideogram 4、HiDream、Fibo 2、MOSS Image | |
| 音訊 / TTS | Qwen3 TTS、Index TTS 2/2.5、Chatterbox、Ace Step 1/1.5/XL、Stable Audio 3、Fish Audio Drama 3、MOSS-TTS、YuE2、HeartMula、KugelAudio | YuE 從獨立的 YuEGP 併進來 |
| 3D | Hunyuan3D 2.1、TRELLIS.2、TripoSG、TripoSplat、WorldMirror 2.0、MoGe-2 等 | v18.00(2026-10-11)新增 |
| 前/後處理 | DWPose、Depth Anything v2/v3、SAM3、MatAnyone、rembg;RIFE、FlashVSR、SeedVR2、MMAudio、SeedVC、DLSS 5 | `preprocessing/`、`postprocessing/` |

`docs/OVERVIEW.md` 有作者的精選推薦,例如影片編輯用 Wan 2.1 VACE、動作轉移用 Wan 2.2 Animate、對嘴用 InfiniteTalk、帶聲音的電影感影片用 LTX-2.5 Distilled 或 H3。

### 低 VRAM 怎麼做到的

核心是作者自己寫的 **mmgp**(Memory Management for the GPU Poor),v17.17 起直接放進 WanGP repo 的 `mmgp/` 目錄(`offload.py` 就有 6,311 行)。概念是:模型平常放在系統 RAM,GPU 算到哪層才把那一塊搬上去,用 RAM 和 PCIe 頻寬換 VRAM。

```
          系統 RAM(Reserved / pinned)                       GPU VRAM
 ┌──────────────────────────────────┐              ┌──────────────────────┐
 │ transformer blocks [0..N]        │  async copy  │ 固定 VRAM slot(預算) │
 │ text encoder / VAE / LoRA 權重   │ ───────────▶ │  block k 計算中       │
 │ (on-the-fly int8 量化或預量化檔) │   預取 k+1   │  block k+1 傳輸中     │
 └──────────────────────────────────┘              │ + 動態 preload 常駐塊 │
                                                    │ + 剩下給 latent/影格  │
                                                    └──────────────────────┘
   LoRA 在 forward 時即時套用(不 merge),量化模型也能用、每步可換強度
```

| 技術 | 做法 | 來源 |
|------|------|------|
| Block swapping | 模型大於 VRAM 預算時分塊處理,依第一步學到的順序預取下一塊 | [mmgp/README.md](https://github.com/deepbeepmeep/WanGP/blob/main/mmgp/README.md) |
| Reserved(pinned)RAM | 鎖頁記憶體讓 RAM→VRAM 傳輸快到 2 倍,依優先度分給各模型 | 同上 |
| 量化 | int8(quanto)、fp8、GGUF、NV FP4、Nunchaku、INT8 ConvRot;依顯卡架構自動下載對應檔 | README、[INSTALLATION.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/INSTALLATION.md) |
| 自訂 VRAM allocator | 取代 PyTorch allocator,長影片/大圖峰值少好幾 GB | mmgp README、v17.17 公告 |
| 加速 kernel | SageAttention 1/2、Sparge、Flash Attention、Triton、自家 [WGPKernels](https://github.com/deepbeepmeep/WGPKernels)(INT8)與 [kernels](https://github.com/deepbeepmeep/kernels)(GGUF CUDA) | INSTALLATION.md |
| 自家重寫 VAE | v18.00 起 LTX-2 VAE 快 3 倍;Wan 2.1 VAE 1080p 解碼從 28 s / 10.5 GB 降到 11 s / 4.7 GB(作者自報) | README v18.00 |

作者自報的代表數字:v17.17(mmgp v4)讓 MiniMax H3 生 15 秒 1080p 從 25 GB VRAM 降到 11 GB,480p 只要 5–6 GB。

### 記憶體 Profile(VRAM 分級)

CLI 用 `--profile 0-5`,預設 4([docs/CLI.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/CLI.md)):

| Profile | 策略 | 適合 |
|---------|------|------|
| 0(實驗) | 執行中的模型才拿 Reserved RAM,跑完讓給下一個 | RAM 少、常切模型 |
| 1 | 模型整個進 VRAM、全部放 Reserved RAM | 最快,RAM/VRAM 都要多 |
| 2 | 全放 Reserved RAM、分塊送 GPU | RAM 多、VRAM 普通 |
| 3 / 3+ | 整個進 VRAM、只有主模型佔 Reserved RAM;3+ 適合音訊模型 | VRAM 夠放整個模型 |
| **4(推薦)/ 4+** | 只有主模型佔 Reserved RAM、分塊送 GPU;4+ 一次送一塊再省 ~1 GB | 最通用 |
| 5(保底) | 幾乎不用 Reserved RAM | RAM、VRAM 都不夠時 |

[GETTING_STARTED.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/GETTING_STARTED.md) 的粗略建議:6–8 GB 用 1.3B 模型;10–12 GB 用 14B 或 Hunyuan;16 GB 以上什麼都能跑、可生更長影片。硬體支援 GTX 10XX 到 RTX 50XX,以及 AMD RDNA 2/3/3.5/4(另有 [AMD 安裝文件](https://github.com/deepbeepmeep/WanGP/blob/main/docs/AMD-INSTALLATION.md))。

### LoRA 與 Finetune

- LoRA 依模型家族放 `loras/wan/`、`loras/wan_i2v/`、`loras/ltx2/`、`loras/flux/`、`loras/qwen/` 等;可用 `--lora-config lora_paths.json` 指到別的磁碟或直接重用其他 app 的 LoRA 收藏([LORAS.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/LORAS.md))。
- mmgp 支援 LoRA、DoRA、LoKr,執行時套用不 merge,倍率可以每個 denoising step 不同(加速 LoRA 常用這招)。
- `finetunes/` 放自訂模型 JSON,可以加 Hugging Face / CivitAI 上找到的 checkpoint([FINETUNES.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/FINETUNES.md));社群有 Finetune Manager、CivitAI 瀏覽器等外掛。

### 程式架構

```
WanGP/
├── wgp.py              # 14,778 行的主程式:Gradio UI + 佇列 + CLI 入口
├── models/             # 33 個模型家族實作(wan/ ltx2/ hyvideo/ flux/ qwen/ minimax_h3/ TTS/ hunyuan3d/ …)
├── defaults/           # 277 個模型定義 JSON(architecture、下載 URL、預設參數)
├── finetunes/          # 使用者自訂模型 JSON
├── profiles/           # 各模型的設定預設(加速 LoRA 組合等)
├── mmgp/               # 內建的記憶體管理函式庫 v4
├── shared/             # api.py、mcp/、deepy/、attention、kernels、llm_engines、remote_llm…
├── preprocessing/      # pose / depth / mask / 人聲分離…
├── postprocessing/     # 超解析、插幀、配樂、換聲…
├── plugins/ + plugins.json   # 內建外掛 + 社群外掛登錄表
├── wangp-agent/SKILL.md      # 官方 agent skill(含 agents/openai.yaml 給 Codex)
└── docs/               # 25 份文件
```

主要相依(`requirements.txt`):`gradio==5.29.0`、`diffusers==0.36.0`、`transformers==4.54.0`、`optimum-quanto==0.2.7`、`gguf`、`mcp==1.30.0`,另外一堆影音/視覺套件。

### 內建 agent:Deepy

v11.13(2026-03-30)加入 **Deepy**,一個跑在本機的低 VRAM agent(用 Qwen3.5VL 系列),可以排生成任務、轉錄、切影片、做遮罩、加字幕;進階版 **Deepy Prime** 可以吃一分鐘的 brief 自動規劃分鏡、維持角色一致、配音樂,再自己檢查黑畫面和錯字(v18.19 公告)。Deepy Prime 也可以改用 **Codex、Claude Code 或 OpenCode** 當大腦,詳見下一節。

## 用 Claude Code 驅動 Wan2GP

先講結論:**Claude 不會自己生影片**。它能做的是當指揮,呼叫一個真的會生影片的工具。「用 Claude Code 生影片」在網路上至少有三種意思,這裡逐一核對:

### (a)WanGP 官方就有 agent 介面(真的,而且是第一方)

| 介面 | 怎麼啟動 | 來源 |
|------|---------|------|
| **MCP server(headless)** | `python wgp.py --mcp --mcp-transport stdio`,或 `--mcp-transport streamable-http --mcp-port 7866` | [docs/API.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/API.md) |
| **MCP 掛在 Web UI 上** | `python wgp.py --mcp-webui`,預設 `http://127.0.0.1:8000/mcp`,跟你正在用的 UI 共用佇列和 gallery | 同上 |
| **Python API** | `from shared.api import init; session = init()`,2026-03-17(v10.9875)公告 | API.md、CHANGELOG |
| **CLI 批次** | 在 UI 存佇列,`python wgp.py --process my_queue.zip` | [docs/CLI.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/CLI.md) |
| **官方 skill** | [`wangp-agent/SKILL.md`](https://github.com/deepbeepmeep/WanGP/blob/main/wangp-agent/SKILL.md):教 agent「先 MCP、其次 Python API、CLI 只當備案」 | repo 內 |

MCP API v2.1 的工具包括 `wangp_models`(找模型)、`wangp_model`(看 schema / 預設值)、`wangp_list_loras`、`wangp_generate`、`wangp_postprocess`、`wangp_toolbox`(抽影格、轉錄、合併影片…)、`wangp_io`(檔案)。v2.1 還能讓外部 agent 直接收到影格圖片自己看結果。

所以 Claude Code 的典型用法是:

```bash
# 1) 在有 GPU 的機器上起 WanGP MCP(HTTP)
python wgp.py --mcp-webui
# 2) 在 Claude Code 註冊這個 MCP server
claude mcp add --transport http wangp http://127.0.0.1:8000/mcp
# 3) 對 Claude 說「用 Wan 2.2 i2v 把這張圖做成 5 秒影片」
#    Claude → wangp_models → wangp_model(defaults) → wangp_generate → 回傳檔案路徑
```

(第 2 步是 Claude Code 通用的 `claude mcp add` 寫法,WanGP 文件沒有專門寫 Claude Code 的設定範例,這裡是依 MCP 標準推出來的,未實測。)

**反方向也有**:WanGP 可以把 Claude Code 當 Deepy Prime 和 Prompt Enhancer 的 LLM 引擎。要在 WanGP 的 Python 環境裝 `claude-agent-sdk==0.1.66`,再 `claude auth login --claudeai`([docs/REMOTE_LLMS.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/REMOTE_LLMS.md))。好處是 LLM 不佔本機 VRAM;代價是 prompt 和取樣影格會送到雲端。

安全提醒(官方文件原文重點):所有連上的 agent 共用一個佇列、可以互相取消任務;MCP 位址請留在 localhost 或開 MCP OAuth,`--auth` 只保護網頁不保護 MCP。

### (b)第三方 MCP / skill 包裝(有,但都很小)

| Repo | 做法 | 規模 |
|------|------|------|
| [PrimeEcto/Wan2AI](https://github.com/PrimeEcto/Wan2AI) | Agent Skills 規格的 skill,宣稱支援 Claude Code / Codex / Cursor / Gemini CLI,偵測 VRAM 選模型 | 1★ |
| [reverb256/wan2gp-mcp-server](https://github.com/reverb256/wan2gp-mcp-server) | stdio MCP,打 WanGP 的 Gradio HTTP(7860) | 1★ |
| [Franzferdinan51/wan2gp-mcp](https://github.com/Franzferdinan51/wan2gp-mcp) | 專攻 MiniMax H3 的 MCP,14 個工具,可推到 Telegram | 0★ |
| [magicmars35/wan2gp_agentic_skill](https://github.com/magicmars35/wan2gp_agentic_skill) | Linux agent 經 FastAPI 叫區網內的 Windows WanGP | 4★ |
| [BrentCrude79/WanGP-Launcher](https://github.com/BrentCrude79/WanGP-Launcher) | Windows 系統匣啟動器,閒置就關掉 WanGP / MCP | 0★ |

這些大多是官方 MCP 出來前或平行時期的產物,星數都個位數,品質未驗證。現在官方 MCP + SKILL.md 已經涵蓋主要用途,**優先用官方的**。

### (c)常被混為一談的其他做法

- **Claude Code + Remotion**:Claude 寫 React/TypeScript,Remotion 渲染成 MP4。這是程式化動態圖像(字卡、資料視覺化),沒有生成式影片模型參與([OpenReplay 教學](https://blog.openreplay.com/making-videos-claude-code-remotion/)、[Blotato](https://www.blotato.com/blog/make-ai-videos-with-claude-code))。
- **Claude Code + ffmpeg / CapCut 自動化**:剪輯拼接,例如本站 [video-autopilot-kit](video-autopilot-kit.md)。
- **Claude Code 呼叫雲端影片 API**:OpenRouter、fal.ai 等,見下表。

### 本機 Wan2GP vs 雲端 Wan API

要分清楚:**Wan 是模型,Wan2GP 是在你自己 GPU 上跑開源 Wan 權重的本機外殼**。OpenRouter / fal 這類雲端服務是在他們的機器上跑模型,**OpenRouter 不能跑 Wan2GP**,它提供的是 Alibaba 的託管模型 API。

| 項目 | 本機 Wan2GP | 雲端 API(OpenRouter / fal.ai 等) |
|------|-------------|-----------------------------------|
| 能用的 Wan 版本 | 只有開源權重:**Wan 2.1 / 2.2** 及衍生 | OpenRouter 有 **Wan 2.6 / 2.7 / 3.0**(Alibaba 託管);fal 有 Wan 2.2 |
| 費用 | 軟體免費(本機使用),成本是顯卡、電費、時間 | OpenRouter Wan 2.7 **US$0.10/秒**(5 秒 ≈ $0.50);Wan 3.0 720p $0.10/秒、1080p $0.20/秒([`/api/v1/videos/models`](https://openrouter.ai/api/v1/videos/models) 即時查詢);fal 指南寫 Wan 2.2 A14B $0.1/秒 |
| VRAM 需求 | 部分模型 6 GB 起,14B 建議 12 GB+,另需大量系統 RAM | 不需要本機 GPU |
| Agent 怎麼呼叫 | MCP(stdio / HTTP)或 Python API,同步等結果或輪詢 | `POST /api/v1/videos` 拿 job ID → 輪詢 `GET /api/v1/videos/{id}` → 下載 `/content`;也可設 webhook([OpenRouter 文件](https://openrouter.ai/docs/features/multimodal/video-generation)) |
| LoRA | 完整支援,本機任意 LoRA / finetune | OpenRouter 的 Wan 2.7 參數裡沒有 LoRA 欄位;fal 有專門的 `.../text-to-video/lora` 端點,也能線上訓練(約 $0.004/step,依 fal 指南) |
| 隱私 / 審查 | 全在本機 | 素材上傳到供應商 |
| 規格限制 | 由模型和你的硬體決定(sliding window 可做長片) | OpenRouter Wan 2.7:720p/1080p、2–10 秒 |

雲端價格會變動,上面是 2026-10-22 查到的數字。

## 快速開始

| 方式 | 指令 / 說明 |
|------|-----------|
| 一鍵腳本(官方) | `scripts/install.bat` 或 `.sh` 安裝(自動挑 Triton/Sage/Flash/GGUF/Nunchaku kernel),`scripts/run.*` 啟動,`scripts/update.*` 更新 |
| Pinokio | README **建議用社群 Morpheus 的 `wan2gp` / `wan2gp-amd` 腳本**,而非 Pinokio 官方版 |
| Wan2GP Desktop | 社群 [GKartist75/Wan2GP-Desktop-Tauri](https://github.com/GKartist75/Wan2GP-Desktop-Tauri),一個視窗搞定安裝與更新 |
| Docker | `./run-docker-cuda-deb.sh`(Debian 系;腳本寫的是 CUDA 12.4.1 + PyTorch 2.6,比手動安裝建議的版本舊) |

手動安裝(RTX 20XX–50XX):

```bash
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP
conda create -n wan2gp python=3.11.14
conda activate wan2gp
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
python wgp.py            # 開 Gradio UI
python wgp.py --profile 4 --attention sdpa   # 低 VRAM 範例
```

GTX 10XX 要改用 Python 3.10 + PyTorch 2.7.1;Windows 另外要依顯卡裝對應版本的 `triton-windows` 和 SageAttention(RTX 20XX 用 Sage 1.0.6,30XX 以上用 2.2.0)。省 VRAM 小撇步:用 `scripts/start-chrome-no-gpu.*` 開不吃 GPU 的瀏覽器,README 說可多出 1–5 GB。

## 實作:Windows + RTX 3060 Ti(8GB VRAM)+ 32GB RAM 手把手

這節照 repo 內的 [README](https://github.com/deepbeepmeep/WanGP/blob/main/README.md)、[INSTALLATION.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/INSTALLATION.md)、[GETTING_STARTED.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/GETTING_STARTED.md)、[CLI.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/CLI.md)、[TROUBLESHOOTING.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/TROUBLESHOOTING.md) 和 `setup_config.json` 寫(2026-10-22 的 v18.21)。3060 Ti 是 Ampere 架構,在 WanGP 裡算 **RTX 30XX** 這組,官方自動安裝會套用 `RTX_30` 組合:**Python 3.11.14 + PyTorch 2.10.0 / CUDA 13.0 + triton-windows 3.7 + SageAttention 2.2.0**。

> 只有 16GB RAM 的話差在一點:改用 `--profile 5`(或 `--perc-reserved-mem-max 0.3`),會比較慢但比較不會把 RAM 吃爆。

### 步驟 0:先檢查環境

```powershell
nvidia-smi                       # 看右上角 Driver Version 和 CUDA Version
git --version                    # 沒有的話 install.bat 會問要不要幫你裝
python --version                 # 一鍵安裝要 3.11 以上;沒有的話 install.bat 會問要不要裝
Get-PSDrive -PSProvider FileSystem   # 看要裝的那顆碟還剩多少空間
```

- **驅動**:WanGP 用 CUDA 13.0 版 PyTorch。NVIDIA 文件寫 CUDA 13.x 需要 **R580 以上**的驅動,而且從 13.0 開始 Windows 版 toolkit 不再附驅動,要自己去 NVIDIA 官網更新([CUDA 13.0 Release Notes](https://docs.nvidia.com/cuda/archive/13.0.0/cuda-toolkit-release-notes/))。`nvidia-smi` 右上角的 CUDA Version 要顯示 13.x 以上。
- **CUDA Toolkit**:INSTALLATION.md 的手動安裝寫「you must install Cuda 13.1」([下載頁](https://developer.nvidia.com/cuda-13-1-0-download-archive))。走一鍵安裝的話文件沒特別要求,不確定是否必要;遇到 Triton 編譯錯誤再補裝。
- **硬碟空間(估算)**:依 `defaults/*.json` 的下載網址查 Hugging Face 檔案大小:

| 要下載的東西 | 大小 |
|-------------|------|
| Wan2.1 T2V 1.3B 主模型 | 2.87 GB |
| Wan2.2 TI2V 5B 主模型(bf16 / int8 版) | 10.14 GB / 5.23 GB |
| umT5-XXL 文字編碼器(bf16 / int8 版) | 11.36 GB / 6.73 GB |
| VAE(Wan2.1 / Wan2.2) | 0.25–0.51 GB / 1.41–2.82 GB |
| Fun InP 1.3B(圖生影片) | 3.13 GB |

  實際下載哪個版本看設定,以上是範圍。加上 Python 環境和各種 kernel,**建議預留 60 GB 以上**(估算,未實測),放 SSD 載入會快很多。

- [ ] 完成確認:`nvidia-smi` 看得到 RTX 3060 Ti 和 CUDA 13.x、`git --version` 有輸出、目標磁碟剩 60 GB 以上。

### 步驟 1:安裝

有三條路,**推薦 1A 一鍵腳本**:它是 README 第一順位的官方方式,會自動判斷你的顯卡,把 Triton、Sage、Flash、GGUF、Nunchaku 這些 kernel 一次裝好,手動裝最容易出錯的就是這幾個。

**1A. 官方一鍵腳本(推薦)**

```powershell
cd D:\AI                         # 換成你要放的資料夾
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP
.\scripts\install.bat
```

選單選 `1. Automatic Install (1-Click)`,它會建一個 `venv` 環境並依 `RTX_30` 組合安裝。想自己選 uv / conda 或版本就選 `2. Manual Install`。

**1B. 官方手動安裝(conda)**

文件的手動安裝是用 conda(要先裝 [Miniconda](https://www.anaconda.com/download/success)),PowerShell 第一次用要先跑 `conda init powershell` 再重開視窗:

```powershell
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP
conda create -n wan2gp python=3.11.14
conda activate wan2gp
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
```

INSTALLATION.md 特別提醒**不要用 PyTorch 2.8.0**(切換模型時有 RAM 洩漏)和 **2.9.0**(3D 卷積效能問題,VAE 的 VRAM 會爆)。

**1C. Pinokio**

到 [pinokio.computer](https://pinokio.computer/) 裝好後,README 建議用社群作者 **Morpheus 的 `wan2gp` 腳本**,不要用 Pinokio 官方那個。GETTING_STARTED 也把 Pinokio 列為「最簡單」的選項。缺點是之後要照 Pinokio 的方式更新,出問題時比較難對照官方文件除錯。

- [ ] 完成確認:在 WanGP 環境裡跑下面這行,印出 `2.10.0+cu130 True NVIDIA GeForce RTX 3060 Ti`(或類似)。

```powershell
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

### 步驟 2:第一次啟動

走 1A 的話直接 `.\scripts\run.bat`;要加參數就在 `scripts\` 裡建一個 `args.txt`,一行寫參數。走 1B 的話:

```powershell
conda activate wan2gp
python wgp.py --profile 4 --attention sage2 --open-browser
```

瀏覽器開 `http://localhost:7860`。參數怎麼選:

| 參數 | 8GB VRAM + 32GB RAM 的建議 | 理由(出處) |
|------|--------------------------|-------------|
| `--profile 4` | **用這個**(也是預設值) | 只有主模型佔 Reserved RAM、分塊送 GPU,能跑比 VRAM 大的模型,官方標「recommended」(CLI.md) |
| `--profile 4.5`(4+) | VRAM 還是不夠時 | 一次只送一塊,約省 1 GB VRAM,稍慢 |
| `--profile 0` | 想試新功能可以試 | v18.21 新增的實驗模式,對低 RAM 機器切模型比較友善 |
| `--profile 2` | 不建議 | 要把所有模型放 Reserved RAM,mmgp README 建議 48 GB RAM 以上 |
| `--profile 3` | 不建議 | 要把整個模型放進 VRAM,8GB 放不下 14B |
| `--attention sage2` | 裝好 Sage 2 後用 | 文件說最多快 2 倍、品質損失很小;沒裝或出錯就改 `sdpa` |
| `--compile` | 先不要開 | 需要 Triton;社群回報(issue [#1956](https://github.com/deepbeepmeep/WanGP/issues/1956))compile 會多吃 VRAM,8GB 先求穩 |
| `--perc-reserved-mem-max` | 先不用設 | Windows 預設最多鎖 40% RAM 當 pinned memory(32GB ≈ 12.8GB) |

省 VRAM 小撇步:用 `.\scripts\start-chrome-no-gpu.bat` 開瀏覽器,README 說可以多擠出 1–5 GB VRAM(依顯卡不同)。Windows 上還可以用 `scripts\gpumem.cmd` 看哪些程式在佔 VRAM。

- [ ] 完成確認:終端機沒有紅字錯誤、瀏覽器打開看得到 WanGP 介面、左上角模型下拉選單能展開。

### 步驟 3:第一支影片(8GB 實際可行的配方)

GETTING_STARTED 對 6–8GB VRAM 的建議很直接:**用 1.3B 模型**。第一支照官方「Recommended First Settings」:

| 設定 | 值 |
|------|----|
| 模型 | **Wan2.1 Text2video 1.3B**(也可以用 `python wgp.py --t2v-1-3B` 直接開這個,參數已標為 deprecated 但還能用) |
| 解析度 | 832x480(Wan 1.3B 的標準 480p) |
| Frames | 49(Wan 2.1 是 16 fps,所以約 3 秒;GETTING_STARTED 寫「≈ 2 秒」,跟程式裡的 16 fps 對不上,以程式為準) |
| Steps | 20 |
| Prompt | `A cat walking in a garden`(官方範例) |

**時間預估**:官方文件和 issue 都沒有 3060 Ti 跑 1.3B 的數字,我也沒找到可信 benchmark。**粗估**第一次要先下載十幾 GB 模型(看網速,可能 10–30 分鐘),之後每支幾分鐘級,實際以你機器為準。

**進階第二支**:Wan2.2 TextImage2video **FastWan 5B**(`ti2v_2_2_fastwan`),預設只跑 **3 steps**、24 fps。它的預設是 1280x720、121 frames,8GB 上建議先把 frames 降到 49 左右再試。注意 issue [#2301](https://github.com/deepbeepmeep/WanGP/issues/2301) 有 6GB 卡(GTX 1660)跑 5B 出現黑畫面的回報,3060 Ti 是否會遇到未驗證。

**別一開始就挑大模型**:issue [#2109](https://github.com/deepbeepmeep/WanGP/issues/2109) 有人用同樣 8GB 的 RTX 3070 跑 MiniMax H3(INT8)生 5 秒 720p 要 **25–30 分鐘**(使用者回報),14B 的 Wan 和 LTX-2 22B 也會很吃時間。

- [ ] 完成確認:生成結束後下方 gallery 出現影片、可以播放,`outputs\` 資料夾裡有 mp4。

### 步驟 4:選配升級

**Triton + SageAttention 2(走 1A 已自動裝好,可略過)**

```powershell
python -m pip install -U "triton-windows>=3.7.0.post26,<=3.7.1.post27"
pip install https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
python -c "import triton; print(triton.__version__)"
```

README 本文寫 RTX 30XX 用 Triton 3.6(`"triton-windows>=3.6,<3.7"`),INSTALLATION.md 和 `setup_config.json` 已改成新裝用 3.7、舊的 3.6 也繼續可用。上面照較新的 INSTALLATION.md 寫。3.7 版在 Windows + Python 3.11 自帶一個 CUDA helper,不用另外裝 Visual Studio,也比較不會被防毒擋。

**LoRA**:把 `.safetensors` 放進對應資料夾,例如 Wan 1.3B 放 `loras\wan_1.3B\`、Wan 5B 放 `loras\wan_5B\`、i2v 放 `loras\wan_i2v\`,重整後在 Advanced 模式的 LoRA 欄位選取並設倍率。LoRA 放在別的硬碟就用 `--lora-config lora_paths.json` 指過去([LORAS.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/LORAS.md))。

**圖生影片**:8GB 可以先試 **Wan2.1 Fun InP 1.3B**(`python wgp.py --i2v-1-3B` 會直接載它,3.13 GB),或 FastWan 5B(TI2V 本身就吃起始圖)。14B 的 i2v 在 8GB 上能不能跑、要多久,文件沒寫,我沒驗證。

- [ ] 完成確認:Configuration 裡 Attention 能選 `Sage2` 且生成不報錯;LoRA 下拉選單看得到你放的檔案。

### 步驟 5:疑難排解

| 症狀 | 先這樣處理 | 出處 |
|------|-----------|------|
| 載入模型就 CUDA out of memory | 換 1.3B、確認 `--quantize-transformer True`(預設開)、用 `--profile 4`、`--preload 0` | TROUBLESHOOTING.md |
| 生成到一半 OOM | 減 frames、降解析度;Configuration / Performance 把 *Attention Head Split* 設 Low/Medium(約省 1–2 GB,稍慢);關掉 `--compile` | TROUBLESHOOTING.md、issue #1956 |
| 系統 RAM 爆掉、整台卡住 | `--perc-reserved-mem-max 0.3` 或 `--profile 5`;調低 *Reserved RAM for Pinning* 並保留 *Smart Memory Pinning* | TROUBLESHOOTING.md |
| 第一次跑很久 | 正常:要下載模型(十幾 GB),Triton/Sage 第一次用也要編譯 GPU kernel | INSTALLATION.md |
| `torch.cuda.is_available()` 是 False / CUDA 錯誤 | `nvidia-smi` 確認驅動支援 CUDA 13,重裝 `torch==2.10.0 ... --index-url https://download.pytorch.org/whl/cu130` | TROUBLESHOOTING.md |
| 套件相容錯誤 | `python --version` 要是 3.11.14(配 PyTorch 2.10) | TROUBLESHOOTING.md |
| `pip install triton-windows` 失敗 | 先 `pip install --upgrade pip`,不行就 `--attention sdpa` 先跑起來 | TROUBLESHOOTING.md |
| Sage Attention 出錯 | 用 `python -c "import triton; print(triton.__version__)"` 檢查;清掉 `%USERPROFILE%\.triton` 快取(建議用搬走的方式,例如改名成 `.triton.bak`)後重試;再不行用 `sdpa` | TROUBLESHOOTING.md |
| Triton 被防毒軟體擋 | 升到 triton-windows 3.7(自帶 helper,不需要防毒排除);v18.19 前後也有 Bitdefender 的 workaround commit | INSTALLATION.md、commit `fde3c7e` |
| 7860 port 被佔用 | `python wgp.py --server-port 7861` | TROUBLESHOOTING.md |
| 什麼都不行時的最小設定 | `python wgp.py --t2v-1-3B --attention sdpa --profile 4 --teacache 0 --fp16` | TROUBLESHOOTING.md「Emergency Fallback」 |

- [ ] 完成確認:遇到的錯誤能在表裡找到對應處理;找不到的話到 [Discord](https://discord.gg/g7efUW9jGV) 或 [Issues](https://github.com/deepbeepmeep/WanGP/issues) 搜關鍵字。

### 步驟 6(選配):從 Claude Code 呼叫

這條是真的有官方路徑,不用靠第三方。在 WanGP 環境啟動帶 MCP 的 Web UI,再到 Claude Code 註冊:

```powershell
python wgp.py --profile 4 --attention sage2 --mcp-webui
# 另開一個終端機
claude mcp add --transport http wangp http://127.0.0.1:8000/mcp
```

之後對 Claude 說「用 Wan2.1 1.3B 生一支 3 秒的貓咪散步影片」,它會呼叫 `wangp_models` → `wangp_model` → `wangp_generate`,生成一樣在你的 3060 Ti 上跑,也會出現在 Web UI 的佇列裡。WanGP 的 MCP 位址和 `--mcp-webui` 出自 [API.md](https://github.com/deepbeepmeep/WanGP/blob/main/docs/API.md);`claude mcp add` 那行是依 Claude Code 通用的 MCP 設定方式推的,官方文件沒寫 Claude Code 專用範例,我沒實測。MCP 只開在 localhost,別對外開放。

不想讓家裡電腦跑,或要用 Wan 2.7 / 3.0 這種沒開源的新版,就改走上面「本機 Wan2GP vs 雲端 Wan API」表格裡的雲端 API。

- [ ] 完成確認:Claude Code 裡 `/mcp` 看得到 `wangp` 且狀態是 connected,請它列出模型會回傳 WanGP 的模型清單。

## 作者 DeepBeepMeep 的其他 repo

`gh api users/deepbeepmeep/repos` 共 21 個公開 repo,帳號 2021-05 建立、915 followers,沒填姓名和所在地。

### 時間線:從「一個模型一個 GP fork」到「全部併進 WanGP」

```
2024-12  FluxFillGP ─┐
2024-12  HunyuanVideoGP ─┤
2024-12  mmgp ◀──────────┼── 共用的記憶體管理核心
2025-01  Cosmos1GP ──────┤
2025-01  Hunyuan3D-2GP ──┤   (各自是上游官方 repo 的 fork + mmgp)
2025-01  OminiControlGP ─┤
2025-01  YuEGP ──────────┘
2025-02  Wan2GP ──▶ 吸收 Hunyuan Video / Flux / Hunyuan3D / YuE … ──▶ 2026 改名 WanGP
2026-03  LTX-Desktop-WanGP(第一個用 WanGP API 的 sample app)
2026-06~ 外掛範本、kernels、WGPKernels、SeedVC / DLSS5 / SageAttention 等配套 fork
```

### mmgp(Memory Management for the GPU Poor)

| 項目 | 內容 |
|------|------|
| Repo | <https://github.com/deepbeepmeep/mmgp>(196★ / 36 forks,2024-12-11 建立,最後 push 2026-09-20) |
| PyPI | `mmgp` 最新 **3.8.2(2026-09-27)**,從 1.0.0(2024-12-09)起共 96 個版本;[pypistats](https://pypistats.org/packages/mmgp) 近一個月約 **10.3 萬次下載** |
| 定位 | 取代 `accelerate` 的 offload,作者說 accelerate 對「在 pipeline 裡反覆載入/卸載的模型(例如 VAE)」處理不好 |
| 用法 | `from mmgp import offload, profile_type` 後 `offload.profile(pipe, profile_type.HighRAM_LowVRAM)`,幾乎隨插即用 |
| 功能 | 5 種 profile、分塊搬運、pinned RAM、即時 int8 量化、重寫的低 RAM safetensors loader、LoRA 不 merge 套用、`torch.compile` 支援 |

**授權有點亂,用之前要注意**:獨立 repo 的 `LICENSE.md` 是 GPL-3.0 全文,但 README 結尾又寫「non commercial use as long you give me proper credits」,兩者互相矛盾,所以 GitHub 判成 NOASSERTION。另外 **mmgp v4 只存在於 WanGP repo 的 `mmgp/` 目錄**(README 標 4.2.0、pyproject 標 4.0.0),而且那份明寫改適用 WanGP Community License 2.0;PyPI 上仍是 3.8.x。所以「pip install mmgp」拿到的跟 WanGP 實際在用的是不同世代。

### 舊的 GP fork 系列(2024-12 ~ 2025-02,多已停更)

| Repo | 上游 | ★ | 最後 push | 跟 WanGP 的關係 |
|------|------|---|----------|----------------|
| [YuEGP](https://github.com/deepbeepmeep/YuEGP) | multimodal-art-projection/YuE(歌曲生成) | 499 | 2025-02-14 | WanGP 已內建 YuE2 |
| [HunyuanVideoGP](https://github.com/deepbeepmeep/HunyuanVideoGP) | Tencent-Hunyuan/HunyuanVideo | 470 | 2025-05-26 | WanGP 已內建 Hunyuan Video 1/1.5 |
| [Hunyuan3D-2GP](https://github.com/deepbeepmeep/Hunyuan3D-2GP) | Tencent-Hunyuan/Hunyuan3D-2 | 459 | 2025-03-29 | WanGP v18.00 起內建 Hunyuan3D 2.1 |
| [Cosmos1GP](https://github.com/deepbeepmeep/Cosmos1GP) | NVIDIA/cosmos | 94 | 2025-02-15 | WanGP 裡沒找到 Cosmos |
| [FluxFillGP](https://github.com/deepbeepmeep/FluxFillGP) | black-forest-labs/flux(inpaint/outpaint,8 GB 起) | 78 | 2025-01-18 | WanGP 已內建 Flux 系列與遮罩編輯 |
| [OminiControlGP](https://github.com/deepbeepmeep/OminiControlGP) | Yuanshi9815/OminiControl | 44 | 2025-01-27 | WanGP 裡沒找到 OminiControl |

這些 repo 都沒有 archive,但一年半以上沒更新,WanGP README 底部仍列為 "Other Models for the GPU Poor"。

### 新一代配套 repo(2026,都是為 WanGP 服務)

| Repo | 用途 |
|------|------|
| [LTX-Desktop-WanGP](https://github.com/deepbeepmeep/LTX-Desktop-WanGP)(99★) | Lightricks 官方 LTX Desktop 的 fork,後端換成 WanGP API,README 說 VRAM 需求從 32 GB 降到 6 GB |
| [WGPKernels](https://github.com/deepbeepmeep/WGPKernels) | 自寫 INT8 weight linear kernel,預先編好的 C 函式庫,用 ctypes 載入,不綁 Python/PyTorch 版本 |
| [kernels](https://github.com/deepbeepmeep/kernels) | 預編 GGUF CUDA kernel wheel(含實驗性 ROCm) |
| [SageAttention](https://github.com/deepbeepmeep/SageAttention) | thu-ml/SageAttention fork,提供 Linux 預編、支援 CUDA Graph 的 wheel |
| [WanGP-SeedVC](https://github.com/deepbeepmeep/WanGP-SeedVC) | Seed-VC 的 GPL-3.0 改版,WanGP 第一次用到換聲功能時才下載,刻意不放進主 repo(授權隔離) |
| [dlss5-visual-enhancer](https://github.com/deepbeepmeep/dlss5-visual-enhancer) | Merserk 專案 fork,加上 WanGP 用的 DLSS 5 / Frame Generation worker |
| wan2gp-pixel-upsampler / wan2gp-blender-upsampler / wan2gp-stable-diffusion-1-4 / wan2gp-test | 外掛範本(空間超解析、插幀、模型外掛) |
| insightface / chumpy / smplfitter | 為了發 Windows wheel 或避開建置問題的相依 fork |

## 生態系(次要資訊,第三方)

- **Pinokio**:README 推薦社群作者 Morpheus 的 `wan2gp` / `wan2gp-amd` 腳本。
- **社群外掛**:`plugins.json` 登錄 File Gallery(Tophness)、Finetune Manager(GKartist75)、Image Suite(saintorphan)、HideUI 等。
- **影片教學**:README 只連了兩支 VACE 教學([1](https://www.youtube.com/watch?v=FMo9oN2EAvE)、[2](https://www.youtube.com/watch?v=T5jNiEhf9xk))。
- **鏡像與改版**:GitHub 和 cnb.cool 上有大量 fork(1,749 個),例如 DGX Spark 版、加 n8n API 的版本,品質未驗證。
- **冒名提醒**:README 特別聲明官方不會收授權費/訂閱,只認 GitHub 和 wangp.ai / wan2gp.ai,其他用 WanGP 名字的服務都跟它無關。

## 目前限制 / 注意事項

- **授權是自訂條款**:想把它包進付費產品、做 SaaS 或付費 API,都需要另談商業授權;條款三年內改了三次,要追最新版。
- **單人主導、更新超快**:1,871 commits 裡 deepbeepmeep 佔 1,416;幾乎每週一版,沒有 tag/release 可以 pin,`git pull` 後偶爾要重裝 kernel。commit 訊息常是 "fixes"、"more fixes"。
- **安裝相依很重**:requirements 一長串,再加上要依顯卡世代挑 PyTorch / Triton / Sage / Flash 版本,Windows 最容易卡。Docker 腳本的版本落後手動安裝說明。
- **open issues 1,308**(含 PR),回應能力有限。
- **只能跑開源權重**:Wan 2.5 之後的版本(OpenRouter 上的 2.6/2.7/3.0)WanGP 沒有,想用就只能走雲端。
- **效能數字缺乏獨立驗證**:VRAM、速度改善都是作者在 changelog 自報。
- **MCP 預設沒有權限隔離**:連上的 agent 共用佇列、能取消彼此任務;對外開放要開 OAuth。

## 研究價值與啟示

### 關鍵洞察

1. **護城河在記憶體工程,模型只是貨架上的商品**:WanGP 自己不訓練任何模型,但它把「新模型一出就能在 8–12 GB 卡上跑」做成常態。mmgp 從獨立函式庫變成內建模組、再補自家 kernel 和 VAE 重寫,一路往下挖到硬體層。這跟本站 [abogen](abogen.md) 的「薄模型 + 厚 pipeline」是同一套邏輯,只是 WanGP 的「厚」做到了 CUDA kernel。
2. **一人維護的平台化路線:先多 repo,後單體**:作者 2024 年底一個模型開一個 GP fork,三個月後全部收進 WanGP,舊 repo 就停更。單體 app 讓 mmgp、UI、佇列、外掛只維護一份,也讓 10.9k 星集中在一個 repo。代價是 `wgp.py` 長到近 1.5 萬行,外部貢獻門檻高。
3. **從 Apache-2.0 收緊到自訂授權,反映「開源 wrapper 被轉售」的壓力**:條款明確點名禁止白牌、付費 API、託管服務,README 也特別警告冒名服務。fork 了 Apache 專案再改成限制性授權,只能約束作者自己新增的程式碼;授權文字本身也寫明第三方部分維持原授權。
4. **生成工具正在變成「agent 的 GPU 後端」**:WanGP 同時做了 MCP server、Python API、官方 SKILL.md、外部 agent 看圖驗收,還能反過來用 Claude Code / Codex 當自己的大腦。本機 AI 工具的 UI 之外,「給 agent 用的介面」已經變成標配,第三方小 wrapper 很快就被官方實作取代。
5. **本機 vs 雲端的分界在「開源權重世代」**:Wan 2.1/2.2 開源,所以 WanGP 能跑還能掛 LoRA;更新的 Wan 2.6/2.7/3.0 只在雲端以每秒計價提供。要最新模型就付雲端費用,要 LoRA、隱私、免費量產就選本機舊一代。

### 與其他專案的關聯

- **[abogen](abogen.md)**:同為「把開源模型產品化的本機工具」,abogen 包一個 82M TTS,WanGP 包幾百個大模型;WanGP 也內建多個 TTS,功能上有部分重疊。
- **[VoiceStudio](voicestudio.md)**:同樣是本機多引擎生成 app 且內建 MCP server,一個專攻語音、一個以影片為主。兩者都證明「本機 AI app + MCP」已成慣例。
- **[Koharu](koharu.md)**:Koharu 內建一個用 Codex backend 的 agent 驅動整個 pipeline;WanGP 的 Deepy Prime 也能接 Codex / Claude Code 當大腦,是同一種「app 內嵌外部 coding agent」做法。
- **[Deep-Live-Cam](deep-live-cam.md)**:同類「消費級 GPU 跑生成式影像」的本機工具,但專做即時換臉。
- **[video-autopilot-kit](video-autopilot-kit.md)**:走 ffmpeg + CapCut 自動化剪輯路線,不生成畫面;和 WanGP 可以互補,一個生素材、一個剪片。

## 一句話總結

> WanGP(Wan2GP)是 DeepBeepMeep 從 Wan2.1 fork 出來、現在已是 10.9k 星的本機生成超級 app:靠自家 mmgp 的分塊 offload、量化和自寫 kernel,讓 Wan 2.1/2.2、LTX-2.x、Hunyuan Video、Flux、Qwen 等上百個開源模型在消費級顯卡上跑,部分 6 GB 起。它還內建 MCP server、Python API 和官方 agent skill,Claude Code 可以當遙控器,但真正生影片的是你的 GPU。授權已從 Apache-2.0 改成禁止轉售與付費託管的 WanGP Community License 2.0。
