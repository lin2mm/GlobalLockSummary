with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 升级 nav 渲染：如果有 subItems，则渲染为高级带有悬停下拉子目录的交互结构
target = """    const icon = item.iconSvg ? `<span class=\"nav__icon-wrap\" style=\"display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; opacity: 0.85;\">${item.iconSvg}</span>` : '';
    return `<a class=\"nav__link\" href=\"${esc(item.href)}\"${active} style=\"display: inline-flex; align-items: center;\">${icon}<span>${esc(item.label)}</span></a>`;"""

replacement = """    const icon = item.iconSvg ? `<span class=\"nav__icon-wrap\" style=\"display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; opacity: 0.85;\">${item.iconSvg}</span>` : '';
    
    if (item.subItems && item.subItems.length > 0) {
      const subMenuHtml = item.subItems.map(sub => 
        `<a class=\"nav__sub-link\" href=\"${esc(sub.href)}\" style=\"display: block; padding: 7px 14px; font-size: 0.82rem; color: #334155; text-decoration: none; border-bottom: 1px solid #f1f5f9; white-space: nowrap; transition: background 0.15s;\">${esc(sub.label)}</a>`
      ).join('');

      return `<div class=\"nav__dropdown\" style=\"position: relative; display: inline-flex; align-items: center;\">
        <a class=\"nav__link\" href=\"${esc(item.href)}\"${active} style=\"display: inline-flex; align-items: center;\">
          ${icon}<span>${esc(item.label)}</span>
          <span style=\"font-size: 0.65rem; margin-left: 4px; opacity: 0.6;\">▼</span>
        </a>
        <div class=\"nav__dropdown-menu\" style=\"position: absolute; top: 100%; left: 0; min-width: 220px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: none; z-index: 1000; padding: 4px 0;\">
          ${subMenuHtml}
        </div>
      </div>`;
    }

    return `<a class=\"nav__link\" href=\"${esc(item.href)}\"${active} style=\"display: inline-flex; align-items: center;\">${icon}<span>${esc(item.label)}</span></a>`;"""

if target in text:
    text = text.replace(target, replacement)
    with open('src/layout.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("src/layout.mjs successfully updated with dropdown sub-directories!")
else:
    print("target not found in src/layout.mjs!")
