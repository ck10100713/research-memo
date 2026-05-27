---
date: "2026-05-27"
category: "AI Agent 框架"
card_icon: "material-web"
oneliner: "Microsoft Research 極簡瀏覽器 agent 框架（~1.5k LoC），核心理念『coding agent + terminal』把瀏覽器當可拋棄環境、用 code-as-action 寫 Playwright 腳本，Online-Mind2Web 86.7% SOTA，可當 Claude Code/Codex skill"
---

# Webwright 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/microsoft/Webwright> |
| 官方 Blog | [Webwright: A Terminal Is All You Need For Web Agents](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/) |
| Project Page | <https://microsoft.github.io/Webwright/> |
| License | MIT |
| 作者 | Yadong Lu, Lingrui Xu, Chao Huang, Ahmed Awadallah (Microsoft Research) |
| 設計靈感 | [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) |

## 專案概述

**Webwright** 是 Microsoft Research 在 2026/04 開源的瀏覽器 agent 框架（~1.5k LoC，Python，1,799 stars），核心主張是標題那句 **「A Terminal Is All You Need For Web Agents」**。

它的關鍵反叛在於**重新定義「state」**：傳統 web agent（Stagehand、browser-use、Vercel agent-browser）都把「瀏覽器 session 本身」當成 workspace，每一步餵當前頁面狀態給 model、預測下一個 click/type/DOM selector——agent 被鎖在「一次預測一個 web action」的迴圈裡。Webwright 反過來，**把 agent 與瀏覽器分離**：瀏覽器只是 agent 可以「啟動、檢查、丟棄」的環境，真正持久的產物是 **本地 workspace 裡的 code 與 logs**。

換句話說，整個 web 任務的瀏覽歷史 = 一個可重跑的 Python 腳本檔案。沒有 multi-agent 系統、沒有 graph engine、沒有 plugin 層、沒有隱藏的 orchestration——只有一個 terminal、一個 browser、一個 model。這個立場正是它命名為 **Web + wright**（如 playwright「劇作家」、wheelwright「造輪匠」——「造 web 的工匠」）的由來。

## 核心理念：Code-as-Action

| 維度 | 傳統 web agent | Webwright |
|------|---------------|-----------|
| **Workspace** | 瀏覽器 session | 本地 code / screenshots / logs |
| **Action space** | 單一 click/type/selector | 自由形式 Python（自己寫 Playwright 腳本） |
| **Loop** | observe → 預測下一步 → 執行 → 重複 | 寫 code → 執行 → 看截圖 → 修復 |
| **瀏覽器角色** | 唯一狀態載體 | 可拋棄的環境，需要時才開 |
| **產物** | 一次性互動歷史 | 可重跑、可參數化、可分享的腳本 |

這帶來幾個好處：
- **Robust & reusable** — 用 query elements / wait conditions 取代脆弱的 pixel-level action，能處理 lazy loading、re-rendering 等動態行為
- **高效組合複雜流程** — 選日期、填表單變成一個 compact program，用 loop/function/abstraction 泛化到相似任務（不同日期不用重新預測整串低階序列）
- **更少互動回合、更少 long-horizon 錯誤累積**

## 效能（SOTA 結果）

兩個真實網站 benchmark，100-step 預算：

| Benchmark | 成績 | 備註 |
|-----------|------|------|
| **Online-Mind2Web (300 tasks)** | **86.7%**（GPT-5.4） | AutoEval 類別開源 harness 最高；Claude Opus 4.7 達 84.7%，hard split 上更強（80.5% vs GPT-5.4 76.6%） |
| **Odysseys (200 long-horizon tasks)** | **60.1%**（GPT-5.4，平均 76.1 步） | 比前 SOTA（Opus 4.6 vision-based 44.5%）**+15.6 分**，比 base GPT-5.4（xy-coordinate 33.5%）**+26.6 分** |

- **Code-as-action 完勝 coordinate prediction**：在所有難度切分都大幅超越重現的「GPT-5.4 screenshot + xy 座標」baseline
- **小模型 + 可重用工具**：生成的腳本可打包成參數化 CLI 工具，連 **Qwen-3.5-9B** 在備好 5+ 工具時也能在 Online-Mind2Web 完成任務

## 架構與依賴

```
webwright/
├── src/webwright/
│   ├── run/cli.py           # CLI entrypoint (~150 lines)
│   ├── agents/default.py    # 核心 agent loop (~450 lines)
│   ├── environments/        # Playwright browser workspace (~570 lines)
│   ├── tools/               # image_qa, self_reflection
│   ├── models/              # openai / anthropic / openrouter backends (各 ~150-200 行)
│   └── config/              # base.yaml, model_openai.yaml, model_claude.yaml
├── assets/task_showcase/    # Flask dashboard（可重複任務）
└── outputs/                 # run artifacts（trajectories、screenshots）
```

**零隱藏框架**——只依賴 `httpx`、`pydantic`、`playwright`、`typer`。Pluggable backend：OpenAI / Anthropic / OpenRouter。

## 快速開始

```bash
pip install -e .
playwright install chromium

python -m webwright.run.cli \
    -c base.yaml -c model_openai.yaml \
    -t "Search for flights from SEA to JFK on 2026-08-15 to 2026-08-20" \
    --start-url https://www.google.com/flights \
    --task-id demo_openai \
    -o outputs/default
```

## 當作 Claude Code / Codex / OpenClaw / Hermes Skill

Webwright 同時 ship 了 plugin manifest，可作為 host agent 的 skill——host agent **原生驅動** Webwright loop，不需額外 LLM API key 或費用（除了你的 host 訂閱）：

