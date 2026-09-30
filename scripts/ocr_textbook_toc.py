# -*- coding: utf-8 -*-
"""Render and OCR textbook TOC + early lesson pages."""
from pathlib import Path
import pymupdf
from rapidocr_onnxruntime import RapidOCR

root = Path(r"D:\AI_WorkSPACE\Chinese Desk")
pdf = next((root / "textbook").glob("*.pdf"), None) or next(root.glob("*.pdf"))
out = root / "test" / "_book_ocr"
out.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(pdf)
print("pdf", pdf.name, "pages", doc.page_count)

# render pages likely to be TOC + unit1 start: try 1-25
engine = RapidOCR()
for i in list(range(0, 12)) + list(range(12, 40, 2)):
    if i >= doc.page_count:
        break
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(2, 2))
    img = out / f"p{i+1:03d}.png"
    pix.save(str(img))
    result, _ = engine(str(img))
    lines = [x[1] for x in (result or [])]
    text = "\n".join(lines)
    (out / f"p{i+1:03d}.txt").write_text(text, encoding="utf-8")
    print(f"page {i+1}: {len(lines)} lines")
    # print if looks like TOC
    if any(k in text for k in ("目录", "第一单元", "观潮", "会写", "爬山虎")):
        print("---", i + 1, "---")
        print(text[:800])
        print()
