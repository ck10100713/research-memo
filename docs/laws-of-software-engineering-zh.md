---
date: "2026-05-25"
category: "軟體工程知識"
card_icon: "material-translate"
oneliner: "56 條軟體工程定律完整中文版，每條附背景、實例、應用建議，搭配 laws-of-software-engineering.md 原版作為中文受眾學習資源"
tags:
  - learning
  - software-engineering
---

# 軟體工程 56 大定律（完整中文版）

> 本文是 [Laws of Software Engineering 研究筆記](laws-of-software-engineering.md) 的中文展開版。原網站每條定律只有一行英文，這裡為每條補上 2–4 句中文說明、典型場景、實務應用。
>
> **資料來源**：<https://lawsofsoftwareengineering.com/>（Dr. Milan Milanović 整理，CC BY-NC-ND 4.0）

---

## 一、Teams 團隊（9 條）

### 1. Conway's Law（康威定律）

> 「設計系統的組織，最終會做出鏡像自己溝通結構的設計。」

當你的後端、前端、QA 各在三個城市、用三種不同的會議節奏，**最終端出的系統就會自然分裂成三個服務**，而且 API 介面會卡在組織邊界上。反過來說，要做出微服務架構，組織必須先變成可以獨立溝通的小組（這就是「逆 Conway 操作」）。**啟示**：架構決定組織？不，是組織決定架構。動架構之前先動組織。

### 2. Brooks's Law（布魯克斯定律）

> 「給落後的軟體專案加人，只會讓它更晚。」

Frederick Brooks 在《人月神話》提出。新成員需要時間 onboard，原成員要花時間帶人，溝通路徑隨人數平方增加。**例子**：12 月發版，11 月才加 3 個工程師基本上等於 0 加速還有減速。**例外**：如果任務真的可平行切分（如獨立模組、寫測試）才有效，但這種狀況遠比想像稀有。

### 3. Dunbar's Number（鄧巴數）

> 「一個人能維持穩定社交關係的認知上限約 150 人。」

人類學家 Robin Dunbar 提出。意味著**單一團隊或公司一旦超過 150 人，就會出現「彼此不認識」的次群體**，需要正式制度（流程、文件、組織圖）取代非正式信任。**啟示**：Startup 在 50/150/500 三個門檻會經歷組織模式劇變，提前準備比事後重組便宜。

### 4. Ringelmann Effect（林格曼效應）

> 「團隊變大時，每個成員的個人產出反而下降。」

1913 年 Maximilien Ringelmann 用拔河實驗證明：8 人拔河的力量小於 8 個人單獨拔河力量加總。**原因**：協調成本 + 責任分散（覺得別人會做）。**啟示**：「再加一個人」常常不是線性增加產能，而是線性增加開會時間。

### 5. Price's Law（普萊斯定律）

> 「任何群體中，前 √N 個人貢獻一半的產出。」

100 人團隊，前 10 人貢獻 50%；10,000 人公司，前 100 人貢獻 50%。**現實**：產出分佈是冪律不是常態。**管理啟示**：找到並留住 top √N 人比平均提升所有人更划算；不過也要小心 √N 一旦離職衝擊巨大（連動 Bus Factor）。

### 6. Putt's Law（普特定律）

> 「科技由兩種人主宰：懂得他們不會管理的事，跟管理他們不懂的事的人。」

諷刺 IT 組織常見現象：技術強的不想當主管，主管又不夠懂技術。**對策**：建立「個人貢獻者（IC）職涯軌道」與管理職並行，讓技術專家有同等晉升通道，避免被迫去管不擅長的人。

### 7. Peter Principle（彼得原理）

> 「在層級組織中，每個員工都會被升遷到自己無法勝任的位置為止。」

Laurence Peter 1969 提出。一個優秀工程師升 tech lead，再升 manager，再升 director——每一步都用「上一個職位的表現」評估，直到他做不來為止，然後就卡在那。**對策**：晉升前先「臨時試任」、設定可逆回機制、雙軌制（IC vs Manager）。

### 8. Bus Factor（公車因子）

> 「團隊裡最少幾個人被公車撞走，專案就會停擺。」

Bus Factor = 1 表示只有一個人懂某個關鍵系統，極度危險。**改善方法**：強制 code review、輪調、配對程式設計（pair programming）、寫文件、舉辦「knowledge sharing 午餐」。**警訊**：當有人說「這個只有 X 才能改」，就是亮紅燈了。

