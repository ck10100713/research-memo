---
date: "2026-11-05"
category: "AI 應用"
card_icon: "material-file-check-outline"
oneliner: "黑客松作品：拿 Meta muse-wonder-1.0 逐句審稿，每句判 SUPPORTED / CONTRADICTED / NOT_ESTABLISHED / NEEDS_HUMAN_REVIEW，引文在本機逐字對回原文；改稿後舊審查自動變 STALE。純 Python 標準函式庫，對 API 金鑰、送出同意、網路出口的防護做得很重"
tags:
  - llm-safety
  - fact-check
  - human-in-the-loop
  - meta
---

# MUSE Evidence Review Core 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [Shak0501/muse-evidence-review-core](https://github.com/Shak0501/muse-evidence-review-core) |
| Demo 影片 | [YouTube：real Meta inference and STALE](https://youtu.be/LRThYu3e7CU) |

| 指標 | 數值 |
|------|------|
| Stars | 0（2026-11-05） |
| 建立 | 2026-11-03，只有 1 個 commit |
| 作者 | Shak Lai |
| License | MIT |
| 相依 | 只用 Python 3.9+ 標準函式庫，前端是原生 HTML/CSS/JS |
| 規模 | Python + JS 約 70KB，很多行塞得很密 |

## 它在做什麼

這是一個黑客松作品，主角是 Meta 的 `muse-wonder-1.0`（打 `https://api.meta.ai/v1/responses`）。流程如下：

1. 載入一份固定的虛構原文（「Larch 修理室公告」，只有三句）
2. 寫一份草稿，最多 8 句、8KB，用標點機械式切成 claim
3. 預覽完整請求，逐項勾同意後送一次給 Meta
4. 模型對每句回一個判定，附上原文引文
5. 本機驗 schema，並把每段引文的 offset 拿去原文逐字比對
6. 改稿存檔後，上一份審查自動標成 **STALE**，就算之後把字改回原樣也一樣

四種判定的定義寫在 `core/contracts.py` 的 `POLICY`：

| 判定 | 條件 |
|------|------|
| `SUPPORTED` | 原文有明確支持的句子，**必須附引文** |
| `CONTRADICTED` | 原文有明確相反的句子，**必須附引文** |
| `NOT_ESTABLISHED` | 原文沒提到。重點是「沒講不等於矛盾」 |
| `NEEDS_HUMAN_REVIEW` | 語意不確定，例如「這房間很溫馨」這種主觀描述 |

範例草稿剛好四句各對到一種判定：四張工作台（支持）、有到府服務（矛盾）、免費燈泡（沒提到）、很溫馨（要人看）。

## 值得學的設計

### 1. 引文在本機驗，不信模型

用 `json_schema` strict 模式要求模型回結構化結果，回來後 `verify_review()` 會再檢查一遍：

- claim 數量要跟送出去的一樣，id 不能重複，起訖位置和原文字串要完全相符
- `SUPPORTED`、`CONTRADICTED` 沒附引文就拒絕（`EVIDENCE_REQUIRED`）
- 每段引文都要 `SOURCE[start:end] == quote`，對不上就是 `QUOTE_MISMATCH`

作者也講得很清楚：**引文對得上只代表那段字確實在原文裡，不代表判斷是對的**。語意上對不對，最後還是人決定。

### 2. 用版本邊界讓審查自然過期

審查會綁住草稿的 SHA、原文 SHA、policy 和程式 Manifest 的 SHA。這些只要有一個變了，舊結果就降級成 STALE 歷史紀錄，不會再被當成目前有效的結論。這招可以用在任何「AI 審過的東西後來被人改了」的場景。

### 3. 每個請求只能送一次

- 送出前要做六個獨立決定：demo 使用、風險、資料外送、單次預算、最終送出，再加上按鈕本身代表的「立即確認」
- 在拿金鑰**之前**，先用 `O_EXCL` 加上 fsync 寫一個「已消耗」標記，所以就算取消也算用掉了
- 失敗、逾時或狀態 UNKNOWN 都**不自動重試**，要送就得重新預覽、重新同意
- 紀錄壞掉、權限不對或遇到 symlink 一律 fail closed

### 4. API 金鑰只從終端機的隱藏輸入拿

不吃環境變數、CLI 參數、設定檔，也不經過瀏覽器欄位。它直接開 TTY、關掉 echo，60 秒沒輸入就逾時；沒有 TTY 就拒絕，不會退回明文輸入。回應裡要是出現跟金鑰一樣的字串也會擋下來。

### 5. 用 Python audit hook 做網路圍欄

`core/network_guard.py` 用 `sys.addaudithook` 攔 `getaddrinfo`、`connect`、`sendto`。只放行 loopback，以及確認送出那一刻、限定 context 內對 `api.meta.ai:443` 的那一條連線。測試模式根本連不出去。用很少的程式碼就做到行程層級的出口控制，這招可以抄。作者也自己說明了，這擋不住同一台機器上的其他程式或管理員。

### 6. 「用量」跟「帳單」是兩回事

傳輸狀態、HTTP 狀態、內容是否有效、用量各自分開記。不知道的用量記 `null`，不記 0。介面上的 US$0.10「風險額度」也明講不是供應商那邊強制執行的上限。

## 怎麼跑

```sh
python3 -I -B -S verify.py      # 離線自檢
python3 -I -B -S app.py         # 離線 demo，回應是固定假資料
python3 -I -B -S live.py        # 真的打 Meta，需要自己的 Meta Model API 帳號
python3 -I -B -S connector_test.py   # 用合成金鑰跟真的 PTY 測連接器
```

`-I -B -S` 是隔離模式，不寫 `.pyc`、不載 site-packages，跟它「只用標準函式庫」的宣稱一致。我這邊沒有實際執行，只讀了原始碼。

## 限制

- **只支援內建那份虛構原文**，不能丟自己的 PDF 或 CSV，比較像概念驗證，不是能直接拿來用的工具
- 草稿最多 8 句，切句只看 `.!?` 加空白，中文句號 `。` 不會被切開
- 離線模式的「審查」是寫死的四句對照表，不在表裡的句子一律回 `NEEDS_HUMAN_REVIEW`
- 只有 1 個 commit、0 star，是黑客松當天寫出來的，README 大量篇幅在講權利聲明跟參賽邊界
- Windows 沒測

## 我的看法

功能本身很小，價值在設計，可以當成「怎麼把 LLM 審查做成可稽核的東西」的範本。要做 AI 事實查核、合約審閱、報告核對時，裡面三招可以直接搬：

1. 引文在本機逐字驗證
2. 用 SHA 綁定讓審查結果自動過期
3. 把「沒提到」跟「矛盾」拆成兩種判定

金鑰處理和單次送出的那套儀式對一般產品來說太重了。但如果是會花錢或對外發送的 agent 動作，「先寫已消耗標記再送、失敗不自動重試」這個順序很值得參考。
