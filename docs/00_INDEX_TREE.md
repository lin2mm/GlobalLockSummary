# GlobalLockSummary 全局索引脉络与架构树 (Index Tree)

> **文档定位**: 本文档为 `lin2mm/GlobalLockSummary` 仓库与工作区（Workspace）的全景架构索引指南，便于研发工程师、产品经理与架构师一眼穿透全局数据流、构建流水线与内部工程资产。  
> **更新时间**: 2026-09-20  
> **分支基准**: `arena/01a0a966-globallocksummary`

---

## 🌲 全局架构索引树 (Architectural Index Tree)

```text
GlobalLockSummary (Repository Root)
│
├── ⚙️ [01] 静态站点编译与开发内核 (Engine & Build)
│   ├── build.mjs                 # 全站编译主脚本 (读取 JSON/MD 数据，输出 228+ HTML 页面)
│   ├── serve.mjs                 # 本地预览轻量 HTTP 服务
│   ├── package.json              # 项目依赖与 npm test 命令定义
│   └── src/                      # 核心编译渲染管道
│       ├── layout.mjs            # 全局 HTML 骨架、导航生成、SEO/Schema、TOC 目录渲染
│       └── markdown.mjs          # Markdown 解析器、双语双行标题解耦引擎 (formatBilingualHeading)
│
├── 🗄️ [02] 核心五金数据库与图谱源 (Content Catalog & Data)
│   └── content/catalog/
│       ├── gallery.json          # 70+ 款全球实物锁型全息数据 (含公差矩阵、减速比、剪切线、大都市分布)
│       ├── adapters-bom.json     # 12 款 100% 实物核实的全球加装标准转接五金 BOM 清单
│       ├── field-issues.json     # 6 大一线避坑实录与机械故障工单数据
│       ├── installation-cases.json # 41 个现场施工工况与开孔实录数据
│       ├── standards.json        # 全球五金安规标准索引 (DIN 18251, ANSI/BHMA, EN 1303 等)
│       ├── smart-locks.json      # 业界代表性后装设备库 (Nuki, August, SwitchBot 等)
│       ├── retrofit-architectures.json # 7 大无损加装/替换工程架构定义
│       └── lock-families/*.json  # 15 大标准机械锁族独立数据卡片 (美标呆锁, 欧标DIN, 澳式001, 日本MIWA等)
│
├── 📖 [03] 内容页面与专题指引 (Public Content Pages)
│   └── content/pages/ (双语平行：zh/ 中文, en/ 英文)
│       ├── index.md              # 首页入口 (8 大工业板块 4×2 黄金阵列)
│       ├── patent-avoidance.md   # 后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)
│       ├── adapters.md           # 标准转接工具与五金配件库 (Hardware Adapters BOM)
│       ├── field-issues.md       # 避坑实录与故障工单 (Field Failure Gallery)
│       ├── indigenous-guides.md  # 全球机械门锁工业索引与本土辨锁指南
│       ├── drilling-templates.md # 主流防盗锁 1:1 官方开孔打样模板图谱
│       ├── bestseller-matrix.md  # 海外电商爆款防盗机械锁兼容性排行榜
│       ├── japan-engravings.md   # 日本主流门锁面板刻印速查字典 (フロント刻印)
│       ├── visitor-overview.md   # 买家/工程人员整体决策指南
│       └── data-hub.md           # 全球机械门锁数据与开放 API 中心
│
├── 🖼️ [04] 物理高清工程图资 (Visual Assets & Diagrams)
│   └── assets/
│       ├── css/site.css          # ASSA ABLOY 墨黑极简工业样式表、双语双行排版与 3 列等高卡片流
│       └── img/
│           ├── hero/             # 8 大工业板块门扇工况实装大图 (日韩MIWA, 欧标DIN, 北美ANSI等)
│           ├── gallery/          # 37+ 张全球主流锁具现场实拍高清图
│           ├── diagrams/         # 30+ 份 1:1 官方开孔与剖面打样蓝图 SVG
│           ├── pitfalls/         # 8 个一线致命卡阻、反锁、热膨胀现场故障照片
│           ├── tools/            # 12 款转接轴套、卡爪与垫片 BOM 实拍图
│           ├── indigenous/       # 德奥瑞、法比、日韩本土五金机械构造分解图
│           └── patent/           # 专利权利要求与 Oldham 浮动拨叉规避对比工程图
│
├── 🛡️ [05] 自动化质量防线与测试套件 (Test Suites)
│   └── tests/
│       ├── site.test.mjs         # 229 个 HTML 页面全链路死链、锚点探测与存在性断言
│       ├── scoring.test.mjs      # 21,952 组选型算法决策树可达性断言
│       ├── dynamic-nav-counter.test.mjs # 导航栏动态数量与底层 JSON 100% 同步断言
│       ├── no-duplicate-h1.test.mjs     # 全网杜绝重复 H1 标题断言
│       └── no-unrendered-placeholders.test.mjs # 零未解析 Mustache 占位符泄漏断言
│
└── 🔒 [06] 内部沉淀、方法论记忆与工程蓝图 (Strict Internal Docs)
    └── docs/ (严格物理隔离，仅留在 GitHub 分支内部，不向外网构建暴露)
        ├── 00_INDEX_TREE.md                     # 本全局索引脉络树文档 (快捷直达)
        ├── 01_METHODOLOGY_AND_CONTEXT_MEMORY.md # 长期上下文记忆库 (沉淀 50 条铁律与工程规范)
        ├── 00_AUTONOMOUS_OPTIMIZATION_LOOP.md   # 调度自进化动态执行日志
        ├── 02_PROJECT_PLAN_AND_CONVENTIONS.xlsx # 里程碑执行甘特图与 WBS 分工表
        ├── 03_GLOBAL_LOCK_DATA_INDEX.xlsx       # 全局机械锁与加装 6 工作表综合数据索引
        ├── 07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx # 色块分层设计系统与 70 款锁型归属表
        ├── 08_HARDWARE_ADAPTERS_AND_BOM.xlsx    # 8 款转接五金 BOM 精确图纸清单
        └── 09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx    # 全站图片资产 5 级全息扫描健康审计表
```

---

## 💡 核心运行逻辑三步提炼

1. **数据驱动（Content Catalog）**：所有页面上的锁型、款数、工具、避坑案例均存储在 `content/catalog/` 的标准 JSON 中，杜绝写死页面常量；
2. **极简编译（Build Pipeline）**：运行 `node build.mjs`，仅需不到 1 秒即可将 Markdown 和 JSON 渲染为 `_site/` 目录下 228 个极速纯静态 HTML 页面（涵盖中英双语）；
3. **闭环质检（Automated Test Suite）**：每次提交前运行 `npm test`，5 大严苛测试套件穿透扫描 229 个页面，确保 **0 死链、0 重复标题、0 占位符、100% 导航动态计数**，全自动推送到 GitHub Pages 和 Cloudflare Pages。
