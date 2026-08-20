# MOEX 高考三級建築工程考古題 × NotebookLM 整合專案

> **專案性質**：個人 POC 驗證專案（Private）  
> **驗證目標**：自動化抓取考選部（MOEX）歷年考古題試題本，並將結構化試題庫串接至 Google NotebookLM 進行出題趨勢分析與 AI 輔助研讀。

---

## 📌 專案概述

本專案實作了一套自動化流程：
1. **試題爬取**：從考選部（MOEX）自動化批次抓取 110～115 年度「公務人員高等考試三級考試－建築工程類科」各科試題本與參考答案 PDF。
2. **格式整理**：將下載之試題進行分類、命名正規化，並支援雙面列印防混頁合併（奇數頁自動補白）。
3. **知識庫上傳**：將歷年試題整合匯入至 Google NotebookLM，建立專屬的建築工程國考知識庫。

---

## 🔗 NotebookLM 知識庫連結

* **線上筆記本**：[高考三級 建築工程 考古題庫 (110-115)](https://notebook.google.com/notebook/cfbc2bb8-818c-4aee-8af7-6002d2fd2e3c?authuser=4)
* **包含核心專業科目**：
  - 建築營造與施工
  - 建築環境控制
  - 建築結構
  - 建築構造與施工
  - 建築法規與實務
  - 營建法規與都市計畫法制

---

## 🚀 執行流程

### 1. 安裝環境依賴
```bash
pip install requests beautifulsoup4 pypdf reportlab
```

### 2. 執行考古題下載
```bash
python scripts/download_exams.py --start 110 --end 115 --category "高考三級" --dept "建築工程"
```

### 3. (選用) 考卷雙面列印合併
```bash
python scripts/merge_exams.py --input-dir "./data" --output "建築工程_110-115歷屆試題_雙面列印版.pdf"
```

---

## ⚙️ Git 管理說明

由於 PDF 檔案量較大且屬公開資料，Git 僅版本控制程式碼與說明文件，試題本暫存目錄（`data/` 與 `*.pdf`）已由 `.gitignore` 排除。

---

## 📅 版本歷程
* **v1.0 (2026-08-20)**：完成 POC 驗證，建立考選部下載自動化架構與 NotebookLM 知識庫串接。
