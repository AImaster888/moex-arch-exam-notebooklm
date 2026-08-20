# MOEX 高考三級建築工程考古題 × NotebookLM 整合專案

> **專案性質**：個人 POC 驗證專案（Private）  
> **核心架構**：自動化試題下載 ➔ 格式整理 ➔ **NotebookLM MCP 知識庫對接** ➔ AI 考點分析

---

> [!IMPORTANT]
> ### ⚠️ 重要前提：必須安裝 NotebookLM MCP
> 本工作流的核心設計是**將動輒數百頁的歷屆試題 PDF 交由 NotebookLM 閱讀與檢索，Agent（Claude / Antigravity）則透過 `NotebookLM MCP` 與線上筆記本無縫對接，進行精準提問、考點分析與引註驗證**。
>
> 若未安裝與設定 NotebookLM MCP，Agent 將無法直接讀取線上筆記本的題目內容。**請務必先完成下方 MCP 安裝設定！**

---

## 📌 專案概述

本專案實作了一套完整的自動化與知識庫協作流程：
1. **試題爬取**：從考選部（MOEX）自動化批次抓取 110～115 年度「公務人員高等考試三級考試－建築工程類科」各科試題本與參考答案 PDF。
2. **格式整理**：將下載之試題進行分類、命名正規化，並支援雙面列印防混頁合併（奇數頁自動補白）。
3. **知識庫上傳與 MCP 對接**：將歷年試題匯入至 Google NotebookLM，並透過 `notebooklm-mcp` 讓 AI 直接調用、分析出題趨勢。

---

## 🔗 NotebookLM 知識庫連結

* **線上筆記本**：[高考三級 建築工程 考古題庫 (110-115)](https://notebook.google.com/notebook/cfbc2bb8-818c-4aee-8af7-6002d2fd2e3c?authuser=4)
* **涵蓋核心專業科目**：
  - 建築營造與施工
  - 建築環境控制
  - 建築結構
  - 建築構造與施工
  - 建築法規與實務
  - 營建法規與都市計畫法制

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

### 2. 執行考古題下載
```bash
python scripts/download_exams.py --start 110 --end 115 --category "高考三級" --dept "建築工程"
```

### 3. (選用) 考卷雙面列印合併（奇數頁自動補白）
```bash
python scripts/merge_exams.py --input-dir "./data" --output "建築工程_110-115歷屆試題_雙面列印版.pdf"
```

---

## ⚙️ Git 管理規範

* PDF 試題檔案與暫存目錄（`data/`、`*.pdf`）已由 `.gitignore` 排除，避免 repo 過度肥大。
* 日後推送到 GitHub 私有倉庫指令：
  ```bash
  gh repo create moex-arch-exam-notebooklm --private --source=. --push
  ```

---

## 📅 版本歷程
* **v1.1 (2026-08-20)**：新增 **NotebookLM MCP 必要安裝與設定指引**，確立大檔閱讀外包與 MCP 提問之分工架構。
* **v1.0 (2026-08-20)**：建立 POC 專案骨架、考選部下載腳本與雙面列印合併工具。
