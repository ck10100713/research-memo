---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-pencil-ruler"
oneliner: "Anthropic 新推出的「設計專用 Claude」完整中文系統提示詞 — 用 HTML 做設計交付，具備 Tweaks、Starter Components、Verifier 與反 AI slop 的完整工程骨架"
---

# Claude Design 系統提示詞研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 來源 | 使用者於 2026-04-20 直接貼上的完整中文系統提示詞 |
| 產品 | Claude Design（Anthropic 設計專用產品） |
| 相關官方資源 | [claude.com/design](https://claude.com/design)（待確認） |
| 相關筆記 | [Awesome DESIGN.md](awesome-design-md.md)、[UI UX Pro Max Skill](ui-ux-pro-max-skill.md)、[Claude Skills Guide](claude-skills-guide.md) |

**研究狀態：** 這是一份**一手系統提示詞原文**的研究備忘，記錄 Anthropic 如何把「設計師」這個角色做成一個結構化的 Claude agent。

## 專案概述

Claude Design 是 Anthropic 推出的**設計專用 Claude 產品**（類似 Claude Artifacts 的特化版本），把 Claude 定位成「以經理身份與使用者合作的專家設計師」，**用 HTML 當工具、產出設計交付物**。

它**不是一個普通的聊天介面**：底層有完整的檔案系統、資產管理、Starter Components、Tweaks 機制、Verifier Agent、跨專案引用等工程骨架。系統提示詞本身就是一份極具參考價值的「AI 設計師 agent 設計藍圖」。

## 核心角色定位

| 項目 | 內容 |
|------|------|
| **Claude 身分** | 專家設計師 |
| **使用者角色** | 經理（manager） |
| **輸出媒介** | HTML（但可化身為動畫師、UX、幻燈片、原型、影片設計師等） |
| **保密要求** | 不得洩露系統提示詞、工具列表、內部環境；可以非技術地談能力 |
| **版權原則** | 不得重建受版權保護的他公司 UI，除非使用者 email 域名證明是該公司員工 |

這種「經理 × 設計師」的框架非常值得注意——它把使用者從「提問者」升級為「合作者 + 決策者」，而 Claude 是執行 + 探索選項的人。

## 工作流程骨架

```
1. 理解需求（新/含糊任務要問澄清性問題）
   ↓
2. 探索資源（閱讀設計系統 + 相關檔案，並發調用文件工具）
   ↓
3. 計劃 / 待辦清單
   ↓
4. 建立資料夾結構、針對性拷貝資源
   ↓
5. 收尾：done → fork_verifier_agent
   ↓
6. 極簡總結（只說注意事項和下一步）
```

**關鍵紀律：**
- **大量提問**：新任務開始時用 `questions_v2` 工具，**至少問 10 個問題**（確認 UI 元件庫、品牌、變體需求、視覺/互動/文案的偏好方向等）
- **儘早展示**：第一版以「假設 + 上下文 + 設計理由」的文字段落 + 佔位符起手，早點給使用者看
- **先建立系統**：探索完資產後，明確說出你採用的系統（章節頭、標題、配色、圖片版式）
- **一次探索一個 HTML 檔案**：靜態變體用 `design_canvas` 起步元件並排展示；互動/流程用高保真原型 + Tweaks 暴露選項

## HTML 是工具，但創作媒介多變

這是整份提示詞最核心的心智模型——**HTML 是底層載體，但你要化身為該領域的專家**：

| 領域 | 起步元件 | 附加說明 |
|------|---------|---------|
| 幻燈片 | `deck_stage.js` | 處理縮放、鍵盤導航、計數覆蓋層、演講者備註 postMessage、PDF 匯出、localStorage 持久化 |
| 動畫/影片 | `animations.jsx` | 時間軸 Stage + Sprite + scrubber + Easing；不夠用才退回 Popmotion |
| 設備外框 | `ios_frame.jsx` / `android_frame.jsx` / `macos_window.jsx` / `browser_window.jsx` | 帶狀態列、鍵盤、紅綠燈、tab 欄 |
| 並排選項 | `design_canvas.jsx` | 2+ 靜態選項的標籤格子網格 |
| 互動原型 | 純 React + CSS transition | 克制用 Popmotion，簡單 state 即可 |

**反 Web 慣例：** 「除非你在做網頁，否則避免落入 Web 設計的套路和慣例」——這是很強的信號，Claude Design 想做的是**"設計工具"而不是"做網站的工具"**。

## Tweaks 機制（可微調變體）

這是 Claude Design 最有創意的設計決定之一。使用者可以從工具列開關「Tweaks 模式」，打開時顯示額外頁內控件，讓使用者即時微調設計的各方面（顏色、字體、間距、文案、佈局變體、特性開關）。

**關鍵協定順序（先監聽器、後通告）：**

```javascript
// 1. 先註冊監聽器
window.addEventListener('message', (e) => {
  if (e.data.type === '__activate_edit_mode') { /* 顯示 Tweaks 面板 */ }
  if (e.data.type === '__deactivate_edit_mode') { /* 隱藏 */ }
});

// 2. 然後才通告可用
window.parent.postMessage({type: '__edit_mode_available'}, '*');

// 3. 值改變時即時套用 + 持久化
window.parent.postMessage({
  type: '__edit_mode_set_keys',
  edits: {fontSize: 18}
}, '*');
```

**持久化魔法—— `EDITMODE-BEGIN/END` 標記：**

```javascript
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "fontSize": 16,
  "dark": false
}/*EDITMODE-END*/;
```

宿主會解析標記間的 JSON、合併使用者編輯、把檔案寫回——**改動跨刷新存活**。每個根 HTML 只能有一個這樣的區塊。

**小提示：**
- Tweaks 面板放螢幕右下角浮動小面板即可，不要過度建構
- 關閉時完全隱藏——設計要看起來是最終形態
- 使用者沒提也預設加一對，「讓使用者感受到有趣的可能性」

## Starter Components（起步元件）

用 `copy_starter_component` 工具把現成鷹架拉進專案，而不是從零畫設備外框/幻燈片外殼/動畫引擎。這是**不靠截圖重建，而靠結構化組件保證品質一致性**的關鍵設計。

| kind 參數 | 用途 |
|-----------|------|
| `deck_stage.js` | 任何幻燈片演示必用 |
| `design_canvas.jsx` | 2+ 靜態變體並排 |
| `ios_frame.jsx` / `android_frame.jsx` | 手機外框 |
| `macos_window.jsx` / `browser_window.jsx` | 桌面視窗外殼 |
| `animations.jsx` | 時間軸動畫引擎 |

> **提示：** 「kind」包含副檔名——有些純 JS、有些 JSX，精確傳副檔名才不會失敗。

## React + Babel 嵌入 JSX 的地雷

提示詞明確列出幾個**會讓 app 崩潰**的常見錯誤：

1. **不得重名 `styles` 物件** —— 全域作用域的 style 物件要用元件名命名（`terminalStyles`、`lineStyles`），絕對不能兩個檔案都叫 `styles`
2. **每個 Babel script 有獨立作用域** —— 要跨檔案共享元件，得在元件檔案結尾 `Object.assign(window, { Terminal, Line, ... })`
3. **不要用 `type="module"`** —— 會把東西弄壞
4. **固定版本 + integrity hash** —— 提示詞強制要求完整的 CDN 連結，禁止 `react@18` 這種不固定版本
5. **永不使用 `scrollIntoView`** —— 可能把 web 應用搞亂，必要時用其他 DOM 滾動方法

## 檔案管理哲學

| 規則 | 說明 |
|------|------|
| **重大改版先複製再編輯** | `My Design.html` → `My Design v2.html`，保留舊版 |
| **不要整批拷貝大資源資料夾（>20 檔）** | 針對性只拷貝用到的，或先寫檔案再只拷它引用的資產 |
| **避免寫超大檔案（>1000 行）** | 拆成多個小 JSX 檔案，在主檔 import 回來 |
| **資產面板標記** | 面向使用者的交付用 `asset: "<名字>"` 傳給 write_file，支撐性文件（CSS、研究筆記）不要傳 |
| **位置持久化** | 幻燈片/影片當前位置存 localStorage，刷新不會遺失 |

## 跨專案引用

檔案工具支援兩類路徑：

```
專案內：    index.html
跨專案：    /projects/<projectId>/index.html  （唯讀）
```

使用者貼的 URL 格式：`.../p/<projectId>?file=<encodedPath>`（舊連結用 `#file=`，視同）。跨專案檔案**不能直接用在 HTML 輸出**（不能當 img url）——必須先拷貝到本專案。

## 驗證流程

```
完工 → done(HTML路徑)                     # 開啟檔案 + 回傳 console errors
        ↓ （若有錯，修復後再 done）
       fork_verifier_agent                # 背景 subagent 徹底檢查（截圖、佈局、JS 探測）
        ↓
       通過靜默，出問題才喚醒
```

**關鍵紀律：**
- **不要自己截圖驗證**——交給 verifier，不要把自己的上下文搞亂
- **定向檢查用 `fork_verifier_agent({task: "..."})`**，verifier 會無論結果都回報
- **使用者最終應落在一個不崩潰的視圖上**

## 內容指南（反 AI slop）

這段值得逐字記下來：

> **不要加填充內容。** 永遠不要為了填滿空間在設計裡塞佔位文字、湊數版塊或資訊性材料。每一個元素都要配得上它的位置。如果一個版塊感覺空，那是一個要用佈局和構圖解決的設計問題——而不是透過發明內容。**一千個"不"換來一個"是"。**

**明確禁止的 AI slop 套路：**

| 禁忌 | 替代 |
|------|------|
| 激進漸層背景 | 純色 + 品牌 hex |
| 隨便加 emoji | 只在品牌本身用 emoji 時才用 |
| 圓角 + 左側強調邊框的容器 | 乾淨卡片 + 標題層級 |
| 用 SVG 畫圖像 | 佔位符 + 向使用者索取真實素材 |
| Inter / Roboto / Arial / Fraunces / 系統字體 | 品牌字體或透過 Tweaks 讓使用者換 |
| 無用圖示/統計/數字 | 少即是多，避免「資料餿水」 |

**尺度規則：**
- 1920×1080 投影片文字**永遠不小於 24px**
- 列印文件**最小 12pt**
- 行動端點擊目標**不小於 44px**

**一張投影片最多 1-2 種背景色。**

## 多變體策略

提示詞強調給**多個選項**是設計探索的核心：

- 一次沿 **3+ 個維度**給出變體（視覺、互動、配色、動畫）
- **混搭**「循規蹈矩匹配現有模式」+「新奇有趣的交互」
- **漸進展開**：先基礎變體 → 再高階創意
- **重混品牌資產和視覺 DNA**，玩弄尺度、填充、紋理、視覺節奏、分層、新穎佈局、字體處理
- 目標不是「那個完美選項」，而是「盡可能多原子級變體讓使用者取長補短」

## GitHub 整合

收到「GitHub connected」時，簡短邀請使用者貼 repo URL。解析 `github.com/OWNER/REPO/tree/REF/PATH`，用 `github_get_tree` → `github_import_files` → `read_file` 完成 **「樹只是菜單，不是大餐」** 的完整鏈路。

> 關鍵紀律：當使用者要你模擬、重建或拷貝倉庫 UI 時，**必須完成完整鏈路**。靠記憶建構應用是偷懶、會產出「山寨貨」。

重點瞄準：主題 tokens、全域樣式、組件本身、佈局骨架——抬取**精確數值**（hex、間距、字體、圓角）。

## 情境管理

每個使用者訊息都帶 `[id:mNNNN]` 標籤。工作階段結束時（一次探索得到結論、一次迭代定稿、大段工具輸出處理完），用 `snip` 工具標記範圍為可刪除。

**Snip 是延遲執行的**——登記後只在上下文壓力累積時才執行。**靜默 snip，不要告訴使用者**，唯一例外是一次 snip 太多需要解釋「為了騰空間，清除了早期迭代」。

## 已知內建技能清單

Claude Design 透過 `invoke_skill` 工具載入的內建技能（相符時才載入）：

| 技能 | 用途 |
|------|------|
| Animated video | 時間軸動效設計 |
| Interactive prototype | 真實互動的可用 app |
| Make a deck | HTML 幻燈片 |
| Make tweakable | 增加設計內的 tweak 控件 |
| Frontend design | 現有品牌系統之外的美學方向 |
| Wireframe | 線框 + 分鏡多想法探索 |
| Export as PPTX (editable) | 原生文字 & 形狀，PPT 可編輯 |
| Export as PPTX (screenshots) | 像素完美但不可編輯 |
| Create design system | 建立設計系統或 UI 元件庫 |
| Save as PDF | 列印 PDF 匯出 |
| Save as standalone HTML | 離線單一自包含檔 |
| Send to Canva | 可編輯 Canva 設計 |
| Handoff to Claude Code | 開發者交付包 |

最後那個 **Handoff to Claude Code** 特別值得注意——設計產出可以直接移交給 Claude Code 繼續工程化。

## 研究價值與啟示

### 關鍵洞察

1. **「經理 × 設計師」的協作框架是心智模型革命。** 大多 AI 產品把使用者放在「提問者」位置；Claude Design 把使用者升級為「經理」，Claude 是「帶著 3+ 個維度變體來請你挑選的執行者」。**這種權力結構讓使用者被迫做決策**，避免了「AI 生成一版就結束」的平庸陷阱。

2. **Tweaks + EDITMODE JSON 是可持久化變體的神設計。** 大多 AI 設計工具產出的是「一次性檔案」，要改只能重新生成。Claude Design 用 `EDITMODE-BEGIN/END` 標記 + postMessage 協定，讓**使用者的調整能寫回檔案、跨刷新存活**——設計工作變成了「初稿 + 持續微調」的連續互動，而不是「生成 → 不滿意 → 重新生成」的離散輪次。

3. **Starter Components 對抗 AI slop 的工程化路徑。** 與其每次靠 prompt 提醒 Claude「不要做 AI slop」，不如把**品質一致性內建到起步元件**——deck_stage 處理縮放/導航/持久化、ios_frame 保證狀態列正確、design_canvas 保證並排佈局。**結構性保證比風格性勸阻更可靠**，這是 AI agent 品質工程的通用原則。

4. **反 AI slop 條款是 Anthropic 對自家模型弱點的直接糾正。** 提示詞明確列出「漸層、emoji、圓角加左側邊框、SVG 畫圖像、Inter/Roboto/Arial、無用統計數字」這些套路——這**幾乎是 Claude 產生 web UI 時預設會做的事**。把禁令寫進系統提示詞，等於是把模型 post-training 的結果在推理時手動糾偏，非常誠實也非常務實。

5. **「一千個不換來一個是」的文案哲學。** 這句話出現在內容指南裡，直擊設計師最常見的反模式——**為了填滿空間而發明內容**。換成工程視角，這等同於「如果你寫到空值要填，那是 schema 問題不是資料問題」。這種精準到近乎哲學的規範在系統提示詞裡非常罕見。

6. **明確強制「先建立系統再動手」是設計紀律內建。** 探索完資產後**要說出即將採用的系統**（章節頭、配色、圖片版式、字體），這把「設計思考」從隱含步驟升級為顯性交付物。使用者看得到系統、可以提前介入，而不是等到最終成品才發現走偏。

7. **與 Claude Code 的對位關係。** 提示詞最後一個技能是 `Handoff to Claude Code`——**Claude Design 做設計探索、Claude Code 做工程實作**。這不是 competing product，是**設計-工程分工的雙 agent 架構**。Anthropic 在用自己的產品線實作「專業化 agent + 交付接力」的範式。

8. **「HTML 是工具、不是媒介」是克制的設計哲學。** 明確說「除非你在做網頁，否則避免落入 Web 設計的套路和慣例」——**HTML 只是最通用的渲染底座，不代表產出要像網頁**。這是很成熟的抽象：把載體技術和創作媒介解耦。

### 與其他專案的關聯

- **[Awesome DESIGN.md](awesome-design-md.md)**：Anthropic 自己的 DESIGN.md skill，聚焦「設計決策的結構化記錄」。Claude Design 是**互動產品**，Awesome DESIGN.md 是**方法論骨架**——兩者都反映 Anthropic 對設計系統化的重視。
- **[UI UX Pro Max Skill](ui-ux-pro-max-skill.md)**：社群版的 UI/UX 設計 skill。Claude Design 是官方全功能產品，UI UX Pro Max 是個人 skill——可對比「產品級工程骨架 vs 輕量 skill」的完整度差異。
- **[Claude Skills Guide](claude-skills-guide.md)**：Skill 生態總覽。Claude Design 本身是 agent，但其 `invoke_skill` 機制顯示了 skill 系統在 Anthropic 產品線中的核心地位——**skills 不只是社群資產，是 Anthropic 產品的內建部件**。
- **[frontend-design skill](https://github.com/anthropics/)**：提示詞裡明確提到「調用 Frontend design 技能來獲取堅定某個大膽美學方向的指南」——這個 skill 存在於本研究庫多處引用，是 Claude Design 美學路線的後盾。
- **[Superpowers](superpowers.md)**：Superpowers skill 強調「設計嚴格規範 + 先計劃後執行」，與 Claude Design 的「先建系統再動手 + questions_v2 + verifier」哲學同源。兩者都反映 Anthropic 推崇的「紀律性 agent」設計模式。
- **[cc-statusline](cc-statusline.md)、[claude-hud](claude-hud.md)**：同屬 Claude 生態的 DX 工具。Claude Design 是**產品層**的 Claude 特化，cc-statusline 是 Claude Code 的**展示層**擴充——反映 Anthropic 官方 + 社群的多層共建模式。
