---
date: "2026-06-11"
category: "AI 創作資源"
card_icon: "material-palette-swatch"
oneliner: "本地優先、開源的 Claude Design 替代品：原生桌面 app，不自帶 agent——用你 PATH 上既有的 Claude Code/Codex/Cursor 等 21 種 CLI 當設計引擎，讀 DESIGN.md 品牌契約串出網頁/簡報/圖/影片，支援 HTML/PDF/PPTX/MP4 匯出，Apache-2.0，兩週衝破 6 萬星"
tags:
  - design
  - desktop-app
  - claude-code
  - mcp
---

# Open Design 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | <https://github.com/nexu-io/open-design>（~63K stars，Apache-2.0，TypeScript） |
| 官網 / 下載 | <https://open-design.ai/> |
| 評測報導 | [XDA Developers](https://www.xda-developers.com/open-source-tools-do-what-claude-charges-for-and-some-do-it-better/)、[TechTimes](https://www.techtimes.com/articles/316749/20260517/open-design-free-local-alternative-claude-design-20-plan-runs-16-ai-agents.htm) |
| DESIGN.md 系統來源 | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) |
| 對標對象 | [Claude Design](https://x.com/claudeai/status/2045156267690213649)（Anthropic，2026/04） |

## 專案概述

**Open Design（OD）** 是 **Claude Design 的本地優先、開源替代品**。2026 年 4 月 Anthropic 推出 Claude Design——第一次讓 LLM 不再寫文章，而是直接交付「設計成品（design artifact）」——爆紅，但它**閉源、只付費、只雲端、鎖定 Anthropic 的模型/技能/介面**。Open Design 做了同樣的 loop（discover brief → lock direction → stream artifact → critique → deliver），但去掉所有 lock-in，兩週內衝破 4 萬星（現約 6.3 萬）。

它最關鍵的架構決策是：**不自帶 agent**。你 `PATH` 上已經有的 `claude` / `codex` / `cursor-agent` / `copilot` / `hermes` / `kimi`（共 21 種 CLI）就是設計引擎，一鍵切換；沒裝任何 CLI 也能用 BYOK proxy 接 OpenAI/Anthropic/Azure/Gemini/Ollama 等任意相容端點。OD 自己只提供**三種可組合的純檔案資產**：**plugins**（可執行工作流）、**skills**（agent 的設計品味）、**design systems**（品牌契約）。

產出形態極廣：網頁/桌面/行動原型、即時儀表板與 artifact、簡報 deck、圖像、影片，外加 **HyperFrames**（HeyGen 開源的 HTML→MP4 動態圖框架）。所有渲染都在沙箱 iframe 預覽、可原地編輯（不是「整個重生成」），可匯出 HTML/PDF/PPTX/MP4。資料全留在本機（SQLite + 檔案），無遙測、無雲端往返。

## 核心功能 / 技術架構

### 三平面可組合資產

| 平面 | 載體 | 數量 | 說明 |
|------|------|------|------|
| **Skills** | `skills/<name>/SKILL.md` | 100+ | 沿用 Claude Code `SKILL.md` 慣例，擴充 `od:` frontmatter（`mode`/`platform`/`scenario`/`fidelity` 等） |
| **Design Systems** | 單一 `DESIGN.md` | 150 | 9 段 schema（色彩/字體/間距/版面/元件/動效/語氣/品牌/反模式），含 Linear/Stripe/Vercel/Apple/Notion/Figma… |
| **Plugins** | 可執行工作流 | 261 | 瀏覽、安裝、散佈，按需擴充生成能力 |

### Artifact 模式（Studio 內同一設計系統串出多型態）

- **Prototype**：讀 `DESIGN.md` 的單頁 HTML，沙箱 iframe 即時預覽、可下載原始碼
- **Live Dashboard**：可編輯 KPI 牆，tweaks 面板調參數、iframe 免重載重渲染
- **Deck**：可翻頁簡報，匯出 PPTX/PDF（15 deck 模板 × 36 themes）
- **Image**：品牌級圖像（`gpt-image-2`/ImageRouter/自訂 API），93 個現成 prompt
- **HyperFrame**：HTML+CSS+GSAP → headless Chrome + FFmpeg 渲染成確定性 MP4

### Agent / 平台相容（核心賣點）

OD 以 **skills + CLI + MCP server** 三種形態被主流 coding agent 原生消費。裝好後 `od mcp install <agent>` 一行把 MCP server 接進該 agent 設定：

```bash
od mcp install claude   # 或 codex / cursor / copilot / gemini / opencode / openclaw …（21+）
```

MCP 讓**其他 repo 的 agent 直接讀你本地 OD 專案的活檔案**（CSS tokens、JSX 元件、entry HTML），按名稱查詢，永遠看到 live file 而非過時匯出。

```bash
od search-files "primary button"
od get-file design-systems/linear-app/DESIGN.md
od plugin run web-prototype --brief "..."
```

## 快速開始

| 方式 | 指令 | 適用 |
|------|------|------|
| **桌面 app（推薦，零設定）** | 下載 macOS/Windows（Linux AppImage 選配） | 自動偵測 PATH 上所有 CLI、載入 skills/系統 |
| **裝進 coding agent（無 UI）** | `curl -fsSL https://open-design.ai/install.sh \| sh -s claude` | 在 agent 內直接呼叫 OD skill/MCP |
| **Docker** | `docker compose up -d`（`deploy/`，須設 `OD_API_TOKEN`） | 自架 server，`localhost:7456` |
| **原始碼** | `corepack enable && pnpm install && pnpm tools-dev run web` | 開發（Node ~24、pnpm 10.33.x） |

完整 workflow：`brief → plugin → direction → design system → artifact → handoff → memory`。產出是真 HTML/CSS，可丟進 Cursor/Codex/Claude Code 繼續寫成 React/Next/Vue。

## 目前限制 / 注意事項

- **它不是「AI」也不是 agent**：OD 本身不含模型，**完全依賴你既有的 coding agent CLI 或 BYOK 端點**。沒有可用的 agent / API key，就只是個殼。實際生成品質取決於你接的模型。
- **`curl | sh` 安裝**：官方 install script 走 `curl -fsSL ... | sh`，採用前應自行審閱腳本內容（供應鏈風險）。
- **安全模型須留意**：daemon 預設綁 `127.0.0.1`、唯讀、proxy 邊界擋 SSRF；要 LAN 曝露需顯式設 `OD_BIND_HOST` + `OD_ALLOWED_ORIGINS`。自架公開時務必審查。
- **第三方資產授權各異**：HyperFrames 縮圖 © HeyGen、guizang-ppt 保留原授權、150 個 DESIGN.md 來自 VoltAgent 整理——商用前須逐一確認。
- **桌面/CLI 依賴環境**：Windows 有專門 troubleshooting 文件；Node/pnpm 版本要求嚴格。
- **行銷語極densely**：README 充斥數字與對標話術（「6 萬星」「21 CLIs」），閱讀時要區分「框架能力」與「依賴外部模型才成立的能力」。

## 研究價值與啟示

### 關鍵洞察

1. **「不自帶 agent」是這個專案最聰明的定位**：當對手（Claude Design、Lovable、v0）都把 agent 綁死在自家雲端，OD 反過來把「使用者 PATH 上已有的 CLI」當引擎。這把「模型競爭」徹底外部化——OD 不跟任何模型廠商競爭，反而**寄生在所有 coding agent 之上**，誰強就用誰。這是 agent 時代工具的一種範式：**做 orchestration 層，不做模型層**。

2. **`DESIGN.md` 作為「品牌契約」是把設計系統 agent 化的關鍵抽象**：把品牌（色彩/字體/動效/語氣/反模式）壓縮成一份 agent 可讀的 9 段 Markdown，使「品牌一致性」從人工 review 變成每次渲染都自動套用的契約。這與 [social-post](skill-social-post.md) 的 `style_profile.md`（語氣契約）異曲同工——**把隱性風格顯式化成 agent 可消費的檔案**，是 agent-native 工具的共同模式。

3. **三平面分離（skills/systems/plugins 皆純檔案）= 可版控、可散佈的生態**：把「設計品味、品牌、工作流」都做成 plain files，任何人可 author/version/publish。這跟 ai-avatar-bot 的「皮肉內容分離」是同一種思維的不同尺度——**把可變維度外部化成檔案，核心引擎才能保持通用**。

4. **MCP 取代「匯出再貼上」是 agent 協作的真實痛點解法**：每次迭代都匯出 zip 再重新 attach 會打斷心流。OD 用 MCP 把設計原始檔當成可查詢 API 暴露給任意 agent，讓 agent 永遠讀到 live file。這是 [MCP](mcp-for-beginners.md) 在「跨工具共享狀態」這個場景的高價值落地案例。

5. **它是「開源複製閉源爆款」速度的極端樣本**：Claude Design 4 月發布，OD 一個多月就做出對標品並衝 6 萬星。這反映 2026 年 agent 生態的一個現實——**只要核心 loop 想清楚，且能寄生在既有 agent CLI 上，開源複製的速度極快**。閉源產品的護城河不再是功能，而是模型與資料。

### 與其他專案的關聯

| 維度 | 對比 |
|------|------|
| vs Claude Design（對標對象） | 同 loop、同 artifact-first 心智模型；OD 開源、本地、模型無關、可自架，Claude Design 閉源雲端鎖定 |
| vs [Awesome Design Systems](awesome-design-systems.md) | OD 直接內建 150 個 `DESIGN.md` 系統並讓 agent 消費；後者是設計系統的彙整清單 |
| vs [社群行銷](topics/social-marketing.md) 類 skill（[social-post](skill-social-post.md)） | 都把「風格/品牌」顯式化成 agent 可讀檔案（`DESIGN.md` vs `style_profile.md`） |
| vs [SkillOpt](skillopt.md) | OD 用 100+ 手寫 skill；SkillOpt 是自動訓練 skill 的方法論——後者可視為前者 skill 生產的上游 |
| 定位 | 與多數「自帶雲端 agent」的設計工具相反，走 local-first + BYOK + 寄生既有 CLI 路線 |

**最大啟示**：Open Design 證明了 agent 時代一個有力的產品策略——**不做模型、不做 agent，只做「讓所有 agent 都能消費的可組合檔案資產 + orchestration 層」**。它把設計工作拆成 skills（品味）、design systems（品牌）、plugins（工作流）三份純檔案，再用 MCP 接上使用者既有的任意 coding agent。這個「寄生而非競爭」的定位，加上 local-first / BYOK 的隱私取捨，是它能在閉源爆款後快速複製並超車的根本原因。
