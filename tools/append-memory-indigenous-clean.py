with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **37** | 工业索引页面图文失衡与深色黑块根治 | 1. **工业图例图片比例与背景重构**：将德奥瑞、法比区、日韩、英澳各体系右侧图片的深黑背景（`#0f172a`）彻底换装为 ASSA ABLOY 浅冷灰工程底（`#f8fafc`），消除死黑压迫感；<br>2. **图例溢出与挤压根治**：将 `object-fit: cover` 改为带有 6px 内边距的 `object-fit: contain`，彻底杜绝双向锁芯、水滴旋钮被裁切腰斩；<br>3. **推荐转接件框轻量化**：由厚重蓝色底块转为 ASSA ABLOY 墨黑极细微通告框，与左侧图纸保持完美比例平衡。 | `content/pages/zh/indigenous-guides.md`, `content/pages/en/indigenous-guides.md` |
""")

print("Appended batch 37 to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
