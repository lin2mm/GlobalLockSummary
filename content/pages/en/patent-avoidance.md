---
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
