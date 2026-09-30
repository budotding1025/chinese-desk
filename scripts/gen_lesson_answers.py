# -*- coding: utf-8 -*-
"""Generate per-lesson answer A4 PDFs + refresh print-index with answer URLs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_lesson_printables import LESSONS, save_pair, tight_doc, p, section
from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "printables" / "answers"


def build_answer(les: dict):
    doc = tight_doc()
    p(doc, "语文书桌 · 参考答案（做完再看）", size=9, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=1)
    p(
        doc,
        f"第{les['bookNo']}课《{les['title']}》· 答案",
        size=14,
        bold=True,
        color=BRAND_ORANGE_RED,
        center=True,
        after=4,
    )
    section(doc, "一、字词听写")
    p(doc, "、".join(w for w, _ in les["words"]), size=11, after=4)
    if les.get("idioms"):
        section(doc, "二、成语")
        p(doc, "、".join(w for w, _ in les["idioms"]), size=11, after=3)
        p(doc, "造句：通顺合理即可。", size=10, color=BRAND_DEEP, after=4)
    if les.get("compounds"):
        section(doc, "组词（合理即可）")
        tips = "；".join(f"{a}/{b}" for a, b in les["compounds"])
        p(doc, tips, size=10.5, after=4)
    section(doc, "三、多音字")
    if les.get("poly"):
        p(doc, "；".join(f"{w}→{opts[i]}" for w, opts, i in les["poly"]), size=11, after=3)
    if les.get("poly_wrong"):
        wrongs = [f"{w}（{py}）{'正确' if ok else '有误'}" for w, py, ok in les["poly_wrong"]]
        p(doc, "读音正误：" + "；".join(wrongs), size=10.5, after=4)
    if not les.get("poly") and not les.get("poly_wrong"):
        p(doc, "本课多音较少，略。", size=10, after=4)
    section(doc, "四、句型仿写")
    p(doc, "开放题：符合要求、语句通顺即可。", size=10.5, after=2)
    p(doc, "提示：" + les["pattern"]["example"], size=9, color=BRAND_DEEP, after=4)
    if les.get("recite"):
        section(doc, "课文默写（另页）")
        p(doc, les["recite"]["answer"], size=11, after=4)
    p(doc, "错题请记入「记录 → 错题」。", size=8, color=BRAND_DEEP, center=True, before=8)
    return doc


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    md_root = ROOT / "answers" / "lessons"
    md_root.mkdir(parents=True, exist_ok=True)
    index = {"lessons": {}, "sprint": {
        "u1": "printables/sprint/U1-sprint.pdf",
        "u2": "printables/sprint/U2-sprint.pdf",
        "u3": "printables/sprint/U3-sprint.pdf",
    }}
    for les in LESSONS:
        n = les["bookNo"]
        daily = f"printables/lessons/L{n:02d}-{les['title']}-每日10分钟.pdf"
        recite = f"printables/lessons/L{n:02d}-{les['title']}-背诵默写10分钟.pdf" if les.get("recite") else None
        ans_stem = f"L{n:02d}-{les['title']}-答案"
        save_pair(build_answer(les), OUT, ans_stem)
        ans_pdf = f"printables/answers/{ans_stem}.pdf"
        # markdown for online view
        lines = [
            f"# 第{n}课《{les['title']}》参考答案\n\n",
            f"> 做完练习再看。开放题意思对即可。\n\n",
            "## 字词听写\n\n",
            "、".join(w for w, _ in les["words"]) + "\n\n",
        ]
        if les.get("idioms"):
            lines.append("## 成语\n\n" + "、".join(w for w, _ in les["idioms"]) + "\n\n")
        if les.get("compounds"):
            lines.append("## 组词\n\n合理即可：" + "；".join(f"{a}/{b}" for a, b in les["compounds"]) + "\n\n")
        if les.get("poly"):
            lines.append("## 多音字\n\n" + "；".join(f"{w}→{opts[i]}" for w, opts, i in les["poly"]) + "\n\n")
        lines.append("## 句型仿写\n\n通顺即可。提示：" + les["pattern"]["example"] + "\n\n")
        if les.get("recite"):
            lines.append("## 课文默写\n\n" + les["recite"]["answer"] + "\n")
        md_path = md_root / f"L{n:02d}-{les['title']}-答案.md"
        md_path.write_text("".join(lines), encoding="utf-8")
        index["lessons"][str(n)] = {
            "daily": daily,
            "recite": recite,
            "answerPdf": ans_pdf,
            "answerMd": f"answers/lessons/L{n:02d}-{les['title']}-答案.md",
            "answerHtml": "".join(lines).replace("\n", "<br>").replace("# ", "").replace("## ", "<b>").replace("</b><br>", "</b><br>"),
            "title": les["title"],
        }
    (ROOT / "print-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README.md").write_text("# 每课答案（可打印）\n\n与 `../lessons/` 练习对应。\n", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
