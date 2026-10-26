import re

files = [
    'docs/00_AUTONOMOUS_OPTIMIZATION_LOOP.md',
    'docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md'
]

for p in files:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace("返回全球 5 大板块", "返回全球 8 大板块")
        c = c.replace("全球 5 大板块", "全球 8 大工业板块")
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated {p}")
    except Exception as e:
        print(f"Error updating {p}: {e}")

