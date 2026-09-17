---
title: "全球五大工业板块标准索引与多国本土辨锁大百科"
slug: "indigenous-guides.html"
lang: "zh"
---

# 全球工业索引与多国本土辨锁图谱 (Master Engineering Index)

面向出海智能硬件与五金研发工程师，采用全站统一的**双列卡片流 (2-Column Gallery Grid)** 风格，整合德国 (DIN)、法国 (NF)、日本 (JIS)、英澳 (BS/AS) 与拉美 (ABNT) 的本地核心术语、门锁物理实拍图解与一线避坑红线。


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

<div class="gallery-grid-indigenous" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; margin: 28px 0;">

  <!-- 卡片 1：德语区 DIN 18251 -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/de-dornmass-pz.png" alt="德国 DIN 18251 Dornmaß 与 PZ 测量" style="width: 100%; height: 100%; object-fit: contain; padding: 6px; background: #fff;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">DIN 图解</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/de-gefahrenfunktion.jpg" alt="Not- und Gefahrenfunktion 结构" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">双向离合实拍</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-DE · 德语区</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">DIN 18251 / 18252</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">德奥瑞：Dornmaß、PZ 与双向应急离合</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>Dornmaß (背距):</b> 住宅标准为 <b>55mm / 65mm</b>；窄框门为 35/40/45mm。小于 55mm 加装锁易碰门框。</li>
        <li><b>Entfernungsmaß / PZ:</b> 室内木门为 <b>72mm</b>；入户大门与防火逃生门统一为 <b>92mm</b>。</li>
        <li><b>Drückernuss (方轴孔):</b> 普通门为 8×8mm，公建防火逃生门为 9×9mm。</li>
      </ul>
      <div style="background: #fef2f2; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #991b1b; border-left: 3px solid #dc2626;">
        <b>⚠️ 绝对红线 (Gefahrenfunktion):</b> 门内夹持钥匙加装必须确认原锁芯具备应急离合，否则电池耗尽将导致彻底反锁只能破门！
      </div>
    </div>
  </div>

  <!-- 卡片 2：法语区 NF / Vachette -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #ffffff;">
        <img src="../assets/img/indigenous/fr-entraxe-70.png" alt="法国 Axe 50 Entraxe 70 锁体" style="width: 100%; height: 100%; object-fit: contain; padding: 6px;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">Vachette 70mm</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/gallery/eu-19_real.jpg" alt="法国 Bricard Série 70 实景" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">门上实态</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-FR · 法语区</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">NF / EN 12209</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">法比区：Axe 50、Entraxe 70 与 7mm 特殊方轴</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>L'Axe (背距):</b> 住宅标准普遍为 <b>40mm 或 50mm</b>。</li>
        <li><b>L'Entraxe (中心距):</b> <b>法国绝大多数为 70mm</b>（切勿套用德规 72mm！公模面板绝对装不进）。</li>
        <li><b>Carré / Fouillot (方轴):</b> 普遍采用 <b>7×7mm 方轴</b>，必须配备 7mm转8mm 变径铜套方能适配。</li>
      </ul>
      <div style="background: #fff7ed; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #9a3412; border-left: 3px solid #ea580c;">
        <b>⚠️ 结构红线 (Serrure en applique):</b> 巴黎老式公寓高频使用明装箱体多点锁，天地锁杆裸露在门内侧，无法安装常规面板智能锁。
      </div>
    </div>
  </div>

  <!-- 卡片 3：日本区 JIS A 1510 -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/jp-miwa-13la.jpg" alt="MIWA 13LA フロント刻印" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">刻印即型号</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/jp-thumbturn.jpg" alt="MIWA 防犯サムターン" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">防犯旋钮实拍</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-JP · 日本区</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">JIS A 1510 / MIWA / GOAL</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">日本：フロント刻印反查与防盗旋钮避坑</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>フロント刻印 (Front Engraving):</b> 侧边钢印英文字母（如 MIWA 13LA、LA・MA、GOAL LX），<b>刻印即代表确切型号与 CAD 尺寸</b>。</li>
        <li><b>扉厚 / ドア厚:</b> 日本门扇普遍极薄，通常为 <b>33~42mm</b>，标准配件螺栓长度需严格控制在 35mm 以内。</li>
        <li><b>バックセット (Backset):</b> 常用背距为 51mm 或 64mm；窄铝门为 31/38mm。</li>
      </ul>
      <div style="background: #eff6ff; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #1e40af; border-left: 3px solid #3b82f6;">
        <b>💡 机构死穴 (防犯サムターン):</b> MIWA B5 等旋钮必须双侧按压才能转动，普通夹爪会堵转烧毁，必须配备下压联动抓手。
      </div>
    </div>
  </div>

  <!-- 卡片 4：英联邦与澳洲 BS 3621 / AS 4145 -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/uk-nightlatch.jpg" alt="Yale Rim Nightlatch" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">英式 Nightlatch</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/au-lockwood-001.jpg" alt="Lockwood 001 Deadlatch" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">澳洲 Lockwood 001</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-UK/AU · 英澳板块</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">BS 3621 / AS 4145</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">英澳：Rim Nightlatch 与 Lockwood 001 辅助舌</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>Rim Nightlatch (外装夜闩锁):</b> 英国普及率极高，外部为圆柱锁芯，内部为外装大锁壳。背距通常为 40mm 或 60mm。</li>
        <li><b>Auxiliary Latch (辅助舌):</b> 澳洲主力锁具。主舌伸出后，旁边的三角小副舌必须被门框扣板压平，方能进入 deadlatch 状态。</li>
        <li><b>椭圆锁芯 (Oval Cylinder):</b> 澳洲使用独特的 AS 椭圆截面锁芯，无法直接替换常规美标或欧标锁芯。</li>
      </ul>
      <div style="background: #fff7ed; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #9a3412; border-left: 3px solid #ea580c;">
        <b>⚠️ 假锁死隐患:</b> 门缝超过 4mm 时副舌无法被扣板完全压下，智能锁误报已锁，实则一顶即开。
      </div>
    </div>
  </div>

  <!-- 卡片 5：拉美工业板块 ABNT NBR 14913 -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/indigenous/latam-entrada-40.jpg" alt="拉美 40mm 背距锁体" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">Entrada 40mm</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/gallery/latam-rolete-pivotante_real.webp" alt="巴西 PADO Concept 实态" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">PADO 实景</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-LATAM · 拉美板块</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">ABNT NBR 14913</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">西语与拉美：40mm 极窄 Entrada 与碰撞干涉</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>Entrada / Aguja (背距):</b> 住宅普遍使用 <b>40mm 或 45mm 极窄背距</b>。</li>
        <li><b>Espesor de puerta (门厚):</b> 大量薄型夹板门厚度仅 <b>30~35mm</b>。</li>
        <li><b>ABNT 锁芯变体:</b> 锁芯外形虽类似欧标，但拨叉与下部固定螺丝孔径与标准 DIN 存在微小公差差异。</li>
      </ul>
      <div style="background: #fef2f2; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #991b1b; border-left: 3px solid #dc2626;">
        <b>⚠️ 严重干涉红线:</b> 背距 40mm 意味着转轴距门框边缘仅 40mm。若智能锁后壳半宽超过 38mm，旋钮必将直接剐蹭门套封条！
      </div>
    </div>
  </div>

  <!-- 卡片 6：北美板块 ANSI / BHMA A156 -->
  <div class="gallery-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; flex-direction: column;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; background: #0b1120; gap: 1px; height: 180px; position: relative;">
      <div style="position: relative; overflow: hidden; background: #1e293b;">
        <img src="../assets/img/gallery/us-27_real.jpg" alt="北美 Schlage B60 单插销死锁" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">美标 Deadbolt</span>
      </div>
      <div style="position: relative; overflow: hidden; background: #ffffff;">
        <img src="../assets/img/diagrams/US-27_schematic.svg" alt="ANSI Deadbolt 结构" style="width: 100%; height: 100%; object-fit: contain; padding: 6px;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px;">扁平尾轴 1:1</span>
      </div>
      <div style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">IDX-NA · 北美板块</span>
        <span style="background: #0f172a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">ANSI / BHMA A156</span>
      </div>
    </div>
    <div style="padding: 18px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.1rem; color: #0f172a;">北美：60/70mm 双背距与扁平尾轴传动</h3>
      <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 14px; padding-left: 18px; flex: 1;">
        <li><b>Backset (2-3/8" / 2-3/4"):</b> 标准死锁舌自带 <b>60mm 与 70mm 旋转切换调节</b>机构。</li>
        <li><b>Flat Tailpiece (扁平转动尾轴):</b> 内外传动完全依赖一根 1.6mm×4.8mm 的扁平金属拨片。</li>
        <li><b>Core Interchange (可换锁芯):</b> 商业场景采用 SFIC (Small Format Interchangeable Core)。</li>
      </ul>
      <div style="background: #fef2f2; padding: 10px 12px; border-radius: 4px; font-size: 0.78rem; color: #991b1b; border-left: 3px solid #dc2626;">
        <b>⚠️ 门扇下沉红线:</b> 门体重力下沉导致死锁舌与扣板沉孔错位摩擦，普通加装电机扭矩不足会在 3 周内彻底耗尽电池。
      </div>
    </div>
  </div>

</div>
