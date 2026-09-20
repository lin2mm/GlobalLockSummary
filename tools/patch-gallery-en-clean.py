import re

with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 优化 8 大板块的定义：统一英文卡片标题与基准，杜绝冗长破折号折行
new_block_defs = """    {
      code: 'na',
      title: isZh ? '🇺🇸 北美标准板块 (Americas — ANSI / BHMA)' : '🇺🇸 North America (ANSI/BHMA)',
      shortTitle: isZh ? '北美标准板块' : 'North America',
      subtitle: isZh ? '全球存量最大的智能锁加装市场 · 标准 54mm 大孔位、单插销死锁 (Deadbolt) 与 60/70mm 标准背距' : 'World largest retrofit market · Standard 54mm bore, deadbolt & 60/70mm backset',
      hero: {
        title: isZh ? '核心改装基准：美标单缸插销死锁 (ANSI Deadbolt / Schlage B60)' : 'Core Retrofit Baseline: ANSI Deadbolt (Schlage B60)',
        desc: isZh ? 'August 与 SwitchBot 的全球基本盘。标准扁平尾轴（Tailpiece）直接啮合；改造核心难点在于门扇下沉与密封条导致插销与扣板卡阻。' : 'Core baseline for August & SwitchBot. Flat tailpiece interface; key challenge is sag binding.',
        image: '/assets/img/hero/hero-na-deadbolt.png',
        familyId: 'us-deadbolt',
        tag: isZh ? '⭐ 极强相关 · 改装第一基准' : '⭐ Core Retrofit Baseline'
      },
      items: items.filter(i => i.block === 'na')
    },
    {
      code: 'europe5',
      title: isZh ? '🇪🇺 欧陆五国板块 (Continental Europe — DIN / EN)' : '🇪🇺 Continental Europe (DIN/EN)',
      shortTitle: isZh ? '欧陆五国板块' : 'Continental Europe',
      subtitle: isZh ? '西欧与中欧成熟大容量市场 · 欧标槽型锁芯 (Euro Profile DIN 18252)、DIN 18251 插芯锁体与抬把手多点联动锁' : 'Mature European standard · Euro profile cylinders, DIN 18251 cases & multipoint systems',
      hero: {
        title: isZh ? '核心改装基准：欧标槽型双锁芯 (Euro Profile DIN 18252)' : 'Core Retrofit Baseline: Euro Profile Double-Cylinder (DIN 18252)',
        desc: isZh ? 'Nuki 与 Yale Linus 的全球基本盘。死穴在于内侧常插钥匙时，锁芯必须具备 DIN 18252 BS 双向应急离合认证，否则断电造成彻底反锁。' : 'Nuki & Linus core baseline. Critical: MUST feature DIN 18252 BS dual-action emergency clutch.',
        image: '/assets/img/hero/hero-europe-eurocylinder.jpg',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⭐ 极强相关 · 欧标第一基准' : '⭐ Core Euro Baseline'
      },
      items: items.filter(i => i.block === 'europe5')
    },
    {
      code: 'uk-anz',
      title: isZh ? '🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK — AS / BS)' : '🇦🇺🇬🇧 Australia & UK (AS/BS)',
      shortTitle: isZh ? '澳新英国板块' : 'Australia & UK',
      subtitle: isZh ? '高防盗高人工成本市场 · 澳洲 Lockwood 001 表面安装夜闩锁 (Rim Deadlatch)、大洋洲短进深锁体与英国 5 拨杆防盗插芯锁' : 'High-security & high-labor market · Lockwood 001 surface deadlatches, short-backset & BS 5-lever',
      hero: {
        title: isZh ? '核心改装基准：澳式表面安装双扣死锁 (Lockwood 001 Deadlatch)' : 'Core Retrofit Baseline: Lockwood 001 Rim Deadlatch',
        desc: isZh ? '澳洲独栋木门第一基准。特有水滴形大旋钮需专属 ADP-05 夹具；致命点在于辅舌必须完全压入方可死锁，门缝变异极易引发假锁死。' : 'AU wooden door benchmark. Teardrop turn requires ADP-05 adapter; auxiliary bolt must depress fully.',
        image: '/assets/img/hero/hero-anz-lockwood001.jpg',
        familyId: 'au-deadlatch',
        tag: isZh ? '⭐ 极强相关 · 澳新第一基准' : '⭐ Pacific Baseline'
      },
      items: items.filter(i => i.block === 'uk-anz')
    },
    {
      code: 'jp-kr',
      title: isZh ? '🇯🇵🇰🇷 日韩精工板块 (Japan & Korea — JIS / KS)' : '🇯🇵🇰🇷 Japan & Korea (JIS/KS)',
      shortTitle: isZh ? '日韩精工板块' : 'Japan & Korea',
      subtitle: isZh ? '极高精密装配工业体系 · 日本 MIWA / GOAL 超薄锁体、B5 防犯捏合旋钮与韩国无孔全自动锁' : 'Precision Asian standards · MIWA/GOAL slim mortise, B5 anti-theft thumbturn & Korean electronic push-pull',
      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/hero/hero-jp-miwa-door.jpg',
        familyId: 'jp-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },
      items: items.filter(i => i.block === 'jp-kr')
    },
    {
      code: 'sea',
      title: isZh ? '🇸🇬🇲🇾 东南亚板块 (ASEAN / SEA — SS / MS)' : '🇸🇬🇲🇾 South East Asia (ASEAN)',
      shortTitle: isZh ? '东南亚板块' : 'South East Asia',
      subtitle: isZh ? '东盟高密度热带五金体系 · 新加坡组屋 HDB 外铁闸与内木门极窄防撞空间、大马与泰国窄体铝门锁' : 'High-density tropical ASEAN systems · Singapore HDB gate clash, Malaysian & Thai narrow aluminum doors',
      hero: {
        title: isZh ? '核心改装基准：新加坡建屋局组屋 HDB 铁闸双门联动锁' : 'Core Retrofit Baseline: Singapore HDB Gate Mortise',
        desc: isZh ? '新加坡组屋特色。外侧铁防盗网门与内侧木门间距极窄（通常 <80mm）；改装锁外壳极易与内门拉手碰撞（Clash），需极窄面板与超薄把手。' : 'Singapore HDB benchmark. Gate-to-door gap <80mm causes severe handle collision.',
        image: '/assets/img/hero/hero-sea-hdb.jpg',
        familyId: 'sg-hdb-mortise',
        tag: isZh ? '⭐ 极强相关 · 东南亚基准' : '⭐ South East Asia Baseline'
      },
      items: items.filter(i => i.block === 'sea')
    },
    {
      code: 'gcc',
      title: isZh ? '🇦🇪🇸🇦 中东海湾板块 (Middle East / GCC — SASO / BS / EN)' : '🇦🇪🇸🇦 Middle East GCC (SASO)',
      shortTitle: isZh ? '中东海湾板块' : 'Middle East / GCC',
      subtitle: isZh ? '高客单重门耐候市场 · 沙特与阿联酋 60~90mm 超厚大门、英标 85mm 插芯、意标多点防盗与 75°C 太阳暴晒耐候工况' : 'High-AOV heavy door market · KSA/UAE 60-90mm doors, BS 85mm mortise & 75°C solar resistance',
      hero: {
        title: isZh ? '核心改装基准：海湾厚木门英标 85mm 重型插芯锁' : 'Core Retrofit Baseline: GCC BS 85mm Heavy-Duty Mortise',
        desc: isZh ? '中东公寓与独栋大门最主流五金。大门厚重（55~85mm），标配必须提供 ADP-11 超长螺栓与方轴包；电子系统需耐受 75°C 暴晒与 IP65 沙尘。' : 'GCC benchmark. 55-85mm heavy doors require ADP-11 long-tailpiece bolts & 75°C solar thermal design.',
        image: '/assets/img/gallery/eu-kfv-multipoint_real.jpg',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⭐ 极强相关 · 中东海湾基准' : '⭐ Middle East GCC Baseline'
      },
      items: items.filter(i => i.block === 'gcc')
    },
    {
      code: 'latam',
      title: isZh ? '🌎 拉美新兴板块 (Latin America — ABNT / IRAM)' : '🌎 Latin America (ABNT)',
      shortTitle: isZh ? '拉美新兴板块' : 'Latin America',
      subtitle: isZh ? '拉美大容量新兴五金体系 · 巴西 ABNT 窄背距插芯锁 (40/45mm)、薄门扇 (30mm) 与安第斯重型外装双钩锁' : 'Emerging market · Brazil ABNT narrow backsets (40/45mm), thin doors (30mm) & rim locks',
      hero: {
        title: isZh ? '核心改装基准：巴西 ABNT NBR 14913 极窄背距插芯锁 (PADO)' : 'Core Retrofit Baseline: Brazil ABNT Narrow Mortise (PADO)',
        desc: isZh ? '拉美市场第一基准。门框立柱极窄，背距仅 40mm/45mm；传统智能锁体过宽无法开槽，改装必须采用 38mm 极窄面板并保留原厂扣板。' : 'LatAm benchmark. Narrow stiles with 40/45mm backset require 38mm slim bodies.',
        image: '/assets/img/hero/hero-latam-abnt.webp',
        familyId: 'us-mortise',
        tag: isZh ? '⭐ 极强相关 · 拉美改装基准' : '⭐ Latin America Baseline'
      },
      items: items.filter(i => i.block === 'latam')
    },
    {
      code: 'af-sa',
      title: isZh ? '🇮🇳🇿🇦 非洲与南亚板块 (South Asia & Africa — BIS / SABS)' : '🇮🇳🇿🇦 South Asia & Africa (BIS)',
      shortTitle: isZh ? '非洲南亚板块' : 'South Asia & Africa',
      subtitle: isZh ? '印度 Godrej 表面夜闩死锁三插销体系、东非与南非 Union 杠杆防盗锁与高湿耐候工况' : 'Indian Godrej rim deadbolts, South African Union lever systems & tropical monsoon weatherproofing',
      hero: {
        title: isZh ? '核心改装基准：印度与南亚 Godrej 三插销外装防撬死锁' : 'Core Retrofit Baseline: Indian Godrej Tribolt Deadbolt',
        desc: isZh ? '印度与南亚民居第一基准。表面安装重型方形锁盒，三根高碳钢圆形死锁插销；内侧为机械大旋钮，改装需搭配专用外装夹爪。' : 'South Asian benchmark. Surface-mounted box with 3 heavy deadbolts requiring external pinch cams.',
        image: '/assets/img/indigenous/uk-nightlatch.jpg',
        familyId: 'in-mortise-rim',
        tag: isZh ? '⭐ 极强相关 · 南亚非洲基准' : '⭐ South Asia Africa Baseline'
      },
      items: items.filter(i => i.block === 'af-sa')
    }"""

