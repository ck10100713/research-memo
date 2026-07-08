---
date: "2026-07-08"
category: "Coding Agent 工具"
card_icon: "material-head-lightbulb"
oneliner: "executor（Sonnet/Haiku）生成中途諮詢 advisor（Opus）取得策略指引，近 Opus 品質、Sonnet 成本的 Anthropic beta 工具"
tags:
  - harness
  - multi-agent
  - prompt-engineering
---

# Advisor Tool（顧問工具）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方文件 | <https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool> |
| 官方部落格：The advisor strategy | <https://claude.com/blog/the-advisor-strategy> |
| LiteLLM 支援文件 | <https://docs.litellm.ai/docs/completion/anthropic_advisor_tool> |
| Builder.io 分析 | <https://www.builder.io/blog/the-claude-advisor-pattern> |
| The Agent Report（進階工具使用平台綜述） | <https://the-agent-report.com/2026/06/anthropic-advanced-tool-use-platform-june-2026/> |

> Beta 功能，需在請求帶上 header：`anthropic-beta: advisor-tool-2026-03-01`。

## 功能概述

Advisor tool 是 Anthropic 在 Claude API 推出的 **beta server tool**，核心概念是把一次 agentic 任務拆成兩個角色：

- **Executor（執行者）**：較快、較便宜的模型（Haiku / Sonnet），負責跑完整個任務——呼叫工具、讀結果、迭代收斂，產生絕大部分的 token。
- **Advisor（顧問）**：更聰明的模型（Opus / Fable 5 / Mythos 5），只在**生成中途**被叫來一次或數次，讀完整段對話後給出一份計畫或修正方向，然後 executor 帶著建議繼續。

這個「委託人—代理人」（principal-agent）模式專為**長程 agentic 工作負載**設計（coding agent、computer use、多步驟研究 pipeline）——這類任務大多數回合都是機械性操作，但「有一個好計畫」是成敗關鍵。結果就是：**token 產出主要以 executor 費率計價，品質卻逼近 advisor 單獨執行**。

官方基準（來自部落格）：

| 組合 | 效果 |
|------|------|
| Sonnet + Opus advisor（vs Sonnet 單獨） | SWE-bench Multilingual **+2.7pp**，每任務成本 **−11.9%** |
| Haiku 4.5 + Opus advisor（vs Haiku 單獨） | BrowseComp **19.7% → 41.2%**（>2x） |

## 適用與不適用場景

**適合：**

- 目前用 **Sonnet** 做複雜任務 → 加 Opus 當 advisor，成本相近或更低卻拉高品質。
- 目前用 **Haiku** 想要智力升級 → 加 Opus advisor，成本高於純 Haiku，但低於直接把 executor 換成大模型。

**不適合：** 單輪 Q&A（沒東西可規劃）、使用者自行選模型的純轉發場景、以及**每一回合都真的需要 advisor 全部能力**的工作負載（那不如直接用大模型當 executor）。

## 模型相容性

Executor 是頂層 `model` 欄位，advisor 是工具定義內的 `model` 欄位。規則：**advisor 必須是 Sonnet 4.6 或更強，且至少與 executor 同級**。同級可互為顧問（如 Opus 4.7 ↔ Opus 4.8）。

| Executor | 可用 Advisor |
|----------|-------------|
| Haiku 4.5 / Sonnet 4.6 | Fable 5、Mythos 5、Opus 4.8/4.7/4.6、Sonnet 4.6 |
| Sonnet 5 | Fable 5、Mythos 5、Opus 4.8/4.7 |
| Opus 4.6 | Fable 5、Mythos 5、Opus 4.8/4.7/4.6 |
| Opus 4.7 / Opus 4.8 | Fable 5、Mythos 5、Opus 4.8/4.7 |
| Fable 5 | Fable 5（僅自身） |
| Mythos 5 | Mythos 5（僅自身） |

無效組合會回 `400 invalid_request_error`。

**平台可用性**：Claude API 與 Claude Platform on AWS（beta）。**尚未支援** Amazon Bedrock、Google Cloud、Microsoft Foundry。

