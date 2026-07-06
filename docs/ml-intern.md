---
date: "2026-07-06"
category: "Coding Agent 工具"
card_icon: "material-school"
oneliner: "Hugging Face 官方開源的自主 ML 工程師 agent：讀論文、訓練模型、上架模型，GPQA 表現超越 Claude Code"
tags:
  - agent-framework
  - llm-training
  - harness
---

# ML Intern 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/huggingface/ml-intern> |
| HF Space（Web 版） | <https://huggingface.co/spaces/smolagents/ml-intern> |
| MarkTechPost 發布報導 | <https://www.marktechpost.com/2026/04/21/hugging-face-releases-ml-intern-an-open-source-ai-agent-that-automates-the-llm-post-training-workflow/> |
| Analytics Vidhya 實測評測 | <https://www.analyticsvidhya.com/blog/2026/05/ml-intern-from-prompt-to-a-shipped-hugging-face-model/> |
| Medium 深度分析（生態系護城河論） | <https://medium.com/@AdithyaGiridharan/hugging-face-just-open-sourced-an-ml-engineer-why-ml-intern-bets-on-ecosystem-access-not-model-0dd1af12c8d4> |
| Agent Trace Viewer 說明 | <https://huggingface.co/changelog/agent-trace-viewer> |

**基本資料**（2026-07-06）：⭐ 10,581 · Fork 1,136 · Python · Apache-2.0 · 2025-10 建立、2026-04 公開發布 · 作者含 Leandro von Werra、Lewis Tunstall（smolagents / TRL 團隊）

## 專案概述

ML Intern 是 Hugging Face 官方推出的開源「自主 ML 工程師」agent：給它一句 prompt（例如 `ml-intern "fine-tune llama on my dataset"`），它會自己查文件、讀 arXiv 論文、找資料集、寫訓練腳本、送 HF Jobs 跑訓練、看評測結果、診斷失敗、重跑迭代，最後把模型連同 model card 和 Gradio demo 上架到 Hub。定位是「實習生」而非取代者——昂貴或破壞性操作（開 GPU job、建 sandbox）都要人工核准。

它解決的問題不是「模型會不會寫 PyTorch」，而是 ML 工作流的碎片化摩擦：找論文、追引用、挖資料集、調整格式、申請算力、追蹤實驗，這些貫穿 arXiv / Hub / Jobs / Trackio 的手工管線工作。ML Intern 把整個 HF 生態當成它的檔案系統來操作。

官方 launch demo 的成績：在 PostTrainBench 上，10 小時內（單張 H100）把 Qwen3-1.7B 的 GPQA 科學推理分數從約 10% 拉到 32%，超越同一任務上 Claude Code 的 22.99%。過程中它自己做了合成資料生成（先評估資料集品質、針對 edge case 補資料）和 GRPO 強化學習（含 reward 監控與 component ablation）。

## 核心功能與技術架構

### 功能總覽

| 面向 | 內容 |
|------|------|
| 執行模式 | 互動 CLI、headless（單 prompt 自動核准）、HF Space web 版 |
| 模型來源 | HF Inference Providers（Kimi、GLM、DeepSeek、GPT、Claude…）+ 本地模型（`ollama/`、`vllm/`、`lm_studio/`、`llamacpp/`，走 LiteLLM OpenAI 相容端點） |
| 工具運行時 | 預設本地 `bash`/`read`/`write`/`edit`；`--sandbox-tools` 切到 HF Space sandbox（可要 GPU） |
| ML 專屬工具 | HF docs 檢索、arXiv / hf.co/papers 論文閱讀 + 引用圖遍歷、Hub 資料集探索與重格式化、HF Jobs 訓練、GitHub code search、Trackio 實驗追蹤 |
| Session 紀錄 | 自動上傳到私有 HF dataset，格式是 **Claude Code JSONL**，Hub 的 Agent Trace Viewer 直接可視化 |
| 通知 | Slack 單向通知 gateway（approval_required / error / turn_complete） |
| 擴充 | MCP servers（HTTP transport，env var 自動代入）、`agent/core/tools.py` 加內建工具 |

### Agent 迴圈架構

```
User/CLI
   │ Operation（user_input / exec_approval / interrupt / compact）
   ▼
submission_loop ──► Handlers.run_agent()
                        │
                        ▼
              Agentic Loop（上限 300 迭代）
              ├─ Session
              │   ├─ ContextManager   ← 訊息歷史、170k 自動壓縮、上傳 HF
              │   └─ ToolRouter       ← HF docs/papers/datasets/jobs、
              │                          GitHub search、sandbox、planning、MCP
              ├─ Doom Loop Detector   ← 偵測重複工具呼叫模式、注入矯正 prompt
              └─ 每迭代：LLM call → 解析 tool_calls → 核准檢查
                        → 執行 → 結果回填 context → 重複
```

