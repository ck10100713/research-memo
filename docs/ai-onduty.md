---
date: "2026-11-10"
category: "學習資源"
card_icon: "material-clock-alert-outline"
oneliner: "繁中策展影片課，主題是排程與 CI/CD：GitHub Actions、Cloudflare Cron Triggers、把 Claude Code 放進 CI。13 章 49 單元 201 支影片，每個單元對照 2026 官方文件標時效（49 單元查 29 個，17 個已飄移），repo 本身用週排程驗連結、死了自動開 issue"
tags:
  - course
  - github-actions
  - cloudflare-workers
  - claude-code
  - ci-cd
---

# AI On-Duty（AI 自動化工作流：困難部分）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [htlin222/ai-onduty](https://github.com/htlin222/ai-onduty) |
| 線上課程 | [ai-onduty.pages.dev](https://ai-onduty.pages.dev) |
| 框架來源 | [htlin222/curate-course](https://github.com/htlin222/curate-course) |

| 指標 | 數值 |
|------|------|
| Stars | 0（2026-11-10） |
| 建立 | 2026-08-06，最後 push 2026-09-09 |
| License | 程式碼 MIT（LICENSE 署名還是舊專案 `body-course contributors`），影片版權屬原頻道 |
| 技術 | 建置用 Python 標準函式庫（uv 跑），前端原生 HTML/CSS/JS，部署到 Cloudflare Pages |
| 規模 | build/audit 腳本約 2,000 行 Python，前端 JS 約 2,800 行，課程內容全在 `course/data/*.json` |

## 它是什麼

一門免費的**策展影片課**，課程本身不拍影片，是幫每個單元從 YouTube 挑一支主課加幾支延伸影片，再自己寫驗收標準和時效查核。主題是「讓自動化在你不在的時候還能準時跑、有權限、壞了會來找你」。

| 區塊 | 章節 |
|------|------|
| 地基 | CH0 使用說明、CH1 無人值守的心智模型、CH2 Git 最小必要 |
| GitHub Actions | CH3 入門、CH4 CI、CH5 CD 與審核閘門、CH6 排程的真相 |
| Cloudflare Workers | CH7 入門、CH8 Cron Triggers、CH9 有狀態的排程 |
| Claude Code 與生產化 | CH10 放進 CI、CH11 排程能力、CH12 安全、成本與觀測 |

## 值得學的地方

### 1. 每個單元的資料結構

看 `course/data/ch8.json` 一個單元長這樣：

| 欄位 | 內容 |
|------|------|
| `assessment` | 一段可操作的驗收標準，例如「deploy 後不要打它，只開 `wrangler tail` 等三分鐘，應該看到三筆日誌，而且 fetch handler 一次都沒被呼叫」 |
| `tight` | 常見誤解清單（「以為 scheduled handler 也拿得到 Request」） |
| `weak` | 學完應該會的能力清單 |
| `lesson` | 主課影片：標題、頻道、長度、`why`（為什麼挑這支） |
| `drills` | 延伸影片 |

`audit.py` 的 `audit_depth()` 會檢查 `assessment` 字數，太短直接讓建置失敗。等於把「每單元都要有能自己跑的驗收」寫成 CI 規則，不靠作者自律。

### 2. 時效查核是一等公民

`evidence-*.json` 每個單元標四級之一：現行有效、已飄移、已淘汰（照做會壞）、無官方依據。每條附官方文件網址和查核摘要。README 說 29 個查過的單元裡 17 個已經飄移，例如 `actions/checkout@v2`、`::set-output`、`wrangler publish`、`claude-code-action@beta`。

查核摘要寫得很老實。例如 Cloudflare 那份會指出官方從沒說過「0ms 冷啟動」，Cron Triggers 文件也沒承諾恰好執行一次，「查不到就是查不到」。

### 3. 引用網址真的會被打開驗證

`verify_refs.py` 原本（來自 curate-course 框架，原用途是醫學課）只驗 PMID 和 DOI。作者加了第三種：純網址，`make verify` 會逐一 GET，捏造的文件連結會 404。對 LLM 輔助寫課程的情境很實用，因為 agent 最容易編的就是「看起來合理的官方文件網址」。

### 4. Video ID 只能來自搜尋結果

`docs/VIDEO_SPEC.md` 是寫給策展 agent 看的規格，最重要一條：**11 字元的 video ID 沒有冗餘，憑印象拼的一定是錯的**。所以：

- `tools/yt_search.py`：直接抓 YouTube 搜尋頁的 `ytInitialData`（不用 API key），回傳 ID、長度、觀看數、頻道
- `--check` 走 oEmbed 驗證，200 才算活著；作者實測有搜得到但 oEmbed 回 401 的影片
- 頻道分級白名單（官方 > 實務創作者 > 研討會），長度、觀看數門檻，放寬時必須在 `why` 寫原因
- 找不到合格影片就留空，寫明查過哪些關鍵字。目前有 2 格空著（DO Alarms、cron 呼叫 CLI agent）

這套「工具強制 ID 來源 + 驗證 + 允許誠實留空」的模式，可以直接拿去管任何 agent 產出的外部連結。

### 5. Repo 自己用課程教的東西

| workflow | 做什麼 | 對應章節 |
|----------|--------|----------|
| `audit.yml` | push/PR 跑離線稽核（不打網路，結果可重現） | CH4 |
| `deploy.yml` | 先 audit 才部署；綁 `environment: production` 可加人工審核；沒設 Cloudflare secret 就略過部署而不是紅燈 | CH5 |
| `verify-links.yml` | 每週一 `17 3 * * 1` 重打 oEmbed，失敗就用 `github-script` 開 issue | CH6、CH12 |

細節很到位：cron 刻意寫 17 分避開整點尖峰；留 `workflow_dispatch` 當逃生門，因為公開 repo 60 天沒活動排程會被 GitHub 停用；離線稽核和連線驗證拆成兩個 workflow，前者確定性、後者排程。deploy 的註解寫「一個永遠是紅的 CI，跟沒有 CI 一樣」，是很實在的考量。

### 6. 0 元 paywall 實驗

`docs/PAYWALL.md`：CH3 之後顯示鎖頭，走一個完整的購物車 → 結帳 → 收據流程，金額 NT$0，解鎖狀態存 `localStorage`。目的是測「解鎖」這個動作會不會讓人更願意開始上課，順便先把真收費的接縫留好：

- 所有 UI 只問 `paywall.ready()` 和 `paywall.canAccess()`，換真金流只改這兩個
- `ready()` 第一天就是 async，避免日後同步改非同步的大重構
- 文件自己承認前端鎖擋不住人，`dist/course.json` 把所有影片 URL 都攤開，真要收費得切資料、加伺服器端 entitlement（Pages Functions + D1）

## 課程立場（值得一讀的四條）

- GitHub Actions `schedule` 是盡力而為：會延遲，高負載可能被丟棄，公開 repo 60 天沒活動自動停用
- Cloudflare Cron Triggers 比較準，但官方沒承諾恰好一次；免費方案每次觸發只有 10ms CPU
- 把 agent 放進 CI，難的是權限邊界和提示注入，排程本身不難
- 無人值守的真正成本在壞掉時沒人知道（作者自己標成「無官方依據」，是主張不是結論）

## 限制

- 時效查核日期是 2026-08-06，repo 9 月後沒更新，現在看要自己再驗一次
- 內容幾乎都是英文影片，繁中只有架構、驗收標準和查核摘要
- 0 stars、單人專案，`verify-links` 能不能持續跑要看 repo 有沒有人維護
- LICENSE 署名沒改，沿用框架的 `body-course contributors`

## 對我們的用處

- 想學 GitHub Actions 排程、Cloudflare Cron、Claude Code 進 CI：直接照 CH6、CH8、CH10–12 的驗收標準做，比看影片本身有用
- 讓 agent 產出含外部連結的內容時，可以借「ID 只能來自工具輸出 + oEmbed/HTTP 驗證 + 允許留空」這套
- 「離線稽核進 CI、連線驗證走排程、失敗自動開 issue」可以套到 research-memo 自己的連結健康檢查
