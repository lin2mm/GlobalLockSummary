with open('content/pages/zh/indigenous-guides.md', 'r', encoding='utf-8') as f:
    zh = f.read()

zh_banner = """<!-- 核心排序依据显式声明横幅 -->
<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #f8fafc; border-left: 5px solid #38bdf8; padding: 14px 18px; border-radius: 8px; margin: 18px 0 24px; box-shadow: 0 4px 12px rgba(15,23,42,0.08);">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
    <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">核心排序依据 · Engineering Architecture</span>
    <span style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">出海加装复杂度与工程暗坑深度递减 (Engineering Complexity Decrescendo)</span>
  </div>
  <p style="margin: 0; font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
    本索引并非按地理位置或经济体量随意排列，而是严格基于海外免换锁加装（Retrofit）的<b>机械适配壁垒、锁芯反锁困人风险、抬把手多点联动阻尼与开模离散度</b>自上而下递减排列。越靠顶部的板块（如德欧瑞 DIN、法比 NF、中东海湾 SASO），出海工程暗坑越深、售后退货率越高；越靠底部的板块（如北美 ANSI），标准化与免工具加装成熟度越高。
  </p>
</div>
"""

if "出海加装复杂度与工程暗坑深度递减" not in zh:
    zh = zh.replace("<!-- 顶部 8 大工业板块快速穿透锚点导航条", zh_banner + "\n<!-- 顶部 8 大工业板块快速穿透锚点导航条")
    with open('content/pages/zh/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(zh)
    print("Added complexity decrescendo banner to zh/indigenous-guides.md")

with open('content/pages/en/indigenous-guides.md', 'r', encoding='utf-8') as f:
    en = f.read()

en_banner = """<!-- Engineering Complexity Decrescendo Sorting Banner -->
<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #f8fafc; border-left: 5px solid #38bdf8; padding: 14px 18px; border-radius: 8px; margin: 18px 0 24px; box-shadow: 0 4px 12px rgba(15,23,42,0.08);">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
    <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">Core Architecture · Engineering Rationale</span>
    <span style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">Engineering Complexity & Field Pitfall Depth Decrescendo</span>
  </div>
  <p style="margin: 0; font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
    This directory is systematically sequenced by <b>mechanical retrofit barriers, lockout risks, multipoint lift-to-lock kinematics, and dimensional tolerances</b> in descending order. Divisions near the top (DIN, NF, GCC SASO) present the steepest technical hurdles and warranty claim risks; divisions toward the bottom (ANSI/BHMA) feature the highest level of universal standardization and drop-in simplicity.
  </p>
</div>
"""

if "Engineering Complexity & Field Pitfall Depth Decrescendo" not in en:
    en = en.replace("<!-- Top 8 Divisions Quick Jump Bar", en_banner + "\n<!-- Top 8 Divisions Quick Jump Bar")
    with open('content/pages/en/indigenous-guides.md', 'w', encoding='utf-8') as f:
        f.write(en)
    print("Added complexity decrescendo banner to en/indigenous-guides.md")

