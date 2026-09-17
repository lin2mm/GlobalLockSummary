# GlobalLockSummary: 工程方法论、业务认知与长期记忆体系

> **版本**：v1.0 (2026-09-17)  
> **维护分支**：`arena/01a0a966-globallocksummary`  
> **核心使命**：为中国及全球智能锁研发与改造工程师，建立公开、可机读、带真实公差与改装避坑指南的全球存量机械门锁知识库。

---

## 一、用户指导原则与长期铁律（不可违背）

1. **服务对象与数据流向原则**：
   - **服务对象**：国内一线智能锁硬件与改造工程师（他们缺乏海外存量锁的一手参数、暗坑和真实安装案例）；
   - **数据流向只进不出**：我们负责从**海外原生生态**（海外原厂型录、Reddit 锁匠与改装社区、海外电商差评、海外安装服务工单）主动爬取、逆向并清洗结构化数据；
   - **严禁向国内工程师索取海外数据**：国内工程师是数据的纯消费者，不是海外数据的供给方。
2. **分支与发布铁律**：
   - 严格在绑定分支 `arena/01a0a966-globallocksummary` 工作并 push；
   - **PR #3 保持 OPEN，绝不自动合并，绝不擅自关闭会话**；
   - 只有用户明确发出“现在合并”且二次确认后才可操作。
3. **视觉与用户体验原则**：
   - **图片导航优先**：首页首屏以高清实物安装主图为第一导航，拒绝贴片广告式的冗长堆砌文本；
   - **免登录站内闭环**：中国工程师无需科学上网、无需 GitHub 账号，通过 `/api/feedback` 一行提交需求，支持本地剪贴板复制兜底。

---

## 二、全球锁 5 大标准工业板块（ASSA ABLOY 事业部 + 五金标准体系）

| 板块代码 | 工业板块名称 | 核心标准与五金特征 | Retrofit 改造强相关基准锁（大主图） |
| :---: | :--- | :--- | :--- |
| **`na`** | **🇺🇸 北美标准板块 (Americas)** | `ANSI/BHMA A156.36 / A156.2`<br>54mm 标准大孔位、60/70mm 背距 | **北美单缸插销死锁 (ANSI Deadbolt / Schlage B60 / US-27)**<br>August/SwitchBot 基本盘，尾轴直接驱动 |
| **`europe5`** | **🇪🇺 欧陆五国板块 (Continental Europe)** | `DIN 18251 / 18252`、`EN 12209`<br>欧标槽型锁芯、72/92mm PZ、多点联动 | **欧标槽型双锁芯 (Euro Profile DIN 18252 / EU-19)**<br>Nuki/Linus 基本盘，死穴为必须具备 BS 双向应急离合 |
| **`uk-anz`** | **🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK)** | `AS 4174`（澳标）、`BS 3621`（英标）<br>表面安装夜锁、双扣死锁、5 拨杆防盗 | **澳式外装夜锁与双扣锁 (Lockwood 001/355 / AU-11)**<br>内侧大旋钮抓取，死穴为辅舌必须完全压入死锁 |
| **`sea`** | **🇸🇬 东南亚与东亚板块 (Asia-Pacific)** | `SS 312`、SCDF 逃生规范、KS 标<br>HDB 铁闸双门极端净距 (<80mm)、推拉锁 | **新加坡 HDB 铁闸与推拉锁 (SG-04/SG-07)**<br>薄型化要求极高，存在把手碰撞边界 |
| **`latam`** | **🌎 拉美新兴板块 (Latin America)** | `ABNT NBR 14913`（巴西）、ODIS<br>40/45mm 极窄背距、30mm 薄门扇 | **拉美 ABNT 窄背距插芯锁 (La Fonte / Silvana / LA-01)**<br>需严格限制电机旋转半径以防撞门框 |

---

## 三、文件与目录工程命名规范（File System Conventions）

为保证项目长期演进中文件结构井井有条、机器与人类均易于检索，确立以下命名规范：

