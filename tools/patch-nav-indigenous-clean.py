with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

old_indigenous_sub = """    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (5)
      label = `${rawLabel} (${indexCount})`;
      subItems = [
        { label: isZh ? '🇩🇪 德奥瑞 DIN 18251/18252' : '🇩🇪 DACH DIN 18251/18252', href: isZh ? '/zh/indigenous-guides.html#de' : '/en/indigenous-guides.html#de' },
        { label: isZh ? '🇫🇷 法比区 NF / Vachette 70' : '🇫🇷 France NF 70mm', href: isZh ? '/zh/indigenous-guides.html#fr' : '/en/indigenous-guides.html#fr' },
        { label: isZh ? '🇯🇵 日本区 JIS A 1510 / MIWA' : '🇯🇵 Japan JIS / MIWA', href: isZh ? '/zh/indigenous-guides.html#jp' : '/en/indigenous-guides.html#jp' },
        { label: isZh ? '🇦🇺 英澳 BS 3621 / AS 4145' : '🇦🇺 UK/AU BS & AS', href: isZh ? '/zh/indigenous-guides.html#uk' : '/en/indigenous-guides.html#uk' },
        { label: isZh ? '🇧🇷 拉美 ABNT NBR 14913' : '🇧🇷 Latin America ABNT', href: isZh ? '/zh/indigenous-guides.html#latam' : '/en/indigenous-guides.html#latam' }
      ];
    }"""

new_indigenous_sub = """    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (6)
      indexCount = 6;
      label = `${rawLabel} (${indexCount})`;
      subItems = [
        { label: isZh ? '🇩🇪 德奥瑞 DIN 18251 锁体与双向离合' : '🇩🇪 DACH DIN 18251 & Dual Clutch', href: isZh ? '/zh/indigenous-guides.html#de-at-ch' : '/en/indigenous-guides.html#de-at-ch' },
        { label: isZh ? '🇫🇷 法比区 NF 70mm 与 7mm 特殊方轴' : '🇫🇷 France NF 70mm & 7mm Spindle', href: isZh ? '/zh/indigenous-guides.html#fr-be' : '/en/indigenous-guides.html#fr-be' },
        { label: isZh ? '🇯🇵 日本区 MIWA 刻印与防盗旋钮抓取' : '🇯🇵 Japan MIWA Case & Pinch Grip', href: isZh ? '/zh/indigenous-guides.html#jp' : '/en/indigenous-guides.html#jp' },
        { label: isZh ? '🇦🇺 澳新英国 Lockwood 001 辅舌死锁' : '🇦🇺 UK/ANZ Lockwood 001 Deadlatch', href: isZh ? '/zh/indigenous-guides.html#uk-anz' : '/en/indigenous-guides.html#uk-anz' },
        { label: isZh ? '🇧🇷 西语拉美 ABNT 40mm 极窄进深' : '🇧🇷 LatAm ABNT 40mm Narrow Backset', href: isZh ? '/zh/indigenous-guides.html#latam' : '/en/indigenous-guides.html#latam' },
        { label: isZh ? '🇺🇸 北美 ANSI 54mm 大孔与扁轴死锁' : '🇺🇸 North America ANSI 54mm Bore', href: isZh ? '/zh/indigenous-guides.html#na' : '/en/indigenous-guides.html#na' }
      ];
    }"""

if old_indigenous_sub in text:
    text = text.replace(old_indigenous_sub, new_indigenous_sub)
    print("Replaced old_indigenous_sub successfully!")
else:
    print("old_indigenous_sub not matched directly")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

