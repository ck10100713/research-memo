---
date: "2026-04-02"
category: "Coding Agent 工具"
card_icon: "material-cog-outline"
oneliner: "香港大學開源 Agent Harness — 11,700 行 Python 重現 98% Claude Code 工具能力，支援多 LLM Provider"
---

# OpenHarness 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) |
| Substack 分析 | [The Open Source Agent Framework That Is 44 Times Lighter Than Claude Code](https://pythonlibraries.substack.com/p/the-open-source-agent-framework-that) |
| Hacker News 討論 | [Show HN: OpenHarness](https://news.ycombinator.com/item?id=47600371) |
| HKUDS Lab | [Data Intelligence Lab @ HKU](https://github.com/HKUDS) |

## 專案概述

OpenHarness（CLI 指令為 `oh`）是由香港大學 Data Intelligence Lab（HKUDS）開發的開源 Agent Harness 框架。核心理念是：**模型提供智能，Harness 提供手、眼、記憶和安全邊界**。

專案於 2026-04-01 首次開源（v0.1.0），僅 11,700 行 Python 核心程式碼，號稱實現 Claude Code 約 98% 的工具能力，且體積只有 Claude Code 的 1/44。完全相容 Anthropic 的 Skills 系統和 Claude Code Plugin 生態系。

| 指標 | 數值 |
|------|------|
| Stars | ~7,170（截至 2026-04-02） |
| 語言 | Python |
| License | MIT |
| 核心程式碼 | ~11,700 行 |
| 內建工具數 | 43+ |
| 內建指令數 | 54 |
| 測試 | 114 unit/integration + 多套 E2E |

## 核心功能 / 技術架構

### Harness 架構（10 個子系統）

```
openharness/
  engine/          # Agent Loop — query → stream → tool-call → loop
  tools/           # 43 Tools — file I/O, shell, search, web, MCP
  skills/          # Knowledge — on-demand skill loading (.md)
  plugins/         # Extensions — commands, hooks, agents, MCP servers
  permissions/     # Safety — multi-level modes, path rules, command deny
  hooks/           # Lifecycle — PreToolUse/PostToolUse event hooks
  commands/        # 54 Commands — /help, /commit, /plan, /resume, ...
  mcp/             # MCP — Model Context Protocol client
  memory/          # Memory — persistent cross-session knowledge
  tasks/           # Tasks — background task management
  coordinator/     # Multi-Agent — subagent spawning, team coordination
  prompts/         # Context — system prompt assembly, CLAUDE.md, skills
  config/          # Settings — multi-layer config, migrations
  ui/              # React TUI — backend protocol + frontend (React + Ink)
```

### Agent Loop 核心

```python
while True:
    response = await api.stream(messages, tools)
    if response.stop_reason != "tool_use":
        break  # 模型完成
    for tool_call in response.tool_uses:
        result = await harness.execute_tool(tool_call)  # 權限檢查 → Hook → 執行 → Hook → 結果
    messages.append(tool_results)
```

### 五大 Harness 特性

| 特性 | 說明 |
|------|------|
| **Agent Loop** | Streaming tool-call cycle、API retry with exponential backoff、parallel tool execution、token counting |
| **Harness Toolkit** | 43+ 工具（File, Shell, Search, Web, MCP）、on-demand skill loading、plugin 生態系 |
| **Context & Memory** | CLAUDE.md discovery & injection、context compression（auto-compact）、MEMORY.md 持久記憶 |
| **Governance** | 多級權限模式（Default / Auto / Plan Mode）、path-level rules、PreToolUse/PostToolUse hooks |
| **Swarm Coordination** | Subagent spawning & delegation、team registry、background task lifecycle |

### Provider 相容性

OpenHarness 將 Provider 包裝為 **Workflow + Profile** 概念，透過 `oh setup` 引導式設定：

| Workflow | 支援的後端 |
|----------|-----------|
| **Anthropic-Compatible API** | Claude 官方、Moonshot/Kimi、Zhipu/GLM、MiniMax |
| **Claude Subscription** | 本地 `~/.claude/.credentials.json` |
| **OpenAI-Compatible API** | OpenAI、OpenRouter、DashScope、DeepSeek、SiliconFlow、Groq、Ollama |
| **Codex Subscription** | 本地 `~/.codex/auth.json` |
| **GitHub Copilot** | GitHub OAuth device flow |

每個 Profile 可以有獨立的 API key，不同 Provider 不需共用同一把金鑰。

### ohmo 個人 Agent

`ohmo` 是基於 OpenHarness 的個人 Agent 應用，有獨立 workspace（`~/.ohmo/`）：

| 檔案 | 用途 |
|------|------|
| `soul.md` | Agent 長期人格和行為定義 |
| `identity.md` | Agent 身份 |
| `user.md` | 使用者偏好 |
| `BOOTSTRAP.md` | 首次啟動儀式 |
| `memory/` | 個人記憶 |
| `gateway.json` | Provider 和頻道設定 |

支援 Telegram、Slack、Discord、Feishu 等 IM 頻道作為 gateway。

## 快速開始

```bash
# 一鍵安裝
curl -fsSL https://raw.githubusercontent.com/HKUDS/OpenHarness/main/scripts/install.sh | bash

# 或從原始碼安裝
git clone https://github.com/HKUDS/OpenHarness.git
cd OpenHarness
uv sync --extra dev

# 引導式設定 Provider
oh setup

# 啟動
oh

# 非互動模式
oh -p "Explain this codebase"

# JSON 輸出
oh -p "List all functions" --output-format json
```

## 目前限制 / 注意事項

- **極早期版本**（v0.1.2，2026-04-06）：功能變動快，API 可能不穩定
- **社群討論有限**：HN 討論串只有少量回覆，尚未經過大規模實戰驗證
- **「98% 功能覆蓋」需保留態度**：Claude Code 的核心競爭力不只在工具數量，還在 system prompt 的精密設計和 Anthropic 的模型微調
- **ClawTeam 多 Agent 整合**仍在 Roadmap，尚未實作
- **ohmo 個人 Agent** 概念新穎但成熟度未知
- **效能基準測試缺乏**：未公布與 Claude Code 的對比 benchmark（如 SWE-bench）

## 研究價值與啟示

### 關鍵洞察

1. **「Harness」抽象是正確的思維框架** — OpenHarness 明確區分「模型智能」和「執行基礎設施」，這與 Claude Code 洩漏事件後社群對 Agent 架構的共識一致：LLM 本身只是引擎，真正的工程在 harness 層（工具、權限、記憶、上下文管理）。

2. **Claude Code 相容性是聰明的策略** — 直接相容 `CLAUDE.md`、`MEMORY.md`、Skills（`.md`）、Plugin（`.claude-plugin/`）格式，讓現有 Claude Code 使用者可以零成本遷移知識資產。這也意味著社群圍繞 Claude Code 生態建立的 Skills 和 Plugin 可以直接複用。

3. **多 Provider 統一是差異化亮點** — Claude Code 綁定 Anthropic API，而 OpenHarness 透過 Workflow + Profile 抽象支援 Anthropic、OpenAI、Copilot、甚至 Ollama 本地模型。對於想用中國大陸 LLM（Kimi、GLM、DashScope）的開發者特別有吸引力。

4. **學術團隊背景值得關注** — HKUDS 是港大的 Data Intelligence Lab，有學術研究的系統性和嚴謹度。但學術專案的長期維護和社群經營能力是未知數，需觀察後續迭代速度。

5. **ohmo 個人 Agent 是有趣的方向** — 將 Agent Harness 擴展到個人助理場景（有身份、人格、記憶、IM 頻道），預示了 Agent 從「開發工具」走向「個人入口」的趨勢。但 `soul.md` / `identity.md` 的設計是否足夠靈活仍需觀察。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [Claw Code](claw-code.md) | 同屬 Claude Code 洩漏事件後的 clean-room 重寫陣營，但 Claw Code 用 Python + Rust，OpenHarness 純 Python |
| [OpenClaw](openclaw.md) | OpenHarness README 提及與 OpenClaw 的 workflow 相容性，共享 Markdown-first 知識系統 |
| [Claude Code Reverse](claude-code-reverse.md) | OpenHarness 的架構可與逆向分析對照，驗證其 98% 功能覆蓋的說法 |
| [Copilot Ralph](copilot-ralph.md) | 同樣支援多 Provider（BYOK），但 Ralph 是 TypeScript 生態，OpenHarness 是 Python |
| [Kuberwastaken Claude Code](kuberwastaken-claude-code.md) | Rust clean-room 重寫 vs. OpenHarness 的 Python 輕量路線，架構取捨不同 |
| [Analysis Claude Code](analysis-claude-code.md) | OpenHarness 的 harness 架構直接對應 Claude Code 的核心設計模式 |
