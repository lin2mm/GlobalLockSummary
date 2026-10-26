import re

def reorder_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    header_part = content[:content.find('<div style="display: grid;')]
    grid_start = content.find('<div style="display: grid;')
    grid_open = content[grid_start:content.find('>', grid_start) + 1]
    cards_part = content[content.find('>', grid_start) + 1:content.rfind('</div>')]
    footer_part = content[content.rfind('</div>'):]

    raw_cards = re.split(r'(?=<div class="gallery-card" id="adp-)', cards_part)
    cards = [c.strip() for c in raw_cards if c.strip().startswith('<div class="gallery-card" id="adp-')]
    
    card_dict = {}
    for c in cards:
        m = re.search(r'id="(adp-\d+)"', c)
        if m:
            card_dict[m.group(1)] = c

    # 商业出货量大盘排序
    market_priority = [
        'adp-04', 'adp-06', 'adp-03', 'adp-07', 'adp-05', 'adp-01',
        'adp-02', 'adp-08', 'adp-11', 'adp-12', 'adp-10', 'adp-09'
    ]

    reordered_cards = []
    for pid in market_priority:
        if pid in card_dict:
            reordered_cards.append(card_dict[pid])

    new_content = header_part + grid_open + '\n\n  ' + '\n\n  '.join(reordered_cards) + '\n' + footer_part
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Reordered {path} based on global market sales volume!")

reorder_file('content/pages/zh/adapters.md')
reorder_file('content/pages/en/adapters.md')

