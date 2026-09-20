with open("content/pages/zh/adapters.md", "r", encoding="utf-8") as f:
    adp_zh = f.read()

print("=== adapters.md card sample ===")
cards = adp_zh.split('<div class="gallery-card"')
if len(cards) > 1:
    print(cards[1][:800])

with open("content/pages/zh/field-issues.md", "r", encoding="utf-8") as f:
    fl_zh = f.read()

print("\n=== field-issues.md card sample ===")
fl_cards = fl_zh.split('<div class="gallery-card"')
if len(fl_cards) > 1:
    print(fl_cards[1][:800])