pattern = r"    \{\s*code: 'na',.*?tag: isZh \? '⭐ 极强相关 · 南亚非洲基准' : '⭐ South Asia Africa Baseline'\s*\},?\s*items: items\.filter\(i => i\.block === 'af-sa'\)\s*\}"
match = re.search(pattern, code, re.DOTALL)
if match:
    code = code[:match.start()] + new_block_defs + code[match.end():]
    print('Block definitions updated.')

# 2. 优化卡片标题与基准行展示
old_card_body = """      <div class="gallery-portal-card__body">
        <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px; margin-bottom: 4px;">
          <h2 class="gallery-portal-card__name" style="margin: 0; flex: 1;">${escapeHtml(b.title)}</h2>
          <span style="font-size: 0.72rem; color: #64748b; font-weight: 600; white-space: nowrap; background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">${b.items.length} ${isZh ? '款' : 'models'}</span>
        </div>
        <div class="gallery-portal-card__baseline" style="color: var(--color-primary, #0f172a); font-weight: 500; font-size: 0.85rem;">${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, ''))}</div>
      </div>"""

new_card_body = """      <div class="gallery-portal-card__body">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 6px; margin-bottom: 4px;">
          <h2 class="gallery-portal-card__name" style="margin: 0; flex: 1; font-size: 0.96rem; font-weight: 700; line-height: 1.35; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(b.title)}">${escapeHtml(b.title)}</h2>
          <span style="font-size: 0.70rem; color: #64748b; font-weight: 700; white-space: nowrap; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; border: 1px solid #e2e8f0;">${b.items.length} ${isZh ? '款' : 'models'}</span>
        </div>
        <div class="gallery-portal-card__baseline" style="color: var(--color-primary, #0f172a); font-weight: 600; font-size: 0.82rem; line-height: 1.35; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, '').trim())}">${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, '').trim())}</div>
      </div>"""

