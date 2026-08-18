---
date: "2026-08-18"
category: "Coding Agent 工具"
card_icon: "material-presentation-play"
oneliner: "本機優先的可編輯簡報 workspace，以 presentation.mdx 為單一真相源，內建 5 個 MCP workspace tool + 4 個專案內 Agent Skills，讓 Claude Code / Codex 用 revision-safe 的方式改 deck"
tags:
  - mcp
  - agent-skills
  - design
---

# OpenSlideX 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/zz41354899/open-slidex> |
| npm CLI | `npx open-slidex@latest init my-deck` |
| npm MCP server | `open-slidex-mcp`（v0.3.6） |

## 專案概述

**OpenSlideX** 是一套「open-source、local-first 的簡報製作工具」──每份 deck 就是**你自己掌控的一個資料夾**，資料夾裡的 `presentation.mdx` 是**單一真相源（single source of truth）**。沒有帳號、沒有雲端同步、沒有外部相依，所有內容都留在本機、可用 git 管、可用一般工具編輯。

它解的問題和 [Slide Editor](slide-editor.md) 是同一條線但打法不同：**AI 生第一版 deck 很強、但迭代很貴/很危險**。OpenSlideX 的答案是把 deck 定義成一個**結構化、agent 可安全操作**的 MDX 文件，再開一套 **MCP workspace tool** 讓 Claude Code / Codex 用「讀最小片段 → 改單一 slide → 帶版本號防覆寫 → 跑品質閘」的方式迭代，而不是把整份 deck 重灌進 context。

repo 2026-08-11 剛建、MIT、TypeScript、Node 22.12+、8 stars，monorepo（Vite + PostCSS）。它明說自己**獨立於商業產品 SlideX Cloud**：本 repo 含本機編輯器、Workbench、MCP runtime、filesystem-safe SDK、CLI、starter、範例與 contributor 工具；**排除**雲端認證/帳號/協作/計費/付費模板。等於是「把商業產品的本機 runtime 從原始碼重建成開源版」。

## Monorepo 結構

```
open-slidex/
├── packages/
│   ├── motion-doc/          # MotionDoc 的 parser / serializer / layout / export 引擎
│   ├── slidex-sdk/          # filesystem-safe SDK + CLI
│   ├── slidex-workbench/    # 本機 Workspace / 編輯器
│   ├── editor-ui/           # 公開編輯器入口（React + shadcn UI, MotionDocEditor.tsx）
│   ├── open-slidex-mcp/     # workspace-scoped MCP server（發到 npm）
│   └── open-slidex/         # CLI 套件（init / dev）
└── .agents/skills/          # 4 個專案內 Agent Skills（見下）
```

## 核心格式：MotionDoc MDX

每份簡報是一個 `presentation.mdx`，用 MotionDoc 標籤描述。從 `server.ts` 反推，目前**允許的 block 標籤**收斂成 7 個：

`Slide`、`Text`、`ImageBlock`、`VideoBlock`、`Chart`、`Table`、`Shape`

而且明確**移除了一批舊標籤**（`Card` / `Group` / `Icon` / `Metric` / `Notes` / `Stack` / `Title`）── 這是把「格式契約收窄」的動作:標籤越少、agent 越不會亂生、parser/QA 越好保證。

## 五個 MCP Workspace Tool

MCP server 對 agent 只開五個工具，把「選 deck → 讀 → 改 → 配圖 → 審」整條 workflow 收在裡面，敘事方向仍留在 skills、修改保有版本安全：

| Tool | 職責 | 關鍵設計 |
|------|------|----------|
| `open_slidex_workspace` | 選 deck | `action: list / select`，先列出再鎖定要操作的 presentation |
| `open_slidex_read` | 漸進式讀取 | 帶 `intent / knowledgeQuery / resourceCursor / resourcePath / slideIndex`──**只餵 agent 需要的片段**（單 slide、指定資源、知識查詢），不是整份塞 context |
| `open_slidex_edit` | 改 deck / slide | 帶 `expectedRevision`──**樂觀鎖**:版本對不上就回 `revision_conflict`，避免蓋掉別人/自己的並行修改 |
| `open_slidex_media` | 管媒體 | 內建 Unsplash「trusted images」下載、檔名正規化，圖片走可信來源而非任意 URL |
| `open_slidex_review` | 算圖 + 品質閘 | `scope: deck / slide`，渲染到 `dist/renders/`；品質不過回 `quality_gate_failed` |

`edit` 的 `expectedRevision` + `revision_conflict` 與 `review` 的 `quality_gate_failed` 是這套工具最值得記的兩點：**它把「agent 改結構化文件」這件事做成有版本、有閘門的交易**，而不是 blind overwrite。

MCP 以 `npx -y open-slidex-mcp mcp --project <root>`（或 `--workspace <root>`）啟動，支援 Claude Code、Claude Desktop、Codex。

## 四個專案內 Agent Skills

