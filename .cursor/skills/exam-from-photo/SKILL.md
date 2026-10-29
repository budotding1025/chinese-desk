---
name: exam-from-photo
description: >-
  从手机拍照/扫描的语文练习卷、单元测、资料页生成可打印高清 PDF（无答案卷 + 答案）。
  叠用 VeryInt/PDF-Exercise-Maker 的预处理与转录流程，并强制遵守 Chinese Desk
  小学生书写版面规则（田字格、作答行距、页脚贴底）。用户发试卷照片、扫描件、
  JPG/PNG、或说「录入卷子」「重排高清」「拍照出 PDF」时使用。
---

# 拍照/扫描练习卷 → 语文书桌高清 PDF

本 skill = **PDF-Exercise-Maker 工作流** + **Chinese Desk `exam-ingest` 硬规则**。

## 何时用

- 用户发来：单元练习卷照片、扫描 PDF、教辅截图
- 用户说：录入 / 入库 / 高清重排 / 可打印 / 配答案

## 工具路径（本仓库已 vendoring）

| 用途 | 命令 |
| --- | --- |
| 照片回正 | `python tools/pdf-exercise-maker/scripts/preprocess_worksheet_image.py <图>` |
| 通用习题 JSON→PDF | `python tools/pdf-exercise-maker/scripts/make_worksheet_pdf.py worksheet.json` |
| 一键预处理+落源 | `python scripts/ingest_exam_photo.py <图或目录> --unit u3` |
| 四上单元摸底卷 | `scripts/gen_unit_exams.py` + `scripts/docx_utils.py`（田字格/页脚） |
| 答案页 | `scripts/gen_pack_answers.py` |

上游说明：`tools/pdf-exercise-maker/SKILL.md`（VeryInt/PDF-Exercise-Maker）。

## 必须叠加的书写规则

完整条文见 `.cursor/rules/exam-ingest.mdc`。执行时不可省略：

1. 田字格约 **1.0–1.15cm**，禁止压到 0.7 以下  
2. 作答横线用 `write_lines`（字号≥16、行距够高）；简答≥2 行  
3. 页脚用 `end_exam_page` / `set_section_footer` **贴纸张底**，禁止正文里假页脚悬半页  
4. 禁止「上半截挤满、下半截大片空」——用放大作答区/段距/田字格填满  
5. 出处行保留（选自…有删改）；答案另出 full-answers + markdown  

若走 XeLaTeX/`make_worksheet_pdf.py` 通用通道：仍须保证填空线够高、行距够大；语文单元卷**优先走 Desk 的 docx 管道**（田字格更稳）。

## 推荐流程（Agent）

### A. 四上语文「单元练习 / 摸底卷」（默认）

1. 原图拷到 `units/u0N-…/source/`（可用 `ingest_exam_photo.py`）。  
2. 倾斜/透视 → 跑 `preprocess_worksheet_image.py`，用 `*-corrected.png` 看题。  
3. **视觉转录**全文（可 RapidOCR 辅助，但必须人工校对）。  
4. 写入/更新 `scripts/gen_unit_exams.py` 的 `build_uN()`，遵守 exam-ingest。  
5. `python scripts/gen_unit_exams.py uN`  
6. 更新 `scripts/gen_pack_answers.py` 的 FULL_ANSWERS → 生成答案 PDF。  
7. 更新 `print-index.json`、`answers/u0N-….md`、单元 README。  
8. 预览首页：田字格能否写、作答行、页脚是否贴底。

### B. 零散练习 / 非单元结构卷

1. 预处理照片。  
2. 整理成 `worksheet.json`（格式见 `tools/pdf-exercise-maker/SKILL.md`）。  
3. JSON 的 `notes` 写上：`chinese-desk exam-ingest: 大空格/高行距`。  
4. `python tools/pdf-exercise-maker/scripts/make_worksheet_pdf.py worksheet.json`  
5. 需要入库 Desk 路径时，再把 PDF 拷到 `printables/` 并登记 `print-index.json`。

### 图形策略

默认 `source_crop_first`：复杂图带留白裁切；简单规则图可重绘。不要用 AI 乱画几何图。

## 自检清单

- [ ] 学生版无「答案：」「讲解：」  
- [ ] 田字格 ≥1cm；作答行够高  
- [ ] 页脚在纸张底部  
- [ ] 无「不完整/待补」字样（完整卷）  
- [ ] 原扫描仍在 `units/.../source/`  

## 对用户可说的话

处理完成后给出：练习 PDF 路径、答案 PDF 路径、是否跑过预处理、需人工复核的模糊处。
