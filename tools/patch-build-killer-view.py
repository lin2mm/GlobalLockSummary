with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          ${s.engineeringMatrix.nukiRetrofitProfile ? `
          <div style="background: #fdf4ff; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #c026d3;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🎯 ${lang === 'zh' ? 'Nuki 加装指数与核心 ICP 画像' : 'Nuki Retrofit & ICP Profile'}:</b> <span style="color: #86198f; font-weight: 700;">★ 指数: ${s.engineeringMatrix.nukiRetrofitProfile.nukiRetrofitScore}/100</span> · <span style="color: #701a75;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.primaryICP || 'N/A')}</span></div>
              <div><b>🔑 ${lang === 'zh' ? '租客退租无损复原评级' : 'Tenant Zero-Damage Grade'}:</b> <span style="color: #86198f;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.tenantFriendlyGrade || 'N/A')}</span> · 预计施工耗时: ${s.engineeringMatrix.nukiRetrofitProfile.installationTimeMin} 分钟</div>
              <div><b>🛠️ ${lang === 'zh' ? '推荐搭载专属改装 BOM' : 'Recommended Retrofit Kit'}:</b> <span style="color: #4a044e; font-weight: 600;">${escapeHtml((s.engineeringMatrix.nukiRetrofitProfile.retrofitKit || []).join(' + '))}</span></div>
            </div>
          </div>` : ''}"""

replacement = """          ${s.engineeringMatrix.nukiRetrofitProfile ? `
          <div style="background: #fdf4ff; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #c026d3; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🎯 ${lang === 'zh' ? 'Nuki 加装指数与核心 ICP 画像' : 'Nuki Retrofit & ICP Profile'}:</b> <span style="color: #86198f; font-weight: 700;">★ 指数: ${s.engineeringMatrix.nukiRetrofitProfile.nukiRetrofitScore}/100</span> · <span style="color: #701a75;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.primaryICP || 'N/A')}</span></div>
              <div><b>🔑 ${lang === 'zh' ? '租客退租无损复原评级' : 'Tenant Zero-Damage Grade'}:</b> <span style="color: #86198f;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.tenantFriendlyGrade || 'N/A')}</span> · 预计施工耗时: ${s.engineeringMatrix.nukiRetrofitProfile.installationTimeMin} 分钟</div>
              <div><b>🛠️ ${lang === 'zh' ? '推荐搭载专属改装 BOM' : 'Recommended Retrofit Kit'}:</b> <span style="color: #4a044e; font-weight: 600;">${escapeHtml((s.engineeringMatrix.nukiRetrofitProfile.retrofitKit || []).join(' + '))}</span></div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.weatherproofingMatrix ? `
          <div style="background: #fffbeb; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #d97706; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>☀️ ${lang === 'zh' ? '耐候防腐与盐雾测试标准 (Weatherproofing & Salt Spray)' : 'Salt Spray & Weatherproofing'}:</b> <span style="color: #92400e; font-weight: 600;">${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.saltSprayClass)}</span> · ${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.ipRating)}</div>
              <div><b>🌡️ ${lang === 'zh' ? '极限温度与密封胶条规范' : 'Thermal & Gasket'}:</b> <span style="color: #b45309;">${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.solarThermalMax)}</span> · ${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.epdmGasketSpec)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.multipointKinematics && s.engineeringMatrix.multipointKinematics.isMultipointCompatible ? `
          <div style="background: #f0fdfa; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #0d9488; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔄 ${lang === 'zh' ? '多点联动门抬把手行程与阻尼 (Multipoint Kinematics)' : 'Multipoint Kinematics & Torque'}:</b> <span style="color: #115e59; font-weight: 600;">抬把手角度: ${escapeHtml(s.engineeringMatrix.multipointKinematics.liftAngle)}</span> · 传动阻尼: ${escapeHtml(s.engineeringMatrix.multipointKinematics.camDriveTorque)}</div>
              <div><b>🔧 ${lang === 'zh' ? '主流五金厂与偏心调节指南' : 'Hardware Vendors & Tuning'}:</b> <span style="color: #134e4a;">${escapeHtml(s.engineeringMatrix.multipointKinematics.majorHardwareVendors)}</span> · ${escapeHtml(s.engineeringMatrix.multipointKinematics.fieldAdjustmentGuide)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.emergencyClutchWhitelist && s.engineeringMatrix.emergencyClutchWhitelist.isMandatory ? `
          <div style="background: #fef2f2; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #ef4444; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚠️ ${lang === 'zh' ? '欧标防反锁应急双离合官方认证白名单' : 'Emergency Dual-Clutch Approved List'}:</b> <span style="color: #991b1b; font-weight: 700;">${escapeHtml(s.engineeringMatrix.emergencyClutchWhitelist.standard)}</span></div>
              <div style="color: #b91c1c;"><b>官方推荐防锁死锁芯:</b> ${(s.engineeringMatrix.emergencyClutchWhitelist.approvedModels || []).map(m => escapeHtml(m)).join(' · ')}</div>
              <div style="color: #7f1d1d; font-size: 0.7rem; font-style: italic;">${escapeHtml(s.engineeringMatrix.emergencyClutchWhitelist.lockoutRiskWarning)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.doorThicknessMatrix ? `
          <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #475569;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🚪 ${lang === 'zh' ? '门扇厚度与对穿螺栓方轴速查 (Door Thickness & Fasteners)' : 'Door Thickness & Fasteners'}:</b> <span style="color: #1e293b; font-weight: 600;">主流门厚: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.typicalDoorThickness)}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '方轴与螺栓包工程选型' : 'Spindle & Bolt Spec'}:</b> 方轴: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.spindleRequirement)} · 螺丝: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.boltRequirement)}</div>
              <div><b>🛡️ ${lang === 'zh' ? '门板加固与压溃防护' : 'Reinforcement'}:</b> ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.reinforcementPlate)}</div>
            </div>
          </div>` : ''}"""

if target in text:
    text = text.replace(target, replacement)
    print("Patched build.mjs with 4 killer features view cards!")
else:
    print("target block not found in build.mjs, checking...")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

