---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-view-dashboard-variant"
oneliner: "Claude Code 一眼看穿全貌的 statusline：quota 條、agent tracker、MCP 健康、全 session 成本聚合"
---
# cc-statusline — Claude Code 的全能 statusline 儀表板

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [NYCU-Chung/cc-statusline](https://github.com/NYCU-Chung/cc-statusline) |
| README 繁中 | [README.zh-TW.md](https://github.com/NYCU-Chung/cc-statusline/blob/main/README.zh-TW.md) |
| Claude Code statusline 寬度 issue | [#22115](https://github.com/anthropics/claude-code/issues/22115) |
| Claude Code MCP 即時狀態 issue | [#5511](https://github.com/anthropics/claude-code/issues/5511) |

## 專案概述

| 項目 | 內容 |
|------|------|
| 作者 | **NYCU-Chung**（陽明交通大學） |
| Stars / Forks | **82 / 4** |
| 語言 | JavaScript（純 Node.js，無外部依賴） |
| License | MIT |
| 建立日期 | **2026-04-12**（本筆記建立時僅 8 天） |
| 定位 | Claude Code 的 statusline + 配套 hooks 合集 |
| 安裝方式 | Claude Code plugin marketplace 一行指令 |

`cc-statusline` 是一個為 **Claude Code 打造的 statusline 儀表板**，把過去需要用 slash command 查的所有資訊整合在底部一條 line 上。核心 `statusline.js`（34KB，純 Node.js）搭配 6 個可選 hook 餵資料，無額外 npm 依賴。

適合場景：
- 想在終端機「一眼看到」session 狀態、quota、成本、跑中的 agent
- 用 Claude Code `--resume` 找不回 session（它把 summary 寫進 JSONL 當 custom-title）
- Max / Team 方案需要精準追蹤 5h / 7d quota 的人

---

## 它顯示什麼（13 個 section）

| Section | 顯示內容 |
|---------|---------|
| **session summary** | Claude 自動產生的整 session 摘要（每 ~10 條訊息重寫一次，壓縮到 ~120 字元內） |
| **directory** | 目前 cwd + `+added -removed lines` |
| **repo + branch** | `owner/repo`（從 `git remote` 解析）+ branch + `(N changed)` |
| **cost** | `cost $TOTAL ($SESSION this session) · duration` — **全歷史累計** + 當前 session 即時 |
| **model** | 模型名 + effort 等級（5 色梯度：`low` 暗 / `medium` 綠 / `high` 黃 / `xhigh` 橘 / `max` 紅） |
| **tokens / context / compact** | tokens 全歷史 + session、context window %、compact 次數 |
| **5h-quota** | 綠→黃→紅 bar + 自動倒數 `resets Xh Ym`；過期後自動歸零 |
| **7d-quota** | 同上，以天/時顯示 |
| **agents** | 本 session 跑過的 subagent：`critic ✓ 5m ago`、平行併成 `critic ○×3` 或 `critic ✓×2 5m ago` |
| **memory** | 目前載入哪些 CLAUDE.md scope（global / project / rules） |
| **mcp** | 透過 `claude mcp list` 探測的健康狀態：啟用數 + 失敗服務（`✘ failed`、`△ needs auth`） |
| **edited** | 本 session 最近編輯的檔案（新→舊，過長以 `…` 前縮） |
| **history** | 右欄：最近訊息（▶ 你 / ◀ Claude），隨終端寬度擴展 |

---

## 安裝（Plugin 一行指令）

```bash
claude plugin marketplace add NYCU-Chung/cc-statusline
claude plugin install cc-statusline@cc-statusline
```

Hooks 會自動註冊，但還要手動加 statusLine 設定到 `~/.claude/settings.json`：

```json
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/statusline.js",
    "refreshInterval": 30
  }
}
```

然後 clone + copy：

```bash
git clone https://github.com/NYCU-Chung/cc-statusline ~/cc-statusline
cp ~/cc-statusline/statusline.js ~/.claude/statusline.js
cp ~/cc-statusline/hooks/*.js ~/.claude/hooks/
```

### Hook 連線（完整功能需要）

```json
{
  "hooks": {
    "SubagentStart":   [{ "matcher": ".*", "hooks": [{ "type": "command", "command": "node ~/.claude/hooks/subagent-tracker.js" }]}],
    "SubagentStop":    [{ "matcher": ".*", "hooks": [{ "type": "command", "command": "node ~/.claude/hooks/subagent-tracker.js" }]}],
    "PreCompact":      [{ "matcher": ".*", "hooks": [{ "type": "command", "command": "node ~/.claude/hooks/compact-monitor.js" }]}],
    "UserPromptSubmit":[{ "hooks": [
      { "type": "command", "command": "node ~/.claude/hooks/message-tracker.js" },
      { "type": "command", "command": "node ~/.claude/hooks/summary-updater.js" }
    ]}],
    "Stop":            [{ "matcher": "*", "hooks": [
      { "type": "command", "command": "node ~/.claude/hooks/message-tracker.js" }
    ]}],
    "PostToolUse":     [{ "matcher": "Write|Edit", "hooks": [
      { "type": "command", "command": "node ~/.claude/hooks/file-tracker.js" }
    ]}]
  }
}
```

### 6 個 Hook 各司其職

| Hook | 事件 | 功能 |
|------|------|------|
| `subagent-tracker.js` | SubagentStart/Stop | 追蹤跑中或完成的 subagent（含平行 invocations） |
| `compact-monitor.js` | PreCompact | 計算 context 壓縮次數 |
| `file-tracker.js` | PostToolUse (Write/Edit) | 記錄最近編輯的檔案 |
| `message-tracker.js` | UserPromptSubmit / Stop | 快取最近訊息給 history 欄 |
| `summary-updater.js` | UserPromptSubmit | 每 ~10 條訊息要 Claude 重寫全 session 摘要 |
| `mcp-status-refresh.js` | 自動由 statusline 在背景 spawn | 從 `claude mcp list` 更新 `~/.claude/mcp-status-cache.json`；cache 新鮮（< 90s）就跳過 |

---

## 工程亮點（解決了 Claude Code 官方的痛點）

### 1. Delta-based 累計值，解決官方「mid-session reset」

Claude Code 在 context compaction / auto-recovery 時會重置 `cost.total_cost_usd`、`total_duration_ms`。

**作法**：在 `/tmp/claude-cum-<sid>.json` 存 baseline，payload 掉下來時只重置 baseline，**累計值絕不倒退**。以 `session_id` 為 key，`--continue` / `--resume` 也能接續。

### 2. 跨 session quota 聚合，解決「全域 quota 只看到自己」

官方 quota 是全域的，但每個 session payload 只反映自己的觀察。

**作法**：每次 render 寫 snapshot 到 `~/.claude/rate-limit-snapshots.json`，挑 **最新 `resets_at`** 那組，取 `used_percentage` 的 MAX。所有 session 顯示同一個 %。

### 3. All-session cost/tokens 聚合

`cost $TOTAL ($SESSION this session)` 同步顯示 **全歷史總花費 + 當前 session 花費**。聚合所有 `claude-cum-*.json`。

### 4. 時間基礎的 quota 歸零

Claude Code 的 `rate_limits.*.resets_at` 會凍結在上次 API 回應的瞬間。若使用者閒置過了 reset 邊界，payload 仍顯示「87% used」。

**作法**：對比 `resets_at` 與真實時間，過期自動歸零 bar，倒數改算下一個 5h/7d 邊界。

### 5. `/resume` 自動重命名

Claude Code 的 transcript JSONL 支援 `{"type":"custom-title","customTitle":"..."}`。

**作法**：`summary-updater.js` 每次寫 summary 時把**前 40 字元** inject 為 custom-title。`/resume` 選單不再是一堆 UUID，而是有意義的標題。

### 6. Session Summary 帶壓縮規則

Summary 要反映**整個 session 的弧線**而非最後話題。

**作法**：summary-updater 的 prompt 強制 120 字元上限 + 明確壓縮規則（合併相關子議題、丟最不重要的舊項）。結果是新主題擠掉舊小事，而不是把最近的工作截斷。

### 7. 無 hooks 也能跑，但功能退化

不裝 hooks 一樣能用 —— 只是看不到 agents、edited files、message history、compact count、summary。**Quotas、cost、model、git、tokens、memory、MCP** 從官方 statusline JSON payload + 自動 spawn 的 MCP refresher 就能跑。

---

## `/cc-statusline:rows` Slash Command

不想看每一行？用隨插件附送的 slash command（儲存到 `~/.claude/cc-statusline-rows.json`）：

```
/cc-statusline:rows                      — 看目前設定
/cc-statusline:rows off                  — 主開關：完全隱藏 statusline
/cc-statusline:rows on                   — 主開關：重新啟用
/cc-statusline:rows hide agents edited   — 隱藏列出的 row
/cc-statusline:rows show agents          — 顯示列出的 row
/cc-statusline:rows only cost quota      — 只開這些，其他全關
/cc-statusline:rows toggle history       — 翻轉列出的 row
/cc-statusline:rows reset                — 全開
```

11 個 row key：`summary`、`dir`、`repo`、`model`、`cost`、`usage`、`quota`、`agents`、`memory_mcp`、`edited`、`history`。

**自動收合**：row 變空會自動合併寬度；整個 split block 隱藏時，水平線會融合上下區塊不冗贅。

---

## 目前限制

| 限制 | 原因 / 追蹤 Issue |
|------|------------------|
| 右邊界不完全對齊 | Claude Code 不傳 terminal width 給 statusline（[#22115](https://github.com/anthropics/claude-code/issues/22115)）；Windows 用 PowerShell fallback 偵測 |
| MCP 狀態與 `/mcp` UI 可能不一致 | `claude mcp list` 是 fresh probe；`/mcp` 是 session cache；兩者反映不同時間點 |
| 某些內建 bridge（如 `claude-in-chrome`）看不到 | `claude mcp list` 不曝露所有內建 bridge |
| statusline payload 無即時 MCP 狀態 | 官方 issue [#5511](https://github.com/anthropics/claude-code/issues/5511)，未來原生支援後就不需要 auto-refresher |

---

## 研究價值與啟示

### 關鍵洞察

1. **Statusline 是被低估的 Claude Code 擴充點**
   - 大多數 Claude Code plugin 聚焦在 slash command / skill / agent
   - Statusline 是「**每次渲染都會跑一次的長駐位置**」，最適合放監控型資料
   - 配合 `refreshInterval` 可以做到準即時（30 秒）儀表板

2. **Hook 即資料層**
   - cc-statusline 的架構是「hook 當 producer、statusline 當 consumer」
   - 6 個 hook 各寫不同的 cache 檔（subagent、message、file、compact、summary、mcp）
   - Statusline 從 cache 檔讀 → 渲染；**完全解耦、無 daemon、無 IPC**
   - 這是 Claude Code 官方 hook 系統的 **canonical 消費模式**

3. **作者補官方洞**
   - Delta-based 累計值 → 補官方「mid-session reset」
   - Cross-session quota 聚合 → 補官方「全域 quota 只看自己」
   - 時間基礎 quota 歸零 → 補官方「resets_at 凍結」
   - `/resume` 重命名 → 補官方「UUID 選單難用」
   - 這個 repo 某種程度是 **Claude Code issue tracker 的反向投影**

4. **Plugin marketplace 的可用案例**
   - 「一行 `claude plugin marketplace add`」代表 Claude Code 的 plugin 生態系真的能用了
   - cc-statusline 把 plugin、hook、slash command、statusline 四種 extension 點 **都用上**，是目前最完整的 reference implementation

5. **台灣貢獻者在全球 CC 生態系**
   - 作者 NYCU-Chung 來自陽明交大
   - 8 天拿 82 stars、純 JS 34KB 單檔 + 6 個 hook，工程密度高
   - 對照本站既有的其他台灣 Claude Code 專案（OpenClam、Kronos、tw-house-ops…）呈現局部群聚

### 與其他筆記的關聯

| 相關筆記 | 關聯點 |
|---------|-------|
| [Claude HUD](claude-hud.md) | 同類「把 Claude Code 內部狀態視覺化」工具，Claude HUD 是 TUI 獨立視窗、cc-statusline 是 inline 底部條 |
| [Claude Code Boris Cherny 57 Tips](claude-code-boris-cherny-tips.md) | Boris 的「多 session 並行」工作流特別需要跨 session quota 聚合 |
| [Boris Cherny × Opus 4.7 心得](boris-cherny-opus-4-7.md) | 4.7 引入 `xhigh` effort，cc-statusline 有 5 色 effort ladder 對應 |
| [Claude Agent SDK](claude-agent-sdk.md) | SubagentStart/Stop hook 是 SDK hook 系統的使用者層 |
| [Superpowers](superpowers.md) | hook + slash command + skill 組合應用的工程實作參考 |
| [Claude Skills Guide](claude-skills-guide.md) | `/cc-statusline:rows` 是 skill 類命令的設計範例 |
| [Analysis Claude Code](analysis-claude-code.md) | 分析 Claude Code 內部；cc-statusline 是建立在分析結果上的產品 |

### 可直接抄的 Pattern

```
1. Hook + cache file 解耦：
   - PreHook 寫 JSON 到已知路徑
   - Consumer（statusline / CLI tool）只讀，不 blocking

2. Delta 計算邏輯：
   baseline = 上次 payload 值
   如果 new_payload < baseline → 重置 baseline = new_payload（偵測到 reset）
   accumulated += max(0, new_payload - baseline)
   baseline = new_payload

3. 全域狀態聚合：
   - 每個 session 寫自己的 snapshot 到共用目錄
   - 讀取時 glob 所有 snapshot，取最新 timestamp 那組 + MAX 聚合

4. 讓 /resume 好看：
   往 transcript JSONL 寫 { type: "custom-title", customTitle: "..." }

5. Background refresher pattern：
   - Statusline 每次 render 都 spawn 一個 detached process
   - 那個 process 檢查 cache age，不新鮮才 probe
   - 不 block 當前 render
```
