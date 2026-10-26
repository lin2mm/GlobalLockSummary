with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 替换 getGalleryBlocks 为 8 大工业板块
idx_start = text.find('function getGalleryBlocks(lang) {')
idx_return = text.find('  return [', idx_start)
idx_end = text.find('  ];\n}', idx_return)

eight_blocks_code = """  return [
    {
      code: 'na',
      title: isZh ? '🇺🇸 北美标准板块 (Americas — ANSI / BHMA)' : '🇺🇸 North America (Americas — ANSI / BHMA)',
      shortTitle: isZh ? '北美标准板块' : 'North America',
      subtitle: isZh ? '全球存量最大的智能锁加装市场 · 标准 54mm 大孔位、单插销死锁 (Deadbolt) 与 60/70mm 标准背距' : 'World largest retrofit market · Standard 54mm bore, deadbolt & 60/70mm backset',
      hero: {
        title: isZh ? '核心改装基准：美标单缸插销死锁 (ANSI Deadbolt / Schlage B60)' : 'Core Retrofit Baseline: ANSI Single-Cylinder Deadbolt (Schlage B60)',
        desc: isZh ? 'August 与 SwitchBot 的全球基本盘。标准扁平尾轴（Tailpiece）直接啮合；改造核心难点在于门扇下沉与密封条导致插销与扣板卡阻。' : 'Core baseline for August & SwitchBot. Flat tailpiece interface; key challenge is sag binding.',
        image: '/assets/img/hero/hero-na-deadbolt.png',
        familyId: 'us-deadbolt',
        tag: isZh ? '⭐ 极强相关 · 改装第一基准' : '⭐ Core Retrofit Baseline'
      },
      items: items.filter(i => i.block === 'na')
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
      code: 'europe5',
      title: isZh ? '🇪🇺 欧陆五国板块 (Continental Europe — DIN / EN)' : '🇪🇺 Continental Europe (DIN / EN)',
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
      title: isZh ? '🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK — AS / BS)' : '🇦🇺🇬🇧 Australia, NZ & UK (Pacific & UK — AS / BS)',
      shortTitle: isZh ? '澳新英国板块' : 'Australia & UK',
      subtitle: isZh ? '高防盗高人工成本市场 · 澳洲 Lockwood 001 表面安装夜闩锁 (Rim Deadlatch)、大洋洲短进深锁体与英国 5 拨杆防盗插芯锁' : 'High-security & high-labor market · Lockwood 001 surface deadlatches, short-backset & BS 5-lever',
      hero: {
        title: isZh ? '核心改装基准：澳式表面安装双扣死锁 (Lockwood 001 Deadlatch)' : 'Core Retrofit Baseline: Australian Lockwood 001 Deadlatch',
        desc: isZh ? '澳洲独栋木门第一基准。特有水滴形大旋钮需专属 ADP-05 夹具；致命点在于辅舌必须完全压入方可死锁，门缝变异极易引发假锁死。' : 'AU wooden door benchmark. Teardrop turn requires ADP-05 adapter; auxiliary bolt must depress fully.',
        image: '/assets/img/hero/hero-anz-lockwood001.jpg',
        familyId: 'au-deadlatch',
        tag: isZh ? '⭐ 极强相关 · 澳新第一基准' : '⭐ Pacific Baseline'
      },
      items: items.filter(i => i.block === 'uk-anz')
    },
    {
      code: 'gcc',
      title: isZh ? '🇦🇪🇸🇦 中东海湾板块 (Middle East / GCC — SASO / BS / EN)' : '🇦🇪🇸🇦 Middle East / GCC (SASO / BS / EN)',
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
      code: 'jp-kr',
      title: isZh ? '🇯🇵🇰🇷 日韩精工板块 (Japan & Korea — JIS / KS)' : '🇯🇵🇰🇷 Japan & Korea (JIS / KS)',
      shortTitle: isZh ? '日韩精工板块' : 'Japan & Korea',
      subtitle: isZh ? '极高精密装配工业体系 · 日本 MIWA / GOAL 超薄锁体、B5 防犯捏合旋钮与韩国无孔全自动锁' : 'Precision Asian standards · MIWA/GOAL slim mortise, B5 anti-theft thumbturn & Korean electronic push-pull',
      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: Japan MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/indigenous/jp-thumbturn.jpg',
        familyId: 'jp-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },
      items: items.filter(i => i.block === 'jp-kr')
    },
    {
      code: 'sea',
      title: isZh ? '🇸🇬🇲🇾 东南亚东盟板块 (ASEAN / SEA — SS / MS)' : '🇸🇬🇲🇾 South East Asia (ASEAN / SEA — SS / MS)',
      shortTitle: isZh ? '东南亚板块' : 'South East Asia',
      subtitle: isZh ? '东盟高密度热带五金体系 · 新加坡组屋 HDB 外铁闸与内木门极窄防撞空间、大马与泰国窄体铝门锁' : 'High-density tropical ASEAN systems · Singapore HDB gate clash, Malaysian & Thai narrow aluminum doors',
      hero: {
        title: isZh ? '核心改装基准：新加坡建屋局组屋 HDB 铁闸双门联动锁' : 'Core Retrofit Baseline: Singapore HDB Metal Gate Clash Mortise',
        desc: isZh ? '新加坡组屋特色。外侧铁防盗网门与内侧木门间距极窄（通常 <80mm）；改装锁外壳极易与内门拉手碰撞（Clash），需极窄面板与超薄把手。' : 'Singapore HDB benchmark. Gate-to-door gap <80mm causes severe handle collision.',
        image: '/assets/img/hero/hero-sea-hdb.jpg',
        familyId: 'sg-hdb-mortise',
        tag: isZh ? '⭐ 极强相关 · 东南亚基准' : '⭐ South East Asia Baseline'
      },
      items: items.filter(i => i.block === 'sea')
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
    }
  ];"""

text = text[:idx_return] + eight_blocks_code + text[idx_end+5:]

# 2. 更新 categories 注册
text = text.replace(
    "for (const b of ['na', 'europe5', 'uk-anz', 'jp-kr', 'sea', 'gcc']) register(lang, `categories/${b}.html`);",
    "for (const b of ['na', 'latam', 'europe5', 'uk-anz', 'gcc', 'jp-kr', 'sea', 'af-sa']) register(lang, `categories/${b}.html`);"
)

# 3. 替换全站残留的“返回全球 5 大板块”为动态
text = text.replace("返回全球 5 大板块主图库", "返回全球 8 大工业板块主图库")
text = text.replace("Back to 5 Major Area Gallery", "Back to 8 Major Industrial Divisions")
text = text.replace("5大板块图库", "8大工业板块图库")
text = text.replace("5 Divisions Gallery", "8 Industrial Divisions Gallery")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated build.mjs with 8 blocks and dynamic navigation!")
