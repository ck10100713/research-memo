---
date: "2026-06-12"
category: "AI 應用"
card_icon: "material-message-processing-outline"
oneliner: "用 decorator 註冊指令、Redis 存對話狀態的早期 LINE chatbot Python boilerplate（Wit.ai NLU、Yeoman 產生器）"
tags:
  - chatbot
  - automation
  - system-design
---

# LINE Chatbot Boilerplate 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub repo | <https://github.com/mgilangjanuar/line-chatbot-boilerplate> |
| Yeoman 產生器 (npm) | `generator-line-chatbot-boilerplate`（jsDelivr CDN v1.0.2） |
| 作者 | M Gilang Januar（LINE API Expert，印尼） — <https://developers.line.biz/en/community/api-experts/id-m-gilang-januar/> |
| LINE Messaging API 文件 | <https://developers.line.me/en/docs/messaging-api/reference/> |
| LINE SDK for Python | <https://github.com/line/line-bot-sdk-python> |

> Repo 統計：⭐ 50、Python、MIT License、無 topics。屬作者早期作品（依賴 Python 3.5 / MongoDB 2.6 / Redis 4.0 / Wit.ai），技術棧偏舊，研究價值主要在**架構設計模式**而非可直接上線使用。

## 專案概述

`line-chatbot-boilerplate` 是一套用 **Python** 寫的 LINE 聊天機器人專案範本（boilerplate），透過 **Yeoman 產生器**（`yo line-chatbot-boilerplate`）一鍵 scaffold 出專案骨架。它在 LINE 官方的 `line-bot-sdk-python` 之上，疊了一層自訂的 **client / 路由 / 狀態管理框架**，把「收到 webhook 事件 → 解析指令 → 分派到對應 handler → 回覆訊息」這條流程抽象成 decorator 寫法。

它要解決的問題是：原生 LINE SDK 只給你 webhook handler 與訊息 model，**指令怎麼分派、多輪對話的狀態怎麼存、自然語言意圖怎麼接 NLU**，全都要自己寫。這個 boilerplate 把這三件事都模板化了：

- **指令分派** → 用 `@client.on_command(...)` decorator 註冊
- **多輪對話狀態** → 用 Redis 存 per-user/room/group 的 state + data
- **NLU 意圖** → 整合 **Wit.ai**，用 entity 觸發 handler

適合的場景：想用 Python 快速做一個「指令式 + 簡單多輪對話」的 LINE bot，且願意接受 MongoDB + Redis 的基礎設施。

## 核心架構

```
LINE Platform ──webhook──▶ index.py (ChatbotHandler)
                               │
                   register.py │  load_clients() 註冊各 client 對應的事件/訊息類型
                               ▼
                        ┌─────────────────┐
                        │  modules/*.py   │  每個檔案是一個 client 物件
                        │  (你的業務邏輯)  │
                        └─────────────────┘
                               │  decorator 路由
              ┌────────────────┼────────────────────┐
              ▼                ▼                     ▼
        on_command()      on_state()           Wit.ai entity
       (指令觸發)        (多輪狀態觸發)         (NLU 意圖觸發)
              │                │
              ▼                ▼
         MongoDB           Redis (state/data)
        (資料持久化)       (對話狀態機)
```

### 四種 Client 類型

| Client | 觸發方式 | 典型用途 |
|--------|---------|---------|
| `StandardClient` | 任何訊息都觸發（單一 `on_command`） | 全攔截型（如 echo、log） |
| `TextClient` | 文字指令 `/xxx` 觸發 | 指令式 bot 主力 |
| `SimpleWitClient` | Wit.ai entity 為某值時觸發，handler 收 `value` | 輕量 NLU |
| `AdvancedWitClient` | Wit.ai entity = 指定值時觸發 | 精確意圖比對 |

### 兩種路由 decorator

```python
# 1) on_command — 指令觸發，可收參數
@client.on_command('echo')
def action_echo(args):                    # method 必須以 action_ 為前綴
    client.bot.reply_message(client.event.reply_token,
                             TextSendMessage(text=args))

# 2) on_state — 狀態機，多輪對話
@client.on_command('echo')
def action_echo():
    client.state.set_state('echo/input')  # 設定狀態 → 存進 Redis
    client.state.set_data('...')
    client.bot.reply_message(..., TextSendMessage(text='Please input your string'))

@client.on_state('echo/input')            # 使用者下一句話會進到這裡
def action_echo_input():
    message = client.event.message.text
    if message == '/end':
        client.state.delete_state()       # 清狀態 → 離開對話
    else:
        client.bot.reply_message(..., TextSendMessage(text=message))
```

### 註冊 client（register.py）

