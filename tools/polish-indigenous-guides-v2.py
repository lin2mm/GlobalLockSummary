# 对 indigenous-guides.md 彻底进行现代工业极简重构：
# 1. 顶部提供 6 大区域清晰的锚点导航条（避免用户向下滚动时眼花）
# 2. 统一左右分栏为：左侧为高清物理图（实物+原理图），右侧为统一格式的 5 项核心指标（中心距/背距/方轴/关键风险/标准）
# 3. 彻底清除凌乱的嵌套样式

for lang in ['zh', 'en']:
    path = f'content/pages/{lang}/indigenous-guides.md'
    is_zh = lang == 'zh'
    
    content = f"""---
title: "{'全球机械门锁工业索引与本土辨锁指南 (Indigenous Lock Guides)' if is_zh else 'Global Indigenous Lock Identification & Engineering Matrix'}"
slug: "indigenous-guides.html"
lang: "{lang}"
---

# {'全球机械门锁工业索引与本土辨锁指南' if is_zh else 'Global Indigenous Lock Standards & Identification Matrix'}

{'面向智能锁研发工程师与海外工程商。深度拆解德奥瑞 (DIN)、法比区 (NF)、日本 (JIS/MIWA)、英澳 (AS/BS)、拉美 (ABNT) 与北美 (ANSI) 6 大工业五金体系的独有尺寸公差、开槽逻辑与加装防呆规则。' if is_zh else 'Engineered for overseas smart lock developers. Consolidating indigenous mechanical tolerances, mortise cutting logic, and error-proofing guidelines across DACH (DIN), France (NF), Japan (JIS), UK/ANZ (AS/BS), LatAm (ABNT), and North America (ANSI).'}

<!-- 顶部 6 大区域快速穿透锚点导航条 -->
<div style="margin: 20px 0 32px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 {'快速直达工业板块:' if is_zh else 'Quick Navigation:'}</span>
  <a href="#de-at-ch" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇩🇪 {'德奥瑞 (DIN)' if is_zh else 'DACH (DIN)'}</a>
  <a href="#fr-be" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇫🇷 {'法比区 (NF)' if is_zh else 'France (NF)'}</a>
  <a href="#jp" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇯🇵 {'日本精工 (JIS/MIWA)' if is_zh else 'Japan (JIS/MIWA)'}</a>
  <a href="#uk-anz" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇦🇺 {'英澳体系 (AS/BS)' if is_zh else 'UK & ANZ (AS/BS)'}</a>
  <a href="#latam" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🌎 {'西语与拉美 (ABNT)' if is_zh else 'Latin America (ABNT)'}</a>
  <a href="#na" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">🇺🇸 {'北美标准 (ANSI)' if is_zh else 'North America (ANSI)'}</a>
</div>

<div style="display: flex; flex-direction: column; gap: 36px; margin: 28px 0;">

  <!-- 1. 德奥瑞 -->
  <div id="de-at-ch" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇩🇪 {'德奥瑞体系：Dornmaß、PZ 规尺与双向应急离合' if is_zh else 'DACH Region: Dornmaß, PZ Dimensions & Dual-Action Clutch'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">DIN 18251 / DIN 18252</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/de-dornmass-pz.png" alt="DIN 18251 Dornmaß PZ" style="width: 100%; height: 100%; object-fit: contain; padding: 8px;" />
        </div>
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/de-gefahrenfunktion.jpg" alt="Gefahrenfunktion Clutch" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Dornmaß ({'背距' if is_zh else 'Backset'}):</b> {'木门标配 55/65mm，型材门 35/40/45mm。' if is_zh else 'Standard 55/65mm for timber, 35-45mm for profile doors.'}</li>
          <li><b>PZ ({'孔距' if is_zh else 'Centres'}):</b> {'入户门标准 72mm，防火门强制 92mm。' if is_zh else 'Standard 72mm for entrance, 92mm for fire doors.'}</li>
          <li><b>Gefahrenfunktion ({'应急功能' if is_zh else 'Emergency Clutch'}):</b> {'锁芯必须具备双向离合，否则内侧常插钥匙断电后室外无法用物理钥匙开门。' if is_zh else 'Cylinder must feature BS dual-clutch; otherwise lockout occurs when motor stalls.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-02 ({'8转9mm 防火套管' if is_zh else '8-to-9mm panic sleeve'}) + ADP-06 ({'钥匙紧定爪' if is_zh else 'key clamp'})
        </div>
      </div>
    </div>
  </div>

  <!-- 2. 法比区 -->
  <div id="fr-be" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇫🇷 {'法比区：Axe 50、Entraxe 70 与 7mm 特殊方轴' if is_zh else 'France & Belgium: Axe 50, Entraxe 70 & 7mm Spindles'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">NF / Vachette 70</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/fr-entraxe-70.png" alt="France Entraxe 70" style="width: 100%; height: 100%; object-fit: contain; padding: 8px;" />
        </div>
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/gallery/eu-19_real.jpg" alt="Bricard Serie 70" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Entraxe ({'中心距' if is_zh else 'Centres'}):</b> {'法国强制 70mm（不同于德国 72mm），混用会导致把手偏斜拉紧。' if is_zh else 'Strict 70mm centres (differs from German 72mm); mixing causes latch binding.'}</li>
          <li><b>Axe ({'背距' if is_zh else 'Backset'}):</b> {'主流为 50mm，老房存在 40mm 浅槽。' if is_zh else 'Standard 50mm, with older buildings featuring 40mm.'}</li>
          <li><b>Fouillot ({'方轴孔' if is_zh else 'Spindle'}):</b> {'7×7mm 方轴孔，智能锁标配 8mm 方轴无法插入，强插会损坏锁体。' if is_zh else '7x7mm square hole. Standard 8mm spindle cannot fit without adapter.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-01 ({'法国 7转8mm 变径套管' if is_zh else '7-to-8mm brass sleeve'})
        </div>
      </div>
    </div>
  </div>

  <!-- 3. 日本精工 -->
  <div id="jp" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇯🇵 {'日本精工：フロント刻印反查与防盗捏合旋钮避坑' if is_zh else 'Japan: Faceplate Engraving Decoding & Anti-Theft Thumbturn'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">JIS A 1510 / MIWA / GOAL</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/jp-miwa-13la.jpg" alt="MIWA 13LA Engraving" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/jp-thumbturn.jpg" alt="MIWA Thumbturn" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>フロント刻印 ({'面板钢印' if is_zh else 'Faceplate Engraving'}):</b> {'侧边刻印「MIWA 13LA / LA・MA」即唯一确定 64mm/51mm 背距与切欠图纸。' if is_zh else 'Marking MIWA 13LA determines 64mm backset & CAD cutting pocket directly.'}</li>
          <li><b>防犯サムターン ({'防盗旋钮' if is_zh else 'Pinch Thumbturn'}):</b> {'内侧旋钮自带双侧按压弹簧片，转动前必须先捏合解锁，直接加装会卡死电机。' if is_zh else 'Thumbturn has spring-loaded pinch tabs. Direct motor drive stalls without release adapter.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-03 ({'MIWA B5 斜坡双侧捏合抓手' if is_zh else 'MIWA B5 pinch gripper'})
        </div>
      </div>
    </div>
  </div>

  <!-- 4. 英澳体系 -->
  <div id="uk-anz" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇦🇺🇬🇧 {'英澳体系：Rim Nightlatch 与 Lockwood 001 辅舌死锁' if is_zh else 'UK & Australia: Rim Nightlatches & Lockwood 001 Deadlatches'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">AS 4145 / BS 3621</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/uk-nightlatch.jpg" alt="UK Nightlatch" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/au-lockwood-001.jpg" alt="Lockwood 001" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Lockwood 001 ({'澳标表面夜闩' if is_zh else 'Australian Deadlatch'}):</b> {'水滴大旋钮（48×34mm），关门时辅助小舌必须完全压入扣盒方可死锁。' if is_zh else 'Teardrop knob (48x34mm); auxiliary bolt must depress fully into strike box.'}</li>
          <li><b>门缝变异假锁死风险:</b> {'门缝超过 3.5mm 会导致辅舌悬空虚假上锁；改装必须搭配可调垫片。' if is_zh else 'Gap >3.5mm causes false lock where door can be carded open.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-05 ({'水滴大旋钮夹具' if is_zh else 'Teardrop turn adapter'}) + ADP-07 ({'扣板垫片' if is_zh else 'Strike shims'}) + ADP-10 ({'修饰大背板' if is_zh else 'Cover plate'})
        </div>
      </div>
    </div>
  </div>

  <!-- 5. 西语与拉美 -->
  <div id="latam" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🌎 {'西语与拉美：40mm 极窄 Entrada 与轴心门碰珠锁' if is_zh else 'Latin America: 40mm Narrow Entrada & Pivot Roller Latches'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">ABNT NBR 14913 / IRAM</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/indigenous/latam-entrada-40.jpg" alt="ABNT 40mm Entrada" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/gallery/latam-rolete-pivotante_real.webp" alt="PADO Pivotante" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Entrada 40mm ({'极窄背距' if is_zh else 'Narrow Backset'}):</b> {'巴西最主流 40mm/45mm 背距，立柱极窄，传统大面板智能锁横向必超宽干涉。' if is_zh else 'Brazil standard 40/45mm backset. Standard wide smart locks collide with door frames.'}</li>
          <li><b>Porta Pivotante ({'轴心门' if is_zh else 'Pivot Doors'}):</b> {'豪宅流行轴心门配碰珠锁 (Rolete)，关门靠阻尼弹簧，智能锁需支持独立碰锁。' if is_zh else 'High-end pivot doors use roller catches; smart locks require standalone latch drive.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-08 ({'薄夹板门防压溃加强圈' if is_zh else 'Door reinforcer'})
        </div>
      </div>
    </div>
  </div>

  <!-- 6. 北美标准 -->
  <div id="na" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 6px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.06);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 16px;">
      <h2 style="margin: 0; font-size: 1.25rem; color: #0f172a;">🇺🇸 {'北美标准：54mm 标准大开孔与扁平尾轴插销' if is_zh else 'North America: 54mm Bore & Flat Tailpiece Deadbolts'}</h2>
      <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">ANSI / BHMA A156.36</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="height: 200px; background: #0f172a; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/gallery/us-27_real.jpg" alt="Schlage B60 Real" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="height: 200px; background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
          <img src="/assets/img/diagrams/US-27_schematic.svg" alt="ANSI Deadbolt Schematic" style="width: 100%; height: 100%; object-fit: contain; padding: 8px;" />
        </div>
      </div>
      <div style="font-size: 0.86rem; color: #475569; line-height: 1.6; display: flex; flex-direction: column; justify-content: space-between;">
        <ul style="margin: 0; padding-left: 18px;">
          <li><b>Cross Bore 2-1/8" ({'54mm 贯穿大孔' if is_zh else '54mm Cross Bore'}):</b> {'全美民居通用标准大圆孔，厚度 35~45mm (1-3/8" ~ 1-3/4")。' if is_zh else 'Universal 54mm cross bore across US homes for door thickness 35-45mm.'}</li>
          <li><b>Tailpiece ({'扁平尾轴' if is_zh else 'Tailpiece Cam'}):</b> {'Schlage (4.5mm 厚) 与 Kwikset (2.2mm 薄) 尾轴截面差异大，需万向阶梯盘。' if is_zh else 'Schlage thick cam vs Kwikset thin cam require universal stepped adapter.'}</li>
        </ul>
        <div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0.78rem; color: #1e40af;">
          💡 <b>{'推荐转接件' if is_zh else 'Recommended Adapter'}:</b> ADP-04 ({'万向阶梯适配盘' if is_zh else 'Universal tailpiece cam'}) + ADP-07 ({'防卡阻垫片' if is_zh else 'Anti-binding shims'})
        </div>
      </div>
    </div>
  </div>

</div>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("indigenous-guides.md completely restructured into modern, clean industrial cards!")