### 9. Dilbert Principle（呆伯特原理）

> 「公司把最不適任的員工升上管理職，以免他們真的搞砸技術。」

Scott Adams 在漫畫《呆伯特》中諷刺提出，比 Peter Principle 更悲觀。**現實意涵**：晉升決策有時不是擇優而是避害，新人面試時觀察管理職的技術水準，可以推測該公司的晉升文化。

---

## 二、Planning 規劃（6 條）

### 10. Premature Optimization（過早優化）

> 「過早優化是萬惡之源。」—— Donald Knuth

Knuth 完整原句是「我們應該忘記小效率，大約 97% 的時間都應該如此：過早優化是萬惡之源。」**重點**：先寫對、再寫好、最後才寫快。**例子**：為了「萬一未來要支援百萬 QPS」而現在引入 Kafka + 分散式 cache，但目前 DAU 才 100，這就是過早優化。**例外**：演算法複雜度（O(n²) vs O(n log n)）這種「結構性」優化要在設計時就考慮，而非微觀效率。

### 11. Parkinson's Law（帕金森定律）

> 「工作會自動膨脹，直到填滿所有可用的完成時間。」

給 1 週就花 1 週，給 2 週就花 2 週。**對策**：設「足夠緊但合理」的 deadline、用 timebox（如 2 小時內必須產出 v0）、限制 sprint 長度。**注意**：太緊會壓垮品質，目標是「沒有閒置時間」而非「沒有思考時間」。

### 12. Ninety-Ninety Rule（九十-九十法則）

> 「程式碼前 90% 花 90% 時間，剩下 10% 又再花 90% 時間。」

Tom Cargill, Bell Labs 提出，幽默地說明軟體開發總是「快做完了，再給我兩週」。**真實成因**：邊界情境、整合測試、UI 細節、效能調校永遠比想像多。**對策**：估算時把「完工 90%」當成「進度 50%」處理。

### 13. Hofstadter's Law（霍夫斯塔特定律）

> 「事情花的時間總是比你預期長，就算你已經把這條定律算進預期也一樣。」

Douglas Hofstadter 提出的自指悖論。**啟示**：估算時加 buffer 然後告訴自己「這次有加 buffer 不會爆」——還是會爆。**對策**：不要單純加百分比，而是「拆細到 0.5 天為單位」的任務切分；對未知性高的任務直接做 spike（探索性實作）。

### 14. Goodhart's Law（古哈特定律）

> 「當一個指標變成目標，它就不再是個好指標。」

英國經濟學家 Charles Goodhart 1975 年提出。**例子**：用「代碼行數」評估工程師 → 大家寫長 code；用「修 bug 數」評估 QA → 大家拼命找小 bug 充數；用「PR 數量」評估產出 → PR 變小變多但價值未提升。**對策**：用多個互相牽制的指標（如 PR 數 + 線上故障率 + code review 評分），並定期換指標。

### 15. Gilb's Law（吉爾布定律）

> 「凡是需要量化的東西，再爛的量化都比不量化好。」

Tom Gilb 提出。**意涵**：很多人因為「無法精準量化」就放棄量化，但「粗略量化」也能逼出共識。**例子**：估「使用者滿意度」與其爭論「該用 NPS 還是 CSAT 還是質性訪談」，先用最簡單的「1-10 分」開始，至少能比較不同版本的相對好壞。

---

## 三、Architecture 架構（9 條）

### 16. Hyrum's Law（海勒姆定律）

> 「當一個 API 的使用者夠多時，你在合約上承諾的內容都不重要——所有可觀察的行為都會被人依賴。」

Google 工程師 Hyrum Wright 提出。**例子**：你只承諾「回傳 user list」，但實際回傳「按創建時間排序」。某天你優化 query 改成按 ID 排序，**所有依賴順序的客戶端都會壞**——即使你從未在合約中承諾過順序。**對策**：故意加入隨機性（如打亂回傳順序），讓使用者不可能依賴你沒承諾過的行為。

### 17. Gall's Law（蓋爾定律）

> 「能運作的複雜系統，無一例外是從能運作的簡單系統演化而來。從零設計的複雜系統永遠不會 work，且無法事後修補成 work。」

