with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 升级输入框占位符：采用专业工整的双模输入指引（既懂工程师需求，又亲和买家）
old_placeholder = 'placeholder="${lang === \'zh\' ? \'输入您的锁型需求或改装建议（支持直接输入，站内直达）...\' : \'Type your suggestion or missing lock model...\'}"'
new_placeholder = 'placeholder="${lang === \'zh\' ? \'输入你的锁型需求，或者对网站的调整建议（直通研发工程师）...\' : \'Enter your lock model requirement, or website suggestions for our R&D engineers...\'}"'

if old_placeholder in text:
    text = text.replace(old_placeholder, new_placeholder)
    print("Updated layout.mjs placeholder successfully!")
else:
    print("Old placeholder not matched exactly, checking pattern...")

with open('src/layout.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

