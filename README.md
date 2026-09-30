# 语文书桌 / Chinese Desk

考前查漏补缺 · 可打印 Word / PDF。结构对齐翻翻英语（按课次 / 分场次），内容按语文学法来。

**状态：已上线（四上 · 第 1–3 单元）**  
**网址：[https://budotding1025.github.io/chinese-desk/](https://budotding1025.github.io/chinese-desk/)**  
本机：`python desk_server.py` → http://127.0.0.1:8732/

## 主色

橙红 `#E85D04` · 橙黄 `#F4A261` · 焦橙 `#C2410C`

## 怎么学（对齐翻翻英语的「场次」，换成语文）

| 场次 | 对应英语 | 语文做什么 | 材料 |
| --- | --- | --- | --- |
| **工作日① 默写过关** | 词听检测 | **本课**会写字/词语默写 + 形近组词；有背诵则加**课文片段默写** | `printables/weekday/dictation/` |
| **工作日② 考点练习** | 过关后的句型/听力练 | 默写过关后：多音·字义·园地·仿写·短阅读（题型难度对齐单元测 JPG） | `printables/weekday/practice/` |
| **周末** | 周末综合 | 作文仿写 + 教委课外阅读理解 | `printables/weekend/` |
| **测前摸底** | — | 单元整卷 | `printables/full/` |

**顺序硬规则：** 先①默写过关 → 再②考点练习。默写不过关不刷整套考点型。

单课默写约 8–12 分钟；考点练习约 8–15 分钟。卷面 **A4**，参照上传单元测 JPG：**少留空、填空行要够大**。

## 错题档案

做错 → `printables/weekday/错题登记表` → `mistakes/错题档案.md`  
**考试前**只复习相关单元未掌握错题。

## 推荐日程（可自选）

见 [`schedule.md`](schedule.md)。学校进度不同可整体平移。

## 目录

```
printables/
  weekday/dictation/   ← 每课默写过关
  weekday/practice/    ← 单元考点练习（过关后）
  weekend/             ← 周末
  full/                ← 大测摸底
scripts/curriculum.py  ← 课次·会写字·背诵·园地数据（对齐教材）
```

## 已知

- U3 整卷扫描仍不完整  
- 略读课默写以积累词为主  
- 教材全文 PDF 仅本机，不进公开仓  
