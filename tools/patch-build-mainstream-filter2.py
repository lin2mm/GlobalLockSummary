with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '类实物样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>
        </div>"""

replacement = """        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '款实物样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>
          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 14px 0 0; flex-wrap: wrap; align-items: center;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #475569;">${isZh ? '🎯 市场分级直选:' : 'Market Filter:'}</span>
            <button class="tier-filter-btn is-active" data-filter="all" onclick="filterTier('all', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer;">
              ${isZh ? '全部样本' : 'All'} (${block.items.length})
            </button>
            <button class="tier-filter-btn" data-filter="Mainstream" onclick="filterTier('Mainstream', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #0284c7; cursor: pointer;">
              ★ ${isZh ? '主流基准锁' : 'Mainstream Standards'} (${block.items.filter(i => i.tierClass === 'Mainstream').length})
            </button>
            <button class="tier-filter-btn" data-filter="Niche" onclick="filterTier('Niche', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">
              🔍 ${isZh ? '小众/特殊锁' : 'Niche & Specialty'} (${block.items.filter(i => i.tierClass !== 'Mainstream').length})
            </button>
          </div>
        </div>"""

if target in text:
    text = text.replace(target, replacement)
    print("Injected filter buttons into category header successfully!")
else:
    print("Target block not found!")

# 保证 renderGalleryCard 的外层容器带有 data-tier-class 属性
old_card_start = 'return `<div class="gallery-card" data-gallery-card data-region="${escapeHtml(item.block)}"'
new_card_start = 'return `<div class="gallery-card" data-gallery-card data-tier="${escapeHtml(item.tierClass || "Mainstream")}" data-region="${escapeHtml(item.block)}"'

if old_card_start in text:
    text = text.replace(old_card_start, new_card_start)
    print("Injected data-tier attribute into gallery card!")

# 在分类页面底部增加前端即时切换脚本
script_target = "      const categoryPageHtml = `<div class=\"gallery-wall gallery-wall--category wrap\">"
script_inject = """      const filterScript = `
      <script>
        function filterTier(tier, btn) {
          const cards = document.querySelectorAll('.gallery-card[data-tier]');
          cards.forEach(c => {
            if (tier === 'all' || c.getAttribute('data-tier') === tier) {
              c.style.display = '';
            } else {
              c.style.display = 'none';
            }
          });
          const allBtns = document.querySelectorAll('.tier-filter-btn');
          allBtns.forEach(b => {
            b.style.background = '#ffffff';
            b.style.color = '#475569';
            b.style.borderColor = '#cbd5e1';
          });
          btn.style.background = '#0284c7';
          btn.style.color = '#ffffff';
          btn.style.borderColor = '#0284c7';
        }
      </script>`;
"""

if script_target in text:
    text = text.replace(script_target, script_inject + "\n" + script_target)
    # 在分类页面末尾闭合前加上 filterScript
    text = text.replace("      return emitPage({", "      // Injected filter script\n      return emitPage({")
    print("Injected client-side filter script!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied to build.mjs!")
