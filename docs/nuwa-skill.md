---
date: "2026-04-17"
category: "Coding Agent 工具"
card_icon: "material-head-lightbulb"
oneliner: "蒸餾任何人的思維方式 — 6 路並行調研 → 三重驗證 → 心智模型 + 決策啟發式 + 表達 DNA，11.8K stars"
---

# 女娲.skill（nuwa-skill）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) |
| 靈感來源 | [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)（蒸餾同事） |
| 配套進化工具 | [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) |
| LINUX DO 討論 | [用女娲.skill 蒸馏了八个大人物](https://linux.do/t/topic/1922796) |

**作者：** 花叔 Huashu — AI Native Coder，獨立開發者（代表作：小猫補光燈，AppStore 付費榜 Top1）

**專案狀態：** ⭐ 11.8K+ stars · Python · MIT · 2026-04-05 創建 · 已蒸餾 13 人物 + 1 主題

## 專案概述

女娲.skill 是一個 Claude Code Skill，核心能力是：**輸入一個人名，自動完成調研、提煉、驗證，產出一份可運行的「認知操作系統」Skill。**

> 「你想蒸餾的下一個員工，何必是同事。」

靈感來自 [colleague-skill](https://github.com/titanwings/colleague-skill)（蒸餾離職同事，GitHub 爆火），女娲進一步問：既然能蒸餾同事，為什麼不蒸餾賈伯斯、芒格、費曼、馬斯克？他們留下了大量可蒸餾的公開材料——著作、演講、訪談、社交媒體。

**這不是角色扮演。** 蒸餾出來的 Skill 用的是名人的**認知框架**來分析問題：賈伯斯用「聚焦即說不」和「端到端控制」，Naval 用「欲望即合同」，馬斯克用「漸近極限法」。

## 蒸餾五層

| 層次 | 說明 | 範例（芒格） |
|------|------|------------|
| **怎麼說話** | 表達 DNA — 語氣、節奏、用詞偏好 | 反向思考的措辭風格 |
| **怎麼想** | 心智模型、認知框架 | 多元思維模型、能力圈 |
| **怎麼判斷** | 決策啟發式 | 逆向思考、護城河判斷 |
| **什麼不做** | 反模式、價值觀底線 | 不碰看不懂的東西 |
| **知道局限** | 誠實邊界 | 蒸餾不了直覺、公開表達 ≠ 真實想法 |

## 工作原理（四階段）

```
輸入：一個人名
       │
       ▼
1. 六路並行採集（6 個 Agent 同時跑）
   ├── 著作
   ├── 播客 / 訪談
   ├── 社交媒體
   ├── 批評者視角
   ├── 決策記錄
   └── 人生時間線
       │
       ▼
2. 三重驗證提煉
   ├── 跨 2+ 領域出現過（不是隨口一說）
   ├── 能推斷對新問題的立場（有預測力）
   └── 不是所有聰明人都會這麼想（有排他性）
       │
       ▼
3. 構建 SKILL.md
   ├── 3-7 個心智模型
   ├── 5-10 條決策啟發式
   ├── 表達 DNA
   ├── 價值觀與反模式
   └── 誠實邊界
       │
       ▼
4. 品質驗證
   ├── 3 個此人公開回答過的問題（方向一致才通過）
   └── 1 個他沒討論過的問題（應表現適度不確定）
```

## 已蒸餾人物（13 + 1）

| 人物 | 領域 | 安裝 |
|------|------|------|
| Paul Graham | 創業/寫作/產品 | `npx skills add alchaincyf/paul-graham-skill` |
| 張一鳴 | 產品/組織/全球化 | `npx skills add alchaincyf/zhang-yiming-skill` |
| Karpathy | AI/工程/教育 | `npx skills add alchaincyf/karpathy-skill` |
| Ilya Sutskever | AI 安全/scaling | `npx skills add alchaincyf/ilya-sutskever-skill` |
| MrBeast | 內容創造/YouTube | `npx skills add alchaincyf/mrbeast-skill` |
| 特朗普 | 談判/權力/傳播 | `npx skills add alchaincyf/trump-skill` |
| 賈伯斯 | 產品/設計/戰略 | `npx skills add alchaincyf/steve-jobs-skill` |
| 馬斯克 | 工程/成本/第一性原理 | `npx skills add alchaincyf/elon-musk-skill` |
| 芒格 | 投資/多元思維 | `npx skills add alchaincyf/munger-skill` |
| 費曼 | 學習/教學/科學思維 | `npx skills add alchaincyf/feynman-skill` |
| Naval | 財富/槓桿/人生哲學 | `npx skills add alchaincyf/naval-skill` |
| 塔勒布 | 風險/反脆弱 | `npx skills add alchaincyf/taleb-skill` |
| 張雪峰 | 教育/職業規劃 | `npx skills add alchaincyf/zhangxuefeng-skill` |
| **X 導師** | X/Twitter 運營 | `npx skills add alchaincyf/x-mentor-skill` |

## 快速開始

```bash
# 安裝女娲
npx skills add alchaincyf/nuwa-skill

# 在 Claude Code 中蒸餾新人物
> 蒸餾一個保羅·格雷厄姆
> 造一個張小龍的視角 Skill

# 使用已蒸餾的 Skill
> 用芒格的視角幫我分析這個投資決策
> 費曼會怎麼解釋量子計算？
> 切換到 Naval，我在糾結三件事
```

## 配套：達爾文.skill

女娲造 Skill，**達爾文**讓 Skill 進化：

- 8 維度自動評估
- 棘輪機制（只保留改進，自動回滾退步）
- 獨立子 agent 評分

```bash
npx skills add alchaincyf/darwin-skill
```

## 目前限制 / 注意事項

- **蒸餾不了直覺** — 框架能提取，靈感不能
- **時間快照** — 截止到調研時間的認知狀態，捕捉不了突變
- **公開表達 ≠ 真實想法** — 只能基於公開資訊
- **依賴公開資料量** — 資料少的人物蒸餾品質會差
- **偏中文生態** — 張雪峰、張一鳴等中文人物有優勢，英文人物的中文表達可能不自然
- **品質驗證有限** — 4 題測試只是基本檢驗，複雜場景可能失準

## 研究價值與啟示

### 關鍵洞察

1. **「蒸餾認知操作系統」是 Skill 設計的新範式。** 大多數 Skill 封裝的是「方法論」（怎麼做 A/B 測試、怎麼審計廣告），女娲封裝的是「思維方式」（芒格怎麼想、費曼怎麼教）。這是更高層次的抽象——方法論教你做事，認知框架教你判斷。

2. **三重驗證是防止「名人語錄堆砌」的關鍵設計。** 要求觀點必須跨領域出現（不是隨口說）、有預測力（能推斷新問題）、有排他性（不是常識）——這三道門檻確保提取的是真正的認知框架，而非表面引言。

3. **六路並行 + 批評者視角是調研方法論的亮點。** 特別是「批評者視角」——大多數人只看正面資料。女娲刻意收集批評，讓蒸餾出的 Skill 更平衡。這對任何調研工作都有參考價值。

4. **「誠實邊界」讓 Skill 值得信任。** 每個 Skill 明確標注做不到什麼——這是 Asgard Skills 的「Iron Law」概念的另一種表達。一個不告訴你局限在哪的 Skill，確實不值得信任。

5. **達爾文.skill 的棘輪機制是 Skill 品質進化的正確模式。** 只保留改進、自動回滾退步——這是遺傳演算法的思路，用在 Skill 優化上非常契合。

### 與其他專案的關聯

- **vs Andrej Karpathy Skills（筆記庫中）：** Karpathy Skills 蒸餾的是「LLM 的行為規範」（4 條原則），女娲蒸餾的是「人類的認知框架」（心智模型 + 決策啟發式）。前者控制 Agent 行為，後者賦予 Agent 視角。
- **vs Asgard Skills（筆記庫中）：** Asgard 封裝 263 個領域方法論（SWOT、DCF、OEE），女娲封裝 13 個人物的思維方式。Asgard 告訴你「怎麼分析」，女娲告訴你「用誰的視角分析」。
- **vs Karpathy LLM Wiki（筆記庫中）：** LLM Wiki 蒸餾研究知識到 Markdown，女娲蒸餾人物認知到 SKILL.md。兩者都是 Karpathy 「編譯」理念的延伸——預先編譯知識/認知，而非每次重新推導。
- **vs wshobson/agents：** wshobson 提供 182 個 Agent 做具體工作（code review、security scan），女娲提供 13 個「思維顧問」做決策輔助。一個是「手」，一個是「腦」。
