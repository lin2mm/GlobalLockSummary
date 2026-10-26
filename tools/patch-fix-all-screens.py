import re

# 1. 修复 zh/patent-avoidance.md 的 title 和 h1 重复
with open('content/pages/zh/patent-avoidance.md', 'r', encoding='utf-8') as f:
    zh_patent = f.read()

zh_patent = zh_patent.replace(
    'title: "后装智能锁专利壁垒排查与海外规避设计指南 (Patent FTO) (Patent FTO & Workaround)"',
    'title: "后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)"'
)
zh_patent = zh_patent.replace(
    '# 后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide) (Patent FTO Guide)',
    '# 后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)'
)
with open('content/pages/zh/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(zh_patent)
print("Fixed zh/patent-avoidance.md duplicate titles!")

# 2. 修复 en/patent-avoidance.md
with open('content/pages/en/patent-avoidance.md', 'r', encoding='utf-8') as f:
    en_patent = f.read()

en_patent = en_patent.replace(
    'title: "Retrofit Smart Lock Patent Avoidance & FTO Guide & FTO Engineering Guide"',
    'title: "Retrofit Smart Lock Patent Avoidance & FTO Guide"'
)
en_patent = en_patent.replace(
    '# Retrofit Smart Lock Patent Avoidance & FTO Guide & FTO Engineering Guide',
    '# Retrofit Smart Lock Patent Avoidance & FTO Guide'
)
with open('content/pages/en/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(en_patent)
print("Fixed en/patent-avoidance.md duplicate titles!")

# 3. 优化 zh/indigenous-guides.md 中的蓝色大渐变横幅，改为 ASSA ABLOY 墨黑极简工业风
with open('content/pages/zh/indigenous-guides.md', 'r', encoding='utf-8') as f:
    zh_indig = f.read()

# 替换大横幅
old_banner_zh = """<!-- 核心排序依据显式声明横幅 -->
<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #f8fafc; border-left: 5px solid #38bdf8; padding: 14px 18px; border-radius: 8px; margin: 18px 0 24px; box-shadow: 0 4px 12px rgba(15,23,42,0.08);">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
    <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">核心排序依据 · Engineering Architecture</span>
    <span style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">出海加装复杂度与工程暗坑深度递减 (Engineering Complexity Decrescendo)</span>
  </div>
  <p style="margin: 0; font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
    本索引并非按地理位置或经济体量随意排列，而是严格基于海外免换锁加装（Retrofit）的<b>机械适配壁垒、锁芯反锁困人风险、抬把手多点联动阻尼与开模离散度</b>自上而下递减排列。越靠顶部的板块（如德欧瑞 DIN、法比 NF、中东海湾 SASO），出海工程暗坑越深、售后退货率越高；越靠底部的板块（如北美 ANSI），标准化与免工具加装成熟度越高。
  </p>
</div>"""

new_banner_zh = """<div style="margin: 14px 0 20px; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px;">
  <span style="font-weight: 700; font-size: 0.82rem; color: #0f172a;">★ 排序依据：</span>
  <span style="font-size: 0.82rem; color: #475569;">严格基于海外后装加装（Retrofit）的<b>机械适配壁垒、锁芯反锁风险与工程暗坑深度递减</b>排列（德奥瑞 DIN ➔ 法比 NF ➔ 北美 ANSI）。</span>
</div>"""

if old_banner_zh in zh_indig:
    zh_indig = zh_indig.replace(old_banner_zh, new_banner_zh)
    print("Replaced loud banner in zh/indigenous-guides.md with ASSA ABLOY clean block!")
else:
    print("old_banner_zh not found in zh/indigenous-guides.md")

with open('content/pages/zh/indigenous-guides.md', 'w', encoding='utf-8') as f:
    f.write(zh_indig)

# 4. 同样排查 en/indigenous-guides.md
with open('content/pages/en/indigenous-guides.md', 'r', encoding='utf-8') as f:
    en_indig = f.read()

old_banner_en = """<!-- Engineering Ranking Architecture Banner -->
<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #f8fafc; border-left: 5px solid #38bdf8; padding: 14px 18px; border-radius: 8px; margin: 18px 0 24px; box-shadow: 0 4px 12px rgba(15,23,42,0.08);">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
    <span style="background: #0284c7; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">Engineering Architecture</span>
    <span style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">Engineering Complexity & Pitfall Depth Decrescendo</span>
  </div>
  <p style="margin: 0; font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
    This index is not arranged geographically, but strictly based on retrofit mechanical barriers, lockout hazards, multipoint lift-to-lock damping, and tooling dispersion in descending order.
  </p>
</div>"""

new_banner_en = """<div style="margin: 14px 0 20px; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px;">
  <span style="font-weight: 700; font-size: 0.82rem; color: #0f172a;">★ Sorting Criteria:</span>
  <span style="font-size: 0.82rem; color: #475569;">Arranged in descending order of <b>retrofit mechanical barriers, lockout hazards, and engineering pitfall depth</b> (DACH DIN ➔ France NF ➔ Americas ANSI).</span>
</div>"""

if old_banner_en in en_indig:
    en_indig = en_indig.replace(old_banner_en, new_banner_en)
    print("Replaced loud banner in en/indigenous-guides.md!")
else:
    print("old_banner_en not found in en/indigenous-guides.md")

with open('content/pages/en/indigenous-guides.md', 'w', encoding='utf-8') as f:
    f.write(en_indig)

# 5. install-gallery.html 检查 8 大板块支持
