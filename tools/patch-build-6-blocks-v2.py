with open('build.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "code: 'sea'" in line:
        # 替换 sea 和 latam
        block_code = """    {
      code: 'jp-kr',
      title: isZh ? '🇯🇵🇰🇷 日韩精工板块 (Japan & Korea — JIS / KS)' : '🇯🇵🇰🇷 Japan & Korea (JIS / KS)',
      shortTitle: isZh ? '日韩精工板块' : 'Japan & Korea',
      subtitle: isZh ? '极高精密装配工业体系 · 日本 MIWA / GOAL 超薄锁体、B5 防犯捏合旋钮与韩国无孔全自动锁' : 'Precision Asian standards · MIWA/GOAL slim mortise, B5 anti-theft thumbturn & Korean electronic push-pull',
      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: Japan MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/indigenous/jp-thumbturn.jpg',
        familyId: 'japan-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },
      items: items.filter(i => i.block === 'jp-kr')
    },
    {
      code: 'sea',
      title: isZh ? '🇸🇬🇲🇾 东南亚板块 (ASEAN / SEA — SS / MS)' : '🇸🇬🇲🇾 South East Asia (ASEAN / SEA — SS / MS)',
      shortTitle: isZh ? '东南亚板块' : 'South East Asia',
      subtitle: isZh ? '东盟高密度热带五金体系 · 新加坡组屋 HDB 外铁闸与内木门极窄防撞空间、大马与泰国窄体铝门锁' : 'High-density tropical ASEAN systems · Singapore HDB gate clash, Malaysian & Thai narrow aluminum doors',
      hero: {
        title: isZh ? '核心改装基准：新加坡建屋局组屋 HDB 铁闸双门联动锁' : 'Core Retrofit Baseline: Singapore HDB Metal Gate Clash Mortise',
        desc: isZh ? '新加坡组屋特色。外侧铁防盗网门与内侧木门间距极窄（通常 <80mm）；改装锁外壳极易与内门拉手碰撞（Clash），需极窄面板与超薄把手。' : 'Singapore HDB benchmark. Gate-to-door gap <80mm causes severe handle collision.',
        image: '/assets/img/hero/hero-sea-hdb.jpg',
        familyId: 'singapore-hdb-gate',
        tag: isZh ? '⭐ 极强相关 · 东南亚基准' : '⭐ South East Asia Baseline'
      },
      items: items.filter(i => i.block === 'sea')
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
    }
"""
        new_lines.append(block_code)
        skip = True
    elif skip and "items: items.filter(i => i.block === 'latam')" in line:
        skip = False
        continue # 跳过 latam 的结尾
    elif not skip:
        new_lines.append(line)

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("build.mjs successfully rewritten with 6-block array!")
