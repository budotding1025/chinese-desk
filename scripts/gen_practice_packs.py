# -*- coding: utf-8 -*-
"""Generate weekday mini + weekend packs for Units 1–3."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

from docx_utils import (
    ROOT,
    add_page_break,
    add_para,
    docx_to_pdf,
    footer_line,
    header_block,
    new_doc,
    section_title,
)
from theme import BRAND_DEEP, BRAND_ORANGE_RED, BRAND_ORANGE_YELLOW, INK

WEEKDAY = ROOT / "printables" / "weekday"
WEEKEND = ROOT / "printables" / "weekend"
ANS = ROOT / "answers"


def save_pair(doc, folder: Path, stem: str):
    folder.mkdir(parents=True, exist_ok=True)
    docx_path = folder / f"{stem}.docx"
    pdf_path = folder / f"{stem}.pdf"
    doc.save(str(docx_path))
    print("Wrote", docx_path.relative_to(ROOT))
    try:
        docx_to_pdf(docx_path, pdf_path)
    except Exception:
        import subprocess

        ps = (
            f"$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
            f"$d=$w.Documents.Open('{docx_path.resolve()}'); "
            f"$d.SaveAs([ref]'{pdf_path.resolve()}',[ref]17); $d.Close($false); $w.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    print("Wrote", pdf_path.relative_to(ROOT))


def wrong_box(doc):
    add_para(
        doc,
        "□ 本题做错 → 记入错题档案（题号 / 类型 / 订正）",
        size=8,
        color=BRAND_DEEP,
        space_after=2,
    )


# ——— Weekday U1 ———
def weekday_u1():
    doc = new_doc()
    header_block(
        doc,
        "工作日迷你 · 四上第一单元（8–15 分钟）",
        "字词 · 园地 · 仿写 · 短阅读　|　错题请勾选并记入错题档案　|　可按推荐日期做，也可自选",
    )
    section_title(doc, "一、字词易错（约 4 分钟）")
    add_para(doc, "1. 看拼音写词语：fán xīng ______　mó hu ______　shà shí ______")
    add_para(doc, "2. 形近字组词：潮（　　）朝（　　）　堤（　　）提（　　）")
    add_para(doc, "3. 多音字选音（画√）：观潮（cháo / zhāo）　朝阳（cháo / zhāo）　闷雷（mēn / mèn）")
    add_para(doc, "4. 字义：「外围」中的「围」更接近哪一种？①环绕拦挡　②四周；周围　③周长　　（　　）")
    wrong_box(doc)

    section_title(doc, "二、园地（约 4 分钟）")
    add_para(doc, "5. 《赠刘景文》作者是____代____。默写：一年好景君须记，____________________。")
    add_para(doc, "6. 上下句配对（填序号）：①老大徒伤悲　②最是橙黄橘绿时")
    add_para(doc, "　　（　　）少壮不努力，________。　（　　）一年好景君须记，________。")
    wrong_box(doc)

    section_title(doc, "三、句型仿写（约 2–3 分钟）")
    add_para(doc, "7. 照样子写：忽然……过了一会儿……")
    add_para(doc, "　　例：忽然风大了，过了一会儿，江面掀起白浪。")
    add_para(doc, "　　写：________________________________________________________________")
    wrong_box(doc)

    section_title(doc, "四、短阅读（约 4–5 分钟）")
    add_para(
        doc,
        "钱塘江大潮来时，浪潮犹如千万匹白色战马齐头并进，浩浩荡荡地飞奔而来；那声音如同山崩地裂。",
        first_line=Cm(0.74),
        size=10,
    )
    add_para(doc, "8. 判断：这句话主要写潮来时的平静。（　　）（√ / ×）")
    add_para(doc, "9. 选择：加点写法主要表现潮的（　　）A. 颜色　B. 声势　C. 温度")
    add_para(doc, "10. 用自己的话说说「齐头并进」在文中的意思：________________________")
    wrong_box(doc)

    add_para(doc, "———————— 参考答案（做完再看） ————————", size=9, bold=True, color=BRAND_ORANGE_YELLOW, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "1. 繁星　模糊　霎时　2. 浪潮/朝阳；堤坝/提醒（合理即可）　3. cháo；zhāo；mèn　4. ②", size=9)
    add_para(doc, "5. 宋　苏轼；最是橙黄橘绿时　6. ①；②　7. 通顺且用上两个词即可　8. ×　9. B　10. 一起向前冲（意思对即可）", size=9)
    footer_line(doc, "语文书桌 · 工作日迷你 · U1　错题 → mistakes/")
    return doc


def weekday_u2():
    doc = new_doc()
    header_block(
        doc,
        "工作日迷你 · 四上第二单元（8–15 分钟）",
        "字词 · 园地 · 仿写 · 短阅读　|　错题请勾选并记入错题档案",
    )
    section_title(doc, "一、字词易错（约 4 分钟）")
    add_para(doc, "1. 看拼音写词语：shēn fèn ______　zhù shì ______　dí què ______　zhèng míng ______")
    add_para(doc, "2. 选字组词：纲/冈　提（　　）　井（　　）山　（　　）要")
    add_para(doc, "　　即/既　（　　）使　（　　）然　立（　　）")
    add_para(doc, "3. 多音字画√：蝙蝠（biān / biǎn）　避开（bì / pì）　一溜烟（liū / liù）　嚷嚷（rāng / rǎng）")
    add_para(doc, "4. 字义：「善疑者，不疑人之所疑」中的「疑」主要指（　　）A. 怀疑提问　B. 生病　C. 忘记")
    wrong_box(doc)

    section_title(doc, "二、园地（约 4 分钟）")
    add_para(doc, "5. 填空：人非生而知之者，____________________。")
    add_para(doc, "6. 博____之，审____之，慎____之，明____之，笃____之。")
    add_para(doc, "7. 善疑者，不疑________疑，而疑________疑。")
    wrong_box(doc)

    section_title(doc, "三、句型仿写（约 2–3 分钟）")
    add_para(doc, "8. 照样子改写：那盏灯晴天、阴天、雨天的时候都亮着。")
    add_para(doc, "　　→ 那盏灯晴天的时候亮着，阴天的时候亮着，雨天的时候也亮着。")
    add_para(doc, "　　原句：小鸟早上、中午、傍晚的时候都唱歌。")
    add_para(doc, "　　改写：________________________________________________________________")
    add_para(doc, "9. 照样子：人类呼风唤雨。→ 是谁呼风唤雨呢？当然是人类。")
    add_para(doc, "　　原句：爸爸把自行车修好了。　改写：________________________________")
    wrong_box(doc)

    section_title(doc, "四、短阅读（约 4 分钟）")
    add_para(
        doc,
        "夏天日照强，地面水分蒸发，近地热空气上升，到高空遇冷，水汽凝结成雨落下——这就是对流雨。",
        first_line=Cm(0.74),
        size=10,
    )
    add_para(doc, "10. 「笼罩」在「乌云笼罩大地」中的意思：________________________")
    add_para(doc, "11. 判断：对流雨形成与空气上下流动有关。（　　）")
    add_para(doc, "12. 对流雨一般有什么特点？（选）A. 常常下很久　B. 多在夏日且往往不久　C. 只在冬天出现　　（　　）")
    wrong_box(doc)

    add_para(doc, "———————— 参考答案（做完再看） ————————", size=9, bold=True, color=BRAND_ORANGE_YELLOW, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "1. 身份　注视　的确　证明　2. 纲；冈；纲　|　即；既；即　3. biān；bì；liù；rāng　4. A", size=9)
    add_para(doc, "5. 孰能无惑　6. 学问思辨行　7. 人之所；人之所不　8–9. 句式对即可　10. 像罩子一样遮盖　11. √　12. B", size=9)
    footer_line(doc, "语文书桌 · 工作日迷你 · U2　错题 → mistakes/")
    return doc


def weekday_u3():
    doc = new_doc()
    header_block(
        doc,
        "工作日迷你 · 四上第三单元（8–15 分钟）",
        "字词 · 园地 · 仿写 · 短阅读　|　错题请勾选并记入错题档案",
    )
    section_title(doc, "一、字词易错（约 4 分钟）")
    add_para(doc, "1. 看拼音写词语：guāng huá ______　nèn lǜ ______　pá shān hǔ ______　kòng xì ______")
    add_para(doc, "2. 多音字画√：投降（jiàng / xiáng）　降温（jiàng / xiáng）　曲折（qǔ / qū）　茎（jīng / jìng）")
    add_para(doc, "3. 改错别字（只改错的）：痕际（　　）　平担（　　）　触脚（　　）")
    add_para(doc, "4. 字义选择正确的一项：（　　）①可怜九月初三夜（可惜）②只缘身在此山中（因为）③梅须逊雪三分白（谦逊）")
    wrong_box(doc)

    section_title(doc, "二、园地（约 4 分钟）")
    add_para(doc, "5. 俗语：一场秋雨一场寒，____________________。")
    add_para(doc, "6. 《题西林壁》：横看成岭侧成峰，____________________。")
    add_para(doc, "7. 理解：为什么说「远近高低各不同」？用自己的话答一句：________________")
    wrong_box(doc)

    section_title(doc, "三、句型仿写（约 2–3 分钟）")
    add_para(doc, "8. 照样子把观察写具体（用上比喻）：")
    add_para(doc, "　　例：枝条上冒出嫩黄色的小芽，像一个个小逗号。")
    add_para(doc, "　　写一种植物或小动物：________________________________________________")
    add_para(doc, "　　________________________________________________________________")
    wrong_box(doc)

    section_title(doc, "四、短阅读（约 4–5 分钟）")
    add_para(
        doc,
        "米虫有时钻进米里，潜伏片刻，又从那端钻出来，出出进进，躲躲藏藏，玩得极有兴致。",
        first_line=Cm(0.74),
        size=10,
    )
    add_para(doc, "9. 「潜伏」在文中的意思：________________________________")
    add_para(doc, "10. 判断：作者觉得米虫很笨，什么也不会。（　　）")
    add_para(doc, "11. 作者主要是在（　　）A. 编故事吓唬人　B. 仔细观察并描写　C. 说明米虫有毒")
    wrong_box(doc)

    add_para(doc, "———————— 参考答案（做完再看） ————————", size=9, bold=True, color=BRAND_ORANGE_YELLOW, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "1. 光滑　嫩绿　爬山虎　空隙　2. xiáng；jiàng；qū；jīng　3. 迹；坦；角　4. ②", size=9)
    add_para(doc, "5. 十场秋雨穿上棉（或：要穿棉）　6. 远近高低各不同　7. 从不同角度看庐山样子不同（意思对即可）", size=9)
    add_para(doc, "8. 有比喻、写具体即可　9. 隐藏、埋伏　10. ×　11. B", size=9)
    footer_line(doc, "语文书桌 · 工作日迷你 · U3　错题 → mistakes/")
    return doc


# ——— Weekend ———
def weekend_u1():
    doc = new_doc()
    header_block(
        doc,
        "周末练习 · 四上第一单元",
        "作文仿写 + 课外阅读理解　|　错题记入错题档案　|　可按推荐日期做，也可自选",
    )
    section_title(doc, "一、作文仿写（约 25–40 分钟）")
    add_para(doc, "题目：推荐一个好地方", bold=True, color=BRAND_DEEP)
    add_para(doc, "要求：写清在哪里、有什么特别、为什么推荐。语句通顺，条理清楚。")
    add_para(doc, "仿写支架（可先填再成文）：", bold=True)
    add_para(doc, "1. 我想推荐的地方是________，它在________。")
    add_para(doc, "2. 最特别的是________（景物 / 声音 / 气味 / 感受）。")
    add_para(doc, "3. 有一次，我________（一个具体小事例）。")
    add_para(doc, "4. 所以我推荐它，因为________。")
    add_para(doc, "正文（可另纸）：", space_before=4)
    for _ in range(10):
        add_para(doc, "________________________________________________________________")
    wrong_box(doc)

    section_title(doc, "二、课外阅读理解（教委/学校书目任选一篇短文或一章）")
    add_para(doc, "书名/篇名：____________________　　阅读日期：________")
    add_para(doc, "1. 用一两句话写主要内容：________________________________")
    add_para(doc, "2. 文中不认识或易错的字词（抄 3 个并组词/释义）：")
    add_para(doc, "　　①________　②________　③________")
    add_para(doc, "3. 找出一个好词好句，抄下来：________________________________")
    add_para(doc, "4. 针对内容提一个问题并试答：")
    add_para(doc, "　　问：________________________________？")
    add_para(doc, "　　答：________________________________。")
    add_para(doc, "5. 针对写法提一个问题（如：为什么这样写？）：________________")
    wrong_box(doc)
    footer_line(doc, "语文书桌 · 周末 · U1　错题 → mistakes/")
    return doc


def weekend_u2():
    doc = new_doc()
    header_block(
        doc,
        "周末练习 · 四上第二单元",
        "作文仿写（写人物特点）+ 课外阅读理解　|　错题记入错题档案",
    )
    section_title(doc, "一、作文仿写（约 25–40 分钟）")
    add_para(doc, "题目：写出他（她）与众不同的特点", bold=True, color=BRAND_DEEP)
    add_para(doc, "要求：选身边一人，用一个印象深刻的事例；语句通顺，事例具体。")
    add_para(doc, "仿写支架：", bold=True)
    add_para(doc, "1. 我要写的人是________，他/她最大的特点是________。")
    add_para(doc, "2. 事情发生在________（时间地点）。")
    add_para(doc, "3. 经过：先……接着……最后……（写具体动作、语言）。")
    add_para(doc, "4. 从这个事例看出：____________________。")
    for _ in range(10):
        add_para(doc, "________________________________________________________________")
    wrong_box(doc)

    section_title(doc, "二、课外阅读理解（教委/学校书目）")
    add_para(doc, "书名/篇名：____________________　　日期：________")
    add_para(doc, "1. 主要内容：________________________________________________")
    add_para(doc, "2. 本单元重点是「提问」。请分类提问：")
    add_para(doc, "　　针对内容：________________________________？")
    add_para(doc, "　　针对写法：________________________________？")
    add_para(doc, "　　联系生活：________________________________？")
    add_para(doc, "3. 选一个最值得思考的问题，尝试解答：________________________")
    add_para(doc, "4. 摘录好词好句 1–2 句：____________________________________")
    wrong_box(doc)
    footer_line(doc, "语文书桌 · 周末 · U2　错题 → mistakes/")
    return doc


def weekend_u3():
    doc = new_doc()
    header_block(
        doc,
        "周末练习 · 四上第三单元",
        "作文仿写（观察写植物/小动物）+ 课外阅读理解　|　错题记入错题档案",
    )
    section_title(doc, "一、作文仿写（约 25–40 分钟）")
    add_para(doc, "题目：观察一种植物或小动物", bold=True, color=BRAND_DEEP)
    add_para(doc, "要求：写出外形、动作或变化；用上比喻或具体描写；条理清楚。")
    add_para(doc, "仿写支架：", bold=True)
    add_para(doc, "1. 我观察的是________，观察时间________。")
    add_para(doc, "2. 外形：________（颜色、形状，可用比喻）。")
    add_para(doc, "3. 变化/活动：刚开始……过了几天/一会儿……")
    add_para(doc, "4. 我的发现或感受：____________________。")
    for _ in range(10):
        add_para(doc, "________________________________________________________________")
    wrong_box(doc)

    section_title(doc, "二、课外阅读理解（教委/学校书目）")
    add_para(doc, "书名/篇名：____________________　　日期：________")
    add_para(doc, "1. 主要内容：________________________________________________")
    add_para(doc, "2. 作者观察最仔细的一处是：________________________________")
    add_para(doc, "3. 解释文中一个加点词或难懂词：________ → ________________")
    add_para(doc, "4. 判断/简答：这篇主要是（说明事理 / 观察描写 / 童话想象）。我选________，因为________。")
    add_para(doc, "5. 摘录并仿写一句观察句：")
    add_para(doc, "　　原句：________________________________________________")
    add_para(doc, "　　仿写：________________________________________________")
    wrong_box(doc)
    footer_line(doc, "语文书桌 · 周末 · U3　错题 → mistakes/")
    return doc


def write_answer_sheets():
    ANS.mkdir(exist_ok=True)
    (ANS / "weekday-u01-参考答案.md").write_text(
        """# 工作日迷你 · U1 · 参考答案

