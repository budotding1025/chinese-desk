# -*- coding: utf-8 -*-
"""Regenerate garden practice+answer PDFs only; refresh print-index gardens."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gen_fill_gaps import (  # noqa: E402
    OUT_G,
    OUT_GA,
    MD_G,
    build_garden_practice,
    _garden_answer_doc,
    garden_answer_md,
    load_data,
)
from gen_lesson_printables import save_pair  # noqa: E402

INDEX_PATH = ROOT / "print-index.json"

OUT_G.mkdir(parents=True, exist_ok=True)
OUT_GA.mkdir(parents=True, exist_ok=True)
MD_G.mkdir(parents=True, exist_ok=True)

DATA = load_data()
index = {}
if INDEX_PATH.exists():
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
index.setdefault("gardens", {})
index.setdefault("lessons", {})
index.setdefault("sprint", index.get("sprint") or {})
index.setdefault("full", index.get("full") or {})

for unit in DATA.get("units") or []:
    g = unit.get("garden")
    if not g:
        continue
    uid = unit["id"]
    stem = f"{uid.upper()}-garden"
    save_pair(build_garden_practice(uid, unit["name"], g), OUT_G, stem)
    save_pair(_garden_answer_doc(uid, g), OUT_GA, stem + "-answers")
    md = garden_answer_md(g)
    (MD_G / f"{uid}.md").write_text(md, encoding="utf-8")
    html_parts = [f"<h2>{g.get('title') or '语文园地'}答案</h2><p class='meta'>做完再看</p>"]
    acc = g.get("accumulate") or {}
    html_parts.append("<h3>默写全文</h3>")
    if acc.get("lines"):
        for ln in acc["lines"]:
            html_parts.append(f"<p>{ln}</p>")
    elif acc.get("items"):
        for it in acc["items"]:
            html_parts.append(f"<p>{it.get('text') or ''}</p>")
    html_parts.append("<h3>根据意思写原句</h3>")
    src = acc.get("linesDetail") or acc.get("items") or []
    for it in src:
        tip = (it.get("tip") or "").strip()
        text = (it.get("text") or "").strip()
        if tip and text:
            html_parts.append(f"<p>- 意思：{tip}<br>原句：{text}</p>")
    if acc.get("background"):
        html_parts.append(f"<h3>背景</h3><p>{acc['background']}</p>")
    prev = index["gardens"].get(uid) or {}
    index["gardens"][uid] = {
        "daily": f"printables/gardens/{stem}.pdf",
        "answerPdf": f"printables/garden-answers/{stem}-answers.pdf",
        "answerMd": f"answers/gardens/{uid}.md",
        "answerHtml": "".join(html_parts),
        "title": g.get("title") or uid,
        "sprint": prev.get("sprint"),
    }
    print("ok", uid)

INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
print("index gardens", len(index["gardens"]))
