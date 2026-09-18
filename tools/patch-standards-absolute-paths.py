# 统一将 content/pages/zh/indigenous-guides.md 与 en/indigenous-guides.md 中的 src="../assets/ 替换为 src="/assets/
for lang in ['zh', 'en']:
    path = f'content/pages/{lang}/indigenous-guides.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace('src="../assets/', 'src="/assets/')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Updated indigenous-guides.md image paths to root-relative /assets/!")
