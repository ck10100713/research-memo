---
date: "2026-04-20"
category: "開發工具"
card_icon: "material-tune-variant"
oneliner: "Python 超參數優化框架天花板，14K stars、define-by-run API，v5 將加上 Prompt Optimization 與 MCP Server"
---
# Optuna — Python 超參數優化天花板，正邁向 Prompt Optimization 時代

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [optuna/optuna](https://github.com/optuna/optuna) |
| 官網 | [optuna.org](https://optuna.org/) |
| 文件 | [optuna.readthedocs.io](https://optuna.readthedocs.io/en/stable/) |
| v4.8.0 Release Note | [github.com/optuna/optuna/releases/tag/v4.8.0](https://github.com/optuna/optuna/releases/tag/v4.8.0) |
| **Optuna v5 Roadmap** | [Medium — Optuna v5 Roadmap](https://medium.com/optuna/optuna-v5-roadmap-ac7d6935a878) |
| AutoSampler 最新進展 | [Medium — AutoSampler: Full Support for Multi-Objective & Constrained](https://medium.com/optuna/autosampler-full-support-for-multi-objective-constrained-optimization-c1c4fc957ba2) |
| v4.5 GPSampler 多目標 | [Medium — Optuna v4.5](https://medium.com/optuna/optuna-v4-5-81e78d8e077a) |
| OptunaHub | [hub.optuna.org](https://hub.optuna.org/) |
| Optuna Dashboard | [github.com/optuna/optuna-dashboard](https://github.com/optuna/optuna-dashboard) |
| Optuna Integration | [github.com/optuna/optuna-integration](https://github.com/optuna/optuna-integration) |
| 範例 | [github.com/optuna/optuna-examples](https://github.com/optuna/optuna-examples) |
| 論文 | [Akiba et al. KDD 2019](https://doi.org/10.1145/3292500.3330701) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 維護方 | **Preferred Networks（PFN）** — 原作者 Takuya Akiba、Shotaro Sano 等日本 AI 公司 |
| Stars / Forks | **13,995 / 1,312** |
| 語言 | Python（支援 3.9-3.14） |
| License | MIT |
| 建立 | 2018-02-21（公開於 2018-10） |
| 最新版本 | **v4.8.0**（2026-03-16） |
| 最近更新 | 2026-04-20 |
| 關鍵字 | distributed、hyperparameter-optimization、machine-learning、parallel、python |

**Optuna** 是一個自動化超參數優化框架，採 **define-by-run** API（對照 TensorFlow 1.x 的 define-and-run）。你用正常 Python 語法（if/for）動態建搜尋空間，Optuna 在 runtime 決定取樣策略。

截至 2026 年，它是 Python 社群最流行的 HPO 工具（對比 Hyperopt 7K stars、Ray Tune 雖然更多功能但較重），**多數 Kaggle 解法 + 工業界 ML pipeline 的預設選擇**。

最值得關注的轉折：**v5 roadmap 明確把 Prompt Optimization 與 MCP Server 列為核心**，意味著 Optuna 要從 ML HPO 工具擴張為「通用 black-box optimization + LLM 工具」。

---

## 核心概念

### Study 與 Trial

| 術語 | 意義 |
|------|------|
| **Study** | 以 objective function 為中心的優化任務 |
| **Trial** | Study 裡的單次 objective function 執行 |

```python
import optuna, sklearn

def objective(trial):
    regressor_name = trial.suggest_categorical("regressor", ["SVR", "RandomForest"])
    if regressor_name == "SVR":
        svr_c = trial.suggest_float("svr_c", 1e-10, 1e10, log=True)
        regressor_obj = sklearn.svm.SVR(C=svr_c)
    else:
        rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32)
        regressor_obj = sklearn.ensemble.RandomForestRegressor(max_depth=rf_max_depth)
    # ... train + validate ...
    return error

study = optuna.create_study()
study.optimize(objective, n_trials=100)
```

Define-by-run 的威力：**搜尋空間可以有條件分支**（SVR 才有 `svr_c`，RF 才有 `rf_max_depth`），傳統 grid / random search 難以表達。

### Samplers（取樣演算法）

| Sampler | 適合場景 |
|---------|---------|
| **`TPESampler`** | 預設值；複雜搜尋空間（含 categorical、條件分支） |
| `GPSampler`（Gaussian Process） | 連續/整數空間；v4.5 起支援 **constrained multi-objective**；v4.8 加 constant liar strategy 支援平行化 |
| `CmaEsSampler` | 連續高維空間 |
| `NSGAIISampler` / `NSGAIIISampler` | 多目標（high eval count / many-objective） |
| `RandomSampler` / `GridSampler` / `BruteForceSampler` | baseline 對照 |
| `PartialFixedSampler` / `QMCSampler` / `IntersectionSearchSpace` | 特殊情境 |
| **`AutoSampler`**（OptunaHub） | **動態選最適 sampler**，v4.8 已支援多目標 + constrained |

### Pruners（剪枝器）

在 trial 中途就終止明顯沒希望的組合，**大幅省運算**：

- `MedianPruner`（預設概念）、`HyperbandPruner`、`SuccessiveHalvingPruner`、`ThresholdPruner`、`PercentilePruner`、`PatientPruner`

### 其他核心能力

- **Parallel / Distributed** — 多 worker 共享同一個 RDB storage，近無需改 code
- **Storage** — `sqlite:///db.sqlite3`、PostgreSQL、MySQL、Redis-compatible、JournalFileStorage
- **Visualization** — `optuna.visualization`（plotly）+ matplotlib 雙版本；歷史、重要性、平行座標圖、slice、contour、EDF

---

## 生態系全景

```
optuna              ← 核心（本 repo, 14K stars）
  ├─ optuna-dashboard      ← Web UI，即時視覺化優化歷史
  ├─ optuna-integration    ← 第三方整合（PyTorch、XGBoost…）
  ├─ optuna-examples       ← 可執行範例
  └─ optunahub             ← 社群擴充（samplers、visualizations、benchmarks）
       └─ optunahub-registry ← 公開發佈的 package
```

### Optuna Dashboard

```bash
pip install optuna-dashboard
optuna-dashboard sqlite:///db.sqlite3   # 不用寫 Python 看視覺化
```

即時 web dashboard（localhost:8080），免寫 Python 就能看優化歷史 / 超參數重要性。

### OptunaHub — 社群擴充平台

```python
import optunahub
module = optunahub.load_module(package="samplers/auto_sampler")
study = optuna.create_study(sampler=module.AutoSampler())
```

已有的知名包：
- `samplers/auto_sampler` — AutoSampler
- `samplers/ctpe` — c-TPE（含不等式約束的 TPE）
- `visualization/plot_beeswarm` — SHAP-like beeswarm 圖（v4.8 加入）

### Integrations

Catboost / Dask / fastai / Keras / LightGBM / MLflow / PyTorch / PyTorch Ignite / PyTorch Lightning / TensorBoard / TensorFlow / tf.keras / Weights & Biases / XGBoost / Trackio（新，v4.8）

---

## 最近版本重點

### v4.8.0（2026-03-16）

| 改進 | 說明 |
|------|------|
| **GPSampler + Constant Liar Strategy** | 平行優化時搜尋點重疊大幅降低（`n_jobs=10, n_trials=100` 場景）；目前僅支援 single-objective unconstrained，v4.9 會擴充 |
| **Beeswarm 視覺化** | SHAP 風格的參數重要性圖（經由 OptunaHub） |
| **Trackio Integration** | 新增 experiment tracking 整合 |
| 安全性 | `FileSystemArtifactStore` 驗證 `artifact_id` 防 path traversal |

### v4.7.0（2026-01-19）
### v4.6（2025-11-10）
### v4.5（2025-09-22）— **GPSampler 可做 constrained multi-objective**
### v4.4（2025-06-16）

---

## Optuna v5 Roadmap（🔥 重大轉折）

**發佈目標：2026 夏季**，以「regular minor releases」逐步上線，**無 breaking changes**。

### 🎯 Pillar 1：Generative AI Integration

| 新功能 | 描述 |
|--------|------|
| **Prompt Optimization** | 用 Optuna 演算法做自動/半自動 prompt engineering，包含建議候選 prompt + 評估機制 |
| **MCP Server for Optuna** | 讓 LLM agent 透過 MCP 存取 Optuna；提供「自動分析優化歷史」的 agent；MCP client 整合指南 |

> 這是 Optuna 從 ML HPO 跨入 **LLM Prompt / Agent 優化**的明確訊號。接下來 Claude Code、Cursor 等工具的 prompt 可能用 Optuna 自動調校。

### 🎯 Pillar 2：可及性提升

| 方向 | 做法 |
|------|------|
| 效能優化 | **Rust 重寫核心**降低記憶體 / 提升速度 |
| 嵌入式 | 目標資源受限與嵌入式環境 |
| 非 Python | Google Sheets 黑箱優化範本、自然語言問題描述、Rust 編譯成 **WASM** 供多語言使用 |

### 🎯 Pillar 3：核心演算法升級

| 方向 | 做法 |
|------|------|
| 預設 sampler | 跨各種設定都更強的預設 sampler |
| **AutoSampler 升級** | 自動演算法選擇更進化（v4.8 已納入 GPSampler 為選項） |
| GP 多目標 | Gaussian Process 為基礎的多目標優化 |
| Constrained | 對 infeasible 參數的完整評估支援 |
| **Multi-fidelity** | 引入 multi-fidelity 優化框架 |
| **ELA** | Exploratory Landscape Analysis 整合 |

---

## 使用情境

### 什麼時候該用 Optuna

| 情境 | 適合度 |
|------|-------|
| ML 模型超參數調整（XGBoost / LightGBM / PyTorch） | ⭐⭐⭐⭐⭐ 業界預設 |
| 有條件分支的搜尋空間（例如不同 optimizer 配不同 LR 範圍） | ⭐⭐⭐⭐⭐ define-by-run 殺手級場景 |
| 多目標優化（精度 vs 延遲、精度 vs 模型大小） | ⭐⭐⭐⭐⭐ NSGAII / NSGAIII / GPSampler |
| Constrained optimization（有效參數區間受限） | ⭐⭐⭐⭐ v4.5+ |
| 黑箱工程參數優化（ML 以外） | ⭐⭐⭐⭐ 搜尋、模擬、強化學習 reward tuning |
| 分散式並行優化 | ⭐⭐⭐⭐ 共用 RDB storage |
| **Prompt / LLM Agent 超參數** | ⭐⭐⭐（v5 才會原生支援，目前需自己寫 objective） |

### 什麼時候選別的工具

- 要 AutoML 全套（特徵工程 + 模型選型 + HPO）→ **H2O AutoML、AutoGluon、TPOT**
- 要 Ray cluster 大規模 → **Ray Tune**（本身是 Ray ecosystem，也可當 Optuna runner）
- 只要簡單 random / grid → `scikit-learn` `GridSearchCV` / `RandomizedSearchCV`

---

## 研究價值與啟示

### 關鍵洞察

1. **Define-by-run 是概念勝利**
   - 對照 Hyperopt 要預先寫死搜尋空間字典，Optuna 讓搜尋空間就是一段 Python
   - **條件分支搜尋空間是工業界常態**（不同 model family 有不同超參數集），Optuna 是少數一級支援的框架
   - 這個設計讓 Optuna 能被當成「通用 black-box optimization DSL」—— 這是 v5 roadmap 擴充到 Prompt Optimization 的前提

2. **OptunaHub 把 Optuna 從框架升級為平台**
   - 類似 HuggingFace Hub 的邏輯，讓研究論文的新 sampler（c-TPE、HEBO 等）能直接 `load_module` 使用
   - 意味著新研究成果的採用時間從「等下個 release」縮短到「Hub 上發佈當天」
   - **研究者也有動機上架**（學術引用價值提升）

3. **AutoSampler 是「把選擇權還給使用者」的反向設計**
   - 一般框架都在簡化 API，但 HPO 的難點是「選對演算法」
   - AutoSampler 把演算法選擇自動化 → **使用者 API 只有 `AutoSampler()`，其他都丟給它決定**
   - 是 ML 工具鏈「meta-optimization」的典範

4. **v5 的 MCP Server 是 LLM 生態系的 test case**
   - Optuna 要當 MCP server → 讓 Claude / Cursor 等 agent 可以「自動幫我調超參數 + 分析結果」
   - 這是 **非程式碼類工具率先被 MCP 化** 的早期案例
   - 搭配 Prompt Optimization 等於一個閉環：LLM agent 透過 MCP 呼叫 Optuna 優化 LLM prompt，再用結果改善 agent

5. **Rust + WASM 路線揭示 Python 工具的長期焦慮**
   - 13K stars 的 Python 框架卻計畫「Rust 重寫核心 + WASM」
   - 原因：**Python GIL 限制平行化、記憶體佔用高、無法上嵌入式**
   - 如果成功，Optuna 會是第一個原生支援 Google Sheets 黑箱優化的工具，意義遠超 ML

### 與其他筆記的關聯

| 相關筆記 | 關聯點 |
|---------|-------|
| [OpenAI Agent 建構指南](openai-practical-guide-building-agents.md) | v5 的 Prompt Optimization 與 agent evaluation 可對接 |
| [LangGraph Multi-Agent](langgraph-multi-agent.md) | multi-agent 系統的 reward / routing 超參數可用 Optuna 調 |
| [TradingAgents](tradingagents.md) | 交易策略參數可用 Optuna 搜索 |
| [AI Hedge Fund](ai-hedge-fund.md) | 策略超參數 tuning 的實戰場景 |
| [Kronos](kronos.md) | 時序模型的超參數調整 |
| [TimesFM](timesfm.md) | 預訓練模型的 fine-tune HPO |
| [StockStats](stockstats.md) | 技術指標參數優化 |
| [AI Engineering from Scratch](ai-engineering-from-scratch.md) | 在底層實作背景下理解 HPO 的必要性 |

### 可直接抄的 Pattern

```python
# 1. 寫 objective 時回傳要最小化的 metric
def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    # ... train, return val_loss ...

# 2. 加 pruning 省運算（train loop 裡 report 給 Optuna）
def objective(trial):
    for epoch in range(100):
        val_loss = train_one_epoch(...)
        trial.report(val_loss, epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()
    return val_loss

# 3. 多目標（精度 vs 模型大小）
study = optuna.create_study(directions=["maximize", "minimize"])

# 4. 用 OptunaHub 的 AutoSampler，自己不用選 sampler
import optunahub
sampler = optunahub.load_module("samplers/auto_sampler").AutoSampler()
study = optuna.create_study(sampler=sampler)

# 5. 共用 RDB 做分散式（多個 worker 同時跑）
study = optuna.create_study(
    storage="postgresql://user:pw@host/optuna",
    study_name="my-exp",
    load_if_exists=True,
)
```
