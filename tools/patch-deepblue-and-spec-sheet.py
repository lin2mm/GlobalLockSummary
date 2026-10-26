import re

# 1. 替换 build.mjs 中的剩余 #0284c7 为 #0B1D47 或墨黑细线
with open('build.mjs', 'r', encoding='utf-8') as f:
    bm = f.read()

# 替换分类页主流卡片的高光蓝色边框为 ASSA ABLOY 墨黑工业基准边框
bm = bm.replace("border: 1.5px solid #0284c7; background: #ffffff; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08); border-left: 4px solid #0284c7;",
                "border: 1px solid #cbd5e1; background: #ffffff; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04); border-left: 3px solid #0B1D47;")
bm = bm.replace("background: #0284c7;", "background: #0B1D47;")
bm = bm.replace("border-left: 4px solid #0284c7;", "border-left: 3px solid #0B1D47;")
bm = bm.replace("color: #0284c7;", "color: #0B1D47;")

# 增强卡片：引入 ASSA ABLOY 标准五金规格微参数表
# 检查 renderLockFamilyCard 或卡片渲染处
with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(bm)
print("Updated build.mjs colors to #0B1D47!")

# 2. 全站 content/pages 中的 #0284c7 替换为 #0B1D47，彩色边框转为工业冷灰墨黑
def replace_in_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);',
                  'border: 1px solid #e2e8f0; border-left: 4px solid #0B1D47; border-radius: 6px; padding: 20px; box-shadow: 0 2px 6px rgba(15,23,42,0.03);')
    c = c.replace('#0284c7', '#0B1D47')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

for p in [
    'content/pages/en/adapters.md', 'content/pages/zh/adapters.md',
    'content/pages/en/indigenous-guides.md', 'content/pages/zh/indigenous-guides.md',
    'content/pages/en/japan-engravings.md', 'content/pages/zh/japan-engravings.md',
    'content/pages/en/visitor-overview.md', 'content/pages/zh/visitor-overview.md'
]:
    replace_in_file(p)
print("Updated content pages!")

# 3. 优化 CSS site.css 中的链接颜色和高亮
with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace("color: #0284c7;", "color: #0B1D47;")
css = css.replace("border: 1.5px solid #0284c7 !important;", "border: 1px solid #0B1D47 !important;")
css = css.replace("border-left: 4px solid #0284c7 !important;", "border-left: 3px solid #0B1D47 !important;")
css = css.replace("color: #0284c7 !important;", "color: #0B1D47 !important;")

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated site.css!")