John Gall 提出。**對應**：不要試圖一次設計微服務帝國，先從 monolith 開始，用得不爽再拆。**例子**：Twitter、Amazon、Netflix 都從 monolith 開始，幾年後才拆成微服務。從第一天就上分散式架構的新創 99% 都失敗。

### 18. Law of Leaky Abstractions（抽象洩漏定律）

> 「所有非平凡的抽象，在某種程度上，都會洩漏底層細節。」

Joel Spolsky 提出。**例子**：ORM 號稱讓你不用懂 SQL，但 N+1 query 問題、deadlock、transaction isolation 還是會逼你回去懂底層；TCP 號稱可靠傳輸，但 network partition 還是會讓你的 socket hang。**對策**：使用任何抽象前，先理解它在什麼情境會洩漏，並準備好降級路徑。

### 19. Tesler's Law（特斯勒定律 / 複雜度守恆律）

> 「每個系統都有一個不可消除的最小複雜度——這份複雜度只能轉移，不能消除。」

Larry Tesler 在設計使用者介面時提出。**例子**：日期解析的所有時區、夏令時、閏秒問題——你可以把它藏進函式庫讓使用者輕鬆，但函式庫作者必須承擔。**啟示**：當你「簡化」一個系統時，問自己「我把複雜度推到哪去了？」如果答不出來，你只是搬到使用者頭上。

### 20. CAP Theorem（CAP 定理）

> 「分散式系統在 Consistency（一致性）、Availability（可用性）、Partition Tolerance（分區容錯）三者中，最多只能保證兩個。」

Eric Brewer 2000 年提出，後由 MIT Gilbert & Lynch 證明。**現實**：網路分區一定會發生（P 必選），所以實際是 CP vs AP 的選擇。**例子**：銀行交易選 CP（寧可拒絕也不能不一致）；社群動態選 AP（寧可看到舊資料也不能不能用）。

### 21. Second-System Effect（第二系統效應）

> 「成功的小系統，往往在第二版被過度設計毀掉。」

Frederick Brooks 在《人月神話》提出。第一版因為資源緊湊被迫精簡，剛好做到能用；做第二版時「這次我有時間、有預算、有經驗，我要把所有第一版的妥協都修正」——結果加了一堆沒人要的功能。**例子**：Netscape 6、Windows Vista、Perl 6（Raku）都是經典案例。

### 22. Fallacies of Distributed Computing（分散式運算謬誤）

> 「新手設計分散式系統時常犯的 8 個錯誤假設。」

由 L. Peter Deutsch 1994 提出，後 James Gosling 補完：
1. 網路可靠
2. 延遲為零
3. 頻寬無限
4. 網路安全
5. 拓撲不變
6. 只有一個管理員
7. 傳輸成本為零
8. 網路是同質的

**對策**：設計分散式系統前，每一條都假設為 false 來規劃。

### 23. Law of Unintended Consequences（非預期後果定律）

> 「對複雜系統的任何介入都會產生超出預期的後果，有時還是負面的。」

社會學家 Robert K. Merton 提出。**例子**：加 cache 提速但帶來 cache invalidation 地獄；引入 message queue 解耦但帶來重複訊息問題；上 Kubernetes 解環境差異但增加團隊認知負擔。**對策**：所有架構變動先設「回滾路徑」，並監控「沒預期到的指標」。

### 24. Zawinski's Law（札溫斯基定律）

> 「所有程式最終都會擴展到能夠讀電子郵件的地步。無法擴展的會被能擴展的取代。」

Jamie Zawinski（Netscape、Mozilla）幽默觀察。**現代版本**：所有程式最終都會擴展到內建聊天功能 / AI 助理。**啟示**：成功軟體傾向變肥；要保持精簡需要刻意抗拒功能蔓延（feature creep）。

---

## 四、Quality 品質（11 條）

### 25. Boy Scout Rule（童子軍規則）

> 「離開營地時讓它比你來的時候更乾淨。」—— 套用到 code 上：每次 check in 都讓 codebase 變好一點點。

Robert C. Martin 提出。**實踐**：修 bug 時順手改個爛變數名、補個註解、補個測試。**注意**：別變成 yak shaving——讓 PR 過大難 review。原則是「小到不會擋住主要改動」的範圍。

### 26. Murphy's Law（莫非定律）

> 「凡是可能出錯的事，就一定會出錯。」

