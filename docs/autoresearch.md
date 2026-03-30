---
date: ""
category: "AI Agent 框架"
icon: "material-flask"
oneliner: "Karpathy 的自主 AI 研究代理，讓 Agent 整夜跑 LLM 實驗"
---
# Autoresearch 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/karpathy/autoresearch |
| 作者 | Andrej Karpathy |
| Stars | ~49.5K |
| 授權 | MIT |
| 語言 | Python (83.5%), Jupyter Notebook (16.5%) |
| 相關專案 | [nanochat](https://github.com/karpathy/nanochat) |
| 推文說明 | [tweet 1](https://x.com/karpathy/status/2029701092347630069), [tweet 2](https://x.com/karpathy/status/2031135152349524125) |

## 專案概述

Autoresearch 是 Andrej Karpathy 開源的**自主 AI 研究代理系統**，核心概念是：給一個 AI agent 一個小型但真實的 LLM 訓練環境，讓它整夜自主實驗。Agent 修改訓練程式碼、跑 5 分鐘實驗、檢查是否改善、保留或捨棄、然後重複。你早上醒來就能看到實驗日誌和（希望是）更好的模型。

Karpathy 在 README 開頭的科幻風格引言：

> *One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of "group meeting". That era is long gone. Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies.*

### 核心理念

- **人類寫 program.md**（研究方向、Agent 指令）
- **AI Agent 改 train.py**（模型架構、超參數、優化器等）
- 人機協作：人類是研究主管，AI 是不眠不休的研究員

適合場景：

- 自主 AI 研究流程的探索與實踐
- LLM 訓練實驗的自動化
- 理解 AI Agent 如何進行科學研究
- 小型 GPU 上的 LLM 架構搜索

## 專案結構

```
prepare.py      — 固定常數、資料準備 + 執行時工具（不可修改）
train.py        — 模型、優化器、訓練迴圈（Agent 修改此檔案）
program.md      — Agent 指令（人類修改此檔案）
pyproject.toml  — 依賴套件
```

只有三個重要檔案，刻意保持極簡：

| 檔案 | 角色 | 誰修改 |
|------|------|--------|
| `prepare.py` | 資料下載、BPE tokenizer 訓練、dataloader、evaluation | 無人修改（固定） |
| `train.py` | 完整 GPT 模型、Muon + AdamW 優化器、訓練迴圈 | **AI Agent** |
| `program.md` | Agent 指令、研究方向設定 | **人類研究員** |

## 設計決策

### 1. 固定 5 分鐘時間預算

訓練永遠跑固定 5 分鐘（wall clock，不含啟動/編譯），不論你的硬體規格：

- 每小時約 **12 次實驗**
- 整夜約 **100 次實驗**
- **優點**：不同實驗直接可比較（不管 Agent 改了什麼）；會找到你平台上時間預算內的最佳模型
- **缺點**：不同硬體平台之間的結果無法互相比較

### 2. 單一指標

使用 **val_bpb**（validation bits per byte）：

- 越低越好
- 與 vocab size 無關，架構變更可公平比較

### 3. 單檔修改

Agent 只碰 `train.py` 一個檔案，保持範圍可控、diff 可審查。

### 4. 自包含

- 只需 PyTorch 和少量套件
- 不需分散式訓練
- 單 GPU、單檔案、單指標

## 快速開始

```bash
# 1. 安裝 uv 套件管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安裝依賴
uv sync

# 3. 下載資料並訓練 tokenizer（一次性，約 2 分鐘）
uv run prepare.py

# 4. 手動跑一次訓練實驗（約 5 分鐘）
uv run train.py
```

**需求：** 單張 NVIDIA GPU（在 H100 上測試）、Python 3.10+、[uv](https://docs.astral.sh/uv/)

## 啟動 Agent

在此 repo 中開啟 Claude/Codex 或其他 Agent（關閉所有權限），然後提示：

```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```

`program.md` 本質上就是一個超輕量的 "skill"。

## 小型裝置調校建議

如果在較小的裝置（如 MacBook）上跑，Karpathy 建議：

1. **使用低熵資料集**：例如 [TinyStories](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean)（GPT-4 生成的短故事），較窄範圍的資料可以用更小的模型得到合理結果
2. **降低 `vocab_size`**：從 8192 降到 4096、2048、1024，甚至 256（byte-level tokenizer）
3. **降低 `MAX_SEQ_LEN`**：根據裝置可降至 256，同時增加 `DEVICE_BATCH_SIZE` 補償
4. **減少 `EVAL_TOKENS`**：讓驗證損失在更少資料上評估
5. **降低 `DEPTH`**：預設 8，可降至 4
6. **使用 `WINDOW_PATTERN = "L"`**：預設 "SSSL" 的交替 banded attention 在小裝置上可能很慢
7. **降低 `TOTAL_BATCH_SIZE`**：保持 2 的冪次，可降至 `2**14`（~16K）

## 社群 Fork

| Fork | 平台 |
|------|------|
| [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) | MacOS |
| [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) | MacOS (MLX) |
| [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) | Windows |
| [andyluo7/autoresearch](https://github.com/andyluo7/autoresearch) | AMD |

## 研究價值與啟示

### 人機協作的新範式

Autoresearch 代表了一種新的研究模式：

```
人類（研究主管）                    AI Agent（研究員）
    │                                    │
    ├── 設定研究方向 (program.md)          │
    │                                    ├── 修改模型 (train.py)
    │                                    ├── 跑實驗（5 分鐘）
    │                                    ├── 評估結果 (val_bpb)
    │                                    ├── 保留 or 捨棄
    │                                    └── 重複...（整夜）
    │                                    │
    └── 早上審查實驗日誌 ◄───────────────┘
```

### 關鍵洞察

1. **研究也可以被 Agent 化**：不只是 coding，連科學實驗的 iterate 過程都可以交給 AI
2. **約束是好的**：固定時間、單一指標、單檔案修改，這些約束讓自主研究變得可行
3. **program.md 是「元研究」**：人類不直接做研究，而是「研究如何讓 AI 做研究」
4. **極簡設計哲學**：三個檔案就構成完整的自主研究系統，沒有複雜的框架或配置

### 與其他專案的關聯

| 專案 | 層級 | 對比 |
|------|------|------|
| Autoresearch | 研究自動化 | AI 自主進行 ML 實驗 |
| Paperclip | 公司編排 | 多 Agent 組成組織 |
| gstack | 開發工作流 | Agent 輔助軟體開發 |
| CrewAI / LangChain | Agent 框架 | Agent 建構工具 |

Autoresearch 獨特之處在於它不是在做「軟體開發」，而是在做「科學研究」——讓 AI Agent 成為真正的研究員。