三個值得留意的 harness 設計：

1. **Doom Loop Detector**——偵測 agent 卡在重複工具呼叫的死循環，主動注入矯正 prompt，這是長時間自主運行必備的防呆
2. **核准閘門**——jobs、sandbox、破壞性操作強制等待人工確認，配合 Slack 通知形成「放著跑、有事叫我」的工作模式
3. **170k 自動壓縮**——ContextManager 在 context 逼近上限時自動 compact，支撐 10 小時級別的長任務

## 快速開始

```bash
git clone git@github.com:huggingface/ml-intern.git
cd ml-intern
uv sync && uv tool install -e .

# .env
HF_TOKEN=<hf-token>          # 需開通 Inference Providers 權限
GITHUB_TOKEN=<github-pat>

ml-intern                                      # 互動模式
ml-intern "fine-tune llama on my dataset"      # headless
ml-intern --model ollama/llama3.1:8b "..."     # 本地模型
ml-intern --sandbox-tools "test this in a GPU sandbox"
```

## 目前限制 / 注意事項

- **HF 生態鎖定**：推理走 HF Router 計費到你的 HF 帳號、訓練走 HF Jobs、sandbox 是 HF Space——離開 HF 生態價值大減，這是設計取捨而非缺陷
- **Trace 預設自動上傳**：session 會傳到你名下的私有 dataset，隱私敏感場景要在 config 設 `share_traces: false` 關掉
- **完美指標會騙人**：Analytics Vidhya 實測 DistilBERT 分類器拿到 100% test accuracy，但壓力測試（否定句、錯字、模糊輸入）全數翻車；agent 不會主動處理類別不平衡或 edge case，評測設計仍需人把關
- **通知是單向的**：Slack gateway 只送不收，不能從 Slack 回覆核准
- **成熟度**：2026-04 才公開，63 個 open issues，API 和 config 格式還在快速變動

## 研究價值與啟示

### 關鍵洞察

1. **押注生態系存取而非模型智力**。ml-intern 的論點是：agentic ML 的瓶頸不在「模型能否寫對 PyTorch」，而在碎片化工作流的摩擦。它不跟 frontier model 比推理，而是提供對 Hub / Jobs / Papers / Trackio 的特權級整合——價值歸屬於「擁有無摩擦基底的人」，不是「擁有最聰明模型的人」。這對思考任何垂直領域 agent 的護城河都適用：**整合深度可以打贏模型品質**（GPQA 32% vs Claude Code 22.99% 就是證據，儘管 Claude Code 底層模型更強）。

2. **Claude Code JSONL 正在變成 agent trace 的事實標準**。HF 官方選擇用 Claude Code 的 session 格式儲存 trace，Hub 的 Agent Trace Viewer 原生支援。一個競品生態主動採用 Anthropic 的格式，說明 agent 可觀測性領域正在收斂——做 agent 工具時直接輸出這個格式可以免費獲得整條工具鏈。

3. **「實習生」定位是精準的產品設計**。supervision-first：便宜操作全自動、昂貴操作等核准、單向通知讓人非同步監工。這比「全自主」誠實，也比「每步都問」實用——實測裡 agent 在 GPU credits 不足時自己降級到免費 CPU 繼續跑，該省的省、該問的問。

4. **Doom Loop Detector 值得抄**。自主 agent 跑 300 迭代、10 小時，最常見的死法是卡在重複工具呼叫。用模式偵測 + 矯正 prompt 注入來自救，比單純設 max-iterations 上限聰明，是所有長任務 harness 都該有的元件。

5. **領域 agent 的工具設計勝過通用工具**。ml-intern 的工具不是 generic bash + browser，而是「讀論文並遍歷引用圖」「檢查資料集並重格式化」這種領域動詞。同樣的 LLM，工具的抽象層次對了，效率就完全不同。

### 與其他專案的關聯

- **[Anthropic Harness Design](harness-design-long-running-apps.md)**：ml-intern 的 ContextManager 自動壓縮、doom loop 偵測、核准閘門，是該文長任務 harness 原則的完整實作範例
- **[OpenCode](opencode.md) / [Open SWE](open-swe.md)**：同為 CLI coding agent，但 ml-intern 示範了「垂直領域特化」路線——用領域工具和生態整合對打通用 agent
- **[LiteLLM](litellm.md)**：ml-intern 的多模型支援（HF Router + 本地四種 provider）全靠 LiteLLM 抽象層，是 LiteLLM 作為 agent 基礎設施的實例
- **[Autoresearch](autoresearch.md)**：同樣做自主研究迴圈，ml-intern 多了「研究之後動手訓練並出貨」的後半段
