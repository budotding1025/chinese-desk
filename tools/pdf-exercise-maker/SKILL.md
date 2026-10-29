---
name: pdf-exercise-maker
description: Turn scanned PDFs or worksheet images/photos into clean printable worksheets and separate answer-explanation PDFs. Use when the user provides a workbook, worksheet, exam paper, practice sheet, scanned PDF, JPG, PNG, or phone photo and asks to remove answers, keep choices/options, create a student version, create a teacher/answer version, extract worksheet content, or produce detailed explanations.
---

# PDF Exercise Maker

## Goal

Create two polished, printable outputs from a source exercise PDF or worksheet image:

- A **student worksheet** with answers, handwritten marks, circles, and hints removed while preserving prompts, blanks, choices, and problem order.
- An **answer/explanation PDF** containing the complete worksheet plus answers and concise teaching explanations.

Also create an editable transcription file when the source PDF has no embedded text or when manual correction is needed.

For math-heavy worksheets, formulas, fractions, limits, sums, roots, vectors, geometry notation, or any content where formula readability matters, use **XeLaTeX** as the default PDF generator.

## Core Workflow

1. **Inspect the source first.**
   - For PDFs, use `pypdf` or `pdfplumber` to check page count and whether text extraction returns real content.
   - For JPG/PNG/photos, inspect the image directly and crop/enhance locally if that improves readability.
   - If a worksheet photo is tilted, perspective-skewed, dark, or surrounded by background, run the optional image preprocessor before visual transcription:

     ```powershell
     python scripts/preprocess_worksheet_image.py worksheet.jpg
     ```

   - The preprocessor prefers any installed package that provides `cv2`. If OpenCV is missing, ask the user before installing `opencv-python-headless`; if the user declines or installation fails, use the Pillow fallback output.
   - If extraction text is empty or garbled, treat the source as scanned/image-based and rely on rendered images plus visual transcription.
   - Preserve the original source file; do not overwrite it.

2. **Render or inspect pages visually.**
   - Prefer available PDF rendering tools or existing page images.
   - If Poppler/PyMuPDF is unavailable, use any reliable local preview path and clearly record that visual verification was manual/browser-based.
   - Check for handwritten answers, circled choices, cross-page questions, missing sections, and blurry regions.
   - If the worksheet contains geometry diagrams, function graphs, multiple-choice option diagrams, pattern figures, or real-object images, ask once at the start for the diagram strategy instead of asking per problem. Recommend `source_crop_first` unless the user has a strong preference.

3. **Transcribe into structured data.**
   - Keep every problem, blank, and multiple-choice option.
   - Remove student answers and markings from the student version.
   - For answer keys, reason from the subject matter; do not blindly copy handwritten answers when they conflict with grammar/math/content.
   - Mark uncertain or blurry source text in the transcription, and prefer a human-review note over pretending certainty.
   - For repeatable generation, write a worksheet data file first. Prefer `worksheet.json` because it needs no extra Python dependencies; use `worksheet.yaml` only when PyYAML is available.
   - For math-heavy content, store display-ready formulas in `prompt_tex`, `options_tex`, `answer_tex`, and `explanation_tex`.
   - For geometry diagrams, coordinate axes, function graphs, grids, pattern figures, and simple construction drawings, store TikZ code in `figure_tex` for one diagram or `figures_tex` for multiple diagrams.
   - If the diagram shape or labels cannot be confidently redrawn, crop the original figure locally and store the path in `figure_image` or `figure_images`.
   - When using cropped figures, include a small margin on all sides. Avoid tight crops that cut off arrowheads, labels, curve endpoints, captions, or pattern edges.

