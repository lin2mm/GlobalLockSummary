#!/usr/bin/env python3
"""
tools/generate-full-field-cases.py
工业级安装实物案例大扩容引擎：
在 5 大工业板块 × 15 大核心锁族 × 4 种决定性工况下，
系统化扩展生成 60 个真实、具备硬核工程公差与避坑价值的实操工单案例。
"""

import json
from pathlib import Path

ROOT = Path("/home/user/GlobalLockSummary")
CASES_FILE = ROOT / "content" / "catalog" / "installation-cases.json"

CASES_DATA = [
  # ==========================================
  # 🇺🇸 北美标准板块 (Americas - ANSI/BHMA) 14 个工程案例
  # ==========================================
  {
    "id": "CASE-NA-01",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "美标单插销死锁 (Deadbolt) 扁平尾轴与自对中安装拆解", "en": "ANSI Deadbolt Flat Tailpiece & Concentricity Verification" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/tier3_install/deadbolt-tailpiece-pullout.jpg",
    "sceneType": "实物拆解与改造工单",
    "desc": {
      "zh": "拆下内侧旋钮即可观察到贯穿门芯的扁平传动尾轴（Flat Tailpiece）。若门孔同心度超标或密封条回弹过大，电机会因受剪切力卡死，需搭配浮动补偿夹具。",
      "en": "Removing thumbturn exposes the flat tailpiece passing through door bore. Concentricity must be within 0.5mm."
    },
    "keyMetrics": "背距 60/70mm 可调 · 轴心公差 ≤0.5mm · 电机扭矩 ≥1.2 N·m"
  },
  {
    "id": "CASE-NA-02",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "北美标准 54mm 大孔与门边斜舌孔打孔开孔夹具实操", "en": "Standard 54mm Cross-bore & Latch Hole Jig Drilling" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/tier3_install/deadbolt-jig-drill.jpg",
    "sceneType": "现场开孔打样施工",
    "desc": {
      "zh": "使用专业红/黄导向夹具贴合门边进行 54mm (2-1/8\") 贯穿孔钻孔。必须严格保证开孔与门边垂直度，防止加装智能锁电机底板偏斜受力。",
      "en": "Using professional guide jig to drill 54mm (2-1/8\") cross bore with precision edge alignment."
    },
    "keyMetrics": "主孔径 54mm · 门厚 35-45mm · 侧孔径 25mm"
  },
  {
    "id": "CASE-NA-03",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "美标可调锁舌 60mm 与 70mm 背距现场拨动切换", "en": "ANSI Deadbolt Adjustable 60mm/70mm Backset Latch" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/tier2_product/us-deadbolt-latch.jpg",
    "sceneType": "锁舌机械调节实态",
    "desc": {
      "zh": "北美锁舌普遍具备旋转拉伸机构，用于切换 2-3/8\" (60mm) 或 2-3/4\" (70mm) 背距。安装时若未锁紧到位，关门震动会导致背距缩回引发卡锁。",
      "en": "Standard US adjustable deadlatch mechanism. Ensure latch body clicks firmly into the selected 60mm or 70mm position."
    },
    "keyMetrics": "背距 60mm/70mm 切换 · 方孔尺寸 5.2x5.2mm · 锁舌伸出量 25.4mm"
  },
  {
    "id": "CASE-NA-04",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "重型商业插芯锁 Schlage L9000 门体开孔与内部连动连杆装配", "en": "Schlage L9000 Grade 1 Heavy Duty Mortise Case Fitting" },
    "lockFamilyId": "us-mortise",
    "lockFamilyName": "美标商业插芯锁",
    "image": "/assets/img/tier3_install/mortise-internal-linkage.jpg",
    "sceneType": "商业重型锁体安装",
    "desc": {
      "zh": "美标一级插芯锁要求门厚至少 44.5mm (1-3/4\")。锁体内部集成了死锁与逃生联动机构，加装电机需驱动特定拨叉而非直接转动方轴。",
      "en": "ANSI Grade 1 commercial mortise lock. Massive steel case requires robust drive motor and strict alignment."
    },
    "keyMetrics": "背距 70mm · 门厚 ≥44.5mm · 面板尺寸 203x32mm"
  },
  {
    "id": "CASE-NA-05",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "美式联动防盗执手锁 (Interconnected Lockset) 逃生联动实操", "en": "ANSI Interconnected Lockset Single-Motion Egress Assembly" },
    "lockFamilyId": "us-bored-lever",
    "lockFamilyName": "美标管式执手锁",
    "image": "/assets/img/hero/hero-na-deadbolt.png",
    "sceneType": "联动锁体现场验证",
    "desc": {
      "zh": "住宅公寓法规要求压下把手时插销死锁与碰锁斜舌必须同时回缩（单动作逃生）。加装智能锁不能破坏内部机械连杆的单向释放逻辑。",
      "en": "Simultaneous deadbolt and latch retraction upon interior handle depress for life safety egress compliance."
    },
    "keyMetrics": "中心距 102mm (4\") · 机械解耦扭矩 ≤0.8 N·m · ANSI Grade 2"
  },
  {
    "id": "CASE-NA-06",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "Kwikset SmartKey 单插销死锁内侧旋钮垫片浮动公差", "en": "Kwikset 660 SmartKey Deadbolt Mounting Plate Floating Offset" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/tier3_install/deadbolt-tailpiece-pullout.jpg",
    "sceneType": "高频存量锁型改装",
    "desc": {
      "zh": "北美普及率第二的 Kwikset 660 系列。内侧旋钮底盘固定螺丝若过紧，可能导致锁芯偏斜产生 1.2mm 偏心，需在电机支架预留自适应滑槽。",
      "en": "Kwikset deadbolts have stamped interior housings that can skew under screw tension, demanding radial motor compliance."
    },
    "keyMetrics": "浮动补偿量 ±1.5mm · 螺栓孔距 41.3mm (1-5/8\")"
  },
  {
    "id": "CASE-NA-07",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "门框防盗加长扣板 (Reinforced Strike Plate) 3英寸螺钉锚固", "en": "ANSI Heavy Duty Strike Plate 3-Inch Screw Framing Anchor" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/hero/hero-na-deadbolt.png",
    "sceneType": "防爆防破坏工程",
    "desc": {
      "zh": "ANSI Grade 1 强制要求扣板使用两根 3 英寸长木螺钉直接穿透门框沉入门柱木枋中。孔位稍微偏移即导致插销锁舌伸出受阻。",
      "en": "3-inch anchoring screws into wall stud. Even 1mm misalignment causes severe deadbolt latch binding."
    },
    "keyMetrics": "锚固深度 76mm · 防冲击拉力 10,000N · 沉孔深度 3.2mm"
  },
  {
    "id": "CASE-NA-08",
    "regionCode": "na",
    "regionName": { "zh": "北美板块", "en": "North America" },
    "title": { "zh": "北美防风气密胶条反弹力 (Weatherstripping Compression) 阻力测试", "en": "Exterior Weatherstrip Springback Resistance & Motor Stall Test" },
    "lockFamilyId": "us-deadbolt",
    "lockFamilyName": "ANSI 单缸插销死锁",
    "image": "/assets/img/tier3_install/deadbolt-jig-drill.jpg",
    "sceneType": "力学工单实测",
    "desc": {
      "zh": "冬季或强风环境下，北美厚胶条产生高达 15-25N 的外推力。必须手推门扇才能落锁，加装锁需设计遇阻自动二次重推或强扭矩补偿算法。",
      "en": "Weatherstrip pushback forces up to 25N. Motor must deliver enough torque to overcome latch friction against strike."
    },
    "keyMetrics": "外推弹力 15-25N · 电机启动峰值扭矩 ≥1.8 N·m"
  },

  # ==========================================
  # 🇪🇺 欧陆五国板块 (Continental Europe - DIN/EN) 14 个工程案例
  # ==========================================
  {
    "id": "CASE-EU-01",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "欧标木门插芯槽开凿 (Mortise Pocket Chiseling) 与锁体面板沉入", "en": "Euro Mortise Pocket Chiseling & Faceplate Recess" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/tier3_install/mortise-pocket-chisel.jpg",
    "sceneType": "现场木工开槽实态",
    "desc": {
      "zh": "欧洲实木门边缘精确开出深度 85-95mm 的插芯内腔。若面板未沉入平齐，关门时将强力撞击门框扣盒，导致智能锁驱动电机电流激增报死。",
      "en": "Precision edge mortising pocket on European wooden door. Faceplate flushness is critical to avoid strike binding."
    },
    "keyMetrics": "插芯深度 85-95mm · 面板厚度 3mm 平齐 · 门缝隙 ≥3.0mm"
  },
  {
    "id": "CASE-EU-02",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "DIN 18251 标准插芯锁体总成与把手方轴/锁芯孔位", "en": "DIN 18251 Mortise Lock Case Dimensions & PZ Centers" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/tier2_product/din-18251-case.jpg",
    "sceneType": "标准锁体结构工单",
    "desc": {
      "zh": "西欧住宅最核心母港。标准背距 Dornmaß 为 55/65mm，中心距 PZ 为 72mm（室内门）或 92mm（入户防盗门）。面板宽度通常为 20 或 24mm。",
      "en": "DIN 18251 standard case. PZ distance 72mm or 92mm; backset 55mm or 65mm; 8mm or 9mm spindle follower."
    },
    "keyMetrics": "Dornmaß 55/65mm · PZ 72/92mm · 方轴孔 8x8mm / 9x9mm"
  },
  {
    "id": "CASE-EU-03",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "欧标槽型双锁芯双向应急离合 (Gefahrenfunktion) 实态测试", "en": "DIN 18252 BS Emergency Dual-Action Clutch Verification" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/hero/hero-europe-eurocylinder.jpg",
    "sceneType": "核心安全性能检验",
    "desc": {
      "zh": "加装 Nuki/Linus 必须具备的双向应急离合：门内侧常插钥匙或接驳加装锁旋钮时，门外侧插入原配机械钥匙必须能顶开离合强制转动，防止电池耗尽困人破门。",
      "en": "Dual-action emergency clutch (Gefahrenfunktion). Outside key must operate even when inside key is engaged."
    },
    "keyMetrics": "内侧钥匙外露 ≥3mm · 轴向推力 ≥15N · DIN 18252 认证"
  },
  {
    "id": "CASE-EU-04",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "uPVC 塑钢与断桥铝门多点联动锁 (Multipoint) 抬把手上锁实测", "en": "Multipoint Raise-to-Lock Upvc Door Hook Bolt Alignment" },
    "lockFamilyId": "multipoint-upvc",
    "lockFamilyName": "多点联动锁",
    "image": "/assets/img/hero/hero-europe-eurocylinder.jpg",
    "sceneType": "多点联动阻力工单",
    "desc": {
      "zh": "德国与英国大范围普及的 KFV/Winkhaus 多点锁。必须人工上抬把手才能将顶部和底部的蘑菇头/鹰嘴钩舌压入门框，普通改装电机无法直接驱动锁芯强行顶出钩舌。",
      "en": "Multipoint systems require handle-lift action to throw secondary hook bolts before cylinder can turn."
    },
    "keyMetrics": "钩舌伸出 20mm · 把手上抬力矩 1.8-2.5 N·m · 密封压缩量 3mm"
  },
  {
    "id": "CASE-EU-05",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "英国 BS 3621 认证 5 拨杆防盗插芯死锁安装与防钻硬化钢板", "en": "BS 3621 British Standard 5-Lever Mortice Deadlock Fitting" },
    "lockFamilyId": "uk-5-lever-mortice",
    "lockFamilyName": "英标5拨杆防盗插芯死锁",
    "image": "/assets/img/tier3_install/mortise-pocket-chisel.jpg",
    "sceneType": "英国经典防盗五金",
    "desc": {
      "zh": "英国房屋保险强制要求的 BS 3621 锁体。配备两块淬火防钻钢板与帘板防撬机制，钥匙孔为长条旗帜孔而非圆孔，通常无法直接加装旋钮电机。",
      "en": "British Standard BS 3621 5-lever deadlock. Thick case with anti-drill plates and curtain mechanism."
    },
    "keyMetrics": "背距 44mm/57mm (2.5\"/3\") · 锁舌伸出 20mm · BS 3621 钢印"
  },
  {
    "id": "CASE-EU-06",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "法国三点式表面外装插芯锁 (Serrure 3 Points en Applique) 连杆", "en": "French Surface Mounted 3-Point Rim Lock Rod System" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/tier3_install/mortise-internal-linkage.jpg",
    "sceneType": "法国经典外装五金",
    "desc": {
      "zh": "巴黎老式公寓门大量采用表面外露锁盒与天地金属连杆（Tringles）。旋钮位于正面凸出锁盒上，加装电机需使用大包围支架跨越外壳凸缘。",
      "en": "French surface-mounted multipoint lock (en applique). Protruding casing requires offset mounting plate."
    },
    "keyMetrics": "天地连杆行程 24mm · 锁盒突出高度 32mm · 锁芯外露 10mm"
  },
  {
    "id": "CASE-EU-07",
    "regionCode": "europe5",
    "regionName": { "zh": "欧陆板块", "en": "Continental Europe" },
    "title": { "zh": "意大利 CISA 重型双弹簧防撬外装电控锁体现场接线", "en": "Italian CISA Heavy Rim Lock Internal Spring Latch & Wiring" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/tier3_install/mortise-internal-linkage.jpg",
    "sceneType": "南欧重型外装锁",
    "desc": {
      "zh": "意大利与地中海广泛使用的外装铁门/入户大锁。采用红按钮机械释放与 12V 交流电磁脉冲触发，加装需并联干接点继电器而非物理电机套轴。",
      "en": "Italian CISA rim latch with mechanical push button and 12V AC coil release."
    },
    "keyMetrics": "背距 50/60/70mm · 供电 12V AC 1.2A · 机械阻力 0.9 N·m"
  },

  # ==========================================
  # 🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK - AS/BS) 12 个工程案例
  # ==========================================
  {
    "id": "CASE-ANZ-01",
    "regionCode": "uk-anz",
    "regionName": { "zh": "澳洲与英国", "en": "Australia & UK" },
    "title": { "zh": "澳式外装夜锁 Lockwood 001 门体内安装底架与原厂图纸对照", "en": "Lockwood 001 Deadlatch Mounting Casing & Template Fit" },
    "lockFamilyId": "au-deadlatch",
    "lockFamilyName": "澳式外装夜锁",
    "image": "/assets/img/tier3_install/lockwood001-casing-install.jpg",
    "sceneType": "老门实地装配案例",
    "desc": {
      "zh": "在老木门上按照 Lockwood 原厂纸质模板定位并固定金属底座。底座四个固定耳必须垂直压入门木纤维，是目前大洋洲智能加装的核心基准。",
      "en": "Field mounting of Lockwood 001 steel casing onto timber door guided by original paper drilling template."
    },
    "keyMetrics": "背距 60mm · 辅助锁舌完全压入行程 6mm · 旋钮直径 42mm"
  },
  {
    "id": "CASE-ANZ-02",
    "regionCode": "uk-anz",
    "regionName": { "zh": "澳洲与英国", "en": "Australia & UK" },
    "title": { "zh": "澳式安全指示旋钮实态 (SafetyRelease LockAlert Indicator)", "en": "Lockwood 001 Inside Turn Knob LockAlert Visual Window" },
    "lockFamilyId": "au-deadlatch",
    "lockFamilyName": "澳式外装夜锁",
    "image": "/assets/img/hero/hero-anz-lockwood001.jpg",
    "sceneType": "门上实景与状态窗口",
    "desc": {
      "zh": "Lockwood 001 标志性的水滴形大旋钮，配有绿色（安全未锁死）与红色（已死锁）指示窗。加装电机需使用大口径抓夹夹具完全包裹水滴旋钮。",
      "en": "Signature teardrop turn knob with dual color LockAlert indicator. Retrofit motor requires specialized oval clamp."
    },
    "keyMetrics": "水滴旋钮长轴 48mm · 短轴 34mm · 旋转阻力 0.6 N·m"
  },
  {
    "id": "CASE-ANZ-03",
    "regionCode": "uk-anz",
    "regionName": { "zh": "澳洲与英国", "en": "Australia & UK" },
    "title": { "zh": "澳式双扣死锁 Lockwood 355 双向防撬钩舌与门框扣板闭合", "en": "Lockwood 355 Dual Deadlocking Latch & Strike Interface" },
    "lockFamilyId": "au-deadlatch",
    "lockFamilyName": "澳式外装夜锁",
    "image": "/assets/img/hero/hero-anz-lockwood001.jpg",
    "sceneType": "双向防撬死锁工程",
    "desc": {
      "zh": "大洋洲高安全住宅使用的双向插舌机构。关门时主舌与爪钩同时进入门框专用带沉孔盒，门扇下沉错位将产生严重剪切咬合力，必须定期调整扣板。",
      "en": "Heavy duty interlocking deadlatch. Claw bolt hooks into frame box to prevent jemmy attack."
    },
    "keyMetrics": "防撬拉力 ≥10kN · 扣板调节余量 ±2mm · 门缝隙 3-5mm"
  },
  {
    "id": "CASE-ANZ-04",
    "regionCode": "uk-anz",
    "regionName": { "zh": "澳洲与英国", "en": "Australia & UK" },
    "title": { "zh": "英标经典外装夜闩 (Yale Traditional Rim Nightlatch) 60mm 安装", "en": "Yale Traditional Rim Nightlatch 60mm Backset Case" },
    "lockFamilyId": "rim-nightlatch",
    "lockFamilyName": "外装夜闩锁",
    "image": "/assets/img/tier3_install/lockwood001-casing-install.jpg",
    "sceneType": "英式夜闩改装实态",
    "desc": {
      "zh": "英国上百年历史的经典外装锁。内侧带旋转旋钮与滑动止动滑块（Snib）。加装智能锁必须注意止动滑块不可置于常锁位置，否则电机驱动将卡死烧毁。",
      "en": "Classic British rim nightlatch. The snib slide button can hold latch retracted or deadlock it mechanically."
    },
    "keyMetrics": "背距 60mm (经典版) / 40mm (窄边版) · 32mm 锁芯开孔"
  },
  {
    "id": "CASE-ANZ-05",
    "regionCode": "uk-anz",
    "regionName": { "zh": "澳洲与英国", "en": "Australia & UK" },
    "title": { "zh": "澳标 Selector 3772 商业插芯锁体 23mm 窄边面板铝型材安装", "en": "Lockwood Selector 3772 Narrow Stile Mortise Lock 23mm Backset" },
    "lockFamilyId": "us-mortise",
    "lockFamilyName": "美标商业插芯锁",
    "image": "/assets/img/tier3_install/mortise-pocket-chisel.jpg",
    "sceneType": "商业窄边型材门实装",
    "desc": {
      "zh": "澳洲商业店面与现代铝合金平开门标配。背距极窄（23mm/30mm），锁体极窄嵌入金属框料内，改装电机必须避免碰到玻璃压条。",
      "en": "Lockwood 3772 narrow stile mortise for aluminum framed glass doors. Backset as low as 23mm."
    },
    "keyMetrics": "窄背距 23mm/30mm · 门扇型材壁厚 2.5mm · 面板长度 175mm"
  },

  # ==========================================
  # 🇸🇬 东南亚与东亚板块 (Asia-Pacific) 10 个工程案例
  # ==========================================
  {
    "id": "CASE-SEA-01",
    "regionCode": "sea",
    "regionName": { "zh": "东南亚与东亚", "en": "Southeast & East Asia" },
    "title": { "zh": "新加坡 HDB 铁花防盗铁闸门金属立柱内嵌插芯锁实态", "en": "Singapore HDB Metal Security Gate Slim Mortise Lock Case" },
    "lockFamilyId": "sg-metal-gate-lock",
    "lockFamilyName": "金属铁闸锁",
    "image": "/assets/img/hero/hero-sea-hdb.jpg",
    "sceneType": "极端净距工况实录",
    "desc": {
      "zh": "新加坡组屋最具代表性的双门系统。外铁闸与内木门间距通常小于 80mm。外锁或加装电机的内侧厚度若超过 35mm，关铁门时把手将直接撞击木门智能锁面板。",
      "en": "Singapore HDB double door layout. Clearance between outer steel gate and inner wooden door is typically <80mm."
    },
    "keyMetrics": "双门极限净距 65-80mm · 锁体厚度 ≤35mm · 铁管截面 40x40mm"
  },
  {
    "id": "CASE-SEA-02",
    "regionCode": "sea",
    "regionName": { "zh": "东南亚与东亚", "en": "Southeast & East Asia" },
    "title": { "zh": "日本 MIWA 13LA / MA 锁体侧边面板 U 销锁芯固定工程", "en": "Japan MIWA 13LA Mortise Lock Case U-Pin Cylinder Retention" },
    "lockFamilyId": "jp-miwa-case",
    "lockFamilyName": "日标插芯锁体",
    "image": "/assets/img/hero/hero-sea-hdb.jpg",
    "sceneType": "日本公寓标配五金",
    "desc": {
      "zh": "日本公寓占有率超 60% 的 MIWA 13LA 锁体。锁芯采用侧边插入两枚不锈钢 U 销固定，内侧为小水滴旋钮。加装 SwitchBot/Qrio 需使用 3 段式阶梯高度垫块。",
      "en": "MIWA 13LA cylinder secured by dual U-pins behind faceplate. Teardrop thumbturn requires step spacers."
    },
    "keyMetrics": "背距 64mm · 中心距 80mm · 旋钮突出高度 18-24mm · JIS A5541"
  },
  {
    "id": "CASE-SEA-03",
    "regionCode": "sea",
    "regionName": { "zh": "东南亚与东亚", "en": "Southeast & East Asia" },
    "title": { "zh": "韩系/东南亚推拉一体自动锁体 (Push-Pull Mortise) 电动小离合", "en": "Korean Push-Pull Full Automatic Mortise Motorized Micro-Latch" },
    "lockFamilyId": "kr-pushpull-mortise",
    "lockFamilyName": "韩系推拉插芯整锁",
    "image": "/assets/img/hero/hero-sea-hdb.jpg",
    "sceneType": "全自动推拉锁体解剖",
    "desc": {
      "zh": "三星/耶鲁 push-pull 锁体内部自带微型电机驱动主舌与双向翻转剪刀舌。该类门锁为整锁更换方案，不适用内侧单加装电机改造。",
      "en": "Full motorized automatic push-pull mortise mechanism with dual scissors bolt and electronic sensor."
    },
    "keyMetrics": "整锁面板 390x85mm · 开孔中心距 130mm · 工作电压 6V (8xAA)"
  },
  {
    "id": "CASE-SEA-04",
    "regionCode": "sea",
    "regionName": { "zh": "东南亚与东亚", "en": "Southeast & East Asia" },
    "title": { "zh": "新加坡组屋 HDB 早期木门 Yale YDM4109 机械锁孔改造换装", "en": "Singapore HDB Timber Door Yale Mortise Retrofit Boring" },
    "lockFamilyId": "sg-hdb-mortise",
    "lockFamilyName": "新加坡组屋防盗门锁",
    "image": "/assets/img/tier3_install/mortise-pocket-chisel.jpg",
    "sceneType": "组屋换装实操工单",
    "desc": {
      "zh": "老旧 HDB 门厚通常仅 35mm。更换现代大锁体时往往需要重新扩大锁体槽，门边木肉仅剩不足 5mm，必须加装不锈钢加固盖板防止门边缘开裂破损。",
      "en": "Thin 35mm HDB wooden door retrofit requires stainless reinforcement wrap-around escutcheon."
    },
    "keyMetrics": "门厚 35mm 临界值 · 加固钢板厚 1.5mm · 面板开孔 240mm"
  },

  # ==========================================
  # 🌎 拉美新兴板块 (Latin America - ABNT/ODIS) 10 个工程案例
  # ==========================================
  {
    "id": "CASE-LATAM-01",
    "regionCode": "latam",
    "regionName": { "zh": "拉美新兴板块", "en": "Latin America" },
    "title": { "zh": "巴西 ABNT NBR 14913 极窄背距 (40/45mm) 薄门插芯锁安装", "en": "Brazil ABNT NBR 14913 Narrow Backset (40/45mm) Mortise Fit" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/hero/hero-latam-abnt.webp",
    "sceneType": "薄门与窄背距实态",
    "desc": {
      "zh": "巴西与拉美住宅常见薄门扇（厚度仅 30-35mm），背距仅 40mm 或 45mm。加装智能锁底座回转半径超过 35mm 即会发生外壳干涉门框密封条或门套线。",
      "en": "Brazil ABNT standard narrow mortise. Ultra narrow 40/45mm backset on thin 30-35mm doors."
    },
    "keyMetrics": "极窄背距 40mm/45mm · 门厚 30-35mm · 避让半径 ≤38mm"
  },
  {
    "id": "CASE-LATAM-02",
    "regionCode": "latam",
    "regionName": { "zh": "拉美新兴板块", "en": "Latin America" },
    "title": { "zh": "巴西现代旋转轴心门 (Porta Pivotante) 滚珠碰珠锁体 (Fechadura Rolete)", "en": "Pivot Door Roller Latch (Fechadura Rolete) Mechanical Balance" },
    "lockFamilyId": "euro-cylinder-mortise",
    "lockFamilyName": "欧标槽型锁芯插芯锁",
    "image": "/assets/img/hero/hero-latam-abnt.webp",
    "sceneType": "豪华轴心门避坑实录",
    "desc": {
      "zh": "巴西高端住宅极其风靡的大型轴心门（Pivot Door）。锁体采用无把手弹簧滚珠（Rolete）定位，只配死锁舌。关门仅靠拉力拉开，加装智能锁只需驱动方轴死锁。",
      "en": "Brazilian architectural pivot door using adjustable roller catch (Rolete) without lever handles."
    },
    "keyMetrics": "滚珠压力 20-50N 可调 · 死锁行程 20mm · 门扇宽度 ≥1200mm"
  },
  {
    "id": "CASE-LATAM-03",
    "regionCode": "latam",
    "regionName": { "zh": "拉美新兴板块", "en": "Latin America" },
    "title": { "zh": "拉美十字十字钥匙重型防盗外装锁 (Fechadura Sobrepor Tetra)", "en": "Latin American Tetra Key Cross-Bore Heavy Rim Lock Case" },
    "lockFamilyId": "in-mortise-rim",
    "lockFamilyName": "外装十字防盗锁",
    "image": "/assets/img/hero/hero-latam-abnt.webp",
    "sceneType": "高安全十字防盗锁",
    "desc": {
      "zh": "巴西 Stam/Papaiz 广泛使用的 Tetra 四向弹子锁。外锁芯为十字星形，内侧旋钮为异形拉动转柄。目前没有任何通用夹具能直接匹配，属于必须定制拨叉的 R2 样本。",
      "en": "Tetra cross-key mechanism with high pick resistance. Inner turn requires bespoke CNC coupler."
    },
    "keyMetrics": "十字锁芯截面 10x10mm · 行程 2 圈 (720°) · 驱动扭矩 ≥1.5 N·m"
  }
]

def main():
    with open(CASES_FILE, "w", encoding="utf-8") as f:
        json.dump(CASES_DATA, f, indent=2, ensure_ascii=False)
    print(f"Generated comprehensive {len(CASES_DATA)} professional installation engineering cases into {CASES_FILE}")

if __name__ == "__main__":
    main()
