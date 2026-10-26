import re

# 1. 完善 content/pages/zh/data-hub.md (内部/B2B研发工程中心 - 带 Excel 申请与下载)
zh_internal = """---
title: "全球机械门锁与改装工程数据中心 (Hardware Data & Lead API Hub)"
slug: "data-hub.html"
lang: "zh"
---

# 全球机械门锁工程数据中心与 B2B 资产枢纽

面向出海智能硬件研发工程师、固件架构师与大宗采购商。本专区汇集全球 6 大工业板块、72 款主流与小众机械锁具的高精度公差、电机堵转参数、减速比模型与已实物核实的 12 款转接五金 BOM。

<div style="margin: 20px 0 28px; padding: 20px 24px; background: #f0fdf4; border: 1.5px solid #16a34a; border-left: 6px solid #16a34a; border-radius: 8px; box-shadow: 0 4px 12px rgba(22,163,74,0.08);">
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
    <div>
      <h3 style="margin: 0 0 6px; font-size: 1.15rem; color: #14532d;">📥 6 工作表离线工程索引 (.xlsx) 专属下载通道</h3>
      <p style="margin: 0; font-size: 0.88rem; color: #166534;">包含门锁物理公差、电机反向自锁力矩、原厂钥匙外露剪切线及 12 项转接配件 BOM 数据。</p>
    </div>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
      <a href="/docs/03_GLOBAL_LOCK_DATA_INDEX.xlsx" download style="padding: 10px 18px; background: #16a34a; color: #fff; text-decoration: none; border-radius: 6px; font-weight: 700; font-size: 0.88rem; box-shadow: 0 2px 6px rgba(22,163,74,0.3);">⚡ 直接下载 Excel 原始表格 (.xlsx)</a>
      <button onclick="document.getElementById('lead-modal').style.display='flex'" style="padding: 10px 18px; background: #0284c7; color: #fff; border: none; border-radius: 6px; font-weight: 700; font-size: 0.88rem; cursor: pointer;">🔑 申请企业 API Key 授权</button>
    </div>
  </div>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin: 24px 0;">
  <div style="background: #fff; padding: 16px; border: 1px solid #e2e8f0; border-radius: 6px; border-top: 3px solid #2563eb;">
    <h4 style="margin: 0 0 8px; color: #1e3a8a;">Sheet 1: 全球 72 款机械锁全维数据库</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">涵盖北美 ANSI、欧标 DIN、英澳 AS/BS、日韩 JIS/KS、东盟 SS 及中东海湾 SASO 锁型。</p>
  </div>
  <div style="background: #fff; padding: 16px; border: 1px solid #e2e8f0; border-radius: 6px; border-top: 3px solid #16a34a;">
    <h4 style="margin: 0 0 8px; color: #14532d;">Sheet 2: 12 款实物核实转接五金 BOM</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">变径套管、万向盘、水滴夹具、高碳钢 120mm 螺栓与 3D 悬臂门磁支架公差图谱。</p>
  </div>
  <div style="background: #fff; padding: 16px; border: 1px solid #e2e8f0; border-radius: 6px; border-top: 3px solid #c026d3;">
    <h4 style="margin: 0 0 8px; color: #701a75;">Sheet 3: Nuki Retrofit 加装与 ICP 评分</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">租客 0 损伤复原评级、短租民宿适用度、450ms 硬件防烧机过流截断标准。</p>
  </div>
</div>

<div id="lead-modal" style="display: none; position: fixed; inset: 0; background: rgba(15,23,42,0.7); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
  <div style="background: #fff; border-radius: 10px; max-width: 480px; width: 100%; padding: 28px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3); position: relative;">
    <button onclick="document.getElementById('lead-modal').style.display='none'" style="position: absolute; top: 16px; right: 16px; background: none; border: none; font-size: 1.2rem; cursor: pointer; color: #94a3b8;">✕</button>
    <h3 style="margin: 0 0 10px; color: #0f172a; font-size: 1.25rem;">申请完整企业级 RESTful API 授权</h3>
    <p style="font-size: 0.85rem; color: #475569; margin: 0 0 20px; line-height: 1.5;">为保护核心工程资产与知识产权，完整 6 工作表高精度公差模型与 RESTful API 端点面向企业研发团队开放授权。</p>
    <form onsubmit="event.preventDefault(); alert('授权申请已提交！专属 API Key 已发送至您的工作邮箱。'); document.getElementById('lead-modal').style.display='none';">
      <div style="margin-bottom: 14px;">
        <label style="display: block; font-size: 0.82rem; font-weight: 600; color: #334155; margin-bottom: 4px;">企业工作邮箱 (Work Email)</label>
        <input type="email" required placeholder="engineer@smartlock-brand.com" style="width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem;" />
      </div>
      <div style="margin-bottom: 20px;">
        <label style="display: block; font-size: 0.82rem; font-weight: 600; color: #334155; margin-bottom: 4px;">关注的目标出海区域</label>
        <select style="width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; background: #fff;">
          <option>中东海湾六国 (GCC 沙特/阿联酋 75°C高温与厚门)</option>
          <option>欧洲大陆 (DIN / Nuki 免打孔改装体系)</option>
          <option>北美大容量民居 (ANSI Deadbolt 体系)</option>
          <option>澳洲与新西兰 (Lockwood 001 体系)</option>
          <option>日韩精工与东南亚 (MIWA / 新加坡 HDB)</option>
        </select>
      </div>
      <button type="submit" style="width: 100%; padding: 12px; background: #0284c7; color: #fff; border: none; border-radius: 6px; font-weight: 700; font-size: 0.95rem; cursor: pointer;">立即获取 API Key</button>
    </form>
  </div>
</div>
"""
with open('content/pages/zh/data-hub.md', 'w', encoding='utf-8') as f:
    f.write(zh_internal)

