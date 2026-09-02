---
date: "2026-08-27"
category: "AI Agent 框架"
card_icon: "material-hammer-wrench"
oneliner: "自架單一 Go binary 的個人 AI Agent harness:缺工具時「自己寫一個」而非停手,sandbox 測試後存進共用工具庫,再透過 MCP 分享給 Claude Code / Codex 等 agent;同時是 TUI + 本機 daemon + MCP server/client。台灣 Pardn Chiu 個人專案,6.5 個月 1,015 commits / 182 releases"
tags:
  - agent-framework
  - harness
  - mcp
  - multi-agent
  - self-hosted
  - taiwan
---

# Agenvoy 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/agenvoy/Agenvoy> |
| 官方網站 | <https://agenvoy.com/>（tagline:*One binary. One install. Infinite tools.*） |
| 文件站 | <https://agenvoy.com/docs/> |
| Web 儀表板 | <https://web.agenvoy.com>(瀏覽器 UI,連到本機 daemon) |
| Go module | `github.com/pardnchiu/agenvoy` |
| 作者 | **Pardn Chiu(邱敬幃)** — 台灣,單一貢獻者 |

> Metadata(研究當下 **2026-08-27**,均取自 GitHub API / repo 一手來源):**472 stars / 43 forks / 0 open issues** · **Go**(100%,倉庫內 362 個 `.go` 檔) · **Apache-2.0**(有明確 LICENSE 檔) · 建立於 **2026-02-05**,最後 push **2026-08-26** · **1,015 commits**、**182 releases**(最新 `v0.32.15`)。

!!! warning "身分要先講清楚:是「組織」外殼,實為一人專案"
    owner `agenvoy` 在 GitHub 上登記為 **Organization**,但 Go module 路徑是 `github.com/pardnchiu/agenvoy`、README 所有連結(releases / issues / contributors)都指向 `pardnchiu/agenvoy`、footer 寫「©️ 2026 邱敬幃 Pardn Chiu」,**貢獻者只有 1 人、1,015 個 commit 全是他一人**。`agenvoy` org 等於個人品牌命名空間,不是團隊。**bus factor = 1**。另外 API 顯示的 `watchers_count`(472)是 GitHub 早期把 star 鏡射成 watcher 的遺留欄位,**真實 watcher(`subscribers_count`)= 2**。

## 專案概述

**Agenvoy 是一個「自架、單一 Go binary」的個人 AI Agent harness**——裝好後在你自己機器上跑一個 daemon,官網定位一句話:*「A Personal AI Agent & MCP Server on Your Machine」*、徽章寫「Open Source · Apache 2.0 · **Built in Taiwan**」。

它要解決的核心問題,用它自己的話講最傳神:**agent 遇到「沒有現成工具」時,不是停下來說做不到,而是「自己寫一個」**(API wrapper、script 或 extension),丟進 **sandbox 測試**,通過就存進工具庫,而且這個工具庫**還會透過 MCP 分享給其他 agent**(Claude Code、Codex、OpenCode…)。README 的「Why Agenvoy」第一條就是:*"Builds the missing tool instead of stopping."*

分類上它**不是一個你 `import` 的函式庫,而是一個本機 agent 平台 / harness**。同一顆 binary 同時扮演四種角色:

1. **互動式 TUI app**(`agen` 指令,預設模式)
2. **本機 HTTP daemon**(綁 `127.0.0.1`)+ 瀏覽器儀表板
3. **MCP server**(把自己的 sandbox 工具暴露給其他 agent)
4. **MCP client**(消費外部 MCP server)

!!! note "定位對照:它不跟你現有的 agent 搶,而是當它們的「共用工具庫」"
    README 沒有跟其他框架比高下的表格,而是主打**互通**:*"Works with the agents you already use"*——一行設定,Claude Code / Codex / OpenCode 就能連上、共用它 sandbox 過的工具庫。這跟站上 [qm](qm.md)(YC 的 multiplayer agent harness,偏協作平台)、[Open Harness](open-harness.md) 是不同取向的 harness:Agenvoy 是 **local-first、Go-first、以「共用工具庫」為核心**。適合已在用 CLI agent、想加一層自架 sandbox + 可重用工具庫的人。

