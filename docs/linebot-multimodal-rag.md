---
date: "2026-05-14"
category: "AI 應用"
card_icon: "material-chat-question"
oneliner: "kkdai 的 LINE Bot + Gemini File Search API 多模態 RAG 範例，靠 metadata_filter 在單一 store 做多租戶隔離、Cloud Run 部署"
---

# LINE Bot Multimodal RAG (kkdai) 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/kkdai/linebot-multimodal-rag> |
| 作者 | <https://github.com/kkdai>（Evan Lin / 台灣 LINE 社群活躍開發者） |
| Gemini File Search 公告 | <https://blog.google/innovation-and-ai/technology/developers-tools/expanded-gemini-api-file-search-multimodal-rag/> |
| Gemini Embedding 2 | <https://deepmind.google/models/gemini/embedding/> |
| File Search API docs | <https://ai.google.dev/gemini-api/docs/file-search?hl=zh-tw> |
| 規模 | 26 stars / 4 forks（May 14 2026 抓取）、無 license、Python 3.12 |

## 專案概述

**linebot-multimodal-rag** 是 kkdai 在 2026-05-11 開的小型 PoC repo，把 Google 剛擴展的 **Gemini File Search API**（managed multimodal RAG）接到 LINE Bot 上，做出「LINE 上傳檔案就能建知識庫、用文字或圖片查詢」的最小可用範例。3 天內累積 26 stars，雖小但對 Gemini File Search 在亞洲市場（特別是 LINE 生態系）的落地很有示範意義。

幾個讓這個 repo 值得單獨研究的點：

1. **完整擁抱 managed RAG**：不接 ChromaDB / FAISS / pgvector，全部交給 Gemini File Search Store（Google 處理 chunking + embedding + indexing）。
2. **單一 store + metadata_filter 做多租戶**：所有 LINE 使用者共用一個 File Search Store，靠 `custom_metadata: user_id=<LINE UID>` 上傳、`metadata_filter='user_id="<UID>"'` 查詢，server-side enforce。
3. **CLAUDE.md 寫得很完整**：作者把設計決策、API 呼叫 shape、未完成事項都列進 CLAUDE.md，是 Claude Code 友善 repo 的範本。

## 功能流程

```text
LINE App
  │ Webhook (HTTPS)
  ▼
FastAPI on Cloud Run
  ├─ 文字訊息 ──────────────────► Gemini File Search → 回覆 + page citation
  ├─ 圖片 / 檔案 ─► GCS 備份 ──► Quick Reply 按鈕 (5min session TTL)
  └─ Postback 按鈕
       ├─ 📥 存入資料庫 ─► BackgroundTask ─► upload+poll ─► push_message
       └─ 🔍 作為搜尋 ──► GCS 讀檔 ──► Gemini File Search → 回覆
```

| 互動 | 行為 |
|------|------|
| 傳 PDF / 文字檔 | Bot 詢問：存入 or 搜尋 |
| 傳圖片 | Bot 詢問：存入 or 搜尋 |
| 點「📥 存入資料庫」 | 非同步索引（含 `user_id` metadata）→ push 通知完成 |
| 點「🔍 作為搜尋」 | 用該檔/圖當 query，只在自己資料中找 |
| 輸入文字 | 直接對自己資料庫做 RAG |
| 工作階段 TTL | 5 分鐘 |

## 技術堆疊

| 元件 | 選型 |
|------|------|
| 框架 | FastAPI + uvicorn |
| LINE SDK | `line-bot-sdk` v3 (`AsyncMessagingApi`, `AsyncMessagingApiBlob`) |
| Gemini SDK | **`google-genai`**（新 SDK，**不是** `google-generativeai`） |
| Embedding | `models/gemini-embedding-2`（多模態，文字 + 圖片同向量空間） |
| Generation | `gemini-3-flash-preview`（env `GEMINI_MODEL` 可調） |
| 儲存 | GCS（`uploads/{user_id}/{message_id}.{ext}` + `config/file_search_store_name.txt`） |
| Session | in-memory + 5min TTL（需要 `min-instances=1`） |
| 部署 | Cloud Run via Cloud Build |
| 限制 | 單檔 100 MB、不支援 audio / video |

## 關鍵 API 呼叫範式（從 CLAUDE.md 摘）

### 建立 File Search Store

```python
store = client.file_search_stores.create(config={
    "display_name": "linebot-multimodal-rag",
    "embedding_model": "models/gemini-embedding-2",
})
```

### 上傳並帶 user metadata

```python
operation = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name,
    file=tmp_path,
    config={
        "display_name": filename,
        "custom_metadata": [{"key": "user_id", "string_value": user_id}],
    },
)
# operation 是 long-running，需 poll: client.operations.get(operation)
```

### 查詢時用 user filter

```python
response = await client.aio.models.generate_content(
    model=GEN_MODEL,
    contents=text,  # 或 Content(parts=[image_part, text_part])
    config=types.GenerateContentConfig(
        tools=[types.Tool(file_search=types.FileSearch(
            file_search_store_names=[store_name],
            metadata_filter=f'user_id="{user_id}"',  # google.aip.dev/160
        ))],
    ),
)
```

