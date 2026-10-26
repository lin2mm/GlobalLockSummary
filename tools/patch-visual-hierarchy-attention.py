with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 在 galleryFragment 中为三大核心基准（北美 na、欧陆 europe5、英澳 uk-anz）配置 Tier 1 视觉强化
old_card_gen = """    return `<a class="gallery-portal-card" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">"""

new_card_gen = """    // 视觉注意力体系：Tier 1 核心基准高亮 vs 其它板块弱化
    const isCoreTier1 = ['na', 'europe5', 'uk-anz'].includes(b.code);
    const cardClass = isCoreTier1 ? 'gallery-portal-card gallery-portal-card--core' : 'gallery-portal-card gallery-portal-card--secondary';
    const tierBadge = isCoreTier1 ? (isZh ? '<span class="portal-tier-pill portal-tier-pill--core">★ 核心加装基准</span>' : '<span class="portal-tier-pill portal-tier-pill--core">★ CORE BASELINE</span>') : '';
    return `<a class="${cardClass}" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">
      ${tierBadge}"""

if old_card_gen in code:
    code = code.replace(old_card_gen, new_card_gen)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Patched build.mjs with visual attention hierarchy!")
else:
    print("old_card_gen not found!")

# 2. 追加 CSS 样式到 assets/css/site.css
css_rules = """
/* ==========================================================================
   Visual Attention & Optical Hierarchy System (注意力与色系层级体系)
   ========================================================================== */

/* Tier 1 Core Baselines: High Contrast, Vibrant & Focused */
.gallery-portal-card--core {
  border: 1.5px solid #2563eb !important;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12) !important;
  opacity: 1 !important;
  transform: scale(1.01);
}
.gallery-portal-card--core:hover {
  border-color: #1d4ed8 !important;
  box-shadow: 0 16px 32px rgba(37, 99, 235, 0.22) !important;
  transform: translateY(-6px) scale(1.02) !important;
}

/* Tier 2 Secondary Divisions: Subdued, De-emphasised, Muted Neutral Tone */
.gallery-portal-card--secondary {
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
  opacity: 0.88;
  background: #f8fafc !important;
}
.gallery-portal-card--secondary .gallery-portal-card__img {
  filter: grayscale(18%) contrast(95%);
  transition: filter .3s ease, transform .3s ease;
}
.gallery-portal-card--secondary:hover {
  opacity: 1;
  border-color: #94a3b8 !important;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08) !important;
  transform: translateY(-4px) !important;
}
.gallery-portal-card--secondary:hover .gallery-portal-card__img {
  filter: grayscale(0%) contrast(100%);
}

/* Core Baseline Floating Badge */
.portal-tier-pill {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  padding: 3px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18);
}
.portal-tier-pill--core {
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  color: #ffffff;
  border: 1px solid rgba(255,255,255,0.3);
}
"""

with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'Visual Attention & Optical Hierarchy System' not in css:
    css += css_rules
    with open('assets/css/site.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added attention hierarchy CSS rules!")

