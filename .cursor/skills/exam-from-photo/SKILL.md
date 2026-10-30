---
name: exam-from-photo
description: >-
  从手机拍照/扫描/截图的语文练习卷生成可打印清晰 PDF（Word 宋体重排，非贴图）。
  用户发试卷照片、扫描件、JPG/PNG、截图，或说「录入卷子」「重排高清」「拍照出 PDF」
  「入库」「可打印」时必须使用。强制：python-docx + Word 打印导出、宋体正文/黑体标题。
---

# 拍照/截图练习卷 → Word 清晰可打印 PDF

**默认且唯一合格交付**：用 **Microsoft Word 管道重排** 出矢量清晰 PDF，不是把截图嵌进 PDF。

本 skill = **PDF-Exercise-Maker 预处理** + **Desk `exam-ingest` 硬规则**。  
全局约定见用户级 Skill `exam-from-photo`：**正文宋体 + 标题黑体**。

## 何时用（一律走本流程）

- 用户发来：单元练习卷**照片、截图、扫描 PDF、教辅图**
- 用户说：录入 / 入库 / 高清重排 / 可打印 / 配答案 / 上线

## 清晰排版铁律

| 项 | 要求 |
| --- | --- |
| 排版引擎 | `scripts/gen_unit_exams.py` + `scripts/docx_utils.py`（`exam_doc`） |
| 导出 | `docx_to_pdf()` → Word `ExportAsFixedFormat`（打印质量） |
| 正文 | **宋体** `EXAM_FONT`，纯黑 |
| 标题/大题 | **黑体** `EXAM_FONT_TITLE` |
| 拼音 | Times New Roman |
| 禁止 | 扫描图当学生卷交付 |
| 田字格 | 高清 PNG，约 **1.2–1.35cm** |
| 笔画冷僻字 | `add_stroke_choice_row`（图示+横折/竖/提/点） |

完整条文：`.cursor/rules/exam-ingest.mdc`。

## 工具路径

| 用途 | 命令 |
| --- | --- |
| 照片回正 | `python tools/pdf-exercise-maker/scripts/preprocess_worksheet_image.py <图>` |
| 一键预处理+落源 | `python scripts/ingest_exam_photo.py <图或目录> --unit uN` |
| 单元摸底卷 | `python scripts/gen_unit_exams.py uN` |
| 答案页 | `python scripts/gen_pack_answers.py uN`（或全量） |

## Agent 标准流程（单元卷 · 默认）

1. 原图 → `units/u0N-…/source/`（可 `ingest_exam_photo.py`）。  
2. 预处理 → `*-corrected.png` 看题。  
3. **视觉转录**全文（OCR 可辅助，必须校对）。  
4. 写/更新 `build_uN()`：宋体管道 + exam-ingest 书写规则。  
5. `python scripts/gen_unit_exams.py uN` → `.docx` + `.pdf`。  
6. 答案：`gen_pack_answers` → `full-answers` + markdown。  
7. `print-index.json`、单元 README；上线则 bump `?v=`。  
8. 交付：练习 PDF + docx、答案 PDF、页数；清晰度以 Word/本机打印为准。

## 自检清单

- [ ] 学生版无「答案：」「讲解：」  
- [ ] 正文宋体、标题黑体  
- [ ] 田字格 ≥1.2cm 级；作答行够高  
- [ ] 页脚在纸张底部  
- [ ] 同时有可打开的 `.docx`  
- [ ] 原扫描在 `units/.../source/`  
