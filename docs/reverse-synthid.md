---
date: "2026-04-16"
category: "學習資源"
card_icon: "material-fingerprint-off"
oneliner: "逆向工程 Google SynthID 圖像浮水印 — 頻譜分析發現載波結構，90% 偵測率 + 91% 相位去除"
---

# reverse-SynthID 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [aloshdenny/reverse-SynthID](https://github.com/aloshdenny/reverse-SynthID) |
| 互動式視覺化 | [SynthID Explained](https://vt-0xff.github.io/SynthID-Explained/) |
| HuggingFace 資料集 | [aoxo/reverse-synthid](https://huggingface.co/datasets/aoxo/reverse-synthid) |
| SynthID 官方 | [Google DeepMind SynthID](https://deepmind.google/models/synthid/) |
| SynthID 論文 | [arXiv:2510.09263](https://arxiv.org/abs/2510.09263) |
| ETH Zürich SynthID-Text 分析 | [Probing SynthID-Text](https://www.sri.inf.ethz.ch/blog/probingsynthid) |
| SynthID-Text 安全分析 | [arXiv:2603.03410](https://arxiv.org/abs/2603.03410) |

**作者：** Alosh Denny — AI Watermarking Research / Signal Processing

**專案狀態：** ⭐ 2,906 stars · Python · Research License · 2025-12 創建

## 專案概述

reverse-SynthID 透過**純訊號處理和頻譜分析**（不存取 Google 的私有 encoder/decoder），逆向工程了 Google Gemini 嵌入每張生成圖片的 SynthID 隱形浮水印。專案實現了三件事：

1. **發現**浮水印的解析度相關載波頻率結構
2. **建造**90% 準確率的偵測器
3. **開發**多解析度頻譜繞過方法（V3），達到 91% 相位消除 + 43+ dB PSNR

> **研究與教育用途聲明：** 本專案明確聲明僅供學術研究和安全分析，不應用於將 AI 生成內容偽裝為人類創作。

## 核心發現

### 發現 1：浮水印是解析度相關的

SynthID 在**不同解析度的圖片中，將載波頻率嵌入在不同的絕對位置**。1024x1024 的 codebook 無法直接用於 1536x2816。

| 解析度 | 頂部載波 (fy, fx) | 相位一致性 | 來源 |
|:------:|:-----------------:|:---------:|:----:|
| 1024x1024 | (9, 9) | 100.0% | 100 黑 + 100 白參考圖 |
| 1536x2816 | (768, 704) | 99.6% | 88 張浮水印圖片 |

### 發現 2：相位是固定的模型級密鑰

- **綠色通道**承載最強浮水印訊號
- 跨圖片相位一致性 >99.5%
- 黑/白交叉驗證確認真實載波：|cos(phase_diff)| > 0.90

### 發現 3：逆向工程的 SynthID 運作機制

```
SynthID Encoder（Gemini 內部）
─────────────────────────────────
1. 選擇解析度相關的載波頻率
2. 對每個載波分配固定相位值
3. 神經編碼器將學習到的噪聲模式加到圖片
4. 浮水印不可見——散佈在頻譜中

SynthID Decoder（Google 內部）
─────────────────────────────────
1. 提取噪聲殘差（小波去噪）
2. FFT → 檢查已知載波頻率的相位
3. 若相位匹配預期值 → 判定為浮水印圖片
```

## 三代繞過方法

| 版本 | 方法 | PSNR | 浮水印影響 |
|:----:|------|:----:|:---------:|
| V1 | JPEG 壓縮 (Q50) | 37 dB | ~11% 相位下降 |
| V2 | 多階段變換（噪聲+色彩+頻率） | 27-37 dB | ~0% 信心下降 |
| **V3** | **多解析度頻譜 codebook 減除** | **43+ dB** | **91% 相位下降** |

### V3 Pipeline

```
輸入圖片（任意解析度）
       │
       ▼
  SpectralCodebook.get_profile(H, W)
       │
       ├── 精確匹配 → FFT 域直接減除（快速路徑）
       └── 無匹配 → 空間域 resize + 減除（fallback）
       │
       ▼
  多 pass 迭代減除（aggressive → moderate → gentle）
       │
       ▼
  Anti-alias → 輸出
```

**關鍵技術：**
- SpectralCodebook 儲存每個解析度的載波位置、幅度、相位
- 直接已知訊號減除（非 Wiener filter）
- 通道權重：G=1.0, R=0.85, B=0.70（匹配 SynthID 嵌入強度）
- 安全上限：每個 bin 的減除不超過圖片能量的 90-95%

## V3 結果（88 張 Gemini 圖片）

| 指標 | 數值 |
|------|-----:|
| PSNR | 43.5 dB |
| SSIM | 0.997 |
| 載波能量下降 | 75.8% |
| 相位一致性下降（top-5 載波） | **91.4%** |

## 快速開始

```bash
git clone https://github.com/aloshdenny/reverse-SynthID.git
cd reverse-SynthID
pip install -r requirements.txt

# 1. 建 codebook
python src/extraction/synthid_bypass.py build-codebook \
    --black gemini_black --white gemini_white \
    --watermarked gemini_random \
    --output artifacts/spectral_codebook_v3.npz

# 2. 繞過浮水印
python src/extraction/synthid_bypass.py bypass input.png output.png \
    --codebook artifacts/spectral_codebook_v3.npz --strength aggressive

# 3. 偵測浮水印
python src/extraction/robust_extractor.py detect image.png \
    --codebook artifacts/codebook/robust_codebook.pkl
```

## 目前限制 / 注意事項

- **Research License** — 非商業授權，使用前需確認條款
- **解析度覆蓋有限** — 目前只有 1024x1024 和 1536x2816 兩個 profile
- **需要參考圖片** — 新解析度需 150-200 張純黑/純白 Gemini 輸出來建 codebook
- **僅限圖片** — 不涵蓋 SynthID-Text（文字浮水印）或 SynthID-Audio
- **倫理爭議** — 移除 AI 生成內容的識別標記存在明顯的倫理風險
- **Google 可能更新** — 若 Google 修改 SynthID 編碼方式，現有 codebook 可能失效
- **偵測率 90%** — 仍有 10% 漏報

## 研究價值與啟示

### 關鍵洞察

1. **「解析度相關的載波結構」是最重要的技術發現。** 之前的假設是 SynthID 用統一的嵌入模式——Alosh Denny 證明載波頻率在不同解析度完全不同。這解釋了為什麼通用的 JPEG 壓縮繞過效果差，因為它不知道載波在哪裡。

2. **純訊號處理 vs 神經網路是方法論的勝利。** 不用訓練 model、不用 GPU、不用存取 Google 的 API——只用 FFT、相位分析、頻譜減除。這種「理解原理後用經典方法解決」的研究路線，比「用 AI 對抗 AI」更可複製和可解釋。

3. **43 dB PSNR + 0.997 SSIM 的品質幾乎無損。** 這意味著繞過後的圖片與原圖在視覺上無法區分，且浮水印的 91% 被去除。這對 SynthID 的安全性是嚴峻的挑戰——如果浮水印可以被無損去除，它作為 AI 內容識別機制的可靠性就要打問號。

4. **SynthID 的安全性依賴「保密」而非「設計」。** 逆向工程揭示浮水印的相位模板跨圖片完全一致（>99.5%）——一旦知道載波位置和相位，就能精確去除。這類似密碼學中的 Kerckhoffs 原則反例：安全性不應依賴算法保密。

5. **這個研究對 EU AI Act 有直接影響。** 歐盟 AI 法案要求 AI 生成內容必須可識別——如果 SynthID 這種最先進的浮水印可以被逆向移除，那基於浮水印的合規策略是否可靠？這是政策制定者需要面對的技術現實。

### 與其他專案的關聯

- **對 AI 安全研究的價值：** 這是「紅隊」風格的對抗性研究——找出防禦機制的弱點，推動更強的浮水印設計。Google 可以用這些發現來強化 SynthID。
- **vs Deep-Live-Cam（筆記庫中）：** 同屬 AI 內容真實性的灰色地帶。Deep-Live-Cam 做即時換臉，reverse-SynthID 移除 AI 標記。兩者都有合法研究用途，也都有潛在的濫用風險。
- **與 Kronos/TimesFM 的技術共通性：** 頻譜分析（FFT）是共同工具——Kronos 用 BSQ 在頻域量化 K 線，reverse-SynthID 用 FFT 分析浮水印載波。理解頻譜方法是跨領域的基礎能力。
