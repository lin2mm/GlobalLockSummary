with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #d97706;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔨 ${lang === 'zh' ? '门侧木槽二次扩孔与防裂加固 (Chisel Mortise Rework)' : 'Chisel Mortise Rework & Reinforcement'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.mortiseReworkGuide || 'N/A')}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '贯穿螺栓剪切公差与防夹线套管 (Through-Bolt Wire Guide)' : 'Through-Bolt & Wire Clearance'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.boltWireClearance || 'N/A')}</span></div>
            </div>
          </div>"""

replacement = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #d97706; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔨 ${lang === 'zh' ? '门侧木槽二次扩孔与防裂加固 (Chisel Mortise Rework)' : 'Chisel Mortise Rework & Reinforcement'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.mortiseReworkGuide || 'N/A')}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '贯穿螺栓剪切公差与防夹线套管 (Through-Bolt Wire Guide)' : 'Through-Bolt & Wire Clearance'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.boltWireClearance || 'N/A')}</span></div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #2563eb;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚡ ${lang === 'zh' ? '电机功耗与电池内阻门槛 (Electrical Stall Profile)' : 'Motor Current & Battery Internal Resistance'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.electricalProfile || 'N/A')}</span></div>
              <div><b>🛡️ ${lang === 'zh' ? '防钻防撬机械安全认证与保险评级 (Security & Insurance Class)' : 'Security & Insurance Rating'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.securityCertification || 'N/A')}</span></div>
              <div><b>🧲 ${lang === 'zh' ? '门状态磁敏传感器与抗金属屏蔽规范 (Door Sensor Gap Spec)' : 'Door Sensor Gap & Metal Shielding'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.doorSensorSpec || 'N/A')}</span></div>
            </div>
          </div>"""

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs successfully updated with Electrical, Security, and Sensor specs!")
else:
    print("Target block not found in build.mjs!")
