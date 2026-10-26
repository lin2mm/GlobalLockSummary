import json

with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
    gallery = json.load(f)

with open('content/catalog/adapters-bom.json', 'r', encoding='utf-8') as f:
    adapters = json.load(f)

print(f"Total gallery locks: {len(gallery)}")
print(f"Total adapters: {len(adapters)}")

# 统计各标准/形态的分布
standards_count = {}
for item in gallery:
    std = item.get('standard', 'Unknown')
    standards_count[std] = standards_count.get(std, 0) + 1

print("\n--- Standards distribution ---")
for k, v in sorted(standards_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{k}: {v}")

