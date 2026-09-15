---
date: "2026-09-15"
category: "學習資源"
card_icon: "material-brain"
oneliner: "61K★、Apache-2.0 的「從 0 訓練一個小 LLM」教學專案——單張 3090、約 2.3 小時、約 3 塊人民幣就能把 64M 參數的 minimind-3 從預訓練練到會對話。關鍵訓練演算法與核心模組全部從 0 實現不依賴框架封裝，但結構對齊 Qwen3 生態、可轉 transformers/llama.cpp/ollama。涵蓋 Pretrain→SFT→LoRA→DPO→RLAIF(PPO/GRPO/CISPO)→Tool Use→Agentic RL 完整鏈路"
tags:
  - learning
  - llm-training
  - llm
---

# MiniMind 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★61,102 / 7,943 forks / Apache-2.0） | <https://github.com/jingyaogong/minimind> |
| 專案站 | <https://jingyaogong.github.io/minimind> |
| 實驗性拓展 | [dLM 離散擴散語言模型](https://github.com/jingyaogong/minimind/discussions/618) · [Linear Attention](https://github.com/jingyaogong/minimind/discussions/704) |

> **Metadata（2026-09-15 抓取）**：**61,102 stars / 7,943 forks / 66 open issues** · **Apache-2.0** · 建立於 **2024-07-27**、最後 push **2026-09-14**（**維護超過兩年、至今每天在動**）· Python · repo size 約 39 MB。

## 一句話定位

> **不是教你微調別人的模型，是教你把一個 LLM 從零拼出來。**

作者在專案介紹裡的比喻很到位：絕大多數「學 LLM」最後都停在用 LoRA 對現成大模型做少量微調——

> 這更像是在**教牛頓如何使用 21 世紀的智慧型手機**——雖然有趣，卻偏離了理解物理本質的初衷。

而 `transformers` / `trl` / `peft` 這些框架只暴露高度抽象的介面，十幾行就跑完「載入模型 + 載入資料集 + 推理 + 強化學習」，**方便但也把開發者與底層實作隔開了**。作者的立場：

> **「用樂高自己拼出一架飛機，遠比坐在頭等艙裡飛行更讓人興奮。」**

## 最有說服力的數字：3 塊錢、2 小時

這是整個專案的鉤子，而且 README 把成本估算攤開給你看（單卡 RTX 3090，租卡約 1.3 ¥/h）：

| 模型 | 參數量 | pretrain_t2t_mini | sft_t2t_mini | toolcall | RLAIF |
|------|--------|-------------------|--------------|----------|-------|
| **minimind-3** | 64M | ≈1.21h / ≈1.57￥ | ≈1.10h / ≈1.43￥ | ≈0.9h / ≈1.17￥ | ≈1.1h / ≈1.43￥ |
| **minimind-3-moe** | 198M-A64M | ≈1.69h / ≈2.20￥ | ≈1.54h / ≈2.00￥ | ≈1.26h / ≈1.64￥ | ≈1.54h / ≈2.00￥ |

**pretrain + sft 跑 1 epoch：約 2.31 小時、約 3.0 元人民幣**，就能從 0 得到一個會對話的 `minimind-3 Zero`。

更誠實的是它**把 Zero 模型的對話樣本原樣貼出來**，包含爛掉的那一段：

```text
👶: Introduce the history of the United States, please.
🤖️: 您提到的"Introok's the believeations of theument." 這個名字來源於中國古代的"groty of of the change."
```

然後直接說「事實知識與泛化效果仍較有限，更適合作為 Zero 訓練路線可行性的早期參考」。**一個 61K★ 的專案願意把自己模型講胡話的輸出貼在 README 上，這件事本身就值得記一筆。**

## 已發布模型系譜

| 模型 | 參數量 | 發布 |
|------|--------|------|
| minimind-3 | 64M | 2026.04.01 |
| minimind-3-moe | 198M-A64M | 2026.04.01 |
| minimind2-small / minimind2-moe / minimind2 | 26M / 145M / 104M | 2025.04.26 |
| minimind-v1-small / -moe / -v1 | 26M / 4×26M / 108M | 2024.08–09 |

**兩年、三個世代**。從 v1 的 26M 到 minimind-3 的 64M，每一代都跟著當時的主流架構走。

## 模型結構：從 0 實現，但對齊 Qwen3 生態

`minimind-3` 是 Decoder-Only Transformer，整體配置**向 Qwen3 生態對齊**，方便轉到 `transformers / llama.cpp / ollama / vllm`：

- 預標準化（Pre-Norm）+ **RMSNorm**
- **SwiGLU** 激活
- **RoPE** 旋轉位置編碼，支援 **YaRN** 外推
- `q_heads=8`、`kv_heads=4`（GQA）、`max_position_embeddings=32768`、`rope_theta=1e6`

| Model | params | vocab | n_layers | d_model | kv_heads | q_heads |
|-------|--------|-------|----------|---------|----------|---------|
| minimind-3 | 64M | 6400 | 8 | 768 | 4 | 8 | 
| minimind-3-moe | 198M-A64M | 6400 | 8 | 768 | 4 | 8 |

> **這個設計取捨是這個專案最有教學價值的一段。** 作者引 [MobileLLM](https://arxiv.org/pdf/2402.14905) 的核心觀察：**參數量固定時，深度往往比寬度重要**——125M / 350M 規模下，30~42 層的「瘦高個」通常優於 12 層的「矮胖子」。
>
> 但 minimind-3 還是選了 `dim=768, n_layers=8` 這個相對矮胖的配置，理由講得很誠實：**更淺的網路訓練更快，同時 dim 不至於過小導致模式崩潰**——是訓練效率、穩定性與效果之間的**工程取捨**，不是照抄論文結論。**知道最佳解在哪、然後說明為什麼不選它**，這比直接給一個配置有用得多。

### MoE 的反直覺觀察

`minimind-3-moe` 用 **4 experts / top-1 routing**（去掉了 shared expert）。作者記了一個容易踩的坑：

> Experts 繼續增加後，**實際耗時往往比同尺寸規模的 dense 模型高非常多**，這和「MoE 推理更快」放在一起看會有點反直覺——但訓練時 token 先按專家分桶、再分別做 forward，**原生訓練時帶來的 kernel 啟停和調度開銷會急劇變重**。

要解決得靠 MoE kernel-fused 的算子庫（Triton 自訂 kernel、DeepSpeed-MoE、Megatron-LM）。但這個專案想保留原生 PyTorch 的普適性，所以做了現實折衷——**`4 experts / top-1` 這個甜點配置大約只比 dense 慢一點**。

## 訓練鏈路涵蓋範圍

這是專案真正的份量所在：

- **Pretrain → SFT → LoRA → RLHF-DPO → RLAIF（PPO / GRPO / CISPO）→ Tool Use → Agentic RL → 自適應思考 → 模型蒸餾**
- **關鍵訓練演算法與核心模組均從 0 實現，不依賴第三方框架封裝**
- 同時**相容** `transformers` / `trl` / `peft`，以及 `llama.cpp` / `vllm` / `ollama` / `Llama-Factory`
- 單機單卡與單機多卡（DDP、DeepSpeed），wandb / swanlab 視覺化，支援動態啟停
- 全階段開源資料（收集、蒸餾、清洗、去重後）
- Tokenizer 訓練碼，支援 `<tool_call>` / `<tool_response>` / `<think>` 模板標記
- 可在 C-Eval、C-MMLU、OpenBookQA 上評測
- OpenAI API 相容的極簡服務端（支援 `reasoning_content` / `tool_calls` / `open_thinking`），可接 FastGPT、Open-WebUI
- Streamlit 聊天 WebUI，支援思考展示與多輪 Tool Call

2026-04 那次更新還做了一件很有指標性的事：**移除獨立的 `train_reason.py`，思考能力統一由 `chat_template + <think>` 與 `open_thinking` 自適應開關控制**；`toolcall` 能力混進 SFT 主線資料，**預設 `full_sft` 就具備基礎 Tool Call**。這反映的是整個產業在 2025–2026 的收斂方向：**推理與工具呼叫從「額外訓練階段」變成「主線資料裡的一部分」。**

## 目前限制

- **64M 模型就是 64M 模型**。它的價值在學習，不在能力。README 自己貼出來的 Zero 對話樣本已經說明一切。
- **簡體中文為主**，README 極長（137 KB），資訊密度高但對不習慣的人門檻不低。
- **66 個 open issue**，以 61K★ 的體量算不多，但要注意回覆速度。
- **實驗性拓展（dLM、Linear Attention）放在 Discussions**，成熟度與主線不同，別當成正式功能。
- 訓練成本估算是**單卡 3090 的經驗值**，換硬體要自己重算——這點 README 有註明。

## 研究價值與啟示

### 關鍵洞察

1. **「3 塊錢 2 小時」不是噱頭，是降低門檻的設計目標。** 把訓練成本壓到一杯飲料以下，改變的不是技術，是**誰願意動手**。一個要花 500 美金才能跑完的教學專案，絕大多數人只會看不會做。**把門檻從「要不要投資」降到「要不要花兩小時」，是這個專案 61K★ 的真正原因。**

2. **「從 0 實現核心，但對齊主流生態」是教學專案的最佳架構。** 完全從 0 會變成學不到可遷移知識的玩具；完全用框架又學不到底層。MiniMind 的切法是：**演算法從 0 寫，但結構配置對齊 Qwen3，訓完能轉 transformers / ollama**。學的是原理，產出的是能用的東西。

3. **MoE 那段反直覺觀察比很多論文有用。** 「MoE 推理更快」是常識，但**原生 PyTorch 訓練時 token 按專家分桶會讓 kernel 啟停開銷急劇變重**——這種只有實際跑過才知道的坑，正是教學專案該記的東西。**它還說明了為什麼要有 DeepSpeed-MoE 這類東西**，把工具的存在理由講清楚了。

4. **引了 MobileLLM 的結論，然後說明為什麼不照做**。深度比寬度重要是論文結論，但在「要讓人兩小時跑完」這個約束下，淺而穩定才是對的選擇。**把約束講清楚再做取捨，比端出一個最佳配置更有教學價值。**

5. **願意貼出自己模型講胡話的輸出**。這跟本站 [ai-infra-book](ai-infra-book.md) 的「負結果與失敗嘗試按原協議完整保留，不改寫成成功」是同一種誠實。**教學材料展示失敗案例的價值，經常高於展示成功案例。**

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [《深入理解 AI Agent》](ai-agent-book.md) | 同為中文圈頂級開源教學資源；那本教 Agent 怎麼設計，這個教模型本身怎麼練出來 |
| [《深入理解 AI Infra》](ai-infra-book.md) | 互補的三層：MiniMind 教你**練模型**，AI Infra 教你**模型底下那台機器**，AI Agent 教你**模型上面怎麼用** |
| [ai-engineering-from-scratch](ai-engineering-from-scratch.md) | 同為 from-scratch 路線的學習資源 |
| [SkillOpt](skillopt.md) | 另一種「不動權重」的路線——MiniMind 從 0 訓權重，SkillOpt 訓自然語言技能。**兩端剛好框出「改變模型行為」的光譜** |
