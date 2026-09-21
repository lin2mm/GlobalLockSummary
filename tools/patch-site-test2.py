with open('tests/site.test.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = "console.log(`OK  ${passed} checks passed`);"
check_code = """
// Check that nav link for catalog dynamically includes lock count
const zhIndexPage = read(join(SITE, 'zh/index.html'));
const galleryCount = JSON.parse(read(join(ROOT, 'content/catalog/gallery.json'))).length;
check(`Catalog nav link includes dynamic count (${galleryCount})`, zhIndexPage.includes(`(${galleryCount})`));

console.log(`OK  ${passed} checks passed`);"""

text = text.replace(target, check_code)
with open('tests/site.test.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied site test correctly!")