## 快速開始

```python
client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",           # executor
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-8",   # advisor
        }
    ],
    messages=[
        {"role": "user", "content": "Build a concurrent worker pool in Go with graceful shutdown."}
    ],
)
```

## 運作機制

把 advisor 加進 `tools` 後，**由 executor 自行決定何時呼叫**（跟一般工具一樣）。一次呼叫的流程全部在**同一個 `/v1/messages` 請求內**完成，不需要你多做 round trip：

```
Executor 產出 server_tool_use (name="advisor", input={})   ← executor 決定「時機」
        │
        ▼
Anthropic 伺服器端跑一次獨立 advisor 推論              ← 伺服器供給「context」
   · advisor 用自己的 system prompt
   · 收到 executor 的完整 transcript 當引用 context
   · 無工具、無 context management，thinking blocks 會被丟棄
        │
        ▼
結果以 advisor_tool_result 回到 executor
        │
        ▼
Executor 帶著建議繼續生成
```

關鍵細節：`server_tool_use.input` **永遠是空的**——advisor 看到的內容由伺服器從完整 transcript 自動建構，executor 塞進 input 的東西不會傳到 advisor。

## 工具參數

| 參數 | 說明 |
|------|------|
| `type` | 必填，`"advisor_20260301"` |
| `name` | 必填，`"advisor"` |
| `model` | 必填，advisor 模型 ID；此 sub-inference 以該模型費率計價 |
| `max_uses` | 單一請求內最多呼叫次數。超過回 `max_uses_exceeded` 錯誤，executor 繼續（**per-request 而非 per-conversation**） |
| `max_tokens` | 每次 advisor 輸出上限（thinking + text），最小 1024 |
| `caching` | `{"type":"ephemeral","ttl":"5m"｜"1h"}`，開關型（非 breakpoint），為 advisor 自身 transcript 做快取 |

## 回應結構與錯誤處理

成功時 assistant content 內會有 `server_tool_use` 後接 `advisor_tool_result`。`content` 是 discriminated union：

- `advisor_result`（含 `text`）：多數模型（如 Opus 4.8）回明文建議。
- `advisor_redacted_result`（含 `encrypted_content`）：**Fable 5 / Mythos 5** 回加密 blob，你讀不到，但下一輪伺服器會解密還原給 executor。

> 兩種都要在後續回合**原封不動 round-trip**。若中途換 advisor 模型，用 `content.type` 分支處理兩種形狀。

Advisor 呼叫失敗**不會讓整個請求失敗**，executor 看到錯誤後繼續。錯誤碼：`max_uses_exceeded`、`too_many_requests`（advisor 被 rate limit）、`overloaded`、`prompt_too_long`（transcript 超過 advisor context window）、`execution_time_exceeded`、`unavailable`。

> Rate limit 分開算：advisor 的 429 變成工具結果內的 `too_many_requests`；executor 的 429 才會讓整個請求以 HTTP 429 失敗。

## 多輪對話與暫停

- 後續回合必須把包含 `advisor_tool_result` 的完整 assistant content 傳回。
- 若歷史仍有 `advisor_tool_result` 但 `tools` 沒帶 advisor 工具 → `400` 錯誤。
- **無內建 conversation-level 上限**。要限制整段對話的 advisor 次數，得 client 端自己數；達到上限時要**同時移除 advisor 工具並清掉所有 `advisor_tool_result` blocks**，否則報 400。
- **`pause_turn`**：advisor 呼叫還沒完成時回應可能以 `stop_reason: "pause_turn"` 結束（帶 `server_tool_use` 但無結果）。把該 assistant 訊息原樣附回、帶同樣工具與 header 再送一次即可續跑，不需加 user 訊息或 `tool_result`。若同一回合 executor 也叫了你的工具，則以 `stop_reason: "tool_use"` 結束，送回 `tool_result` 後，pending 的 advisor 呼叫會在下個請求開頭執行。

## 計費與用量

