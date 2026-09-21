# -*- coding: utf-8 -*-
import re

# 1. 扩展 assets/css/site.css
css_addition = """
/* ==========================================================================
   Bilingual Title Split System (Dual-Line Typographic Hierarchy)
   ========================================================================== */
.bilingual-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.bilingual-title__zh {
  display: block;
  font-weight: inherit;
  color: inherit;
  line-height: 1.25;
}
.bilingual-title__en {
  display: block;
  font-size: 0.62em;
  font-weight: 500;
  letter-spacing: 0.02em;
  color: #64748b;
  line-height: 1.3;
}
h1 .bilingual-title__en {
  font-size: 0.58em;
  margin-top: 2px;
}
h2 .bilingual-title__en {
  font-size: 0.64em;
  margin-top: 2px;
}
h3 .bilingual-title__en {
  font-size: 0.68em;
  margin-top: 1px;
}
.toc__item .bilingual-title__en {
  font-size: 0.8em;
  color: #94a3b8;
}
"""

with open("assets/css/site.css", "r", encoding="utf-8") as f:
    css = f.read()

if "bilingual-title" not in css:
    css += "\n" + css_addition
    with open("assets/css/site.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("Injected .bilingual-title styles into assets/css/site.css.")
else:
    print(".bilingual-title styles already in assets/css/site.css.")

# 2. 修改 src/markdown.mjs 中的 formatHeadingText / inline / heading 渲染
with open("src/markdown.mjs", "r", encoding="utf-8") as f:
    md_code = f.read()

helper_code = """
/**
 * Format bilingual headings: if heading has Chinese and English in parentheses,
 * split into a dual-line presentation with subtle English subtitle.
 */
export function formatBilingualHeading(text) {
  const match = /^(.*?)\\s*[\\(（]([A-Za-z0-9\\s/&,.:+_-]+)[\\)）]\\s*$/.exec(text);
  if (match && /[\\u4e00-\\u9fa5]/.test(match[1]) && /[a-zA-Z]/.test(match[2])) {
    const zh = match[1].trim();
    const en = match[2].trim();
    return `<span class="bilingual-title"><span class="bilingual-title__zh">${inline(zh)}</span><span class="bilingual-title__en">${escapeHtml(en)}</span></span>`;
  }
  return inline(text);
}
"""

if "function formatBilingualHeading" not in md_code:
    # 插入在 inline 函数下方
    idx = md_code.find("function inline(text) {")
    end_inline_idx = md_code.find("return text;\n}", idx)
    if end_inline_idx != -1:
        insert_pos = end_inline_idx + len("return text;\n}")
        md_code = md_code[:insert_pos] + "\n" + helper_code + md_code[insert_pos:]
        print("Inserted formatBilingualHeading into src/markdown.mjs.")

# 在 renderMarkdown 中，替换 headings 渲染:
# 原先: out.push(`<h${level} id="${id}">${inline(text)}</h${level}>`);
old_h_render = 'out.push(`<h${level} id="${id}">${inline(text)}</h${level}>`);'
new_h_render = 'out.push(`<h${level} id="${id}">${formatBilingualHeading(text)}</h${level}>`);'

if old_h_render in md_code:
    md_code = md_code.replace(old_h_render, new_h_render)
    print("Replaced heading renderer with formatBilingualHeading in src/markdown.mjs.")

with open("src/markdown.mjs", "w", encoding="utf-8") as f:
    f.write(md_code)

