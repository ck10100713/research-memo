---
date: "2026-06-11"
category: "Agent Skills"
skill_type: "automation"
card_icon: "material-bullhorn-outline"
oneliner: "駱君昊（Hao）的 Claude Code skill：學使用者 FB 語氣 → 排 14 天內容日曆 → 透過 Claude in Chrome MCP 自動發到 FB/IG/Threads/X；內建「發佈前必打『確認』」硬安全閘，首發即 72K 觸及的實證 viral 框架（v1.0.1：R1-R35 規則 + F1-F27 公式 + 4 種 Mode）"
tags:
  - skills
  - automation
  - browser-agent
  - marketing
---

# social-post

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/Hao0321/claude-skill-social-post> |
| 作者 | 駱君昊 (Hao) — MetaFantasy Co-Founder / AIGC 數位創作者 · <https://github.com/Hao0321> |
| 作者 FB | <https://www.facebook.com/lo.jain.hao> |
| 姐妹 skill | [claude-skill-code-cleanup](https://github.com/Hao0321/claude-skill-code-cleanup)（用來維護本 skill 自己） |
| License | MIT |
| 版本 | **v1.0.1（2026-06-10）**：R1-R35 規則 / F1-F27 公式 / Mode C 9 變體 / Cases 27-31（初稿收錄時為 v1.0.0） |

## Skill 概述

**social-post** 是一個 Claude Code agent skill，把「個人社群經營」做成一條三階段、可路由的自動化工作流。它的本質不是「叫 AI 亂寫貼文」，而是把作者 41 天連續實戰反向工程出來的一整套 viral 方法論（R1-R32 規則、4 種發文 Mode、F1-F25 公式）編碼成 reference 檔，讓 Claude 依使用者意圖只讀必要片段（省 token），生成貼合使用者語氣的草稿，再透過 **Claude in Chrome MCP** 操作瀏覽器實際發佈到 FB / IG / Threads / X。

三個階段：**P1 學風格**（爬使用者自己的 FB 個人頁 ~20 篇貼文 → 萃取語氣寫成 `style_profile.md`）、**P0 排內容日曆**（依目標生成 14 天 `content_plan.md`）、**P2 生成+發佈**（讀當天公式 → 各平台各生一版 → 預覽確認 → 依序發佈 → 回填戰績）。整套設計圍繞一個核心信念：**真 KPI 是社群轉化（Line 群成員、私訊分享），不是讚數**。

作者宣稱的實證戰績是這個 skill 最大的賣點與爭議點：首發貼文（鉤子是「這篇 PO 文就是這個 skill 自己發的」）達 **72K~75K 觸及 / 358~380 讚 / 443~457 留言**，並帶動 Line 社群從 ~800 成長到 41 天後的 4,568+。這些是**作者單一帳號的自我回報數據**，非獨立驗證，閱讀時應視為個案而非可複製保證。

## 安全審查結果

> **v1.0.1 複查（2026-06-11）**：新增的 R34（反 AI 腔寫作風格）、R35（keyword CTA）、F26/F27（giveaway 系列公式）改動僅在 `SKILL.md` / `rules.md` / `formulas.md` / `case_studies.md`，**全為發文內容策略文字，無新增可執行碼、無資料外洩、無新權限需求**。R35 的 DM 版 CTA 會觸發 FB 私訊限制（封號前兆）——但 skill 本身已點明此風險並把預設改為「公開 link 自助派發」以保帳號安全，且維持 R25（正文絕不附外部連結）。**安全姿態與初審一致，🟡 結論不變。**

- **審查日期**：2026-06-09（v1.0.0 初審）/ 2026-06-11（v1.0.1 複查）
- **檢查範圍**：全 repo 所有檔案——`SKILL.md`、`references/*.md`（含 facebook/instagram/threads/x/generate_and_publish/learn_style/rules/formulas/evaluation/case_studies/phase0_plan）、`docs/setup.md`、example 檔、README、CHANGELOG、LICENSE。**無 scripts/ 或 hooks/**，全為 markdown 文字。
- **結果**：🟡 **通過（含灰色地帶備註）**
- **無 🔴 項目**：未發現資料外洩（明列「外傳 `style_profile.md` / 使用者資料」於禁止清單）、無隱蔽執行 / base64 混淆 payload、無破壞性操作（`setup.md` 安裝僅 `git clone` 自家 repo + `cp`/`mv`，無 `curl|bash`）、無惡意 prompt injection。**反而內建強安全閘**：發佈前必須在對話取得明確「確認」字眼，且明文聲明即使用 `--dangerously-skip-permissions` 啟動也不 bypass。

### 🟡 灰色地帶備註（使用者已知悉並同意收錄）

| # | 檔案:位置 | 行為 | 風險說明 |
|---|----------|------|---------|
| 1 | `SKILL.md`、各平台 ref | 透過 Chrome MCP **自動發佈公開貼文** | 對外、不可逆動作；雖有「確認」閘，本質是代操社群帳號 |
| 2 | `setup.md:691-712` | 教使用者把 **Chrome MCP write 權限預寫進 `settings.local.json`** | 預授權瀏覽器寫入 = 降低逐次人工確認、繞過權限彈窗 |
| 3 | `setup.md:674-687` | 用 `mcp__scheduled-tasks` 建 **背景 cron 任務**查流量 | 背景於新 session 自動執行、減少人為監督 |
| 4 | `facebook.md`、`threads.md` 等 | `javascript_tool` **注入 JS 操作第三方站 DOM** | 在 FB/IG 執行腳本，瀏覽器自動化常規但屬注入行為 |
| 5 | `learn_style.md` | 爬取使用者**自己的** FB 貼文做風格分析 | 讀本人資料、有同意、明訂不外傳，風險低 |

> 結論：設計良好、安全意識高的合法自動化 skill，所有灰色地帶都源自「瀏覽器自動發文」這個本質而非惡意。使用者若採用，建議**不要**為了省彈窗而預授權全部 write 權限（備註 2），保留逐次人工確認最安全。

## 工作流程整理（繁中原文已是中文）

### 階段路由（依意圖只讀必要 reference）

| 觸發語 | 階段 | 讀取檔案 |
|--------|------|---------|
| `style_profile.md` 不存在 / 「重新學風格」 | **P1 學風格** | `learn_style.md` |
| `content_plan.md` 不存在 / 「重新規劃」 | **P0 排日曆** | `phase0_plan.md` + `formulas.md` |
| 「發文」「今天發一篇」「PO」 | **P2 生成+發佈** | `generate_and_publish.md` + `style_profile.md` + `content_plan.md` + 目標公式 + 相關規則 + 目標平台 ref |
| 「這篇好不好」「查流量」 | **診斷** | `evaluation.md` + R6/R23 |
| 「Day X 發生什麼」 | **案例** | `case_studies.md` |

### 🛡️ 硬安全閘（不可覆寫）

1. **發佈前必拿到使用者明確「確認」** — 沒「確認」不發
2. **不自動登入 / 不輸入密碼** — 登入牆出現請使用者手動登
3. **不自動按讚 / 回覆 / follow / 大量留言**
4. **不外傳使用者資料**、不刪除留言貼文
5. **FB / Threads 正文絕不附外部連結**（R25，導流改用作者精選留言）
6. 任一平台發佈失敗就**停手回報**，不跳過續發

### 核心方法論骨架

- **Viral 4 條件公式**：`viral = 4 段 4 句結構 + 純血 voice + 全新敘事意圖 + 黃金時段`（4 個 AND，任一缺即死；readability 是隱藏第 5 條件）
- **4 種 Mode**（funnel 互補）：A 日常（鐵粉黏著）/ B 純血 hype（擴散）/ C 深度反思（信任深化，8 變體）/ Thread F19 立場宣言（轉發擴散）
- **平台差異化**：FB 長敘事、X 壓短 punchline、IG 必配圖、Threads 口語短句不分段（連續逗號流）——**嚴禁一稿多投**，每平台重新生成
- **真 KPI**：分享 > 留言 > dwell > 讚；私訊分享為 2026 最強信號

### v1.0.1 新增（2026-06-10，6/7+6/9 雙 mega-viral 實證）

| 項 | 內容 | 重點 |
|----|------|------|
| **R34 真實 voice** 🚨 | 反 AI 腔硬規則 | 診斷出「AI 文」元兇是**抽象空詞**（護城河/本質/真正的 X）+ staged 開場 + over-narrate，**不是標點**；`──`/`！！！` 是 proven 爆款裝置照用。證明 R34 與 F6b mega-viral 相容 |
| **R35 keyword CTA** 🏆 | broke 鐵粉圈引擎 | 「留言『關鍵詞』」= 留言磁鐵（每留言 5x 權重）。**公開 link 自助派發為最優預設**（精選留言、無 DM 天花板、account-safe）；DM 版有封號天花板（6/7 323 留言即觸發 FB 私訊限制）。仍守 R25 不導 GitHub 正文 |
| **F26 / F27 giveaway** | 作品集 reveal / 單品 spotlight | F27 採 PWYW（可輸入 0 元）+ 條件開源 + 必加 R35 keyword CTA。6/9 F6b giveaway 衝 **42,103 觀眾 / 959 留言（史上最高）/ 93.1% 非追蹤** |

> 規則/公式總數：**R1-R35**（R9/R21/R22 已廢除）/ **F1-F27** / Mode C 9 變體。

### 安裝與使用（摘自 `setup.md`）

```bash
git clone https://github.com/Hao0321/claude-skill-social-post.git ~/tmp-social-post
mkdir -p ~/.claude/skills
cp -r ~/tmp-social-post/social-post ~/.claude/skills/social-post
cd ~/.claude/skills/social-post
mv style_profile.example.md style_profile.md
mv content_plan.example.md content_plan.md
```

前置需求：已裝 Claude Code + Claude in Chrome MCP、Chrome 已登入目標平台、FB 個人頁 ≥ 20 篇公開貼文。之後對 Claude 說「幫我學 FB 風格」→「幫我排社群內容日曆」→「今天發一篇」即可。

## 研究價值與啟示

### 關鍵洞察

1. **這是「領域知識 → reference 檔」編碼的範本**：skill 的價值不在程式（它一行可執行碼都沒有），而在把作者 41 天試錯萃取的 R1-R32 規則與公式系統化。任何有深度領域 know-how 的人，都可用這種「SKILL.md 路由 + references/ 分檔」結構把隱性經驗變成 agent 可執行的資產——這正是 [SkillOpt](skillopt.md) 想自動化、而本 skill 純手工打磨的東西。

2. **安全閘設計值得所有「會對外動作」的 skill 抄**：明文「即使 `--dangerously-skip-permissions` 也保留確認閘」「不自動輸密碼」「失敗即停手」——把不可逆的對外操作（公開發文）與可逆的內部操作分級處理。這是 agent 自動化裡少見的成熟安全意識，是本 skill 通過審查的關鍵。

3. **token 路由是長 skill 的生存技巧**：v0.9.0 把 SKILL.md 從 565 行砍到 130 行（-77%），把規則細節拆進 `references/rules.md`，再用「依意圖只讀必要檔」的路由表控制 context。當 skill 知識量大時，**漸進揭露（progressive disclosure）不是選配而是必須**。

4. **「自我 dogfooding」形成閉環**：作者用姐妹 skill code-cleanup 來 audit 這個 skill（抓 doc drift、版本漂移），且這個 skill 的第一篇貼文就是宣傳它自己。skill 維護 skill、skill 行銷 skill——是 agent 工具自舉的有趣案例。

5. **戰績數據要批判性看待**：所有 viral 數字都是作者單帳號自我回報，且高度依賴其既有的 AIGC 創作者人設與台灣 AI 社群網絡。**方法論可借鏡，數字不可複製承諾**——換一個帳號、受眾、niche，結果會完全不同。這也是筆記把它歸 `automation` 而非「行銷保證」的原因。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [SkillOpt](skillopt.md) | SkillOpt 自動「訓練」出 skill 文字；social-post 是人工打磨的高品質 skill。前者是 skill 生產的自動化方法論，後者是該方法論的優質手工樣本 |
| vs 其他 Agent Skills（[research](skill-research.md)、[book-to-skill](skill-book-to-skill.md)） | 同為操作型 skill，但 social-post 是少數**對外、不可逆動作**（公開發文）的 skill，安全閘設計因此更重 |
| 瀏覽器自動化定位 | 依賴 Claude in Chrome MCP 操作真實網站 DOM，屬 `browser-agent` 範疇；與純檔案操作 skill 風險量級不同 |

**最大啟示**：social-post 證明了「**agent skill 的競爭力來自領域知識密度，不是程式複雜度**」。它沒有任何可執行腳本，純靠把作者的社群經營 know-how 結構化編碼，就成為一個有實戰戰績的工具。同時它示範了「對外動作型 skill」該有的安全紀律——這兩點對任何想寫 skill 的人都是直接可抄的模板。

??? note "原文（SKILL.md 全文，Traditional Chinese）"

    ---
    name: social-post
    description: 學使用者的 Facebook 個人貼文語氣，依 14 天內容策略日曆，自動產出並發佈到 FB / Instagram / Threads / X。使用時機：使用者說「發文」、「幫我寫一篇貼文」、「用我的風格發」、「今天發一篇」、「PO 一下」、「學我的語氣」、「分析我的貼文風格」、「重新規劃內容」、「排貼文」、「查流量」、「review」時一律觸發；即使只說「發一篇」、「PO 文」、「PO 個廢文」也要觸發。
    ---

    # social-post

    三階段工作流。**依使用者意圖路由，只讀必要 reference**（省 token）。

    ## 階段路由

    | 觸發 | 階段 | 讀 |
    |---|---|---|
    | `style_profile.md` 不存在 / 說「重新學風格」 | **P1** | `references/learn_style.md` |
    | `content_plan.md` 不存在 / 說「重新規劃」「排新 14 天」 | **P0** | `references/phase0_plan.md` + `formulas.md` |
    | 說「發文」「今天發一篇」「PO」 | **P2** | `references/generate_and_publish.md` + `style_profile.md` + `content_plan.md` + `formulas.md`（目標公式段）+ `rules.md`（相關規則）+ 目標平台 ref |
    | 說「這篇好不好」「查流量」「分析」 | **診斷** | `references/evaluation.md` + `rules.md`（R6/R23）+ 目標 post 戰績 |
    | 說「歷史怎麼樣」「Day X 發生什麼」 | **案例** | `references/case_studies.md` |
    | 想查某條規則細節 | **規則** | `references/rules.md`（R1-R29 完整版）|

    路由前用一句話告知使用者要做哪階段，給糾正機會。

    ## 先決條件

    - `mcp__Claude_in_Chrome__*` 可用（否則停、不模擬）
    - 使用者已登入目標平台（登入牆出現請使用者手動登，不自動化）

    ## 🛡️ 安全閘（硬規則不可覆寫）

    **每次實際發佈前必須在對話裡拿到使用者明確「確認」字眼。** 沒「確認」不發。

    **私人版例外**：使用者若明確在**當前 session** 授權「你自己操作不用問我」，私人版可免逐次確認，僅限該 session。開源版 SKILL.md **永遠保留此閘門不可 bypass**。

    ## 不要做

    - 沒授權發文字眼就發
    - 跨平台同一段複製（每平台重新生成）
    - 自動按讚 / 回覆 / follow / 大量留言
    - 外傳 `style_profile.md` / 使用者資料
    - 幫登入 / 改隱私 / 改帳號
    - 猜測 FB 個人頁網址（P1 必須問）
    - 刪除使用者留言 / 貼文（系統硬規則）
    - **🚨 FB / Threads 正文附外部連結（R25 硬規則，絕對禁止）**

    ## 核心規則（R1-R32 速查，完整定義見 `references/rules.md`）

    - 一天一篇 + 每週 ≥ 2 篇非 AI；爆款後 24h 冷卻禁長文
    - 主題 = 敘事意圖，同意圖 4 天內不重複；必 48-72h plateau 才判定戰績
    - 真 KPI 是社群轉化不是讚；私訊分享 = 2026 最強信號
    - FB/Threads 正文絕不附連結（R25 硬規則）；導流用作者精選留言
    - FB 社團 cross-post = 留言 5-10x 放大（R30）

    ### Viral 4 條件公式

    ```
    viral = 4 段 4 句結構 + 純血 voice + 全新敘事意圖 + 黃金時段
    ```

    4 個 AND，任一缺 = 死。Readability 是隱藏第 5 條件（meta ≤ 2 層 / 數字 ≤ 3 個/段 / 5 秒讀懂）。

    ### 4 個 Mode（funnel 互補）

    | Mode | 公式 | funnel |
    |---|---|---|
    | A 日常 | 短句吐槽 | 鐵粉黏著 |
    | B 純血 | F6b / F15 mini | 擴散 + Line 群 |
    | C 深度反思 | F20-F25a/b/c | 信任深化 + trust reset + 集體 framing |
    | Thread F19 | 立場宣言 | Thread 轉發 |

    > 完整原文（含 R1-R32 規則表、實用技巧、開發原則、快速查詢、常見踩雷）見 repo：
    > <https://github.com/Hao0321/claude-skill-social-post/blob/main/social-post/SKILL.md>
