with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 彻底重构 install-gallery 卡片：
# 1. 删除冗长纯文本 p (cDesc)；
# 2. 关键指标转为 2 个高密度微标签 [⌖ 主孔 54mm] [⌖ 背距 60/70mm]
# 3. 按钮合并为 1 个极简工业按钮 [所属锁型图谱 →]
old_snippet = """      return `<div class="install-case-card" style="background: var(--color-surface, #fff); border: 1px solid var(--color-border, #cbd5e1); border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
        <div style="position: relative; height: 170px; background: #000; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #ffffff; font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: 3px;">
            ${escapeHtml(c.id)} · ${escapeHtml(c.sceneType)}
          </span>
          <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.8); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 12px 14px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; margin-bottom: 4px;">
            <span>${isZh ? '所属锁族:' : 'Family:'} <a href="${lockLink}" style="font-weight: 600; color: #0B1D47;">${escapeHtml(c.lockFamilyName)}</a></span>
            <span><a href="${catLink}" style="color: #64748b;">${escapeHtml(cRegion)} ${isZh ? '图谱' : 'Gallery'} →</a></span>
          </div>
          <h3 style="margin: 0 0 6px; font-size: 0.96rem; line-height: 1.35; font-weight: 700;">${escapeHtml(cTitle)}</h3>
          <p style="font-size: 0.8rem; color: #475569; line-height: 1.45; margin: 0 0 8px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${escapeHtml(cDesc)}</p>
          <div style="background: #f8fafc; border-left: 2.5px solid #0f172a; padding: 4px 8px; font-size: 0.74rem; color: #334155; margin-bottom: 8px;">
            <b>${isZh ? '⌖ 关键指标:' : 'Key Metrics:'}</b> ${escapeHtml(c.keyMetrics)}
          </div>
          <div style="display: flex; gap: 6px;">
            <a style="flex: 1; text-align: center; font-size: 0.76rem; font-weight: 600; padding: 6px 10px; background: #0f172a; color: #ffffff; border: 1px solid #0f172a; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${lockLink}">
              ${isZh ? '所属锁型详情 →' : 'Lock Details →'}
            </a>
            <a style="background: #f8fafc; border: 1px solid #cbd5e1; color: #334155; font-size: 0.76rem; font-weight: 600; padding: 6px 10px; border-radius: 4px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center;" href="${catLink}">
              ${isZh ? '分类图谱' : 'Gallery'}
            </a>
          </div>
        </div>
      </div>`;"""

new_snippet = """      // 提取工程关键微指标，转为 ASSA ABLOY 紧凑工业胶囊
      const metricChips = (c.keyMetrics || '')
        .split(/[·,;]/)
        .filter(m => m.trim().length > 0)
        .slice(0, 2)
        .map(m => `<span style="display: inline-block; background: #f8fafc; border: 1px solid #e2e8f0; color: #334155; font-size: 0.72rem; font-weight: 500; padding: 2px 6px; border-radius: 3px;">⌖ ${escapeHtml(m.trim())}</span>`)
        .join(' ');

      return `<div class="install-case-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="position: relative; height: 160px; background: #0b1120; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #ffffff; font-size: 0.68rem; font-weight: 700; padding: 2px 6px; border-radius: 3px; font-family: monospace;">
            ${escapeHtml(c.id)}
          </span>
          <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.8); color: #cbd5e1; font-size: 0.65rem; padding: 2px 6px; border-radius: 2px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 10px 12px; flex: 1; display: flex; flex-direction: column;">
          <div style="font-size: 0.72rem; color: #64748b; margin-bottom: 2px;">
            <a href="${lockLink}" style="color: #64748b; text-decoration: none; font-weight: 500;">${escapeHtml(c.lockFamilyName)}</a>
          </div>
          <h3 style="margin: 0 0 6px; font-size: 0.92rem; line-height: 1.35; font-weight: 700; color: #0f172a; flex: 1;">
            <a href="${lockLink}" style="color: inherit; text-decoration: none;">${escapeHtml(cTitle)}</a>
          </h3>
          <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px;">
            ${metricChips}
          </div>
          <a style="text-align: center; font-size: 0.75rem; font-weight: 600; padding: 5px 8px; background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 4px; text-decoration: none; display: block;" href="${lockLink}">
            ${isZh ? '查看施工图谱与锁型 →' : 'View Case & Blueprint →'}
          </a>
        </div>
      </div>`;"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    print("Streamlined install-gallery cards into pure ASSA ABLOY minimal spec sheets!")
else:
    print("old_snippet not found in build.mjs")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

