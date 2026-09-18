import json

with open('content/catalog/gallery.json', 'r', encoding='utf-8') as f:
    gallery = json.load(f)

for item in gallery:
    em = item.setdefault('engineeringMatrix', {})
    if 'rentalOptimization' not in em:
        em['rentalOptimization'] = {
            "friendly": True,
            "rating": "Grade A- (免打孔选配超长紧固件)",
            "modificationType": "Non-destructive",
            "notes": "中东公寓实木门无需破坏性开孔"
        }
    if 'egressCompliance' not in em:
        em['egressCompliance'] = {
            "standard": "SASO / EN 179 Panic Safe",
            "isSafe": True,
            "backdriveTorqueMax": "≤0.35 N·m",
            "description": "内侧具备逃生优先权"
        }
    if 'compactSpecs' not in em:
        em['compactSpecs'] = {
            "backset": "60mm",
            "centres": "85mm",
            "spindle": "8×8mm",
            "thickness": "55-85mm"
        }
    if 'keywaySpecification' not in em:
        em['keywaySpecification'] = "Yale / Cisa 欧规槽型钥匙"
    if 'coldWeatherDerating' not in em:
        em['coldWeatherDerating'] = "0°C ~ +75°C (超耐高温暴晒工况)"
    if 'handleSpringResistance' not in em:
        em['handleSpringResistance'] = "≥ 35 N·cm (重型回弹扭簧)"
    if 'mortiseReworkGuide' not in em:
        em['mortiseReworkGuide'] = "BS 85mm 重型深槽，门厚建议 ≥50mm"
    if 'boltWireClearance' not in em:
        em['boltWireClearance'] = "标配 120mm 超长高碳钢对穿螺栓"

with open('content/catalog/gallery.json', 'w', encoding='utf-8') as f:
    json.dump(gallery, f, ensure_ascii=False, indent=2)

print("Fixed rentalOptimization & engineering matrix for all locks!")
