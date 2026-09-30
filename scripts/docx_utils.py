# -*- coding: utf-8 -*-
"""Shared Word helpers for Chinese Desk printables (橙红/橙黄主色)."""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

ROOT = Path(__file__).resolve().parents[1]


def new_doc() -> Document:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    # A4 小学生练习：左右留白接近单元测卷
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    return doc


def set_run_font(run, name_cn="宋体", size=12, bold=False, color=None):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = name_cn
    if color is not None:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), name_cn)


def add_para(
    doc,
    text="",
    *,
    size=10.5,
    bold=False,
    space_after=4,
    space_before=0,
    align=None,
    first_line=None,
    color=None,
    font="宋体",
):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if first_line is not None:
        pf.first_line_indent = first_line
    if text:
        run = p.add_run(text)
        set_run_font(run, name_cn=font, size=size, bold=bold, color=color)
    return p


def add_runs(doc, parts, *, size=10.5, space_after=4, align=None, first_line=None):
    """parts: list of (text, bold, color) or str."""
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if first_line is not None:
        pf.first_line_indent = first_line
    for part in parts:
        if isinstance(part, str):
            text, bold, color = part, False, INK
        else:
            text, bold, color = part[0], part[1] if len(part) > 1 else False, part[2] if len(part) > 2 else INK
        run = p.add_run(text)
        set_run_font(run, size=size, bold=bold, color=color)
    return p


def header_block(doc, title: str, note: str = ""):
    add_para(
        doc,
        "语文书桌 · Chinese Desk",
        size=9,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=2,
        color=BRAND_ORANGE_YELLOW,
    )
    add_para(
        doc,
        title,
        size=16,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
        color=BRAND_ORANGE_RED,
        font="黑体",
    )
    add_para(
        doc,
        "学校：__________　班级：__________　姓名：__________　成绩：__________",
        size=10,
        space_after=6,
        color=INK,
    )
    if note:
        add_para(doc, note, size=8, space_after=6, color=BRAND_DEEP, align=WD_ALIGN_PARAGRAPH.CENTER)


def section_title(doc, text: str):
    add_para(doc, text, size=12, bold=True, space_before=8, space_after=8, color=BRAND_ORANGE_RED)


def footer_line(doc, text: str):
    add_para(doc, text, size=8, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=0, color=BRAND_ORANGE_YELLOW)


