with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """/** Turn navigation hrefs into root-relative paths that work from any depth. */
function rewriteNav(nav) {
  return nav.map((item) => ({ ...item, href: item.href.startsWith('/') ? item.href : `/${item.href}` }));
}"""

replacement = """/** Turn navigation hrefs into root-relative paths that work from any depth and dynamically inject lock count. */
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

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs patched successfully!")
else:
    print("Target string not found in build.mjs!")
