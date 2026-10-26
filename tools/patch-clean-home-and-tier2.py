with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 首页 Entry 彻底去除“浏览分类图谱 →”这一行无用动词
old_entry_action = """        <div class="gallery-portal-card__action" style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">
          <span>${isZh ? '浏览分类图谱' : 'Explore Category'} →</span>
        </div>"""

if old_entry_action in code:
    code = code.replace(old_entry_action, "")
    print("Removed action line from home entry cards!")

# 2. 第二层页面锁型卡片：彻底去除冗长 3 行 features 纯文本，升级为 3 个紧凑小胶囊徽章
old_desc_and_footer = """      <p class="gallery-card__desc" style="font-size: 0.82rem; color: #475569; line-height: 1.5; margin: 0 0 12px;">${escapeHtml(item.features || '')}</p>
      <div class="gallery-card__footer" style="padding-top: 10px; border-top: 1px solid #f1f5f9;">
        <a class="gallery-card__link" href="${familyHref}" style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-primary, #0f172a);">
          <span>${isZh ? '查看工程规格与安装案例' : 'Specifications & Cases'}</span>
          <span class="gallery-card__arrow">→</span>
        </a>
      </div>"""

new_tags_and_footer = """      <!-- 极简五金公差微标签替代冗长文字 -->
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0 10px;">
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⌖ ${escapeHtml(item.engineeringMatrix?.shearLineClearance ? item.engineeringMatrix.shearLineClearance.split('/')[0] : '标准背距')}</span>
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⎔ ${escapeHtml(item.engineeringMatrix?.doorThicknessMatrix?.typicalDoorThickness || '标配门厚')}</span>
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⚡ ${escapeHtml(item.engineeringMatrix?.gearboxSpec ? item.engineeringMatrix.gearboxSpec.split('；')[0] : '直驱减速')}</span>
      </div>
      <div class="gallery-card__footer" style="padding-top: 8px; border-top: 1px solid #f1f5f9; display: flex; justify-content: flex-end;">
        <a class="gallery-card__link" href="${familyHref}" style="font-size: 0.78rem; font-weight: 700; color: #0f172a; text-decoration: none;">
          <span>${isZh ? '拆解图谱' : 'Blueprint'} →</span>
        </a>
      </div>"""

if old_desc_and_footer in code:
    code = code.replace(old_desc_and_footer, new_tags_and_footer)
    print("Replaced verbose features prose with compact spec tags!")

# 3. 第三层锁型详情页工程卡片：去重高彩背景，升级为 ASSA ABLOY 浅色折叠面板
code = code.replace("background: #fdf4ff;", "background: #f8fafc;")
code = code.replace("border-left: 3px solid #c026d3;", "border-left: 3px solid #0f172a;")
code = code.replace("background: #fffbeb;", "background: #f8fafc;")
code = code.replace("border-left: 3px solid #d97706;", "border-left: 3px solid #475569;")
code = code.replace("background: #f0fdfa;", "background: #f8fafc;")
code = code.replace("border-left: 3px solid #0d9488;", "border-left: 3px solid #0f172a;")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build.mjs successfully!")

