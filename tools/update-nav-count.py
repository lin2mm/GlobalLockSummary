import json

with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
    locks = json.load(f)

total_count = len(locks)
print(f"Current total lock count: {total_count}")

with open('content/site.json', 'r', encoding='utf-8') as f:
    site = json.load(f)

# 更新 zh 与 en 导航中的锁型总览标签
for item in site['navigation']['zh']:
    if 'index.html' in item['href']:
        item['label'] = f"锁型总览 ({total_count})"

for item in site['navigation']['en']:
    if 'index.html' in item['href']:
        item['label'] = f"Lock Catalog ({total_count})"

with open('content/site.json', 'w', encoding='utf-8') as f:
    json.dump(site, f, ensure_ascii=False, indent=2)

print("Updated content/site.json navigation labels with dynamic lock count!")
