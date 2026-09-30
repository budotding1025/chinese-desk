# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document

root = Path(r"D:\AI_WorkSPACE\Chinese Desk")
errors = []


def texts(p: Path) -> str:
    d = Document(str(p))
    return "\n".join(x.text for x in d.paragraphs if x.text.strip())


for u in (1, 2, 3):
    wd = next((root / "printables" / "weekday").glob(f"u0{u}-*.docx"))
    we = next((root / "printables" / "weekend").glob(f"u0{u}-*.docx"))
    tw, te = texts(wd), texts(we)
    if "参考答案" not in tw:
        errors.append(f"U{u} weekday missing answer block")
    if "错题" not in tw:
        errors.append(f"U{u} weekday missing mistake hint")
    if "作文" not in te or "课外" not in te:
        errors.append(f"U{u} weekend missing 作文/课外")
    print(f"U{u} weekday={len(tw)}c weekend={len(te)}c OK-ish")

a1 = (root / "answers" / "weekday-u01-参考答案.md").read_text(encoding="utf-8")
a2 = (root / "answers" / "weekday-u02-参考答案.md").read_text(encoding="utf-8")
a3 = (root / "answers" / "weekday-u03-参考答案.md").read_text(encoding="utf-8")
for needle, blob, name in [
    ("繁星", a1, "u01"),
    ("苏轼", a1, "u01"),
    ("身份", a2, "u02"),
    ("孰能无惑", a2, "u02"),
    ("爬山虎", a3, "u03"),
    ("远近高低各不同", a3, "u03"),
]:
    if needle not in blob:
        errors.append(f"{name} answer missing {needle}")

# path consistency
mist = (root / "mistakes" / "错题档案.md").read_text(encoding="utf-8")
if "printables/weekday/错题登记表" in mist and "../printables" not in mist:
    errors.append("mistakes archive should use ../printables/ relative path")

if errors:
    print("ERRORS:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("QA PASS")
