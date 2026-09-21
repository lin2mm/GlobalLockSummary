# -*- coding: utf-8 -*-

rules_content = """
| **45** | 避坑实录与转接工具卡片 100% 图片+标题+按钮全域可点击穿透 | 1. **避坑实录（field-issues）深层穿透**：彻底终结卡片“只能看不能点”的断头路体验，FL-01 至 FL-06 全部实现**整张现场大图可点击 + 标题带超链接 + 底部微按钮 `[查看对应锁族图谱与公差 →]`** 瞬时直达对应标准锁族详情页；<br>2. **转接工具（adapters）双向点击穿透**：除卡片标题外，所有 12 款转接五金的工程图纸与剖面图片均包裹高优先级超链接，点击图片直接穿透至对应适配锁族；<br>3. **路径严格核实断言**：所有跳转路径均经本地 15 大标准锁族与 8 大板块真实静态产物核验，确保 0 死链。 | `content/pages/`, `build.mjs` |

| **46** | 锁型详情页 ASSA ABLOY 工规标题层级语义化治理（H1/H2/H3 铁律） | 1. **解决用户截图反映的 H1 与层级混乱**：用户截图反映的“实操工程规范与安装案例”原在样本容器内层使用了杂乱嵌套与 H4 破损，现全面收敛为标准化大纲层级：`H1 锁族总名 ➔ H2 实物安装与改造图谱 ➔ H3 样本标题 (含工规 ID 徽章与 R1/R0 状态) ➔ H4/H5 细分参数`；<br>2. **视觉降噪与呼吸感提升**：消除内衬黑条顶边重叠，统一度量衡为 ASSA ABLOY 浅冷灰工程边框与精密基线，杜绝粗大描边压迫感。 | `build.mjs`, `assets/css/site.css` |

| **47** | 全站 229 个子页面全量自动化层级与排版穿透审计 | 1. **全网 H1 唯一性断言**：通过扫描 `_site/` 下全部 229 个 HTML 页面，断言除首页纯门厅网格外，所有二级、三级子页面有且仅有唯一一个语义化 H1 主标题；<br>2. **零模板占位符残留断言**：断言全网静态产物中绝对不存在未渲染的 Mustache/模板标记；<br>3. **多端自动化构建绿灯**：持续保持 6 大测试套件 100% 满分通过并自动同步至远端。 | `tools/audit-all-subpages.py`, `tests/` |
"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

if "| **45** |" not in text:
    # 找到规则 44 的行
    target = "| **44** | 全站文字排版系统性重构与信息降噪（ASSA ABLOY 工规体系） | 1. **拒绝长篇叙事与文本堆砌**：全面遵循“关键词优先、结构化参数优先、图表优先”的工业设计信息传达准则；<br>2. **消除胶囊堆叠与密集导航条**：专题导航由杂乱自由浮动的胶囊长条重构为 **单行 5 列等宽微工规卡片网格（`.spec-topic-nav`）**，具备清晰数字编号（如 `01 / CLAMPING`）与极简中英标题；<br>3. **专利规避（Patent FTO）工规化改造**：淘汰彩色描边卡片，统一度量衡为 ASSA ABLOY 浅冷灰框体 + 墨黑标题 + 红绿高对比度参数对比盒（`⚡ 侵权红线特征` vs `🛡️ 规避工程路径`），并引入 5 步核验标准对比表。 | `content/pages/`, `assets/css/site.css` |"
    if target in text:
        text = text.replace(target, target + "\n" + rules_content.strip())
        with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully appended rules 45, 46, and 47 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 44.")
else:
    print("Rules 45-47 already present.")