最古老的工程定律之一。**對軟體啟示**：所有 if/else 的兩支都會被執行到、所有 timeout 都會被觸發、所有 race condition 都會在 production 出現。**對策**：寫程式時假設「不該發生的事一定會發生」，並做 defensive coding（input 驗證、null check、retry、timeout）。

### 27. Postel's Law / Robustness Principle（波斯特定律 / 健壯性原則）

> 「對自己輸出嚴格，對別人輸入寬容。」—— Jon Postel（TCP 設計者）

**例子**：HTML 瀏覽器寬容地處理破碎的 tag，所以網頁能被各種爛爬蟲、爛編輯器產生。但這條定律近年有爭議——**輸入太寬容會讓垃圾資料污染整個生態系**（HTML 標準混亂就是後果）。**現代修正**：對輸入嚴格驗證 + 提供明確錯誤訊息，比「猜」更好。

### 28. Broken Windows Theory（破窗理論）

> 「一棟有破窗的建築會吸引更多破壞——軟體 codebase 也一樣。」

從犯罪學引入軟體工程。**例子**：一個 codebase 有 50 個 TODO 註解、3 處 hack patch，新人會覺得「反正也都這樣」繼續加新 hack。**對策**：高頻清掃小問題、不容忍 commented-out code、不容忍「暫時的」變通方案存活超過 1 sprint。

### 29. Technical Debt（技術債）

> 「任何拖慢未來開發速度的東西都是技術債。」

Ward Cunningham 提出的金融類比：debt 不全是壞事（有時需要快速借貸交付），但要付利息（持續維護成本）。**分類**：刻意的（趕 launch）vs 無心的（不知道更好做法）；可償還的 vs 不可償還的。**對策**：把技術債列入 backlog、量化（多少 dev-day）、定期還債（每個 sprint 留 20%）。

### 30. Linus's Law（林納斯定律）

> 「眼睛夠多，所有 bug 都會浮現。」—— Linus Torvalds

開源運動的核心理念。**前提**：眼睛要真的看，不是在 review 框裡按 LGTM。**現實**：很多開源專案有 100k stars 但實際 review 的只有 3 個人，所以這條定律的有效性其實取決於「有效的眼睛數」。

### 31. Kernighan's Law（柯尼漢定律）

> 「除錯比寫程式碼難一倍。如果你用盡聰明寫程式，定義上你不夠聰明除錯它。」—— Brian Kernighan

**啟示**：寫程式時刻意降一個聰明度，留下空間給除錯。**例子**：別寫一行做 5 件事的 Python 列表推導；別用三層巢狀 ternary。**反例**：那些「one-liner 大師」的 code 漂亮但沒人能維護。

### 32. Testing Pyramid（測試金字塔）

> 「測試金字塔：底層大量單元測試，中層適量整合測試，頂層少量 UI/E2E 測試。」

Mike Cohn 提出。**理由**：單元測試快、便宜、好維護；E2E 慢、貴、脆弱。**反模式**：倒金字塔（一堆 E2E、沒單元測試）會讓 CI 跑 30 分鐘，每次都有人 retry。**例外**：近年「測試蜂巢」「測試冰淇淋」等變體針對微服務、AI 應用有不同建議。

### 33. Pesticide Paradox（殺蟲劑悖論）

> 「同樣的測試案例反覆執行，會逐漸失去抓 bug 的能力——因為 bug 已經適應了。」

Boris Beizer 提出。**現實**：通過 CI 久了不代表沒 bug，只代表沒 **這組測試能抓的 bug**。**對策**：定期 review 測試案例、引入 fuzzing/mutation testing、做 chaos engineering。

### 34. Lehman's Laws of Software Evolution（萊曼軟體演化定律）

> 「持續使用的軟體必須持續演化，否則它的使用價值會下降。」

Manny Lehman 1974 年提出 8 條定律，核心是「軟體不像建築物——它需要持續變化才能保持有用」。**意涵**：「重寫 = 從零做」的衝動經常錯誤；演化式重構（strangler fig pattern）通常更安全。

### 35. Sturgeon's Law（史特金定律）

> 「世上 90% 的東西都是垃圾。」—— Theodore Sturgeon

科幻作家 Sturgeon 回應「為何科幻 90% 都很爛」時說「**所有東西** 90% 都很爛」。**對軟體啟示**：套件、教學文章、Stack Overflow 答案、AI 生成 code，90% 品質堪憂——保持懷疑，主動驗證。