## 六個看點

### 1. 自我延伸工具 + sandbox 測試 + 持久共用工具庫(招牌)

這是全專案最獨特的一環,也是核心 loop:**沒有匹配的工具 → agent 自己寫 → sandbox 跑一遍驗證 → 存進共用 registry → 其他 agent 也能用**。而且工具庫是**跨 agent 共用**的——透過 MCP 暴露,別的 agent 連上就直接繼承這批工具。這種「自造工具 + 跨 agent 共享」的組合在 agent 生態裡少見。

搭配一個**惰性 schema 注入**設計:**13 個內建工具帶完整 schema 出廠**(`ask_user, calculate, edit_file, fetch_page, find_files, find_knowledge, find_tools, read_files, reasoning_guide, run_command, run_skill, search_web, write_todo`),其餘工具一開始只有 name + description,**第一次要用時才透過 `find_tools(mode=search)` 把參數 schema 注入**——避免一開始就把幾百個工具 schema 塞爆 context。

### 2. OS 級 sandbox + 「每次請求授權」取代 sudo(安全邊界)

- daemon 只綁 `127.0.0.1`;敏感的設定 / 管理端點再加一層 `localhostOnly()` 守門。
- 指令執行走三關:allow 規則 → **AST 層級 shell 驗證**(`mvdan.cc/sh`)→ **OS sandbox**(macOS `sandbox-exec`、Linux `bwrap`)。
- 預設 `$HOME` 內可寫;**寫到 `$HOME` 外或非白名單指令不是直接拒絕,而是跳出確認、並且「要求輸入 OS 密碼」**,授權範圍只限這個 session + 這個路徑/binary。作者明講:*"There is no elevated or `/sudo` mode; per-request authorization replaced it."*
- 憑證放 **OS keychain**,不進 repo。

### 3. Skill-aware 模型路由(dispatcher / primary / fallback / summary)

模型分四種角色:**dispatcher**(派工)、**primary**(主力)、**fallback**(送出失敗時接手)、**summary**(摘要)。路由時會把**匹配到的 Skill 描述**餵進模型選擇(所謂 "skill-aware routing")。另有 process-local 的 **`ModeDefault` / `ModeFast`** 切換(TUI 按 Shift+F,標頭顯示 `[fast]`)。Skill 放在 `~/.config/agenvoy/skills`,由 skill scanner 掃描。

官方推薦的省錢配置:拿免費的 **NVIDIA NIM** token 跑 `gpt-oss-20b`(dispatcher)+ `gpt-oss-120b`(fallback + summary),primary 再接一個訂閱制模型(ChatGPT Plus $20/mo 或 SuperGrok $30/mo)。

### 4. Origin-aware 確認路由(CLI / Web / Telegram / Discord)

跨 channel 的關鍵細節:pending 的提問 / 確認帶一個 **origin 前綴**(`cli-` / `chat-` / `tg-` / `dc-`),**只有發起的那個 channel 能 resume 它**。你從 Telegram 問的問題,確認框就回到 Telegram,不會錯亂到 Web。四個 channel 共用同一條 event pipeline,各自帶 per-channel auth。

### 5. 一顆 binary 全自架:排程、記憶、檔案搜尋都在本機

README 能力表(節錄):自動生成工具 · **一句話自我排程**(cron)· 長期記憶 · 知識筆記 · 檔案搜尋 · **Sub-Agent(multi-agent)** · MCP client(官方 go-sdk,支援 `tools/list_changed` 即時刷新)· MCP server · reasoning guides · Tool Market(工具分享/安裝)· 圖片生成 · 即時指令輸出 · 檔案邊界防護 · **MCP OAuth**(loopback callback `localhost:17988`,token 進 OS keychain)· 影音轉文字 · **自我修復**(執行失敗後自動修正)。

