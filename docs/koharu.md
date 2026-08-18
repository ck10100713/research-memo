---
date: "2026-08-18"
category: "AI 應用"
card_icon: "material-translate"
oneliner: "Rust 寫的本機優先漫畫翻譯器,把偵測→OCR→修復→翻譯→排版→PSD 匯出串成 staged ML pipeline;更關鍵的是內建一個 in-process、OAuth 打 ChatGPT Codex backend 的 agent,用 function-calling tool + revision-safe 編輯驅動整個翻譯專案"
tags:
  - agent
  - rust
  - local-llm
---

# Koharu 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/mayocream/koharu> |
| 官網 / 文件 | <https://koharu.rs> |
| 模型（HuggingFace） | <https://huggingface.co/mayocream> |

## 專案概述

**Koharu** 是一個用 **Rust** 寫的**本機優先漫畫翻譯器**（ML-powered manga translator）。它把漫畫翻譯這條 workflow 用機器學習自動化:**物件偵測 + OCR + inpainting + LLM** 串成一條 pipeline,把日文漫畫的對白/旁白抓出來、翻掉、把原字塗掉、再把譯文排回頁面。作者 mayocream,2025-04 建立、5.3k stars、343 forks、2000+ commits,active development,雙授權 MIT / Apache-2.0,文件有 日/簡中/英 三語。

它最強調的一句話是:**vision 模型和 LLM 預設全部跑在你自己機器上**,資料不離開本機。GPU 走 CUDA / ROCm-HIP / Metal / Vulkan,永遠有 CPU fallback;前端是 WebGPU-based GUI。裝法:WinGet（Windows）、Homebrew（macOS）或直接下載 release binary。

> 對這個以 AI agent 為主題的研究站來說,Koharu 最值得記的**不是**翻譯功能本身,而是它內建的 **Koharu Agent**──一個直接打 ChatGPT Codex backend、用 function-calling tool 操作整個翻譯專案的 in-process agent（見下)。

## Staged ML Pipeline

Koharu 刻意**不用單一大模型解整頁**,而是分階段、每階段用專用模型:

```
偵測/版面  →  OCR  →  Inpainting  →  翻譯(LLM)  →  文字排版  →  PSD 匯出
(找文字區/       (認原文)   (塗掉原字)      (本機或雲端)    (直排 CJK / RTL)  (分層可編輯)
 對話框/mask)
```

## 模型堆疊

**Computer Vision**

| 階段 | 模型 |
|------|------|
| 偵測 / 版面分割 | Koharu Layout **RF-DETR Seg 2XL**（作者自訓,HF: `mayocream/koharu-layout-rfdetr-seg-2xl-1152`） |
| OCR | **PaddleOCR-VL 1.6**、**Manga OCR**、**Baberu OCR** |
| Inpainting（塗字） | **FLUX.2 Klein**、**RORem mixed**、**LaMa（manga 版）**、**AOT GAN** |

**Large Language Models（翻譯,可本機可雲端）**

- **本機通用**:LFM 2.5、Ministral 3、Gemma 4（E2B~31B 多尺寸）、Qwen 3.5/3.6/3.8（0.8B~35B-A3B）── 全 GGUF。
- **本機 uncensored**:Gemma 4 / Qwen 系列的無審查版（漫畫常有成人內容,這是實務需求）。
- **雲端 API**:OpenAI、Claude、Gemini、Grok、DeepSeek、MiniMax、Atlas Cloud、OpenRouter。
- **純機器翻譯**:DeepL、Google Cloud Translation、Caiyun。
- 另支援任意 **OpenAI-compatible** 端點。

## Rust Monorepo(23 crates)

整個系統拆成 23 個 crate,層次分明:

| 群組 | crates |
|------|--------|
| **Agent** | `koharu-agent`（in-process Codex agent,見下) |
| **Pipeline / ML** | `koharu-pipeline`、`koharu-ml`、`koharu-diffusion`(+`-sys`)、`koharu-llama`(+`-sys`)、`koharu-torch`(+`-sys`)、`koharu-translator` |
| **渲染 / 畫布** | `koharu-canvas`、`koharu-renderer`、`koharu-rasterizer`、`koharu-scene`、`koharu-psd`（分層匯出） |
| **App / 桌面** | `koharu-app`、`koharu-desktop`、`koharu`、`koharu-bindgen` |
| **基礎** | `koharu-runtime`、`koharu-storage`、`koharu-config`、`koharu-secrets` |

`-sys` crate（`diffusion-sys` / `llama-sys` / `torch-sys`)是 FFI 綁定層,底層靠 LLVM / Ninja / Bun 建。

## Koharu Agent(本站重點)

`koharu-agent` 的 `lib.rs` 開宗明義:**「Koharu's in-process, OAuth-backed Codex agent.」** 拆開來看:

- **直接打 ChatGPT Codex backend**:`codex/mod.rs` 裡 `RESPONSES_URL = https://chatgpt.com/backend-api/codex/responses`──不是 OpenAI 公開 API,而是 **Codex 的 responses 端點**,靠 OAuth 登入（`auth.rs` device-code flow + `token_store.rs`）吃**使用者的 ChatGPT 訂閱 quota,完全不用 API key**。這正是 [Slide Editor](slide-editor.md) 記過的「把訂閱/CLI 當 backend」模式,但這裡是**用 Rust in-process 直接重刻 Codex 協定**(有自己的 `protocol.rs` / `stream.rs` / `catalog.rs`)。

