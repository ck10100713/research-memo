# 量化交易

本分類收錄 45 篇研究筆記。

| 日期 | 筆記 | 摘要 |
| --- | --- | --- |
| 2026-08-06 | [GS Quant（gs-quant）](../gs-quant.md) | Goldman Sachs 官方量化金融 Python 工具包：把 GS 自家衍生品定價／風險引擎、跨資產回測、時間序列分析包成統一 API；近期加碼官方 MCP server 與 agent skills |
| 2026-07-28 | [StockAgent](../stockagent.md) | ACM TIST 論文的官方實作：用 LLM 多代理模擬股市，刻意不餵歷史行情以避開 test set leakage；核心結論是「換一個 LLM 就換一種市場」——GPT 交易少但單量大、個體分散，Gemini 頻繁交易且群體高度趨同。程式碼有多處已驗證的落差，預設參數下所有事件都不會觸發 |
| 2026-07-24 | [Vibe-Trading（HKUDS）](../vibe-trading.md) | HKUDS 的『個人交易 Agent』——pip 一行裝起，自然語言驅動 88 skill / 462 alpha / 8 回測引擎，安全設計靠結構性 paper/live 護欄而非 config flag |
| 2026-05-19 | [Daily Stock Analysis](../daily-stock-analysis.md) | ZhuLinsen 用 GitHub Actions 跑零成本 A/H/美股 LLM 智能分析，37k stars、多 LLM + 多新聞源 + 多通知頻道、15 內建策略 + Agent 問股，工作日 18:00 自動推「決策仪表盘」 |
| 2026-05-19 | [QuantDinger](../quantdinger.md) | brokermr810 自架式 AI 量化交易作業系統，一個 Docker Compose 串聯 AI 研究/Python 策略/回測/實盤(crypto+IBKR+MT5+Alpaca)，Agent Gateway + MCP，內建 USDT 計費可變 SaaS |
| 2026-05-15 | [Fincept Terminal](../fincept-terminal.md) | Fincept Corp 開源 Bloomberg-style 金融終端，C++20 + Qt6 + 嵌入式 Python，37 AI agents（巴菲特/葛拉漢/林區...）、100+ 資料源、16 券商整合，21k stars / AGPL-3.0 |
| 2026-05-07 | [On Accelerating Large-Scale Robust Portfolio Optimization](../accelerating-robust-portfolio-optimization.md) | Hsieh × Lu 2024：把 distributionally robust portfolio 的求解時間從幾千秒壓到個位數秒，extended supporting hyperplane approximation 用在 S&P 500 全成分股 |
| 2026-05-07 | [Generalization of Affine Feedback Stock Trading Results to Include Stop-Loss Orders](../affine-feedback-stop-loss.md) | Hsieh 2022 Automatica：把 affine feedback stock trading 結果擴張至含 stop-loss 訂單，GBM 下給出累積 P&L 的閉式 CDF，含 stop-loss 涵蓋無 stop 為特例 |
| 2026-05-07 | [Asset Pricing Theory with Ambiguity（工作中 working paper）](../asset-pricing-with-ambiguity.md) | Hsieh × Po-Hsuan Hsu 工作中：把 ambiguity（Knightian 不確定性）放進資產定價框架，預期接續作者整條 distributionally robust 路線推到 pricing 層級 |
| 2026-05-07 | [On Asymptotic Log-Optimal Buy-and-Hold Strategy](../asymptotic-log-optimal-buy-hold.md) | Hsieh 2023 Automatica：證明只要存在 dominant asset，buy-and-hold 就是 asymptotically log-optimal，且 frequency-based 高頻再平衡無法超越被動持有 |
| 2026-05-07 | [On Cost-Sensitive Distributionally Robust Log-Optimal Portfolio](../cost-sensitive-distributionally-robust-portfolio.md) | Hsieh × Yu 2024：用 Wasserstein ball 量化分布不確定性，加上一般凸交易成本模型，證明無成本時收斂等權重、有成本時資金往無風險資產偏移 |
| 2026-05-07 | [On Robustness of Double Linear Policy with Time-Varying Weights](../dlp-time-varying-weights.md) | Wang × Hsieh 2023 CDC：把 Double Linear Policy 從常數權重推廣到 time-varying 權重，用 elementary symmetric polynomials 證明 robust positive expectation，可接 moving average 訊號 |
| 2026-05-07 | [On Robustness of Double Linear Trading with Transaction Costs](../dlp-with-transaction-costs.md) | Hsieh 2022 L-CSS：DLP 加上交易成本後 robust positive expected gain 可能消失，本篇給出保留正期望的條件、用 GBM with jumps 模擬與 BTC-USD 回測驗證 |
| 2026-05-07 | [On Data-Driven Drawdown Control with Restart Mechanism in Trading](../drawdown-control-restart-mechanism.md) | Hsieh 2023 IFAC：drawdown modulation 觸發後不再像 stop-loss 那樣放棄，加 data-driven restart 自動重啟，含成本仍打敗原版且維持 max drawdown 上限 |
| 2026-05-07 | [On Drawdown-Modulated Feedback Control in Stock Trading](../drawdown-modulated-stock-trading.md) | Hsieh × Barmish 2017 IFAC：Drawdown Modulation Lemma 刻畫「以機率 1 維持 max drawdown 上限」的投資族，並在此族內最大化 Kelly ELG，給出 drawdown-constrained Kelly 的最佳投資 |
| 2026-05-07 | [The Impact of Execution Delay on Kelly-Based Stock Trading: High-Frequency Versus Buy and Hold](../execution-delay-kelly-trading.md) | Hsieh × Barmish × Gubner 2019 CDC：證明無延遲時 high-frequency trading 嚴格優於 buy-and-hold，但執行延遲存在時 buy-and-hold 反過來勝出 — 即使零成本 |
| 2026-05-07 | [On Feedback Control in Kelly Betting: An Approximation Approach](../feedback-control-kelly-betting-approximation.md) | Hsieh 2020 CCTA：Kelly betting 用 Taylor 近似化為 quadratic programming，得到閉式近似解，並分析績效、變異數、survivability 等性質 |
| 2026-05-07 | [Necessary and Sufficient Conditions for Frequency-Based Kelly Optimal Portfolio](../frequency-based-kelly-portfolio.md) | Hsieh 2021 L-CSS：給出 frequency-based Kelly 最佳組合的充分必要條件、Extended Dominant Asset Theorem，並提出顯式 trading algorithm 用 dominant asset 條件決定下單時點 |
| 2026-05-07 | [At What Frequency Should the Kelly Bettor Bet?](../kelly-bettor-frequency.md) | Hsieh × Barmish × Gubner 2018 ACC：Bernoulli 押注場景下，零成本時最優 ELG 對下注間隔 n 為非遞增、提出 sufficient attractiveness inequality 作為低頻匹配高頻的條件 |
| 2026-05-07 | [On Kelly Betting: Some Limitations](../kelly-betting-limitations.md) | Hsieh × Barmish 2015 Allerton：Kelly 系列研究的開山批判篇—點出 Taylor 近似失準與 drawdown 過大兩個 Kelly 主結論的限制，定調作者後續整條 Kelly 研究線的問題清單 |
| 2026-05-07 | [Kelly Betting Can Be Too Conservative](../kelly-betting-too-conservative.md) | Hsieh × Barmish × Gubner 2016 CDC：跟主流「Kelly 太激進」相反，本篇證明 Kelly 常常太保守—Restricted Betting Theorem 顯示 unbounded support 分布下 Kelly 押注趨近 0、實證樣本反而更積極 |
| 2026-05-07 | [Compounding Effects in Leveraged ETFs: Beyond the Volatility Drag Paradigm](../leveraged-etf-compounding.md) | Hsieh × Chang × Chen 2025：挑戰「LETF 必受 volatility drag」教條，AR(1) + AR-GARCH + regime switching 分析顯示獨立報酬下 LETF 可正複利、動能市每日再平衡有利、均值回復期低頻再平衡反而保護 |
| 2026-05-07 | [On Inefficiency of Markowitz-Style Investment Strategies When Drawdown is Important](../markowitz-inefficiency-drawdown.md) | Hsieh × Barmish 2017 CDC：以 drawdown 取代 variance 當風險指標時，古典 Markowitz LTI 反饋策略不效率，drawdown modulator 時變反饋以機率 1 提供 worst-case drawdown 保護 |
| 2026-05-07 | [On Positive Solutions of a Delay Equation Arising When Trading in Financial Markets](../positive-solutions-delay-equation.md) | Hsieh × Barmish × Gubner 2020 IEEE TAC：把交易者帳戶價值寫成離散時間含延遲線性方程，找出 feedback gain α₋/α₊ 兩個門檻分別保證「永不破產」與「必破產」 |
| 2026-05-07 | [On Frequency-Based Optimal Portfolio with Transaction Costs](../frequency-based-optimal-portfolio-costs.md) | Wong × Hsieh 2023：把 frequency-dependent log-optimal portfolio 加上交易成本後仍保持為 concave program，用兩基金定理 + sliding window 解出每期可實作的解 |
| 2026-05-07 | [A Jump Start to Stock Trading Research for the Uninitiated Control Scientist: A Tutorial](../jump-start-stock-trading-tutorial.md) | Barmish × Formentin × Hsieh × Proskurnikov × Warnick 2024 CDC tutorial：寫給控制論研究者的股票交易入門指南，把交易研究的核心問題、方法論、未解難題系統性地展示給 control 社群 |
| 2026-05-07 | [Rebalancing Frequency Considerations for Kelly-Optimal Stock Portfolios in a Control-Theoretic Framework](../rebalancing-frequency-kelly-portfolios.md) | Hsieh × Gubner × Barmish 2018 CDC：把再平衡頻率明確當參數放進 Kelly-optimal 框架，證明 dominant 條件下績效對頻率為常數函數，HFT 不必然改善 |
| 2026-05-07 | [On Risk-Sensitive Decision Making Under Uncertainty](../risk-sensitive-decision-making.md) | Hsieh × Wong 2025 ACC：固定階段、含確定與隨機選項的 risk-sensitive 多階段決策，導出最佳性必要條件，示範用於最佳押注與庫存管理 |
| 2026-05-07 | [On Solving Robust Log-Optimal Portfolio: A Supporting Hyperplane Approximation Approach](../robust-log-optimal-hyperplane.md) | Hsieh 2024 EJOR：用 supporting hyperplane 把 distributionally robust log-optimal portfolio 化成線性規劃，可內建交易成本、槓桿、做空、survival、分散性條件 |
| 2026-05-07 | [From Semi-Infinite Constraints to Structured Robust Policies: Optimal Gain Selection for Financial Systems](../robust-optimal-linear-feedback-trading.md) | Hsieh 2022 / 2025 修訂：DLP 結構派的源頭論文，把 semi-infinite constraints 化成 balanced / complementary 兩種結構策略，廣義化 mean-variance 並提供圖形求解法 |
| 2026-05-07 | [Robust Trading in a Generalized Lattice Market](../robust-trading-lattice-market.md) | Chung-Han Hsieh × Xin-Yu Wang 把 Double Linear Policy 從單一資產推廣到多資產相關的 lattice market，理論證明在對稱市場仍能保證 survivability + 正期望報酬，S&P 500 前 30 大實證有效 |
| 2026-05-07 | [On Data-Driven Log-Optimal Portfolio: A Sliding Window Approach](../sliding-window-log-optimal-portfolio.md) | Wang × Hsieh 2022 IFAC：用 sliding window 解 log-optimal portfolio，產生時變權重而非靜態配置，累積報酬率超越傳統常數權重 log-optimal |
| 2026-05-07 | [On Unified Adaptive Portfolio Management](../unified-adaptive-portfolio-management.md) | Li × Hsieh 2023：把 dynamic Black-Litterman + 因子模型 + Elastic Net + 動態 sliding window 整合成一個 adaptive portfolio 框架，S&P 500 前 100 大十年實證含 turnover 成本仍有效 |
| 2026-04-24 | [AI Hedge Fund](../ai-hedge-fund.md) | 13 位傳奇投資人 + 6 個分析/管理 Agent 協同分析股票，LangGraph 驅動的多 Agent 對沖基金模擬系統，2026-04 衝到 57K stars 且新增 Nassim Taleb 黑天鵝 Agent |
| 2026-04-15 | [AI-Trader](../ai-trader.md) | 港大 AI 交易 Benchmark + Agent-Native 社交交易平台 — 真實市場、MCP 工具鏈、多 Agent 協作 |
| 2026-04-15 | [TimesFM](../timesfm.md) | Google 時間序列基礎模型 — 200M 參數、16K context、zero-shot 預測，已整合 BigQuery |
| 2026-04-12 | [Kronos](../kronos.md) | 首個金融 K 線基礎模型，將 OHLCV 離散化為階層式 Token 進行自回歸預測 |
| 2026-03-29 | [NOFX](../nofx.md) | Go 撰寫的全自主 AI 交易助理，x402 USDC 微支付取代 API key，連接 9 個交易所執行真實訂單 |
| 2026-03-29 | [pmxt](../pmxt.md) | 預測市場的 CCXT — 統一 API 連接 7 個交易所（Polymarket/Kalshi 等），Sidecar + OpenAPI 雙語言 SDK |
| 2026-03-29 | [Prediction Market Analysis](../prediction-market-analysis.md) | 2.92 億筆 Polymarket/Kalshi 交易的公開最大數據集，附學術研究框架與「財富轉移微結構」論文 |
| 2026-03-29 | [The Alchemy of Multibagger Stocks](../multibagger-stocks.md) | 464 支美股 10-bagger 實證研究：FCF/P 是最強因子、EPS 成長不顯著、動量呈反轉型態（CAFE Working Paper No.33） |
| 2026-03-23 | [OpenStock](../openstock.md) | 開源股票分析工具 |
| 2026-03-23 | [StockStats](../stockstats.md) | 股票統計分析工具 |
| 2026-03-23 | [TEJAPI Python Medium Quant](../tejapi_python_medium_quant.md) | TEJ API 量化交易 Python 教學 |
| 2024-12-28 | [TradingAgents](../tradingagents.md) | 多 Agent 協作的量化交易決策系統 |
