/* 语文书桌 · 主页 / 路径 / 记录 */
window.CHINESE_DESK_DATA = {
  title: "语文书桌",
  book: "统编版四年级上册",
  currentBookLesson: 8,
  brandNote: "先默写过关，再练考点。与教材课次同步。",
  units: [
    {
      id: "u1",
      name: "第一单元 · 自然之美",
      lessons: [
        {
          id: "u1l1",
          bookNo: 1,
          title: "观潮",
          kind: "精读",
          words: [
            { zh: "潮汐", py: "cháo xī" },
            { zh: "据说", py: "jù shuō" },
            { zh: "大堤", py: "dà dī" },
            { zh: "盼望", py: "pàn wàng" },
            { zh: "逐渐", py: "zhú jiàn" },
            { zh: "浩浩荡荡", py: "hào hào dàng dàng" },
            { zh: "山崩地裂", py: "shān bēng dì liè" },
            { zh: "霎时", py: "shà shí" },
          ],
          compounds: [
            { a: "潮", b: "朝", hint: "浪潮 / 朝阳" },
            { a: "堤", b: "提", hint: "堤坝 / 提醒" },
            { a: "盼", b: "扮", hint: "盼望 / 扮演" },
          ],
          polyphones: [
            { word: "观潮", opts: ["cháo", "zhāo"], ok: "cháo" },
            { word: "朝阳", opts: ["cháo", "zhāo"], ok: "zhāo" },
            { word: "闷雷", opts: ["mēn", "mèn"], ok: "mèn" },
          ],
          recite: {
            label: "背诵第3～4自然段",
            prompt: "浪潮越来越近，犹如千万匹白色战马____，____地飞奔而来；那声音如同____。",
            answer: "齐头并进；浩浩荡荡；山崩地裂",
          },
          meaning: {
            prompt: "用两三句话说说《观潮》主要写了什么？（按潮来顺序）",
            sample: "写钱塘江大潮来前、来时、来后的景象与声势，突出天下奇观。",
          },
        },
        {
          id: "u1l2",
          bookNo: 2,
          title: "走月亮",
          kind: "精读",
          words: [
            { zh: "鹅卵石", py: "é luǎn shí" },
            { zh: "坑坑洼洼", py: "kēng keng wā wā" },
            { zh: "稻穗", py: "dào suì" },
            { zh: "成熟", py: "chéng shú" },
            { zh: "葡萄", py: "pú tao" },
            { zh: "闪烁", py: "shǎn shuò" },
          ],
          compounds: [
            { a: "卵", b: "卯", hint: "鹅卵石 / 丁卯" },
            { a: "稻", b: "蹈", hint: "稻田 / 舞蹈" },
          ],
          polyphones: [{ word: "成熟", opts: ["shú", "shóu"], ok: "shú" }],
          recite: {
            label: "背诵第4自然段",
            prompt: "每个小水塘都抱着一个____！稻穗____，稻田像一块月光镀亮的____。",
            sample: "月亮；低垂着头；银毯",
            answer: "月亮；低垂着头；银毯",
          },
          meaning: {
            prompt: "《走月亮》写了谁和谁？主要写怎样的情景与感受？",
            sample: "写“我”和阿妈在月下散步，感受月光下家乡的美好与温馨。",
          },
        },
        {
          id: "u1l3",
          bookNo: 3,
          title: "现代诗二首",
          kind: "略读",
          words: [
            { zh: "秋晚", py: "qiū wǎn" },
            { zh: "花牛", py: "huā niú" },
          ],
          compounds: [],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "任选一首，说说诗中最美的一个画面。",
            sample: "抓住颜色、动作或声音，说出自己的感受即可。",
          },
        },
        {
          id: "u1l4",
          bookNo: 4,
          title: "繁星",
          kind: "略读",
          words: [
            { zh: "繁星", py: "fán xīng" },
            { zh: "模糊", py: "mó hu" },
            { zh: "飞舞", py: "fēi wǔ" },
            { zh: "柔和", py: "róu hé" },
            { zh: "梦幻", py: "mèng huàn" },
            { zh: "摇摇欲坠", py: "yáo yáo yù zhuì" },
          ],
          compounds: [
            { a: "昧", b: "妹", hint: "暧昧 / 姐妹" },
          ],
          polyphones: [{ word: "模糊", opts: ["mó", "mú"], ok: "mó" }],
          recite: null,
          meaning: {
            prompt: "作者看繁星时有怎样的感受？为什么觉得像睡在母亲怀里？",
            sample: "温柔、安心；繁星让他感到被环抱、被爱护。",
          },
        },
      ],
      garden: {
        id: "u1g",
        title: "语文园地一",
        accumulate: {
          title: "日积月累 ·《鹿柴》",
          author: "唐 · 王维",
          lines: ["空山不见人，", "但闻人语响。", "返景入深林，", "复照青苔上。"],
          linesDetail: [
            { text: "空山不见人，", tip: "空旷的山里看不见人。" },
            { text: "但闻人语响。", tip: "只听见有人说话的声音。" },
            { text: "返景入深林，", tip: "夕阳余光（返照）照进幽深的树林。" },
            { text: "复照青苔上。", tip: "又照在青苔上面。" },
          ],
          meaning:
            "空山里看不见人，只听见人说话的声音；夕阳余光照进深林，又照在青苔上。全诗写幽静空山：以响衬静，以光写暗。",
          background: "王维，唐代诗人、画家，诗中有画。柴读 zhài。返景＝夕阳返照。须会背、会默、懂每句意思。",
        },
        extra: "单元测还常考《赠刘景文》（宋·苏轼）：荷尽已无擎雨盖，菊残犹有傲霜枝。一年好景君须记，最是橙黄橘绿时。",
      },
    },
    {
      id: "u2",
      name: "第二单元 · 提问与思考",
      lessons: [
        {
          id: "u2l5",
          bookNo: 5,
          title: "一个豆荚里的五粒豆",
          kind: "精读",
          words: [
            { zh: "豌豆", py: "wān dòu" },
            { zh: "舒适", py: "shū shì" },
            { zh: "僵硬", py: "jiāng yìng" },
            { zh: "囚犯", py: "qiú fàn" },
            { zh: "揭晓", py: "jiē xiǎo" },
          ],
          compounds: [
            { a: "豌", b: "碗", hint: "豌豆 / 饭碗" },
            { a: "僵", b: "疆", hint: "僵硬 / 边疆" },
          ],
          polyphones: [{ word: "囚犯", opts: ["qiú", "qiū"], ok: "qiú" }],
          recite: null,
          meaning: {
            prompt: "五粒豌豆各有怎样的结局？你觉得哪一粒最了不起？为什么？",
            sample: "一粒落窗台长成苗，给生病女孩带来希望；谈“有用/善良”即可。",
          },
        },
        {
          id: "u2l6",
          bookNo: 6,
          title: "夜间飞行的秘密",
          kind: "精读",
          words: [
            { zh: "蝙蝠", py: "biān fú" },
            { zh: "超声波", py: "chāo shēng bō" },
            { zh: "障碍", py: "zhàng ài" },
            { zh: "敏锐", py: "mǐn ruì" },
          ],
          compounds: [
            { a: "蝠", b: "福", hint: "蝙蝠 / 幸福" },
          ],
          polyphones: [
            { word: "蝙蝠", opts: ["biān", "biǎn"], ok: "biān" },
            { word: "一溜烟", opts: ["liū", "liù"], ok: "liù" },
          ],
          recite: null,
          meaning: {
            prompt: "蝙蝠夜间飞行靠什么？科学家从中得到什么启发？",
            sample: "靠嘴发超声波、耳朵接收；启发发明雷达。",
          },
        },
        {
          id: "u2l7",
          bookNo: 7,
          title: "呼风唤雨的世纪",
          kind: "精读",
          words: [
            { zh: "呼风唤雨", py: "hū fēng huàn yǔ" },
            { zh: "世纪", py: "shì jì" },
            { zh: "奥秘", py: "ào mì" },
          ],
          compounds: [
            { a: "唤", b: "换", hint: "呼唤 / 交换" },
            { a: "纪", b: "记", hint: "世纪 / 记忆" },
          ],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "为什么说20世纪是一个“呼风唤雨”的世纪？",
            sample: "科技发展让人类能做过去神话里才能做的事。",
          },
        },
        {
          id: "u2l8",
          bookNo: 8,
          title: "蝴蝶的家",
          kind: "略读",
          words: [
            { zh: "蝴蝶", py: "hú dié" },
            { zh: "避雨", py: "bì yǔ" },
            { zh: "珍惜", py: "zhēn xī" },
            { zh: "安然", py: "ān rán" },
          ],
          compounds: [
            { a: "蝶", b: "碟", hint: "蝴蝶 / 碟子" },
          ],
          polyphones: [{ word: "避开", opts: ["bì", "pì"], ok: "bì" }],
          recite: null,
          meaning: {
            prompt: "作者为什么为蝴蝶着急？你从中读出怎样的情感？",
            sample: "担心雨中蝴蝶无处安家；体现对弱小生命的关爱。",
          },
        },
      ],
      garden: {
        id: "u2g",
        title: "语文园地二",
        accumulate: {
          title: "日积月累 · 提问名句",
          items: [
            {
              text: "好问则裕，自用则小。",
              who: "《尚书》",
              tip: "勤问才能知识丰富；自以为是就眼界狭小。",
            },
            {
              text: "博学之，审问之，慎思之，明辨之，笃行之。",
              who: "《礼记》",
              tip: "广泛地学、详细地问、谨慎地想、清楚地辨、切实地做。（学问思辨行）",
            },
            {
              text: "智能之士，不学不成，不问不知。",
              who: "王充",
              tip: "再聪明的人，不学习就难有成就，不请教就难懂事理。",
            },
            {
              text: "人非生而知之者，孰能无惑？",
              who: "韩愈",
              tip: "人不是生下来就什么都懂，谁能没有疑惑呢？（孰＝谁）",
            },
            {
              text: "善疑者，不疑人之所疑，而疑人之所不疑。",
              who: "方以智",
              tip: "善于提问的人，不只怀疑别人已经怀疑的，更要去怀疑别人还没想到的。",
            },
          ],
          background:
            "教材日积月累：《尚书》→《礼记》（《中庸》）→王充→韩愈；试卷常考方以智「善疑者…」。须会背、会默、会填关键词、能据意写原句。",
        },
      },
    },
    {
      id: "u3",
      name: "第三单元 · 观察与发现",
      lessons: [
        {
          id: "u3l9",
          bookNo: 9,
          title: "古诗三首",
          kind: "精读",
          words: [],
          compounds: [{ a: "逊", b: "孙", hint: "逊色 / 子孙" }],
          polyphones: [],
          recite: {
            label: "默写《题西林壁》名句",
            prompt: "横看成岭侧成峰，____。不识庐山真面目，____。",
            answer: "远近高低各不同；只缘身在此山中",
          },
          meaning: {
            prompt: "「只缘身在此山中」的「缘」是什么意思？说明了什么道理？",
            sample: "缘=因为；当局者迷，要全面看事物。",
          },
          poems: [
            { title: "暮江吟", author: "唐·白居易", tip: "写江上残阳与九月初三月色。" },
            { title: "题西林壁", author: "宋·苏轼", tip: "写庐山多角度景象与哲理。" },
            { title: "雪梅", author: "宋·卢钺", tip: "梅雪争春，各有千秋。" },
          ],
        },
        {
          id: "u3l10",
          bookNo: 10,
          title: "爬山虎的脚",
          kind: "精读",
          words: [
            { zh: "光滑", py: "guāng huá" },
            { zh: "嫩绿", py: "nèn lǜ" },
            { zh: "爬山虎", py: "pá shān hǔ" },
            { zh: "均匀", py: "jūn yún" },
            { zh: "空隙", py: "kòng xì" },
          ],
          compounds: [
            { a: "均", b: "钧", hint: "均匀 / 千钧" },
          ],
          polyphones: [
            { word: "曲折", opts: ["qǔ", "qū"], ok: "qū" },
            { word: "空隙", opts: ["kòng", "kōng"], ok: "kòng" },
          ],
          recite: null,
          meaning: {
            prompt: "爬山虎的“脚”长什么样？有什么作用？",
            sample: "茎上细丝状，末端圆片；贴墙固定，帮助往上爬。",
          },
        },
        {
          id: "u3l11",
          bookNo: 11,
          title: "蟋蟀的住宅",
          kind: "精读",
          words: [
            { zh: "住宅", py: "zhù zhái" },
            { zh: "洞穴", py: "dòng xué" },
            { zh: "慎重", py: "shèn zhòng" },
            { zh: "柔弱", py: "róu ruò" },
          ],
          compounds: [
            { a: "宅", b: "诧", hint: "住宅 / 惊诧" },
            { a: "慎", b: "填", hint: "慎重 / 填写" },
          ],
          polyphones: [{ word: "慎重", opts: ["shèn", "chén"], ok: "shèn" }],
          recite: null,
          meaning: {
            prompt: "蟋蟀的住宅有哪些特点？说明它怎样？",
            sample: "向阳、排水好、干净；说明蟋蟀是出色的建筑师、很勤劳。",
          },
        },
      ],
      garden: {
        id: "u3g",
        title: "语文园地三",
        accumulate: {
          title: "日积月累 · 秋日谚语",
          items: [
            {
              text: "立了秋，把扇丢。",
              who: "谚语",
              tip: "立秋之后天气转凉，扇子可以收起来了。",
            },
            {
              text: "二八月，乱穿衣。",
              who: "谚语",
              tip: "农历二月、八月早晚温差大，穿衣容易忽冷忽热。",
            },
            {
              text: "夏雨少，秋霜早。",
              who: "谚语",
              tip: "夏天雨水少，秋天霜来得早。",
            },
            {
              text: "八月里来雁门开，雁儿脚上带霜来。",
              who: "谚语",
              tip: "农历八月大雁南飞，带来霜降将至的消息。",
            },
            {
              text: "一场秋雨一场寒，十场秋雨要穿棉。",
              who: "谚语",
              tip: "秋雨一场比一场冷，多场秋雨后就要穿棉衣了。",
            },
            {
              text: "八月暖，九月温，十月还有小阳春。",
              who: "谚语",
              tip: "农历八月仍暖、九月温和，十月还会有一段像春天一样的暖和天气（小阳春）。",
            },
          ],
          background:
            "本单元学观察。这些谚语写秋天天气变化，须会背、会默、懂每句意思。注意：二八月＝农历二月和八月。",
        },
      },
    },
    {
      id: "u4",
      name: "第四单元 · 神话故事",
      lessons: [
        {
          id: "u4l12",
          bookNo: 12,
          title: "盘古开天地",
          kind: "精读",
          words: [
            { zh: "宇宙", py: "yǔ zhòu" },
            { zh: "混沌", py: "hùn dùn" },
            { zh: "开天辟地", py: "kāi tiān pì dì" },
          ],
          compounds: [{ a: "辟", b: "僻", hint: "开辟 / 偏僻" }],
          polyphones: [{ word: "混沌", opts: ["hùn", "hún"], ok: "hùn" }],
          recite: null,
          meaning: {
            prompt: "盘古怎样开天辟地？身体变成了什么？",
            sample: "用斧头劈开混沌；身体化作日月山川草木等。",
          },
        },
        {
          id: "u4l13",
          bookNo: 13,
          title: "精卫填海",
          kind: "精读",
          words: [
            { zh: "精卫", py: "jīng wèi" },
            { zh: "衔", py: "xián" },
            { zh: "填海", py: "tián hǎi" },
          ],
          compounds: [{ a: "衔", b: "街", hint: "衔石 / 街道" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "精卫为什么要填海？表现了怎样的精神？",
            sample: "被海水淹没后决心填平东海；坚韧不拔、不畏困难。",
          },
        },
        {
          id: "u4l14",
          bookNo: 14,
          title: "普罗米修斯",
          kind: "精读",
          words: [
            { zh: "惩罚", py: "chéng fá" },
            { zh: "造福", py: "zào fú" },
            { zh: "火种", py: "huǒ zhǒng" },
          ],
          compounds: [{ a: "惩", b: "澄", hint: "惩罚 / 澄清" }],
          polyphones: [{ word: "种", opts: ["zhǒng", "zhòng"], ok: "zhǒng" }],
          recite: null,
          meaning: {
            prompt: "普罗米修斯为什么盗火？后来怎样了？",
            sample: "为人类带来火种与文明；被钉在高加索山遭受惩罚，仍不屈服。",
          },
        },
        {
          id: "u4l15",
          bookNo: 15,
          title: "女娲补天",
          kind: "略读",
          words: [
            { zh: "塌陷", py: "tā xiàn" },
            { zh: "冶炼", py: "yě liàn" },
            { zh: "窟窿", py: "kū long" },
          ],
          compounds: [{ a: "炼", b: "练", hint: "冶炼 / 练习" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "女娲怎样补天？说明她怎样？",
            sample: "炼五色石补天、斩鳌足立四极等；勇敢、善良、造福人类。",
          },
        },
      ],
      garden: {
        id: "u4g",
        title: "语文园地四",
        accumulate: {
          title: "日积月累 ·《嫦娥》",
          author: "唐 · 李商隐",
          lines: [
            "云母屏风烛影深，",
            "长河渐落晓星沉。",
            "嫦娥应悔偷灵药，",
            "碧海青天夜夜心。",
          ],
          linesDetail: [
            { text: "云母屏风烛影深，", tip: "云母装饰的屏风上，烛光的影子又深又暗。" },
            { text: "长河渐落晓星沉。", tip: "银河渐渐西斜，晨星也沉落了。（长河＝银河）" },
            { text: "嫦娥应悔偷灵药，", tip: "料想嫦娥该后悔偷吃了长生不老药。（应＝料想）" },
            { text: "碧海青天夜夜心。", tip: "面对碧海般的青天，夜夜感到孤单寂寞。" },
          ],
          meaning:
            "屏风上烛影深深，银河西斜、晨星沉落；嫦娥大概后悔偷了灵药，从此只能夜夜面对碧海青天，孤清寂寞。",
          background:
            "李商隐，晚唐诗人，与杜牧合称「小李杜」。借嫦娥奔月写孤寂。须会背、会默、懂每句意思。",
        },
      },
    },
    {
      id: "u5",
      name: "第五单元 · 习作单元",
      lessons: [
        {
          id: "u5l16",
          bookNo: 16,
          title: "麻雀",
          kind: "精读",
          words: [
            { zh: "嗅", py: "xiù" },
            { zh: "愣", py: "lèng" },
            { zh: "拯救", py: "zhěng jiù" },
          ],
          compounds: [{ a: "拯", b: "丞", hint: "拯救 / 丞相" }],
          polyphones: [{ word: "嗅", opts: ["xiù", "chòu"], ok: "xiù" }],
          recite: null,
          meaning: {
            prompt: "老麻雀为什么会扑下来？表现了什么？",
            sample: "为了保护小麻雀，不顾自身安危；母爱的伟大。",
          },
        },
        {
          id: "u5l17",
          bookNo: 17,
          title: "爬天都峰",
          kind: "精读",
          words: [
            { zh: "攀着", py: "pān zhe" },
            { zh: "石级", py: "shí jí" },
            { zh: "居然", py: "jū rán" },
          ],
          compounds: [{ a: "攀", b: "樊", hint: "攀登 / 姓樊" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "「我」和老爷爷是怎样爬上天都峰的？说明了什么？",
            sample: "互相鼓励、一起爬上去；勇于挑战、善于从别人身上汲取力量。",
          },
        },
      ],
      garden: {
        id: "u5g",
        title: "语文园地五（习作）",
        accumulate: {
          title: "本单元为习作单元",
          items: [
            {
              text: "本单元重点：写清楚事情的经过",
              who: "习作要点",
              tip: "第五单元是习作单元，教材没有「日积月累」古诗文；请把功夫放在把一件事写清楚（起因—经过—结果），学习例文《我家的杏熟了》《小木船》。",
            },
          ],
          background: "统编四上第五单元为习作单元，无日积月累背诵篇目。",
        },
      },
    },
    {
      id: "u6",
      name: "第六单元 · 体会人物心情",
      lessons: [
        {
          id: "u6l18",
          bookNo: 18,
          title: "牛和鹅",
          kind: "精读",
          words: [
            { zh: "姑娘", py: "gū niang" },
            { zh: "故意", py: "gù yì" },
            { zh: "捶", py: "chuí" },
          ],
          compounds: [{ a: "鹅", b: "饿", hint: "鹅鸭 / 饥饿" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "「我」对牛和鹅的态度有什么变化？明白了什么？",
            sample: "从怕鹅欺牛到敢赶鹅；对待强弱要平等，不能欺软怕硬。",
          },
        },
        {
          id: "u6l19",
          bookNo: 19,
          title: "一只窝囊的大老虎",
          kind: "精读",
          words: [
            { zh: "窝囊", py: "wō nang" },
            { zh: "殷切", py: "yīn qiè" },
            { zh: "露馅", py: "lòu xiàn" },
          ],
          compounds: [{ a: "囊", b: "襄", hint: "窝囊 / 襄阳" }],
          polyphones: [{ word: "露馅", opts: ["lòu", "lù"], ok: "lòu" }],
          recite: null,
          meaning: {
            prompt: "「我」为什么觉得自己演老虎演得窝囊？",
            sample: "不会豁虎跳却被选上；上台紧张、表演失败，心里委屈又难受。",
          },
        },
        {
          id: "u6l20",
          bookNo: 20,
          title: "陀螺",
          kind: "精读",
          words: [
            { zh: "冰冻", py: "bīng dòng" },
            { zh: "威风", py: "wēi fēng" },
            { zh: "嘲笑", py: "cháo xiào" },
          ],
          compounds: [{ a: "嘲", b: "潮", hint: "嘲笑 / 潮水" }],
          polyphones: [{ word: "嘲", opts: ["cháo", "zhāo"], ok: "cháo" }],
          recite: null,
          meaning: {
            prompt: "「我」的陀螺后来怎样？明白了什么道理？",
            sample: "其貌不扬却战胜了大陀螺；不要以貌取人，要看实力。",
          },
        },
      ],
      garden: {
        id: "u6g",
        title: "语文园地六",
        accumulate: {
          title: "日积月累 · 成语/俗语",
          items: [
            {
              text: "尺有所短，寸有所长。",
              who: "俗语",
              tip: "每个人都有短处，也有长处；不要只看一面。",
            },
            {
              text: "机不可失，时不再来。",
              who: "俗语",
              tip: "好机会不能放过，错过就很难再有。",
            },
            {
              text: "差之毫厘，谬以千里。",
              who: "俗语",
              tip: "开头差一点点，结果可能错出很远。（谬读 miù）",
            },
            {
              text: "病从口入，祸从口出。",
              who: "俗语",
              tip: "生病常因饮食不慎；惹祸常因说话不慎。",
            },
            {
              text: "一言既出，驷马难追。",
              who: "俗语",
              tip: "话一说出口，四匹马拉的车也追不回；说话要算数。",
            },
            {
              text: "比上不足，比下有余。",
              who: "俗语",
              tip: "跟更好的比还差些，跟更差的比还强些；常用来自我宽慰或客观看待。",
            },
          ],
          background:
            "六句多为相对工整的俗语。须会背、会默、懂每句意思，并能说说适用场合。",
        },
      },
    },
    {
      id: "u7",
      name: "第七单元 · 家国情怀",
      lessons: [
        {
          id: "u7l21",
          bookNo: 21,
          title: "古诗三首",
          kind: "精读",
          words: [],
          compounds: [],
          polyphones: [],
          recite: {
            label: "默写《别董大》名句",
            prompt: "莫愁前路无知己，____。",
            answer: "天下谁人不识君",
          },
          meaning: {
            prompt: "《出塞》《凉州词》《夏日绝句》各写了什么？",
            sample: "边塞征战；边塞风光与征人；项羽不肯苟活的气概。",
          },
          poems: [
            { title: "出塞", author: "唐·王昌龄", tip: "秦时明月汉时关…" },
            { title: "凉州词", author: "唐·王翰", tip: "葡萄美酒夜光杯…" },
            { title: "夏日绝句", author: "宋·李清照", tip: "生当作人杰…" },
          ],
        },
        {
          id: "u7l22",
          bookNo: 22,
          title: "为中华之崛起而读书",
          kind: "精读",
          words: [
            { zh: "租界", py: "zū jiè" },
            { zh: "耀武扬威", py: "yào wǔ yáng wēi" },
            { zh: "胸膛", py: "xiōng táng" },
          ],
          compounds: [{ a: "耀", b: "曜", hint: "耀武 / 日曜" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "周恩来为什么立下「为中华之崛起而读书」的志向？",
            sample: "在租界看到中国人受欺凌，立志振兴中华。",
          },
        },
        {
          id: "u7l23",
          bookNo: 23,
          title: "梅兰芳蓄须",
          kind: "略读",
          words: [
            { zh: "蓄须", py: "xù xū" },
            { zh: "迫害", py: "pò hài" },
            { zh: "拒绝", py: "jù jué" },
          ],
          compounds: [{ a: "蓄", b: "畜", hint: "蓄须 / 牲畜" }],
          polyphones: [{ word: "畜", opts: ["xù", "chù"], ok: "xù" }],
          recite: null,
          meaning: {
            prompt: "梅兰芳为什么蓄须？表现了什么？",
            sample: "不愿为侵略者演出；爱国气节。",
          },
        },
        {
          id: "u7l24",
          bookNo: 24,
          title: "延安，我把你追寻",
          kind: "略读",
          words: [
            { zh: "崭新", py: "zhǎn xīn" },
            { zh: "火炕", py: "huǒ kàng" },
            { zh: "照耀", py: "zhào yào" },
          ],
          compounds: [],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "「追寻延安」追寻的是什么？",
            sample: "延安精神：艰苦奋斗、无私奉献等，不是追寻旧物本身。",
          },
        },
      ],
      garden: {
        id: "u7g",
        title: "语文园地七",
        accumulate: {
          title: "日积月累 ·《别董大》",
          author: "唐 · 高适",
          lines: [
            "千里黄云白日曛，",
            "北风吹雁雪纷纷。",
            "莫愁前路无知己，",
            "天下谁人不识君？",
          ],
          linesDetail: [
            { text: "千里黄云白日曛，", tip: "千里黄云弥漫，连太阳也变得昏暗。（曛＝昏暗）" },
            { text: "北风吹雁雪纷纷。", tip: "北风吹着大雁，雪花纷纷扬扬。" },
            { text: "莫愁前路无知己，", tip: "不要担心前面的路上没有知心朋友。" },
            { text: "天下谁人不识君？", tip: "天下有谁不认识您呢？（鼓励、赞扬友人）" },
          ],
          meaning:
            "黄云千里、日色昏暗，北风吹雁、大雪纷飞；不要担心前途没有知己，天下谁人不认识您呢？后两句是劝慰与鼓励。",
          background:
            "高适，唐代边塞诗人。董大即董庭兰，著名琴师。须会背、会默、懂每句意思。注意「曛」字。",
        },
      },
    },
    {
      id: "u8",
      name: "第八单元 · 历史传说故事",
      lessons: [
        {
          id: "u8l25",
          bookNo: 25,
          title: "王戎不取道旁李",
          kind: "精读",
          words: [
            { zh: "道路", py: "dào lù" },
            { zh: "李子", py: "lǐ zi" },
            { zh: "缘故", py: "yuán gù" },
          ],
          compounds: [{ a: "缘", b: "绿", hint: "缘故 / 绿色" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "王戎为什么不取道旁李？说明他怎样？",
            sample: "路边李子若好吃早被人摘光；善于观察、推理。",
          },
        },
        {
          id: "u8l26",
          bookNo: 26,
          title: "西门豹治邺",
          kind: "精读",
          words: [
            { zh: "巫婆", py: "wū pó" },
            { zh: "渠道", py: "qú dào" },
            { zh: "开凿", py: "kāi záo" },
          ],
          compounds: [{ a: "凿", b: "槽", hint: "开凿 / 水槽" }],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "西门豹怎样破除迷信？还做了什么？",
            sample: "将巫婆等投入河中揭穿骗局；开凿渠道治理水患。",
          },
        },
        {
          id: "u8l27",
          bookNo: 27,
          title: "故事二则",
          kind: "略读",
          words: [
            { zh: "拜见", py: "bài jiàn" },
            { zh: "理睬", py: "lǐ cǎi" },
            { zh: "聚精会神", py: "jù jīng huì shén" },
          ],
          compounds: [],
          polyphones: [],
          recite: null,
          meaning: {
            prompt: "《扁鹊治病》《纪昌学射》各说明什么？",
            sample: "防微杜渐、及时治病；要练好基本功、持之以恒。",
          },
        },
      ],
      garden: {
        id: "u8g",
        title: "语文园地八",
        accumulate: {
          title: "日积月累 · 描写外貌的词语",
          items: [
            { text: "眉清目秀", who: "词语", tip: "形容相貌清秀俊美。" },
            { text: "亭亭玉立", who: "词语", tip: "形容女子身材修长美丽，也可形容花木。 " },
            { text: "明眸皓齿", who: "词语", tip: "明亮的眼睛、洁白的牙齿；形容容貌美丽。" },
            { text: "文质彬彬", who: "词语", tip: "既文雅又朴实，形容人举止斯文、有修养。" },
            { text: "相貌堂堂", who: "词语", tip: "形容人仪表端正、气宇不凡。" },
            { text: "威风凛凛", who: "词语", tip: "形容气势威严，令人敬畏。" },
            { text: "膀大腰圆", who: "词语", tip: "形容人身体粗壮结实。" },
            { text: "短小精悍", who: "词语", tip: "身材矮小却精明强干；也可指文章短而有力。" },
            { text: "容光焕发", who: "词语", tip: "脸上有光彩，精神饱满。" },
            { text: "鹤发童颜", who: "词语", tip: "白发却脸色红润，形容老年人气色好、有精神。" },
            { text: "慈眉善目", who: "词语", tip: "形容仁慈和善的样子。" },
            { text: "老态龙钟", who: "词语", tip: "形容年老体衰、行动不便。" },
          ],
          background:
            "十二个词语，多写人的外貌或神态。须会读、会写、懂意思，并能用来描写人物。",
        },
      },
    },
  ],
};
