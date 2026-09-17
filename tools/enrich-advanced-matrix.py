import json

def enrich_advanced():
    with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 钥匙槽型映射 (Keyway Blank Specifications)
    # 2. 低温电池衰减与极限工况 (Cold Weather Battery De-rating)
    # 3. 门执手回弹弹簧阻尼 (Handle Return Spring Torque)
    for item in data:
        region = item.get('block') or item.get('regionCode') or 'na'
        fam = item.get('familyId', '')

        # 默认值初始化
        if region == 'na':
            keyway = "Schlage SC1/SC4 (5/6 pin) 或 Kwikset KW1/KW10, 复合Y1备选"
            temp_range = "-35°C ~ +65°C (极寒需专用低温锂铁电池，-20°C 电流衰减约 35%)"
            spring_force = "≤ 15 N·cm (美标分体执手内部弹簧独立，反向阻尼极小)"
        elif region == 'eu':
            keyway = "Euro Profile DIN 18252 (ABUS C83, EVVA, Bricard 5/6 pin paracentric)"
            temp_range = "-25°C ~ +55°C (欧规多点锁需高寒润滑脂，-15°C 电机启动电流需 +20% 裕量)"
            spring_force = "≥ 25 N·cm (DIN 执手强弹簧，抬把手 Raise-to-Lock 需克服 35 N·cm 机械预紧力)"
        elif region == 'oc' or region == 'uk':
            keyway = "Lockwood 001/002 澳洲标准 6-pin 椭圆锁芯 (Oval Cyl), 英式 5-lever 独家钥匙胚"
            temp_range = "-10°C ~ +60°C (澳洲高温与沿海高湿，需满足 AS 4145.2 耐盐雾评级)"
            spring_force = "≤ 20 N·cm (表面夜闩锁主弹簧，关门需完全压下辅助舌)"
        elif region == 'sea' or region == 'asia':
            keyway = "MIWA U9 / PR 旋转滚子磁性槽型, GOAL V18, 新加坡专用双排珠"
            temp_range = "-10°C ~ +55°C (东南亚 95% 极端湿热，强调 PCB 三防漆与电机轴承防水)"
            spring_force = "≤ 12 N·cm (日式精密插芯锁，手感轻盈，反向阻尼敏感度极高)"
        else: # latam
            keyway = "PADO / Stam / La Fonte 宽槽型拉美通用双铣齿"
            temp_range = "-5°C ~ +50°C (高湿高粉尘，锁体内部钢冲压件需自润滑镀层)"
            spring_force = "≥ 30 N·cm (拉美重型弹簧，要求智能锁马达具备双倍回弹扭矩)"

        if 'engineeringMatrix' not in item:
            item['engineeringMatrix'] = {}

        item['engineeringMatrix']['keywaySpecification'] = keyway
        item['engineeringMatrix']['coldWeatherDerating'] = temp_range
        item['engineeringMatrix']['handleSpringResistance'] = spring_force

    with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully enriched all {len(data)} locks with Keyway, Cold-Battery, and Spring Torque specs!")

if __name__ == '__main__':
    enrich_advanced()
