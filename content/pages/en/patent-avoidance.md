---
title: "Retrofit Smart Lock Patent Avoidance & FTO Guide"
slug: "patent-avoidance.html"
lang: "en"
---

# Retrofit Smart Lock Patent Avoidance & FTO Guide

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

  <!-- 1:1 专利权同等对比图 -->
  <div style="margin: 16px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="/assets/img/patent/patent-clamping-comparison.svg" alt="锁芯夹持专利对比图" style="width: 100%; height: auto; display: block;" />
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

  <!-- 钥匙柄耦合与 Oldham 浮动拨叉对比图 -->
  <div style="margin: 16px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="/assets/img/patent/patent-oldham-coupling-comparison.svg" alt="Oldham 十字滑块浮动规避专利对比图" style="width: 100%; height: auto; display: block;" />
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
