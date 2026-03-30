---
date: "2018-12-18"
category: "Coding Agent 工具"
icon: "material-file-compare"
oneliner: "24.8K stars 的結構化 diff 工具，用 tree-sitter 解析語法樹，只顯示真正有意義的程式碼變動"
---
# Difftastic 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [Wilfred/difftastic](https://github.com/Wilfred/difftastic) |
| 官方手冊 | [difftastic.wilfred.me.uk](https://difftastic.wilfred.me.uk/) |
| 作者技術文章 | [Difftastic, the Fantastic Diff](https://www.wilfred.me.uk/blog/2022/09/06/difftastic-the-fantastic-diff/) |
| SemanticDiff 比較 | [SemanticDiff vs. Difftastic](https://semanticdiff.com/blog/semanticdiff-vs-difftastic/) |
| LinuxLinks 評測 | [difftastic - LinuxLinks](https://www.linuxlinks.com/difftastic-structural-diff-tool/) |

| 項目 | 數值 |
|------|------|
| Stars | 24.8K |
| Language | Rust |
| License | MIT |
| 建立日期 | 2018-12-18 |

## 專案概述

Difftastic 是一個**結構化 diff 工具**，與傳統逐行比對的 `diff` 不同，它透過 [tree-sitter](https://tree-sitter.github.io/) 將原始碼解析為語法樹（AST），在語法結構層級進行比對。這意味著它能理解哪些語法片段真正改變了，忽略無意義的空白和格式變動。

典型使用場景：

- **Code Review**：格式化（reformat）後的程式碼不會產生大量噪音 diff
- **重構檢查**：將表達式拆成多行時，difftastic 只顯示真正變動的部分
- **合併衝突視覺化**：v0.50+ 可直接解析 merge conflict markers 並 diff 兩邊衝突

## 核心技術架構

### 運作流程

```
原始碼檔案
    │
    ▼
語言偵測（副檔名 / shebang）
    │
    ▼
tree-sitter 解析 → 語法樹（CST）
    │
    ▼
轉換為 S-expression 表示
    │
    ▼
建構 DAG（有向無環圖）
    │
    ▼
Dijkstra 最短路徑演算法 → 最小 diff
    │
    ▼
終端機彩色輸出（side-by-side / inline）
```

### 演算法核心：圖論最短路徑

Difftastic 將結構化 diff 建模為**最短路徑問題**：

| 概念 | 說明 |
|------|------|
| 頂點（Vertex） | `(left_pos, right_pos)` 兩棵語法樹中的位置對 |
| 邊：刪除（Removal） | 推進左側位置，代表左側有新增項目 |
| 邊：新增（Addition） | 推進右側位置，代表右側有新增項目 |
| 邊：匹配（Match） | 同時推進兩側，S-expression 相同時成本最低 |
| 目標 | 最大化匹配數量 → 最小化 diff 大小 |

作者的關鍵洞見：「Diff 的目標其實是找出**沒有**變動的部分——匹配越多，diff 越小越易讀。」

### 效能最佳化策略

圖的大小為 O(L × R)，其中 L、R 是兩個 S-expression 的項目數。為控制複雜度：

1. **積極裁剪**：檔案邊界的未變動區段直接跳過
2. **惰性建構**：僅在需要時建構圖的頂點
3. **巢狀深度限制**：限制每個位置對最多兩個頂點，避免 O(2^N) 爆炸
4. **降級回退**：圖太大時退回行導向 diff + word highlighting

## 語言支援

支援 **60+ 程式語言**和**結構化文本格式**，透過 `difft --list-languages` 查看完整清單。

| 類別 | 代表語言 |
|------|---------|
| 系統語言 | C, C++, Rust, Zig, Go |
| 腳本語言 | Python, JavaScript, TypeScript, Ruby, Lua |
| JVM 語言 | Java, Kotlin, Scala |
| 函數式語言 | Haskell, Elixir, Scheme, Lisp, OCaml |
| 標記/設定 | HTML, CSS, JSON, YAML, TOML, XML, LaTeX |
| 其他 | SQL, Solidity, VHDL, Nix, HCL |

未識別的副檔名會自動退回行導向 diff + word highlighting。

## 快速開始

### 安裝

```bash
# macOS
brew install difftastic

# Cargo (Rust)
cargo install difftastic

# Arch Linux
pacman -S difftastic
```

### 基本使用

```bash
# 比對兩個檔案
difft old.py new.py

# 解析 merge conflict
difft file_with_conflicts.js

# 僅檢查是否有語法變動（不產生 diff）
difft --check-only --exit-code before.js after.js
```

### 整合 Git

```bash
# 設為 Git 預設外部 diff 工具
git config --global diff.external difft

# 或用環境變數臨時啟用
GIT_EXTERNAL_DIFF=difft git diff
GIT_EXTERNAL_DIFF=difft git log -p
GIT_EXTERNAL_DIFF=difft git show HEAD
```

### 環境變數

| 變數 | 說明 |
|------|------|
| `DFT_BACKGROUND` | `light` / `dark`，解決 Solarized 等主題顏色問題 |
| `DFT_PARSE_ERROR_LIMIT` | 允許的 parse error 數量上限（預設 0，建議設 `20`） |

## 目前限制 / 注意事項

| 限制 | 說明 |
|------|------|
| **效能** | 大量變動的檔案處理較慢、記憶體用量高（O(L×R) 圖） |
| **不產生 patch** | 輸出僅供人類閱讀，無法生成可套用的 patch 檔 |
| **不做 merge** | AST merge 是另一個難題，可參考 [mergiraf](https://mergiraf.org/) |
| **不處理重排** | `set(1, 2)` vs `set(2, 1)` 仍會顯示差異 |
| **字串比對** | 字串是語法原子，無法做 word-level diff |
| **Python 縮排** | 無法偵測 Python 縮排變化 |
| **parse error** | 遇到語法錯誤時退回行導向 diff（保守但安全） |

## 研究價值與啟示

### 關鍵洞察

1. **「什麼沒變」比「什麼變了」更重要**：Difftastic 的核心設計哲學是最大化匹配——找出不變的部分後，變動自然浮現。這個思路適用於許多比對問題，不僅限於程式碼。

2. **tree-sitter 生態的乘數效應**：Difftastic 不自建 parser，而是直接利用 tree-sitter 社群維護的 60+ 語法定義。這讓一個人的 side project 能覆蓋所有主流語言，展示了開源生態系統的槓桿效果。

3. **圖論在日常工具中的實戰價值**：將 diff 問題轉化為 Dijkstra 最短路徑，是一個優雅的建模範例。作者坦言：「我一直好奇為什麼這類工具這麼少見。現在我知道了——它極其難做。」這揭示了看似簡單的開發者工具背後的演算法深度。

4. **務實的降級設計**：未知語言退回 word-level diff、parse error 退回 line-level diff、圖太大退回傳統 diff。三層 fallback 確保工具永遠能用，不會因為「太聰明」反而壞掉。這是工程上很好的韌性設計模式。

5. **對 Coding Agent 的啟示**：在 AI coding agent 的工作流中，diff 是核心操作——code review、patch 驗證、merge conflict 解析都依賴 diff 品質。結構化 diff 能大幅減少 token 浪費在無意義的格式變動上，值得整合到 agent 的工具鏈中。

### 與其他專案的關聯

- **Lightpanda Browser**：同樣用非主流語言（Zig vs Rust）從零打造高效能開發者工具，展示系統語言在 DevTools 領域的優勢
- **Claude Code / Coding Agent 工具鏈**：`GIT_EXTERNAL_DIFF=difft` 可直接整合到 coding agent 的 Git 工作流中，提升 diff 可讀性
- **GitHub Copilot CLI**：兩者都是增強開發者 CLI 體驗的工具，但一個用 AI、一個用演算法，互補而非競爭
