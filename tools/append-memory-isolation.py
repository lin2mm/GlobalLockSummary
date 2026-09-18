with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **14** | 内外部资产绝对物理隔离红线 | 严禁在面向访客的前端网站挂载内部开发文档下载链接；所有内部研发沉淀（docs/ 及 .xlsx）仅保留在 Git 仓库内部目录，与 _site/ 彻底隔离 | `docs/`, `build.mjs`, `content/pages/` |
| **15** | 后装智能锁专利规避导航正式更名 | 导航菜单明确为「后装专利规避 (Retrofit FTO)」 | `content/site.json` |
""")

print("Appended batch 14-15 to memory!")
