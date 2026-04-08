---
date: "2026-04-02"
category: "OSINT / 情報工具"
card_icon: "material-radar"
oneliner: "社群策展的 OSINT 工具目錄 — 335 個工具、21 個分類，按調查工作流組織"
---

# OsintRadar 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官網 | [osintradar.com](https://osintradar.com/) |
| 分類頁 | [osintradar.com/categories](https://osintradar.com/categories) |
| Hacker News | [Show HN: OsintRadar – Curated directory for osint tools](https://news.ycombinator.com/item?id=47646504) |
| GitHub（早期原型） | [makarson/osintradar](https://github.com/makarson/osintradar) |
| 相關生態整理 | [awesome-osint](https://github.com/jivoi/awesome-osint) |
| OSINT AI 趨勢 | [GeoSeer: The AI Agent Era of OSINT](https://geoseeer.com/blog/emerging-osint-tools-ai-agent-era) |

## 專案概述

**OsintRadar** 是一個社群驅動的開源情報（OSINT, Open Source Intelligence）工具策展目錄。它將散落在各處的 OSINT 工具、資源和工作流整理成一個可搜尋、可瀏覽的目錄網站，涵蓋 **335 個活躍連結**、**21 個分類**。

與 GitHub 上的 awesome-osint 列表不同，OsintRadar 提供了兩種導航方式：

1. **按工作流**（Workflow）— 從調查任務出發：「我要查一個 username」「我要追蹤一個 domain」
2. **按分類**（Category）— 從工具類型瀏覽：People OSINT、Cyber Threat OSINT 等

| 指標 | 數值 |
|------|------|
| 工具數量 | 335 個活躍連結 |
| 分類數 | 21 個 |
| License | MIT |
| 模式 | 社群策展 + 贊助 |

## 21 個分類完整列表

### 調查與研究類

| 分類 | 工具數 | 說明 |
|------|--------|------|
| **People OSINT** | 26 | 個人數位足跡、人際關聯映射、身份歸因 |
| **Social Media OSINT** | 24 | X/Twitter、Facebook、Instagram、TikTok、Reddit 資料收集分析 |
| **Username Analysis** | 10 | 跨平台使用者名稱追蹤與關聯 |
| **Email OSINT** | 14 | 電子郵件地址分析、驗證、洩漏研究 |
| **Image & Video OSINT** | 21 | 反向圖搜、EXIF metadata、Deepfake 偵測 |
| **Geolocation OSINT** | 11 | 衛星影像、互動地圖、地理標記定位 |
| **Academic & Records Research** | 11 | 學術文獻、族譜、商業登記檔案 |
| **Public Records OSINT** | 7 | 法院文件、商業登記、財產資料庫 |

### 網路與基礎設施類

| 分類 | 工具數 | 說明 |
|------|--------|------|
| **Domain OSINT** | 18 | WHOIS、DNS 歷史、子網域發現 |
| **IP Address OSINT** | 21 | IP 地理定位、託管商識別、歷史關聯 |
| **Web & URL OSINT** | 26 | 網站分析、基礎設施識別、信譽評估 |
| **OSINT Search Techniques** | 28 | Google dorking、搜尋引擎運算子、進階搜尋技巧 |

### 安全與威脅類

| 分類 | 工具數 | 說明 |
|------|--------|------|
| **Cyber Threat OSINT** | 26 | 惡意軟體分析、威脅情報、威脅行為者追蹤 |
| **Dark Web OSINT** | 15 | Onion 服務、地下論壇、暗網情報 |
| **Breach & Leak OSINT** | 5 | 資料洩漏分析、憑證暴露檢查 |
| **Privacy & Security OSINT** | 25 | 隱私政策、法規行動、安全揭露 |
| **Cryptocurrency OSINT** | 13 | 加密貨幣地址、交易追蹤、錢包分析 |

### 工具與輔助類

| 分類 | 工具數 | 說明 |
|------|--------|------|
| **Archive & Capture** | 11 | 網頁擷取、保存、監控、證據封存 |
| **Transport & Infrastructure Tracking** | 12 | 航班、船舶、鐵路、衛星、包裹追蹤 |
| **Synthetic Identity & Test Data** | 7 | 合成身份、一次性信箱、測試資料生成 |
| **Training & Reference OSINT** | 3 | OSINT 方法論訓練、框架、參考資源 |

## 工作流入口

OsintRadar 提供了以調查任務為起點的快速入口：

| 工作流 | 典型場景 |
|--------|---------|
| **Username investigation** | 已知使用者名稱，想找到所有平台上的帳號 |
| **Email analysis** | 分析郵件地址的歸屬、歷史、洩漏記錄 |
| **Domain research** | 調查網站的註冊資訊、DNS、基礎設施 |
| **Image verification** | 驗證圖片真偽、追溯來源、提取 metadata |
| **Geolocation research** | 從照片/影片定位拍攝地點 |
| **Wallet tracing** | 追蹤加密貨幣交易流向 |

## OSINT 生態概覽（2026）

OsintRadar 存在的背景是 2026 年 OSINT 領域的 AI 化浪潮：

### 新一代 AI OSINT 工具

| 工具 | 說明 |
|------|------|
| **World Monitor** | 開源即時全球情報 dashboard，25 個資料層 + AI 威脅分類，41K+ stars |
| **Taranis AI** | NLP 驅動的 OSINT 收集 + 情境分析，將非結構化新聞轉為結構化報告 |
| **OpenPlanter** | 開源版 Palantir，遞迴 AI Agent + 向量 embedding 進行實體關聯和事件偵測 |
| **IntellyWeave** | GLiNER 實體抽取 + Mapbox 3D 地理視覺化 + 多 Agent 檔案研究 |
| **Cylect.io** | AI OSINT 框架，自動化情報收集流程 |

> 2026 年的趨勢：從被動資料聚合 → 主動 Agentic AI 調查。工具不只檢索，還會推理、模擬和預測。

## 使用方式

OsintRadar 是純瀏覽型工具目錄，不需要安裝：

1. **瀏覽** [osintradar.com](https://osintradar.com/)
2. **選擇工作流**（從調查任務出發）或**瀏覽分類**（按工具類型）
3. **點擊工具連結** → 前往對應工具的官網/GitHub
4. **提交資源** → 社群可貢獻新工具

## 目前限制 / 注意事項

- **純目錄，無整合**：只是連結收集，不提供統一的搜尋介面或 API
- **工具品質參差**：335 個工具中品質和維護狀態不一，缺乏評分或評論機制
- **更新頻率不明**：社群驅動意味著依賴貢獻者活躍度
- **法律風險提醒**：OSINT 工具的合法使用邊界因司法管轄區而異，部分工具（Dark Web、Breach & Leak）需特別注意使用倫理和法規
- **與 awesome-osint 的重疊**：GitHub 上的 [awesome-osint](https://github.com/jivoi/awesome-osint) 已有大量工具列表，OsintRadar 的差異化主要在工作流導航和視覺化

## 研究價值與啟示

### 關鍵洞察

1. **「工作流優先」vs「分類優先」的導航設計值得學習** — 大多數工具目錄只按分類組織（awesome-xxx 列表），OsintRadar 額外提供了「我要做什麼」的工作流入口。這種雙入口設計讓新手可以從任務出發，專家可以按分類瀏覽，是策展型網站的好模式。

2. **OSINT 的 21 個分類本身就是一份知識地圖** — 從 People → Social Media → Username → Email → Domain → IP → Dark Web → Crypto，這個分類體系描繪了一條完整的數位調查路徑。理解這些分類等於理解了 OSINT 的知識結構。

3. **2026 年 OSINT 的 AI Agent 化是顯著趨勢** — World Monitor（41K stars）、OpenPlanter、Taranis AI 等都採用 Agentic AI 架構。OSINT 從「人用工具搜尋」轉向「AI Agent 自主調查」，這與 Coding Agent（Claude Code、gstack）的趨勢平行。

4. **Cryptocurrency OSINT（13 工具）反映了區塊鏈追蹤的主流化** — 錢包追蹤和交易分析已成為 OSINT 的標準分類之一，不再是小眾技能。這對量化交易和合規場景都有參考價值。

5. **Synthetic Identity 分類的存在暗示了攻防兩面** — 「合成身份和測試資料」工具既用於研究時的操作隔離（防止暴露真實身份），也是社交工程防禦的研究對象。這個分類的存在提醒我們 OSINT 工具本質上是雙刃劍。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [Browser-Bound MCP Flights](browser-bound-mcp-flights.md) | Flight tracking 是 Transport & Infrastructure Tracking 分類的核心場景，MCP + 瀏覽器的航班追蹤可視為 OSINT 工具的一種 |
| [ITA Matrix](ita-matrix.md) | 航班搜尋和追蹤與 OSINT 的 Transport Tracking 分類交叉 |
| [gstack](gstack.md) | gstack 的 `/cso` skill 做 OWASP + STRIDE 威脅建模，與 Cyber Threat OSINT 分類有概念交集 |
| [Discord Lobster](discord-lobster.md) | 社群監控工具本質上是 Social Media OSINT 的應用場景 |
