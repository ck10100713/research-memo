---
date: "2026-04-12"
category: "量化交易"
card_icon: "material-chart-line"
oneliner: "首個金融 K 線基礎模型，將 OHLCV 離散化為階層式 Token 進行自回歸預測"
---

# Kronos 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 論文 (AAAI 2026) | [arXiv 2508.02739](https://arxiv.org/abs/2508.02739) |
| GitHub Repo | [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) |
| Hugging Face 模型 | [NeoQuasar](https://huggingface.co/NeoQuasar) |
| Live Demo | [Kronos Demo](https://shiyu-coder.github.io/Kronos-demo/) |
| 技術評論文章 | [Jonathan Kinlay 分析](https://jonathankinlay.com/2026/02/time-series-foundation-models-for-financial-markets-kronos-and-the-rise-of-pre-trained-market-models/) |

**作者：** Yu Shi†, Zongliang Fu†, Shuo Chen, Bohan Zhao, Wei Xu, Changshui Zhang, Jian Li （† 共同第一作者）

**專案狀態：** ⭐ 14.6K+ stars · MIT License · Python · AAAI 2026 Accepted

## 專案概述

Kronos 是**首個專為金融 K 線（candlestick）設計的開源基礎模型**。核心洞察是：通用時間序列基礎模型（TSFM）在金融數據上表現差勁，因為金融序列有低訊噪比、強非平穩性、OHLCV 多維度高階依賴等獨特特性——且既有 TSFM 的預訓練語料中金融數據佔比不到 1%。

Kronos 提出兩階段框架：先用專用 tokenizer 將連續的 K 線數據離散化為階層式 Token，再用 decoder-only Transformer 進行自回歸建模。模型在 **45 個全球交易所、超過 120 億筆 K 線紀錄**上預訓練，覆蓋股票、期貨等多種資產類別。

## 核心技術架構

### 兩階段框架總覽

```
Stage 1: K-line Tokenizer          Stage 2: Autoregressive Modeling
┌─────────────────────────┐       ┌──────────────────────────────┐
│  OHLCVA (6維連續向量)    │       │  Decoder-only Transformer    │
│         ↓               │       │         ↓                    │
│  Transformer Encoder    │       │  Temporal Embeddings (5種)   │
│  (3層, 256d, 4 heads)   │       │  + Coarse/Fine 融合投影      │
│         ↓               │       │         ↓                    │
│  BSQ 量化 → k-bit 二元碼│       │  Sequential Prediction:      │
│  分解為 Coarse + Fine   │       │  1. p(coarse | past)         │
│         ↓               │       │  2. p(fine | past, coarse)   │
│  Transformer Decoder    │       │         ↓                    │
│  (3層, 重建 OHLCVA)     │       │  Token → Decoder → 連續預測  │
└─────────────────────────┘       └──────────────────────────────┘
```

### Stage 1：K-line Tokenizer

| 組件 | 技術細節 |
|------|---------|
| 輸入 | OHLCVA 6 維向量，z-score 正規化後 clip 至 [-5, 5] |
| Encoder | 3 層 Transformer，256 維，4 heads |
| 量化方法 | Binary Spherical Quantization (BSQ) |
| 階層分解 | k=20 bit → 分為 coarse (10 bit) + fine (10 bit) |
| 有效詞彙量 | 每步預測 2×2^10 = 2×1024，而非 2^20 ≈ 100 萬 |
| 損失函數 | `L = L_coarse + L_fine + λL_quant`（λ=1） |
| Decoder | 3 層 Transformer，從 Token 重建原始 OHLCVA |

**BSQ 的關鍵優勢：** 超球面幾何提供「尾部敏感性」（tail sensitivity），增強對極端行情的偵測能力——這對風險管理至關重要。離散量化同時起到去噪效果，過濾金融數據中的高頻雜訊。

### Stage 2：Hierarchical Autoregressive Modeling

| 配置 | Kronos-small | Kronos-base | Kronos-large |
|------|-------------|-------------|-------------|
| Layers | 8 | 12 | 18 |
| d_model | 512 | 832 | 1664 |
| d_ff | 1024 | 2048 | 3072 |
| Heads | 8 | 16 | 32 |
| 參數量 | 24.7M | 102.3M | 499.2M |
| Context | 512 | 512 | 512 |

**關鍵設計：**

- **位置編碼：** RoPE（旋轉位置嵌入）
- **時間嵌入：** 5 種可學習嵌入（分鐘、小時、星期幾、日期、月份），捕捉市場週期性
- **序列預測：** 先預測 coarse subtoken，再以預測結果（非 ground truth）通過 cross-attention 條件生成 fine subtoken——降低 exposure bias
- **Test-time Scaling：** 生成多條隨機軌跡取平均，N=10 可提升 IC/RankIC 約 5-8%

## 預訓練數據

| 項目 | 數據 |
|------|------|
| 總記錄數 | 120+ 億筆 K 線 |
| 交易所 | 45 個，橫跨 30+ 國家 |
| 資產類型 | 股票、期貨等 |
| 時間頻率 | 1分/5分/10分/15分/20分/30分/60分/2小時/4小時/日/週 |

**數據清洗管線：** 結構性斷裂偵測 → 流動性不足過濾 → 價格停滯去除 → 最小長度驗證，每個閾值按頻率自適應調整。

## 實驗結果

### 核心性能（vs 25 個 baseline）

| 任務 | 指標 | 提升幅度 |
|------|------|---------|
| 價格預測 | RankIC | **+93%** vs 最佳 TSFM，**+87%** vs 最佳非預訓練模型 |
| 波動率預測 | MAE | **-9%** vs 競爭基線 |
| 合成 K 線生成 | Generative Fidelity | **+22%** vs 先前生成模型 |
| 投資模擬 | AER & IR | 所有基線中最高 |

### Ablation：為何離散化有效？

| 模型變體 | 預測空間 | Price RankIC | Vol MAE |
|----------|---------|-------------|---------|
| Direct-AR | 連續 | 0.0149 | 0.0565 |
| Prob-AR (Student-t) | 連續 | 0.0102 | 0.0464 |
| Kronos-Parallel | 離散（並行） | 0.0226 | 0.0461 |
| **Kronos (序列)** | **離散（階層）** | **0.0254** | **0.0384** |

結論：離散空間大幅優於連續空間；階層式序列預測優於並行預測。

## 快速開始

```bash
pip install -r requirements.txt
```

```python
from model import Kronos, KronosTokenizer, KronosPredictor

# 載入模型
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
predictor = KronosPredictor(model, tokenizer, max_context=512)

# 預測
pred_df = predictor.predict(
    df=x_df,                # OHLCV DataFrame
    x_timestamp=x_timestamp, # 歷史時間戳
    y_timestamp=y_timestamp, # 預測時間戳
    pred_len=120,
    T=0.6, top_p=0.9, sample_count=10
)
```

**Fine-tuning 流程（以 A 股為例）：**

1. 設定 `finetune/config.py` 路徑與超參數
2. `python finetune/qlib_data_preprocess.py` 準備 Qlib 數據
3. `torchrun --nproc_per_node=N finetune/train_tokenizer.py` 微調 tokenizer
4. `torchrun --nproc_per_node=N finetune/train_predictor.py` 微調預測器
5. `python finetune/qlib_test.py --device cuda:0` 回測驗證

## 目前限制 / 注意事項

- **Context window 僅 512 tokens** — 對長期趨勢分析可能不足（Kronos-mini 為 2048）
- **Kronos-large (499M) 未開源** — 論文中最強結果無法完全復現
- **僅支援 K 線數據** — 不包含訂單簿、新聞、基本面等替代數據
- **回測 ≠ 實盤** — 論文的投資模擬是簡化的 top-K 策略，未考慮滑點、手續費、流動性限制
- **BSQ tokenizer 的域遷移成本** — 轉移到新市場時需要重新微調 tokenizer

## 研究價值與啟示

### 關鍵洞察

1. **離散化是金融時序的正確歸納偏置。** Kronos 證明將連續 K 線量化為離散 token 後再建模，效果遠超直接在連續空間預測——因為離散化同時實現了去噪和狀態空間壓縮。這挑戰了「金融數據應該用連續模型」的直覺。

2. **NLP 範式遷移到金融時序的可行路徑。** Kronos 的技術棧（BSQ tokenizer → autoregressive Transformer → nucleus sampling）本質上是把 K 線當成一種「語言」來處理。這為 LLM 技術遷移到非文本序列提供了成功範例。

3. **階層式 Token 設計的巧妙性。** Coarse/Fine 分解不僅降低了詞彙空間（從 2^20 到 2×2^10），更強制模型先捕捉主要結構再學習殘差——類似於訊號處理中的多解析度分析。序列預測（非並行）在 ablation 中的優勢證實了這種因果依賴的重要性。

4. **Test-time Scaling 在金融場景的實用性。** 生成多條軌跡取平均的策略，本質上是蒙特卡羅模擬的現代版本——用 GPU 並行推理取代傳統的統計模擬，且效果單調遞增。這為實務中的「計算換精度」提供了明確的調節旋鈕。

5. **數據不平衡是 TSFM 在金融領域失敗的主因。** 論文揭露既有 TSFM 金融數據佔比不到 1%（有些 < 0.01%），這解釋了為何通用模型在金融任務上表現差——不是架構問題，而是數據分佈問題。

### 與其他專案的關聯

- **vs AI Hedge Fund / TradingAgents：** Kronos 定位在更底層——提供價格預測基礎能力，可作為上層交易 Agent 的 signal source。兩者是互補而非競爭關係。
- **vs NOFX / OpenStock / StockStats：** 這些工具聚焦於傳統量化因子或統計分析，Kronos 則代表「基礎模型直接預測」的新範式。可以想像將 Kronos 的預測信號作為新的 alpha factor 整合進傳統框架。
- **技術借鑑：** BSQ tokenizer 的設計思路可能對其他非文本序列（音訊、感測器數據、醫療時序）的 foundation model 有參考價值。
