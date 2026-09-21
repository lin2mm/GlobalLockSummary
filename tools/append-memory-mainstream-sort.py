with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **27** | 单一分类页内锁型排序依据定论 | **主流基准（Mainstream）绝对优先排在最前**，紧随其后为小众/特殊衍生锁；在同一层级内，严格按 **`selectionScore.overallScore`（出海大盘占有率与加装相关度得分）降序排列**，彻底消灭无序插花乱序。 | `build.mjs` |
""")

with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'a', encoding='utf-8') as f:
    f.write("""
---

## 十、 单一分类页面内锁型的排序依据（Intra-Category Sorting Algorithm）

在任何一个具体的工业板块二级页面内，锁型卡片的排布绝非随机，而是严格遵循 **「商业与工程双权重降序排序律」**：

1. **第一排序键：分级权重（Tier Priority）**
   - **★ 主流基准锁（Mainstream Standards，权重值 1）**：必须 100% 聚合置于该页面的前半段；
   - **🔍 小众/长尾特殊锁（Niche / Specialty Models，权重值 0）**：统一排在后半段。绝不允许主流与非主流在卡片网格中无序混杂。
2. **第二排序键：综合出海打分（Selection Score Decrescendo）**
   - 在相同分级内，根据 `selectionScore.overallScore`（98分 $\to$ 93分 $\to$ 86分）从大到小严格递减；
   - 该分数综合权衡了：**当地门锁市场保有率（≥30%）**、**免工具加装亲和度（Grade A/B）**、**现场实态照片清晰度** 与 **工程师点击权重**。
""")

print("Appended batch 27 to memory and methodology!")
