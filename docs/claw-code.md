---
date: "2026-04-01"
category: "Coding Agent 工具"
card_icon: "material-claw"
oneliner: "Claude Code 洩漏事件後的 clean-room Python/Rust 重寫，harness 工程研究標竿"
---

# Claw Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原始 Repo（instructkr） | [github.com/instructkr/claw-code](https://github.com/instructkr/claw-code) |
| Fork（ck10100713） | [github.com/ck10100713/claw-code](https://github.com/ck10100713/claw-code) |
| Anthropic 洩漏報導（Axios） | [Anthropic leaked its own Claude source code](https://www.axios.com/2026/03/31/anthropic-leaked-source-code-ai) |
| SiliconANGLE 報導 | [Anthropic accidentally exposes Claude Code source code](https://siliconangle.com/2026/03/31/anthropic-accidentally-exposes-claude-code-source-code-npm-packaging-error/) |
| DEV Community 技術分析 | [Claude Code's Entire Source Code Was Just Leaked](https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo) |
| DEV Community Python 重寫 | [Anthropic leaked the source code... rewritten in Python](https://dev.to/embernoglow/anthropic-leaked-the-source-code-of-claude-code-written-in-ts-but-it-was-immediately-rewritten-in-210l) |
| Gizmodo 報導 | [Source Code for Claude Code Leaks at the Exact Wrong Time](https://gizmodo.com/source-code-for-anthropics-claude-code-leaks-at-the-exact-wrong-time-2000740379) |
| oh-my-codex（OmX） | [github.com/Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) |
| WSJ 報導 | [The Trillion Dollar Race to Automate Our Entire Lives](https://lnkd.in/gs9td3qd)（2026-03-21） |

## 專案概述

Claw Code 是 2026 年 3 月 31 日 **Claude Code 原始碼洩漏事件** 後誕生的 clean-room 重寫專案。作者 **Sigrid Jin**（GitHub: `instructkr`，韓國開發者社群 [instruct.kr](https://instruct.kr/) 主持人）在發現洩漏後數小時內，將 Claude Code 的 harness 架構以 Python 重新實作，目前正進行 Rust 重寫。

專案在發布後 **2 小時內突破 50K stars**，被稱為 GitHub 史上最快達成此里程碑的 repo。截至研究日，原始 repo 已有 **67,900+ stars、69,100+ forks**。

## 事件背景：Claude Code 原始碼洩漏

### 洩漏原因

Anthropic 在發佈 npm 套件 `@anthropic-ai/claude-code` v2.1.88 時，**意外包含了 `.map` source map 檔案**。這些檔案將 minified code 映射回完整原始碼，等同於將整個 codebase 以可讀形式公開。

Anthropic 官方聲明：*「這是由人為錯誤造成的發佈打包問題，不是安全漏洞。」*

### 洩漏內容

| 維度 | 數據 |
|------|------|
| 檔案數 | ~1,900 個 TypeScript 檔案 |
| 程式碼行數 | 512,000+ 行 |
| 內建工具 | ~40 個（權限閘控） |
| Slash 指令 | ~50 個 |
| 工具系統 | ~29,000 行（tool definitions + permissions） |
| Query Engine | ~46,000 行（LLM API 呼叫、streaming、cache） |

### 技術架構揭露

```
Claude Code 架構（從洩漏中觀察到）
├── Runtime: Bun（非 Node.js）
├── Terminal UI: React + Ink
├── Validation: Zod v4
├── Multi-Agent: "swarms" 平行任務協調
├── IDE Bridge: JWT-authenticated channels
├── Memory: 持久化 file-based memory
└── Lazy Loading: OpenTelemetry, gRPC 延遲載入
```

### 影響評估

| 面向 | 影響 |
|------|------|
| 使用者資料 | 未受影響 |
| 智慧財產權 | 重大損害——核心差異化技術曝光 |
| 競爭威脅 | 對手可深入了解 harness 設計 |
| 安全風險 | 工具權限模型、workflow 可被分析 |

## Claw Code 的 Clean-Room 重寫

### 開發過程

Sigrid Jin 在凌晨 4 點發現洩漏後，使用 [oh-my-codex（OmX）](https://github.com/Yeachan-Heo/oh-my-codex) 進行 AI 輔助移植：

- **`$team` 模式**：多 agent 平行 code review 和架構回饋
- **`$ralph` 模式**：持續執行迴圈 + architect 等級驗證
- 整個移植過程從閱讀原始 harness 結構到產出 Python tree + tests，全程由 OmX 協調

### 目前 Python 實作

```
src/
├── __init__.py
├── commands.py          # 指令移植 metadata
├── main.py              # CLI 入口（manifest/summary/parity-audit）
├── models.py            # dataclasses：subsystems, modules, backlog
├── port_manifest.py     # Python workspace 結構摘要
├── query_engine.py      # 移植摘要渲染
└── tools.py             # 工具移植 metadata
```

### 快速開始

```bash
# 渲染移植摘要
python3 -m src.main summary

# 輸出 workspace manifest
python3 -m src.main manifest

# 列出子系統
python3 -m src.main subsystems --limit 16

# 執行測試
python3 -m unittest discover -s tests -v

# 檢查指令/工具清單
python3 -m src.main commands --limit 10
python3 -m src.main tools --limit 10
```

### 重寫進度

| 狀態 | 說明 |
|------|------|
| Python 基礎 | 已完成——mirror 了 root-entry file surface、subsystem names、command/tool inventories |
| Runtime 對等 | 尚未完成——Python tree 的可執行 runtime slices 仍少於原始 TypeScript |
| Rust 移植 | 進行中（`dev/rust` branch），目標：更快、memory-safe 的 harness runtime |

## 目前限制 / 注意事項

- **法律爭議**：雖然標榜 clean-room rewrite，但由洩漏原始碼「學習架構」再重寫的邊界仍有灰色地帶
- **無 License**：原始 repo 和 fork 均未標示任何開源授權
- **功能不完整**：Python 版仍非 runtime-equivalent，更像是 harness 架構的 metadata mirror
- **Rust 版未完成**：`dev/rust` branch 仍在開發中
- **原始洩漏已移除**：repo 不再包含 Anthropic 原始碼的 snapshot

## 研究價值與啟示

### 關鍵洞察

1. **Harness Engineering 成為獨立研究領域**：Claw Code 的核心價值不在「複製 Claude Code」，而在將 harness（agent 如何串接工具、管理 context、協調任務）從特定產品中抽離出來研究。這與本站的 [Anthropic Harness Design](harness-design-long-running-apps.md) 研究互補。

2. **洩漏揭露的 Claude Code 架構決策值得學習**：Bun runtime、React+Ink TUI、Zod v4 validation、file-based persistent memory——這些選擇反映了「agent harness 應該是什麼形狀」的工程判斷，不論洩漏與否都值得研究。

3. **AI 輔助 AI 工具移植是可行的**：整個 TS→Python 移植由 OmX 的 `$team` + `$ralph` 模式驅動，展示了 coding agent 協作框架的實戰能力。這與本站研究的 [oh-my-codex](agent-orchestrator.md) 直接相關。

4. **npm source map 是嚴重的 supply chain 安全風險**：512K 行程式碼因一個 `.map` 檔案全部曝光，對所有 npm 套件開發者都是警示——build pipeline 必須明確排除 source maps。

5. **Star 速度不等於技術價值**：2 小時 50K stars 更多反映社群對洩漏事件的興奮，而非專案本身的技術成熟度。Python 版目前仍是 metadata mirror，距離可用的 harness runtime 還有很長的路。

### 與其他專案的關聯

| 相關筆記 | 關聯 |
|----------|------|
| [Anthropic Harness Design](harness-design-long-running-apps.md) | Anthropic 官方的 harness 設計文件，Claw Code 試圖逆向實作的對象 |
| [Analysis Claude Code](analysis-claude-code.md) | 另一個 Claude Code 分析專案，側重靜態程式碼分析 |
| [Claude Code Reverse](claude-code-reverse.md) | Claude Code 逆向工程研究 |
| [Agent Orchestrator (OmX)](agent-orchestrator.md) | Claw Code 開發過程使用的 AI 協作框架 |
| [OpenClaw](openclaw.md) | 另一個 Claude Code 相關的開源替代品 |
