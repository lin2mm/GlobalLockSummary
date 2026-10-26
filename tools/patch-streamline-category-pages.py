with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 彻底删除绿色的“出海研发选型导读”大段文字框
old_green_banner = """          <!-- 顶部一句话直观说明主流几款、小众几款及其研发指导 -->
          <div class="mainstream-summary-banner" style="margin-top: 14px; padding: 10px 14px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; font-size: 0.85rem; color: #166534; line-height: 1.5;">
            <b>💡 ${isZh ? '出海研发选型导读' : 'Market Breakdown'}:</b> 
            ${isZh 
              ? `本板块共收录 <b>${block.items.length}</b> 款门锁样本，其中 <b>★ 主流基准锁占 ${block.items.filter(i => i.tierClass === 'Mainstream').length} 款</b>（深蓝高亮·覆盖当地 ≥80% 存量），<b>🔍 小众/特殊结构占 ${block.items.filter(i => i.tierClass !== 'Mainstream').length} 款</b>（浅灰淡色·特殊老房与长尾）。大货开模与现货配件优先保障主流锁型。`
              : `This division catalogs <b>${block.items.length}</b> lock models: <b>★ ${block.items.filter(i => i.tierClass === 'Mainstream').length} Mainstream Baselines</b> (bold blue outline, covering ≥80% market share) and <b>🔍 ${block.items.filter(i => i.tierClass !== 'Mainstream').length} Niche / Specialty Models</b> (muted tone, vintage & long-tail). Standardize tooling on mainstream locks.`
            }
          </div>"""

if old_green_banner in code:
    code = code.replace(old_green_banner, "")
    print("Removed green banner from category pages!")
else:
    print("old_green_banner not found, trying regex...")
    import re
    code = re.sub(r'<!-- 顶部一句话直观说明主流几款.*?</div>\s*</div>\n\s*<div class="gallery-tier-filter"', '<div class="gallery-tier-filter"', code, flags=re.DOTALL)

# 2. 简化筛选条样式，采用 ASSA ABLOY 极简黑白灰单色
old_tier_filter = """          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 12px 0 0; flex-wrap: wrap; align-items: center;">
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
          </div>"""

new_tier_filter = """          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 14px 0 0; flex-wrap: wrap; align-items: center;">
            <button class="tier-filter-btn is-active" data-filter="all" onclick="filterTier('all', this)" style="font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 4px; border: 1px solid #0f172a; background: #0f172a; color: #ffffff; cursor: pointer;">
              ${isZh ? '全部' : 'All'} (${block.items.length})
            </button>
            <button class="tier-filter-btn" data-filter="Mainstream" onclick="filterTier('Mainstream', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer;">
              ★ ${isZh ? '主流基准' : 'Mainstream'} (${block.items.filter(i => i.tierClass === 'Mainstream').length})
            </button>
            <button class="tier-filter-btn" data-filter="Niche" onclick="filterTier('Niche', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">
              ${isZh ? '小众/衍生' : 'Niche'} (${block.items.filter(i => i.tierClass !== 'Mainstream').length})
            </button>
          </div>"""

if old_tier_filter in code:
    code = code.replace(old_tier_filter, new_tier_filter)
    print("Simplified tier filter bar!")

# 3. 简化 Hero 基准大卡片：去除“极强相关·改装第一基准”的黄色星星药丸，换成 ASSA ABLOY 极简黑标；去除蓝色大按钮文本，只留纯粹指引
old_hero_tag = '<span class="block-hero__tag">${escapeHtml(block.hero.tag)}</span>'
new_hero_tag = '<span style="display: inline-block; font-size: 0.7rem; font-weight: 700; background: #0f172a; color: #fff; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; margin-bottom: 8px;">★ ${isZh ? "核心基准锁型" : "Core Baseline"}</span>'

if old_hero_tag in code:
    code = code.replace(old_hero_tag, new_hero_tag)

old_hero_btns = """          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" href="${heroHref}">${isZh ? '进入该基准锁实物拆解与工程规范 →' : 'Enter Core Baseline Specs & Photos →'}</a>
            <a class="block-hero__btn" style="background: transparent; border: 1px solid var(--color-border, #cbd5e1); color: var(--color-text, #1e293b);" href="${isZh ? '/zh/drilling-templates.html' : '/en/drilling-templates.html'}">
              📐 ${isZh ? '获取 1:1 开孔打样工程模板' : '1:1 Drilling Templates'}
            </a>
          </div>"""

new_hero_btns = """          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" style="background: #0f172a; color: #fff; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${heroHref}">
              ${isZh ? '实物拆解与工程规范 →' : 'Specifications & Blueprint →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${isZh ? '/zh/drilling-templates.html' : '/en/drilling-templates.html'}">
              📐 ${isZh ? '1:1 开孔图谱' : '1:1 Template'}
            </a>
          </div>"""

if old_hero_btns in code:
    code = code.replace(old_hero_btns, new_hero_btns)
    print("Streamlined hero actions to clean minimalist buttons!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build.mjs with category page streamlining!")

