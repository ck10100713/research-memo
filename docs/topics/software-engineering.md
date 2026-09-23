# 軟體工程知識

本分類收錄 4 篇研究筆記。

| 日期 | 筆記 | 摘要 |
| --- | --- | --- |
| 2026-09-18 | [Copilot runtime 搬到 Rust](../copilot-runtime-rust-port.md) | Stephen Toub 寫的 65 分鐘長文：GitHub Copilot agent runtime 從 TypeScript/Node 整包換成 Rust，43 萬行 TS 換出 83 萬行production Rust，2026-05-12 到 08-21 約 14 週，主要由一個人 + 大量 agent 完成，128 個 PR 邊搬邊出貨。有硬數字：單次 turn 從 5.25 秒降到 292 毫秒（18 倍）、session 生命週期吞吐從 7.55/秒 到 120/秒。更值得看的是 agent 使用數據——工具呼叫 185 萬次裡探索類是編輯類的 10 倍、prompt cache 命中率 96.22%、壓縮 5,116 次、borrow checker 只佔編譯錯誤的 1.7%。還有兩個真實事故：agent 之間互相併吞分支、以及用一個 chat session 當「agentic mutex」擋建置塞車 |
| 2026-06-05 | [HighScalability.com](../highscalability.md) | 經營 17 年的大規模系統架構案例庫，2024 年由 ByteByteGo 收購接手 |
| 2026-05-25 | [Laws of Software Engineering](../laws-of-software-engineering.md) | Dr. Milan Milanović 整理的 56 條軟體工程定律參考站，分七大類（團隊/規劃/架構/品質/設計/規模/決策），含書、海報、JSON API、50k 訂閱電子報，已成 Amazon 暢銷書 |
| 2026-05-25 | [軟體工程 56 大定律（完整中文版）](../laws-of-software-engineering-zh.md) | 56 條軟體工程定律完整中文版，每條附背景、實例、應用建議，搭配 laws-of-software-engineering.md 原版作為中文受眾學習資源 |
