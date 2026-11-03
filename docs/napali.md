---
date: "2026-11-03"
category: "AI 創作資源"
card_icon: "material-image-filter-hdr"
oneliner: "用 Claude Code(Opus 5.5)跑 13 輪 agent 做出來的 Na Pali 海岸無人機空拍,沒有任何貼圖、模型或圖片,地形侵蝕、FFT 海浪、浪花、礁岩、一棵棵 SDF 樹、體積雲全部在一個 5,273 行的 index.html 裡用 WebGL2 shader 算。做法是水/天/地形/植被各派一個 specialist 平行改、再合併、最後由 judge 對照實景照片打分。MIT,129★"
tags:
  - claude-code
  - webgl
  - procedural
  - multi-agent
---

# napali 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/Leonxlnx/napali> |
| 作者 | Leon Lin([@LexnLin](https://x.com/LexnLin)) |
| 分析 commit | `4afb7c3`(2026-10-23) |

> Metadata(2026-11-03 抓取):**129 stars / 26 forks** · 建立於 2026-10-23,整個 repo 只有 1 個 commit(開發過程沒公開)。MIT。

## 一句話

一段夏威夷考艾島 Na Pali 海岸的無人機飛行影片,**全部用程式碼生成**:沒有貼圖、沒有 3D 模型、沒有下載任何素材,打開 `index.html` 就在瀏覽器裡即時算出來。它值得看的地方有兩個:一是程序化圖學本身的密度,二是 README 公開說這是 Claude Code 跑 13 輪多 agent 流程做的。

![四個畫面](https://raw.githubusercontent.com/Leonxlnx/napali/main/media/overview.jpg)

## 為什麼 HTML + JS 就做得到

真正在畫圖的是顯示卡，HTML + JS 只是把工作交給它。

**分工**

- **JS**：開 canvas、跟瀏覽器要 WebGL2、把 shader 送去顯示卡編譯，每一幀告訴它相機在哪。
- **GLSL shader**：寫在 JS 字串裡、跑在顯示卡上的小程式。地形、海、樹、雲都是它算的。

WebGL2 等於瀏覽器開了一扇門讓網頁直接用顯示卡，所以這個「網頁」其實比較像一支跑在顯示卡上的繪圖程式。

**沒有圖片和模型，畫面從哪來**

靠數學公式。遊戲通常是先做好模型和貼圖再畫，這裡是讓每個像素去問公式「我這裡該是什麼顏色」。

- **山**：隨機雜訊堆出起伏，再模擬雨水往下流把山刻出山谷，反覆 4,000 次，長出刀鋒稜線。
- **海**：幾千道不同大小的波浪疊在一起，用 FFT 一次算完。
- **樹**：每棵樹是一個距離函數(SDF)，丟一個點進去，它回答離樹的表面多遠。每個像素從相機射一條光線，照這個距離一步步往前走，碰到表面就停下來上色，這招叫 ray marching。
- **雲和光影**：光線穿過雲時一路累加濃度，越厚越暗。

**顯示卡為什麼扛得住**

1080p 一幀約 200 萬個像素，每個像素跑同一套公式、只是座標不同。顯示卡有幾千個小核心同時算，剛好適合；CPU 只有幾個核心，一個個算會慢到不能用。

**但還是很重**：shader 很長，第一次編譯要 30-90 秒；內顯筆電一張高畫質要 1-2 秒，即時播放會自動降解析度；公開影片是離線一幀幀算好再接起來的。

**這不是新招**：demoscene 和 Shadertoy 圈子玩很多年了，有人用 4KB 程式生出整段 3D 動畫。napali 特別的是規模大、追求照片級寫實，而且是 agent 寫的。

!!! tip "程序化生成的本質"
    一般 3D 是「存資料、讀資料」，程序化是「存公式、現場算」：檔案極小，代價是每幀都吃大量 GPU。SDF 的好處是形狀好組合，兩個距離取最小值就是把兩個物體合在一起，所以幾千棵各不相同的樹只要一個公式配不同的隨機種子。

## 怎麼跑

```bash
# 直接開(第一次編 shader 要 30-90 秒)
open index.html                    # 即時飛行
open "index.html?mode=still"       # 最後那張空拍構圖的高品質靜態圖

# 錄影片:需要 Node 22+、Chrome、ffmpeg
node tools/video.mjs flight.mp4 1920 1080 30 4 "hud=0&bandpx=5000"
```

飛行中:`Space` 暫停、`R` 重來、`←/→` 跳 5 秒、`H` 開關 HUD。需要像樣的 GPU,作者在內顯筆電上一張 1672×941 離線要 1-2 秒,即時模式會自動降解析度。

## 畫面裡每樣東西怎麼來的

| 元素 | 做法 |
|------|------|
| 海岸線 | 唯一的「資料」:從一張參考照片描出來的水線多邊形(`COAST_IMG`,主島 + 5 個海蝕柱),加上兩條山谷軸線的控制點 |
| 地形 | 基礎山體 → **GPU 上跑 stream-power 河流侵蝕**(多流向排水 + 崩積滑落,預設 4,000 次迭代)→ 再用 phasor noise 刻出 Na Pali 特有的刀鋒稜線和侵蝕溝槽 |
| 海洋 | **三層 FFT 海浪**(1013m / 137m / 19.7m 三個尺度),風向和湧浪方向由海岸線法向量推出來 |
| 海水著色 | 依水深算吸收/散射、礁岩、沙底、碎浪、白沫、反光,單獨一個 980 行 shader |
| 植被 | 每棵樹、棕櫚、灌木都是獨立的 **SDF 物件**,在抖動網格上依地形/植被遮罩種下去。樹冠分四層:外形 → 1m 葉叢 → 0.5m 葉簇 → 單片葉子,每層小於約 2 像素就淡出避免閃爍 |
| 天空 | 天頂到地平線的漸層 + 鹽霧帶 + **體積積雲**(依島嶼地形排列:海岸上方留晴空、山上堆雲堤)+ 卷雲 |
| 運鏡 | `v2_flight.js` 裡一串關鍵影格 `[時間, 位置, 看向, FOV]`,從海面 4m 低飛一路拉到 1000m 高空俯瞰 |

所有外觀參數都用 `num('key', 預設值)` 讀 URL query,總共 **194 個旋鈕**,調色、霧、浪高、太陽角度都不用重 build 就能改。

## 原始碼結構:index.html 是 build 出來的

```text
v2_template_backup.html   頁面骨架、地形生成與侵蝕、FFT 海洋、後製(1,993 行)
  + patch_v3.cjs          塞進 v3_geo.glsl(SDF 幾何)、v3_shade.glsl(陸地材質光照)
  + patch_v4.cjs          塞進 v4_water.glsl、v4_sky.glsl
  + tweaks.cjs            一堆「找字串 → 換字串」的 look-dev 補丁(357 行)
  ─────────────────────
  node tools/rebuild.cjs → index.html(5,273 行)
```

這個結構很明顯是為多 agent 平行開發設計的:**水、天、地形、植被各自一個檔案**,specialist 互不踩腳,merge 步驟就是 `rebuild.cjs`。`tweaks.cjs` 的 `rep()` 找不到目標字串會印 `MISSING` 並讓 exit code 變 1,等於幫字串補丁加了一個最低限度的防呆。

## 從註解看得到的 agent 開發痕跡

repo 只有一個 commit,但註解裡留了大量輪次標記(`r4f`、`r5`、`r9`、`r10 terrain` 之類,將近 200 處),有些還寫著從失敗中學到的教訓,例如:

> the round-4 bzL widening painted sand on the cliff toes, removed the beach-front bushes and grew the grey flat

> ref.png / r9 show a shaded V gorge between steep fins

也就是 judge 拿參考照片比對後,下一輪 specialist 把「哪裡不像、上次改壞了什麼」直接寫進程式碼註解,當成跨輪的記憶。這招很便宜:不用額外的記憶系統,下一個 agent 讀程式碼就讀到了歷史。代價是註解會越積越長,而且參考照片沒附在 repo 裡,外人無法重現 judge 那一步。

## 錄影工具也是踩過坑的產物

`tools/cdp.mjs` 是一個零依賴的 Chrome DevTools Protocol 驅動,值得注意的設計:

- **全機器 GPU 鎖**:用 `mkdir` 在 temp 目錄建鎖(原子操作),寫入 owner PID;持有者死掉或超過 20 分鐘就搶回來。
- 每次 render 完讓 GPU 休息 20 秒,`bandpx` 把一幀切成小塊送 GPU。
- README 直說原因:**好幾個平行 render 把內顯驅動搞當了**。多 agent 平行跑時,共享硬體資源要自己序列化,這是很實際的教訓。

公開影片是 1080p30、每幀 4 個 sample、`SPEED=2.5`,共 1,584 幀。

## 評價

**值得參考的**

- 「specialist 平行 + merge + 對照參考圖的 judge」這個迴圈,很適合任何**有明確目標圖、但沒有測試可以跑**的創作型任務(視覺、音訊、版面)。judge 取代了單元測試的角色。
- 依領域拆檔、用 build 腳本合併,讓多個 agent 可以同時改同一個產出物。
- 把輪次教訓寫進註解,是零成本的跨 session 記憶。

**要注意的**

- 「完全沒有資料」要打點折扣:海岸線是從實景照片描的,judge 也靠實景照片,只是這些照片沒進 repo。
- 開發過程(13 輪的 prompt、judge 的評分標準、花了多少 token)完全沒公開,只能從註解反推。
- `tweaks.cjs` 用字串取代修改 template,template 一改字就會 `MISSING`,適合一次性作品,不適合長期維護。
- 對 GPU 要求高,內顯即時播放會明顯降畫質。

## 跟其他筆記的關係

- 創作型 agent 工作流:[storytold](storytold.md)、[video-autopilot-kit](video-autopilot-kit.md)
- 多 agent 平行改同一個 repo 的協調問題:[agent-orchestrator](agent-orchestrator.md)
