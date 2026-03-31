---
date: "2026-03-31"
category: "Coding Agent 工具"
card_icon: "material-file-search-outline"
oneliner: "Claude Code v1.0.33 靜態逆向工程——50,000 行混淆碼拆解為 102 chunks，揭示 h2A 消息隊列、6 層權限驗證、92% 閾值上下文壓縮"
---
# Analysis Claude Code 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [ThreeFish-AI/analysis_claude_code](https://github.com/ThreeFish-AI/analysis_claude_code) |
| 作者 | ShareAI-Lab (@baicai003) |
| 靈感來源 | [Yuyz0112/claude-code-reverse](https://github.com/Yuyz0112/claude-code-reverse) |
| 授權 | Apache-2.0 |

## 專案概述

| 指標 | 數值 |
|------|------|
| Stars | 259 |
| Forks | 101 |
| 語言 | JavaScript |
| 分析版本 | Claude Code v1.0.33 |
| 建立日期 | 2025-08-18 |

這是 ShareAI-Lab（也是 learn-claude-code 的作者）對 Claude Code **混淆原始碼的靜態逆向工程**研究。將 50,000 行混淆程式碼拆解為 102 個 chunks，用 LLM 輔助分析，再進行多輪交叉驗證。

### 與 claude-code-reverse 的方法對比

| 維度 | claude-code-reverse (v2) | analysis_claude_code |
|------|:---:|:---:|
| 方法 | Runtime Monkey Patch | 靜態程式碼分析 |
| 觀察對象 | API 請求/回應 | 混淆後的 JS 原始碼 |
| 優勢 | 直接看到 LLM 對話 | 看到內部實作細節 |
| 劣勢 | 看不到內部邏輯 | 混淆導致分析困難 |
| 準確性 | 100%（實際數據） | ~95%（作者自評） |
| 適合場景 | 理解 Agent 行為 | 理解系統架構 |

## 分析方法論

### 第一階段：靜態程式碼分析

```bash
# 1. 美化混淆程式碼
node scripts/beautify.js source/cli.mjs

# 2. 智能分塊（102 個 chunks）
node scripts/split.js cli.beautify.mjs

# 3. LLM 輔助逐 chunk 分析
node scripts/llm.js chunks/

# 4. 三輪迭代 + 交叉驗證
```

### 第二階段：動態行為驗證

- 函式呼叫追蹤
- 狀態變化監控
- 效能指標收集
- 邊界條件測試

## 核心技術發現

### 1. h2A 雙重緩衝異步消息隊列（Real-time Steering）

```
訊息到達
    │
    ├── 有等待中的讀取者？ → 零延遲直接傳遞（Zero-copy path）
    │
    └── 無讀取者？ → 存入循環緩衝區 + 背壓控制
```

- Promise-based 異步迭代器
- 吞吐量 > 10,000 訊息/秒
- 真正的非阻塞異步處理

### 2. 分層多 Agent 架構

| Agent 類型 | 混淆代號 | 職責 |
|-----------|---------|------|
| 主 Agent | nO | 核心任務調度、主循環引擎 |
| Sub Agent | I2A | 子任務代理、隔離執行環境 |
| Task Agent | — | 專用任務處理器、支援並發 |

每個 Agent 有獨立的權限範圍和資源存取控制。

### 3. 6 層權限驗證

```
UI 輸入驗證 → 消息路由驗證 → 工具呼叫驗證
    → 參數內容驗證 → 系統資源存取 → 輸出內容過濾
```

### 4. 智能上下文壓縮

- **92% 閾值**自動觸發壓縮
- wU2 壓縮器，智能保留關鍵資訊
- 保留比例 0.3（保留 30% 的原始內容）
- 重要性評分 + 內容篩選

### 5. 工具執行 6 階段管道

```
工具發現/註冊 → 參數驗證/類型檢查 → 權限驗證/安全檢查
    → 資源分配/環境準備 → 並發執行/狀態監控 → 結果收集/清理回收
```

- 最大 10 並發
- 每個工具獨立的錯誤處理域

### 驗證結果

| 維度 | 準確性 | 置信度 |
|------|--------|--------|
| 核心架構設計 | 95% | 高 |
| 關鍵機制實作 | 98% | 極高 |
| API 呼叫鏈路 | 92% | 高 |
| 安全機制 | 90% | 中高 |
| UI 互動機制 | 85% | 中 |

## 目前限制 / 注意事項

- **非 100% 準確**：作者自己強調「CC 多少會有幻覺」——用 LLM 分析混淆碼本身就可能產生幻覺
- **版本鎖定**：分析基於 v1.0.33，Claude Code 持續更新
- **混淆代號不穩定**：`nO`, `h2A`, `wU2` 等代號會隨版本改變
- **偏簡體中文**：文件以簡體中文撰寫

## 研究價值與啟示

### 關鍵洞察

1. **「用 LLM 分析 LLM 產品」的後設趣味**：用 Claude Code 自己分析自己的混淆碼，有一種後設的荒誕感。但這也證明了 LLM 在程式碼分析任務上的實際能力。

2. **92% 閾值是個重要的工程數字**：上下文用到 92% 時觸發壓縮，不是 80% 也不是 95%——這個數字背後有 Anthropic 的經驗值，太早壓縮浪費 context，太晚壓縮可能來不及。

3. **6 層安全架構的啟示**：從 UI 到輸出的完整安全鏈，每一層都有獨立的驗證邏輯。這對任何 Agent 產品的安全設計都是參考。

4. **靜態分析 vs Runtime 分析互補**：靜態分析看到內部實作（h2A 消息隊列、wU2 壓縮器），Runtime 分析看到行為（prompt 內容、模型分工）。兩者結合才是完整的逆向。

5. **開源重建 SOP 的價值**：`work_doc_for_this/` 資料夾提供了完整的逆向工程 SOP，從第一階段靜態分析到第二階段重建，方法論本身就值得學習。

### 與其他專案的關聯

- **claude-code-reverse**（`docs/claude-code-reverse.md`）：Runtime 方法互補，兩者結合更完整
- **Learn Claude Code**（`docs/learn-claude-code.md`）：同一作者（ShareAI-Lab），analysis 是「拆解」，learn 是「重建」
