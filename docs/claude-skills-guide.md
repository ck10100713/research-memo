# The Complete Guide to Building Skills for Claude — 研究筆記

## 來源資訊

- **文件名稱**: The Complete Guide to Building Skills for Claude
- **來源**: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- **頁數**: 32 頁
- **發佈者**: Anthropic
- **發佈時間**: 約 2026 年 1 月（文件內提及 January 2026）

---

## 文件結構

| 章節 | 頁碼 | 主題 |
|------|------|------|
| Introduction | 3 | 導讀、目標讀者、兩條學習路徑 |
| Chapter 1: Fundamentals | 4–6 | Skill 定義、設計原則、MCP + Skills 整合 |
| Chapter 2: Planning and Design | 7–13 | 使用案例、技術規格、frontmatter、撰寫指引 |
| Chapter 3: Testing and Iteration | 14–17 | 測試策略、skill-creator 工具、迭代方法 |
| Chapter 4: Distribution and Sharing | 18–20 | 分發模式、API 使用、開放標準 |
| Chapter 5: Patterns and Troubleshooting | 21–27 | 五種設計模式、常見問題排除 |
| Chapter 6: Resources and References | 28–29 | 官方文件、工具、社群資源 |
| Reference A: Quick Checklist | 30 | 上傳前後檢查清單 |
| Reference B: YAML Frontmatter | 31 | frontmatter 完整欄位參考 |
| Reference C: Complete Skill Examples | 32 | 範例 skill 倉庫連結 |

---

## Chapter 1: Fundamentals（基礎知識）

### Skill 是什麼？

一個 **資料夾**，包含：
- `SKILL.md`（必要）：含 YAML frontmatter 的 Markdown 指令
- `scripts/`（選用）：可執行程式碼（Python、Bash 等）
- `references/`（選用）：需要時載入的文件
- `assets/`（選用）：模板、字型、圖示等

### 核心設計原則

#### Progressive Disclosure（漸進式揭露）

三層系統：
1. **YAML frontmatter**（第一層）：永遠載入系統提示中，讓 Claude 知道何時啟用
2. **SKILL.md 本文**（第二層）：Claude 判斷相關時才載入，含完整指令
3. **連結檔案**（第三層）：額外資源，Claude 按需存取

#### Composability（可組合性）
- Claude 可同時載入多個 skill
- Skill 應能與其他 skill 並行運作

#### Portability（可攜性）
- 在 Claude.ai、Claude Code、API 三個介面通用

### Skills + MCP（連接器）

**廚房比喻**：
- MCP = 專業廚房（工具、食材、設備的存取權）
- Skills = 食譜（如何創造有價值產出的步驟指引）

| | MCP（連接性） | Skills（知識） |
|--|---------------|----------------|
| 功能 | 連接 Claude 到你的服務 | 教 Claude 如何有效使用你的服務 |
| 提供 | 即時資料存取和工具調用 | 捕捉工作流程和最佳實踐 |
| 定位 | Claude **能做什麼** | Claude **該怎麼做** |

---

## Chapter 2: Planning and Design（規劃與設計）

### 三種常見使用案例類別

1. **Document & Asset Creation**（文件與素材建立）
   - 建立一致、高品質的輸出
   - 範例：frontend-design、docx、pptx、xlsx skills
   - 技巧：嵌入樣式指南、模板結構、品質檢查表

2. **Workflow Automation**（工作流自動化）
   - 多步驟流程的一致方法論
   - 範例：skill-creator skill
   - 技巧：步驟驗證門、模板、迭代改善循環

3. **MCP Enhancement**（MCP 增強）
   - 為 MCP 提供工作流程指引
   - 範例：sentry-code-review skill
   - 技巧：協調多個 MCP 呼叫、嵌入領域專業知識、錯誤處理

### 成功指標

**量化指標**：
- Skill 在 90% 相關查詢中觸發
- 在 X 次工具呼叫內完成工作流
- 每次工作流 0 個失敗 API 呼叫

**質性指標**：
- 使用者不需提示 Claude 下一步
- 工作流程無需使用者修正即可完成
- 跨 session 結果一致

### 技術規格

#### 檔案結構
```
your-skill-name/
├── SKILL.md          # 必要
├── scripts/          # 選用
├── references/       # 選用
└── assets/           # 選用
```

#### YAML Frontmatter（最重要的部分）

**必要欄位**：
- `name`：kebab-case，無空格或大寫
- `description`：必須包含「做什麼」+「何時使用」，< 1024 字元，不可含 XML 標籤

