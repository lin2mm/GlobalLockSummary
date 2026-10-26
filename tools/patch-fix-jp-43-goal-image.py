import json

with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for it in items:
    if it.get('id') == 'JP-43':
        it['image'] = '/assets/img/gallery/jp-goal-lx-real.jpg'
        it['sceneImage'] = '/assets/img/gallery/jp-goal-lx-real.jpg'
        it['productImage'] = '/assets/img/gallery/jp-goal-lx-real.jpg'
        if 'installationGuide' in it:
            it['installationGuide']['schematic'] = '/assets/img/gallery/jp-goal-lx-real.jpg'
        print("Updated JP-43 to authentic Japanese GOAL door image!")

with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

