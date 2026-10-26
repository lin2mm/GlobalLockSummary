with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 替换 install-gallery 中的按钮样式，强制赋予高对比高亮与醒目图标
old_btn = """            <a class="block-hero__btn" style="flex: 1; text-align: center; font-size: 0.8rem; padding: 6px 10px;" href="${lockLink}">
              ${isZh ? '进入所属锁型详情 →' : 'View Lock Details →'}
            </a>
            <a class="block-hero__btn" style="background: transparent; border: 1px solid #cbd5e1; color: #1e293b; font-size: 0.8rem; padding: 6px 10px;" href="${catLink}">
              ${isZh ? '本区域图库' : 'Regional Gallery'}
            </a>"""

new_btn = """            <a class="block-hero__btn" style="flex: 1; text-align: center; font-size: 0.82rem; font-weight: 700; padding: 8px 12px; background: #0284c7 !important; color: #ffffff !important; border: 1px solid #0284c7; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px;" href="${lockLink}">
              🔍 ${isZh ? '进入所属锁型详情 →' : 'View Lock Details →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff !important; border: 1.5px solid #0284c7; color: #0284c7 !important; font-size: 0.82rem; font-weight: 700; padding: 8px 12px; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              🖼️ ${isZh ? '本区域图库' : 'Regional Gallery'}
            </a>"""

if old_btn in text:
    text = text.replace(old_btn, new_btn)
    print("Upgraded install-gallery button contrast & text styling!")
else:
    print("old_btn not found directly, checking variations...")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

