with open('content/pages/zh/indigenous-guides.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 增设视图切换按钮与高密度紧凑工程参数表
toggle_ui_zh = """
<div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0 10px; padding: 12px 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
  <span style="font-size: 0.9rem; font-weight: 600; color: #1e293b;">📐 视图模式切换 (View Mode):</span>
  <div style="display: flex; gap: 8px;">
    <button id="btn-gallery-view" style="font-size: 0.8rem; font-weight: 600; padding: 6px 12px; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: white; cursor: pointer;">🖼️ 双列画廊模式 (Gallery)</button>
    <button id="btn-table-view" style="font-size: 0.8rem; font-weight: 600; padding: 6px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: white; color: #475569; cursor: pointer;">📊 紧凑工程参数表 (Compact Table)</button>
  </div>
</div>

<div id="indigenous-compact-table" style="display: none; margin: 20px 0; overflow-x: auto;">
  <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; background: white; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
    <thead style="background: #0f172a; color: white;">
      <tr>
        <th style="padding: 10px; text-align: left;">工业板块 / 标准</th>
        <th style="padding: 10px; text-align: left;">主流背距 (Backset)</th>
        <th style="padding: 10px; text-align: left;">中心距 (Centres)</th>
        <th style="padding: 10px; text-align: left;">方轴孔径 (Spindle)</th>
        <th style="padding: 10px; text-align: left;">标准门厚 (Thickness)</th>
        <th style="padding: 10px; text-align: left;">锁体槽修凿要求 (Mortise Pocket)</th>
        <th style="padding: 10px; text-align: left;">走线与对穿螺栓避让 (Wire Clearance)</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇩🇪 德语区 (DIN 18251)</td>
        <td style="padding: 10px;">55mm / 65mm (窄框35-45mm)</td>
        <td style="padding: 10px;">室内72mm / 入户92mm PZ</td>
        <td style="padding: 10px;">8×8mm (逃生9×9mm)</td>
        <td style="padding: 10px;">38-65mm</td>
        <td style="padding: 10px;">原槽 75-80mm；扩深需沿中线钻阶梯孔微修</td>
        <td style="padding: 10px;">M5 沉头螺栓，锁芯上方设专用穿线橡胶套圈</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇫🇷 法语区 (NF / Vachette)</td>
        <td style="padding: 10px;">40mm / 50mm</td>
        <td style="padding: 10px;"><b>70mm</b> (切勿套用德规72mm)</td>
        <td style="padding: 10px;"><b>7×7mm</b> (需配7转8变径套)</td>
        <td style="padding: 10px;">35-50mm</td>
        <td style="padding: 10px;">多点锁多为表面明装天地杆，常规面板不可装</td>
        <td style="padding: 10px;">方轴下方预留 5mm 间隙，避免下压把手挤断线缆</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇯🇵 日本区 (JIS A 1510)</td>
        <td style="padding: 10px;">51mm / 64mm</td>
        <td style="padding: 10px;">独立旋钮 / 联动插芯</td>
        <td style="padding: 10px;">8×8mm 高精</td>
        <td style="padding: 10px;">33-42mm 超薄门扇</td>
        <td style="padding: 10px;">间隙 ≤1.0mm 高精锁槽，铝门禁重击凿削需铣刀</td>
        <td style="padding: 10px;">M4 剪切螺栓，线束置于锁体顶部专属滑槽</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇬🇧 澳英区 (BS / AS 4145)</td>
        <td style="padding: 10px;">40mm / 60mm</td>
        <td style="padding: 10px;">分体夜闩 / 表面锁</td>
        <td style="padding: 10px;">十字尾轴 / 扁平拨叉</td>
        <td style="padding: 10px;">32-45mm</td>
        <td style="padding: 10px;">Lockwood 001 为表面装配，仅打32mm通孔</td>
        <td style="padding: 10px;">表面底盘 4 颗 10# 螺钉，传动销设防缠绕护套</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇧🇷 拉美区 (ABNT NBR 14913)</td>
        <td style="padding: 10px;"><b>40mm / 45mm 极窄</b></td>
        <td style="padding: 10px;">53mm / 70mm</td>
        <td style="padding: 10px;">8×8mm 宽公差</td>
        <td style="padding: 10px;">30-35mm 夹板门</td>
        <td style="padding: 10px;">浅槽 (深60mm)；向内扩孔需加 2.0mm 钢板防撬</td>
        <td style="padding: 10px;">对穿螺栓需加宽平垫片，防止夹板被压溃变形</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇺🇸 北美区 (ANSI / BHMA)</td>
        <td style="padding: 10px;">60mm / 70mm 双向旋转可调</td>
        <td style="padding: 10px;">标准双孔 140mm (5-1/2")</td>
        <td style="padding: 10px;">1.6×4.8mm 扁平转动片</td>
        <td style="padding: 10px;">35-51mm (1-3/8" ~ 2")</td>
        <td style="padding: 10px;">圆孔 54mm 贯穿；老木门开裂需加金属包角锁夹</td>
        <td style="padding: 10px;">#10-32 对穿螺栓，走线通道置于尾轴正下方</td>
      </tr>
    </tbody>
  </table>
</div>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    const btnGallery = document.getElementById('btn-gallery-view');
    const btnTable = document.getElementById('btn-table-view');
    const galleryView = document.querySelector('.gallery-grid-indigenous');
    const tableView = document.getElementById('indigenous-compact-table');

    if (btnGallery && btnTable && galleryView && tableView) {
      btnGallery.addEventListener('click', () => {
        galleryView.style.display = 'grid';
        tableView.style.display = 'none';
        btnGallery.style.background = '#0284c7';
        btnGallery.style.color = '#ffffff';
        btnGallery.style.borderColor = '#0284c7';
        btnTable.style.background = '#ffffff';
        btnTable.style.color = '#475569';
        btnTable.style.borderColor = '#cbd5e1';
      });

      btnTable.addEventListener('click', () => {
        galleryView.style.display = 'none';
        tableView.style.display = 'block';
        btnTable.style.background = '#0284c7';
        btnTable.style.color = '#ffffff';
        btnTable.style.borderColor = '#0284c7';
        btnGallery.style.background = '#ffffff';
        btnGallery.style.color = '#475569';
        btnGallery.style.borderColor = '#cbd5e1';
      });
    }
  });
</script>
"""

# 在 h1 后面注入 toggle_ui
target = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; margin: 28px 0;">'
replacement = toggle_ui_zh + '\n<div class="gallery-grid-indigenous" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; margin: 28px 0;">'

if target in zh:
    zh = zh.replace(target, replacement, 1)
    with open('content/pages/zh/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(zh)
    print("Injected View Mode Toggle and Compact Engineering Table into zh/indigenous-guides.md!")
else:
    print("Target grid not found in zh/indigenous-guides.md!")
