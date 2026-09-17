# GlobalLockSummary: 全局数据、资产与工程索引总览 (Master Data Index)

> **更新时间**：2026-09-17  
> **分支**：`arena/01a0a966-globallocksummary`  
> **Excel 离线全景索引文件**：[`docs/GLOBAL_LOCK_DATA_INDEX.xlsx`](./GLOBAL_LOCK_DATA_INDEX.xlsx)（含 6 个专业工作表，支持离线筛选与搜索）  
> **API 全量机读数据端点**：`/_site/data/catalog.json` 或本站 `/data/catalog.json`

---

## 一、全局数据资产与页面索引总览

| 模块大类 | 业务主题 / 数据分类 | 涵盖记录数 | 物理源数据文件 | 在线访问页面 (Web) | 本地实物/工程图路径 | 核心工程价值与用途 |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **1. 工业板块与图墙** | 5 大标准板块与实物图谱 | 38 类锁型 (已扩容) | `content/catalog/gallery.json` | [`/zh/index.html`](../zh/index.html) | `assets/img/gallery/*_real.*` | 按 ASSA ABLOY 分区与动态数量 (38: 北美6/澳英10/欧洲8/东南亚10/拉美4) 展现真实门锁图墙 |
| **1. 工业板块与图墙** | 3 大强相关 Retrofit 基准锁 | 3 款基准 | `build.mjs` | [`/zh/index.html`](../zh/index.html) 展板 | `assets/img/hero/hero-*.jpg` | 北美 ANSI Deadbolt、欧标双锁芯、澳式 001 顶级大主图与死穴直达 |
| **2. 本土辨锁大百科** | 5 国本土语言量测与术语 | 5 大国别体系 | `content/catalog/indigenous-lock-guides.json` | [`/zh/indigenous-guides.html`](../zh/indigenous-guides.html) | `assets/img/indigenous/*.png\|jpg` | 德 (Dornmaß/PZ/Gefahrenfunktion)、法 (Axe 50/Entraxe 70)、日、英、西 |
| **3. 专项研发工具** | 日本主流门锁面板刻印速查字典 | 5 大族 (28+刻印) | `content/catalog/japan-engraving-matrix.json` | [`/zh/japan-engravings.html`](../zh/japan-engravings.html) | `assets/img/indigenous/jp-*.jpg` | 刻印即型号！输入 MIWA 13LA、GOAL LX 秒级调取 CAD 切欠图与专用夹具 |
| **3. 专项研发工具** | 全球智能锁 Retrofit 转接件 BOM | 4 款核心套管 | `content/catalog/adapters-bom.json` | [`/zh/adapters.html`](../zh/adapters.html) | `assets/img/tools/adapter-7to8mm.png` | 法国 7转8mm 铜套、德标 8转9mm 逃生套、美标十字尾轴盘、日本 B5 捏合爪 |
| **3. 专项研发工具** | 海外主流防盗锁 1:1 开孔打样模板 | 3 套原厂规范 | `content/catalog/drilling-templates.json` | [`/zh/drilling-templates.html`](../zh/drilling-templates.html) | `assets/img/tools/template-*.png` | 北美 54mm 大圆孔、JIS 42mm 对穿孔、DIN 72/92mm PZ 官方开孔打印参数 |
| **4. 改装排雷与电商** | 全球智能锁改装一线避坑实录 | 4 大故障源 | `content/catalog/field-issues.json` | [`/zh/field-issues.html`](../zh/field-issues.html) | `assets/img/tools/gap-clearance.jpg` | Reddit/工单差评：抬把手过载、门缝卡阻、双锁芯反锁、胶贴脱落真实案例 |
| **4. 改装排雷与电商** | 跨境电商爆款机械锁兼容排行榜 | 4 国顶流爆款 | `content/catalog/bestseller-locks.json` | [`/zh/bestseller-matrix.html`](../zh/bestseller-matrix.html) | `assets/img/tools/bestseller-deadbolt.jpg` | 美亚 Kwikset、德亚 ABUS、乐天 MIWA、英亚 Yale 畅销机械锁改装适配榜 |
| **5. 核心机读数据** | 全站全量机读数据集 API | 全站数据集合 | `_site/data/catalog.json` | `/data/catalog.json` | 全站统一资源引用 | 企业 ERP/MES 系统、移动端 App、出海选型工具直接一键 GET 拉取调用 |
| **5. 核心机读数据** | 站内全文检索实时倒排索引 | 118 个页面索引 | `_site/data/search-index.json` | [`/search.html`](../search.html) | 站内全局搜索 | 全站分词索引，支持任意型号、术语、公差毫秒级搜索联想 |

---

## 二、专项数据子索引速查

