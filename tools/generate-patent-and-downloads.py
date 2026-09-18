import json

# 1. 扩充 data-hub.md 页面：增加显式一键下载资产中心
zh_downloads = """
## 📦 长期沉淀工程资产与方法论直接下载 (Direct Download Hub)

以下文件已编译挂载至静态资源服务器，**点击即可通过浏览器直接下载原始文件**，无需任何命令行操作：

| 规范文件名 | 资产类型 | 说明 | 快速直接下载链接 |
| :--- | :--- | :--- | :--- |
| **`10_SMART_LOCK_RETROFIT_METHODOLOGY.md`** | 顶层方法论 | 出海加装全生命周期建站与工程选型范本 | [📥 点击直接下载 (Markdown)](/assets/downloads/10_SMART_LOCK_RETROFIT_METHODOLOGY.md) |
| **`01_METHODOLOGY_AND_CONTEXT_MEMORY.md`** | 长期核心记忆 | 包含全部用户历史指示、红线规矩与长效沉淀记录 | [📥 点击直接下载 (Markdown)](/assets/downloads/01_METHODOLOGY_AND_CONTEXT_MEMORY.md) |
| **`00_AUTONOMOUS_OPTIMIZATION_LOOP.md`** | 动态守护日志 | 双引擎协同闭环调度与健康审计日志 | [📥 点击直接下载 (Markdown)](/assets/downloads/00_AUTONOMOUS_OPTIMIZATION_LOOP.md) |
| **`02_PROJECT_PLAN_AND_CONVENTIONS.xlsx`** | 工程甘特图 | 包含带序号文件命名规范与 WBS 阶段里程碑 | [📥 点击直接下载 (Excel)](/assets/downloads/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx) |
| **`03_GLOBAL_LOCK_DATA_INDEX.xlsx`** | 全量公差主索引 | 74 款海外主流防盗锁工程公差全息表 | [📥 点击直接下载 (Excel)](/assets/downloads/03_GLOBAL_LOCK_DATA_INDEX.xlsx) |
| **`07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx`** | 视觉规范表 | 8 大工业板块配色与光学对比度模型 | [📥 点击直接下载 (Excel)](/assets/downloads/07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx) |
| **`08_HARDWARE_ADAPTERS_AND_BOM.xlsx`** | 改装转接 BOM | 12 款 100% 实物核实的加装五金套件 | [📥 点击直接下载 (Excel)](/assets/downloads/08_HARDWARE_ADAPTERS_AND_BOM.xlsx) |
| **`09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx`** | 图像资产审计 | 全站 5 级全息穿透与 102 张真实图片清单 | [📥 点击直接下载 (Excel)](/assets/downloads/09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx) |
"""

with open('content/pages/zh/data-hub.md', 'r', encoding='utf-8') as f:
    zh_dh = f.read()

if 'Direct Download Hub' not in zh_dh:
    zh_dh = zh_dh.replace('# 全球机械门锁工程数据中心与 B2B 资产枢纽', '# 全球机械门锁工程数据中心与 B2B 资产枢纽\n' + zh_downloads)
    with open('content/pages/zh/data-hub.md', 'w', encoding='utf-8') as f:
        f.write(zh_dh)
    print("Added downloads to zh/data-hub.md")

en_downloads = """
## 📦 Direct Engineering Assets & Methodology Download Hub

The following files are hosted on the public static asset server. **Click any link below to immediately download the raw file**:

| Filename | Asset Type | Description | One-Click Download |
| :--- | :--- | :--- | :--- |
| **`10_SMART_LOCK_RETROFIT_METHODOLOGY.md`** | Methodology | Comprehensive Overseas Smart Lock Retrofit Playbook | [📥 Download (Markdown)](/assets/downloads/10_SMART_LOCK_RETROFIT_METHODOLOGY.md) |
| **`01_METHODOLOGY_AND_CONTEXT_MEMORY.md`** | Core Memory | Standing Instructions, Context Rules & Full History | [📥 Download (Markdown)](/assets/downloads/01_METHODOLOGY_AND_CONTEXT_MEMORY.md) |
| **`00_AUTONOMOUS_OPTIMIZATION_LOOP.md`** | Daemon Log | Autonomous Dual-Loop Execution & Health Audit Log | [📥 Download (Markdown)](/assets/downloads/00_AUTONOMOUS_OPTIMIZATION_LOOP.md) |
| **`02_PROJECT_PLAN_AND_CONVENTIONS.xlsx`** | Gantt Chart | Numbered Conventions & WBS Project Milestones | [📥 Download (Excel)](/assets/downloads/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx) |
| **`03_GLOBAL_LOCK_DATA_INDEX.xlsx`** | Master Index | 74 Mechanical Lock Tolerance & Sizing Sheets | [📥 Download (Excel)](/assets/downloads/03_GLOBAL_LOCK_DATA_INDEX.xlsx) |
| **`07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx`** | Design System | 8 Industrial Division Colour Palette & Contrast | [📥 Download (Excel)](/assets/downloads/07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx) |
| **`08_HARDWARE_ADAPTERS_AND_BOM.xlsx`** | Retrofit BOM | 12 Verified Retrofit Adapters & Mechanical Kits | [📥 Download (Excel)](/assets/downloads/08_HARDWARE_ADAPTERS_AND_BOM.xlsx) |
| **`09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx`** | Image Audit | 5-Tier Asset Audit & 102 Physical Images Register | [📥 Download (Excel)](/assets/downloads/09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx) |
"""

with open('content/pages/en/data-hub.md', 'r', encoding='utf-8') as f:
    en_dh = f.read()

if 'Direct Engineering Assets & Methodology Download Hub' not in en_dh:
    en_dh = en_dh.replace('# Global Mechanical Lock Engineering Data & B2B API Hub', '# Global Mechanical Lock Engineering Data & B2B API Hub\n' + en_downloads)
    with open('content/pages/en/data-hub.md', 'w', encoding='utf-8') as f:
        f.write(en_dh)
    print("Added downloads to en/data-hub.md")

