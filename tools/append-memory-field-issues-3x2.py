with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **41** | 避坑实录 3x2 黄金对称网格重构（彻底终结 4 行错落） | 1. **流式截断根因排查**：原先采用 `repeat(auto-fill, minmax(320px, 1fr))`，在标准笔记本视口（1080px 内容区）下，第 1 排挤入 3 张卡片，第 2 排放 1 张，第 3 排放 1 张，被浏览器强行折行拉伸为 4 行错落长条；<br>2. **固化为 3列 x 2行 黄金矩阵**：显式重载为 `grid-template-columns: repeat(3, 1fr)`，将 6 大核心典型工单工整收敛为 2 行，卡片图高调整为 140px，首屏 100% 完整露出；<br>3. **ASSA ABLOY 单色墨黑徽章**：刺眼大红大橙角标收敛为墨黑工单标牌 `[FL-01 · 致命卡阻]`，视觉秩序与空气感全面回归。 | `content/pages/zh/field-issues.md`, `content/pages/en/field-issues.md` |
""")

print("Appended batch 41 to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