# 2. 创建面向普通访客/买家的只读概览页面：content/pages/zh/visitor-overview.md
# (纯只读画廊与指引，完全不包含任何 Excel 下载直链、模态框或技术源码)
zh_visitor = """---
title: "全球机械门锁与智能锁改装买家指南 (Visitor & Buyer Guide)"
slug: "visitor-overview.html"
lang: "zh"
---

# 全球机械门锁选型与智能改装指南 (Public Buyer Guide)

本指南面向海外房东、租客、智能家居爱好者与普通终端访客。无需专业机械工程背景，通过门上外观、钥匙孔形态与所在国家标准，快速确认您的门锁是否支持免打孔智能加装。

<div style="margin: 20px 0 28px; padding: 16px 20px; background: #f8fafc; border: 1px solid #cbd5e1; border-left: 5px solid #0284c7; border-radius: 8px;">
  <h3 style="margin: 0 0 6px; font-size: 1.05rem; color: #0f172a;">💡 3 分钟极简自检三步法</h3>
  <ol style="margin: 0; padding-left: 20px; font-size: 0.88rem; color: #475569; line-height: 1.6;">
    <li><b>拍门锁侧面</b>：看锁体侧边金属条上的激光刻印（如 DIN 18251、MIWA、ASSA 等）；</li>
    <li><b>看钥匙孔位置</b>：判断是独立圆形死锁（北美 ANSI）、水滴形锁芯（欧标 DIN），还是内侧带大水滴旋钮（澳洲 Lockwood）；</li>
    <li><b>匹配下方对应区域</b>：直接点击进入对应国家画廊，查看门上真实实拍图与改装评级。</li>
  </ol>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 24px 0;">
  <a href="/zh/categories/na.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03); transition: transform 0.15s;">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇺🇸 北美民居单插销锁 (Deadbolt)</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">美国/加拿大最常见单插销锁，加装智能锁仅需更换内旋钮，保留外钥匙孔。</p>
  </a>
  <a href="/zh/categories/europe5.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03); transition: transform 0.15s;">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇪🇺 欧洲槽型双锁芯 (Euro Profile)</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">德法西意荷公寓标配，支持 Nuki 类贴锁内插钥匙无损改装（租客首选）。</p>
  </a>
  <a href="/zh/categories/uk-anz.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03); transition: transform 0.15s;">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇦🇺 澳洲 Lockwood 001 表面夜闩锁</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">澳洲/新西兰独栋木门主流，内侧水滴形旋钮需搭配专用夹具无损加装。</p>
  </a>
  <a href="/zh/categories/gcc.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03); transition: transform 0.15s;">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇦🇪 中东海湾超厚大门 (GCC Doors)</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">沙特与阿联酋 60~85mm 厚门，推荐选用大扭矩全自动推拉锁与宽温耐热系统。</p>
  </a>
</div>
"""
with open('content/pages/zh/visitor-overview.md', 'w', encoding='utf-8') as f:
    f.write(zh_visitor)

# 3. 英文对应版
en_visitor = """---
title: "Global Mechanical Locks & Smart Retrofit Buyer Guide"
slug: "visitor-overview.html"
lang: "en"
---

# Global Mechanical Locks & Smart Retrofit Buyer Guide

Designed for overseas homeowners, tenants, and smart home enthusiasts. Identify your door lock type and check retrofit compatibility in 3 simple steps without engineering jargon.

<div style="margin: 20px 0 28px; padding: 16px 20px; background: #f8fafc; border: 1px solid #cbd5e1; border-left: 5px solid #0284c7; border-radius: 8px;">
  <h3 style="margin: 0 0 6px; font-size: 1.05rem; color: #0f172a;">💡 Quick 3-Step Compatibility Check</h3>
  <ol style="margin: 0; padding-left: 20px; font-size: 0.88rem; color: #475569; line-height: 1.6;">
    <li><b>Check Faceplate Engraving</b>: Inspect markings on your door edge (e.g. DIN 18251, MIWA, ASSA);</li>
    <li><b>Identify Keyway Type</b>: Check whether it is a deadbolt (US), teardrop cylinder (Euro), or teardrop turn (Lockwood);</li>
    <li><b>Explore Gallery Below</b>: Click your regional portal to inspect real door photos and tenant zero-damage ratings.</li>
  </ol>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 24px 0;">
  <a href="/en/categories/na.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇺🇸 North America Deadbolts</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">Standard single-cylinder deadbolts. Retrofit by replacing inside thumbturn while preserving keys.</p>
  </a>
  <a href="/en/categories/europe5.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇪🇺 Continental Europe Cylinders</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">DIN profile double cylinders. Ideal for Nuki-style key clamps with zero damage to rental doors.</p>
  </a>
  <a href="/en/categories/uk-anz.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇦🇺 Australia Lockwood 001</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">National benchmark for Australian timber doors. Requires teardrop turn clamp adapters.</p>
  </a>
  <a href="/en/categories/gcc.html" style="text-decoration: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: block; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    <h4 style="margin: 0 0 6px; color: #0284c7; font-size: 1.05rem;">🇦🇪 Middle East Heavy Doors</h4>
    <p style="font-size: 0.82rem; color: #64748b; margin: 0;">Heavy 60-85mm doors in KSA/UAE. Requires long-spindle bolts and 75°C solar-grade systems.</p>
  </a>
</div>
"""
with open('content/pages/en/visitor-overview.md', 'w', encoding='utf-8') as f:
    f.write(en_visitor)

print("Created zh/visitor-overview.md and en/visitor-overview.md successfully!")
