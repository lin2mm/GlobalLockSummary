with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

patent_subnav = """    } else if (item.href.includes('patent-avoidance.html')) {
      subItems = [
        { label: isZh ? '1. 锁芯夹持与背板锁紧' : '1. Cylinder Clamping', href: isZh ? '/zh/patent-avoidance.html#nuki-clamping' : '/en/patent-avoidance.html#nuki-clamping' },
        { label: isZh ? '2. 钥匙抓取与浮动耦合' : '2. Key Gripper & Oldham', href: isZh ? '/zh/patent-avoidance.html#key-coupling' : '/en/patent-avoidance.html#key-coupling' },
        { label: isZh ? '3. 手动优先与脱开离合' : '3. Manual Clutch & BLDC', href: isZh ? '/zh/patent-avoidance.html#clutch-disconnect' : '/en/patent-avoidance.html#clutch-disconnect' },
        { label: isZh ? '4. 尾轴卡扣与翼形卡爪' : '4. Tailpiece Wing Latches', href: isZh ? '/zh/patent-avoidance.html#august-tailpiece' : '/en/patent-avoidance.html#august-tailpiece' },
        { label: isZh ? '5. 出海 FTO 自查清单' : '5. Global FTO Checklist', href: isZh ? '/zh/patent-avoidance.html#checklist' : '/en/patent-avoidance.html#checklist' }
      ];"""

if "patent-avoidance.html" not in code:
    code = code.replace("    } else if (item.href.includes('indigenous-guides.html')) {", patent_subnav + "\n    } else if (item.href.includes('indigenous-guides.html')) {")
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Patched build.mjs with patent subnav!")
else:
    print("patent-avoidance.html already in build.mjs")

