with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("categories/latam.html", "categories/gcc.html")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced categories/latam.html in build.mjs!")
