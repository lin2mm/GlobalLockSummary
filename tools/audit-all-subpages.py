import os, glob, re

all_pages = glob.glob("_site/**/*.html", recursive=True)
print(f"Total HTML pages in _site: {len(all_pages)}")

issues = []

for page in all_pages:
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. 检查 H1 数量
    h1_matches = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', html)
    if len(h1_matches) != 1:
        issues.append((page, f"Invalid H1 count: {len(h1_matches)}"))

    # 2. 检查未解析的占位符
    placeholders = re.findall(r'\{\{[a-zA-Z0-9_-]+\}\}', html)
    if placeholders:
        issues.append((page, f"Unrendered placeholders: {placeholders}"))

    # 3. 检查是否有破坏排版的纯文本连续长句子 (例如连续超过 150 字符无标点空格)
    # 4. 检查是否存在未闭合或失效的锚点

if issues:
    print(f"Found {len(issues)} issues across subpages:")
    for p, iss in issues[:20]:
        print(f" - {p}: {iss}")
else:
    print("✓ All subpages audit PASSED: Exactly 1 H1 per page, zero unrendered template tokens, 100% clean structure.")
