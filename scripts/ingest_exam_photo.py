# -*- coding: utf-8 -*-
"""拍照/扫描练习卷入库预处理入口。

叠用 PDF-Exercise-Maker 的透视回正，并落到 Chinese Desk 的 units/source。
之后由 Agent 按 .cursor/skills/exam-from-photo + exam-ingest 规则转录排版。

Usage:
  python scripts/ingest_exam_photo.py path/to/photo.jpg --unit u3
  python scripts/ingest_exam_photo.py path/to/folder --unit u3
  python scripts/ingest_exam_photo.py photo.jpg --unit u3 --no-preprocess
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPROCESS = ROOT / "tools" / "pdf-exercise-maker" / "scripts" / "preprocess_worksheet_image.py"
OUT_PRE = ROOT / "output" / "preprocess"

UNIT_DIRS = {
    "u1": "u01-四上第一单元",
    "u2": "u02-四上第二单元",
    "u3": "u03-四上第三单元",
    "u4": "u04-四上第四单元",
    "u5": "u05-四上第五单元",
    "u6": "u06-四上第六单元",
    "u7": "u07-四上第七单元",
    "u8": "u08-四上第八单元",
}

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def collect_images(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in IMAGE_EXT or path.suffix.lower() == ".pdf" else []
    files = []
    for p in sorted(path.iterdir()):
        if p.is_file() and p.suffix.lower() in IMAGE_EXT:
            files.append(p)
    return files


def run_preprocess(src: Path) -> dict:
    OUT_PRE.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(PREPROCESS), str(src), "--out", str(OUT_PRE)]
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=False)
    stem = src.stem
    report = OUT_PRE / f"{stem}-report.json"
    corrected = OUT_PRE / f"{stem}-corrected.png"
    info = {
        "source": str(src),
        "corrected": str(corrected) if corrected.exists() else None,
        "report": str(report) if report.exists() else None,
    }
    if report.exists():
        try:
            info["report_data"] = json.loads(report.read_text(encoding="utf-8"))
        except Exception:
            pass
    return info


def main() -> None:
    ap = argparse.ArgumentParser(description="练习卷照片预处理并落入 units/source")
    ap.add_argument("path", type=Path, help="图片文件或含图片的目录")
    ap.add_argument("--unit", default="u3", help="单元 id，如 u1..u8")
    ap.add_argument("--no-preprocess", action="store_true", help="只拷贝，不跑透视回正")
    args = ap.parse_args()

    src = args.path.resolve()
    if not src.exists():
        raise SystemExit(f"不存在: {src}")
    if not PREPROCESS.exists():
        raise SystemExit(f"缺少 PDF-Exercise-Maker 脚本: {PREPROCESS}")

    unit = args.unit.lower()
    folder_name = UNIT_DIRS.get(unit, f"{unit}-四上单元")
    dest_dir = ROOT / "units" / folder_name / "source"
    dest_dir.mkdir(parents=True, exist_ok=True)

    images = collect_images(src)
    if not images:
        raise SystemExit("未找到图片（jpg/png/…）")

    results = []
    today = date.today().isoformat()
    for i, img in enumerate(images, 1):
        # 保留原图
        raw_name = f"{unit.upper()}-raw-{today}-{i:02d}{img.suffix.lower()}"
        raw_dest = dest_dir / raw_name
        shutil.copy2(img, raw_dest)

        entry = {"raw": str(raw_dest.relative_to(ROOT)), "index": i}
        if not args.no_preprocess and img.suffix.lower() != ".pdf":
            info = run_preprocess(img)
            entry.update(info)
            if info.get("corrected") and Path(info["corrected"]).exists():
                corr_name = f"{unit.upper()}-corrected-{today}-{i:02d}.png"
                corr_dest = dest_dir / corr_name
                shutil.copy2(info["corrected"], corr_dest)
                entry["source_for_ocr"] = str(corr_dest.relative_to(ROOT))
            else:
                entry["source_for_ocr"] = entry["raw"]
        else:
            entry["source_for_ocr"] = entry["raw"]
        results.append(entry)
        print("OK", entry["source_for_ocr"])

    manifest = {
        "unit": unit,
        "date": today,
        "files": results,
        "next": [
            "用 .cursor/skills/exam-from-photo 视觉转录题面",
            "遵守 .cursor/rules/exam-ingest.mdc（田字格/行距/页脚贴底）",
            f"更新 scripts/gen_unit_exams.py build_{unit}() 后: python scripts/gen_unit_exams.py {unit}",
            "更新 gen_pack_answers.py FULL_ANSWERS 并生成答案 PDF",
        ],
    }
    man_path = dest_dir / f"ingest-{today}.json"
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("manifest", man_path.relative_to(ROOT))
    print("下一步：按 exam-from-photo skill 转录并排版。")


if __name__ == "__main__":
    main()
