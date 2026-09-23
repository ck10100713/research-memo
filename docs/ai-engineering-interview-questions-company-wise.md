---
date: "2026-09-23"
category: "學習資源"
card_icon: "material-account-tie-voice"
oneliner: "Outcome School 整理的 AI 工程師面試題庫，按 35 家公司分區(Anthropic、OpenAI、Cursor、Palantir…)，每家附面試流程；約 600 題、四成附答案，但答案全連回作者自家部落格，題目也沒標出處"
tags:
  - learning
  - system-design
  - llm
---

# AI Engineering Interview Questions Company Wise 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/pallavi-shekhar/ai-engineering-interview-questions-company-wise> |
| 維護者 | Pallavi Shekhar / [Outcome School](https://outcomeschool.com)(付費 AI/ML 課程機構) |
| 姊妹 repo(按主題分) | <https://github.com/amitshekhariitbhu/ai-engineering-interview-questions>(3,163 stars) |
| 分析 commit | `14c0106` |

> Metadata(2026-09-23 抓取):**626 stars / 43 forks** · Apache-2.0 · 建立於 **2026-09-19**，只有 8 個 commit，全部在同一天。整個 repo 就一份 2,047 行的 `README.md` 加一張 banner。

## 專案概述

一份 README 形式的面試題庫，鎖定 AI Engineer、LLM Engineer、Forward Deployed Engineer、Inference Engineer 這類職缺。和一般「按主題分」的題庫不同，它**按公司分**，一家一段，每段固定三塊：

1. **Roles this covers**：這家公司這批題目對應哪些職稱。
2. **Interview loop, as publicly reported**：面試流程幾關、每關考什麼、大概多久。
3. **題目**：按 10~12 個主題分組(LLM 內部、推論與 GPU、RAG、Agent、微調、評估、安全、多模態、系統設計、Coding、行為面試、FDE 情境題)。

跨公司重複出現的題目抽到最前面的「Common Questions」，每題標出哪些公司問過，公司段落就不再重複。這個去重設計讓整份文件好讀很多。

## 規模與答案覆蓋率

| 區塊 | 題數 | 附答案 | 覆蓋率 |
|------|------|--------|--------|
| Common Questions(10 個主題) | 119 | 81 | 68% |
| 各公司專屬題 | 479 | 151 | 32% |
| **合計** | **598** | **232** | **39%** |

題數最多的幾家：Anthropic 37、OpenAI 31、Meta 26、Amazon 23、Google 22、Palantir 20、Cursor 17。Waymo、Figure AI 各 12 題，一題答案都沒有。

**答案全部連回作者自家內容**：outcomeschool.com 部落格、Outcome School YouTube、作者 LinkedIn 貼文。沒有任何連到論文、官方文件或第三方文章的答案。所以這份 repo 實質上也是 Outcome School 的導流入口，答案品質要去看他們的部落格才知道。

## 公司分區怎麼涵蓋

| 分組 | 公司 |
|------|------|
| Frontier AI Labs | Anthropic、OpenAI、Google DeepMind、Meta、xAI、Mistral、Cohere、DeepSeek、Moonshot(Kimi)、Zhipu(GLM)、Alibaba(Qwen)、Sarvam AI |
| Big Tech | Microsoft、Amazon、Apple、NVIDIA、Tesla、Uber/Netflix/LinkedIn/Airbnb/Pinterest/Spotify 合併一段 |
| AI Infra / 平台 | Databricks、Groq、Together AI、Hugging Face、Scale AI、Perplexity |
| AI-native 產品 | Cursor、Cognition、Sierra、Harvey、Glean、Character.AI、ElevenLabs、Abridge、Figure AI、Waymo |
| Forward-Deployed | Palantir |

## 值得一看的內容

### 1. 面試流程描述比題目本身更有用

每家公司的流程摘要很具體，看得出各家在測什麼：

- **Anthropic**：recruiter screen 本身就會刷人 → CodeSignal 式 70~90 分鐘、一題分四層遞進 → 約五關 onsite(專案深挖、coding、系統設計、價值觀)。有些 MLE 流程加了「給你 Claude，看你怎麼指揮和驗證它」的 AI 協作關。
- **Cursor**：直接在 Cursor 真實 codebase 上寫資料結構，最後是兩天到場(或 8 小時遠端)在真 code 上做一個功能，明確評分 scoping、自主性和 AI 工具使用。
- **Meta**：2026 年部分流程加了三段式 AI 輔助 coding 關(找 bug 修掉 → 加功能 → 擴充系統)。
- **Palantir**：招牌是 decomposition 關，把「貨運鐵路每年因機車故障損失數千萬」這種模糊問題拆成工程計畫。
- **Hugging Face**：你的公開 GitHub 紀錄真的會被當成評估的一部分。

共通趨勢很明顯：**「AI 協作能力」正在變成獨立的面試關卡**，而且越來越多公司用「需求逐步加碼」的實作題取代 LeetCode。

### 2. Anthropic 的 coding 題偏「長出來的需求」

幾題代表性的：

- 做一個 in-memory database：先 SET/GET/DELETE，再加 filtered scan，再加 TTL，最後做 file compaction。
- 寫 rate limiter，每十分鐘加一個需求(per-tenant、burst、sliding window)，問你怎麼不讓 code 崩掉。
- 對 5 萬份文件跑 LLM call，API 限 ~100 併發、偶爾 429 和 timeout，用 Python 寫出來。

這類題考的是**程式在需求變動下的可維護性**和併發處理，和 LLM 知識關係不大。

### 3. 系統設計題很貼近各公司產品

- Cursor：設計 tab 補全(感知延遲 < 100 ms)、100k 檔 monorepo 的索引怎麼保持新鮮、模型在串流多檔編輯時使用者還在打字怎麼辦。
- Anthropic：「對 Claude Code 這種 coding agent，模型和 harness 哪個比較重要？設計這個 loop」。
- Palantir：為什麼 agent 要架在 ontology 上而不是直接讀資料表和文件。

就算不是要去面試，這些題目拿來當「這家公司的核心工程難題」的索引也很好用。

## 要注意的地方

!!! warning "題目來源無法驗證"
    README 只說題目「compiled from publicly reported interview experiences」，但**沒有任何一題附出處**(沒有 Glassdoor、Blind、Reddit 或部落格連結)。流程細節像「recruiter screen ~30 分鐘」「2 天 onsite」也一樣沒來源。有些題目很像編者自己依公司產品改寫的情境題，例如 Anthropic 那題「企業客戶說 Claude 幻覺太多，你前 48 小時做什麼」。當成「這家公司可能在意什麼」的地圖比較合適，別當成真實考古題。

- **非常新**：2026-09-19 才建立，四天內衝到 626 星，內容還沒經過社群校正，也沒有 issue 或 PR 討論。
- **答案覆蓋不均**：通用題有七成附答案，公司專屬題只有三成，而最有特色的往往是那些沒答案的公司專屬題。
- **答案來源單一**：全部導回 Outcome School，沒有交叉比對的機會。

## 怎麼用

1. 先刷 Common Questions 的 119 題，這部分答案最完整，也是跨公司最常考的基礎(attention、KV cache、RAG、agent loop、eval)。
2. 挑目標公司讀流程摘要，決定要準備哪幾種關卡。
3. 公司專屬題當成自我檢查清單，答案自己去找一手資料(論文、官方工程部落格)補。

## 相關筆記

| 筆記 | 關係 |
|------|------|
| [System Design Primer](system-design-primer.md) | 傳統分散式系統設計面試的基礎，這份題庫的「AI System Design」題也常需要這層功底 |
| [AI Engineering from Scratch](ai-engineering-from-scratch.md) | 題庫裡 LLM 內部、推論優化這類題目的系統性學習路徑 |
| [AI Job Search](ai-job-search.md) / [Career-Ops](career-ops.md) | 求職流程的另一端：找職缺、客製履歷、面試演練 |
