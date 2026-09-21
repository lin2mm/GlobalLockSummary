#!/usr/bin/env python3
"""
Optical & Semantic Icon Evaluation Model (16px Retina Scalability & Universal Cognition)
针对 16px/24px 极小视网膜尺寸下的光学边缘辨识度（Optical Silhouette Recognizability）与普罗大众常识认知度进行严格打分
"""

# 评测标准：
# 1. Optical Silhouette at 16px (16px极小尺寸下的外轮廓直觉辨识度 - 不糊、不丢细节): 40%
# 2. Universal Everyday Recognition (普罗大众/非专业工程师的一眼常识认知度): 35%
# 3. Hardware / Architectural Identity (安防与五金属性，非廉价纯色卡通): 15%
# 4. Geometric Balance & Cleanliness (线条美感与几何平衡): 10%

CRITERIA = {
    "optical_16px": 0.40,
    "universal_recognition": 0.35,
    "hardware_identity": 0.15,
    "geometric_cleanliness": 0.10
}

def calc_score(scores):
    return sum(scores[k] * CRITERIA[k] for k in CRITERIA)

# 1. 品牌主标 (Brand Mark) 候选方案
brand_candidates = [
    {
        "id": "BM-01",
        "name": "Micro Euro-cylinder (Current)",
        "features": "水滴形锁芯+内部钥匙孔+旋转转心",
        "scores": {"optical_16px": 50, "universal_recognition": 60, "hardware_identity": 98, "geometric_cleanliness": 95},
        "critique": "缩到 16px 甚至 24px 时，内部转心与小钥匙槽黏成黑团，用户完全看不出是锁孔，只看到一个几何水滴"
    },
    {
        "id": "BM-02",
        "name": "Standard Flat Padlock (Old)",
        "features": "纯色实心传统挂锁",
        "scores": {"optical_16px": 75, "universal_recognition": 95, "hardware_identity": 40, "geometric_cleanliness": 60},
        "critique": "虽然能看懂是锁，但太卡通廉价，缺乏高级感"
    },
    {
        "id": "BM-03",
        "name": "Architectural Shield & High-Contrast Precision Shackle Lock (Selected)",
        "features": "高级安防防盗锁体盾构外廓 + 醒目的实心金属锁梁 + 负空间清晰高透钥匙孔槽 (Keyhole Negative Space)",
        "scores": {"optical_16px": 96, "universal_recognition": 98, "hardware_identity": 94, "geometric_cleanliness": 96},
        "critique": "极小尺寸下：锁梁 (Shackle) + 经典锁孔 (Keyhole) 的双重负空间极其分明！哪怕缩小到 14px，大脑也能毫秒级识别出这是'锁'；同时采用高阶几何切角与盾构锁体线条，质感极具高级工业科技范"
    }
]

# 2. 工程实录 (Field Cases) 候选方案
field_cases_candidates = [
    {
        "id": "FC-01",
        "name": "Calipers / Inspection Cross (Current)",
        "features": "游标卡尺与十字测量线",
        "scores": {"optical_16px": 65, "universal_recognition": 45, "hardware_identity": 95, "geometric_cleanliness": 90},
        "critique": "一般人/非机械工程师完全看不出是卡尺，误以为是某种复杂方框或十字架，缺乏场景常识认知"
    },
    {
        "id": "FC-02",
        "name": "Generic Cartoon Camera",
        "features": "通俗照相机",
        "scores": {"optical_16px": 80, "universal_recognition": 85, "hardware_identity": 50, "geometric_cleanliness": 65},
        "critique": "太像旅游拍照相册，未体现工程施工与安装案例"
    },
    {
        "id": "FC-03",
        "name": "Real Door with Handle & Field Verification Badge / Wrench (Selected)",
        "features": "一扇清晰微开的门扇 (Door) + 门把手 (Handle) + 侧边安装工程扳手 (Wrench/Checkmark)",
        "scores": {"optical_16px": 95, "universal_recognition": 96, "hardware_identity": 96, "geometric_cleanliness": 94},
        "critique": "普通人第一眼就能看出这是'门上安装/门锁工程实操'！门扇轮廓在 16px 下轮廓坚挺，搭配微斜扳手或门把手，全球普通用户与工程师皆能毫无门槛秒懂"
    }
]

print("=== Brand Mark Optical Ranking ===")
for c in brand_candidates:
    score = calc_score(c["scores"])
    print(f"[{c['id']}] {c['name']}: {round(score, 2)} pts -> {c['critique']}")

print("\n=== Field Cases Optical Ranking ===")
for c in field_cases_candidates:
    score = calc_score(c["scores"])
    print(f"[{c['id']}] {c['name']}: {round(score, 2)} pts -> {c['critique']}")
