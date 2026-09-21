with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #2563eb;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚡ ${lang === 'zh' ? '电机功耗与电池内阻门槛 (Electrical Stall Profile)' : 'Motor Current & Battery Internal Resistance'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.electricalProfile || 'N/A')}</span></div>
              <div><b>🛡️ ${lang === 'zh' ? '防钻防撬机械安全认证与保险评级 (Security & Insurance Class)' : 'Security & Insurance Rating'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.securityCertification || 'N/A')}</span></div>
              <div><b>🧲 ${lang === 'zh' ? '门状态磁敏传感器与抗金属屏蔽规范 (Door Sensor Gap Spec)' : 'Door Sensor Gap & Metal Shielding'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.doorSensorSpec || 'N/A')}</span></div>
            </div>
          </div>"""

replacement = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #2563eb; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚡ ${lang === 'zh' ? '电机功耗与电池内阻门槛 (Electrical Stall Profile)' : 'Motor Current & Battery Internal Resistance'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.electricalProfile || 'N/A')}</span></div>
              <div><b>🛡️ ${lang === 'zh' ? '防钻防撬机械安全认证与保险评级 (Security & Insurance Class)' : 'Security & Insurance Rating'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.securityCertification || 'N/A')}</span></div>
              <div><b>🧲 ${lang === 'zh' ? '门状态磁敏传感器与抗金属屏蔽规范 (Door Sensor Gap Spec)' : 'Door Sensor Gap & Metal Shielding'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.doorSensorSpec || 'N/A')}</span></div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #059669;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🏙️ ${lang === 'zh' ? '大都市存量高频分布 (Metropolitan Cities)' : 'Metropolitan Distribution'}:</b> <span style="color: #065f46; font-weight: 600;">${escapeHtml((s.engineeringMatrix.representativeCities || []).join(' · '))}</span></div>
              <div><b>⚙️ ${lang === 'zh' ? '推荐齿轮减速比与反向自锁力矩 (Gearbox Ratio & Torque)' : 'Gearbox Ratio & Back-Drive Torque'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.gearboxSpec || 'N/A')}</span></div>
              <div><b>📏 ${lang === 'zh' ? '原厂锁芯外露量与剪切平面规尺 (Shear Line Clearance)' : 'Shear Line Clearance & Depth'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.shearLineClearance || 'N/A')}</span></div>
            </div>
          </div>"""

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs successfully updated with Cities, Gearbox, and Shear Line specs!")
else:
    print("Target block not found in build.mjs!")
