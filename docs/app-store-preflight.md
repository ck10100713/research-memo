# App Store Preflight Skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | [truongduy2611/app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills) |
| 作者推文 | [Duy Nguyen @truongduy2611](https://x.com/truongduy2611/status/2034515540279267506) |
| 相關專案 — asc CLI | [rudrankriyam/App-Store-Connect-CLI](https://github.com/rudrankriyam/App-Store-Connect-CLI) |
| 相關專案 — ASC CLI Skills | [rudrankriyam/app-store-connect-cli-skills](https://github.com/rudrankriyam/app-store-connect-cli-skills) |
| 競品 — Greenlight | [RevylAI/greenlight](https://github.com/RevylAI/greenlight) |
| Stars | ~819 |
| 授權 | MIT |
| 建立時間 | 2026-03-19（非常新） |

## 專案概述

App Store Preflight 是一個 **Claude Code Skill**，在提交 iOS/macOS 應用至 App Store 之前，自動掃描 Xcode 專案、原始碼、metadata 和設定檔，找出可能導致 Apple 審核拒絕的常見問題。

這不是一個獨立的 CLI 工具，而是一組**給 AI Agent 讀取的結構化規則文件**。透過 Claude Code 的 skill 機制，AI Agent 能載入這些規則、對比你的專案，產出報告並嘗試自動修復。

### 核心價值

- 覆蓋 **100+ Apple Review Guidelines**
- 按 **10 種 App 類型** 提供專屬 checklist
- 整合 `asc` CLI 拉取 App Store Connect metadata
- 掃描結果含嚴重度、影響檔案、修復步驟
- 支援自動修復 + 重新驗證

## 技術架構

### 運作流程

```
Step 1: 識別 App 類型
        │
        ▼
Step 2: asc metadata pull（拉取 App Store metadata）
        │
        ▼
Step 3: 載入 references/rules/ 下的規則
        │  比對 Xcode 專案、原始碼、metadata
        ▼
Step 4: 產出 Preflight Report
        │  ❌ Rejections → ⚠️ Warnings → ✅ Passed
        ▼
Step 5: Autofix + 重新驗證
```

### 規則分類體系

所有規則以 Markdown 結構化存放在 `references/rules/`：

| 分類 | 規則數 | 涵蓋內容 |
|------|--------|---------|
| **Metadata** | 5 | 競品品牌詞、Apple 商標濫用、中國區禁用 AI 詞彙、不正確 metadata、訂閱 metadata |
| **Subscription** | 2 | 缺少 ToS/PP 連結、誤導性定價 |
| **Privacy** | 2 | 非必要個資收集、缺少 `PrivacyInfo.xcprivacy` |
| **Design** | 2 | Sign in with Apple 後重複要求姓名/email、最低功能要求（WebView wrapper 等） |
| **Entitlements** | 1 | 未使用的 entitlement |

每條規則都包含：`What to Check` → `How to Detect` → `Resolution` → `Example Rejection`

### App 類型 Checklist

| Checklist | 適用 App 類型 |
|-----------|-------------|
| `all_apps.md` | 所有提交（通用規則） |
| `subscription_iap.md` | 訂閱 / 應用內購買 |
| `social_ugc.md` | 社群 / UGC 內容 |
| `kids.md` | 兒童類別 |
| `health_fitness.md` | 健康、健身、醫療 |
| `games.md` | 遊戲 |
| `macos.md` | macOS / Mac App Store |
| `ai_apps.md` | AI / 生成式 AI |
| `crypto_finance.md` | 加密貨幣、金融交易 |
| `vpn.md` | VPN 與網路 |

## 安裝與使用

### 安裝

```bash
npx skills add truongduy2611/app-store-preflight-skills
```

### 前置需求

- **asc CLI**：`brew install asc`（App Store Connect CLI）
- **asc 認證**：`asc auth login` 或設定 `ASC_KEY_ID` / `ASC_ISSUER_ID` / `ASC_PRIVATE_KEY_PATH`
- **jq**（選用）：部分 JSON 檢查範例使用

### 使用方式

安裝 skill 後，在 Claude Code 中直接描述需求即可：

- 「幫我檢查這個 iOS 專案是否有 App Store 審核風險」
- 「我的 App 有訂閱功能，幫我做 preflight 檢查」
- 「上次被 Apple 拒絕了，幫我掃描哪裡有問題」

AI Agent 會自動載入對應的 checklist 和規則檔案進行比對。

## 重要注意事項（Gotchas）

作者在 SKILL.md 中特別標注的陷阱：

| 陷阱 | 說明 |
|------|------|
| **中國區 AI 詞彙** | 禁用詞（ChatGPT、Gemini 等）會檢查**所有** locale，不只 `zh-Hans` |
| **Privacy Manifest** | 即使你的 App 不直接呼叫 Required Reason API，第三方 SDK（Firebase、Amplitude 等）使用 `UserDefaults` / `NSFileManager` 也會觸發此要求 |
| **訂閱 ToS/PP** | Apple 要求在 App Store 描述**和**應用內購買畫面**都有** ToS/PP 連結，缺任一個都會被拒 |
| **macOS Entitlements** | Apple 會要求你解釋每個 temporary exception entitlement，不用的就移除 |
| **asc 認證** | `asc metadata pull` 需要認證，先跑 `asc auth doctor` 確認狀態 |

## 與 Greenlight 的比較

搜尋中發現了競品 [Greenlight](https://github.com/RevylAI/greenlight)，兩者定位類似但方法不同：

| 面向 | App Store Preflight | Greenlight |
|------|-------------------|------------|
| **形式** | Claude Code Skill（AI Agent 讀取規則） | 獨立 CLI 工具（Go 語言） |
| **掃描方式** | AI Agent 理解規則 + 比對專案 | 程式化模式匹配（30+ patterns） |
| **規則格式** | 結構化 Markdown（人+AI 可讀） | 硬編碼在程式中 |
| **可擴展性** | 新增 `.md` 檔案即可加規則 | 需修改原始碼 |
| **Binary 掃描** | 不支援 | 支援 IPA 檔案檢查 |
| **語言支援** | 主要 Swift / Xcode | Swift、ObjC、React Native、Expo |
| **CI/CD** | 透過 Claude Code | 原生支援 GitHub Actions |
| **輸出格式** | Markdown Report | Terminal、JSON、JUnit |

## 研究價值與啟示

### 關鍵洞察

1. **「規則即文件」是 AI Agent Skill 的優雅範式**：整個專案幾乎沒有程式碼，全是結構化 Markdown。AI Agent 讀取規則文件後自行判斷如何檢查，這比硬編碼 pattern matching 更靈活，也更容易由社群貢獻新規則

2. **Claude Code Skill 的真實落地案例**：這是一個非常實用的 skill 範例——把領域知識（Apple 審核規則）結構化後餵給 AI Agent，讓 Agent 成為領域專家。模式可遷移到任何有明確規則的審核/合規場景

3. **領域知識的半衰期問題**：Apple Review Guidelines 會隨版本更新，這些規則文件需要持續維護。作者選擇 Markdown 格式降低了維護門檻，但仍需要有人追蹤 Apple 的政策變化

4. **Autofix 的邊界很清楚**：能自動修的（刪競品詞、補 URL template）就自動修，不能自動修的（截圖、UI 重設計）就給清楚指引。這種分層策略比「全自動」或「全手動」都務實

5. **`asc` CLI 生態圈的協作模式**：Preflight Skill 建立在 `asc` CLI 和 ASC CLI Skills 之上，三個專案形成工具鏈。這種「小工具組合」的生態模式值得學習

### 與其他專案的關聯

| 對比專案 | 關聯 |
|---------|------|
| 本站 [Claude Skills Guide](claude-skills-guide.md) | Preflight 是 Claude Code Skill 的優秀實作範例，展示了「規則即文件」的 skill 設計模式 |
| 本站 [Learn Claude Code](learn-claude-code.md) | 可作為學習 Claude Code skill 開發的實戰案例 |
| [Greenlight](https://github.com/RevylAI/greenlight) | 同領域競品，但採用傳統程式化方法而非 AI Agent 方法 |
| [asc CLI](https://github.com/rudrankriyam/App-Store-Connect-CLI) | Preflight 的上游依賴，提供 App Store Connect metadata 存取 |
