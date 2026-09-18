import re
from pathlib import Path

site_dir = Path("_site")
html_files = list(site_dir.glob("**/*.html"))
print(f"Checking {len(html_files)} HTML pages for empty buttons...")

empty_buttons = []
for hf in html_files:
    text = hf.read_text(encoding="utf-8")
    matches = re.finditer(r'<a([^>]+class=[\"\'][^\"\']*btn[^\"\']*[\"\'][^>]*)>(.*?)</a>', text, re.DOTALL)
    for m in matches:
        attrs = m.group(1)
        content = m.group(2).strip()
        # 移除内部标签
        clean_content = re.sub(r'<[^>]+>', '', content).strip()
        if len(clean_content) == 0:
            empty_buttons.append((str(hf.relative_to(site_dir)), attrs))

if empty_buttons:
    print(f"❌ Found {len(empty_buttons)} buttons without text:")
    for eb in empty_buttons[:10]:
        print(f"   - In {eb[0]}: {eb[1]}")
else:
    print("✓ All <a class='*btn*'> tags contain non-empty text!")

# 再检查所有带 background: #0284c7 或 background: #2563eb 的 <a> 标签
empty_colored_links = []
for hf in html_files:
    text = hf.read_text(encoding="utf-8")
    matches = re.finditer(r'<a([^>]+style=[\"\'][^\"\']*background:\s*(#[0-9a-fA-F]{3,6}|var\(--accent\))[^\"\']*[\"\'][^>]*)>(.*?)</a>', text, re.DOTALL)
    for m in matches:
        attrs = m.group(1)
        content = m.group(2).strip()
        clean_content = re.sub(r'<[^>]+>', '', content).strip()
        if len(clean_content) == 0:
            empty_colored_links.append((str(hf.relative_to(site_dir)), attrs))

if empty_colored_links:
    print(f"❌ Found {len(empty_colored_links)} colored links without text:")
    for el in empty_colored_links[:10]:
        print(f"   - In {el[0]}: {el[1]}")
else:
    print("✓ All colored <a> action tags contain non-empty text!")