---

## 五、Design 設計（6 條）

### 36. YAGNI（You Aren't Gonna Need It）

> 「你不會需要它的。」

XP（極限程式設計）的核心原則。**意涵**：「萬一未來要⋯」這種理由 99% 不會發生，但你為它寫的程式碼會 100% 增加維護成本。**例子**：「先做個 plugin 系統吧未來會擴充」——結果未來只擴充了一次，但 plugin 系統花了 3 週寫且讓所有人都要學它。**例外**：成本極低的擴充點（如 enum）可以預留。

### 37. DRY（Don't Repeat Yourself）

> 「每一份知識都該在系統中只有一份權威、明確、清楚的表示。」

Andy Hunt & Dave Thomas《The Pragmatic Programmer》提出。**注意**：DRY 是「知識不重複」不是「代碼不重複」。**反例**：兩段看起來一樣但其實邏輯獨立的 code 被強行抽出共用函式，結果兩邊需求分歧時這個函式變怪物。**對立面**：WET（Write Everything Twice，先重複兩次再抽象）或 AHA（Avoid Hasty Abstractions）。

### 38. KISS（Keep It Simple, Stupid）

> 「保持簡單，傻瓜。」

美國海軍 Kelly Johnson 工程師提出。**啟示**：能用 if/else 就別用 strategy pattern；能用 list 就別用樹；能不寫 cache 就別寫 cache。**判準**：當你需要解釋三層才有人聽懂，就太複雜了。

### 39. SOLID Principles（SOLID 五原則）

> Robert C. Martin 提出的物件導向五大原則：
>
> - **S**ingle Responsibility：一個類別只負責一件事
> - **O**pen/Closed：對擴充開放，對修改封閉
> - **L**iskov Substitution：子類別必須能無痛取代父類別
> - **I**nterface Segregation：寧可多個小介面，不要一個大介面
> - **D**ependency Inversion：依賴抽象，不依賴具體實作

**現代爭議**：函式式編程社群認為 SOLID 過度物件導向，且容易導致過度抽象。但在大型 codebase（特別是 Java、C#、TypeScript）仍是基本功。

### 40. Law of Demeter（迪米特法則 / 最少知識原則）

> 「只跟你的直接朋友說話，別跟陌生人說話。」

物件 A 不該知道物件 B 的內部結構。**反模式**：`user.account.address.city.toUpperCase()`——這就是「跟陌生人說話」，A 知道太多 B 的內部結構。**對策**：B 提供 `getCity()` 介面，A 不需要穿越多層。**啟示**：減少耦合，重構時影響面更小。

### 41. Principle of Least Astonishment（最少驚訝原則）

> 「軟體應該以使用者預期的方式運作。」

**例子**：刪除鈕真的刪除（不是封存）；Ctrl+S 真的存檔（不是另存）；命令列 `--help` 真的給說明。**反例**：rm -rf / 沒有警告（雖然 GNU rm 後來補了 --preserve-root）。**對 API 設計**：函式名稱要忠實反映行為，否則使用者會基於名稱推測錯誤的行為。

---

## 六、Scale 規模（3 條）

### 42. Amdahl's Law（阿姆達爾定律）

> 「程式平行化的最大加速比，受限於不可平行化部分的比例。」

公式：S = 1 / ((1-P) + P/N)，其中 P 是可平行比例，N 是處理器數。**意涵**：即使你有 1000 核心，如果 5% 的程式必須序列執行，最大加速比也只有 20 倍。**啟示**：找出並消除序列瓶頸比加機器更有效。

### 43. Gustafson's Law（古斯塔夫森定律）

> 「對於夠大的問題，平行加速比可以接近處理器數量。」

修正 Amdahl 過度悲觀的視角：實務上問題規模會隨運算力一起變大（如資料變大、模擬精度變高），所以 N 越多，能解的問題也越大。**對應 Amdahl**：兩條定律不矛盾——Amdahl 看固定問題、Gustafson 看可放大問題。**現代意涵**：大資料 / ML 訓練適用 Gustafson；單一請求 latency 優化適用 Amdahl。

### 44. Metcalfe's Law（梅特卡夫定律）

> 「網路的價值正比於連線使用者數的平方。」

