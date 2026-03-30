---
date: ""
category: "量化交易"
card_icon: "material-chart-bar"
oneliner: "股票統計分析工具"
---
# StockStats 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub | https://github.com/jealous/stockstats |
| PyPI | https://pypi.org/project/stockstats/ |
| 版本 | 0.6.7 |
| 授權 | BSD-3-Clause |

## 專案概述

StockStats 是一個 Python 套件，提供 pandas DataFrame 的包裝器 `StockDataFrame`，支援內建的股票統計指標計算。只需要使用欄位名稱存取，指標就會自動計算，極大簡化了技術分析的程式撰寫。

這個專案解決的問題是技術指標計算繁瑣的困境。傳統上計算 MACD、RSI、布林通道等指標需要自己撰寫公式，而 StockStats 只需要 `df['macd']` 或 `df['rsi_14']` 就能自動完成計算。

適合場景：
- 量化交易策略回測
- 股票技術分析
- 金融數據研究
- AI Agent 整合股票分析功能

## 核心功能

1. **趨勢指標**：SMA、EMA、MACD、TRIX、TEMA、DMA
2. **動量指標**：RSI、KDJ、CCI、WR、MFI、ROC
3. **波動率指標**：Bollinger Bands、ATR、CHOP
4. **成交量指標**：VR、VWMA、PVO
5. **其他指標**：Ichimoku Cloud、Aroon、Supertrend、Z-Score
6. **基本運算**：delta、shift、log return、max/min in range
7. **比較運算**：cross（上穿/下穿）、count（計數）
8. **進階指標**：KAMA、StochRSI、Wave Trend、Coppock Curve

## 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                    StockStats 架構                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                 pandas.DataFrame                        ││
│  │  ┌───────────────────────────────────────────────────┐  ││
│  │  │  date | open | high | low | close | volume        │  ││
│  │  └───────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                   │
│                          ▼ wrap()                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                 StockDataFrame                          ││
│  │  ┌───────────────────────────────────────────────────┐  ││
│  │  │  繼承 pandas.DataFrame 所有功能                    │  ││
│  │  │  + 內建指標自動計算                                │  ││
│  │  └───────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    指標存取模式                               │
│                                                              │
│  df['指標名稱']          → 自動計算並返回 Series             │
│  df['column_window_統計'] → 帶參數的指標                     │
│                                                              │
│  範例：                                                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  df['rsi']        → 14 期 RSI (預設)                    ││
│  │  df['rsi_6']      → 6 期 RSI                            ││
│  │  df['macd']       → MACD 線                             ││
│  │  df['macds']      → MACD 訊號線                         ││
│  │  df['macdh']      → MACD 柱狀圖                         ││
│  │  df['boll']       → 布林中軌                            ││
│  │  df['boll_ub']    → 布林上軌                            ││
│  │  df['boll_lb']    → 布林下軌                            ││
│  │  df['close_10_sma'] → 10期收盤價SMA                     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    支援的指標分類                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐│
│  │ 趨勢指標   │  │ 動量指標   │  │ 波動指標   │  │ 成交量    ││
│  │ ───────── │  │ ───────── │  │ ───────── │  │ ───────── ││
│  │ SMA/EMA   │  │ RSI       │  │ Bollinger │  │ VR        ││
│  │ MACD      │  │ KDJ       │  │ ATR       │  │ VWMA      ││
│  │ TRIX/TEMA │  │ CCI/WR    │  │ CHOP      │  │ MFI       ││
│  │ DMA       │  │ ROC       │  │ Supertrend│  │ PVO       ││
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 安裝與使用

### 安裝

```bash
pip install stockstats
```

### 基本使用

```python
import pandas as pd
from stockstats import wrap

# 載入股票數據（需包含 date, open, high, low, close, volume）
data = pd.read_csv('stock.csv')

# 包裝成 StockDataFrame
df = wrap(data)

# 自動計算指標
rsi = df['rsi']           # 14期 RSI
macd = df['macd']         # MACD 線
boll = df['boll']         # 布林中軌

# 帶參數的指標
rsi_6 = df['rsi_6']       # 6期 RSI
sma_20 = df['close_20_sma']  # 20期 SMA

# 一次初始化所有快捷指標
df.init_all()
```

### yfinance 整合

```python
import yfinance as yf
from stockstats import wrap

# 下載數據（禁用多層索引）
data = yf.download('AAPL', multi_level_index=False)

# 包裝並計算指標
df = wrap(data)
print(df[['close', 'rsi', 'macd']])
```

### 交叉訊號檢測

```python
# 檢測 MACD 金叉（上穿）
golden_cross = df['macd_macdh_xu_macds']

# 檢測 MACD 死叉（下穿）
death_cross = df['macd_macdh_xd_macds']

# 自訂交叉
# close 上穿 close_20_sma
df['close_xu_close_20_sma']
```

## 與其他工具的比較

| 特性 | StockStats | TA-Lib | pandas-ta |
|------|-----------|--------|-----------|
| 安裝難度 | ✅ 簡單 | ❌ 需編譯 | ✅ 簡單 |
| 語法簡潔 | ✅ 極簡 | ⚠️ 中等 | ✅ 簡潔 |
| 指標數量 | ⚠️ 50+ | ✅ 150+ | ✅ 130+ |
| 自動計算 | ✅ 存取即算 | ❌ 需呼叫 | ⚠️ 需呼叫 |
| pandas 整合 | ✅ 原生 | ⚠️ 需轉換 | ✅ 原生 |
| 維護狀態 | ✅ 活躍 | ⚠️ 較少 | ✅ 活躍 |

## 研究心得

StockStats 是一個優雅且實用的技術分析套件，其「存取即計算」的設計理念非常巧妙。

**設計亮點：**
1. **繼承 DataFrame**：保留所有 pandas 功能，無學習成本
2. **Lazy Evaluation**：首次存取時才計算，後續直接使用快取
3. **命名規範清晰**：`column_window_indicator` 格式直觀易懂
4. **自動欄位適配**：支援大小寫不敏感的欄位名稱

**對 AI Agent 開發的價值：**
- 可作為股票分析 Agent 的技術指標工具
- 簡潔的 API 適合 Agent 工具封裝
- 與 yfinance 整合可實現完整的數據流程

**使用建議：**
- 小規模數據使用 `init_all()` 方便，大數據量按需計算
- 刪除已計算欄位可觸發重新計算
- 注意 yfinance 的多層索引問題，建議禁用

**限制：**
- 指標數量不如 TA-Lib 完整
- 某些複雜指標的參數自訂較受限

---
研究日期：2026-02-03
