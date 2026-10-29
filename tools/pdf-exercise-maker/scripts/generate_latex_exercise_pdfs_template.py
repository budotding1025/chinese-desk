"""XeLaTeX template for clean worksheet and answer PDFs.

Copy this file into the working folder for a specific exercise task, then
replace WORKSHEET with visually transcribed content. Use LaTeX math syntax for
all formulas so the generated PDFs remain readable and printable.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path.cwd()
OUT = ROOT / "output" / "pdf"
BUILD = OUT / "latex-build"
OUT.mkdir(parents=True, exist_ok=True)
BUILD.mkdir(parents=True, exist_ok=True)

TITLE = "练习题"
SUBTITLE = "清晰打印版"

# Replace this with real transcribed worksheet data.
# Fields ending in "_tex" may contain LaTeX commands and math expressions.
WORKSHEET = [
    {
        "section_tex": "一、填空题",
        "questions": [
            {
                "prompt_tex": r"计算：$\displaystyle \lim_{n\to\infty}\sum_{i=1}^{n}\frac{1}{(-5)^i}=\underline{\hspace{3cm}}$。",
                "answer_tex": r"$-\frac{1}{6}$",
                "explanation_tex": (
                    r"这是等比数列求和。首项为 $-\frac{1}{5}$，公比为 $-\frac{1}{5}$，"
                    r"且 $|q|<1$，所以无穷和为 $\frac{a_1}{1-q}"
                    r"=\frac{-1/5}{1+1/5}=-\frac{1}{6}$。"
                ),
            },
            {
                "prompt_tex": r"下列说法正确的是（\quad）。",
                "options_tex": [
                    r"A. $\sqrt{n}$ 一定是整数",
                    r"B. 任意两个正整数都有公因数 $1$",
                    r"C. $\frac{1}{a}+\frac{1}{b}=\frac{1}{a+b}$",
                    r"D. 若 $a>b$，则 $\frac{1}{a}>\frac{1}{b}$",
                ],
                "answer_tex": r"B",
                "explanation_tex": r"任意两个正整数都至少有公因数 $1$，其余选项均不恒成立。",
            },
        ],
    }
]


def find_xelatex() -> str:
    found = shutil.which("xelatex")
    if found:
        return found

    candidates = [
        Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "xelatex.exe",
        Path(r"C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise SystemExit(
        "xelatex was not found. Install MiKTeX first, for example:\n"
        "winget install --id MiKTeX.MiKTeX --scope user "
        "--accept-package-agreements --accept-source-agreements --silent"
    )


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def tex_preamble(title: str, include_answers: bool) -> str:
    version = "答案详解版" if include_answers else "无答案习题版"
    return rf"""\documentclass[12pt]{{article}}
\usepackage[a4paper,left=18mm,right=18mm,top=18mm,bottom=18mm]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\usepackage{{amsmath,amssymb}}
\usepackage{{enumitem}}
\usepackage{{fancyhdr}}
\usepackage[most]{{tcolorbox}}
\usepackage{{xcolor}}
\setmainfont{{Times New Roman}}
\setCJKmainfont{{Microsoft YaHei}}
\linespread{{1.18}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{7pt}}
\setlist[enumerate]{{leftmargin=*, itemsep=9pt, topsep=4pt}}
\pagestyle{{fancy}}
\fancyhf{{}}
\lhead{{{latex_escape(SUBTITLE)}}}
\rhead{{{version}}}
\cfoot{{第 \thepage 页}}
\definecolor{{answerbg}}{{HTML}}{{F4F7FB}}
\definecolor{{answerline}}{{HTML}}{{D9E2F0}}
\newtcolorbox{{answerbox}}{{colback=answerbg,colframe=answerline,boxrule=0.5pt,arc=1mm,left=5pt,right=5pt,top=5pt,bottom=5pt}}
\begin{{document}}
\begin{{center}}
{{\LARGE\bfseries {latex_escape(title)}}}\\[4pt]
{{\large {latex_escape(SUBTITLE)} -- {version}}}
\end{{center}}
\vspace{{4pt}}
"""


def render_question(question: dict, number: int, include_answers: bool) -> list[str]:
    lines = [rf"\item {question['prompt_tex']}"]

    options = question.get("options_tex") or []
    if options:
        lines.append(r"\begin{enumerate}[label=\Alph*.,itemsep=3pt,topsep=3pt]")
        for option in options:
            cleaned = option
            if len(cleaned) > 2 and cleaned[1] in ".、":
                cleaned = cleaned[2:].strip()
            lines.append(rf"\item {cleaned}")
        lines.append(r"\end{enumerate}")

    if include_answers:
        lines.append(r"\begin{answerbox}")
        lines.append(rf"\textbf{{答案：}}{question['answer_tex']}\\")
        lines.append(rf"\textbf{{讲解：}}{question['explanation_tex']}")
        lines.append(r"\end{answerbox}")

    return lines


def build_tex(include_answers: bool) -> str:
    lines = [tex_preamble(TITLE, include_answers)]
    for section in WORKSHEET:
        lines.append(rf"\section*{{{section['section_tex']}}}")
        lines.append(r"\begin{enumerate}")
        for idx, question in enumerate(section["questions"], 1):
            lines.extend(render_question(question, idx, include_answers))
        lines.append(r"\end{enumerate}")
    lines.append(r"\end{document}")
    return "\n".join(lines)


def compile_tex(tex_path: Path) -> None:
    xelatex = find_xelatex()
    cmd = [
        xelatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory",
        str(BUILD),
        str(tex_path),
    ]
    for _ in range(2):
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            log_path = BUILD / f"{tex_path.stem}.log"
            raise SystemExit(
                f"XeLaTeX failed for {tex_path.name}.\n"
                f"Command: {' '.join(cmd)}\n"
                f"Log: {log_path}\n"
                f"STDOUT:\n{result.stdout[-4000:]}\nSTDERR:\n{result.stderr[-2000:]}"
            )


def write_and_compile(stem: str, include_answers: bool) -> Path:
    tex_path = BUILD / f"{stem}.tex"
    tex_path.write_text(build_tex(include_answers), encoding="utf-8")
    compile_tex(tex_path)
    pdf_path = BUILD / f"{stem}.pdf"
    final_path = OUT / f"{TITLE}-{stem}.pdf"
    shutil.copy2(pdf_path, final_path)
    return final_path


def main() -> None:
    student_pdf = write_and_compile("无答案习题", include_answers=False)
    answer_pdf = write_and_compile("答案详解", include_answers=True)
    print(f"Generated: {student_pdf}")
    print(f"Generated: {answer_pdf}")


if __name__ == "__main__":
    main()
