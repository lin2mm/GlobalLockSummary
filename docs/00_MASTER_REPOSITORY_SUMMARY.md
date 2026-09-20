# GlobalLockSummary 仓库全景资料总索引与工程资产摘要 (Repository Master Summary)

> **文档定位**: 本文档是对 `lin2mm/GlobalLockSummary` 整个 GitHub 仓库所有核心工程资料、数据底座、视觉图资、设计方法论与工具链的一站式全景索引（Master Summary）。  
> **分支基准**: `arena/01a0a966-globallocksummary`  
> **物理位置**: `/docs/00_MASTER_REPOSITORY_SUMMARY.md`  
> **更新时间**: 2026-09-20

---

## 一、 顶层定位与核心资产全景概览

GlobalLockSummary 是一座面向出海智能硬件产品经理、机械结构工程师、锁匠与海外买家的**全球机械门锁与后装智能锁（免换锁 / 租客无损加装）开放工程知识库**。整个仓库由 **六大核心资料体系** 构成：

```text
GlobalLockSummary 核心资料大图
├── 1. 结构化五金工程数据底座 (JSON Core Databases)
├── 2. 严苛工业标准与开孔打样图谱 (Standards & 1:1 Blueprints)
├── 3. 100% 实物核实的转接件 BOM 清单 (Verified Hardware Adapters)
├── 4. 海外一线安装工单与避坑实录库 (Jobsite Cases & Failure Gallery)
├── 5. 欧美日后装智能锁专利规避与 FTO 指南 (Patent Claims & Design-Around)
└── 6. 长期工程方法论与质量守护防线 (Methodology, Memory & Tests)
```

---

## 二、 六大核心资料体系与直达索引

### 🗄️ 1. 结构化五金工程数据底座 (Content Catalog & Databases)
存放路径：`content/catalog/`
- **`gallery.json` (全球 74 款实物机械锁全息数据)**：
  - 覆盖北美 (ANSI)、欧陆五国 (DIN)、英澳 (Lockwood)、日韩 (MIWA/GOAL)、东南亚 (HDB)、拉美 (ABNT)、中东 (GCC)、南亚非洲 8 大工业板块；
  - 深度集成：原厂锁芯外露量与剪切线公差、电机反向自锁力矩、垂直下沉耐受度、大都市存量高频分布、租客退租无损复原评级。
- **`lock-families/*.json` (15 大标准机械锁族独立数据卡片)**：
  - 涵盖 `us-deadbolt.json` (美标呆锁)、`euro-cylinder-mortise.json` (欧标槽型插芯锁)、`au-deadlatch.json` (澳洲辅舌死锁)、`jp-miwa-case.json` (日本 MIWA LA)、`sg-metal-gate-lock.json` (新加坡铁闸门锁) 等；
  - 包含每个锁族的结构组成 (Anatomy)、测量顺序与公差带 (Measurements)、匹配改造架构与常见 FAQ。
- **`smart-locks.json` & `retrofit-architectures.json`**：
  - 涵盖 7 大智能化改造架构（如常插钥匙转动、尾轴转接盘联动、通用模块化锁芯换装）；
  - 收集 Nuki Smart Lock Ultra / 4.0 Pro、August Smart Lock、SwitchBot Lock Ultra 等主流设备的尺寸约束与适用范围。

### 📐 2. 严苛工业标准与 1:1 开孔打样蓝图库 (Standards & Blueprints)
存放路径：`content/catalog/standards.json`, `assets/img/diagrams/`, `drilling-templates.md`
- **17 大全球门锁标准专著**：
  - 涵盖德国 `DIN 18251` / `DIN 18252` (应急离合认证)、欧洲 `EN 12209` / `EN 1303`、北美 `ANSI/BHMA A156.2` / `A156.36`、日本 `JIS A 5511`、澳洲 `AS 4145` 等；
  - 详细定义了标准决定的核心参数（背距 Backset、中心距 CTC、方轴孔径 Spindle Hole、门缝剪切间隙）。
- **30+ 份 1:1 官方开孔打样蓝图 (SVG 矢量)**：
  - 位于 `assets/img/diagrams/`，包含 `US-27` ~ `US-30`、`EU-19` ~ `EU-26`、`AU-11` ~ `AU-18`、`SG-01` ~ `SG-10` 锁体的精密传动与开孔图。

### 🔩 3. 100% 实物核实的转接件 BOM 清单 (Hardware Adapters BOM)
存放路径：`content/catalog/adapters-bom.json`, `content/pages/zh/adapters.md`
- 经过实物图纸对照与力矩剪切核实的 12 款改装标杆五金：
  - **`ADP-04`**：北美 ANSI Deadbolt 十字/扁条万向阶梯适配盘（出海千万级爆款）；
  - **`ADP-06`**：欧标双向锁芯钥匙柄薄形夹爪与 Oldham 浮动拨叉；
  - **`ADP-03`**：日本 MIWA B5 防盗捏合旋钮双侧斜坡抓手（数百万级高难锁具）；
  - **`ADP-07`**：门框防盗扣板二次下沉加厚垫片（吸收下沉错位）；
  - **`ADP-05`**：澳洲 Lockwood 001 执手内退偏心适配垫盘；
  - **`ADP-01` ~ `ADP-02`**：法国 7 转 8mm、德国 8 转 9mm 方轴开槽变径套管；
- 每款工具均标明：**推荐制造材质、关键加工公差、力矩门槛、采购批量预估成本、对应实装锁族**。