**選用欄位**：
- `license`：MIT、Apache-2.0 等
- `compatibility`：1-500 字元，環境需求
- `metadata`：自訂 key-value（建議：author、version、mcp-server）
- `allowed-tools`：限制工具存取

**安全限制**：
- frontmatter 禁止 XML 角括號（`<` `>`）
- 名稱不可含 "claude" 或 "anthropic"（保留字）

#### 好的 description 範例
```yaml
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".
```

#### 壞的 description 範例
```yaml
# 太模糊
description: Helps with projects.
# 缺少觸發條件
description: Creates sophisticated multi-page documentation systems.
```

### 撰寫主指令的最佳實踐

- **具體且可操作**：明確指出要執行什麼命令、檢查什麼條件
- **清楚引用資源**：`references/api-patterns.md` 而非模糊描述
- **使用漸進式揭露**：SKILL.md 聚焦核心指令，詳細文件放 `references/`
- **包含錯誤處理**：常見錯誤和解決方案
- **SKILL.md 內不放 README.md**

---

## Chapter 3: Testing and Iteration（測試與迭代）

### 三種測試方式
1. **手動測試**（Claude.ai）：直接執行查詢觀察行為
2. **腳本測試**（Claude Code）：自動化測試案例
3. **程式化測試**（Skills API）：系統性評估套件

### 建議測試方法

#### 1. Triggering Tests（觸發測試）
- ✅ 明確任務觸發
- ✅ 改述請求觸發
- ❌ 不相關主題不觸發

#### 2. Functional Tests（功能測試）
- 驗證正確輸出
- API 呼叫成功
- 錯誤處理正常
- 邊界案例覆蓋

#### 3. Performance Comparison（效能比較）
- 與無 skill 基線比較
- 量化：訊息數、token 消耗、API 失敗次數

### skill-creator 工具
- 內建於 Claude.ai，可下載至 Claude Code
- 功能：從自然語言描述生成 skill、審查 skill、建議改善
- 使用方式：`"Use the skill-creator skill to help me build a skill for [your use case]"`
- 15-30 分鐘可建好第一個 skill

### 迭代策略
- **Undertriggering**：增加 description 細節和關鍵詞
- **Overtriggering**：加入負面觸發條件、更具體化
- **執行問題**：改善指令、增加錯誤處理

---

## Chapter 4: Distribution and Sharing（分發與共享）

### 目前分發模式（2026 年 1 月）

**個人使用者**：
1. 下載 skill 資料夾
2. 壓縮為 zip
3. 上傳至 Claude.ai > Settings > Capabilities > Skills
4. 或放入 Claude Code skills 目錄

**組織層級**：
- 管理員可部署全工作區的 skills（2025/12/18 上線）
- 自動更新、集中管理

### Skills API

- `/v1/skills` 端點管理 skills
- `container.skills` 參數加入 Messages API 請求
- 與 Claude Agent SDK 整合
- 需要 Code Execution Tool beta

### 開放標準
- Agent Skills 已發佈為開放標準（類似 MCP）
- 跨平台可攜性

### 推薦做法
1. 在 GitHub 上 host（公開 repo + README + 截圖）
2. 在 MCP 文件中連結 skill
3. 建立安裝指南

---

## Chapter 5: Patterns and Troubleshooting（模式與故障排除）

### 五種設計模式

#### Pattern 1: Sequential Workflow Orchestration（循序工作流編排）
- **適用**：多步驟流程需特定順序
- **技巧**：明確步驟排序、步驟間依賴、每階段驗證、失敗回滾

#### Pattern 2: Multi-MCP Coordination（多 MCP 協調）
- **適用**：工作流跨越多個服務
- **範例**：設計到開發交接（Figma → Drive → Linear → Slack）
- **技巧**：清楚的階段分隔、MCP 間資料傳遞、跨階段驗證

#### Pattern 3: Iterative Refinement（迭代精煉）
- **適用**：輸出品質可透過迭代改善
- **範例**：報告生成（初稿 → 品質檢查 → 精煉循環 → 定稿）
- **技巧**：明確品質標準、驗證腳本、知道何時停止

#### Pattern 4: Context-Aware Tool Selection（上下文感知工具選擇）
- **適用**：同一結果但根據情境選不同工具
- **範例**：檔案儲存（依檔案類型/大小選不同 MCP）
- **技巧**：清楚的決策標準、備選方案、選擇透明度

