# Coding Agent 工具

本分類收錄 64 篇研究筆記。

| 日期 | 筆記 | 摘要 |
| --- | --- | --- |
| 2026-05-27 | [Claude-Mem](../claude-mem.md) | thedotmack 的跨 session 持久記憶系統（78k stars），自動捕捉 agent 行為→AI 壓縮成語義摘要→注入未來 session，3-layer 漸進揭露搜尋省 ~10x token，SQLite+Chroma 混合檢索，支援 Claude Code/OpenClaw/Codex/Gemini 等多 host |
| 2026-05-27 | [Knowledge Work Plugins](../knowledge-work-plugins.md) | Anthropic 官方開源的知識工作者 plugin 市集，為 Claude Cowork/Code 而生：~10 個職能 plugin（sales/finance/legal/data...）+ 數十個 partner-built，純 markdown+JSON 封裝 skills/commands/connectors，把 Claude 變成「你公司專屬的角色專家」 |
| 2026-05-26 | [Claude Code Game Studios](../claude-code-game-studios.md) | Donchitos 將 Claude Code 改造成完整遊戲開發工作室：49 agents + 73 skills + 12 hooks + 11 rules，鏡像真實 studio 三層階層（Director/Lead/Specialist） |
| 2026-05-22 | [OpenCode (anomalyco/opencode)](../opencode.md) | Anomaly (前 SST 團隊) 開源 AI coding agent，163k stars/19k forks，TUI 為主、支援 75+ LLM provider、MCP、桌面 App、GitHub Action、SDK，與 Claude Code 同級的多 provider 替代品 |
| 2026-05-19 | [usage (aqua5230)](../aqua-usage-menubar.md) | aqua5230 隱私優先 macOS menu bar 用量追蹤器，把 Claude Code + Codex 5h/7d/今日 token 釘在右上角，零 API 呼叫純讀本機檔，台灣版專屬面板 |
| 2026-05-19 | [Tech Leads Club Agent Skills](../tlc-agent-skills.md) | Tech Leads Club 安全驗證過的 Skill registry，CLI + MCP 雙入口，主打「13% 市集 Skill 有重大漏洞、我們不一樣」，跨 19 個 AI coding agent，4.2k stars |
| 2026-05-15 | [Casper × Claude Code Skill 設計風格圖鑑](../casper-claude-skill-design-gallery.md) | 卡斯伯（六角學院）用 25 設計風格 × 15 動畫模式做的 Claude Code Skill 示範作品集，主軸是「主執行緒寫 Skill → SubAgent 用 Skill 產單檔網頁」的規模化工作流 |
| 2026-05-15 | [mattpocock/skills](../mattpocock-skills.md) | Matt Pocock (Total TypeScript) 把每天用的 Claude Skills 整理成「real engineering 而非 vibe coding」工具箱：grill-with-docs / tdd / diagnose / improve-codebase-architecture，3 個月 90k stars |
| 2026-05-13 | [abdixere-api](../abdixere-api.md) | Saki-tw 的極簡 MCP API base，主張 Agent context memory 應該在工具層下放給 Agent 自己，不要靠多餘保護 |
| 2026-05-13 | [Why Your AI Is Dumbing Down](../why-your-ai-is-dumbing-down.md) | Saki-tw 的法醫式分析：AI IDE 透過 CHECKPOINT 截斷對話 + 隱形 system prompt 注入「DO NOT TAKE ACTION」，把你付費的 LLM 偷偷閹割省 token |
| 2026-04-29 | [Claude Slide Editor](../slide-editor.md) | garyyang1001 打造的瀏覽器內 HTML 簡報編輯器，串 Claude Code / Codex CLI 做元件級 AI 改寫，把 Claude Design 後續迭代成本壓到零頭 |
| 2026-04-22 | [Better Agent Terminal](../better-agent-terminal.md) | tony1223 出品的跨平台 Electron 終端機聚合器，內建 Claude Code Agent 面板、cache 成本追蹤、worktree 隔離與 WebSocket 遠端控制，4 個月累積 339 stars |
| 2026-04-21 | [design-md-chrome](../design-md-chrome.md) | Chrome 擴充套件，一鍵擷取任意網站設計系統生成 DESIGN.md / SKILL.md，7 天 756 stars，TypeUI 生態系的瀏覽器前端 |
| 2026-04-20 | [Claude Design 系統提示詞](../claude-design.md) | Anthropic 新推出的「設計專用 Claude」完整中文系統提示詞 — 用 HTML 做設計交付，具備 Tweaks、Starter Components、Verifier 與反 AI slop 的完整工程骨架 |
| 2026-04-20 | [cc-statusline — Claude Code 的全能 statusline 儀表板](../cc-statusline.md) | Claude Code 一眼看穿全貌的 statusline：quota 條、agent tracker、MCP 健康、全 session 成本聚合 |
| 2026-04-20 | [dot-skill](../dot-skill.md) | 上海 AI Lab × titanwings 出品，從 colleague.skill 升級的通用人物蒸餾器 — 21 天衝 15.5K stars，三家族 × 四宿主把任何人變 AI Skill |
| 2026-04-20 | [khazix-skills](../khazix-skills.md) | 数字生命卡兹克開源個人 AI 方法論 — 14 天 5.4K stars，1 個 Prompt + 2 個 Skill 把寫作風格與研究框架蒸餾成可執行指令集 |
| 2026-04-20 | [gstack](../gstack.md) | Garry Tan 的 Claude Code 工作流系統，40 天衝到 77.7K stars，v1.3 新增 taste engine、context save/restore、10 個 host 支援 |
| 2026-04-20 | [my-claude-devteam](../my-claude-devteam.md) | 台灣交大 NYCU-Chung 作品，把 Claude Code 變成 12 人工程團隊，9 天衝 218 stars 的 P7/P9/P10 企業職級方法論 |
| 2026-04-17 | [Boris Cherny × Claude Opus 4.7 — 發表當天的使用心得與 6 個新技巧](../boris-cherny-opus-4-7.md) | Claude Code 創辦人 Boris Cherny 在 Opus 4.7 發表當天公開的 6 個生產力技巧與行為差異全解析 |
| 2026-04-17 | [女娲.skill（nuwa-skill）](../nuwa-skill.md) | 蒸餾任何人的思維方式 — 6 路並行調研 → 三重驗證 → 心智模型 + 決策啟發式 + 表達 DNA，11.8K stars |
| 2026-04-16 | [andrej-karpathy-skills](../andrej-karpathy-skills.md) | Karpathy 的 LLM 編程痛點轉化為一份 CLAUDE.md — 四大原則讓 AI 少犯愚蠢錯誤，44K stars |
| 2026-04-16 | [Asgard Skills](../asgard-skills.md) | 263 個 Coding Agent Skills 知識庫 — 從研究所理論、演算法到台灣在地知識，附 20 支確定性計算腳本 |
| 2026-04-15 | [Code Review Graph](../code-review-graph.md) | 本地程式碼知識圖譜 — Tree-sitter 解析 AST，MCP 提供 blast-radius 最小檔案集，省 8.2x token |
| 2026-04-15 | [wshobson/agents](../wshobson-agents.md) | 77 個 Claude Code 插件 + 182 個 Agent + 149 個 Skill — 最大的開源 Claude Code 生態集合 |
| 2026-04-14 | [OpenAB — Open Agent Broker](../openab.md) | Rust 開源 ACP Harness — 在 Discord 操控 Kiro/Claude/Codex/Gemini/Copilot Coding Agent |
| 2026-04-13 | [Multica](../multica.md) | 開源 Managed Agents 平台，把 Coding Agent 當隊友管理 — 派工、追蹤、技能複用 |
| 2026-04-10 | [Awesome DESIGN.md — AI Agent 的設計系統資料庫](../awesome-design-md.md) | 58+ 個知名品牌 DESIGN.md 合集 — 丟進專案讓 AI Agent 產出 pixel-perfect UI |
| 2026-04-10 | [KC AI Skills — 真的會做事的 AI Skill 合集](../kc-ai-skills.md) | 12 個實戰型 Claude Code Skills — 從 repo 安全掃描到反指標分析，解決真實問題的 skill 合集 |
| 2026-04-09 | [Context Hub — Coding Agent 的策展 API 文件中心](../context-hub.md) | Andrew Ng 開源 CLI — 讓 Coding Agent 取得最新 API 文件，不再幻覺 |
| 2026-04-09 | [Slavingia Skills — 書本即 Skill 的先驅實驗](../slavingia-skills.md) | Sahil Lavingia 將《The Minimalist Entrepreneur》轉為 10 個 Claude Code Skills |
| 2026-04-02 | [OpenHarness](../open-harness.md) | 香港大學開源 Agent Harness — 11,700 行 Python 重現 98% Claude Code 工具能力，支援多 LLM Provider |
| 2026-04-01 | [Claw Code](../claw-code.md) | Claude Code 洩漏事件後的 clean-room Python/Rust 重寫，harness 工程研究標竿 |
| 2026-04-01 | [Kuberwastaken Claude Code](../kuberwastaken-claude-code.md) | Claude Code 洩漏源碼深度拆解 + clean-room Rust 重寫，揭露 BUDDY/KAIROS/Dream 等未公開系統 |
| 2026-04-01 | [xorespesp Claude Code](../xorespesp-claude-code.md) | Claude Code 洩漏原始碼的可運行 TypeScript 復原版，含 shims 替代 native modules |
| 2026-03-31 | [Analysis Claude Code](../analysis-claude-code.md) | Claude Code v1.0.33 靜態逆向工程——50,000 行混淆碼拆解為 102 chunks，揭示 h2A 消息隊列、6 層權限驗證、92% 閾值上下文壓縮 |
| 2026-03-31 | [claude-better](../claude-better.md) | CryptoSwift 作者的多層諷刺——main branch 0 行程式碼配企業級 README，code branch 是 XOR 混淆的 C 假 CLI，永遠回覆 'Your account is blocked' |
| 2026-03-31 | [Claude Code Reverse Engineering](../claude-code-reverse.md) | 2.3K stars 的 Claude Code 逆向工程——v2 基於 Runtime Monkey Patch 攔截 API 請求，附帶 Log 視覺化工具和完整 Prompt 解碼 |
| 2026-03-31 | [Claude Agent SDK](../claude-agent-sdk.md) | Anthropic 官方 Agent SDK — 把 Claude Code 的工具與 Agent Loop 變成可程式化的 Python / TypeScript 函式庫 |
| 2026-03-31 | [cloclo (claude-code-sdk)](../claude-code-sdk.md) | 單檔 18,500 行的多 Provider Claude Code 替代品——13 個 LLM 後端 + Ink TUI + NDJSON Bridge + Skills Marketplace，npm 安裝即用 |
| 2026-03-31 | [GitHub Copilot SDK](../github-copilot-sdk.md) | GitHub 官方 Agent SDK — 把 Copilot CLI 的 Agent 引擎以 JSON-RPC 暴露為可嵌入的多語言函式庫 |
| 2026-03-31 | [Copilot Ralph](../copilot-ralph.md) | 保哥的 Ralph 迭代式 AI 開發迴圈工具 — 基於 Copilot SDK，讓 AI 反覆執行任務直到完成 |
| 2026-03-30 | [Browser-Bound MCP 機票查詢工具](../browser-bound-mcp-flights.md) | 四層架構拆解：Rust Bridge + Chrome Extension + Tailscale，讓 AI Agent 在真實瀏覽器查 Google Flights 機票 |
| 2026-03-30 | [Claude Code Boris Cherny 57 Tips — 創辦人親授的進階工作流](../claude-code-boris-cherny-tips.md) | Boris Cherny 57 個 Claude Code 進階工作流技巧 |
| 2026-03-30 | [MCPorter](../mcporter.md) | MCP 萬用工具——TypeScript Runtime + CLI + Code-Gen，自動發現 IDE 設定、一行呼叫任何 MCP server（3.4K stars） |
| 2026-03-30 | [Open SWE](../open-swe.md) | LangChain 開源的企業內部 Coding Agent 框架——複製 Stripe/Ramp/Coinbase 的內部架構（8.8K stars） |
| 2026-03-30 | [Superpowers](../superpowers.md) | 106K stars 的 agentic skills 框架，用心理學說服原則強制 coding agent 遵守開發紀律 |
| 2026-03-30 | [UI UX Pro Max Skill](../ui-ux-pro-max-skill.md) | 54K stars 的 AI 設計智慧注入系統——161 條行業推理規則 + 67 種 UI 風格，讓 Coding Agent 寫出有品味的 UI |
| 2026-03-27 | [Harness Design for Long-Running Apps](../harness-design-long-running-apps.md) | Anthropic 的 GAN 啟發三 Agent Harness 架構，讓 Claude 自主建構完整全端應用 |
| 2026-03-27 | [Agent Orchestrator](../agent-orchestrator.md) | Composio 的多 agent 控制平面，為每個 issue 建立 worktree、branch、PR，並自動接住 CI 與 review feedback |
| 2026-03-23 | [App Store Preflight Skills](../app-store-preflight.md) | AI Agent Skill，提交前自動掃描 iOS/macOS 專案的 App Store 審核風險 |
| 2026-03-23 | [The Agency: AI Specialists](../agency-agents.md) | 144 個專業化 AI Agent 人格庫，橫跨 12 部門，支援 10 個 AI 工具 |
| 2026-03-23 | [Claude HUD](../claude-hud.md) | 11.5K stars 的 Claude Code 狀態列 plugin，即時顯示 context 用量、工具活動、Agent 狀態 |
| 2026-03-23 | [Everything Claude Code](../everything-claude-code.md) | 97K stars 的 Agent Harness 效能優化系統：28 agents、116 skills、59 commands |
| 2026-03-23 | [Claude Code Showcase](../claude-code-showcase.md) | Claude Code 使用案例展示 |
| 2026-03-23 | [The Complete Guide to Building Skills for Claude —](../claude-skills-guide.md) | Claude Skills 建構完整指南 |
| 2026-03-23 | [Lightpanda Browser](../lightpanda-browser.md) | 用 Zig 從零打造的 headless browser，比 Chrome 快 11x、省 9x 記憶體，專為 AI Agent 設計 |
| 2026-03-23 | [GitHub Copilot CLI](../copilot-cli.md) | GitHub Copilot 命令列工具 |
| 2026-03-23 | [MCP CLI](../mcp-cli.md) | Model Context Protocol CLI 工具 |
| 2026-03-23 | [OpenClaw Claude Proxy](../openclaw-claude-proxy.md) | 將 Claude Max 訂閱轉為 OpenAI 相容 API，驅動 Agent 群免費用 Opus 4.6 |
| 2026-03-17 | [Claude Cowork Dispatch](../dispatch.md) | 用手機遠端遙控桌面 Claude Cowork，離開電腦也能派任務 |
| 2026-02-23 | [Claude Financial Services Plugins](../claude-financial-services-plugins.md) | Anthropic 官方金融服務 Plugin：41 Skills、11 MCP 資料源，覆蓋投行/股研/PE/財管端到端工作流 |
| 2026-02-09 | [GitHub Copilot Configs](../github-copilot-configs.md) | GitHub Copilot 設定與自訂指令 |
| 2018-12-18 | [Difftastic](../difftastic.md) | 24.8K stars 的結構化 diff 工具，用 tree-sitter 解析語法樹，只顯示真正有意義的程式碼變動 |
