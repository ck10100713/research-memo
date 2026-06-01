---
date: "2026-05-15"
category: "學習資源"
card_icon: "material-clipboard-list"
oneliner: "zeuikli 整理 29 篇 best-practices + 52 篇 Claude blog 的 Claude Code 九面向最佳實踐總報告，含 CLAUDE.md、Hook、Cache、Subagent、Skill、MCP、安全、Routines、成本工程"
tags:
  - claude-code
  - learning
---

# Claude Code 最佳實踐完整研究報告（zeuikli）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原始報告 | <https://github.com/zeuikli/claude-code-workspace/blob/main/docs/2026-05-16-claude-code-best-practices.md> |
| 所屬 repo | <https://github.com/zeuikli/claude-code-workspace>（Shell-based workspace, 16 stars） |
| 報告日期 | 2026-05-16 |
| 上游素材 | `research/best-practices/` 29 篇 + `research/claude-blog/` 52 篇 |
| 報告字數 | ≥ 10,000 中文字（36 KB） |
| 重要引用人物 | Boris Cherny、Thariq Shihipar（Claude Code 核心團隊） |

## 概述

這是 GitHub 使用者 **zeuikli** 在自己的 `claude-code-workspace` repo 裡，把 29 篇 best-practices 文獻與 52 篇 Anthropic claude-blog 文章**整併成單一 10,000 字長文**的研究報告，覆蓋 Claude Code 從 CLAUDE.md 到成本工程共 9 個面向。屬於高密度二手知識整理，**對「想一次補完所有 Claude Code 工程實踐」的開發者來說，是 2026-05 截至目前最完整的單篇繁體中文整理**。

整篇核心論點：

> **Context Engineering（在執行時組裝正確資訊並正確排序）是 Claude Code 真正的工程護城河，遠比 Prompt 撰寫技巧更重要。**

---

## 九大章節骨架

```text
1. CLAUDE.md 與記憶系統      → 規則寫多少、用 Path-Scoped Rules 拆分、三層 Context 架構
2. Hooks 自動化              → PreToolUse 防守、PostToolUse 自動化、Conditional / async / effort 感知
3. Prompt Caching            → Cache Rate 當 SLA、分層快取、五個禁止操作、<system-reminder> 注入動態
4. Subagent 委派             → 5 條委派觸發條件、fan-out 上限 4、模型分層（Haiku / Sonnet / Opus）
5. Skill 知識封裝            → Description 給模型看、Progressive Disclosure、自由度反比於風險
6. MCP 整合                  → 3 種 Transport、Scope 優先序、Tool Search defer_loading 省 85% schema
7. 安全部署                  → Permission deny → ask → allow、Sandbox、Proxy 隔離 API key
8. Routines 排程             → 三種觸發（Schedule / API / GitHub Event）、Boris Cherny `/loop` 案例
9. 成本工程                  → 三層成本防線、Effort Level 選擇、CJK 不要用 LLMLingua（衰退 25%）
```

---

## 各章節最高密度的洞見摘要

### 第 1 章 — CLAUDE.md 黃金法則

| 規則 | 數據 |
|------|------|
| 長度 ≤ 200 行（最佳 60 行） | > 200 行後遵從率從 76% → 52% |
| 每行通過測試：「移除後 Claude 會犯錯嗎？」 | 否就刪 |
| 大型 codebase 用 **Path-Scoped Rules**（`.claude/rules/<glob>.md` + frontmatter `paths:`） | 只在符合 glob 的檔案被讀時載入，避免污染 context |

### 第 2 章 — Hooks 三層

| Hook 種類 | 用途 | 範例 |
|----------|------|------|
| `PreToolUse` | 阻擋危險操作（`exit 2`） | 攔截 `git push --force`、`rm -rf` |
| `PostToolUse` | 自動補品質（formatter / linter） | Edit/Write 後自動 prettier / black / gofmt |
| `SessionStart` | 環境初始化 | git pull、注入 branch / 最近 commit |

進階：`if` conditional（v2.1.83+）、`async: true`（Slack 通知不卡 Claude）、Hook 可讀 `effort.level` 動態調整。

### 第 3 章 — Cache 是 SLA

Thariq Shihipar 原話：

> 「Cache rules everything. We treat it like uptime. When it drops, we have an incident.」

**五個會炸快取的操作**：

1. 動態修改 system prompt（時間戳） → 改用 `<system-reminder>` 在 messages 注入
2. Mid-session 切換模型 → 用 Subagent 換 model
3. 對話中增刪工具 → 用 stub + `defer_loading: true`
4. Compact 改 system prompt → 重建 session 時 prompt 必須 byte-identical
5. 不一致的工具清單 → 每次工具定義 hash 必須相同

**Compact 決策樹**：context 相關 → continue；走錯 → `/rewind`；中段膨脹 → `/compact <hint>`；新任務 → `/clear`；大量中間輸出 → Subagent。

### 第 4 章 — Subagent 五條委派觸發

