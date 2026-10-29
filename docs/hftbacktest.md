---
date: "2026-10-28"
category: "量化交易"
card_icon: "material-timer-sand"
oneliner: "nkaz001 的高頻交易 / 造市回測框架:用逐筆 L2/L3 訂單簿重建市場,模擬掛單在佇列中的位置、行情與下單兩種延遲,讓回測結果盡量對得上實盤;Rust 核心 + Python(Numba njit)介面,同一份 Rust 策略能直接接 Binance Futures / Bybit 實盤。5k★、MIT,但 master 自 2025-12 後沒有新 commit"
tags:
  - quant
  - backtesting
  - rust
---

# hftbacktest 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/nkaz001/hftbacktest> |
| 文件 | <https://hftbacktest.readthedocs.io/> |
| PyPI / crates | `pip install hftbacktest` · `hftbacktest` crate |
| 分析 commit | `5f3ec40`(2025-12-23) |

> Metadata(2026-10-28 抓取):**5,016 stars / 951 forks** · MIT · 建立於 2022-08-25。最新版 rust-v0.9.4 / py-v2.4.4(2025-12-10),之後 master 沒有新 commit,另有 `ci`、`eventhandler`、`ipc` 分支。Rust 約 2.7 萬行、Python 約 7.9k 行,23 個 open issue。

## 一句話

給**高頻交易和造市策略**用的回測框架。它把重點放在一般回測框架會忽略的三件事:掛單排在佇列第幾位、行情延遲、下單延遲,目標是讓同一段期間的回測結果接近實盤結果。

## 為什麼需要它

作者在 README 講得很直接:高頻的 edge 很小,所以回測不能太悲觀(把 edge 藏掉),也不能太樂觀(把 edge 放大)。順序應該是**先確認回測能重現實盤**,再談最佳化和過擬合。

一般 bar-based 回測假設「價格碰到就成交」,這對限價掛單的造市策略完全不成立:

- 你掛在 best bid,前面可能還排了 50 張,價格碰到也輪不到你
- 你看到的行情已經晚了幾毫秒,你送的單又要晚幾毫秒才到交易所
- 這兩段延遲加起來,決定你是不是被逆選擇(adverse selection)

## 架構

Cargo workspace 有五個 crate:

| crate | 用途 |
|-------|------|
| `hftbacktest` | 核心:回測引擎、訂單簿、模型、live bot |
| `hftbacktest-derive` | 產生 numpy dtype 的 derive macro |
| `py-hftbacktest` | PyO3 綁定,Python 端用 Numba `@njit` 寫策略 |
| `collector` | 錄行情:Binance(現貨、U 本位、幣本位)、Bybit、Hyperliquid |
| `connector` | 實盤連線:Binance Futures、Binance Spot、Bybit,透過 IPC(iceoryx2)讓多個 bot 共用一條連線 |

### 資料格式

所有行情都是同一個 64 bytes 的 `Event` struct,存成 `.npz`:

```rust
pub struct Event {
    pub ev: u64,        // 事件旗標:DEPTH / TRADE / SNAPSHOT / ADD_ORDER ... | BUY/SELL | EXCH/LOCAL
    pub exch_ts: i64,   // 交易所時間
    pub local_ts: i64,  // 本機收到時間
    pub px: f64,
    pub qty: f64,
    pub order_id: u64,  // 只有 L3 用
    pub ival: i64,
    pub fval: f64,
}
```

關鍵在**每筆事件都帶兩個時間戳**。`exch_ts - local_ts` 的差就是真實的行情延遲,所以回測不用另外假設行情延遲。`EXCH_EVENT` / `LOCAL_EVENT` 兩個旗標決定這筆事件要餵給交易所端模擬器還是策略端,同一筆資料可以只給其中一邊。

### 兩個處理器

回測時其實有兩個獨立的狀態機在跑:

- **exchange processor**(`proc/partialfillexchange.rs`、`nopartialfillexchange.rs`、L3 版本):用 `exch_ts` 推進,維護交易所視角的訂單簿和你的掛單,決定成交
- **local processor**(`proc/local.rs`):用 `local_ts` 推進,這是策略看到的世界

下單從 local 送出,經過「進場延遲」才到 exchange;回報再經過「回應延遲」回到 local。策略呼叫 `hbt.elapse(ns)` 推進時間,呼叫 `wait_order_response()` 等回報。

### 佇列位置模型(`models/queue.rs`)

L2 行情只知道每個價位的總量,不知道你前面有誰,所以要估:

- `RiskAdverseQueueModel`:最保守,只有成交量會讓你往前,撤單不會
- `ProbQueueModel`:價位總量減少時,用機率決定減少的量有多少來自你前面。機率是 `f(back) / (f(back) + f(front))`,`f` 可以選 `PowerProbQueueFunc`(`x^n`)、`LogProbQueueFunc`(`log(1+x)`)等幾種變形。核心更新:

  ```rust
  let est_front = front - (1.0 - prob) * chg + (back - prob * chg).min(0.0);
  ```

