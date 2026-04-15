---
date: "2026-04-15"
category: "開發工具"
card_icon: "material-spider-web"
oneliner: "自適應 Web Scraping 框架 — 網站改版後自動重新定位元素，內建繞過 Cloudflare + MCP Server"
---

# Scrapling 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |
| 官方文件 | [scrapling.readthedocs.io](https://scrapling.readthedocs.io) |
| 作者 Medium | [Creating self-healing spiders](https://medium.com/@d4vinci/creating-self-healing-spiders-with-scrapling-in-python-without-ai-web-scraping-4042a16ec4a5) |
| v0.4 介紹 | [Top AI Product](https://topaiproduct.com/2026/02/24/scrapling-v0-4-just-dropped-and-web-scraping-will-never-feel-the-same/) |

**作者：** Karim Shoair (D4Vinci)

**專案狀態：** ⭐ 36.9K+ stars · Python · BSD 3-Clause · 2024-10 創建 · v0.4

## 專案概述

Scrapling 是一個自適應（adaptive）Python Web Scraping 框架，核心差異化是：**網站改版後能自動重新定位元素**——不靠 AI/LLM，純用演算法的元素指紋比對。同時內建三層反偵測機制，可繞過 Cloudflare Turnstile 等防護。

一個 library 覆蓋從 HTTP 請求到大規模並發爬蟲的完整流程，包含 MCP Server 讓 AI Agent 直接呼叫。

## 三大核心能力

### 1. Adaptive Selector（自適應選擇器）

```python
# 第一次：建立基線
products = page.css('.product', auto_save=True)

# 網站改版後：自適應找回元素
products = page.css('.product', adaptive=True)
```

運作原理：對目標元素建立輕量指紋（tag、attributes、鄰居、DOM 結構），網站改版後用相似度演算法在新 DOM 中搜尋最匹配元素。**不依賴 LLM**。

### 2. 三層反偵測

| 層級 | Fetcher | 技術 |
|------|---------|------|
| Layer 1 | `Fetcher` | TLS 指紋模擬、stealthy headers、HTTP/3 |
| Layer 2 | `DynamicFetcher` | Playwright Chromium 完整瀏覽器 |
| Layer 3 | `StealthyFetcher` | 指紋偽造 + 自動解 Cloudflare Turnstile + DNS-over-HTTPS |

額外：內建 3,500+ 廣告/追蹤器網域封鎖、Proxy 輪換。

### 3. Spider 爬蟲框架（v0.4 新增）

- Scrapy-like API + async 支援
- 多 Session 混用（HTTP/Stealthy/Dynamic）
- 暫停 & 復原（Ctrl+C 停止，重啟繼續）
- 串流模式 + 即時統計
- robots.txt 遵守

## 效能比較

| Library | 解析 5000 元素 | vs Scrapling |
|---------|---------------|-------------|
| **Scrapling** | **2.02ms** | **1.0x** |
| Parsel/Scrapy | 2.04ms | 1.01x |
| Raw Lxml | 2.54ms | 1.26x |
| PyQuery | 24.17ms | ~12x |
| BS4 with Lxml | 1584ms | **~784x** |
| BS4 with html5lib | 3392ms | ~1679x |

## 快速開始

```bash
# 安裝
pip install "scrapling[all]"
scrapling install          # 下載瀏覽器（~500MB）

# 基本用法
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()

# 隱身模式（繞 Cloudflare）
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://example.com', headless=True)

# MCP Server（讓 AI Agent 使用）
pip install "scrapling[ai]"
```

## 目前限制 / 注意事項

- **StealthyFetcher 資源消耗大** — 瀏覽器實例消耗記憶體，大規模爬取不實際
- **Adaptive 需先建基線** — 必須先 `auto_save=True` 爬一次
- **瀏覽器下載 ~500MB** — `scrapling install` 需額外空間
- **非萬能反爬** — Akamai、DataDome 等進階防護仍可能需要額外服務
- **Python 3.10+** — 較舊環境無法使用
- **Spider 框架較新** — 相比 Scrapy 成熟生態，功能相對簡潔

## 研究價值與啟示

### 關鍵洞察

1. **「Self-healing spiders without AI」是務實的工程選擇。** 不用 LLM 而用演算法做元素追蹤——速度快（2ms vs LLM 的秒級延遲）、成本零、離線可用。這提醒我們：不是所有「智慧」問題都需要 AI，好的演算法往往更實用。

2. **36.9K stars 反映了 web scraping 的持續剛需。** 在 API 經濟和 AI 數據需求的雙重驅動下，web scraping 仍是最基礎的數據獲取方式。Scrapling 解決了兩大痛點：網站改版後 selector 壞掉、反爬蟲機制。

3. **MCP Server 整合讓 AI Agent 有了「爬蟲能力」。** 先用 Scrapling 萃取再傳給 AI，比直接讓 LLM 看整頁 HTML 省大量 token。這與 tw-house-ops 用 agent-browser 的理念一致——給 Agent 專門的「眼睛」工具。

### 與其他專案的關聯

- **vs agent-browser（tw-house-ops 依賴）：** agent-browser 專為 Claude Code 設計，Scrapling 是通用 Python 框架。Scrapling 的 MCP Server 模式可以取代 agent-browser 作為 AI Agent 的爬蟲後端。
- **對 Fluffy 生態的啟示：** fluffy-core 的 ETL pipeline 如果需要爬取外部數據（商品比價、市場監控），Scrapling 的 adaptive selector + 反偵測比 BeautifulSoup/Scrapy 更可靠。
