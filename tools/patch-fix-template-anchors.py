with open('content/pages/zh/drilling-templates.md', 'r', encoding='utf-8') as f:
    zh = f.read()

zh = zh.replace('## 1. 北美 ANSI A156.36 呆锁开孔打样规程', '<h2 id="tpl-us-ansi-deadbolt">1. 北美 ANSI A156.36 呆锁开孔打样规程</h2>')
zh = zh.replace('## 2. 日本 JIS A5511 切欠打样规程', '<h2 id="tpl-jp-miwa-la">2. 日本 JIS A5511 切欠打样规程</h2>')
zh = zh.replace('## 3. 欧标 DIN 18251 锁体与双锁芯开孔打样规程', '<h2 id="tpl-eu-din-18251">3. 欧标 DIN 18251 锁体与双锁芯开孔打样规程</h2>')

with open('content/pages/zh/drilling-templates.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Added anchors to zh/drilling-templates.md!")

with open('content/pages/en/drilling-templates.md', 'r', encoding='utf-8') as f:
    en = f.read()

en = en.replace('## 1. North America ANSI A156.36 Deadbolt Drilling Guidelines', '<h2 id="tpl-us-ansi-deadbolt">1. North America ANSI A156.36 Deadbolt Drilling Guidelines</h2>')
en = en.replace('## 2. Japan JIS A5511 MIWA LA Cutout Guidelines', '<h2 id="tpl-jp-miwa-la">2. Japan JIS A5511 MIWA LA Cutout Guidelines</h2>')
en = en.replace('## 3. Euro DIN 18251 Mortise & Profile Cylinder Guidelines', '<h2 id="tpl-eu-din-18251">3. Euro DIN 18251 Mortise & Profile Cylinder Guidelines</h2>')

with open('content/pages/en/drilling-templates.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Added anchors to en/drilling-templates.md!")

