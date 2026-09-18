with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 替换 jp-kr 的 hero.image 为真实门体安装的 hero-jp-miwa-door.jpg
old_str = "image: '/assets/img/indigenous/jp-miwa-13la.jpg',"
new_str = "image: '/assets/img/hero/hero-jp-miwa-door.jpg',"

if old_str in code:
    code = code.replace(old_str, new_str)
    print("Replaced JP hero image with authentic installed door photo /assets/img/hero/hero-jp-miwa-door.jpg!")
else:
    print("old_str not found in build.mjs")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