### 🔨 4. 海外一线安装工单与避坑实录库 (Jobsite & Failure Gallery)
存放路径：`content/catalog/installation-cases.json`, `content/catalog/field-issues.json`
- **41 个现场施工工况图库 (`install-gallery.html`)**：
  - 涵盖北美 ANSI 呆孔钻孔夹具实操、欧标开槽、澳洲夜闩工单、新加坡组屋双门间隙等现场高清实拍；
- **6 大一线致命避坑工单 (`field-issues.html`)**：
  - `FL-01 (致命卡阻)`：北美插销与门框扣板沉孔错位摩擦；
  - `FL-02 (反锁困人)`：欧标双锁芯无应急离合导致的彻底反锁绝境；
  - `FL-03 (机械碰撞)`：新加坡组屋铁闸门与木门把手极端碰撞 (<80mm)；
  - `FL-04 (假锁死)`：澳式 Lockwood 001 辅助舌悬空导致卡片即开；
  - `FL-05 (门皮塌陷)`：拉美 30mm 中空薄门拧紧螺栓导致门皮塌陷；
  - `FL-06 (热胀卡死)`：中东海湾地区极端烈日暴晒导致金属门热膨胀卡死。

### ⚖️ 5. 后装智能锁专利规避与 FTO 指南 (Patent FTO Guide)
存放路径：`content/pages/zh/patent-avoidance.md`, `content/pages/en/patent-avoidance.md`
- 拆解欧美日主流后装智能锁核心专利，为出海企业提供规避路径：
  - **01 / 锁芯夹持**：避开 Nuki 3 颗平头螺钉点压锁芯专利（改用 360° 弹性夹头套圈或面板对穿螺栓）；
  - **02 / 钥匙浮动抓取**：避开自定心夹爪权利要求（改用 Oldham 十字滑块浮动联轴器传递纯扭矩）；
  - **03 / 手动优先离合**：避开微型舵机推拉齿轮轴向位移专利（改用单向滚柱超越离合器或 ≤1:15 低反驱 BLDC）；
  - **04 / 机身固定卡爪**：避开 August 侧向翻折双翼卡扣专利（改用单反镜头 45° 旋转卡口环）；
  - **05 / 出海 FTO 自查清单**：工业五金出海 5 步核验表格。

### 📚 6. 长期工程方法论与质量守护防线 (Docs & Tests)
存放路径：`docs/`, `tests/`
- **`docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md` (核心记忆库)**：
  - 沉淀 **50 条经过严苛实证的工程铁律**（涵盖 ASSA ABLOY Deep Blue 视觉色彩律、双语双行排版、超长页面聚类微导栏、公私资产物理隔离、Cloudflare Pages 分支映射防御机制）；
- **`docs/00_INDEX_TREE.md`**：全仓库物理文件架构树；
- **`docs/*.xlsx` (多维度工程 Excel 索引)**：
  - `02_PROJECT_PLAN_AND_CONVENTIONS.xlsx`：项目甘特图与 WBS 分工；
  - `03_GLOBAL_LOCK_DATA_INDEX.xlsx`：全球 6 大工作表综合数据总库；
  - `07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx`：色彩分层与 70 款锁型归属表；
  - `08_HARDWARE_ADAPTERS_AND_BOM.xlsx`：转接件详细图纸 BOM 清单；
  - `09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx`：全站 102 张图片 5 级全息扫描健康报表；
- **`tests/` (自动化持续集成质量防线)**：
  - 5 大自动化测试套件（229 个 HTML 死链与锚点探测、决策树 21,952 种组合判定、导航栏动态计数、H1 唯一性、无占位符泄漏），保障代码迭代永不劣化。

---

## 三、 核心资料物理位置速查表

| 核心资料类别 | 存储路径 / 入口文件 | 语言支持 | 典型内容与作用 |
| :--- | :--- | :--- | :--- |
| **全库文件架构树** | `docs/00_INDEX_TREE.md` | 中文/英 | 仓库与 Workspace 物理文件架构一览 |
| **50 条工程方法论与记忆** | `docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md` | 中文 | 用户铁律、视觉工规排版与根因防御库 |
| **全球 74 款锁型数据库** | `content/catalog/gallery.json` | 双语 | 机械锁核心参数、公差带、大都市分布 |
| **15 大机械锁族详尽卡片** | `content/catalog/lock-families/` | 双语 | 美标呆锁、欧标DIN、澳标、日韩MIWA等 |
| **12 款转接五金 BOM** | `content/catalog/adapters-bom.json` | 双语 | 万向轴、变径套、抓手材料及公差 |
| **6 大避坑实录与工单** | `content/catalog/field-issues.json` | 双语 | 现场安装错位、反锁卡死实操解析 |
| **41 篇一线施工案例** | `content/catalog/installation-cases.json` | 双语 | 开孔夹具、门框调整施工图集 |
| **全球锁具安规标准索引** | `content/catalog/standards.json` | 双语 | DIN 18251、ANSI、EN 1303 等标准详解 |
| **专利壁垒与规避指南** | `content/pages/{zh,en}/patent-avoidance.md`| 双语 | Nuki/August 等专利权利要求与规避设计 |
| **综合数据与 BOM 表格** | `docs/*.xlsx` | 中文 | 6工作表五金数据表、BOM图纸、图片审计表 |
| **自动化测试套件** | `tests/*.mjs` | Node.js | 覆盖死链、H1、占位符与导航计数的 5 大套件 |