- **agent 是專案操作員,不是聊天機**。system prompt(`agent.rs` 的 `INSTRUCTIONS`)把它定義成「operating a manga translation project inside Koharu」,重點規則:
  - 每個 user turn 都附一個 **`koharu_project_context` block**（完整專案狀態),但**刻意不放頁面圖**──要看圖才呼叫 `view_page`,且只看相關頁。**這是 token 經濟:預設餵最小狀態、視覺資訊按需載入。**
  - **「All project changes are revisioned and reversible. Do not ask for permission.」**──所有修改可版本化、可回溯,所以 agent 不必問許可就動手。
  - 「Never claim a change succeeded unless its tool result says it succeeded.」「Do not invent entity identifiers.」──明確反幻覺、反瞎編 ID。
  - 不出計畫、不露內部步驟,持續呼叫 tool 直到完成。

- **function-calling tool 介面**（`tool.rs`）:`Tool { type:"function", name, description, parameters(JSON schema), strict }`,`ToolCall { call_id, name, arguments }`,`Invocation` 帶 `changed` 旗標與 `ToolImage`(以 `data_url` 回傳圖)。等於把「檢視/修改翻譯專案」的每個動作做成型別化 function tool 給 LLM 呼叫。

## 目前限制與注意事項

- **重度桌面應用、build 門檻高**:Rust 2024 + LLVM + Ninja + Bun + 多 GPU backend + 20+ crate,不是 clone 就跑,一般人走 release binary。
- **本機跑大模型吃資源**:預設本機推論,要好效果得有能跑 GGUF 大模型的 GPU;CPU fallback 慢。
- **Agent 綁 ChatGPT Codex OAuth**:agent 路徑吃的是 ChatGPT 訂閱,非官方公開端點,存在被上游調整的風險（翻譯本身仍可走一般雲端 API 或純本機 LLM,不受影響）。
- **內容合法性**:內建 uncensored 模型與漫畫翻譯情境,使用需自負版權/內容責任。

## 研究價值與啟示

### 關鍵洞察

1. **「訂閱當 backend」被推到極致:in-process 重刻 Codex 協定**。slide-editor 是 shell out `codex` CLI;Koharu 更進一步,在 Rust 裡直接對 `chatgpt.com/backend-api/codex/responses` 說話,自己實作 auth / token store / streaming / protocol。**對桌面 app 來說,「不要求使用者填 API key、直接吃他的 ChatGPT 訂閱」是巨大的 onboarding 優勢**,代價是綁定非公開端點的維護風險。這個取捨值得記進「AI 桌面工具的 backend 選型」清單。

2. **agent 操作結構化專案的三件套,和 [OpenSlideX](open-slidex.md) 幾乎同構**:(a) 每回合餵**最小專案狀態**、重資產(圖)按需載入(`view_page` ↔ OpenSlideX 的 `open_slidex_read`);(b) **所有修改 revisioned & reversible**,所以 agent「不必問許可」(↔ OpenSlideX 的 `expectedRevision` 樂觀鎖);(c) **型別化 function tool** 當唯一動作介面。兩個完全不同領域(漫畫翻譯 vs 簡報)、不同技術棧(Rust in-process vs TS MCP)的工具,竟收斂到同一組「讓 agent 安全改結構化文件」的設計原則──**這組原則正在變成 agent-native app 的事實標準**。

3. **staged pipeline > 單一大模型**:Koharu 不賭「一個 VLM 解整頁」,而是偵測/OCR/inpaint/翻譯各用最合適的專用模型,每階段可替換(光 OCR 就 3 個、inpaint 4 個、LLM 數十個)。對真實產品,**可組合、可替換的多模型 pipeline 比單一 end-to-end 模型更好調、更好維護、品質更可控**。

4. **local-first 是隱私 + 成本雙贏**:vision 模型與 LLM 預設全本機,漫畫內容(常涉版權/成人)不外流;雲端 API 是選配而非必須。搭配多 GPU backend + CPU fallback,把「隱私敏感的 AI 應用」做成可完全離線。

### 與其他研究筆記的關聯

- **[Slide Editor](slide-editor.md)**:同樣「把 `codex`/訂閱當 AI backend、免 API key」;slide-editor shell out CLI,Koharu 在 Rust 裡直接重刻 Codex responses 協定,是同一模式的兩種深度。
- **[OpenSlideX](open-slidex.md)**:最強的結構對照──兩者都用「最小狀態 read + revision-safe edit + function tool」讓 agent 安全操作結構化專案,一個 MCP/TS、一個 in-process/Rust。
- **[LiteLLM](litellm.md)**:Koharu 的翻譯層支援數十家雲端 + OpenAI-compatible 端點,和 LiteLLM「統一多 provider」是同一需求的 app 內建版。
- **[Gemma 4 與 Local LLM](gemma-4-local-llm.md)**:Koharu 大量用 Gemma 4 / Qwen 的 GGUF 本機模型跑翻譯,是 local-LLM 落地到消費級應用的實例。
