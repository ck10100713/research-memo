---
date: "2026-04-10"
category: "OSINT / 情報工具"
card_icon: "material-magnify-scan"
oneliner: "Python CLI — 自動辨識文字/檔案中的 email、IP、API key、加密貨幣錢包等 141 種模式"
---

# pyWhat — 「這是什麼？」的萬用辨識器

## 資料來源

| 項目 | 連結 |
|------|------|
| GitHub Repo | [bee-san/pyWhat](https://github.com/bee-san/pyWhat) |
| PyPI | [pywhat](https://pypi.org/project/pywhat/) |
| API 文件 | [GitHub Wiki](https://github.com/bee-san/pyWhat/wiki/API) |
| Kali Linux Tutorials | [kalilinuxtutorials.com/pywhat](https://kalilinuxtutorials.com/pywhat/) |
| OSINT 工具清單 | [Intel 471](https://www.intel471.com/blog/python-libraries-for-osint-automation) |
| OffSec KB | [kb.offsec.nl](https://kb.offsec.nl/tools/other/pywhat/) |

## 專案概述

pyWhat 是一個 Python CLI 工具，核心功能只有一個：**告訴你「這是什麼」**。丟給它一段文字、一個檔案、一個目錄、甚至一個 `.pcap` 網路封包，它會用 141 個 regex 模式遞迴掃描，辨識出所有結構化資料——email、IP 位址、API key、加密貨幣錢包、信用卡號、JWT token、SSH 公鑰等等。

主要使用場景：

- **惡意軟體分析**：快速找出 malware 中硬編碼的 domain、C2 伺服器 IP、比特幣錢包
- **Pcap 分析**：從網路封包中秒速提取 URL、email、電話、信用卡號
- **Bug Bounty**：掃描 GitHub repo 或網頁，找出洩漏的 API key 和 credentials
- **CTF 競賽**：快速辨識 flag 格式、hash 類型、編碼方式

專案始於 2021 年，目前 7,200+ GitHub stars，MIT 授權。

## 141 個 Regex 模式分類

pyWhat 內建的 `regex.json` 包含 141 個辨識模式，涵蓋以下類別：

| 類別 | 範例模式 |
|------|---------|
| **網路** | IPv4、IPv6、URL、MAC Address、Bluetooth Address |
| **身份識別** | Email、Phone Number、SSN、Date of Birth |
| **金融** | Visa/MasterCard/AMEX/Discover 信用卡、PayPal |
| **加密貨幣** | Bitcoin、Ethereum、Litecoin、Dogecoin、Monero、Ripple、Nano 錢包 |
| **API Keys / Token** | AWS、Google Cloud、Stripe、Twilio、Slack、Discord Bot、GitHub、Heroku、SendGrid、Shopify、Mailgun、Zapier 等 |
| **安全** | JWT Token、SSH Public Key、PGP、TOTP |
| **識別碼** | UUID、ULID、ObjectID、UNIX Timestamp |
| **社群媒體** | YouTube Video/Channel、Twitter、LinkedIn、Facebook |
| **其他** | CTF Flag、License Plate、Geo-location (Lat & Long) |

此外還有輔助資料檔：

| 檔案 | 用途 |
|------|------|
| `regex.json` | 141 個核心辨識模式 |
| `file_signatures.json` | 檔案魔數（magic bytes）辨識 |
| `mac_vendors.json` | MAC 位址→廠商對照 |
| `mastercard_companies.json` | MasterCard BIN→發卡行對照 |
| `phone_codes.json` | 國際電話區碼對照 |

## CLI 使用方式

```bash
# 安裝
pip3 install pywhat
# 或 macOS
brew install pywhat

# 基本用法：辨識文字
pywhat "0x52908400098527886E0F7030069857D2E4169EE7"
# → Ethereum Wallet

# 辨識檔案
pywhat /path/to/suspicious.exe

# 遞迴掃描目錄
pywhat /path/to/malware_samples/

# 分析 pcap
pywhat capture.pcap

# 只顯示 Bug Bounty 相關
pywhat --include "Bug Bounty" leaked_code.py

# 篩選稀有度（0=常見, 1=罕見）
pywhat --rarity 0.2:0.8 some_text

# 組合篩選：加密貨幣但排除 Ripple
pywhat --include "Cryptocurrency Wallet" --exclude "Ripple Wallet" some_text

# 排序 + JSON 輸出
pywhat -k rarity --reverse --json input.txt > results.json

# 查看所有可用 tag
pywhat --tags
```

## Python API

```python
from pywhat import Identifier

identifier = Identifier()

# 辨識文字
result = identifier.identify("test@example.com and 192.168.1.1")

# 辨識檔案
result = identifier.identify("/path/to/file")

# 結果是 dict，包含 matches 清單
for match in result["Regexes"]:
    print(f"{match['Regex Pattern']['Name']}: {match['Matched']}")
```

## 實戰場景

### 場景 1：掃描 GitHub org 找洩漏的 API Key

```bash
# 下載整個 org 的 repo
GHUSER=target-org
curl "https://api.github.com/users/$GHUSER/repos?per_page=1000" \
  | grep -o 'git@[^"]*' | xargs -L1 git clone

# 遞迴掃描所有檔案
find . -type f -execdir pywhat --include 'Bug Bounty' {} \;
```

### 場景 2：Malware 分析找 Kill Switch

```bash
# 找出 malware 中所有硬編碼的 domain 和 IP
pywhat --include "URL,IP" suspicious_malware.exe
# → 註冊這些 domain 可能就是 kill switch
```

### 場景 3：CTF 快速辨識

```bash
# 不知道這串 hash 是什麼？
pywhat "5f4dcc3b5aa765d61d8327deb882cf99"
# → MD5 Hash

# 不知道這個 base64 解碼後是什麼？
echo "dGVzdA==" | base64 -d | pywhat
```

## 目前限制

| 限制 | 說明 |
|------|------|
| Regex-only | 純模式匹配，無語意理解，可能有誤報 |
| 無即時更新 | API key 格式變更時需要手動更新 regex.json |
| 無驗證能力 | 只辨識格式，不驗證是否為真實有效的 key/address |
| 大型檔案效能 | 遞迴掃描大量檔案時可能較慢 |
| 141 個模式有限 | 無法涵蓋所有可能的格式（但可自行擴充） |
| 非主動維護 | 2021 年啟動，近期更新頻率較低 |

## 研究價值與啟示

### 關鍵洞察

1. **「這是什麼？」是資安工作流中最頻繁的問題**：分析師每天都在面對未知的 hash、token、錢包地址。pyWhat 用最簡單的方式解決這個問題——不需要 AI、不需要雲端服務，就是 141 個精心維護的 regex。有時最有效的工具就是最簡單的。

2. **Tag 系統讓它從「辨識工具」升級為「情境化掃描器」**：`--include "Bug Bounty"` 和 `--include "Cryptocurrency Wallet"` 這種篩選能力，讓同一個工具在不同場景下有不同的行為。這是一個值得借鏡的 CLI 設計模式——用 tag 而非子命令來切換上下文。

3. **regex.json 是可複用的資產**：pyWhat 最有價值的不是它的 Python 程式碼，而是那份 141 個正則表達式的 JSON 資料庫。這份資料可以被移植到任何語言、任何工具中——Rust CLI、JavaScript 掃描器、甚至 AI Agent 的工具函數。

4. **和 AI/LLM 工具鏈的整合潛力巨大**：想像一個 Coding Agent 在分析 log 或 pcap 時，先用 pyWhat 快速提取結構化資料，再用 LLM 做語意分析。pyWhat 做「辨識」，LLM 做「理解」——這是比純 LLM 分析更精確且更快的組合。

5. **社群驅動的 regex 策展是護城河**：任何人都能寫 regex，但要維護一份涵蓋 API key、加密貨幣、信用卡、社群媒體等多領域的 regex 資料庫，需要持續的社群貢獻。Hacktoberfest 標籤說明了這個策略。

### 與其他專案的關聯

- **OsintRadar**：OsintRadar 是 OSINT 工具目錄的策展，pyWhat 是實際的 OSINT 執行工具——pyWhat 正是 OsintRadar 會收錄的那類工具
- **OpenHarness / Claude Code**：如果將 pyWhat 包裝成 MCP tool，Coding Agent 就能在分析檔案時自動呼叫 `pywhat` 辨識結構化資料，大幅提升 OSINT 和安全分析的效率
- **Context Hub**：Context Hub 提供 API 文件讓 Agent 寫正確的程式碼，pyWhat 提供模式辨識讓 Agent 理解未知資料——兩者都在擴充 Agent 的「感知能力」