持久化都在 `~/.config/agenvoy/`:`config.json`(fsnotify 熱重載)、每 session 目錄、`.store/history.db`(SQLite 搜尋索引)、**ToriiDB** `.store/db_0..db_3`(db_0 工具快取 / db_1 對話 / db_2 工具錯誤記憶 / db_3 operator 知識)。

### 6. 垂直整合在作者自己的 Go 生態上(而非第三方框架)

這點很不一樣:Agenvoy 的底座**幾乎全是作者自己的 `pardnchiu/*` 函式庫**——`ToriiDB`(embedding / 語意儲存)、`go-llm-router`(多供應商模型路由,類似 [LiteLLM](litellm.md) 的角色)、`go-scheduler`(cron)、`go-bot`、`go-browser`、`go-sqlkit`、`go-pkg`、`go-utils`。它是這位作者整套 Go 生態的**集大成之作**,不是拼裝 LangChain/LlamaIndex 的產物。第三方直接依賴主要是 UI/協定層:`bubbletea`(TUI)、`gin`(HTTP)、`modelcontextprotocol/go-sdk` v1.6.1(MCP 官方 SDK)、`go-telegram/bot`、`discordgo`、`go-rod`(headless 瀏覽器)、`mattn/go-sqlite3`。

## 技術棧與安裝

- **語言 / 版本**:純 Go(`go 1.25.1`),倉庫內含 `cmd/app`(進入點)、`internal/`(agents / runtime / tools / session / filesystem / knowledge)、`extensions/`(9 個內建 skill + public API 目錄)、`configs/`、`doc/`、`page/`(編譯進 binary 的 web 儀表板)。
- **內建 skills(9 個)**:`code-reviewer, commit-generate, extension-install, extension-upload, readme-generate, scheduler-skill-creator, search-suitable-public-api, skill-creator, version-generate`。
- **安裝**:`curl -fsSL https://agenvoy.com/scripts/install.sh | bash`。macOS 另建議 `sudo pmset -c sleep 0`,免得睡眠打斷排程。
- **並發**:每 session slot 上限 `MaxSessionTasks` 預設 = 4 × CPU 數;超額的 task 進佇列(仍可見、可取消)而非直接拒絕;每個 task 記錄 owning PID,PID 死掉的視為 stale 清掉。

## 注意事項(一手來源實測)

- **平台缺口**:release binary 只有 `darwin-arm64` + `linux-amd64/arm64`,**沒有 Windows、也沒有 Intel Mac(`darwin-amd64`)**。Linux 用戶還得自備 `bwrap` 才有 sandbox。
- **測試稀疏**:362 個 Go 檔中只找到少數 `_test.go`(集中在 `toolAdapter` 與 `calculate`),相對於程式碼規模偏薄。
- **bus factor = 1**:一人專案、2 個真實 watcher、0 open issue(issue 有開但沒人提);PR 政策限 collaborator。整個底座依賴作者自己的 `pardnchiu/*` 函式庫,**它們的成熟度就是本專案的成熟度**。
- **「10 個模型供應商」未逐一列名**:官網與 architecture doc 都說「10 LLM providers」,但 README 沒把這 10 家點名(topics 暗示含 OpenAI / Gemini / Grok / DeepSeek / OpenRouter / NVIDIA NIM),**無法逐家驗證**。
- **文件與程式碼有微小落差**:architecture doc 寫 `go-llm-router v0.5.1`,`go.mod` 釘的是 v0.5.3。repo 根目錄**沒有明確 roadmap / TODO**。
- 授權為 Apache-2.0(明確、商用友善),這點沒有問題。

## 研究價值與啟示

### 關鍵洞察

