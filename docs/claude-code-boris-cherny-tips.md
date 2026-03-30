---
date: "2026-03-30"
category: "Coding Agent 工具"
icon: "material-file-document-outline"
oneliner: ""
---
# Claude Code Boris Cherny 57 Tips — 創辦人親授的進階工作流

## 資料來源

| 項目 | 連結 |
|------|------|
| INSIDE 報導 | [Claude Code 創辦人示範 15 個功能](https://www.inside.com.tw/article/40974-claude-code-boris-cherny-hidden-features-voice-scheduling-workflow-2026) |
| 完整 57 Tips 技能檔 | [howborisusesclaudecode.com](https://howborisusesclaudecode.com/) |
| Boris 原始推文串（Part 1） | [Threads — 我的設置](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm/) |
| Boris 原始推文串（隱藏功能） | [Threads — Hidden Features](https://www.threads.com/@boris_cherny/post/DWfjnqGFPHE) |
| 53 Tips 整理 | [enkr1 Blog](https://blog.enkr1.com/boris-cherny-claude-code-workflow/) |
| Substack 分析 | [How Boris Cherny Uses Claude Code](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow) |
| Medium 技能分析 | [Boris Cherny's Tips Are Now a Skill](https://alirezarezvani.medium.com/boris-chernys-claude-code-tips-are-now-a-skill-here-is-what-the-complete-collection-reveals-b410a942636b) |

## 概述

| 項目 | 內容 |
|------|------|
| 作者 | **Boris Cherny** — Claude Code 創辦人/負責人（Anthropic） |
| 發布期間 | 2026-01-02 至 2026-03-17（8 卷推文串） |
| 總計 Tips | **57 個** |
| 推文瀏覽量 | 隱藏功能篇 56 萬+ |
| 背景數據 | Anthropic 內部工程師程式碼產出年成長 **200%+**；Claude Code 佔 GitHub 公開提交量 **4%**（SemiAnalysis 估計，年底可能 20%） |

Boris Cherny 透過 8 卷推文公開了 57 個 Claude Code 進階技巧，涵蓋從並行執行、排程自動化到語音驅動工作流。核心哲學三原則：

1. **並行化**：把循序工作轉為並行執行
2. **先規劃**：投資在計畫上，讓實作一次成功
3. **驗證迴圈**：讓 Claude 能驗證自己的產出，品質提升 2-3x

---

## 一、並行處理（最大生產力提升）

### Git Worktrees（團隊第一推薦）

```bash
claude --worktree my_worktree        # CLI 隔離 worktree
claude --worktree my_wt --tmux       # 在 Tmux 中啟動
```

- 同一 repo 開多個完全獨立的工作樹
- Boris 隨時有 **10-15 個並行 Claude session**：5 個 terminal + 5-10 個 browser + mobile
- Shell alias：`za`, `zb`, `zc` 一鍵切換
- Desktop App：Code tab → 勾選 "worktree"
- Agent frontmatter 可設 `isolation: worktree` 強制隔離
- 非 Git VCS（Mercurial/Perforce/SVN）：透過 `WorktreeCreate` / `WorktreeRemove` hooks

### /batch — 並行程式碼遷移

```
/batch migrate src/ from Solid to React
/batch migrate from jest to vite
```

- 互動式規劃 → 數十個 agent 在各自 worktree 並行執行
- 每個 agent 獨立測試、獨立建 PR

### Subagent Orchestration

- 在 prompt 中加「use subagents」→ Claude 自動分散工作
- `.claude/agents/` 存放自訂 agent（build-validator, code-architect, code-simplifier, verify-app）

---

## 二、排程與自動化

### /loop — 循環任務（≤3 天）

```
/loop 5m /babysit          # 每 5 分鐘自動處理 code review
/loop 30m /slack-feedback   # 每 30 分鐘整理使用者回饋
/loop babysit all my PRs. Auto-fix build issues and when comments come in, use a worktree agent to fix them
/loop every morning use the Slack MCP to give me a summary of top posts I was tagged in
```

Boris 稱 loop 是「Claude Code 最強功能之一」。

### /schedule — 雲端排程（無限期）

- 超越 `/loop` 的 3 天限制，可排程最長一週的任務
- 不依賴本機——雲端執行
- 範例：每日從已 ship 的 PR 更新文件、CI 失敗自動修復、Slack 通知

### Hooks 系統

| Hook | 觸發時機 | 用途 |
|------|---------|------|
| **SessionStart** | session 啟動 | 自動載入專案上下文 |
| **PreToolUse** | tool 執行前 | 自動記錄操作日誌 |
| **PostToolUse** | tool 執行後 | 自動格式化程式碼（Boris 用 `bun run format`） |
| **PermissionRequest** | 需要授權時 | 轉發至 WhatsApp/Slack/Opus 4.5 自動核准 |
| **Stop** | Claude 停止前 | 跑 lint/test/部署前檢查；或 poke Claude 繼續 |
| **PostCompact** | context 壓縮後 | 重新注入關鍵指令（防止壓縮時遺失） |

---

## 三、跨裝置工作

| 功能 | 用途 |
|------|------|
| **--teleport** | 本機 ↔ 雲端 session 無縫切換 |
| **/remote-control** | 從手機/瀏覽器即時操控本機 session |
| **行動 App** | iPhone/Android Claude app 的 Code 分頁 |
| **Cowork Dispatch** | Claude Desktop 的安全遠端控制（MCP + 瀏覽器） |
| **iMessage Plugin** | `Text Claude like a friend` — 任何 Apple 裝置傳訊息給 Claude |

Boris 的模式：早上用手機啟動 session → 在 desktop 接手繼續。

---

## 四、規劃與品質

### Plan Mode（必備）

1. `shift+tab` 兩次進入 plan mode
2. 反覆迭代計畫直到滿意
3. 切到 auto-accept mode → Claude 通常一次到位
4. 如果實作偏離 → 重新進 plan mode（不要 patch）

進階：**第一個 Claude 寫計畫，第二個 Claude 以 staff engineer 身份 review**。

### /simplify — 品質審查

- 附加在 prompt 後面
- 並行 agent 審查改動過的程式碼：重用性、品質、效率

### CLAUDE.md — 複合知識

- 單一 git-tracked 文件，記錄 Claude 所有錯誤行為
- 格式：「Claude should never [行為]」
- 團隊每週貢獻多次
- 修正 Claude 時說：「Update CLAUDE.md so you don't make that mistake again」
- PR 標記 `@.claude` → GitHub Action 自動更新 CLAUDE.md

### 驗證（Boris 最重要的 Tip）

> 「Give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result.」

- Chrome 擴充套件截圖驗證 UI
- bash 指令 + test suite 驗證邏輯
- Docker logs 驗證分散式系統
- 確保 Claude 有 domain-specific 測試手段

---

## 五、權限與安全

| 方式 | 說明 |
|------|------|
| **/permissions** | 白名單安全指令，支援 wildcard：`Bash(bun run *)`、`Edit(/docs/**)` |
| **/sandbox** | 檔案 + 網路隔離（macOS/Linux） |
| **Auto Mode** | `shift+tab` 循環：plan → auto → normal。內建分類器評估安全性 |
| **--bare** | 跳過自動載入，啟動時間快 10x（適合 CI/batch） |

**絕對不要用** `--dangerously-skip-permissions`。

---

## 六、工具整合

| 工具 | 方式 | Boris 用法 |
|------|------|-----------|
| **Slack** | MCP | 貼 bug thread → 說「fix」→ Claude 修 |
| **BigQuery** | bq CLI | 「我 6 個月沒寫 SQL 了」 |
| **Sentry** | MCP | 自動存取 error log 除錯 |
| **GitHub** | @.claude PR tag | 自動更新 CLAUDE.md |

---

## 七、個人化與開發者體驗

| 功能 | 指令 | 說明 |
|------|------|------|
| 終端機 | Ghostty | GPU 渲染、同步輸出、24-bit color |
| 狀態列 | `/statusline` | 顯示 model、cost、context 剩餘、git branch |
| Session 顏色 | `/color` | 每個 session 不同顏色，視覺區分 |
| Session 命名 | `--name "auth-refactor"` | 人類可讀 session 識別 |
| 語音輸入 | `/voice` 或 macOS `fn×2` | 比打字快 3x，更詳細的 prompt |
| Vim 模式 | `/vim` | 原生 vim 鍵綁定 |
| 努力等級 | `/effort max` | 四級：low/medium/high/max |
| 輸出風格 | `/config` | Explanatory / Learning / Custom |
| 自訂 spinner | settings.json | Star Trek 主題等 |
| 記憶系統 | `/memory` + `/dream` | 自動記憶 + 自動整理（REM sleep 隱喻） |

---

## 八、Slash Command 速查

| 指令 | 功能 |
|------|------|
| `/loop [interval] [task]` | 循環任務（≤3 天） |
| `/schedule` | 雲端排程（無限期） |
| `/batch [task]` | 並行遷移/批次處理 |
| `/simplify` | 並行品質審查 |
| `/btw [question]` | 不中斷主任務的旁支問答 |
| `/branch` | 分叉嘗試方向 |
| `/teleport` | 本機↔雲端切換 |
| `/remote-control` | 遠端操控本機 session |
| `/voice` | 語音輸入 |
| `/effort [level]` | 推理深度 |
| `/permissions` | 權限白名單 |
| `/sandbox` | 隔離模式 |
| `/statusline` | 狀態列設定 |
| `/color` | Session 顏色 |
| `/memory` | 持久記憶 |
| `/dream` | 記憶整理 |
| `/config` | 主題/通知/風格 |
| `/plugin` | 插件市場 |
| `/boris` | 載入 57 Tips 技能文件 |

---

## 安裝 Boris Tips Skill

```bash
mkdir -p ~/.claude/skills/boris && \
curl -L -o ~/.claude/skills/boris/SKILL.md \
  https://howborisusesclaudecode.com/api/install
```

之後在任何 session 中輸入 `/boris` 即可載入。

---

## 研究價值與啟示

### 關鍵洞察

1. **並行化是最大生產力提升**：Boris 隨時 10-15 個並行 session，團隊第一推薦是 git worktrees。`/batch` 可以開數十到數千個 worktree agent。這不是單一 agent 更聰明——而是多個 agent 同時工作。

2. **Plan Mode 是必備的第一步**：所有複雜任務都先進 plan mode。Claude 通常一次到位是因為計畫做得好，不是因為它天生就對。「Don't patch; redesign the approach」——如果實作偏離就重新規劃。

3. **驗證迴圈是品質的 2-3x 倍增器**：Boris 最重要的 tip。不是更好的 prompt，而是讓 Claude 有能力驗證自己的產出。Chrome extension、test suite、Docker logs——domain-specific 驗證才是關鍵。

4. **CLAUDE.md 是複合知識的載體**：每次 Claude 犯錯就更新 CLAUDE.md。團隊級別的共享知識，透過 `@.claude` PR tag 自動化。「Claude learns once, team benefits forever.」

5. **Hooks 讓 Claude Code 成為可程式化的 agent runtime**：SessionStart、PostToolUse、PostCompact、PermissionRequest——這些 lifecycle hook 把 Claude Code 從「工具」變成「平台」。

6. **/loop + /schedule 代表 agent 的時間維度**：Claude 不再只是「回答問題」或「執行一次任務」。它可以循環監控、排程執行、自主處理——這是 agent 從「工具」到「同事」的轉變。

7. **行動端 + 遠端控制 = 隨時隨地的 AI 開發**：早上手機啟動 session → 通勤時語音輸入 → desktop 接手繼續。這不是「手機寫 code」，而是「隨時指揮 agent」。

### 與我們的 Skill 系統對照

| Boris 建議 | 我們的現狀 |
|-----------|-----------|
| Plan Mode 必備 | 我們的 `/research` skill 有類似流程 |
| CLAUDE.md 複合知識 | 已有 CLAUDE.md，但未自動化更新 |
| Slash Commands | 已有多個 skill（/research, /commit 等） |
| Hooks | 可考慮加入 PostToolUse auto-format |
| Worktrees | 已有 worktree 支援，可更積極使用 |
| /loop | 可用於持續研究或監控任務 |
