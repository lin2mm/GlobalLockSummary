with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **30** | ASSA ABLOY 官方设计语言（Deep Blue）全栈收敛与两处截图缺陷根治 | 1. **品牌与 Favicon 色彩统一**：彻底将 Favicon 与 Header SVG 锁标统一定义为 ASSA ABLOY 官方核心标色 **`#0B1D47` (Deep Blue)**，全站 CSS `--accent` 变量同步升级为 `#0B1D47`；<br>2. **导航激活态精密线化**：导航当前页激活状态由大面积浅灰底色改为极简 **2px 墨黑下划线（`border-bottom: 2px solid #0B1D47`）**；<br>3. **图1（工程实录）缺陷根治**：彻底拔除实操案例卡片底部粗大高亮天蓝色按钮，换装为 ASSA ABLOY 墨黑极简工业按钮；工程关键指标彩色小图标收敛为精准游标符号 `[⌖ 关键指标]` 与墨黑细线；<br>4. **图2（转接五金）缺陷根治**：彻底消除卡片顶部双重徽章遮挡（将 ADP 编号与 Verified 合并为单行半透明墨黑胶囊），消除浅蓝色粗边框，解决卡片底部多层核实文本截断与换行重叠问题。 | `assets/img/favicon.svg`, `assets/css/site.css`, `build.mjs`, `content/pages/` |
""")

print("Appended batch 30 to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
