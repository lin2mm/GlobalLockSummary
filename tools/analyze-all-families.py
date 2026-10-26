import json, glob

with open("content/catalog/gallery.json") as f:
    items = json.load(f)

for p in sorted(glob.glob("content/catalog/lock-families/*.json")):
    fam_id = p.split("/")[-1].replace(".json", "")
    fam_samples = [i for i in items if i.get("familyId") == fam_id]
    types = set()
    for s in fam_samples:
        t = s.get("title", {}).get("zh", s.get("title", {}).get("en"))
        types.add(t.split("：")[0].split(":")[0].strip())
    print(f"{fam_id:25} | count: {len(fam_samples):2} | sample types: {list(types)[:3]}")
