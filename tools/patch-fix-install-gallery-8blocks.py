with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 升级 install-gallery.html 顶部的区域快速穿透栏为 8 大工业板块（ASSA ABLOY 极简工业风格）
old_filter_bar = """      <div class="install-filter-bar" style="margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; background: #f1f5f9; padding: 10px 14px; border-radius: 8px;">
        <span style="font-weight: 700; font-size: 0.85rem; color: #334155; display: flex; align-items: center;">📍 ${isZh ? '区域快速穿透:' : 'Quick Navigation:'}</span>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美板块 (6款)' : 'North America (6)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国 (8款)' : 'Continental Europe (8)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳英板块 (10款)' : 'Australia & UK (10)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🇸🇬 ${isZh ? '东南亚/东亚 (10款)' : 'Southeast Asia (10)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html'}">🇯🇵 ${isZh ? '日韩精工 (10款)' : 'Japan & Korea (10)'}</a>
          <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html'}">🇦🇪 ${isZh ? '中东海湾 (2款)' : 'Middle East GCC (2)'}</a>
      </div>"""

new_filter_bar = """      <div class="install-filter-bar" style="margin-bottom: 24px; display: flex; gap: 8px; flex-wrap: wrap; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; padding: 10px 14px; border-radius: 4px;">
        <span style="font-weight: 700; font-size: 0.82rem; color: #0f172a; display: flex; align-items: center;">★ ${isZh ? '8大工业板块穿透:' : '8 Industrial Sectors:'}</span>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美板块' : 'Americas'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html'}">🌎 ${isZh ? '拉美新兴' : 'LatAm'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国' : 'Europe'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳英体系' : 'UK/ANZ'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html'}">🇦🇪 ${isZh ? '中东海湾' : 'GCC'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html'}">🇯🇵 ${isZh ? '日韩精工' : 'Japan/Korea'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🇸🇬 ${isZh ? '东南亚' : 'SEA'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/af-sa.html' : '/en/categories/af-sa.html'}">🇮🇳 ${isZh ? '南亚非洲' : 'South Asia/Africa'}</a>
      </div>"""

if old_filter_bar in code:
    code = code.replace(old_filter_bar, new_filter_bar)
    print("Updated install-gallery 8 sectors filter bar!")
else:
    print("old_filter_bar not found in build.mjs")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

