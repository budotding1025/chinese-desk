# -*- coding: utf-8 -*-
"""期中复习 · 基础练习（第一至四单元每课填空）→ Word 宋体 + PDF。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Pt  # noqa: E402

from docx_utils import (  # noqa: E402
    EXAM_FONT,
    EXAM_FONT_TITLE,
    EXAM_INK,
    add_para,
    docx_to_pdf,
    end_exam_page,
    exam_body,
    exam_doc,
    exam_header,
    exam_section,
)

OUT_DIR = ROOT / "printables" / "midterm"
ANS_DIR = ROOT / "printables" / "midterm-answers"
MD_ANS = ROOT / "answers" / "midterm-basic-参考答案.md"


def _blank(n: int = 6) -> str:
    return "＿" * n


def _q(doc, text: str, *, size=12, space_after=3):
    exam_body(doc, text, size=size, space_after=space_after)


def _lesson(doc, title: str):
    add_para(
        doc,
        title,
        size=13,
        bold=True,
        space_before=6,
        space_after=3,
        color=EXAM_INK,
        font=EXAM_FONT_TITLE,
    )


def _unit_bar(doc, title: str, element: str):
    exam_section(doc, title)
    exam_body(doc, "语文要素：" + element, size=11, space_after=4)


def build_student():
    doc = exam_doc()
    exam_header(doc, "四年级上册 · 期中复习重点")
    exam_body(
        doc,
        "新教材｜第一至四单元｜每课填空（已按课本核对）",
        size=11,
        space_after=2,
    )
    exam_body(
        doc,
        "先独立完成，再听老师讲评；错一题在题号上画☆，回到课文里找一找。",
        size=10,
        space_after=6,
    )

    # —— 第 1 页：一单元 ——
    _unit_bar(doc, "第一单元 自然之美", "边读边想象画面，感受自然之美")

    _lesson(doc, "第1课 《观潮》")
    _q(doc, f"作者：{_blank(4)}、{_blank(4)}")
    _q(
        doc,
        f"1.本文作者是{_blank(4)}、{_blank(4)}。钱塘江大潮，自古以来被称为{_blank(5)}。"
        f"观潮的时间是{_blank(7)}，地点是{_blank(8)}。",
    )
    _q(doc, f"2.午后一点左右，从远处传来{_blank(6)}，好像{_blank(5)}。")
    _q(doc, f"3.顿时{_blank(5)}，有人告诉我们，潮来了！")
    _q(doc, f"4.过了一会儿，响声越来越大，只见东边水天相接的地方出现了一条{_blank(3)}。")
    _q(doc, f"5.再近些，只见白浪翻滚，形成一堵{_blank(4)}水墙。")
    _q(
        doc,
        f"6.浪潮越来越近，犹如千万匹{_blank(5)}齐头并进，浩浩荡荡地飞奔而来；"
        f"那声音如同{_blank(5)}，好像大地都被震得颤动起来。",
    )

    _lesson(doc, "第2课 《繁星》　作者：巴金")
    _q(doc, f"1.本文的作者是{_blank(3)}。“我爱月夜，但我也爱{_blank(3)}。”")
    _q(
        doc,
        f"2.课文写了“我”在三个地方看星星：{_blank(10)}、{_blank(8)}、{_blank(8)}。",
    )
    _q(
        doc,
        f"3.“渐渐地我的眼睛模糊了，我好像看见无数{_blank(4)}在我的周围飞舞。”",
    )
    _q(doc, f"4.海上的夜是{_blank(4)}，是{_blank(4)}，是{_blank(4)}。")

    _lesson(doc, "第3课 《现代诗二首》　《秋晚的江上》《花牛歌》")
    _q(
        doc,
        f"1.《秋晚的江上》的作者是{_blank(4)}。归鸟驮着{_blank(3)}，双翅一翻，"
        f"把斜阳掉在江上；头白的芦苇也妆成一瞬的{_blank(3)}了。",
    )
    _q(
        doc,
        f"2.《花牛歌》的作者是{_blank(4)}。花牛在草地里{_blank(2)}、{_blank(2)}、"
        f"{_blank(2)}、{_blank(3)}。",
    )

    _lesson(doc, "语文园地一 日积月累　《赠刘景文》（宋·苏轼）")
    _q(doc, f"1.荷尽已无{_blank(4)}，菊残犹有{_blank(4)}。")
    _q(doc, f"2.一年好景君须记，最是{_blank(6)}。")

    end_exam_page(doc, "期中复习 · 基础练习 · 第 1 页（共 4 页）")

    # —— 第 2 页：一单元续 + 二单元 ——
    _q(
        doc,
        f"3.园地一词句段运用：人声鼎沸、锣鼓喧天、震耳欲聋、响彻云霄是写声音{_blank(3)}的；"
        f"低声细语、窃窃私语、鸦雀无声、悄无声息是写声音{_blank(3)}的。",
    )
    _q(
        doc,
        f"4.“钱塘江大潮，自古以来被称为天下奇观”和“自古以来，人们把钱塘江大潮称为天下奇观”"
        f"意思相同，前者是{_blank(3)}字句，后者是{_blank(3)}字句。",
    )

    _unit_bar(
        doc,
        "第二单元 提问策略",
        "阅读时尝试从不同角度去思考，提出自己的问题",
    )

    _lesson(doc, "第4课 《一个豆荚里的五粒豆》　丹麦·安徒生，译者叶君健")
    _q(doc, f"1.本文的作者是丹麦作家{_blank(4)}，译者是{_blank(4)}。")
    _q(
        doc,
        f"2.五粒豌豆中，那粒钻进窗子旁{_blank(8)}里的豌豆，在那里生了根、长出小叶子，"
        f"最后开出了{_blank(5)}的豌豆花。",
    )
    _q(
        doc,
        f"3.顶楼窗子旁躺着一个{_blank(4)}。豌豆的生长给她带来了{_blank(5)}，"
        f"她的脸上洋溢着{_blank(6)}。",
    )

    _lesson(doc, "第5课 《夜间飞行的秘密》　作者：郝应其")
    _q(
        doc,
        f"1.本文作者是{_blank(4)}。科学家做了{_blank(2)}次实验：第一次把蝙蝠的{_blank(3)}蒙上；"
        f"第二次把它的{_blank(3)}塞上；第三次把它的{_blank(3)}封上。",
    )
    _q(
        doc,
        f"2.事实证明，蝙蝠夜里飞行，靠的不是{_blank(3)}，它是用{_blank(6)}配合起来探路的。",
    )
    _q(
        doc,
        f"3.蝙蝠一边飞，一边从嘴里发出{_blank(5)}；遇到障碍物，超声波反射回来，传到蝙蝠的{_blank(3)}里。",
    )
    _q(doc, f"4.科学家模仿蝙蝠探路的方法，给飞机装上了{_blank(3)}。")

    _lesson(doc, "第6课 《方帽子店》　作者：施雁冰　略读课文")
    _q(
        doc,
        f"1.本文作者是{_blank(4)}。从前，方帽子店里卖的帽子都是{_blank(2)}的，店主从不做{_blank(2)}帽子。",
    )
    _q(doc, f"2.后来，孩子们做出了{_blank(2)}帽子，方帽子渐渐被淘汰了。")
    _q(doc, f"3.这个故事告诉我们：世界在变化，我们要{_blank(8)}，不能墨守成规。")

    _lesson(doc, "第7课 《田忌赛马》　略读课文")
    _q(doc, f"1.{_blank(3)}是齐国大将{_blank(3)}的门客，他观察赛马后出了主意。")
    _q(
        doc,
        f"2.孙膑让田忌用{_blank(3)}等马对齐威王的{_blank(3)}等马，用{_blank(3)}等马对{_blank(3)}等马，"
        f"用{_blank(3)}等马对{_blank(3)}等马，最后赢了比赛。",
    )

    end_exam_page(doc, "期中复习 · 基础练习 · 第 2 页（共 4 页）")

    # —— 第 3 页：二单元续 + 三单元 ——
    _q(doc, f"3.比赛结果：田忌{_blank(6)}，赢了齐威王。后来齐威王任命孙膑为{_blank(4)}。")
    _q(
        doc,
        f"4.本文根据《{_blank(4)}》相关内容改写。故事告诉我们：只要{_blank(10)}，就能在比赛中取胜。",
    )

    _lesson(doc, "语文园地二 日积月累（关于“问”的名言）")
    _q(doc, f"1.博学之，{_blank(4)}，慎思之，{_blank(4)}，笃行之。——{_blank(5)}")
    _q(doc, f"2.智能之士，{_blank(6)}，不问不知。——{_blank(3)}")
    _q(doc, f"3.人非生而知之者，{_blank(5)}？——{_blank(3)}")
    _q(doc, f"4.善疑者，不疑人之所疑，而疑人之所{_blank(4)}。——{_blank(4)}")
    _q(
        doc,
        f"5.识字加油站：冈—{_blank(2)}（提纲）、奏—{_blank(2)}（挨揍）、秀—{_blank(2)}（生锈）、"
        f"末—{_blank(2)}（泡沫）、宗—{_blank(2)}（综合）、羊—{_blank(2)}（氧气）、"
        f"长—{_blank(2)}（结账）、广—{_blank(2)}（矿物）、具—{_blank(2)}（俱乐部）。",
    )

    _unit_bar(
        doc,
        "第三单元 连续观察",
        "体会文章准确生动的表达，感受作者连续细致的观察",
    )

    _lesson(doc, "第8课 《古诗三首》　《暮江吟》《题西林壁》《雪梅》")
    _q(
        doc,
        f"1.《暮江吟》的作者是{_blank(2)}代诗人{_blank(4)}。“一道残阳铺水中，{_blank(3)}半江红。”"
        f"（瑟瑟：{_blank(6)}）",
    )
    _q(
        doc,
        f"2.“可怜九月初三夜，露似{_blank(3)}，月似{_blank(3)}。”（可怜：{_blank(5)}）",
    )
    _q(
        doc,
        f"3.《题西林壁》的作者是{_blank(2)}代诗人{_blank(3)}。“横看成岭侧成峰，{_blank(5)}各不同。”",
    )
    _q(doc, f"4.“不识庐山真面目，{_blank(7)}。”（缘：{_blank(4)}）")
    _q(
        doc,
        f"5.《雪梅》的作者是{_blank(2)}代诗人{_blank(4)}。“梅须{_blank(3)}雪三分白，雪却输梅{_blank(3)}。”"
        f"（逊：{_blank(4)}）",
    )

    _lesson(doc, "第9课 《爬山虎的脚》　作者：叶圣陶")
    _q(
        doc,
        f"1.本文的作者是{_blank(4)}。爬山虎的嫩红叶子，叶尖一顺儿朝下，在墙上铺得那么{_blank(3)}。",
    )
    _q(
        doc,
        f"2.爬山虎的脚长在茎上。茎上长叶柄的地方，反面伸出枝状的六七根细丝，像{_blank(5)}；"
        f"细丝头上变成{_blank(4)}，巴住墙。",
    )
    _q(
        doc,
        f"3.触着墙的，细丝和小圆片逐渐变成{_blank(3)}；没触着墙的，不几天就{_blank(5)}了。",
    )

    _lesson(doc, "第10课 《蟋蟀的住宅》　法国·法布尔，译者王大文")
    end_exam_page(doc, "期中复习 · 基础练习 · 第 3 页（共 4 页）")

    # —— 第 4 页：三单元续 + 四单元 ——
    _q(
        doc,
        f"1.本文的作者是{_blank(3)}的{_blank(4)}，译者是{_blank(4)}。他写下了著名的《{_blank(4)}》。",
    )
    _q(
        doc,
        f"2.蟋蟀和它们不同，不肯{_blank(5)}。它常常{_blank(6)}，一定要{_blank(6)}，并且有{_blank(5)}。",
    )
    _q(doc, f"3.住宅的出口的地方总有一丛草，好像一座{_blank(3)}。")

    _lesson(doc, "语文园地三 日积月累（秋天的谚语）")
    _q(doc, f"1.立了秋，{_blank(4)}。")
    _q(doc, f"2.夏雨少，{_blank(4)}。八月里来雁门开，雁儿脚上{_blank(4)}。")
    _q(doc, f"3.一场秋雨一场寒，{_blank(8)}。")
    _q(doc, f"4.八月暖，{_blank(4)}，十月还有{_blank(4)}。")
    _q(
        doc,
        f"5.词句段运用：狗{_blank(4)}　鼠{_blank(4)}　牛{_blank(4)}　猪{_blank(4)}　"
        f"马{_blank(4)}　鱼{_blank(4)}　鸟{_blank(4)}（也可以是鸟{_blank(4)}）　虎{_blank(4)}",
    )
    _q(
        doc,
        f"6.“触着墙的，细丝和小圆片{_blank(3)}变成灰色”，“逐渐”说明爬山虎的脚是{_blank(6)}变成灰色的，用词很准确。",
    )

    _unit_bar(
        doc,
        "第四单元 神话",
        "了解故事的起因、经过、结果，感受神话中神奇的想象和鲜明的人物形象",
    )

    _lesson(doc, "第11课 《盘古开天地》")
    _q(
        doc,
        f"1.盘古用{_blank(3)}劈开了混沌，轻而清的东西变成{_blank(2)}，重而浊的东西变成{_blank(2)}。"
        f"他头顶天，脚踏地，像一根{_blank(3)}。",
    )
    _q(
        doc,
        f"2.盘古呼出的气息变成了{_blank(3)}；声音变成了{_blank(3)}；左眼和右眼变成了{_blank(6)}。",
    )
    _q(
        doc,
        f"3.盘古的四肢和躯干变成了{_blank(6)}；血液变成了{_blank(3)}；汗毛变成了{_blank(5)}；"
        f"汗水变成了{_blank(3)}。",
    )

    _lesson(doc, "第12课 《精卫填海》　选自《山海经》")
    _q(doc, f"1.本文选自《{_blank(4)}》。炎帝之{_blank(2)}（小女儿），名{_blank(3)}。")
    _q(
        doc,
        f"2.女娃游于{_blank(3)}，溺而不返，故为{_blank(3)}，常衔{_blank(7)}以堙于{_blank(3)}。",
    )

    _lesson(doc, "第13课 《普罗米修斯》")
    _q(doc, f"1.普罗米修斯从天上{_blank(5)}，给人类带来了光明和温暖。")

    end_exam_page(doc, "期中复习 · 基础练习 · 第 4 页（共 4 页）", last=True)
    return doc


def build_answers():
    doc = exam_doc()
    exam_header(doc, "期中复习 · 基础练习 · 参考答案")
    exam_body(doc, "做完再看。意思对即可。", size=11, space_after=6)

    exam_section(doc, "第一单元")
    _q(doc, "第1课：赵宗成、朱明元｜天下奇观｜农历八月十八｜海宁市的盐官镇｜隆隆的响声｜闷雷滚动｜人声鼎沸｜白线｜高高的｜白色战马｜山崩地裂")
    _q(doc, "第2课：巴金｜星天｜从前在家乡的庭院里、在南京的菜园里、在海上的舱面上｜萤火虫｜柔和的、静寂的、梦幻的")
    _q(doc, "第3课：刘大白｜斜阳｜红颜｜徐志摩｜坐、眠、走、做梦")
    _q(doc, "园地一：擎雨盖｜傲霜枝｜橙黄橘绿时｜大（响）／小（静）｜把字／被字（或：主动／被动）")

    exam_section(doc, "第二单元")
    _q(doc, "第4课：安徒生｜叶君健｜长满青苔的裂缝｜一朵紫色｜生病的小姑娘｜生活的乐趣（愉快）｜健康的光彩")
    _q(doc, "第5课：郝应其｜三｜眼睛｜耳朵｜鼻子｜眼睛｜嘴和耳朵｜超声波｜耳朵｜雷达")
    _q(doc, "第6课：施雁冰｜方｜圆｜圆｜敢于创新／适应变化")
    _q(doc, "第7课：孙膑｜田忌｜下／上｜中／中｜上／下｜两胜一负（或赢了两局）｜军师｜史记｜善于观察、动脑筋想办法")

    exam_section(doc, "园地二")
    _q(doc, "1.审问之；明辨之——《礼记》（《中庸》）　2.不学不成——王充　3.孰能无惑——韩愈　4.不疑——方以智")
    _q(doc, "识字：纲、揍、锈、沫、综、氧、账、矿、俱")

    exam_section(doc, "第三单元")
    _q(doc, "第8课：唐·白居易｜半江瑟瑟｜江水细波／碧色｜珍珠｜弓｜可爱｜宋·苏轼｜远近高低｜只缘身在此山中｜因为｜宋·卢梅坡｜逊｜一段香｜差／比不上")
    _q(doc, "第9课：叶圣陶｜均匀｜蜗牛的触角｜小圆片｜灰色｜枯萎了")
    _q(doc, "第10课：法国｜法布尔｜王大文｜昆虫记｜随遇而安｜慎重选址｜排水优良｜足够的食物｜门")

    exam_section(doc, "园地三")
    _q(doc, "1.把扇丢　2.秋霜早；带霜来　3.十场秋雨要穿棉　4.九月温；小阳春")
    _q(doc, "5.示例：狗急跳墙、鼠目寸光、牛高马大、猪狗不如、马到成功、鱼目混珠、鸟语花香／鸟尽弓藏、虎头蛇尾　6.逐渐；慢慢／一点一点")

    exam_section(doc, "第四单元")
    _q(doc, "第11课：斧头｜天｜地｜柱子｜风和云｜雷霆｜太阳和月亮｜大山／五岳｜江河｜花草树木｜雨露")
    _q(doc, "第12课：山海经｜女｜女娃｜东海｜精卫｜西山之木石｜东海")
    _q(doc, "第13课：盗取火种（拿取火种）")

    end_exam_page(doc, "期中复习 · 基础练习答案", last=True)
    return doc


ANSWERS_MD = """# 期中复习 · 基础练习 · 参考答案

