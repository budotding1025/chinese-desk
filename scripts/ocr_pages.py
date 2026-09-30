# -*- coding: utf-8 -*-
"""OCR split unit-test pages with RapidOCR."""
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

ROOT = Path(r"D:\AI_WorkSPACE\Chinese Desk")
PAGES = ROOT / "test" / "_pages"
OUT = ROOT / "test" / "_ocr"
OUT.mkdir(parents=True, exist_ok=True)

engine = RapidOCR()
for img in sorted(PAGES.glob("*.png")):
    result, _ = engine(str(img))
    lines = []
    if result:
        for item in result:
            # item: [box, text, score]
            lines.append(item[1])
    text = "\n".join(lines)
    out_path = OUT / (img.stem + ".txt")
    out_path.write_text(text, encoding="utf-8")
    print(f"{img.name}: {len(lines)} lines -> {out_path.name}")
