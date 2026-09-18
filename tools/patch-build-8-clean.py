with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 替换 categories 遍历注册
text = text.replace(
    "for (const b of ['na', 'europe5', 'uk-anz', 'jp-kr', 'sea', 'gcc']) register(lang, `categories/${b}.html`);",
    "for (const b of ['na', 'latam', 'europe5', 'uk-anz', 'gcc', 'jp-kr', 'sea', 'af-sa']) register(lang, `categories/${b}.html`);"
)

# 2. 定位 getGalleryBlocks 并在 return [ ... ] 中加入 latam 与 af-sa
old_gcc_end = """      hero: {
        title: isZh ? '核心改装基准：海湾厚木门英标 85mm 重型插芯锁' : 'Core Retrofit Baseline: GCC BS 85mm Heavy-Duty Mortise',
        desc: isZh ? '中东公寓与独栋大门最主流五金。大门厚重（55~85mm），标配必须提供 ADP-11 超长螺栓与方轴包；电子系统需耐受 75°C 暴晒与 IP65 沙尘。' : 'GCC benchmark. 55-85mm heavy doors require ADP-11 long-tailpiece bolts & 75°C solar thermal design.',
        image: '/assets/img/gallery/eu-kfv-multipoint_real.jpg',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⭐ 极强相关 · 中东海湾基准' : '⭐ Middle East GCC Baseline'
      },
      items: items.filter(i => i.block === 'gcc')
    }"""

new_gcc_latam_af = """      hero: {
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
      title: isZh ? '🌎 拉美新兴板块 (Latin America — ABNT / IRAM)' : '🌎 Latin America (ABNT / IRAM)',
      shortTitle: isZh ? '拉美新兴板块' : 'Latin America',
      subtitle: isZh ? '拉美大容量新兴五金体系 · 巴西 ABNT 窄背距插芯锁 (40/45mm)、薄门扇 (30mm) 与安第斯重型外装双钩锁' : 'Emerging market · Brazil ABNT narrow backsets (40/45mm), thin doors (30mm) & rim locks',
      hero: {
        title: isZh ? '核心改装基准：巴西 ABNT NBR 14913 极窄背距插芯锁 (PADO)' : 'Core Retrofit Baseline: Brazil ABNT Narrow-Backset Mortise (PADO)',
        desc: isZh ? '拉美市场第一基准。门框立柱极窄，背距仅 40mm/45mm；传统智能锁体过宽无法开槽，改装必须采用 38mm 极窄面板并保留原厂扣板。' : 'LatAm benchmark. Narrow stiles with 40/45mm backset require 38mm slim bodies.',
        image: '/assets/img/hero/hero-latam-abnt.webp',
        familyId: 'latin-mortise',
        tag: isZh ? '⭐ 极强相关 · 拉美改装基准' : '⭐ Latin America Baseline'
      },
      items: items.filter(i => i.block === 'latam')
    },
    {
      code: 'af-sa',
      title: isZh ? '🇮🇳🇿🇦 非洲与南亚板块 (South Asia & Africa — BIS / SABS)' : '🇮🇳🇿🇦 South Asia & Africa (BIS / SABS)',
      shortTitle: isZh ? '非洲南亚板块' : 'South Asia & Africa',
      subtitle: isZh ? '印度 Godrej 表面夜闩死锁三插销体系、东非与南非 Union 杠杆防盗锁与高湿耐候工况' : 'Indian Godrej rim deadbolts, South African Union lever systems & tropical monsoon weatherproofing',
      hero: {
        title: isZh ? '核心改装基准：印度与南亚 Godrej 三插销外装防撬死锁' : 'Core Retrofit Baseline: Indian Godrej Tribolt Rim Deadbolt',
        desc: isZh ? '印度与南亚民居第一基准。表面安装重型方形锁盒，三根高碳钢圆形死锁插销；内侧为机械大旋钮，改装需搭配专用外装夹爪。' : 'South Asian benchmark. Surface-mounted box with 3 heavy deadbolts requiring external pinch cams.',
        image: '/assets/img/indigenous/uk-nightlatch.jpg',
        familyId: 'in-mortise-rim',
        tag: isZh ? '⭐ 极强相关 · 南亚非洲基准' : '⭐ South Asia Africa Baseline'
      },
      items: items.filter(i => i.block === 'af-sa')
    }"""

if old_gcc_end in text:
    text = text.replace(old_gcc_end, new_gcc_latam_af)
    print("Added latam & af-sa to getGalleryBlocks!")
else:
    print("Warning: old_gcc_end not matched.")

# 3. 替换全站残留的“5大板块”文字
text = text.replace("返回全球 5 大板块主图库", "返回全球 8 大工业板块主图库")
text = text.replace("Back to 5 Major Area Gallery", "Back to 8 Major Industrial Divisions")
text = text.replace("5大板块图库", "8大工业板块图库")
text = text.replace("5 Divisions Gallery", "8 Industrial Divisions Gallery")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

