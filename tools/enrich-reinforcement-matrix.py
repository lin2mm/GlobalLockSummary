import json

def enrich_reinforcement():
    with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 海外老旧门锁侧边木槽二次扩孔规范 (Chisel Mortise Rework)
    # 2. 智能锁对穿螺栓剪切公差与防夹线套管 (Through-bolt & Wire Guide)
    # 3. 紧凑型工程参数 (Compact Engineering Specs)
    for item in data:
        region = item.get('block') or item.get('regionCode') or 'na'
        fam = item.get('familyId', '')

        if region == 'na':
            mortise_rework = "死锁门边钻孔 25.4mm (1\")，门面 54mm (2-1/8\")；如遇老旧门扇开裂，需加装不锈钢防劈裂抱门锁夹套板 (Wrap-Around Reinforcer)"
            bolt_wire = "双内六角贯穿对穿螺丝 (#10-32)，走线通道需位于扁平尾轴正下方，预留 ≥4mm 硅胶绝缘套管避让区"
            compact_specs = {"backset": "60/70mm 可调", "centres": "独立分体", "spindle": "1.6×4.8mm 扁平尾轴", "thickness": "35-51mm"}
        elif region == 'eu':
            mortise_rework = "DIN 18251 锁槽深度原为 75-80mm；改装加长智能插芯若需凿深至 90mm，必须沿门梃中心线钻阶梯孔，使用 20mm 扁平木工凿微修，严禁劈裂门扇立挺"
            bolt_wire = "M5 欧规沉头对穿螺栓，锁芯上方设专属穿线橡胶护线圈 (Grommet)，严防执手下压时方轴与线束摩擦"
            compact_specs = {"backset": "55/65mm", "centres": "72/92mm PZ", "spindle": "8×8mm (逃生9×9mm)", "thickness": "38-65mm"}
        elif region == 'oc' or region == 'uk':
            mortise_rework = "英式 5-lever 锁槽较深 (通常 80-100mm)；Lockwood 001 为表面装配，门体仅需打 32mm 锁芯对穿孔，无需凿槽，但必须在门框安装不锈钢加固角铁扣盒"
            bolt_wire = "表面底盘 4 颗 10# 镀锌螺钉固定，旋钮传动拨叉内置防缠绕护套"
            compact_specs = {"backset": "60mm", "centres": "分体夜闩", "spindle": "十字/偏心尾轴", "thickness": "32-45mm"}
        elif region == 'sea' or region == 'asia':
            mortise_rework = "日式 MIWA/GOAL 锁槽开孔极其精密 (间隙 ≤1.0mm)；铝合金窄框门严禁重击凿削，必须采用金属铣刀开孔，加装 1.5mm 铝衬板加固"
            bolt_wire = "M4 高精贯穿螺栓，日韩超薄门体 (33mm) 必须使用剪切型对穿螺钉，走线通道置于锁体顶部专属滑槽"
            compact_specs = {"backset": "51/64mm", "centres": "独立/联动", "spindle": "8×8mm 高精", "thickness": "33-42mm"}
        else: # latam
            mortise_rework = "拉美 40mm 极窄浅槽 (深度通常仅 60mm)；若改装大电机锁体需向内扩孔 20mm，必须加装 2.0mm 冷轧钢加强扣板以防撬门"
            bolt_wire = "M4 粗牙螺栓对穿，薄夹板门必须在内部加装垫片防止夹板被螺钉压溃变形"
            compact_specs = {"backset": "40/45mm 极窄", "centres": "53/70mm", "spindle": "8×8mm 粗公差", "thickness": "30-35mm"}

        if 'engineeringMatrix' not in item:
            item['engineeringMatrix'] = {}

        item['engineeringMatrix']['mortiseReworkGuide'] = mortise_rework
        item['engineeringMatrix']['boltWireClearance'] = bolt_wire
        item['engineeringMatrix']['compactSpecs'] = compact_specs

    with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully injected Mortise Rework, Wire Guide & Compact Specs into all {len(data)} locks!")

if __name__ == '__main__':
    enrich_reinforcement()
