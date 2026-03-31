---
date: "2026-03-31"
category: "AI 應用"
card_icon: "material-airplane-search"
oneliner: "Google 旗下最強機票研究引擎——Routing Code + Extension Code + 日曆比價 + Open Jaw，Skyscanner 做不到的進階查詢全靠它"
---
# ITA Matrix 機票搜尋引擎 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| 官方網站 | [matrix.itasoftware.com](https://matrix.itasoftware.com/) |
| 進階指南 (Upgraded Points) | [Matrix ITA Advanced Guide](https://upgradedpoints.com/travel/matrix-ita-finding-cheap-airfare/) |
| Routing Code 教學 (Travel Codex) | [ITA Matrix Routing Guide](https://www.travelcodex.com/advanced-routing-language-in-ita/) |
| Google 官方 Routing Code 說明 | [Google Support](https://support.google.com/faqs/answer/2736497?hl=en) |
| Extension Code 速查表 (GitHub) | [flightgold/itamatrix-codes](https://github.com/flightgold/itamatrix-codes) |
| Prince of Travel 教學 | [How to Use ITA Matrix Like a Pro](https://princeoftravel.com/guides/how-to-use-ita-matrix-like-a-pro/) |
| BookWithMatrix 訂票橋接 | [bookwithmatrix.com](https://bookwithmatrix.com/) |
| 中文教學 (TripPlus) | [如何使用 ITA Matrix](https://blog.tripplus.cc/zh/85653/brady-newbie-how-to-use-ita-matrix) |
| 中文教學 (TravelWithHans) | [ITA Matrix 教學](https://travelwithhans.com/%E6%A9%9F%E7%A5%A8-ita-matrix-%E6%95%99%E5%AD%B8/) |
| 中文教學 (PY 旅行大小事) | [ITA 常用指令及查票技巧](https://www.ustatz.com/?p=3737) |
| NerdWallet 指南 | [ITA Matrix: When to Use It](https://www.nerdwallet.com/travel/learn/how-to-use-ita-matrix) |

## 工具概述

ITA Matrix 是 **Google 旗下的機票研究引擎**（前身為 MIT 科學家於 1996 年創建的 ITA Software），2010 年被 Google 收購後成為 Google Flights 的底層引擎，同時也驅動 Kayak、Orbitz 等主流 OTA 的搜尋功能。

### 核心定位：研究工具，非訂票平台

| 特性 | 說明 |
|------|------|
| 功能 | 純搜尋 + 票價分析，**不能直接訂票** |
| 優勢 | 業界最強的進階搜尋語法（Routing Code + Extension Code） |
| 劣勢 | 介面老舊、需透過第三方工具訂票、學習曲線高 |
| 費用 | 完全免費 |
| 與 Google Flights 的關係 | Google Flights 是 ITA Matrix 的簡化版前端 |

## 為什麼要用 ITA Matrix？（vs Skyscanner / Google Flights）

```
搜尋深度：  ITA Matrix >>>>> Google Flights > Skyscanner
易用性：    Skyscanner > Google Flights >>>>> ITA Matrix
航空覆蓋：  Skyscanner（含廉航）> ITA Matrix（傳統航空為主）
訂票：      Skyscanner ✅  Google Flights ✅  ITA Matrix ❌（需橋接）
```

### ITA Matrix 的獨家能力

| 能力 | Skyscanner | Google Flights | ITA Matrix |
|------|:---:|:---:|:---:|
| 指定艙等代碼 (Fare Class) | ❌ | ❌ | ✅ |
| 指定轉機點 / 排除轉機點 | ❌ | 有限 | ✅（精確控制） |
| 指定航空聯盟 | ❌ | ❌ | ✅ |
| 排除 Codeshare 航班 | ❌ | ❌ | ✅ |
| 設定最長轉機時間 | ❌ | ❌ | ✅ |
| 強制 Overnight Stopover | ❌ | ❌ | ✅ |
| 查看完整票價結構 (Fare Construction) | ❌ | ❌ | ✅ |
| 查看票價規則 (Fare Rules) | ❌ | 部分 | ✅（完整） |
| 切換銷售城市 (Sale City) | ❌ | ❌ | ✅ |
| 切換計價貨幣 | ❌ | ✅ | ✅ |

## 核心功能拆解

### 1. Routing Code（路由代碼）

控制航線路由的核心語法，填入搜尋頁的「Routing Codes」欄位。

| 語法 | 意義 | 範例 |
|------|------|------|
| `XX`（航空代碼） | 只搜該航空 | `BR` → 只看長榮 |
| `C:XX` | 指定行銷航空 (Marketing Carrier) | `C:BR` |
| `O:XX` | 指定實際執飛航空 (Operating Carrier) | `O:BR` |
| `XXX`（機場代碼） | 指定轉機點 | `NRT` → 必須經東京成田 |
| `~XXX` | 排除轉機點 | `~ICN` → 不經首爾仁川 |
| `XX,YY` | 逗號 = OR 邏輯 | `BR,SQ` → 長榮或星航 |
| `XX YY` | 空格 = 航段連接 | `BR NRT SQ` → 長榮飛到 NRT，再搭星航 |
| `/f XX` | 指定航空聯盟 | `/f *A` → 星空聯盟 |
| `123` | 指定航班號 | `BR 31` → 長榮 BR31 |

### 2. Extension Code（擴展代碼）

填入「Advanced controls」的 Extension Code 欄位，提供更精細的過濾。

| 語法 | 意義 | 範例 |
|------|------|------|
| `MAXSTOPS N` | 最多 N 次轉機 | `MAXSTOPS 1` |
| `MAXDUR H:MM` | 最長旅行時間 | `MAXDUR 18:00` |
| `MINCONNECT H:MM` | 最短轉機時間 | `MINCONNECT 2:00` |
| `MAXCONNECT H:MM` | 最長轉機時間 | `MAXCONNECT 4:00` |
| `MINCONNECT 20:00` | 強制 Overnight Stopover | 轉機時間 ≥ 20 小時 |
| `MINMILES N` | 最少里程 | `MINMILES 5000`（Mileage Run 用） |
| `-CODESHARE` | 排除共掛航班 | 確保里程累積正確 |
| `-REDEYES` | 排除紅眼航班 | 避開半夜出發 |
| `f bc=X` | 指定 Fare Class | `f bc=V\|bc=W` → 只看 V 或 W 艙 |

### 3. 日曆比價（Calendar of Lowest Fares）

- 勾選 **「See calendar of lowest fares」** 可查看出發日起 **30 天內的每日最低票價**
- 支援設定回程天數（如 5~7 晚），自動組合最便宜的去回日期
- 支援 ±1 天 / ±2 天的彈性日期搜尋

### 4. Multi-City / Open Jaw 搜尋

- 支援多段行程（最多 6 段）
- **Open Jaw**：去程 A→B，回程 C→A（中間自行移動）
- Open Jaw 經常比兩張單程便宜，且可與 Routing Code 搭配

### 5. Sale City（銷售城市）

- 切換票價的「銷售地」可能顯示不同價格
- 例：同一張機票，從台北出票 vs 從曼谷出票，價格可能差很大
- 在 Advanced controls 中設定

## 實戰指令範例

### 場景 1：台北→歐洲，只搭長榮或星空聯盟，經東京轉機

```
出發：TPE    目的地：CDG（巴黎）
Routing Code：/f *A NRT
Extension Code：MAXSTOPS 1
```

### 場景 2：搜尋華航（Skyscanner 搜不到的航空）

```
出發：TPE    目的地：AMS（阿姆斯特丹）
Routing Code：CI
→ ITA Matrix 可以搜到華航，解決 Skyscanner 搜不到的問題
```

### 場景 3：Open Jaw — 東京進大阪出

```
Multi-city 模式：
  段 1：TPE → NRT（東京成田）
  段 2：KIX（大阪關西）→ TPE
→ 通常比兩張來回票便宜
```

### 場景 4：強制 Overnight Stopover（免費多玩一站）

```
出發：TPE    目的地：LHR（倫敦）
Routing Code：HKG（香港轉機）
Extension Code：MINCONNECT 20:00
→ 在香港強制停留一晚，相當於免費多一個目的地
```

### 場景 5：Fare Class 搜尋（累積里程最大化）

```
出發：TPE    目的地：SIN（新加坡）
Routing Code：BR
Extension Code：f bc=Y|bc=B|bc=M
→ 只搜 Y/B/M 艙，這些艙等通常累積 100% 里程
```

### 場景 6：排除紅眼 + 限制旅行時間

```
Extension Code：-REDEYES MAXDUR 15:00 -CODESHARE
→ 無紅眼、總時長 ≤ 15 小時、無共掛航班
```

## 訂票流程（ITA Matrix → 實際購買）

ITA Matrix 不能直接買票，需要橋接到實際購票管道：

```
┌─────────────┐     找到理想航班     ┌──────────────────┐
│  ITA Matrix  │ ──────────────────→ │  訂票方式選擇     │
│  (搜尋研究)   │                     │                  │
└─────────────┘                     ├──────────────────┤
                                    │ 1. BookWithMatrix │ → 自動帶入 OTA
                                    │ 2. 航空官網手動搜  │ → 用 ITA 找到的日期/航班號
                                    │ 3. 電話訂票       │ → 報 Fare Code 給客服
                                    └──────────────────┘
```

### BookWithMatrix 使用方式

1. 在 ITA Matrix 搜尋結果頁，點選 **「Copy itinerary as JSON」**
2. 到 [bookwithmatrix.com](https://bookwithmatrix.com/) 貼上 JSON
3. 選擇 OTA（支援 Priceline、JustFly、Flight Network、AA、Delta、Alaska）
4. 跳轉到 OTA 完成訂票

也可安裝 **BookWithMatrix 瀏覽器擴充套件**，在 ITA Matrix 結果頁直接一鍵跳轉。

## 對照截圖中的「還沒做到」清單

回到圖片中提到的待辦項目，ITA Matrix 可以解決哪些：

| 待辦項目 | ITA Matrix 能否解決 | 怎麼做 |
|---------|:---:|------|
| 華航搜尋（Skyscanner 搜不到） | ✅ | Routing Code 輸入 `CI` 即可搜尋華航 |
| 價格監控 / Alert | ❌ | ITA Matrix 無此功能，需搭配 Google Flights Price Alert |
| 自動偵測票價效期（3/6 個月限制） | ⚠️ 部分 | 可查看完整 Fare Rules 了解票價有效期，但無自動偵測 |

### 額外可強化的已有能力

| 已做到的項目 | ITA Matrix 加值 |
|------------|----------------|
| 艙等敏感日期微調 | 日曆比價 + `f bc=X` 指定艙等，更精確找低價艙 |
| 中停次數/停留費 | `MINCONNECT` / `MAXCONNECT` 精確控制，可看 Fare Rules 中的 Stopover 條款 |
| Open Jaw（東京進大阪出） | Multi-city 模式原生支援，比 Skyscanner 更彈性 |
| 多航空比較（長榮 vs 星宇） | `BR,JX` 一次搜兩家，或分別搜再比票價結構 |
| 頭尾城市矩陣搜尋 | 多組搜尋 + Sale City 切換，可能發現更多價差 |

## 使用限制與注意事項

| 限制 | 說明 |
|------|------|
| 不含廉航 | 虎航、樂桃、亞航等廉航搜不到，需用 Skyscanner 補 |
| 不能訂票 | 純研究工具，需橋接 BookWithMatrix 或手動到官網 |
| 無價格追蹤 | 無法設定降價通知，需搭配 Google Flights |
| 無行李/餐食資訊 | 只顯示航班和票價，不含附加服務 |
| 介面不友善 | 老舊 UI，學習曲線高 |
| 一次最多 6 段 | Multi-city 最多 6 段航程 |

## 建議搜尋策略組合

```
最佳實踐工作流：

1. Skyscanner → 廣泛掃描（含廉航），找大方向
2. Google Flights → 視覺化日曆比價 + 設定 Price Alert
3. ITA Matrix → 進階搜尋：
   - 指定航空 / 艙等 / 轉機點
   - Open Jaw / Stopover 組合
   - 查看完整 Fare Rules
   - 搜尋 Skyscanner 找不到的航空（如華航）
4. BookWithMatrix → 橋接 ITA 結果到 OTA 訂票
5. 航空官網 → 最終確認價格 + 完成購買
```

## 關鍵結論

1. **ITA Matrix 是 Skyscanner 的完美互補**：Skyscanner 覆蓋廉航但缺乏進階控制，ITA Matrix 提供專業級搜尋語法
2. **華航問題直接解決**：`CI` routing code 即可搜尋華航航班
3. **價格監控仍需 Google Flights**：ITA Matrix 無此功能
4. **Open Jaw + Stopover 是最大省錢利器**：Multi-city + `MINCONNECT` 組合可創造免費多玩一站的行程
5. **Fare Class 搜尋對里程玩家極有價值**：精確控制艙等 = 精確控制里程累積比例
