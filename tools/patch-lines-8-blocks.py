with open('build.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 替换第 185 行到 192 行
new_sub_items = """      subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🌎 拉美新兴板块 (${latamCount}款)` : `🌎 Latin America (${latamCount})`, href: isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (2款)` : `🇦🇪 Middle East GCC (2)`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' },
        { label: isZh ? `🇯🇵 日韩精工板块 (10款)` : `🇯🇵 Japan & Korea (10)`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇸🇬 东南亚板块 (${seaCount}款)` : `🇸🇬 South East Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🇮🇳 非洲南亚板块 (2款)` : `🇮🇳 South Asia & Africa (2)`, href: isZh ? '/zh/categories/af-sa.html' : '/en/categories/af-sa.html' }
      ];
"""

start_i = 185
end_i = 192
for idx in range(180, 200):
    if "subItems = [" in lines[idx]:
        start_i = idx
    if "];" in lines[idx] and idx > start_i:
        end_i = idx
        break

lines = lines[:start_i] + [new_sub_items] + lines[end_i+1:]

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("build.mjs updated with 8-block navbar subItems!")
