import re

with open("content/pages/zh/field-issues.md") as f:
    text = f.read()

matches = re.findall(r'<a href="([^"]+)"', text)
print("ZH field-issues links:", len(matches), matches)

with open("content/pages/en/field-issues.md") as f:
    text_en = f.read()

matches_en = re.findall(r'<a href="([^"]+)"', text_en)
print("EN field-issues links:", len(matches_en), matches_en)
