---
date: "2026-05-19"
category: "開發工具"
card_icon: "material-console-line"
oneliner: "HKUDS 把任何 GUI 軟體用 7 步驟 pipeline 自動產出 agent-friendly CLI harness，60+ 軟體覆蓋，CLI-Hub 一鍵安裝，36k stars / 2 個月"
tags:
  - harness
  - automation
---

# CLI-Anything 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/HKUDS/CLI-Anything> |
| 官方網站 / CLI Hub | <https://clianything.cc/>、<https://hkuds.github.io/CLI-Anything/> |
| Trendshift | <https://trendshift.io/repositories/22991> |
| 規模 | 36,720 stars / 3,560 forks / Apache 2.0 / 創建 2026-03-08（**2 個月衝到 36k+ stars**） |
| 語言 | Python ≥ 3.10 + Click ≥ 8.0 |
| 上游組織 | HKUDS（同 [[rag-anything]]、LightRAG） |
| 中文 / 日文 README | README_CN.md / README_JA.md |
| 測試規模 | 2,269 passing tests / 18 個 demo apps |

## 概述

**CLI-Anything** 是港大 HKUDS（也是 LightRAG / [[rag-anything]] 的同一個 lab）2026-03 推出的工具，slogan 直白：

> *"Today's Software Serves Humans. Tomorrow's Users will be Agents. CLI-Anything: Bridging the Gap Between AI Agents and the World's Software."*

它在解的問題：**多數軟體（GIMP、Blender、LibreOffice、Obsidian、Audacity ...）沒有 agent-friendly 的介面**。Agent 看不懂 GUI、不能點滑鼠，所以一堆生產級軟體被擋在 agent 工作流外面。CLI-Anything 的解法是——**用一個 7 階段 pipeline，自動把任何軟體變成 agent-native CLI**：

```text
/cli-anything ./gimp
  ↓
🔍 Analyze    掃描原始碼、把 GUI 動作對應到 API
📐 Design     架構 command groups / state model / 輸出格式
🔨 Implement  用 Click 寫出 CLI + REPL + JSON output + undo/redo
📋 Plan Tests 產出 TEST.md（unit + E2E plan）
🧪 Write Tests 把測試實作出來
📝 Document   把測試結果寫回 TEST.md
📦 Publish    生成 setup.py + 裝進 PATH
```

→ **agent 不再需要為每個軟體手刻 wrapper**。Pipeline 跑完一次就有完整 CLI、SKILL.md、測試、setup.py。

## 為什麼是 CLI 而不是 MCP？

README 直接陳述設計哲學：

| CLI 優勢 | 為什麼 agent 友善 |
|---------|------------------|
| **Structured & Composable** | 文字指令對 LLM 友善、可串接（pipe / xargs / scripts） |
| **Lightweight & Universal** | 不需要 daemon、不需要 transport 層、無相依 |
| **Self-Describing** | `--help` 自帶說明，agent 一秒上手 |
| **Proven Success** | Claude Code 每天靠 CLI 跑成千上萬個 workflow |
| **JSON output** | 機器讀直接 parse |
| **Deterministic** | 結果可重現，agent 行為可預期 |

→ **隱含主張**：CLI 是比 MCP server 更輕量、更通用的 agent 介面。MCP 要起 server、要連 stdio/HTTP、要管 lifecycle；CLI 是「shell 直接呼叫」。**對開發者門檻低很多**。

→ 對照 [[rag-anything]] 的 MCP-server 路線、[[linebot-multimodal-rag]] 的 Gemini File Search 路線，CLI-Anything 走的是**第三條路**——「**讓 agent 直接呼叫 shell 工具**」。

## 60+ 已支援軟體（依領域分類）

從 repo 根目錄掃出來的子目錄，每個都是一個獨立 CLI harness：

| 領域 | 軟體 |
|------|------|
| **3D / CAD** | Blender、FreeCAD、CloudCompare |
| **2D / 影像 / 繪圖** | GIMP、Krita、Inkscape、Sketch |
| **影音 / 直播** | Audacity、Kdenlive、Shotcut、OBS Studio、Openscreen、VideoCaptioner |
| **GIS / 地圖** | QGIS |
| **辦公 / 文件** | LibreOffice、Mubu、draw.io、Mermaid |
| **筆記 / 知識管理** | Obsidian、Zotero、NotebookLM |
| **遊戲引擎 / 遊戲** | Godot、Sbox、Slay the Spire II |
| **音樂** | MuseScore |
| **工作流自動化** | n8n、Dify、ComfyUI |
| **瀏覽器 / Web** | Safari、Browser、Openscreen |
| **開發工具** | iTerm2、LLDB、PM2、WireMock、Mailchimp、Anygen |
| **GPU / Rendering** | RenderDoc、Nsight Graphics、Unreal Insights、NSLogger |
| **網路 / 雲端** | CloudAnalyzer、AdGuardHome、RMS、SeaClip |
| **金融 / Web3** | Firefly-iii、eth2-quickstart |
| **AI / ML** | Ollama、ChromaDB、Novita、UniMol Tools |
| **協作 / 通訊** | Zoom |
| **OSINT** | IntelWatch |
| **CLI-Hub 自身** | cli-hub、cli-hub-meta-skill、anygen、macrocli、skill_generation |

