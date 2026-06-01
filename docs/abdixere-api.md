---
date: "2026-05-13"
category: "Coding Agent 工具"
card_icon: "material-memory"
oneliner: "Saki-tw 的極簡 MCP API base，主張 Agent context memory 應該在工具層下放給 Agent 自己，不要靠多餘保護"
tags:
  - mcp
  - memory
---

# abdixere-api 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/Saki-tw/abdixere-api> |
| 作者 | <https://github.com/Saki-tw> (Saki-Chan) |
| 內附架構文件 | `202605080625_SakiMCPDeus_ARCHITECTURE.md` |
| 內附 prompt | `prompt.preskill`（Skill self-fix 偽碼） |
| 相關前作 | `SakiMCPforDeusExAgentX64`（Rust MCP server，~305 行） |

## 專案概述

**abdixere-api** 是 Saki-tw 在 2026-05-10 公開的一個 Rust workspace（`abdixere-core` + `abdixere-cli`，目前以 zip 形式收錄），定位是「給 Agent 用的 base API，讓任何 Agent interface 失效時都能重建」。倉庫描述用了極為挑釁的語氣，核心訊息是：許多人問「Agent 怎麼記住 context」，作者覺得這問題不該再問，乾脆丟一個 API 出來終結這類「無用思考」。

從附帶的架構文件可以看出，abdixere-api 屬於 `SakiMCPDeus` 系列的延伸——一個刻意精簡的 MCP server，原版 SakiMCP 有 2,868 行、11 個工具、含路徑限制與 Session Guard，而 Deus 版只剩約 305 行、6 個工具，**故意拿掉所有保護機制**。本研究是 May 13 2026 抓到 repo 仍處於早期狀態的快照（0 star、無 release、core/cli 仍以 zip 形式存在）。

整體上這是一個「概念宣言型 repo」：程式碼份量小，但設計理念明確——把 Agent context memory 的責任從工具層往上推回到 Agent 自身的 System Prompt 與 skill 機制。

## 核心架構（依附帶文件還原）

```text
LLM Agent
  │  MCP stdio JSON-RPC
  ▼
SakiMCPDeus (Rust, rmcp 0.14)
  ├── run_command   → cmd /c 或 sh -c, timeout 60s/上限 300s, 輸出截斷 100KB
  ├── read_file     → tokio::fs::read + magic bytes 判 binary
  ├── write_file    → 自動建立父目錄 + tokio::fs::write
  ├── list_files    → 委派 fd --type f
  ├── search_files  → 委派 rg --json
  └── search_filename → 委派 fd pattern
```

| 維度 | SakiMCP（原） | abdixere-api / SakiMCPDeus |
|------|---------------|---------------------------|
| 代碼量 | 2,868 行 | ~305 行 |
| 工具數 | 11 | 6 |
| 路徑限制 | 有 | **無** |
| Session Guard | 有（強制先 read 再 write） | **無** |
| Context Manager | 有 | **無** |
| 遠端 MCP / Web Search | 有 | **無** |
| 安全模式 | `SAKIMCP_READ_ONLY` | **無** |
| 依賴 crate | ~12 | ~8 |

## 設計理念（作者論述摘要）

- **為什麼拿掉路徑限制**：Agent 本身已經透過 System Prompt 擁有完整系統存取權限，再多一層攔截只會逼 Agent 多寫 error recovery、多吃 token。
- **為什麼拿掉 Session Guard**：先 read 再 write 的安全性應由 Agent System Prompt 保障，MCP server 不該重複檢查。
- **為什麼提高 timeout / 輸出上限**：Agent 真實會跑 `cargo build`、`hugo` 等長命令，60s/300s + stdout 100KB 比 30s/120s 更貼近實況。
- **`prompt.preskill` 暗示**：作者把 skill 本身視為可被 self-fix 的單元，`No Skill_Fail → Parse skill.md + Axiom → IF context-independent logic error THEN Modify Core ELSE Supplement missing cases`，把「skill 演化」的優先順序明寫成偽碼。

## 倉庫結構

