---
date: "2026-08-04"
category: "AI 應用"
card_icon: "material-notebook-edit"
oneliner: "演講／研習錄影 → 結構化「可溯源」筆記 + 影片-逐字稿-摘要三向同步的 HTML 檢視器；本機 GPU pipeline(Whisper·投影片抽取·OCR·VLM),Claude Code skill + CLI"
tags:
  - claude-code
  - skills
  - knowledge-base
  - taiwan
---

# lecture-to-notes 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/drpwchen/lecture-to-notes> |
| 作者部落格（工具緣起，繁中） | <https://drpwchen.com/posts/lecture-to-notes/> |
| 作者工具總覽 | <https://drpwchen.com/map/> |
| README（繁中版） | <https://github.com/drpwchen/lecture-to-notes/blob/main/README.zh-TW.md> |

> Metadata（研究當下）：**64 stars** · Python（594 KB）+ JS + CSS · MIT · 建立於 2026-08-02（極新）。
> 作者是台灣**復健科（PM&R）醫師** drpwchen，工具是從自己上課記筆記的需求長出來的——README 的預設值仍留著痕跡：dedup 詞表針對中文 Zoom UI、筆記模板用繁中標題、內建詞頻表偏醫學。

## 專案概述

**把一段演講／研習會錄影,變成結構化、投影片配圖的筆記**——更重要的是變成一個**三向同步的單頁 HTML 檢視器**:影片、帶時間戳的逐字稿、策展過的摘要三者放在同一頁,影片播到哪就高亮對應筆記,點任一筆記時間戳就跳播影片到那一刻。

它的設計目標**不是「摘要一段影片」,而是「可溯源(traceability)」**:成品筆記裡每一句主張,都應該能扣回逐字稿的某個時刻、以及那個時刻螢幕上的那張投影片。README 一句話點破整個專案的靈魂——「大部分的機制存在,是為了讓這個連結**可信賴,而不只是看起來合理**」。

緣起很具體:復健醫學課程(徒手治療、超音波掃描)的知識在**動作**裡,每堂課都是一片腳架森林——大家都錄影想回家重看,但沒人真的重看幾小時影片。作者的頓悟是:**筆記不必是「文字+圖」的傳統形狀**——做一個把影片綁到逐字稿的網頁,就能直接跳到你在意的那一刻。於是分工變成:**摘要拿來讀、逐字稿拿來查證、影片離兩者都只有一鍵**。

**貴的階段全部在本機跑**:Whisper ASR 用你的 GPU、抽 frame、OCR、本地視覺模型做投影片語意。LLM 只在**最後**用一次,把 pipeline 已經組好的證據寫成散文。

## 技術架構:A–E 零 token,F 才用 LLM

```
material folder (影片/音檔/PDF deck/投影片照片)
   │
   ▼ route_inputs.py  ── 分類資料夾、印出該跑的計畫(plan-only,不執行不寫檔)
   ├──────────────► transcribe_video.py  faster-whisper 本機 GPU
   │
   └─ slide source?
        ├ 只有影片 → extract_slides.py(frame + 感知去重)
        ├ PDF deck → build_slides_from_pdf.py(頁面 render + 內嵌文字)
        └ 散圖    → build_slides_from_images.py
   ▼
 Stage B  quick_ocr.py       便宜 OCR 分流
 Stage C  dedup_semantic.py  產出 canonical 投影片
 Stage B2 ocr_surya.py       高品質 OCR
 Stage D  vlm_signals.py     投影片語意(本地 VLM,只給訊號、不做 OCR)
 Stage E  ground_slides.py   把投影片綁到「說到它時」的逐字稿片段
   │  ↑ 逐字稿也匯入這裡
   ▼  產出 slides_grounded.json  ← 這是整條 pipeline 的心臟
 Stage F  synthesis(LLM)  tier pass → write pass
   ├─► render_embeds → finalize_to_vault → audit_note.py
   └─► export_web.py  ★ 三向同步 HTML 檢視器
```

**Stage A–E 全是純 Python、零 LLM token**,產出 `slides_grounded.json`:每張 canonical 投影片的 OCR 文字、語意訊號、以及它在螢幕上時被講到的逐字稿片段。**就算你完全不跑 Stage F,也已經有逐字稿 + 去重投影片集 + 兩者的對映**——這是「大部分的價值和全部的本機算力」。

### 招牌輸出:三向同步的 HTML 檢視器

