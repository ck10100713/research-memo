---
date: "2026-05-15"
category: "量化交易"
card_icon: "material-chart-multiple"
oneliner: "Fincept Corp 開源 Bloomberg-style 金融終端，C++20 + Qt6 + 嵌入式 Python，37 AI agents（巴菲特/葛拉漢/林區...）、100+ 資料源、16 券商整合，21k stars / AGPL-3.0"
---

# Fincept Terminal 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/Fincept-Corporation/FinceptTerminal> |
| 官方網站 | <https://fincept.in> |
| Discord | <https://discord.gg/ae87a8ygbN> |
| Reddit | <https://reddit.com/r/finceptTerminal/> |
| Telegram | <https://t.me/finceptTerminalcorp> |
| Trendshift | <https://trendshift.io/repositories/17028> |
| 最新版本 | v4.0.3（pure native C++ 重寫版） |
| 規模 | 21,480 stars / 2,905 forks / AGPL-3.0 / 創建 2024-08-29（May 2026 抓取） |
| 語言 | C++20 + Qt 6.8.3 + 嵌入式 Python 3.11.9 |

## 概述

**Fincept Terminal** 是印度公司 Fincept Corporation 推出的開源金融終端機，定位是 **「Bloomberg Terminal 的開源版」**，提供 buy-side analyst 等級的多資產分析、AI 自動化決策、機構級即時行情。slogan：**"Your Thinking is the Only Limit. The Data Isn't."**

v4 是 2026 推出的**純原生 C++20 重寫版**——以 Qt6 做 UI、嵌入式 Python 跑分析，**單檔 native binary**，刻意避開 Electron / 瀏覽器 runtime / Node.js 的肥大堆疊。這是這個專案在 21k stars 規模下仍敢做架構大轉身的關鍵賭注。

## 核心功能矩陣

| 模組 | 內容 |
|------|------|
| 📊 **Multi-Asset Analytics** | DCF 模型、portfolio optimization、VaR / Sharpe / 衍生品定價，跨股票 / 固收 / 衍生品 / 投組 / 另類資產（embedded Python） |
| 🤖 **37 AI Agents** | Trader/Investor: Buffett, Graham, Lynch, Munger, Klarman, Marks ...；Economic、Geopolitics 兩大框架；支援本地 LLM + 多 provider (OpenAI / Anthropic / Gemini / Groq / DeepSeek / MiniMax / OpenRouter / Ollama) |
| 🌐 **100+ Data Connectors** | DBnomics、Polygon、Kraken、Yahoo、FRED、IMF、World Bank、AkShare、政府 API；可選 **Adanos 替代資料**（Reddit / X / 金融新聞 / Polymarket 散戶情緒） |
| 📈 **Real-Time Trading** | 加密貨幣：Kraken / HyperLiquid WebSocket；股票算法交易；**paper trading engine**；16 券商整合 |
| 🔬 **QuantLib Suite** | 18 個量化分析模組（pricing / risk / stochastic / volatility / fixed income） |
| 🚢 **Global Intelligence** | 海運追蹤、地緣政治分析、關係圖、衛星資料 |
| 🎨 **Visual Workflows** | Node Editor 做自動化 pipeline + **MCP 工具整合** |
| 🧠 **AI Quant Lab** | ML 模型、因子發掘、HFT、強化學習交易 |

## 16 個券商整合（**主場印度市場**）

```text
印度券商（10）: Zerodha, Angel One, Upstox, Fyers, Dhan, Groww,
                Kotak, IIFL, 5paisa, AliceBlue, Shoonya, Motilal
國際券商（5） : IBKR (Interactive Brokers), Alpaca, Tradier, Saxo
```

→ **這是世界上極少數同時支援 10 家以上印度本土券商的開源終端**。對印度散戶 / 量化團隊是重大利多；對台灣 / 美國使用者主要靠 IBKR + Alpaca 即可。

## 技術選型

