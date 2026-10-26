import re

# 1. 统一 Favicon 和 Header Logo 为 ASSA ABLOY Deep Blue (#0B1D47) 与 精密墨黑
favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0B1D47"/>
  <!-- Precision Shackle in pure white -->
  <path d="M10 13V8.5C10 5.2 12.7 2.5 16 2.5C19.3 2.5 22 5.2 22 8.5V13" fill="none" stroke="#ffffff" stroke-width="2.8" stroke-linecap="round"/>
  <!-- High Precision Keyhole -->
  <circle cx="16" cy="18.5" r="2.6" fill="#ffffff"/>
  <path d="M14.7 19.5L14 25H18L17.3 19.5Z" fill="#ffffff"/>
</svg>"""

with open('assets/img/favicon.svg', 'w', encoding='utf-8') as f:
    f.write(favicon_svg)
print("Updated favicon.svg to ASSA ABLOY Deep Blue #0B1D47!")

# 2. 修改 assets/css/site.css
with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 将 --accent 升级为 ASSA ABLOY 工业权威色 Deep Blue
css = css.replace("--accent: #0b5fff;", "--accent: #0B1D47;")
# 品牌 logo 图标
css = css.replace(".brand__mark { width: 1.5rem; height: 1.5rem; color: var(--accent); flex: none; }",
                  ".brand__mark { width: 1.5rem; height: 1.5rem; color: #0B1D47; flex: none; }")

# 导航激活态：由大块浅灰底色变为 ASSA ABLOY 极简工业细线/纯净通透状态
old_nav_css = """.nav-link[aria-current="page"] {
  background: var(--bg-inset);
  color: var(--fg);
  font-weight: 600;
}"""
new_nav_css = """.nav-link[aria-current="page"] {
  background: transparent;
  color: #0B1D47;
  font-weight: 700;
  border-bottom: 2px solid #0B1D47;
  border-radius: 0;
}"""
if old_nav_css in css:
    css = css.replace(old_nav_css, new_nav_css)
    print("Updated nav active state to ASSA ABLOY bottom border indicator!")
else:
    print("old_nav_css pattern not matched directly, appending targeted rule...")
    css += "\n.nav-link[aria-current='page'] { background: transparent !important; color: #0B1D47 !important; font-weight: 700 !important; border-bottom: 2px solid #0B1D47 !important; border-radius: 0 !important; }\n"

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. 修复 install-gallery.html 底部蓝色粗大按钮与本区域图库按钮
with open('build.mjs', 'r', encoding='utf-8') as f:
    bm = f.read()

old_action_buttons = """          <div style="display: flex; gap: 8px;">
            <a class="block-hero__btn" style="flex: 1; text-align: center; font-size: 0.82rem; font-weight: 700; padding: 8px 12px; background: #0284c7 !important; color: #ffffff !important; border: 1px solid #0284c7; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px;" href="${lockLink}">
              🔍 ${isZh ? '进入所属锁型详情 →' : 'View Lock Details →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff !important; border: 1.5px solid #0284c7; color: #0284c7 !important; font-size: 0.82rem; font-weight: 700; padding: 8px 12px; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              🖼️ ${isZh ? '本区域图库' : 'Regional Gallery'}
            </a>
          </div>"""

new_action_buttons = """          <div style="display: flex; gap: 8px;">
            <a style="flex: 1; text-align: center; font-size: 0.8rem; font-weight: 600; padding: 7px 12px; background: #0f172a; color: #ffffff; border: 1px solid #0f172a; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px;" href="${lockLink}">
              ${isZh ? '所属锁型详情 →' : 'Lock Details →'}
            </a>
            <a style="background: #f8fafc; border: 1px solid #cbd5e1; color: #334155; font-size: 0.8rem; font-weight: 600; padding: 7px 12px; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              ${isZh ? '分类图谱' : 'Gallery'}
            </a>
          </div>"""

if old_action_buttons in bm:
    bm = bm.replace(old_action_buttons, new_action_buttons)
    print("Updated install-gallery buttons to ASSA ABLOY sleek dark grey style!")
else:
    print("old_action_buttons not found in build.mjs")

# 统一工程关键指标小图标，去掉刺眼的彩色齿轮/亮条
bm = bm.replace('⚙️ <b>${isZh ? \'工程关键指标:\' : \'Key Metrics:\'}</b>', '<b>${isZh ? \'⌖ 关键指标:\' : \'Key Metrics:\'}</b>')
bm = bm.replace('border-left: 3px solid #0284c7;', 'border-left: 3px solid #0f172a;')

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(bm)

# 4. 修复 adapters.md 中的高亮绿标与徽章重叠、截断与蓝框问题
def clean_adapters_page(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    t = re.sub(
        r'<div style="position: absolute; top: 8px; left: 8px; display: flex; gap: 5px;">\s*<span style="background: #0284c7; color: #fff;[^"]*">(ADP-\d+) · 核实件</span>\s*<span style="background: #16a34a;[^"]*">✓ 100% 实物核实</span>\s*</div>',
        r'<div style="position: absolute; top: 8px; left: 8px; background: rgba(15,23,42,0.9); color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">\1 · 100% Verified</div>',
        t
    )
    t = re.sub(
        r'<div style="position: absolute; top: 8px; left: 8px; display: flex; gap: 5px;">\s*<span style="background: #0284c7; color: #fff;[^"]*">(ADP-\d+) · Verified</span>\s*<span style="background: #16a34a;[^"]*">✓ 100% Verified</span>\s*</div>',
        r'<div style="position: absolute; top: 8px; left: 8px; background: rgba(15,23,42,0.9); color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">\1 · 100% Verified</div>',
        t
    )

    t = t.replace('border: 1.5px solid #0284c7; border-left: 4px solid #0284c7;', 'border: 1px solid #e2e8f0; border-left: 3px solid #0f172a;')
    t = t.replace('border: 1.5px solid #0284c7;', 'border: 1px solid #e2e8f0;')
    t = t.replace('box-shadow: 0 4px 12px rgba(2,132,199,0.06);', 'box-shadow: 0 2px 6px rgba(0,0,0,0.03);')
    t = t.replace('border-left: 3px solid #0284c7;', 'border-left: 3px solid #0f172a;')

    t = t.replace('<span style="color: #15803d; font-weight: 600;">100% Verified', '<span style="color: #475569; font-weight: 600;">Verified')
    t = t.replace('<span style="color: #15803d; font-weight: 600;">✓ 100% 实物核实', '<span style="color: #475569; font-weight: 600;">✓ Verified')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Cleaned {path}!")

clean_adapters_page('content/pages/zh/adapters.md')
clean_adapters_page('content/pages/en/adapters.md')

