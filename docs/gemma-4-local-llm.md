---
date: "2026-04-02"
category: "學習資源"
card_icon: "material-memory"
oneliner: "Google Gemma 4 模型全解析 + 2026 Local LLM 推論工具對比（Ollama / llama.cpp / vLLM / LM Studio）"
---

# Gemma 4 與 Local LLM 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| Google 官方公告 | [Gemma 4: Byte for byte, the most capable open models](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) |
| Google DeepMind 模型頁 | [Gemma 4 — Google DeepMind](https://deepmind.google/models/gemma/gemma-4/) |
| Latent Space 分析 | [AINews: Gemma 4](https://www.latent.space/p/ainews-gemma-4-the-best-small-multimodal) |
| 模型對比 | [Gemma 4 vs Qwen 3.5 vs Llama 4](https://ai.rs/ai-developer/gemma-4-vs-qwen-3-5-vs-llama-4-compared) |
| Local LLM 完整指南 | [Local LLM Inference in 2026](https://blog.starmorph.com/blog/local-llm-inference-tools-guide) |
| Ollama 部署指南 | [How to Run Gemma 4 Locally with Ollama](https://www.mindstudio.ai/blog/how-to-run-gemma-4-locally-ollama) |
| llama.cpp 部署 | [How to use Gemma 4 locally with llama.cpp](https://aiengineerguide.com/til/google-gemma-4-locally-llama-cpp/) |
| Ollama vs vLLM 效能 | [Ollama vs vLLM: Performance Benchmark 2026](https://www.sitepoint.com/ollama-vs-vllm-performance-benchmark-2026/) |
| AMD Day-0 支援 | [Day 0 Support for Gemma 4 on AMD](https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-gemma-4-on-amd-processors-and-gpus.html) |
| NVIDIA Edge 部署 | [Bringing AI Closer to the Edge with Gemma 4](https://developer.nvidia.com/blog/bringing-ai-closer-to-the-edge-and-on-device-with-gemma-4/) |

---

## Part 1：Gemma 4 模型概覽

### 基本資訊

Google DeepMind 於 **2026-04-02** 發佈 Gemma 4 — 四款開放權重模型，源自 Gemini 3 的同一研究基礎，採用 **Apache 2.0** 授權（無使用限制、無 MAU 上限）。

> **"Byte for byte, the most capable open models"**

### 四款模型規格

| 模型 | 參數量 | 活躍參數 | 架構 | Context | 模態 | 定位 |
|------|--------|---------|------|---------|------|------|
| **E2B** | - | 2.3B | Dense | 128K | 文字 + 圖片 + 音訊 | 手機/IoT edge |
| **E4B** | - | 4.5B | Dense | 128K | 文字 + 圖片 + 音訊 | 平板/edge |
| **26B-A4B** | 26B total | **3.8B active** | MoE (128 experts, 8+1 per token) | 256K | 文字 + 圖片 | 效率最佳 |
| **31B** | 31B | 31B | Dense | 256K | 文字 + 圖片 | 品質最佳 |

### 架構特點

- **Sliding-window + Global attention 交替**：local 層用 512-1024 tokens sliding window，global 層用 full-context attention
- **Proportional RoPE**：global 層啟用，實現 256K context 無品質衰減
- **QK norm + V norm**：無顯式 attention scale
- **KV cache sharing**：跨層共享，降低記憶體佔用
- **Softcapping**：穩定訓練

### Benchmark 成績

#### Gemma 3 27B → Gemma 4 對比

| Benchmark | Gemma 3 27B | Gemma 4 31B | Gemma 4 26B-A4B | 提升幅度 |
|-----------|------------|-------------|-----------------|---------|
| **MMLU Pro** | 67.6% | **85.2%** | 82.6% | +26% |
| **GPQA Diamond** | 42.4% | **84.3%** | 82.3% | +99% |
| **BigBench Extra Hard** | 19.3% | **74.4%** | 64.8% | +285% |
| **AIME 2026** | 20.8% | **89.2%** | 88.3% | +329% |
| **LiveCodeBench v6** | 29.1% | **80.0%** | 77.1% | +175% |
| **Codeforces ELO** | 110 | **2150** | 1718 | +1855 |
| **MMMU Pro (Vision)** | 49.7% | **76.9%** | 73.8% | +55% |
| **MATH-Vision** | 46.0% | **85.6%** | 82.4% | +86% |

#### Arena AI 排名

| 排名 | 模型 | ELO |
|------|------|-----|
| #3 | Gemma 4 31B Dense | 1452 |
| #6 | Gemma 4 26B-A4B MoE | 1441 |

> 26B-A4B 只用 3.8B active parameters 就達到 31B 的 97% 品質，Arena 排名僅差 11 分。

### 與競品對比

| 面向 | Gemma 4 31B | Qwen 3.5 27B | Llama 4 Maverick |
|------|-------------|-------------|-----------------|
| **授權** | Apache 2.0 ✅ | Apache 2.0 ✅ | 自訂（700M MAU 限制）❌ |
| **數學推理** | **89.2%** AIME | - | - |
| **程式碼** | 80.0% LiveCodeBench | **72.4%** SWE-bench Verified | - |
| **多語言** | 一般 | **250K 詞彙、201 語言** | 一般 |
| **Vision** | ✅（全系列） | ✅（Omni 支援影片+語音輸出） | ✅ |
| **Edge 模型** | ✅（E2B 2.3B, E4B 4.5B） | ❌ | ❌（最小 17B active） |
| **最大 Context** | 256K | 131K | 10M（Scout） |
| **部署門檻** | 消費級 GPU/Mac | 消費級 GPU/Mac | 資料中心級 |

**選擇建議**：

- **Gemma 4** — 最佳品質/參數比、真開源、edge 部署
- **Qwen 3.5** — coding 工作流、多語言
- **Llama 4** — 需要最大規模開放模型、可接受授權限制

---

## Part 2：2026 Local LLM 推論工具生態

### 工具對比總覽

```
使用者經驗
  初學者 ────── 中級 ────── 進階 ────── 專家
  LM Studio     Ollama      llama.cpp    vLLM
  GPT4All       Jan.ai      MLX          Exo
  KoboldCpp     LocalAI
```

### 主要工具對比

| 工具 | 介面 | 最佳場景 | 優勢 | 限制 |
|------|------|---------|------|------|
| **Ollama** | CLI | 開發者本地測試 | 一行安裝、OpenAI API 相容、最大模型庫（166K stars） | 僅 GGUF、無 GUI、略高 overhead |
| **llama.cpp** | CLI | 進階用戶、edge 部署 | 基礎引擎、最大平台支援、最佳 CPU 效能（98.6K stars） | 學習曲線陡 |
| **vLLM** | Python API | 生產部署、多用戶服務 | PagedAttention（記憶體碎片 -50%）、最高吞吐量（741 tok/s AWQ） | Linux only、需獨立 GPU |
| **LM Studio** | GUI | 初學者、模型評估 | 一鍵下載、Split-view 對比、MLX Mac 優化 | 閉源（個人免費）、無 EXL2/GPTQ |
| **Jan.ai** | GUI | 隱私優先 | 100% 離線、混合 local/cloud 切換（41.1K stars） | 較年輕、社群小 |
| **LocalAI** | API | 取代 OpenAI API | 完整 drop-in OpenAI 替代、支援文字/圖片/語音 | 設定複雜、資源需求高 |
| **MLX** | Framework | Apple Silicon 原生開發 | 零 CPU-GPU 資料複製、混合精度量化、M5 Neural 加速 | macOS only、需 Swift 知識 |
| **Exo** | CLI | 多設備分散推論 | P2P 跨設備拆分模型、示範 671B 跨 Mac cluster | Alpha 狀態、網路瓶頸 |

### 推薦工作流

```
LM Studio（評估模型）→ Ollama（本地開發）→ vLLM（生產部署）
```

### 硬體需求

#### 按模型大小（Q4 量化）

| 模型大小 | 最低記憶體 | 舒適記憶體 |
|---------|----------|----------|
| 3B | 4 GB | 6 GB |
| 7-8B | 6 GB | 10 GB |
| 13-14B | 10 GB | 16 GB |
| **30-34B** | **20 GB** | **32 GB** |
| 70B | 40 GB | 64 GB |
| 100B+ | 64 GB | 128 GB+ |

#### 量化對品質的影響（7B 模型範例）

| 格式 | Bits | 檔案大小 | 品質保留 | 建議 |
|------|------|---------|---------|------|
| Q8_0 | 8-bit | ~7.5 GB | ~99% | 近無損 |
| Q6_K | 6-bit | ~5.5 GB | ~97% | 高品質 |
| Q5_K_M | 5-bit | ~4.8 GB | ~95% | |
| **Q4_K_M** | **4-bit** | **~4.0 GB** | **~92%** | **推薦甜蜜點** |
| Q3_K_M | 3-bit | ~3.2 GB | ~85% | 品質開始下降 |
| Q2_K | 2-bit | ~2.5 GB | ~75% | 僅緊急用 |

#### GPU 優化格式（NVIDIA）

| 格式 | Bits | 品質 | 速度 | 最佳場景 |
|------|------|------|------|---------|
| AWQ | 4-bit | ~95% | 741 tok/s | NVIDIA 最佳 |
| GPTQ | 4-bit | ~90% | 712 tok/s | 舊系統 |
| EXL2 | 2-8 mixed | 可變 | 最快 | 單用戶 |
| FP8 | 8-bit | ~99% | 很快 | 高品質需求 |
| NVFP4 | 4-bit | ~92% | 最快 | Blackwell GPU |

#### 按預算的推薦硬體

| 預算 | 硬體 | 能力 |
|------|------|------|
| $0 | 現有機器 + Ollama | 3-7B models |
| $375 | 二手 M1 Mac (16GB) | 7B models |
| $599 | Mac Mini M4 (24GB) | 7-14B models |
| $900 | 二手 RTX 3090 | 7-13B GPU 速度 |
| **$1,999** | **Mac Mini M4 Pro (48GB)** | **70B models（最佳性價比）** |
| $2,000 | 二手 RTX 4090 | 13B 快、70B 量化 |
| $3,500+ | RTX 5090 / M4 Max | 70B 快、frontier 等級 |

> **核心原則：LLM 推論的瓶頸是記憶體頻寬，不是算力。**

---

## Part 3：Gemma 4 本地部署實戰

### Ollama（最簡單）

```bash
# 安裝
brew install ollama  # macOS
# 或 curl -fsSL https://ollama.com/install.sh | sh  # Linux

# 拉取模型
ollama pull gemma4:4b       # E4B edge（推薦入門）
ollama pull gemma4:26b-moe  # 26B MoE（效率最佳）
ollama pull gemma4:31b      # 31B Dense（品質最佳）

# 互動
ollama run gemma4:26b-moe

# API 服務
ollama serve  # 預設 http://localhost:11434
```

### llama.cpp（進階控制）

```bash
# 安裝
brew install llama.cpp  # macOS

# 啟動 server（自動下載 GGUF）
llama-server -hf ggml-org/gemma-4-E4B-it-GGUF:Q8_0

# 帶 Vision（需額外下載 mmproj）
llama-server \
  -hf ggml-org/gemma-4-31B-it-GGUF:Q4_K_M \
  --mmproj ggml-org/gemma-4-31B-it-mmproj-GGUF
```

### 接入 Coding Agent

```bash
# OpenHarness（支援 OpenAI-compatible API）
oh provider add ollama-gemma4 \
  --provider openai \
  --api-format openai \
  --base-url http://localhost:11434/v1 \
  --model gemma4:26b-moe

# Claude Code（透過 MCP 或 API proxy）
# Gemma 4 可作為 OpenAI-compatible backend
```

## 目前限制 / 注意事項

### Gemma 4 限制

- **31B Dense 需要 ~20GB+ VRAM**（Q4 量化），消費級 GPU 勉強、Mac 48GB 舒適
- **Vision 需要額外下載 mmproj 檔案**，設定比純文字多一步
- **Audio 僅 E2B/E4B 支援**，大模型不支援音訊輸入
- **中文能力未特別強調**：Qwen 3.5 在多語言方面更強（250K 詞彙、201 語言）
- **MoE 模型的 KV cache 問題**：llama.cpp 的 KV cache 在 MoE 模型上有已知 bug，需注意版本

### Local LLM 通用限制

- **品質差距仍然存在**：即使是 Gemma 4 31B，在複雜 coding 和長上下文推理上仍不及 Claude Opus / GPT-5.4
- **量化品質損失**：Q4 量化保留 ~92% 品質，某些任務（數學、推理）可能更敏感
- **記憶體頻寬是真正瓶頸**：CPU 推論速度受限於 RAM 頻寬，Mac 的統一記憶體架構在此有優勢
- **長 context 推論慢**：256K context 在本地推論時 prefill 時間顯著增加

## 研究價值與啟示

### 關鍵洞察

1. **26B-A4B MoE 是 2026 本地 LLM 的甜蜜點** — 只有 3.8B active parameters 卻達到 31B 的 97% 品質，Arena 排名 #6。這意味著在 ~16GB 記憶體的設備上就能跑接近 frontier 品質的模型。MoE 架構正在讓「小設備跑大模型」成為現實。

2. **Apache 2.0 授權是戰略性決定** — Google 放棄了任何使用限制（對比 Llama 4 的 700M MAU 上限），直接與 Qwen 3.5 的授權看齊。這讓 Gemma 4 成為商業產品的首選開放模型。對於 OpenHarness、Copilot Ralph 等多 Provider Agent 工具來說，Gemma 4 是最安全的本地選項。

3. **`LM Studio → Ollama → vLLM` 的漸進式工作流成為業界共識** — 評估用 GUI、開發用 CLI、生產用高效能引擎。這個分層對應了不同的技術深度和規模需求，也解釋了為什麼市場上能共存這麼多推論工具。

4. **Mac M4 Pro 48GB ($1,999) 成為最佳性價比選擇** — 統一記憶體架構讓 Mac 在 LLM 推論上有獨特優勢（零 CPU-GPU 資料複製），能舒適運行 70B 模型。M2 Ultra 甚至能跑 Gemma 4 31B 達到 ~300 tok/s。這讓「本地 AI 工作站」的門檻大幅降低。

5. **Edge 模型（E2B/E4B）+ 音訊輸入是獨特賣點** — Gemma 4 是唯一在 2-5B 參數級別同時支援文字+圖片+音訊的開放模型。這開啟了手機端 AI Agent 的可能性，是 Llama 4 和 Qwen 3.5 都沒有的能力。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [OpenHarness](open-harness.md) | OpenHarness 的多 Provider 支援讓 Gemma 4 可作為 Ollama backend 直接使用，是 Anthropic API 的免費替代方案 |
| [Copilot Ralph](copilot-ralph.md) | 同樣支援 BYOK 多 Provider，Gemma 4 可作為 OpenAI-compatible backend 接入 |
| [Karpathy LLM Wiki](karpathy-llm-wiki.md) | LLM Wiki 的 qmd 搜尋工具使用 node-llama-cpp + GGUF 進行本地 LLM re-ranking，Gemma 4 E4B 是理想的本地 re-ranker |
| [MemPalace](mempalace.md) | MemPalace 的零 LLM 寫入路徑可與 Gemma 4 結合 — 用本地模型做讀取和搜尋，完全離線 |
| [LLM Course](llm-course.md) | Local LLM 部署是 LLM 課程的實戰延伸 |