→ **覆蓋面驚人**：從 Blender / GIMP / FreeCAD 這種重 GUI 創作工具，到 LLDB / GPU profiler 這種開發者深度工具，到 Zoom / Mailchimp 這種協作 SaaS，再到 Slay the Spire II 這種遊戲 agent 介面，全部用同一個 pipeline 自動產。

## CLI-Hub：「npm for agent CLIs」

CLI-Hub 是 CLI-Anything 的 **package manager + registry**：

```bash
pip install cli-anything-hub             # 裝 hub package manager
cli-hub install <name>                   # 安裝任一 CLI
```

或 npm 風格：

```bash
npx skills add HKUDS/CLI-Anything --skill <skill-name> -g -y
```

特性：

- **`public_registry.json`** 列出所有公開 CLI（含 pip / npm / brew / 系統工具多 install 源）
- **PyPI auto-publish workflow**：每個 merge 自動發版
- **Live end-to-end checks**：CI 真實跑 install / update / uninstall 驗證
- **公開貢獻流程**：開 PR → review merge → **Hub 立即更新**
- **可上自家 repo**：CLI 可以放在自己 repo 下，CLI-Hub 用 `skill_md` URL 引用即可（[[zotero]] CLI 就是這樣）

## 與多 AI Coding Agent 平台整合

不只 Claude Code——CLI-Anything 對下列**七個** agent 平台都有 first-class 支援：

| 平台 | 安裝路徑 |
|------|---------|
| **Claude Code** | `/plugin marketplace add HKUDS/CLI-Anything` → `/plugin install cli-anything` |
| **Pi Coding Agent** | `.pi-extension/cli-anything/install.sh`（全域裝進 `~/.pi/agent/extensions/`） |
| **OpenClaw** | 內建支援（2026-03-15 merged） |
| **OpenCode** | `opencode-commands/` |
| **Codex** | `codex-skill/`（2026-03-12 merged） |
| **Qodercli** | `qoder-plugin/`（2026-03-13 merged） |
| **GitHub Copilot CLI** | 透過 skill 機制 |

→ **一份 CLI harness、七個平台共用**——這是 CLI 作為 agent 介面的最大優勢，跨平台零改動。

## 工作流範例：把 GIMP 變成 agent-native

```bash
# 1. 裝 plugin
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# 2. 一個指令搞定（跑 7 階段）
/cli-anything ./gimp

# 3. 結果：你現在有完整 GIMP CLI
gimp-cli image open ./photo.jpg
gimp-cli filter gaussian-blur --radius 5
gimp-cli image save ./output.png

# 4. （選用）增量擴充覆蓋
/cli-anything:refine ./gimp "I want more CLIs on batch processing and filters"
```

`:refine` 子指令做 **gap analysis**——比對軟體完整功能跟目前 CLI 覆蓋度，**增量補上缺失**，可跑很多次、非破壞性。

## HARNESS.md 與 SKILL.md 雙層架構

CLI-Anything 對每個 CLI 維護兩份 markdown：

| 檔案 | 給誰看 | 內容 |
|------|--------|------|
| `HARNESS.md` | **開發者** | 該 CLI 的設計決策、phase 進度、實作細節 |
| `SKILL.md` | **AI agent** | 該 CLI 的功能總覽、命令、何時用、JSON schema |

→ 對照 [[mattpocock-skills]] 的 **CLAUDE.md（meta-rules）+ CONTEXT.md（domain language）** 雙層拆分，CLI-Anything 對應的是 **HARNESS.md（工程紀錄）+ SKILL.md（agent 介面）**——**「給人看的」與「給 agent 看的」嚴格分離**，已成為 2026 Skill 生態系的共識結構。

2026-04-18 還做了一次「**所有 SKILL.md 統一到頂層 `skills/` 目錄**」的大整併，每個 CLI 從一個 canonical source 安裝。

## 目前限制與注意事項

- **強相依目標軟體已安裝**：CLI 只是 wrapper，**底層仍要本機有 GIMP / Blender / FreeCAD** 等。不是「替代品」，是「自動化介面」。
- **Windows 體驗較差**：Claude Code 在 Windows 跑 shell 需要 Git for Windows 或 WSL 才能用 `bash` / `cygpath`。
- **品質依賴 generation pipeline**：自動產的 CLI 可能漏掉部份功能、抽象不完美，**需要 `/cli-anything:refine` 多輪修補**。
- **沒在演 agent 行為**：CLI-Anything 只提供「工具表面」，**agent 要怎麼用、是否會用對、是 agent / Skill 端的責任**——這個 repo 不做 agent decision logic。
- **每個 CLI 各自的安全模型不同**：GIMP CLI 給檔案系統存取、Browser CLI 給網路、Zoom CLI 給日曆/會議——權限模型分散，**production 用要逐一審查**（GIMP Script-Fu path injection 就在 2026-03-14 被修過）。
- **CLI 還在快速演進**：2026-04 一個月就 merge 了 QGIS / UniMol / Safari / Obsidian / Eth2 / Zotero / n8n / Exa / Godot / WireMock / Slay the Spire II / VideoCaptioner 等 12+ CLI，**API 仍會頻繁變動**。

