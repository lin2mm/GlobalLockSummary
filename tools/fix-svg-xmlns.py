import os
from pathlib import Path

diagrams_dir = Path("assets/img/diagrams")
svg_files = list(diagrams_dir.glob("*.svg"))
fixed_count = 0

for svg_path in svg_files:
    text = svg_path.read_text(encoding="utf-8")
    if 'xmlns="http://www.w3.org/2000/svg"' not in text:
        # 在 <svg 后面补上 xmlns
        text = text.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        svg_path.write_text(text, encoding="utf-8")
        fixed_count += 1

print(f"Fixed xmlns attribute in {fixed_count} SVG diagram files!")
