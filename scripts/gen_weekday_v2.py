# -*- coding: utf-8 -*-
"""Generate dense A4 weekday sheets: 默写过关 + 考点练习 (JPG-like layout)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

from curriculum import UNITS
from docx_utils import docx_to_pdf, set_run_font
from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

ROOT = Path(__file__).resolve().parents[1]
OUT_D = ROOT / "printables" / "weekday" / "dictation"
OUT_P = ROOT / "printables" / "weekday" / "practice"
ANS = ROOT / "answers"


def tight_doc() -> Document:
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    # JPG-like: tighter margins
    sec.left_margin = Cm(1.2)
    sec.right_margin = Cm(1.2)
    sec.top_margin = Cm(1.0)
    sec.bottom_margin = Cm(1.0)
    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(10.5)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.08
    return doc


def p(doc, text, *, size=10.5, bold=False, color=None, center=False, after=2, before=0):
    para = doc.add_paragraph()
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(before)
    para.paragraph_format.space_after = Pt(after)
    para.paragraph_format.line_spacing = 1.08
    run = para.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color or INK)
    return para


def section(doc, text):
    p(doc, text, size=11, bold=True, color=BRAND_ORANGE_RED, before=4, after=3)


def grids_for_word(doc, pinyin: str, n_chars: int):
    """One row: pinyin + n square cells (approx 田字格)."""
    cols = 1 + n_chars
    table = doc.add_table(rows=2, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = True
    # pinyin cell spans conceptually in first col row0
    cell0 = table.cell(0, 0)
    cell0.merge(table.cell(1, 0))
    cell0.text = pinyin
    for para in cell0.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in para.runs:
            r.font.size = Pt(8)
            r.font.name = "宋体"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    for i in range(n_chars):
        top = table.cell(0, i + 1)
        bot = table.cell(1, i + 1)
        top.text = ""
        bot.text = ""
        # set approximate square width
        for cell in (top, bot):
            cell.width = Cm(0.85)
            for para in cell.paragraphs:
                para.paragraph_format.space_before = Pt(0)
                para.paragraph_format.space_after = Pt(0)
    # thin spacer paragraph
    p(doc, "", after=1)


def save_pair(doc, folder: Path, stem: str):
    folder.mkdir(parents=True, exist_ok=True)
    docx = folder / f"{stem}.docx"
    pdf = folder / f"{stem}.pdf"
    doc.save(str(docx))
    print("Wrote", docx.relative_to(ROOT))
    try:
        docx_to_pdf(docx, pdf)
    except Exception:
        import subprocess

        ps = (
            f"$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
            f"$d=$w.Documents.Open('{docx.resolve()}'); "
            f"$d.SaveAs([ref]'{pdf.resolve()}',[ref]17); $d.Close($false); $w.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    print("Wrote", pdf.relative_to(ROOT))


def build_dictation(unit, lesson):
    doc = tight_doc()
    p(doc, "语文书桌 · Chinese Desk", size=9, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=1)
    p(
        doc,
        f"工作日①默写过关 · {unit['name']} · 第{lesson['no']}课 {lesson['title']}（{lesson['kind']}）",
        size=13,
        bold=True,
        color=BRAND_ORANGE_RED,
        center=True,
        after=2,
    )
    p(doc, "姓名：________　日期：________　用时：____分钟　□字词过关　□背诵过关", size=9, after=3)
    p(doc, "先做默写；全对或订正后再做「工作日②考点练习」。错题记入错题档案。", size=8, color=BRAND_DEEP, after=4)

    section(doc, "一、看拼音，写词语（田字格，写大些）")
    words = lesson.get("words") or []
    if not words and lesson.get("write_chars"):
        # fall back: write chars individually with blank pinyin space
        chars = lesson["write_chars"]
        line = "　".join(f"（　）{c}" for c in chars[:12])
        p(doc, "会写字（听写/看拼音由家长报）：" + "".join(chars), size=10, after=2)
        p(doc, "默写区（每个字写一遍）：", size=9)
        # big blank lines for handwriting
        for _ in range(3):
            p(doc, "______________________________________________________________", size=12, after=6)
    else:
        for zh, py in words:
            p(doc, py, size=9, after=0)
            # wide writing line instead of tiny boxes (JPG uses grids; lines are more reliable in Word)
            blanks = "□" * max(2, len(zh))
            p(doc, f"{'　'.join('□' for _ in zh)}　　（词语：{len(zh)}字）", size=14, after=6)

    if lesson.get("write_chars"):
        section(doc, "二、会写字（每个字写正确、写工整）")
        chars = lesson["write_chars"]
        # chunk 8 per line
        for i in range(0, len(chars), 8):
            chunk = chars[i : i + 8]
            p(doc, "　".join(f"{c}□" for c in chunk), size=14, after=8)

    if lesson.get("confusable"):
        section(doc, "三、形近字组词")
        parts = []
        for a, b in lesson["confusable"]:
            parts.append(f"{a}（　　　）　{b}（　　　）")
        for i in range(0, len(parts), 2):
            p(doc, "　　".join(parts[i : i + 2]), size=10.5, after=6)

    if lesson.get("recite"):
        section(doc, "四、课文片段默写（背诵要求）")
        p(doc, lesson["recite"]["label"], size=9, color=BRAND_DEEP, after=2)
        p(doc, lesson["recite"]["prompt"], size=10.5, after=4)
        p(doc, "______________________________________________________________", size=12, after=4)
        p(doc, "______________________________________________________________", size=12, after=4)
    elif lesson.get("note"):
        section(doc, "四、本课提示")
        p(doc, lesson["note"], size=10, after=4)

    p(doc, "□ 默写过关（错≤2且已订正）→ 可做工作日②　　□ 未过关 → 明日重默错字", size=9, color=BRAND_ORANGE_RED, before=6)
    p(doc, f"语文书桌 · 默写 · {lesson['id']}", size=8, color=BRAND_ORANGE_YELLOW, center=True, before=6)
    return doc


def build_practice(unit):
    """Unit-level exam-skill practice after dictation pass — dense like JPG."""
    doc = tight_doc()
    p(doc, "语文书桌 · Chinese Desk", size=9, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=1)
    p(
        doc,
        f"工作日②考点练习 · {unit['name']}（8–15分钟）",
        size=13,
        bold=True,
        color=BRAND_ORANGE_RED,
        center=True,
        after=1,
    )
    p(doc, "前置：本单元相关课默写已过关。　姓名：________　日期：________", size=9, after=2)
    p(doc, "题型对齐单元测：字词·多音·字义·园地·仿写·短阅读。错题入档。", size=8, color=BRAND_DEEP, after=4)

    # collect polyphones / words from lessons
    polys = []
    confs = []
    for les in unit["lessons"]:
        polys.extend(les.get("polyphones") or [])
        confs.extend(les.get("confusable") or [])

    section(doc, "一、多音字（在正确读音下画√）")
    if polys:
        for i, (word, opts, _) in enumerate(polys[:6], 1):
            p(doc, f"{i}. {word}　（{'　'.join(opts)}）", size=10.5, after=4)
    else:
        p(doc, "（本单元多音较少，复习园地读音即可）", size=9, after=3)

    section(doc, "二、形近字 / 错别字")
    if confs:
        line = "　".join(f"{a}（　　）{b}（　　）" for a, b in confs[:4])
        p(doc, line, size=10.5, after=4)
    p(doc, "圈出错字并改正：①蜜密麻麻（　　）　②齐头并近（　　）　③痕际（　　）", size=10.5, after=5)

    section(doc, "三、园地默写与理解")
    g = unit.get("garden") or {}
    if g.get("poem"):
        poem = g["poem"]
        p(doc, f"默写《{poem['title']}》（{poem['author']}）：", size=10, after=2)
        for _ in poem["lines"]:
            p(doc, "________________________________________________", size=11, after=3)
    if g.get("quotes"):
        p(doc, "填空：", size=10, after=2)
        p(doc, "人非生而知之者，____________________。", size=10.5, after=3)
        p(doc, "博____之，审____之，慎____之，明____之，笃____之。", size=10.5, after=3)
        p(doc, "善疑者，不疑________疑，而疑________疑。", size=10.5, after=4)
    if g.get("sayings"):
        for s in g["sayings"]:
            # show first half as hint style blank
            p(doc, "俗语：一场秋雨一场寒，____________________。", size=10.5, after=3)
    if g.get("also"):
        for a in g["also"]:
            p(doc, a, size=8, color=BRAND_DEEP, after=2)

    section(doc, "四、句型仿写（1～2题）")
    if unit["id"] == "u2":
        p(doc, "照样子改写：那盏灯晴天、阴天、雨天的时候都亮着。", size=10, after=1)
        p(doc, "→ 那盏灯晴天的时候亮着，阴天的时候亮着，雨天的时候也亮着。", size=9, after=2)
        p(doc, "原句：小鸟早上、中午、傍晚的时候都唱歌。", size=10, after=2)
        p(doc, "改写：________________________________________________", size=11, after=5)
        p(doc, "________________________________________________", size=11, after=5)
    else:
        p(doc, "用上「忽然／霎时／过了一会儿」写两三句，描写一种景物或小动物：", size=10, after=2)
        p(doc, "________________________________________________", size=11, after=5)
        p(doc, "________________________________________________", size=11, after=5)
        p(doc, "________________________________________________", size=11, after=5)

    section(doc, "五、短阅读（少量选择/判断/简答）")
    if unit["id"] == "u1":
        p(
            doc,
            "浪潮越来越近，犹如千万匹白色战马齐头并进，浩浩荡荡地飞奔而来；那声音如同山崩地裂。",
            size=10,
            after=3,
        )
        p(doc, "1. 判断：这句话主要写潮来前的平静。（　　）√/×", size=10.5, after=3)
        p(doc, "2. 选择：「齐头并进」表现潮的（　　）A.温度 B.声势 C.颜色", size=10.5, after=3)
        p(doc, "3. 用自己的话说说加点句好在哪里：", size=10.5, after=2)
        p(doc, "________________________________________________", size=11, after=5)
    elif unit["id"] == "u2":
        p(doc, "夏天热空气上升，到高空遇冷凝结成雨，这叫对流雨。", size=10, after=3)
        p(doc, "1. 「笼罩」意思：____________________", size=10.5, after=4)
        p(doc, "2. 判断：对流雨与空气上下流动有关。（　　）", size=10.5, after=3)
        p(doc, "3. 针对内容提一个问题：________________________________？", size=10.5, after=4)
    else:
        p(doc, "米虫有时钻进米里，潜伏片刻，又从那端钻出来。", size=10, after=3)
        p(doc, "1. 「潜伏」意思：____________________", size=10.5, after=4)
        p(doc, "2. 作者主要在（　　）A.编故事 B.仔细观察描写 C.说明有毒", size=10.5, after=3)
        p(doc, "3. 「缘」在「只缘身在此山中」中的意思：（　　）A.可惜 B.因为 C.谦逊", size=10.5, after=4)

    p(doc, "□本题有错 → 记入错题档案（类型：多音/组词/园地/仿写/阅读）", size=8, color=BRAND_DEEP, before=4)
    p(doc, f"语文书桌 · 考点练习 · {unit['id']}", size=8, color=BRAND_ORANGE_YELLOW, center=True, before=4)
    return doc


def write_answers():
    ANS.mkdir(exist_ok=True)
    lines = ["# 工作日默写 / 考点练习 · 参考答案\n", "> 课文原句以教材为准；开放题意思对即可。\n"]
    for unit in UNITS:
        lines.append(f"\n## {unit['name']}\n")
        for les in unit["lessons"]:
            lines.append(f"### 第{les['no']}课 {les['title']}（默写）\n")
            if les.get("words"):
                lines.append("- 词语：" + "；".join(w for w, _ in les["words"]) + "\n")
            if les.get("write_chars"):
                lines.append("- 会写字：" + "".join(les["write_chars"]) + "\n")
            if les.get("recite"):
                lines.append(f"- 片段：{les['recite']['answer']}\n")
        lines.append("\n### 考点练习要点\n")
        if unit["id"] == "u1":
            lines.append("- 多音：潮 cháo；朝阳 zhāo；闷雷 mèn\n- 错字：密；进；迹\n- 阅读：1× 2B\n")
        elif unit["id"] == "u2":
            lines.append("- 园地：孰能无惑；学问思辨行；人之所 / 人之所不\n- 仿写句式对即可\n")
        else:
            lines.append("- 俗语：十场秋雨穿上棉\n- 潜伏：隐藏\n- 缘：因为（B）\n")
    (ANS / "weekday-dictation-practice-参考答案.md").write_text("".join(lines), encoding="utf-8")
    print("answers written")


def main():
    for unit in UNITS:
        for les in unit["lessons"]:
            if les["kind"] == "略读" and not les.get("words") and not les.get("write_chars"):
                continue
            stem = f"{unit['id']}-l{les['no']:02d}-{les['title']}-默写过关"
            save_pair(build_dictation(unit, les), OUT_D, stem)
        stem_p = f"{unit['id']}-考点练习-8至15分钟"
        save_pair(build_practice(unit), OUT_P, stem_p)
    write_answers()
    print("done")


if __name__ == "__main__":
    main()
