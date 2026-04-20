---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-dna"
oneliner: "上海 AI Lab × titanwings 出品，從 colleague.skill 升級的通用人物蒸餾器 — 21 天衝 15.5K stars，三家族 × 四宿主把任何人變 AI Skill"
---

# dot-skill 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)（default branch：`dot-skill`） |
| README（英） | [README.md](https://github.com/titanwings/colleague-skill/blob/dot-skill/README.md) |
| README（中） | [docs/lang/README_ZH.md](https://github.com/titanwings/colleague-skill/blob/dot-skill/docs/lang/README_ZH.md) |
| 進化路線圖 | [ROADMAP.md](https://github.com/titanwings/colleague-skill/blob/dot-skill/ROADMAP.md) |
| 技術論文（前身） | [Colleague.Skill: Automated AI Skill Generation via Expert Knowledge Distillation](https://github.com/titanwings/colleague-skill/blob/dot-skill/colleague_skill.pdf) |
| 社群 Gallery | [titanwings.github.io/colleague-skill-site](https://titanwings.github.io/colleague-skill-site/) |
| 開放標準 | [agentskills.io](https://agentskills.io) |
| 兄弟作品 | [titanwings/ex-skill](https://github.com/titanwings/ex-skill) |

**作者：** [@titanwings](https://github.com/titanwings) · Powered by **Shanghai AI Lab · AI Safety Center**

**專案狀態：** ⭐ **15,499 stars** · 1,561 forks · Python · MIT · 建立 2026-03-30（**21 天衝到 15K+ stars**，預設分支已從 `main` 改名 `dot-skill`）

**最新里程碑：** 2026-04-19 突破 15K stars · 2026-04-13 發布 Roadmap（宣告從 colleague.skill 升級為 dot-skill） · 2026-04-07 社群 Gallery 上線，收錄 100+ 社區 Skills

## 專案概述

dot-skill 把一個極度情感化的問題寫進 README 開頭——「同事跳槽、導師畢業、搭檔轉崗，帶走了整套工作方法和上下文？家人老友漸行漸遠，你想留住和 TA 相處的方式？你喜歡的作家、偶像、思想家你夠不著，但你想聽他對你的問題怎麼看？」

它給出的答案是：**原材料 + 你的描述 → 一個真正像他的 AI Skill**，用他的方式思考、用他的口吻說話。

這是一個由「單一場景的 PMF 驗證」升級為「通用蒸餾引擎」的典型案例。前身 colleague.skill 只解決同事離職知識流失問題、有附論文（見上表），在社群貢獻了「老闆、教授、前任、自己、小說角色」等意料之外的用法後，作者決定把 `/create-colleague` 入口廢掉、改成通用 `/dot-skill`，底下接三大人物家族 prompt pipeline——**從「script」變「engine」**。

```
colleague.skill (v1.0, 2026-03-30)
        │   13K stars 驗證 PMF，社群瘋狂貢獻非同事用例
        ▼
dot-skill (2026-04-13 Roadmap 發布)
        ├── colleague     （同事 / 導師 / 搭檔）
        ├── relationship  （前任 / 伴侶 / 家人 / 老友）
        └── celebrity     （名人 / 創作者 / 小說角色 / 自己）
```

## 三大人物家族

dot-skill 的核心設計是**用 Persona 做通用基底、再疊加家族專屬模組**：

| 家族 | Persona 內容 | 附加模組 | 最佳素材 |
|------|-------------|---------|---------|
| 🧑‍💼 **colleague** | 6 層人格（硬規則→身分→表達→決策→人際→Correction） | ➕ **Work Skill**：工作範疇、流程、輸出偏好、經驗知識庫 | 本人長文書寫 > 決策性回覆 > 群聊閒聊 |
| 💞 **relationship** | 表達 DNA · 情緒觸發點 · 衝突模式 · 修復模式 | —（未來：照片分享、貼圖、語音） | 完整聊天記錄 > 書信/社群動態/日記 > 第三方描述 |
| 🌟 **celebrity** | 心智模型 · 決策啟發法 · 表達 DNA · 他者評價對照 | ➕ 六維度研究檔案（作品/訪談/決策/表達 DNA/外部評價/時間線） | 第一人稱著作/長訪談 > 決策紀錄 > 第三方解讀 |

> **執行邏輯：** 收到任務 → Persona 決定態度與語氣 → 附加模組補執行細節 → 用他的口吻輸出

每個家族有獨立的 prompt pipeline、資料採集策略、生成模板——但共用同一個 skill engine。

## 四個宿主 × AgentSkills 標準

dot-skill 不綁單一 Agent 宿主，走 [AgentSkills](https://agentskills.io) 開放標準：

| Host | 安裝位置 | 呼叫方式 |
|------|---------|---------|
| 🟣 Claude Code | `~/.claude/skills/dot-skill` | slash command 原生支援 |
| 🟠 Hermes Agent | 跑 `python3 tools/install_hermes_skill.py --force` | `/dot-skill` 直接呼叫 |
| 🔵 OpenClaw | `~/.openclaw/workspace/skills/dot-skill` | 完整相容 |
| ⚫ Codex | `~/.codex/skills/dot-skill` | skill name 呼叫 |

最有趣的是安裝流程——**直接叫 Agent 自己裝自己**：

> 「幫我安裝 dot-skill 這個 skill：`https://github.com/titanwings/colleague-skill`」

Agent 會自動偵測宿主的 skills 目錄、完成 clone、註冊入口。生成的角色 Skill 也能一鍵安裝到任何宿主。

## 資料採集矩陣

| 來源 | 訊息 | 文檔 | 表格 | 備註 |
|------|:---:|:---:|:---:|------|
| 飛書自動採集 | ✅ API | ✅ | ✅ | 輸入姓名即全自動 |
| 釘釘自動採集 | ⚠️ 瀏覽器 | ✅ | ✅ | 釘釘 API 不支援歷史訊息 |
| Slack 自動採集 | ✅ API | — | — | 需 admin 安裝 Bot；免費版限 90 天 |
| 微信聊天記錄 | ✅ SQLite | — | — | 需先用 WeChatMsg / PyWxDump / 留痕匯出 |
| PDF/圖片/截圖 | — | ✅ | — | 手動上傳 |
| 飛書 JSON 匯出 | ✅ | ✅ | — | 手動上傳 |
| 郵件 `.eml`/`.mbox` | ✅ | — | — | 手動上傳 |
| Markdown/直接貼上 | ✅ | ✅ | — | 手動輸入 |

明顯是**為大中華企業辦公棧（飛書、釘釘、微信）量身打造**，Slack 是國際化延伸、英文版 README 是 i18n 門面——這決定了它的第一波社群組成以中文使用者為主。

## Celebrity 研究工具鏈

celebrity 家族最特別之處是附了一套**端到端研究管線**，把公眾人物的內容從影片變成結構化心智模型：

```bash
# 1. 下載影片字幕
bash tools/research/download_subtitles.sh "<video-url>" "./tmp/subtitles"

# 2. 字幕 → 可讀逐字稿
python3 tools/research/srt_to_transcript.py "./tmp/subtitles/example.srt"

# 3. 六維度研究合併（作品/訪談/決策/表達DNA/外部評價/時間線）
python3 tools/research/merge_research.py "./skills/celebrity/<slug>"

# 4. 品質檢查
python3 tools/research/quality_check.py "./skills/celebrity/<slug>/SKILL.md"
```

README 示範的 celebrity skill 就是 Andrej Karpathy——引用的資料來源正是社群作品 [alchaincyf/karpathy-skill](https://github.com/alchaincyf/karpathy-skill)。

## 專案結構

```
dot-skill/
├── SKILL.md                        # AgentSkills 標準 entrypoint
├── prompts/                        # 三家族 prompt 系統
│   ├── intake.md                   # [colleague] 資訊採集
│   ├── work_analyzer.md            # [colleague] 工作能力提取
│   ├── persona_analyzer.md         # [colleague] 人格提取
│   ├── work_builder.md             # [colleague] work.md 生成
│   ├── persona_builder.md          # [colleague] persona.md 6 層結構
│   ├── merger.md                   # [shared] 增量合併
│   ├── correction_handler.md       # [shared] 對話修正
│   ├── relationship/               # [relationship] 情感/衝突/修復
│   └── celebrity/                  # [celebrity] 六維研究 + 心智模型
├── tools/                          # Python 工具
│   ├── feishu_auto_collector.py    # 飛書
│   ├── dingtalk_auto_collector.py  # 釘釘
│   ├── slack_auto_collector.py     # Slack
│   ├── email_parser.py             # 郵件解析
│   ├── research/                   # [celebrity] 六維研究管線
│   ├── install_*_skill.py          # 多宿主一鍵安裝
│   ├── skill_writer.py             # Skill 檔案管理
│   └── version_manager.py          # 版本封存 & 回滾
├── skills/                         # 生成的 Skills（gitignored）
│   ├── colleague/
│   ├── relationship/
│   └── celebrity/
├── docs/PRD.md
└── LICENSE
```

## 進化機制

dot-skill 的設計避開「重訓 persona」，走輕量修正路徑：

- **📥 增量素材合併** — 追加檔案會自動分析 delta、合併進對應段落，**不覆蓋既有結論**
- **💬 對話式修正** — 使用者說「他不會這樣，他應該是 xxx」 → 寫入 Correction 層 → 立刻生效
- **🕰️ 版本管理** — 每次更新自動封存，能回滾到任意版本
- **🔬 celebrity 研究管線** — 字幕 → 逐字稿 → 六維研究 → 品質檢查

## Roadmap 四階段

| 階段 | 重點 |
|------|------|
| **Phase 1 — 社群建設** | GitHub Discussions、CONTRIBUTING.md、`good-first-issue`、v1.0.0 Release、公開專案看板 |
| **Phase 2 — dot-skill 通用化** | `/create-skill` 統一入口（已完成）、Gallery 分類升級、WeCom/iMessage/Windows 支援 |
| **Phase 3 — Skill 生態** | **多 skill 協作**（`/meeting @zhangsan @lisi` 三個 persona 同台討論）、關係圖譜、一鍵安裝社群 skill、**主動進化**（定期吸收新資料源） |
| **Phase 4 — 多模態** | **自動發貼圖/照片（相機版 persona）**、語音克隆、短影片「他的一天」生成 |

## 目前限制與注意事項

- **釘釘 API 不支援歷史訊息**，只能走瀏覽器自動化，可靠性較差
- **Slack 免費版限 90 天歷史**，對長期關係蒸餾是硬傷
- **微信需要先用 WeChatMsg / PyWxDump / 留痕等第三方工具匯出 SQLite**，門檻不低、且涉及私有資料合規
- **素材品質決定一切**——飛書群聊閒聊蒸餾出來的同事只會「嗯嗯好的」，得餵設計文件和 review 評論
- 仍是 demo 版本，Windows 相容性待優化、Issue 需要 triage

## 研究價值與啟示

### 關鍵洞察

1. **「數字生命 1.0」是產品敘事，不是技術定位。** 作者沒把它寫成「prompt engineering 工具」或「persona 模型」，而是用「離別」「傳承」「偶像」三個情感錨點鋪陳，標語「你們搞大模型的都是碼聖！血肉苦弱！賽博飛升！」直接引用《流浪地球》的迷因。**情感定位 × AgentSkills 技術紅利 × 中文社群 → 21 天 15.5K stars 的爆炸傳播**。技術專案早已不缺功能，缺的是「讓人願意分享」的敘事。

2. **「先做垂直 MVP 再平台化」的教科書路徑。** colleague.skill 只解決一個極窄問題、發了論文、衝到 13K stars；觀察社群用法（蒸餾前任、偶像、自己）後，不是拒絕而是升級通用引擎。**Roadmap 公開宣告改名**（預設 branch 從 `main` 改成 `dot-skill`）是一次品牌再定位，但保留舊 repo URL 作為 canonical，不破壞既有 star 和 SEO 流量——**品牌升級但繼承資產**。

3. **Persona 與能力解耦是關鍵架構決定。** Work Skill（做什麼）+ Persona（怎麼做）雙層，讓同一個人格可以掛不同能力、同一套能力可以換不同人格。**Correction 層**更是神來之筆——使用者在對話中吐槽「他不會這樣說」直接寫入、立刻生效，把 persona 調校從「訓練」降維成「對話」。

4. **六維度 celebrity 研究工具鏈是最高含金量模組。** 字幕下載 → 逐字稿 → 六維合併（作品/訪談/決策/表達 DNA/外部評價/時間線）→ 品質檢查，這是一條**半自動化的知識蒸餾管線**，遠超一般「抓 RAG 資料餵 LLM」的做法。隨便把這套管線拆出來當獨立工具就能再做一個 repo。

5. **AgentSkills 開放標準扮演通用介面。** Claude Code / Hermes / OpenClaw / Codex 四端通用，**不綁任何 Agent 廠商**。這是 2026 上半年 Skill 生態爆發（Karpathy Skills、khazix-skills、Nuwa Skill、Asgard Skills 等）的共同戰略——用開放標準對抗單一廠商的 lock-in。

6. **Gallery「無中間商」引流設計對齊個人品牌經濟。** [社群 Gallery](https://titanwings.github.io/colleague-skill-site/) 收錄 100+ 社區 Skills，每個 skill 卡片直接連到作者自己的 GitHub repo——dot-skill 不搶流量、作者樂意貢獻，形成正向循環。這是 meta-skill 設計中最容易被忽略但最重要的一環。

7. **來源品質分級表揭露對蒸餾材料的深度理解。** colleague 優先本人長文書寫、relationship 優先完整聊天記錄、celebrity 優先第一人稱書籍——**不同家族蒸餾出品質的上限來源不同**。這種分級指引比「餵什麼都行」的做法高明太多，直接提升生成 Skill 的品質天花板。

### 與其他專案的關聯

- **[khazix-skills](khazix-skills.md)**：同樣遵循 AgentSkills 標準、同樣來自中文 AI KOL 生態（數字生命卡茲克）。差別是 khazix 是**「蒸餾自己的方法論」**（1 人 × 個人 SOP），dot-skill 是**「蒸餾任何他人」**（N 人 × 通用引擎）。兩者構成「自我蒸餾 vs 他者蒸餾」的完整光譜，都在「數字生命」這個敘事框架下傳播。
- **[Andrej Karpathy Skills](andrej-karpathy-skills.md)**：dot-skill 的 celebrity 示範案例正是 Karpathy，且直接引用 [alchaincyf/karpathy-skill](https://github.com/alchaincyf/karpathy-skill)——兩者互為對照：一個是「把 Karpathy 蒸餾成 skill」的手工作品，一個是「給你工具讓你蒸餾任何人」的通用引擎。
- **[Claude Skills Guide](claude-skills-guide.md) / [Nuwa Skill](nuwa-skill.md) / [Asgard Skills](asgard-skills.md) / [Slavingia Skills](slavingia-skills.md)**：同屬 Skill 生態研究。dot-skill 的差異化點是**「人物蒸餾」垂直場景**而非通用 skill 庫。
- **[my-claude-devteam](my-claude-devteam.md)**：同樣是把「人」轉化成可呼叫單位（dev team 12 人），但前者是**虛構團隊**，dot-skill 是**真實人物**。兩者在 roadmap 上都會碰到「多角色協作」這一關——dot-skill Phase 3 明確寫了 `/meeting @zhangsan @lisi @wangwu`。
- **[cc-statusline](cc-statusline.md)**：同一時期（2026-04）的中文 Claude Code 生態爆發品。cc-statusline 解決 Claude Code 的 DX 問題，dot-skill 解決 Skill 生態的蒸餾問題——兩者共同標示 **2026 Q2 是中文 AI 生態的 Skill 大爆發期**。

Sources：
- [titanwings/colleague-skill GitHub](https://github.com/titanwings/colleague-skill)
- [dot-skill 社群 Gallery](https://titanwings.github.io/colleague-skill-site/)
- [titanwings/ex-skill](https://github.com/titanwings/ex-skill)
