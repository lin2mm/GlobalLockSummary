# -*- coding: utf-8 -*-

rule_49 = """
| **49** | 中英文混排标题「双行层次解耦」排版体系与右侧目录（TOC）全域下钻 | 1. **标题过长与单行挤压根治**：针对全站（包括 H1 主标、H2 专区、H3 模块）以及右侧 TOC 目录中所有带括号的中英文混合标题（如 `后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)`），建立自动化双行解耦引擎：**第 1 行中文主标题置顶醒目、第 2 行英文专业术语（`.bilingual-title__en`）新起一行作为精致冷灰副标**；<br>2. **眼睛一扫而过（F 型视线工规律）**：中文读者视线瞬间捕捉母语核心含义，专业外语工程术语紧随其后作为基准，告别标题拖沓折行与视觉疲劳；<br>3. **底层通用自动化编译**：在 `src/markdown.mjs`、`build.mjs` 与 `src/layout.mjs` 中全域注入，无缝覆盖 Markdown 标题、程序化 H1 与右侧目录树。 | `src/markdown.mjs`, `src/layout.mjs`, `assets/css/site.css`, `build.mjs` |
"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

if "| **49** |" not in text:
    target = "| **48** | 超长锁族详情页「工业子类别快速锚点网格」与动态大纲双向索引 | 1. **根治超长子页面翻滚疲劳**：以包含 20 款锁型的 `euro-cylinder-mortise.html` 为典型，样本层级全面按工业构型聚类（如 `双面槽型锁芯 (Double Cylinder)`、`内侧旋转手扭 (Thumbturn)`、`插芯锁体 (Mortise Case)`、`特种防盗异形锁 (Specialty)`）；<br>2. **顶部工规微导栏（`.spec-cluster-bar`）**：在实物图谱区顶部置顶 ASSA ABLOY 冷灰工规快速分类导航条，展示微游标（`⌖`）、类别名称与对应实物款数微胶囊，1 键平滑滚动直达；<br>3. **右侧桌面端 TOC 与移动端大纲同步下钻**：将多类别 H3 语义化挂载进全局目录大纲系统，实现桌面侧栏与移动视口双向无缝寻址。 | `build.mjs`, `assets/css/site.css` |"
    if target in text:
        text = text.replace(target, target + "\n" + rule_49.strip())
        with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully appended rule 49 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 48.")
else:
    print("Rule 49 already present.")
