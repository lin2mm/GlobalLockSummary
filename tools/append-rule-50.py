# -*- coding: utf-8 -*-

rule_50 = """
| **50** | 画廊卡片信息极致降噪（单图+单标+双微标签）与多重重复按钮根治 | 1. **转接工具（adapters）文字极端减负 70%**：彻底拔除卡片内大段“关键公差与尺寸”、“推荐材质”、“3D打印适配”四行长文本，收敛为标准 ASSA ABLOY 工业结构：**140px 产品剖面图 + 极简标题 + 2 个微参数标签（`⌖ 关键公差` + `🔩 材质`）+ 底部单一直达链接**；<br>2. **避坑工单（field-issues）错位重复彻底根治**：根除了上轮脚本在卡片闭合处意外追加的双重文本与重复按钮（消除 `查看对应锁族图谱与公差 →` 双重错位重叠）；<br>3. **统一为 3 列黄金等高卡片流**：`adapters.html` 与 `field-issues.html` 全网统一采用 `grid-template-columns: repeat(3, 1fr)`，卡片高度完全齐平、内部留白透气，告别密集压迫感。 | `content/pages/zh/adapters.md`, `content/pages/en/adapters.md`, `content/pages/zh/field-issues.md`, `content/pages/en/field-issues.md` |
"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

if "| **50** |" not in text:
    target = "| **49** | 中英文混排标题「双行层次解耦」排版体系与右侧目录（TOC）全域下钻 | 1. **标题过长与单行挤压根治**：针对全站（包括 H1 主标、H2 专区、H3 模块）以及右侧 TOC 目录中所有带括号的中英文混合标题（如 `后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)`），建立自动化双行解耦引擎：**第 1 行中文主标题置顶醒目、第 2 行英文专业术语（`.bilingual-title__en`）新起一行作为精致冷灰副标**；<br>2. **眼睛一扫而过（F 型视线工规律）**：中文读者视线瞬间捕捉母语核心含义，专业外语工程术语紧随其后作为基准，告别标题拖沓折行与视觉疲劳；<br>3. **底层通用自动化编译**：在 `src/markdown.mjs`、`build.mjs` 与 `src/layout.mjs` 中全域注入，无缝覆盖 Markdown 标题、程序化 H1 与右侧目录树。 | `src/markdown.mjs`, `src/layout.mjs`, `assets/css/site.css`, `build.mjs` |"
    if target in text:
        text = text.replace(target, target + "\n" + rule_50.strip())
        with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully appended rule 50 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 49.")
else:
    print("Rule 50 already present.")
