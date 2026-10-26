# -*- coding: utf-8 -*-
import json

with open("content/catalog/adapters-bom.json", "r", encoding="utf-8") as f:
    bom = json.load(f)

print(f"Loaded {len(bom)} items from adapters-bom.json")
for item in bom:
    print(item.get("id"), item.get("targetFamily"), item.get("material"), item.get("specsShort"))
