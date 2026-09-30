# -*- coding: utf-8 -*-
"""Fill missing gardens (u1–u8) and lessons L12–L27 printables + answers; refresh print-index."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from docx_utils import add_pinyin_write_grid, docx_to_pdf, set_run_font
from gen_lesson_printables import (
    LESSONS as LESSONS_1_11,
    blank,
    p,
    save_pair,
    section,
    tight_doc,
)
from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

ROOT = Path(__file__).resolve().parents[1]
OUT_L = ROOT / "printables" / "lessons"
OUT_G = ROOT / "printables" / "gardens"
OUT_A = ROOT / "printables" / "answers"
OUT_GA = ROOT / "printables" / "garden-answers"
MD_L = ROOT / "answers" / "lessons"
MD_G = ROOT / "answers" / "gardens"


def load_data():
    text = (ROOT / "data.js").read_text(encoding="utf-8")
    # strip to object
    m = re.search(r"window\.CHINESE_DESK_DATA\s*=\s*(\{[\s\S]*\});\s*$", text)
    if not m:
        raise RuntimeError("cannot parse data.js")
    # eval as JS-like JSON: need to convert - use node instead
    import subprocess

    script = r"""
const fs=require('fs');
const vm=require('vm');
const code=fs.readFileSync('data.js','utf8');
const ctx={window:{}};
vm.runInNewContext(code, ctx);
process.stdout.write(JSON.stringify(ctx.window.CHINESE_DESK_DATA));
"""
    raw = subprocess.check_output(["node", "-e", script], cwd=str(ROOT))
    return json.loads(raw.decode("utf-8"))


def render_html(md: str) -> str:
    parts = []
    for line in md.split("\n"):
        if line.startswith("# "):
            parts.append("<h2>" + line[2:] + "</h2>")
        elif line.startswith("## "):
            parts.append("<h3>" + line[3:] + "</h3>")
        elif line.startswith("> "):
            parts.append("<p class='meta'>" + line[2:] + "</p>")
        elif line.strip():
            parts.append("<p>" + line + "</p>")
    return "".join(parts)


def lesson_from_data(unit, les) -> dict:
    words = [(w["zh"], w["py"]) for w in (les.get("words") or []) if w.get("zh") and w.get("py")]
    compounds = [(c["a"], c["b"]) for c in (les.get("compounds") or [])]
    poly = []
    for ph in les.get("polyphones") or []:
        opts = ph.get("opts") or []
        ok = ph.get("ok")
        idx = opts.index(ok) if ok in opts else 0
        poly.append((ph.get("word") or "", opts, idx))
    meaning = les.get("meaning") or {}
    pattern = {
        "label": meaning.get("prompt") or "根据课文回答（写2～3句）",
        "example": "参考：" + (meaning.get("sample") or "意思对即可"),
    }
    recite = None
    if les.get("recite"):
        r = les["recite"]
        recite = {
            "label": r.get("label") or "课文默写",
            "lines": [r.get("prompt") or "____________________"],
            "answer": r.get("answer") or "",
        }
    # ensure at least something to write
    if not words and les.get("poems"):
        words = [(po.get("title") or "古诗", "gǔ shī") for po in les["poems"][:3]]
    if not words:
        words = [("积累", "jī lěi"), ("理解", "lǐ jiě")]
    if not compounds:
        compounds = [("学", "字")]
    return {
        "unit": unit["id"],
        "unitName": unit["name"].split("·")[0].strip(),
        "bookNo": les["bookNo"],
        "title": les["title"],
        "words": words,
        "idioms": [],
        "compounds": compounds,
        "poly": poly,
        "poly_wrong": [],
        "pattern": pattern,
        "recite": recite,
    }


def build_lesson_doc(les: dict):
    from gen_lesson_printables import build_lesson

    return build_lesson(les)


def build_lesson_answer_doc(les: dict):
    doc = tight_doc()
    p(doc, "语文书桌 · 参考答案（做完再看）", size=10, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=2)
    p(doc, f"第{les['bookNo']}课《{les['title']}》· 答案", size=16, bold=True, color=BRAND_ORANGE_RED, center=True, after=6)
    section(doc, "一、字词听写")
    p(doc, "、".join(w for w, _ in les["words"]), size=14, after=6)
    if les.get("compounds"):
        section(doc, "二、组词")
        p(doc, "；".join(f"{a}/{b}" for a, b in les["compounds"]), size=13, after=6)
    section(doc, "三、多音字")
    if les.get("poly"):
        p(doc, "；".join(f"{w}→{opts[i]}" for w, opts, i in les["poly"]), size=14, after=6)
    else:
        p(doc, "本课多音较少，略。", size=12, after=6)
    section(doc, "四、理解 / 仿写")
    p(doc, "开放题：通顺合理即可。", size=12, after=3)
    p(doc, les["pattern"]["example"], size=11, color=BRAND_DEEP, after=6)
    if les.get("recite"):
        section(doc, "课文默写")
        p(doc, les["recite"]["answer"], size=14, after=6)
    return doc


def lesson_answer_md(les: dict) -> str:
    n = les["bookNo"]
    lines = [
        f"# 第{n}课《{les['title']}》参考答案\n\n",
        "> 做完练习再看。开放题意思对即可。\n\n",
        "## 字词听写\n\n",
        "、".join(w for w, _ in les["words"]) + "\n\n",
    ]
    if les.get("compounds"):
        lines.append("## 组词\n\n" + "；".join(f"{a}/{b}" for a, b in les["compounds"]) + "\n\n")
    if les.get("poly"):
        lines.append("## 多音字\n\n" + "；".join(f"{w}→{opts[i]}" for w, opts, i in les["poly"]) + "\n\n")
    lines.append("## 理解 / 仿写\n\n" + les["pattern"]["example"] + "\n\n")
    if les.get("recite"):
        lines.append("## 课文默写\n\n" + les["recite"]["answer"] + "\n")
    return "".join(lines)


def build_garden_practice(unit_id: str, unit_name: str, garden: dict):
    acc = garden.get("accumulate") or {}
    doc = tight_doc()
    p(doc, "语文书桌 · Chinese Desk", size=10, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=2)
    p(doc, f"{garden.get('title') or '语文园地'} · 日积月累练习", size=16, bold=True, color=BRAND_ORANGE_RED, center=True, after=2)
    p(doc, f"{unit_name}　|　A4　|　姓名：________　日期：________", size=11, center=True, after=8)

    items = acc.get("items") or []
    lines = acc.get("lines") or []
    lines_detail = acc.get("linesDetail") or []

    if "习作" in (acc.get("title") or "") or unit_id == "u5":
        section(doc, "一、本单元要点（习作单元）")
        for it in items:
            p(doc, it.get("text") or "", size=13, bold=True, after=4)
            p(doc, it.get("tip") or "", size=12, color=BRAND_DEEP, after=8)
        section(doc, "二、把一件事写清楚（提纲）")
        p(doc, "起因：________________________________________________", size=12, after=8)
        p(doc, "经过（写具体）：", size=12, after=4)
        blank(doc, 3)
        p(doc, "结果：________________________________________________", size=12, after=8)
        return doc

    section(doc, "一、日积月累默写（不看书）")
    if lines_detail or lines:
        # poem style
        if acc.get("author"):
            p(doc, (acc.get("title") or "") + "　" + acc.get("author", ""), size=12, after=6)
        src = lines_detail or [{"text": ln} for ln in lines]
        for i, ln in enumerate(src, 1):
            text = (ln.get("text") if isinstance(ln, dict) else ln) or ""
            # blank half
            clean = text.replace("，", "").replace("。", "").replace("？", "").replace("！", "")
            cut = max(2, len(clean) // 2)
            hint = text[:cut] if len(text) > cut else ""
            p(doc, f"{i}. {hint}____________________", size=14, after=10)
    elif items:
        for i, it in enumerate(items, 1):
            full = it.get("text") or ""
            cut = max(4, len(full) // 2)
            p(doc, f"{i}. {full[:cut]}____________________", size=13, after=8)
            if it.get("who"):
                p(doc, f"　　出处 / 作者：________（提示：{it['who'][:6]}…）", size=11, color=BRAND_DEEP, after=6)

    section(doc, "二、说说意思（用自己的话）")
    if lines_detail:
        for i, ln in enumerate(lines_detail, 1):
            p(doc, f"{i}. 「{(ln.get('text') or '').strip('，。')}」意思是：", size=12, after=4)
            blank(doc, 1)
    elif items:
        for i, it in enumerate(items, 1):
            p(doc, f"{i}. 「{it.get('text') or ''}」意思是：", size=12, after=4)
            blank(doc, 1)
    else:
        blank(doc, 2)

    if acc.get("background"):
        section(doc, "三、背景（选做）")
        p(doc, "用一两句话写出作者或积累提示：", size=12, after=4)
        blank(doc, 2)

    p(doc, "□默写过关　□意思说得清　□错题入档", size=10, color=BRAND_DEEP, before=8)
    return doc


def build_garden_answer(unit_id: str, unit_name: str, garden: dict):
    return _garden_answer_doc(unit_id, garden)


def _garden_answer_doc(unit_id: str, garden: dict):
    acc = garden.get("accumulate") or {}
    doc = tight_doc()
    p(doc, "语文书桌 · 园地参考答案（做完再看）", size=10, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=2)
    p(doc, f"{garden.get('title') or '语文园地'} · 答案", size=16, bold=True, color=BRAND_ORANGE_RED, center=True, after=6)

    items = acc.get("items") or []
    lines = acc.get("lines") or []
    lines_detail = acc.get("linesDetail") or []

    section(doc, "一、默写（全文）")
    if lines:
        if acc.get("author"):
            p(doc, acc["author"], size=12, after=4)
        for ln in lines:
            p(doc, ln, size=14, after=4)
    elif items:
        for it in items:
            p(doc, (it.get("text") or "") + ("　——" + it["who"] if it.get("who") else ""), size=13, after=6)

    section(doc, "二、意思")
    if lines_detail:
        for ln in lines_detail:
            p(doc, (ln.get("text") or "") + "　→　" + (ln.get("tip") or ""), size=12, after=6)
    elif items:
        for it in items:
            p(doc, (it.get("text") or "") + "　→　" + (it.get("tip") or ""), size=12, after=6)
    if acc.get("meaning"):
        p(doc, "大意：" + acc["meaning"], size=12, after=6)
    if acc.get("background"):
        section(doc, "三、背景")
        p(doc, acc["background"], size=12, after=6)
    if garden.get("extra"):
        p(doc, garden["extra"], size=11, color=BRAND_DEEP, after=4)
    return doc


def garden_answer_md(garden: dict) -> str:
    acc = garden.get("accumulate") or {}
    lines_out = [
        f"# {garden.get('title') or '语文园地'}参考答案\n\n",
        "> 做完再看。\n\n",
        "## 默写全文\n\n",
    ]
    if acc.get("lines"):
        if acc.get("author"):
            lines_out.append(acc["author"] + "\n\n")
        lines_out.append("\n".join(acc["lines"]) + "\n\n")
    elif acc.get("items"):
        for it in acc["items"]:
            lines_out.append((it.get("text") or "") + (f"（{it['who']}）" if it.get("who") else "") + "\n\n")
    lines_out.append("## 意思\n\n")
    if acc.get("linesDetail"):
        for ln in acc["linesDetail"]:
            lines_out.append(f"- {ln.get('text') or ''} → {ln.get('tip') or ''}\n")
        lines_out.append("\n")
    elif acc.get("items"):
        for it in acc["items"]:
            lines_out.append(f"- {it.get('text') or ''} → {it.get('tip') or ''}\n")
        lines_out.append("\n")
    if acc.get("meaning"):
        lines_out.append("大意：" + acc["meaning"] + "\n\n")
    if acc.get("background"):
        lines_out.append("## 背景\n\n" + acc["background"] + "\n")
    return "".join(lines_out)


def main():
    data = load_data()
    OUT_L.mkdir(parents=True, exist_ok=True)
    OUT_G.mkdir(parents=True, exist_ok=True)
    OUT_A.mkdir(parents=True, exist_ok=True)
    OUT_GA.mkdir(parents=True, exist_ok=True)
    MD_L.mkdir(parents=True, exist_ok=True)
    MD_G.mkdir(parents=True, exist_ok=True)

    # map existing 1-11 from LESSONS_1_11 for answer regen consistency
    lessons_map = {les["bookNo"]: les for les in LESSONS_1_11}

    index = {
        "lessons": {},
        "gardens": {},
        "sprint": {
            "u1": "printables/sprint/U1-第一单元冲刺.pdf",
            "u2": "printables/sprint/U2-第二单元冲刺.pdf",
            "u3": "printables/sprint/U3-第三单元冲刺.pdf",
        },
    }

    # —— gardens for all units ——
    for unit in data["units"]:
        g = unit.get("garden")
        if not g:
            continue
        uid = unit["id"]
        stem = f"{uid.upper()}-garden"
        save_pair(build_garden_practice(uid, unit["name"], g), OUT_G, stem)
        save_pair(_garden_answer_doc(uid, g), OUT_GA, stem + "-answers")
        md = garden_answer_md(g)
        (MD_G / f"{uid}.md").write_text(md, encoding="utf-8")
        index["gardens"][uid] = {
            "daily": f"printables/gardens/{stem}.pdf",
            "answerPdf": f"printables/garden-answers/{stem}-answers.pdf",
            "answerMd": f"answers/gardens/{uid}.md",
            "answerHtml": render_html(md),
            "title": g.get("title") or uid,
            "sprint": index["sprint"].get(uid),
        }
        print("garden", uid)

    # —— lessons: keep 1-11 files, add 12-27 ——
    for unit in data["units"]:
        for les0 in unit.get("lessons") or []:
            n = les0["bookNo"]
            if n in lessons_map:
                les = lessons_map[n]
            else:
                les = lesson_from_data(unit, les0)
                stem = f"L{n:02d}-{les['title']}-每日10分钟"
                save_pair(build_lesson_doc(les), OUT_L, stem)
                if les.get("recite"):
                    from gen_lesson_printables import build_recite

                    save_pair(build_recite(les), OUT_L, f"L{n:02d}-{les['title']}-背诵默写10分钟")
                # answers for new lessons
                ans_stem = f"L{n:02d}-{les['title']}-答案"
                save_pair(build_lesson_answer_doc(les), OUT_A, ans_stem)
                md = lesson_answer_md(les)
                (MD_L / f"L{n:02d}-{les['title']}-答案.md").write_text(md, encoding="utf-8")
                print("lesson", n, les["title"])

            # always index (1-11 use existing paths)
            title = les["title"]
            daily = f"printables/lessons/L{n:02d}-{title}-每日10分钟.pdf"
            recite = (
                f"printables/lessons/L{n:02d}-{title}-背诵默写10分钟.pdf" if les.get("recite") else None
            )
            ans_pdf = f"printables/answers/L{n:02d}-{title}-答案.pdf"
            ans_md = f"answers/lessons/L{n:02d}-{title}-答案.md"
            # ensure answer md exists for 1-11
            if n in lessons_map:
                md = lesson_answer_md(les)
                md_path = MD_L / f"L{n:02d}-{title}-答案.md"
                if not md_path.exists():
                    md_path.write_text(md, encoding="utf-8")
                # ensure answer pdf exists
                if not (OUT_A / f"L{n:02d}-{title}-答案.pdf").exists():
                    save_pair(build_lesson_answer_doc(les), OUT_A, f"L{n:02d}-{title}-答案")
            else:
                md = (MD_L / f"L{n:02d}-{title}-答案.md").read_text(encoding="utf-8")

            if n in lessons_map:
                md = lesson_answer_md(les)
                (MD_L / f"L{n:02d}-{title}-答案.md").write_text(md, encoding="utf-8")

            index["lessons"][str(n)] = {
                "daily": daily,
                "recite": recite,
                "answerPdf": ans_pdf,
                "answerMd": ans_md,
                "answerHtml": render_html(
                    (MD_L / f"L{n:02d}-{title}-答案.md").read_text(encoding="utf-8")
                    if (MD_L / f"L{n:02d}-{title}-答案.md").exists()
                    else lesson_answer_md(les)
                ),
                "title": title,
            }

    (ROOT / "print-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_G / "README.md").write_text("# 语文园地练习（A4）\n\n`Ux-garden.pdf` 日积月累默写+释义练习。\n", encoding="utf-8")
    (OUT_GA / "README.md").write_text("# 园地答案（A4）\n\n与 `../gardens/` 对应。\n", encoding="utf-8")
    print("done lessons", len(index["lessons"]), "gardens", len(index["gardens"]))


if __name__ == "__main__":
    main()