if old_card_body in code:
    code = code.replace(old_card_body, new_card_body)
    print('Card body updated in build.mjs.')

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

# 3. 优化 CSS 样式
with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_css_part = """.gallery-wall--pure-portal .gallery-portal-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 1.25rem;
  margin: 1rem 0;
}

@media (min-width: 1100px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1.25rem;
  }
}
@media (min-width: 640px) and (max-width: 1099px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1.15rem;
  }
}
@media (max-width: 639px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: 1fr !important;
    gap: 1rem;
  }
}

.gallery-portal-card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(16, 42, 67, 0.07);
  transition: all .25s ease;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  cursor: pointer;
}"""

new_css_part = """.gallery-wall--pure-portal .gallery-portal-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 1.15rem;
  margin: 1rem 0 2.5rem;
  align-items: stretch;
}

@media (min-width: 1100px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1.15rem;
  }
}
@media (min-width: 640px) and (max-width: 1099px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1.15rem;
  }
}
@media (max-width: 639px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: 1fr !important;
    gap: 1rem;
  }
}

.gallery-portal-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
  transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  cursor: pointer;
  height: 100%;
}"""

if old_css_part in css:
    css = css.replace(old_css_part, new_css_part)
    print('CSS grid & card styles updated.')

old_media = """.gallery-portal-card__media {
  position: relative;
  width: 100%;
  height: 200px;
  background: #f8fafc;
  overflow: hidden;
}"""

new_media = """.gallery-portal-card__media {
  position: relative;
  width: 100%;
  height: 155px;
  background: #f8fafc;
  overflow: hidden;
}"""

if old_media in css:
    css = css.replace(old_media, new_media)
    print('Media height updated to 155px.')

old_body_css = """.gallery-portal-card__body {
  padding: 1.2rem 1.1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}"""

new_body_css = """.gallery-portal-card__body {
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  background: #ffffff;
}"""

if old_body_css in css:
    css = css.replace(old_body_css, new_body_css)
    print('Card body padding updated.')

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('All patches applied cleanly.')
