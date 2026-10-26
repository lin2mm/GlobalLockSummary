zh_patent = """---
title: "Nuki-Like 智能锁专利壁垒排查与海外规避设计指南 (Patent FTO & Workaround)"
slug: "patent-avoidance.html"
lang: "zh"
---

# Nuki-Like 智能锁专利壁垒与海外规避设计 (Patent FTO Guide)

面向出海智能硬件产品经理、机械结构工程师与 IP 法务。深度拆解以 Nuki、August、SwitchBot、Tedee 为代表的**免换锁加装（Retrofit）智能锁**在欧美日重点市场的核心专利布局、权利要求（Claims）保护边界与实战规避设计路径（Design Around）。

<!-- 顶部快速锚点 -->
<div style="margin: 20px 0 28px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 规避专题导航:</span>
  <a href="#nuki-clamping" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">1. 锁芯夹持与背板锁紧规避</a>
  <a href="#key-coupling" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">2. 常插钥匙抓取与离合传动</a>
  <a href="#clutch-disconnect" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">3. 手动优先与脱开离合器</a>
  <a href="#august-tailpiece" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">4. 美标尾轴卡扣与翼形卡爪</a>
  <a href="#checklist" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">5. 出海 FTO 防侵权自查清单</a>
</div>

---

## 核心认知：加装锁专利诉讼重灾区

加装锁的机械专利主要集中在**「三点固定机制」**、**「钥匙/旋钮自适应抓取」**与**「手动/电动双向脱开离合」**。以下为四大核心权利要求特征与破局方案：

---

### 1. 锁芯夹持背板（Mounting Plate Clamping）壁垒与规避
<div id="nuki-clamping" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #2563eb; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #1e3a8a;">⚠️ 专利壁垒点：利用 3 颗平头紧定螺钉直接向欧标锁芯外壳施压夹紧</h3>
  <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 12px; padding-left: 18px;">
    <li><b>竞品方案（Nuki Plate A）:</b> 背板预留欧标水滴孔，套入外露 ≥3mm 的欧标锁芯后，通过侧面/底部的 3 颗内六角平端紧定螺钉直接顶紧锁芯黄铜外壳。</li>
    <li><b>侵权风险:</b> 欧美大量外观与实用新型保护了“多螺钉环向径向顶压固定于锁芯外轮廓”的特征组合。</li>
  </ul>
  <div style="background: #eff6ff; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #1e40af;">
    <b>🛡️ 推荐规避设计路径（Design Around）:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>柔性包覆收紧套圈（Collet / Split Collar）:</b> 放弃独立顶丝，改用类似数控机床弹簧夹头（ER Collet）的 360° 均匀对称收紧圈，通过单一偏心快拆扳手或斜楔收紧。不仅避开点接触权利要求，还能防止顶丝顶伤租客锁芯黄铜表面。</li>
      <li><b>门框面板螺丝共用锚定（Faceplate Rose Anchor）:</b> 卸下原门把手的装饰圆盖（Rose），直接利用门上原有的对穿螺栓固定底座，彻底无需抓取锁芯本身。</li>
    </ol>
  </div>
</div>

---

### 2. 常插钥匙抓取与槽位浮动（Key Gripper & Floating Alignment）
<div id="key-coupling" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #0d9488; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #115e59;">⚠️ 专利壁垒点：弹性夹爪夹紧钥匙柄并允许轴向浮动</h3>
  <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 12px; padding-left: 18px;">
    <li><b>竞品方案:</b> 旋转输出轴内嵌自适应硅胶垫或弹片，将插入的机械钥匙柄强制夹紧在旋转中心。</li>
    <li><b>侵权风险:</b> 围绕“钥匙柄容置槽（Key Bow Cavity）带有轴向限位与自定心弹片”有严密的从属权利要求保护。</li>
  </ul>
  <div style="background: #f0fdfa; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #134e4a;">
    <b>🛡️ 推荐规避设计路径:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>外跨十字拨叉（Oldham Coupling 十字滑块浮动）:</b> 不直接夹紧钥匙柄，而是配置标准的十字滑块联轴器，只传递纯扭矩，容许 ±2.0mm 的径向与角度偏心跳动，彻底消灭轴向摩擦。</li>
      <li><b>模块化插芯替换（Modular Cylinder Head）:</b> 借鉴最新 Nuki Ultra / Tedee 路线，直接向用户提供符合 DIN EN 1303 的预制通用锁芯（Universal Cylinder），从源头规避“转动常插钥匙”的所有专利。</li>
    </ol>
  </div>
</div>

---

### 3. 手动优先与电脱开离合器（Manual Override Clutch）
<div id="clutch-disconnect" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #d97706; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #b45309;">⚠️ 专利壁垒点：减速齿轮箱带有微型舵机/电磁铁强制拉开离合</h3>
  <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 12px; padding-left: 18px;">
    <li><b>竞品方案:</b> 电机驱动时，小型伺服舵机将离合齿轮压入主齿轮环；待机或手动拧旋钮时，弹簧将齿轮推回脱开位置，实现轻巧手感。</li>
  </ul>
  <div style="background: #fffbeb; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #92400e;">
    <b>🛡️ 推荐规避设计路径:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>单向机械超越离合器（One-Way Sprag / Ratchet Clutch）:</b> 采用纯机械式滚柱超越离合器，电机正转驱动锁舌，手动转动时滚柱退回自由状态，完全无需附加电子舵机，降低成本且结构可靠性提高 3 倍。</li>
      <li><b>低反驱阻尼无刷直驱（Brushless Low-Backdrive BLDC）:</b> 采用大扭矩低减速比（≤1:15）无刷电机，常态下反转阻尼只有 0.1 N·m，人手轻推即可转动，从物理上消灭离合器机构。</li>
    </ol>
  </div>
</div>

---

### 4. 美标死锁尾轴适配器（August-Style Tailpiece Wing Latches）
<div id="august-tailpiece" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #dc2626; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #991b1b;">⚠️ 专利壁垒点：侧向双翼翻折卡扣（Wing Latches）</h3>
  <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 12px; padding-left: 18px;">
    <li><b>竞品方案（August）:</b> 背板安装后，机身两侧设计有可向外拉开的翻折翼片（Wing Latches），合上后通过卡钩将机身与背板紧固。</li>
  </ul>
  <div style="background: #fef2f2; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #7f1d1d;">
    <b>🛡️ 推荐规避设计路径:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>卡口旋转自锁环（Bayonet Twist-Lock Ring）:</b> 采用类似单反相机镜头的旋转 45° 螺口自锁环，一旋即紧，彻底避开侧向翻折卡爪专利。</li>
      <li><b>强磁预定位 + 底部隐藏单螺钉（Magnetic Dock + Security Screw）:</b> 采用 4 颗 N52 钕铁硼磁铁辅助吸附定位，底部只需拧紧一颗防盗螺丝即完成刚性锁定。</li>
    </ol>
  </div>
</div>

---

## 5. 出海 FTO 防侵权自查清单 (Patent Clearance Checklist)
<div id="checklist" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px;">
  <ul style="margin: 0; padding-left: 18px; font-size: 0.88rem; color: #334155; line-height: 1.7;">
    <li>[ ] <b>背板安装机构:</b> 是否避开了 Nuki 的“三螺钉径向顶紧锁芯”特征？（建议改为夹头收紧或面板对穿）。</li>
    <li>[ ] <b>机身固定方式:</b> 是否避开了 August 的“双侧翻折翼形夹爪（Wing Latches）”？（建议改为旋转卡扣或磁吸锁紧）。</li>
    <li>[ ] <b>钥匙/旋钮耦合:</b> 是否避开了“自定心弹性卡爪容纳钥匙柄”的权利要求？（建议改为十字滑块浮动连轴）。</li>
    <li>[ ] <b>离合驱动方式:</b> 是否避开了“单独电磁铁/舵机带动齿轮轴向位移”方案？（建议改为机械滚柱超越离合或无刷低反驱）。</li>
    <li>[ ] <b>门状态检测传感器:</b> 是否侵犯了特定门磁霍尔传感器的相对安装结构专利？（建议采用外置飞行时间 ToF 激光或陀螺仪角度姿态闭环）。</li>
  </ul>
</div>
"""

