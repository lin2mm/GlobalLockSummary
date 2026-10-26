with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #64748b;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; font-size: 0.72rem;">
              <div><b>🔑 原厂钥匙胚槽型:</b> ${escapeHtml(s.engineeringMatrix.keywaySpecification || 'N/A')}</div>
              <div><b>❄️ 极限气候与电池衰减:</b> ${escapeHtml(s.engineeringMatrix.coldWeatherDerating || 'N/A')}</div>
              <div><b>🔄 执手回弹弹簧阻力:</b> ${escapeHtml(s.engineeringMatrix.handleSpringResistance || 'N/A')}</div>
            </div>
          </div>"""

replacement = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #64748b; margin-bottom: 6px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; font-size: 0.72rem;">
              <div><b>🔑 原厂钥匙胚槽型:</b> ${escapeHtml(s.engineeringMatrix.keywaySpecification || 'N/A')}</div>
              <div><b>❄️ 极限气候与电池衰减:</b> ${escapeHtml(s.engineeringMatrix.coldWeatherDerating || 'N/A')}</div>
              <div><b>🔄 执手回弹弹簧阻力:</b> ${escapeHtml(s.engineeringMatrix.handleSpringResistance || 'N/A')}</div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #d97706;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔨 ${lang === 'zh' ? '门侧木槽二次扩孔与防裂加固 (Chisel Mortise Rework)' : 'Chisel Mortise Rework & Reinforcement'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.mortiseReworkGuide || 'N/A')}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '贯穿螺栓剪切公差与防夹线套管 (Through-Bolt Wire Guide)' : 'Through-Bolt & Wire Clearance'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.boltWireClearance || 'N/A')}</span></div>
            </div>
          </div>"""

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs successfully updated with Mortise Rework and Wire Guide specs!")
else:
    print("Target block not found in build.mjs!")