`metadata_filter` 用的是 **google.aip.dev/160** 過濾語法（同 GCP 通用 API filter spec）。

## 部署摘要

```bash
# 本機
cp .env.example .env  # 填 LINE 兩把 key + GEMINI_API_KEY + GCS_BUCKET
gcloud auth application-default login
uvicorn app.main:app --reload --port 8080
ngrok http 8080

# Cloud Run
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_GCS_BUCKET=你的-bucket
```

API 端點：`/health`、`/store/info`（看已索引文件數與 state）、`/webhook`。

## 目前限制與注意事項（作者自陳）

- **`/store/info` 未做認證**：production 前要加保護。
- **Session in-memory**：Cloud Run 多實例會丟資料；要 `min-instances=0` 必須換 Firestore。
- **沒有刪除流程**：使用者無法透過 LINE 刪自己的文件。
- **沒有 quota / rate limit per user**：被 spam 上傳會吃掉所有人額度。
- **不支援 audio / video**：Gemini File Search 限制。
- **LINE access token 30 天會過期**：要 rotation 或申請長期 token。
- **無 license**：repo 沒 `LICENSE` 檔，引用前要主動問作者授權方式。

## 研究價值與啟示

### 關鍵洞察

1. **Managed RAG 已可取代多數自架 vector DB 場景**：作者 CLAUDE.md 第一條設計決策直接寫「Do NOT add ChromaDB / FAISS / pgvector — that defeats the point」。這個立場呼應 Google 把 chunking + embedding + indexing 包成 service 的策略——對 PoC 與中小流量場景，**自架 vector DB 的工程價值正在快速縮水**。對照 [[rag-anything]] 那種「全套 self-host」與本研究「全套 managed」是同一光譜的兩端。
2. **單一 store + metadata_filter 做多租戶**是個聰明的取捨：N 個使用者開 N 個 store 操作成本高（quota、生命週期、刪除），共用 store + server-side filter 的設計把運維成本壓到極低。代價是 quota 共享、需要對抗 prompt injection（讓使用者繞過 filter）。**對 LINE / Discord / Slack 這類「每個 user ID 都是已驗證身分」的場景特別合適**。
3. **`google-genai` vs `google-generativeai` 是兩個不同的 SDK**：作者特別在 CLAUDE.md 提醒——許多人會誤裝舊版。新 SDK (`google-genai`) 是 google-deepmind 端整併後的官方版，**File Search API 只在新 SDK 出現**。這個提醒值得寫進任何接 Gemini 的 repo。
4. **非同步索引 + push notification 是 LINE Bot RAG 的必要模式**：LINE reply token 30 秒會 expire，但建索引動輒 30 秒到 5 分鐘。作者用 FastAPI BackgroundTasks + LINE `push_message` 解這個問題，是值得抄的 pattern。對 Discord / Slack bot 同樣適用（webhook 都有類似的 timeout 限制）。
5. **CLAUDE.md as 設計決策契約**：這個 repo 的 CLAUDE.md 是「給 AI 看的 ARCHITECTURE.md」典範——明確標註「Do NOT undo without asking」的設計決策、API call shape 範本、未完成事項清單。對 vibe-coding 場景，這種寫法可以大幅減少 AI 改動時的破壞性。值得提取成 CLAUDE.md 寫作 template。
6. **`gemini-embedding-2` 是多模態同向量空間**：文字 + 圖片 + PDF 一起 embed 到同一空間（README 標 "5 種模態"），這意味著「傳圖找 PDF」、「傳 PDF 找圖」這類 cross-modal query 是免費送的，不需要再做 captioning 中介層——對比 [[rag-anything]] 為了做 cross-modal 還要拉 VLM 生 caption + 建多模態 KG，managed embedding 的工程成本省非常多（但代價是 black-box、模型 lock-in、無法離線）。

### 與其他研究的關聯

- 與 [[rag-anything]]：**同一問題的兩種光譜端解法**。RAG-Anything 走自架 + multimodal KG + Vector-Graph fusion 的學術深度路線；本研究走 fully managed + 只用 metadata_filter 的工程便利路線。同時讀完，能準確判斷專案要走哪條。
- 與 [[ai-agents-for-beginners]]：本研究實作的「multimodal query + cross-modal embedding」正好是 Microsoft 課程第 5 / 12 / 13 課的 Google 對應方案。對學習者來說是 Microsoft Agent Framework 之外的對照組。
- 與 [[ramp-ai-agents]]、[[appflowy]] 等 AI 應用研究：屬於同樣的「把新 AI 能力包成可用產品」族群，本案最小規模、最直接，適合作為「想做 LINE/Discord/Slack RAG bot」的起手 template。
- 與 [[why-your-ai-is-dumbing-down]] 的 context engineering：本研究示範了「retrieval 端的 context 是 Google 端建構好的」這個全託管路線。對使用者來說好處是不用煩惱 chunking 策略，壞處是無法檢視/控制 Google 怎麼切、怎麼排——對需要可審計性的場景必須慎用。
- 對「教 AI 寫 code」的人：CLAUDE.md 寫法值得直接 fork 來改。建議放在 [[learn-claude-code]]、[[claude-md-improver]]（如果存在）這條學習鏈上一起讀。