> 对应：`printables/midterm/midterm-basic.pdf`
> 打印答案页：`printables/midterm-answers/midterm-basic-answers.pdf`

## 第一单元
- 第1课：赵宗成、朱明元；天下奇观；农历八月十八；海宁市的盐官镇；隆隆的响声；闷雷滚动；人声鼎沸；白线；高高的；白色战马；山崩地裂
- 第2课：巴金；星天；家乡庭院、南京菜园、海上舱面；萤火虫；柔和的、静寂的、梦幻的
- 第3课：刘大白；斜阳；红颜；徐志摩；坐、眠、走、做梦
- 园地一：擎雨盖；傲霜枝；橙黄橘绿时；大／小；把字句／被字句

## 第二单元
- 第4课：安徒生；叶君健；长满青苔的裂缝；紫色；生病的小姑娘；生活的乐趣；健康的光彩
- 第5课：郝应其；三次；眼睛／耳朵／鼻子；眼睛；嘴和耳朵；超声波；耳朵；雷达
- 第6课：施雁冰；方；圆；圆；敢于创新、适应变化
- 第7课：孙膑；田忌；下对上、中对中、上对下；两胜一负；军师；《史记》；善于观察、想办法
- 园地二：审问之／明辨之（《中庸》）；不学不成（王充）；孰能无惑（韩愈）；不疑（方以智）；纲揍锈沫综氧账矿俱

