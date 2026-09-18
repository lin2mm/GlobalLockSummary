import re
import os
import shutil

# 1. 从 content/pages/zh/data-hub.md 彻底移除下载表格
with open('content/pages/zh/data-hub.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 移除我们之前添加的 "Direct Download Hub" 段落
zh = re.sub(r'## 📦 长期沉淀工程资产与方法论直接下载 \(Direct Download Hub\).*?(?=##|\Z)', '', zh, flags=re.DOTALL)
with open('content/pages/zh/data-hub.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Removed Direct Download Hub from zh/data-hub.md")

# 2. 从 content/pages/en/data-hub.md 彻底移除下载表格
with open('content/pages/en/data-hub.md', 'r', encoding='utf-8') as f:
    en = f.read()

en = re.sub(r'## 📦 Direct Engineering Assets & Methodology Download Hub.*?(?=##|\Z)', '', en, flags=re.DOTALL)
with open('content/pages/en/data-hub.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Removed Direct Download Hub from en/data-hub.md")

# 3. 删除 assets/downloads 目录
if os.path.exists('assets/downloads'):
    shutil.rmtree('assets/downloads')
    print("Deleted assets/downloads directory")

