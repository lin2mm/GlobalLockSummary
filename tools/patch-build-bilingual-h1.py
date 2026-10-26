# -*- coding: utf-8 -*-
with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 检查 formatBilingualHeading 是否需要引入
if "formatBilingualHeading" not in code:
    code = code.replace(
        "import { renderMarkdown, splitFrontMatter, slugify, escapeHtml } from './src/markdown.mjs';",
        "import { renderMarkdown, splitFrontMatter, slugify, escapeHtml, formatBilingualHeading } from './src/markdown.mjs';"
    )
    print("Imported formatBilingualHeading in build.mjs.")

# 在 buildPages 中，替换自动生成的 <h1>${escapeHtml(title)}</h1>
old_h1_expr = "const bodyHtmlContent = isHomePage ? html : (hasLeadingH1 ? html : `<h1>${escapeHtml(title)}</h1>\\n${html}`);"
new_h1_expr = "const bodyHtmlContent = isHomePage ? html : (hasLeadingH1 ? html : `<h1>${formatBilingualHeading(title)}</h1>\\n${html}`);"

if old_h1_expr in code:
    code = code.replace(old_h1_expr, new_h1_expr)
    print("Replaced bodyHtmlContent h1 with formatBilingualHeading.")
else:
    print("Could not find exact old_h1_expr.")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)

# 并在 src/layout.mjs 中检查 buildToc
with open("src/layout.mjs", "r", encoding="utf-8") as f:
    layout_code = f.read()

# 在 buildToc 中，让 TOC 也支持双行优雅展示
# 原先: .map((h) => `<li class="toc__item toc__item--h${h.level}"><a href="#${h.id}">${esc(h.text)}</a></li>`)
old_toc_item = '.map((h) => `<li class="toc__item toc__item--h${h.level}"><a href="#${h.id}">${esc(h.text)}</a></li>`)'
new_toc_item = '''.map((h) => {
      const match = /^(.*?)\\s*[\\(（]([A-Za-z0-9\\s/&,.:+_-]+)[\\)）]\\s*$/.exec(h.text);
      let label = esc(h.text);
      if (match && /[\\u4e00-\\u9fa5]/.test(match[1]) && /[a-zA-Z]/.test(match[2])) {
        label = `<span class="bilingual-title"><span class="bilingual-title__zh">${esc(match[1].trim())}</span><span class="bilingual-title__en">${esc(match[2].trim())}</span></span>`;
      }
      return `<li class="toc__item toc__item--h${h.level}"><a href="#${h.id}">${label}</a></li>`;
    })'''

if old_toc_item in layout_code:
    layout_code = layout_code.replace(old_toc_item, new_toc_item)
    print("Updated buildToc to format bilingual items in src/layout.mjs.")
    with open("src/layout.mjs", "w", encoding="utf-8") as f:
        f.write(layout_code)

