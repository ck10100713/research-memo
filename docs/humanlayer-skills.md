---
date: "2026-09-07"
category: "Coding Agent 工具"
card_icon: "material-toy-brick"
oneliner: "YC 新創 HumanLayer(12-factor agents、Advanced Context Engineering、CodeLayer 的同一批人)公開的 5 個 Claude Code plugin。不是大雜燴 skill 包,而是把自家「context engineering」哲學做成可安裝範本:improve-claude-md 用 `<important if>` 區塊救 CLAUDE.md、narrow-react-prop-types 收窄 React prop 型別、show-me 最小視覺化解說,以及兩個招牌——build-iterated-agentic-loop 與 design-control-loop,用控制理論(sensor/controller/actuator)幫你蓋出「排程跑、每次只開一個 PR、人站在迴圈外掌舵」的自動化 coding agent。每個 plugin 只包一個 skill,repo 本身就是一個 Claude Code marketplace,也能 npx skills add"
tags:
  - claude-code
  - skills
  - plugins
  - humanlayer
  - context-engineering
---

# humanlayer/skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/humanlayer/skills> |
| 作者/公司 | **HumanLayer**(GitHub org,YC 新創)· 官網 <https://humanlayer.dev> · support@humanlayer.dev |
| 主要貢獻者 | `dexhorthy`(Dexter Horthy,CEO/共同創辦人,提出「context engineering」一詞)、`K-Mistele`(Kyle Mistele,CTO/共同創辦人) |
| 同門作品 | [12-factor agents](https://github.com/humanlayer/12-factor-agents)、[Advanced Context Engineering for Coding Agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)、**CodeLayer**(HumanLayer 的 coding agent harness / 多人協作 IDE) |
| 安裝器 | skills.sh — `npx skills add humanlayer/skills --skill <名稱>` |

> Metadata(**2026-09-07** 即時抓取,取自 GitHub API 與 `git clone`):**3,320 stars / 98 forks / 7 open issues / subscribers 7** · **MIT**(有明確 LICENSE,©2026 HumanLayer)· 建立於 **2026-03-18**,最後 push **2026-08-13** · **4 個分支**(`main` + `helptext`、`run-ec2-daemon`、`show-me-tree-glyphs` 三個工作分支)· **僅 12 commits / 2 位 contributor**(dexhorthy 8、K-Mistele 4)· **無 release、無 tag** · repo size 僅 **66 KB** · GitHub 標主語言 **TypeScript(11.8 KB)**。整包只有 **5 個 plugin**,每個 plugin 只包 **1 個 skill**——這是一份**小而精、拿來 dogfood 自家理念**的展示集,不是動輒幾十個的大 skill 倉庫。

!!! warning "四個要先校正的判讀"
    - **「TypeScript 專案」是假象**:GitHub 語言長條圖 100% TypeScript,但全 repo 唯一的 `.ts` 是 `agent-iteration.ts`(`/iterate` 留言的輔助腳本,而且在兩個 plugin 裡各放一份=同一支複製兩次)。**skill 的本體全是 Markdown(SKILL.md)**,語言統計完全看不出這是一份 agent skill 集。
    - **「plugin」≠「skill」,這裡是 1:1 包裝**:repo 用了 Claude Code 的 **plugin/marketplace** 機制。`plugins/` 下每個資料夾是一個 *plugin*(有 `.claude-plugin/plugin.json`),裡面 `skills/<名>/SKILL.md` 才是真正的 *skill*。這 5 個 plugin **各自只包一個同名 skill**,沒有 command / agent / hook——所以 plugin 在這裡純粹是「讓 skill 能上 marketplace 的外殼」。
    - **這不是 Superpowers / mattpocock 那種「工作流全家桶」**:只有 5 個 skill,其中 2 個(improve-claude-md、narrow-react-prop-types)是很具體的小工具,3 個(show-me + 兩個 loop builder)是把 HumanLayer 方法論做成範本。**看它的重點是「設計理念」而非「數量」**。
    - **安裝有兩條路,但 README 只寫了一條**:README 只教 `npx skills add`(skills.sh);可是 repo 根目錄其實有 `.claude-plugin/marketplace.json`,代表它**同時也是一個 Claude Code plugin marketplace**,可以走原生 `/plugin` 機制安裝(見下)。

## 專案概述

**humanlayer/skills** 是 AI agent 新創 **HumanLayer** 公開出來的一小撮 Claude Code skills。HumanLayer 這家公司值得先交代清楚,因為這份 repo 幾乎是它整套世界觀的縮影:

- 公司由 **Dexter Horthy(dexhorthy)** 創辦,他就是紅遍 AI engineering 圈的 **[12-factor agents](https://github.com/humanlayer/12-factor-agents)**(「怎麼把 LLM 應用做到能真的上 production」的 12 條原則)與 **Advanced Context Engineering for Coding Agents(ACE / RPI:Research → Plan → Implement)** 的作者,也是把「**context engineering** 比 prompt engineering 更貼切」講法推紅的人。
- HumanLayer 最早的產品是給 AI agent 加「**human-in-the-loop** 人工核准」的 API/SDK;後來往 coding 工具延伸,做出 **CodeLayer**——官網現在自稱「**The multiplayer control plane for your software factory**」的多人協作 coding agent 工作台,slogan 是「**Do not outsource the thinking**」「Ship Fast Without Sacrificing Quality」。這兩位 contributor(dexhorthy、K-Mistele)就是公司的 CEO 與 CTO。

所以這份 skills repo 不是「社群收集的 skill 大全」,而是**一家把 context engineering 當招牌的公司,把自己每天在用的幾個 skill 拿出來開源**——而且其中兩個招牌 skill,骨子裡就是 12-factor agents / ACE 那套「小步、可審查、人掌舵」哲學做成的可安裝範本。

repo 結構乾淨到極點:

```text
skills/
├── .claude-plugin/
│   └── marketplace.json         # ← repo 本身就是一個 Claude Code marketplace(列 5 個 plugin)
├── LICENSE                      # MIT © 2026 HumanLayer
├── README.md                    # 只教 npx skills add
└── plugins/
    ├── improve-claude-md/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/improve-claude-md/SKILL.md
    ├── narrow-react-prop-types/
    │   └── skills/narrow-react-prop-types/{SKILL.md, references/…}
    ├── build-iterated-agentic-loop/
    │   └── skills/build-iterated-agentic-loop/{SKILL.md, references/…}
    ├── design-control-loop/
    │   └── skills/design-control-loop/{SKILL.md, references/…}
    └── show-me/
        └── skills/show-me/SKILL.md
```

## 六個看點

### 1. `plugins/` 到底有哪五個 plugin(逐一拆解)

**這是本篇重點。** 五個 plugin 大致分成「兩個具體小工具 + 一個解說工具 + 兩個招牌 loop builder」:

| plugin(= 同名 skill) | 版本 | 一句話用途 |
|---|---|---|
| **`improve-claude-md`** | 1.0.0 | 用 `<important if="條件">` XML 區塊改寫 CLAUDE.md,提升指令遵從度 |
| **`narrow-react-prop-types`** | 1.0.0 | 把 React 元件 prop 型別收窄到「實際 live code path」用到的形狀,不遷就 Storybook/測試/mock |
| **`show-me`** | 1.0.1 | 用最小的圖(pseudocode/呼叫樹/元件樹/檔案樹/Mermaid/diff/HTML)把當前主題視覺化解釋 |
| **`build-iterated-agentic-loop`** | 1.0.0 | 把「可重複的 agent 任務」做成 repo 內 skill + 排程 GitHub Actions 工作流(iterated agentic loop) |
| **`design-control-loop`** | 1.0.0 | 用控制理論訪談式設計一套「小步、低風險、可審查」推進 codebase 的 agentic 控制迴圈,再幫你蓋出來 |

**① `improve-claude-md`——把「context engineering」做成一個 skill(最有記憶點)**

它的 SKILL.md 開宗明義點破一個很多人踩過的坑:Claude Code 對每份 CLAUDE.md 都會注入一段 system reminder——

> *「this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.」*

(順帶一提:**這段 reminder 就是本筆記自己 context 裡也看得到的那一段**,不是它瞎編的。)結果就是:CLAUDE.md 裡越多「跟當前任務無關」的內容,Claude 越傾向**整份都忽略**,連該遵守的也一起丟。

它的解法是把「只在特定情境才相關」的段落包進 `<important if="條件">` XML 標籤——刻意複用 Claude Code **自家 system prompt 就在用的 XML 標籤模式**,給模型一個明確的相關性訊號,穿透「可能相關可能不相關」的模糊框架。原則整理得很到位,值得任何寫 CLAUDE.md 的人抄:

- **地基 context 裸放,領域規則才包**:專案身分、目錄地圖、技術棧(≈90% 任務都要用)留成純 Markdown 放最上面;測試/API/狀態管理/i18n 這類只在特定工作才用到的,才各自包一個 `<important if>`。
- **條件要窄、要具體**:反例是 `if="you are writing or modifying any code"`(等於沒條件);正解是每條規則自己的窄觸發,例如 `if="you are adding or modifying imports"`、`if="you are creating new components"`。
- **Less is more**:能被 linter / formatter / pre-commit hook 擋的規則一律砍;能從既有程式碼 pattern 推斷的也砍(LLM 是 in-context learner);程式碼片段砍掉改成檔案路徑引用(會過期又肥)。
- **指令別分片到別的檔**:`<important if>` 的重點就是**全部 inline、但條件加權**——agent 一次看到全部,只對符合的段落用心。

SKILL.md 還附了一個完整的 before/after 範例(Turborepo monorepo 的 CLAUDE.md),示範怎麼把一坨 Coding Standards 拆成分條 block、哪些該刪、哪些要留(所有 command 一定保留)。

**② `narrow-react-prop-types`——很具體的 TypeScript 收型別工具**

情境:一個 React 元件的 props 為了 Storybook / mock / 測試被放寬,結果型別能表達出「線上程式根本不會進入」的狀態。這個 skill 的信條是:**以 live code path(app route、被實際接線的元件、provider、hook、production export)為 prop 契約的唯一 source of truth**,讓 stories/tests 去適應嚴格型別,而不是反過來為了測試好寫就把型別放鬆。它有 11 步 workflow + review checklist + anti-patterns,細到教你用 `Parameters<typeof fn>[0]`、`Extract<Union, Shape>` 去 derive 型別、把 `onRename?.(...)` 收成 `onRename(...)`、拿掉 `?? []` 這種防禦性 fallback。**注意它綁 HumanLayer 自家 monorepo**(驗證指令直接寫 `bun --bun run typecheck --filter <package>`)。它同時也是下面兩個 loop builder 拿來當「這才叫一個好 loop」的具體參考範例。

**③ `show-me`——最小視覺化解說**

一個純溝通用的 skill:要 Claude 用「能講清楚重點的最小視圖」解釋當前主題,並列了一整套形式讓它挑——pseudocode、呼叫樹、元件樹(含 state / 模組邊界)、淺層檔案樹、Mermaid 圖、`diff`(當重點是「改了什麼」時),真的太密才寫一個 focused HTML artifact 再 `open` 給你看。收尾特別叮嚀「你可能用其中一種、也可能用幾種,但不太可能全用——別淹沒使用者」。

**④⑤ 兩個招牌:`build-iterated-agentic-loop` 與 `design-control-loop`**——見看點 3、4。

### 2. plugin 的檔案結構與 manifest 格式(怎麼組出一個 marketplace)

這 repo 是研究「**Claude Code plugin/marketplace 長怎樣**」的乾淨樣本,兩層 manifest 都有:

**(a) repo 根的 marketplace manifest** — `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "skills",
  "owner": { "name": "humanlayer", "email": "support@humanlayer.dev" },
  "metadata": { "description": "Claude Code skills from HumanLayer", "version": "1.0.0" },
  "plugins": [
    { "name": "improve-claude-md", "description": "…", "version": "1.0.0",
      "author": { … }, "source": "./plugins/improve-claude-md",
      "category": "productivity",
      "keywords": ["claude-md", "instructions", "important-if", "claude-code"] },
    …其餘四個…
  ]
}
```

重點欄位:`$schema` 指向 Anthropic 官方 marketplace schema、`plugins[]` 每筆用 **`source` 指到 repo 內的相對路徑**(`./plugins/<名>`)、`category` 全填 `productivity`、`keywords` 供搜尋。

**(b) 每個 plugin 自己的 manifest** — `plugins/<名>/.claude-plugin/plugin.json`:

```json
{
  "name": "build-iterated-agentic-loop",
  "description": "…",
  "version": "1.0.0",
  "author": { "name": "humanlayer", "email": "support@humanlayer.dev" },
  "repository": "https://github.com/humanlayer/skills",
  "license": "MIT",
  "keywords": ["iterated-agentic-loop", "coding-agents", "github-actions", "skills", "claude-code"]
}
```

**(c) skill 本體** — `plugins/<名>/skills/<名>/SKILL.md`,frontmatter 極簡,**只有 `name` + `description` 兩欄**(沒有 `allowed-tools`),下面接純 Markdown 指令。較複雜的 skill(narrow-react、兩個 loop)另有 `references/` 放模板與範例,靠 progressive disclosure「用到才讀」。

一句話:**marketplace.json 是「店」的目錄,plugin.json 是「一件商品」的標籤,SKILL.md 是「商品實際做的事」。** 這是想自建 Claude Code marketplace 時最省事的抄襲對象。

### 3. 招牌一:`build-iterated-agentic-loop`——把「重複的 agent 任務」變成排程 CI

這個 skill 幫你把一個「可重複的 agent 任務」變成一整組落地的東西:

- `.claude/skills/<名>/SKILL.md`——repo 內的 agent 行為(judgement)
- `.github/workflows/agent-<任務>.yml`——排程/手動觸發的 coding-agent 工作流
- `.github/agent-memory/<任務>.md`——**跨執行之間傳遞的長效回饋**
- 選配 `references/` 模板

它自述的目標形狀叫 **iterated agentic loop**:「一個聚焦的 skill 定義 agent 的判斷力,一個 workflow 用 repo 專屬 prompt 叫起 coding agent,一個 memory 檔在多次執行間帶著長效回饋,每個 workflow 給自己的 PR 打 label,讓**每個迴圈同時只存在一個 open PR**。」——並直接點名 `narrow-react-prop-types` 是「具體參考 pattern」。

9 步 workflow 每步都有「completion criterion」,而且處處是**運維老手才會在意的細節**:

- **先讀 repo 再問問題**:看既有 workflow、package manager、驗證指令、既有 `.claude/skills`,帶著預設答案來訪談,而不是丟一張空白表。
- **把任務壓成三題**:找什麼(finding)→ 改什麼(changing:fix / migrate / generate / refactor)→ 怎麼驗(validate),逼你把 job 講成一句話(例:「找 5 個 react-doctor 違規、修好、跑過 typecheck 與 quality」)。
- **PR bounding(招牌設計)**:預設「**每個 agent loop 只准 1 個 open PR**」,排程跑之前用 `gh pr list --label <label> --state open` 數,達標就 no-op;手動 `workflow_dispatch` 可繞過。理由講得很直白:沒有這個上限,一個每天跑的 agent 一週能生 5+ 個沒人 review 的 PR,製造 review 疲勞與 merge 衝突。
- **agent 中立**:workflow 模板同時給 Claude Code / Codex / OpenCode / **CodeLayer** 四種 headless 跑法與各自的 response 抽取方式(每種 agent 輸出格式不同,都要把最終回覆導進 `/tmp/pr-body.md` 當 PR body)。SKILL.md 裡一句話點名——**「CodeLayer is Humanlayer's ultra-lightweight agent harness」**。
- **memory 檔的紀律**:好的條目=永久排除範圍、已知誤報區、該改變未來選擇的 review 回饋;壞的條目=一次性指令、單次執行 log、skill 裡已寫過的規則。判準是「刪掉這檔會不會損失未來執行需要的 context」。
- 最後還教你 dry-run(GitHub Actions 首次要靠 `push` trigger bootstrap,跑過一次才能 `workflow_dispatch`)。

### 4. 招牌二:`design-control-loop`——把控制理論搬進 codebase 自動化

這是整包裡**理念密度最高**的一個,直接把**控制理論(control theory)**當心智模型:把 codebase 看成一個被隊友、相依套件、生成程式碼**持續擾動(disturbance)**的動態系統,用一個控制迴圈把它「小步」推向目標,而不是一次到位:

| 元件 | 意義 |
|---|---|
| **Set point(設定點)** | 想達到的目標狀態:一個 invariant(「沒有模組跨這些邊界 import」)、一個 threshold(「`core` 覆蓋率 ≥ 80%」)、或一個方向(「每次跑都更少」) |
| **Sensor(感測器)** | 量現況與目標的差距:lint/靜態分析、AST 搜尋、型別檢查、測試、telemetry 查詢、自訂腳本,甚至一個檢查用的 agent |
| **Controller(控制器)** | 從量測結果挑「這次要改哪個、幾個、什麼順序」,大小控制在低風險可審查。可從全 deterministic 腳本到全 agentic,**這是你會隨時間 tune 的部分,從簡單開始** |
| **Actuator(致動器)** | 一個 coding agent + repo 內 skill,在 CI 跑、開 PR |
| **Disturbance(擾動)** | 迴圈外部對系統的一切改動,迴圈必須「帶病」持續推進 |

它跟 ④ 最大的差別是**態度**:build-iterated-agentic-loop 有明確模板可複製;design-control-loop **明說「沒有固定工具組、沒有模板可照抄」**,要 agent 先讀 repo、帶著提案來**訪談使用者**、一起設計、再蓋。8 個 Phase(A→H)一路從「理解系統 → 跟使用者設計迴圈 → 寫 actuator skill → 讓每個元件都能在本機單獨跑 → 接進 CI → **把人放到迴圈外(put a human on the loop)** → flow control → 驗證與 dry-run」。幾個亮點:

- **每個元件先能在本機單獨手跑,才准接 CI**(sensor 跑出穩定量測、controller 選出合理下一步、actuator 在選定目標上改成功並過驗證)——workflow 只是「把你本來就能手跑的東西串起來」的薄薄一層 orchestrator,好 debug。
- **元件會 blur 也 OK**:sensor+controller 融合(工具同時報告又排序)、controller+actuator 融合(一個 prompt 又選又改)都行,「別製造設計裡沒有的分工」。
- **dampener(阻尼器/回歸閘)**:選配的 PR/push 檢查,把 sensor 輸出跟 baseline 比,**在迴圈慢慢改善的同時,擋住問題變更糟**。
- **人「站在迴圈上」而非「在迴圈裡」**:memory 檔 + PR 上留言 `/iterate` 兩個 channel,都要求「改變未來行為,而不只是這次 PR」,並明白告訴使用者「這就是你**隨時間 tune controller 與 skill** 的方式——迴圈會變好,是因為有人一直在修正它」。

這一個 skill 幾乎就是 **HumanLayer 從「human-in-the-loop」演化到「human-on-the-loop」** 的世界觀濃縮:自主 coding agent 不是放牛吃草,而是一個有感測、有邊界、有回饋、有人掌舵的控制系統。

### 5. 怎麼安裝、怎麼用(兩條路)

**路線 A — skills.sh(README 唯一寫的)**:把可編輯的 skill 檔複製進你的專案。

```bash
npx skills add humanlayer/skills --skill improve-claude-md
# 然後在專案裡:
/improve-claude-md
```

其餘四個同理(`--skill narrow-react-prop-types` / `build-iterated-agentic-loop` / `design-control-loop` / `show-me`,再用對應的 `/xxx` 觸發)。這條路跟 [mattpocock/skills](mattpocock-skills.md) 用的是同一個 skills.sh 生態(「fork / 擁有」:檔案進你的 repo,自己改、自己追上游)。

**路線 B — Claude Code 原生 plugin marketplace(README 沒寫、但 manifest 支援)**:因為 repo 根有 `marketplace.json`,可以把它當 marketplace 加進來,再裝個別 plugin:

```text
/plugin marketplace add humanlayer/skills
/plugin install improve-claude-md@skills
```

這條路是「訂閱 / managed」:拿到託管的整包、跟著上游走。**兩條路的產物都一樣**——5 個 skill 都是「既可被 model 自動抓、也能當 `/slash` 指令手動叫」的 skill(SKILL.md 只有 name + description)。

### 6. 設計理念:這是「context engineering」的可安裝樣本

把五個 skill 擺在一起看,它們其實在講同一件事——**幫 agent 把 context 這件事做對**,只是切入點不同:

- `improve-claude-md`:**進入 context 的東西要條件加權**(`<important if>`),別讓無關內容稀釋該遵守的。
- `narrow-react-prop-types`:**型別即 context**——收窄型別=減少 agent 要 reason 的狀態分支,「越嚴格,程式越簡單」。
- `show-me`:**輸出 context 要挑最小視圖**,別淹沒人。
- 兩個 loop builder:**把自主 agent 包成有感測、有邊界、有記憶、有人掌舵的控制迴圈**,呼應 12-factor agents「小而聚焦的 agent + 策略性的人為介入」與 ACE 的 RPI(Research/Plan/Implement)。

換句話說,別人是「給你一堆好用的 skill」,HumanLayer 是「給你幾個 skill,順便把我們對 agent 的整套主張塞給你」。這跟 [Superpowers](superpowers.md) 用心理學說服強推紀律、[mattpocock/skills](mattpocock-skills.md) 用「四種失敗模式」組織工具箱,是三種很不一樣的「用 skill 傳教」姿態。

## 授權與商用可行性

- **MIT License**(©2026 HumanLayer),商用、修改、再散布、閉源整合都可以,只要保留版權與授權聲明。對「拿去改成自己公司內部 skill」最友善的授權。
- **實務要留意的相依**:
  - `narrow-react-prop-types` 綁 HumanLayer 自家 **monorepo + Bun** 慣例(`bun --bun run typecheck --filter`),非該環境要改驗證指令。
  - 兩個 loop builder 產出的是 **GitHub Actions 工作流**,且預設 agent 選項含 **CodeLayer**(HumanLayer 自家 harness)——雖然也支援 Claude Code / Codex / OpenCode,但要小心它會很自然地把你導向自家生態。跑 CI agent 需要對應的 API secret(`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` 等),且範例用 `--permission-mode bypassPermissions`,**只適合在可信、隔離的 runner 上跑**。
  - `improve-claude-md`、`show-me` 幾乎零外部相依,拿去用最安全。
- **沒有 telemetry、沒有外部呼叫**:skill 本體是純 Markdown 指令,不會偷連家裡(唯一的 `.ts` 是 CI 輔助腳本,你自己讀得懂)。

## 與其他 skills 集合的差異

| | humanlayer/skills | [Superpowers](superpowers.md) | [mattpocock/skills](mattpocock-skills.md) | [microsoft/skills](microsoft-skills.md) |
|---|---|---|---|---|
| 規模 | **5 個 skill**(小而精) | 14 個核心 skill(完整流程) | 30+ 個(大型個人作品集) | 一批官方 skill |
| 分發機制 | **同時是 marketplace + skills.sh** | Claude Code plugin marketplace | skills.sh + 官方 plugin | 官方 plugin |
| 定位 | 公司理念的 dogfood 展示 | 強制紀律的開發方法論框架 | 「real engineering not vibe coding」工具箱 | 官方參考實作 |
| 招牌 | **控制理論式的 iterated agentic loop / CI 自動化** | brainstorm→plan→TDD→review 全流程 | grill-with-docs / tdd / 反熵 | 各領域範例 |
| 授權 | MIT | MIT | MIT | MIT |

一句話:**別的集合在解「怎麼寫好一段 code / 怎麼跑好一次 session」,humanlayer/skills 有兩個招牌在解「怎麼讓一個自主 agent 在 CI 上安全地、可審查地、長期地推進整個 codebase」**——這是它最獨到的角度,和它「human-in/on-the-loop」的公司出身直接相關。

## 注意事項與已知限制

- **很新、很小、更新慢**:2026-03 建立,到 8 月才 12 個 commit、5 個 skill、無任何 release/tag。這不是活躍迭代中的大專案,而是「偶爾拿幾個好用的東西出來開源」。要當「完整 skill 生態」用會失望。
- **README 只寫了一半的安裝路徑**:只教 `npx skills add`,沒提 repo 本身其實是個 marketplace;想走原生 `/plugin` 的人得自己看 `marketplace.json`。
- **兩個 loop builder 門檻高**:它們不是「跑一下就有結果」的 skill,而是「陪你設計一整套 CI 自動化」的引導流程,需要你對自家 repo、CI、agent secret、控制論心智模型都有一定掌握,產物還要你自己 review、dry-run、長期 tune。**新手直接上手會 overwhelm**。
- **明顯的自家生態引力**:CodeLayer 被放進預設選項、React skill 綁 Bun monorepo——不是壞事,但要意識到你在採用的是「HumanLayer 怎麼做」的一種意見,不是中立最佳實踐。
- **語言統計誤導**:如前述,GitHub 標 TypeScript 會讓人誤以為是程式庫。
- **`.gitignore` 的小線索**:忽略 `.humanlayer/tasks/`(註解寫 "Riptide artifacts, cloud-synced"),透露他們自家工具(Riptide / CodeLayer)產物的存在,對外部使用者無影響。

## 研究價值與啟示

### 關鍵洞察

1. **`<important if>` 是可以馬上抄走的 context engineering 技巧**:它抓到一個很多人沒意識到的真相——Claude Code 對 CLAUDE.md 會加一句「可能相關可能不相關,不高度相關就別理」,所以**塞越多無關內容,越可能整份被忽略**。用 `<important if="窄條件">` 把領域規則條件加權、地基 context 裸放,是「怎麼寫 CLAUDE.md」這題目前看過最具體、最有理論依據的答案。可直接跟本站 [zeuikli 的 CLAUDE.md 最佳實踐](zeuikli-claude-code-best-practices.md)、[mattpocock 的 CONTEXT.md 拆分](mattpocock-skills.md)對讀。

2. **「iterated agentic loop / 控制迴圈」是自主 agent 進 CI 的成熟框架**:大家都在講「讓 agent 自動修 code」,但很少人把「怎麼**不失控**」講清楚。HumanLayer 用控制理論給了一套完整詞彙與護欄——set point / sensor / controller / actuator / disturbance / dampener,加上「**每個迴圈只准 1 個 open PR**」「每個元件先能本機單獨跑再接 CI」「人站在迴圈外用 memory + `/iterate` 掌舵」。這是把 agent 自動化從「有時候會跑」變成「**可觀測、有界、可審查**」的關鍵一步,值得任何想做 CI agent 的人先讀。

3. **「human-in-the-loop → human-on-the-loop」是這家公司的主線,也是 agent 自主化的縮影**:HumanLayer 從「每個工具呼叫都要人核准」起家,到 design-control-loop 裡「人站在迴圈**上**掌舵、而非**在**迴圈裡逐步核准」——這條演化路線本身就是「agent 能自主到什麼程度、人該介入在哪一層」這個大哉問的具體答案。

4. **plugin 只是 skill 的分發外殼——1 plugin = 1 skill 是合法且乾淨的做法**:很多人以為 plugin 一定要塞 command + agent + hook 一大包。這 repo 示範了**「一個 plugin 只包一個 skill」也完全成立**,而且讓 repo 同時是 marketplace 又能 skills.sh 安裝。想自建 marketplace 的人,這是最小可行範本。

5. **小集合 + 強理念 > 大雜燴**:5 個 skill 卻資訊量很大,因為每一個都在夾帶一個明確主張。相比動輒幾十個 skill 的集合,這種「精選 + 每個都有觀點」的策略,對讀者反而更有啟發。

### 與其他研究筆記的關聯

- 與 [Superpowers](superpowers.md)、[mattpocock/skills](mattpocock-skills.md):三者並列可看「用 skill 傳教」的三種姿態——Superpowers 用心理學說服強推紀律、mattpocock 用「失敗模式→對應 skill」組織工具箱、humanlayer 用「控制理論 + context engineering」把公司世界觀做成範本。
- 與 [microsoft/skills](microsoft-skills.md)、[casper 的 skill 設計藝廊](casper-claude-skill-design-gallery.md)、[claude-skills-guide](claude-skills-guide.md):都是研究「skill 該怎麼設計」的材料,humanlayer 這份的獨到處在「skill × CI 自動化」的交叉點。
- 與 [knowledge-work-plugins](knowledge-work-plugins.md)、[claude-financial-services-plugins](claude-financial-services-plugins.md):同樣是「Claude Code plugin marketplace」的樣本,可對照 manifest 結構;humanlayer 這份是「1 plugin = 1 skill」的極簡版。
- 與 [zeuikli 的 Claude Code 最佳實踐](zeuikli-claude-code-best-practices.md):`improve-claude-md` 的 `<important if>` 技巧,是「CLAUDE.md 該長還是該短」這題的一個具體工程解,可跟該報告的方法論層對讀。

## 一句話總結

> **YC 新創 HumanLayer(12-factor agents、Advanced Context Engineering、CodeLayer 的同一批人)公開的 5 個 Claude Code plugin——不是 skill 大雜燴,而是把自家 context engineering 世界觀做成可安裝範本。** 兩個具體小工具(`improve-claude-md` 用 `<important if>` 救 CLAUDE.md、`narrow-react-prop-types` 收窄 React prop 型別)、一個解說工具(`show-me`),加上兩個招牌 `build-iterated-agentic-loop` / `design-control-loop`——用控制理論(sensor/controller/actuator/disturbance)幫你蓋出「排程跑、每次只開一個 PR、人站在迴圈外掌舵」的自主 coding agent。MIT、每個 plugin 只包一個 skill、repo 本身即 marketplace 也能 `npx skills add`;規模小(3.3k stars、12 commits、2 位 contributor=公司 CEO/CTO)但理念密度極高。想學「怎麼寫好 CLAUDE.md」和「怎麼讓 agent 安全地在 CI 上長期改 codebase」的人必看。
