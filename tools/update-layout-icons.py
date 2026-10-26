import re

with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 替换左上角品牌图标
old_brand_pat = r'<svg class="brand__mark".*?</svg>'
new_brand_svg = '''<svg class="brand__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false" style="width: 1.6rem; height: 1.6rem;">
          <defs>
            <linearGradient id="brandMarkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0284c7"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>
          <path d="M12 2 C7.58 2 4 5.58 4 10 C4 12.8 5.6 15.2 8 16.5 L8 21 C8 21.55 8.45 22 9 22 L15 22 C15.55 22 16 21.55 16 21 L16 16.5 C18.4 15.2 20 12.8 20 10 C20 5.58 16.42 2 12 2 Z" fill="url(#brandMarkGrad)"/>
          <circle cx="12" cy="9.5" r="3" fill="#ffffff" fill-opacity="0.95"/>
          <path d="M11.3 9 h1.4 v3 h-1.4 Z" fill="#0284c7"/>
          <rect x="11.2" y="16.5" width="1.6" height="3.5" rx="0.8" fill="#ffffff" fill-opacity="0.95"/>
        </svg>'''

text = re.sub(old_brand_pat, new_brand_svg, text, count=1, flags=re.DOTALL)

# 2. 替换导航链接渲染
old_nav_snippet = "return `<a class=\"nav__link\" href=\"${esc(item.href)}\"${active}>${esc(item.label)}</a>`;"
new_nav_snippet = "const icon = item.iconSvg ? `<span class=\"nav__icon-wrap\" style=\"display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; opacity: 0.85;\">${item.iconSvg}</span>` : '';\n    return `<a class=\"nav__link\" href=\"${esc(item.href)}\"${active} style=\"display: inline-flex; align-items: center;\">${icon}<span>${esc(item.label)}</span></a>`;"

text = text.replace(old_nav_snippet, new_nav_snippet)

with open('src/layout.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated src/layout.mjs with high-end Euro-Cylinder brand icon & nav icons!")
