---
date: "2026-04-20"
category: "Coding Agent 工具"
card_icon: "material-account-voice"
oneliner: "数字生命卡兹克開源個人 AI 方法論 — 14 天 5.4K stars，1 個 Prompt + 2 個 Skill 把寫作風格與研究框架蒸餾成可執行指令集"
---

# khazix-skills 研究筆記

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) |
| README | [README.md](https://github.com/KKKKhazix/khazix-skills/blob/main/README.md) |
| 內部協作說明 | [CLAUDE.md](https://github.com/KKKKhazix/khazix-skills/blob/main/CLAUDE.md) |
| 橫縱分析法 SKILL | [hv-analysis/SKILL.md](https://github.com/KKKKhazix/khazix-skills/blob/main/hv-analysis/SKILL.md) |
| 寫作風格 SKILL | [khazix-writer/SKILL.md](https://github.com/KKKKhazix/khazix-skills/blob/main/khazix-writer/SKILL.md) |
| 橫縱分析法公眾號文 | [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Y_uRMYBmdLWUPnz_ac7jWA) |
| 寫作風格公眾號文 | [mp.weixin.qq.com](https://mp.weixin.qq.com/s/AtxGrii_K-nzkwUM9SNhEg) |
| 開放標準 | [agentskills.io](https://agentskills.io) |

**作者：** 數字生命卡茲克（Khazix）— AI 行業深耕三年的中文公眾號創作者、創業者，slogan「永遠對世界保持好奇」

**專案狀態：** ⭐ 5,414 stars · 906 forks · Python · MIT · 2026-04-06 創建（**14 天衝到 5K+ stars**）

## 專案概述

khazix-skills 是卡茲克把自己**長期使用的個人方法論「一字不改」開源**的成果。倉庫只放 3 個東西——1 個 Prompt（橫縱分析法）+ 2 個 Skill（hv-analysis、khazix-writer），卻在 2 週內衝到 5.4K stars。

它的價值不在於工具本身有多複雜，而在於把一個高影響力中文 AI KOL 的「思考框架」與「寫作風格」蒸餾成可被任何 Agent 直接 load 的結構化指令。Prompt 是輕量級複製貼上即用，Skill 則遵循 [agentskills.io](https://agentskills.io) 開放標準，由 Claude Code、OpenClaw、Codex 等 Agent 自動載入。

CLAUDE.md 揭露了一個關鍵架構：作者把工作流分成 `skill-build/`（私有開發評估區）和 `github-share/`（公開鏡像區）兩層，**新 Skill 必須在 skill-build 評估穩定後才複製到開源倉庫**——這是把「個人方法論產品化」的工程紀律。

## 倉庫結構

```
khazix-skills/
├── prompts/
│   └── 橫縱分析法.md           # 7KB，純 Prompt，貼進任何 Deep Research 模型即用
├── hv-analysis/                 # 橫縱分析法 Skill（自動聯網 + PDF 輸出）
│   ├── SKILL.md                # 19.7KB，方法論本體
│   ├── scripts/                # md_to_pdf.py（WeasyPrint）
│   └── references/             # 風格指南
├── khazix-writer/               # 個人寫作風格 Skill
│   ├── SKILL.md                # 30.2KB，最厚的一份
│   └── references/             # 風格示例庫
├── README.md                    # 中文，2KB
└── CLAUDE.md                    # 內部協作規則（外人也能看到）
```

## 兩個 Skill 解析

### 1. hv-analysis（橫縱分析法）

| 維度 | 內容 |
|------|------|
| **方法論來源** | 索緒爾歷時-共時分析（語言學）+ 社科縱向-橫截面研究設計 + 商學院案例研究法 + 競爭戰略分析 |
| **核心結構** | 縱軸追時間深度 + 橫軸追同期廣度 + 兩軸交匯出洞察 |
| **產出** | 排版精美的 PDF 研究報告（封面 + 目錄 + 章節 + 來源），全文 10K-30K 字 |
| **技術實作** | 子 Agent 並行搜尋（縱向 / 橫向 / 補充三組），WebSearch + WebFetch + arXiv API 聯網，WeasyPrint 渲染 PDF |
| **競品場景處理** | A 無競品 / B 1-2 個 / C 3+ 個——**根據場景動態切換寫法**，不是寫死的模板 |

縱向分析硬性要求 6,000-15,000 字，橫向 3,000-10,000 字，交匯總結 1,500-3,000 字。Skill 強調「宁可寫長寫細，也不要蜻蜓點水」——這個篇幅約束本身就是方法論的一部分。

### 2. khazix-writer（公眾號長文寫作）

最厚也最有趣的 Skill。它把卡茲克的個人聲音拆成「**核心價值觀 → 5 種文章原型 → 18 個風格內核 → 7 條絕對禁區 → 6 類推薦口語詞 → 4 層自檢體系**」。

**5 種文章原型：** 調查實驗型（親自下場）/ 產品體驗型（帶讀者一起玩）/ 現象解讀型（層層深入）/ 工具分享型（個人故事包裝）/ 方法論分享型（坦誠講學習曲線）

**絕對禁區（一出現立刻暴露 AI 味）：**

| 類別 | 禁用內容 |
|------|---------|
| 套話 | 首先...其次...最後、綜上所述、值得注意的是 |
| 標點 | 冒號「：」、破折號「——」、雙引號"" — 全用「」或逗號替代 |
| 高頻踩雷詞 | **說白了**、**意味著什麼？**、**這意味著**、本質上、換句話說、不可否認 |
| 假設例子 | 不准寫「比如有一次...」這種編造場景 |
| 空泛工具名 | 不准用「AI 工具」「某個模型」，必須具名 |
| 教科書開頭 | 禁止「在當今 AI 快速發展的時代」 |

**4 層自檢體系（從 L1 到 L4）：**

```
L1 硬性規則    → 禁用詞 / 禁用標點 / 結構性套話 / 工具名 全文掃描
   ↓
L2 風格一致性  → 開頭 / 節奏結構 / 口語化 / 標點二次確認
   ↓
L3 內容質量    → 觀點深度 / 案例支撐 / 私人視角
   ↓
L4 活人感判斷  → 最主觀層，「讀起來像不像真人在聊」
```

設計理念明確類比軟體測試金字塔——這是把編程紀律遷移到內容創作的罕見案例。

## 安裝方式

| 工具 | Skills 路徑 |
|------|------------|
| Claude Code | `~/.claude/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |

也可在支援 Skill 的 Agent 中直接對話「安裝這個 skill：https://github.com/KKKKhazix/khazix-skills」。

## CLAUDE.md 揭露的發布策略

倉庫的 CLAUDE.md 不藏私，把作者的多平台佔位策略寫得很白：

| 優先級 | 平台 | 動作 |
|--------|------|------|
| 1 | **ClawHub** (clawhub.ai) | `clawhub publish <path> --slug <name>` |
| 2 | **Tessl** (tessl.io) | `tessl skill publish --workspace khazix-skills --public --skip-evals <path>` |
| 3 | **claude-skill-registry** | 向 majiayu000/claude-skill-registry-core 提 PR |

「**不需要等使用者要求，有新 skill 就主動發布**」「**防止被他人 fork 搶註**」——這兩句話直接寫進 Agent 操作規則。

## 目前限制

- **強烈中文語境**：寫作風格 Skill 完全綁定簡中網路語感（「不是哥們」「太牛逼了」「這玩意」），繁體 / 英文場景無法直接套用
- **個人風格不一定通用**：khazix-writer 是高度個人化的聲音克隆，套到別人公眾號上會失真
- **PDF 排版依賴 WeasyPrint**：需要 `pip install weasyprint markdown --break-system-packages`，CSS 已寫死
- **方法論偏好「重」**：hv-analysis 動輒 1-3 萬字，不適合輕量級主題
- **倉庫只是鏡像**：真正的開發在私有的 `skill-build/`，外部貢獻者很難參與迭代

## 研究價值與啟示

### 關鍵洞察

1. **個人方法論是 Skills 最被低估的應用場景。** 當大家都在做通用工具型 Skill（git 操作、API call）時，khazix-skills 證明了「**把一個有影響力的人的思考方式蒸餾成 Skill**」的市場價值——14 天 5.4K stars 是用結果說話的論證。對比 [andrej-karpathy-skills](andrej-karpathy-skills.md) 用一份 CLAUDE.md 拿 44K stars，路徑類似但深度更高。

2. **「開源工作流規則」本身是一種品牌策略。** 把 CLAUDE.md（包含 ClawHub / Tessl 帳號、發布優先級、私有工作區命名）公開放出來，等於告訴讀者「我是怎麼把個人經驗系統化的」。這比寫一篇「我怎麼用 AI」的公眾號文更有說服力，因為**規則本身就是證據**。

3. **「禁止清單」比「鼓勵清單」更精準地刻畫風格。** khazix-writer 用大量篇幅列「**絕對不能寫什麼**」——禁用標點、禁用詞彙、禁用句式。這個負面定義比「請寫得有節奏」這種正面要求精準 10 倍，因為負面規則可以機械掃描，而 L1 自檢層就是這樣設計的。任何想 clone 個人風格的 Skill 作者都應該先列禁區。

4. **多平台主動發布是新一輪「網域名稱戰」。** ClawHub / Tessl / claude-skill-registry 三個平台同步佔位，是因為作者預期 Agent Skills 生態會像 npm / PyPI 一樣形成中心化 registry——**slug 名稱會成為稀缺資源**。這是 2026 年 Skills 生態剛起步時的窗口期套利，下半年可能就佔不到了。

5. **「skill-build / github-share」雙軌制是專業 Skill 作者的標配。** 私有評估區做 eval、迭代、踩坑，公開區只放穩定版本。這個結構暗示 Skills 開發已經從「個人玩具」進入「軟體工程紀律」階段——和早期 Open Source 從「程式碼共享」進化到 CI/CD + Release Channel 的軌跡一模一樣。

### 與其他專案的關聯

- 與 [andrej-karpathy-skills](andrej-karpathy-skills.md) 並列「個人 IP 蒸餾型」Skill 雙標竿——Karpathy 走的是「四條工程原則」極簡路線，卡茲克走的是「方法論 + 寫作風格」雙 Skill 完整路線
- 與 [Asgard Skills](asgard-skills.md)、[KC AI Skills](kc-ai-skills.md)、[Claude Skills Guide](claude-skills-guide.md) 同為 2026 Q1-Q2 Skills 生態爆發期的代表作
- README 提到的 **OpenClaw** 與本站 [OpenClaw](openclaw.md) 筆記對應，可見作者也是該 Agent 的早期推廣者
- hv-analysis 的「子 Agent 並行搜尋」實作思路，與 [DeerFlow](deer-flow.md)、[Autoresearch](autoresearch.md) 等深度研究型 Agent 框架可以橫向比較
- khazix-writer 的「4 層自檢體系」設計類比軟體測試金字塔，與 [Andrej Karpathy Skills](andrej-karpathy-skills.md) 的「Goal-Driven Execution（轉成寫測試）」是同一思維譜系——**把編程紀律遷移到非程式碼領域**
