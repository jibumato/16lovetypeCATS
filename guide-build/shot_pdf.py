#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成したPDFの全ページをコンタクトシート画像にする（目視チェック用）。

verify_pdf.py のテキスト検査だけでは、図の重なり・枠線の欠け・
不自然な空白など「見た目の崩れ」は検知できない（実際にENFJ版で
何度も見落とした）。このスクリプトで必ず画像化し、Readツールで
目視確認してから完成とすること。
"""
import glob
import os
import sys

import pymupdf
from PIL import Image

SP = "/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"


def sheet(pdf_path, out_path, dpi=48, cols=8):
    d = pymupdf.open(pdf_path)
    ims = []
    for i in range(d.page_count):
        pm = d[i].get_pixmap(dpi=dpi)
        ims.append(Image.frombytes("RGB", [pm.width, pm.height], pm.samples))
    d.close()
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    out = Image.new("RGB", (w * cols, h * rows), "white")
    for i, im in enumerate(ims):
        out.paste(im, ((i % cols) * w, (i // cols) * h))
    out.save(out_path)
    return out_path, len(ims)


def pair(pdf_path, out_path, page_a, page_b, dpi=100):
    """指定した2ページを横並びの読める解像度で書き出す（細部確認用）。"""
    d = pymupdf.open(pdf_path)
    ims = []
    for i in (page_a - 1, page_b - 1):
        if 0 <= i < d.page_count:
            pm = d[i].get_pixmap(dpi=dpi)
            ims.append(Image.frombytes("RGB", [pm.width, pm.height], pm.samples))
    d.close()
    w = sum(im.width for im in ims)
    h = max(im.height for im in ims)
    out = Image.new("RGB", (w, h), "white")
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width
    out.save(out_path)
    return out_path


if __name__ == "__main__":
    targets = sys.argv[1:] or sorted(glob.glob(os.path.join(SP, "*_love_guide_cat.pdf")))
    for path in targets:
        code = os.path.basename(path).split("_")[0]
        out, n = sheet(path, os.path.join(SP, f"sheet_{code}.png"))
        print(f"{code}: {n}ページ -> {out}")
