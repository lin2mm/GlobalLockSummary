with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 更新 rewriteNav 下拉中的板块统计
old_nav_blocks = """      let naCount = 14;
      let euCount = 20;
      let ocCount = 16;
      let seaCount = 16;
      let latamCount = 4;
      try {
        const items = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'gallery.json'), 'utf8'));
        naCount = items.filter(i => i.block === 'na').length;
        euCount = items.filter(i => i.block === 'europe5').length;
        ocCount = items.filter(i => i.block === 'uk-anz').length;
        seaCount = items.filter(i => i.block === 'sea').length;
        latamCount = items.filter(i => i.block === 'latam').length;
      } catch (e) {}

      const subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🌏 亚太日韩板块 (${seaCount}款)` : `🌏 Asia-Pacific (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🌎 拉美工业板块 (${latamCount}款)` : `🌎 Latin America (${latamCount})`, href: isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html' }
      ];"""

new_nav_blocks = """      let naCount = 14;
      let euCount = 20;
      let ocCount = 16;
      let jpCount = 10;
      let seaCount = 10;
      let gccCount = 2;
      try {
        const items = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'gallery.json'), 'utf8'));
        naCount = items.filter(i => i.block === 'na').length;
        euCount = items.filter(i => i.block === 'europe5').length;
        ocCount = items.filter(i => i.block === 'uk-anz').length;
        jpCount = items.filter(i => i.block === 'jp-kr').length;
        seaCount = items.filter(i => i.block === 'sea').length;
        gccCount = items.filter(i => i.block === 'gcc').length;
      } catch (e) {}

      const subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇯🇵 日韩精工板块 (${jpCount}款)` : `🇯🇵 Japan & Korea (${jpCount})`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇸🇬 东南亚板块 (${seaCount}款)` : `🇸🇬 South East Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (${gccCount}款)` : `🇦🇪 Middle East GCC (${gccCount})`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' }
      ];"""

if old_nav_blocks in text:
    text = text.replace(old_nav_blocks, new_nav_blocks)
    print("Replaced old_nav_blocks with 6 blocks!")
else:
    print("old_nav_blocks not found directly")

# 2. 替换分类页顶部的过滤 chips
old_filter_chips = """          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美标准 (14款)' : 'North America (14)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国 (20款)' : 'Continental Europe (20)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳洲英国 (16款)' : 'Australia & UK (16)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🌏 ${isZh ? '亚太日韩 (16款)' : 'Asia-Pacific (16)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html'}">🌎 ${isZh ? '拉美新兴 (4款)' : 'Latin America (4)'}</a>"""

new_filter_chips = """          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美标准 (14款)' : 'North America (14)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国 (20款)' : 'Continental Europe (20)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳洲英国 (16款)' : 'Australia & UK (16)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html'}">🇯🇵 ${isZh ? '日韩精工 (10款)' : 'Japan & Korea (10)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🇸🇬 ${isZh ? '东南亚 (10款)' : 'South East Asia (10)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html'}">🇦🇪 ${isZh ? '中东海湾 (2款)' : 'Middle East GCC (2)'}</a>"""

if old_filter_chips in text:
    text = text.replace(old_filter_chips, new_filter_chips)
    print("Replaced old_filter_chips with 6 blocks!")
else:
    print("old_filter_chips not found directly")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