| 項目 | 選擇 |
|------|------|
| 語言 | C++20 + 嵌入式 Python |
| UI | Qt 6.8.3（Qt Online Installer，**版本鎖死**，drift 需傳 `-DFINCEPT_ALLOW_QT_DRIFT=ON`） |
| 編譯 | CMake 3.27.7 + Ninja 1.11.1 |
| 編譯器 | MSVC 19.38 (VS 2022 17.8) / GCC 12.3 / Apple Clang 15.0 |
| 部署目標 | Win10 SDK 10.0.22621.0 / macOS 11+ / glibc 2.31+ |
| 二進位 | 單一 native exe / dmg / AppImage |
| 預編譯支援 | Windows x64 / Linux x64 / **macOS Apple Silicon** |
| Docker | 僅給 CI/CD 用，**Linux + X11 限定**，Windows / macOS 不支援 |

→ **「版本鎖死 + 單一 native binary」** 反映 Fincept 把這個專案當 production-grade product 在做，不是業餘玩具。對使用者來說好處是「下載 → 跑」，沒有 Python 環境地獄。

## 安裝路徑（最簡 → 最完整）

```bash
# Option 1：直接下載 installer（推薦給使用者）
# Windows / Linux / macOS arm64 都有預編譯

# Option 2：一鍵腳本（Linux / macOS）
git clone https://github.com/Fincept-Corporation/FinceptTerminal.git
cd FinceptTerminal && chmod +x setup.sh && ./setup.sh

# Option 3：Docker（CI only）

# Option 4：手動 CMake preset 編譯
cd fincept-qt
cmake --preset macos-release
cmake --build --preset macos-release
```

## 路線圖

| 時程 | 內容 |
|------|------|
| 已交付 | Real-time streaming、16 broker integrations、multi-account trading、PIN authentication、theme system |
| 2026 Q2 | Options strategy builder、多投組管理、AI agents 擴至 50+ |
| 2026 Q3 | Programmatic API、ML 訓練 UI、機構功能 |
| 未來 | 行動 app、雲端同步、社群 marketplace |

## 目前限制與注意事項

- **AGPL-3.0**：任何 SaaS / 二創必須**開源整個系統**（不只是改動部分），商用要走 commercial license（`docs/COMMERCIAL_LICENSE.md`）。
- **發行 pump.fun meme coin**：repo README 直接列了 Solana mint address，靠社群幣募資。**對追求嚴肅工程的量化使用者是負面訊號**——任何依賴 token 經濟學支撐的開源項目，未來治理風險都偏高。
- **主場是印度市場**：16 個券商有 10 個是印度的，AI agents 預設策略可能對印度市場做過調整；對非印度市場使用者，券商支援只剩 IBKR / Alpaca / Tradier / Saxo。
- **架構變動成本**：v3 → v4 從 Python 改 C++ 是大重寫，目前仍在演進，**新功能跨版本搬遷可能存在不一致**。
- **Qt 版本鎖死**：必須用 Qt 6.8.3 精確版本，系統包管理的 6.x minor 可能不相容；CI / production 需要自管 Qt 安裝。
- **沒有 Docker 真實桌面支援**：Docker 只給 Linux X11 用，Windows / macOS 沒法在容器跑——這對 dev / CI 場景是個侷限。
- **AI Agents 是「人格 prompt 包裝」級別**：37 個 agents（Buffett / Graham / Lynch ...）本質是 LLM + 角色 prompt，**不是真的執行該人物投資策略的程式**。看到「Buffett Agent」要明白這是「用 LLM 模擬 Buffett 視角的分析框架」，不是 quantitative reproduction。
- **無同行評審 / 學術 paper**：跟 [[ai-hedge-fund]] 類似，是 productized open source，內含的策略 / 因子需自行驗證。

## 研究價值與啟示

### 關鍵洞察

