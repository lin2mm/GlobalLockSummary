with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 替换 rewriteNav 下拉中的板块
old_nav = """      const subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇸🇬 东南亚东亚板块 (${seaCount}款)` : `🇸🇬 East & SE Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🇯🇵 日韩精工板块 (10款)` : `🇯🇵 Japan & Korea (10)`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (2款)` : `🇦🇪 Middle East GCC (2)`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' }
      ];"""

new_nav = """      let afCount = 2;
      try {
        const items = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'gallery.json'), 'utf8'));
        afCount = items.filter(i => i.block === 'af-sa').length;
      } catch (e) {}

      const subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🌎 拉美新兴板块 (${latamCount}款)` : `🌎 Latin America (${latamCount})`, href: isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (2款)` : `🇦🇪 Middle East GCC (2)`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' },
        { label: isZh ? `🇯🇵 日韩精工板块 (10款)` : `🇯🇵 Japan & Korea (10)`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇸🇬 东南亚板块 (${seaCount}款)` : `🇸🇬 South East Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🇮🇳 非洲南亚板块 (${afCount}款)` : `🇮🇳 South Asia & Africa (${afCount})`, href: isZh ? '/zh/categories/af-sa.html' : '/en/categories/af-sa.html' }
      ];"""

if old_nav in text:
    text = text.replace(old_nav, new_nav)
    print("Replaced rewriteNav with full 8 blocks!")
else:
    print("old_nav not matched directly")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