放在 `.agents/skills/`，每個 skill 同時帶 `SKILL.md` **和** `agents/openai.yaml`──**同一份 skill 同時給 Claude 與 Codex/OpenAI 吃**（就是 [mattpocock skills](mattpocock-skills.md) 記過的 `.agents/` 跨 agent 遷移格式）。skill 隨產品 repo 一起出貨、是 project-local 的:

| Skill | 內容 | references |
|-------|------|-----------|
| `slidex-deck-design` | input→story、敘事模式、視覺方向 | `narrative-patterns.md`、`source-to-story.md`、`visual-direction.md` + **5 份已驗證範例 deck**（`data-brief` / `editorial-story` / `product-launch` / `strategy-proposal` / `training-workshop`.mdx） |
| `slidex-mdx-authoring` | MotionDoc 撰寫規則 | `motiondoc-contract.md`、`media-and-data.md` |
| `slidex-motion-direction` | 動態/轉場方向 | `motion-patterns.md` |
| `slidex-deck-qa` | 交付前 QA | `review-matrix.md` |

四個 skill 剛好對齊四個階段:**design（構思故事）→ authoring（寫 MDX）→ motion（動態）→ QA（審查）**,和五個 MCP tool 的 review 閘互補。

## 快速開始

```bash
# 方案 A:獨立 deck
npx open-slidex@latest init my-deck

# 方案 B:跑整個 workspace（Vite HMR live preview）
git clone https://github.com/zz41354899/open-slidex.git
cd open-slidex && npm install && npm run dev
```

## 目前限制與注意事項

- **極早期**:2026-08-11 才建、8 stars、TypeScript monorepo，MCP 才 v0.3.6,格式契約還在收斂（剛砍掉 7 個舊標籤）。
- **格式綁死 MotionDoc**:不是泛用簡報工具,deck 必須是 `presentation.mdx` + 允許的 7 種 block,自由度換取的是 agent 可安全操作。
- **開源版 ≠ 完整產品**:雲端協作/帳號/計費/付費模板都不在這 repo,想要那些得走商業 SlideX Cloud。
- **Node 22.12+**:相對新的 runtime 要求。

## 研究價值與啟示

### 關鍵洞察

1. **「讓 agent 安全改結構化文件」的一個完整範本**:`open_slidex_edit` 的 `expectedRevision`（樂觀鎖 → `revision_conflict`）+ `open_slidex_review` 的品質閘（`quality_gate_failed`），把 agent 編輯做成**有版本、有閘門的交易**。對照 [Slide Editor](slide-editor.md) 用 regex 覆寫 + `.backups/` 當 safety net,OpenSlideX 走的是「型別化格式 + 交易式 MCP tool」這條更工程化的路。下次要讓 agent 改任何結構化資產(config、schema、文件),這組 pattern(最小讀取 + 版本鎖 + 品質閘)值得抄。

2. **漸進式 read = token 經濟**:`open_slidex_read` 用 `intent / cursor / slideIndex` 只餵需要的片段,和 slide-editor「元素級 prompt」是同一個底層教訓──**AI 迭代的成本槓桿在 context 粒度**。差別是 OpenSlideX 把這件事做進 MCP tool 的介面設計裡,而非靠人手動框選。

3. **`presentation.mdx` 作為「人 / git / agent」三方共用的介面**:MDX 既是人類可讀可手改、又是 agent 可 parse 可精準改、還天生 git-friendly。**單一結構化真相源**同時服務三種編輯者,是 local-first + agent-native 工具的關鍵設計選擇。

4. **skill 隨產品出貨、且跨 agent**:4 個 skill 放在 `.agents/skills/`、每個都附 `openai.yaml`,等於「這個產品怎麼用」的知識**跟著 repo 一起發、Claude 和 Codex 都能載**。加上每個 skill 帶 reference 範例 deck(5 份 verified mdx),是「用 skill 當產品說明書 + few-shot 樣板」的實作。

5. **open-core 的信任牌**:把商業產品的本機 runtime「從原始碼重建成 MIT 開源」,使用者可以完全本機、可審、可 fork,雲端功能才收費。這是 local-first 工具建立信任與分發的一種標準玩法。

### 與其他研究筆記的關聯

- **[Slide Editor](slide-editor.md)**:最直接的雙生對照。兩者都解「AI 生 deck、本機迭代」,但 slide-editor 是單檔 Python + regex 存檔 + 把 `claude`/`codex` CLI 當 backend;OpenSlideX 是 TS monorepo + MDX 格式 + MCP tool + Agent Skills。一個輕、一個工程化,適合並讀比較兩種取捨。
- **[Claude Design](claude-design.md)**:同屬「AI 從零生整份 deck」的上游生成端,OpenSlideX 補的是它下游的可編輯、可迭代、可 agent 操作。
- **[mattpocock skills](mattpocock-skills.md)**:`.agents/` 跨 agent(Claude + Codex)skill 格式的先例,OpenSlideX 把它落地成產品內建 skill。
- **[MCP CLI](mcp-cli.md)**:同樣圍繞 MCP 生態;OpenSlideX 示範「用最小的一組 workspace tool 把一整條 domain workflow 包成 MCP server」的設計。
