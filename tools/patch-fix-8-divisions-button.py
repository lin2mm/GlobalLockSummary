with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

target = "← ${isZh ? '返回全球 5 大板块' : 'Back to 5 Major Divisions'}"
replacement = "← ${isZh ? '返回全球 8 大板块' : 'Back to 8 Major Divisions'}"

if target in code:
    code = code.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully replaced with 8 Major Divisions!")
else:
    print("Target not found!")

