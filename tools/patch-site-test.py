with open('tests/site.test.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 清理最后出错的行
while lines and ('OUT' in lines[-1] or 'expectedCatalogNav' in lines[-1] or 'Catalog nav link' in lines[-1]):
    lines.pop()

check_code = """
// Check that nav link for catalog dynamically includes lock count
const zhIndexHtml = readFileSync(join(SITE, 'zh/index.html'), 'utf8');
const allGalleryItems = JSON.parse(readFileSync(join(ROOT, 'content/catalog/gallery.json'), 'utf8'));
const expectedCatalogNav = `(${allGalleryItems.length})`;
check(`Catalog nav link includes dynamic count ${expectedCatalogNav}`, zhIndexHtml.includes(expectedCatalogNav));
"""

lines.append(check_code)

with open('tests/site.test.mjs', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("tests/site.test.mjs patched successfully!")