1. **「缺工具就自己造」把 agent 從『固定工具集的執行者』推向『會擴充自己的 runtime』**:多數 agent 框架的工具是人預先寫好註冊的,遇到沒有的就回「我沒有這能力」。Agenvoy 的核心 loop 是**自造 → sandbox 驗證 → 存庫 → 跨 agent 共享**,把「工具集」從靜態資產變成會長大的共用資本。這比單純的 function calling 更接近「self-improving agent」的實作樣貌。

2. **「共用 sandbox 工具庫 + MCP」是它真正的殺手鐧,而非又一個 agent**:它不跟 Claude Code / Codex 搶位置,而是當它們的**共用工具後端**——一份 sandbox 過的工具,多個 agent 透過 MCP 都能用。這種「互補而非取代」的定位,對照 [Bring Your Own Agent](bring-your-own-agent.md) 的 BYOA 思路是同一條路線:harness 層要贏,靠的是「讓你現有的 agent 更強」而非要你換掉它。

3. **「per-request 授權取代 sudo」是本機 agent 安全的一個乾淨解法**:不給 agent 一個常開的 elevated 模式(那是災難),而是**預設 `$HOME` 內可寫、越界就跳 OS 密碼確認且限定 scope**。對「本機自主 agent 的最小權限」是可直接借鏡的設計——把授權從「一次給到底」拆成「每次請求、限定範圍」。

4. **Go-first 在 agent 生態是稀缺選擇,而「單一 binary 自架」正是 Go 的主場**:競品幾乎清一色 Python/TS。Go 的靜態編譯讓「一顆 binary、一次安裝、無外部 runtime」變得自然——TUI + daemon + web + MCP server/client 全塞進同一顆執行檔。對想做 **local-first、可離線、好散布**的 agent 工具,這是很有說服力的技術選型範例。

5. **一人 6.5 個月 1,015 commits / 182 releases,是「垂直整合個人生態」的極端案例**:作者先把 ToriiDB、go-llm-router、go-scheduler 等基礎件一個個做出來,Agenvoy 是把它們縫成產品的 capstone。好處是掌控力極強、沒有第三方框架的版本地獄;代價是 bus factor = 1、成熟度綁在個人 velocity 上。對照 [Building Applications with AI Agents](building-applications-with-ai-agents.md) 那種「拼裝多個成熟第三方框架」的取向,正好是光譜的兩端。

### 與其他研究的關聯

- 與 [qm](qm.md)、[Open Harness](open-harness.md)、[harness 設計(長時運行 app)](harness-design-long-running-apps.md):四者都在談 agent「harness」層,但 Agenvoy 最偏 **local-first + 共用工具庫**;qm 偏 multiplayer 協作、harness-design 偏長時運行/記憶/排程的工程論述,Agenvoy 的自我排程 + 長期記憶 + ToriiDB 正是後者的一個具體落地。
- 與 [MCP for Beginners](mcp-for-beginners.md)、[MCP CLI](mcp-cli.md):Agenvoy 同時是 MCP server + client,是「MCP 既暴露又消費工具」的完整雙向實例,可當 MCP 進階案例讀。
- 與 [LiteLLM](litellm.md):作者的 `go-llm-router` 扮演與 LiteLLM 相同的「多供應商、一個介面」角色,是 Go 版的 LLM gateway 對照。
- 與 [Bring Your Own Agent](bring-your-own-agent.md):同屬「讓你現有 agent 更強、而非取代」的互通哲學。
- 與 [OpenCode](opencode.md)、其他 CLI agent:Agenvoy 明確把它們列為可連上共用工具庫的 client,是這些 CLI 工具的橫向後端。

## 一句話總結

> 台灣 Pardn Chiu 一人打造的自架 Go agent harness——最大看點是**「缺工具就自己寫、sandbox 測完存進共用庫、再透過 MCP 分享給 Claude Code / Codex」**這條 self-extending loop,加上「per-request 授權取代 sudo」的本機安全設計;一顆 binary 兼 TUI + daemon + web + MCP server/client,6.5 個月狂飆 182 個 release,代價是 bus factor = 1、只支援 arm64 Mac 與 Linux。
