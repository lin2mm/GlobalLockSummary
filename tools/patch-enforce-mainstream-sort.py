with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

old_snippet = """  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (!existsSync(galleryPath)) return [];
  const items = JSON.parse(readFileSync(galleryPath, 'utf8'));"""

new_snippet = """  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (!existsSync(galleryPath)) return [];
  const items = JSON.parse(readFileSync(galleryPath, 'utf8'));
  // 核心排序依据：1. 主流基准 (Mainstream) 严格排在最前面；2. 综合打分/市场占有率 (selectionScore) 降序排列
  items.sort((a, b) => {
    const aMain = a.tierClass === 'Mainstream' ? 1 : 0;
    const bMain = b.tierClass === 'Mainstream' ? 1 : 0;
    if (aMain !== bMain) return bMain - aMain; // 主流排在非主流前面
    const aScore = (a.selectionScore && a.selectionScore.overallScore) || 0;
    const bScore = (b.selectionScore && b.selectionScore.overallScore) || 0;
    if (aScore !== bScore) return bScore - aScore; // 得分高的排前面
    return a.id.localeCompare(b.id);
  });"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Enforced mainstream-first sorting order in getGalleryBlocks successfully!")
else:
    print("old_snippet not found!")

