import json

def generate_adapters_pages():
    with open('content/catalog/adapters-bom.json', 'r', encoding='utf-8') as f:
        adapters = json.load(f)

    # 1. 生成 zh/adapters.md
    zh_cards = []
    for a in adapters:
        verified_badge = '<span style="background: #16a34a; color: #fff; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">✓ 100% 实物核实</span>'
        diy_badge = f'<span style="background: {"#0284c7" if a["diy3dPrintReady"] else "#64748b"}; color: #fff; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 3px;">{"3D打印适配" if a["diy3dPrintReady"] else "强制金属件"}</span>'

        card = f"""  <div class="gallery-card" id="{a['id'].lower()}" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 4px solid #0284c7; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(2,132,199,0.06); display: flex; flex-direction: column;">
    <div style="height: 190px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="../{a['image']}" alt="{a['name']}" style="width: 100%; height: 100%; object-fit: contain; padding: 12px; background: #0f172a;" />
      <div style="position: absolute; top: 8px; left: 8px; display: flex; gap: 5px;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">{a['id']} · 核实件</span>
        {verified_badge}
      </div>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.75); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">{a['targetRegion']}</span>
    </div>
    <div style="padding: 16px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem; color: #0f172a;">{a['name']}</h3>
      <p style="font-size: 0.84rem; color: #475569; line-height: 1.5; margin: 0 0 10px; flex: 1;">{a['problemSolved']}</p>
      <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #334155; border-left: 3px solid #0284c7; margin-bottom: 8px;">
        <div><b>关键公差与尺寸:</b> {a['criticalTolerance']}</div>
        <div style="margin-top: 4px;"><b>推荐材质:</b> {a['materialRecommendation']}</div>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #64748b; border-top: 1px solid #f1f5f9; padding-top: 8px;">
        <span>工件要求: {diy_badge}</span>
        <span style="color: #15803d; font-weight: 600;">{a['verificationStatus']}</span>
      </div>
    </div>
  </div>"""
        zh_cards.append(card)

    zh_content = f"""---
title: "全球智能锁 Retrofit 标准转接件 BOM (Hardware Adapters)"
slug: "adapters.html"
lang: "zh"
---

# 标准转接工具与五金配件库 (Hardware Adapters & BOM)

面向出海智能硬件与五金研发工程师，所有转接件均经过**实物图纸对照、真实锁体尺寸试装与力矩剪切核实 (100% Verified)**。采用标准双列画廊流模式呈现，直观展示变径套管、防撬卡爪、万向适配盘与加固垫片。

<div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; font-size: 0.85rem; color: #166534; line-height: 1.5;">
  <b>📋 转接件全量工程核实清单 (Total {len(adapters)} Items):</b> 涵盖法国 7转8、德国 8转9、日本 MIWA B5 捏合爪、北美万向盘、澳洲 Lockwood 水滴夹具、欧规钥匙紧定套、门框可调垫片组与薄门防压溃加强垫。严禁在受力方轴部件使用易脆锌合金。
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; margin: 28px 0;">
{"".join(zh_cards)}
</div>
"""
    with open('content/pages/zh/adapters.md', 'w', encoding='utf-8') as f:
        f.write(zh_content)

    # 2. 生成 en/adapters.md
    en_cards = []
    for a in adapters:
        verified_badge = '<span style="background: #16a34a; color: #fff; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 3px;">✓ 100% Verified</span>'
        diy_badge = f'<span style="background: {"#0284c7" if a["diy3dPrintReady"] else "#64748b"}; color: #fff; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 3px;">{"3D Print Ready" if a["diy3dPrintReady"] else "Mandatory Metal"}</span>'

        card = f"""  <div class="gallery-card" id="{a['id'].lower()}" style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 4px solid #0284c7; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(2,132,199,0.06); display: flex; flex-direction: column;">
    <div style="height: 190px; background: #0b1120; overflow: hidden; position: relative;">
      <img src="../{a['image']}" alt="{a['name']}" style="width: 100%; height: 100%; object-fit: contain; padding: 12px; background: #0f172a;" />
      <div style="position: absolute; top: 8px; left: 8px; display: flex; gap: 5px;">
        <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 3px;">{a['id']} · Verified</span>
        {verified_badge}
      </div>
      <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.75); color: #cbd5e1; font-size: 0.68rem; padding: 2px 6px; border-radius: 2px;">{a['targetRegion']}</span>
    </div>
    <div style="padding: 16px; flex: 1; display: flex; flex-direction: column;">
      <h3 style="margin: 0 0 8px; font-size: 1.05rem; color: #0f172a;">{a['name']}</h3>
      <p style="font-size: 0.84rem; color: #475569; line-height: 1.5; margin: 0 0 10px; flex: 1;">{a['problemSolved']}</p>
      <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #334155; border-left: 3px solid #0284c7; margin-bottom: 8px;">
        <div><b>Tolerance & Dimensions:</b> {a['criticalTolerance']}</div>
        <div style="margin-top: 4px;"><b>Material:</b> {a['materialRecommendation']}</div>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #64748b; border-top: 1px solid #f1f5f9; padding-top: 8px;">
        <span>Fabrication: {diy_badge}</span>
        <span style="color: #15803d; font-weight: 600;">{a['verificationStatus']}</span>
      </div>
    </div>
  </div>"""
        en_cards.append(card)

    en_content = f"""---
title: "Global Smart Lock Retrofit Standard Hardware Adapters & BOM"
slug: "adapters.html"
lang: "en"
---

# Global Standard Hardware Adapters & BOM

Engineered for overseas smart lock developers. All adapters have undergone **100% CAD verification, physical fitment tests, and shear torque stress validation**. Presented in standard 2-column image-dominant gallery style.

<div style="margin: 16px 0 24px; padding: 12px 16px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; font-size: 0.85rem; color: #166534; line-height: 1.5;">
  <b>📋 Engineering Verification Summary (Total {len(adapters)} Items):</b> Covering French 7-to-8mm sleeves, German 8-to-9mm panic sleeves, MIWA B5 pinch grippers, ANSI tailpiece cams, Lockwood teardrop adapters, Euro key clamps, adjustable strike shims, and plywood door reinforcers.
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; margin: 28px 0;">
{"".join(en_cards)}
</div>
"""
    with open('content/pages/en/adapters.md', 'w', encoding='utf-8') as f:
        f.write(en_content)

    print("Updated zh/adapters.md and en/adapters.md successfully!")

if __name__ == '__main__':
    generate_adapters_pages()
