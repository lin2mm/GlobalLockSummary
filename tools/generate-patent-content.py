# -*- coding: utf-8 -*-

zh_content = """---
title: "后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)"
slug: "patent-avoidance.html"
lang: "zh"
---

<!-- ASSA ABLOY 工规信息头 -->
<div class="spec-hero-meta">
  <span><b>适用对象:</b> 硬件PM / 结构工程师 / IP法务</span>
  <span><b>保护领域:</b> 免换锁/无损后装 (Retrofit Smart Lock)</span>
  <span><b>法域涵盖:</b> EPO (欧洲) / USPTO (美国) / JPO (日本)</span>
  <span><b>合规底线:</b> FTO 自由实施不落入独权保护范围</span>
</div>

<!-- 5 大核心规避专题导航卡片阵列 (单行5列等宽网格，告别胶囊堆叠) -->
<nav class="spec-topic-nav" aria-label="专利规避专题导航">
  <a class="spec-topic-pill" href="#nuki-clamping">
    <span class="spec-topic-pill__num">01 / CLAMPING</span>
    <span class="spec-topic-pill__title">锁芯夹持背板</span>
  </a>
  <a class="spec-topic-pill" href="#key-coupling">
    <span class="spec-topic-pill__num">02 / COUPLING</span>
    <span class="spec-topic-pill__title">常插钥匙浮动</span>
  </a>
  <a class="spec-topic-pill" href="#clutch-disconnect">
    <span class="spec-topic-pill__num">03 / CLUTCH</span>
    <span class="spec-topic-pill__title">手动优先离合</span>
  </a>
  <a class="spec-topic-pill" href="#august-tailpiece">
    <span class="spec-topic-pill__num">04 / TAILPIECE</span>
    <span class="spec-topic-pill__title">美标尾轴卡扣</span>
  </a>
  <a class="spec-topic-pill" href="#checklist">
    <span class="spec-topic-pill__num">05 / AUDIT</span>
    <span class="spec-topic-pill__title">FTO 自查清单</span>
  </a>
</nav>

## 核心诉讼重灾区与规避工程图谱

后装智能锁海外诉讼集中于**「三点固定机制」**、**「钥匙自适应抓取」**与**「手动/电动双向脱开离合」**。以下为四大核心权利要求特征与突破方案：

---

### 1. 锁芯夹持背板 (Mounting Plate Clamping)
<div id="nuki-clamping" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 专题 01：欧标锁芯环向平端顶丝夹持机构规避</h3>
    <span class="spec-card__badge spec-card__badge--red">EPO / EP3014032 核心壁垒</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ 侵权红线特征 (Claims)</div>
        <div class="spec-box__text">
          <b>竞品基准 (Nuki Plate A):</b> 背板开欧标水滴孔，套入外露 ≥3mm 锁芯，侧面或底面设 3 颗平端紧定内六角顶丝，向锁芯黄铜壳体施加径向点接触顶紧力。
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ 推荐规避工程路径 (Design Around)</div>
        <div class="spec-box__text">
          <b>① 柔性包覆收紧套圈 (Collet):</b> 采用数控机床弹簧夹头（ER Collet）360° 均匀抱紧，无独立顶丝，彻底避开点压权利要求且不伤原锁；<br>
          <b>② 门面装饰盖穿孔锚定 (Rose Anchor):</b> 卸下原把手饰盖，借用门扇对穿螺栓，完全无需接触或夹持锁芯。
        </div>
      </div>
    </div>
    <!-- 1:1 专利权同等对比图 -->
    <div style="margin-top: 12px; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
      <img src="/assets/img/patent/patent-clamping-comparison.svg" alt="锁芯夹持专利对比图" style="width: 100%; height: auto; display: block;" loading="lazy" />
    </div>
  </div>
</div>

---

### 2. 常插钥匙抓取与槽位浮动 (Key Gripper & Floating Coupler)
<div id="key-coupling" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 专题 02：钥匙柄自定心弹性夹紧与浮动机构规避</h3>
    <span class="spec-card__badge spec-card__badge--red">EP3175062 / US9822557 核心壁垒</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ 侵权红线特征 (Claims)</div>
        <div class="spec-box__text">
          <b>竞品基准:</b> 驱动轴腔内嵌自适应硅胶套或弹片，对插入的机械钥匙柄强制施加弹性夹紧力，同时提供微量轴向自定心补偿。
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ 推荐规避工程路径 (Design Around)</div>
        <div class="spec-box__text">
          <b>① Oldham 十字滑块浮动联轴器:</b> 不对钥匙柄施加任何径向夹持，仅通过浮动拨叉传递旋转扭矩，允许 ±2.0mm 径向/偏角跳动，彻底消灭摩擦力与夹持特征；<br>
          <b>② 预制模块化通用锁芯:</b> 标配 DIN EN 1303 认证通用锁芯换装（Nuki Ultra 路线），从物理源头消灭常插钥匙。
        </div>
      </div>
    </div>
    <!-- Oldham 浮动拨叉对比图 -->
    <div style="margin-top: 12px; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
      <img src="/assets/img/patent/patent-oldham-coupling-comparison.svg" alt="Oldham 十字滑块浮动规避专利对比图" style="width: 100%; height: auto; display: block;" loading="lazy" />
    </div>
  </div>
</div>

---

### 3. 手动优先与脱开离合器 (Manual Override Clutch)
<div id="clutch-disconnect" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 专题 03：电动齿轮箱轴向推拉离合机构规避</h3>
    <span class="spec-card__badge spec-card__badge--red">US9347244 / EP2890858 核心壁垒</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ 侵权红线特征 (Claims)</div>
        <div class="spec-box__text">
          <b>竞品基准:</b> 减速齿轮箱内置微型舵机或电磁推杆，电动转动前强行将离合齿轮轴向推入啮合，待机时弹簧推回脱开，确保手动手感轻盈。
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ 推荐规避工程路径 (Design Around)</div>
        <div class="spec-box__text">
          <b>① 机械滚柱超越离合器 (Sprag Clutch):</b> 采用单向超越离合轴承，电机正转驱动锁舌，手动转动时滚柱自由滚退，完全免除电子舵机，BOM 成本降 35%；<br>
          <b>② 超低反驱无刷电机 (Low-Backdrive BLDC):</b> 采用减速比 ≤1:15 的大扭矩外转子电机，反驱阻尼仅 0.1 N·m，人手轻推自如，在机构上彻底消灭离合器。
        </div>
      </div>
    </div>
  </div>
</div>

---

### 4. 美标死锁尾轴适配器 (ANSI Deadbolt Wing Latches)
<div id="august-tailpiece" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 专题 04：机身双侧翻折翼形卡扣 (Wing Latches) 规避</h3>
    <span class="spec-card__badge spec-card__badge--red">US9228373 / US9598881 核心壁垒</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ 侵权红线特征 (Claims)</div>
        <div class="spec-box__text">
          <b>竞品基准 (August):</b> 底座背板安装于死锁后，主机机身两侧设有向外摆动的翻折翼片，合拢后卡爪紧咬背板凸耳固定机身。
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ 推荐规避工程路径 (Design Around)</div>
        <div class="spec-box__text">
          <b>① 45° 旋转卡口锁紧环 (Bayonet Twist Ring):</b> 借鉴单反镜头旋转 45° 自锁机构，一旋即紧，彻底避开侧向翻折翼爪权利要求；<br>
          <b>② 强磁预定心 + 底部防盗螺钉:</b> 机身嵌入 4 颗 N52 钕铁硼磁铁自动吸附对齐，底端由 1 颗隐藏梅花螺丝锁死，外观纯平无翼爪。
        </div>
      </div>
    </div>
  </div>
</div>

---

## 5. 出海 FTO 防侵权自查清单 (Patent Clearance Checklist)
<div id="checklist" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 工业五金出海 FTO 自由实施五步核验表</h3>
    <span class="spec-card__badge spec-card__badge--green">工程放行准则</span>
  </div>
  <div class="spec-card__body" style="padding: 0;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; margin: 0;">
      <thead>
        <tr style="background: #f8fafc; border-bottom: 2px solid #cbd5e1; color: #0f172a;">
          <th style="padding: 10px 14px; width: 22%;">核验机构模块</th>
          <th style="padding: 10px 14px; width: 40%;">侵权高危特征 (Avoid)</th>
          <th style="padding: 10px 14px; width: 38%;">已验证规避路线 (Pass)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">01 背板锁芯夹持</td>
          <td style="padding: 10px 14px; color: #991b1b;">3 颗径向内六角顶丝直顶锁芯壳体</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">ER 弹性夹头抱紧圈 / 把手饰盖螺栓锚定</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">02 钥匙/旋钮抓取</td>
          <td style="padding: 10px 14px; color: #991b1b;">输出轴内嵌自定心弹片夹死钥匙柄</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">Oldham 十字浮动拨叉 / 配套模块化锁芯</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">03 手动优先离合</td>
          <td style="padding: 10px 14px; color: #991b1b;">电子舵机或电磁铁强行拉开齿轮啮合</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">单向滚柱超越离合器 / ≤1:15 低反驱 BLDC</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">04 机身卡扣紧固</td>
          <td style="padding: 10px 14px; color: #991b1b;">外壳双侧摆动翻折翼片夹爪 (August)</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">镜头式 45° 旋转卡口 / 强磁对位底钉</td>
        </tr>
        <tr>
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">05 门开闭状态检测</td>
          <td style="padding: 10px 14px; color: #991b1b;">机身与门框特定贴装霍尔磁铁排布</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">飞行时间 ToF 测距 / IMU 六轴陀螺仪姿态算法</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

en_content = """---
title: "Retrofit Smart Lock Patent Avoidance & FTO Guide"
slug: "patent-avoidance.html"
lang: "en"
---

