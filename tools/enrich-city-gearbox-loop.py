import json

def enrich_city_gearbox():
    with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        region = item.get('block') or item.get('regionCode') or 'na'
        fam = item.get('familyId', '')

        # 1. 核心代表城市分布热力 (Metropolitan Cities)
        # 2. 齿轮箱减速比与反向自锁力矩 (Gearbox Ratio & Back-drive Torque)
        # 3. 钥匙外露剪切平面规尺 (Key Cylinder Extension & Shear Line Clearance)
        if region == 'na':
            cities = ["纽约 (NYC)", "洛杉矶 (LA)", "芝加哥 (Chicago)", "多伦多 (Toronto)", "温哥华 (Vancouver)"]
            gearbox = "推荐减速比 1:75 ~ 1:90；双向电磁/离合自锁力矩 0.35 N·m；手动物理开锁阻尼 ≤0.25 N·m"
            shear_line = "外露凸出量 2.0~4.5mm；内侧旋钮底座沉槽需留空直径 ≥38mm，沉孔深度 ≥3.0mm，确保扁条完全插入剪切轴芯"
        elif region == 'europe5':
            cities = ["巴黎 (Paris)", "柏林 (Berlin)", "法兰克福 (Frankfurt)", "马德里 (Madrid)", "维也纳 (Vienna)"]
            gearbox = "推荐减速比 1:110 ~ 1:130 (大扭矩克服多点联动)；行星减速箱，离合器必须具备通电脱开功能"
            shear_line = "DIN 水滴外露高度标准为 3mm 或 5mm；加装底盘厚度严禁超过 2.5mm，否则钥匙无法插至剪切平面触发旋转"
        elif region == 'uk-anz':
            cities = ["伦敦 (London)", "悉尼 (Sydney)", "墨尔本 (Melbourne)", "曼彻斯特 (Manchester)", "布里斯班 (Brisbane)"]
            gearbox = "推荐减速比 1:85 ~ 1:100；夜闩锁回弹弹簧较强，关门时自锁力矩需 ≥0.45 N·m 稳固锁舌"
            shear_line = "Lockwood 001 旋钮高度 28mm；内侧夹爪必须包裹外缘并预留 15mm 钥匙孔直接对穿孔"
        elif region == 'sea':
            cities = ["东京 (Tokyo)", "新加坡 (Singapore)", "大阪 (Osaka)", "首尔 (Seoul)", "吉隆坡 (Kuala Lumpur)"]
            gearbox = "推荐减速比 1:60 ~ 1:75 (超静音微型行星齿轮箱)；低阻尼自锁力矩 0.20 N·m"
            shear_line = "日式超薄锁体间隙 ≤1.0mm；旋钮抓手避让外圈沉深 5mm，双侧捏合行程精准控制在 2.5mm"
        else: # latam
            cities = ["圣保罗 (São Paulo)", "里约热内卢 (Rio de Janeiro)", "圣地亚哥 (Santiago)", "波哥大 (Bogotá)", "布宜诺斯艾利斯 (Buenos Aires)"]
            gearbox = "推荐减速比 1:100 ~ 1:120 (金属粉末冶金齿轮)；高自锁力矩 ≥0.50 N·m 抵抗重门震动"
            shear_line = "40mm 极窄锁体距门框边缘仅 40mm；加装锁壳横向半宽严禁超过 38mm，防止剐蹭密封条"

        if 'engineeringMatrix' not in item:
            item['engineeringMatrix'] = {}

        item['engineeringMatrix']['representativeCities'] = cities
        item['engineeringMatrix']['gearboxSpec'] = gearbox
        item['engineeringMatrix']['shearLineClearance'] = shear_line

    with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully enriched all {len(data)} locks with Cities, Gearbox, and Shear Line specs!")

if __name__ == '__main__':
    enrich_city_gearbox()
