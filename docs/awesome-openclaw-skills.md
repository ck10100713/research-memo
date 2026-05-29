---
date: "2026-05-29"
category: "資源彙整 / Awesome List"
card_icon: "material-shaker-outline"
oneliner: "VoltAgent 策展的 OpenClaw skill 精選清單（49.5k stars），從 ClawHub 官方 13,729 個社群 skill 中過濾出 5,211 個分 31 類，標註 spam/duplicate/低品質/crypto/惡意各排除多少，附 VirusTotal/Snyk 等安全工具，可看作「OpenClaw 生態的 App Store 看板」"
---

# Awesome OpenClaw Skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/VoltAgent/awesome-openclaw-skills> |
| 官網（清單可視化） | <https://clawskills.sh/> |
| 上游 Registry | ClawHub (`github.com/openclaw/skills`) |
| 策展團隊 | [VoltAgent](https://github.com/VoltAgent) |
| License | MIT |
| 社群 | [VoltAgent Discord](https://s.voltagent.dev/discord) |

## 專案概述

**Awesome OpenClaw Skills** 是 VoltAgent 在 2026/01 開源的 awesome-list（**49,470 stars / 4,835 forks**，MIT），是目前 OpenClaw 生態最具影響力的第三方策展清單，自稱「**官方資源後人氣 #1 的社群資源**」。

它解決的痛點很具體：OpenClaw 的官方 registry **ClawHub** 截至 2026/02/28 有 **13,729 個社群 skill**，但其中**超過一半是雜訊**（spam、重複、低品質、crypto、惡意）。VoltAgent 把這份吵雜的官方目錄過濾、去重、分類，產出 **5,211 個值得看的 skill**，按用途分 31 大類，附 GitHub + ClawHub 雙連結與一句話描述。

換句話說，它扮演的角色是「**OpenClaw 生態的 App Store 看板**」——當官方 registry 是 raw firehose，這份 awesome-list 是有品味的 editorial pick。

## 策展過濾（公開的扣分機制）

README 列出明確的過濾統計，是這份清單最珍貴的元資料：

| 過濾類別 | 排除數量 |
|---------|---------|
| 疑似 spam（大量帳號、bot 帳號、test/junk） | **4,065** |
| 重複 / 名稱相似 | **1,040** |
| 低品質或非英文描述 | **851** |
| Crypto / Blockchain / Finance / Trade | **886** |
| 惡意（安全研究員稽核，排除 VirusTotal 僅標記者） | **373** |
| **總共排除（未列入官方 registry 衍生清單）** | **7,215** |

= 13,729 - 7,215 ≈ 6,500（再經其他篩選後落在 5,211）。**過半官方 skill 被過濾**，這個數字本身就是 OpenClaw 生態狀態的重要指標。

> 特別注意：「Crypto / Blockchain / Finance / Trade」是被刻意排除的整類，這是 VoltAgent 的編輯立場——不是所有合法 skill 都會列入。

## 涵蓋類別（31 類、5,198 skill）

| 類別 | 數量 | 類別 | 數量 |
|------|------|------|------|
| **Coding Agents & IDEs** | 1,184 | Marketing & Sales | 103 |
| **Web & Frontend Development** | 919 | PDF & Documents | 105 |
| **DevOps & Cloud** | 393 | Transportation | 110 |
| **Search & Research** | 345 | Health & Fitness | 87 |
| **Browser & Automation** | 323 | Media & Streaming | 86 |
| Productivity & Tasks | 206 | Notes & PKM | 69 |
| CLI Utilities | 180 | Calendar & Scheduling | 66 |
| AI & LLMs | 176 | Security & Passwords | 54 |
| Image & Video Generation | 170 | Shopping & E-commerce | 51 |
| Git & GitHub | 167 | Personal Development | 50 |
| Communication | 146 | Speech & Transcription | 46 |
| 其他（含 Apple Apps、iOS/macOS Dev、Smart Home、Self-Hosted、Gaming、Moltbook、Clawdbot Tools、Data & Analytics 等） | — | | |

最大三類（Coding Agents / Web Frontend / DevOps）合計約 2,500 個 skill，佔近一半——反映 OpenClaw 用戶**主力是開發者**。

## 安裝方式

```bash
# ClawHub CLI
clawhub install <skill-slug>

# 或手動拷貝：
#   Global    → ~/.openclaw/skills/
#   Workspace → <project>/skills/
# 優先順序：Workspace > Local > Bundled
```

**Alternative**：直接把 skill 的 GitHub repo 連結貼進 assistant 對話、請它「使用」——agent 會自動處理 setup。

## 生態工具（README 推薦/Sponsor 位）

- **🔌 外部服務連接器**：[Composio](https://composio.dev/claw) — 管理 OAuth、scoped permission、1000+ apps 的 native tool call
- **☁️ Hosting**：[MyClaw](https://myclaw.ai/) — 一鍵雲端託管 OpenClaw 實例
- **🤖 25+ Model Providers**：OpenAI（`gpt-5.4` / `gpt-5.4-pro` 含 ChatGPT/Codex OAuth）、Anthropic 等，一行 config 切換

## Security Notice（值得整段引用的責任聲明）

> **Skills 是被策展，不是被稽核（curated, not audited）**。維護者隨時可能更新/替換內容。
>
> 安裝前**自己審查**程式碼。OpenClaw 與 **VirusTotal 合作**提供掃描，可在 ClawHub skill 頁面查報告。
>
> 推薦工具：
> - [Snyk Skill Security Scanner](https://github.com/snyk/agent-scan)
> - [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)
>
> Agent skill 可能含 **prompt injection、tool poisoning、隱藏 malware payload、不安全資料處理**。

這段是任何使用第三方 agent skill 都該牢記的紅色警示。

## 目前限制 / 注意事項

- **「策展，不是稽核」** — 列入清單≠安全，仍須自審
- **編輯立場有過濾偏好** — Crypto/Blockchain 整類被排除（合法 skill 也不收）
- **不接受外部 repo PR** — 必須先發布到 `github.com/openclaw/skills`，這裡才會收
- **資料快照性質** — 數字隨時間變動，目前 README 內 badge 顯示 5,198，文字部分稱 5,211/5,300+，數量會持續波動
- **5,211 個 skill 仍是巨量** — 即使過濾後也難以瀏覽完，需靠分類與搜尋

## 研究價值與啟示

### 關鍵洞察

1. **「過濾統計表」比「skill 清單本身」更有價值**：絕大多數 awesome-list 只給你「精選清單」，但這份明確公開「我排除了哪些、各排除多少」（4,065 spam、1,040 重複、886 crypto、373 惡意）。這份**透明的扣分機制**本身就是對 OpenClaw 生態現況的最佳體檢——超過 52% 的 ClawHub skill 被認定為雜訊。對任何要評估 OpenClaw 是否成熟的人，這是無價的元資料。

2. **「策展，不是稽核」是當代 agent skill 生態的共同困境**：清單明確聲明「列入≠安全」，並指向 VirusTotal、Snyk Agent Scan、Agent Trust Hub 等外部工具。這呼應本站 [Knowledge Work Plugins](knowledge-work-plugins.md) 與 [Claude Code Game Studios](claude-code-game-studios.md) 的觀察——agent skill 是**新一代供應鏈安全的弱點**（prompt injection、tool poisoning、hidden payload），策展層無法替代使用者自己的稽核。

3. **「Coding Agents & IDEs」+ 「Web/DevOps」佔近半說明 OpenClaw 主力用戶畫像**：1,184 + 919 + 393 ≈ 2,500/5,211，將近一半 skill 服務開發者。這對 OpenClaw 的定位重新校準——它表面上是「locally-running AI assistant」（給所有人），實際上的活躍社群仍以工程師為主。

4. **49.5k stars 揭示「策展品牌」可以超越「上游平台」**：VoltAgent 不是 OpenClaw 官方，但這份 awesome-list 衝到 49k stars，比許多上游平台還高。這印證**在資訊過載時代，策展層本身就是可獨立成立的品牌**——它把「找到好 skill」的痛點抽象成自己的產品，並透過 sponsor 位（Composio、MyClaw）變現。

5. **31 大類分類學是 OpenClaw 用例的最佳目錄**：從 Transportation（110）、Health & Fitness（87）、Moltbook（29）這些長尾類別，可以一眼看穿「人們實際上拿 OpenClaw 做什麼」。這比官方 marketing material 更真實。

6. **PR 政策（只收已發布到上游的 skill）反向強化官方 registry**：清單只列 `github.com/openclaw/skills` 上的 skill，不收個人 repo/gist。這個策展紀律一方面保證可追蹤性，另一方面也**把流量導回上游 registry**，形成「上游發布 → 策展層精選 → 流量回上游」的閉環。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs [Awesome Free Apps](awesome-free-apps.md) | 同為 awesome-list 策展，本清單規模大 ~10x、有公開過濾統計、且專攻單一生態（OpenClaw） |
| vs [Knowledge Work Plugins](knowledge-work-plugins.md) | KWP 是 Anthropic 第一方 plugin 市集（精選為主），本清單是 OpenClaw 第三方策展（廣度為主） |
| vs [Casper Claude Skill Design Gallery](casper-claude-skill-design-gallery.md) / [Superpowers](superpowers.md) | 那些是 Claude Code 生態的 skill 集合，本清單是 OpenClaw 生態的對等品 |
| vs ClawHub（上游官方） | 上游 13,729 個無篩選 skill；本清單過濾後 5,211 個分 31 類，並附安全與生態指引 |
| vs [OpenClaw](openclaw.md) 本身研究筆記 | OpenClaw 是平台，這份是平台上「最值得安裝什麼」的編輯版地圖 |

**最大啟示**：在「skill 經濟」時代，**策展層的價值正在追上甚至超越上游平台本身**。49.5k stars 證明「替你過濾雜訊」是個獨立可成立的產品，而公開過濾統計（哪些被排除、為什麼）比精選清單更能反映生態真實狀態。對任何想做 agent skill 生態的人，這份清單提供了三個可借鑑的範式：**透明的編輯立場、明確的責任聲明（策展≠稽核）、把流量回流上游的 PR 政策**。
