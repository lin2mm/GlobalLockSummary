#!/usr/bin/env python3
"""
tools/generate-hierarchy-index.py
自动生成 3 层工业级视觉图谱与内容索引体系文档 (05_HIERARCHICAL_GALLERY_INDEX.md)
"""

import json
from pathlib import Path

ROOT = Path("/home/user/GlobalLockSummary")
GALLERY_JSON = ROOT / "content" / "catalog" / "gallery.json"
OUT_MD = ROOT / "docs" / "05_HIERARCHICAL_GALLERY_INDEX.md"

def main():
    items = json.load(open(GALLERY_JSON, "r", encoding="utf-8"))

    md = []
    md.append("# 05_HIERARCHICAL_GALLERY_INDEX.md —— 全球五大板块 3 层视觉穿透与内容索引体系\n")
    md.append("> **规范体系**：按照工业五金标准、Retrofit 智能锁强相关性、高清门上实拍场景与产品剖面双图谱、以及原厂打孔打样安装工程构建。\n")
    md.append("## 一、5 大区域 Entry 主图筛选参数与权重标准 (Selection Criteria)\n")
    md.append("| 筛选维度 | 权重 | 判定指标 | 目标门槛 | 选用基准锁 |")
    md.append("|---|---|---|---|---|")
    md.append("| **1. 市场主流保有率** | 30% | 所在国独栋/公寓住宅五金存量占比 | ≥ 30% 存量 | US: Schlage B60 / EU: Euro Profile / ANZ: Lockwood 001 |")
    md.append("| **2. 改装强相关性** | 25% | 主流加装智能锁 (August/Nuki/SwitchBot/Linus) 原生兼容度 | R1/R2 认证 | 具备标准转接扁轴、葫芦锁芯或标准夹具 |")
    md.append("| **3. 门上场景图分辨率** | 25% | 真实木门/防盗门安装视角、光影、无模糊噪点 | ≥ 1080P/4K | 真实家居实拍而非纯白底渲染渲染假图 |")
    md.append("| **4. 工程师关注与点击率 (CTR)** | 20% | 行业工单报障频率、论坛检索量与避坑搜索热度 | 预测 CTR > 0.90 | 排查门下沉卡阻、双面锁芯应急离合等高频痛点 |\n")

    md.append("## 二、3 层视觉穿透架构定义 (3-Tier Hierarchical Structure)\n")
    md.append("- **第 1 层 (Division Level - 首页门户)**：5 大工业板块大幅实景卡片，仅展示各区域最核心的 1 款基准锁实拍大图，带动态样本数量及 `[1-5]` 快捷键盲切。")
    md.append("- **第 2 层 (Category & Product Gallery - 区域分类页)**：各区域下细分门锁类别的**【产品剖面/白底图】+【真实门上场景图】双图对照 Gallery 模式**，展示 R1/R2 等级及筛选参数。")
    md.append("- **第 3 层 (Installation & Retrofit Blueprint - 锁型详情页)**：各门锁类别下的**1:1 原厂开孔打孔打样图、关键公差、电机啮合转接件 BOM 及 4 步安装实操图谱**。\n")

    md.append("## 三、全量 38 款锁型 3 层视觉资产与安装索引明细\n")
    md.append("| 序号 ID | 锁型名称 | 板块代码 | 场景实景图 (Scene) | 产品图 (Product) | 1:1安装示意 (Blueprint) | 综合筛选分 |")
    md.append("|---|---|---|---|---|---|---|")

    for it in items:
        iid = it.get("id")
        title = (it.get("title", {}).get("zh") if isinstance(it.get("title"), dict) else it.get("title")) or iid
        block = it.get("block", "")
        scene = it.get("sceneImage", it.get("image", ""))
        product = it.get("productImage", scene)
        has_schematic = "✅ 矢量示意图" if (ROOT / f"assets/img/diagrams/{iid}_schematic.svg").exists() else "🖼️ 场景图替代"
        score = it.get("selectionScore", {}).get("overallScore", 85)
        md.append(f"| `{iid}` | {title} | `{block}` | `{scene}` | `{product}` | {has_schematic} | **{score} 分** |")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(f"Generated {OUT_MD}")

if __name__ == "__main__":
    main()
