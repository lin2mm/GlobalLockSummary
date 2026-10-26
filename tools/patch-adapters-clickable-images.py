import re

def patch_adapters(filepath, is_zh=True):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    cards = text.split('<div class="gallery-card"')
    new_cards = [cards[0]]

    for card in cards[1:]:
        # 寻找卡片内部的详情页链接 href="/zh/locks/..." 或 href="/en/locks/..."
        m_link = re.search(r'href="(/[^"/]+/locks/[^"]+\.html)"', card)
        if m_link:
            target_url = m_link.group(1)
            # 找到图片并为其包裹 <a> 标签
            # 检查图片是否已有 <a> 包裹
            img_pat = r'(<div style="height: 150px;[^>]*>)\s*(<img [^>]*>)'
            def img_repl(m):
                box_div = m.group(1)
                img_tag = m.group(2)
                return f'{box_div}\n      <a href="{target_url}" style="display: block; width: 100%; height: 100%; cursor: pointer;" title="点击查看对应锁型图谱与五金工程详情">{img_tag}</a>'
            card = re.sub(img_pat, img_repl, card, count=1)
        new_cards.append(card)

    new_text = '<div class="gallery-card"'.join(new_cards)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_text)

patch_adapters("content/pages/zh/adapters.md", True)
patch_adapters("content/pages/en/adapters.md", False)
print("Finished patching adapters.md with clickable images.")
