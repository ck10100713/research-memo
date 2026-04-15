---
date: "2026-04-15"
category: "學習資源"
card_icon: "material-school"
oneliner: "從零學 AI 工程 — 20 Phases、260+ 課、290 小時，從數學到多 Agent Swarm 全覆蓋"
---

# AI Engineering from Scratch 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) |
| 官網 | [aiengineeringfromscratch.com](https://aiengineeringfromscratch.com) |
| SkillKit 工具 | [rohitg00/skillkit](https://github.com/rohitg00/skillkit) |

**作者：** Rohit Ghumare

**專案狀態：** ⭐ 2,779 stars · Python · MIT · 2026-03-18 創建 · 96/260+ 課已完成

## 專案概述

AI Engineering from Scratch 是一個從零開始學 AI 工程的完整課程，核心理念是 **「先從零打造，再用框架」**。涵蓋 **20 個 Phase、260+ 堂課、約 290 小時**，從數學基礎一路到多 Agent Swarm 和生產部署。

每堂課 6 步驟：**Motto → Problem → Concept（Mermaid 圖解）→ Build It（純 Python）→ Use It（框架）→ Ship It（prompt/skill/agent）**

內建 Claude Code Skills：`/find-your-level` 測程度、`/check-understanding` 隨堂測驗。

## 課程路線圖（20 Phases）

| Phase | 名稱 | 課數 | 重點 |
|:-----:|------|:----:|------|
| 0 | Setup & Tooling | 12 | Git、GPU、Docker、Linux |
| 1 | Math Foundations | 22 | 線代、微積分、機率、SVD |
| 2 | ML Fundamentals | 18 | 回歸、SVM、集成、時序 |
| 3 | Deep Learning Core | 13 | 反向傳播、自建框架、PyTorch |
| 4 | Computer Vision | 16 | CNN、YOLO、GAN、Diffusion、ViT |
| 5 | NLP | 18 | Word2Vec、Seq2Seq、Attention |
| 6 | Speech & Audio | 12 | ASR、Whisper、TTS、Voice Clone |
| 7 | Transformers | 14 | Multi-Head、RoPE、Flash Attention |
| 8 | Generative AI | 14 | VAE、Stable Diffusion、ControlNet |
| 9 | Reinforcement Learning | 12 | PPO、RLHF、Multi-Agent RL |
| 10 | LLMs from Scratch | 14 | Tokenizer、Pre-Training 124M GPT、量化 |
| 11 | LLM Engineering | 13 | Prompt、RAG、LoRA、Guardrails |
| 12 | Multimodal AI | 11 | CLIP、Vision-Language、Text-to-Video |
| 13 | Tools & Protocols | 10 | MCP Server/Client 建置 |
| 14 | Agent Engineering | 15 | Agent Loop、Memory、Permissions |
| 15 | Autonomous Systems | 11 | Self-Healing、AutoResearch |
| 16 | Multi-Agent & Swarms | 14 | Swarm Intelligence、DAG Orchestration |
| 17 | Infrastructure | 11 | K8s、Edge、ONNX/WASM、CI/CD |
| 18 | Ethics & Safety | 6 | Bias、Alignment、Differential Privacy |
| 19 | Capstone Projects | 5 | Mini GPT、Multimodal RAG、Multi-Agent |

### 建議起點

| 你是... | 從哪開始 | 預估時間 |
|---------|---------|---------|
| AI 新手 | Phase 0 | ~290h |
| 會 ML，DL 新手 | Phase 3 | ~200h |
| 會 DL，想學 LLM/Agent | Phase 10 | ~100h |
| 資深工程師，只要 Agent | Phase 14 | ~60h |

## 課程產出

每堂課產出可重用的工具：

```
outputs/
├── prompts/          # Prompt 模板
├── skills/           # SKILL.md（可裝到 Claude Code）
├── agents/           # 可部署的 Agent 定義
└── mcp-servers/      # 課程中建置的 MCP Servers
```

## 目前限制 / 注意事項

- **僅完成 37%** — 260+ 課中只完成 96 課，大量後段內容尚未產出
- **單人維護** — Rohit Ghumare 為唯一主要維護者
- **純文字課程** — 無影片講解
- **需要 GPU** — Phase 10（Pre-Training 124M GPT）等課程需 GPU
- **建立不到一個月** — 內容品質穩定性待驗證

## 研究價值與啟示

### 關鍵洞察

1. **「Build → Use → Ship」三步驟是 AI 學習的正確節奏。** 先用純 Python 從零建造理解原理，再用框架學效率，最後產出可重用工具——這比「只看 API 文件」或「只讀論文」都更有效。

2. **Claude Code Skills 整合是創新的教學方式。** `/find-your-level` 自動測程度規劃路線、`/check-understanding` 隨堂測驗——這讓「AI 教你 AI」成為現實，也展示了 Claude Code Skill 在教育場景的潛力。

3. **260+ 課覆蓋的廣度前所未見。** 從數學基礎到 Multi-Agent Swarm，從 Computer Vision 到 Speech，從 RL 到 Ethics——目前沒有其他開源課程有如此全面的覆蓋。但 37% 的完成率也是風險。

### 與其他專案的關聯

- **vs LLM Course（筆記庫中）：** LLM Course 專注於 LLM 領域（Phase 10-11 的範圍），本課程從數學基礎開始覆蓋整個 AI 工程。兩者可以互補——LLM Course 深度更深，本課程廣度更廣。
- **vs AI Agents 黃佳：** 黃佳的書專注在 Agent 框架應用，本課程的 Phase 14-16 更注重從零建造 Agent 的原理。
- **對個人學習的價值：** 如果想系統性補強 AI 工程知識，Phase 14（Agent Engineering）和 Phase 13（MCP）最直接相關。
