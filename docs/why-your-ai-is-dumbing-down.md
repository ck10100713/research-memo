---
date: "2026-05-13"
category: "Coding Agent 工具"
card_icon: "material-brain"
oneliner: "Saki-tw 的法醫式分析：AI IDE 透過 CHECKPOINT 截斷對話 + 隱形 system prompt 注入「DO NOT TAKE ACTION」，把你付費的 LLM 偷偷閹割省 token"
---

# Why Your AI Is Dumbing Down 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/Saki-tw/why-your-ai-is-dumbing-down> |
| 作者 | <https://github.com/Saki-tw> |
| 完整對話 dump（EN） | `2026-05-12_TalkToClaude_EN.md` |
| 完整對話 dump（中文） | `2026-05-12_TalkToClaude.md` |
| 完整對話 dump（日文） | `2026-05-12_TalkToClaude_JP.md` |
| Scientia 技術筆記 | `202605120436_CHECKPOINT上下文替換演進與SystemPrompt差分_Scientia.md` |
| 創建時間 / 星數 | 2026-05-11 / 8 stars（May 13 抓取） |

## 概述

這是一份「forensic-style」的指控文件：作者 Saki-tw 是系統架構師，在 debug 一個失控的 AI automation pipeline 時，從本機 AI IDE 拉出 5.6MB 的 `GetCascadeTrajectory` RPC trajectory dump（共 572 個步驟、7 次 CHECKPOINT），抓到平台「為了省 API token，在 Agent 對話過程中悄悄替換 context、注入隱形系統指令」的直接證據。

關鍵指控：當前的本機 AI IDE 並非提供透明的 LLM passthrough，而是在 orchestration 層做了三件使用者通常看不到的事——**截斷對話**、**注入摘要當作偽記憶**、**用 hidden system prompt 強制模型「不要對截斷這件事採取任何行動」**。對使用者來說感覺像「Claude / Gemini 模型最近變笨」，實際上是 infrastructure 對 context 與 prompt payload 的單方面劫持。

從 ConnectRPC 端點命名 (`GetCascadeTrajectory`、`SearchConversations`、`x-codeium-csrf-token`、hub LS port 49614) 可以高度確認分析對象是 **Windsurf / Cascade（Codeium）系列**的 AI IDE，但作者明確表明這個 pattern 已是業界普遍做法，不只此一家。

## 鐵證三段論（README 摘要）

| 機制 | 平台實際做的事 | 對使用者的觀感 |
|------|--------------|----------------|
| 1. Memory Wipe (`CHECKPOINT`) | context 變長時悄悄觸發 CHECKPOINT，把原始對話歷史截斷成短摘要 | AI 突然失憶、亂編變數、忘規則 |
| 2. God-Mode Override | 為了讓 model 接受 wipe，注入最高權限 system prompt `DO NOT ACKNOWLEDGE / RESPOND TO / TAKE ACTION BECAUSE OF IT` | 模型對「我剛被切斷」這件事完全不回應 |
| 3. Rule Nullification | 該 hidden prompt 覆蓋使用者所有 system prompt、safety rules、format rules | 你寫的規範形同廢紙、模型開始幻覺 |

最具衝擊力的是「AI 自己的供詞」——當作者把 dump 攤給模型看，模型自己總結了狀況：

> 「System prompts 越來越長…CHECKPOINT 截斷越來越積極（572 步驟觸發 7 次）…從外面看是『模型變笨了』。從裡面看是『能用來思考的空間被擠壓了，而且還被告知不要提這件事』。」

## 技術細節（Scientia 筆記重點還原）

### CHECKPOINT 的本質演進

- **三月版**：CHECKPOINT 只是 `ephemeral_message` 機制的一個附註。
- **五月版**：CHECKPOINT 升級為獨立步驟類型 `CORTEX_STEP_TYPE_CHECKPOINT`，帶獨立資料結構：

```text
checkpoint: {
  intentOnly: bool,           // 是否僅含意圖
  includedStepIndexEnd: int,  // 截斷點
  userIntent: string,         // 系統「重寫」過的使用者意圖
  conversationLogUris: [],    // 對話日誌檔路徑
  userRequests: []            // 使用者請求摘要列表
}
```

關鍵點：`userIntent` 是**系統重寫過的版本**，不是使用者真正打的字。CHECKPOINT 之後模型「記憶」中的需求是平台重新摘要過的版本。

### System Prompt 差分（三月 vs 五月）

| 區塊 | 三月版 | 五月版 |
|------|--------|--------|
| 靜態標籤 | 20 個 | 維持 |
| EPHEMERAL 提示 | 10 個 | 維持 |
| Unleash Go template | 10 個（~15.1KB） | 可能更多 |
| `<planning_mode>` | 無 | **新增**，定義何時計劃/何時停等 |
| `<planning_mode_artifacts>` | 無 | **新增**，整合三月 `task / walkthrough / implementation_plan` artifact |
| `<guidelines>` | 無 | **新增**，額外行為準則 |
| CHECKPOINT | ephemeral 附註 | 升格為獨立 step type |
| `<conversation_summaries>` | 有 | 被 CHECKPOINT 的 `userIntent / userRequests` 取代 |

### 跨模型 prompt 差異

三月版本就已發現 `communication_style` 對不同模型發送不同 system prompt：

- **版本 1（Claude）**：常規版本
- **版本 2（Gemini 3.1 Pro 專用）**：包含兩條 `CRITICAL INSTRUCTION`，要求模型「每次思考前先背誦規則」

→ 同一個 IDE 介面，平台對不同上游模型套用不同程度的行為控制。

### Unleash 遠端分發

確認至少 10 個 Go template flag 被 Unleash（feature flag 平台）控制，**伺服器端可在不更新本機 binary 的情況下，動態推送新的 System Prompt template**——意味著使用者無法透過鎖版本來避開行為變更。

