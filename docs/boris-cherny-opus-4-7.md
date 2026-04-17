---
date: "2026-04-17"
category: "Coding Agent 工具"
card_icon: "material-brain"
oneliner: "Claude Code 創辦人 Boris Cherny 在 Opus 4.7 發表當天公開的 6 個生產力技巧與行為差異全解析"
---
# Boris Cherny × Claude Opus 4.7 — 發表當天的使用心得與 6 個新技巧

## 資料來源

| 項目 | 連結 |
|------|------|
| Anthropic 官方新聞 | [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) |
| Boris 推薦官方最佳實踐 | [Best Practices for Using Claude Opus 4.7 with Claude Code](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code) |
| Boris Threads 貼文（上線公告） | [Opus 4.7 is in Claude Code today](https://www.threads.com/@boris_cherny/post/DXMqkOkFOGr/) |
| Boris Threads 貼文（學習心得） | [Opus 4.7 feels more intelligent, agentic, and precise](https://www.threads.com/@boris_cherny/post/DXMzhV-lPuQ/) |
| Boris Threads 貼文（6 Tips 串） | [Dogfooding Opus 4.7 — 6 Tips](https://www.threads.com/@boris_cherny/post/DXM_ATtjxna/) |
| Boris X 貼文（Effort 調整） | [Configure your effort level](https://x.com/bcherny/status/2044847856872546639) |
| 社群整理 | [shanraisshan/claude-code-best-practice — 6 tips](https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-boris-6-tips-16-apr-26.md) |
| 第三方評測（Opus 4.7 for AI Code Review） | [CodeRabbit Blog](https://www.coderabbit.ai/blog/claude-opus-4-7-for-ai-code-review) |
| 限制與問題報導 | [Sherwood News — doom loops](https://sherwood.news/tech/anthropic-releases-claude-opus-4-7-with-better-coding-better-vision-and-occasional-doom-loops/) |
| Snowflake 合作 | [Announcing Claude Opus 4.7 on Snowflake Cortex AI](https://www.snowflake.com/en/blog/claude-opus-4-7-snowflake-cortex-ai/) |

## 發表背景

| 項目 | 內容 |
|------|------|
| 發表日期 | **2026-04-16** — Anthropic 正式釋出 Opus 4.7 |
| 作者 | **Boris Cherny** — Claude Code 創辦人 / Anthropic Staff Engineer |
| Model ID | `claude-opus-4-7` |
| 價格 | 輸入 **$5/M tokens**、輸出 **$25/M tokens**（與 4.6 相同） |
| 預設 Effort | **`xhigh`** — 新增介於 `high` 與 `max` 之間的等級 |
| 視覺能力 | 接受長邊 **2576px（約 3.75 MP）圖像**，是過往 Claude 的 **3 倍** |
| 可用平台 | Claude 產品線、API、Amazon Bedrock、Google Cloud Vertex AI、Microsoft Foundry、Snowflake Cortex |

Boris Cherny 在模型發表後連發多條 Threads：**「Opus 4.7 比 4.6 更聰明、更 agentic、更精準。我花了幾天才學會如何有效地使用它。」** 接著釋出 Anthropic 內部 dogfood 幾週後的 **6 個生產力技巧**。

---

## Boris Cherny 的核心感想

| 面向 | Boris 原話 / 觀察 |
|------|------------------|
| **整體定位** | 「更 agentic、更精準、在長時間任務上表現好很多」 |
| **上下文持續性** | 跨 session 能攜帶 context，處理模糊需求的能力大幅提升 |
| **單一 prompt 承載量** | 多檔修改、模糊除錯、整個服務的 code review，**一個 prompt 就能完成**。這些過去必須切成小塊因為模型會 drift |
| **學習曲線** | 需要幾天時間重新調整 prompt 策略，才能完全發揮新能力 |
| **生產力體感** | Dogfood 幾週後「感覺前所未有地生產力」 |

---

## Boris 的 6 Tips（2026-04-16）

### Tip 1 — Auto Mode：擺脫許可提示

Opus 4.7 特別擅長長時間任務（深度研究、重構、建複雜功能、迭代到打中效能基準）。過去要嘛 babysit，要嘛用 `--dangerously-skip-permissions`。

**Auto Mode** 的安全替代方案：

- 許可提示交給 **classifier 模型** 判斷
- 安全 → 自動核准
- 風險 → 暫停詢問
- **意義**：可以把焦點切到下一個 Claude，**平行跑更多 session**

```
Shift+Tab 循環：Ask permissions → Plan mode → Auto mode
```

> 目前開放給 Max / Teams / Enterprise 使用者。

### Tip 2 — `/fewer-permission-prompts` Skill

新 skill 掃描 session 歷史，找出「明明安全卻一直被問許可」的 bash/MCP 指令，產出 allowlist 建議。

> 如果你不用 Auto Mode，這個 skill 是最佳替代方案。

### Tip 3 — Recaps：長時間 session 的回顧摘要

Anthropic 特意在 4.7 前一週上線 Recaps。Agent 會產生短摘要告訴你「做了什麼、接下來要做什麼」。

```
* Cogitated for 6m 27s

* recap: Fixing the post-submit transcript shift bug.
  The styling-flash part is shipped as PR #29869
  (auto-merge on, posted to stamps).
  Next: I need a screen recording of the remaining
  horizontal rewrap on `cc -c` to target that separate cause.
```

> 離開幾小時後回來接手特別有用。不要的話用 `/config` 關掉。

### Tip 4 — Focus Mode：只看最終結果

CLI 新增 `/focus` 切換專注模式，**隱藏所有中間工作**，只顯示最終結果。

> Boris：「模型已經到了我大致可以信任它跑對指令、做對修改的程度。我只需要看最後結果。」

### Tip 5 — 調整 Effort 等級（最重要的設定改變）

**Opus 4.7 改用 adaptive thinking，取代固定 thinking budgets**。要控制思考量請調整 Effort：

```
Speed ←  low · medium · high · xhigh · max  → Intelligence
```

| Effort | 場景 | 說明 |
|--------|------|------|
| `low` / `medium` | 成本/延遲敏感 | 快速回應 |
| `high` | 並行多 session | 平衡智能與成本 |
| **`xhigh`** | **Boris 大部分任務預設** | 強自主性與智能、不會像 max 一樣在長 agentic run 裡跑飛 token |
| `max` | 真正困難的問題 | 邊際效益遞減；**只套用當前 session**（其他等級會延續到下次） |

> 4.7 思考更多 → token 用量比 4.6 高。Anthropic 相應調升 rate limits。

### Tip 6 — Verification：4.7 時代更關鍵

Boris：「讓 Claude 有方法驗證自己的工作，一直能讓你從 Claude 得到 **2-3 倍** 的產出。4.7 更是如此。」

**依任務類型配不同驗證手段**：

| 任務類型 | 驗證手段 |
|---------|---------|
| Backend | 讓 Claude 跑 server/service 做 end-to-end 測試 |
| Frontend | 用 [Claude Chromium 擴充](https://code.claude.com/docs/en/chrome) 控制瀏覽器 |
| Desktop apps | 用 Computer Use |

**Boris 現在的 prompt 模式**：

```
Claude do blah blah /go
```

`/go` 是一個 skill，會依序：
1. 用 bash / browser / computer use 做 **end-to-end 測試**
2. 執行 `/simplify`
3. **開 PR**

> 長時間任務的驗證更重要 —— 你回來接手時能確信 code 真的能跑。

---

## 官方「Best Practices for Opus 4.7」濃縮版

Boris 親自推的 Anthropic 官方指南，與 6 Tips 互補。

### 把 Claude 當「被委派的工程師」而非 pair programmer

1. **任務規格前置** — 意圖、約束、驗收標準、相關檔案位置，一次給齊
2. **減少 user turns** — 每一輪都有 reasoning overhead，**批次提問**
3. **用 Auto Mode** — Research preview 給 Max 使用者（Shift+Tab 切換）
4. **完成通知** — 讓 Claude 在完成時播放聲音

### Adaptive Thinking 的控制語

**固定 thinking budget 已不支援**，改用自然語言引導：

| 目的 | Prompt |
|------|--------|
| 想多思考 | "Think carefully and step-by-step before responding; this problem is harder than it looks." |
| 想快回應 | "Prioritize responding quickly rather than thinking deeply. When in doubt, respond directly." |

### 從 4.6 → 4.7 的行為差異（會影響既有 prompt）

| 行為 | 變化 | 應對 |
|------|------|------|
| **Response length** | 會依任務複雜度自動校準 | 需要明確說你要的長度 |
| **Tool calls** | 變少（改用 reasoning 代替） | 需要工具呼叫時 **明確要求** |
| **Subagents** | 變少 | 平行跨檔/跨項目工作時 **明確指定** |

### Claude Code 新增能力

| 功能 | 狀態 | 說明 |
|------|------|------|
| **Task Budgets** | Public beta | 導引長時間 run 的 token 花費 |
| **`/ultrareview` slash command** | GA | 專門的 code review session，Pro/Max 用戶 **3 次免費** |
| **Auto Mode** | 延伸到 Max | 長時間無人介入任務 |
| **預設 `xhigh`** | 所有 plan | Claude Code 預設改為 xhigh |

---

## 誠實面：Opus 4.7 的限制

雖然 Boris 大力推薦，但官方與第三方報導也揭露幾個要注意的點：

| 問題 | 說明 | 來源 |
|------|------|------|
| **Doom loops** | 約 **0.1%** 回應會出現長篇 spiraling（曾有 25,000 字回應伴隨大量大寫與髒話），比例與過往版本相當 | Sherwood News |
| **Mythos 更強但未釋出** | Anthropic 自己承認內部 Mythos 模型更強，Opus 4.7 只是「目前 GA 最強」 | Axios |
| **Token 用量上升** | 思考更多 → token 比 4.6 高，需靠 effort / task budgets / 明確指示「簡短」控制 | Boris 親述 |
| **Response length 不可預期** | 會依任務複雜度自動調整，過去固定風格的 prompt 可能需重調 | 官方 Best Practices |
| **Severity skew（CodeRabbit 觀察）** | Code review 輸出偏向 critical/major，comment density 偏高，需後處理過濾 | CodeRabbit 評測 |

---

## 研究價值與啟示

### 關鍵洞察

1. **Adaptive thinking 是典範轉移，不只是參數改名**
   - 4.6 的「thinking budget」是量化預算，4.7 的 Effort 更像 **行為模式切換**
   - `xhigh` 取代 `max` 當預設，暗示 Anthropic 自己發現 max 在 agentic run 會 **token 跑飛** —— 這是一個容易被忽略的故障模式
   - 對生產環境：**不要盲目用 max**，xhigh 才是經過 dogfood 驗證的甜蜜點

2. **Auto Mode + Classifier 是 Claude Code 的下一個分水嶺**
   - 過去要嘛 babysit（浪費人力）、要嘛 `--dangerously-skip-permissions`（有風險）
   - Classifier 模型當 gatekeeper → **讓平行多 session 真正可行**
   - 這是 Boris 57 Tips 裡「10-15 個並行 session」工作流的關鍵補完

3. **Verification 的 2-3x 定律在 4.7 被重新強調**
   - 模型能力越強，**沒驗證的產出越危險**（因為你更會相信它）
   - Boris 的 `/go` skill 把「測試 + simplify + PR」綁成一個原子動作，是個可直接抄的設計模式

4. **行為差異會讓舊 prompt 失效**
   - Tool calls 與 subagents 都變少，意味著 **依賴「Claude 自己會分派」的 prompt 會失靈**
   - 4.6 時期的 skill / prompt 要逐個重審，明確標注需要 tool use 和 parallel 的位置

5. **Boris 的 prompt 已極度精簡**
   - `Claude do blah blah /go` —— 業務描述 + 一個 skill
   - 把「如何測試、如何 simplify、如何 PR」**封裝到 skill**，任務描述只剩「做什麼」
   - 這是 57 Tips 裡「先規劃、驗證迴圈」原則的實戰終型

### 與其他筆記的關聯

| 相關筆記 | 關聯點 |
|---------|-------|
| [Claude Code Boris Cherny 57 Tips](claude-code-boris-cherny-tips.md) | 本篇是 57 Tips 的**時間續作**：57 Tips 是通用工作流，本篇是 Opus 4.7 模型專屬調整 |
| [Claude Agent SDK](claude-agent-sdk.md) | Auto Mode 的 classifier 機制可能影響 SDK 的許可判斷層 |
| [Claude Skills Guide](claude-skills-guide.md) | Boris 的 `/go`、`/simplify`、`/fewer-permission-prompts` 都是 skill |
| [Superpowers](superpowers.md) | Verification 作為 skill 的作法與 superpowers 哲學一致 |
| [Anthropic Harness Design](harness-design-long-running-apps.md) | Auto Mode + Recaps 都是長時間任務的 harness 設計 |
| [OpenAI Agent 建構指南](openai-practical-guide-building-agents.md) | 對比 Anthropic 官方指南的 agentic 設計哲學 |

### 可以直接抄的設計模式

```
新 Claude Code 工作流（基於 Boris 4.7 版本）：

1. 設定預設 Effort = xhigh（不再是 max）
2. 打開 Auto Mode（Shift+Tab 切換）
3. 跑 /fewer-permission-prompts 清一次 allowlist
4. 建一個 /go skill：e2e test → simplify → open PR
5. Prompt 模式：「Claude do <業務描述> /go」
6. 長任務離開後用 recap 接手
7. 信任模型後用 /focus 只看最終結果
```