- `L3FIFOQueueModel`:有 L3(Market-By-Order)資料時,直接按 order id 排 FIFO,不用估

### 延遲模型(`models/latency.rs`)

- `ConstantLatency`:固定的進場 / 回應延遲
- `IntpOrderLatency`:用實際錄下來的 `(req_ts, exch_ts, resp_ts)` 內插。沒有自己的下單延遲紀錄時,作者建議用行情延遲推估,或做一個用成交量、事件數當特徵的回歸模型
- 負值代表交易所拒單,值是收到拒單通知的時間

另外有手續費模型(按成交金額、按數量、按筆、maker/taker 分開)和幾種訂單簿實作(BTreeMap、HashMap、只保留關注價格範圍的 `ROIVectorMarketDepth`,以及把不同頻率資料流合併的 `fuse`)。

## 怎麼用

Python 版(策略寫在 Numba `@njit` 裡):

```python
from hftbacktest import BacktestAsset, HashMapMarketDepthBacktest

asset = (
    BacktestAsset()
        .linear_asset(1.0)
        .data(['data/ethusdt_20221003.npz', ...])
        .initial_snapshot('data/ethusdt_20221002_eod.npz')
        .no_partial_fill_exchange()
        .intp_order_latency(['data/latency_20221003.npz', ...])
        .power_prob_queue_model(2.0)
        .tick_size(0.01)
        .lot_size(0.001)
)
hbt = HashMapMarketDepthBacktest([asset])
market_making_algo(hbt)   # @njit 函式,裡面 while hbt.elapse(...) == 0: 下單撤單
```

策略迴圈的典型寫法:每 10ms `elapse` 一次,算 reservation price(`mid + a*forecast - b*risk`)和半價差,撤掉不在新價位的掛單,掛新的 GTX(post-only)單,再 `wait_order_response`。

資料要自己準備:用 `collector` 錄,或把 Tardis.dev 之類的資料轉成 `.npz`(文件有 Data Preparation 教學)。社群贊助者在 <https://reach.stratosphere.capital/data/usdm/> 放了一些樣本資料。

**實盤只有 Rust 版**。Rust 策略寫成 `Bot` trait 的泛型函式,回測和實盤吃同一個 trait,換 backend 就能上線。Python 實盤還在 roadmap 上。

## 教學

文件裡的 notebook 是這個專案最有價值的部分之一,很多是在講造市理論本身:

- GLFT(Guéant–Lehalle–Fernandez-Tapia)造市模型和它簡化成網格交易的版本
- 用訂單簿不平衡、basis、APT 當 alpha 的造市
- 延遲對績效的影響、怎麼取得下單延遲資料
- 大 tick 資產的佇列型造市、極端行情的價格保護、L3 回測、多市場造市

## 值得注意的地方

1. **它在解的問題是「回測跟實盤對不對得上」,跟回測速度無關**。雙時間戳事件、兩個處理器、可換的佇列與延遲模型,都是為了這件事。如果你的策略是吃單或日頻,這些成本換不到什麼,用一般向量化回測就好
2. **佇列模型是估計,不是真相**。L2 資料下前面排多少只能用機率猜,`PowerProbQueueFunc` 的 `n` 要拿實盤成交去校準。作者自己也建議先拿實盤的那段期間回測,對照結果
3. **資料門檻高**。要逐筆 L2 深度 + 成交,最好還有自己的下單延遲紀錄;一天的幣安 U 本位單一合約就很大。這不是拿 Yahoo Finance 日 K 就能玩的東西
4. **主要針對加密貨幣**。collector / connector 只有 Binance、Bybit、Hyperliquid,examples 也全是幣圈交易所;股票或期貨要自己轉資料
5. **維護狀態要留意**。2025-12 之後 master 沒有新 commit,roadmap 上 OKX、Hyperliquid 實盤、Parquet 支援都還沒做。核心已經穩定,但遇到問題可能要自己修
6. 社群已經有衍生專案,例如 `mirkovicdev/HFTENGINE`(終端機重播 console,顯示每張掛單的佇列位置)、`mileswangs/pm-hftbacktest`(Polymarket 版)

## 跟其他筆記的關係

- [Execution Delay on Kelly Trading](execution-delay-kelly-trading.md) 從理論面討論執行延遲對下注策略的影響,hftbacktest 是在毫秒尺度把延遲實際模擬出來
- [pmxt](pmxt.md)、[Prediction Market Analysis](prediction-market-analysis.md) 跟 Polymarket 版的衍生專案可以對照看
- 跟 [Vibe-Trading](vibe-trading.md)、[QuantDinger](quantdinger.md) 這類 bar-based、偏 AI agent 的交易平台是完全不同層級的工具
