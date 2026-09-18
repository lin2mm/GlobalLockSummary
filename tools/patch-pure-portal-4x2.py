with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 彻底修复 .gallery-wall--pure-portal .gallery-portal-grid
old_snippet = """.gallery-wall--pure-portal .gallery-portal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.75rem;
  margin: 1rem 0;
}

@media (min-width: 1100px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 1.25rem;
  }
}"""

new_snippet = """.gallery-wall--pure-portal .gallery-portal-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 1.25rem;
  margin: 1rem 0;
}

@media (min-width: 1100px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1.25rem;
  }
}
@media (min-width: 640px) and (max-width: 1099px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1.15rem;
  }
}
@media (max-width: 639px) {
  .gallery-wall--pure-portal .gallery-portal-grid {
    grid-template-columns: 1fr !important;
    gap: 1rem;
  }
}"""

if old_snippet in css:
    css = css.replace(old_snippet, new_snippet)
    print("Replaced pure-portal CSS directly!")
else:
    # 查找并替换
    css = css.replace("grid-template-columns: repeat(5, 1fr);", "grid-template-columns: repeat(4, 1fr) !important;")
    print("Replaced repeat(5, 1fr) with repeat(4, 1fr)!")

with open('assets/css/site.css', 'w', encoding='utf-8') as f:
    f.write(css)

