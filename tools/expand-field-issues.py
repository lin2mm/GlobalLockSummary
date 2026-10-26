import json

# 1. 扩充 content/catalog/field-issues.json
with open('content/catalog/field-issues.json', 'r', encoding='utf-8') as f:
    issues = json.load(f)

new_issues = [
    {
        "source": "Mercosul Locksmith Group & LATAM Field Ops Log",
        "date": "2026-08",
        "brand": "Smart Retrofit Locks on Narrow Stile Doors",
        "market": "Latin America (Brazil / Argentina / Chile)",
        "lockType": "ABNT NBR 14913 Narrow Mortise (30-35mm Hollow Door)",
        "symptom": "Door skin crushes inward during screw tightening; deadbolt binds against mortise side wall",
        "rootCause": "LATAM timber doors commonly have hollow or semi-solid cores with skin thickness only 3mm. Tightening M5 mounting bolts beyond 2.0 N·m collapses door skin, distorting the lock pocket.",
        "mechanicalFailureMode": "Door surface indentation, latch linkage misalignment, permanent exterior panel slant",
        "engineeringRecommendation": "Enforce maximum 1.8 N·m fastener torque spec; provide oversized reinforcement load-spreading plates."
    },
    {
        "source": "GCC Smart Home Warranty Claim #KSA-49102",
        "date": "2026-07",
        "brand": "Direct-Drive Deadbolt Motors",
        "market": "Middle East Gulf (UAE / Saudi Arabia / Qatar)",
        "lockType": "Heavy Steel Security Door / SASO 2063",
        "symptom": "Smart lock operates smoothly at night but consistently errors out ('Motor Stalled') between 11:00 AM and 4:00 PM",
        "rootCause": "Extreme solar radiation (>65°C surface temp) causes heavy steel door leaf and perimeter frame to undergo differential thermal expansion. Lock clearance collapses from 3.5mm to <0.8mm, binding the latch.",
        "mechanicalFailureMode": "Thermal expansion deadbolt seizure; motor overcurrent cutoff under friction load >3.8 N·m",
        "engineeringRecommendation": "Require 5.0mm minimum seasonal clearance buffer in Gulf installations; configure motor peak boost torque profile."
    }
]

# 避免重复追加
existing_sources = [x.get('source') for x in issues]
for ni in new_issues:
    if ni['source'] not in existing_sources:
        issues.append(ni)

with open('content/catalog/field-issues.json', 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)
print(f"Updated field-issues.json! Total cases: {len(issues)}")

# 2. 扩充 content/pages/zh/field-issues.md
zh_card_7 = """  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
    <div style="height: 200px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="/assets/img/pitfalls/latam-hollow-door-crush.jpg" alt="拉美中空薄门压溃与锁体形变" style="width: 100%; height: 100%; object-fit: cover;" />
      <span style="position: absolute; top: 8px; left: 8px; background: #ea580c; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">FL-07 · 门皮压溃</span>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">拉美 (ABNT)</span>
    </div>
    <div style="padding: 16px;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem;">拉美 30mm 中空薄门拧紧螺栓导致门皮塌陷与锁舌卡滞</h3>
      <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 10px;">巴西/阿根廷大量 30-35mm 中空木门门皮仅 3mm。安装螺栓扭矩 >2.0 N·m 时门板向内凹陷，导致内部立柱锁盒严重扭曲偏心，锁舌卡死无法弹出。</p>
      <div style="background: #fff7ed; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #9a3412; border-left: 3px solid #ea580c;">
        <b>避坑准则:</b> 严格限制螺钉拧紧扭力 ≤1.8 N·m，包装标配内外加固大分压板（Reinforcement Escutcheon Plate）。
      </div>
    </div>
  </div>

  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
    <div style="height: 200px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="/assets/img/pitfalls/gcc-thermal-expansion-jam.jpg" alt="中东极端高温门体热膨胀咬死" style="width: 100%; height: 100%; object-fit: cover;" />
      <span style="position: absolute; top: 8px; left: 8px; background: #dc2626; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">FL-08 · 热胀咬死</span>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">中东 (GCC/SASO)</span>
    </div>
    <div style="padding: 16px;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem;">中东海湾地区极端烈日暴晒导致金属门热胀冷缩卡死</h3>
      <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 10px;">沙特/阿联酋室外地表在正午暴晒下超过 65°C。厚重装甲钢门热膨胀导致 3.5mm 门缝极限缩减至 <0.8mm，锁舌被门框锁孔死死夹住，电机过载堵转报错。</p>
      <div style="background: #fef2f2; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #991b1b; border-left: 3px solid #dc2626;">
        <b>避坑准则:</b> 中东入户门安装强制要求预留 ≥5.0mm 门缝余量；电机固件引入正午大扭矩爬坡防堵转算法。
      </div>
    </div>
  </div>
"""