## 第三单元
- 第8课：唐·白居易；半江瑟瑟；江水细波；珍珠／弓；可爱；宋·苏轼；远近高低；只缘身在此山中；因为；宋·卢梅坡；逊；一段香；差
- 第9课：叶圣陶；均匀；蜗牛的触角；小圆片；灰色；枯萎
- 第10课：法国·法布尔；王大文；《昆虫记》；随遇而安；慎重选址；排水优良；足够的食物；门
- 园地三：把扇丢；秋霜早；带霜来；十场秋雨要穿棉；九月温；小阳春；逐渐

## 第四单元
- 第11课：斧头；天／地；柱子；风和云；雷霆；太阳和月亮；大山；江河；花草树木；雨露
- 第12课：《山海经》；女；女娃；东海；精卫；西山之木石；东海
- 第13课：盗取火种
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ANS_DIR.mkdir(parents=True, exist_ok=True)
    student = OUT_DIR / "midterm-basic.docx"
    student_pdf = OUT_DIR / "midterm-basic.pdf"
    answers = ANS_DIR / "midterm-basic-answers.docx"
    answers_pdf = ANS_DIR / "midterm-basic-answers.pdf"

    d1 = build_student()
    d1.save(student)
    print("Wrote", student.name)
    docx_to_pdf(student, student_pdf)
    print("Wrote", student_pdf.name)

    d2 = build_answers()
    d2.save(answers)
    print("Wrote", answers.name)
    docx_to_pdf(answers, answers_pdf)
    print("Wrote", answers_pdf.name)

    MD_ANS.write_text(ANSWERS_MD, encoding="utf-8")
    print("Wrote", MD_ANS.name)


if __name__ == "__main__":
    main()