Advisor 是獨立 sub-inference，以 advisor 模型費率計價，用量報在 **`usage.iterations[]`** 陣列：

- `type: "message"` 的 iteration → executor 費率。
- `type: "advisor_message"` 的 iteration → advisor 費率。
- **頂層 `usage` 只反映 executor tokens**；advisor tokens 不併入頂層（費率不同）。頂層 `output_tokens` = 所有 executor iteration 加總；頂層 `input_tokens` 只取第一個 executor iteration。要精算成本請用 `iterations`。
- Advisor 輸出通常 400–700 text tokens（含 thinking 約 1,400–1,800）。省錢來自「advisor 不產出你的完整最終輸出」，那部分由較便宜的 executor 完成。
- 頂層 `max_tokens` 只管 executor；要限 advisor 得在工具定義設 `max_tokens`。Advisor tokens 也不吃 executor 的 task budget。
- Priority Tier 各模型獨立——executor 有承諾不等於 advisor 也走 priority。

## 成本與品質調校（重點實務）

這份文件最有價值的部分是大量 Anthropic 內部實測的調校手法：

**1. 引導呼叫時機（system prompt steering）**

- 內建工具描述已會提示 executor 在複雜任務開頭與遇到困難時呼叫；研究任務通常不必額外提示。
- **Coding 任務常會 under-call**，官方提供了建議 system prompt（timing block + 如何對待建議 block），核心原則：**在「實質工作」前先呼叫**（寫檔、下判斷、建立假設之前）；orientation（找檔、抓來源）不算實質工作。任務完成前也呼叫一次，且**先把成果落地（寫檔/commit）再呼叫**，因為 advisor 呼叫耗時，session 中斷時已落地的成果才留得住。
- Haiku 有專用的更積極 block（含 "Hard rule：第一次 write/edit/改狀態的 bash 前必須先呼叫 advisor"），內部 coding benchmark 提升約 **+7.5pp**；但在 browse-comprehension benchmark 反而掉約 4pp——混合工作負載要小心。

**2. Nudge（提醒 under-calling 的 executor）**

- 若 Haiku executor 第一個 assistant 回合沒叫 advisor，在第二回合前補一則 user 提醒訊息，內部評測 pass rate 約 **+7pp**。
- **Sonnet 無明顯效果，Opus 反而略降 pass rate（不要用）**。
- 副作用：nudge 讓 turn-2 立刻呼叫的比例 Sonnet 74%、Haiku 98%——若在 executor 讀懂問題前就觸發，會產生低 context 的無效呼叫。baseline 首呼在 turn 7+ 的工作負載被 turn-2 nudge 打擾，反而掉 3–4pp。**先量自己的 baseline 首呼回合再決定 `NUDGE_TURN`**。
- 要在特定請求強制呼叫，用 `tool_choice: {"type":"tool","name":"advisor"}`（不能與 extended thinking 併用，否則 400）。

**3. 縮短 advisor 輸出（最大成本驅動）**

- 頂層 `max_tokens` 管不到 advisor。兩種做法：
  - **軟限制（prompt）**：在 user 訊息加一行**直接對 advisor 說話**的指示（advisor 把 system + user 都當引用 context，第二人稱比第三人稱描述可靠得多）：`(Advisor: please keep your guidance under 80 words ...)`。因是軟限制，要求約真正上限的 80%。
  - **硬上限（`max_tokens`）**：工具定義設 `max_tokens`（最小 1024），伺服器會把剩餘預算傳給 advisor 讓它自我塑形。推薦起點 **2048**（實測輸出約降 7x、幾乎不截斷）；1024 降約 10x 但約 10% 被截。截斷時結果帶 `stop_reason: "max_tokens"`，並在文字尾附 `[Advisor output truncated at max_tokens=2048.]`。

**4. Advisor prompt caching**