<!-- ASSA ABLOY Engineering Header -->
<div class="spec-hero-meta">
  <span><b>Target Audience:</b> Hardware PMs / Mechanical Engineers / IP Counsel</span>
  <span><b>Focus:</b> Non-destructive Retrofit Smart Locks</span>
  <span><b>Jurisdictions:</b> EPO (Europe) / USPTO (US) / JPO (Japan)</span>
  <span><b>Compliance Metric:</b> Strict Freedom-to-Operate (FTO)</span>
</div>

<!-- 5-Topic Navigation Grid (Uniform 5-col grid, replacing crowded pills) -->
<nav class="spec-topic-nav" aria-label="Patent Avoidance Navigation">
  <a class="spec-topic-pill" href="#nuki-clamping">
    <span class="spec-topic-pill__num">01 / CLAMPING</span>
    <span class="spec-topic-pill__title">Cylinder Clamping</span>
  </a>
  <a class="spec-topic-pill" href="#key-coupling">
    <span class="spec-topic-pill__num">02 / COUPLING</span>
    <span class="spec-topic-pill__title">Key Gripper & Oldham</span>
  </a>
  <a class="spec-topic-pill" href="#clutch-disconnect">
    <span class="spec-topic-pill__num">03 / CLUTCH</span>
    <span class="spec-topic-pill__title">Manual Clutch</span>
  </a>
  <a class="spec-topic-pill" href="#august-tailpiece">
    <span class="spec-topic-pill__num">04 / TAILPIECE</span>
    <span class="spec-topic-pill__title">ANSI Tailpiece</span>
  </a>
  <a class="spec-topic-pill" href="#checklist">
    <span class="spec-topic-pill__num">05 / AUDIT</span>
    <span class="spec-topic-pill__title">FTO Checklist</span>
  </a>