4. **Generate outputs.**
   - Write final artifacts under `output/pdf/`.
   - Recommended outputs:
     - `<source-name>-卷面转录.md`
     - `<source-name>-无答案习题.pdf`
     - `<source-name>-答案详解.pdf`
   - Use **XeLaTeX** for generated PDFs when formulas or Chinese/math mixed typography matter.
   - If `xelatex` is missing, install a LaTeX distribution before generating:
     - Windows user-scope preferred: `winget install --id MiKTeX.MiKTeX --scope user --accept-package-agreements --accept-source-agreements --silent`
     - Admin shell alternative: `choco install miktex -y --no-progress`
   - After installing MiKTeX, verify with `xelatex --version`. If PATH has not refreshed, call the full path, commonly `C:\Users\<user>\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.
   - Use `reportlab` only as a fallback for simple non-math worksheets, or when the user explicitly accepts less precise formula rendering.
   - Prefer clear printable typography: near-black text, readable Chinese/English font, moderate line spacing, enough room for handwritten answers.
   - Prefer the bundled command generator for new work:

     ```powershell
     python scripts/make_worksheet_pdf.py worksheet.json
     ```

     If the skill has been copied into a working project, call the copied script path instead.

5. **Verify before finishing.**
   - Extract text from generated PDFs and check that the student version does not contain answer markers such as `答案：` or `讲解：`.
   - Check that the answer version contains answers and explanations.
   - Open or render sample pages to confirm no乱码, clipping, overlap, unwanted blank pages, literal HTML tags such as `<br/>`, or overly faint text.
   - Re-run the generation command after cleanup to confirm outputs are reproducible.

## Photo Preprocessing

Use `scripts/preprocess_worksheet_image.py` before transcription when a phone photo is rotated, shot at an angle, dim, low contrast, or includes distracting table/background areas.

```powershell
python scripts/preprocess_worksheet_image.py input.jpg
python scripts/preprocess_worksheet_image.py input.jpg --backend auto
python scripts/preprocess_worksheet_image.py input.jpg --backend opencv
python scripts/preprocess_worksheet_image.py input.jpg --backend pillow
python scripts/preprocess_worksheet_image.py input.jpg --install-opencv
```

Outputs are written to `output/preprocess/` by default:

```text
<name>-corrected.png
<name>-preview.png
<name>-report.json
```

Rules:

- OpenCV is preferred because it can detect paper contours, find four corners, and apply perspective correction.
- OpenCV does not judge whether worksheet text is readable. It only detects geometry such as paper edges, contours, and rotation.
- Perspective correction depends on finding a reliable four-corner page contour. If this fails, the output may only be enhanced or lightly deskewed.
- Check `<name>-report.json`: `perspective_corrected=false` means the image was not truly perspective-corrected.
- OpenCV is an optional runtime dependency. Do not bundle OpenCV into the `.skill` package.
- Prefer `opencv-python-headless` for this skill because GUI functions such as `cv2.imshow` are not needed.
- If either `opencv-python` or `opencv-python-headless` is already installed and provides `cv2`, use it as-is. Do not uninstall or replace it.
- If `cv2` is missing, ask the user before installing it. Suggested command: `pip install opencv-python-headless pillow`.
- In a normal local shell, `--install-opencv` can attempt that installation automatically. In Codex or other agent environments, request user permission first.
- If the user does not want to install OpenCV, or if installation fails, continue with the Pillow fallback.
- The Pillow fallback handles small in-plane rotation, conservative cropping, auto-contrast, and light sharpening. It does not promise strong perspective correction.
- Keep the original source photo. Use the corrected image for transcription only after visual inspection.
- Severe page curl, heavy shadows, fingers covering text, or blurry areas still require human review or a better photo.

## Diagram Strategy

When a worksheet includes geometry diagrams, function graphs, option diagrams, pattern figures, or real-object images, choose one diagram strategy at the beginning:

- `source_crop_first` (recommended): use padded crops from the original image for complex or irregular figures; use TikZ only for simple regular diagrams that can be reproduced exactly.
- `tikz_when_safe`: use TikZ for rectangles, triangles, coordinate axes, simple line graphs, and other clearly specified diagrams; use padded source crops for everything uncertain.
- `tikz_first`: redraw most diagrams in TikZ only when the user explicitly prefers a fully re-typeset look. Mark uncertain diagrams for review.

Rules:

- Do not redraw irregular geometry by approximation. If arcs, intersections, angle marks, proportions, or label placement affect the answer, prefer `figure_image`.
- For real objects, decorative patterns, dense option diagrams, and figures with uncertain curves, prefer padded source crops.
- If a source crop would include handwritten answers, red pen marks, or calculation notes, do not use it in the student worksheet. Use a clean schematic and mark the item for review.
- Do not ask for diagram strategy problem by problem. Ask once up front, apply the chosen strategy consistently, and record it in the transcription notes.

## Output Quality Rules

- Keep multiple-choice options in the student worksheet.
- Do not erase by painting over scanned pages unless the user explicitly wants a scan-like edit; default to a clean re-typeset worksheet.
- Keep page breaks natural. Avoid forced `PageBreak()` unless a new section truly needs a new page.
- Use stronger fonts if the PDF looks faint. With XeLaTeX, prefer Windows CJK fonts such as `Microsoft YaHei`, `SimSun`, or `DengXian`; keep body text near black and avoid thin gray strokes.
- For math, write formulas in LaTeX source, for example `$\lim_{n\to\infty}\sum_{i=1}^{n}\frac{1}{(-5)^i}$`, not as plain slash text.
- For drawings, prefer padded source crops unless the figure is simple, regular, and can be recreated exactly. Recreate clean teaching diagrams only when the geometry is certain.
- If a figure is too complex to redraw reliably, crop the original figure as an image and note that the image is retained for human review; do not invent unseen labels or geometry.
- Do not use AI image generation to recreate worksheet diagrams unless the user explicitly asks for an illustrative replacement. For worksheets, cropped source figures are more faithful than generated images.
- Crop images with enough padding for print readability. A slightly larger crop with clean surrounding paper is better than a tight crop that clips the figure. If padding would include answers or red marks, crop conservatively and add a review note.
- For answer explanations, explain the rule or reasoning for each problem, not only the final answer.
- Keep old temporary renderings, screenshots, and helper scripts out of the final folder unless they are needed for reproducibility.

## Suggested Implementation Pattern

For most new worksheets, use the data-driven generator `scripts/make_worksheet_pdf.py`:

1. If the source is a tilted or perspective-skewed photo, run `python scripts/preprocess_worksheet_image.py source.jpg` first and inspect the corrected preview.
2. Create `worksheet.json` from the visual transcription.
3. Put plain readable text in `prompt`, `answer`, and `explanation`.
4. Put LaTeX-rich text in `prompt_tex`, `options_tex`, `answer_tex`, and `explanation_tex` when formulas are needed.
5. Run `python scripts/make_worksheet_pdf.py worksheet.json`.
6. Verify `output/pdf/<title>-无答案习题.pdf`, `output/pdf/<title>-答案详解.pdf`, and `output/pdf/<title>-卷面转录.md`.

Diagram notes:

- `figure_tex` is inserted below the question/options in both PDFs.
- `figures_tex` accepts a list when one question needs multiple diagrams.
- TikZ code should be complete, usually starting with `\begin{tikzpicture}` and ending with `\end{tikzpicture}`.
- Use `scale`, `baseline`, and compact coordinates to keep figures printable inside an A4 worksheet.
- `figure_image` inserts a cropped source image below the question/options in both PDFs.
- `figure_images` accepts a list of paths, or objects such as `{"path": "assets/q13.png", "width": "0.5\\linewidth"}`.
- Prefer `figure_image` for diagrams where the curve, angle mark, proportion, intersection, or label placement is visually important and uncertain.
- Use padded crop filenames such as `q13_crop_padded.png` when a crop is intentionally preserved with margin. Verify the rendered PDF page, not only the raw crop image.

Use this minimal JSON shape:

```json
{
  "title": "数学练习题",
  "subtitle": "清晰打印版",
  "source": "IMG_1923.JPG",
  "notes": "题面模糊处已标注需复核。",
  "sections": [
    {
      "title": "一、填空题",
      "questions": [
        {
          "no": 1,
          "prompt": "计算：lim(n→∞) Σ(i=1..n) 1/(-5)^i = ________.",
          "prompt_tex": "计算：$\\\\displaystyle \\\\lim_{n\\\\to\\\\infty}\\\\sum_{i=1}^{n}\\\\frac{1}{(-5)^i}=\\\\fillblank$.",
          "answer": "-1/6",
          "answer_tex": "$-\\\\frac{1}{6}$",
          "explanation": "这是无穷等比级数求和。",
          "explanation_tex": "这是首项为 $-\\\\frac15$、公比为 $-\\\\frac15$ 的无穷等比级数。",
          "figure_tex": "\\\\begin{tikzpicture}[scale=0.55]\\\\draw[->] (0,0)--(4,0) node[right] {$x$};\\\\draw[->] (0,0)--(0,3) node[above] {$y$};\\\\draw (0,0)--(2,2.5)--(3.5,0);\\\\end{tikzpicture}"
        }
      ]
    }
  ]
}
```

For one-off custom layouts, `scripts/generate_latex_exercise_pdfs_template.py` remains available as a starting point:

1. Copy the template into the user's working folder.
2. Replace the `WORKSHEET` data with the transcribed problems and answers.
3. Write formulas in LaTeX syntax in `prompt_tex`, `options_tex`, `answer_tex`, and `explanation_tex`.
4. Adjust title, filenames, fonts, and spacing.
5. Run the script with the available Python runtime. It writes `.tex` files and compiles them with XeLaTeX.
6. Verify the generated PDFs with `pypdf` and visual inspection.

For simple language worksheets with little or no formula notation, `scripts/generate_exercise_pdfs_template.py` remains available as a ReportLab fallback:

1. Copy the template into the user's working folder.
2. Replace the `WORKSHEET` data with the transcribed problems and answers.
3. Adjust title, filenames, and styles.
4. Run the script with the available Python runtime.
5. Verify the generated PDFs with `pypdf` and visual inspection.

The templates are intentionally simple. They give stable generation structures without pretending OCR, visual transcription, or answer reasoning can be fully automated.

## XeLaTeX Smoke Test

Before producing a math worksheet, compile a minimal Chinese/math document:

```tex
\documentclass[12pt]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb}
\setmainfont{Times New Roman}
\setCJKmainfont{Microsoft YaHei}
\begin{document}
数学公式：$\displaystyle \lim_{n\to\infty}\sum_{i=1}^{n}\frac{1}{(-5)^i}$。
\end{document}
```

Run:

```powershell
xelatex -interaction=nonstopmode -halt-on-error test.tex
```

If MiKTeX prompts for missing packages, allow package installation or configure MiKTeX package auto-install, then rerun. Do not ship math PDFs until this smoke test or the project generator compiles successfully.

## Common Validation Snippet

```python
from pathlib import Path
from pypdf import PdfReader

for name in ["无答案习题.pdf", "答案详解.pdf"]:
    r = PdfReader(str(Path("output/pdf") / name))
    text = "\n".join((page.extract_text() or "") for page in r.pages)
    print(name, len(r.pages), "<br/>" in text, "答案：" in text, "讲解：" in text)
```

Expected pattern:

- Student worksheet: no `答案：`, no `讲解：`, no literal `<br/>`.
- Answer PDF: contains `答案：` and `讲解：`, no literal `<br/>`.

## Handoff

When the task is complete, record:

- Source type: text PDF, scanned/image PDF, or worksheet photo/image.
- Final output paths.
- Generation command.
- Fonts/rendering tools used, including the `xelatex` path/version for math-heavy worksheets.
- Validation performed.
- Any uncertain transcription items or answers needing human review.