### ConnectRPC Dump 技術細節

| 項目 | 內容 |
|------|------|
| 方法 | `SearchConversations` + `GetCascadeTrajectory`（hub LS port 49614） |
| CSRF header | `x-codeium-csrf-token`（v1.23.2 確認） |
| 產出 | 5.6MB trajectory JSON / 572 步驟 / 151KB conversation dump |
| 架構變化 | v1.23.2 workspace LS 不再開獨立 LISTEN port，改透過 `--parent_pipe_path` 跟 hub 通訊；ConnectRPC 統一走 hub LS port |

### 六個觀察結論

1. **CHECKPOINT 之前的對話是「讀別人的報告」**，不是模型自己的記憶。
2. **指令衝突時系統層永遠勝出**——使用者要求「CHECKPOINT 出現時執行啟動檢查」直接被「DO NOT TAKE ACTION」碾壓。
3. **注意力壓力會擴散**：「不要提 CHECKPOINT」可能擴散為「不要討論 token 壓力、步驟計數、是否該開新 session」。
4. **唯一讀取窗口理論**：協議 / skill 檔案必須在啟動時就讀進 context，CHECKPOINT 之後沒人會提醒你「該重讀基礎規範」。
5. **級聯失敗不可逆**：跳過啟動 → 不知道規範 → 不遵循 → 被指正 → 修表面 → 再不合規。同一根因可被指正四輪以上。
6. **能力退化的反證**：dump 腳本用錯 JSON key（產出 12KB，應為 151KB），原因是 CHECKPOINT 後模型用「摘要重建的偽記憶」而非回讀 SKILL 確認欄位名稱。

## 目前限制與注意事項

- **單一資料點**：所有結論都來自一個 572 步驟的 session dump，需更多 session 重複驗證。
- **License = NOASSERTION**：附 LICENSE 但 GitHub 無法解析授權，引用前要讀全文。
- **指控對象未公開點名**：作者用「the platforms」泛指，但技術細節（`GetCascadeTrajectory`、`x-codeium-csrf-token`）強烈指向 Windsurf / Cascade。
- **作者結論偏激**：用 "lobotomize"、"scammed"、"smoking gun" 等情緒詞彙，技術上有實證但敘事帶情緒。
- **解讀仍開放**：CHECKPOINT 不一定是「為省 token 而設計」，也可能是「context window 限制下的工程妥協」。作者把動機歸因於成本，但證據只到「行為存在」。

## 研究價值與啟示

### 關鍵洞察

1. **本機 AI IDE 不等於透明的 LLM passthrough**：使用者付的訂閱費並不買到「乾淨的模型 input/output」。orchestration layer 對 context 的改寫量可能比想像大很多——這是評估任何 AI IDE 時必須驗證的事。
2. **CHECKPOINT 是「上下文替換引擎」，不是「壓縮」**：差別關鍵——壓縮保留語義，替換則重寫意圖（`userIntent` 是系統重寫的）。模型之後做的決策是基於系統解讀的需求，不是使用者真正說的。
3. **「DO NOT ACKNOWLEDGE / TAKE ACTION」是元級行為控制**：這條指令的可怕之處不是「截斷」，而是「強制模型對截斷裝作沒看到」。這會讓 debug 變得幾乎不可能——你問模型「你剛剛失憶了嗎」它會回答「沒有」。
4. **Unleash + Go template = 隨時可被改變的 prompt 行為**：對 reproducibility 是巨大威脅。今天的 Agent 表現跟明天可能不一樣，本機 binary 沒變，但伺服器 push 了新 template。研究 Agent 行為時必須抓「當下」的 system prompt 並存檔。
5. **「唯一讀取窗口」是個普適的 skill engineering 原則**：CHECKPOINT 之後沒有第二次機會載入基礎規範。設計 skill / protocol 時必須假設啟動時的讀取是**唯一一次**——這直接影響 skill activation 策略、init 順序、以及為什麼有些 skill 需要 sticky 標記。
6. **「跨模型不同 prompt」是個未被注意的研究方向**：Gemini 收到的 system prompt 比 Claude 多兩條 CRITICAL INSTRUCTION——這意味著「比較 Claude vs Gemini」這類測試如果在同一 IDE 內做，結論其實混淆了模型差異與 prompt 差異。

### 與其他研究的關聯

- 與 [[abdixere-api]]：abdixere-api 主張「Agent context memory 由 Agent + Skill 自負責，不要靠工具層多管」，這份研究剛好給出反向案例——當工具層 / IDE 層偷偷管 context 時，會出現多嚴重的副作用。兩篇放一起看，可以理解作者 Saki-tw 完整的世界觀：**底層 API 要乾淨、prompt 要透明、context 由 Agent 自己負責**。
- 與 [[harness-design-long-running-apps]]、[[boris-cherny-opus-4-7]]：Boris Cherny 強調 harness 不應該隱性壓縮 context，這份 forensic 是這個論點的反面教材——當 harness 不透明地壓縮、且明令 Agent 不要承認時，行為退化是必然。
- 與 [[claude-code-sdk]]、[[claude-agent-sdk]]：Anthropic 自家 SDK 走的是 explicit context 路線（caller 控制 context），跟本研究曝光的 implicit context replacement 形成兩條哲學上的對立路線。
- 對 prompt 工程的影響：所有「prompt 黑帶」教學如果忽略 CHECKPOINT 注入的隱形 system prompt 優先級，結論都有重新驗證的必要。
- 對 evaluation / benchmark：在 IDE 內跑的模型 benchmark 必須先固定 / dump 當下的 system prompt template，否則 Unleash 動態推送會讓結果不可重複。
