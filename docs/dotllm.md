---
date: "2026-04-15"
category: "學習資源"
card_icon: "material-language-csharp"
oneliner: "用純 C#/.NET 10 從零打造 LLM 推論引擎 — Zero-GC、SIMD、CUDA、Paged KV-cache"
---

# dotLLM 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 部落格文章 | [Introducing dotLLM](https://kokosa.dev/blog/2026/dotllm/) |
| GitHub Repo | [kkokosa/dotLLM](https://github.com/kkokosa/dotLLM) |
| 官網 | [dotllm.dev](https://dotllm.dev/) |

**作者：** Konrad Kokosa — .NET 效能專家

**專案狀態：** ⭐ 183 stars · C# · GPLv3 · v0.1.0-preview.2 · 實驗性專案

## 專案概述

dotLLM 是一個**完全用純 C#/.NET 10 原生實作的 LLM 推論引擎**——不是 llama.cpp 的包裝器，不依賴 Python。從 GGUF 模型載入、tokenization、attention、sampling 到 CPU/GPU compute 全部用 C# 實作。

同時也是一個 AI 輔助開發實驗：大量使用 Claude Code、Gemini、Codex 等 coding agent，探索人類領域專家主導下 AI 工具能把系統級專案推進到什麼程度。

## 技術架構

```
┌─────────────────────────────────────────┐
│            DotLLM.Server                │  ASP.NET OpenAI-compatible API
├─────────────────────────────────────────┤
│            DotLLM.Engine                │  KV-cache, scheduler, samplers
├──────────┬──────────┬───────────────────┤
│ DotLLM.  │ DotLLM.  │ DotLLM.Cpu/Cuda   │  GGUF, BPE/SPM, SIMD/CUDA
│ Models   │Tokenizers│                   │
├──────────┴──────────┴───────────────────┤
│            DotLLM.Core                  │  Interfaces, tensor types
└─────────────────────────────────────────┘
```

### 效能亮點

| 技術 | 說明 |
|------|------|
| Zero-GC 推論 | `NativeMemory.AlignedAlloc`（64-byte 對齊），hot path 零 GC |
| SIMD 向量化 | AVX2/AVX-512 處理量化矩陣乘法、RMSNorm、RoPE |
| Memory-mapped | GGUF 模型毫秒級載入 |
| 量化 | FP16、Q8_0、Q4_K_M |
| Paged KV-cache | PagedAttention + prefix caching + copy-on-write |
| Speculative decoding | draft-verify-accept + KV-cache rollback |
| Structured output | FSM/PDA-based 約束解碼，保證合法 JSON/Schema/regex |
| CUDA backend | PTX kernels + CUDA Driver API，CPU/GPU 混合 offloading |

## 快速開始

```bash
# .NET 全域工具安裝
dotnet tool install -g DotLLM.Cli --prerelease

# 下載模型
dotllm model pull QuantFactory/SmolLM-135M-GGUF

# 單次生成
dotllm run QuantFactory/SmolLM-135M-GGUF -p "The capital of France is" -n 64

# 互動聊天
dotllm chat QuantFactory/SmolLM-135M-GGUF

# OpenAI-compatible API + Web UI
dotllm serve QuantFactory/SmolLM-135M-GGUF  # http://localhost:8080
```

支援模型：Llama、Mistral、Phi、Qwen、DeepSeek

## 目前限制 / 注意事項

- **實驗性質** — 明確標示不適合生產環境，預期有 breaking changes
- **GPLv3 授權** — 商業整合有傳染性授權限制
- **吞吐量不及 llama.cpp** — 差距在縮小但仍落後
- **CUDA 效能未成熟** — 小模型因 launch overhead 反而比 CPU 慢
- **模型支援有限** — 僅 5 個架構家族
- **需要 .NET 10** — 相當新的 runtime
- **Speculative decoding 僅 greedy mode**

## 研究價值與啟示

### 關鍵洞察

1. **「用你最熟悉的語言從零打造」是最好的學習方式。** Kokosa 是 .NET 效能專家，用 C# 而非 Python 重寫 LLM 推論——這迫使他理解每個底層細節（記憶體對齊、SIMD 指令、CUDA kernel），而不是靠 PyTorch 抽象層。

2. **Zero-GC 推論展示了 C# 的系統級能力。** 用 `NativeMemory` + `Span<T>` + `stackalloc` 達到接近 C/C++ 的效能——打破了「.NET 不適合做系統程式」的偏見。

3. **AI 輔助開發系統級專案的真實案例。** 整個專案大量使用 Claude Code 和 Codex——不是寫 CRUD，而是寫 CUDA kernel 和 SIMD 向量化。這為「AI 能否寫複雜系統」提供了正面數據。

### 與其他專案的關聯

- **vs Gemma 4 / Local LLM（筆記庫中）：** Gemma 是跑在別人引擎上的模型，dotLLM 是引擎本身。如果你想了解 LLM 推論的底層運作，dotLLM 的原始碼比讀論文更直觀。
- **vs AI Engineering from Scratch：** 那是「教你 AI」的課程，dotLLM 是「用 AI 幫你寫 AI 引擎」的實戰案例。Phase 10（LLMs from Scratch）的終極實踐版。
