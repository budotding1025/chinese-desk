"""Template for generating a student worksheet PDF and an answer PDF.

Copy this file into the working folder for a specific PDF exercise task, then
replace WORKSHEET with the transcribed problems and answers.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path.cwd()
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

TITLE = "练习题"
SUBTITLE = "清晰打印版"

# Replace this with real transcribed worksheet data.
WORKSHEET = [
    {
        "section": "I. Choose the best answer.",
        "questions": [
            {
                "prompt": "Example question ________.",
                "options": ["A. option one", "B. option two", "C. option three", "D. option four"],
                "answer": "A",
                "explanation": "Explain the rule or reasoning here.",
            }
        ],
    }
]


def register_fonts():
    regular_candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path(r"C:\Windows\Fonts\Deng.ttf"),
    ]
    bold_candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\Dengb.ttf"),
    ]

    regular = "Helvetica"
    bold = "Helvetica-Bold"
    for path in regular_candidates:
        if path.exists():
            regular = "WorksheetRegular"
            pdfmetrics.registerFont(TTFont(regular, str(path)))
            break
    for path in bold_candidates:
        if path.exists():
            bold = "WorksheetBold"
            pdfmetrics.registerFont(TTFont(bold, str(path)))
            break
    return regular, bold


FONT, BOLD = register_fonts()


def make_styles():
    base = getSampleStyleSheet()
    ink = colors.HexColor("#050505")
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName=BOLD, fontSize=21, leading=27, alignment=TA_CENTER, textColor=ink),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName=FONT, fontSize=11, leading=16, alignment=TA_CENTER, textColor=ink, spaceAfter=7 * mm),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName=BOLD, fontSize=14, leading=20, textColor=ink, spaceBefore=5 * mm, spaceAfter=3 * mm),
        "normal": ParagraphStyle("normal", parent=base["Normal"], fontName=FONT, fontSize=10.5, leading=16, alignment=TA_LEFT, textColor=ink, spaceAfter=2.5 * mm),
        "small": ParagraphStyle("small", parent=base["Normal"], fontName=FONT, fontSize=9.5, leading=14, alignment=TA_LEFT, textColor=ink),
        "answer": ParagraphStyle(
            "answer",
            parent=base["Normal"],
            fontName=FONT,
            fontSize=10,
            leading=15,
            textColor=ink,
            backColor=colors.HexColor("#F4F7FB"),
            borderColor=colors.HexColor("#D9E2F0"),
            borderWidth=0.5,
            borderPadding=5,
            spaceAfter=3 * mm,
        ),
    }


STYLES = make_styles()


def para(text, style_name="normal"):
    html = escape(text).replace("&lt;br/&gt;", "<br/>").replace("\n", "<br/>")
    return Paragraph(html, STYLES[style_name])


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(18 * mm, 10 * mm, SUBTITLE)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def option_grid(options):
    rows = []
    for start in range(0, len(options), 2):
        rows.append([para(opt, "small") for opt in options[start : start + 2]])
        if len(rows[-1]) == 1:
            rows[-1].append(para("", "small"))
    table = Table(rows, colWidths=[78 * mm, 78 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def build_pdf(path, include_answers):
    story = [para(TITLE, "title"), para(SUBTITLE + (" - 答案详解版" if include_answers else " - 无答案习题版"), "subtitle")]

    for section in WORKSHEET:
        story.append(para(section["section"], "h1"))
        for idx, q in enumerate(section["questions"], 1):
            suffix = "" if include_answers else " ________"
            story.append(para(f"{idx}. {q['prompt']}{suffix}", "normal"))
            if q.get("options"):
                story.append(option_grid(q["options"]))
            if include_answers:
                story.append(para(f"答案：{q['answer']}<br/>讲解：{q['explanation']}", "answer"))
            story.append(Spacer(1, 3 * mm))

    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main():
    build_pdf(OUT / f"{TITLE}-无答案习题.pdf", include_answers=False)
    build_pdf(OUT / f"{TITLE}-答案详解.pdf", include_answers=True)
    print(f"Generated outputs in {OUT}")


if __name__ == "__main__":
    main()
