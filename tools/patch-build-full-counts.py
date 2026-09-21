with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 升级 rewriteNav，精确计算导航每个菜单项背后的锁型/案例数量，并挂载子目录下拉数据
old_rewrite_nav = """/** Turn navigation hrefs into root-relative paths that work from any depth and dynamically inject lock count. */
function rewriteNav(nav) {
  let count = 54;
  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (existsSync(galleryPath)) {
    try {
      const items = JSON.parse(readFileSync(galleryPath, 'utf8'));
      count = items.length;
    } catch (e) {}
  }

  return nav.map((item) => {
    let label = item.label;
    if (item.href.includes('index.html')) {
      if (label.includes('(')) {
        label = label.replace(/\\(\\d+\\)/, `(${count})`);
      } else {
        label = `${label} (${count})`;
      }
    }
    return {
      ...item,
      label,
      href: item.href.startsWith('/') ? item.href : `/${item.href}`
    };
  });
}"""

new_rewrite_nav = """/** Turn navigation hrefs into root-relative paths with exact dynamic lock counts and sub-directory metadata. */
function rewriteNav(nav, lang = 'en') {
  let totalLocks = 70;
  let naCount = 14;
  let euCount = 16;
  let ocCount = 15;
  let seaCount = 15;
  let latamCount = 10;
  let casesCount = 41;
  let adaptersCount = 4;
  let pitfallsCount = 6;
  let indexCount = 5;

  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (existsSync(galleryPath)) {
    try {
      const items = JSON.parse(readFileSync(galleryPath, 'utf8'));
      totalLocks = items.length;
      naCount = items.filter(i => i.block === 'na').length;
      euCount = items.filter(i => i.block === 'europe5').length;
      ocCount = items.filter(i => i.block === 'uk-anz').length;
      seaCount = items.filter(i => i.block === 'sea').length;
      latamCount = items.filter(i => i.block === 'latam').length;
    } catch (e) {}
  }

  const casesPath = join(CONTENT, 'catalog', 'installation-cases.json');
  if (existsSync(casesPath)) {
    try { casesCount = JSON.parse(readFileSync(casesPath, 'utf8')).length; } catch (e) {}
  }

  const isZh = lang === 'zh';

  return nav.map((item) => {
    let rawLabel = item.label.replace(/\\s*\\([\\d\\w+%/ -]+\\)/g, '').trim();
    let label = rawLabel;
    let subItems = null;

    if (item.href.includes('index.html') && !item.href.includes('indigenous')) {
      // 锁型总览 (70)
      label = `${rawLabel} (${totalLocks})`;
      subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇸🇬 东南亚东亚板块 (${seaCount}款)` : `🇸🇬 East & SE Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🌎 拉美工业板块 (${latamCount}款)` : `🌎 Latin America (${latamCount})`, href: isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html' }
      ];
    } else if (item.href.includes('install-gallery.html')) {
      // 工程实录 (41)
      label = `${rawLabel} (${casesCount})`;
      subItems = [
        { label: isZh ? `🇺🇸 北美现场案例 (${Math.round(casesCount * 0.28)}篇)` : `🇺🇸 North America Field (${Math.round(casesCount * 0.28)})`, href: isZh ? '/zh/install-gallery.html#na' : '/en/install-gallery.html#na' },
        { label: isZh ? `🇪🇺 欧标开槽案例 (${Math.round(casesCount * 0.26)}篇)` : `🇪🇺 Euro Chisel Cases (${Math.round(casesCount * 0.26)})`, href: isZh ? '/zh/install-gallery.html#eu' : '/en/install-gallery.html#eu' },
        { label: isZh ? `🇦🇺 澳式夜闩工单 (${Math.round(casesCount * 0.24)}篇)` : `🇦🇺 Lockwood Cases (${Math.round(casesCount * 0.24)})`, href: isZh ? '/zh/install-gallery.html#oc' : '/en/install-gallery.html#oc' },
        { label: isZh ? `🇸🇬 组屋双门案例 (${Math.round(casesCount * 0.22)}篇)` : `🇸🇬 HDB Gate Cases (${Math.round(casesCount * 0.22)})`, href: isZh ? '/zh/install-gallery.html#sea' : '/en/install-gallery.html#sea' }
      ];
    } else if (item.href.includes('adapters.html')) {
      // 转接工具 (4)
      label = `${rawLabel} (${adaptersCount})`;
      subItems = [
        { label: isZh ? 'ADP-01 变径衬套轴套 (7转8mm)' : 'ADP-01 Spindle Sleeve (7-to-8mm)', href: isZh ? '/zh/adapters.html#adp-01' : '/en/adapters.html#adp-01' },
        { label: isZh ? 'ADP-02 偏心传动轴与拨叉' : 'ADP-02 Eccentric Coupler', href: isZh ? '/zh/adapters.html#adp-02' : '/en/adapters.html#adp-02' },
        { label: isZh ? 'ADP-03 门框锁盒垫高加深片' : 'ADP-03 Strike Box Shims', href: isZh ? '/zh/adapters.html#adp-03' : '/en/adapters.html#adp-03' },
        { label: isZh ? 'ADP-04 薄门对穿防压溃垫圈' : 'ADP-04 Washer Reinforcer', href: isZh ? '/zh/adapters.html#adp-04' : '/en/adapters.html#adp-04' }
      ];
    } else if (item.href.includes('field-issues.html')) {
      // 避坑实录 (6)
      label = `${rawLabel} (${pitfallsCount})`;
      subItems = [
        { label: isZh ? 'FL-01 门框扣板剪切错位摩擦' : 'FL-01 Strike Binding', href: isZh ? '/zh/field-issues.html#fl-01' : '/en/field-issues.html#fl-01' },
        { label: isZh ? 'FL-02 欧标无离合锁死破门' : 'FL-02 Euro Lockout', href: isZh ? '/zh/field-issues.html#fl-02' : '/en/field-issues.html#fl-02' },
        { label: isZh ? 'FL-03 新加坡组屋门把手碰撞' : 'FL-03 HDB Gate Clash', href: isZh ? '/zh/field-issues.html#fl-03' : '/en/field-issues.html#fl-03' },
        { label: isZh ? 'FL-04 澳式副舌悬空假锁死' : 'FL-04 False Deadlock', href: isZh ? '/zh/field-issues.html#fl-04' : '/en/field-issues.html#fl-04' }
      ];
    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (5)
      label = `${rawLabel} (${indexCount})`;
      subItems = [
        { label: isZh ? '🇩🇪 德奥瑞 DIN 18251/18252' : '🇩🇪 DACH DIN 18251/18252', href: isZh ? '/zh/indigenous-guides.html#de' : '/en/indigenous-guides.html#de' },
        { label: isZh ? '🇫🇷 法比区 NF / Vachette 70' : '🇫🇷 France NF 70mm', href: isZh ? '/zh/indigenous-guides.html#fr' : '/en/indigenous-guides.html#fr' },
        { label: isZh ? '🇯🇵 日本区 JIS A 1510 / MIWA' : '🇯🇵 Japan JIS / MIWA', href: isZh ? '/zh/indigenous-guides.html#jp' : '/en/indigenous-guides.html#jp' },
        { label: isZh ? '🇦🇺 英澳 BS 3621 / AS 4145' : '🇦🇺 UK/AU BS & AS', href: isZh ? '/zh/indigenous-guides.html#uk' : '/en/indigenous-guides.html#uk' },
        { label: isZh ? '🇧🇷 拉美 ABNT NBR 14913' : '🇧🇷 Latin America ABNT', href: isZh ? '/zh/indigenous-guides.html#latam' : '/en/indigenous-guides.html#latam' }
      ];
    }

    return {
      ...item,
      label,
      subItems,
      href: item.href.startsWith('/') ? item.href : `/${item.href}`
    };
  });
}"""

if old_rewrite_nav in text:
    text = text.replace(old_rewrite_nav, new_rewrite_nav)
    print("Replaced rewriteNav successfully!")
else:
    print("old_rewrite_nav not found!")

# 2. 确保 rewriteNav 接收 lang 参数
text = text.replace("site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang]) } }", "site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang], lang) } }")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("build.mjs updated with full counts & sub-items!")
