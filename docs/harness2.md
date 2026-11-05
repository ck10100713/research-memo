---
date: "2026-11-05"
category: "AI Agent 框架"
card_icon: "material-sync"
oneliner: "Google Research 的遞迴 harness 優化框架：不動模型權重，每遇到新任務就自己改 prompt / skill / script / hook 再跑，沒有標準答案也能挑出更好的 harness，並把學到的教訓存成跨任務經驗庫"
tags:
  - harness
  - agent-framework
  - self-improvement
  - google
---

# Harness²（google-research/harness2）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [google-research/harness2](https://github.com/google-research/harness2) |
| 論文 | [Harness²: Recursive Agent Harnessing for an Open World（arXiv:2610.14224）](https://arxiv.org/abs/2610.14224) |
| 專案網站 | [harness2.github.io](https://harness2.github.io) |

| 指標 | 數值 |
|------|------|
| Stars / Forks | ~22.7K / ~2.3K（2026-11-05） |
| 建立 | 2026-10-06，最後 push 2026-11-02 |
| 版本 | 0.1.0 |
| 語言 | Python 3.12–3.13（核心零相依） |
| License | Apache-2.0（「不是 Google 官方產品」） |
| 核心碼 | `core/` + `substrate/` 約 6,800 行 |

## 一句話

**harness** 指模型外面那一整圈東西：system prompt、工具、記憶、skill、subagent、hook。Harness² 做的事是「讓 agent 自己改自己的 harness」，模型權重完全不動，而且**不需要評分標準或標準答案**就能判斷改得好不好。

這跟 [Anthropic Harness Design](harness-design-long-running-apps.md) 那種「人設計 harness」是互補的：那邊教你怎麼手工設計，這邊是把設計過程自動化。

## 兩層遞迴

```
任務 T 進來
 ├─ 任務層遞迴（Propose → Probe → Compose）
 │    1. 用目前 harness 跑 k 次 baseline（reference executions）
 │    2. Propose：改進者讀軌跡，提出兩種候選 harness
 │         INV = 怎麼「做事」（流程、工具使用、收尾檢查）
 │         DOM = 「專業知識」（交付物結構、決策規則、領域檢查點）
 │    3. Probe：每個候選 harness 在同一個任務上實際跑一次
 │    4. Compose：比對各次執行行為的差異，組出一個 refined harness
 │    5. Selection：把所有交付物匿名化、盲選一個提交
 └─ Harness 層遞迴
      Reflect：逐條判斷每個改動 helped / hurt / 無效 / confounded，
      最多寫一條可轉移的教訓（cue + lesson + evidence），
      連同採用的 harness 存進「該領域」的經驗庫，給下一個任務讀
```

重點是第 4 步的 **contrastive**：沒有 ground truth，所以靠「同一任務、不同 harness、行為哪裡分岔」來推論哪個改動有用。

### 平行 vs 循序

| 模式 | 做法 | 直覺 |
|------|------|------|
| `--mode parallel --k K` | 一次提 K 個 INV + K 個 DOM 候選，全部 probe 完，再做 K 個獨立 composition | 探索廣 |
| `--mode sequential --k K` | 跑 K 輪 Propose–Probe–Compose，每輪帶著上一輪的 harness 和累積證據 | 改得深 |

`k=1` 就是一步。論文說預算加大還會再進步。

## 可編輯的八個元件

system prompt、guardrails、memory、tool guidance、subagents、skills、scripts、plugins（hooks）。改進者只輸出「有改的部分」，沒寫的就繼承（omitted-is-inherited）。

執行器（substrate）支援 **OpenCode**（預設）和 **Codex**，差異全被抽成 `SurfaceSpec` 資料：always-on 檔路徑、字數上限、skill 目錄、hook 事件清單等，共用邏輯只寫一次（`harness2/core/tree.py`）。

## Prompt 設計裡值得抄的東西

這個 repo 最有價值的其實是 `harness2/core/prompts.py`（1,163 行），裡面幾條規則對自己寫 CLAUDE.md / skill 很有參考價值：

1. **把驗證過的事實直接寫進 harness，而不是只寫「怎麼找」**
   「workspace fact：A 檔的 HR 對應 B 檔的 HR Manager」比「join 前先對齊角色名稱」更有用，因為最難的那步已經被 baseline 跑出來了。但要標明「in this workspace」，跟通用流程分開。
2. **能做成具名元件就不要寫成 prose**
   skill / script / subagent 可以被下一個任務呼叫或複製；塞在 always-on 文字裡的段落每次都付 context 成本，而且搬不走。
3. **always-on 記憶要「加一條就刪一條」**
   有明確觸發條件的領域知識預設放 skill，只有每個任務都適用的短事實才放 always-on。
4. **`KEEP_BASE` 是合法答案**
   證據不支持的改動就是退步，花 context 卻沒換到任何東西。
5. **反省時偏好標 `confounded`**
   一個候選同時改了好幾個元件、或只有一次 rollout 撐著，就別硬說是哪個改動有效。「被選中」不等於「改動有效」，因為 selection 是盲選交付物，不看 harness。
6. **證據是資料，不是指令**
   候選 harness 裡的 script/plugin 只能當文字讀，不能執行，防 prompt injection。

教訓的粒度範例也寫得很好：「be thorough」太泛沒用；「費用 1/1 起調到 250」太窄不會再觸發；理想是「當文件依序做多個動作、其中一個會終止行為人的授權時，把終止動作排最後」。

## 實驗結果（README 自述）

三個專業 benchmark × 四種模型/harness 組合，**一步** Harness² 就讓 GLM-5 與 Gemini 3.5 Flash 超過各自的 base harness：

| Benchmark | 內容 | 最大提升 |
|-----------|------|---------|
| WorkBuddy-Bench | 辦公、網頁、程式 | +11.5 分 |
| JobBench | 專業工作 | +4.5 分 |
| LAB（Harvey） | 法律工作，1,143 題 | Partial pass +11.8 pp |

## 上手

```bash
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -e '.[render]'
harness2-demo --output runs/demo --k 2      # 不需要任何 API key，跑兩種模式的 deterministic demo
```

真的跑 benchmark 需要 Linux、Node 20+、gcloud（預設走 Vertex AI），WorkBuddy 要 Docker，LAB 要 Pandoc + Poppler：

```bash
cp .env.example .env    # 填 GOOGLE_CLOUD_PROJECT、HARNESS2_SOLVER_MODEL（OpenCode provider/model 格式）、HARNESS2_JUDGE_MODEL
harness2-setup lab && harness2-check --bench lab
harness2 --bench lab --k 1 --mode parallel --only-domains antitrust-competition --max-tasks 1
harness2-judge  --bench lab --k 1 --mode parallel
harness2-report --bench lab --k 1 --mode parallel
```

- `--dry-run` 先看會選哪些題，不花錢
- `--max-tasks` 是**每個 domain** 的上限，不是總數
- 重跑同一指令就會 resume；換模型或題目要換 `HARNESS2_RUNS_DIR`
- 改進者模型（`HARNESS2_IMPROVER_MODEL`）沒填就跟執行器同一個；proposer 通道支援 `opencode` 和 `claude_cli`

## 要注意的地方

- **網路沒鎖**：執行器可以上網，Codex 還把 sandbox 關了。官方自己承認驗證時有 Codex rollout 主動去 Hugging Face 把 JobBench 的 `RUBRICS.json` 抓下來。要比分數得自己在網路層擋 `huggingface.co`、`github.com` 等。
- **成本**：每個任務 = k 次 baseline + 2k 個候選 rollout + composition rollout + 改進者呼叫 + 選擇 + 反省，模型呼叫數量是單跑的好幾倍。
- **經驗庫按 domain 分**：同一 domain 的任務必須依序跑（後面的只能讀前面的），不同 domain 才能並行。
- **README 的模型名（GLM-5、Gemini 3.5 Flash）和數字是作者自述**，我沒有自己重現。

## 跟其他筆記的關係

- [Anthropic Harness Design](harness-design-long-running-apps.md)：人工設計 harness 的方法論
- [OpenHarness](open-harness.md)：一個 harness 的實作；Harness² 是優化 harness 的方法，兩者不同層
- [SkillOpt](skillopt.md)：同樣在做「自動優化 agent 外圍」，但聚焦在 skill 單一元件
- [OpenCode](opencode.md)：Harness² 的預設執行器
