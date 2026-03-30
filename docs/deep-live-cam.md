---
date: "2026-03-30"
category: "AI 應用"
icon: "material-file-document-outline"
oneliner: ""
---
# Deep-Live-Cam 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [hacksider/Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam) |
| 官方網站 | [deeplivecam.net](https://deeplivecam.net/) |
| DeepWiki 架構分析 | [System Architecture](https://deepwiki.com/hacksider/Deep-Live-Cam/4.1-system-architecture) |
| YUV.AI 技術介紹 | [Real-Time Face Swapping with One Image](https://yuv.ai/blog/deep-live-cam) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | hacksider |
| Stars | 85.6K（截至 2026-03-30） |
| Forks | 12.5K |
| 語言 | Python |
| 授權 | AGPL-3.0 |
| 最新版本 | v2.6（2026-02） |

Deep-Live-Cam 是一套**即時人臉替換與一鍵影片 deepfake 工具**，只需一張照片即可在即時視訊、影片或圖片中換臉。完全離線運行，無需網路連接。

> **核心賣點**：一張照片 + 一鍵操作 = 即時換臉，無需訓練模型。

---

## 核心功能

| 功能 | 說明 |
|------|------|
| **即時 Webcam 換臉** | 視訊通話或直播中即時替換臉部 |
| **影片 / 圖片處理** | 批次處理預錄影片和圖片 |
| **Mouth Masking** | 保留原始嘴部動作，提升說話時的真實感 |
| **Multi-Face Mapping** | 多人場景中為不同人分配不同來源臉部 |
| **Movie Mode** | 處理完整電影級影片 |
| **Virtual Camera** | 整合 OBS，可在任何直播平台使用（v2.6） |
| **HyperSwap 模型** | 256×256 人臉，品質提升 200%（v2.3+） |
| **即時預覽** | 處理影片時即時預覽換臉效果 |

---

## 五層系統架構

```
┌─────────────────────────────────────────┐
│ Layer 1: Entry Points（run.py）          │
│   CLI + GUI 啟動                         │
├─────────────────────────────────────────┤
│ Layer 2: Application Core                │
│   modules/core.py — 生命週期管理         │
│   modules/globals.py — 集中狀態（單一真相）│
├─────────────────────────────────────────┤
│ Layer 3: User Interface                  │
│   modules/ui.py — CustomTkinter GUI     │
│   Preview windows + 控制面板             │
├─────────────────────────────────────────┤
│ Layer 4: Processing Pipeline             │
│   modules/processors/frame/              │
│   動態載入、標準介面、模組化              │
├─────────────────────────────────────────┤
│ Layer 5: Analysis & Utilities            │
│   face_analyser.py — InsightFace 偵測   │
│   utilities.py — 影片 I/O               │
└─────────────────────────────────────────┘
```

### Frame 處理管線

```
輸入幀（Webcam / 影片 / 圖片）
    │
    ▼
┌──────────────────┐
│ Face Detection    │ InsightFace buffalo_l
│                  │ 512 維 embedding + 106 點 landmark
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Face Swapping     │ inswapper_128_fp16.onnx
│                  │ 1. 5 點 landmark affine 變換
│                  │ 2. ONNX 推理生成換臉結果
│                  │ 3. Poisson blending / alpha 混合
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Face Enhancement  │ GFPGAN v1.4 (1024×1024)
│                  │ 或 GPEN-BFR-256/512
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Post-processing   │ Mouth masking
│                  │ Color correction
│                  │ Sharpness enhancement
│                  │ Frame interpolation
└──────────────────┘
```

### 關鍵模型

| 模型 | 用途 | 說明 |
|------|------|------|
| `inswapper_128_fp16.onnx` | 人臉替換引擎 | InsightFace 的 ONNX 模型，128×128 輸入 |
| `GFPGANv1.4` | 人臉增強 | 1024×1024 解析度 |
| `GPEN-BFR-256/512` | 替代增強模型 | 較輕量 |
| `buffalo_l` | 人臉偵測 | InsightFace 分析模型 |
| HyperSwap | 高品質換臉 | 256×256，v2.3 新增 |

### Mouth Masking 技術

保留原始嘴部動作的機制：

1. 用 106 點 facial landmark 提取嘴部區域
2. 建立雙 mask（臉部 + 嘴部）via convex hull
3. Gaussian blur 羽化（`mask_feather_ratio` 1-20）
4. Alpha compositing 將原始嘴部貼回

可調參數：`mouth_mask_size`（0-100%）、`mask_feather_ratio`、`mask_down_size`

### Multi-Face Mapping

- **影片/圖片模式**：`source_target_map` — frame-level 詳細映射
- **即時/Webcam 模式**：`simple_map` — embedding-based dictionary
- KMeans 聚類識別獨特個體，`find_similar_faces()` 用 cosine similarity 即時匹配

---

## 硬體支援

| 加速方式 | 平台 | 需求 |
|---------|------|------|
| **NVIDIA CUDA** | Windows/Linux | CUDA 12.8.0 + cuDNN v8.9.7 |
| **AMD DirectML** | Windows | DirectX 12 相容 GPU |
| **Apple CoreML** | macOS | Apple Silicon M1/M2/M3 |
| **Intel OpenVINO** | 全平台 | Intel CPU/GPU |
| **CPU** | 全平台 | 最慢，但最高相容性 |

### 效能優化

- **多執行緒影片處理**：`ThreadPoolExecutor` 並行編碼
- **即時模式**：獨立的 capture / detection / processing / display 執行緒
- **Frame interpolation**：時間平滑（`interpolation_weight` 可調）
- **影片編碼器選擇**：`libx264`、`h264_nvenc`（GPU）、`libx265`
- **CRF 品質控制**：0-51

---

## 安裝需求

- Python 3.11（macOS Apple Silicon 用 3.10）
- FFmpeg
- Visual Studio 2022 Runtimes（Windows）
- 模型檔案 ~300MB（自動或手動下載）

---

## 版本演進

| 版本 | 重點 |
|------|------|
| v2.3 | HyperSwap 模型（256×256, 200% 品質提升）、Lightning-Fast Face Enhancer（4x 加速）、smart model dropdown |
| v2.4 | 穩定性改進 |
| v2.6 | **Virtual Camera**（OBS 整合，任何直播平台可用）、核心渲染重建（顯著加速）、熱插拔攝影機（Refresh 按鈕）|

> 開發團隊跳過 v2.5，認為進展幅度值得直接跳到 v2.6。

---

## 倫理與安全

### 內建防護

- **內容過濾器**：自動阻擋裸露、暴力、敏感素材（戰爭畫面等）的處理
- **使用聲明**：要求使用者取得被換臉者同意，分享時標明為 deepfake

### 風險與爭議

Deep-Live-Cam 因為極低的使用門檻（一張照片 + 一鍵）引發廣泛關注：

| 風險類型 | 案例 |
|---------|------|
| **金融詐騙** | 英國工程公司 CFO deepfake 導致 $25M 未授權轉帳 |
| **語音詐騙** | Deepfake 語音促成 €220K 轉帳 |
| **選舉干預** | 2024 美國初選，deepfake Biden 語音 robocall 呼籲選民不投票 |
| **非自願色情** | 目前 deepfake 最大宗的惡意使用 |

### 法規動態（2024-2025）

| 法規 | 說明 |
|------|------|
| **美國 TAKE IT DOWN Act**（2025-04） | 針對非自願親密影像（含 AI 生成），提供受害者快速移除機制 |
| **美國 50 州 + DC** | 全部已立法針對非自願親密影像，部分涵蓋 deepfake |
| **EU AI Act**（2024-08 生效） | 規範 AI 驅動的假訊息，未合規平台面臨罰款 |

### 媒體報導

Ars Technica、Yahoo!、CNN Brasil、TrendMicro、PetaPixel 等主流媒體均有報導，焦點在技術能力與詐騙/濫用風險之間的張力。

---

## 研究價值與啟示

### 關鍵洞察

1. **門檻降低是雙面刃**：Deep-Live-Cam 把 deepfake 的門檻從「需要訓練模型 + GPU + 技術背景」降到「一張照片 + 一鍵」。85.6K stars 反映了巨大需求，但同時大幅降低了惡意使用的門檻。

2. **ONNX Runtime 是跨平台 AI 推理的統一層**：透過 ONNX，同一個模型可以在 CUDA、DirectML、CoreML、OpenVINO、CPU 上運行。這種「一次訓練，到處推理」的策略值得 AI 應用開發參考。

3. **即時處理的多執行緒架構**：capture / detection / processing / display 四條獨立執行緒是即時 AI 應用的標準架構模式。

4. **Mouth Masking 是實用創新**：保留原始嘴部動作讓說話場景更真實。用 106 點 landmark + dual mask + Gaussian blur feathering 的技術路線簡單有效。

5. **內容過濾器是最低限度的倫理防護**：阻擋裸露/暴力素材是必要的，但無法防止金融詐騙、選舉干預等惡意使用。真正的防護需要法規層面的配合。

6. **AGPL-3.0 授權的意涵**：不同於 MIT/Apache 的寬鬆授權，AGPL 要求任何修改版本（包括 SaaS 部署）都必須開源。這是有意識的選擇——降低被商業化包裝為封閉服務的風險。

### 技術面的借鑑

- **InsightFace + ONNX Runtime** 的組合是人臉 AI 應用的標準技術棧
- **Poisson blending** 在影像合成中的應用（梯度域混合，邊緣更自然）
- **KMeans 聚類 + cosine similarity** 做人臉辨識匹配
- **CustomTkinter** 做 Python GUI（比 Tkinter 美觀，比 Electron 輕量）
