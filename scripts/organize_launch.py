# -*- coding: utf-8 -*-
"""Organize textbook + unit folders for Chinese Desk launch."""
from pathlib import Path
import shutil

ROOT = Path(r"D:\AI_WorkSPACE\Chinese Desk")
TEXTBOOK = ROOT / "textbook"
TEXTBOOK.mkdir(exist_ok=True)

# move / copy textbook pdf
pdfs = list(ROOT.glob("*.pdf"))
for p in pdfs:
    dest = TEXTBOOK / "四年级上册语文_统编版.pdf"
    if not dest.exists():
        shutil.copy2(p, dest)
        print("textbook ->", dest.name)
    else:
        print("textbook exists")

units = [
    ("u01-四上第一单元", "第一单元", "完整（4页）", "观潮 / 走月亮 / 现代诗二首 / 繁星 · 语文园地一"),
    ("u02-四上第二单元", "第二单元", "完整（4页）", "一个豆荚里的五粒豆 / 爬天都峰 / 为中华之崛起而读书 / 那一定会很好 · 提问 · 园地二"),
    ("u03-四上第三单元", "第三单元", "不完整（仅1–2页）", "爬山虎的脚 / 蟋蟀的住宅 · 观察 · 园地三"),
]
for folder, title, status, note in units:
    d = ROOT / "units" / folder
    d.mkdir(parents=True, exist_ok=True)
    src = d / "source"
    src.mkdir(exist_ok=True)
    (d / "README.md").write_text(
        f"""# 四上 · {title}

**状态**：{status}  
**教材要点**：{note}

## 文件

- 练习：`../../printables/` 下对应 `u0x-…练习.docx/.pdf`
- 答案：`../../answers/` 下对应参考答案
- 原扫描：`../../test/`（U1/U2/U3 双页拼图）

## 用法

考前：测一测 → 看漏洞 → 只补漏洞（约 8–15 分钟抓字词与园地；整卷可分两次）。
""",
        encoding="utf-8",
    )
    print("unit", folder)

# copy source scans into units
mapping = {
    "u01-四上第一单元": ["U1-1.png", "U1-2.png"],
    "u02-四上第二单元": ["U2-1.png", "U2-2.png"],
    "u03-四上第三单元": ["U3-1.png"],
}
for folder, files in mapping.items():
    for f in files:
        s = ROOT / "test" / f
        if s.exists():
            shutil.copy2(s, ROOT / "units" / folder / "source" / f)
            print("copied", f, "->", folder)

# remove sample placeholder if still there
sample = ROOT / "units" / "sample-u01-四上示例"
if sample.exists():
    shutil.rmtree(sample)
    print("removed sample unit")

print("organize done")