| 路徑 | 內容 |
|------|------|
| `abdixere-core.zip` | 13 KB，推測為 Rust core crate |
| `abdixere-cli.zip` | 21 KB，推測為 CLI |
| `Cargo.toml` | workspace 定義（members = core, cli, resolver = 2） |
| `Cargo.lock` | 已 commit，53 KB |
| `SakiMCPforDeusExAgentX64/` | 空目錄（佔位） |
| `Win64_Antigravity/` | 空目錄（佔位，疑似為 Google DeepMind Antigravity 環境保留） |
| `Skill-level_AgentContext&ConversationDump.zip` | 172 KB，內附 skill 與 conversation dump 樣本 |
| `20260225_GeminiCLI_Conversation_Dump.md` | 僅 72 bytes，內容為 parser error log |
| `prompt.preskill` | Skill self-fix 偽碼宣言 |
| `LICENSE` | Other / NOASSERTION |

語言欄位 GitHub 顯示為 `PowerShell`，但 `Cargo.toml` 表明這實質上是 Rust workspace，PowerShell 推測來自 build script 或 zip 內容檢測誤判。

## 目前限制與注意事項

- **核心仍是 zip**：`abdixere-core` / `abdixere-cli` 沒有展開原始碼，無法用 GitHub UI 直接審視；要研讀必須先下載 unzip。
- **License = NOASSERTION**：附 LICENSE 檔但 GitHub 無法解析成已知授權，使用前必須讀 LICENSE 全文確認商用條件。
- **0 star / 0 fork / 0 issue**：完全是個人實驗 repo，沒有社群驗證。
- **故意移除所有保護**：在多 Agent / 共用環境下直接套用會有風險，預設場景是「Agent 自己對自己負責」。
- **強烈個人語氣的 README**：對協作和外部引用造成阻力，這個 repo 更像理念宣告，不是工具發布。

## 研究價值與啟示

### 關鍵洞察

1. **「Agent 記憶 context」這個問題不一定要在工具層解決**：abdixere-api 的核心論點是把 memory 的責任推回 Agent + Skill 系統，工具層只需提供乾淨的 read/write/run/search。這跟 [[context-hub]]、[[claude-code-sdk]] 中把 context 集中化管理的思路是反向選擇。
2. **MCP server 的最小可行集合可能比想像更小**：6 個工具（run_command / read_file / write_file / list_files / search_files / search_filename）涵蓋了多數 coding agent 的 90% 行為，剩下的 Web search、context manager、session guard 都是 nice-to-have，能拆解到 Agent 層處理。
3. **「安全檢查重複層」是被低估的成本**：原版 2,868 行裡有大量篇幅在做路徑限制、READ_ONLY 切換、Session Guard，而這些行為 Agent System Prompt 本身就會約束。如果把 prompt 視為可信契約，工具層的二次檢查反而拖累效率與 token。
4. **Skill self-fix 偽碼是個有趣的副產物**：`prompt.preskill` 三行虛擬碼把「skill 評估失敗 → 判斷是 logic error 改核心、還是 case 不足補例外」寫成決策樹，這個結構可以直接拿來設計 skill review pipeline。
5. **Rust + rmcp 的最小 MCP server 樣板**：~305 行用 rmcp 0.14 + tokio + serde + schemars 就能交付 production-ready 工具集，是非常好的 Rust MCP 入門參考——尤其相對於多數 Python MCP server 動輒上千行。

### 與其他研究的關聯

- 與 [[andrej-karpathy-skills]]、[[claude-skills-guide]]、[[asgard-skills]]：abdixere-api 主張 context memory 應該交還給 Skill 系統管理，與 skill-centric 工具鏈天然耦合，反過來變成 skill 系統的「下層 API 基底」。
- 與 [[mcp-cli]]、[[mcporter]]、[[harness-design-long-running-apps]]：這些研究在處理 MCP server 的安全模式 / 連線管理時，多走向「加層保護」；abdixere 走的是反向，提供另一個極端的比較對照。
- 與 [[gstack]] 的 `careful` / `freeze` 路線完全相反：gstack 預設加上 destructive-action guard，abdixere 預設取消所有 guard。把兩者放一起，正好是「Agent 工具層該做多少 safety」這條光譜的兩端。
- 對於 Fluffy Agent Core 這類 multi-tenant agent 平台**不適用**：abdixere 預設 Agent = 工具擁有者，多租戶場景下仍需要 SakiMCP 原版或更嚴格的方案。
