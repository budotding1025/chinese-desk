# -*- coding: utf-8 -*-
"""Generate Unit 1–4 full exams (Word + PDF) — A4 layout matching JPG 原卷."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from docx_utils import (
    add_choice_char_table,
    add_emphasis_words,
    add_inline_pinyin_line,
    add_page_break,
    add_para,
    add_stroke_choice_row,
    docx_to_pdf,
    end_exam_page,
    exam_body,
    exam_doc,
    exam_footer,
    exam_header,
    exam_section,
    set_run_font,
    write_lines,
)
from theme import BRAND_DEEP, BRAND_ORANGE_RED, INK


def _set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "8")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "000000")
        tcBorders.append(element)
    tcPr.append(tcBorders)


def add_observe_table(doc):
    """米虫观察表：与原卷第3页一致。"""
    table = doc.add_table(rows=4, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["观察场景", "米虫的样子、行为", "我的发现"]
    data = [
        ["在大米中", "米里潜伏，出出进进，躲躲藏藏", "米虫活泼好动，很有趣"],
        ["盒子倾斜后", "", ""],
        ["侧翻倒地时", "六只脚乱抓，张开翅膀扇动滑行，靠米粒翻身", ""],
    ]
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=10, bold=True, color=INK)
        p.alignment = 1
        _set_cell_border(cell)
    for i, row in enumerate(data):
        for j, text in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            filler = text if text else ("\n\n" if j > 0 else "　")
            run = p.add_run(filler)
            set_run_font(run, size=11, color=INK)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            _set_cell_border(cell)
        tr = table.rows[i + 1]._tr
        trPr = tr.get_or_add_trPr()
        trHeight = OxmlElement("w:trHeight")
        trHeight.set(qn("w:val"), "900")
        trHeight.set(qn("w:hRule"), "atLeast")
        trPr.append(trHeight)
    # spacer after table
    add_para(doc, "", size=6, space_after=4)

PRINT = Path(__file__).resolve().parents[1] / "printables" / "full"


def build_u1():
    doc = exam_doc()
    exam_header(doc, "语文·四上·第一单元练习")

    exam_section(doc, "一、看拼音，写词语。")
    # 与原卷一致：方格嵌在句中，按原卷断行
    add_inline_pinyin_line(
        doc,
        ["深蓝色的天空中，悬着", ("fán xīng", 2), "。它们是这样低，真是摇摇欲坠。"],
        after=2,
    )
    add_inline_pinyin_line(
        doc,
        ["渐渐地我的眼睛", ("mó hu", 2), "了，我好像看见无数萤火虫在我的周围", ("fēi wǔ", 2), "。"],
        after=2,
    )
    add_inline_pinyin_line(
        doc,
        ["海上的夜是", ("róu hé", 2), "的，是静寂的，是", ("mèng huàn", 2), "的。"],
        after=4,
    )

    exam_section(doc, "二、选出下列各组词语中读音有误的一项，将序号填在括号里。")
    exam_body(doc, "1. ①薄雾（bó）　②闷雷（mèn）　③萤火虫（yín）　　（　　）")
    exam_body(doc, "2. ①芦苇（wěi）　②霎时（chà）　③半明半昧（mèi）　　（　　）")
    exam_body(doc, "3. ①尽管（jǐn）　②虽然（suī）　③悄无声息（qiǎo）　　（　　）")

    exam_section(doc, "三、把下列各组词语中的错别字圈出来，将正确的字写在后面的括号里。")
    exam_body(doc, "1. ①据说　②蜜密麻麻　③怀抱　　（　　）")
    exam_body(doc, "2. ①余波　②齐头并近　③山崩地裂　　（　　）")
    exam_body(doc, "3. ①逐浙　②浩浩荡荡　③风平浪静　　（　　）")

    exam_section(doc, "四、按照要求完成填空。")
    exam_body(
        doc,
        "“围”字的第六笔是________。在词典中，“围”字的意思有：①四周拦挡起来，使里外不通；环绕；②四周；周围；③某些物体周围的长度。在“外围”中，“围”的意思应该选择第________种解释。",
        size=10.5,
    )
    exam_footer(doc, "语文·四上·第一单元　第 1 页（共 4 页）")
    add_page_break(doc)

    # p2
    exam_section(doc, "五、将下列词语补充完整并选词填空（填序号），再写一写。")
    exam_body(doc, "①低声（　　）语　②鸦雀（　　）声　③响彻（　　）霄")
    exam_body(doc, "④（　　）无声息　⑤窃窃（　　）语　⑥摇摇（　　）坠")
    exam_body(doc, "1. 形容声音小或者没有声音的词语有：________________________________。")
    exam_body(doc, "2. 读词语②，我仿佛看到这样的画面：")
    write_lines(doc, 2)

    exam_section(doc, "六、选一个事物，用一两个加点的词语描绘它，再写下来。")
    exam_body(doc, "事物：雪　烟花　雨　小狗", space_after=2)
    add_emphasis_words(doc, "加点词语：", ["霎时", "顿时", "忽然", "过了一会儿", "一会儿工夫"])
    write_lines(doc, 2)

    exam_section(doc, "七、按要求将内容补充完整。")
    exam_body(
        doc,
        "《赠刘景文》的作者是________代的________。这首诗中勉励朋友珍惜大好时光、乐观向上的诗句是（　　）。（填序号）",
    )
    exam_body(doc, "①荷尽已无擎雨盖，菊残犹有傲霜枝。")
    exam_body(doc, "②一年好景君须记，最是橙黄橘绿时。")

    exam_section(doc, "八、阅读诗歌和短文，回答问题。")
    exam_body(doc, "（一）一朵淡紫色的小花", bold=True)
    exam_body(doc, "那是一朵（　　）的小花，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "那么（　　），那么柔弱。", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "我不知道她的名字。", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "可是我知道：", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "她终于会开放，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "只要有一点点水，一点点土壤。", first_line=Cm(0.74), space_after=2)
    exam_footer(doc, "语文·四上·第一单元　第 2 页（共 4 页）")
    add_page_break(doc)

    # p3
    exam_body(doc, "我也知道她会报答。", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "在开放的时候，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "她会不断地投放出芳香。", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "在太阳光下，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "她还会投射出一个小小的影子，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "具有大树冠的影子的同样颜色。", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "她的影子虽然是一把极小极小的伞，", first_line=Cm(0.74), space_after=1)
    exam_body(doc, "却也能为一个可怜的蚂蚁遮阳。", first_line=Cm(0.74), space_after=2)
    exam_body(doc, "（根据严文井《一朵淡紫色的小花》改写）", size=9, space_after=4)

    exam_body(doc, "1. 选择恰当的词语，将序号填在文中的括号里。")
    exam_body(doc, "　　①文雅　　②淡紫色")
    exam_body(doc, "2. 用“____”画出诗中描写小花影子的作用的句子。")
    exam_body(doc, "3. 诗中的“她”指的是____________________。读了这首小诗，我觉得她是一朵____________________的小花。")

    exam_body(doc, "（二）____________________", bold=True, space_before=6)
    exam_body(doc, "峻青", size=10, space_after=3)
    exam_body(
        doc,
        "①在北戴河那著名的二十四景中，最美、最壮丽的景致，要算在东山鹰角亭上看到的日出了。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "②四点钟，天还蒙蒙亮，沿着海滨大道向东山走，抵达鹰角亭时，残云已经散尽，星星在天空中闪烁着，东方的天际，还是一片黛（dài）色。稍待片刻，就泛起了粉红色的霞光，霞光立即染遍大海，一种柔和明快的美，使你陶醉入神。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "③不久，霞光中渐渐裂开一道金黄的缝隙。这缝隙越来越宽，越来越长，在地平线上放射出万道金光。这金光映射在天空和大海中，像一团火焰似的热烈地燃烧着。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_footer(doc, "语文·四上·第一单元　第 3 页（共 4 页）")
    add_page_break(doc)

    # p4
    exam_body(
        doc,
        "④过了一会儿，在那水天融为一体的苍茫的远方，在那好像燃烧着火焰一般的远方，一轮巨大的、紫红色的太阳仿佛积聚了万钧（jūn）之力，一跃而起，顶出了海面冉冉升起。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "⑤霎时间，太阳由紫红而玫红，由玫红而火红，把大半边天上的云霞映得红彤彤的，辽阔无垠的天空和大海，一下子就布满了耀眼的金光。这金光很快就铺了一条又宽又亮又红的“海上大道”，一直伸展到了鹰角亭下的海边。这又长又直的路，令人觉得仿佛沿着这条红彤彤的征途，就可以走进太阳的门槛。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(doc, "（有改动）", size=9, space_after=4)

    exam_body(doc, "1. 请给这篇短文选择一个最合适的题目，写在文前的横线上。")
    exam_body(doc, "　　①北戴河　　②鹰角亭　　③北戴河日出")
    exam_body(doc, "2. “辽阔无垠”在文中的意思是________________________________。")
    exam_body(doc, "3. 读文中第④自然段画线的句子，发挥想象，把你脑海中浮现的画面写下来。")
    exam_body(doc, "　　读了这个句子，我想到________________________________________。")
    exam_body(doc, "4. 这篇文章表达了作者____________________之情，也流露出作者对大自然美景的热爱与赞叹。")

    exam_section(doc, "九、习作。")
    exam_body(doc, "题目：推荐一个好地方", bold=True)
    exam_body(
        doc,
        "写一写你最喜欢的地方，可以是公园、校园、家乡、景区等。写清楚这个地方在哪里，有什么特别之处，写出推荐的理由，让大家也喜欢上这里。要求：语句通顺，条理清楚。",
        size=10,
    )
    write_lines(doc, 9, size=13, space_after=3)
    exam_footer(doc, "语文·四上·第一单元　第 4 页（共 4 页）")
    return doc


def build_u2():
    doc = exam_doc()
    exam_header(doc, "语文·四上·第二单元练习")

    exam_section(doc, "一、看拼音，写词语。")
    add_inline_pinyin_line(
        doc,
        [
            "当",
            ("shēn fèn", 2),
            ("jiē xiǎo", 2),
            "的那一刻，众人",
            ("zhù shì", 2),
            "着他的双眼，",
        ],
        after=2,
    )
    add_inline_pinyin_line(
        doc,
        [
            "过往的汗水",
            ("dí què", 2),
            "没有白费，他最终用实力",
            ("zhèng míng", 2),
            "了所有的坚持都终有回报。",
        ],
        after=5,
    )

    exam_section(doc, "二、在加点字的正确读音下面画“√”。")
    exam_body(doc, "囚 犯（qiú　qiū）　　蝙 蝠（biān　biǎn）　　避 开（bì　pì）")
    exam_body(doc, "荧 屏（yín　yíng）　　一溜 烟（liū　liù）　　嚷 嚷（rāng　rǎng）")

    exam_section(doc, "三、选字组词。")
    add_choice_char_table(
        doc,
        [
            ("纲　冈", ["提（　　）", "井（　　）山", "（　　）要"]),
            ("末　沫", ["泡（　　）", "（　　）尾", "飞（　　）"]),
            ("即　既", ["（　　）使", "（　　）然", "立（　　）"]),
            ("具　俱", ["（　　）体", "（　　）乐部", "万事（　　）备"]),
        ],
    )

    exam_section(doc, "四、照样子，改写句子。")
    exam_body(doc, "1. 原句：那条狗高兴、紧张、发怒的时候都叫。", size=10)
    exam_body(doc, "　　改写：那条狗高兴的时候叫，紧张的时候叫，发怒的时候也叫。", size=10)
    exam_body(doc, "　　原句：那盏灯晴天、阴天、雨天的时候都亮着。", size=10)
    exam_body(doc, "　　改写：", size=10, space_after=1)
    write_lines(doc, 1, size=12)
    exam_footer(doc, "语文·四上·第二单元　第 1 页（共 4 页）")
    add_page_break(doc)

    exam_body(doc, "2. 原句：人类呼风唤雨。", size=10)
    exam_body(doc, "　　改写：是谁呼风唤雨呢？当然是人类。", size=10)
    exam_body(doc, "　　原句：妈妈把家里打扫得干干净净。", size=10)
    exam_body(doc, "　　改写：", size=10, space_after=1)
    write_lines(doc, 1, size=12)

    exam_section(doc, "五、根据所学内容填空。")
    exam_body(
        doc,
        "从韩愈的“____________________，孰能无惑”和王充的“智能之士，____________________，____________________”这两句话中，我们明白了，学习中遇到问题很正常，要敢于通过提问进行学习，像《中庸》中说的那样，努力做到“博____之，审____之，慎____之，明____之，笃____之”，因为提问能给我们的成长带来帮助，正如方以智所说“善疑者，不疑________疑，而疑________疑”。",
        size=10,
    )

    exam_section(doc, "六、阅读短文，回答问题。")
    exam_body(doc, "（一）对流雨", bold=True)
    exam_body(
        doc,
        "①在夏日午后，人们常常经历这样的天气：一开始是烈日高照，让人感到十分闷热。后来，几朵乌云飘了过来，笼罩着大地，凉风随之袭来，并且风速较快。路上行人匆忙赶路，小贩们忙于收摊，家庭主妇则赶紧将晾晒的衣服收进屋。一会儿，倾盆大雨从天而降，有时候还伴有电闪雷鸣。雨一般下的时间不长，雨过便天晴。这种炎热夏季和热带地区常见的雷阵雨，就属于对流雨。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "②“对流”指的是空气的上下垂直流动。简单来说，夏天日照强、气温高，地面水分被迅速蒸发，地面近处的大量空气受热膨胀向上升，到高空遇到冷空气，水汽就冷却凝结成雨从天而降，这就形成了对流雨。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(doc, "（根据相关内容改写）", size=9)
    exam_footer(doc, "语文·四上·第二单元　第 2 页（共 4 页）")
    add_page_break(doc)

    exam_body(doc, "1. 联系短文内容和生活实际，想想加点词语的意思，试着写下来。")
    exam_body(doc, "　　笼罩：________________________________________________")
    exam_body(doc, "2. 对流雨是怎样形成的？在文中用“____”画下来。")
    exam_body(doc, "3. 试着从不同角度提出自己的问题，并分类写下来。")
    exam_body(doc, "　　针对内容提出的问题：________________________________？")
    exam_body(doc, "　　针对写法提出的问题：________________________________？")
    exam_body(doc, "　　联系生活实际提出的问题：____________________________？")

    exam_body(doc, "（二）纸上谈兵", bold=True, space_before=6)
    exam_body(
        doc,
        "①赵国名将赵奢的儿子赵括自幼爱学兵法，谈起用兵之道，口若悬河，自以为天下无敌，不把任何人放在眼里。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "②后来秦国大举攻打赵国，赵国老将廉颇奉命驻守长平，他坚守营寨，拒不出战。秦军久攻不下，就使出反间计，派人到赵国散布谣言：秦军根本不怕廉颇，只怕赵括做大将。赵王听信了流言，叫人把赵括找来，问他能不能打败秦军。赵括说：“秦国的大将白起比较难对付，但是王龁（hé）没有什么了不起的，只能当廉颇的对手。要是换上我，打败他轻而易举。”赵王听了很高兴，就拜赵括为大将，去（接替　托管）廉颇。这个决定遭到了蔺相如的反对，可是赵王听不进去蔺相如的劝告。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "③赵括的母亲也给赵王上书，不赞成赵王派她儿子去换廉颇。赵王把她召了来，问她原因。赵母说：“他父亲临终时再三（嘱托　嘱咐）我说，‘赵括这孩子把用兵打仗看作儿戏似的，派不上用场。将来大王不用他还好，如果用他为大将的话，只怕赵军断送在他手里。’所以我请求大王千万别让他当大将。”赵王说：“你不要管了，我已经决定了。”",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_footer(doc, "语文·四上·第二单元　第 3 页（共 4 页）")
    add_page_break(doc)

    exam_body(
        doc,
        "④赵括替换廉颇的消息传到秦国，秦国知道反间计成功了，就秘密派白起代替王龁为上将军，去指挥秦军。白起到长平后，布置好埋伏，故意打了几个败仗。赵括不知是计，带兵拼命追击秦军。白起把赵军引到（预先　预备）埋伏好的地区，把赵括的兵马围在当中，无计可施的赵括带兵向外突围，被秦军乱箭射死。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(
        doc,
        "⑤40万赵军，全部葬送在纸上谈兵的主帅赵括手里。",
        first_line=Cm(0.74),
        size=10,
        space_after=2,
    )
    exam_body(doc, "（选自《中华上下五千年》，有改动）", size=9)

    exam_body(doc, "1. 用“\\”画掉文中括号里不恰当的词语。")
    exam_body(doc, "2. 从文中找到与释义相同的词语，写在括号里。")
    exam_body(doc, "　　（1）说话像瀑布流泻一样滔滔不绝，形容能言善辩。（　　　　）")
    exam_body(doc, "　　（2）没有计谋可以施展，指想不出对策，没有任何办法。（　　　　）")
    exam_body(doc, "　　（3）在文字上谈用兵策略，比喻不联系实际情况，空发议论。（　　　　）")
    exam_body(doc, "3. 文中的赵括给你留下了怎样的印象？把理由写下来。")
    write_lines(doc, 2)
    exam_body(doc, "4. 试着从不同角度提出问题，把你认为值得思考的一个问题写下来，并尝试解答。")
    exam_body(doc, "　　值得思考的问题：________________________________________？")
    exam_body(doc, "　　尝试解答：________________________________________________。")

    exam_section(doc, "七、习作。")
    exam_body(
        doc,
        "我们身边有很多熟悉的人：家人、朋友、老师、邻居……他们身上都有自己的特点。请你选择其中一个人，用一个印象深刻的事例，写出他（她）与众不同的特点。要求：语句通顺，事例具体。",
        size=10,
    )
    write_lines(doc, 8, size=13, space_after=3)
    exam_footer(doc, "语文·四上·第二单元　第 4 页（共 4 页）")
    return doc


def build_u3():
    doc = exam_doc()
    exam_header(doc, "语文·四上·第三单元练习")

    # —— 第 1 页：田字格加大，段距拉开，写得下 ——
    exam_section(doc, "一、看拼音，写词语。")
    add_inline_pinyin_line(
        doc,
        [
            ("guāng huá", 2),
            "的墙壁上，",
            ("nèn lǜ", 2),
            "的",
            ("pá shān hǔ", 3),
            "正悄悄生长，叶片之间毫不拥挤，还留着",
        ],
        box_cm=1.15,
        after=10,
    )
    add_inline_pinyin_line(
        doc,
        [("jūn yún", 2), "的", ("kòng xì", 2), "，看着格外舒服。"],
        box_cm=1.15,
        after=12,
    )

    exam_section(doc, "二、在加点字的正确读音下面画“√”。")
    exam_body(doc, "1. 战士们顽强抵抗，绝不投 降（jiàng　xiáng），任凭气温不断 降（jiàng　xiáng）低，也没有退缩。", space_after=10)
    exam_body(doc, "2. 他一边哼着欢快的歌 曲（qǔ　qū），一边沿着 曲（qǔ　qū）折的小路往前走。", space_after=10)
    exam_body(doc, "3. 这株植物的 茎（jīng　jìng）纤细，所以搬动时需格外谨 慎（chèn　shèn）。", space_after=12)

    exam_section(doc, "三、按要求选择正确答案，将序号填在括号里。")
    exam_body(doc, "1. 选出下列每组词语中有错别字的一项。", space_after=6)
    exam_body(doc, "　　（1）①住宅　②柔弱　③痕际　　（　　）", space_after=8)
    exam_body(doc, "　　（2）①选择　②平担　③叶柄　　（　　）", space_after=8)
    exam_body(doc, "　　（3）①大厅　②触脚　③增长　　（　　）", space_after=10)
    exam_body(doc, "2. 下列诗句中，加点字词解释正确的一项是（　　）", space_after=6)
    exam_body(doc, "　　①可怜九月初三夜（可惜）", space_after=6)
    exam_body(doc, "　　②只缘身在此山中（因为）", space_after=6)
    exam_body(doc, "　　③梅须逊雪三分白（谦逊）", space_after=10)

    # 用第四大题前两题填满本页下半截，避免大片空白
    exam_section(doc, "四、根据所学知识和要求填空。")
    exam_body(
        doc,
        "1. 最近下了好几场秋雨，气温越来越低，真是应了那句俗语：",
        space_after=4,
    )
    write_lines(doc, 1)
    exam_body(doc, "2. 无论从哪儿看，庐山呈现出的样子都各不相同，真是应了那句：", space_after=4)
    write_lines(doc, 1)
    end_exam_page(doc, "语文·四上·第三单元　第 1 页（共 4 页）")

    # —— 第 2 页 ——
    exam_body(doc, "3. 两位同学都观察了柳树。你更喜欢谁的写法？说明理由。")
    exam_body(
        doc,
        "小明：刚开始，枝条上冒出一个个嫩黄色的小芽，像一个个小逗号。过了几天，小芽长成了细细的叶子，颜色也变成了嫩绿色。",
        size=10,
    )
    exam_body(
        doc,
        "小红：柳树发芽了，枝条长长的，叶子绿绿的，很好看。风一吹，枝条就动来动去，真漂亮。",
        size=10,
    )
    exam_body(doc, "我喜欢________，因为")
    write_lines(doc, 2)

    exam_section(doc, "五、阅读短文，回答问题。")
    exam_body(doc, "（一）米虫", bold=True)
    exam_body(
        doc,
        "①我在厨房发现了这只米粒大小的甲虫。我想：它会不会就是米虫呢？",
        first_line=Cm(0.74),
        size=11,
        space_after=4,
    )
    exam_body(
        doc,
        "②我把它收纳进养金铃子的小盒子里，又抓了一小把大米放了进去，想近距离地观察它。它有时从大米里钻出来，在米粒上走来走去；有时从这里钻进米里，潜伏片刻，又从那端钻出来，出出进进，躲躲藏藏，玩得极有兴致。",
        first_line=Cm(0.74),
        size=11,
        space_after=4,
    )
    exam_body(
        doc,
        "③有时候，我想单独清晰地观察米虫，就把小盒子倾斜一下，大米就滑落到盒子的一侧，米虫就从米粒里凸现出来，开始在空旷的盒子里，转着圈儿走起来，就像模特儿走台步，那样子很美。有时候，走着走着，不知怎的，就侧翻倒地，仰面躺下了。它想翻过身来，先是六只脚在空中乱抓乱挑。它什么也抓挠不住，就仰面躺着，支起身体，把翅膀张开，用力扇动，使身体贴着地面向前滑行，滑到米粒处，它就倚附着翻过身来，继续走来走去。小小米虫，真是聪明！",
        first_line=Cm(0.74),
        size=11,
        space_after=4,
    )
    exam_body(doc, "（选自金波《昆虫印象》，有删改）", size=9)
    exam_body(doc, "1. 联系上下文，解释文中加点的词语。")
    exam_body(doc, "　　潜伏：")
    write_lines(doc, 1)
    end_exam_page(doc, "语文·四上·第三单元　第 2 页（共 4 页）")

    # —— 第 3 页 ——
    exam_body(doc, "2. 结合短文内容完成表格。", bold=True, space_before=2)
    add_observe_table(doc)
    exam_body(doc, "3. 生活中，你有没有像作者这样仔细观察过一种事物？请简单写两三句话。")
    write_lines(doc, 3)

    exam_body(doc, "（二）它们的聪明与愚笨", bold=True, space_before=6)
    exam_body(
        doc,
        "①为了观察黄蜂的巢穴，我在九月的一天带着我的小儿子保罗出门。他视力很好，注意力也非常集中，能帮我不少忙。我们饶有兴趣地观察着小路两旁的草地。",
        first_line=Cm(0.74),
        size=11,
        space_after=5,
    )
    exam_body(
        doc,
        "②突然，保罗喊道：“黄蜂窝！肯定是黄蜂窝！”我们小心翼翼地靠近那个地方，生怕引起这些凶猛生物的注意。它们巢穴的入口是一个圆形的洞，大约有拇指粗细，里面的居民们忙碌地进进出出，彼此擦肩而过，朝着相反的方向飞去。想到如果我们靠得太近，激怒了这些易怒的战士，将会遭遇多么难堪的场面，我不禁打了个寒战。我们没有再进一步探寻，以免付出惨痛的代价，而是记下了这个位置，决定等到夜幕降临时再回来。到那时，巢穴里的居民们都会从田野回到家中。",
        first_line=Cm(0.74),
        size=11,
        space_after=5,
    )
    exam_body(
        doc,
        "③如果不采取一定的谨慎措施，征服一个普通黄蜂的巢穴将是一项相当艰巨的任务。在尝试了各种不太成功的方法之后，我认为汽油、芦苇和一小团黏土是最好用、最简单的工具。",
        first_line=Cm(0.74),
        size=11,
        space_after=5,
    )
    exam_body(
        doc,
        "④使用汽油是因为它的效果不会太猛烈，为了便于观察，我希望能留下一小部分活着的黄蜂。巢中有一个大约九英寸长、几乎水平的前厅通往地下的蜂巢。如果直接将汽油倒进这个通道口，可能是一个带来严重后果的错误。因为这么少量的汽油会被土壤吸收，根本无法到达蜂巢；第二天，当我们以为可以安全地挖掘时，却会发现一群愤怒的黄蜂在铲子下涌出。一小段芦苇可以防止这种意外发生。将芦苇插入通道后，它就形成了一个防水的漏斗，可以迅速地将汽油一滴不漏地送入蜂巢。然后，我们用一团揉好的黏土堵住洞口。",
        first_line=Cm(0.74),
        size=11,
        space_after=5,
    )
    end_exam_page(doc, "语文·四上·第三单元　第 3 页（共 4 页）")

    # —— 第 4 页 ——
    exam_body(
        doc,
        "⑤每当准备进行这项操作时，保罗和我会在某个温和、月光皎洁的夜晚九点钟，带着一盏灯笼和装有工具的篮子出发。远处农舍的狗在相互吠叫，橄榄树间的猫头鹰在鸣叫，灌木丛中的意大利蟋蟀在演奏交响乐，保罗和我则聊着昆虫。他热切地提出问题，渴望学习，而我则告诉他我所知道的一点知识。这些捕捉黄蜂的夜晚是如此令人愉快，我们几乎不在意熬夜或被蜇的风险！",
        first_line=Cm(0.74),
        size=11,
        space_after=5,
    )
    exam_body(doc, "（选自法布尔《昆虫记》，有删改）", size=9, space_after=6)

    exam_body(doc, "1. 根据短文内容判断，正确的画“√”，错误的画“×”。")
    exam_body(
        doc,
        "　　（1）“到那时，巢穴里的居民们都会从田野回到家中。”这句话中“居民们”指的是住在这里的人们。（　　）",
        size=11,
        space_after=6,
    )
    exam_body(doc, "　　（2）作者不直接将汽油倒进黄蜂巢穴通道的原因是会立刻激怒所有黄蜂。（　　）", size=11, space_after=6)
    exam_body(doc, "　　（3）作者用来对付黄蜂巢穴的三种工具是：汽油、芦苇和黏土。（　　）", size=11, space_after=6)
    exam_body(doc, "2. 用“____”画出作者选择在夜晚去观察黄蜂原因的句子。", space_after=6)
    exam_body(doc, "3. 作者为什么说“这些捕捉黄蜂的夜晚是如此令人愉快”？")
    write_lines(doc, 3)

    exam_section(doc, "六、习作。")
    exam_body(
        doc,
        "你是否曾静下心来，仔细观察身边的事物？当我们用眼睛去看，用耳朵去听，用心去感受，就一定会有所发现。请选择你喜欢的一种事物，用日记的形式介绍一下你的收获和发现吧。",
        size=11,
    )
    exam_body(doc, "要求：1. 题目自拟。　2. 语句通顺，表达真实感受。", size=11)
    write_lines(doc, 4)
    end_exam_page(doc, "语文·四上·第三单元　第 4 页（共 4 页）", last=True)
    return doc


def add_reading_card_table(doc):
    """常羲沐月阅读卡片：行高够小学生手写。"""
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    labels = ["故事名称", "主人公", "故事中最神奇的地方", "我的阅读感受"]
    for i, lab in enumerate(labels):
        c0 = table.rows[i].cells[0]
        c1 = table.rows[i].cells[1]
        c0.text = ""
        c1.text = ""
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lab)
        set_run_font(r0, size=11, bold=True, color=INK)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run("\n")
        set_run_font(r1, size=11, color=INK)
        for cell in (c0, c1):
            _set_cell_border(cell)
        tr = table.rows[i]._tr
        trPr = tr.get_or_add_trPr()
        trHeight = OxmlElement("w:trHeight")
        # ~1.1cm 行高，够写一字行
        trHeight.set(qn("w:val"), "480")
        trHeight.set(qn("w:hRule"), "atLeast")
        trPr.append(trHeight)
        c0.width = Cm(4.2)
        c1.width = Cm(12.5)
    add_para(doc, "", size=2, space_after=2)


def build_u4():
    """第四单元练习：无习作；楷体清晰字；田字格加大；共 4 页。"""
    doc = exam_doc()
    exam_header(doc, "语文·四上·第四单元练习")

    # —— 第 1 页：一 + 二 ——
    exam_section(doc, "一、看拼音，写词语。")
    add_inline_pinyin_line(
        doc,
        ["众神沉睡了千万年，终于在", ("yǔ zhòu", 2), "中苏醒。"],
        box_cm=1.25,
        size=13,
        after=6,
    )
    add_inline_pinyin_line(
        doc,
        ["春风拂过大地，曾经驱赶黑暗的勇士虽已", ("jīng pí lì jié", 4), "，"],
        box_cm=1.2,
        size=13,
        after=6,
    )
    add_inline_pinyin_line(
        doc,
        ["但滚烫的血液仍滋养着世间，开出美丽的鲜花，让人深深", ("jìng pèi", 2), "。"],
        box_cm=1.25,
        size=13,
        after=8,
    )

    exam_section(doc, "二、按要求选择正确答案，将序号填在括号里。")
    exam_body(doc, "1. 下列词语中，加点字字音完全正确的一组是（　　）", space_after=3)
    exam_body(doc, "　　①立即（jí）　花卉（huì）", space_after=3)
    exam_body(doc, "　　②茉莉（mò）　违抗（wéi）", space_after=3)
    exam_body(doc, "　　③下降（xiáng）　肝脏（zàng）", space_after=3)
    exam_body(doc, "　　④尽管（jǐn）　花蕾（léi）", space_after=5)
    exam_body(doc, "2. 下列笔画数相同的一组是（　　）", space_after=3)
    exam_body(doc, "　　①瑰　溺　　②口　卉　　③醒　渴　　④衔　颗", space_after=5)
    exam_body(doc, "3. “遭”的第六笔是（　　）", space_after=3)
    add_stroke_choice_row(
        doc,
        [
            ("①", "hengzhe", "横折"),
            ("②", "shu", "竖"),
            ("③", "ti", "提"),
            ("④", "dian", "点"),
        ],
        icon_cm=0.95,
        size=12,
    )
    exam_body(
        doc,
        "4. “醒”在词典中的意思有：①酒醉、麻醉或昏迷后神志恢复正常状态；②睡眠状态结束，大脑皮层恢复兴奋状态，也指尚未入睡；③醒悟；觉悟；④明显，清楚。给下列词语中的“醒”选择正确的意思，将序号填在括号里。",
        size=12,
        space_after=3,
    )
    exam_body(
        doc,
        "　　（1）醒目（　　）　（2）清醒（　　）　（3）大梦初醒（　　）　（4）提醒（　　）",
        space_after=4,
    )
    end_exam_page(doc, "语文·四上·第四单元　第 1 页（共 4 页）")

    # —— 第 2 页：二·5 + 三 + 四 + 五（一）开篇 ——
    exam_body(doc, "5. 下列说法中有误的一项是（　　）", space_after=3)
    exam_body(doc, "　　①神话故事里的人物往往具有非凡的本领和鲜明的性格", space_after=2)
    exam_body(doc, "　　②普罗米修斯、宙斯、赫淮斯托斯都是古希腊神话中的人物", space_after=2)
    exam_body(doc, "　　③神话充满了神奇的想象，里面很多人物个性都很鲜明", space_after=2)
    exam_body(doc, "　　④神话是真实的，古人用神话来表达他们对世界的认识", space_after=6)

    exam_section(doc, "三、按要求填空。")
    exam_body(doc, "1. 选字填空。（既　即）", space_after=3)
    exam_body(doc, "　　立（　　）　　（　　）然　　（　　）时　　（　　）刻", space_after=6)
    exam_body(doc, "2. 按课文内容填空。", space_after=3)
    exam_body(
        doc,
        "　　女娃____________________，溺而不返，故为精卫，____________________，以堙于东海。",
        space_after=8,
    )

    exam_section(doc, "四、将下面的词语与联想到的人物用线连起来。")
    exam_body(doc, "三头六臂　　　未卜先知　　　各显神通　　　开天辟地", space_after=14)
    exam_body(doc, "哪　吒　　　　盘　古　　　　诸葛亮　　　　八　仙", space_after=10)

    exam_section(doc, "五、阅读短文，回答问题。")
    exam_body(doc, "（一）共工怒撞不周山", bold=True, space_after=3)
    exam_body(
        doc,
        "①在远古的神话里，水神共工和火神祝融，为了争夺天地间的统治权，展开了一场惊天动地的大战。",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    exam_body(
        doc,
        "②共工骑着凶猛的黑龙，（指挥　指使）着滔滔洪水，掀起万丈巨浪；祝融驾着火龙，喷出熊熊烈火，烧得天地一片通红。双方打得昏天黑地，从天上一直打到人间，洪水泛滥（fàn làn），大火蔓延，生灵涂炭（tàn）。大战持续了很久很久，共工渐渐落了下风，他的手下一个个被打败，自己也被逼得走投无路。",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    exam_body(
        doc,
        "③看着手下一个个倒下，共工既心痛又愤怒，心里满是（不解　不甘）。他猛地转过头，朝着天边那根撑着天空的巨柱——不周山，发疯似的撞了过去。只听“轰隆”一声巨响，不周山瞬间断成两截！天柱一倒，天地立刻变了模样：天空向西北方向倾斜，日月星辰都跟着往西移动；大地向东南方向塌陷，江河湖水都朝着东边奔涌流淌。",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    end_exam_page(doc, "语文·四上·第四单元　第 2 页（共 4 页）")

    # —— 第 3 页：共工④+题 + 常羲开篇 ——
    exam_body(
        doc,
        "④共工这一撞，虽然让自己遭受了重创，也搅乱了天地秩序，却也让天地形成了如今日月运转、江河东流的模样，成了神话里一段（震撼　振动）人心的故事。",
        first_line=Cm(0.74),
        size=12,
        space_after=2,
    )
    exam_body(doc, "（根据《淮南子·天文训》相关内容改写）", size=10, space_after=5)

    exam_body(doc, "1. 根据句子的意思在文中找到相应的词语，写在括号里。", space_after=3)
    exam_body(
        doc,
        "　　（1）所有的生命都陷在泥塘和火坑里，形容万物处于极端困苦的境地。（　　　　　　）",
        space_after=4,
    )
    exam_body(doc, "　　（2）形容陷入绝境，找不到出路。（　　　　　　）", space_after=5)
    exam_body(doc, "2. 根据语境，从文中括号里选择合适的词语，在正确的下面画“√”。", space_after=5)
    exam_body(doc, "3. 请你按照起因、经过、结果的顺序，把故事的主要内容填写完整。", space_after=3)
    exam_body(doc, "　　（1）起因：________________________________", space_after=4)
    exam_body(
        doc,
        "　　（2）经过：大战中共工渐渐落败，走投无路之下，一头撞向撑天的不周山。",
        space_after=4,
    )
    exam_body(doc, "　　（3）结果：________________________________", space_after=4)
    exam_body(doc, "4. 读了短文，你喜欢文中的共工吗？说说你的理由。", space_after=2)
    write_lines(doc, 2, size=15, space_after=6)

    exam_body(doc, "（二）常羲沐月", bold=True, space_before=4, space_after=3)
    exam_body(
        doc,
        "①在遥远的上古神话中，住着一位温柔又圣洁的女神，她的名字叫常羲。她是月亮的母亲，掌管着天上的月亮。",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    exam_body(
        doc,
        "②常羲一共生下了十二个月亮女儿，这十二个月亮长得一模一样，都是圆的、亮晶晶的，像一颗颗温润的玉盘。她们轮流挂在天上，照亮漆黑的夜晚，陪着人间的百姓度过一个个黑夜。",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    end_exam_page(doc, "语文·四上·第四单元　第 3 页（共 4 页）")

    # —— 第 4 页：常羲续 + 阅读题（无习作）——
    exam_body(
        doc,
        "③每天清晨，当最后一个月亮女儿从天上落下，常羲就会带着她们，来到天地边缘的清澈银河里，为月亮女儿们沐浴。她用温柔的手，轻轻拂去月亮身上的灰尘，让月亮变得干干净净，重新焕发出柔和的光芒。银河的水凉凉的、清清的。月亮女儿们钻进水里，你推我一下，我挤你一下，圆滚滚的身子在水面上滚来滚去，溅起一串串亮晶晶的水花；有的月亮女儿还会比赛谁游得快，银白色的身影在水里一闪而过，留下淡淡的波纹。洗完澡，她们总喜欢围着常羲撒娇：有的靠在常羲的身上，听妈妈讲人间的趣事……",
        first_line=Cm(0.74),
        size=12,
        space_after=3,
    )
    exam_body(
        doc,
        "④洗完澡后，常羲会细心地把女儿们安顿在月宫休息，等着她们轮流上岗，照亮人间。日复一日，年复一年，常羲从不偷懒，她用满满的爱意守护着十二个月亮，也守护着人间的夜色。人们都十分敬佩这位温柔又尽责的月亮女神。",
        first_line=Cm(0.74),
        size=12,
        space_after=2,
    )
    exam_body(doc, "（根据《山海经·大荒西经》相关内容改写）", size=10, space_after=5)

    exam_body(doc, "1. 从文中找出和下面词语意思相近的词，写在括号里。", space_after=3)
    exam_body(doc, "　　温顺——（　　　　　　）　　佩服——（　　　　　　）", space_after=5)
    exam_body(
        doc,
        "2. 文中画横线的句子后面用了省略号，省略了月亮女儿们围着妈妈撒娇的画面，请你展开想象，写一两句话，写出省略的内容。",
        size=12,
        space_after=2,
    )
    write_lines(doc, 2, size=15, space_after=6)
    exam_body(doc, "3. 请你根据这篇神话故事的内容，完成下面的阅读卡片。", space_after=2)
    add_reading_card_table(doc)
    exam_body(
        doc,
        "4. 推荐一个你最喜欢的中国古代神话故事，用两三句话说说理由。",
        size=12,
        space_after=2,
    )
    write_lines(doc, 2, size=15, space_after=5)
    end_exam_page(doc, "语文·四上·第四单元　第 4 页（共 4 页）", last=True)
    return doc


def save_pair(doc, stem: str):
    PRINT.mkdir(parents=True, exist_ok=True)
    docx_path = PRINT / f"{stem}.docx"
    pdf_path = PRINT / f"{stem}.pdf"
    doc.save(str(docx_path))
    print("Wrote", docx_path.name)
    try:
        docx_to_pdf(docx_path, pdf_path)
        print("Wrote", pdf_path.name)
    except Exception as e:
        print("PDF convert failed:", e)
        import subprocess

        ps = (
            f"$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
            f"$d=$w.Documents.Open('{docx_path.resolve()}'); "
            f"$d.SaveAs([ref]'{pdf_path.resolve()}',[ref]17); $d.Close($false); $w.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
        print("Wrote", pdf_path.name, "(fallback)")


def main():
    import sys

    targets = sys.argv[1:] or ["u1", "u2", "u3", "u4"]
    builders = {
        "u1": ("u01-full", build_u1),
        "u2": ("u02-full", build_u2),
        "u3": ("u03-full", build_u3),
        "u4": ("u04-full", build_u4),
    }
    for t in targets:
        stem, fn = builders[t]
        save_pair(fn(), stem)
    print("done", targets)


if __name__ == "__main__":
    main()
