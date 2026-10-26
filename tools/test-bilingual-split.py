import re

test_cases = [
    "后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)",
    "1. 锁芯夹持背板 (Mounting Plate Clamping)",
    "2. 常插钥匙抓取与槽位浮动 (Key Gripper & Floating Coupler)",
    "3. 手动优先与脱开离合器 (Manual Override Clutch)",
    "4. 美标死锁尾轴适配器 (ANSI Deadbolt Wing Latches)",
    "5. 出海 FTO 防侵权自查清单 (Patent Clearance Checklist)",
    "全球机械门锁开放知识库与实物图谱",
    "Retrofit Smart Lock Patent Avoidance & FTO Guide",
    "欧标槽型双锁芯：Euro 30/30",
    "全球智能锁 Retrofit 标准转接件 BOM (Hardware Adapters)"
]

pattern = r'^(.*?)\s*[\(（]([A-Za-z0-9\s/&,.:+_-]+)[\)）]\s*$'

for text in test_cases:
    m = re.match(pattern, text)
    if m and re.search(r'[\u4e00-\u9fa5]', m.group(1)) and re.search(r'[a-zA-Z]', m.group(2)):
        print(f"SPLIT SUCCESS:")
        print(f"  Orig:  {text}")
        print(f"  Line1: {m.group(1).strip()}")
        print(f"  Line2: {m.group(2).strip()}")
    else:
        print(f"NO SPLIT: {text}")
