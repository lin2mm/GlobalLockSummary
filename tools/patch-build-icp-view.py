with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #059669;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🏙️ ${lang === 'zh' ? '大都市存量高频分布 (Metropolitan Cities)' : 'Metropolitan Distribution'}:</b> <span style="color: #065f46; font-weight: 600;">${escapeHtml((s.engineeringMatrix.representativeCities || []).join(' · '))}</span></div>
              <div><b>⚙️ ${lang === 'zh' ? '推荐齿轮减速比与反向自锁力矩 (Gearbox Ratio & Torque)' : 'Gearbox Ratio & Back-Drive Torque'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.gearboxSpec || 'N/A')}</span></div>
              <div><b>📏 ${lang === 'zh' ? '原厂锁芯外露量与剪切平面规尺 (Shear Line Clearance)' : 'Shear Line Clearance & Depth'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.shearLineClearance || 'N/A')}</span></div>
            </div>
          </div>"""

replacement = """          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #059669; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🏙️ ${lang === 'zh' ? '大都市存量高频分布 (Metropolitan Cities)' : 'Metropolitan Distribution'}:</b> <span style="color: #065f46; font-weight: 600;">${escapeHtml((s.engineeringMatrix.representativeCities || []).join(' · '))}</span></div>
              <div><b>⚙️ ${lang === 'zh' ? '推荐齿轮减速比与反向自锁力矩 (Gearbox Ratio & Torque)' : 'Gearbox Ratio & Back-Drive Torque'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.gearboxSpec || 'N/A')}</span></div>
              <div><b>📏 ${lang === 'zh' ? '原厂锁芯外露量与剪切平面规尺 (Shear Line Clearance)' : 'Shear Line Clearance & Depth'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.shearLineClearance || 'N/A')}</span></div>
            </div>
          </div>
          ${s.engineeringMatrix.nukiRetrofitProfile ? `
          <div style="background: #fdf4ff; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #c026d3;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🎯 ${lang === 'zh' ? 'Nuki 加装指数与核心 ICP 画像' : 'Nuki Retrofit & ICP Profile'}:</b> <span style="color: #86198f; font-weight: 700;">★ 指数: ${s.engineeringMatrix.nukiRetrofitProfile.nukiRetrofitScore}/100</span> · <span style="color: #701a75;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.primaryICP || 'N/A')}</span></div>
              <div><b>🔑 ${lang === 'zh' ? '租客退租无损复原评级' : 'Tenant Zero-Damage Grade'}:</b> <span style="color: #86198f;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.tenantFriendlyGrade || 'N/A')}</span> · 预计施工耗时: ${s.engineeringMatrix.nukiRetrofitProfile.installationTimeMin} 分钟</div>
              <div><b>🛠️ ${lang === 'zh' ? '推荐搭载专属改装 BOM' : 'Recommended Retrofit Kit'}:</b> <span style="color: #4a044e; font-weight: 600;">${escapeHtml((s.engineeringMatrix.nukiRetrofitProfile.retrofitKit || []).join(' + '))}</span></div>
            </div>
          </div>` : ''}"""

if target in text:
    text = text.replace(target, replacement)
    with open('build.mjs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build.mjs successfully updated with Nuki Retrofit & ICP Profile cards!")
else:
    print("Target block not found in build.mjs!")
