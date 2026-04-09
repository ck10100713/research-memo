---
date: "2026-04-09"
category: "學習資源"
card_icon: "material-school"
oneliner: "港大 HKUDS 開源 AI 學習助理 — RAG 知識庫 + 多 Agent 解題 + TutorBot 自主家教 + CLI 原生"
---

# DeepTutor 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) |
| 官方文件站 | [hkuds.github.io/DeepTutor](https://hkuds.github.io/DeepTutor/) |
| 架構概覽 | [DeepTutor's Framework](https://hkuds.github.io/DeepTutor/features/overview.html) |
| ChatGate 介紹 | [DeepTutor: AI-Powered Paper Reading Inside Zotero](https://chatgate.ai/post/deeptutor/) |
| ScriptByAI 評測 | [DeepTutor: Open-Source, Multi-agent AI Learning Assistant](https://www.scriptbyai.com/deeptutor-ai-learning-assistant/) |
| HKUDS Lab | [Data Intelligence Lab @ HKU](https://github.com/HKUDS) |

## 專案概述

**DeepTutor** 是香港大學 HKUDS Lab（與 [OpenHarness](open-harness.md) 同一實驗室）開發的開源 AI 個人化學習助理。v1.0.0（2026-04-04）進行了 agent-native 架構重寫，核心理念是**讓 AI 成為持久化的家教，而非一次性的聊天機器人**。

五個功能模式共享同一對話上下文，搭配持久記憶、知識庫、TutorBot 自主 Agent 和完整 CLI 介面，構成一個從學習到評估的閉環系統。

| 指標 | 數值 |
|------|------|
| Stars | ~13,730 |
| 語言 | Python + Next.js 16 |
| License | Apache 2.0 |
| 首發 | 2025-12-29 |
| 當前版本 | v1.0.0-beta.3（2026-04-08） |
| LLM Providers | 25+（OpenAI、Anthropic、Ollama、Gemini 等） |
| IM 頻道支援 | Telegram、Discord、Slack、Feishu、WeChat Work、DingTalk、Email |

## 核心架構

### 五大功能模式（共享上下文）

```
統一對話 Workspace
     │
     ├── Chat ─────────── 工具增強對話（RAG、搜尋、程式碼執行、推理）
     ├── Deep Solve ───── 多 Agent 解題（規劃→調查→解題→驗證）
     ├── Quiz Generation ─ 從知識庫生成測驗 + 內建驗證
     ├── Deep Research ── 分解主題→並行 Agent 研究→完整引用報告
     └── Math Animator ── 數學概念→Manim 視覺化動畫
```

> 在同一對話中無縫切換：聊天提問 → Deep Solve 解難題 → 生成測驗自測 → Deep Research 深入研究，不丟失任何上下文。

### 分層架構

| 層級 | 說明 |
|------|------|
| **Capabilities**（能力層） | Chat, Deep Solve, Quiz, Research, Math Animator — 編排推理工作流 |
| **Tools**（工具層） | RAG 檢索、網路搜尋、程式碼執行、深度推理、學術論文搜尋、腦暴 — 與工作流解耦，任意組合 |
| **Knowledge Hub** | PDF/TXT/Markdown 上傳 → RAG-ready 知識庫，支援漸進式增量新增 |
| **Memory** | 持久化學習者畫像：Summary（學習進度摘要）+ Profile（偏好、程度、目標） |
| **TutorBot** | 基於 nanobot 的自主 Agent，獨立 workspace、記憶、人格 |

### TutorBot — 不是聊天機器人，是自主家教

TutorBot 基於 HKUDS 的 [nanobot](https://github.com/HKUDS/nanobot) 引擎，每個 bot 是獨立的 Agent 實例：

| 特性 | 說明 |
|------|------|
| **Soul Templates** | 可編輯人格檔案：蘇格拉底式、鼓勵型、嚴謹型，或自訂 |
| **獨立 Workspace** | 每個 bot 有獨立目錄、記憶、session、技能、設定 |
| **Proactive Heartbeat** | 主動發起：學習簽到、複習提醒、排程任務 — 不只回應，還主動出擊 |
| **Skill Learning** | 透過新增 skill 檔案擴展能力 |
| **Multi-Channel** | Telegram、Discord、Slack、Feishu、WeChat Work、DingTalk、Email |
| **Team & Sub-Agents** | 可在單一 bot 內派遣子 Agent 或組建 Agent 團隊 |

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
```

### 其他功能

| 功能 | 說明 |
|------|------|
| **Co-Writer** | Markdown 編輯器，AI 為一等公民 — 選取文字即可重寫、擴展、縮短，可引用知識庫 |
| **Guided Learning** | 將材料轉化為 3-5 步結構化學習旅程，每步生成互動 HTML 頁面 |
| **Notebooks** | 跨 session 筆記管理，色碼分類 |

### LLM Provider 支援

支援 25+ 個 Provider，涵蓋主流中外 LLM：

| 類型 | Providers |
|------|----------|
| 國際 | OpenAI、Anthropic、Gemini、Mistral、Groq、OpenRouter |
| 中國 | DashScope (Qwen)、DeepSeek、Moonshot (Kimi)、Zhipu (GLM)、MiniMax、VolcEngine、SiliconFlow |
| 本地 | Ollama、vLLM、OpenVINO Model Server |
| 訂閱制 | GitHub Copilot、OpenAI Codex |

## 快速開始

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

conda create -n deeptutor python=3.11 && conda activate deeptutor

# 引導式安裝（推薦）
python scripts/start_tour.py

# 或 CLI only
pip install -e ".[cli]"
deeptutor chat
deeptutor run deep_solve "Prove that √2 is irrational"
deeptutor kb create my-kb --doc textbook.pdf
```

也支援 Docker 一鍵部署：

```bash
cp .env.example .env  # 編輯 LLM/Embedding 設定
docker compose -f docker-compose.ghcr.yml up -d
# → http://localhost:3782
```

## HKUDS 生態系

DeepTutor 是 HKUDS Lab 多個開源專案之一：

| 專案 | 角色 |
|------|------|
| **LightRAG** | 輕量級 RAG 引擎（DeepTutor 知識庫的未來後端） |
| **nanobot** | 超輕量 Agent 引擎（TutorBot 的底層） |
| **AutoAgent** | Zero-Code Agent 框架 |
| **AI-Researcher** | 自動化研究助理 |
| **OpenHarness** | Claude Code 風格的 Agent Harness |

## 目前限制 / 注意事項

- **v1.0.0-beta 階段**：架構剛重寫，穩定性待驗證。beta.1 → beta.3 在五天內連發三版修復
- **需要外部 LLM + Embedding API**：不像 MemPalace 的零 API 模式，DeepTutor 核心功能依賴 LLM 呼叫
- **Knowledge Base 僅支援 PDF/TXT/Markdown**：不支援 Word、Excel、影片等格式
- **單用戶設計**：目前無 authentication/login，不適合公開部署（在 Roadmap 中）
- **Deep Solve 的多 Agent 成本**：規劃→調查→解題→驗證的 4 步 Agent 鏈，每次解題消耗多次 LLM 呼叫
- **Math Animator 依賴 Manim**：需要額外安裝 Manim 和 LaTeX 環境
- **LightRAG 尚未整合**：知識庫目前用 LlamaIndex，LightRAG 整合在 Roadmap

## 研究價值與啟示

### 關鍵洞察

1. **「五模式共享上下文」是學習工具的正確設計** — 傳統工具把聊天、解題、測驗、研究切割成獨立功能。DeepTutor 讓它們共享同一對話上下文，使用者可以在聊天中發現問題 → 切到 Deep Solve 解題 → 切到 Quiz 自測 → 切到 Deep Research 深入。這種「一個 thread 走天下」的設計大幅降低了上下文切換成本。

2. **TutorBot 的「Proactive Heartbeat」挑戰了 AI 工具的被動範式** — 大多數 AI 工具是被動的：你問它答。TutorBot 會主動發起學習簽到和複習提醒，這是從「工具」走向「教練」的關鍵設計差異。結合 Soul Template 的人格定制，每個 TutorBot 實際上是一個有個性的持久化學習夥伴。

3. **HKUDS Lab 正在建立一個完整的 AI 工具生態** — 從 LightRAG（知識檢索）→ nanobot（Agent 引擎）→ DeepTutor（學習）→ OpenHarness（開發）→ AutoAgent（框架）→ AI-Researcher（研究），HKUDS 在每個環節都有開源專案，且相互依賴（DeepTutor 用 nanobot，未來用 LightRAG）。這種「學術團隊做完整生態」的模式在開源社群中很少見。

4. **CLI-first + SKILL.md 設計讓 AI Agent 可以操作 DeepTutor** — 這是真正的「Agent-Native」含義：不只是人用 DeepTutor 學習，而是其他 AI Agent 也可以透過 CLI 和 SKILL.md 自主操作 DeepTutor。例如 Claude Code 可以透過 SKILL.md 自動建立知識庫、執行研究、生成測驗。

5. **25+ LLM Provider 支援反映了中國開發者的需求** — DashScope、DeepSeek、Moonshot、Zhipu、MiniMax、VolcEngine、SiliconFlow、BytePlus — 這些中國 LLM Provider 的一級支援，讓 DeepTutor 在中國市場比大多數國際工具更實用。這與 OpenHarness 的多 Provider 策略一致。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [OpenHarness](open-harness.md) | 同為 HKUDS Lab 出品，OpenHarness 專注開發（Agent Harness），DeepTutor 專注學習（個人化家教）。兩者都支援 25+ LLM Providers，都有 CLI-first 設計 |
| [Karpathy LLM Wiki](karpathy-llm-wiki.md) | 兩者都解決「知識管理」問題，但路線不同：Karpathy 讓 LLM 編譯 wiki（寫作者視角），DeepTutor 讓 LLM 當家教（學習者視角）。DeepTutor 的 Knowledge Hub + Guided Learning 可視為 LLM Wiki 的「教學版」 |
| [MemPalace](mempalace.md) | 同樣有持久記憶系統，但 MemPalace 記錄「你做過什麼」（對話歷史），DeepTutor 記錄「你學會了什麼」（學習畫像）。DeepTutor 的 Memory 更像是個人化學習檔案而非原始對話儲存 |
| [Gemma 4 與 Local LLM](gemma-4-local-llm.md) | DeepTutor 支援 Ollama 和 vLLM 作為 LLM Provider，可搭配 Gemma 4 實現完全本地的學習助理 |
| [Career-Ops](career-ops.md) | Career-Ops 的 14 個 modes 管理求職，DeepTutor 的 5 個 capabilities 管理學習。兩者都是 Claude Code / Agent-native 的「生活面向」應用 |
