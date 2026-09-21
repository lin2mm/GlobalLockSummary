with open('content/pages/zh/field-issues.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 替换 Grid 规则为 3 列黄金阵列
old_grid = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin: 28px 0;">'
new_grid = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 16px 0 24px;">'

zh = zh.replace(old_grid, new_grid)

# 将卡片图片高度从 155px 调整为 140px，让 2 行在首屏一览无余
zh = zh.replace('height: 155px;', 'height: 140px;')
# 消除红色刺眼胶囊，采用 ASSA ABLOY 单色墨黑徽章
zh = zh.replace('background: #dc2626;', 'background: #0f172a;')
zh = zh.replace('background: #ea580c;', 'background: #0f172a;')

with open('content/pages/zh/field-issues.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Updated zh/field-issues.md to 3x2 grid!")

with open('content/pages/en/field-issues.md', 'r', encoding='utf-8') as f:
    en = f.read()

en = en.replace(old_grid, new_grid)
en = en.replace('height: 155px;', 'height: 140px;')
en = en.replace('background: #dc2626;', 'background: #0f172a;')
en = en.replace('background: #ea580c;', 'background: #0f172a;')

with open('content/pages/en/field-issues.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Updated en/field-issues.md to 3x2 grid!")

