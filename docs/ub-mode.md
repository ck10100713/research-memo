---
date: "2026-10-30"
category: "Coding Agent 工具"
card_icon: "material-broom"
oneliner: "Uncle Bob(Robert C. Martin)把 poteto-mode 的原則砍到只剩一份約 140 行的 SKILL.md:Make it Work → Make it Right → Practice 三段,每條原則壓成兩三句祈使句,並強制 TDD;最大差異是把『寫得好不好』交給自己寫的三個確定性工具把關(crapper 的 CRAP < 10、dryer 的重複度 < 0.8、mutator 的突變測試)。5 天 4.8k★,但 repo 沒有授權檔"
tags:
  - claude-code
  - skills
  - ai-coding
  - testing
---

# ub-mode 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/unclebob/ub-mode> |
| 品質閘門工具 | [crapper](https://github.com/unclebob/crapper)、[dryer](https://github.com/unclebob/dryer)、[mutator](https://github.com/unclebob/mutator) |
| 視覺化 | [uml-viewer](https://github.com/unclebob/uml-viewer) |
| 來源 | [poteto-mode / pstack](poteto-mode.md) |
| 分析 commit | `57a8bdd`(2026-10-25) |

> Metadata(2026-10-30 抓取):**4,842 stars / 268 forks** · 建立於 2026-10-25,總共 4 個 commit,全部是 Robert C. Martin 本人。整個 repo 只有 `README.md` 和 `SKILL.md`。**沒有 LICENSE 檔**,預設保留所有權利;三個工具則是 0BSD。

## 一句話

《Clean Code》作者 Uncle Bob 的 agent 工作守則。README 自己說是「loosely based on portions of @poteto's rules」,把 poteto-mode 的原則刪減、改寫成短句,再配上他自己寫的三個量化品質工具。

## SKILL.md 的結構

每次改動都依序走三段:

### 1. First Make it Work

| 原則 | ub-mode 的寫法(摘要) |
|------|------|
| Laziness Protocol | 一個決定只放在一個地方;交出解決問題的最小改動 |
| Foundational Thinking | 先把資料形狀弄對再寫邏輯;先做對後面每個階段都有幫助的事;有並行寫入就不要共享狀態 |
| **TDD** | 先寫會失敗的測試,看它**因為你預期的原因**失敗,再做讓它通過的最小改動;寫不出誠實的測試就別寫爛測試 |
| Redesign From First Principles | 別把新需求硬接到舊設計上,想「一開始就有這需求會怎麼做」,再分段交付 |
| Attack the Premise | 共用同一個前提的兩個修法都失敗,就把前提寫成一句話,在動下一個修法前先處理它 |
| Subtract Before You Add | 加東西之前先拿掉複雜度 |
| Outcome-Oriented Execution | 瞄準可檢查的最終狀態;中途壞掉可以,但要是計畫好、可回復的 |
| Build the Lever | 不是一眼就懂的工作,就做工具來做;先手做一個單位,再讓工具做到一樣 |
| Architecture | Model the Domain(讓非法狀態不可能存在,**維護領域詞彙表**,已經清楚的局部程式碼就別動)、Boundary Discipline、Type System Discipline(不准讓編譯器閉嘴)、Idempotent、一個寫入者 |

### 2. Then Make it Right

- **Fix Root Causes**:重現、修原因;只是把 crash 藏起來的 guard 不算修
- **Sequence work into verifiable units**:做完一小塊、驗證,再做下一塊
- **Test Behavior, Not Implementation**:測試要像使用者那樣呼叫、檢查使用者看得到的結果。**如果每個函式都回傳空值測試還會過,就把它丟掉**
- **Crapper**:每個函式 CRAP 壓到 10 以下,靠拆分、補測試或兩者;case 敘述值不值得拆要考慮
- **Dryer**:消除相似度 0.8 以上的重複
- **Mutator**:補上沒覆蓋的、殺掉存活的突變、刪掉死碼
- **Refactoring**:先釘住行為、改結構、證明行為沒變

### 3. Practice

- **Keep a Log**:記下每個動作和理由,完成時回報
- **Guard the Context Window**:主線保持精簡,大量內容送出去、只留摘要
- **Worktree Cleanup**:確認沒人在用才回收;沒 commit 的東西等人決定
- **Commit and Push**:小而有序的 commit,每個說明為什麼、改了什麼、怎麼證明的;**最後 push 到主線**

## 三個品質閘門工具

三個都是 Python 寫的,0BSD,支援 Clojure、Java、Go、TypeScript、Rust、Python。第一次跑會自己建 `.venv`,結果寫進 `.metrics/*.edn` 給 uml-viewer 讀。

| 工具 | 量什麼 | 判準 |
|------|--------|------|
| `crapper` | `CRAP = CC² × (1 − coverage)³ + CC`,CC 是循環複雜度 | 1–5 低風險、5–30 值得看、30+ 又複雜又沒測;ub-mode 要求 < 10。`--threshold` 超標 exit 2 |
| `dryer` | 正規化後的語法樹指紋做 Jaccard 相似度,變數名、字面值都會被抹掉,只留呼叫名、運算子、樹形 | 預設門檻 0.82,ub-mode 寫 0.8 |
| `mutator` | 突變測試:改掉 `>` 變 `>=` 之類,看測試有沒有抓到 | 有存活突變 exit 3。第二次起只重跑存活的和有改過的函式 |

常用參數三個都有:`--changed`(只看 git 變動)、`--use-existing-coverage`。mutator 需要把 crapper clone 在旁邊(`../crapper`)。

`uml-viewer`(Clojure + Quil,需要 Java 21+)把專案畫成可點擊的 UML,依 CRAP 和突變分數上色,違反 Clean Architecture 依賴規則的箭頭標紅。它跟 agent 雙向連動:你在圖上說哪裡不喜歡,agent 改 policy 重畫,滿意了再叫 agent 把程式碼改成圖上那樣。

## 跟 poteto-mode 比

| | poteto-mode | ub-mode |
|---|---|---|
| 大小 | 1 入口 + 23 playbook + 24 principle + 二十多個 skill | 1 份約 140 行的 SKILL.md |
| 怎麼觸發 | 依情境觸發表 + playbook 路由 | 沒有路由,每次改動都走同樣三段 |
| 品質靠什麼 | 多模型對抗審查(interrogate)、subagent 寫審分離 | **確定性工具的數字**:CRAP、重複度、突變存活數 |
| 測試 | 有 tdd skill,但 bug fix 才建議先寫失敗測試 | TDD 是第一段的必經步驟 |
| Subagent | 大量使用,模型分工 | 只有一句「大量內容送出去」 |
| 刪掉的 | | playbook、多模型、PR 流程、回覆文風、Experience First、Exhaust the Design Space、Never Block on the Human 等 |
| 新加的 | | TDD、領域詞彙表、Keep a Log、三個量化閘門、Refactoring 三步 |

刪掉的東西很有代表性:poteto-mode 偏向「讓 agent 自己判斷、少打擾人、多模型交叉檢查」,ub-mode 偏向「用測試和數字約束 agent,判斷越少越好」。

## 值得注意的地方

1. **把「寫得好」從主觀判斷變成可量測的閘門**。這是 poteto-mode 的 Encode Lessons in Structure 原則真正落地的樣子:agent 不用自己判斷函式夠不夠簡單,跑 crapper 看數字就好。突變測試尤其能抓 agent 寫出「每個函式回傳空值也會過」的假測試
2. **原則壓成兩三句祈使句**,跟 poteto-mode 每條原則一個 skill 檔相比,context 成本低很多,適合直接常駐
3. **「最後 push 到主線」要小心**。直接推 main 適合他一個人的專案;團隊協作或有「只有使用者要求才 push」規則的環境,這條要改
4. **沒有授權檔**。可以讀、可以照著寫自己的版本,但嚴格來說不能直接轉載或改作發布。工具本身是 0BSD,可以放心用
5. **工具門檻**:三個工具都需要測試覆蓋率報告才有完整分數,沒有測試的專案只能先跑 `--no-coverage`;突變測試第一次跑整個 repo 會很慢,作者建議從正在改的檔案開始
6. 5 天 4.8k 星主要是作者的名氣。內容本身是 poteto-mode 的濃縮版,真正新的東西是那三個工具

## 跟其他筆記的關係

- [poteto-mode](poteto-mode.md) 是它的來源,兩篇對照看最清楚
- [Ponytail](ponytail.md) 的「先問要不要存在、最小改動」對應 Laziness Protocol 和 Subtract Before You Add
- [Laws of Software Engineering](laws-of-software-engineering-zh.md) 收了 Uncle Bob 提出的童子軍規則和 SOLID