def _set_cell_border(cell, **kwargs):
    """kwargs: top/left/bottom/right -> {'sz': '4', 'val': 'single', 'color': '000000'} or None to clear."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge in ("top", "left", "bottom", "right"):
        spec = kwargs.get(edge)
        existing = tcBorders.find(qn(f"w:{edge}"))
        if existing is not None:
            tcBorders.remove(existing)
        if not spec:
            continue
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), spec.get("val", "single"))
        el.set(qn("w:sz"), str(spec.get("sz", "12")))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), spec.get("color", "000000"))
        tcBorders.append(el)


def _clear_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    if tbl.tblPr is None:
        tbl.insert(0, tblPr)
    borders = tblPr.first_child_found_in("w:tblBorders")
    if borders is not None:
        tblPr.remove(borders)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)


def add_pinyin_write_grid(doc, items, *, cols=3, py_size=14, gap_after=10):
    """看拼音写词语：三列网格，拼音居中、下方留白横线一一对应（贴近单元测卷）。

    items: list of (zh, py) or py strings.
    """
    from docx.enum.table import WD_TABLE_ALIGNMENT

    pairs = []
    for it in items:
        if isinstance(it, (tuple, list)):
            zh, py = it[0], it[1]
        else:
            zh, py = "", str(it)
        pairs.append((zh, py))

    # usable width ≈ A4 21cm − margins 1.8*2 ≈ 17.4cm
    usable = 17.2
    col_w = usable / cols

    for start in range(0, len(pairs), cols):
        chunk = pairs[start : start + cols]
        table = doc.add_table(rows=1, cols=cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        _clear_table_borders(table)

        for i in range(cols):
            cell = table.cell(0, i)
            cell.width = Cm(col_w)
            cell.text = ""
            para_py = cell.paragraphs[0]
            para_py.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para_py.paragraph_format.space_before = Pt(2)
            para_py.paragraph_format.space_after = Pt(6)
            para_py.paragraph_format.line_spacing = 1.0

            if i < len(chunk):
                zh, py = chunk[i]
                run = para_py.add_run(py)
                set_run_font(run, name_cn="宋体", size=py_size, bold=False, color=INK)
                rPr = run._element.get_or_add_rPr()
                rFonts = rPr.get_or_add_rFonts()
                rFonts.set(qn("w:ascii"), "Times New Roman")
                rFonts.set(qn("w:hAnsi"), "Times New Roman")

                n = max(2, len(zh) if zh else 2)
                para_line = cell.add_paragraph()
                para_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
                para_line.paragraph_format.space_before = Pt(0)
                para_line.paragraph_format.space_after = Pt(4)
                pPr = para_line._p.get_or_add_pPr()
                pBdr = OxmlElement("w:pBdr")
                bottom = OxmlElement("w:bottom")
                bottom.set(qn("w:val"), "single")
                bottom.set(qn("w:sz"), "18")
                bottom.set(qn("w:space"), "10")
                bottom.set(qn("w:color"), "000000")
                pBdr.append(bottom)
                pPr.append(pBdr)
                # 按字数加宽留白，方便小学生书写
                spacer = para_line.add_run("　" * (n + 3))
                set_run_font(spacer, size=16, color=INK)

            _set_cell_border(cell, top=None, left=None, bottom=None, right=None)

        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_before = Pt(0)
        spacer.paragraph_format.space_after = Pt(gap_after)


def exam_doc() -> Document:
    """A4 完整摸底卷：边距贴近小学单元测原卷。"""
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)
    section.top_margin = Cm(1.2)
    section.bottom_margin = Cm(1.2)
    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(10.5)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    return doc


def exam_header(doc, title: str, *, incomplete: bool = False):
    """原卷式页眉：标题 + 学校班级姓名成绩（少装饰、少占高）。"""
    add_para(
        doc,
        title,
        size=15,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
        space_before=0,
        color=INK,
        font="黑体",
    )
    add_para(
        doc,
        "学校：____________　班级：________　姓名：____________　成绩：________",
        size=10,
        space_after=6 if not incomplete else 2,
        color=INK,
    )
    if incomplete:
        add_para(
            doc,
            "（扫描件仅有第 1–2 页 · 第 3–4 页待补）",
            size=8,
            space_after=6,
            color=BRAND_DEEP,
            align=WD_ALIGN_PARAGRAPH.CENTER,
        )


def exam_section(doc, text: str):
    add_para(doc, text, size=11, bold=True, space_before=7, space_after=4, color=INK)


def exam_body(doc, text: str, *, size=10.5, space_after=3, space_before=0, first_line=None, bold=False):
    return add_para(
        doc,
        text,
        size=size,
        bold=bold,
        space_after=space_after,
        space_before=space_before,
        first_line=first_line,
        color=INK,
    )


def exam_footer(doc, text: str):
    add_para(doc, text, size=8, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=0, color=INK)


def write_lines(doc, n: int = 1, *, size=12, space_after=2):
    """作答横线：字号略大，方便手写。"""
    for _ in range(n):
        add_para(
            doc,
            "＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
            size=size,
            space_after=space_after,
            color=INK,
        )


def add_zi_boxes(doc, n: int, *, box_cm: float = 0.82, after: float = 2):
    """田字风格写字格（实线方格），贴近原卷拼音写词留空。"""
    from docx.enum.table import WD_TABLE_ALIGNMENT

    table = doc.add_table(rows=1, cols=n)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    border = {"sz": "12", "val": "single", "color": "000000"}
    for i in range(n):
        cell = table.cell(0, i)
        cell.width = Cm(box_cm)
        cell.text = ""
        # vertical padding so box looks square
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run("　")
        set_run_font(run, size=14, color=INK)
        _set_cell_border(cell, top=border, left=border, bottom=border, right=border)
    # row height ≈ box
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement("w:trHeight")
    trHeight.set(qn("w:val"), str(int(box_cm * 567)))  # cm → twips approx
    trHeight.set(qn("w:hRule"), "atLeast")
    trPr.append(trHeight)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(after)


def add_pinyin_zi_blank(doc, py: str, n: int = 2, *, box_cm: float = 0.82):
    """拼音在上、方格在下（一个词语）。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(py)
    set_run_font(run, size=10, color=INK)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    add_zi_boxes(doc, n, box_cm=box_cm, after=3)


def add_pinyin_sentence(doc, segments, *, size=10.5):
    """segments: str 或 (pinyin, n_chars)。按原卷：正文夹拼音方格。"""
    buf = []
    for seg in segments:
        if isinstance(seg, tuple):
            if buf:
                exam_body(doc, "".join(buf), size=size, space_after=1)
                buf = []
            py, n = seg
            add_pinyin_zi_blank(doc, py, n)
        else:
            buf.append(seg)
    if buf:
        exam_body(doc, "".join(buf), size=size, space_after=4)


def add_page_break(doc):
    doc.add_page_break()


def docx_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        d = word.Documents.Open(str(docx_path.resolve()))
        d.SaveAs(str(pdf_path.resolve()), FileFormat=17)
        d.Close(False)
    finally:
        word.Quit()
