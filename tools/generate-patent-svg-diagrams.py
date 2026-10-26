# 1. 生成 Nuki 锁芯夹持 vs 柔性夹头规避设计图
nuki_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="8"/>
  <text x="20" y="32" fill="#94a3b8" font-size="14" font-weight="bold">PATENT COMPARISON: CYLINDER CLAMPING MECHANISM</text>
  
  <!-- Left: Prior Art Patent Risk -->
  <g transform="translate(40, 50)">
    <rect width="340" height="280" fill="#1e293b" rx="6" stroke="#ef4444" stroke-width="2"/>
    <rect x="15" y="15" width="120" height="24" fill="#dc2626" rx="4"/>
    <text x="25" y="32" fill="#fff" font-size="12" font-weight="bold">⚠️ 专利保护构型</text>
    <text x="145" y="32" fill="#f87171" font-size="12">EP3056660 / Nuki Plate A</text>
    
    <!-- Cylinder outline -->
    <path d="M 170 80 A 30 30 0 0 1 200 110 L 200 160 A 10 10 0 0 1 190 170 L 150 170 A 10 10 0 0 1 140 160 L 140 110 A 30 30 0 0 1 170 80 Z" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <circle cx="170" cy="110" r="14" fill="#1e293b"/>
    
    <!-- 3 Set Screws -->
    <!-- Left screw -->
    <line x1="80" y1="130" x2="135" y2="130" stroke="#f87171" stroke-width="4" stroke-dasharray="4,2"/>
    <polygon points="135,130 125,125 125,135" fill="#ef4444"/>
    <text x="50" y="125" fill="#fca5a5" font-size="11">顶丝 1</text>
    
    <!-- Right screw -->
    <line x1="260" y1="130" x2="205" y2="130" stroke="#f87171" stroke-width="4" stroke-dasharray="4,2"/>
    <polygon points="205,130 215,125 215,135" fill="#ef4444"/>
    <text x="265" y="125" fill="#fca5a5" font-size="11">顶丝 2</text>
    
    <!-- Bottom screw -->
    <line x1="170" y1="230" x2="170" y2="175" stroke="#f87171" stroke-width="4" stroke-dasharray="4,2"/>
    <polygon points="170,175 165,185 175,185" fill="#ef4444"/>
    <text x="145" y="248" fill="#fca5a5" font-size="11">底向顶丝 3</text>
    
    <text x="25" y="270" fill="#fca5a5" font-size="12">权利要求特征：3颗紧定螺钉径向点压锁芯壁</text>
  </g>
  
  <!-- Right: Design Around Workaround -->
  <g transform="translate(420, 50)">
    <rect width="340" height="280" fill="#1e293b" rx="6" stroke="#10b981" stroke-width="2"/>
    <rect x="15" y="15" width="130" height="24" fill="#059669" rx="4"/>
    <text x="25" y="32" fill="#fff" font-size="12" font-weight="bold">🛡️ 推荐规避方案</text>
    <text x="155" y="32" fill="#34d399" font-size="12">360° 柔性弹性夹头 (Collet)</text>
    
    <!-- Concentric clamping collar -->
    <circle cx="170" cy="130" r="55" fill="none" stroke="#10b981" stroke-width="6" stroke-dasharray="15,4"/>
    <path d="M 170 90 A 25 25 0 0 1 195 115 L 195 155 A 10 10 0 0 1 185 165 L 155 165 A 10 10 0 0 1 145 155 L 145 115 A 25 25 0 0 1 170 90 Z" fill="#334155" stroke="#10b981" stroke-width="2"/>
    
    <!-- Tangential Cam Lever -->
    <line x1="225" y1="130" x2="280" y2="90" stroke="#34d399" stroke-width="5" stroke-linecap="round"/>
    <circle cx="225" cy="130" r="6" fill="#10b981"/>
    <text x="240" y="80" fill="#6ee7b7" font-size="11">偏心快拆压杆</text>
    
    <text x="25" y="240" fill="#a7f3d0" font-size="12">1. 360° 环向均载面接触，零顶丝点压</text>
    <text x="25" y="262" fill="#a7f3d0" font-size="12">2. 彻底不伤租客锁芯黄铜外壁，避开所有原案</text>
  </g>
</svg>"""

with open('assets/img/patent/patent-clamping-comparison.svg', 'w', encoding='utf-8') as f:
    f.write(nuki_svg)

# 2. 生成 钥匙柄夹持 vs 十字滑块 (Oldham) 浮动拨叉规避设计图
oldham_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="8"/>
  <text x="20" y="32" fill="#94a3b8" font-size="14" font-weight="bold">PATENT COMPARISON: KEY DRIVE &amp; FLOATING MISALIGNMENT</text>
  
  <!-- Left: Prior Art -->
  <g transform="translate(40, 50)">
    <rect width="340" height="280" fill="#1e293b" rx="6" stroke="#ef4444" stroke-width="2"/>
    <rect x="15" y="15" width="120" height="24" fill="#dc2626" rx="4"/>
    <text x="25" y="32" fill="#fff" font-size="12" font-weight="bold">⚠️ 专利保护构型</text>
    <text x="145" y="32" fill="#f87171" font-size="12">弹性弹片夹紧钥匙柄</text>
    
    <!-- Motor shaft slot -->
    <rect x="120" y="80" width="100" height="110" rx="8" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <!-- Key Bow -->
    <rect x="145" y="60" width="50" height="100" rx="4" fill="#cbd5e1"/>
    <!-- Leaf springs clamping key -->
    <path d="M 125 110 Q 140 120 144 130" stroke="#ef4444" stroke-width="4" fill="none"/>
    <path d="M 215 110 Q 200 120 196 130" stroke="#ef4444" stroke-width="4" fill="none"/>
    
    <text x="35" y="235" fill="#fca5a5" font-size="12">缺陷：钥匙柄被刚性/弹性夹紧</text>
    <text x="35" y="258" fill="#fca5a5" font-size="12">门轴同心度偏差直接卡死减速箱</text>
  </g>
  
  <!-- Right: Oldham Workaround -->
  <g transform="translate(420, 50)">
    <rect width="340" height="280" fill="#1e293b" rx="6" stroke="#10b981" stroke-width="2"/>
    <rect x="15" y="15" width="130" height="24" fill="#059669" rx="4"/>
    <text x="25" y="32" fill="#fff" font-size="12" font-weight="bold">🛡️ 推荐规避方案</text>
    <text x="155" y="32" fill="#34d399" font-size="12">Oldham 十字滑块浮动拨叉</text>
    
    <!-- Outer motor driving disk -->
    <circle cx="170" cy="130" r="50" fill="#1e293b" stroke="#10b981" stroke-width="3"/>
    <!-- Floating cross element -->
    <rect x="155" y="95" width="30" height="70" rx="3" fill="#34d399" opacity="0.8"/>
    <rect x="135" y="115" width="70" height="30" rx="3" fill="#10b981" opacity="0.8"/>
    <!-- Key slot -->
    <rect x="162" y="110" width="16" height="40" rx="2" fill="#0f172a"/>
    
    <text x="25" y="235" fill="#a7f3d0" font-size="12">1. 纯扭矩传递，吸收 ±2.0mm 径向跳动</text>
    <text x="25" y="258" fill="#a7f3d0" font-size="12">2. 彻底脱钩“钥匙柄弹性夹持腔”权利要求</text>
  </g>
</svg>"""

with open('assets/img/patent/patent-oldham-coupling-comparison.svg', 'w', encoding='utf-8') as f:
    f.write(oldham_svg)

print("Generated patent SVG comparison diagrams!")
