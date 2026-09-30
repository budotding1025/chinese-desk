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
          meaning: "空山里看不见人，只听见人说话的声音；夕阳余光照进深林，又照在青苔上。",
          background: "王维，唐代诗人、画家，诗中有画。此诗写空山人语与返照青苔，意境清幽。",
        },
        extra: "单元测常考《赠刘景文》（宋·苏轼）：一年好景君须记，最是橙黄橘绿时。",
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
            { text: "人非生而知之者，孰能无惑？", who: "韩愈", tip: "人不是生下来就什么都懂，谁能没有疑惑？" },
            { text: "智能之士，不学不成，不问不知。", who: "王充", tip: "再聪明也要学、要问。" },
            { text: "博学之，审问之，慎思之，明辨之，笃行之。", who: "《中庸》", tip: "广泛学、详细问、谨慎想、明白辨、切实做。" },
            { text: "善疑者，不疑人之所疑，而疑人之所不疑。", who: "方以智", tip: "会提问的人，能想到别人想不到的问题。" },
          ],
          background: "本单元学习“提问”。韩愈、王充、方以智等强调疑惑与学问的关系；《中庸》五句是学习的完整步骤。",
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
          title: "日积月累 · 秋雨俗语等",
          items: [
            { text: "一场秋雨一场寒，十场秋雨穿上棉。", who: "俗语", tip: "秋雨过后天气渐冷。" },
            { text: "横看成岭侧成峰，远近高低各不同。", who: "苏轼", tip: "观察角度不同，看到的样子也不同。" },
          ],
          background: "本单元重“观察”。写植物小动物要具体：外形、变化、动作；可用比喻。",
        },
      },
    },
  ],
};
