#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考選部（MOEX）歷屆高考三級建築工程試題下載腳本 (POC)
"""

import os
import sys
import argparse
import requests

def download_file(url, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ 下載完成: {target_path}")
        return True
    else:
        print(f"❌ 下載失敗 ({response.status_code}): {url}")
        return False

def main():
    parser = argparse.ArgumentParser(description="考選部考古題下載工具")
    parser.add_argument("--start", type=int, default=110, help="起始年度 (民國)")
    parser.add_argument("--end", type=int, default=115, help="結束年度 (民國)")
    parser.add_argument("--category", type=str, default="高考三級", help="考試類別")
    parser.add_argument("--dept", type=str, default="建築工程", help="類科名稱")
    parser.add_argument("--output-dir", type=str, default="./data", help="檔案儲存目錄")

    args = parser.parse_args()

    print(f"=== 開始處理 {args.category} - {args.dept} 考古題 ({args.start}~{args.end} 年) ===")
    print(f"檔案將儲存至: {os.path.abspath(args.output_dir)}")
    print("提示: 試題檔案下載後可批次上傳至 Google NotebookLM 知識庫。")

if __name__ == "__main__":
    main()
