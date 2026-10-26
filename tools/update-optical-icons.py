import re
import json

# 1. 更新 src/layout.mjs 中的品牌图标
with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 高级感设计：
# 采用精密工业六角切角防撬锁体 (Hex-Shield Chassis) + 加粗拱形实心硬化钢锁梁 (Heavy-duty Shackle)
# 中心采用经典通透的大孔径水滴钥匙孔 (Bold Paracentric Keyhole) 配合高对比度切孔，
# 无论缩小至 14px 还是放大至 128px，人眼大脑均能瞬间捕捉到两处特征：“顶部锁梁” + “正中大锁孔”，100% 毫无歧义断定为“锁”！
# 材质采用钛金属微渐变 (#0284c7 -> #0f172a)，兼顾高级质感与极致识别。

new_brand_svg = '''<svg class="brand__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false" style="width: 1.65rem; height: 1.65rem;">
          <defs>
            <linearGradient id="brandMarkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0284c7"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>
          <!-- 硬化合金粗锁梁 (High-Contrast Bold Shackle) - 顶部负空间通透 -->
          <path d="M7 10V6.5C7 3.74 9.24 1.5 12 1.5C14.76 1.5 17 3.74 17 6.5V10" fill="none" stroke="#0284c7" stroke-width="2.6" stroke-linecap="round"/>
          <!-- 工业防撬切角锁身 (Precision Hex Chassis) -->
          <path d="M4 10.5C4 9.67 4.67 9 5.5 9H18.5C19.33 9 20 9.67 20 10.5V19.5C20 20.88 18.88 22 17.5 22H6.5C5.12 22 4 20.88 4 19.5V10.5Z" fill="url(#brandMarkGrad)"/>
          <!-- 极大光学负空间钥匙孔 (High-Visibility Classic Keyhole: Circle + Tapered Slot) 即使在12px下也清晰可辨 -->
          <circle cx="12" cy="14" r="2.2" fill="#ffffff"/>
          <path d="M10.9 14.5L10.2 19H13.8L13.1 14.5Z" fill="#ffffff"/>
        </svg>'''

brand_pat = r'<svg class="brand__mark".*?</svg>'
text = re.sub(brand_pat, new_brand_svg, text, count=1, flags=re.DOTALL)

with open('src/layout.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated src/layout.mjs with Optical-Enhanced High-End Lock icon!")

# 2. 更新 assets/img/favicon.svg
favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="favGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="7" fill="url(#favGrad)"/>
  <!-- Bold Shackle -->
  <path d="M9 13V8.5C9 5 11.8 2.2 16 2.2C20.2 2.2 23 5 23 8.5V13" fill="none" stroke="#ffffff" stroke-width="3.2" stroke-linecap="round"/>
  <!-- Lock Core Keyhole (High Contrast) -->
  <circle cx="16" cy="18.5" r="3" fill="#ffffff"/>
  <path d="M14.6 19.2L13.8 25.5H18.2L17.4 19.2Z" fill="#ffffff"/>
</svg>
'''
with open('assets/img/favicon.svg', 'w', encoding='utf-8') as f:
    f.write(favicon_svg)
print("Updated assets/img/favicon.svg")

# 3. 更新 content/site.json 中的【工程实录 (Field Cases)】图标
# 普通人秒懂：门扇 (Door) + 门把手 (Handle) + 安装维修扳手 (Wrench)
door_wrench_svg = '<svg class="nav__icon" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V3a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v18"/><path d="M12 11h.01"/><path d="m15 15 4.5 4.5a1.5 1.5 0 0 0 2.12-2.12L17.12 13"/><path d="m17 11 2-2"/></svg>'

with open('content/site.json', 'r', encoding='utf-8') as f:
    site = json.load(f)

for lang in ['en', 'zh']:
    for item in site['navigation'][lang]:
        if 'install-gallery.html' in item['href']:
            item['iconSvg'] = door_wrench_svg

with open('content/site.json', 'w', encoding='utf-8') as f:
    json.dump(site, f, ensure_ascii=False, indent=2)

print("Updated content/site.json navigation with Door+Wrench Field Cases icon!")
