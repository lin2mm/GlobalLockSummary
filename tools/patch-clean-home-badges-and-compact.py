with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 首页 Entry 卡片：去除图片右上角悬浮的款数角标，将款数下沉到标题旁，图片只留极简 ★ 核心加装基准
old_portal_card = """    return `<a class="${cardClass}" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">
      ${tierBadge}
      <div class="gallery-portal-card__media" style="position: relative; overflow: hidden; background: #0b1120;">
        <img class="gallery-portal-card__img" src="${escapeHtml(b.hero.image)}" alt="${escapeHtml(b.title)}" loading="lazy" width="360" height="230" />
        <span class="gallery-portal-card__badge" style="font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase;">${b.items.length} ${isZh ? '款实物样本' : 'MODELS'}</span>
        <span class="gallery-portal-card__keyhint" title="${isZh ? '按数字键直达' : 'Press key'}">[${idxBadge}]</span>
      </div>
      <div class="gallery-portal-card__body">
        <h2 class="gallery-portal-card__name">${escapeHtml(b.title)}</h2>
        <div class="gallery-portal-card__baseline" style="color: var(--color-primary, #0f172a); font-weight: 500; font-size: 0.88rem;">${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, ''))}</div>

      </div>
    </a>`;"""

new_portal_card = """    return `<a class="${cardClass}" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">
      ${tierBadge}
      <div class="gallery-portal-card__media" style="position: relative; overflow: hidden; background: #0b1120;">
        <img class="gallery-portal-card__img" src="${escapeHtml(b.hero.image)}" alt="${escapeHtml(b.title)}" loading="lazy" width="360" height="230" />
        <span class="gallery-portal-card__keyhint" title="${isZh ? '按数字键直达' : 'Press key'}">[${idxBadge}]</span>
      </div>
      <div class="gallery-portal-card__body">
        <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px; margin-bottom: 4px;">
          <h2 class="gallery-portal-card__name" style="margin: 0; flex: 1;">${escapeHtml(b.title)}</h2>
          <span style="font-size: 0.72rem; color: #64748b; font-weight: 600; white-space: nowrap; background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">${b.items.length} ${isZh ? '款' : 'models'}</span>
        </div>
        <div class="gallery-portal-card__baseline" style="color: var(--color-primary, #0f172a); font-weight: 500; font-size: 0.85rem;">${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, ''))}</div>
      </div>
    </a>`;"""

if old_portal_card in code:
    code = code.replace(old_portal_card, new_portal_card)
    print("Updated home portal cards: moved count badge into title row, freed image space!")
else:
    print("old_portal_card not found in build.mjs")

# 2. 压缩 install-gallery.html 的卡片高度，防止截断
old_cases_card = """      return `<div class="install-case-card" style="background: var(--color-surface, #fff); border: 1px solid var(--color-border, #cbd5e1); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
        <div style="position: relative; height: 220px; background: #000; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 8px; left: 8px; background: rgba(15,23,42,0.85); color: #38bdf8; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">
            ${escapeHtml(c.id)} · ${escapeHtml(c.sceneType)}
          </span>
          <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #fff; font-size: 0.7rem; padding: 2px 6px; border-radius: 3px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 16px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b; margin-bottom: 6px;">
            <span>${isZh ? '所属锁族:' : 'Family:'} <a href="${lockLink}" style="font-weight: 700; color: #0B1D47;">${escapeHtml(c.lockFamilyName)}</a></span>
            <span><a href="${catLink}" style="color: #64748b;">${escapeHtml(cRegion)} ${isZh ? '图库' : 'Gallery'} →</a></span>
          </div>
          <h3 style="margin: 0 0 8px; font-size: 1.05rem; line-height: 1.4;">${escapeHtml(cTitle)}</h3>
          <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 12px; flex: 1;">${escapeHtml(cDesc)}</p>
          <div style="background: #f8fafc; border-left: 3px solid #0f172a; padding: 6px 10px; font-size: 0.78rem; color: #334155; margin-bottom: 12px;">
            <b>${isZh ? '⌖ 关键指标:' : 'Key Metrics:'}</b> ${escapeHtml(c.keyMetrics)}
          </div>
          <div style="display: flex; gap: 8px;">
            <a style="flex: 1; text-align: center; font-size: 0.8rem; font-weight: 600; padding: 7px 12px; background: #0f172a; color: #ffffff; border: 1px solid #0f172a; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px;" href="${lockLink}">
              ${isZh ? '所属锁型详情 →' : 'Lock Details →'}
            </a>
            <a style="background: #f8fafc; border: 1px solid #cbd5e1; color: #334155; font-size: 0.8rem; font-weight: 600; padding: 7px 12px; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              ${isZh ? '分类图谱' : 'Gallery'}
            </a>
          </div>
        </div>
      </div>`;"""

new_cases_card = """      return `<div class="install-case-card" style="background: var(--color-surface, #fff); border: 1px solid var(--color-border, #cbd5e1); border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
        <div style="position: relative; height: 170px; background: #000; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #ffffff; font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: 3px;">
            ${escapeHtml(c.id)} · ${escapeHtml(c.sceneType)}
          </span>
          <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.8); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 12px 14px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; margin-bottom: 4px;">
            <span>${isZh ? '所属锁族:' : 'Family:'} <a href="${lockLink}" style="font-weight: 600; color: #0B1D47;">${escapeHtml(c.lockFamilyName)}</a></span>
            <span><a href="${catLink}" style="color: #64748b;">${escapeHtml(cRegion)} ${isZh ? '图谱' : 'Gallery'} →</a></span>
          </div>
          <h3 style="margin: 0 0 6px; font-size: 0.96rem; line-height: 1.35; font-weight: 700;">${escapeHtml(cTitle)}</h3>
          <p style="font-size: 0.8rem; color: #475569; line-height: 1.45; margin: 0 0 8px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${escapeHtml(cDesc)}</p>
          <div style="background: #f8fafc; border-left: 2.5px solid #0f172a; padding: 4px 8px; font-size: 0.74rem; color: #334155; margin-bottom: 8px;">
            <b>${isZh ? '⌖ 关键指标:' : 'Key Metrics:'}</b> ${escapeHtml(c.keyMetrics)}
          </div>
          <div style="display: flex; gap: 6px;">
            <a style="flex: 1; text-align: center; font-size: 0.76rem; font-weight: 600; padding: 6px 10px; background: #0f172a; color: #ffffff; border: 1px solid #0f172a; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${lockLink}">
              ${isZh ? '所属锁型详情 →' : 'Lock Details →'}
            </a>
            <a style="background: #f8fafc; border: 1px solid #cbd5e1; color: #334155; font-size: 0.76rem; font-weight: 600; padding: 6px 10px; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              ${isZh ? '分类图谱' : 'Gallery'}
            </a>
          </div>
        </div>
      </div>`;"""

if old_cases_card in code:
    code = code.replace(old_cases_card, new_cases_card)
    print("Compacted install-gallery cards to prevent viewport cutoffs!")
else:
    print("old_cases_card not found in build.mjs")

# 3. 压缩 install-gallery.html 顶部的空隙
code = code.replace('<div style="margin-bottom: 24px;">\n        <h1 style="margin: 0 0 8px;">',
                    '<div style="margin-bottom: 14px;">\n        <h1 style="margin: 0 0 6px; font-size: 1.6rem;">')
code = code.replace('<div class="install-filter-bar" style="margin-bottom: 24px;',
                    '<div class="install-filter-bar" style="margin-bottom: 16px;')

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

