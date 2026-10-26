import re

# 1. build.mjs: 将分类页锁型卡片双图容器从 #0b1120 替换为极简细线分割 #e2e8f0，内衬统一为冷灰 #f8fafc
with open('build.mjs', 'r', encoding='utf-8') as f:
    bm = f.read()

bm = bm.replace('background: #0b1120; gap: 1px;', 'background: #e2e8f0; gap: 1px;')
bm = bm.replace('height: 160px; background: #0b1120;', 'height: 160px; background: #f8fafc;')
bm = bm.replace('background: #0b1120; color: #f8fafc; padding: 8px 14px;', 'background: #0f172a; color: #f8fafc; padding: 8px 14px;')
bm = bm.replace('background: #0b1120;"', 'background: #f8fafc;"')

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(bm)
print("Cleaned dark containers in build.mjs!")

# 2. field-issues.md: 替换图片深黑背景为浅冷灰
def clean_issues(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
    t = t.replace('background: #0b1120;', 'background: #f8fafc;')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Cleaned {path}!")

clean_issues('content/pages/zh/field-issues.md')
clean_issues('content/pages/en/field-issues.md')

