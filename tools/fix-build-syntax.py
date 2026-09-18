with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("  ]; * GlobalLockSummary build.", "  ];\n}\n\n/**\n * GlobalLockSummary build.")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed build.mjs syntax error!")
