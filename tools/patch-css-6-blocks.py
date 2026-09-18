with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 升级为 2×3 黄金对称栅格
old_css_5 = """@media (min-width: 1024px) {
  .gallery-portal-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
  }
}"""

new_css_6 = """@media (min-width: 1024px) {
  .gallery-portal-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
}
@media (min-width: 640px) and (max-width: 1023px) {
  .gallery-portal-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }
}"""

if old_css_5 in css:
    css = css.replace(old_css_5, new_css_6)
    print("Replaced 5-col CSS with 2x3 golden matrix!")
else:
    # 替换其他 repeat(5, 1fr)
    css = css.replace("grid-template-columns: repeat(5, 1fr);", "grid-template-columns: repeat(3, 1fr);")
    print("Replaced repeat(5, 1fr) in site.css!")

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)
