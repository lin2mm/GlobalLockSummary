with open('content/pages/zh/adapters.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 1. 消除 Nuki-type，统一规范为 后装智能锁
zh = zh.replace("Nuki-type 加装智能锁", "后装智能锁（免换锁 / 租客无损加装）")

# 2. 彻底移除绿色冗长文本框：
# <div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; ...
import re
zh = re.sub(r'<!-- 转接件全量工程核实清单 -->\s*<div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4;.*?</div>', '', zh, flags=re.DOTALL)
zh = re.sub(r'<div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4;.*?</div>', '', zh, flags=re.DOTALL)

with open('content/pages/zh/adapters.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Updated content/pages/zh/adapters.md!")

# 同样排查英文版
with open('content/pages/en/adapters.md', 'r', encoding='utf-8') as f:
    en = f.read()

en = en.replace("Nuki-type", "Retrofit Smart Lock")
en = re.sub(r'<div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4;.*?</div>', '', en, flags=re.DOTALL)

with open('content/pages/en/adapters.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Updated content/pages/en/adapters.md!")

