# -*- coding: utf-8 -*-
import pymupdf
from pathlib import Path

root = Path(r"D:\AI_WorkSPACE\Chinese Desk")
pdfs = list(root.glob("*.pdf"))
print("pdfs:", [p.name for p in pdfs])
path = pdfs[0]
doc = pymupdf.open(path)
print("pages", doc.page_count)
keys = [
    "赠刘景文",
    "人非生而知之者",
    "博学之",
    "横看成岭侧成峰",
    "一场秋雨",
    "善疑者",
    "暮江吟",
    "题西林壁",
]
for k in keys:
    hits = [i + 1 for i, p in enumerate(doc) if k in p.get_text()]
    print(k, hits[:10])
