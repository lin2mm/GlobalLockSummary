with open("_site/zh/patent-avoidance.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
bilingual_matches = re.findall(r'<span class="bilingual-title">[\s\S]*?</span>\s*</span>', html)
print(f"Total bilingual-title rendered in zh/patent-avoidance.html: {len(bilingual_matches)}")

for i, m in enumerate(bilingual_matches[:5]):
    # 清理多余空格
    clean = " ".join(m.split())
    print(f" {i+1}: {clean}")
