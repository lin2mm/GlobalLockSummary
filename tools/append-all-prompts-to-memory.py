with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""

---

## 阶段七：用户历史指令与核心对话精要全量沉淀清单

| 批次 | 用户指示与指导核心 | 沉淀结果与系统响应 | 对应规范/测试文件 |
| :--- | :--- | :--- | :--- |
| **01** | 全站 5 大板块架构确立，建立 10 分钟自主优化常驻循环 | 建立双引擎调度器与常驻轮询守护进程 | `tools/runner-10m.py`, `docs/00_AUTONOMOUS_OPTIMIZATION_LOOP.md` |
| **02** | 明确 3 层 Gallery 结构（场景图、剖面图、安装图） | 建立 74 款锁型 3 层视觉穿透索引 | `docs/05_HIERARCHICAL_GALLERY_INDEX.md` |
| **03** | 首页仅保留区域 Entry 大卡片，其他类别不可混入 | 首页重构为纯粹 Entry 视觉总控门户 | `content/pages/zh/index.md`, `src/layout.mjs` |
| **04** | 南美锁（ABNT 40mm 极窄、薄门、防风滚轮）与北美锁物理隔离，扩充至 8 大工业板块 | 确立 4x2 黄金对称阵列（北美、拉美、欧陆、英澳、中东、日韩、东南亚、非南亚） | `assets/css/site.css`, `build.mjs` |
| **05** | 菜单 Menu 后的统计数字必须随内部内容增加而完全动态联动 | 移除 build.mjs 全部静态回退常量，实现穿透 JSON 实时计算，挂载防回归测试 | `tests/dynamic-nav-counter.test.mjs` |
| **06** | 离线工程数据与 B2B API 权限分层设计 | 设立数据中心 Lead Capture 下载机制，保护敏感公差数据 | `content/pages/zh/data-hub.md` |
| **07** | 纠正二级分类页返回按钮残留文字从 5 大板块更新为 8 大板块 | 彻底修复 build.mjs 模版文案与全站同步 | `build.mjs` (L1417) |
| **08** | 修复左上角标题文字重复（H1 重复） | 重构 markdownPage 生成逻辑，并新增全站 226 页面零重复 H1 强校验门禁 | `tests/no-duplicate-h1.test.mjs` |
| **09** | 明确工业索引排序依据，增加显式声明横幅 | 显式增加「出海加装复杂度与工程暗坑深度递减律」深色横幅 | `content/pages/zh/indigenous-guides.md` |
| **10** | 提炼全站全生命周期方法论，便于后续出海产品站点经验复用 | 沉淀完整出海智能锁 Retrofit 建站与工程实战方法论 | `docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md` |
""")

print("Appended all prompts log to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
