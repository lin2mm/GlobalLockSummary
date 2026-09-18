with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

old_landing_form = '<form id="site-feedback-form"'
strip_html = """<div class="data-hub-strip" style="margin: 28px 0 20px; padding: 14px 20px; background: #f8fafc; border: 1.5px solid #0284c7; border-left: 5px solid #0284c7; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; box-shadow: 0 2px 8px rgba(2,132,199,0.06);">
    <div style="font-size: 0.88rem; color: #1e293b;">
      <b style="color: #0284c7;">📊 ${isZh ? '出海工程数据与 API 枢纽' : 'Hardware Data & Lead API Hub'}:</b> 
      ${isZh ? '查阅全球 6 大板块 72 款机械锁精密公差、堵转模型、减速比与 12 款核实 BOM 矩阵。' : 'Access tolerances, stall models, and 12 verified BOM adapters across 6 global divisions.'}
    </div>
    <a href="${isZh ? '/zh/data-hub.html' : '/en/data-hub.html'}" style="padding: 6px 14px; background: #0284c7; color: #fff; font-size: 0.82rem; font-weight: 700; text-decoration: none; border-radius: 4px; white-space: nowrap;">
      ${isZh ? '进入工程数据中心 (Data Hub) →' : 'Enter Data Hub →'}
    </a>
  </div>
  <form id="site-feedback-form" """

if old_landing_form in text:
    text = text.replace(old_landing_form, strip_html, 1)
    print("Injected data-hub-strip above feedback form in build.mjs!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

