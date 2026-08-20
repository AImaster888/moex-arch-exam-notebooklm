# 國考歷屆試題 × NotebookLM MCP 知識庫分析助手

> **專案性質**：個人 POC 技術驗證專案（Private）  
> **核心架構**：公開試題下載 ➔ 格式整理 ➔ **NotebookLM MCP 知識庫對接** ➔ AI 考點分析

---

> [!IMPORTANT]
> ### ⚠️ 重要前提：必須安裝 NotebookLM MCP
> 本工作流的核心設計是**將動輒數百頁的歷屆試題 PDF 交由 NotebookLM 閱讀與檢索，Agent（Claude / Antigravity）則透過 `NotebookLM MCP` 與線上筆記本無縫對接，進行精準提問、考點分析與引註驗證**。
>
> 若未安裝與設定 NotebookLM MCP，Agent 將無法直接讀取線上筆記本的題目內容。**請務必先完成下方 MCP 安裝設定！**

---

## 📌 專案概述

本專案實作了一套公開試題與 AI 知識庫協作的通用自動化流程（以國考高考三級公開試題為 POC 測試案例）：
1. **試題爬取**：自動化批次抓取公開歷屆試題本與參考答案 PDF。
2. **格式整理**：將下載之試題進行分類、命名正規化，並支援雙面列印防混頁合併（奇數頁自動補白）。
3. **知識庫上傳與 MCP 對接**：將歷年試題匯入至 Google NotebookLM 建立專屬筆記本，並透過 `notebooklm-mcp` 讓 AI 直接調用、分析出題趨勢。

---

## 🛠️ NotebookLM MCP 安裝與設定步驟

### 步驟 1：安裝 NotebookLM MCP Server
套件為 PyPI 上的 **`notebooklm-mcp-cli`**（同時提供 MCP server `notebooklm-mcp` 與認證工具 `nlm`）：

```bash
# 使用 pip 安裝
pip install notebooklm-mcp-cli

# 或使用 uv 安裝 (推薦)
uv tool install notebooklm-mcp-cli
```

安裝完成後確認執行檔正常可用：
```bash
notebooklm-mcp --version
```

### 步驟 2：Google 帳號認證登入
```bash
nlm login
```
*系統會自動開啟瀏覽器引導您完成 Google 帳號登入（請登入持有該 NotebookLM 筆記本的帳號）。*

### 步驟 3：註冊 MCP Server 至 Agent 環境

#### 方式 A：Claude Code CLI 註冊
```bash
claude mcp add notebooklm-mcp --env NOTEBOOKLM_HL=zh-TW -- notebooklm-mcp
```

#### 方式 B：手動加入設定檔 (`~/.claude.json` 或 `claude_desktop_config.json`)
在 `mcpServers` 區塊中加入：
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "type": "stdio",
      "command": "notebooklm-mcp",
      "args": [],
      "env": {
        "NOTEBOOKLM_HL": "zh-TW"
      }
    }
  }
}
```

---

## 🚀 腳本執行流程

### 1. 安裝 Python 依賴套件
```bash
pip install requests beautifulsoup4 pypdf
```

### 2. 執行公開試題下載
```bash
python scripts/download_exams.py --start 110 --end 115 --category "高考三級" --dept "建築工程"
```

### 3. (選用) 考卷雙面列印合併（奇數頁自動補白）
```bash
python scripts/merge_exams.py --input-dir "./data" --output "歷屆試題_雙面列印版.pdf"
```

---

## ⚖️ 合法性與技術說明

* 依中華民國《著作權法》第 9 條第 1 項第 5 款規定，**「依法令舉行之各類考試試題及其備選試題，不得為著作權之標的」**。本工具僅作為個人研讀及技術驗證之用。
* PDF 試題檔案與暫存目錄（`data/`、`*.pdf`）已由 `.gitignore` 排除，避免 repo 過度肥大。

---

## 📅 版本歷程
* **v1.2 (2026-08-20)**：泛化專案說明為通用國考試題知識庫分析架構，去識別化並補充法規依據。
* **v1.1 (2026-08-20)**：新增 **NotebookLM MCP 必要安裝與設定指引**。
* **v1.0 (2026-08-20)**：建立 POC 專案骨架、試題下載腳本與雙面列印合併工具。
