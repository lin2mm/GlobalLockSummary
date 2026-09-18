with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """      <div class="gallery-card__badges" style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span class="gallery-card__id" style="font-family: var(--font-mono, monospace); font-weight: 700; font-size: 0.72rem;">${escapeHtml(item.id)}</span>
        <span class="gallery-card__status ${statusClass}">${escapeHtml(statusText)}</span>
      </div>"""

replacement = """      <div class="gallery-card__badges" style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; align-items: center; pointer-events: none;">
        <div style="display: flex; gap: 4px; align-items: center;">
          <span class="gallery-card__id" style="font-family: var(--font-mono, monospace); font-weight: 700; font-size: 0.72rem;">${escapeHtml(item.id)}</span>
          ${item.tierClass === 'Mainstream' 
            ? `<span style="background: #0284c7; color: #ffffff; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 3px; letter-spacing: 0.02em;">★ ${isZh ? '主流基准' : 'MAINSTREAM'}</span>` 
            : `<span style="background: #475569; color: #f8fafc; font-size: 0.65rem; font-weight: 600; padding: 2px 5px; border-radius: 3px;">${isZh ? '小众/特殊' : 'NICHE'}</span>`}
        </div>
        <span class="gallery-card__status ${statusClass}">${escapeHtml(statusText)}</span>
      </div>"""

if target in text:
    text = text.replace(target, replacement)
    print("Replaced badge in renderGalleryCard!")
else:
    print("Target badge not found in build.mjs!")

# 在分类列表顶部加入主流锁 vs 小众锁筛选过滤器
cat_header_target = """      const categoryHtml = `<div class="gallery-block">
        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '类实物样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>
        </div>"""

cat_header_replacement = """      const mainstreamCount = block.items.filter(i => i.tierClass === 'Mainstream').length;
      const nicheCount = block.items.length - mainstreamCount;

      const categoryHtml = `<div class="gallery-block">
        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '类全球样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>

          <!-- 主流基准 vs 小众锁快速筛选工具条 -->
          <div class="gallery-tier-filter" style="display: flex; gap: 10px; margin: 16px 0 0; flex-wrap: wrap; align-items: center;">
            <span style="font-size: 0.8rem; font-weight: 600; color: #64748b;">${isZh ? '市场分级筛选:' : 'Market Filter:'}</span>
            <button class="tier-filter-btn is-active" data-tier-filter="all" style="font-size: 0.78rem; font-weight: 600; padding: 5px 12px; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: #fff; cursor: pointer;">
              ${isZh ? '全部样本' : 'All'} (${block.items.length})
            </button>
            <button class="tier-filter-btn" data-tier-filter="Mainstream" style="font-size: 0.78rem; font-weight: 600; padding: 5px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #0284c7; cursor: pointer;">
              ★ ${isZh ? '主流基准锁' : 'Mainstream Standards'} (${mainstreamCount})
            </button>
            <button class="tier-filter-btn" data-tier-filter="Niche" style="font-size: 0.78rem; font-weight: 600; padding: 5px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">
              🔍 ${isZh ? '小众/老旧/特殊锁' : 'Niche & Specialty'} (${nicheCount})
            </button>
          </div>
        </div>"""

if cat_header_target in text:
    text = text.replace(cat_header_target, cat_header_replacement)
    print("Injected Mainstream/Niche filter into category header!")
else:
    print("cat_header_target not found in build.mjs!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("build.mjs successfully updated with Mainstream vs Niche tags and filters!")
