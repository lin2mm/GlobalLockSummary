with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #06b6d4;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <b>🏠 ${lang === "zh" ? "免打孔/租房改装友好度" : "No-Drill / Rental-Friendly"}:</b>
              <span style="color: #0e7490; font-weight: 600; font-size: 0.75rem;">${escapeHtml(s.engineeringMatrix.rentalOptimization.modificationType)}</span>
            </div>
            <div style="color: #475569; font-size: 0.75rem; margin-top: 3px;">${escapeHtml(s.engineeringMatrix.rentalOptimization.notes)}</div>
          </div>"""

replacement = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #06b6d4; margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <b>🏠 ${lang === "zh" ? "免打孔/租房改装友好度" : "No-Drill / Rental-Friendly"}:</b>
              <span style="color: #0e7490; font-weight: 600; font-size: 0.75rem;">${escapeHtml(s.engineeringMatrix.rentalOptimization.modificationType)}</span>
            </div>
            <div style="color: #475569; font-size: 0.75rem; margin-top: 3px;">${escapeHtml(s.engineeringMatrix.rentalOptimization.notes)}</div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #64748b;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; font-size: 0.72rem;">
              <div><b>🔑 原厂钥匙胚槽型:</b> ${escapeHtml(s.engineeringMatrix.keywaySpecification || 'N/A')}</div>
              <div><b>❄️ 极限气候与电池衰减:</b> ${escapeHtml(s.engineeringMatrix.coldWeatherDerating || 'N/A')}</div>
              <div><b>🔄 执手回弹弹簧阻力:</b> ${escapeHtml(s.engineeringMatrix.handleSpringResistance || 'N/A')}</div>
            </div>
          </div>"""

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs successfully updated with Keyway, Battery, and Spring Torque rendering!")
else:
    print("Target block not found in build.mjs!")