| 條件（任一成立即委派） |
|----------------------|
| 讀取 ≥ 10 個檔案 |
| 預期工具呼叫 > 20 次 |
| 可拆 ≥ 3 個獨立子任務 |
| 任務類型 ∈ {研究、安全審查、架構決策} |
| 側邊任務會淹沒主線 |

**反直覺數據（AgentOpt 實測）**：強模型當 Planner 31.71% vs 懂得委派的弱規劃者 74.27%——**「會委派的弱規劃者 > 什麼都自己做的強規劃者」**。

模型分層：Haiku（researcher）/ Sonnet（implementer + orchestrator）/ Opus（reviewer + architect）。

### 第 5 章 — Skill 撰寫

`description` 四要素：做什麼 + 何時用 + **何時不用（Do NOT use for ...）** + 主動觸發提示（`Make sure to use this skill whenever ...`，因為模型傾向 undertrigger）。

**反直覺**：自由度應該**反比於風險**。

| 操作 | 自由度 |
|------|--------|
| Code review、分析 | 高（文字指引） |
| Deploy、CI | 中（pseudocode + 參數化） |
| DB 遷移、破壞性 | 低（精確腳本，禁止修改） |

**保留門檻**：30 天評估，品質提升 ≥ 1.5 分（10 制）+ 時間節省 ≥ 30%，兩者同時才保留；0 觸發次數直接停用。

**Skill 上限**：API 同時載入 ≤ 8 個，超過 recall accuracy 顯著下降。

### 第 6 章 — MCP 職責分離

```
MCP Server  → 連接（工具、外部 API、資料庫）
Skills      → 邏輯（領域知識、工作流）
Subagents   → 任務委派（隔離 context）
Hooks       → 自動化（確定性流程）
```

Scope：Local > Project > User，同名 server 只連一次。

`defer_loading: true` 實測**降 85% tool schema token**（Anthropic 2026-05 數據）。

MCP 輸出上限：`MAX_MCP_OUTPUT_TOKENS` 預設 25,000，單工具最大 500,000 字元（`_meta["anthropic/maxResultSizeChars"]`）。

### 第 7 章 — Permission Wildcard 坑

- `Bash(npm run *)` 匹配 `npm run test` 但**不匹配** `npm run-linter`（無 word boundary）
- `Bash(curl *)` 容易被 redirect/protocol 繞過 → 改 deny + 用 `WebFetch(domain:...)` allowlist
- 自動剝離：`timeout / time / nice` 會被剝離；`docker exec / npx` **不會剝離**

**Proxy Pattern**：Agent 永遠看不到實際 API Key（`ANTHROPIC_BASE_URL` 指向 proxy，proxy 注入 key + allowlist + 稽核）。

Docker 生產設定的安全選項：`--cap-drop ALL --security-opt no-new-privileges --read-only --network none --pids-limit 100`。

### 第 8 章 — Boris Cherny 的 `/loop` 自動化

```bash
/loop 5m /babysit         # PR 自動 shepherd：監控 + 回應 reviewer
/loop 30m /slack-feedback # Slack → 自動建 PR
/loop /post-merge-sweeper # 處理 merge 後遺留留言
/loop 1h /pr-pruner       # 關超過 30 天 stale PR
```

Routine 配額：Pro 5 / Max 15 / Team 25 / Enterprise 依約。

### 第 9 章 — CJK 特殊警告

> **禁止使用 token-pruning 類壓縮工具（如 LLMLingua）處理繁體中文/日文/韓文內容。實測繁中內容衰退 25% 以上。**

CJK 安全替代：（a）官方 Prompt Caching 零品質風險；（b）caveman rules 輸出規則約束實測英文 -80.6%、繁中 -86.2% token 而 LLM Judge 品質無衰退。

**量化案例**：Anthropic Engineering 每日合併 PR +67%；Anthropic Legal 合規審閱 2-3 天 → 24 小時；eSentire 威脅分析 5 小時 → 7 分鐘（95% 準確率）；Skyline 70 萬行 C# 一年專案 → 兩週。

### 第 10 章 — PGE 原則

> **產生程式碼的模型不應是評估程式碼的模型。**

完成驗證必須執行外部腳本並貼真實輸出，**禁止口頭聲稱「測試通過」**。Boris Cherny 心法：

> 「宣告完成前自問：資深工程師會核准這個嗎？否 → 先修再報。」

---

## 附錄精華（Prompt 模板）

報告附錄 A 提供五個可直接套用的範本：

1. **專案 CLAUDE.md 範本**（60 行內）
2. **複雜任務 System Prompt 範本**（XML 結構 + 「verify before claiming done」段）
3. **Subagent 委派範本**（三角色 fan-out 範本）
4. **Routine Prompt 範本**（含目標 / 步驟 / 成功定義 / 異常處理四段）
5. **Prompt Caching Python 範例**（system 完全靜態 + `<system-reminder>` 注入動態 + cache hit rate 監控）

