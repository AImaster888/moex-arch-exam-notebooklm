#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考卷 PDF 雙面列印合併腳本 (奇數頁自動補空白，避免混頁)
"""

import os
import sys
import argparse
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

def create_blank_page(width, height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.showPage()
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def merge_exams_for_duplex(input_dir, output_file):
    writer = PdfWriter()
    pdf_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')])
    
    if not pdf_files:
        print(f"⚠️ 在 {input_dir} 中找不到任何 PDF 檔案。")
        return

    print(f"找到 {len(pdf_files)} 個 PDF 檔案，開始合併...")

    for pdf_name in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_name)
        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
        
        for page in reader.pages:
            writer.add_page(page)

        if page_count % 2 != 0:
            last_page = reader.pages[-1]
            box = last_page.mediabox
            width = float(box.width)
            height = float(box.height)
            blank = create_blank_page(width, height)
            writer.add_page(blank)
            print(f"  📄 {pdf_name}: 共 {page_count} 頁 (奇數頁，已自動補 1 頁空白)")
        else:
            print(f"  📄 {pdf_name}: 共 {page_count} 頁 (偶數頁)")

    with open(output_file, 'wb') as f_out:
        writer.write(f_out)
    print(f"✅ 雙面列印合併完成！輸出檔案: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="考卷雙面列印合併工具")
    parser.add_argument("--input-dir", type=str, default="./data", help="PDF 來源目錄")
    parser.add_argument("--output", type=str, default="雙面列印合併考卷.pdf", help="輸出 PDF 檔名")
    args = parser.parse_args()

    merge_exams_for_duplex(args.input_dir, args.output)

if __name__ == "__main__":
    main()