### 1. 🇯🇵 日本面板刻印反查速查索引 (MIWA / GOAL / SHOWA)
- **数据源**：`content/catalog/japan-engraving-matrix.json`
- **在线页面**：[`/zh/japan-engravings.html`](../zh/japan-engravings.html)
- **索引摘要**：
  - `MIWA LA / 13LA / LA・MA`：插芯呆舌把手锁，BS 51/64mm，门厚 33-42mm，改装极易，配 SwitchBot C 夹爪或 Qrio；
  - `MIWA BH / DZ / LD / LDSP`：独立呆锁，BS 31/51/64mm，门厚 33-42mm，改装易；
  - `MIWA LSP / LE / SWLSP / TE`：轻型插芯锁，BS 51/64mm，门厚 28-40mm，配 B5 防盗旋钮夹头；
  - `GOAL LX / AS・LX / LG`：高安全把手插芯锁，BS 38/51/64mm，门厚 33-43mm，适配 Aqara U200 / SwitchBot G 夹爪；
  - `SHOWA CL / 516 / 397`：公团老式逃生锁，BS 50/60mm，需长行程自学习电机。

### 2. 🧩 转接件 BOM 清单与公差索引 (Adapters BOM)
- **数据源**：`content/catalog/adapters-bom.json`
- **在线页面**：[`/zh/adapters.html`](../zh/adapters.html)
- **索引摘要**：
  - `ADP-01`：**法国 7mm 转 8mm 变径方轴套管**，材质 H62 黄铜/淬火碳钢，外径 $8.00_{-0.05}^{0}\text{ mm}$，内孔 $7.05_{0}^{+0.05}\text{ mm}$；
  - `ADP-02`：**德规 8mm 转 9mm 逃生方轴套管**，材质 SUS304 不锈钢，外径 $9.00_{-0.05}^{0}\text{ mm}$，内方 $8.05_{0}^{+0.05}\text{ mm}$；
  - `ADP-03`：**日本 MIWA B5 防盗捏合旋钮驱动爪**，材质 POM/PA12，双侧下压斜坡行程 2.5mm，支持 3D 打印打样；
  - `ADP-04`：**北美 ANSI Deadbolt 十字/扁条万向适配盘**，6061-T6 铝合金 CNC，双层台阶开槽（2.2mm / 4.5mm）。

### 3. 📐 官方 1:1 开孔打样工程模板索引 (Drilling Templates)
- **数据源**：`content/catalog/drilling-templates.json`
- **在线页面**：[`/zh/drilling-templates.html`](../zh/drilling-templates.html)
- **索引摘要**：
  - `TPL-01`：**北美 ANSI A156.36 呆锁**，大圆孔 $\Phi 54\text{ mm}$，侧舌孔 $\Phi 25.4\text{ mm}$，孔深 76mm，背距 60/70mm 可调；
  - `TPL-02`：**日本 JIS MIWA 13LA 切欠**，面板 $130\times 25\text{ mm}$，对穿固定孔中心垂直间距固定为 $42\text{ mm} (\pm 0.5\text{ mm})$；
  - `TPL-03`：**欧标 DIN 18251 锁体与双锁芯**，中心距 PZ 72mm（室内）/ 92mm（外门），方轴孔 8/9mm。

### 4. 🛒 跨境爆款机械锁改装兼容索引 (Bestsellers)
- **数据源**：`content/catalog/bestseller-locks.json`
- **在线页面**：[`/zh/bestseller-matrix.html`](../zh/bestseller-matrix.html)
- **索引摘要**：
  - `BEST-01`：**Kwikset 660 / 92580 (Amazon US #1)**，适配率 98%，死穴为门扇下沉扣板错位卡阻；
  - `BEST-02`：**ABUS EC550 / D6X (Amazon DE #1)**，适配率 100%，具备双向应急离合 (Gefahrenfunktion)；
  - `BEST-03`：**MIWA 13LA / LA (日本乐天 #1)**，适配率 99%，日本公寓普及率 >60%；
  - `BEST-04`：**Yale PBS1 BS 3621 (Amazon UK #1)**，适配率 85%，死穴为内侧常闭 snib 拨钮误锁卡死。

---

## 三、如何随时查看与使用该索引？

1. **直接查看 Markdown 索引**：随时打开本文件 `docs/GLOBAL_LOCK_DATA_INDEX.md`；
2. **下载或在 Office/WPS 中打开 Excel**：打开 `docs/GLOBAL_LOCK_DATA_INDEX.xlsx`，内含 6 个已按颜色排版、带列宽自适应的专业工作表；
3. **调用全量 API 数据**：访问本地或线上 `_site/data/catalog.json`，直接提取任意字段。
