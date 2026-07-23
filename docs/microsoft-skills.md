---
date: "2026-07-23"
category: "Coding Agent 工具"
card_icon: "material-microsoft"
oneliner: "微軟官方 Agent Skills 庫（175 skills）— 用 Skill/Custom Agent/AGENTS.md/MCP 把 coding agent 接地到 Azure SDK 與 Foundry，含官方 Agent Framework 建構 skill"
tags:
  - skills
  - agent-framework
  - mcp
---

# microsoft/skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [github.com/microsoft/skills](https://github.com/microsoft/skills) |
| Skill Explorer（1-click install） | [microsoft.github.io/skills](https://microsoft.github.io/skills/) |
| 官方部落格 | [Context-Driven Development: Agent Skills for Microsoft Foundry and Azure](https://devblogs.microsoft.com/all-things-azure/context-driven-development-agent-skills-for-microsoft-foundry-and-azure/) |
| Agent Framework 建構 skill | repo 內 `.github/plugins/azure-sdk-python/skills/agent-framework-azure-ai-py/SKILL.md` |

**GitHub 數據**：2.8k stars、315 forks、TypeScript、MIT License、2026-01 建立、活躍開發中（WIP）

## 專案概述

microsoft/skills 是**微軟官方**的「Agent Skills」庫：提供 **Skills + Custom Agents + AGENTS.md 模板 + MCP 設定**，用來把 AI coding agent「接地」（ground）到 Azure SDK 與 Microsoft AI Foundry 上。

它的核心論點很有意思：**模型不缺知識，缺的是「啟動脈絡」**。

> "The patterns are already in their weights from pretraining. All you need is the right activation context to surface them."

也就是說，coding agent 其實在預訓練時就見過這些 SDK 的用法，但沒有正確脈絡時會生出過時/錯誤的 API。Skill 的作用不是灌新知識，而是**在對的時機把權重裡已有的正確 pattern 喚出來**。這也是為什麼官方特別警告：

> ⚠️ **要選擇性使用 skill**。全部載入會造成 **context rot**（注意力被稀釋、浪費 token、pattern 互相混淆）。只複製當前專案必要的 skill。

## 內容結構

| 資源 | 說明 |
|------|------|
| **175 Skills** | Azure SDK / Foundry 開發的領域知識，按語言分 plugin |
| **Custom Agents** | 角色型 agent（backend / frontend / infrastructure / planner） |
| **AGENTS.md** | 設定 agent 行為的模板 |
| **MCP Configs** | 預設好的 server（docs / GitHub / browser automation） |
| **Plugins** | 可安裝的 plugin 包（deep-wiki、azure-skills 等） |

### Skill 按語言 plugin 劃分

| 語言 | 數量 | 後綴 | 路徑 |
|------|------|------|------|
| Core | 11 | — | `.github/plugins/.../skills/` |
| Foundry（語言無關） | 11 | — | |
| Python | 39 | `-py` | `azure-sdk-python/skills/` |
| .NET | 28 | `-dotnet` | `azure-sdk-dotnet/skills/` |
| Java | 多個 | `-java` | `azure-sdk-java/skills/` |
| TypeScript | 26 | `-ts` | `azure-sdk-typescript/skills/` |

每個 skill 是 `.github/plugins/azure-sdk-<lang>/skills/<name>/SKILL.md`，帶 YAML frontmatter（name / description / license / metadata）。

## 安裝與 agent 無關性

```bash
npx skills add microsoft/skills          # 精靈式選取要的 skill
# 或 git clone 後複製 / symlink 特定 skill
```

裝到你選的 agent 目錄，並可 symlink 給多個 agent 共用——**同一份 skill 跨 agent 通用**：

```bash
ln -s ../.github/skills .opencode/skills   # OpenCode
ln -s ../.github/skills .claude/skills      # Claude Code
# .github/skills → GitHub Copilot
```

支援 Copilot CLI、GitHub Copilot in VS Code、Claude、OpenCode 等。repo 內有 **evals/tests CI**（`test-harness.yml`、Copilot SDK Tests）確保 skill 品質。

## 焦點：agent-framework-azure-ai-py（官方 Agent Framework 建構 skill）

這是本次研究的關鍵——**唯一一個「教 coding agent 用 Microsoft Agent Framework 寫 agent」的官方 skill，且只有 Python**：

```
User Query → AzureAIAgentsProvider → Azure AI Agent Service (Persistent)
                    ↓ Agent.run() / Agent.run_stream()
              Tools: Functions | Hosted (Code/Search/Web) | MCP
                    ↓
              AgentThread（對話持久化）
```

- 教你建 Azure AI Foundry 上的**持久化 agent**：hosted tools（code interpreter / file search / web search）、MCP 整合、thread 管理、streaming、function tools、structured outputs
- `pip install agent-framework --pre`（或 `agent-framework-azure-ai --pre`）
- **TypeScript 缺口**：官方 TS 這側只到 SDK 層（`azure-ai-projects-ts`、`m365-agents-ts`），**沒有 Agent Framework 本身的 TS 建構 skill**，因為 Agent Framework 的 JS/TS 第一方支援還沒到位（[agent-framework #6181](https://github.com/microsoft/agent-framework/discussions/6181)）

詳細跨 SDK 對照見 [建構型 Agent SDK Skills 對照](agent-sdk-builder-skills.md)。

## 目前限制 / 注意事項

- **WIP**：仍在快速新增/更新 skill，pattern 會隨 SDK 演進調整
- **聚焦 Azure/Foundry**：領域集中在微軟自家 SDK，不是通用 skill 庫
- **context rot 風險**：官方自己強調不要全裝，要按專案挑——這是使用 skill 的真實成本
- **Agent Framework skill 只有 Python**：想用 TS 建 Agent Framework agent 的人目前沒有官方 skill 可用

## 研究價值與啟示

### 關鍵洞察

1. **「skill = 啟動脈絡而非新知識」是很強的框架**——微軟明講 pattern 早在權重裡，skill 只是把它喚出來。這重新定義了 skill 的價值：不是餵模型不知道的東西，而是**對抗「模型知道正確做法、卻預設生出過時 API」的傾向**。對評估任何 skill 都適用：好 skill 提供的是「觸發條件 + 最新 pattern 的精確錨點」，不是百科全書。

2. **context rot 是 skill 生態的核心成本**——「全裝會稀釋注意力」這點被多數 skill marketplace 迴避，微軟卻寫進 README。這揭示 skill 不是「越多越好」，而是**要像相依套件一樣精挑**。skill 的數量增長反而放大了「選對 skill」這個新問題。

3. **官方第一方 skill 的最大優勢是「與 SDK 同步演進 + 有 evals」**——第三方 skill 常在 SDK 改版後過時；微軟用 CI evals/tests 綁著 SDK 更新。研究第三方 vs 官方 skill 時，**「誰負責在 SDK 改版時更新這個 skill」**是比內容豐富度更關鍵的判準。

4. **agent 無關性（symlink 給 Copilot/Claude/OpenCode）指向 skill 標準化**——同一份 SKILL.md 跨多家 agent 共用，代表 SKILL.md 正在成為跨 harness 的**可攜資產格式**。這與 [cc-to-grok-bridge](cc-to-grok-bridge.md) 系列「把 agent 設定當可攜資產」是同一個大趨勢：資產與 harness 解耦。

5. **微軟同時做 Agent Framework（SDK）與 skills（教 agent 用 SDK）**——這是一個完整的閉環：出 SDK、再出教 coding agent 用該 SDK 的 skill。但目前這個閉環**只在 Python 完整**，TS 斷在 Agent Framework 尚未第一方支援。這說明「有 SDK ≠ 有建構 skill」，兩者的成熟度可能差一截。

### 與其他專案的關聯

- **核心對照 [建構型 Agent SDK Skills 對照](agent-sdk-builder-skills.md)**：本筆記的 agent-framework-azure-ai-py 是「官方建構 skill」的代表；那篇把它與 Claude Agent SDK 第三方 skill、OpenAI 側缺口並列比較
- **vs [OpenAI Agents SDK](openai-agents-sdk.md) 的 Sandbox Skills**：OpenAI 在 SDK 內建 `Capabilities` 掛 skill；微軟則把 skill 做成獨立 repo 供 coding agent 取用——**「skill 內建於 SDK」vs「skill 作為外部脈絡庫」**兩種路線
- **vs [cc-to-grok-bridge](cc-to-grok-bridge.md)**：都在處理「agent 資產可攜」，微軟用 symlink 跨 agent 共用 skill，bridge 系列用 adapter 跨 harness 搬設定