```text
GlobalLockSummary/
├── content/
│   ├── catalog/                         # 机器可读核心数据库
│   │   ├── gallery.json                 # 32 类实物图墙与工程对齐主清单
│   │   ├── field-issues.json            # 全球真实改装故障与差评抓取数据库
│   │   ├── smart-lock-benchmarks.json   # Nuki/August/SwitchBot 等竞品实测对标表
│   │   └── lock-families/*.json         # 各锁族详细参数与尺寸定义
│   └── pages/{zh,en}/*.md               # 双语内容页面源文件
├── assets/
│   ├── img/
│   │   ├── gallery/                     # 真实门上实物安装照片
│   │   │   └── {region}_{model}_real.{ext}  (如 us-27_real.jpg, au-11_real.jpg)
│   │   ├── diagrams/                    # 传动与受力原理矢量图
│   │   │   └── {region}_{model}_schematic.svg
│   │   └── hero/                        # 5 大板块顶级入口超大展示主图
│   │       ├── hero-na-deadbolt.jpg
│   │       ├── hero-europe-eurocylinder.jpg
│   │       └── hero-anz-lockwood001.jpg
│   └── js/                              # 交互逻辑脚本 (feedback.js, gallery.js)
├── functions/api/                       # Cloudflare Pages Functions 服务端无服务接口
│   └── feedback.js                      # 站内免登录安全提交接口
├── tools/                               # 自动化抓取、校验与数据处理工具链
│   ├── fetch-field-issues.mjs           # 全球改装痛点自动化摄取脚本
│   └── validate-data.mjs                # 目录数据引用完整性校验
└── docs/                                # 长期方法论与架构文档体系
    └── METHODOLOGY_AND_CONTEXT_MEMORY.md
```

---

## 四、历史沟通与决策日志（Changelog & Memory Log）

- **2026-09-17 (Session Start)**: 核实长期分支 `arena/01a0a966-globallocksummary`，PR #3 保持 OPEN。
- **2026-09-17 (Raw Data Ingestion)**: 顺利从 GitHub 分支解压获取 30 类候选锁实物图与矢量原理图。
- **2026-09-17 (Landing Page Gallery)**: 首页改造为纯实物图墙，支持地区筛选与搜索。
- **2026-09-17 (In-Site Feedback)**: 实现 Cloudflare Pages Functions `/api/feedback` 免 GitHub 站内提交。
- **2026-09-17 (Taxonomy Upgrade)**: 对标 ASSA ABLOY 分区与 GTM 市场容量，重构为 5 大工业板块，确立三大核心强相关 Retrofit 锁型并挂载超大主图。
- **2026-09-17 (Field Issues Repository)**: 抓取 Reddit / 锁匠社区真实痛点，建立《全球智能锁改装避坑实录》。

---

## 五、每次沟通触发式总结（Triggered Summary & Methodology Log）

### 2026-09-17 沟通轮次总结（本次指导触发）

#### 1. 核心指令与纠偏触发
- **触发 1（认知彻底纠偏）**：严禁向国内一线工程师索取海外锁具信息。网站的目标是为“不了解海外锁的国内工程师”服务，国内工程师是数据的**使用者与受益者**，不是海外数据的供给者。
- **触发 2（数据供给唯一渠道）**：所有海外锁的参数、安装难点、竞品吐槽与真实故障，必须由我自主从**海外原生生态**（海外原厂手册、Reddit 锁匠与改装社区、海外工单差评）通过工具链自动化爬取并逆向清洗。
- **触发 3（长效记忆与工程规范）**：所有用户发送的信息与指导，必须持续触发总结并沉淀至本记忆文件（`docs/METHODOLOGY_AND_CONTEXT_MEMORY.md`）及工程规划 Excel（`docs/PROJECT_PLAN_AND_CONVENTIONS.xlsx`）。
- **触发 4（五大工业板块与三大核心大主图落地）**：
  - 确立 ASSA ABLOY 事业部 + 五金标准的 5 大板块；
  - 确立北美单插销（US-27）、欧标槽型双锁芯（EU-19）、澳式外装夜锁（AU-11）为三大强相关改造基准锁，并在首页板块顶部设置专属的大主图入口；
  - 每个区域标签强制显示动态样本数量（全部 32，北美 4，澳洲与英国 10，欧洲五国 6，东南亚 10，拉美 2）。

#### 2. 工程计划与模板沉淀
已生成并维护 `docs/PROJECT_PLAN_AND_CONVENTIONS.xlsx`，包含：
1. **工作包与里程碑执行总计划表 (WBS)**；
2. **工程文件分类体系与强制命名规范表**；
3. **5 大工业板块与 Retrofit 强相关基准锁对标矩阵**。
