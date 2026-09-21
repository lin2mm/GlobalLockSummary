with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. 替换日韩精工板块的主图为完整的实态门锁 MIWA 13LA，彻底解决纯白孤立小旋钮与文字截断
old_jp_hero = """      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: Japan MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/indigenous/jp-thumbturn.jpg',
        familyId: 'jp-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },"""

new_jp_hero = """      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: Japan MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/indigenous/jp-miwa-13la.jpg',
        familyId: 'jp-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },"""

if old_jp_hero in code:
    code = code.replace(old_jp_hero, new_jp_hero)
    print("Replaced jp-thumbturn with full door lock jp-miwa-13la.jpg in build.mjs!")
else:
    print("old_jp_hero not found in build.mjs")

# 2. 视觉注意力层级（Visual Attention）：前 4 大板块均为第一梯队重点（北美、欧陆、澳英、日韩），赋予核心基准微标签
old_core_tier = "const isCoreTier1 = ['na', 'europe5', 'uk-anz'].includes(b.code);"
new_core_tier = "const isCoreTier1 = ['na', 'europe5', 'uk-anz', 'jp-kr'].includes(b.code);"

if old_core_tier in code:
    code = code.replace(old_core_tier, new_core_tier)
    print("Added jp-kr into core tier baselines for balanced 4x2 visual hierarchy!")
else:
    print("old_core_tier not found in build.mjs")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

