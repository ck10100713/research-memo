---
date: "2026-07-23"
category: "Coding Agent 工具"
card_icon: "material-hammer-wrench"
oneliner: "『建構型 skill』對照 — 教 coding agent 用 SDK 把 agent 寫出來：Claude Agent SDK（雙語第三方最成熟）、OpenAI、Microsoft Agent Framework 三方現況"
tags:
  - skills
  - agent-framework
  - claude-code
---

# 建構型 Agent SDK Skills 對照研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| WalterSumbon/claude-agent-sdk-skill | [github.com/WalterSumbon/claude-agent-sdk-skill](https://github.com/WalterSumbon/claude-agent-sdk-skill) |
| btgaskin/claude-agent-sdk-skill | [github.com/btgaskin/claude-agent-sdk-skill](https://github.com/btgaskin/claude-agent-sdk-skill) |
| openai/skills（Codex 官方 skill 目錄） | [github.com/openai/skills](https://github.com/openai/skills) |
| microsoft/skills（官方 Agent Framework skill） | [github.com/microsoft/skills](https://github.com/microsoft/skills)（[另篇筆記](microsoft-skills.md)） |
| Agents SDK 納入 skills 的 issue | [openai-agents-python #2361](https://github.com/openai/openai-agents-python/issues/2361) |
| Agent Framework TS 支援討論 | [agent-framework #6181](https://github.com/microsoft/agent-framework/discussions/6181) |
| 官方結合教學 | [Build AI Agents with Claude Agent SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-claude-agent-sdk-and-microsoft-agent-framework/) |

## 什麼是「建構型 skill」

一般 skill 是「領域知識」（教 agent 怎麼用某個 API / 做某件事）。**建構型 skill** 更窄：**教 coding agent 用某個 Agent SDK 把「另一個 agent」寫出來**——subagents、hooks、custom tools、guardrails、多 agent workflow 這些 SDK 專屬 pattern。

這類 skill 的價值在於：SDK 改版快、模型權重裡的 pattern 常過時，建構型 skill 提供「觸發條件 + 最新 pattern 錨點」，讓 agent 生出**跑得起來**的 SDK 程式碼而非幻覺 API。

> **研究方法note**：本筆記所有結論以**實際 clone/fetch 各 repo 的 SKILL.md** 為準，不採信 marketplace 描述——過程中就抓到 marketplace 條目與 repo 實況不符的案例（見下方 OpenAI 段）。

## 三方現況（實測）

### 1. Claude Agent SDK — 雙語、第三方最成熟 ✅

兩個第三方 skill 都做成 Claude Code plugin，且**都同時覆蓋 Python + TypeScript**：

| repo | ★ | 授權 | 結構 | 內容特點 |
|------|---|------|------|---------|
| **WalterSumbon** | 6 | Apache-2.0 | `claude-agent-sdk-python` + `claude-agent-sdk-typescript` **兩個獨立 skill**，各含 `references/troubleshooting.md` | 觸發詞極細（`ClaudeAgentOptions`、`async for message in query`…）；區分 `query()` 無狀態 vs `ClaudeSDKClient` 有狀態兩模式；標註 **Claude Code SDK → Claude Agent SDK 改名**（v0.1.0+）；涵蓋 subagents/hooks/batch |
| **btgaskin** | 8 | MIT | 單一 `claude-agent-sdk` skill + 5 份 references（custom-tools / hooks-reference / multi-agent / python-patterns / typescript-patterns） | 有 **Agent SDK vs Messages API 決策表**；雙語 quick start；in-process MCP 自訂工具、hooks、subagents |

- **沒有 Anthropic 官方建構 skill**——官方靠 SDK 文件本身；但這兩個第三方品質不錯，雙語覆蓋是最大優勢
- 兩者定位略不同：WalterSumbon 把 Python/TS 拆成兩個 skill（載入更精準、避免 context rot）；btgaskin 合成一個 skill + 語言分 reference（入口單純）

### 2. OpenAI Agents SDK — 官方有 skill 目錄，但**沒有** Agents-SDK 建構 skill ⚠️

- **官方 [openai/skills](https://github.com/openai/skills)**（24k★，「Skills Catalog for Codex」，44 curated skills）**確實存在**，但內容是 Codex 通用 skill（figma / deploy / notion / security / `openai-docs`…），**沒有一個是教你用 `@openai/agents` 建 agent 的建構 skill**
- **[issue #2361](https://github.com/openai/openai-agents-python/issues/2361)**：社群要求把 skills 系統納入 Agents SDK——**尚未實作**
- **第三方不可靠**：marketplace（mcpmarket / claude-plugins.dev）列的「OpenAI Agents SDK Skill」中，被引用的 `@jezweb/claude-skills/openai-agents` **實際不在該 repo 裡**（jezweb/claude-skills 有 63 個 skill，無一是 OpenAI）——marketplace 條目已失效
- **結論**：SDK 本身雖 TS 優先且成熟，但**沒有可靠的建構型 skill**（官方沒做、第三方查無實體）

### 3. Microsoft Agent Framework — 官方有，但**只 Python** ⚠️

- **官方 `agent-framework-azure-ai-py`**（在 [microsoft/skills](microsoft-skills.md) 內）：教你用 Microsoft Agent Framework Python SDK 建 Azure AI Foundry 持久化 agent（`AzureAIAgentsProvider`、hosted tools、MCP、AgentThread、streaming）
- **TS 缺口**：官方 TS 側只有 SDK 層 skill（`azure-ai-projects-ts`、`m365-agents-ts`），**沒有 Agent Framework 本身的 TS 建構 skill**，因 JS/TS 第一方支援還沒到位（[#6181](https://github.com/microsoft/agent-framework/discussions/6181)）

## 收斂表（聚焦 JS/TS 建構型 skill）

| SDK | 官方建構 skill | 第三方建構 skill | JS/TS 覆蓋 | 推薦度 |
|-----|--------------|----------------|-----------|--------|
| **Claude Agent SDK** | ❌（靠 SDK 文件） | ✅ WalterSumbon / btgaskin，**皆雙語** | ✅ TS + Python | **最佳** |
| **OpenAI Agents SDK** | ❌（openai/skills 無此項；#2361 未做） | ⚠️ marketplace 有列、查無實體 | SDK 本身 TS 優先，但無可靠 skill | 待補 |
| **Microsoft Agent Framework** | ✅ 但**只 Python**（`agent-framework-azure-ai-py`） | — | ❌ TS 只到 Azure SDK 層（#6181） | 待補（TS） |

## 對原始判斷的修正（實測 vs marketplace）

研究時對照了「看 marketplace 描述」與「實際讀 repo」的差異，修正三點：

1. **OpenAI 官方其實有 skill 庫**：不是「OpenAI 只有第三方」——官方 `openai/skills`（24k★）存在，只是**沒有 Agents-SDK 建構 skill**（是 Codex 通用目錄）。缺口位置要講精確
2. **被引用的 jezweb OpenAI skill 已不存在**：marketplace 連結指向的 skill 在 repo 裡查無——**marketplace 條目會過時/失效**
3. **btgaskin 也是雙語**：不只 TS——它的 references 同時有 `python-patterns.md` 與 `typescript-patterns.md`

## 研究價值與啟示

### 關鍵洞察

1. **「有成熟 SDK」不等於「有成熟建構 skill」**——OpenAI Agents SDK 是 TS 優先且成熟的 SDK，卻**沒有**可靠的建構型 skill；Microsoft Agent Framework 有官方 skill 卻卡在 Python。SDK 成熟度與「教 agent 用它」的 skill 成熟度是**兩條獨立的曲線**，選型時要分開評估。

2. **marketplace 描述不可作為事實來源**——本研究直接抓到「被引用的 skill 不在 repo 裡」。skill 生態還太新、marketplace 與 repo 常不同步。**評估任何 skill 都應該讀它真正的 SKILL.md**，而非信 marketplace 卡片——這也是這批研究刻意 clone/fetch 而非轉述的原因。

3. **官方 vs 第三方的真正差別是「誰在 SDK 改版時更新」**——Claude Agent SDK 的第三方 skill 品質好，但 SDK 一改（如 Claude Code SDK → Claude Agent SDK 改名）就靠作者自覺更新（WalterSumbon 有標註改名，是好徵兆）；官方 skill（微軟）用 CI evals 綁著 SDK。長期可靠度，**維護承諾 > 當下內容豐富度**。

4. **雙語覆蓋是 Claude Agent SDK skill 勝出的關鍵**——兩個第三方都同時給 Python + TS，正好補上 OpenAI（無可靠 skill）與 Microsoft（只 Python）的缺口。對想用 **TS/JS** 建 agent 的人，Claude Agent SDK 目前是**唯一有現成、雙語、可用建構 skill**的選項。

5. **建構型 skill 是「SDK 採用率」的槓桿**——一個 SDK 若沒有好的建構 skill，coding agent 幫使用者寫出來的程式碼就容易是過時 API，體感變差、採用受阻。**SDK 廠商該把「官方建構 skill」視為和文件同等的一級交付物**——微軟已在做（Python），OpenAI 的 #2361 顯示需求已浮現但尚未補上。

### 與其他專案的關聯

- **[microsoft/skills](microsoft-skills.md)**：本筆記 Microsoft 段的官方 skill 出處；那篇深入其 175-skill 庫與「skill = 啟動脈絡」哲學
- **三個 SDK 本體筆記**：[Claude Agent SDK](claude-agent-sdk.md)、[OpenAI Agents SDK](openai-agents-sdk.md)——本筆記是「教 agent 用這些 SDK」的 meta 層，與 SDK 本體筆記互補
- **[cc-to-grok-bridge](cc-to-grok-bridge.md) 系列**：同屬「agent 資產（skill / rules / hooks）如何可攜、如何跨 harness 復用」的大主題
