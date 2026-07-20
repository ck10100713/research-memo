---
date: "2026-07-20"
category: "Coding Agent 工具"
card_icon: "material-bridge"
oneliner: "從 Claude Code 驅動 Google Antigravity CLI (agy) — 靠 Gemini 抗反爬搜尋做雙軌查證 + 共享 system prompt"
tags:
  - claude-code
  - harness
  - prompt-engineering
---

# cc-to-antigravity-cli-bridge 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [github.com/yyu0310/cc-to-antigravity-cli-bridge](https://github.com/yyu0310/cc-to-antigravity-cli-bridge) |
| README（英/繁/簡） | repo 內 `README.md` / `README.zh-TW.md` / `README.zh-CN.md` |
| 研究 prefix | repo 內 `research-prefix.md` |
| IDE 版對應專案 | [claude-code-antigravity-ide-bridge](https://github.com/yyu0310/claude-code-antigravity-ide-bridge) |

**GitHub 數據**：19 stars、Shell 為主、MIT License、2026-07-16 建立（極新，僅 10 個檔案）

## 專案概述

cc-to-antigravity-cli-bridge 讓你**從 Claude Code 驅動 Google 的 Antigravity CLI（`agy`）**：用你的 Gemini 訂閱做搜尋與模型工作，與 Claude 搭配互補；共享同一份 system prompt；並可選擇用研究方法 prefix 提升 headless 回答品質。

它是同作者「CC harness bridge 系列」的第三個（Grok、Codex、Antigravity），也是 IDE 版 `claude-code-antigravity-ide-bridge` 的 **CLI 對應版**。定位很明確：**Claude Code 仍是日常主力，`agy` 是互補車道**，不是要取代 Claude 環境。

> 舊的 Gemini CLI 已於 2026-06-18 停用；現在的訂閱存取走 Antigravity CLI（`agy`）。

## 四個使用價值

| # | 價值 | 說明 |
|---|------|------|
| 1 | **抗反爬的搜尋**（核心） | Claude 的 `web_search`/`web_fetch` 常在有輕度反爬的頁面失敗；透過 `agy` 的 Gemini Pro 常常還搆得到。**Claude 空手而回時跑 Gemini 對照** —— 這個雙軌查證是最主要的日常價值 |
| 2 | **用掉你已經付費的 Gemini 額度** | 很多人還有 2025 promo 的 Gemini 學生年、或其他 Google 訂閱的 Pro/Flash。轉用 Claude 後那些額度常閒置，`agy -p` 把它變成一次性研究與輔助呼叫 |
| 3 | **Claude 旁邊多幾個模型** | `agy` 不只 Gemini，也能叫 Claude Sonnet 4.6 / Opus 4.6 做輕量輔助：第二意見、平行草稿、不想燒主 CC session 時的溢流 |
| 4 | **研究 prefix 提升 headless 品質** | 裸 `agy -p`（或 `grok -p`/`claude -p`）給的來源模糊、事實與意見混雜。`research-prefix.md` 是 model-agnostic 的短 prefix，要求多角度搜尋、標日期來源、decision-first 回答 |

## 快速開始

```bash
# 安裝（macOS Homebrew）
brew install --cask antigravity-cli
# 或官方腳本
curl -fsSL https://antigravity.google/cli/install.sh | bash

# 帶研究 prefix、乾淨 cwd（推薦）
scripts/ccagy.sh "best fried chicken in Taipei"
scripts/ccagy.sh "your question" "Gemini 3.5 Flash (High)"

# 原始一次性呼叫
agy -p "your question" --model "Gemini 3.1 Pro (High)"
```

- `ccagy.sh` 會掛上研究 prefix 並從 temp 目錄執行，讓專案 `AGENTS.md`/rules **不洩漏**進純研究查詢
- ⚠️ 登入時選「Login with Google」用有 Gemini 訂閱的帳號；**不要設 `GEMINI_API_KEY`** —— 有的話 CLI 會走 API 計費而非你的訂閱

### 共享 system prompt

`agy` 讀工作目錄的 `AGENTS.md`。把它 symlink 到既有的 `CLAUDE.md`，兩個工具共用一份：

```bash
ln -s CLAUDE.md AGENTS.md
```

### 可用模型（`agy models`）

| 模型 | Reasoning tiers |
|------|-----------------|
| Gemini 3.5 Flash | Low / Medium / High |
| Gemini 3.1 Pro | Low / High |
| Claude Sonnet 4.6 | Thinking |
| Claude Opus 4.6 | Thinking |
| GPT-OSS 120B | Medium |

## 目前限制 / 注意事項（刻意做成「薄橋」）

- **無 memory sync、無 hook adapter**：截至 2026-07，`agy` **沒有原生 memory API、也沒有公開的 hook schema**，所以拿不到姊妹作 [cc-to-grok-bridge](cc-to-grok-bridge.md) 那種 memory 同步與 hook 硬攔截
- **只有軟規則**：soft rules 放 `AGENTS.md`；`~/.gemini/antigravity-cli/brain/` 下的 per-conversation 狀態**不是**共享知識庫
- **不是 Claude 環境的替代品**：要完整 Claude 環境就用 Claude Code；這個 repo 只解決「更強的搜尋、用起閒置的 Gemini 訂閱、輕鬆多一個模型」
- **API key 陷阱**：誤設 `GEMINI_API_KEY` 會導致走 API 計費而非訂閱

## 研究價值與啟示

### 關鍵洞察

1. **「雙軌搜尋查證」是被低估的實用模式**——這個 bridge 最核心的價值不是換模型，而是**用第二個 agent 的搜尋能力補第一個的盲點**。Claude 的 web_fetch 撞反爬失敗時，Gemini Pro 常還搆得到。把「跨模型」當成**冗餘查證管道**而非單純換腦，對研究型任務是很紮實的可靠度提升。

2. **薄橋 vs 厚橋，取決於目標 harness 有沒有 API**——對照姊妹作 grok bridge（有 hook adapter + 三區 memory）與這個 antigravity bridge（只有 prompt 共享），差異不在作者偷懶，而在 **`agy` 目前沒有 memory/hook 的 API 可接**。這揭示跨 harness 移植的天花板由**目標平台開放多少擴充點**決定——沒有 hook schema，就不可能有硬攔截。

3. **「閒置訂閱貨幣化」是真實的使用者洞察**——鎖定「很多人有 2025 Gemini 學生年額度、轉用 Claude 後閒置」這個具體情境，把沉沒成本變成研究輔助。這種「不是叫你多付費、而是榨乾已付費資源」的定位，比多數要你再訂閱的工具更貼近真實使用者。

4. **research-prefix 作為跨模型可攜資產**——同一份 `research-prefix.md` 套 `agy -p`/`grok -p`/`claude -p` 三家，且有可測量的效果（同一 query、同一 Gemini 3.1 Pro：無 prefix 給模糊清單，有 prefix 給 decision-first + 標日期來源 + 事實/意見分離）。把 prompt 工程當成**跨模型資產**管理，是這整個 bridge 系列一致的哲學。

5. **CC 作為「編排中樞」的生態雛形**——Grok、Codex、Antigravity(CLI+IDE) 一整個 bridge 系列，共同指向一個模式：**以 Claude Code 為日常主力，按任務把子工作外包給最適合的 harness**（Gemini 搜尋、Grok hard-block、Codex 某些強項）。這比「單一 agent 全包」更像成熟團隊的分工。

### 與其他專案的關聯

- **姊妹作 [cc-to-grok-bridge](cc-to-grok-bridge.md)**：同作者、同「CC harness bridge」系列。Grok 版是**厚橋**（hook adapter 做真 hard-block + memory 三區同步），這個 Antigravity 版是**薄橋**（只共享 system prompt + 研究 prefix）。兩者並讀是理解「移植深度受目標平台 API 限制」的最佳案例
- **搜尋工具角度**：核心價值「抗反爬雙軌搜尋」與 OSINT / 研究型工具同屬「提升資訊取得可靠度」；可與站內深研究/情報類筆記對照
- **多模型編排**：`agy` 能同時叫 Gemini 與 Claude，與 [OpenAI Agents SDK](openai-agents-sdk.md)/[Claude Agent SDK](claude-agent-sdk.md) 的「多模型 provider」思路呼應，但層級更低——直接在 CLI 層做模型切換而非框架內
