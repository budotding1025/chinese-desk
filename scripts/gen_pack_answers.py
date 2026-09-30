# -*- coding: utf-8 -*-
"""Generate printable A4 answer pages for 单元冲刺 + 完整摸底卷; update print-index.

Full-exam answers are compressed to fit on ONE A4 page.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from docx_utils import docx_to_pdf, set_run_font
from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

ROOT = Path(__file__).resolve().parents[1]
OUT_SA = ROOT / "printables" / "sprint-answers"
OUT_FA = ROOT / "printables" / "full-answers"
INDEX = ROOT / "print-index.json"

SPRINT_ANSWERS = {
    "u1": {
        "title": "第一单元冲刺 · 参考答案",
        "lines": [
            ("h", "一、看拼音写词语"),
            "繁星、模糊、浩浩荡荡、山崩地裂、鹅卵石、逐渐",
            ("h", "二、多音 / 错读"),
            "观潮 cháo；朝阳 zhāo；霎时 shà；萤火虫 yíng",
            ("h", "三、园地默写"),
            "《鹿柴》：空山不见人，但闻人语响。返景入深林，复照青苔上。",
            "《赠刘景文》：一年好景君须记，最是橙黄橘绿时。",
            ("h", "四、仿写 / 五、短阅读"),
            "忽然……过了一会儿……（通顺即可）。潮来声势相关题：意思对即可。",
        ],
    },
    "u2": {
        "title": "第二单元冲刺 · 参考答案",
        "lines": [
            ("h", "一、字词"),
            "身份、揭晓、注视、的确、证明、蝙蝠、呼风唤雨",
            ("h", "二、选字 / 多音"),
            "提纲、井冈山、纲要；即使、既然、立即；具体、俱乐部、俱备",
            "蝙蝠 biān；一溜烟 liù；避开 bì",
            ("h", "三、改写 + 园地"),
            "并列展开：……的时候……，……的时候……，……的时候也……",
            "设问：是谁……呢？当然是……。",
            "人非生而知之者，孰能无惑？博学之，审问之，慎思之，明辨之，笃行之。善疑者，不疑人之所疑，而疑人之所不疑。",
            ("h", "四、阅读"),
            "词语意思对即可；能按内容/写法/生活分类提问即可。",
        ],
    },
    "u3": {
        "title": "第三单元冲刺 · 参考答案",
        "lines": [
            ("h", "一、字词"),
            "光滑、嫩绿、爬山虎、均匀、空隙、住宅、慎重",
            ("h", "二、多音 / 错别字"),
            "投降 xiáng / 降低 jiàng；歌曲 qǔ / 曲折 qū；茎 jīng；谨慎 shèn",
            "痕迹；平坦；触角",
            ("h", "三、诗句 / 俗语"),
            "横看成岭侧成峰，远近高低各不同；缘＝因为",
            "一场秋雨一场寒，十场秋雨要穿棉",
            ("h", "四、观察 + 阅读"),
            "仿写写出变化即可；潜伏：隐藏、埋伏。",
        ],
    },
}

# Compact one-page keys for full exams
FULL_ANSWERS = {
    "u1": {
        "title": "第一单元完整摸底卷 · 参考答案",
        "lines": [
            ("h", "一、看拼音写词语"),
            "繁星；模糊；飞舞；柔和；梦幻",
            ("h", "二、读音有误"),
            "1.③（萤火虫 yíng）　2.②（霎时 shà）　3.无（均正确；若③印成 qiāo 则选③）",
            ("h", "三、错别字"),
            "1.蜜→密　2.近→进　3.浙→渐",
            ("h", "四、填空"),
            "第六笔：横；“外围”选②（四周；周围）",
            ("h", "五、词语补充"),
            "①细②无③云④悄⑤私⑥欲；1.①②④⑤；2.画面描写通顺即可",
            ("h", "六、片段描写"),
            "用上加点时间词、通顺即可",
            ("h", "七、古诗"),
            "宋　苏轼　（②）",
            ("h", "八、阅读"),
            "（一）1.②淡紫色、①文雅　2.画：却也能为一个可怜的蚂蚁遮阳　3.小花；善良/坚强等",
            "（二）1.③北戴河日出　2.非常广阔、没有边际　3.画面想象通顺即可　4.兴奋/赞美等",
            ("h", "九、习作"),
            "略（地点清楚、特别之处与推荐理由）",
        ],
    },
    "u2": {
        "title": "第二单元完整摸底卷 · 参考答案",
        "lines": [
            ("h", "一、看拼音写词语"),
            "身份；揭晓；注视；的确；证明",
            ("h", "二、加点字读音"),
            "qiú；biān；bì；yíng；liù；rāng",
            ("h", "三、选字组词"),
            "提纲、井冈山、纲要；泡沫、末尾、飞沫；即使、既然、立即；具体、俱乐部、俱备",
            ("h", "四、改写"),
            "1.那盏灯晴天的时候亮着，阴天的时候亮着，雨天的时候也亮着。",
            "2.是谁把家里打扫得干干净净呢？当然是妈妈。",
            ("h", "五、日积月累"),
            "人非生而知之者；不学不成，不问不知（以教材为准）；博学/审问/慎思/明辨/笃行；不疑人之所疑，而疑人之所不疑",
            ("h", "六、阅读"),
            "（一）笼罩：像笼子罩住/乌云遮盖；画形成过程句；分类提问即可",
            "（二）画掉：托管、嘱托、预备（留：接替、嘱咐、预先）；口若悬河；无计可施；纸上谈兵；印象言之有理即可",
            ("h", "七、习作"),
            "略（事例具体，写出人物特点）",
        ],
    },
    "u3": {
        "title": "第三单元完整摸底卷 · 参考答案（第1–2页）",
        "lines": [
            ("h", "一、看拼音写词语"),
            "光滑；嫩绿；爬山虎；均匀；空隙",
            ("h", "二、加点字读音"),
            "1.投降 xiáng；降低 jiàng　2.歌曲 qǔ；曲折 qū　3.茎 jīng；谨慎 shèn",
            ("h", "三、选择"),
            "1.（1）③痕际→痕迹　（2）②平担→平坦　（3）②触脚→触角　2.②（缘＝因为）",
            ("h", "四、填空"),
            "1.一场秋雨一场寒，十场秋雨穿上棉　2.横看成岭侧成峰，远近高低各不同",
            "3.示例：更喜欢小明（观察细腻/有比喻/写出变化）",
            ("h", "五、阅读（米虫）"),
            "潜伏：隐藏、埋伏；文中指米虫藏在米里。",
            "（第3–4页待补）",
        ],
    },
}


def tight_doc(*, margin=1.4):
    from docx import Document
    from docx.oxml.ns import qn

    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(margin)
    sec.right_margin = Cm(margin)
    sec.top_margin = Cm(1.1)
    sec.bottom_margin = Cm(1.1)
    st = doc.styles["Normal"]
    st.font.name = "宋体"
    st.font.size = Pt(10)
    st._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    return doc


def add_p(doc, text, *, size=10, bold=False, color=None, center=False, after=2, before=0, font="宋体"):
    para = doc.add_paragraph()
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(before)
    para.paragraph_format.space_after = Pt(after)
    para.paragraph_format.line_spacing = 1.05
    run = para.add_run(text)
    set_run_font(run, name_cn=font, size=size, bold=bold, color=color or INK)
    return para


def save_pair(doc, folder: Path, stem: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    docx = folder / f"{stem}.docx"
    pdf = folder / f"{stem}.pdf"
    doc.save(str(docx))
    try:
        docx_to_pdf(docx, pdf)
    except Exception as e:
        print("COM pdf fail", e)
        import subprocess

        ps = (
            f"$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
            f"$d=$w.Documents.Open('{docx}'); "
            f"$d.SaveAs([string]'{pdf}',17); $d.Close(); $w.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)
    print("OK", pdf.name if pdf.exists() else docx.name)
    return pdf


def build_answer_page(title: str, lines: list, *, one_page: bool = True):
    doc = tight_doc(margin=1.3 if one_page else 1.5)
    add_p(doc, "语文书桌 · 参考答案（做完再看）", size=8, bold=True, color=BRAND_ORANGE_YELLOW, center=True, after=1)
    add_p(doc, title, size=13, bold=True, color=BRAND_ORANGE_RED, center=True, after=1, font="黑体")
    add_p(doc, "单独答案页 · 尽量一页打完　|　先做卷再对答案", size=8, center=True, after=4, color=BRAND_DEEP)
    for item in lines:
        if isinstance(item, tuple) and item and item[0] == "h":
            add_p(doc, item[1], size=10, bold=True, color=BRAND_ORANGE_RED, before=4, after=1)
        else:
            add_p(doc, str(item), size=9.5, after=1)
    add_p(doc, "□已对答案　□错题已入档", size=9, color=BRAND_DEEP, before=6)
    return doc


def main():
    OUT_SA.mkdir(parents=True, exist_ok=True)
    OUT_FA.mkdir(parents=True, exist_ok=True)

    sprint_ans = {}
    for uid, meta in SPRINT_ANSWERS.items():
        stem = f"{uid.upper()}-sprint-answers"
        doc = build_answer_page(meta["title"], meta["lines"], one_page=True)
        save_pair(doc, OUT_SA, stem)
        sprint_ans[uid] = f"printables/sprint-answers/{stem}.pdf"
        # md sidecar
        md_lines = []
        for it in meta["lines"]:
            if isinstance(it, tuple):
                md_lines.append(f"## {it[1]}")
            else:
                md_lines.append(it)
        (ROOT / "answers" / f"{uid}-sprint-参考答案.md").write_text(
            f"# {meta['title']}\n\n> 对应单元冲刺卷\n\n" + "\n\n".join(md_lines) + "\n",
            encoding="utf-8",
        )

    full_ans = {}
    stems = {"u1": "u01-full-answers", "u2": "u02-full-answers", "u3": "u03-full-answers"}
    for uid, meta in FULL_ANSWERS.items():
        doc = build_answer_page(meta["title"], meta["lines"], one_page=True)
        save_pair(doc, OUT_FA, stems[uid])
        full_ans[uid] = f"printables/full-answers/{stems[uid]}.pdf"

    index = {}
    if INDEX.exists():
        index = json.loads(INDEX.read_text(encoding="utf-8"))
    index["sprintAnswers"] = sprint_ans
    index["fullAnswers"] = full_ans
    for key in ("sprint", "full", "sprintAnswers", "fullAnswers"):
        if key in index and isinstance(index[key], dict):
            index[key] = {k: str(v).replace("\\", "/") for k, v in index[key].items()}
    # ensure full/sprint ascii paths remain
    index.setdefault("sprint", {})
    index.setdefault("full", {})
    index["sprint"].update(
        {
            "u1": "printables/sprint/U1-sprint.pdf",
            "u2": "printables/sprint/U2-sprint.pdf",
            "u3": "printables/sprint/U3-sprint.pdf",
        }
    )
    index["full"].update(
        {
            "u1": "printables/full/u01-full.pdf",
            "u2": "printables/full/u02-full.pdf",
            "u3": "printables/full/u03-full.pdf",
        }
    )
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("index fullAnswers", full_ans)

    (OUT_SA / "README.md").write_text("# 单元冲刺 · 答案（A4 · 一页）\n", encoding="utf-8")
    (OUT_FA / "README.md").write_text("# 完整摸底卷 · 答案（A4 · 尽量一页）\n", encoding="utf-8")


if __name__ == "__main__":
    main()
