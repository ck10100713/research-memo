---
date: "2026-07-23"
category: "Coding Agent 工具"
card_icon: "material-toolbox"
oneliner: "Jezweb 的 63-skill / 10-plugin 生產型 skill 市集——核心價值在兩份把官方規範編輯化的 authoring 準則（SKILL_SHAPE.md / CLAUDE.md）"
tags:
  - skills
  - claude-code
  - plugin
---

# jezweb/claude-skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★940 / 96 forks / MIT / 2025-10 建） | [github.com/jezweb/claude-skills](https://github.com/jezweb/claude-skills) |
| README（公開總覽、plugin 表） | [README.md](https://github.com/jezweb/claude-skills/blob/main/README.md) |
| SKILL_SHAPE.md（authoring 準則，最有料） | [SKILL_SHAPE.md](https://github.com/jezweb/claude-skills/blob/main/SKILL_SHAPE.md) |
| CLAUDE.md（repo 開發慣例、quality bar） | [CLAUDE.md](https://github.com/jezweb/claude-skills/blob/main/CLAUDE.md) |
| 姊妹庫 dotjez（思考型 skill：規劃/prompt/驗證） | [github.com/jezweb/dotjez](https://github.com/jezweb/dotjez) |
| 第三方評測（11 tested, 4 worth keeping） | [buildtolaunch.substack.com](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review) |
| Anthropic 官方 skill 規範 / skill-creator | [agentskills.io](https://agentskills.io/specification) · [anthropics/skills](https://github.com/anthropics/skills) |

## 專案概述

`jezweb/claude-skills` 是 Jeremy Dawes（澳洲 web agency Jezweb）維護的 **Claude Code skill 市集（plugin marketplace）**。定位一句話講完：**每個 skill 都必須「生出東西」**——scaffold 好的專案、產生的素材、專業文件、部署好的服務。不是知識傾倒（knowledge dump），而是「產出一份可交付物」的 workflow 食譜。

安裝方式是標準 Claude Code plugin 流程：

```bash
/plugin marketplace add jezweb/claude-skills   # 一次性加市集
/plugin install cloudflare@jezweb-skills        # 按需裝 plugin
/plugin install dev-tools@jezweb-skills
```

裝好後不用記指令——skill 由自然語言的 trigger phrase 自動觸發。

**與本站其他 skill 筆記的定位差異**：這是一個**單人/單 agency 出品、偏「Jezweb 自家生產線」的實戰庫**（Cloudflare 全家桶 + 澳洲商業寫作 + Shopify/WordPress），不是像 [microsoft/skills](microsoft-skills.md) 那種官方庫，也不是 [awesome-openclaw-skills](awesome-openclaw-skills.md) 那種純彙整清單。它的價值密度集中在**設計哲學**，而非數量。

## 數字現況（實測 main 分支）

> **文件與程式碼漂移**：README 開頭寫「Ten plugins」、History 段寫「v13 = 11 plugins / 52 skills」、清單標題寫「All 60 Skills」——三個數字互不一致。實際數 `main` 上的 `SKILL.md`：

| 指標 | README 宣稱 | main 實測 |
|------|------------|-----------|
| plugin 數 | 10~11 | **10** |
| skill 數 | 52 / 60 | **63** |

實測各 plugin skill 分布（數 `SKILL.md`）：

```
dev-tools     16   ← 最大，開發生命週期工具
frontend       9   （含 CLAUDE.md 有列、README 沒列的 design-loop / design-system）
integrations   9
cloudflare     8   ← repo 的招牌（Workers / Hono / D1+Drizzle / Vite / TanStack）
writing        8   （AU/US/UK/NZ 商業英文 + 履歷/提案/獎項/策略文件）
design-assets  5
shopify        3
wordpress      3
social-media   1
web-design     1
```

諷刺的是，這個 repo 自己就有一個 `skill-review` skill 專門抓「version drift（依賴版本漂移）」——但它自己的 README 就對不上 code。研究時務必**以 clone/API 抓到的 tree 為準，不採信 README 數字**。

## 十大 plugin 一覽

| 群組 | Plugin | 招牌 skill |
|------|--------|-----------|
| Build & Deploy | `cloudflare` | worker-builder、vite-flare-starter、hono-api-scaffolder、d1-drizzle-schema、d1-migration |
| | `shopify` / `wordpress` | 產品/內容/SEO；WP-CLI + Elementor |
| Design & Frontend | `frontend` | tailwind-theme-builder、shadcn-ui、react-patterns、design-review、react-native |
| | `design-assets` | color-palette、favicon-gen、icon-set-generator、ai-image-generator |
| | `web-design` | seo-local-business（JSON-LD schema） |
| Writing | `writing` | 四國商業英文風格指南 + 履歷/提案/獎項/SWOT |
| | `social-media` | 多平台貼文（字數/hashtag/campaign 序列） |
| Dev Tools | `dev-tools` | project-health、deep-research、ux-audit、github-release、roadmap、vitest、codex-review |
| | `integrations` | mcp-builder、stripe-payments、elevenlabs-agents、gws-setup |

> 「思考型」skill（planning、prompt-writing、verification doctrine、brains-trust）刻意**不放這裡**，另拆到 [dotjez](https://github.com/jezweb/dotjez)——關注點分離：這個庫只收「會產出交付物」的。

## 核心價值：兩份 authoring 準則

這才是這個 repo 值得研究的地方——它把 Anthropic 官方 skill 規範 + agentskills.io best practices，**編輯化（editorial layer）**成一套可直接套用的寫作準則。

### SKILL_SHAPE.md 的六條原則

| 原則 | 白話 |
|------|------|
| **Spend context wisely** | skill 一觸發全文進 context，每句都跟對話史搶位。逐句問：「Claude 沒這句會做錯嗎？」不會就砍。不要解釋 Claude 已懂的東西（什麼是 PDF、HTTP、migration）。 |
| **Favor procedures over declarations** | 教「怎麼處理這一類問題」而非「這一題的答案」。可重用的方法比特定解活得久。 |
| **Match specificity to fragility** | 按段落校準規範強度：多解法且容錯 → 給自由講 why；操作脆弱/順序重要 → 給精確指令、精確 flag。 |
| **Provide defaults, not menus** | 別列「你可以用 A/B/C/D」，選一個 default + 一句逃生門。選擇多半不重要，糾結才是 overhead。 |
| **Explain why, drop musty MUSTs** | 「你 MUST 用 X」會過時且不幫 Claude 推理邊界；「用 X 因為它處理 unicode PDF 而其他會爛」才讓 Claude 帶著原則走到 skill 沒預期的情境。 |
| **Start from real expertise（3-instance rule）** | 第三次跑這流程時才寫 skill，不是第一次——早了你不知道辨識訊號在哪、坑在哪、哪步要規範。generic 文章產 generic skill。 |

### description 要「pushy」

`description` 是 Claude 觸發前唯一會讀的欄位，而 Claude **傾向 under-trigger**，所以描述要「霸道」不要中性：

```yaml
# 太中性——相關時可能被跳過
description: How to build internal data dashboards.

# pushy——即使使用者沒說 "dashboard" 也會觸發
description: ...Use whenever the user mentions dashboards, data visualization,
  KPIs, or wants to display company data — even if they don't say "dashboard".
```

領頭寫「做什麼 + 何時用」，塞入真實使用者會打的 trigger phrase，上限 1024 字。

### 高價值 pattern（可直接借用）

- **Gotchas section** — 往往是 skill 裡最值錢的段落：**具體糾正 Claude 不被告知就會犯的錯**（如「`users` 表用 soft delete，查詢要加 `WHERE deleted_at IS NULL`」）。當你在一次對話裡糾正 Claude，就把糾正加進 gotchas——改善 skill 最短路徑。
- **Plan-validate-execute** — 批次/破壞性操作先產中間 plan、對照 source of truth 驗證、才執行。validator 的錯誤訊息就是 Claude 自我修正的依據。
- **Validation loops** — 指示 Claude 做完先自我驗證再前進。
- **Bundled scripts** — 發現 Claude 每次都重造同一段邏輯（解析格式、畫圖、驗證），就寫一次 script 丟進 `scripts/`。

### 「Inline everything critical」——用血換來的教訓

CLAUDE.md 記了一個實際踩坑：agent 被告知「curl 指令見 `references/stitch-direct.md`」，結果它**整份跳過**，改去瀏覽器開網站試。關鍵指令只在 20 行外的 reference 檔裡，它從沒讀。

結論反直覺但正確——**檔案長度不是問題，關鍵內容在 reference 才是**：

> 「一個能跑的 800 行 skill，勝過一個關鍵內容藏在 agent 從不讀的 references 裡的 300 行壞 skill。」

| 內容類型 | 該放哪 |
|---------|--------|
| workflow 步驟、指令、mapping 表、gotchas（**每次都要**） | **SKILL.md 內文（inline）** |
| 可執行 helper script（agent「跑」不「讀」） | `scripts/` |
| variant/選用文件（AWS vs GCP） | `references/`，**且要給明確載入 trigger** |
| 複製進使用者專案的模板 | `assets/` |

老的「500 行上限」被明確推翻：500 行 ≈ 2500 token，在 1M context 是 0.25%。上限是 200K 時代的 context 經濟學遺物。

## 版本治理：誠實的退場機制

repo 對「skill rot（skill 腐敗）」有明確態度，這在多數 skill 庫裡少見：

- **起點 105 個 skill → 現在精簡**：很多當初是「參考指南」，後來被 Claude 訓練資料涵蓋而冗餘，直接退役。
- **退場三選項**：archive in git（打 tag，如 v1 的 105 skill → `v1-final` tag）／roll into another skill／replace。
- **ERRATA.md 慣例**：library 改版導致 skill 指令失準時，先在 skill 旁記 `ERRATA.md`（狀態 `active → absorbed → outdated`），不急著改寫 SKILL.md。
- 版本軌跡：v1（105 skills，扁平）→ v2（拆成 plugin，「每個 skill 必須產出」）→ v12（10 plugin / 44）→ v13（11 plugin / 52，README 版）。

## 目前限制 / 注意事項

- **文件對不上 code**（README 52/60 vs main 63）——引用數字前務必自己數 tree。
- **強烈 Jezweb 傾向**：Cloudflare 全家桶、澳洲/紐西蘭商業英文、Shopify/WP——非其技術棧的使用者，通用價值集中在 `dev-tools`、`design-assets`、`SKILL_SHAPE.md` 準則本身。
- **單一維護者**：品質高但 bus factor 低；`pushed_at` 為 2026-07-02，非每日更新。
- 第三方評測（buildtolaunch「11 tested, 4 worth keeping」）顯示：market 上 plugin 存活率不高，選裝比全裝重要。

## 研究價值與啟示

### 關鍵洞察

1. **「每個 skill 必須產出」是最狠的過濾器**。它一刀切掉所有「Claude 訓練資料已涵蓋」的知識型 skill——這正是 skill 生態最大的雜訊來源。判斷一個 skill 該不該存在，問「它產出什麼可交付物？」比問「它教什麼」更有效。

2. **description 要 pushy，是因為 Claude 天生 under-trigger**。這解釋了為何本站 `/research`、`/skill-review` 等 skill 的描述都塞滿 trigger phrase——不是囉嗦，是對抗模型的保守觸發傾向。與本站 [casper-claude-skill-design-gallery](casper-claude-skill-design-gallery.md)、[microsoft-skills](microsoft-skills.md) 的觸發設計互為印證。

3. **「Inline everything critical」推翻了 progressive disclosure 的誤用**。progressive disclosure 是把「選用/變體」內容外置，不是把「關鍵路徑」外置。LLM 面對「去讀檔案 X」和「做任務」兩個指令時會選後者——這是可預測的失敗模式，不是偶發。

4. **退場機制比新增機制更能定義一個庫的品質**。多數 skill 庫只增不減，靠數量行銷；這個庫敢從 105 砍到 63，還把砍掉的打 tag 存進 git history。**「marketplace 裡的 stale skill 不是免費的——它仍在競爭觸發」**。

5. **文件漂移是活教材**。它自己有 skill-review 抓 version drift，README 卻對不上 code——反過來證明：**skill 治理必須自動化（sync 腳本 / CI），靠人手維護數字一定漂**。本站用 `sync.py` 從 frontmatter 自動生成索引，正是同一結論的實作。

### 與其他專案的關聯

| 對照對象 | 關係 |
|---------|------|
| [microsoft/skills](microsoft-skills.md) | 官方庫 vs 單 agency 實戰庫；兩者都強調 skill 觸發設計 |
| [建構型 Agent SDK Skills 對照](agent-sdk-builder-skills.md) | 該筆記腳註提過「jezweb 有 63 skill 無一是 OpenAI」——本筆記證實：確實聚焦 Claude Code plugin，marketplace 曾錯誤引用其不存在的 OpenAI skill |
| [awesome-openclaw-skills](awesome-openclaw-skills.md) | 彙整清單 vs 可安裝市集；jezweb 是「有維護者、會退役」的活庫 |
| 本站 `/skill-review`、`/research` skill | jezweb 的 SKILL_SHAPE.md 準則（inline critical、pushy description、gotchas）可直接當本站 skill 審查與撰寫的 checklist |
| [dotjez](https://github.com/jezweb/dotjez) | 同作者的「思考型 skill」姊妹庫——關注點分離：生產型 vs 思考型分開放 |