Robert Metcalfe（乙太網路發明者）提出。**例子**：一台傳真機沒用、兩台傳真機可以互傳、100 台傳真機產生 4950 對連線。**對社群網路啟示**：用戶數翻倍，網路效應四倍；這也是為什麼 Facebook、LinkedIn 一旦領先就難被追上。**修正版**：Reed's Law（Network of Groups）認為價值是 2^N（指數）；Zipf's Law 認為實際是 N×log(N)。

---

## 七、Decisions 決策（12 條）

### 45. Dunning-Kruger Effect（達克效應）

> 「能力不足者高估自己；高能力者低估自己。」

心理學家 Dunning & Kruger 1999 研究。**新人陷阱**：剛學會 Python 兩週的人最容易覺得「我能寫整個系統」。**老兵陷阱**：相反，越懂越覺得自己不夠懂（冒牌者症候群）。**對策**：對自信過剩者要求 demo；對自信不足者給予明確 feedback。

### 46. Hanlon's Razor（漢隆剃刀）

> 「能用愚蠢解釋的，別用惡意解釋。」

**對 code review 啟示**：看到爛 code 別先假設「他在搞我」，先假設「他不知道更好做法」。**對工作關係啟示**：同事忘記回信、忘記 review，先假設他忙昏，不是針對你。**例外**：當行為模式重複出現時，可能真的不只是粗心。

### 47. Occam's Razor（奧坎剃刀）

> 「若無必要，勿增實體。」—— 14 世紀 William of Ockham

**簡化版**：最簡單的解釋通常最對。**除錯應用**：bug 出現時，先懷疑自己最近的改動，不是「編譯器壞了」「Linux kernel 有問題」「太陽黑子干擾」。**例外**：簡單不是真理的保證——只是「在沒有更多資訊前的合理起點」。

### 48. Sunk Cost Fallacy（沉沒成本謬誤）

> 「已經投入的成本不該影響未來決策，但人類大腦總是會被它影響。」

**例子**：花了 6 個月寫的微服務拆分專案，發現方向錯了——但「都做了一半了」這個念頭讓你繼續做完。**對策**：定期做 sunk cost audit：「如果我今天從零開始，會不會選這條路？」答案若是 no，就該止損。

### 49. The Map Is Not the Territory（地圖不是領土）

> 「我們對現實的描述不等於現實本身。」—— Alfred Korzybski

**對軟體啟示**：架構圖不是系統、文件不是真相、metrics 不是使用者體驗。**例子**：監控圖表全綠，但使用者抱怨慢——因為你的 dashboard 量的是「平均延遲」而不是「P99 延遲」。**對策**：定期離開地圖、直接接觸領土（用自家產品、看真實 log、訪談使用者）。

### 50. Confirmation Bias（確認偏誤）

> 「人會優先尋找、解讀、記住能支持自己既有信念的資訊。」

**對除錯啟示**：你認為是資料庫的問題，所以一直查 DB log，忽略真正壞掉的是 cache 層。**對 A/B 測試啟示**：實驗結果不顯著時，會忍不住挑「對自己有利」的子群顯著結果（p-hacking）。**對策**：刻意找「我可能錯」的證據，pre-register 假設。

### 51. Hype Cycle & Amara's Law（炒作循環與阿馬拉定律）

> Amara: 「我們總是高估科技短期影響，低估長期影響。」  
> Gartner Hype Cycle: 創新觸發 → 期望膨脹 → 幻滅低谷 → 啟蒙坡道 → 生產高原。

**例子**：區塊鏈在 2017 被高估、2020 跌進低谷、之後慢慢找到金融以外的應用；LLM 在 2023 被高估「明年取代工程師」、2024-2025 進入「實際整合」階段。**對策**：對新技術評估時加上 3-5 年時間軸校正。

### 52. Lindy Effect（林迪效應）

> 「對於非生物的事物（書、技術、想法），已經存在越久，預期還會存在越久。」

**對技術選型啟示**：Python（35 年）比某新框架（3 年）更可能在 10 年後還在；SQL（50 年）比某 NoSQL 新貴（5 年）更穩健。**反向**：Lindy 不適用於「正在被淘汰中」的事物——它假設目前還活著。**對策**：選穩定技術做核心，選新技術做邊緣實驗。

### 53. First Principles Thinking（第一性原理思考）

> 「把問題拆解到最基本的事實，再從那裡重新推理。」—— Aristotle、Elon Musk 推廣

