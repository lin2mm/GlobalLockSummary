with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 替换 renderGalleryCard 的渲染逻辑：
# 主流锁与非主流锁的色块与淡度差异化显式强化
old_card_pattern = """  return `<div class="gallery-card" data-gallery-card data-tier="${escapeHtml(item.tierClass || "Mainstream")}" data-region="${escapeHtml(item.block)}" data-search-text="${escapeHtml(searchText)}">"""

new_card_pattern = """  const isMainstream = item.tierClass === 'Mainstream';
  const cardStyle = isMainstream 
    ? 'border: 1.5px solid #0284c7; background: #ffffff; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08); border-left: 4px solid #0284c7;' 
    : 'border: 1px solid #e2e8f0; background: #f8fafc; opacity: 0.88; border-left: 3px solid #94a3b8; filter: saturate(0.9);';

  return `<div class="gallery-card gallery-card--${isMainstream ? 'mainstream' : 'niche'}" data-gallery-card data-tier="${escapeHtml(item.tierClass || "Mainstream")}" data-region="${escapeHtml(item.block)}" data-search-text="${escapeHtml(searchText)}" style="${cardStyle} border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;">"""

if old_card_pattern in text:
    text = text.replace(old_card_pattern, new_card_pattern)
    print("Replaced card container with color hierarchy styles!")
else:
    print("old_card_pattern not found!")

# 增强卡片角标与背景色块
old_badge_part = """          ${item.tierClass === 'Mainstream' 
            ? `<span style="background: #0284c7; color: #ffffff; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 3px; letter-spacing: 0.02em;">★ ${isZh ? '主流基准' : 'MAINSTREAM'}</span>` 
            : `<span style="background: #475569; color: #f8fafc; font-size: 0.65rem; font-weight: 600; padding: 2px 5px; border-radius: 3px;">${isZh ? '小众/特殊' : 'NICHE'}</span>`}"""

new_badge_part = """          ${isMainstream 
            ? `<span style="background: #0284c7; color: #ffffff; font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 3px; letter-spacing: 0.03em; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">★ ${isZh ? '主流基准' : 'MAINSTREAM'}</span>` 
            : `<span style="background: #e2e8f0; color: #64748b; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 3px; border: 1px solid #cbd5e1;">${isZh ? '非主流/小众' : 'NICHE'}</span>`}"""

if old_badge_part in text:
    text = text.replace(old_badge_part, new_badge_part)
    print("Replaced badge styling!")
else:
    print("old_badge_part not found!")

# 在卡片标题旁加上高亮/淡色徽标
old_title_part = """      <h3 class="gallery-card__title" style="margin: 0 0 6px; font-size: 1.02rem; font-weight: 600; line-height: 1.4;">
        <a href="${familyHref}">${escapeHtml(title)}</a>
      </h3>"""

new_title_part = """      <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
        <h3 class="gallery-card__title" style="margin: 0; font-size: 1.02rem; font-weight: ${isMainstream ? '700' : '500'}; line-height: 1.4; color: ${isMainstream ? '#0f172a' : '#475569'};">
          <a href="${familyHref}" style="color: inherit; text-decoration: none;">${escapeHtml(title)}</a>
        </h3>
        <span style="font-size: 0.7rem; font-weight: 600; padding: 1px 5px; border-radius: 3px; white-space: nowrap; ${isMainstream ? 'background: #e0f2fe; color: #0369a1;' : 'background: #f1f5f9; color: #94a3b8;'}">
          ${escapeHtml(item.marketSharePercent || (isMainstream ? '≥25%' : '<10%'))}
        </span>
      </div>"""

if old_title_part in text:
    text = text.replace(old_title_part, new_title_part)
    print("Replaced title part with market percentage color indicator!")
else:
    print("old_title_part not found!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Color hierarchy patch applied to build.mjs!")
