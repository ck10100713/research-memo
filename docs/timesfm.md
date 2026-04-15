---
date: "2026-04-15"
category: "量化交易"
card_icon: "material-chart-timeline-variant"
oneliner: "Google 時間序列基礎模型 — 200M 參數、16K context、zero-shot 預測，已整合 BigQuery"
---

# TimesFM 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [google-research/timesfm](https://github.com/google-research/timesfm) |
| 論文 (ICML 2024) | [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688) |
| Google Research Blog | [官方介紹](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/) |
| HuggingFace 模型 | [TimesFM Collection](https://huggingface.co/collections/google/timesfm-release) |
| BigQuery 整合 | [TimesFM in BigQuery](https://cloud.google.com/bigquery/docs/timesfm-model) |
| TSFM 比較 | [TimesFM vs Chronos vs MOIRAI](https://paperswithbacktest.com/course/timesfm-vs-chronos-vs-moirai) |
| 效能比較 | [AI Models Demand Forecasting](https://www.griddynamics.com/blog/ai-models-demand-forecasting-tsfm-comparison) |

**專案狀態：** ⭐ 17.4K+ stars · Python · Apache 2.0 · ICML 2024 · Google Research 官方

## 專案概述

TimesFM（Time Series Foundation Model）是 **Google Research 開發的預訓練時間序列基礎模型**，專為 zero-shot 時間序列預測設計。核心架構是 decoder-only Transformer，將連續時間點的 patch 當作 token 進行自回歸建模。

預訓練資料量從最初的 **1,000 億個真實時間點**擴展到後來的 **4,000 億+**，涵蓋 Google Trends、Wikipedia 等來源。模型能在未見過的時間序列上直接做零樣本預測，無需重新訓練。

## 版本演進

| 版本 | 發布 | 參數量 | Context | 重點變化 |
|------|------|--------|---------|---------|
| **1.0** | 2024-05 | 200M | 512 | 首版，單變量預測 |
| **2.0** | 2025-05 | 500M | 2,048 | 擴大模型和 context |
| **2.5** | 2025-09 | 200M | **16,384** | 參數縮回但 context 大幅擴展，移除 frequency indicator |

### TimesFM 2.5 重點特性

- **200M 參數**（從 2.0 的 500M 縮減）— 更快推理
- **16K context**（從 2,048 擴展 8 倍）
- **連續分位數預測** — 可選 30M quantile head，最多 1K horizon
- **外部協變量支援**（XReg）— 2025-10 加回
- **移除 frequency indicator** — 簡化 API
- **支援 PyTorch + Flax** 雙後端
- **Claude Code SKILL.md** — 2026-03 新增 Agent 整合

## 核心架構

```
輸入時間序列
     │
     ▼
┌──────────────────────┐
│  Patching            │  連續時間點 → 固定長度 patch（token）
│  (Continuous Embed)  │  不像 Chronos 做離散化
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Decoder-only        │  Stacked Transformer layers
│  Transformer         │  Self-attention + FFN
│  (200M params)       │  Context: 最長 16,384 時間點
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Output Head         │  Point forecast
│  + Quantile Head     │  + 10th-90th 分位數（可選 30M head）
│  (optional 30M)      │
└──────────────────────┘
```

**與 LLM 的類比：**
- Patch = Token
- 時間序列 = 句子
- 自回歸預測下一個 patch = 預測下一個 token

## vs 競品比較

| 維度 | TimesFM 2.5 | Chronos-2 | MOIRAI-2 |
|------|-------------|-----------|----------|
| 開發者 | Google | Amazon | Salesforce |
| 架構 | Decoder-only Transformer | Encoder-only T5 | Decoder-only + MoE |
| 參數量 | 200M | 9M–710M（5 種規格） | MoE 路由 |
| 多變量 | ❌ 單變量 | ✅（2025-10 新增） | ✅（原生設計） |
| 預訓練數據 | 400B+ 時間點 | 公開時序 + 合成數據 | 27B 觀測值，9 領域 |
| 輸出 | 點預測 + 分位數 | Token 分佈（原生概率） | 分位數回歸 |
| 企業整合 | **BigQuery + AlloyDB** | 社群最廣 | 最強跨資產建模 |
| Zero-shot 表現 | 強（GIFT-Eval 前三） | **最強**（最高 win rate） | 強（多變量最佳） |

### 金融場景推薦

| 場景 | 推薦模型 | 原因 |
|------|---------|------|
| 單一股票日頻預測 | **TimesFM 2.5** | 快速單變量 + BigQuery 整合 |
| 多資產組合 | MOIRAI-2 | 原生跨序列依賴建模 |
| 概率區間預測 | Chronos-2 | Token 分佈輸出，彈性規格 |
| CPU 部署 | Chronos-Bolt | 9M 參數，300+ forecasts/sec |
| 新資產/少量歷史 | 任何 TSFM | 遷移學習自預訓練 |

> **重要發現：** 研究顯示部分 TSFM benchmark 的測試集與預訓練資料重疊，「膨脹了 47-184% 的準確度」。使用前務必驗證數據分離。

## 快速開始

```bash
# 安裝
git clone https://github.com/google-research/timesfm.git
cd timesfm
uv venv && source .venv/bin/activate
uv pip install -e .[torch]
```

```python
import torch
import numpy as np
import timesfm

torch.set_float32_matmul_precision("high")

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)
model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
    )
)

# 預測
point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[np.linspace(0, 1, 100), np.sin(np.linspace(0, 20, 67))],
)
point_forecast.shape     # (2, 12)
quantile_forecast.shape  # (2, 12, 10): mean + 10th-90th 分位數
```

### BigQuery 整合（企業用）

```sql
-- 在 BigQuery 中直接使用 TimesFM 預測
SELECT *
FROM ML.FORECAST(MODEL `project.dataset.timesfm_model`, ...)
```

## 目前限制 / 注意事項

- **僅支援單變量** — 無法建模多資產間的依賴關係（Chronos-2 和 MOIRAI-2 已支援）
- **金融數據表現未必最佳** — 研究顯示「off-the-shelf TSFMs 在金融數據上表現不佳，但金融領域專屬預訓練能帶來顯著提升」
- **需要 fine-tuning** — 「Few-shot fine-tuning on your specific asset class consistently outperforms zero-shot inference for financial applications」
- **Benchmark 數據洩漏風險** — 部分評估可能包含與預訓練重疊的數據
- **非官方 Google 產品** — 開源版明確標示「not an officially supported Google product」（BigQuery 版才是正式產品）
- **2.5 版 API 仍在調整** — README 標示「under construction」

## 研究價值與啟示

### 關鍵洞察

1. **「縮小參數、擴大 context」是 TimesFM 2.5 的反直覺選擇。** 從 500M 縮回 200M 參數，但 context 從 2K 擴展到 16K——這暗示對時間序列預測來說，**看得更長比模型更大更重要**。更長的 context 捕捉更多季節性和趨勢，比增加參數的邊際效益更高。

2. **TimesFM 是 Kronos 的直接參照物。** Kronos 論文中 TimesFM 是主要 baseline 之一，Kronos 的 RankIC 比 TimesFM 提升 93%。但兩者定位不同：TimesFM 是通用時序基礎模型（天氣、能源、流量都行），Kronos 專注金融 K 線。TimesFM 的通用性 vs Kronos 的領域特化，反映了 TSFM 領域「通才 vs 專才」的根本張力。

3. **BigQuery 整合是 Google 的殺手級差異化。** Chronos-2 在 benchmark 上可能更強，但 TimesFM 直接內嵌在 BigQuery SQL 中——對已在 GCP 生態的企業來說，這是零摩擦的價值。不需要懂 Python、不需要部署模型、不需要管 GPU——一句 SQL 搞定。

4. **SKILL.md 整合代表 TSFM 進入 Agent 時代。** 2026-03 新增的 Claude Code Skill 整合，讓 AI Agent 可以直接呼叫 TimesFM 做預測。這不只是「用 AI 預測」，而是「讓 AI Agent 自主決定何時需要預測、預測什麼、如何解讀」。

5. **三大 TSFM 的生態分工已成形。** TimesFM（Google/企業整合）、Chronos（Amazon/社群最廣）、MOIRAI（Salesforce/多變量最強）——各有不可替代的優勢，未來更可能是組合使用而非贏家通吃。

### 與其他專案的關聯

- **vs Kronos（筆記庫中）：** Kronos 是金融 K 線專用模型，TimesFM 是通用時序模型。Kronos 的 tokenizer 將 OHLCV 離散化，TimesFM 用 continuous patch embedding。在金融預測上 Kronos 大幅領先 TimesFM（RankIC +93%），但 TimesFM 的通用性和企業整合更強。
- **vs AI-Trader（筆記庫中）：** AI-Trader 是 Agent 交易平台，TimesFM 可作為其 Agent 的預測信號來源——用 TimesFM 預測未來走勢，再由 Agent 決定交易策略。
- **vs MCP Toolbox（筆記庫中）：** TimesFM 整合 BigQuery，MCP Toolbox 橋接 AI Agent 與資料庫。兩者可以組合：Agent 透過 MCP Toolbox 查詢歷史數據，再用 TimesFM 做預測。
