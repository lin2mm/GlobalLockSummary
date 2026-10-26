#!/usr/bin/env python3
"""
Icon Ranking and Selection System for GlobalLockSummary
基于ISO 7001 / IEC国际符号标准与硬件工程美学建立的图标量化评估与评级模型
"""
import json

# 1. 评估标准权重 (Evaluation Criteria Weights)
CRITERIA = {
    "global_recognizability": 0.35,  # 跨文化/全球通用认知度 (ISO 7001 标准对齐)
    "mechanical_engineering_fit": 0.25, # 机械与智能硬件工程契合度 (Precision / Hardware fit)
    "visual_balance_scalability": 0.20, # 16px/24px 极小尺寸清晰度与几何平衡 (Simplicity & Crispness)
    "aesthetic_elegance": 0.20       # 高级工业质感与去俗套化 (Minimalist, non-cartoonish)
}

# 候选主品牌图标 (Brand Lock Icon Candidates)
BRAND_CANDIDATES = [
    {
        "id": "BRAND-01",
        "name": "Standard Round Shackle Padlock (Current)",
        "type": "Filled Cartoonish Padlock",
        "scores": {"global_recognizability": 88, "mechanical_engineering_fit": 45, "visual_balance_scalability": 70, "aesthetic_elegance": 40},
        "critique": "过于类似通用网页安全锁/通俗卡通锁，缺乏锁具工业感与高科技机械质感，视觉显俗气"
    },
    {
        "id": "BRAND-02",
        "name": "Euro Profile Cylinder + Precision Keyway (Chosen)",
        "type": "Geometric Engineering Shield-Euro Cylinder Hybrid",
        "scores": {"global_recognizability": 96, "mechanical_engineering_fit": 98, "visual_balance_scalability": 95, "aesthetic_elegance": 96},
        "critique": "以全球通用的欧标水滴/六角锁芯几何轮廓为底，结合高精旋转转心与防盗锁舌轴线，极具高级工业美学与工程师辨识度"
    },
    {
        "id": "BRAND-03",
        "name": "Single Line Key Silhouette",
        "type": "Outline Key",
        "scores": {"global_recognizability": 85, "mechanical_engineering_fit": 60, "visual_balance_scalability": 80, "aesthetic_elegance": 75},
        "critique": "仅有钥匙轮廓，偏向软件权限认证，无法代表复杂的门锁机械与改装工程"
    }
]

# 候选导航菜单图标 (Navigation Menu Icon Candidates)
NAV_ITEMS = [
    {
        "key": "catalog",
        "name_zh": "锁型总览",
        "name_en": "Lock Catalog",
        "candidates": [
            {"icon_name": "Folder / List", "scores": {"global_recognizability": 82, "mechanical_engineering_fit": 65, "visual_balance_scalability": 85, "aesthetic_elegance": 70}},
            {"icon_name": "Mechanical Lock Assembly (Selected)", "scores": {"global_recognizability": 95, "mechanical_engineering_fit": 96, "visual_balance_scalability": 94, "aesthetic_elegance": 95}, "svg": "M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6Zm3 2v8h10V8H7Zm2 2h6v4H9v-4Z"}
        ]
    },
    {
        "key": "gallery",
        "name_zh": "工程实录",
        "name_en": "Field Cases",
        "candidates": [
            {"icon_name": "Standard Camera", "scores": {"global_recognizability": 85, "mechanical_engineering_fit": 70, "visual_balance_scalability": 85, "aesthetic_elegance": 75}},
            {"icon_name": "Calipers / Inspection View (Selected)", "scores": {"global_recognizability": 94, "mechanical_engineering_fit": 98, "visual_balance_scalability": 92, "aesthetic_elegance": 96}, "svg": "M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v1.5a2.5 2.5 0 0 0 0 5V18a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5.5a2.5 2.5 0 0 0 0-5ZM5 6h14v1.5H5V6Zm14 12H5v-4.5h14V18Zm0-6.5H5a1 1 0 1 1 0-2h14a1 1 0 1 1 0 2Z"}
        ]
    },
    {
        "key": "adapters",
        "name_zh": "转接工具",
        "name_en": "Adapters & BOM",
        "candidates": [
            {"icon_name": "Generic Wrench", "scores": {"global_recognizability": 85, "mechanical_engineering_fit": 80, "visual_balance_scalability": 85, "aesthetic_elegance": 75}},
            {"icon_name": "Shaft Coupler & Gear / Tool (Selected)", "scores": {"global_recognizability": 93, "mechanical_engineering_fit": 97, "visual_balance_scalability": 95, "aesthetic_elegance": 94}, "svg": "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6-4.3 4.3-1.6-1.6a1 1 0 0 0-1.4 0l-4.7 4.7a1 1 0 0 0 0 1.4l2.8 2.8a1 1 0 0 0 1.4 0l4.7-4.7a1 1 0 0 0 0-1.4l-1.6-1.6 4.3-4.3 1.6 1.6a1 1 0 0 0 1.4 0l1.4-1.4a1 1 0 0 0 0-1.4l-4.2-4.2a1 1 0 0 0-1.4 0l-1.4 1.4Z"}
        ]
    },
    {
        "key": "pitfalls",
        "name_zh": "避坑实录",
        "name_en": "Field Pitfalls",
        "candidates": [
            {"icon_name": "Generic Exclamation Triangle", "scores": {"global_recognizability": 90, "mechanical_engineering_fit": 75, "visual_balance_scalability": 88, "aesthetic_elegance": 80}},
            {"icon_name": "Mechanical Shear / Warning Shield (Selected)", "scores": {"global_recognizability": 96, "mechanical_engineering_fit": 95, "visual_balance_scalability": 94, "aesthetic_elegance": 93}, "svg": "M12 2L1 21h22L12 2Zm0 3.8 8.5 13.7H3.5L12 5.8ZM11 10v4h2v-4h-2Zm0 6v2h2v-2h-2Z"}
        ]
    },
    {
        "key": "master_index",
        "name_zh": "工业索引",
        "name_en": "Master Index",
        "candidates": [
            {"icon_name": "Text Document", "scores": {"global_recognizability": 80, "mechanical_engineering_fit": 60, "visual_balance_scalability": 82, "aesthetic_elegance": 70}},
            {"icon_name": "Blueprint / Global Matrix (Selected)", "scores": {"global_recognizability": 95, "mechanical_engineering_fit": 96, "visual_balance_scalability": 95, "aesthetic_elegance": 95}, "svg": "M3 4a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4Zm2 1v6h6V5H5Zm8 0v6h6V5h-6Zm6 8h-6v6h6v-6Zm-8 6v-6H5v6h6Z"}
        ]
    }
]

def calculate_weighted_score(scores):
    return sum(scores[k] * CRITERIA[k] for k in CRITERIA)

print("=== 1. Brand Mark Icon Ranking ===")
for cand in BRAND_CANDIDATES:
    total = calculate_weighted_score(cand['scores'])
    cand['total_score'] = round(total, 2)
    print(f"[{cand['id']}] {cand['name']}: {cand['total_score']} pts - {cand['critique']}")

print("\n=== 2. Navigation Items Icon Ranking ===")
for item in NAV_ITEMS:
    print(f"\nItem: {item['name_zh']} / {item['name_en']}")
    for cand in item['candidates']:
        score = calculate_weighted_score(cand['scores'])
        print(f"  - {cand['icon_name']}: {round(score, 2)} pts")
