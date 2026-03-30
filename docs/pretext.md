---
date: "2026-03-29"
category: "開發工具"
card_icon: "material-format-text"
oneliner: "Cheng Lou 的零 DOM 文字排版引擎 — `layout()` 比 DOM 測量快 480-1240x，17+ 語言深度支援（4.6K stars / 3 天）"
---
# Pretext 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [chenglou/pretext](https://github.com/chenglou/pretext) |
| npm | `@chenglou/pretext` |
| Live Demos | [chenglou.me/pretext](https://chenglou.me/pretext/) |
| 社群 Demos | [somnai-dreams.github.io/pretext-demos](https://somnai-dreams.github.io/pretext-demos/) |
| 作者 Twitter | [@_chenglou](https://x.com/_chenglou) |
| Josh Kale 推文介紹 | [X](https://x.com/JoshKale/status/2037900758750761053) |
| react-motion（同作者） | [chenglou/react-motion](https://github.com/chenglou/react-motion)（21.7K stars） |

## 專案概述

**Pretext** 是 Cheng Lou 開發的零依賴 TypeScript 函式庫，解決一個存在 30 年的網頁核心問題：**DOM 文字測量造成的 layout reflow 瓶頸**。

核心思路：把文字排版拆成兩步——`prepare()` 一次性用 Canvas 測量所有 segment 寬度並快取，`layout()` 在熱路徑上只做純算術。結果是 `layout()` 的成本降到 **每個文字區塊 0.0002ms**，比傳統 DOM interleaved 測量快 **480x（Chrome）到 1,240x（Safari）**。

截至 2026-03-29（發布僅 3 天），已累積 **4,599 stars、178 forks**。這是 Cheng Lou 繼 react-motion（21.7K stars）之後又一個引爆社群的專案。

### 作者背景

Cheng Lou 是前端/程式語言社群的知名人物：

- **Meta 時期**：React 團隊核心成員，主導 [ReasonML](https://reasonml.github.io/) 開發，參與 ReScript、Messenger.com
- **代表作**：[react-motion](https://github.com/chenglou/react-motion) — 基於物理彈簧的 React 動畫庫（21.7K stars）
- **著名演講**：
  - "On the Spectrum of Abstraction"（React Europe 2016）— 用統一框架理解抽象層級
  - "Taming the Meta Language"（React Conf 2017）— 語言 vs 後設語言的流動性
- **現職**：Midjourney 工程師

## 核心問題

當 UI 需要知道「這段文字有多高？」時（虛擬化、動畫、Layout Shift 防止等），傳統做法是呼叫 `getBoundingClientRect()` 或讀取 `offsetHeight`，但每次讀取都會觸發瀏覽器的**同步 layout reflow**。多個元件讀寫交錯時，瀏覽器反覆重新排版整份文件。

### Benchmark（500 個文字區塊）

| 方法 | Chrome | Safari |
|------|--------|--------|
| **Pretext `layout()`** | **0.09ms** | **0.12ms** |
| DOM batch 測量 | 4.05ms | 87.00ms |
| DOM interleaved 測量 | 43.50ms | 149.00ms |

`layout()` 比 DOM interleaved 快約 **480x（Chrome）** 到 **1,240x（Safari）**。

## 技術架構

### 兩階段模型

```
階段 1: prepare(text, font)          ← 一次性，用 Canvas 測量
  正規化空白 → Intl.Segmenter 分詞 → 標點合併 → CJK 拆分
  → Canvas measureText() → 快取 segment 寬度 → Emoji 修正

階段 2: layout(prepared, maxWidth, lineHeight)   ← 熱路徑，純算術
  零 DOM 讀取 | 零 Canvas 呼叫 | 零字串操作 | 零記憶體配置
  → { height, lineCount }
```

### 階段 1 細節（`prepare`）

1. **正規化空白**：匹配 CSS `white-space: normal` 行為
2. **`Intl.Segmenter` 分詞**：正確處理 CJK 逐字斷行、泰文、阿拉伯文等
3. **標點合併**：將 "better." 當作一個測量單位（匹配 CSS 行為）
4. **CJK 字元拆分**：每字元可獨立斷行
5. **Canvas `measureText()` 測量**：按 (segment, font) 快取
6. **長單字 grapheme 預測量**：支援 `overflow-wrap: break-word`
7. **Emoji 修正**：自動偵測並修正 Chrome/Firefox 在 canvas 上測量 emoji 偏大的問題
8. **可選 Bidi metadata**：供自定義渲染器使用

### 內部 Segment 模型

區分 8 種 break kind：

| Kind | 說明 |
|------|------|
| `text` | 一般文字 |
| `space` | 空白 |
| `preserved-space` | 保留空白 |
| `tab` | Tab |
| `glue` | NBSP/Word Joiner（不可斷行） |
| `zero-width-break` | 零寬斷行點 |
| `soft-hyphen` | 軟連字號 |
| `hard-break` | 強制換行 |

### 原始碼結構

| 檔案 | 職責 |
|------|------|
| `src/layout.ts` | 核心公開 API |
| `src/analysis.ts` | 文字正規化、分詞、膠合規則 |
| `src/measurement.ts` | Canvas 測量、快取、emoji 修正、瀏覽器 profile |
| `src/line-break.ts` | 內部斷行核心 |
| `src/bidi.ts` | 簡化 bidi metadata（源自 pdf.js，via Sebastian Markbage） |
| `src/test-data.ts` | 共享測試語料庫 |
| `src/layout.test.ts` | 不變性測試 |

大小：**~1.7 kB min+gzip / ~8 kB raw**，零依賴。

## API 設計

### Use Case 1：純高度預測（最常用）

```typescript
import { prepare, layout } from '@chenglou/pretext'

// 一次性：測量所有 segment 寬度
const prepared = prepare('AGI 春天到了. بدأت الرحلة', '16px Inter')

// 熱路徑：純算術，每次 resize 都可呼叫
const { height, lineCount } = layout(prepared, 320, 20)
```

### Use Case 2：手動逐行排版

```typescript
// 完整行資訊
prepareWithSegments(text, font, options?) -> PreparedTextWithSegments
layoutWithLines(prepared, maxWidth, lineHeight) -> { lines: LayoutLine[] }

// 串流式：不建構字串，只回傳寬度/cursor
walkLineRanges(prepared, maxWidth, onLine) -> number

// 逐行迭代：每行可不同寬度（繞障礙物）
layoutNextLine(prepared, start, maxWidth) -> LayoutLine | null
```

### 輔助 API

```typescript
clearCache()         // 清除內部快取
setLocale(locale?)   // 設定 Intl.Segmenter locale
```

## i18n 深度支援

這是 Pretext 與其他文字測量庫的**最大差異**。在 `corpora/` 目錄中包含 17+ 語言的長文本 canary：

| 語言 | 語料 | 精確度 |
|------|------|--------|
| 日文 | 羅生門、蜘蛛の糸 | anchor 精確，Chrome 有小幅正向漂移 |
| 韓文 | 운수 좋은 날 | 完全精確 |
| 中文 | 祝福、故鄉 | Safari 精確，Chrome 有字型敏感性 |
| 泰文 | Nithan Vetal | 精確 |
| 高棉文 | Prachum Reuang Preng | 精確 |
| 緬甸文 | 兩篇故事 | 殘留 Chrome/Safari 分歧 |
| 烏爾都文 | چغد | Nastaliq/Naskh canary |
| 印地文 | Eidgah | 完全精確 |
| 阿拉伯文 | 兩篇長文 | 粗語料精確 |
| 希伯來文 | Masaot Binyamin | 完全精確 |
| Mixed app text | URL、emoji、時間範圍等 | 幾乎完全精確 |

**瀏覽器精確度回歸門**：7,680/7,680 測試全部通過（4 字型 x 8 尺寸 x 8 寬度 x 30 文字，跨 Chrome/Safari/Firefox）。

## 七個 Demo

| Demo | 說明 | 核心技術 |
|------|------|---------|
| **Accordion** | 展開/收合區段 | 高度由 Pretext 計算而非 DOM |
| **Bubbles (Shrinkwrap)** | 訊息氣泡最緊寬度 | `walkLineRanges()` 做二分搜尋找最窄寬度 |
| **Dynamic Layout** | 固定高度編輯版面 | 障礙物感知標題路由 + 連續兩欄排版 |
| **Variable Typographic ASCII** | 粒子驅動 ASCII art | 比例字型 vs 等寬字型 |
| **Editorial Engine** | 動態球體、即時文字重排 | Pull quotes、多欄排版、零 DOM 測量 |
| **Rich Text** | 混合 inline 元素排版 | Code spans、links、chips |
| **Masonry** | 文字卡片遮蔽 | 高度預測來自 Pretext |

其中 **Bubbles** 展示了 CSS `fit-content` 無法做到的能力：用二分搜尋找到「保持相同行數的最窄寬度」。

## 實際應用場景

1. **虛擬化/遮蔽**：不需猜測或快取即可做正確的 row height 預測
2. **Masonry layout**：純 JS 計算每張卡片高度
3. **JS-driven flexbox**：微調 layout 值而不用 CSS hack
4. **開發時驗證**：AI 生成的 UI 可以在無瀏覽器環境下驗證按鈕文字是否溢出
5. **防止 Layout Shift**：新文字載入時重新錨定捲軸位置
6. **雜誌/報紙式排版**：文字繞障礙物流動、多欄排版
7. **訊息氣泡 Shrinkwrap**：找到最緊湊的寬度

## 技術研究發現（RESEARCH.md）

Cheng Lou 在開發過程中的關鍵發現：

### 1. `system-ui` 字型不安全
macOS 上 Canvas 和 DOM 在不同字體大小解析 `system-ui` 到不同字型變體（SF Pro Text vs SF Pro Display），造成測量結果不一致。

### 2. 逐詞加總的精確度策略
Canvas 內部足夠一致，加總 segment 寬度效果很好。但在完整段落上微小差異會累積成行邊界誤差。解法是**語義前處理**（標點合併、trailing space hanging），而非 runtime 修正。

### 3. Emoji Canvas/DOM 寬度差異
Chrome/Firefox 在小字體下 canvas 測量 emoji 偏寬。透過自動偵測和快取修正解決。

### 4. 被拒絕的方法
- DOM 隱藏元素測量 — 重新引入 reflow
- SVG `getComputedTextLength()` — 效能不足
- Full-string verification in `layout()` — 違反零 DOM 原則
- Pair correction models — 準確度不足

### 5. Sebastian Markbage 的遺產
原始 text-layout 原型的直覺是正確的：word/run 為快取單位、瀏覽器為測量基準、串流式貪婪斷行。Pretext 在此基礎上加入了工程紀律。

## 作者的願景（thoughts.md）

Cheng Lou 的觀點：

- **80% 的 CSS 規範在使用者空間有更好的文字控制時可以避免**
- CSS 的便利性正在被侵蝕：更多 CSS 表達力帶來更差效能，而 AI 減少了對硬編碼 CSS 配置的需求
- **新的網頁瀏覽器引擎很難實現**，因為規範太龐大；唯一的出路是將更多能力交給使用者空間
- **可驗證軟體的成本將趨近於零**

這暗示 Pretext 不只是一個測量工具，而是 Cheng Lou 對「瀏覽器應該把什麼交給使用者空間」這個大問題的回答的第一步。

## 與替代方案比較

| 維度 | Pretext | 傳統 DOM 測量 | text-metrics 等 JS 庫 |
|------|---------|-------------|---------------------|
| **熱路徑成本** | ~0.0002ms 純算術 | 30ms+（interleaved reflow） | 仍需 DOM 或 canvas |
| **Resize 效能** | 極低 | 每次觸發 reflow | 多數無快取策略 |
| **i18n 支援** | 17+ 語言深度驗證 | 依賴瀏覽器 | 多數只支援拉丁文 |
| **手動排版** | 逐行變寬、繞障礙物 | 不可能 | 不可能 |
| **Bidi** | 有 metadata 支援 | 瀏覽器內建 | 多數無 |
| **Soft Hyphen** | 完整支援 | 瀏覽器內建 | 多數無 |
| **大小** | ~1.7 kB gzip | N/A | 各異 |

## 目前限制

- 目標 CSS 配置：`white-space: normal` + `word-break: normal` + `overflow-wrap: break-word` + `line-break: auto`
- `system-ui` 字型不安全
- 尚未支援 `break-all`, `keep-all`, `strict`, `loose`, `anywhere`
- 尚未支援 server-side 渲染（未來目標）
- 自動斷字（hyphenation）超出範圍

## 社群反應

> "Every website you've ever used has a problem you've never noticed, and it's been here for 30 years... a Midjourney engineer just fixed it." — Josh Kale

> "This is pure genius. Measuring and laying out text on the web without ever asking the browser." — Humi

三天內從 0 到 4,599 stars — Cheng Lou 的社群影響力與技術深度的雙重體現。
