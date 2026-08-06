---
date: "2026-08-06"
category: "量化交易"
card_icon: "material-bank"
oneliner: "Goldman Sachs 官方量化金融 Python 工具包：把 GS 自家衍生品定價／風險引擎、跨資產回測、時間序列分析包成統一 API；近期加碼官方 MCP server 與 agent skills"
tags:
  - quant
  - finance
  - mcp
  - skills
---

# GS Quant（gs-quant）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/goldmansachs/gs-quant> |
| 官方開發者文件 | <https://developer.gs.com/docs/gsquant/> |
| Marquee 平台頁 | <https://marquee.gs.com/welcome/our-platform/gs-quant> |
| PyPI | `pip install gs-quant` |
| DeepWiki（社群整理） | <https://deepwiki.com/goldmansachs/gs-quant/2-getting-started> |
| 第三方介紹 | [Medium — Coding Nexus](https://medium.com/coding-nexus/introducing-gs-quant-goldman-sachs-python-toolkit-for-quantitative-finance-feb3ad6911e1) |

> Metadata（研究當下）：**11,773 stars / 1,595 forks** · Python · Apache 2.0 · 建立於 2018-12-14（**老牌、非新專案**）· 最新 release `release-2.1.2`（2026-08-03）。Python 3.9+（MCP 功能需 3.10+）。

## 專案概述

**GS Quant 是 Goldman Sachs 官方維護的量化金融 Python 工具包**——由 GS 內部的 quant developers 打造、跑在「全球最強風險轉移平台之一」（GS Marquee）之上，號稱累積 25 年市場經驗。它的核心價值主張是:**把投行內部 sales / strategists / risk managers 每天在用的衍生品定價模型與分析工具,用統一的 Python API 開放出來**。

用途涵蓋:衍生品結構化(structuring)、交易、風險管理,以及純粹當統計/資料分析套件。功能面主要有四大塊——**時間序列分析、投資組合操作、風險與情境分析、回測**。

**它跟本站量化交易分類裡多數專案的定位完全不同**:這裡收錄的大多是學術論文實作(Kelly、DLP、drawdown control)或社群開源 agent(AI Hedge Fund、TradingAgents)。GS Quant 則是**唯一一個「機構券商把自家 production 定價引擎商品化」的工具包**——它不是在你本機重造一個定價模型,而是當作「GS 分析服務的 Python 前端」。

> ⚠️ **最關鍵前提**:大部分定價與風險計算並非在本機跑,而是**把 instrument 送到 GS 的 analytics service** 計算。要用這些 API 需要 **client id / secret**,而這些**只發給 Goldman Sachs 的機構客戶**。沒有 GS 帳號,能用的主要是不需連線的本地工具(部分 timeseries、資料結構),定價/風險/回測的核心價值拿不到。

## 核心架構與模組

`gs_quant/` 下的主要子模組:

| 模組 | 職責 |
|------|------|
| `instrument` | 各類衍生品物件(`IRSwap`、`IRSwaption`、FX、equity vol…),cross-asset |
| `markets` | `Portfolio`（把多個 instrument 當單一單位定價/分析）、`PricingContext`（定價脈絡:日期、市場資料、情境） |
| `risk` | 風險量測(measures)、敏感度、情境/shock 分析 |
| `backtests` | 回測引擎(`generic_engine`、`equity_vol_engine`、`predefined_asset_engine`)+ `strategy` / `triggers` / `actions` 的宣告式框架 |
| `timeseries` | 時間序列分析函式庫(可獨立當統計套件用) |
| `analytics` / `models` / `data` | 分析元件、模型、Marquee 資料集存取 |
| `markets` + `entities` | 資產/實體抽象 |
| `mcp` ★ | **新增**:FastMCP 打造的 MCP server + client,把 gs_quant 功能開放給 LLM agent |
| `skills` ★ | **新增**:內建 agent skills（SKILL.md 套件），可安裝進 `.claude/skills/` |

### 兩個招牌設計模式

**1. `resolve()` — 部分指定 → 服務端補完**

```python
from gs_quant.instrument import IRSwap
swap = IRSwap('Pay', '10y', 'USD')   # 只給方向/年期/幣別
swap.resolve()                        # 把 instrument 送到 GS 定價服務
print(swap.fixed_rate)                # 服務算出當前 par rate,例如 0.0345
```

你只指定 instrument 的一部分參數,`resolve()` 把其餘欄位(par rate、premium、forward points…)交給 GS analytics service 依當前 `PricingContext` 補齊。預設 in-place 改寫,`in_place=False` 回傳新副本。

**2. `PricingContext` — 用 context manager 控制「在什麼市場條件下定價」**

定價、風險、情境全部繞著 `PricingContext`(日期、市場資料快照、shock/scenario)運作,配合 `Portfolio` 可把一籃子 instrument 當單一單位一次定價、算風險。

### 回測框架:「一種描述回測的語言」

官方把 backtesting 定位成一個 **描述回測的 language**,強調三個特性:**(1) 直覺 (2) 跨資產、與 instrument 無關 (3) python native 可自由改寫擴充**。用 `strategy` + `triggers`（何時動作）+ `actions`（做什麼,如加倉/避險）宣告式組合,再交給對應 engine 跑歷史回放。

## ★ 新亮點:投行把量化平台接上 AI Agent

2026 年版本最值得注意的是 `gs_quant/mcp` 與 `gs_quant/skills` 兩個(標註 **Experimental** 的)新套件——這是**一家投資銀行主動把自家 quant 工具開放給 LLM agent** 的訊號。

**MCP server（`pip install gs-quant[mcp]`,需 Python 3.10+）**

- 用 [FastMCP](https://github.com/jlowin/fastmcp) 打造,**自動探索 (auto-discover) tools**、支援 **tag-based 過濾**、兩種認證策略(`local` / `passthrough`)。
- 附一個 client(one-shot CLI + 互動 REPL,走 streamable-HTTP transport),單一進入點 `python -m gs_quant.mcp <server|client|discover>`。
- 目前 tools 分三組:`data`、`marketview`、`users`(例:`current_user_info`、`whois`)。可用 `gs_quant` 的 Marquee OAuth 憑證啟動。
- 支援「寫自己的 tool」與「從別的 package 載入 tool」——是可延伸的 tool registry,不是寫死的一組。

**Agent skills（`python -m gs_quant.skills install`）**

- 內建 SKILL.md 套件,可裝進 `.claude/skills/`(`--global` → `~/.claude/skills/`;`--project` → 當前專案),供 Claude Code、GitHub Copilot 等讀取。
- Linux/macOS 用 **symlink** 指回 package 源碼——**升級 gs_quant 就自動更新 skill**;Windows 用複製、升級後要重跑 install。
- 目前隨附 `gs-quant-overview` skill,拆成 `pricing.md` / `measure.md` / `instruments.md` / `backtesting.md` / `datasets.md` / `results.md` 等漸進式檔案,教 agent 正確用 `GsSession`、建 portfolio、resolve instrument——本質是**把「怎麼正確呼叫這個 SDK」的知識打包給 agent**,降低 agent 亂用 API 的機率。

## 目前限制 / 注意事項

- **核心功能綁定 GS 機構帳號**:沒有 client id/secret,定價、風險、回測(需市場資料)、Marquee 資料集全都拿不到。這是它跟本站其他「開箱即跑」量化專案最大的差別——**對零售/個人開發者而言,可玩的部分有限**。
- **是「GS 服務的前端」而非獨立引擎**:定價邏輯在 GS 伺服器端,你看不到也改不了模型內部;可重現性、離線性、審計性都受此限制。
- **MCP / skills 標註 Experimental**:API、CLI、設定在未來版本可能變動,別押在 production。
- **資料/計算送到 GS**:instrument 與市場觀點會送到 GS analytics service,機密部位資訊的傳輸與合規須自行評估。
- **文件雙軌**:GitHub README 極簡,真正的 examples/tutorials 在 `developer.gs.com`,且很多要登入機構帳號才看得到完整內容。

## 研究價值與啟示

### 關鍵洞察

1. **「production 引擎商品化」是一條與開源重造不同的路**——本站量化分類多數專案在「用開源工具**重造**一個定價/優化模型」;GS Quant 反其道,把**已在跑真實交易的內部引擎**包成 API 賣給機構客戶。對比之下能看清:學術/社群專案的價值在**透明可改**,券商工具的價值在**權威市場資料 + production 級模型**,兩者受眾與信任來源完全不同。

2. **`resolve()` 模式體現「薄客戶端、厚服務端」的量化架構**——client 只描述 instrument 的意圖,真正的 par rate / 定價交給服務端。這跟 [[headroom]] 那種「本地優先、資料不外流」的哲學正好相反,反映**機構量化的現實**:定價模型與市場資料是券商的核心資產,不可能下放到客戶端。要學的是這個**責任邊界的切法**。

3. **回測被設計成一種「語言」而非一個函式**——用 strategy / triggers / actions 宣告式組合、cross-asset、可 python 擴充,這個「把回測當 DSL」的思路,比多數把回測寫死成一支迴圈的社群專案(如本站 [[quantdinger]]、[[stockstats]] 類)更有延展性,值得任何要做通用回測框架的人參考。

4. **★ 投行出官方 MCP + skills,是「機構級能力接上 agent 生態」的早期訊號**——把定價/資料能力包成 MCP tools、把「怎麼正確用 SDK」包成 agent skill,等於承認**未來很多量化操作會由 LLM agent 發起**。這跟本站 [[mattpocock-skills]]、[[claude-agent-sdk]] 記錄的 skill/agent 浪潮在**完全不同的產業**匯流,是「skills 不只是給 coding agent,也給 domain 專業工具」的具體案例。

5. **skill 用 symlink 隨套件版本走,是可抄的維運細節**——skill 檔 symlink 回 package 源碼,SDK 一升級 skill 自動同步,避免「文件與程式碼版本漂移」。對照 [[mattpocock-skills]] 的「subscribe vs fork」,GS 這招是第三種:**skill 生命週期綁定 SDK 版本**——最適合「skill 就是該套件的一部分」的情境。

6. **它同時是提醒:量化的護城河是資料與模型,不是程式碼**——gs-quant 程式碼全開源(Apache 2.0),但沒帳號幾乎沒用。這對想做量化工具的人是一記警鐘:**開源工具鏈很容易,難的是背後那個 25 年市場經驗的定價服務與資料**。

### 與其他專案的關聯

- **與本站量化交易分類多數專案的對照**:[[ai-hedge-fund]]、[[tradingagents]]、[[stockagent]] 是 agent 驅動的策略；[[quantdinger]]、[[stockstats]]、[[tejapi_python_medium_quant]] 是開源分析/回測；Kelly/DLP 系列是學術實作。GS Quant 是**唯一的「機構券商 production 工具包」**,補上了這個光譜缺的一角。
- **與 AI agent / skills 生態的交會**:`gs_quant/skills` 的 SKILL.md 機制與 [[mattpocock-skills]]、[[microsoft-skills]]、[[claude-skills-guide]] 同源；`gs_quant/mcp` 的 FastMCP 用法可與 [[mcp-for-beginners]] 對讀。這是「傳統金融基礎設施」與「agent 工具鏈」交會的鮮活樣本。
- **與 [[headroom]] 的架構哲學對比**:一個把運算/資料留在本地(隱私優先),一個把定價留在服務端(資產保護優先)——兩種截然不同的信任與責任邊界,適合並讀理解「什麼該放本地、什麼該放遠端」。
- **對台灣/零售開發者的現實提醒**:相較本站可直接跑的 [[tejapi_python_medium_quant]](TEJ 台股資料)等,GS Quant 對沒有機構帳號者門檻極高,列此以標明「機構工具 ≠ 個人可用」。