附錄 B 三張快速決策表：
- CLAUDE.md vs Auto Memory vs Skill 分工
- 何時委派 Subagent
- Context 0–40%、40–70%、70–85%、85–95%、95%+ 五段決策

---

## 目前限制與注意事項

- **這是「整理」報告，不是一手原始來源**：所有結論的可信度取決於 zeuikli 對 29 + 52 篇上游素材的篩選與詮釋；引用前建議交叉比對 [[boris-cherny-opus-4-7]] 等一手研究。
- **數據的時效性**：CLAUDE.md > 200 行遵從率 76% → 52%、AgentOpt 31.71% vs 74.27%、`defer_loading` -85% schema token 等，原報告未給出研究來源連結，需另行查核。
- **repo 無 LICENSE**：使用 / 翻譯前要主動詢問 zeuikli 授權方式。
- **報告偏 Anthropic 官方視角**：上游 52 篇 claude-blog 是 Anthropic 自家內容，對於替代生態系（Codex、Gemini CLI、Cursor）的對等做法未涵蓋。
- **`/loop`、`/babysit`、`/grill`、`/post-merge-sweeper` 都是 Boris Cherny 個人或團隊內 routine 命名**，並非 Claude Code 標準功能——你的環境裡需要自己造對應 skill / routine。

---

## 研究價值與啟示

### 關鍵洞察

1. **這份報告本身就是「Context Engineering」的具體展示**：把 81 篇文獻收成單一 10K 字長文，正是它主張的「在執行時組裝正確資訊並正確排序」的元級實踐。讀者拿這份當 CLAUDE.md 預讀或讓 SubAgent 摘要產子報告，會直接受益。
2. **CLAUDE.md 黃金 60 行**：跟業界常見「寫得越詳細越好」的直覺相反。**移除後不會犯錯的條目就該刪**——這個測試適用於所有 prompt-as-policy 場景，是極可遷移的設計原則。
3. **Cache Hit Rate 應該被當 SLA 監控**：把基礎設施 mindset 帶進 LLM 工程，意味著有些團隊已經跳出「prompt 是黑魔法」階段，把 Claude Code 當作可量化、可監控的 production system 在跑。
4. **「會委派的弱規劃者 > 什麼都自己做的強規劃者」**：AgentOpt 31.71 vs 74.27 的數據顛覆「主執行緒越強越好」的直覺。對應到 [[casper-claude-skill-design-gallery]] 的「主執行緒寫 Skill、SubAgent 用 Skill」是同一條主軸的兩種落地。
5. **CJK 不要用 LLMLingua**：少見的非英文場景 specific 警告。對台灣 / 日本團隊有重要實務價值，比英文社群轉述的「壓縮就對了」更可靠。
6. **PGE 原則（Generator ≠ Evaluator）是被低估的工程紀律**：很多人讓 Claude 同時寫 code + 自評，就是反 PGE。把驗證腳本獨立成 bash / pytest 並要求貼輸出，是預防「Claude 自己說通過」幻覺最有效的單一機制。
7. **報告是「以 Anthropic 為中心的世界觀」**：第 6 章把 MCP 講得很細、第 8 章排程也只覆蓋 Anthropic Routines。對需要跨生態系（Codex / Cursor / Gemini）的讀者，這份是好起點但不是終點。

### 與其他研究的關聯

- 與 [[boris-cherny-opus-4-7]]、[[claude-code-boris-cherny-tips]]：本報告大量引用 Boris Cherny，可當作那些研究的整合層 / 延伸閱讀。
- 與 [[casper-claude-skill-design-gallery]]：「主執行緒寫 Skill、SubAgent 用 Skill」的方法論在本報告第 4 + 5 章被理論化（fan-out 上限 4、Skill description 寫法），Casper 的作品集則是實作層。**兩篇合讀正好補完「為什麼這樣做 × 怎麼做」**。
- 與 [[claude-skills-guide]]、[[andrej-karpathy-skills]]、[[asgard-skills]]：本研究第 5 章是這些 Skill 觀念整理的「實戰版」，特別是「Description 給模型看」、「自由度反比於風險」兩條值得回頭補進那些研究。
- 與 [[harness-design-long-running-apps]]：本報告第 3 章對 Prompt Caching 與 `<system-reminder>` 的論述，跟 harness 設計的「不要動態改 system prompt」原則完全對齊。
- 與 [[why-your-ai-is-dumbing-down]]：那篇揭示 IDE 平台**主動**截斷 context（CHECKPOINT），本報告主張開發者**主動**做 Context Engineering，兩者剛好是「被動劫持」vs「主動掌控」的兩面，合讀可看清 Agent context 議題的整個光譜。
- 與 [[learn-claude-code]]、[[claude-code-from-source]]、[[mcp-for-beginners]]：對學習者來說，這份報告是 Anthropic 官方教材外**最完整的繁體中文補充**，可放在學習路徑的「進階對齊」階段。