#### Pattern 5: Domain-Specific Intelligence（領域專業知識）
- **適用**：需超越工具存取的專業知識
- **範例**：金融合規性付款處理
- **技巧**：領域專業嵌入邏輯、行動前合規檢查、完整文件記錄

### 常見問題排除

| 問題 | 原因 | 解決方案 |
|------|------|----------|
| Skill 上傳失敗 | 檔案未命名為 SKILL.md | 重新命名（大小寫敏感） |
| frontmatter 無效 | YAML 格式問題 | 檢查 `---` 分隔符、引號 |
| Skill 名稱無效 | 名稱含空格或大寫 | 改用 kebab-case |
| Skill 不觸發 | description 太模糊 | 加入具體觸發短語 |
| Skill 過度觸發 | 範圍太廣 | 加入負面觸發、更具體化 |
| 指令未遵循 | 指令太冗長/埋太深/語意模糊 | 精簡指令、重要內容置頂、用明確語言 |
| MCP 連接問題 | 伺服器未連接/認證失敗 | 檢查連接狀態、API key、工具名稱 |
| 上下文過大 | Skill 內容太大 | SKILL.md < 5000 字、用 references/、同時啟用 < 20-50 skills |

### 進階技巧
- 關鍵驗證考慮用腳本（確定性）而非語言指令
- 對抗模型「懶惰」：加入鼓勵語句（「Take your time」「Quality is more important than speed」）
  - 注意：這在使用者提示中比 SKILL.md 中更有效

---

## Reference A: Quick Checklist（快速檢查清單）

### 開始前
- [ ] 識別 2-3 個具體使用案例
- [ ] 確認工具（內建或 MCP）
- [ ] 瀏覽本指南和範例 skills
- [ ] 規劃資料夾結構

### 開發中
- [ ] 資料夾 kebab-case 命名
- [ ] SKILL.md 存在（大小寫正確）
- [ ] YAML frontmatter 有 `---` 分隔符
- [ ] name 欄位：kebab-case
- [ ] description 包含 WHAT 和 WHEN
- [ ] 無 XML 標籤
- [ ] 指令清晰可操作
- [ ] 包含錯誤處理
- [ ] 提供範例
- [ ] 參考資料正確連結

### 上傳前
- [ ] 測試明確任務觸發
- [ ] 測試改述請求觸發
- [ ] 驗證不相關主題不觸發
- [ ] 功能測試通過
- [ ] 工具整合正常
- [ ] 壓縮為 .zip

### 上傳後
- [ ] 在真實對話中測試
- [ ] 監控 under/over-triggering
- [ ] 收集使用者回饋
- [ ] 迭代 description 和指令
- [ ] 更新 metadata 版本

---

## Reference B: YAML Frontmatter（完整欄位）

```yaml
---
name: skill-name                    # 必要，kebab-case
description: [做什麼 + 何時使用]     # 必要，< 1024 字元
license: MIT                         # 選用
allowed-tools: "Bash(python:*) WebFetch"  # 選用，限制工具
compatibility: [環境需求]            # 選用，< 500 字元
metadata:                            # 選用
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
---
```

**允許**：標準 YAML 型別（字串、數字、布林、列表、物件）、長 description（最多 1024 字元）、自訂 metadata 欄位

**禁止**：XML 角括號（`<` `>`）、YAML 中的程式碼執行、"claude"/"anthropic" 前綴的 skill 名稱

---

## Reference C: 範例 Skills 倉庫

- **Document Skills**：PDF、DOCX、PPTX、XLSX 建立
- **Example Skills**：各種工作流模式
- **Partner Skills Directory**：Asana、Atlassian、Canva、Figma、Sentry、Zapier 等合作夥伴 skills
- **GitHub 倉庫**：`anthropics/skills`

---

## 關鍵洞察摘要

1. **Skill = 資料夾 + SKILL.md**：結構極為簡單，但 frontmatter 的 description 是最關鍵的部分
2. **Progressive Disclosure 是核心設計**：三層系統最小化 token 使用量
3. **MCP + Skills = 完整方案**：MCP 提供工具存取，Skills 提供工作流程知識
4. **description 決定一切**：觸發、不觸發、過度觸發都取決於 description 的品質
5. **測試三部曲**：觸發測試 → 功能測試 → 效能比較
6. **五種模式覆蓋大多數場景**：循序工作流、多 MCP 協調、迭代精煉、上下文感知選擇、領域專業知識
7. **Skills 是開放標準**：像 MCP 一樣跨平台可攜
8. **用腳本取代語言指令做驗證**：程式碼是確定性的，語言解讀不是