1. **「開源 Bloomberg」是個正在被多方嘗試的賽道**：跟 [[ai-hedge-fund]]（純 Python + LLM agents 路線）、[[openstock]]（更輕量）、[[tradingagents]] 形成清晰的競爭光譜。**Fincept 是其中唯一走「native C++ + 預編譯 binary」路線的**，瞄準的是「真的要每天看盤的人」而非「跑研究 notebook 的人」。
2. **AI Agents = 投資人物 prompt 包裝**已成 retail quant 圈標配 UX：Buffett / Graham / Lynch / Munger / Klarman / Marks 這套 cast 跟 [[ai-hedge-fund]] 高度重合。背後反映的是「LLM 角色扮演」變成散戶 quant tool 的固定 UI pattern——但這不等於這些 agents 真的能複製大師的決策框架，**只是把對應投資哲學寫進 system prompt**。
3. **「不是 Electron」是個越來越值錢的賣點**：21k stars 的 Bloomberg-clone 走純 native C++ 路線，反映社群對 Electron / 瀏覽器 runtime 的疲勞。對比 [[appflowy]] 那種跨平台 Tauri / Flutter / native 嘗試，Fincept 的 Qt6 + C++ 是少數**對 desktop performance 做嚴肅承諾**的金融工具。
4. **印度 retail quant 生態系正在開源化**：10 個印度券商集成 + 印度 founder + AGPL，反映印度 fintech 圈正在用開源策略打進原本被 Bloomberg / Reuters 壟斷的機構工具市場。台灣 retail quant 圈可以參考這個路線（TEJ + 永豐 + 元大 API 也能整成類似的 stack）。
5. **嵌入式 Python 是 C++ 桌面金融 app 的正解**：用 C++ 寫 UI + WebSocket + 即時行情、用 Python 跑 DCF / VaR / pricing，是經典「performance-critical 用快語言、業務邏輯用快開發語言」的分工。值得當作任何 native 金融 app 的架構範本。
6. **meme coin 募資是 2026 開源金融項目的新風險訊號**：Fincept 直接在 README 放 pump.fun token，這跟 [[ai-hedge-fund]] 的「純 retail quant + 純 OSS」路線形成對比。**對需要長期穩定的工具使用者，token 經濟學引入的不可控因素應該被列入評估**。
7. **`docs/COMMERCIAL_LICENSE.md` 是 AGPL 雙授權的標準操作**：對台灣中小型 fintech / 投顧公司，要把 Fincept 整進產品就必須走商用授權；對個人 / 學術使用 AGPL 完全 OK。值得當作開源量化工具的商用模式參考。

### 與其他研究的關聯

- 與 [[ai-hedge-fund]]、[[tradingagents]]、[[ai-trader]]：四者都做「LLM agents + 投資策略」，但 Fincept 是**唯一把這個能力包進完整 native desktop app** 的；其他三者是 Python framework / CLI。對「散戶要看盤 vs 研究員要 backtest」兩種使用者體驗對比明確。
- 與 [[openstock]]、[[stockstats]]、[[tejapi_python_medium_quant]]：純資料 / 純指標路線的另一極；Fincept 把這些都吞進去了（100+ data connectors）。
- 與 [[ramp-ai-agents]]、[[appflowy]]：本案是「桌面 desktop app 的金融特化版」，跟 Ramp / AppFlowy 同屬「AI-powered desktop tool」族群，技術選型上 Fincept 的 Qt6 + C++ 路線是最重的。
- 與 [[ai-agents-for-beginners]]、[[mcp-for-beginners]]：Fincept 的 Node Editor 整合了 MCP 工具——對學完 Microsoft 那套 Agent 教材後想看實戰應用的學習者，是個值得對照的範例。
- 與 [[claude-financial-services-plugins]]：兩者都針對金融場景做 AI 整合，但走完全不同方向——Anthropic plugin 是 Claude-native skill，Fincept 是 native app 內接多 LLM provider。對「金融 AI 工具該綁哪個生態」的決策有參考價值。
- 對台灣 retail quant：Fincept 不直接支援台股券商（永豐、元大、富邦），要實用需自寫 connector；但**它的整體架構（嵌入式 Python + Qt + 多 broker abstraction）是值得直接 fork 改成「台版 Fincept」的範本**。