with open('content/pages/zh/field-issues.md', 'r', encoding='utf-8') as f:
    zh_content = f.read()

if 'FL-07' not in zh_content:
    zh_content = zh_content.replace('</div>\n\n</div>', zh_card_7 + '\n</div>\n\n</div>')
    if 'FL-07' not in zh_content: # 尝试另一种结尾匹配
        zh_content = zh_content[:-7] + zh_card_7 + '\n</div>'
    with open('content/pages/zh/field-issues.md', 'w', encoding='utf-8') as f:
        f.write(zh_content)
    print("Appended FL-07 and FL-08 to zh/field-issues.md")

# 3. 扩充 content/pages/en/field-issues.md
en_card_7 = """  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
    <div style="height: 200px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="/assets/img/pitfalls/latam-hollow-door-crush.jpg" alt="Latin America Thin Door Indentation" style="width: 100%; height: 100%; object-fit: cover;" />
      <span style="position: absolute; top: 8px; left: 8px; background: #ea580c; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">FL-07 · Skin Collapse</span>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">Latin America (ABNT)</span>
    </div>
    <div style="padding: 16px;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem;">LATAM 30mm Hollow Door Core Indentation Under Bolt Clamp</h3>
      <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 10px;">Brazil/Argentina widespread 30-35mm hollow core doors have thin 3mm skins. Overtightening bolts >2.0 N·m crushes the wood skin, skewing internal mortise pocket and seizing latch throw.</p>
      <div style="background: #fff7ed; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #9a3412; border-left: 3px solid #ea580c;">
        <b>Design Rule:</b> Limit screw torque spec to ≤1.8 N·m; mandate oversized load-spreading reinforcement escutcheon plates.
      </div>
    </div>
  </div>

  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
    <div style="height: 200px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="/assets/img/pitfalls/gcc-thermal-expansion-jam.jpg" alt="GCC Solar Thermal Expansion Jam" style="width: 100%; height: 100%; object-fit: cover;" />
      <span style="position: absolute; top: 8px; left: 8px; background: #dc2626; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">FL-08 · Thermal Seizure</span>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">Middle East (GCC/SASO)</span>
    </div>
    <div style="padding: 16px;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem;">Middle East Extreme Solar Thermal Expansion Jamming Steel Doors</h3>
      <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 10px;">Saudi & UAE exterior doors reach >65°C at midday. Metal thermal expansion compresses door edge gap from 3.5mm down to <0.8mm, tightly pinching the bolt and triggering motor stall errors.</p>
      <div style="background: #fef2f2; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #991b1b; border-left: 3px solid #dc2626;">
        <b>Design Rule:</b> Mandate ≥5.0mm seasonal clearance buffer during Gulf installation; deploy boost torque firmware profiles for midday cycles.
      </div>
    </div>
  </div>
"""

with open('content/pages/en/field-issues.md', 'r', encoding='utf-8') as f:
    en_content = f.read()

if 'FL-07' not in en_content:
    en_content = en_content.replace('</div>\n\n</div>', en_card_7 + '\n</div>\n\n</div>')
    if 'FL-07' not in en_content:
        en_content = en_content[:-7] + en_card_7 + '\n</div>'
    with open('content/pages/en/field-issues.md', 'w', encoding='utf-8') as f:
        f.write(en_content)
    print("Appended FL-07 and FL-08 to en/field-issues.md")

