---
date: "2026-09-16"
category: "Coding Agent 工具"
card_icon: "material-eye-lock"
oneliner: "台灣開發者 nathawu 寫的「確認優先（Confirm-First）」閘門外掛，同時支援 Claude Code 與 OpenAI Codex——AI 先用白話文覆述最多 5 點需求重點（自己補的假設要標「（假設）」），你按下「正確，開始執行」之前，PreToolUse hook 硬性擋掉除提問工具外的所有工具呼叫。實作只有 148 行核心 + 83 行 Codex adapter，測試卻有 487 行（33 個 case，實測 32 pass / 1 skip）。設計上刻意 fail-open：hook 自己出錯就放行，絕不卡住正常使用。目前 5★、3 個 commit、**沒有 LICENSE 檔**"
tags:
  - claude-code
  - codex
  - hooks
  - agent-safety
  - plugin
---

# Argus 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★5 / 0 forks / JavaScript） | [github.com/NathanWu8343/Argus](https://github.com/NathanWu8343/Argus) |
| 作者 | nathawu（NathanWu8343） |
| Topics | `claude-code`、`openai-codex` |

> **Metadata（2026-09-16 即時抓取）：** 建立於 **2026-09-14**、最後 push **2026-09-15**（只有兩天大，**3 個 commit**）· 預設分支 `master` · repo size 35 KB · **無 LICENSE 檔** · plugin 版本 `0.4.0`。
>
> 本筆記的判斷來自 `git clone` 後**實際讀完全部原始碼並在本機跑過測試**（`node --test "tests/*.test.js"` → 33 tests / 32 pass / 1 skip，skip 的那個需要設定 `CODEX_CLI` 指向 Codex CLI 進入點）。

!!! warning "三個要先知道的事"
    - **沒有 LICENSE 檔。** repo 公開但沒授權聲明，法律上預設是「保留所有權利」——可以讀、可以學，但要拿去改造散布或塞進公司流程前，最好先問作者。
    - **它是 fail-open，不是 fail-safe。** `core.js` 最外層用 `try/catch` 把所有錯誤吞掉，註解寫得很明白：「A failure inside argus always lets the action through; it must never block normal use」。所以 Node.js 沒裝、狀態目錄不可寫、JSON 解析失敗，閘門會**安靜地打開**。當成「防手滑」很好，當成「安全邊界」不行。
    - **很新、很小。** 兩天大、3 個 commit、5 顆星。設計品質不錯，但還沒被時間驗證過。

## 專案概述

Argus（百眼巨人）解決的是一個每天都在發生的問題：**你講 A、AI 做 B，等你發現時它已經改了七個檔案。**

作法是在 AI 動手前插一道閘門：

1. 你用 `/argus:confirm-first <需求>`（Claude Code）或 `$confirm-first <需求>`（Codex）發動。
2. AI **不准碰任何工具**，只能根據你的文字，列出最多 5 點白話需求重點；自己補的部分要另外列並前綴「（假設）」。
3. AI 用 `AskUserQuestion` 跳出三選一：`正確，開始執行` / `需要修正` / `取消此請求`。
4. 你選「正確，開始執行」，閘門才放行。

README 給的範例長這樣：

```text
需求重點：
1. 將現有單欄登入表單調整為雙欄網格佈局
2. 左欄保留登入輸入框與送出按鈕
3. 右欄加入品牌宣傳橫幅與說明文字
4. （假設）維持既有表單驗證與 API 串接邏輯
```

## 架構：一個核心 + 兩個 adapter

整包程式碼小到可以全部讀完：

| 檔案 | 行數 | 作用 |
|---|---|---|
| `hooks/core.js` | 125 | 共用狀態機與決策邏輯 |
| `hooks/argus.js` | 23 | Claude Code adapter |
| `codex/src/argus.js` | 83 | Codex adapter |
| `scripts/build-codex.js` | 46 | 從 `codex/src/` 產生可安裝的 Codex 套件 |
| `tests/*.js` | 487 | 33 個測試 |

**測試行數是實作的 1.7 倍**，這在只有 3 個 commit 的個人專案裡很少見。

`core.js` 開頭的註解直接定義了 adapter 介面，宿主之間所有差異都收斂在這裡：

```js
//   stateNamespace    host subdirectory when ARGUS_STATE_DIR overrides the default
//   stateDir          default directory for state files
//   invocation        RegExp matching a prompt that starts the gate
//   questionTool      tool name allowed while pending
//   answerOf          (tool_response, question) → the label the user picked, or undefined
//   denyReason        text returned when a tool is denied
//   stopReason        when set, ending the turn is blocked once while pending
```

兩個宿主的差異：

