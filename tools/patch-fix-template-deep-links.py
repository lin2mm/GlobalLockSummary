with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

old_actions = """          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" style="background: #0f172a; color: #fff; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${heroHref}">
              ${isZh ? '实物拆解与工程规范 →' : 'Specifications & Blueprint →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${isZh ? '/zh/drilling-templates.html' : '/en/drilling-templates.html'}">
              📐 ${isZh ? '1:1 开孔图谱' : '1:1 Template'}
            </a>
          </div>"""

new_actions = """          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" style="background: #0f172a; color: #fff; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${heroHref}">
              ${isZh ? '实物拆解与工程规范 →' : 'Specifications & Blueprint →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${isZh ? (block.code === 'jp-kr' ? '/zh/drilling-templates.html#tpl-jp-miwa-la' : (block.code === 'europe5' ? '/zh/drilling-templates.html#tpl-eu-din-18251' : '/zh/drilling-templates.html#tpl-us-ansi-deadbolt')) : (block.code === 'jp-kr' ? '/en/drilling-templates.html#tpl-jp-miwa-la' : (block.code === 'europe5' ? '/en/drilling-templates.html#tpl-eu-din-18251' : '/en/drilling-templates.html#tpl-us-ansi-deadbolt'))}">
              📐 ${isZh ? '1:1 开孔图谱' : '1:1 Template'}
            </a>
          </div>"""

if old_actions in code:
    code = code.replace(old_actions, new_actions)
    print("Fixed template deep links to point to exact national blueprint!")
else:
    print("old_actions not found in build.mjs")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

