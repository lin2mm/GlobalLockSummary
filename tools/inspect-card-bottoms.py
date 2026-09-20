with open("content/pages/zh/field-issues.md", "r", encoding="utf-8") as f:
    text = f.read()

cards = text.split('<div class="gallery-card"')
if len(cards) > 1:
    print(cards[1][-600:])
