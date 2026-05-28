---
date: "2026-05-28"
category: "學習資源"
card_icon: "material-school-outline"
oneliner: "joshhu 對 Microsoft SkillOpt 的精簡忠實重現版，針對 HotpotQA 多跳問答，用 ~9 個檔案講清「文字空間優化器」全貌，含真實 Qwen3.6-27B 實驗結果（種子→優化 test F1 0.8424→0.8524），離線測試零網路"
---

# skillopt-qa 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/joshhu/skillopt-qa> |
| 原始框架 | [microsoft/SkillOpt](skillopt.md) |
| 論文 | [arXiv:2605.23904](https://arxiv.org/abs/2605.23904)《SkillOpt: Executive Strategy for Self-Evolving Agent Skills》 |
| 維護者 | [joshhu](https://github.com/joshhu) |
| License | MIT |
| 性質 | 獨立教學用實作，**非官方程式碼** |

## 專案概述

**skillopt-qa** 是 joshhu 對 [Microsoft SkillOpt](skillopt.md) 的**精簡、忠實重現版**（24 stars，建立於 2026/05/27），專門針對 **HotpotQA** 多跳推理問答任務。它的定位明確：用最少的程式碼把 SkillOpt 的「文字空間優化器」核心講清楚，是教學/理解導向的最小實作。

SkillOpt 的核心理念（不微調權重，而是為凍結 LLM agent 訓練一份可重用的自然語言技能 `best_skill.md`）在這裡被濃縮成約 9 個檔案。整個技能學習流程仿照神經網路訓練——有 epoch、mini-batch，以及一道**驗證閘門**：只有當 held-out 準確率提升時才接受編輯。

對想理解 SkillOpt 但被官方 repo 的多 benchmark/多後端/WebUI 複雜度勸退的人，這是絕佳的入門路徑。

## 運作原理（README 的 ASCII 流程）

```
種子技能 ──► [agent 帶技能跑 train batch] ──► 軌跡(答對/答錯)
                          │
                          ▼
              [optimizer LLM 提出一次「有界」編輯]
                          │
                          ▼
              [在驗證集上評估候選技能]
                          │
              有進步? ──是──► 接受，成為新最佳技能
                          │
                          └─否──► 拒絕，回饋 optimizer(別再提同樣的)
```

完整實作了論文的穩定機制：**足夠證據**（同時呈現成功與失敗）、**有界文字更新**（小而精準）、**拒絕編輯記憶**、**慢更新**（每步一次且須過閘門）。

## 真實實驗結果（本筆記重點）

skillopt-qa 最有價值之處是**附了實跑數據**——在本機 **Qwen3.6-27B（凍結、關閉思考）** 上跑 HotpotQA（train 64 / val 64 / test 100）：

**驗證閘門軌跡**（只接受讓 val f1 提升的編輯）：

| step | 候選 val f1 | 當前最佳 | 動作 |
|------|------------|---------|------|
| baseline | 0.8465 | — | 種子技能 |
| 1 | **0.8822** | 0.8465 | ✅ ACCEPT |
| 2 | 0.8465 | 0.8822 | reject |
| 3 | 0.8822 | 0.8822 | reject |
| 4 | 0.8822 | 0.8822 | reject |
| 5 | 0.8465 | 0.8822 | reject → 連續 4 次拒絕，提早停止 |

**種子 vs 優化後比較**（test 為 100 題未見資料）：

| Skill | val F1 | test EM | test F1 |
|-------|--------|---------|---------|
| Seed (baseline) | 0.8465 | 0.700 | 0.8424 |
| Optimized | 0.8822 | 0.710 | 0.8524 |
| **Delta** | **+0.0357** | **+0.010** | **+0.0100** |

關鍵結論：優化後技能在**完全未見資料**上仍有提升 → 學到的是可泛化策略而非擬合 val，且**全程未動任何權重，只改一份 `skill.md`**。

> 維護者誠實標註：提升幅度小，因為 Qwen3.6-27B 在 HotpotQA 本就強（種子即 0.84 F1）、樣本小，且 temperature=0 在 vLLM 連續批次下非完全 deterministic（±1 分波動）。換較弱模型或更難任務，SkillOpt 論文可達 +20 分級。

## 環境與使用

```bash
cd skillopt-qa
uv venv && uv pip install -e ".[dev]"
cp .env.example .env

# 1. 下載資料集（從 HuggingFace 抓 HotpotQA）
uv run skillopt-download --out data/hotpotqa --n-train 64 --n-val 64 --n-test 200

# 2. 訓練技能
uv run skillopt-train --config configs/hotpotqa/default.yaml \
    --split-dir data/hotpotqa --out-root outputs

# 3. 部署：best_skill.md 就是純文字，接到任何 QA agent 的 system prompt 前面即可
```

- 需 Python ≥3.10、`uv`、一個 **OpenAI 相容** chat endpoint（預設對接本機 Qwen vLLM `qwen3.6-27b` @ `localhost:8080/v1`）
- 不安裝任何 GPU 套件——把 `model.base_url` 指向任何 endpoint 即可
- **離線測試**：`uv run pytest` 全部以 fake LLM 執行，完全不需網路

### 專案結構（~9 個核心檔案）

| 路徑 | 角色 |
|------|------|
| `skillopt/config.py` | YAML 設定 + CLI 覆寫 |
| `skillopt/llm.py` | OpenAI 相容 chat 客戶端 |
| `skillopt/data.py` | HotpotQA 下載與切分 |
| `skillopt/agent.py` | 凍結 QA agent + 平行 rollout |
| `skillopt/evaluator.py` | EM / token-F1 評分 |
| `skillopt/optimizer.py` | 文字空間技能優化器 |
| `skillopt/trainer.py` | epoch/batch 迴圈 + 驗證閘門 |

## 目前限制 / 注意事項

- **非官方、教學導向**——忠實但簡化，正式研究/生產請用 [官方 SkillOpt](skillopt.md)
- **只支援 HotpotQA**——官方支援 6 種 benchmark，這裡聚焦單一任務
- **24 stars、剛建立**——個人教學專案，無 license 以外的維護承諾
- **實驗的小提升不代表方法無效**——是強模型 + 小樣本所致，README 已誠實說明

## 研究價值與啟示

### 關鍵洞察

1. **「最小忠實重現」是理解論文的最佳路徑**：官方 SkillOpt 為了支援 6 benchmark、多後端、WebUI、resume，程式碼必然複雜。skillopt-qa 把同一套核心機制（軌跡→有界編輯→驗證閘門→接受/拒絕）濃縮成 ~9 個檔案，讓人能一眼看穿「文字空間優化器」的骨架。這呼應本站 [Claude Code from Source](claude-code-from-source.md)、[AI Engineering from Scratch](ai-engineering-from-scratch.md) 的學習價值——**讀最小實作勝過讀完整框架**。

2. **附真實實驗數據讓抽象方法變得可信**：很多論文重現只有程式碼沒有結果。skillopt-qa 給了完整的 step-by-step 驗證閘門軌跡與 test 集數字，還誠實解釋「為何提升幅度小」。這種**可重現 + 誠實標註侷限**的態度，是教學實作的最高標準。

3. **驗證閘門軌跡把「優化在做什麼」視覺化了**：那張 step 表（step 1 接受 0.8822，step 2-5 連續拒絕後早停）比任何文字解釋都清楚地展示了 validation gate 的運作——大多數候選編輯會被拒絕，只有真正泛化的改進才存活。這是理解「為何 SkillOpt 不會發散」的最佳教材。

4. **「best_skill.md 接到別的模型」驗證了跨模型部署**：README 明說產物可套到別的模型上，印證 SkillOpt 的核心賣點——技能是模型無關的純文字資產。教學版親自演示了這個可攜性。

5. **離線 fake-LLM 測試是務實的工程示範**：`pytest` 全程不需網路，用 fake LLM 跑 e2e。這對任何做 LLM 應用的人是重要範式——**把 LLM 呼叫抽象成可替換介面，測試邏輯而非測試模型**，讓 CI 快速且零成本。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [microsoft/SkillOpt](skillopt.md) | 本 repo 是其精簡教學重現；官方多 benchmark/後端/WebUI，這裡專注 HotpotQA + 最小程式碼 + 實驗數據 |
| vs [Claude Code from Source](claude-code-from-source.md) / [AI Engineering from Scratch](ai-engineering-from-scratch.md) | 同屬「最小重現幫助理解」的學習資源範式 |
| vs 一般論文 repo | 多了誠實的實驗結果與侷限說明，教學價值更高 |

**最大啟示**：skillopt-qa 示範了「論文重現」作為學習資源的理想形態——**不只重現程式碼，還重現實驗、誠實標註侷限、提供離線可測的最小骨架**。想理解 SkillOpt「文字空間優化」這個略抽象的概念，先讀這份 24-star 的教學版，再回頭看官方框架，會比直接啃論文或完整 repo 高效得多。它也再次印證本站的一個觀察：在 AI 領域，一份好的最小實作的教學價值，往往超過原始的完整框架。
