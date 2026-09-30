# -*- coding: utf-8 -*-
"""Generate sample printable Word + PDF for Chinese Desk."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "printables"
STEM = "sample-u01-四上示例-迷你练习"
DOCX_PATH = OUT_DIR / f"{STEM}.docx"
PDF_PATH = OUT_DIR / f"{STEM}.pdf"


def set_run_font(run, name_cn: str = "宋体", size: float = 11, bold: bool = False, color=None):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = name_cn
    if color is not None:
        run.font.color.rgb = RGBColor(*color)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), name_cn)


def add_para(
    doc,
    text: str,
    *,
    size=11,
    bold=False,
    space_after=6,
    align=None,
    first_line=None,
    color=None,
):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    if first_line is not None:
        pf.first_line_indent = first_line
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color)
    return p


def add_blank_line(doc, count: int = 1):
    for _ in range(count):
        add_para(doc, "", size=10, space_after=4)


def build_doc() -> Document:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)

    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(11)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    add_para(
        doc,
        "语文书桌 · Chinese Desk",
        size=16,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
        color=BRAND_ORANGE_RED,
    )
    add_para(
        doc,
        "四上 · 示例单元 · 迷你练习（考前 8–15 分钟）",
        size=13,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=2,
        color=BRAND_DEEP,
    )
    add_para(
        doc,
        "定位：查漏补缺 · 非每日作业　|　做完先自批，只补错的部分　|　示例卷，正式内容待教材到位后替换",
        size=9,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
        color=BRAND_ORANGE_YELLOW,
    )
    add_para(doc, "姓名：__________　　日期：__________　　用时：____ 分钟", size=10, space_after=10, color=INK)

    # —— 一、字词 ——
    add_para(doc, "一、字词（约 4 分钟）", size=12, bold=True, space_after=6, color=BRAND_ORANGE_RED)

    add_para(doc, "1. 看拼音写词语", size=11, bold=True, space_after=4, color=BRAND_DEEP)
    add_para(doc, "cháo　xī　　　　jù　shuō　　　　dà　dī", size=11, space_after=2)
    add_para(doc, "________　　　　________　　　　________", size=11, space_after=6)
    add_para(doc, "táo　zuì　　　　pàn　wàng　　　　zhèn　ěr　yù　lóng", size=11, space_after=2)
    add_para(doc, "________　　　　________　　　　____________________", size=11, space_after=8)

    add_para(doc, "2. 形近字组词", size=11, bold=True, space_after=4)
    add_para(doc, "潮（　　　）　朝（　　　）　提（　　　）　堤（　　　）", size=11, space_after=4)
    add_para(doc, "盼（　　　）　扮（　　　）", size=11, space_after=8)

    add_para(doc, "3. 多音字：给加点字选择正确读音（打 ✓）", size=11, bold=True, space_after=4)
    add_para(doc, "（1）观潮　　cháo（　）　zhāo（　）", size=11, space_after=3)
    add_para(doc, "（2）朝阳　　cháo（　）　zhāo（　）", size=11, space_after=3)
    add_para(doc, "（3）处理　　chǔ（　）　chù（　）", size=11, space_after=3)
    add_para(doc, "（4）到处　　chǔ（　）　chù（　）", size=11, space_after=10)

    # —— 二、园地 ——
    add_para(doc, "二、语文园地（约 4 分钟）", size=12, bold=True, space_after=6, color=BRAND_ORANGE_RED)

    add_para(doc, "4. 古诗填空（《暮江吟》· 白居易）", size=11, bold=True, space_after=4)
    add_para(doc, "一道残阳铺水中，________________。", size=11, space_after=4)
    add_para(doc, "可怜九月初三夜，________________。", size=11, space_after=8)

    add_para(doc, "5. 上下句配对（把正确答案的序号填在括号里）", size=11, bold=True, space_after=4)
    add_para(doc, "① 老大徒伤悲　　② 下笔如有神　　③ 梅花香自苦寒来", size=10, space_after=4)
    add_para(doc, "（　）少壮不努力，____________。", size=11, space_after=3)
    add_para(doc, "（　）读书破万卷，____________。", size=11, space_after=3)
    add_para(doc, "（　）宝剑锋从磨砺出，____________。", size=11, space_after=10)

    # —— 三、短阅读 ——
    add_para(doc, "三、短阅读（约 5–7 分钟）", size=12, bold=True, space_after=6, color=BRAND_ORANGE_RED)
    add_para(doc, "阅读短文，完成练习。", size=10, space_after=4)

    passage = (
        "钱塘江大潮，自古以来被称为天下奇观。"
        "农历八月十八是一年中潮水最大的一天。"
        "潮来之前，江面很平静。可是过了一会儿，远处出现了一条白线，那条白线很快地向前移动，逐渐拉长、变粗，横贯江面。"
        "再近些，只见白浪翻滚，形成一道两丈多高的水墙。"
        "浪潮越来越近，犹如千万匹白色战马齐头并进，浩浩荡荡地飞奔而来；那声音如同山崩地裂，好像大地都被震得颤动起来。"
        "过了好久，潮头才奔腾西去。看看堤下，江水已经涨了两丈来高了。"
    )
    add_para(doc, passage, size=10.5, space_after=8, first_line=Cm(0.74))

    add_para(doc, "6. 本文主要写的是（　）。", size=11, space_after=2)
    add_para(doc, "A. 钱塘江的风景　　B. 钱塘江大潮的壮观　　C. 农历八月的习俗", size=10, space_after=6)

    add_para(doc, "7. 判断：潮来之前，江面已经翻起很高的浪。（　）（对打√，错打×）", size=11, space_after=6)

    add_para(doc, "8. 判断：潮头奔腾西去之后，堤下江水几乎没有变化。（　）", size=11, space_after=6)

    add_para(doc, "9. 短文用「千万匹白色战马齐头并进」写潮来时的什么？（用自己的话答一句）", size=11, space_after=2)
    add_para(doc, "________________________________________________________________", size=11, space_after=2)
    add_para(doc, "________________________________________________________________", size=11, space_after=12)

    # —— 参考答案 ——
    add_para(
        doc,
        "———————— 以下为参考答案（做完再看） ————————",
        size=10,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
        color=BRAND_ORANGE_YELLOW,
    )
    add_para(doc, "一、字词", size=11, bold=True, space_after=4, color=BRAND_ORANGE_RED)
    add_para(doc, "1. 潮汐　据说　大堤　陶醉　盼望　震耳欲聋", size=10, space_after=3)
    add_para(doc, "2. 潮（浪潮）朝（朝阳）提（提醒）堤（堤坝）盼（盼望）扮（扮演）（合理即可）", size=10, space_after=3)
    add_para(doc, "3. （1）cháo　（2）zhāo　（3）chǔ　（4）chù", size=10, space_after=6)

    add_para(doc, "二、语文园地", size=11, bold=True, space_after=4, color=BRAND_ORANGE_RED)
    add_para(doc, "4. 半江瑟瑟半江红；露似真珠月似弓。", size=10, space_after=3)
    add_para(doc, "5. ①；②；③（少壮不努力—老大徒伤悲；读书破万卷—下笔如有神；宝剑锋从磨砺出—梅花香自苦寒来）", size=10, space_after=6)

    add_para(doc, "三、短阅读", size=11, bold=True, space_after=4, color=BRAND_ORANGE_RED)
    add_para(doc, "6. B　7. ×　8. ×　9. 写出潮来时声势浩大、气势勇猛（意思对即可）。", size=10, space_after=6)
    add_para(doc, "另见 answers/sample-u01-四上示例-参考答案.md", size=9, space_after=0)

    return doc


def docx_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    """Convert via Microsoft Word COM (Windows)."""
    import win32com.client  # type: ignore

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(docx_path.resolve()))
        # 17 = wdFormatPDF
        doc.SaveAs(str(pdf_path.resolve()), FileFormat=17)
        doc.Close(False)
    finally:
        word.Quit()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = build_doc()
    doc.save(str(DOCX_PATH))
    print(f"Wrote {DOCX_PATH}")

    try:
        import win32com.client  # noqa: F401
    except ImportError:
        print("pywin32 not installed; trying PowerShell COM fallback…", file=sys.stderr)
        ps = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('{DOCX_PATH.resolve()}')
$doc.SaveAs([ref]'{PDF_PATH.resolve()}', [ref]17)
$doc.Close($false)
$word.Quit()
"""
        import subprocess

        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
        print(f"Wrote {PDF_PATH}")
        return 0

    docx_to_pdf(DOCX_PATH, PDF_PATH)
    print(f"Wrote {PDF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
