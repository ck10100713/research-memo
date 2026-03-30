---
date: ""
category: "Coding Agent 工具"
icon: "material-account-multiple"
oneliner: "144 個專業化 AI Agent 人格庫，橫跨 12 部門，支援 10 個 AI 工具"
---
# The Agency: AI Specialists 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/msitarzewski/agency-agents |
| 作者 | Mike Sitarzewski |
| Stars | ~59.3K |
| 授權 | MIT |
| 語言 | Shell（安裝/轉換腳本） |
| 社群 | Reddit r/ClaudeAI、GitHub Discussions |

## 專案概述

The Agency 是一個大規模的 **AI Agent 人格庫**，收錄了 **144 個專業化 Agent**，橫跨 **12 個部門**。每個 Agent 都有獨特的身份、人格、工作流程和交付物——不是泛用 prompt 模板，而是完整的「虛擬專家」角色定義。

起源於 Reddit 討論串，經過數月社群迭代，成為目前最大的開源 AI Agent 人格庫之一。

### 核心理念

> "Assembling your dream team, except they're AI specialists who never sleep, never complain, and always deliver."

每個 Agent 設計遵循五大原則：

1. **強烈人格**：有獨特的聲音、溝通風格和態度
2. **明確交付物**：具體的產出，不是模糊的指導
3. **成功指標**：可衡量的品質標準
4. **驗證過的工作流**：有步驟的流程
5. **學習記憶**：模式辨識與持續改善

## 12 個部門 × 144 個 Agent

| 部門 | Agent 數 | 代表角色 |
|------|---------|---------|
| **Engineering** | 22 | Frontend Developer、Backend Architect、AI Engineer、Security Engineer、SRE、Database Optimizer |
| **Design** | 8 | UI Designer、UX Researcher、Brand Guardian、Whimsy Injector、Image Prompt Engineer |
| **Paid Media** | 7 | PPC Strategist、Search Query Analyst、Ad Creative Strategist、Programmatic Buyer |
| **Sales** | 8 | Outbound Strategist、Discovery Coach、Deal Strategist、Sales Engineer、Pipeline Analyst |
| **Marketing** | 26 | Growth Hacker、Content Creator、SEO Specialist、TikTok/Instagram/Reddit Strategist、Baidu SEO、微博/小紅書/B站 |
| **Product** | 5 | Sprint Prioritizer、Trend Researcher、Feedback Synthesizer、Product Manager |
| **Project Management** | 6 | Studio Producer、Project Shepherd、Experiment Tracker、Jira Workflow Steward |
| **Testing** | 8 | Evidence Collector、Reality Checker、Performance Benchmarker、API Tester、Accessibility Auditor |
| **Support** | 6 | Support Responder、Analytics Reporter、Finance Tracker、Legal Compliance Checker |
| **Spatial Computing** | 6 | XR Interface Architect、visionOS Engineer、macOS Metal Engineer、WebXR Developer |
| **Specialized** | 27 | Agents Orchestrator、MCP Builder、ZK Steward、Salesforce Architect、Blockchain Security Auditor |
| **Game Development** | 15 | Game Designer、Unity/Unreal/Godot/Roblox 各引擎專家、Blender Addon Engineer |
| **Academic** | 5 | Anthropologist、Geographer、Historian、Narratologist、Psychologist |

### 特色亮點

**中國市場覆蓋廣泛**：少見地包含微信小程序開發、小紅書策略、B站內容、快手策略、微博運營、百度SEO、跨境電商、直播帶貨等中國市場專用 Agent。

**遊戲開發完整**：覆蓋 Unity、Unreal Engine、Godot、Roblox Studio、Blender 五大平台，從遊戲設計到技術美術都有。

**學術部門**：獨特的 worldbuilding 導向——人類學家、地理學家、歷史學家、敘事學家、心理學家，用於建構虛構世界的學術嚴謹性。

## 跨工具支援

The Agency 不只是 Claude Code 專用，支援 **10 個 AI coding 工具**：

