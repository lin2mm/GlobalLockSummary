# -*- coding: utf-8 -*-

rule_43_and_44 = """
| **43** | 全球 8 大工业板块首页卡片三行解耦与视觉对称绝对齐平 | 1. **标题三行层次解耦**：彻底拔除单行中英混排与换行挤压，重构为：**第 1 行中文大标题 (1.05rem / 800) + 第 2 行英文代号标准副标 (0.74rem / 600) + 第 3 行虚线基准锁型**；<br>2. **卡片绝对高度对齐**：8 张卡片在 4×2 黄金对称阵列下消除任何错落跳行，无论中英文版均保持严格垂直基线对齐；<br>3. **ASSA ABLOY 工业克制**：悬停阴影与微动效严格遵循工业制图克制规范，杜绝花哨动效。 | `build.mjs`, `assets/css/site.css` |

| **44** | 全站文字排版系统性重构与信息降噪（ASSA ABLOY 工规体系） | 1. **拒绝长篇叙事与文本堆砌**：全面遵循“关键词优先、结构化参数优先、图表优先”的工业设计信息传达准则；<br>2. **消除胶囊堆叠与密集导航条**：专题导航由杂乱自由浮动的胶囊长条重构为 **单行 5 列等宽微工规卡片网格（`.spec-topic-nav`）**，具备清晰数字编号（如 `01 / CLAMPING`）与极简中英标题；<br>3. **专利规避（Patent FTO）工规化改造**：淘汰彩色描边卡片，统一度量衡为 ASSA ABLOY 浅冷灰框体 + 墨黑标题 + 红绿高对比度参数对比盒（`⚡ 侵权红线特征` vs `🛡️ 规避工程路径`），并引入 5 步核验标准对比表。 | `content/pages/`, `assets/css/site.css` |
"""

with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到规则 41 后面
if '| **43** |' not in content:
    target = '| **41** | 避坑实录 3x2 黄金对称网格重构（彻底终结 4 行错落） | 1. **流式截断根因排查**：原先采用 `repeat(auto-fill, minmax(320px, 1fr))`，在标准笔记本视口（1080px 内容区）下，第 1 排挤入 3 张卡片，第 2 排放 1 张，第 3 排放 1 张，被浏览器强行折行拉伸为 4 行错落长条；<br>2. **固化为 3列 x 2行 黄金矩阵**：显式重载为 `grid-template-columns: repeat(3, 1fr)`，将 6 大核心典型工单工整收敛为 2 行，卡片图高调整为 140px，首屏 100% 完整露出；<br>3. **ASSA ABLOY 单色墨黑徽章**：刺眼大红大橙角标收敛为墨黑工单标牌 `[FL-01 · 致命卡阻]`，视觉秩序与空气感全面回归。 | `content/pages/zh/field-issues.md`, `content/pages/en/field-issues.md` |'
    
    if target in content:
        new_content = content.replace(target, target + '\n' + rule_43_and_44.strip())
        with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully inserted rules 43 and 44 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 41 target string.")
else:
    print("Rules already present.")