## 研究價值與啟示

### 關鍵洞察

1. **「CLI 是 agent 的最佳介面」是 2026 浮現的共識**：對比 MCP server 路線需要 daemon、傳輸層、生命週期管理，CLI 是「shell 呼叫 + `--help` 描述 + JSON 輸出」三件套，**對所有平台都通用、設計成本最低**。CLI-Anything 用 36k stars 在 2 個月內證明這個論點被市場接受。
2. **「Software Agent-Native」是個被低估的市場機會**：絕大多數 GUI 軟體（GIMP、Blender、Audacity、Zoom）沒有 agent 介面、API 文件對 LLM 不友善。**把這些軟體變 agent-native 是「最後一哩路」**——大廠不會做（投入產出比低），但開源社群可以靠自動化 pipeline 用半人工方式蓋完。
3. **「7 階段 pipeline + Skill 化」是現代 codegen 工作流範本**：Analyze → Design → Implement → Plan Tests → Write Tests → Document → Publish，每階段獨立、有測試門檻、有產出物。**這個結構可以直接抄去做任何 codegen 場景**（不只 CLI）。
4. **`/cli-anything:refine` 的 gap analysis 思路值得學**：不是一次寫完，而是「初版 → 跑 → 比對 spec → 補缺 → 再跑」的 incremental loop。這跟 [[mattpocock-skills]] 的 `/improve-codebase-architecture`（每幾天跑一次反熵）、[[zeuikli-claude-code-best-practices]] 的「Skill 保留門檻 30 天評估」是同一條哲學光譜——**agent 工作流要設計成可被反覆 refine 的，不是一次完成的**。
5. **HARNESS.md / SKILL.md 雙層架構是 Skill 生態系的浮現共識**：對應 [[mattpocock-skills]] 的 CLAUDE.md + CONTEXT.md。**「給人 / 給 agent」的文件嚴格分離**正在成為 best practice。
6. **HKUDS 的「Anything」系列形成完整生態圈**：LightRAG → [[rag-anything]] → CLI-Anything，三個 repo 在 2 年內合計 70k+ stars，**HKUDS 已成為東亞最有產出的 LLM infra lab 之一**。CLI-Anything + RAG-Anything 一起用，等於「**agent 能查資料 + agent 能用任何軟體**」兩塊基石都有開源解。
7. **CLI-Hub 是「應用商店化」的 agent skills 嘗試**：對標 npm / PyPI，**為 agent skill 建立「可被搜尋、可被一鍵安裝、可被自動更新」的市集**。這個方向若成功，會深刻改變 agent 開發體驗——你想做某個任務，先到 CLI-Hub 看有沒有人做過。

### 與其他研究的關聯

- 與 [[rag-anything]]：**HKUDS 同個 lab 的姊妹專案**，rag-anything 解「agent 能查資料」、cli-anything 解「agent 能用工具」。兩者搭起來是完整 agent infra。
- 與 [[mattpocock-skills]]、[[casper-claude-skill-design-gallery]]：**Skill 生態系的三條主軸**——Matt 走 workflow（grilling / tdd）、Casper 走 design（25 風格圖鑑）、CLI-Anything 走 tool-wrapping（60+ 軟體）。三者構成 Skill 應用的完整光譜。
- 與 [[abdixere-api]]：abdixere-api 主張「Agent 工具層要乾淨小巧、context memory 給 Skill」，CLI-Anything 是這個哲學的具體實踐——**每個軟體一個 CLI，每個 CLI 一個 SKILL.md，工具層各自獨立**。
- 與 [[zeuikli-claude-code-best-practices]] 第 6 章 MCP 整合：zeuikli 報告把 MCP / Skills / Subagents / Hooks 做職責分離，CLI-Anything 是「**用 CLI 取代 MCP server 作為工具層**」的另一條路線。對比兩者可以判斷你自己專案該選哪邊。
- 與 [[mcp-for-beginners]]、[[ai-agents-for-beginners]]：Microsoft 教材重 MCP，CLI-Anything 是輕量替代路線。對學習者來說兩個一起讀能看清「工具層該抽象到哪一層」的取捨。
- 與 AWS LangGraph + Strands agent sample（討論中未寫成筆記）：那個專案的 MCP server 也是 subprocess，**跟 CLI-Anything 哲學相通**——「工具是 process，不是 import」。
- 對 retail quant 應用：可以用 CLI-Anything pipeline 把 TWSE / Yahoo Finance / TEJ 等台股資料源包成 agent-native CLI，讓 Claude / Codex 直接用。