</nav>

## High-Risk Litigation Zones for Smart Retrofit Locks

Retrofit smart lock patents predominantly concentrate on **three-point mounting mechanisms**, **key/thumbturn adaptive grippers**, and **dual-action decoupling clutches**.

---

### 1. Mounting Plate Cylinder Clamping Design-Around
<div id="nuki-clamping" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ Topic 01: Circumferential Set Screw Clamping Workaround</h3>
    <span class="spec-card__badge spec-card__badge--red">EPO / EP3014032 Core Claim</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ High-Risk Claim Limitation</div>
        <div class="spec-box__text">
          <b>Competitor Baseline (Nuki Plate A):</b> Euro-profile cutout with 3 allen set screws radially pressing against the brass cylinder housing.
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ Recommended Workaround Pathway</div>
        <div class="spec-box__text">
          <b>① 360° Split Collar Collet:</b> Uniform concentric clamping sleeve inspired by CNC ER collets. Eliminates point screws and surface scratching;<br>
          <b>② Rose Escutcheon Through-Bolt Mounting:</b> Fasten directly to existing door through-bolts behind the decorative rose trim without touching the cylinder.
        </div>
      </div>
    </div>
    <!-- 1:1 Comparison Diagram -->
    <div style="margin-top: 12px; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
      <img src="/assets/img/patent/patent-clamping-comparison.svg" alt="Cylinder clamping patent comparison diagram" style="width: 100%; height: auto; display: block;" loading="lazy" />
    </div>
  </div>
</div>

---

### 2. Key Gripper & Floating Misalignment Coupling
<div id="key-coupling" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ Topic 02: Resilient Key Bow Gripper & Floating Link</h3>
    <span class="spec-card__badge spec-card__badge--red">EP3175062 / US9822557 Core Claim</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ High-Risk Claim Limitation</div>
        <div class="spec-box__text">
          <b>Competitor Baseline:</b> Output shaft cavity featuring resilient elastomer pads or leaf springs forcefully clamping inserted key bows.
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ Recommended Workaround Pathway</div>
        <div class="spec-box__text">
          <b>① Oldham Cross-Slide Floating Coupler:</b> Pure torque transmission with ±2.0mm radial play without gripping the key bow;<br>
          <b>② Modular EN 1303 Cylinder Replacement:</b> Bundle standard modular cylinders (Nuki Ultra approach) to eliminate key turning entirely.
        </div>
      </div>
    </div>
    <!-- Oldham Comparison Diagram -->
    <div style="margin-top: 12px; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
      <img src="/assets/img/patent/patent-oldham-coupling-comparison.svg" alt="Oldham coupling patent comparison diagram" style="width: 100%; height: auto; display: block;" loading="lazy" />
    </div>
  </div>
