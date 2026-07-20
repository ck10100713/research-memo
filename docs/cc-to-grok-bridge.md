---
date: "2026-07-20"
category: "Coding Agent 工具"
card_icon: "material-bridge"
oneliner: "把 Claude Code 的 rules/skills/hooks/memory 搬到 Grok Build — 靠 thin adapter 讓 CC 資安 hook 在 Grok 上真正 hard-block"
tags:
  - claude-code
  - harness
  - mcp
  - memory
---

# cc-to-grok-bridge 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [github.com/yyu0310/cc-to-grok-bridge](https://github.com/yyu0310/cc-to-grok-bridge) |
| README（英/繁/簡） | repo 內 `README.md` / `README.zh-TW.md` / `README.zh-CN.md` |
| 設計不變量 | repo 內 `architecture.md` |
| 差距矩陣 / SOP | repo 內 `docs/00_差距矩陣.md`、`docs/01_絲滑啟動.md` |

**GitHub 數據**：9 stars（很新，2026-07 建立）、Python、MIT License、macOS/Linux + Python 3.10+

## 專案概述

cc-to-grok-bridge 解決一個具體痛點：**你已經在 Claude Code 建好一整套 rules / slash skills / 資安 hooks / memory，想把同一套搬到 [Grok Build](https://x.ai/)（xAI 的 coding agent）上用，而不是重做一遍。**

它不是「複製設定」那麼簡單——不同 harness 的 hook 契約、memory 格式、MCP 安裝方式都不一樣。這個 bridge 用**一層薄 adapter** 把 Claude Code 既有的資產「翻譯」給 Grok，核心原則是：

- **單一真相來源（single source of truth）**：blocklist / 安全策略仍留在 CC 的 hook 腳本裡，不 fork、不複製一份給 Grok
- **真正的 hard-block**：不是「請模型記得別做」，而是工具呼叫**實際被拒絕**
- **secrets 永不自動複製**：MCP env / token / OAuth 一律不搬

它是同作者一系列「把 CC 搬到別的 agent」橋接工具之一，姊妹作是難度更高的 [cc-to-antigravity-cli-bridge](cc-to-antigravity-cli-bridge.md)。README 直言：搬到 Grok Build 通常**比 Antigravity / Gemini 那條路順很多**（有真 hard-block、memory 更簡單）。

## 核心設計：Hook Adapter（整個專案的關鍵）

Claude Code 的 hook 是 shell 腳本（例如擋讀 `.env`）。Grok 也跑 hook，但兩者契約不同：

1. **stdin 的 JSON 欄位名不同**（payload 形狀）
2. **「擋下這個工具呼叫」怎麼回報不同**（deny 協定）

所以不能讓 Grok 直接指向 CC 腳本。`scripts/hook_adapter.py` 這層薄 adapter 夾在中間：Grok 呼叫它 → 它呼叫你既有的 `~/.claude/hooks/*.sh`。

| 術語 | 意思 |
|------|------|
| **Thin adapter** | 只做格式翻譯，**不重寫**安全策略 |
| **Wraps CC scripts** | 呼叫同一批腳本，policy 本體留在 CC 端 |
| **Payload normalize** | 把 Grok 欄位名映射成 CC 腳本要的（如 `target_file` → `file_path`） |
| **Deny translate** | CC 常用 `exit 2` + stderr；adapter 轉成 Grok 的 `{"decision":"deny", …}` |

```
Grok 工具呼叫 ──▶ hook_adapter.py ──▶ ~/.claude/hooks/block_sensitive_read.sh
                  (欄位/deny 翻譯)        (真正的安全策略，唯一真相來源)
                       │
                       └──▶ 回傳 Grok 格式的 allow / deny
```

## 六個相容層（Compatibility Matrix）

| 層 | 相容度 | 能用什麼 | 缺口 |
|----|-------|---------|------|
| System Prompt | 高 | 同一份 workspace `CLAUDE.md`（Grok compat 自動載入） | — |
| skill | 高 | 同一組 `~/.claude/commands`（symlink 也 OK） | frontmatter / trigger 些微差異 |
| Memory | 高 | `memory_sync` + rules pointer + 三區隔離；可選 push | 非 CC 的 MEMORY.md index 載入方式 |
| Hooks | 中 | adapter + 你的 CC hard-block 腳本 | payload/deny 翻譯；無完整 CC ask UI |
| MCP | 中 | 按類型重裝（HTTP key / OAuth / stdio） | claude.ai cloud connector 不可移；secrets 不自動複製 |
| Plugins | 低 | A: 有 Grok 打包才裝；B: rules 常駐 `.grok/rules/` | CC 設定不會自動移植；marketplace 不同 |

## 其他值得注意的元件

### ccgrok.sh — 把 Grok 當紀律化研究工具

一個小 wrapper 驅動 `grok -p`，會先掛上一段 model-agnostic 的研究方法 prefix（`research-prefix.md`），並從乾淨的 temp 目錄執行，讓純研究查詢**不被專案規則污染**。

```bash
scripts/ccgrok.sh "your question"
```

- prefix 強制「有出處、標日期、事實與臆測分離」的回答，並讓 Grok 主動標記過時/降級的事實而非自信地講錯
- 唯讀旗標 `--disallowed-tools "run_terminal_cmd,write,search_replace"` 讓它即使在 auto-approve 下也**碰不到本地檔案**
- 同一份 `research-prefix.md` 可套任何 headless AI CLI（`grok -p`、`agy -p`、`claude -p`）

### 三區記憶隔離

memory 分區設計，讓 **Grok-only 的資產永遠不進 Claude 的 context**；`memory_sync.py` 做 CC → Grok 單向 pull，`memory_push.py` 是可選的受限回推（只有 `general/` → CC）。日常使用**不需先開 `[memory] enabled=true`**——rules pointer 會隨專案載入。

### 腳本清單

| 腳本 | 角色 |
|------|------|
| `install_bridge.py` | 裝 adapter + Grok hooks JSON；關掉重複觸發 |
| `bridge_doctor.py` | 唯讀健檢 + hard-block 冒煙測試（期望 `fails=0`） |
| `hook_acceptance.py` | adapter 層驗收測試 |
| `memory_sync.py` / `memory_push.py` | 記憶 pull / 受限 push |

## 目前限制 / 注意事項

- **MCP secrets 不自動搬**：claude.ai cloud connector 不可移植，需按 `docs/03_mcp.md` / `AGENTS.md` 重裝
- **全域 Grok memory ≠ CC 專案 memory**：`~/.grok/memory/MEMORY.md`（`/remember`）與 CC 專案記憶不同，sync 用專案子資料夾
- **Plugins 相容度低**：CC 自動啟用的 plugin ≠ Grok 的 per-session 注入，需走 A（有 Grok 打包才裝）或 B（`.grok/rules/` 常駐文字）
- **裝完要重啟 session**：從 workspace root 重開 Grok 讓 hook reload
- **極早期專案**：2026-07 建立、star 數個位數，尚未有廣泛實測

## 研究價值與啟示

### 關鍵洞察

1. **「adapter 而非 fork」是跨 harness 移植的正解**——最誘人的錯誤做法是把 CC 的安全腳本複製一份改成 Grok 版，結果是兩份會 drift 的 blocklist。這個專案堅持**薄翻譯層 + 單一真相來源**：policy 本體只有一份，adapter 只做欄位/deny 格式轉換。這是所有「A 工具設定搬到 B 工具」場景都該遵守的架構原則。

2. **hard-block 與「請模型記得」是本質不同的安全等級**——README 反覆強調「not model please remember；the tool call is actually denied」。這點出 agent 資安的核心：**寫在 prompt 裡的禁令是軟約束、會被繞過；掛在 hook / 執行層的攔截才是硬約束**。移植時若只搬 prompt 不搬 hook，安全性會悄悄降級。

3. **coding agent harness 正在「去平台鎖定」**——rules、skills、hooks、memory 這些資產原本綁死在某個 harness。這類 bridge 出現，代表使用者開始把自己的 agent 設定視為**可攜的資產**，而非某個工具的附庸。若這種橋接普及，harness 之間的競爭會從「鎖定資產」轉向「執行品質」。

4. **相容度矩陣是誠實工程的範本**——它不吹「完美相容」，而是逐層標 高/中/低 並列出缺口（Plugins 低、MCP secrets 不可搬）。這種「明講哪裡不行」的文件，比多數宣稱 seamless 的遷移工具可信得多，也是評估任何移植方案時該要求看到的東西。

5. **研究 prefix 的可攜性呼應同一哲學**——`research-prefix.md` 刻意做成 model-agnostic，一份 prefix 套 Grok / Antigravity / Claude 三家 CLI。這與整個專案「資產應可攜、不綁單一模型」的立場一致：連 prompt 工程都當成跨模型資產在管理。

### 與其他專案的關聯

- **姊妹作 [cc-to-antigravity-cli-bridge](cc-to-antigravity-cli-bridge.md)**：同作者、同架構思路，但目標換成 Google Antigravity / Gemini。README 直言 Antigravity 那條路更難（hard-block 較弱、memory 較複雜），是研究「不同 harness 移植難度」的絕佳對照組
- **vs [Claude Agent SDK](claude-agent-sdk.md) / [OpenAI Agents SDK](openai-agents-sdk.md)**：SDK 是「從零建 agent」，這個 bridge 是「把既有 agent 設定橫移到另一個 harness」——兩者互補，反映 agent 生態從「怎麼建」走向「怎麼搬/怎麼互通」
- **Hook / 資安角度**：與研究筆記中談 agent 安全治理的專案（如 skill 資安審查流程）同屬「執行層硬約束」思路
