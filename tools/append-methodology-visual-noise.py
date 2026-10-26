with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'r', encoding='utf-8') as f:
    methodology = f.read()

noise_chapter = """
---

## 九、 视觉噪音消除、注意力机制与极简工程美学（Visual Noise & Minimalist Engineering）

针对硬件工程师与 B2B 决策者，深入研究 **Nielsen Norman Group (NN/g) 认知负荷理论 (Cognitive Load Theory)**、**Steve Krug《点石成金》(Don't Make Me Think)** 与 **ASSA ABLOY 工业设计哲学**，提炼出全站视觉降噪与美观度的三大底层法则：

### 1. 认知负荷与视觉噪音的本质（The Anatomy of Visual Noise）
* **外在认知负荷（Extraneous Cognitive Load）**：
  - 凡是**不能直接帮助工程师做判断的元素，全都是视觉噪音**。
  - *典型噪音*：浮夸的渐变蓝背景、大面积弥散阴影、冗长重复的大段说明文字、过多的辅助说明标签、繁琐的多步表单。
* **内在负荷管理（Intrinsic Load Management）**：
  - 硬件公差（如背距 55mm、方轴 8mm）是用户本身必须理解的复杂度（内在负荷）。界面设计的首要目标，是通过**「图示化（Visual Schema）」**替代“文字描述”，降低理解门槛。
* **生成负荷支持（Germane Load）**：
  - 优秀的设计用**「实拍场景图 + 1:1 剖面图 + 极简单色微标签」**形成即时空间心智映射，让工程师的大脑把带宽集中在“结构是否干涉”上。

### 2. 能用图就绝不用文字的四大落地原则（Images over Words）
1. **场景胜过万语（Scene Replaces Prose）**：一张清晰的门扇外立面实拍照，比 300 字解释“什么是外装夜锁”或“什么是中东装甲门”更加直观；
2. **尺寸落盘于图谱标尺（Annotated Diagrams）**：将背距（Backset）、中心距（PZ）等关键尺寸直接标注在 SVG 矢量剖面图上，正文中严禁重复描述长篇累赘数字；
3. **状态胶囊化（Capsule Tokens）**：将复杂的文字判断缩减为 2~4 个字的紧凑标签（如 `★ 核心基准`、`⚠️ 需双离合`、`≤30mm 薄门`）；
4. **渐进式沉底（Progressive Footer）**：次要操作（如反馈留资、版权声明）必须彻底单行化、低对比化，绝不向上争抢首屏注意力。
"""

if "视觉噪音消除、注意力机制与极简工程美学" not in methodology:
    methodology += "\n" + noise_chapter
    with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'w', encoding='utf-8') as f:
        f.write(methodology)
    print("Added visual noise & cognitive load chapter to docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md")