</div>

---

### 3. Manual Override Clutch Decoupling
<div id="clutch-disconnect" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ Topic 03: Motorized Gearbox Axial Disconnect Clutch</h3>
    <span class="spec-card__badge spec-card__badge--red">US9347244 / EP2890858 Core Claim</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ High-Risk Claim Limitation</div>
        <div class="spec-box__text">
          <b>Competitor Baseline:</b> Auxiliary servo motor or solenoid physically translating a sliding clutch gear into mesh during motor drive.
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ Recommended Workaround Pathway</div>
        <div class="spec-box__text">
          <b>① Mechanical Sprag / Roller Overrunning Clutch:</b> Unidirectional driving roller bearing; free manual turning with zero electronic actuators;<br>
          <b>② Low-Backdrive Brushless DC Motor (BLDC):</b> Gear ratio ≤1:15 with 0.1 N·m drag, eliminating clutch mechanisms entirely.
        </div>
      </div>
    </div>
  </div>
</div>

---

### 4. ANSI Deadbolt Tailpiece Wing Latches
<div id="august-tailpiece" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ Topic 04: Lateral Wing Latches Chassis Clamping</h3>
    <span class="spec-card__badge spec-card__badge--red">US9228373 / US9598881 Core Claim</span>
  </div>
  <div class="spec-card__body">
    <div class="spec-grid-2col">
      <div class="spec-box-risk">
        <div class="spec-box__label">⚡ High-Risk Claim Limitation</div>
        <div class="spec-box__text">
          <b>Competitor Baseline (August):</b> Lateral swing-out wing latches clamping down over mounting plate tabs.
        </div>
      </div>
      <div class="spec-box-solution">
        <div class="spec-box__label">🛡️ Recommended Workaround Pathway</div>
        <div class="spec-box__text">
          <b>① 45° Bayonet Twist-Lock Ring:</b> Quarter-turn interlocking ring inspired by camera bayonet mounts;<br>
          <b>② Neodymium Magnetic Docking + Security Fastener:</b> 4× N52 magnets for auto-alignment, fastened rigidly with one hidden Torx bolt.
        </div>
      </div>
    </div>
  </div>
</div>

---

## 5. Global FTO Clearance Checklist
<div id="checklist" class="spec-card">
  <div class="spec-card__header">
    <h3 class="spec-card__title">⌖ 5-Step Hardware FTO Clearance Matrix</h3>
    <span class="spec-card__badge spec-card__badge--green">Pass Criteria</span>
  </div>
  <div class="spec-card__body" style="padding: 0;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; margin: 0;">
      <thead>
        <tr style="background: #f8fafc; border-bottom: 2px solid #cbd5e1; color: #0f172a;">
          <th style="padding: 10px 14px; width: 22%;">Mechanism Module</th>
          <th style="padding: 10px 14px; width: 40%;">Litigation Risk (Avoid)</th>
          <th style="padding: 10px 14px; width: 38%;">Verified Pathway (Pass)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">01 Plate Clamping</td>
          <td style="padding: 10px 14px; color: #991b1b;">3 radial set screws pressing cylinder body</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">ER concentric collet / Escutcheon through-bolt</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">02 Key / Thumbturn Gripper</td>
          <td style="padding: 10px 14px; color: #991b1b;">Output shaft cavity with resilient clips</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">Oldham floating link / Modular DIN cylinder</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">03 Manual Override Clutch</td>
          <td style="padding: 10px 14px; color: #991b1b;">Motorized auxiliary actuator shifting gear</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">One-way sprag clutch / ≤1:15 Low-drag BLDC</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">04 Chassis Fastening</td>
          <td style="padding: 10px 14px; color: #991b1b;">Lateral swinging wing latches (August)</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">Bayonet 45° twist ring / Magnetic dock + bolt</td>
        </tr>
        <tr>
          <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">05 Door Sensor Array</td>
          <td style="padding: 10px 14px; color: #991b1b;">Specific dual-magnet alignment arrays</td>
          <td style="padding: 10px 14px; color: #166534; font-weight: 600;">ToF laser distance sensor / 6-axis IMU gyro</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

with open('content/pages/zh/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(zh_content)
with open('content/pages/en/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(en_content)

print("Updated content/pages/zh/patent-avoidance.md & en/patent-avoidance.md successfully.")
