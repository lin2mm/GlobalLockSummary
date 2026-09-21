with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **33** | 单图双标剥离与首屏视口防截断紧凑化全面实施 | 1. **单图双标彻底去噪**：首页 Entry 图片彻底剥离右上角“14款实物样本”浮标，将款数下沉规整至标题右侧中性胶囊 `[14款]`，图片仅留左上角单行 `★ 核心加装基准`，门锁实态 100% 还原干净通透；<br>2. **首屏防截断紧凑化（Anti-Viewport Cutoff）**：全面压缩 `adapters.html`、`install-gallery.html`、`field-issues.html` 的顶部空隙与图片高（190/220px ➔ 150/170px），描述文本施加 2 行 clamp，卡片总高严控在 360px 内，实现主流笔记本与桌面端打开即呈 100% 完整视图；<br>3. **日韩精工基准决策与落地**：正式确立日韩（JIS）为四大独立原发五金体系之一，纳入第一排 Core Tier 1 阵列，构建黄金 4×2 视觉注意力闭环。 | `build.mjs`, `content/pages/` |
""")

print("Appended batch 33 to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