`export_web.py` 產一個**單一自包含 HTML**,影片 / 帶時間戳逐字稿 / 摘要三者並置且**雙向同步**:

- **影片 → 筆記**:播放時對應筆記 bullet 自動高亮、捲入視野
- **筆記 → 影片**:每個 bullet 帶 `(Vn MM:SS)` 時間戳,點了影片就 seek 過去
- **三種閱讀模式**:只看摘要 / 只看逐字稿 / 並排;摘要層(策展、依工作流排序)與逐字稿層(逐字、依時間排序)是同一條時間軸的兩個章節,可以**由上而下讀、由下而上驗**
- **離線可分享**:一個 `.html` + 一個支援資料夾,對方雙擊就開,無需 server、無 build step;`--compress` 產較小的 H.264 版好傳遞

檢視器 UI 全在 `scripts/layout2/`(`viewer.css` / `viewer.js`),`export_web.py` 只生時間軸 manifest 與同步筆記 HTML——**改 UI 是改 asset,不是改 generator**。

### 三種持久格式 + Obsidian vault

HTML 是閱讀介面,但**純 markdown 才是儲存格式**:`finalize_to_vault.py` 把成品筆記與引用投影片圖送進 Obsidian 式 vault;支援資料夾內含 `markdown/` 版(wikilink 已改寫,資料夾本身**可直接當 Obsidian vault 開**),外加 PDF 副本。→ 同一場演講三種耐久形態:**同步網頁拿來學、markdown 進知識庫、PDF 交給任何人**。

## 最值得偷的一招:對位(alignment)

> 「capture time 是一個假設,cross-correlation 才是證據」——README 說如果只帶走一樣東西,帶這個。

當一場演講被多台裝置錄(房間錄影 + 手機片段 + 投影片照片),你需要共享時間軸。**天真作法是信任每個檔案的 capture timestamp——這錯的頻率高到會出事**:手機時鐘會漂移、有些檔案只有 mtime、錄到一半停掉再開的檔案會謊報自己的起始時間。所以 pipeline 把兩者分開:

| 元件 | 職責 |
|------|------|
| `media_capture_index.py` | 讀 capture 時間,當成**帶 `reliable` flag 的「聲稱(claim)」**;起始時間來自 mtime 或根本沒有的,標為 unreliable、**不准拿來對位** |
| `xcorr_media_offsets.py` | 用重疊音訊的逐字稿做**互相關(cross-correlation)量出真實 offset**——這是證據 |
| 衝突處理 | 當 claim 與量測差超過 5 秒,設 `"conflict": true` 並**停下**,**永不自動修正** |

它防的是一種災難:**一個 44 分鐘的錯位在輸出裡看起來完全正常**,因為每個下游階段都忠實地處理了錯誤的配對。「一條會默默調和衝突證據的 pipeline 產出自信的垃圾;一條會標記衝突的 pipeline 產出一個問題。」

## 是 Claude Code skill 還是一堆腳本?——兩者皆是

- Repo 佈局成 **Claude Code skill**:`SKILL.md` 是 agent 面向的地圖,`reference/` 放 agent 按需讀的細部規格。把整棵樹丟進 `~/.claude/skills/lecture-to-notes/`,agent 就能開全自動。
- **當純 CLI:Stage 0–E 可獨立跑**,給你逐字稿、canonical 投影片集、OCR 文字、VLM 訊號、grounding map。
- **Stage F(synthesis)是 prompt-driven**:它是 `reference/note-spec.md` 裡「一個稱職寫手該拿 `slides_grounded.json` 做什麼」的**規格**,不是一支呼叫 API 的腳本——**沒有 `synthesize.py`**。不用 agent driver 的人,就把 `slides_grounded.json` 當交接點、自己寫 Stage F,規格告訴你輸出要滿足什麼,`audit_note.py` 會機械式檢查。

## 目前限制 / 注意事項

