import re

# 1. 扩充 content/pages/zh/indigenous-guides.md
with open('content/pages/zh/indigenous-guides.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 替换顶部导航条和前言
old_zh_nav = """<!-- 顶部 6 大区域快速穿透锚点导航条 -->
<div style="margin: 20px 0 32px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 快速直达工业板块:</span>
  <a href="#de-at-ch" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇩🇪 德奥瑞 (DIN)</a>
  <a href="#fr-be" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇫🇷 法比区 (NF)</a>
  <a href="#jp" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇯🇵 日本精工 (JIS/MIWA)</a>
  <a href="#uk-anz" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇺 英澳体系 (AS/BS)</a>
  <a href="#latam" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🌎 西语与拉美 (ABNT)</a>
  <a href="#na" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇺🇸 北美标准 (ANSI)</a>
</div>"""

new_zh_nav = """<!-- 顶部 8 大工业板块快速穿透锚点导航条（按工程暗坑与加装复杂度降序排列） -->
<div style="margin: 20px 0 32px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 快速直达工业板块:</span>
  <a href="#de-at-ch" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇩🇪 德奥瑞 (DIN)</a>
  <a href="#fr-be" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇫🇷 法比区 (NF)</a>
  <a href="#gcc" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇪 中东海湾 (SASO/GCC)</a>
  <a href="#jp" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇯🇵 日本精工 (JIS/MIWA)</a>
  <a href="#uk-anz" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇺 英澳体系 (AS/BS)</a>
  <a href="#latam" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🌎 西语与拉美 (ABNT)</a>
  <a href="#in-sa" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇮🇳 南亚非洲 (BIS/SABS)</a>
  <a href="#na" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇺🇸 北美标准 (ANSI)</a>
</div>"""

zh_card_gcc = """  <!-- 中东海湾 SASO/GCC -->
  <div id="gcc" style="background: #ffffff; border: 1.5px solid #d97706; border-left: 6px solid #d97706; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(217,119,6,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇦🇪🇸🇦 中东海湾体系：超厚重装甲门、SASO 85mm 距与耐极端暴晒</h2>
      <span style="background: #d97706; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">SASO 2063 / GSO EN 12209</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
        <img src="/assets/img/indigenous/gcc-saso-mortise.jpg" alt="中东 SASO 重型铜锁与装甲门" style="width: 100%; height: 100%; object-fit: cover;" />
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>门扇极端厚度 (60~85mm):</b> 标配重型实木雕花门或双层防弹铸铝门，常规 45mm 螺栓与方轴完全穿不透。</li>
          <li><b>中心距 (Entraxe 85mm):</b> 大量沿用英制衍生与意式 85mm 大中心距，区别于西欧 72mm 规范。</li>
          <li><b>极限暴晒工况 (>65°C):</b> 正午金属门体严重热胀，门缝压缩导致死锁舌咬死，要求电机静态防堵转与耐热硅胶密封。</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #fffbeb; border-radius: 4px; font-size: 0.78rem; color: #92400e;">
          <b>加装工程铁律:</b> 必须随箱配发 110mm 加长对穿螺栓与 120mm 加长分体方轴；电机固件必须具备正午自适应高扭矩脉冲破冰脱困功能。
        </div>
      </div>
    </div>
  </div>
"""

zh_card_insa = """  <!-- 印度南亚与非洲 BIS/SABS -->
  <div id="in-sa" style="background: #ffffff; border: 1.5px solid #059669; border-left: 6px solid #059669; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(5,150,105,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇮🇳🇿🇦 南亚与非洲体系：三轨混杂市场、Godrej 外装双向舌与高盐雾</h2>
      <span style="background: #059669; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">IS 2209 (BIS) / SABS 4 / EN 12209</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
        <img src="/assets/img/indigenous/in-godrej-rim.jpg" alt="印度 Godrej Ultra 外装死锁" style="width: 100%; height: 100%; object-fit: cover;" />
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>三轨并存生态:</b> 市场同时流通欧标插芯锁（50mm背距）、Godrej外装夜锁（69mm背距）与球形锁（60mm）。</li>
          <li><b>外装表面锁主导:</b> 印度大都市公寓大量在门内表面加装 Godrej 旋钮外装锁，无法直接套用管状插销电机。</li>
          <li><b>沿海高盐雾腐蚀:</b> 孟买、德班等沿海城市湿度常年 >85%，锌合金表面镀层极易起泡剥落。</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #ecfdf5; border-radius: 4px; font-size: 0.78rem; color: #065f46;">
          <b>加装工程铁律:</b> 严禁仅提供单一插芯锁转接件；外装锁必须配备专属外跨转动盘，且整机耐盐雾防护必须达到 ASTM B117 96小时防腐测试。
        </div>
      </div>
    </div>
  </div>
"""

zh = zh.replace(old_zh_nav, new_zh_nav)
zh = zh.replace("6 大工业五金体系", "8 大工业五金体系（按工程复杂度降序排列）")

if 'id="gcc"' not in zh:
    # 插入在法比区后面
    zh = zh.replace('  <!-- 3. 日本 -->', zh_card_gcc + '\n  <!-- 3. 日本 -->')

if 'id="in-sa"' not in zh:
    # 插入在拉美后面，北美前面
    zh = zh.replace('  <!-- 6. 北美标准 -->', zh_card_insa + '\n  <!-- 6. 北美标准 -->')

with open('content/pages/zh/indigenous-guides.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Updated content/pages/zh/indigenous-guides.md with 8 divisions!")

# 2. 扩充 content/pages/en/indigenous-guides.md
with open('content/pages/en/indigenous-guides.md', 'r', encoding='utf-8') as f:
    en = f.read()

old_en_nav = """<!-- 顶部 6 大区域快速穿透锚点导航条 -->
<div style="margin: 20px 0 32px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 Quick Jump to Standards:</span>
  <a href="#de-at-ch" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇩🇪 DACH (DIN)</a>
  <a href="#fr-be" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇫🇷 France (NF)</a>
  <a href="#jp" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇯🇵 Japan (JIS/MIWA)</a>
  <a href="#uk-anz" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇺 UK & ANZ (AS/BS)</a>
  <a href="#latam" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🌎 Latin America (ABNT)</a>
  <a href="#na" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇺🇸 North America (ANSI)</a>
</div>"""

new_en_nav = """<!-- Top 8 Divisions Quick Jump Bar (Sorted in Engineering Complexity Decrescendo) -->
<div style="margin: 20px 0 32px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 Quick Jump to Standards:</span>
  <a href="#de-at-ch" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇩🇪 DACH (DIN)</a>
  <a href="#fr-be" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇫🇷 France (NF)</a>
  <a href="#gcc" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇪 GCC Middle East (SASO)</a>
  <a href="#jp" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇯🇵 Japan (JIS/MIWA)</a>
  <a href="#uk-anz" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇺 UK & ANZ (AS/BS)</a>
  <a href="#latam" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🌎 Latin America (ABNT)</a>
  <a href="#in-sa" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇮🇳 South Asia & Africa (BIS)</a>
  <a href="#na" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇺🇸 North America (ANSI)</a>
</div>"""

en_card_gcc = """  <!-- GCC Middle East SASO -->
  <div id="gcc" style="background: #ffffff; border: 1.5px solid #d97706; border-left: 6px solid #d97706; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(217,119,6,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇦🇪🇸🇦 Middle East Gulf: Heavy Armoured Doors, 85mm Centres & Solar Heat Binding</h2>
      <span style="background: #d97706; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">SASO 2063 / GSO EN 12209</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
        <img src="/assets/img/indigenous/gcc-saso-mortise.jpg" alt="Middle East SASO Heavy Mortise" style="width: 100%; height: 100%; object-fit: cover;" />
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Extreme Door Thickness (60~85mm):</b> Prevalent solid cast aluminum and carved timber doors require oversized fixing bolts and long split spindles.</li>
          <li><b>Centre Distance (85mm):</b> Widely adheres to Italian/Levantine 85mm centres rather than Western European 72mm.</li>
          <li><b>Midday Thermal Expansion (>65°C):</b> Massive heat absorption compresses edge gap, seizing latchbolts under heavy friction.</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #fffbeb; border-radius: 4px; font-size: 0.78rem; color: #92400e;">
          <b>Engineering Protocol:</b> Bundle 110mm bolts and 120mm spindles; implement high-torque pulse break-away firmware profiles for hot climates.
        </div>
      </div>
    </div>
  </div>
"""

en_card_insa = """  <!-- South Asia & Africa BIS/SABS -->
  <div id="in-sa" style="background: #ffffff; border: 1.5px solid #059669; border-left: 6px solid #059669; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(5,150,105,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇮🇳🇿🇦 South Asia & Africa: Tri-Track Heterogeneity, Surface Rim Locks & High Salinity</h2>
      <span style="background: #059669; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">IS 2209 (BIS) / SABS 4 / EN 12209</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
        <img src="/assets/img/indigenous/in-godrej-rim.jpg" alt="India Godrej Surface Rim Lock" style="width: 100%; height: 100%; object-fit: cover;" />
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Tri-Track Market:</b> Euro mortise (50mm backset), Godrej surface rim locks (69mm backset), and bored locks coexist on the same corridors.</li>
          <li><b>Surface-Mounted Domination:</b> Heavy penetration of surface-mounted deadlatches prevents standard tubular deadbolt motor drop-ins.</li>
          <li><b>Coastal Corrosion:</b> High humidity (>85%) requires ASTM B117 96h salt spray corrosion resistance.</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #ecfdf5; border-radius: 4px; font-size: 0.78rem; color: #065f46;">
          <b>Engineering Protocol:</b> Provide specialized external rotary turn-knob coupler brackets; enforce marine-grade powder coating on all exterior components.
        </div>
      </div>
    </div>
  </div>
"""

en = en.replace(old_en_nav, new_en_nav)
en = en.replace("6 major indigenous hardware systems", "8 major industrial divisions (sorted in engineering complexity decrescendo)")

if 'id="gcc"' not in en:
    en = en.replace('  <!-- 3. Japan -->', en_card_gcc + '\n  <!-- 3. Japan -->')

if 'id="in-sa"' not in en:
    en = en.replace('  <!-- 6. North America -->', en_card_insa + '\n  <!-- 6. North America -->')

with open('content/pages/en/indigenous-guides.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Updated content/pages/en/indigenous-guides.md with 8 divisions!")

