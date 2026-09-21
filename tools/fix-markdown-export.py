with open("src/markdown.mjs", "r", encoding="utf-8") as f:
    code = f.read()

helper = """
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

if "export function formatBilingualHeading" not in code:
    code = helper + "\n" + code
    with open("src/markdown.mjs", "w", encoding="utf-8") as f:
        f.write(code)
    print("Prepend formatBilingualHeading to src/markdown.mjs.")
