with open('build.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 替换第 190 行左右
for i in range(170, 205):
    if 'categories/latam.html' in lines[i]:
        lines[i] = """        { label: isZh ? `🇯🇵 日韩精工板块 (10款)` : `🇯🇵 Japan & Korea (10)`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (2款)` : `🇦🇪 Middle East GCC (2)`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' }
"""
        break

# 替换第 1286 行左右
for i in range(1270, 1310):
    if 'categories/latam.html' in lines[i]:
        lines[i] = """          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html'}">🇯🇵 ${isZh ? '日韩精工 (10款)' : 'Japan & Korea (10)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html'}">🇦🇪 ${isZh ? '中东海湾 (2款)' : 'Middle East GCC (2)'}</a>
"""
        break

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Exact lines replaced successfully!")
