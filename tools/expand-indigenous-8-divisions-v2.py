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

# 更新 zh
with open('content/pages/zh/indigenous-guides.md', 'r', encoding='utf-8') as f:
    zh = f.read()

if 'id="gcc"' not in zh:
    zh = zh.replace('  <!-- 3. 日本精工 -->', zh_card_gcc + '\n  <!-- 3. 日本精工 -->')
    with open('content/pages/zh/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(zh)
    print("Added gcc card to zh")

# 更新 en
with open('content/pages/en/indigenous-guides.md', 'r', encoding='utf-8') as f:
    en = f.read()

if 'id="gcc"' not in en:
    en = en.replace('  <!-- 3. Japan', en_card_gcc + '\n  <!-- 3. Japan')
    with open('content/pages/en/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(en)
    print("Added gcc card to en")

