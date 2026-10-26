with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

old_logic = "const bodyHtmlContent = isHomePage ? html : `<h1>${escapeHtml(title)}</h1>\\n${html}`;"
new_logic = """const hasLeadingH1 = html.trim().startsWith('<h1') || html.includes('<h1');
      const bodyHtmlContent = isHomePage ? html : (hasLeadingH1 ? html : `<h1>${escapeHtml(title)}</h1>\\n${html}`);"""

if old_logic in code:
    code = code.replace(old_logic, new_logic)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully patched build.mjs to avoid duplicate H1!")
else:
    print("Pattern old_logic not found or already patched!")