| | Claude Code | OpenAI Codex |
|---|---|---|
| 觸發 | `/argus:confirm-first` | `$confirm-first`（也吃 `[$confirm-first](...)` 連結形式） |
| 允許的提問工具 | `AskUserQuestion` | `request_user_input` |
| 狀態目錄 | `~/.claude/argus` | `$CODEX_HOME/argus`（預設 `~/.codex/argus`） |
| 答案取法 | `response.answers[question.question]` | `answers[question.id].answers`（陣列，長度必須是 1） |
| `Stop` hook | 有，會擋一次讓回合結束在提問上 | **沒有**（答案是以下一則 prompt 進來的，回合必須能結束） |

## 狀態機：一個 `.pending` 檔就是全部

狀態只有 `idle` 與 `pending` 兩種，而 **pending 的定義就是「狀態檔存在」**：

```
~/.claude/argus/<session_id>.pending
```

沒有資料庫、沒有 JSON schema、沒有記憶體常駐，檔案在就是 pending，檔案不在就是 idle。副作用是**閘門會跨 session 存活**——你關掉再 `--resume`，閘門還在。被放生的狀態檔則在每次 prompt 時掃一遍，超過 24 小時就清掉。

四個 hook 的分工：

- **`UserPromptSubmit`**：比對 `invocation` 正則決定要不要進 pending；如果這則 prompt 剛好是確認標籤，就解除。
- **`PreToolUse`（matcher `*`）**：pending 期間，除了提問工具一律回 `permissionDecision: "deny"`，並在 `permissionDecisionReason` 裡告訴模型「現在在對齊需求，把覆述寫完然後用 AskUserQuestion 問」。
- **`PostToolUse`**：抓提問工具的回答，`正確，開始執行` → 解除並注入 `additionalContext` 要模型照最後一版覆述執行。
- **`Stop`**（僅 Claude）：pending 且還沒擋過就 `decision: "block"`，逼模型把回合結束在提問上。用 `stop_hook_active` 防止無限迴圈。

## 三個設計細節值得抄

**1. 確認必須是精確字串，語意上的「好」不算**

```js
return label === CONFIRM || label === CANCEL ? label : null;
```

SKILL.md 也寫死：「Free text that merely means confirm or cancel is not one; ask again.」模型不能自己判斷「使用者應該是同意了」——這正是這類閘門最容易被繞過的地方。

**2. Codex 版把 skill 內文塞進 context，因為閘門擋住了檔案讀取**

閘門連 Read 都擋，所以 Codex adapter 不能叫模型自己去讀 SKILL.md，它直接在 `UserPromptSubmit` 時把 skill 全文當 `additionalContext` 注入：

```js
// The gate denies file reads, so the skill text travels with the prompt instead of being read from disk.
```

這是「把自己的規則擋在門外」的典型陷阱，作者有意識地處理掉了。

**3. 明令禁用 async 提問工具**

Codex adapter 的 deny reason 特別寫「Never use `request_user_input_async`（its question card is dismissed when the turn ends）, sleep or any other tool while waiting」。這種宿主層級的坑只有實際踩過才寫得出來。

## 安裝

需要 Node.js。

=== "Claude Code"

    ```bash
    claude --plugin-dir /path/to/Argus
    ```

=== "OpenAI Codex"

    ```powershell
    codex plugin marketplace add .
    codex plugin add argus@argus
    codex features enable default_mode_request_user_input
    ```

Codex 的 `default_mode_request_user_input` 是讓 Default 模式支援選項卡片用的實驗功能；嫌警告吵可在 `config.toml` 加 `suppress_unstable_features_warning = true`。

## 開發與除錯

```bash
node scripts/build-codex.js           # 從 codex/src/ 產生 codex/plugins/argus/
node scripts/build-codex.js --check    # 檢查產生套件與原始碼是否同步
node --test "tests/*.test.js"
```

`ARGUS_DEBUG=1` 會把每次 hook 的 stdin 原文寫進狀態目錄的 `debug.log`。另外 `ARGUS_STATE_DIR` 可以把狀態目錄整個搬走（測試隔離就是靠這個，`tests/isolation.test.js`）。

## 評估

**適合**：架構重構、跨模組修改、DB schema 或生產設定這類不可逆操作，以及需求本身就長又模糊的時候。用一次對齊換掉「AI 改錯 → `git reset` → 重來」的成本。

**不適合**：當成安全機制。fail-open 的設計意味著它防的是誤解，不是惡意；真的要擋危險操作應該用 permission rules 或 deny hook。

**還缺的**：
- 沒有 LICENSE。
- 沒有 CI，測試要手動跑。
- `disable-model-invocation: true` 代表只能手動觸發，沒有「偵測到高風險操作就自動開閘」的模式。
- 狀態檔用 `session_id` 當檔名，多個併發 session 各自獨立（這點是對的），但沒有跨 session 的全域開關。

## 相關筆記

- [Claude Code 最佳實踐（Boris Cherny）](claude-code-boris-cherny-tips.md) — hooks 與權限控制的官方觀點
- [Coding Agent 工具總覽](topics/coding-agent-tools.md)
