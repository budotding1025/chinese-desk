# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image

src = Path(r"D:\AI_WorkSPACE\Chinese Desk\test")
out = Path(r"D:\AI_WorkSPACE\Chinese Desk\test\_pages")
out.mkdir(exist_ok=True)
for name in ["U1-1.png", "U1-2.png", "U2-1.png", "U2-2.png", "U3-1.png"]:
    im = Image.open(src / name)
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid + 20, h))
    right = im.crop((mid - 20, 0, w, h))
    stem = name.replace(".png", "")
    left.save(out / f"{stem}_pL.png")
    right.save(out / f"{stem}_pR.png")
    print(name, im.size, "->", left.size, right.size)
