with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 替换 sampleCards 中 header 的 h4 为 h3
old_h4_snippet = """        <div class="lock-detail-sample__header">
          <span class="lock-detail-sample__id">${escapeHtml(s.id)}</span>
          <h4>${escapeHtml(sTitle)}</h4>
          <span class="gallery-card__status ${s.status === 'R1' ? 'gallery-card__status--r1' : 'gallery-card__status--r0'}">${escapeHtml(s.status || 'R0')}</span>
        </div>"""

new_h3_snippet = """        <div class="lock-detail-sample__header">
          <span class="lock-detail-sample__id">${escapeHtml(s.id)}</span>
          <h3 style="margin: 0; font-size: 1.12rem; font-weight: 700; color: #0f172a; display: inline-flex; align-items: center; gap: 8px;">
            ${escapeHtml(sTitle)}
          </h3>
          <span class="gallery-card__status ${s.status === 'R1' ? 'gallery-card__status--r1' : 'gallery-card__status--r0'}">${escapeHtml(s.status || 'R0')}</span>
        </div>"""

if old_h4_snippet in code:
    code = code.replace(old_h4_snippet, new_h3_snippet)
    print("Replaced h4 with semantic h3 in lock-detail-sample__header")
else:
    print("Could not find exact old_h4_snippet in build.mjs, checking variants...")
    import re
    code = re.sub(
        r'<div class="lock-detail-sample__header">\s*<span class="lock-detail-sample__id">\$\{escapeHtml\(s\.id\)\}</span>\s*<h4>\$\{escapeHtml\(sTitle\)\}</h4>\s*<span class="gallery-card__status',
        r'<div class="lock-detail-sample__header">\n          <span class="lock-detail-sample__id">${escapeHtml(s.id)}</span>\n          <h3 style="margin: 0; font-size: 1.12rem; font-weight: 700; color: #0f172a;">${escapeHtml(sTitle)}</h3>\n          <span class="gallery-card__status',
        code
    )
    print("Regex replaced h4 with h3.")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)

