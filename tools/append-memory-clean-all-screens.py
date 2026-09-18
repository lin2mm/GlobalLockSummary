with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **29** | 全量页面 ASSA ABLOY 去噪与 8 大板块收敛 | 1. `install-gallery.html`：筛选栏由历史 6 板块全面收敛升级为 **8 大工业板块**，采用 ASSA ABLOY 墨黑冷灰风格微胶囊；<br>2. `patent-avoidance.html`：消除标题与 H1 的重复括号文字（消除 `(Patent FTO Guide) (Patent FTO Guide)` 重复尾缀）；<br>3. `indigenous-guides.html`：拔除顶部深蓝色高饱和度大横幅，替换为 ASSA ABLOY 极简工业细线折叠微通知框。 | `build.mjs`, `content/pages/` |
""")

print("Appended batch 29 to memory!")
