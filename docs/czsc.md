---
date: "2026-09-15"
category: "量化交易"
card_icon: "material-chart-timeline-variant"
oneliner: "纏中說禪（纏論）技術分析工具，6.2K★、2019 年至今維護六年。1.0 版把分型／筆／中樞等纏論核心演算法全部改用 Rust 重寫，透過 PyO3 以 czsc._native 暴露給 Python，底層 9 個 crate、220+ 個信號函數。定義了「信號—事件—交易」三層邏輯體系，把中文技術分析理論做成可回測的工程系統"
tags:
  - quant
  - taiwan
---

# CZSC（纏中說禪技術分析工具）研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo（★6,221 / 1,739 forks） | <https://github.com/waditu/czsc> |
| PyPI | <https://pypi.org/project/czsc/> |
| 專案文件（飛書 wiki） | [CZSC 1.0.X 使用說明和案例](https://s0cqcxuy3p.feishu.cn/wiki/X0mAwSZyqiuebek2EUacbyPMnDd) |
| DeepWiki 架構分析 | <https://deepwiki.com/waditu/czsc/1-overview> |
| 理論來源 | [纏中說禪博客備份](https://chzhshch.blog)（原新浪博客內容不完整且無評論，這是網友整理的備份） |
| 舊 Python 實作（0.9.X） | [v0.9.69 tag](https://github.com/waditu/czsc/tree/v0.9.69) |

> **Metadata（2026-09-15 抓取）**：**6,221 stars / 1,739 forks / 11 open issues / 160 subscribers** · 主語言 **Rust** · 建立於 **2019-06-11**、最後 push **2026-09-02** · topics：`czsc` / `quant` / `tushare` · License 標為 Other（非標準授權，商用前請自行確認）。

## 先說清楚「纏論」是什麼

**纏中說禪**是 2006–2008 年在新浪博客寫作的一位中文作者（本名李彪，2008 年過世），他的技術分析體系被中文量化圈簡稱「纏論」。核心是用**分型 → 筆 → 線段 → 中樞**這套遞歸結構去描述 K 線走勢，再做多級別聯立判斷。

在中文投資圈這套理論的爭議很大：支持者認為它給了走勢一個嚴謹的形式化定義，質疑者認為它的判讀高度依賴人為解讀。**CZSC 這個專案的價值，正好落在這個爭議點上——它把一套原本靠人讀圖的理論，變成了可以程式化、可回測、可統計驗證的東西。** 演算法能不能賺錢是一回事；把模糊理論做成確定性程式碼，本身就是有意義的工程。

## 1.0 版最大的變化：核心演算法整包搬到 Rust

這是這個專案現在最值得看的地方。

> **1.0.X 版本開始，纏論核心演算法（分型、筆、中樞等）已全部遷移到 Rust 實作，透過 PyO3 擴展（`czsc._native`）暴露給 Python。**

架構長這樣：

```
czsc (Python 套件)
├── czsc._native          ← Rust 擴展（PyO3），纏論核心
│   ├── CZSC / FX / BI / ZS / RawBar / NewBar / BarGenerator
│   ├── Freq / Mark / Direction / Signal / Event / Position / Operate
│   ├── CzscTrader / CzscSignals / generate_czsc_signals
│   ├── signals.*         ← 220+ 信號函數
│   └── ta.*              ← Rust TA 算子（ema/sma/boll…）
├── czsc.traders          ← Python 門面，匯聚 Rust 交易 API
├── czsc.utils            ← 繪圖／快取／統計／交易工具
├── czsc.connectors       ← 資料源連接器（天勤／Tushare／CCXT／本地快取）
├── czsc.strategies       ← 策略門面
├── czsc.fsa              ← 飛書自動化工具
└── czsc.envs             ← 環境變數管理
```

底層 Rust workspace 有 **9 個 crate**：`czsc` / `czsc-core` / `czsc-derive` / `czsc-signals` / `czsc-trader` / `czsc-utils` / `czsc-ta` / `czsc-signal-macros` / `czsc-python`（PyO3 綁定入口）。

> **為什麼這件事值得注意**：纏論的分型與筆識別是**逐根 K 線的遞歸狀態機**，在 Python 裡跑多品種多級別會很慢。搬到 Rust 之後，多級別聯立與大批量回測才變得可行。這是「**中文量化圈少見的、把 Python 效能瓶頸真的用 Rust 解掉**」的案例，不是拿 Rust 當招牌。
>
> 代價也很直接：**安裝從純 Python 變成需要預編譯 wheel，自己從源碼建置要裝 Rust 工具鏈 + maturin**，而且 `pyo3` 0.22 要求 **Python ≥ 3.10**。系統預設 Python 低於 3.10 時要自己 `export PYO3_PYTHON=$(which python3.12)`，否則 `cargo build` 會在 `crates/czsc-python/build.rs` 提前 panic。

## 核心設計：信號—事件—交易 三層

這是這個專案除了纏論之外，**最可以獨立帶走的架構**：

| 層 | 做什麼 |
|----|--------|
| **信號（Signal）** | 220+ 個信號函數，每個回傳一個結構化的信號值。命名帶版本號（如 `cxt_bi_status_V230101`）——**信號函數一旦發布就不改語意，要改就發新版本**，這樣歷史回測結果才可重現 |
| **事件（Event）** | 用 `signals_all` / `signals_any` / `signals_not` 對信號做邏輯組合，組出交易事件 |
| **交易（Position / Operate）** | 事件觸發倉位操作；`CzscTrader` 做多級別聯立決策 |

信號函數帶版本號這個約定值得特別點名——**它把「策略回測不可重現」這個量化研究的老問題，用命名規範直接解掉了**。

## 快速開始

```python
import czsc
from czsc import CZSC, Freq, format_standard_kline
from czsc.mock import generate_symbol_kines

df = generate_symbol_kines('000001', '30分钟', '20240101', '20240601')
bars = format_standard_kline(df, freq=Freq.F30)

czsc_obj = CZSC(bars)          # 自動識別分型、筆、中樞
print(f"筆數量：{len(czsc_obj.bi_list)}")
print(f"中樞數量：{len(czsc_obj.zs_list)}")
```

多級別合成、信號生成、權重回測：

```python
from czsc import BarGenerator, generate_czsc_signals, WeightBacktest

bg = BarGenerator(base_freq='1分钟', freqs=['5分钟', '30分钟', '日线'])
for bar in raw_bars:
    bg.update(bar)

signals_seq = [
    "czsc._native.signals.bar.bar_end_V230331",
    "czsc._native.signals.cxt.cxt_bi_status_V230101",
]
results = generate_czsc_signals(bars, signals_seq)

wb = WeightBacktest(dfw, fee_rate=0.0002)
print(wb.stats)
```

視覺化用 plotly + lightweight-charts，**產出自包含的離線 HTML**（分型／筆／線段／中樞畫在 K 線上），方便分享與嵌入。

安裝：`pip install czsc -U`（Python ≥ 3.10）。

## 目前限制 / 注意事項

- **授權不是標準開源授權**（GitHub 標 Other / NOASSERTION）。商用前務必自己確認 LICENSE 內容。
- **README 頂端掛著商業產品推廣**（「勝可知」大模型量化策略研究平台，附邀請碼與 500 元額度）。專案本身是開源的，但要知道它現在有商業產品在上面。
- **文件主要在飛書 wiki**，不是 GitHub。這對牆外使用者的可及性是個問題，而且飛書連結的長期穩定性不如 repo 內文件。
- **理論本身有爭議**。纏論在中文投資圈的評價兩極；這個專案提供的是**工程實現與驗證工具**，不是「纏論有效」的證明。想驗證有沒有效，就用它的 `WeightBacktest` 自己跑。
- **主要面向 A 股 / 中國期貨**（連接器是天勤、Tushare），台股要自己接資料源。
- 信號函數數量在 README 不同段落寫 220+ 和 246，**以實際 `czsc._native.signals` 為準**。

## 研究價值與啟示

### 關鍵洞察

1. **「把模糊理論做成確定性程式碼」本身就是一種研究貢獻**。纏論的分型、筆、中樞原本是靠人讀圖判斷的東西，CZSC 給了它一個**唯一確定的演算法定義**。結果是：你終於可以問「這套理論到底有沒有統計優勢」——而在有程式碼之前，這個問題連問都問不清楚。

2. **信號函數帶版本號（`cxt_bi_status_V230101`）是可以直接抄走的約定**。發布後不改語意、要改就發新版本——**回測可重現性的問題，用一條命名規範就解掉一大半**。任何做策略庫的人都該照抄。

3. **Rust + PyO3 是 Python 量化效能瓶頸的務實解法**。CZSC 沒有整包重寫成 Rust 服務，而是**只把熱路徑（遞歸狀態機）搬過去，Python 端保留門面**。這個切法保住了 Python 生態的易用性，又拿到了 Rust 的速度。代價是安裝複雜度上升——**值不值得，取決於你的熱路徑是不是真的在那裡**。

4. **六年維護（2019 → 2026）在量化開源專案裡很稀有**。大多數量化 repo 活不過一次牛熊。這個專案能活下來，跟它有明確的理論根基（不是東拼西湊的指標集合）、有社群（飛書群、B 站教程）、後來還長出商業產品，都有關係。

### 與其他專案的關聯

| 對照 | 關係 |
|------|------|
| [Vibe-Trading](vibe-trading.md) | 同為中文量化工程專案；Vibe-Trading 是 LLM agent 工作台，CZSC 是**確定性的技術分析引擎**。兩者其實互補——CZSC 可以當 agent 的一個工具 |
| [反詐投資王](anti-gambling-trader-tw.md) | 兩端對照：CZSC 給你**更精細的進出場判斷**，反詐投資王問你**這些判斷到底有沒有統計優勢**。先用後者驗證前者，順序才對 |
| [StockAgent](stockagent.md) / [TradingAgents](tradingagents.md) | 那些是 LLM 多 agent 做決策，CZSC 是**規則明確的形式化系統**——兩種完全不同的建模哲學 |
| [awesome-data](awesome-data.md) | CZSC 的 connector 接的就是 Tushare 那一類資料源 |
