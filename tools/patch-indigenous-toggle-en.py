with open('content/pages/en/indigenous-guides.md', 'r', encoding='utf-8') as f:
    en = f.read()

toggle_ui_en = """
<div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0 10px; padding: 12px 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
  <span style="font-size: 0.9rem; font-weight: 600; color: #1e293b;">📐 View Mode Toggle:</span>
  <div style="display: flex; gap: 8px;">
    <button id="btn-gallery-view-en" style="font-size: 0.8rem; font-weight: 600; padding: 6px 12px; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: white; cursor: pointer;">🖼️ 2-Column Gallery View</button>
    <button id="btn-table-view-en" style="font-size: 0.8rem; font-weight: 600; padding: 6px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: white; color: #475569; cursor: pointer;">📊 Compact Engineering Table</button>
  </div>
</div>

<div id="indigenous-compact-table-en" style="display: none; margin: 20px 0; overflow-x: auto;">
  <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; background: white; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
    <thead style="background: #0f172a; color: white;">
      <tr>
        <th style="padding: 10px; text-align: left;">Division / Standard</th>
        <th style="padding: 10px; text-align: left;">Backset</th>
        <th style="padding: 10px; text-align: left;">Centres</th>
        <th style="padding: 10px; text-align: left;">Follower / Spindle</th>
        <th style="padding: 10px; text-align: left;">Door Thickness</th>
        <th style="padding: 10px; text-align: left;">Mortise Pocket Rework</th>
        <th style="padding: 10px; text-align: left;">Wire & Bolt Clearance</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇩🇪 Germany (DIN 18251)</td>
        <td style="padding: 10px;">55mm / 65mm (Narrow 35-45mm)</td>
        <td style="padding: 10px;">Interior 72mm / Entrance 92mm PZ</td>
        <td style="padding: 10px;">8×8mm (Panic 9×9mm)</td>
        <td style="padding: 10px;">38-65mm</td>
        <td style="padding: 10px;">Pocket depth 75-80mm; chisel deeper along centerline</td>
        <td style="padding: 10px;">M5 bolts; rubber grommet above cylinder</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇫🇷 France (NF / Vachette)</td>
        <td style="padding: 10px;">40mm / 50mm</td>
        <td style="padding: 10px;"><b>70mm</b> (Not German 72mm)</td>
        <td style="padding: 10px;"><b>7×7mm</b> (Requires 7-to-8mm reducer)</td>
        <td style="padding: 10px;">35-50mm</td>
        <td style="padding: 10px;">Rim multipoints common; standard plates clash</td>
        <td style="padding: 10px;">Reserve 5mm wire gap below follower</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇯🇵 Japan (JIS A 1510)</td>
        <td style="padding: 10px;">51mm / 64mm</td>
        <td style="padding: 10px;">Separate / Interconnected</td>
        <td style="padding: 10px;">8×8mm precision</td>
        <td style="padding: 10px;">33-42mm ultra-thin doors</td>
        <td style="padding: 10px;">≤1.0mm tolerance pocket; use milling cutters for alloy</td>
        <td style="padding: 10px;">M4 shear bolts; routing slot along top casing</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇬🇧 UK & AU (BS / AS 4145)</td>
        <td style="padding: 10px;">40mm / 60mm</td>
        <td style="padding: 10px;">Surface Nightlatch</td>
        <td style="padding: 10px;">Cross / Flat tailpiece</td>
        <td style="padding: 10px;">32-45mm</td>
        <td style="padding: 10px;">Lockwood 001 surface mounted; 32mm hole</td>
        <td style="padding: 10px;">4× 10# screws; anti-tangle sleeve for driver</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9;">
        <td style="padding: 10px; font-weight: 600;">🇧🇷 Latin America (ABNT)</td>
        <td style="padding: 10px;"><b>40mm / 45mm narrow</b></td>
        <td style="padding: 10px;">53mm / 70mm</td>
        <td style="padding: 10px;">8×8mm wide tolerance</td>
        <td style="padding: 10px;">30-35mm plywood</td>
        <td style="padding: 10px;">Shallow pocket (60mm); reinforce with 2.0mm steel</td>
        <td style="padding: 10px;">Wide flat washers to prevent face crushing</td>
      </tr>
      <tr style="border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
        <td style="padding: 10px; font-weight: 600;">🇺🇸 North America (ANSI)</td>
        <td style="padding: 10px;">60mm / 70mm dual switchable</td>
        <td style="padding: 10px;">Standard 140mm (5-1/2")</td>
        <td style="padding: 10px;">1.6×4.8mm flat tailpiece</td>
        <td style="padding: 10px;">35-51mm (1-3/8" ~ 2")</td>
        <td style="padding: 10px;">54mm cross bore; wrap-around plate for split wood</td>
        <td style="padding: 10px;">#10-32 through-bolts; wire channel below tailpiece</td>
      </tr>
    </tbody>
  </table>
</div>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    const btnGallery = document.getElementById('btn-gallery-view-en');
    const btnTable = document.getElementById('btn-table-view-en');
    const galleryView = document.querySelector('.gallery-grid-indigenous-en');
    const tableView = document.getElementById('indigenous-compact-table-en');

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

target = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; margin: 28px 0;">'
replacement = toggle_ui_en + '\n<div class="gallery-grid-indigenous-en" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; margin: 28px 0;">'

if target in en:
    en = en.replace(target, replacement, 1)
    with open('content/pages/en/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(en)
    print("Injected View Mode Toggle and Compact Engineering Table into en/indigenous-guides.md!")
else:
    print("Target grid not found in en/indigenous-guides.md!")