| 工具 | 安裝位置 | 格式 |
|------|---------|------|
| Claude Code | `~/.claude/agents/` | `.md` 原生 |
| GitHub Copilot | `~/.github/agents/` | `.md` 原生 |
| Antigravity (Gemini) | `~/.gemini/antigravity/skills/` | `SKILL.md` |
| Gemini CLI | `~/.gemini/extensions/` | Extension + SKILL.md |
| OpenCode | `.opencode/agents/` | `.md` |
| Cursor | `.cursor/rules/` | `.mdc` |
| Aider | `./CONVENTIONS.md` | 單一合併檔 |
| Windsurf | `./.windsurfrules` | 單一合併檔 |
| OpenClaw | `~/.openclaw/` | SOUL.md + AGENTS.md + IDENTITY.md |
| Qwen Code | `.qwen/agents/` | `.md` SubAgent |

透過 `convert.sh` 和 `install.sh` 腳本自動轉換與安裝，支援平行處理。

## 使用方式

### 安裝

```bash
# Claude Code（推薦）
cp -r agency-agents/* ~/.claude/agents/

# 或使用安裝腳本（自動偵測已安裝的工具）
./scripts/convert.sh        # 生成各工具的整合檔
./scripts/install.sh        # 互動式安裝
```

### 啟動 Agent

```
# 在 Claude Code 中
"Hey Claude, activate Frontend Developer mode and help me build a React component"
"Use the Security Engineer agent to review this code"
```

### 實戰場景範例

**Startup MVP 團隊：**
Frontend Developer → Backend Architect → Growth Hacker → Rapid Prototyper → Reality Checker

**行銷活動團隊：**
Content Creator → Twitter Engager → Instagram Curator → Reddit Community Builder → Analytics Reporter

**企業功能開發：**
Senior PM → Senior Developer → UI Designer → Experiment Tracker → Evidence Collector → Reality Checker

## Agent 設計模板

每個 Agent 檔案的結構：

```markdown
---
name: Agent Name
description: 一句話描述
color: 品牌色
---

# Identity & Memory
（角色身份、人格特質、記憶模式）

# Core Mission
（核心使命和目標）

# Critical Rules
（領域專用的關鍵規則）

# Technical Deliverables
（具體交付物和程式碼範例）

# Workflow Process
（步驟式工作流程）

# Success Metrics
（成功指標和品質標準）

# Communication Style
（溝通風格和語氣）
```

### Agent 人格範例

> "I don't just test your code - I default to finding 3-5 issues and require visual proof for everything."
> — Evidence Collector (Testing Division)

> "You're not marketing on Reddit - you're becoming a valued community member who happens to represent a brand."
> — Reddit Community Builder (Marketing Division)

## 研究價值與啟示

### 關鍵洞察

1. **人格比 prompt 重要**：泛用的「Act as a developer」遠不如有完整身份、工作流、成功指標的角色定義。人格驅動的 Agent 產出品質和一致性更高。

2. **Agent 是「可組合的虛擬團隊」**：每個 Agent 獨立運作，但可以像真實團隊一樣組合——這個 pattern 與 Paperclip 的組織架構、gstack 的虛擬工程團隊異曲同工，但規模大得多。

3. **跨工具相容是趨勢**：支援 10 個 AI coding 工具代表 Agent 定義正在成為一種可攜的標準格式。`.md` 作為 Agent 定義語言已經是事實標準。

4. **中國市場 Agent 的空白被填補**：小紅書、B站、快手、微博、百度SEO 等中國平台的 Agent 定義在英文開源世界非常稀有，這個專案填補了重要空白。

5. **144 個 Agent 的啟示**：當 Agent 數量夠多，分類和發現機制就變得關鍵——這也是為什麼專案有清晰的「12 部門」組織結構和詳細的「何時使用」指引。

### 與其他專案的關聯

| 面向 | The Agency | gstack | Paperclip |
|------|-----------|--------|-----------|
| Agent 數量 | 144 | 18 (slash commands) | 由使用者定義 |
| 組織模型 | 12 部門 | 虛擬工程團隊 | 公司組織架構 |
| 重點 | 角色定義（人格+流程） | 工作流自動化 | 編排+治理 |
| 跨工具 | 10 個工具 | Claude Code 專用 | 工具無關 |
| 適用範圍 | 軟體開發 + 行銷 + 設計 + 銷售 + 遊戲 | 軟體開發 | 通用 Agent 管理 |
