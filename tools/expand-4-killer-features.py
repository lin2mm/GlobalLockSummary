import json

def expand_killer_features():
    with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
        gallery = json.load(f)

    # 1. 扩容 4 大杀手级核心版图数据字段：
    # - weatherproofingMatrix: 盐雾 ASTM B117 (h), 防护等级 IP, UV 耐老化, EPDM 胶条规范
    # - multipointKinematics: Winkhaus/GU/KFV 抬把手角度 (45°), 预紧克服阻尼 (N·m), 蘑菇头调节指南
    # - emergencyClutchWhitelist: 欧标双向离合官方白名单型号 (ABUS, EVVA, Bricard, ISEO)
    # - doorThicknessFastenerMatrix: 门厚与螺栓选配矩阵 (门厚, 螺栓长度, 方轴规格, 垫圈)

    for item in gallery:
        region = item.get('block') or item.get('regionCode') or 'na'
        em = item.setdefault('engineeringMatrix', {})

        # 1. 耐候标准与盐雾等级 (Weatherproofing Matrix)
        if region in ['gcc']:
            weather = {
                "saltSprayClass": "ASTM B117 480小时 (沿海重盐雾超高防腐电泳/PVD)",
                "ipRating": "IP65 沙暴防尘防水 (全密封双层硅胶垫圈圈闭)",
                "solarThermalMax": "+75°C ~ +80°C 太阳直射无热膨胀卡死",
                "epdmGasketSpec": "采用耐 120°C 宽温 EPDM 闭孔发泡密封圈，严禁普通天然橡胶"
            }
        elif region in ['sea', 'uk-anz']:
            weather = {
                "saltSprayClass": "ASTM B117 240小时 (热带海岛高湿海洋气候防腐)",
                "ipRating": "IP55 抵御暴雨与高湿凝露",
                "solarThermalMax": "+55°C",
                "epdmGasketSpec": "高弹性抗霉菌阻燃硅橡胶密封垫"
            }
        elif region in ['latam']:
            weather = {
                "saltSprayClass": "ASTM B117 144小时 (城市与沿海基础防锈)",
                "ipRating": "IP54 防泼水与灰尘",
                "solarThermalMax": "+60°C",
                "epdmGasketSpec": "耐候丁腈橡胶 NBR 减震密封垫片"
            }
        else: # na, europe5, jp-kr
            weather = {
                "saltSprayClass": "ASTM B117 96小时 (内陆与标准居住环境)",
                "ipRating": "IP54 防泼水",
                "solarThermalMax": "-40°C ~ +60°C 耐严寒低温锂电池补偿",
                "epdmGasketSpec": "耐低温耐老化硅胶密封衬垫"
            }
        em['weatherproofingMatrix'] = weather

        # 2. 多点联动抬把手与传动阻尼 (Multipoint Kinematics)
        if region in ['europe5', 'uk-anz']:
            em['multipointKinematics'] = {
                "isMultipointCompatible": True,
                "liftAngle": "45° 向上抬把手行程",
                "camDriveTorque": "1.2 ~ 1.8 N·m (克服 3~5 个蘑菇头偏心锁点摩擦力)",
                "majorHardwareVendors": "Winkhaus autoLock, GU-Secury, KFV/Siegenia",
                "fieldAdjustmentGuide": "门框扣盒偏心六角螺丝可微调 ±1.5mm 压缩间隙，降低抬把手阻尼 40%"
            }
        else:
            em['multipointKinematics'] = {
                "isMultipointCompatible": False,
                "liftAngle": "N/A (单点或传统直插式天地插锁)",
                "camDriveTorque": "0.35 ~ 0.65 N·m",
                "majorHardwareVendors": "ANSI Deadbolt / ABNT Standard",
                "fieldAdjustmentGuide": "调整门框平扣板沉深即可消除阻尼"
            }

        # 3. 欧标应急离合官方认证白名单 (Emergency Clutch Whitelist)
        if region in ['europe5']:
            em['emergencyClutchWhitelist'] = {
                "isMandatory": True,
                "standard": "DIN 18252 BS / EN 1303 Class 6 Emergency Clutch",
                "approvedModels": [
                    "ABUS Bravus 1000 / 2000 / 4000 MX (带 Not- und Gefahrenfunktion)",
                    "EVVA 4KS / EPS / ICS (带 BS 双向离合旋钮)",
                    "Bricard Chifral S2 (Série 70 兼容型双离合锁芯)",
                    "ISEO R6 Plus 双向同转防锁死锁芯"
                ],
                "lockoutRiskWarning": "严禁在无离合锁芯内侧常插钥匙加装智能锁，一旦电机故障将导致室外彻底锁死无法破门"
            }
        else:
            em['emergencyClutchWhitelist'] = {
                "isMandatory": False,
                "standard": "物理机械钥匙直通贯穿 (Physical Key Direct Override)",
                "approvedModels": ["原厂机械锁芯均保留独立外插物理钥匙开锁通路"],
                "lockoutRiskWarning": "保留外部物理钥匙插口，应急时直接插入旋转即可物理开锁"
            }

        # 4. 门扇厚度与对穿螺栓速查矩阵 (Door Thickness & Fastener Matrix)
        if region in ['gcc']:
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "60mm ~ 90mm (超厚实木及铸铝装甲防盗门)",
                "spindleRequirement": "8×8×130mm 高碳钢镀锌方轴 (带 5mm 预截槽)",
                "boltRequirement": "M5×110mm / M5×120mm 易断槽对穿螺丝包 (标配必须提供)",
                "reinforcementPlate": "必须在内侧加装 2.5mm 钢制加强拉紧背板，防止夹紧凹陷"
            }
        elif region in ['latam']:
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "30mm ~ 38mm (拉美超薄中空夹板门)",
                "spindleRequirement": "8×8×65mm 短方轴",
                "boltRequirement": "M4×45mm 短螺丝，必须加配 ADP-08 防压溃加强圈",
                "reinforcementPlate": "严禁大扭力电动螺丝刀直接紧固，必须用 32mm 垫圈分散压强"
            }
        elif region in ['na']:
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "35mm ~ 45mm (1-3/8\" ~ 1-3/4\" 标准木门)",
                "spindleRequirement": "死锁扁条尾轴 (Tailpiece 长度 45mm)",
                "boltRequirement": "1/4-20 粗牙十字盘头螺栓 (长 55mm / 65mm)",
                "reinforcementPlate": "标准 54mm 大孔内嵌金属固定底盘"
            }
        elif region in ['uk-anz']:
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "35mm ~ 50mm (澳洲标准实木大门)",
                "spindleRequirement": "Lockwood 001 专用偏心扁条与大旋钮转轴",
                "boltRequirement": "4× 木螺钉表面直接紧固 + 对穿螺柱 60mm",
                "reinforcementPlate": "选配 ADP-10 260×68mm 金属大背板无缝遮盖原厂打孔"
            }
        elif region in ['jp-kr']:
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "33mm ~ 42mm (日本防火不锈钢门)",
                "spindleRequirement": "MIWA 专用扁销与方轴组合",
                "boltRequirement": "M4×38mm 精密机丝，沉头防滑",
                "reinforcementPlate": "超窄边不锈钢压板"
            }
        else: # europe5
            em['doorThicknessMatrix'] = {
                "typicalDoorThickness": "40mm ~ 65mm (欧标入户木门与复合门)",
                "spindleRequirement": "8×8×90mm 镀锌方轴 (法国 7×7mm 需配 ADP-01)",
                "boltRequirement": "M5 对穿螺栓长 70mm~90mm",
                "reinforcementPlate": "DIN 标准 PZ 72/92mm 长条一体化或分体式盖板"
            }

    with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
        json.dump(gallery, f, ensure_ascii=False, indent=2)

    print(f"Successfully expanded 4 killer engineering features to all {len(gallery)} locks in gallery.json!")

if __name__ == '__main__':
    expand_killer_features()
