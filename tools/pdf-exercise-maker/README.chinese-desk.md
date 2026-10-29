# PDF-Exercise-Maker × 语文书桌

来源：[VeryInt/PDF-Exercise-Maker](https://github.com/VeryInt/PDF-Exercise-Maker)（vendoring 关键脚本，非 git submodule）。

## 在本仓库怎么用

1. **照片回正**  
   `python tools/pdf-exercise-maker/scripts/preprocess_worksheet_image.py photo.jpg`

2. **入库预处理（推荐）**  
   `python scripts/ingest_exam_photo.py photo.jpg --unit u3`  
   → 原图 + corrected 进 `units/.../source/`，并写 manifest。

3. **Agent 流程**  
   读 `.cursor/skills/exam-from-photo/SKILL.md`，并遵守 `.cursor/rules/exam-ingest.mdc`。

4. **四上单元卷**  
   优先 `scripts/gen_unit_exams.py`（田字格/小学书写），不要只用上游 XeLaTeX 通用模板硬套。

5. **零散卷**  
   可整理 `worksheet.json` 后：  
   `python tools/pdf-exercise-maker/scripts/make_worksheet_pdf.py worksheet.json`

## 更新上游

网络可用时重新拉取：

```powershell
# 示例：刷新脚本
Invoke-WebRequest https://raw.githubusercontent.com/VeryInt/PDF-Exercise-Maker/main/pdf-exercise-maker/scripts/preprocess_worksheet_image.py -OutFile tools/pdf-exercise-maker/scripts/preprocess_worksheet_image.py
```

或在网络正常时 `git clone` 到临时目录再复制 `pdf-exercise-maker/`。
