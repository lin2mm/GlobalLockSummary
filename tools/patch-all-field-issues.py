import re

mapping_zh = {
    "FL-01": ("/zh/locks/us-deadbolt.html", "北美 ANSI 呆锁与插销详情"),
    "FL-02": ("/zh/locks/euro-cylinder-mortise.html", "欧标 DIN 插芯锁族详情"),
    "FL-03": ("/zh/locks/sg-metal-gate-lock.html", "新加坡组屋铁门锁族详情"),
    "FL-04": ("/zh/locks/au-deadlatch.html", "澳洲 Lockwood 001 辅舌死锁详情"),
    "FL-05": ("/zh/categories/latam.html", "拉美窄体锁体板块详情"),
    "FL-06": ("/zh/categories/gcc.html", "中东重型欧标插芯锁板块详情")
}

mapping_en = {
    "FL-01": ("/en/locks/us-deadbolt.html", "US ANSI Deadbolt Specification"),
    "FL-02": ("/en/locks/euro-cylinder-mortise.html", "Euro DIN Mortise Lock Family"),
    "FL-03": ("/en/locks/sg-metal-gate-lock.html", "Singapore HDB Metal Gate Lock Family"),
    "FL-04": ("/en/locks/au-deadlatch.html", "ANZ Lockwood 001 Deadlatch Family"),
    "FL-05": ("/en/categories/latam.html", "LatAm Narrow Profile Division"),
    "FL-06": ("/en/categories/gcc.html", "GCC Heavy Mortise Division")
}

def clean_and_repatch(filepath, mapping, is_zh=True):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    cards = text.split('<div class="gallery-card"')
    new_cards = [cards[0]]

    for card in cards[1:]:
        # 寻找匹配的 FL-0x
        matched_fl = None
        for fl_id in mapping:
            if fl_id in card:
                matched_fl = fl_id
                break
        
        if matched_fl:
            url, desc = mapping[matched_fl]
            # 先清除可能存在的重复链接
            card = re.sub(r'<a href="[^"]+"[^>]*>([\s\S]*?)</a>', r'\1', card)
            
            # 1. 替换图片区域，使整张图片可点击直达
            card = re.sub(
                r'(<img [^>]*src="([^"]+)"[^>]*alt="([^"]+)"[^>]*>)',
                rf'<a href="{url}" style="display: block; width: 100%; height: 100%; cursor: pointer;" title="{desc}">\1</a>',
                card,
                count=1
            )
            # 2. 替换标题，使标题包含链接
            def h3_repl(m):
                h3_attrs = m.group(1)
                inner = m.group(2).strip()
                return f'<h3{h3_attrs}><a href="{url}" style="color: inherit; text-decoration: none;">{inner}</a></h3>'
            
            card = re.sub(r'<h3([^>]*)>(.*?)</h3>', h3_repl, card, count=1)
            
            # 3. 在卡片底部增加一个明确的极简直达按钮
            btn_text = "查看对应锁族图谱与公差 →" if is_zh else "View Lock Family & Tolerances →"
            footer_html = f'''
      <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #e2e8f0; display: flex; justify-content: flex-end;">
        <a href="{url}" style="font-size: 0.76rem; font-weight: 700; color: #0B1D47; text-decoration: none;">{btn_text}</a>
      </div>
'''
            # 插入到卡片最后一个 </div> 之前
            last_div_idx = card.rfind('</div>')
            if last_div_idx != -1:
                card = card[:last_div_idx] + footer_html + card[last_div_idx:]

        new_cards.append(card)

    new_text = '<div class="gallery-card"'.join(new_cards)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_text)

clean_and_repatch("content/pages/zh/field-issues.md", mapping_zh, True)
clean_and_repatch("content/pages/en/field-issues.md", mapping_en, False)
print("Finished clean repatching of field-issues.md with verified existing paths.")