```python
def load_clients(client_handler):
    client_handler.add(ping.client, [
        EventEntity(MessageEvent, message=TextMessage),
        EventEntity(MessageEvent, message=StickerMessage)
    ])
    return client_handler
```

`EventEntity` 把「哪種事件 + 哪種訊息類型」綁到哪個 client，等於是一張**事件分派表**。

## 快速開始

```bash
# 1) 裝 Yeoman 與產生器
npm install -g yo
npm install -g generator-line-chatbot-boilerplate

# 2) scaffold 專案
yo line-chatbot-boilerplate
```

依賴環境：Python 3.5、Redis 4.0.8、MongoDB 2.6.10、LINE@ Messaging API channel、Wit.ai token（選用）。設定 MongoDB / Redis 連線與 bot handler 在 `index.py`，業務邏輯放 `modules/`，事件分派寫在 `register.py`。

`/` 指令前綴與 `action_` method 前綴都可在 `lib/client.py` 改。

## 目前限制 / 注意事項

- **技術棧過舊**：Python 3.5（已 EOL）、MongoDB 2.6（2014）、Redis 4.0、Wit.ai。直接拿來新專案不切實際，需大幅升級。
- **重基礎設施**：同時要 MongoDB + Redis，對「只想做小 bot」的人偏重。現代等價需求多半用單一 SQLite/Postgres 或雲端 KV 就夠。
- **Wit.ai 依賴**：Facebook 的 Wit.ai 政策與可用性多年來反覆，NLU 路線的長期穩定性存疑；現在多半改用 LLM 做意圖理解。
- **社群小**：50 stars、更新停滯，幾乎沒有外部評測或教學文章，遇到問題只能讀原始碼。
- **無多模態 / LLM**：純指令 + 規則式 NLU，沒有 GPT/Claude 類的生成式對話能力。

## 研究價值與啟示

### 關鍵洞察

1. **Decorator 路由是 chatbot 框架的常見抽象，但要小心「魔法字串」契約。** `action_` method 前綴、`echo/input` 的斜線狀態命名，都是靠**字串約定**把 method 名稱、狀態、指令串起來。這種設計上手快，但重構脆弱（改名字會默默失效）、IDE 無法靜態檢查。現代框架（如 FastAPI 的 router、aiogram）多改用顯式註冊或型別標註來換取可維護性。

2. **「狀態機存在 Redis」是多輪對話的經典解法，本質是把對話建模成 FSM。** `set_state / on_state / delete_state` 三件套，等於手寫一個 per-user 的有限狀態機。這個模式至今仍是對話流程控制的主流（LangGraph 的 state、Rasa 的 slot/form 都是同一思路的演化版）——差別只在於現在多了 LLM 來決定狀態轉移，而非寫死指令。

3. **它把「框架 / 業務邏輯 / 分派表」三層硬切開，是好的關注點分離。** `lib/`（框架）、`modules/`（你的 client）、`register.py`（事件→client 對應），這種分層讓新增功能只需動 `modules/` + `register.py`，框架碼不動。這正是現代 agent 框架（Runtime → Orchestration → Worker → Tools 分層，見 [開源 Agent 框架比較](open-source-agent-frameworks.md)）想達到的同一件事，只是年代更早、更樸素。

4. **Yeoman 產生器 = 那個時代的「create-app」。** 用 `yo xxx` scaffold 專案，是 2015～2018 年前端/全端的主流 DX。如今被 `npm create`、`degit`、`cookiecutter`、以及 AI Agent 直接生成取代。研究這個 repo 像看一份「pre-LLM 時代的 chatbot 工程考古」。

5. **NLU 從「entity 規則」走到「LLM 意圖」的分水嶺，這個 repo 剛好站在前一側。** `SimpleWitClient` / `AdvancedWitClient` 用 entity 值硬比對觸發 handler，是規則式 NLU 的代表。對照 [LINE Bot Multimodal RAG](linebot-multimodal-rag.md) 用 LLM + RAG 直接理解任意輸入，可清楚看到 chatbot 意圖理解的典範轉移。

### 與其他專案的關聯

| 專案 | 關聯 |
|------|------|
| [LINE Bot Multimodal RAG (kkdai)](linebot-multimodal-rag.md) | 同為 LINE bot，但走 LLM + RAG 的生成式路線，與本 repo 的指令 + 規則式 NLU 形成「前 LLM vs 後 LLM」對照 |
| [AI Avatar Bot (Live2D 虛擬人)](ai-avatar-bot.md) | 同屬「AI 應用」聊天介面，展示 chatbot 從文字指令 → 語音/虛擬人的互動演化 |
| [開源 Agent 框架比較](open-source-agent-frameworks.md) | 本 repo 的 client/state/router 三件套，可視為現代 agent 框架「節點 + 狀態 + 路由 + 分層解耦」的原始雛形 |