with open('content/pages/zh/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(zh_patent)

en_patent = """---
title: "Nuki-Like Smart Lock Patent Avoidance & FTO Engineering Guide"
slug: "patent-avoidance.html"
lang: "en"
---

# Nuki-Like Smart Lock Patent Avoidance & FTO Engineering Guide

Designed for overseas smart hardware PMs, mechanical engineers, and IP legal counsel. Deconstructing core patent thickets, claims boundaries, and design-around pathways for **retrofit smart locks** (Nuki, August, SwitchBot, Tedee) across Europe, North America, and Japan.

<!-- Quick Nav -->
<div style="margin: 20px 0 28px; padding: 12px 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
  <span style="font-weight: 700; font-size: 0.85rem; color: #334155;">📍 Navigation:</span>
  <a href="#nuki-clamping" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">1. Cylinder Clamping Workaround</a>
  <a href="#key-coupling" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">2. Key Gripper & Floating Coupler</a>
  <a href="#clutch-disconnect" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">3. Manual Override Clutch</a>
  <a href="#august-tailpiece" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">4. ANSI Tailpiece Wing Latches</a>
  <a href="#checklist" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;">5. Global FTO Checklist</a>
</div>

---

## High-Risk Litigation Zones for Smart Retrofit Locks

Retrofit smart lock patents predominantly concentrate on **three-point mounting mechanisms**, **key/thumbturn adaptive grippers**, and **dual-action decoupling clutches**.

### 1. Mounting Plate Cylinder Clamping Design-Around
<div id="nuki-clamping" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #2563eb; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #1e3a8a;">⚠️ Core Claim: Fastening a mounting plate to an Euro cylinder using 3 set screws</h3>
  <ul style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0 0 12px; padding-left: 18px;">
    <li><b>Competitor Baseline (Nuki Plate A):</b> Employs three allen set screws directly pressing radially against the brass euro cylinder profile.</li>
  </ul>
  <div style="background: #eff6ff; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #1e40af;">
    <b>🛡️ Recommended Workaround Pathways:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>360° Split Collar Collet:</b> Replace individual screws with an ER-collet-inspired concentric clamping sleeve with a quick-release cam lever. Eliminates screw marring on the tenant's cylinder while bypassing point-pressure claim limitations.</li>
      <li><b>Rose Escutcheon Through-Bolt Mounting:</b> Mount directly to existing through-door bolt holes behind the decorative rose trim.</li>
    </ol>
  </div>
</div>

### 2. Key Gripper & Floating Misalignment Coupling
<div id="key-coupling" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #0d9488; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #115e59;">⚠️ Core Claim: Spring-loaded resilient clips gripping key bow with axial play</h3>
  <div style="background: #f0fdfa; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #134e4a;">
    <b>🛡️ Recommended Workaround Pathways:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>Oldham Coupling (Cross-Slide Floating Link):</b> Transmits pure torque with ±2.0mm radial play, preventing axial friction and bypassing key bow clamping claims.</li>
      <li><b>Modular Euro Cylinder Swap:</b> Bundle an EN 1303 universal modular cylinder (Nuki Ultra / Tedee approach) rather than gripping inserted keys.</li>
    </ol>
  </div>
</div>

### 3. Manual Override Clutch Decoupling
<div id="clutch-disconnect" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #d97706; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #b45309;">⚠️ Core Claim: Gearbox with dedicated servo or solenoid shifting clutch gear axially</h3>
  <div style="background: #fffbeb; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #92400e;">
    <b>🛡️ Recommended Workaround Pathways:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>Mechanical Sprag / Roller Overrunning Clutch:</b> Unidirectional driving without any electrical actuators.</li>
      <li><b>Ultra-Low Backdrive Brushless DC Motor:</b> Low gear-ratio BLDC drive (≤1:15) with only 0.1 N·m backdrive drag, allowing effortless hand-turning without a mechanical clutch.</li>
    </ol>
  </div>
</div>

### 4. ANSI Deadbolt Wing Latches
<div id="august-tailpiece" style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #dc2626; border-radius: 6px; padding: 18px; margin: 16px 0 24px;">
  <h3 style="margin: 0 0 10px; font-size: 1.1rem; color: #991b1b;">⚠️ Core Claim: Lateral swinging wing latches clamping motor to mounting plate</h3>
  <div style="background: #fef2f2; padding: 12px 14px; border-radius: 6px; font-size: 0.82rem; color: #7f1d1d;">
    <b>🛡️ Recommended Workaround Pathways:</b>
    <ol style="margin: 6px 0 0; padding-left: 18px;">
      <li><b>45° Bayonet Twist-Lock Ring:</b> Quarter-turn interlocking ring similar to camera lens mounts.</li>
      <li><b>Neodymium Magnetic Alignment + Concealed Screw:</b> Magnetic pre-docking followed by a single mechanical security bolt.</li>
    </ol>
  </div>
</div>

---

## 5. Global FTO Clearance Checklist
<div id="checklist" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px;">
  <ul style="margin: 0; padding-left: 18px; font-size: 0.88rem; color: #334155; line-height: 1.7;">
    <li>[ ] <b>Cylinder Attachment:</b> Avoided 3-screw radial clamp? (Use split collar or escutcheon through-bolt).</li>
    <li>[ ] <b>Chassis Fixing:</b> Avoided dual lateral wing latches? (Use bayonet twist-lock or magnetic docking).</li>
    <li>[ ] <b>Key Gripping:</b> Avoided spring-loaded key bow clamping? (Use Oldham coupling or modular cylinder).</li>
    <li>[ ] <b>Clutch Mechanism:</b> Avoided motorized axial gear shifting? (Use overrunning clutch or low-backdrive BLDC).</li>
    <li>[ ] <b>Door Sensor:</b> Avoided patented magnetic alignment structures? (Use ToF laser distance or IMU gyro).</li>
  </ul>
</div>
"""

with open('content/pages/en/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(en_patent)

print("Created content/pages/zh/patent-avoidance.md and en/patent-avoidance.md")
