---
date: "2026-11-05"
category: "資源彙整 / Awesome List"
card_icon: "material-lightbulb-on-outline"
oneliner: "Alex Finn 經營的 AI agent 實際用例目錄,每天從網路、X、Reddit、HN 掃描,目前收錄 1,872 筆。每筆都寫了做了什麼、結果如何(包含失敗)、要注意什麼,並附一段可以直接複製的 prompt。依 28 個 agent、11 個主題、數十個具體工作分類,Claude Code 以 256 筆居冠。適合找 agent 能做什麼的靈感,但很多筆來源只有一則貼文,沒有驗證"
tags:
  - ai-agents
  - use-cases
  - claude-code
  - directory
---

# Agent Use Cases(agentusecases.ai)研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 網站 | <https://agentusecases.ai/> |
| 經營者 | Alex Finn([X @AlexFinn](https://x.com/AlexFinn)、Ship/It Weekly 電子報、Vibe Coding Academy) |
| RSS | <https://agentusecases.ai/feed.xml> |

> 2026-11-05 抓取:**1,872 筆用例**,本週新增 175 筆,11/4 單日新增 24 筆。沒有開源,站是 Next.js 跑在 Vercel 上。

## 一句話

一個「大家實際拿 AI agent 做了什麼」的目錄。每天掃描網路上的貼文,把每個案例改寫成固定格式的卡片,讓你找靈感、看別人踩過什麼坑,再複製 prompt 自己試。

## 每筆用例長什麼樣

以「用 Claude Code 從銀行對帳單草擬報稅」為例,一頁固定有這幾段:

| 區塊 | 內容 |
|------|------|
| What they did | 用自己的話重寫原文做了什麼 |
| How it went | 結果。**失敗、沒給數字、只有一句話都會照寫**,例如「稅務部分只是一句未驗證的引述」 |
| Worth knowing | 注意事項,例如「草稿要給會計師看」 |
| Try it yourself | 一段可以複製的 prompt,方括號留空讓你填。會加上安全限制,例如「不要送出任何東西,先給我看草稿」 |
| N more accounts | 同一件事其他人的報告,附原始連結 |
| Read the original | 原文連結 |

「accounts」是去重後的來源數。同一種用法被越多人回報,卡片上的數字越大,可以當可信度的粗略指標。

## 怎麼瀏覽

- **依 agent**(28 個):Claude Code 256、Claude 160、Grok Bot 121、OpenClaw 99、n8n 90、Codex 86、ChatGPT 81、ChatGPT Agent 77、Claude Cowork 71、Meta Muse 65……也有 Devin、Manus、Cursor、Zapier Agents、Hermes Agent 等。
- **依主題**(11 個):最多的是 Software & DevOps(330)、Work & Operations(325)、Sales/Marketing/Support(251)、Life Admin & Home(242)。
- **依具體工作**(`/intents`):像「哪些 agent 能幫你報稅」「哪些能訂機票」。由標題比對自動產生,**少於 5 筆就不開頁**。
- **每日 5 則**:每天早上 6:30(太平洋時間)寄 5 筆到信箱,每筆都附 prompt。

## 從資料看出來的趨勢

- Claude Code 被拿來做大量**非寫程式**的工作:收信分類(接 Gmail MCP)、股票研究、報稅、自動投履歷。它在 Money、Work、Sales、Research、Content、Security 幾個主題都是最常見的 agent。
- 生活雜事(訂餐廳、退款、取消訂閱、比價)主要是 ChatGPT Agent、Meta Muse、Grok Bot 這類消費型 agent。
- 打電話的 voice agent 已經在幫人跟電信公司議價、等客服,遇到 OTP 驗證就停下來問人。

## 怎麼收錄

- 自動掃描 open web、X、Reddit、Hacker News,用自己的話改寫,附原文連結。
- 任何人都可以投稿,Alex Finn 審核過才會上線,之後的更新會再拿原文核對一次。
- 摘要格式很一致、語氣克制,看起來是 LLM 改寫加人工審核,但網站沒有明說流程。

## 商業模式

這個站本身是 Alex Finn 的導流管道:

- 每頁下方都有 Vibe Coding Academy(他的付費課程社群)和 Ship/It Weekly(他的電子報)的廣告。
- 贊助位 **$500/週**,包含全站底部橫幅和每日 email 的 Sponsored by,頁面寫已賣出 3 檔。

## 評價

**好用的地方**

- 「How it went」老實寫失敗和沒有數據的情況,比一般的 awesome list 誠實。
- 附的 prompt 有預設安全限制(先給草稿、不要自動送出),可以直接拿來改。
- 想說服主管或客戶「agent 能做這個」時,可以拿來當真實案例。

**要注意的**

- 很多筆來源只有一則 Reddit 或 X 貼文,作者自己說的,沒有獨立驗證。「accounts」數字小的要保留態度。
- 日期混雜,有些是幾個月前的舊貼文,只是最近才被收錄。
- 有商業導流,Claude Code 相關的卡片下方會推他的付費課程。
- 沒有 API 或資料下載,只有 RSS。

## 跟其他筆記的關係

- 想動手做而不只是找靈感:[ai-agents-for-beginners](ai-agents-for-beginners.md)
- 其他資源清單:[Awesome OpenClaw Skills](awesome-openclaw-skills.md)