- 兩層獨立快取：executor 側（`advisor_tool_result` 本身可被 `cache_control` 快取）與 advisor 側（工具定義的 `caching`）。
- Advisor 側 caching **約 3 次呼叫才損益兩平**，之後才划算——長 agent loop 開、短任務關。設定要**整段對話保持一致**，中途切換造成 cache miss。
- ⚠️ `clear_thinking` 若 `keep` 非 `"all"` 會位移 advisor 引用 transcript，造成 advisor 側 cache miss（只是成本退化，不影響品質）。啟用 extended thinking 又沒設 `clear_thinking` 時，較舊 Opus/Sonnet 與所有 Haiku 預設 `keep: thinking_turns=1` 會踩到；設 `keep: "all"` 保穩定。

**5. 搭配 effort**：Sonnet executor 用 medium effort + Opus advisor，可達接近 Sonnet default effort 的智力但更便宜。

## 目前限制 / 注意事項

- Beta 階段，需帶 `advisor-tool-2026-03-01` header；僅 Claude API 與 AWS 平台，其他雲端未支援。
- Advisor sub-inference **不 streaming**——executor 串流會暫停直到 advisor 完成，結果一次到位（暫停期間僅有約每 30 秒的 SSE `ping`）。
- Advisor **無工具、無 context management**，thinking blocks 被丟棄，只有建議文字回到 executor。
- 無 conversation-level 呼叫上限，需 client 端自行控管。
- Context editing 的 `clear_tool_uses` 與 advisor blocks **不完全相容**。
- Token counting 只回 executor 首 iteration input；advisor 估算需另用 advisor 模型呼叫 `count_tokens`。

## 研究價值與啟示

### 關鍵洞察

1. **這是「把 orchestration 內建進 API」的一步**——過去要自己在 harness 裡串「便宜模型跑活、貴模型審計畫」（OpenClaw 之類的 principal-agent 模式都是手工做），現在變成單一請求內的 server tool，省去多次 round trip 與狀態管理。與本站〈[Anthropic Harness Design](harness-design-long-running-apps.md)〉的長程 agent 設計思路一脈相承。

2. **成本結構的巧思在「誰產出 token」**：advisor 只吐 400–700 token 的計畫，你的完整最終輸出仍由便宜的 executor 產。所以省錢的前提是**任務夠長、機械性回合夠多**；單輪任務用它反而是純加價。

3. **「時機」比「次數」重要**：文件反覆強調早期一次（探索後、動手前）+ 收尾一次（寫檔後、宣告完成前）兩個時點。太早（沒 context）或太晚（approach 已定型）都拉低價值——這其實是把人類 code review 的「設計前對齊 + 交付前複查」節奏編碼進 prompt。

4. **大量調校是「行為工程」而非「模型能力」**：nudge、hard rule、80-word 限制、`NUDGE_TURN` 這些都是在**操縱 executor 的呼叫行為**，且每個手法都附「在某工作負載 +7pp、在另一工作負載 −4pp」的誠實副作用。啟示：任何 prompt 級別的行為調整都該在自己的 workload 上量測，官方數字只是量級參考。

5. **加密結果（Fable 5 / Mythos 5）揭示了模型分層**：這兩個模型的建議以 `encrypted_content` 回傳、client 讀不到——暗示 Anthropic 對某些高階模型的中間產物做保護，開發者只能「round-trip 不能觀察」。設計整合時要用 `content.type` 分支，別假設一定拿得到明文。

### 與其他專案的關聯

- **〈[Anthropic Harness Design](harness-design-long-running-apps.md)〉**：advisor tool 正是「長程任務的 harness」思路的官方原語化。
- **〈[Claude Agent SDK](claude-agent-sdk.md)〉**：SDK 是搭建 agent 的框架，advisor tool 是可插入其中的成本/品質最佳化零件。
- **〈[多 Agent 辯論會](multi-agent-debate.md)〉**：同屬「多模型協作提升品質」家族，但 advisor 是非對稱的 executor↔advisor 分工，而非對等辯論——用一次貴推論換全程品質，成本模型完全不同。
- **〈[OpenClaw](openclaw.md)〉/ principal-agent 模式**：社群早已手工實作「便宜模型幹活、貴模型當顧問」，advisor tool 等於把這個 pattern 收進 API 官方支援。
