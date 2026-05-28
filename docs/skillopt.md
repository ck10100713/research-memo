---
date: "2026-05-28"
category: "AI Agent 框架"
card_icon: "material-tune-variant"
oneliner: "Microsoft「文字空間優化器」：像訓練神經網路（epoch/batch/learning rate/validation gate）一樣訓練凍結 LLM agent 的自然語言技能，不動權重、產出可部署的 best_skill.md，弱模型上可達 +20 分級提升，arXiv:2605.23904"
---

# SkillOpt 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/microsoft/SkillOpt> |
| Project Page | <https://microsoft.github.io/SkillOpt/> |
| 論文 | [arXiv:2605.23904](https://arxiv.org/abs/2605.23904)《SkillOpt: Executive Strategy for Self-Evolving Agent Skills》 |
| Demo 影片 | <https://youtu.be/JUBMDTCiM0M> |
| License | MIT |
| 精簡教學重現版 | [skillopt-qa](skillopt-qa.md)（joshhu，針對 HotpotQA） |

## 專案概述

**SkillOpt** 是 Microsoft Research 在 2026/05 開源的「**文字空間優化器（text-space optimizer）**」（1,203 stars，MIT，Python），核心主張用一句 slogan 概括：

> *「像訓練神經網路一樣訓練 agent 技能——有 epoch、(mini-)batchsize、learning rate、validation gate——但完全不碰模型權重。」*

傳統提升 agent 表現靠微調模型權重（昂貴、需 GPU、綁定特定模型）。SkillOpt 反過來——**凍結 LLM agent，只優化一份自然語言「技能」文件（`best_skill.md`）**。它把整個技能學習流程做成類神經網路訓練的迴圈：讓 agent 帶著當前技能跑 batch → 收集軌跡（答對/答錯）→ optimizer LLM 提出有界編輯 → 在驗證集評估 → 只有準確率提升才接受。

最終唯一保留的產物就是 `best_skill.md`——一段純文字，**可跨模型、跨執行環境部署**（接到任何 agent 的 system prompt 前面即可）。

## 核心機制（論文的穩定化設計）

SkillOpt 的關鍵不是「讓 LLM 改 prompt」這麼簡單，而是一套防止優化發散的穩定機制：

| 機制 | 作用 |
|------|------|
| **Trajectory-driven edits** | 編輯由實際軌跡驅動（同時呈現成功與失敗案例＝足夠證據） |
| **Bounded text updates（有界更新）** | 小而精準的編輯，非整篇重寫——對應「learning rate」概念 |
| **Validation-gated updates（驗證閘門）** | 只有候選技能在 held-out 集提升才接受，否則拒絕 |
| **Rejected-edit memory（拒絕記憶）** | 記住被拒版本，回饋 optimizer「別再提同樣的」 |
| **Slow update（慢更新）** | 每步只做一次通過驗證的編輯，避免震盪 |
| **Meta skill** | epoch 層級的高階技能整合 |

這套設計把「prompt 優化」從黑箱 trial-and-error 變成有收斂保證、可監控的訓練流程。

## 支援的 Benchmark

| Benchmark | 類型 | Config |
|---|---|---|
| SearchQA | QA | `configs/searchqa/default.yaml` |
| ALFWorld | Embodied agent（具身） | `configs/alfworld/default.yaml` |
| DocVQA | 文件 QA | `configs/docvqa/default.yaml` |
| LiveMathematicianBench | 數學 | `configs/livemathematicianbench/default.yaml` |
| SpreadsheetBench | 程式碼生成 | `configs/spreadsheetbench/default.yaml` |
| OfficeQA | 工具增強 QA | `configs/officeqa/default.yaml` |

> 資料集本身不含在 repo，需自備（依 `train/val/test` split 目錄 + `items.json` 格式）。

## 快速開始

```bash
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt && pip install -e .

python scripts/train.py \
    --config configs/searchqa/default.yaml \
    --split_dir /path/to/searchqa_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5
```

支援 Azure OpenAI（推薦）、OpenAI、Anthropic Claude、本機 Qwen vLLM 等後端。關鍵超參數：`--num_epochs`、`--batch_size`、`--workers`。重跑同指令會從上次完成步驟 auto-resume。另附 Gradio WebUI 監控 dashboard（port 7860）。

### 輸出結構

```
outputs/<run_name>/
├── best_skill.md            # 最佳驗證技能（可部署產物）
├── history.json             # 每步訓練歷史
├── skills/skill_vXXXX.md    # 每步技能快照
├── steps/step_XXXX/         # 每步 patch/eval
├── slow_update/epoch_XX/    # 慢更新日誌
└── meta_skill/epoch_XX/     # meta skill 日誌
```

## 目前限制 / 注意事項

- **資料集需自備**——repo 不含 benchmark 資料，要自己按格式準備
- **依賴 optimizer + target 兩個模型呼叫**——訓練過程是多次 LLM rollout + 編輯評估，有 API 成本
- **提升幅度與模型強度反相關**——目標模型越強、種子技能越好，可改進空間越小；論文在**較弱模型**上可達 +20 分級（強模型上提升有限）
- **「技能」是 system-prompt 級的文字**——本質是高品質、可泛化的 prompt，不是模型能力本身的提升
- **研究專案性質**——2026/05 釋出，生態與長期維護待觀察

## 研究價值與啟示

### 關鍵洞察

1. **「文字空間優化」是介於 prompt engineering 與 fine-tuning 之間的第三條路**：fine-tune 改權重（貴、綁模型），手動 prompt engineering 靠人類試錯（不可規模化）。SkillOpt 把 prompt 優化變成**有訓練框架的自動化流程**——epoch/batch/validation gate 一應俱全。它證明「在文字空間做梯度下降的類比」是可行且有收斂保證的。

2. **validation gate 是防止 prompt 優化發散的關鍵**：純靠 LLM 反覆改 prompt 很容易過擬合或震盪。SkillOpt 的「只接受 held-out 提升的編輯 + 拒絕記憶」直接對應 ML 的早停與正則化。這是把成熟的訓練紀律移植到 prompt 優化——**任何做 auto-prompt 的人都該加上 held-out 驗證閘門**。

3. **「有界更新（bounded edit）」= learning rate**：不讓 optimizer 整篇重寫，只做小而精準的編輯。這個類比很精妙——大步更新會震盪，小步更新才穩定收斂。把 learning rate 概念搬到文字編輯的粒度控制，是個可推廣的設計原則。

4. **產物可跨模型部署是最大的實用價值**：`best_skill.md` 是純文字，可接到任何模型的 system prompt。這意味著**用強 optimizer 訓出的技能，可以部署到弱/便宜的 target 模型上**——一種「知識蒸餾」的文字空間版本，但不需重訓任何權重。

5. **涵蓋 QA、具身、數學、程式、表格、工具六大 benchmark 顯示方法泛用性**：從 ALFWorld（具身 agent）到 SpreadsheetBench（程式生成），同一套優化框架都適用，說明「文字空間技能優化」不限特定任務類型，是通用的 agent 改進手段。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [skillopt-qa](skillopt-qa.md) | 官方完整框架（多 benchmark、Azure/多後端、WebUI），skillopt-qa 是針對 HotpotQA 的精簡教學重現版 |
| vs DSPy / 自動 prompt 優化 | 同屬「自動優化文字提示」，但 SkillOpt 明確引入 epoch/batch/validation gate 的訓練框架類比與穩定化機制 |
| vs fine-tuning | 都在「提升 agent 表現」，但 SkillOpt 不碰權重、產物可跨模型、無需 GPU |
| vs [Superpowers](superpowers.md) / [Knowledge Work Plugins](knowledge-work-plugins.md) | 那些是人工撰寫的 skill，SkillOpt 是**自動訓練出 skill**——可視為 skill 生產的上游 |
| vs [Claude-Mem](claude-mem.md) | Claude-Mem 累積記憶，SkillOpt 蒸餾可泛化策略；前者是經驗存檔，後者是經驗提煉成可部署技能 |

**最大啟示**：SkillOpt 點出一個重要方向——**skill/prompt 不該靠人手寫，而該像模型一樣「訓練」出來**。當業界大量手寫 agent skill（Superpowers、KWP 等）時，SkillOpt 提供了自動化生產這些 skill 的方法論。它把 ML 訓練的成熟紀律（epoch、batch、learning rate、validation、早停）系統性移植到文字空間，是「自我演化 agent 技能」這個命題目前最完整的工程化答案。