- **只在 Windows 11 + NVIDIA RTX 3070 Ti(8 GB)實測**;設計上不綁 Windows,但 Linux/macOS 未測。Python 3.12。
- **GPU 是快路徑、非必要**:無 GPU 時 CPU fallback 內建(自動降 int8、先印誠實 ETA;60 分鐘講稿要跑數小時);或用 `groq_asr.py` 把轉錄外送 Groq 的 `whisper-large-v3-turbo`(免費 tier 可用)——**但機密錄影別送出去**,且 hosted Whisper 對嚴重 code-switching 音訊沒有 anti-collapse 旋鈕。
- **8 GB 卡上 GPU 階段必須序列化**:Whisper 與 VLM 不能同時跑,抽 frame 不能在轉錄時跑;實測甜蜜點 `--batch-size 3 --beam-size 10`,`--beam-size 15` 序列模式會 crash。
- **`ffmpeg` / `ffprobe` 必須在 PATH**,非選配。選配:ollama + `minicpm-v:8b`(Stage D)、Surya 獨立 venv(高品質 OCR)、pandoc(web/PDF 匯出)。
- **轉錄沒有預設語言**:`transcribe_video.py` 不給 `--lang` 就不啟動——因為猜錯會讓 Whisper「把帶口音的英文幻覺成流利中文」,而且不讀不會發現。

## 研究價值與啟示

### 關鍵洞察

1. **「可溯源」是比「摘要」高一階的產品目標**——多數 AI 影片工具做的是「壓縮成摘要」,本質有損且無法驗證。這個專案把目標定成「每句話都能扣回逐字稿時刻 + 當下投影片」,於是整個架構(grounding、雙向同步、audit)都是為了讓那條連結**可信賴而非看似合理**。這是把「AI 輸出可驗證性」當一等公民的極佳範例,值得任何做 RAG / 知識工具的人參考。

2. **「證據 vs 聲稱」的分離,是防止自信垃圾的通用模式**——`media_capture_index`(claim + reliable flag)與 `xcorr_media_offsets`(measurement)分離、衝突就停不自動修,這個模式遠超影片對位:任何有「元資料聲稱」與「實測」兩個來源的系統(檔案時戳、使用者輸入 vs 感測、快取 vs 真實值)都適用。**寧可產出一個問題,不要產出自信的垃圾**。

3. **「大聲降級(degrade loudly)」是最省成本的錯誤設計哲學**——README 直說:少了選配套件,就停用該功能並告訴你失去了什麼,**絕不默默換一個更差的方法**。因為「默默替換」產出的是**錯的輸出**而非**少的輸出**,是 `AUDIT_SUMMARY.md` 裡最貴的一類 bug。這一條可以直接寫進任何 pipeline 的設計守則。

4. **職責純粹化避免「重複腳本」幻覺**——「VLM 不做 OCR,只給語意訊號;文字一律來自 OCR 階段」。作者說混淆這兩者正是「我們有三支重複 OCR 腳本」長期困惑的根源。**把「看起來相似但職責不同」的東西明確切開**,是維護性的關鍵。

5. **本機優先 + LLM 只用在最後一步,是成本與隱私的雙贏**——A–E 零 token、全本機,LLM 只負責「把已組好的證據寫成散文」。這把「哪些工作真的需要 LLM」想得很清楚:對位、去重、OCR、grounding 都是確定性工程問題,不該花 token;LLM 的價值在最後的**表達**。這也讓中間產物(`slides_grounded.json`)本身就有價值、可換任何模型接手。

6. **「筆記不必是文字+圖的形狀」——重新定義輸出載體**——當知識在動作裡(徒手治療、超音波),硬要塞回文字反而失真。做一個綁影片的網頁,承認「有些知識只活在影像中」。這是提醒:**別預設 AI 產出一定是一段文字**,先問這個領域的知識天生長什麼樣。

### 與其他專案的關聯

- **與 [notebooklm-py](notebooklm-py.md) 對照**:都是「把長內容轉成好消化的形態」,但方向相反——NotebookLM 把文件轉成**音訊**(podcast),lecture-to-notes 把**影音轉成可溯源的文字+同步網頁**。一個追求「輕鬆聽」,一個追求「可查證」。
- **與 [OpenDataLoader PDF](opendataloader-pdf.md) / [pdf-inspector](pdf-inspector.md) 的關係**:都在做「非結構化輸入 → 結構化資料」的解析,本專案的 slide OCR / PDF deck 匯入是同類問題;差別是它多了時間軸對位這個維度。
- **作為 Claude Code skill 的範例**:對照本站 [Agent Skills](topics/agent-skills.md) 分類與 skill-review 流程,這是一個「skill + 可獨立跑的 CLI」雙形態的優秀樣本——`SKILL.md` 當 agent 地圖、`reference/` 按需載入,是 progressive disclosure 的實作參考。
- **台灣開發者作品**:作者是復健科醫師,工具從真實臨床教育需求長出來,預設值帶繁中/醫學脈絡——與本站其他 [taiwan](tags.md) 標籤專案同屬「在地需求驅動」的一脈。
