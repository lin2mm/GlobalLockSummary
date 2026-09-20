# -*- coding: utf-8 -*-

rule_48 = """
| **48** | 超长锁族详情页「工业子类别快速锚点网格」与动态大纲双向索引 | 1. **根治超长子页面翻滚疲劳**：以包含 20 款锁型的 `euro-cylinder-mortise.html` 为典型，样本层级全面按工业构型聚类（如 `双面槽型锁芯 (Double Cylinder)`、`内侧旋转手扭 (Thumbturn)`、`插芯锁体 (Mortise Case)`、`特种防盗异形锁 (Specialty)`）；<br>2. **顶部工规微导栏（`.spec-cluster-bar`）**：在实物图谱区顶部置顶 ASSA ABLOY 冷灰工规快速分类导航条，展示微游标（`⌖`）、类别名称与对应实物款数微胶囊，1 键平滑滚动直达；<br>3. **右侧桌面端 TOC 与移动端大纲同步下钻**：将多类别 H3 语义化挂载进全局目录大纲系统，实现桌面侧栏与移动视口双向无缝寻址。 | `build.mjs`, `assets/css/site.css` |
"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

if "| **48** |" not in text:
    target = "| **47** | 全站 229 个子页面全量自动化层级与排版穿透审计 | 1. **全网 H1 唯一性断言**：通过扫描 `_site/` 下全部 229 个 HTML 页面，断言除首页纯门厅网格外，所有二级、三级子页面有且仅有唯一一个语义化 H1 主标题；<br>2. **零模板占位符残留断言**：断言全网静态产物中绝对不存在未渲染的 Mustache/模板标记；<br>3. **多端自动化构建绿灯**：持续保持 6 大测试套件 100% 满分通过并自动同步至远端。 | `tools/audit-all-subpages.py`, `tests/` |"
    if target in text:
        text = text.replace(target, target + "\n" + rule_48.strip())
        with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully appended rule 48 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 47.")
else:
    print("Rule 48 already present.")
