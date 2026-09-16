---
date: "2026-09-16"
category: "學習資源"
card_icon: "material-book-multiple"
oneliner: "金門大學資工系陳鍾誠教授 115 學年上學期《現代軟體工程》課程 repo（MIT、30★）裡藏的 `_more/mybook`——三本各自寫完整的繁體中文技術書草稿，共 216 個分節 Markdown、約 198K 漢字、256 個 mermaid 圖：《現代軟體工程：從基礎到 AI Agent 實踐》（87 節，三篇 14 章 + 附錄 ABC，明講參考李博杰 agent-book）、《演進式架構實戰》（75 節，用淘寶 14 次架構演進當問題驅動主線）、《從 Docker 到 Kubernetes：Rust × WebSocket/SSR/MPA 實戰》（46 節）。每節一檔、靠 README 當目錄，本筆記附上把它們合併成單一本書的方法與腳本"
tags:
  - learning
  - software-engineering
  - kubernetes
  - system-design
  - agent-framework
---

# ccc115a/se `_more/mybook` 三本書 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★30 / 12 forks / MIT） | [github.com/ccc115a/se](https://github.com/ccc115a/se) |
| 本筆記主角目錄 | [`_more/mybook`](https://github.com/ccc115a/se/tree/main/_more/mybook) |
| 作者 | **陳鍾誠** — [金門大學資訊工程學系](https://www.nqu.edu.tw/educsie/index.php) 教師 |
| 課程 | 現代軟體工程，115 學年上學期 |
| 課程正課教材 | repo 根目錄 `01-overview` ～ `06-engineering`、`大綱.md`、`教材.md` |

> **Metadata（2026-09-16 即時抓取）：** 建立於 **2026-08-27**，最後 push **2026-09-16**（開學中、每天都在動）· MIT License · 預設分支 `main` · repo size 約 33 MB · **30 stars / 12 forks**。`_more/mybook` 本身 1.4 MB，**216 個分節 Markdown**，合計約 **198K 漢字**、**256 個 mermaid 圖**、**1,676 行表格**。

!!! warning "四個要先講清楚的判讀"
    - **這三本是「書稿」，不是課本定稿，也不是課程正課內容。** 它們放在 `_more/`（額外資料）底下，正課教材是 repo 根目錄的 `01-overview` ～ `06-engineering`。把它當成老師備課時生出來的延伸讀物比較準確。
    - **明顯是 AI 協作寫出來的。** `現代軟體工程/outline.md` 裡直接留著「待決定事項」的未勾選 checkbox（模型後訓練講多深、要不要中英夾雜、哪幾章必讀），章節對照表也直接寫「主要參考：agent-book Ch2 / Ch4」。這不是缺點，但讀的時候要知道它沒經過出版社編審。
    - **淘寶那本的資料夾名字跟書名不一樣。** 資料夾叫「向淘寶學習網站架構演進」，書名是《演進式架構實戰：從單體、微服務到 Docker、Kubernetes 與 AI 雲原生轉型》，而且 README 自己就標明「以淘寶架構演變簡史為主線（**教學模型，非淘寶真實路徑**）」。引用時別當成阿里官方史料。
    - **沒有 build 腳本。** 三本書都是「一節一個 `.md` + 一個 README 當目錄」，repo 裡沒有任何工具把它們組成一本。要整本讀就得自己合併，本筆記最後附了做法。

## 專案概述

`ccc115a/se` 是陳鍾誠老師 115 學年上學期「現代軟體工程」的課程 repo。課程主線很清楚——傳統軟體工程（瀑布／螺旋／敏捷、人月神話、結構化與物件導向分析）接上 AI 寫碼時代（OpenCode、Hermes Agent、Claude Academy 的「AI 四大特性」）。`教材.md` 的參考清單裡也直接列了李博杰的[《深入理解 AI Agent》](ai-agent-book.md)。

真正有份量的東西在 `_more/mybook`：**三本互不相干、但各自都寫到「可以直接印出來上課」程度的繁中技術書**。

| 書 | 節數 | 漢字 | mermaid | 定位 |
|---|---|---|---|---|
| 《現代軟體工程：從基礎到 AI Agent 實踐》 | 87 | 123K | 74 | 資工系大學部教科書 |
| 《演進式架構實戰》（淘寶線） | 75 | 51K | 123 | 問題驅動的架構演進課 |
| 《從 Docker 到 Kubernetes：Rust × WebSocket/SSR/MPA 實戰》 | 46 | 24K | 59 | 進階實戰手冊 |

## 第一本：《現代軟體工程：從基礎到 AI Agent 實踐》

87 節、123K 漢字，是三本裡最厚的一本，也是唯一有完整寫作方針文件（`outline.md`）的。

### 結構

**三篇 14 章 + 三個附錄**：

- **第一篇 軟體工程基礎（Ch 1-6）**：本質／需求／設計／實作／測試／維運。骨架是傳統 SDLC，但每章都硬塞一個 AI 融合點——例如 Ch2 收「Red Teaming Prompting」與 Spec-Driven Development，Ch5 收「LLM-as-a-Judge」。
- **第二篇 AI 工程基礎（Ch 7-10）**：提示 → 上下文工程、工具與 Agent 架構（ACI／五類工具／MCP／ReAct）、**Harness 工程**、評估與持續進化。這篇的章節對照表直接註明取材自 agent-book。
- **第三篇 主題式深入（Ch 11-14）**：複雜系統架構（事件驅動、即時互動、多 Agent 拓撲）、團隊協作、安全與倫理（提示注入、工具權限）、前沿展望。
- **附錄 A（6 節）**：Git 與 GitHub 實務，從 `init` 講到 `bisect`。
- **附錄 B（7 節）**：OpenCode 與 AI 輔助開發——`AGENTS.md`、權限控制、MCP Servers、Skills，最後一節是實戰小專案。
- **附錄 C（7 節）**：案例集，含軟體缺陷與安全關鍵系統、架構演進與技術債、網站營運失敗案例。

### 它的四個核心主張

`outline.md` 把立場寫得很直白：

1. AI 沒有改變軟體工程的本質——需求模糊性、系統複雜性、品質驗證仍是**本質性困難**。
2. AI 大幅降低了**附屬性困難**——樣板碼、基礎測試、文件生成被自動化。
3. 工程師的角色從「建築工」變成「指揮官與架構師」。
4. 「沒有度量就沒有改進」在 AI 時代更重要。

這是 Brooks《人月神話》essential/accidental complexity 那組概念直接搬過來當全書骨架。

### 寫作品質抽樣

抽 1.1「什麼是軟體工程」來看，開場是餐廳訂位系統的滾雪球式需求擴張，接一張「程式設計 vs 軟體工程」五列對照表，然後刻意打掉自己剛畫的界線：

> 教科書式的區分很容易，但實務上的界線其實是模糊而且漸進的……本書要傳達的不是「你現在在寫程式，等你夠資深才叫軟體工程」這種傲慢的二分法。

這種「先給框架、再自己拆框架」的寫法在 AI 生成的教材裡不常見，讀起來不像模板。

## 第二本：《演進式架構實戰》（淘寶線）

75 節、51K 漢字，但 **123 個 mermaid 圖**——圖密度是三本最高的。

方法論寫在 README 第一行：**問題驅動（Problem-Driven）**——不先拋 Docker / K8s 概念，而是重現從 100 併發到千萬級併發的 14 次架構演進，讓讀者在堆疊的運維痛點裡自然長出「這裡非用容器與編排不可」的需求。

路線大致是：單機 Tomcat + DB → Web/DB 分離 → 快取（Memcached/Redis/Tair，含穿透／擊穿／雪崩／熱點失效四種痛點）→ 反向代理與無狀態化 → LVS/F5 + Keepalived 四七層搭配 → 讀寫分離與分庫分表 → …… → 一路接到 Serverless、FinOps 與 AI 雲原生。

附錄 B 有兩個滿實用的東西：B.1 是「淘寶 14 次演進 vs 本書章節對照表」，B.4 是「如何用本書上課」的教學指引。B.3 收了 2025-2026 的新名詞表（AI 原生 / AgentRun / FunctionAI / MCP / A2A / AI Serving Stack）。

`ref.md` 只有兩行：一個 Gemini 對話連結、一篇 CSDN 部落格。來源就這樣，心裡有數。

## 第三本：《從 Docker 到 Kubernetes：Rust × WebSocket/SSR/MPA 實戰》

46 節、24K 漢字，四個部分 + 序言。這本的切入角度在中文 K8s 教材裡算少見。

序言把動機講得很清楚：

> REST + SPA 的教程很多，但真實世界不是只有按鈕調 API：聊天室要 WebSocket 長連線、官網要 SEO 要 SSR，後台要 MPA 簡單好維護。

所以全書用 **Rust（Axum）當後端主線**，前端同時帶 WebSocket、SSR、MPA、SPA 四種形態一起上 K8s。重點章節：

- **Ch2**：Rust 容器化——多階段構建到 Alpine/Distroless、musl 靜態編譯壓進 20 MB 以內、cargo-chef 三段式 Dockerfile 加速 CI。
- **Ch5-7**：長連線的雲原生改造——WS 狀態抽離與跨 Pod 廣播、Sticky Sessions、SIGTERM 優雅停機、「別讓長連線害死你的 Pod」的健康檢查設計。
- **Ch10-11**：Ingress 超時與 WebSocket 支援（自己標成「核心節」）、**基於 active 連線數的 Custom Metrics HPA**、Rolling Update 的長連線平滑遷移。
- **Ch14**：在 K8s 上部署 vLLM，前端 + Rust Gateway SSE 串流 + LLM Pod。

序言還給了三條讀法（前端／後端／SRE 路線）跟四種閱讀順序表，這個設計很務實。

## 怎麼把它組成一本書

三本書都是「一節一個 `.md`」，GitHub 上只能一節一節點。要整本讀（或丟給 LLM、轉 PDF）就得合併。

關鍵在**順序不能靠檔名排**——檔名是 `1.1.md`、`10.1.md`、`A.1.md`、`B.3.md`，字典序會把 `10.1` 排到 `2.1` 前面，附錄也會亂掉。**正確的順序來源是每本的 `README.md`**，它本身就是一份帶連結的完整目錄：

```markdown
## 第一篇：軟體工程基礎

- 一、軟體工程的本質
   - [1.1 什麼是軟體工程](1.1.md)
```

所以合併規則很簡單：照 README 由上到下走，`## 篇` 變 H1、`- 章` 變 H2、`- [節](x.y.md)` 換成該檔內容並把標題降兩級（原本的 `#` 變 `###`）。

```python
def demote(txt: str) -> str:
    """標題降兩級，但跳過 fenced code block。"""
    out, fence = [], False
    for l in txt.splitlines():
        if l.lstrip().startswith(('```', '~~~')):
            fence = not fence
        elif not fence:
            l = re.sub(r'^(#{1,4}) ', r'\1## ', l)
        out.append(l)
    return '\n'.join(out)
```

!!! danger "這裡有個一定會踩的坑"
    **不能直接對整個檔案做正規表示式降級。** docker2k8s 那本的 shell 範例裡全是 `# 1. 觀察宿主的行程` 這種註解，一律降級會把程式碼區塊裡的註解改成 `### 1. 觀察宿主的行程`，範例就毀了。必須追蹤 ` ``` ` 圍籬，只降圍籬外的標題。第一版沒處理，三本書一共壞掉 3 行。

另外 README 目錄裡的 `[1.1 什麼是軟體工程](1.1.md)` 連結在合併後全部失效，要拆成純文字（或改成錨點）。

合併後的規模：

| 產出 | 行數 | 大小 |
|---|---|---|
| `現代軟體工程.md` | 10,000 | 533 KB |
| `向淘寶學習網站架構演進.md` | 7,544 | 300 KB |
| `docker2k8s.md` | 5,334 | 206 KB |

驗證方式：合併後的 `###` 數量要等於原始節檔數（87 / 75 / 47），而且 ` ``` ` 的行數必須是偶數（圍籬成對）。

## 授權與可用性

MIT License，整個 repo（含三本書稿）都可自由使用、修改、再散布，只要保留版權聲明。對「拿來當自己課程教材」或「改寫成內部讀物」來說沒有障礙。

不過三本書都沒有 LICENSE 以外的引用聲明，`ref.md` 只有兩條連結，所以**引用書中的具體數據（例如淘寶的併發量級）前要自己查證**。

## 值得借鑑的地方

- **「一節一檔 + README 當目錄」是很輕的書籍工程。** 不用 mdBook、不用 GitBook、不用 SUMMARY.md 格式，README 本身就是人讀的目錄也是機器可解析的目次。代價是沒有現成的 build。
- **問題驅動的教學順序**（淘寶那本）比概念驅動好用——先讓讀者痛，再給工具。
- **把 AI 融合點掛在傳統 SDLC 骨架上**，而不是另外開一本 AI 課，這個結構決定讓第一本書不會變成「兩本書釘在一起」。

## 限制

- 沒有配套程式碼倉庫，實驗都是書裡的片段。
- 三本書沒有交叉引用，主題有重疊（Docker/K8s 在兩本書都出現）。
- `outline.md` 的待決事項還沒決，代表書稿本身還在調整期，現在的版本可能會變。
- 更新極快（每天 push），本筆記的節數與字數是 2026-09-16 的快照。

## 相關筆記

- [《深入理解 AI Agent》(ai-agent-book)](ai-agent-book.md) — 第一本書第二篇明確標示的主要參考來源
- [System Design Primer](system-design-primer.md) — 跟淘寶那本的架構演進主題重疊
- [HighScalability](highscalability.md) — 真實世界的架構案例來源
