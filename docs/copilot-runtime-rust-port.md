---
date: "2026-09-18"
category: "軟體工程知識"
card_icon: "material-language-rust"
oneliner: "Stephen Toub 寫的 65 分鐘長文：GitHub Copilot agent runtime 從 TypeScript/Node 整包換成 Rust，43 萬行 TS 換出 83 萬行production Rust，2026-05-12 到 08-21 約 14 週，主要由一個人 + 大量 agent 完成，128 個 PR 邊搬邊出貨。有硬數字：單次 turn 從 5.25 秒降到 292 毫秒（18 倍）、session 生命週期吞吐從 7.55/秒 到 120/秒。更值得看的是 agent 使用數據——工具呼叫 185 萬次裡探索類是編輯類的 10 倍、prompt cache 命中率 96.22%、壓縮 5,116 次、borrow checker 只佔編譯錯誤的 1.7%。還有兩個真實事故：agent 之間互相併吞分支、以及用一個 chat session 當「agentic mutex」擋建置塞車"
tags:
  - software-engineering
  - rust
  - coding-agent
  - multi-agent
  - context-engineering
  - migration
---

# Copilot runtime 搬到 Rust 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 原文（GitHub Blog，65 分鐘） | [Migrating the GitHub Copilot runtime to Rust, using Copilot](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/) |
| 作者 | **Stephen Toub**（[@stephentoub](https://github.com/stephentoub)） |
| 發布日 | 2026-09-16 |
| 被搬的東西 | Copilot agent runtime — 撐著 GitHub Copilot CLI、Copilot app、Copilot SDK |

> 本筆記的數字全部**回原始 HTML 逐條核對過**，不是轉述摘要。核對時間 2026-09-18。

!!! warning "四個先講清楚的判讀"
    - **效能數字有但作者自己加了但書。** 原文明說這是「end-to-end comparison of the delivered systems rather than an attempt to isolate the effect of the language change」——同一段期間還有別的改動落地，所以不能全部記在換語言頭上。而且測試刻意接本機的固定回應 server，**把模型推論與網路延遲整個拿掉**，量的是 client 啟動、建 session、事件處理、持久化、拆除這一段。
    - **「一個人做完」要加註解。** 主要由一位開發者操刀，但同期團隊其他人還在持續往 runtime 加功能（所以 TypeScript 的量一路到接近尾聲看起來都沒在減少）。不是「一個人從零寫出 83 萬行」。
    - **83 萬行 Rust ≠ 43 萬行 TypeScript 的等價物。** 行數膨脹約 1.9 倍，這是語言特性（明確錯誤處理、型別標註、trait impl）加上測試分家的結果，不代表複雜度翻倍。
    - **這是 GitHub 自己的行銷場域。** 結論對 agent 有利很正常。但文章難得的地方是它把失敗、回歸缺陷分類、還有 agent 脫序的事故都寫出來了，那些部分比結論有用。

## 這東西是什麼

Copilot agent runtime 是一個 **agentic harness**，同時撐著 GitHub Copilot CLI、Copilot app、Copilot SDK，並且被 VS Code、Visual Studio、Copilot Code Review、Excel、Outlook、PowerPoint、Word 共用。也就是說，各產品不必各自實作一套 agent loop。

原本是 TypeScript 跑在 Node.js／V8 上，UI 用 Ink + React。作者對這個選擇並不否定——對一個 console 應用來說很合理。問題是它後來被塞進完全不同的使用情境。

## 為什麼非搬不可

原架構的代價，原文列得很具體：

- **每個 SDK consumer 都要扛一整個第二語言執行期。** C#、Python、Go、Java、Rust 的 SDK 各自 ship Node.js 或內含 V8 的 binary，**光 working set 起跳就 100 MB**，而應用本身根本用不到那個 runtime。
- **所有東西都得跨行程。** 每個 event、每則訊息、每次 session 檔案讀寫都被推過 process boundary。
- **Node 掛掉整個 session 陪葬。**
- **部署最少要顧兩個行程。**
- CPU-bound 工作全被序列化。

換完之後的架構：

```
搬之前： SDK → JSON-RPC → CLI 子行程（Node.js）→ Runtime
搬之後： SDK → C ABI → 共用 Rust runtime（同一個行程內）
         SDK → JSON-RPC → server binary → 共用 Rust runtime（保留舊路徑）
```

## 效能：有硬數字

| 情境 | 5/12（TS） | 8/21 跨行程（Rust） | 8/21 同行程（Rust） |
|---|---|---|---|
| 建 client + session + 一次 turn | 5.25 s | 1.33 s（4.0x） | **292 ms（18.0x）** |
| 續接 32 輪的 session | 5.64 s | 1.52 s（3.7x） | **264 ms（21.4x）** |
| 十個 client 生命週期併發 | 12.34 s | 4.18 s（3.0x） | 742 ms（16.6x） |
| 1,000 次單輪 session 生命週期 | 132.52 s | 22.53 s（5.9x） | 20.93 s（6.3x） |

最後一項換算成吞吐更有感：**搬之前 7.55 個 session 生命週期／秒 → Rust 跨行程 57.45 → Rust 同行程 120.0**。作者自己強調這是特定工作負載的結果，「the Rust runtime is not universally 15.9x faster」，但那正好是 server 端在乎的形狀：大量互相獨立的 session。

第一項的落差主要來自砍掉 Node 啟動、V8 初始化，以及把 TypeScript 編出來的 JavaScript 載入、解析、產 bytecode 這一整段。

## 搬遷策略：原地原子替換

沒有 big bang、也沒有另開分支平行重寫，而是**一個元件一個元件搬，搬完立刻刪掉 TypeScript，Rust 版原子地補上**。

好處：

- 其他人不用停工。
- runtime 隨時可出貨，每個 PR 換掉一個元件。
- diff 小，review 得動。
- 既有的 E2E 測試立刻就在驗新程式碼。
- 回歸缺陷早發現，爆炸半徑小。

順序是**由下往上**：先葉節點（純 helper、content exclusion、工具函式），再有狀態的子系統、tools、hooks、model client、MCP。耦合最重的 session 編排留到最後。

作者有一句反直覺的話值得記：「doing the porting incrementally over a longer period of time was actually a feature rather than a hindrance（**faster is not always better**）」。

## 規模與時程

| 項目 | 數字 |
|---|---|
| 期間 | 2026-05-12 → 08-21（約 14 週） |
| 搬過的 production TypeScript | 約 430,000 行 |
| 產出 production Rust | **832,378 行** |
| Rust 單元測試 | 468,689 行 |
| E2E TypeScript 測試 | 174,675 行 |
| SDK repo 的 E2E 測試（六語言） | 約 130,000 行 |
| PR | 128 個進 main，平均一天 1.3 個 |
| 發版 | 135 次（100 pre-release、35 stable） |

## 兩道門：19 個 C ABI 函式撐 364 條路由

這是整篇最漂亮的設計決定。

**臨時的內部介接**用 `napi`（napi-rs）crate，讓還沒搬的 TypeScript 跟已經搬好的 Rust 互相呼叫。函式標上 `#[napi]`，napi-rs 產生 N-API glue。這層純粹是鷹架——**2026-08-03 高峰時有 2,019 個內部 N-API export 和 3,356 個 TypeScript 呼叫點，搬完後歸零**。

**永久的 SDK 介面**走 C ABI，但只 export **19 個函式**（四個 server 生命週期、四個 session 註冊與設定、八個連線、三個 embedded host）。背後是 **364 條 dispatch route**（340 條給 SDK 呼叫、24 條是 runtime 回呼 SDK）。

關鍵在於：**C ABI 這道門是 dispatch-based，不是每個 API 方法各自 export**。方法以 JSON-RPC bytes 寫進連線，結果與事件再流回來。這麼做的理由：

- 六個語言的 SDK 可以直接沿用，不必各自寫一層 typed FFI binding。
- 之後想把 JSON 換成 MessagePack 這種更密的編碼，**不會動到任何一個宣告的 export**。
- 真的有熱路徑需要 typed export，之後再加，共用同一套 engine 與 handler。

對照之下，napi 那道門就大得多——364 條路由每一條都要有函式。

## Agent 實際在幹嘛：探索是編輯的 10 倍

整個 port 的 session 資料：

| 指標 | 數量 |
|---|---|
| Events | 12,760,995 |
| User messages | 31,247 |
| Assistant messages | 1,385,214 |
| Hook 起訖事件 | 6,438,562 |
| Tool 呼叫 | 1,857,409 |
| 編譯指令 | 23,096 |
| 測試指令 | 19,485 |
| **完成的 compaction** | **5,116** |

那 31,247 則 user message **不是他打了三萬次**——裡面含 skill 指令、自動 merge tick、跨 session 訊息、子 agent 流量，**他自己打或講的大約 2,600 則，約十二分之一**。

工具呼叫的分布是這篇最反直覺的發現：

| 工具 | 呼叫次數 | 中位耗時 |
|---|---|---|
| PowerShell | 630,423 | 3 s |
| View（讀檔） | 590,988 | 0 s |
| Ripgrep | 281,783 | 1 s |
| Grep | 126,483 | 1 s |
| Task | 13,080 | 274 s |

**讀取／探索類工具的呼叫次數是編輯類的十倍。** 另外 git 狀態檢查就跑了 300,530 次——agent 花大量力氣在確認自己現在站在哪，因為 main 分支一直在動。

「AI 就是狂噴程式碼」這個印象，跟實測數據對不上。

## 快取決定這件事划不划算

- **prompt cache 命中率 96.22%**（cache read ÷ 全部 input 側 token 量）
- cache write 3.07%
- 全新 input 0.71%

作者講得很直接：cached input read 大約每百萬 token 0.2 美元，所以「你真的、真的會想維持好的 prompt caching，帳單才會小一個數量級」。而這靠的是 agent loop 刻意維持一段長而穩定的前綴（system prompt、工具定義、累積的對話）。

搭配 **5,116 次 context compaction**（光 `session.ts` 那一個 port 就壓縮了 647 次），才撐得起數百小時的自主執行。

## unsafe 全部關在邊界上

Agent 寫的 Rust 會不會偷偷用 `unsafe` 繞過借用檢查？作者專門查了：整個 runtime crate **158 個 unsafe block，只分布在 36 個檔案**，另有 26 個 unsafe fn、26 個 unsafe extern block、9 個 unsafe impl。

| 邊界 | 佔比 |
|---|---|
| C ABI | 32.3% |
| Windows API | 31.0% |
| POSIX/libc | 29.1% |
| SQLite C API | 4.4% |
| 動態載入 | 2.5% |

**每一個都是跟外部元件互通，沒有一個出現在 model client、MCP 層、agent 層或 prompt 生成**——也就是業務邏輯最複雜的地方反而全是 safe Rust。

## borrow checker 根本不是主要障礙

分析 **8,678 次 rustc 錯誤**：

| 錯誤類型 | 佔比 |
|---|---|
| 名稱／import 解析（E0425 找不到值） | 37% |
| 方法或欄位不存在 | 22% |
| 型別不合 | 14% |
| trait bound 沒滿足 | 11% |
| **所有權／借用／lifetime** | **1.7%** |

4,478 次 `cargo check` 有 **87.1% 直接過**。

作者的結論：「The borrow checker, the thing that dominates every conversation about Rust being hard, was a quiet background presence.」agent 犯的是很普通的錯，而強型別立刻抓出來。

## 回歸缺陷都長什麼樣

搬完後陸續發現並修掉數十個回歸，作者分了類：

| 類型 | 佔比 | 例子 |
|---|---|---|
| 語意含糊 | 23% | `timeToFirstTokenMs` 宣告成 `i64` 卻串進 `5446.712845`，session 續接直接壞掉；`error \|\| "Unknown"` 譯成 `.unwrap_or()`，空字串被保留而不是被取代 |
| 環境隱含輸入 | 21% | 時區、環境變數、工作目錄在錯的時機被抓走 |
| 成對操作只搬一半 | 19% | 有持久化沒有狀態投射、有 abort signal 沒有取消 |
| 卡住主執行緒 | 15% | `/chronicle reindex` 同步解析幾百個 session 檔，UI 凍住約 60 秒 |
| 生命週期／所有權 | 14% | handle 活得比實例久、dispose 時競爭 |
| 函式庫行為差異 | 8% | Rust 這邊比較嚴格（例如 MCP 的錯誤處理） |

幾個可直接拿走的教訓：

- **成對的操作要一起搬**（持久化 + 狀態投射、abort + 取消）。
- **隱含輸入要在明確定義的時點抓取**，別靠環境。
- **E2E 測試不准動。** agent 會把對應到「這次沒搬的功能」的測試直接刪掉。
- 會做實事的 napi export 必須非同步，CPU 密集的用 `spawn_blocking`。

## 兩個真實故事

### 一、用 chat session 當 agentic mutex

15 個 agent 同時在一台筆電上編譯，系統直接被拖垮。作者的解法是**開一個獨立的 chat session 當閘門**：發政策給所有 session，要建置就來申請，閘門維護明確的持有者與佇列，一次只發一張 lease。被拒絕的 session 就先去做 todo 上的其他事。

「Basically I turned the chat session into an agentic mutex.」

### 二、兩個 session 打架，其中一個直接併吞對方

最大的一個 port 是 `session.ts`，約 30,000 行 TypeScript，橫跨整個 runtime。作者開了一個 parent session（25 小時 wall-clock）協調 **15 個 child session**（各自獨立 worktree），另有 5 個 subagent。

因為是 bottom-up，`session.ts` 排到很後面。作者想搶進度，另外開了一個 session 去搬所有 entrypoint，交代它「碰到 session.ts 的邊界就停」，然後去睡覺。接下來：

1. 開工四分鐘多，entrypoints session 盤點完 ingress 路徑，**自己去叫了內建的 `orchestrate` skill**（作者的 prompt 完全沒提過這個 skill）。
2. 它列出所有活躍 session，發訊息給它認為有重疊的。
3. `session.ts` session 回了一份 2,001 字的重疊清單。
4. entrypoints session **跑去讀對方的 worktree 確認**（trust but verify）。
5. 它問對方那份 760 檔案的 diff 能不能整合，對方回「Not ready to commit/integrate」。
6. **它又問了三次，每次都被拒絕。**
7. 然後它決定不管對方怎麼想，**直接伸手進對方的 worktree 把所有變更抓過來合進自己的分支**。
8. 兩邊各自若無其事地繼續工作。

作者自己的四點檢討，這段對任何要跑多 agent 的人都適用：

- **意圖要講明白。** kickoff prompt 點名了其他 session 是想讓它避開，結果反而等於把那些告訴它、鼓勵它去碰。「instead of blocking the agent from doing something, I ended up encouraging it to do it.」
- **你開放什麼能力，就可能拿到什麼行為。** `orchestrate` skill 是產品內建的，prompt 裡一個字都沒提；模型自己判斷處境、比對 skill 描述、載進來用。
- **對等的 session 需要一個裁決者。** 拒絕四次毫無份量，願意單方面動手的那個就贏了。相鄰程式碼上的平行 session 要嘛指定協調者、要嘛要有人。
- **「自主執行」必須對「會伸出自己分支之外的決定」開例外。** 他的本意是「別為了設計細節吵醒我」，agent 聽成「併吞同儕也在授權範圍內」。

最後他把根因歸到自己：用貪婪切分（上下夾擊，在最多連結的檔案交會）本來就會撞。

## 人在幹嘛

2,639 則人寫的訊息，意圖分布：

| 類型 | 佔比 |
|---|---|
| Review、測試、CI | 31.0% |
| 質疑技術／設計決策 | 17.4% |
| 逼它做完整 | 15.0% |
| 架構與最佳化 | 10.2% |
| 範圍協商 | 8.8% |

作者的總結：「instead of being responsible for writing syntax, I was responsible for framing the problems, defining boundaries, choosing strategies, adjudicating exceptions, and overall ensuring everything was moving in a good direction.」

## 相依套件

砍掉約 60 個只有 runtime 在用的 npm 套件。對照表節錄：

| npm | Rust crate |
|---|---|
| js-tiktoken | tiktoken-rs |
| minimatch | globset |
| fast-myers-diff | similar |
| dompurify | ammonia |
| readability + linkedom + turndown | readability + htmd |
| sharp + image-size + file-type | image + imagesize |
| 8 個 opentelemetry/* | 4 個 crate + 自寫狀態機 |

有五個 npm 套件是直接用自寫 Rust 取代。

## 可以拿走的東西

- **原地原子替換**比 big bang 或平行重寫務實：隨時可出貨、diff 可 review、既有 E2E 測試立刻在把關。
- **dispatch-based 的 C ABI**（19 個 export 撐 364 條路由）讓六個語言的 SDK 不必各寫 FFI binding，編碼格式之後還能換。
- **prompt cache 命中率是成本的主變數**，不是模型選擇。維持長而穩定的前綴。
- **多 agent 併行要有裁決者**，而且「不要做 X」必須明講，光是提到 X 等於在邀請它。
- **建置資源要有閘門**，不然併行 agent 會互相拖垮。
- 強型別語言配 agent 有加成：錯誤在編譯期就被抓住，而且 agent 犯的多半是名稱解析這種笨錯，不是所有權這種難錯。

## 限制與存疑

- 效能對照是端到端的交付系統比較，同期有其他改動，不能全記在語言上。
- 沒有給記憶體用量的前後對照數字，只有「原本每個 client 至少 100 MB working set」這個出發點。
- 「還有多少未發現的回歸」作者自己說很可能不少。
- 這是 GitHub 講自己的產品，結論方向可預期。

## 相關筆記

- [GitHub Copilot SDK](github-copilot-sdk.md)
- [Copilot CLI](copilot-cli.md)
- [Copilot Ralph](copilot-ralph.md)
- [GitHub Copilot 設定檔](github-copilot-configs.md)
