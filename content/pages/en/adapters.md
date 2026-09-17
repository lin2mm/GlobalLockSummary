---
title: "Global Smart Lock Retrofit Adapters & BOM Engineering Guide"
slug: "adapters.html"
lang: "en"
---

# 🧩 Global Smart Lock Retrofit Adapters & BOM Engineering Guide

Due to decades of fragmented industrial standards, door lock followers, thumbturns, and tailpieces differ significantly around the world. This engineering BOM specifies the essential **reducer sleeves, adaptive gimbals, and dynamic clamps** required for global smart lock deployments.

---

## 1. Essential Retrofit Adapter Bill of Materials (BOM)

<div style="display: flex; gap: 20px; align-items: flex-start; margin: 24px 0; background: var(--color-bg-card, #f8fafc); padding: 18px; border-radius: 8px; border: 1px solid var(--color-border, #e2e8f0); flex-wrap: wrap;">
  <div style="flex: 1; min-width: 260px;">
    <img src="../assets/img/tools/adapter-7to8mm.png" alt="7mm to 8mm Spindle Reducer Sleeve" style="width: 100%; border-radius: 6px;" />
    <p style="font-size: 0.85em; color: var(--color-text-muted, #64748b); margin-top: 6px;">Fig 1: French standard 7mm to 8mm slotted spindle reducer sleeve</p>
  </div>
  <div style="flex: 1.4; min-width: 300px;">
    <h3>ADP-01: French 7mm to 8mm Spindle Reducer Sleeve</h3>
    <ul>
      <li><strong>Target Region</strong>: France, Belgium (FR/BE).</li>
      <li><strong>Problem Solved</strong>: French lock followers are 7×7mm square. Standard 8×8mm spindles will not penetrate. This sleeve enables 7mm original spindles to securely engage 8mm smart lock hubs.</li>
      <li><strong>Material Recommendation</strong>: <strong>H62 Brass or Hardened Carbon Steel</strong> (avoid cheap zinc alloys, which shear under downward handle torque).</li>
      <li><strong>Tolerances</strong>: Outer: $8.00_{-0.05}^{0}\text{ mm}$, Inner: $7.05_{0}^{+0.05}\text{ mm}$, Length: 25~30mm.</li>
    </ul>
  </div>
</div>

<div style="display: flex; gap: 20px; align-items: flex-start; margin: 24px 0; background: var(--color-bg-card, #f8fafc); padding: 18px; border-radius: 8px; border: 1px solid var(--color-border, #e2e8f0); flex-wrap: wrap;">
  <div style="flex: 1; min-width: 260px;">
    <img src="../assets/img/indigenous/jp-thumbturn.jpg" alt="Japanese MIWA B5 Gripper Clamp" style="width: 100%; border-radius: 6px;" />
  </div>
  <div style="flex: 1.4; min-width: 300px;">
    <h3>ADP-02: Japanese MIWA B5 Anti-Burglar Dynamic Squeeze Clamp</h3>
    <ul>
      <li><strong>Target Region</strong>: Japan (JP).</li>
      <li><strong>Problem Solved</strong>: MIWA B5 thumbturns incorporate dual spring tabs. Rigid rotational adapters will jam.</li>
      <li><strong>Mechanism</strong>: The inner adapter features dual cam slopes that squeeze the side release buttons inward during initial motor torque, releasing the locking brake before rotation begins.</li>
      <li><strong>Material</strong>: <strong>POM (Acetal/Delrin) or PA12 Nylon</strong>.</li>
    </ul>
  </div>
</div>
