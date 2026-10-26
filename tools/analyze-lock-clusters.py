import json

with open("content/catalog/gallery.json") as f:
    items = json.load(f)

euro_items = [i for i in items if i.get("familyId") == "euro-cylinder-mortise"]
print(f"Total euro items: {len(euro_items)}")

clusters = {}
for it in euro_items:
    sid = it.get("id")
    title = it.get("title", {}).get("zh", it.get("title", {}).get("en"))
    # 聚类规则
    if "Thumbturn" in title or "手扭" in title or "旋钮" in title:
        group = "thumbturn"
    elif "双锁芯" in title or "30/30" in title or "35/35" in title or "EVVA" in title or "ABUS" in title or "Bravus" in title or "blueChip" in title or "Diamant" in title:
        group = "double-cylinder"
    elif "插芯锁体" in title or "锁体" in title or "OneFit" in title or "Bricard" in title or "Electa" in title or "PADO" in title or "La Fonte" in title or "Silvana" in title or "Fechadura" in title or "GCC" in title:
        group = "mortise-case"
    else:
        group = "specialty"
    clusters.setdefault(group, []).append((sid, title))

for g, lst in clusters.items():
    print(f"[{g}] ({len(lst)}款):")
    for sid, t in lst:
        print(f"   - {sid}: {t}")