```text
# Claude Code
/plugin marketplace add microsoft/Webwright
/plugin install webwright@webwright
```

兩種 slash command 模式：
- **`/webwright:run`** — 產生 **one-shot** `final_script.py`，針對字面任務值
- **`/webwright:craft`** — 產生 **可重用 CLI 工具**：把 `final_script.py` 變成一個參數化 function（Google-style `Args:` docstring + `argparse` wrapper），之後可用不同參數重跑，例如 `python final_script.py --origin JFK --destination LAX --depart-date 2026-07-01`

同一份 `skills/webwright/` 資料夾可跨 **Claude Code / Codex / OpenClaw / Hermes** 載入（agentskills.io 標準）。能原生讀 PNG 截圖的 host 會跳過 `image_qa` / `self_reflection` 工具。

## 目前限制 / 注意事項

- **依賴 Playwright Chromium**——需安裝瀏覽器，非純 API
- **`/webwright:craft` 的 named subcommand 在 Hermes 失效**（`/webwright:run`、`:craft` 是 Claude Code/Codex 慣例，Hermes 中 inert，但 skill 本身仍可端到端運作）
- **效能高度依賴底層模型強度**——SOTA 數字來自 GPT-5.4 / Opus 4.7 這類前沿 coding model，弱模型表現會明顯下降（這也是設計前提：「models get stronger at code → 傳統 harness 變瓶頸」）
- **研究專案性質**——repo 較新（2026/04），生態與長期維護待觀察

## 研究價值與啟示

### 關鍵洞察

1. **「Workspace-as-state」是 web agent 的範式轉移**：絕大多數 web agent 把瀏覽器當唯一狀態載體，Webwright 把狀態移到本地 code/log。這個轉移直接解鎖了「可重跑、可參數化、可分享」——web 任務不再是一次性互動，而是像人類工程師迭代 RPA 腳本那樣的軟體產物。這是它能在 long-horizon 任務大幅領先的根本原因。

2. **「模型變強 → 舊 harness 變瓶頸」是個重要的趨勢判讀**：作者明說「那個一次預測一個 action 的 harness 在 LLM 較弱時有用，但模型越來越會寫和 debug code，同樣的 harness 就變成瓶頸」。這是對整個 agent 設計史的反思——很多 scaffold 是為了「補模型的不足」而生，模型補強後反而該拆掉 scaffold，讓模型發揮 code 能力。**減法設計**勝過加法。

3. **Code-as-action +26.6 分 over coordinate prediction 是強證據**：同一個 GPT-5.4，用「寫 Playwright 腳本」比「預測 xy 座標」在 Odysseys 高 26.6 分。這說明 LLM 在「結構化、可組合的程式空間」遠比在「連續座標空間」可靠——對任何在設計 action space 的人都是重要參考：**盡量把 action 設計成程式碼，而非低階指令**。

4. **「~1.5k LoC、零隱藏框架」的反平台立場**：核心 loop 單檔 ~450 行、environment ~570 行、CLI ~150 行，只依賴 4 個套件。這種極簡 = 可讀、可 debug、可 fork。對比那些把 agent loop 埋在層層抽象下的重量級平台，Webwright 證明 SOTA 不一定要靠複雜度。靈感來自 mini-swe-agent 的「最小 agent loop」哲學一脈相承。

5. **「生成腳本可打包成 CLI 工具，小模型靠工具補強」是個務實的 cost 策略**：用強模型（GPT-5.4）一次性生成參數化工具後，弱模型（Qwen-3.5-9B）靠這些工具也能完成任務。這是「強模型做一次性昂貴探索 → 固化成便宜工具 → 弱模型重複使用」的分層 cost 架構，與 `/webwright:craft` 的 reusable tool 模式呼應。

6. **「同一份 skill 跨四個 host」展現 agentskills.io 標準的價值**：同一個 `skills/webwright/` 資料夾能在 Claude Code、Codex、OpenClaw、Hermes 載入，host agent 原生驅動、不需額外 API 成本。這是 skill 作為「可攜帶能力單元」的範例——把一個 SOTA 能力一次寫好，分發到所有支援 skill 標準的 agent。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs Stagehand / browser-use / Vercel agent-browser | 三者皆「browser-as-state」一次一動作，Webwright 是唯一「workspace-as-state + code-as-action」，瀏覽器可拋棄 |
| vs [Browser-Bound MCP Flights](browser-bound-mcp-flights.md) | 同樣聚焦瀏覽器自動化（且都拿 Google Flights 當範例），但 BB-MCP 是 MCP server 工具導向，Webwright 是 code-as-action agent |
| vs [Lightpanda Browser](lightpanda-browser.md) | Lightpanda 是為 AI 設計的輕量無頭瀏覽器（底層引擎），Webwright 是上層 agent 框架，理論上可疊用 |
| vs [Superpowers](superpowers.md) | 都走「skill 跨 host 分發」路線，Superpowers 是通用工程紀律 skill，Webwright 是專精瀏覽器任務的單一強 skill |
| vs [OpenClaw](openclaw.md) / [Page Agent](page-agent.md) | OpenClaw 是可載入 Webwright 的 host 之一；都在探索 agent × 瀏覽器，但 Webwright 的差異化在 code-as-action 範式 |

**最大啟示**：Webwright 是 2026 年「減法 agent 設計」的代表作。當模型在 code 能力上越來越強，與其堆疊 multi-agent / graph engine / orchestration，不如**把瀏覽器降級成可拋棄環境、把 action space 升級成完整程式語言、把狀態放回本地 workspace**。它用 ~1.5k LoC 拿下 SOTA，是對「複雜度 = 能力」這個迷思最有力的反駁。
