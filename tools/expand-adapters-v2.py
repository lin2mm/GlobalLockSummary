import json

with open('content/catalog/adapters-bom.json', 'r', encoding='utf-8') as f:
    adapters = json.load(f)

# 为每款转接件补充 3 大一线落地核心字段：
# 1. 3D 打印建议切片参数 (3D Print Slicing Config)
# 2. 批量采购/开模成本预估与代号 (Batch Unit Cost & Production Method)
# 3. 关联的核心锁型直链代码 (Associated Benchmark Lock IDs)

additional_specs = {
    "ADP-01": {
        "productionMethod": "H62黄铜 CNC 走心机精密车削 + 表面微倒角钝化",
        "batchCostEst": "$0.45 ~ $0.65 / 件 (5000pcs 批量)",
        "slicingConfig": "❌ 严禁 FDM/SLA 打印，纯金属件",
        "compatibleLockIds": ["EU-19", "EU-21", "EU-23"]
    },
    "ADP-02": {
        "productionMethod": "SUS304 激光切管 + 高精度拉拔",
        "batchCostEst": "$0.55 ~ $0.80 / 件 (5000pcs 批量)",
        "slicingConfig": "❌ 防火逃生强制受力件，严禁塑料件",
        "compatibleLockIds": ["EU-01", "EU-03", "EU-05"]
    },
    "ADP-03": {
        "productionMethod": "POM (赛钢) 高速注塑开模 (一模四穴) 或 SLS 激光烧结",
        "batchCostEst": "$0.25 ~ $0.35 / 件 (模具费约 $1,200)",
        "slicingConfig": "推荐材料 PETG / PA12-CF，填充率 ≥80%，壁厚 ≥4 层，层高 0.16mm",
        "compatibleLockIds": ["JP-01", "JP-02", "JP-05"]
    },
    "ADP-04": {
        "productionMethod": "航空铝 6061-T6 CNC 加工 + 喷砂阳极氧化",
        "batchCostEst": "$0.85 ~ $1.20 / 件 (2000pcs 批量)",
        "slicingConfig": "推荐材料 ABS / PLA-CF，填充率 100%，需耐受 ≥1.8 N·m 扭矩",
        "compatibleLockIds": ["US-01", "US-27", "US-28"]
    },
    "ADP-05": {
        "productionMethod": "PC/ABS 合金注塑 + 1.5mm 导电硅胶内胆双色模具",
        "batchCostEst": "$0.95 ~ $1.35 / 件 (含硅胶衬垫)",
        "slicingConfig": "推荐材料 TPU 95A (内衬垫) + PETG (外夹壳)，层高 0.20mm",
        "compatibleLockIds": ["AU-11", "AU-12", "AU-15"]
    },
    "ADP-06": {
        "productionMethod": "航空铝 7075 阳极黑 + 3× M3 平端淬火紧定螺钉",
        "batchCostEst": "$0.70 ~ $0.95 / 件",
        "slicingConfig": "打样可采用 PA-CF 碳纤维尼龙，紧定螺孔需预埋热熔铜螺母",
        "compatibleLockIds": ["EU-01", "EU-02", "EU-04", "GCC-01"]
    },
    "ADP-07": {
        "productionMethod": "SUS304 不锈钢连续冲压模具 (厚度 1.0/1.5/2.0mm 套装)",
        "batchCostEst": "$0.15 ~ $0.25 / 套 (含 3 种厚度)",
        "slicingConfig": "推荐金属冲压件，塑料件在门扇重力撞击下易蠕变变形",
        "compatibleLockIds": ["US-01", "AU-11", "EU-01", "GCC-01"]
    },
    "ADP-08": {
        "productionMethod": "冷轧钢 SPCC 冲压拉深 + 环保蓝白镀锌",
        "batchCostEst": "$0.20 ~ $0.30 / 对",
        "slicingConfig": "推荐 PETG / 尼龙，填充率 100%，内径 5.5mm",
        "compatibleLockIds": ["BR-01", "SG-01", "SG-04"]
    },
    "ADP-09": {
        "productionMethod": "65Mn 弹簧钢热卷淬火 + 磷化防锈处理",
        "batchCostEst": "$0.40 ~ $0.60 / 件",
        "slicingConfig": "❌ 强制弹簧钢，塑料件无法提供恒定 1.5 N·m 预紧扭力",
        "compatibleLockIds": ["EU-08", "EU-12", "UK-05"]
    },
    "ADP-10": {
        "productionMethod": "2.0mm SUS304 砂光拉丝板激光落料 + 沉孔倒角",
        "batchCostEst": "$1.40 ~ $1.90 / 片",
        "slicingConfig": "推荐打样采用 PLA 快速验证孔距，成品必须机加工不锈钢板",
        "compatibleLockIds": ["AU-11", "AU-13", "UK-01"]
    },
    "ADP-11": {
        "productionMethod": "10.9 级高碳钢冷镦 + 激光刻蚀 5mm 易断槽 + 环保镀锌",
        "batchCostEst": "$0.35 ~ $0.50 / 套 (2螺栓+1方轴)",
        "slicingConfig": "❌ 螺栓与方轴受力极大，严禁塑料件",
        "compatibleLockIds": ["GCC-01", "GCC-02", "EU-15"]
    },
    "ADP-12": {
        "productionMethod": "自润滑 POM 赛钢注塑 + 镶嵌 N52 钕铁硼强磁体",
        "batchCostEst": "$0.50 ~ $0.75 / 套",
        "slicingConfig": "推荐材料 PETG / ASA (耐户外紫外线)，填充率 ≥60%，内置磁铁凹槽",
        "compatibleLockIds": ["US-01", "EU-01", "AU-11", "GCC-01"]
    }
}

for a in adapters:
    aid = a.get('id')
    if aid in additional_specs:
        a.update(additional_specs[aid])

with open('content/catalog/adapters-bom.json', 'w', encoding='utf-8') as f:
    json.dump(adapters, f, ensure_ascii=False, indent=2)

print("Expanded adapters-bom.json with manufacturing, cost, and 3D printing specs!")