另见卷末。错题请记入 `mistakes/错题档案.md`。

1. 繁星　模糊　霎时
2. 浪潮/朝阳；堤坝/提醒（合理即可）
3. cháo；zhāo；mèn
4. ②
5. 宋　苏轼；最是橙黄橘绿时
6. ①；②
7. 通顺即可
8. ×　9. B　10. 一起向前冲（意思对即可）
""",
        encoding="utf-8",
    )
    (ANS / "weekday-u02-参考答案.md").write_text(
        """# 工作日迷你 · U2 · 参考答案

1. 身份　注视　的确　证明
2. 纲；冈；纲　|　即；既；即
3. biān；bì；liù；rāng
4. A
5. 孰能无惑
6. 学、问、思、辨、行
7. 人之所；人之所不
8–9. 句式正确即可
10. 像罩子一样遮盖　11. √　12. B
""",
        encoding="utf-8",
    )
    (ANS / "weekday-u03-参考答案.md").write_text(
        """# 工作日迷你 · U3 · 参考答案

1. 光滑　嫩绿　爬山虎　空隙
2. xiáng；jiàng；qū；jīng
3. 迹；坦；角
4. ②
5. 十场秋雨穿上棉（或：要穿棉）
6. 远近高低各不同
7. 从不同角度看庐山样子不同
8. 有比喻、写具体即可
9. 隐藏、埋伏　10. ×　11. B
""",
        encoding="utf-8",
    )
    (ANS / "weekend-u01-u03-说明.md").write_text(
        """# 周末练习 · 说明与参考

周末卷以**支架 + 开放题**为主，无唯一标准答案。

## 批改关注点

- 作文：是否写清「地方/人物/观察对象 + 具体事例 + 推荐或特点」
- 课外阅读：是否完成摘录、提问、简答；字词是否订正

## 错题

习作结构严重跑题、阅读题答错 → 记入 `mistakes/错题档案.md`，考前按单元复习。
""",
        encoding="utf-8",
    )
    print("answer sheets written")


def main():
    save_pair(weekday_u1(), WEEKDAY, "u01-工作日迷你-8至15分钟")
    save_pair(weekday_u2(), WEEKDAY, "u02-工作日迷你-8至15分钟")
    save_pair(weekday_u3(), WEEKDAY, "u03-工作日迷你-8至15分钟")
    save_pair(weekend_u1(), WEEKEND, "u01-周末-作文仿写与课外阅读")
    save_pair(weekend_u2(), WEEKEND, "u02-周末-作文仿写与课外阅读")
    save_pair(weekend_u3(), WEEKEND, "u03-周末-作文仿写与课外阅读")
    write_answer_sheets()
    print("all packs done")


if __name__ == "__main__":
    main()