**例子**：「火箭很貴」這個前提，拆到第一性原理變成「鋁、銅、燃料的原料成本」，發現實際只佔售價 2%——所以 SpaceX 從製造端切入。**對軟體啟示**：當所有人都說「必須用 X 框架」時，問「我們的核心需求是什麼？X 真的是滿足那個需求的最佳解嗎？」

### 54. Inversion（反向思考）

> 「想解決問題，先思考如何讓它失敗。」—— Carl Jacobi、Charlie Munger

**例子**：想做出好的 onboarding？先列「怎樣讓新人最快流失」，然後反過來做。**對軟體啟示**：寫 spec 時除了「成功路徑」，先列「最糟情況清單」（pre-mortem），然後設計防護。

### 55. Pareto Principle（80/20 法則）

> 「80% 的結果來自 20% 的原因。」

Vilfredo Pareto 1906 提出。**例子**：80% 的 bug 集中在 20% 的程式碼；80% 的 customer support 來自 20% 的功能；80% 的 cloud cost 來自 20% 的服務。**對策**：找出那 20%，集中資源處理。**警告**：不是萬靈丹——有時分佈不是 80/20 而是 99/1 或 60/40。

### 56. Cunningham's Law（康寧漢定律）

> 「在網路上得到正解最快的方法不是發問，是發表錯誤答案。」—— Ward Cunningham

**原理**：人類更願意糾正錯誤而非回答問題。**應用**：寫部落格、發 X 推文時故意提出有破綻的觀點，引出更深入的討論；做 RFC 時提出「scrappy 草稿」比完美草稿更快收到 feedback。**注意**：用過頭會被當 troll，要拿捏。

---

## 整體啟示

### 1. 56 條的「次數密度」洩漏軟體工程真實瓶頸

| 分類 | 條數 | 比例 |
|------|------|------|
| Decisions | 12 | 21.4% |
| Quality | 11 | 19.6% |
| Teams | 9 | 16.1% |
| Architecture | 9 | 16.1% |
| Design | 6 | 10.7% |
| Planning | 6 | 10.7% |
| Scale | 3 | 5.4% |

**Decisions + Quality + Teams = 57%**。三大類都跟「人」直接相關——人會誤判（Decisions）、人寫的東西會壞（Quality）、人組成團隊有摩擦（Teams）。**Architecture/Design/Scale 的「純技術」類加起來只佔 32%**。意涵：軟體工程的瓶頸主要在人，不在機器。

### 2. 多條定律互相印證 / 互相矛盾

- **互相印證**：Conway + Brooks + Ringelmann + Dunbar 共同說明「組織結構決定軟體結構」。
- **互相矛盾**：DRY vs YAGNI——前者鼓勵抽象、後者反對提早抽象；Postel's Law vs 現代 API 安全——前者要寬容、現代要嚴格驗證。**意涵**：定律不是教條，是「在某種情境下成立的經驗法則」，活用比死記重要。

### 3. AI 時代的新讀法

- Hyrum's Law 在 AI 時代成倍重要：AI agent 會學會依賴「所有可觀察行為」，比人類使用者更敏感。
- Sturgeon's Law（90% 是垃圾）在 LLM 生成內容時代成倍可怕。
- Goodhart's Law 在用 eval / benchmark 衡量 AI 時是核心警告——任何被當目標的指標都會被 overfit。
- 第一性原理思考 + Inversion 是 AI 時代給工程師最寶貴的兩個工具——LLM 擅長模式匹配但不擅長這兩種思考。

## 與其他研究筆記的關聯

- **[Laws of Software Engineering 原版筆記](laws-of-software-engineering.md)**：本文的英文簡表版 + meta 分析。
- **[Why Your AI Is Dumbing Down](why-your-ai-is-dumbing-down.md)**：可從「Quality + Decisions」雙重角度解讀 AI 退化問題。
- **[Boris Cherny × Opus 4.7 心得](boris-cherny-opus-4-7.md)**：實戰技巧版，與本文的抽象定律互為樓上樓下。
- **[Andrej Karpathy Skills](andrej-karpathy-skills.md)**：可結合多條定律做成「AI 評論員」skill，每次 review code 時 LLM 自動引用最相關定律。
- **[Casper Claude Skill Design Gallery](casper-claude-skill-design-gallery.md)**：把這 56 條做成 skill 是高 ROI 的小專案。
