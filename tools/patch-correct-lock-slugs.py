def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
    t = t.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)

for p in ['content/pages/zh/adapters.md', 'content/pages/en/adapters.md', 'content/pages/zh/field-issues.md', 'content/pages/en/field-issues.md']:
    replace_in_file(p, 'us-single-cylinder-deadbolt.html', 'us-deadbolt.html')
    replace_in_file(p, 'bricard-bloctout.html', 'euro-cylinder-mortise.html')
    replace_in_file(p, 'lockwood-001.html', 'au-deadlatch.html')

print("Corrected slugs to exact 15 lock families!")
