with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 升级为 4 列 × 2 行 黄金对称栅格
old_css = """@media (min-width: 1024px) {
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

new_css = """@media (min-width: 1200px) {
  .gallery-portal-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
  }
}
@media (min-width: 768px) and (max-width: 1199px) {
  .gallery-portal-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }
}
@media (max-width: 767px) {
  .gallery-portal-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}"""

if old_css in css:
    css = css.replace(old_css, new_css)
    print("Replaced CSS with 4x2 golden 8-block matrix!")
else:
    css = css.replace("grid-template-columns: repeat(3, 1fr);", "grid-template-columns: repeat(4, 1fr);")
    print("Replaced repeat(3, 1fr) with repeat(4, 1fr) in site.css!")

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)

