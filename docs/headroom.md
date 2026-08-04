---
date: "2026-08-04"
category: "Coding Agent 工具"
card_icon: "material-arrow-collapse-horizontal"
oneliner: "AI Agent 的 context 壓縮層：在 tool 輸出、log、RAG chunk 進入 LLM 前壓縮，JSON 省 60–95%、coding agent 省 15–20%，且可逆還原"
tags:
  - llm-gateway
  - mcp
  - rag
  - prompt-engineering
---

# Headroom 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/headroomlabs-ai/headroom> |
| 官方文件 | <https://headroom-docs.vercel.app/docs> · <https://docs.headroomlabs.ai/docs> |
| PyPI（`headroom-ai`） | <https://pypi.org/project/headroom-ai/> |
| npm（TypeScript SDK） | <https://www.npmjs.com/package/headroom-ai> |
| HuggingFace 模型 | <https://huggingface.co/chopratejas/kompress-v2-base> |
| 第三方評測 | [silenceper](https://silenceper.com/en/article/2026-06-14-headroom-ai-agent-context-compression/) · [AlphaMatch](https://www.alphamatch.ai/blog/headroom-context-compression-ai-agents-2026) · [Tosea.ai 教學](https://tosea.ai/blog/how-to-use-headroom-context-compression-guide) |

> Metadata（研究當下）：**64.4k stars** · Python + Rust · Apache 2.0 · 最新 release `v0.33.0`（2026-07-29）· 建立於 2026-01-07。
> Repo 已從個人帳號 `chopratejas` 搬到組織 `headroomlabs-ai`（README badge 仍指向舊 URL），走 **open-core** 商業模式：OSS 免費本地版 + 付費 org 部署／代管。

## 專案概述

**Headroom 是一個「context 壓縮層」**：把 AI agent 會讀到的所有東西——tool 輸出、log、RAG chunk、檔案、對話歷史——在送進 LLM **之前**先壓縮，號稱「same answers, fraction of the tokens」。它解決的痛點是 agentic workflow 裡最貴的一環：coding agent 每一步都塞大量 tool 輸出（`grep` 結果、檔案、堆疊追蹤、JSON API 回應）進 context window，token 成本與 latency 隨之爆炸。

它的定位不是「另一個 agent 框架」，而是一層**放在 agent 與 LLM provider 之間的中介**。核心賣點有三：

1. **content-aware（內容感知）**——不是無腦截斷，而是先偵測內容型別（JSON / 程式碼 / 純文字 / 圖片），再選對應的壓縮器。
2. **reversible（可逆）**——原文快取在本地，LLM 需要時可透過 `headroom_retrieve` 工具把原文叫回來（稱為 CCR, Cache-and-Compress-Reversibly）。
3. **local-first（本地優先）**——壓縮全在你機器上跑，資料不外流；這也是它跟 Compresr、Token Co. 這類「把文字送到它們 API」的競品最大差異。

官方公布的實測數字（見下方 Proof 表）宣稱 JSON 省 60–95%、coding agent 整體省 15–20%，而 GSM8K / TruthfulQA / SQuAD / BFCL 等 benchmark 準確度幾乎不掉甚至微升。

## 核心架構

Headroom 在本地跑一條 pipeline，request 依序經過各個 transform：

```
 你的 agent / app  (Claude Code, Cursor, Codex, LangChain, Agno, Strands, 自己的程式…)
      │  prompts · tool 輸出 · logs · RAG 結果 · files
      ▼
 ┌────────────────────────────────────────────────┐
 │  Headroom（本地執行，資料留在你機器）           │
 │  CacheAligner → ContentRouter → CCR            │
 │                  ├─ SmartCrusher   (JSON)      │
 │                  ├─ CodeCompressor (AST)       │
 │                  └─ Kompress-v2-base (text)    │
 │  Cross-agent memory · headroom learn · MCP     │
 └────────────────────────────────────────────────┘
      │  壓縮後的 prompt  +  retrieval 工具
      ▼
 LLM provider（Anthropic · OpenAI · Bedrock · …）
```

| 元件 | 職責 |
|------|------|
| **ContentRouter** | 偵測內容型別，挑選對應壓縮器 |
| **SmartCrusher** | 通用 JSON 壓縮：dict 陣列、巢狀物件、混合型別 |
| **CodeCompressor** | AST 感知，支援 Python / JS·TS / Go / Rust / Java / C·C++ / Perl |
| **Kompress-v2-base** | 自家 HuggingFace 模型，用 agentic traces 訓練，壓純文字散文 |
| **CacheAligner** | **只偵測、不改寫**——警告會打斷 provider KV cache 前綴的 volatile 內容 |
| **CCR** | 把原文存本地，LLM 用 `headroom_retrieve` 按需取回 |
| **Live-zone compression** | 只壓「新 bytes」（最新 tool 輸出、當前 turn），frozen 前綴保持 byte 完全一致，避免 bust 掉 provider cache；歷史永不丟棄 |

### 四種接入方式

| 模式 | 用法 | 特性 |
|------|------|------|
| **Library** | `from headroom import compress` / `await compress(messages, {model})` | 內嵌任何 app，Python 與 TypeScript |
| **Proxy** | `headroom proxy --port 8787` | 零程式碼改動，任何語言、任何 OpenAI 相容 client |
| **Agent wrap** | `headroom wrap claude\|codex\|cursor\|aider\|copilot…` | 一行包住 coding agent；`headroom unwrap <tool>` 還原 |
| **MCP server** | `headroom mcp install` | 暴露 `headroom_compress` / `headroom_retrieve` / `headroom_stats` |

### 兩個獨立的節流方向

Headroom 少見地**同時**處理「送出」與「寫回」兩端的 token：

- **Input compression**（送出）——上面整條 pipeline，壓你送進去的 prompt。
- **Output token reduction**（寫回，`HEADROOM_OUTPUT_SHAPER=1`）——Opus 級模型 output 是 input 的 5×，Headroom 從 proxy 端剪掉「Great, let me…」開場白、重印你剛給的程式碼、routine 步驟的深度 thinking。手法是 **verbosity steering**（在 system prompt **尾端**追加簡短「別複述」提示，保住 prompt cache）＋ **effort routing**（turn 只是模型讀完 tool 結果後接續時，把 thinking effort 調低；新問題與錯誤維持全 effort）。因為看不到模型「原本會寫什麼」，output 節省是**反事實估計**，誠實給出信賴區間（`31.7% (95% CI 27.7…35.7%) [estimated]`），也可留 10% 對照組換取 `measured` 數字。

## Proof（官方實測）

**真實 agent workload 上的節省：**

| Workload | Before | After | 省 |
|----------|-------:|------:|---:|
| Code search（100 筆結果） | 17,765 | 1,408 | **92%** |
| SRE 事故除錯 | 65,694 | 5,118 | **92%** |
| GitHub issue triage | 54,174 | 14,761 | **73%** |
| Codebase 探索 | 78,502 | 41,254 | **47%** |

**標準 benchmark 上準確度不掉：**

| Benchmark | 類別 | N | Baseline | Headroom | Delta |
|-----------|------|--:|---------:|---------:|-------|
| GSM8K | Math | 100 | 0.870 | 0.870 | **±0.000** |
| TruthfulQA | Factual | 100 | 0.530 | 0.560 | **+0.030** |
| SQuAD v2 | QA | 100 | — | **97%** | 19% 壓縮 |
| BFCL | Tools | 100 | — | **97%** | 32% 壓縮 |

> 復現：`python -m headroom.evals suite --tier 1`。數字均來自官方 README，尚未見獨立第三方復現。

## 快速開始

```bash
# 1 — 安裝（CLI 只從 PyPI 出；npm 版是 library-only，沒有 headroom CLI）
uv tool install --python 3.13 "headroom-ai[all]"   # CLI 裝進隔離環境（建議）
pip install "headroom-ai[all]"                      # Python，含 headroom CLI
npm install headroom-ai                             # TypeScript SDK（僅 library）

# 2 — 選模式
headroom wrap claude          # 包住 coding agent（會順帶裝 Serena 做語意導航）
headroom proxy --port 8787    # drop-in proxy，零程式碼改動

# 3 — 驗證與看省了多少
headroom doctor               # 健康檢查，確認 routing 有作用
headroom dashboard            # 即時節省儀表板（需 proxy 在跑）
```

- 需要 **Python 3.10+**；顆粒化 extras：`[proxy]` `[mcp]` `[ml]` `[code]` `[memory]` `[vector]` `[image]` `[langchain]` `[agno]` 等。
- **建議選 3.13**：dashboard 的「Proxy $ Saved」用 LiteLLM 計價，而 LiteLLM 裝不上 Python 3.14+，3.14 上 token 省仍算得出來但金額會停在 `$0.00`。
- Agent 相容矩陣涵蓋 Claude Code、Codex、Grok CLI、Cursor、Aider、Copilot CLI、VS Code Copilot、Cline、Continue、Goose、OpenHands、OpenCode 等十多個；任何 OpenAI 相容 client 都能透過 proxy 接。

## 目前限制 / 注意事項

- **本地程序依賴**：sandbox / 無法跑 local process 的環境不適用（官方自己列在「Skip it if…」）。
- **平台 wheel 覆蓋不齊**：原生 wheel 目前只保證 macOS Apple Silicon 與 Linux；Intel macOS 的 ONNX Runtime 沒有預編譯 binary，需 `ORT_STRATEGY=system` 或走 Docker。
- **企業 SSL inspection 摩擦**：MITM proxy 環境下 `maturin` 抓 rustup、`cdn.pyke.io`（ONNX）、`huggingface.co`（壓縮模型）都可能被擋，README 用了大量篇幅教怎麼繞（`HEADROOM_TLS_STRICT=0`、預先裝 Rust、`HF_HUB_OFFLINE=1`）——反映它的重依賴面其實不小。
- **Copilot subscription 模式尚未全平台驗證**：只有 macOS Keychain auth reuse 有 smoke test，Windows / Linux / Docker 路徑「已實作或計畫中但未實測」。
- **Output 節省是估計值**：本質是反事實推估，除非開對照組，否則只給信賴區間，別當精確數字用。
- **數據皆官方自報**：64k stars 與 benchmark 目前都缺獨立第三方復現，導入前建議用 `headroom.evals` 在自己的 workload 上實測。

## 研究價值與啟示

### 關鍵洞察

1. **「壓縮」被抽成獨立的一層，而非塞進 agent 框架裡**——這是最值得學的架構決策。多數專案把 context 管理耦合在 agent 邏輯內；Headroom 把它做成 proxy／middleware／MCP 三種可插拔形態，於是**與 agent 實作解耦**：不管上游是 Claude Code、LangChain 還是你自己寫的程式，只要流量經過它就會被壓。這是典型「用中介層換取通用性」的 Unix 哲學。

2. **content-aware routing 是壓縮率的關鍵**——同一段 context 裡 JSON、程式碼、散文的最佳壓法完全不同（JSON 可省 60–95%，散文只能靠 ML 模型省一成多）。先用 ContentRouter 分流、再交給專用壓縮器，比單一通用演算法高出一個量級。這也解釋了為何 coding agent 整體只省 15–20%（程式碼與散文本就難壓），而純 JSON workload 能到 90%+。

3. **「可逆」把有損壓縮的風險降到可接受**——壓縮本質有損，agent 可能剛好需要被丟掉的細節。CCR 把原文留在本地、給模型一個 `headroom_retrieve` 逃生口，等於**把「壓多少」的賭注從一次性決定改成按需回補**。這是它敢在 tool 輸出上大膽壓縮的底氣。

4. **cache 對齊被當成一等公民**——`CacheAligner` 只警告不改寫、live-zone 只壓新 bytes、verbosity 提示加在 system prompt 尾端，全都是為了**不 bust 掉 provider 的 KV cache 前綴**。這反映一個常被忽略的現實：壓縮省下的 token 若害你 cache miss，反而更貴。省 token 與保 cache 的張力，是這個層級的核心工程約束。

5. **同時打 input 與 output 兩端**——業界多數 context 工具只管「送出」端；Headroom 點出 Opus 級 output 貴 5×，並用 verbosity steering + effort routing 去剪「模型寫回來的廢話」。而且它誠實承認 output 節省無法直接量測、只給信賴區間——這種**對估計不確定性的坦白**，在充斥灌水數字的 AI 工具裡反而是可信度訊號。

### 與其他專案的關聯

- **與 [Ponytail](ponytail.md) 是互補而非競爭**：Headroom README 直接把 Ponytail 列為「想要更精簡模型輸出」的推薦搭配——Ponytail 從 **prompt 策略**端讓模型少寫，Headroom 從 **proxy** 端剪掉已經要寫的廢話，兩者疊加。本站同時收錄兩者，正好對照「省 token」的兩種切入點。
- **與 [RAG-Anything](rag-anything.md) / RAG 類專案的分工**：RAG 決定「取回哪些 chunk」，Headroom 決定「這些 chunk 進 context 前先壓多少」——一個管檢索、一個管壓縮，可串在同一條 pipeline 上。
- **與 coding agent 生態（[Claude Agent SDK](claude-agent-sdk.md)、Codex、Cursor 等）的關係**：Headroom 不取代它們，而是用 `headroom wrap` 包在外層。對照本站大量 coding agent 逆向與工具筆記，Headroom 代表另一個層次的機會——**不改 agent，只在傳輸層做優化**。
- **商業模式對照**：走 open-core（OSS 本地免費 + org 代管付費），與本站收錄的多數純 OSS 專案不同，值得觀察其社群與商業如何共存。
