import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# Sheet 1: 工程计划全景甘特表 (Project Roadmap & Execution Plan)
ws1 = wb.active
ws1.title = "工程执行总计划"

# Styles
font_title = Font(name="Arial", size=14, bold=True, color="102A43")
font_section = Font(name="Arial", size=11, bold=True, color="FFFFFF")
font_header = Font(name="Arial", size=10, bold=True, color="1E3A8A")
font_body = Font(name="Arial", size=10, color="1F2937")
font_tag = Font(name="Arial", size=9, bold=True, color="166534")

fill_section = PatternFill(start_color="102A43", end_color="102A43", fill_type="solid")
fill_header = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
fill_done = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
fill_wip = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
fill_todo = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

ws1["A1"] = "GlobalLockSummary 工程实施总计划表（工程里程碑与交付矩阵）"
ws1["A1"].font = font_title
ws1.row_dimensions[1].height = 25

headers1 = ["WBS编号", "阶段 / 工作包", "任务项明细", "责任模式", "输入依据 / 资料源", "交付物产出 / 对应代码", "当前状态", "完成日期"]
ws1.append([]) # row 2 empty
ws1.append(headers1) # row 3
ws1.row_dimensions[3].height = 22

for col_num, h in enumerate(headers1, 1):
    cell = ws1.cell(row=3, column=col_num)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

tasks1 = [
    # Phase 1
    ["1.0", "阶段一：基础与交接", "核实长期分支 arena/01a0a966，对齐 upstream 保持 PR #3 打开", "自主闭环", "Git 状态与上游远端", "Git 分支跟踪已对齐", "已完成", "2026-09-17"],
    ["1.1", "阶段一：基础与交接", "从 GitHub raw_import 拉取并解压 30 类候选锁 Bundle", "用户协同", "GlobalLock_30_Gallery_Bundle.zip", "71 个图片/清单/源码文件解压", "已完成", "2026-09-17"],
    ["1.2", "阶段一：基础与交接", "建立持久化工程方法论与沟通记忆库", "自主闭环", "用户指导要求", "docs/METHODOLOGY_AND_CONTEXT_MEMORY.md", "已完成", "2026-09-17"],
    
    # Phase 2
    ["2.0", "阶段二：图墙落地页改造", "落地页重构为照片驱动图墙（彻底剔除广告长文本）", "自主闭环", "57_GTM 安装图汇总", "content/pages/{zh,en}/index.md", "已完成", "2026-09-17"],
    ["2.1", "阶段二：图墙落地页改造", "实现 5 大工业板块（ASSA ABLOY 体系）：北美、英澳、欧陆、东南亚、拉美", "自主闭环", "全球标准与 ASSA 体系", "build.mjs, content/catalog/gallery.json", "已完成", "2026-09-17"],
    ["2.2", "阶段二：图墙落地页改造", "大号标签 + 动态样本数量显式绑定 (32/4/10/6/10/2)", "自主闭环", "gallery.json 动态统计", "assets/css/site.css, build.mjs", "已完成", "2026-09-17"],
    ["2.3", "阶段二：图墙落地页改造", "3 大强相关 Retrofit 锁型确立为各板块横向 Block-Hero 大主图入口", "自主闭环", "ANSI Deadbolt, Euro 18252, Lockwood 001", "assets/img/hero/*.jpg, build.mjs", "已完成", "2026-09-17"],
    
    # Phase 3
    ["3.0", "阶段三：锁族子页工程深化", "子页面挂载双图（真实安装实物图 + 传动原理图）", "自主闭环", "30 张 real 图 + 30 张 SVG 原理图", "build.mjs lockPage() 渲染扩展", "已完成", "2026-09-17"],
    ["3.1", "阶段三：锁族子页工程深化", "深度解析智能化改造三大难点：关键尺寸、力矩阻力、避坑红线", "自主闭环", "57_GTM 与 56_GTM CSV 数据", "build.mjs, site.css", "已完成", "2026-09-17"],

    # Phase 4
    ["4.0", "阶段四：站内免登反馈闭环", "编写 Cloudflare Pages Functions 接口 /api/feedback", "自主闭环", "国内免科学上网要求", "functions/api/feedback.js", "已完成", "2026-09-17"],
    ["4.1", "阶段四：站内免登反馈闭环", "前端表单改造为单行直接提交 + 工单号生成 + 剪贴板复制兜底", "自主闭环", "用户交互体验指导", "assets/js/feedback.js, src/layout.mjs", "已完成", "2026-09-17"],

    # Phase 5
    ["5.0", "阶段五：全球改装数据爬取", "建立海外一线社媒（Reddit/锁匠论坛）痛点与差评抓取管道", "自主爬虫", "Reddit r/Nuki, r/August, r/homeautomation", "tools/fetch-field-issues.mjs", "已完成", "2026-09-17"],
    ["5.1", "阶段五：全球改装数据爬取", "发布中英双语《全球智能锁改装一线避坑实录》独立页面", "自主闭环", "真实用户退货差评与工单", "content/pages/{zh,en}/field-issues.md", "已完成", "2026-09-17"],
    ["5.2", "阶段五：全球改装数据爬取", "首页上线全球主流改装锁（Nuki/August/SwitchBot/Aqara）对标表格", "自主闭环", "海外社区极限实测数据", "content/catalog/smart-lock-benchmarks.json", "已完成", "2026-09-17"],

    # Phase 6
    ["6.0", "阶段六：长期体系与文件规范", "出台标准化工程计划模板与全套文件命名规范 Excel", "自主闭环", "用户最新指令", "docs/PROJECT_PLAN_AND_CONVENTIONS.xlsx", "已完成", "2026-09-17"],
    ["6.1", "阶段六：长期体系与文件规范", "持续运行 npm test 自动化测试并保持 PR #3 开启", "自主闭环", "项目 CI 与测试规范", "tests/site.test.mjs (31 checks passed)", "进行中", "长期持续"]
]

for row_idx, task in enumerate(tasks1, 4):
    ws1.append(task)
    ws1.row_dimensions[row_idx].height = 20
    for col_idx in range(1, len(task) + 1):
        cell = ws1.cell(row=row_idx, column=col_idx)
        cell.font = font_body
        cell.border = thin_border
        if col_idx in [1, 4, 7, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        if task[6] == "已完成":
            if col_idx == 7:
                cell.fill = fill_done
                cell.font = font_tag
        elif task[6] == "进行中":
            if col_idx == 7:
                cell.fill = fill_wip


# Sheet 2: 文件分类体系与命名规范 (Directory Structure & Naming Conventions)
ws2 = wb.create_sheet(title="文件命名与目录体系规范")
ws2["A1"] = "GlobalLockSummary 工程文件分类体系与命名规则 (Standard Conventions)"
ws2["A1"].font = font_title
ws2.row_dimensions[1].height = 25

headers2 = ["层级分类", "目录物理路径", "文件命名规则 / 格式模板", "说明与示例", "强制约束原则"]
ws2.append([])
ws2.append(headers2)
ws2.row_dimensions[3].height = 22

for col_num, h in enumerate(headers2, 1):
    cell = ws2.cell(row=3, column=col_num)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

conventions2 = [
    ["1. 结构化数据库", "content/catalog/", "*.json (纯小写横杠 kebab-case)", "gallery.json, field-issues.json, smart-lock-benchmarks.json", "纯数据定义，严禁嵌入可执行 JS 逻辑；必须支持双语 zh/en 字段"],
    ["2. 锁族单项参数", "content/catalog/lock-families/", "{family-id}.json", "us-deadbolt.json, au-deadlatch.json, euro-cylinder-mortise.json", "ID 必须为全局唯一稳定标识，严禁随意改名破坏外部链接与机读引用"],
    ["3. 双语静态页面", "content/pages/{zh,en}/", "{slug}.md (小写横杠)", "index.md, retrofit.md, field-issues.md, identify.md", "以 Markdown 编写，头部携带 FrontMatter (title, description)，必须中英成对存在"],
    ["4. 真实安装实物图", "assets/img/gallery/", "{region}_{model}_real.{ext}", "us-27_real.jpg, au-11_real.jpg, sg-01_real.jpg", "必须为门上实物照片；图片宽度统一切割压缩至 <= 1000px，保留清晰度控制体积"],
    ["5. 传动受力原理图", "assets/img/diagrams/", "{region}_{model}_schematic.svg", "US-27_schematic.svg, AU-11_schematic.svg, EU-19_schematic.svg", "必须为矢量 SVG；统一标明内侧电机、锁体、方轴与联动箭头路线"],
    ["6. 板块大主图", "assets/img/hero/", "hero-{region}-{model}.{ext}", "hero-na-deadbolt.jpg, hero-europe-eurocylinder.jpg", "用于 5 大板块顶级入口展示的大号横向代表图，长宽比控制在 16:10"],
    ["7. 服务端无服务接口", "functions/api/", "{service-name}.js", "functions/api/feedback.js", "Cloudflare Pages Functions 接口；严禁将任何 Webhook/API Key 提交至 Git"],
    ["8. 自动化与爬取脚本", "tools/", "{verb}-{noun}.mjs", "tools/fetch-field-issues.mjs, tools/validate-data.mjs", "Node.js ESM 脚本；用于数据自动拉取、清洗转换与引用完整性校验"],
    ["9. 长期记忆与文档", "docs/", "*.md / *.xlsx (大写下划线或标准名)", "docs/METHODOLOGY_AND_CONTEXT_MEMORY.md, docs/PROJECT_PLAN_AND_CONVENTIONS.xlsx", "永久固化用户沟通指令、演进决策与全景规划，防跨会话失忆"]
]

for row_idx, conv in enumerate(conventions2, 4):
    ws2.append(conv)
    ws2.row_dimensions[row_idx].height = 20
    for col_idx in range(1, len(conv) + 1):
        cell = ws2.cell(row=row_idx, column=col_idx)
        cell.font = font_body
        cell.border = thin_border
        if col_idx in [1, 2, 3]:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")


# Sheet 3: 全球锁 5 大板块与 Retrofit 矩阵 (5 Divisions & Retrofit Matrix)
ws3 = wb.create_sheet(title="5大工业板块与Retrofit基准")
ws3["A1"] = "全球锁 5 大工业板块划分与智能改造强相关基准矩阵"
ws3["A1"].font = font_title
ws3.row_dimensions[1].height = 25

headers3 = ["板块代码", "工业板块名称", "涵盖重点国家", "遵循主流五金标准", "核心代表机械锁族", "Retrofit 强相关度", "核心改装成败死穴 (Engineering Bottleneck)"]
ws3.append([])
ws3.append(headers3)
ws3.row_dimensions[3].height = 22

for col_num, h in enumerate(headers3, 1):
    cell = ws3.cell(row=3, column=col_num)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

matrix3 = [
    ["na", "🇺🇸 北美标准板块 (Americas)", "美国、加拿大、墨西哥", "ANSI/BHMA A156.36 / A156.2", "单缸插销死锁 (Deadbolt / Schlage B60)", "⭐⭐⭐ 极强相关 (基准)", "木门受潮下沉或防风条弹性将门向外推，导致插销与扣板卡阻 (Deadbolt Jam)"],
    ["europe5", "🇪🇺 欧陆五国板块 (Continental Europe)", "德国、法国、意大利、西班牙、荷兰", "DIN 18251 / 18252, EN 12209", "欧标槽型双锁芯 (Euro Profile DIN 18252)", "⭐⭐⭐ 极强相关 (基准)", "内侧常插钥匙时，锁芯必须具备 DIN 18252 BS 双向应急离合认证，否则断电造成彻底反锁"],
    ["uk-anz", "🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK)", "澳大利亚、新西兰、英国、爱尔兰", "AS 4174 (澳标), BS 3621 (英标)", "澳式外装夜锁与双扣锁 (Lockwood 001/355)", "⭐⭐⭐ 极强相关 (基准)", "辅助锁舌 (Auxiliary Latch) 必须完全压入门框扣板，否则旋钮转动主舌并未死锁 (假安全)"],
    ["sea", "🇸🇬 东南亚与东亚板块 (Asia-Pacific)", "新加坡、马来西亚、泰国、越南、韩国", "SS 312, SCDF 逃生规范, KS", "新加坡 HDB 铁闸锁与推拉式插芯锁", "⭐⭐ 强相关 (边界)", "组屋双门外闸与内木门净距 <80mm，智能锁厚度超过 35mm 即发生把手致命撞击"],
    ["latam", "🌎 拉美新兴板块 (Latin America)", "巴西、智利、秘鲁、哥伦比亚、阿根廷", "ABNT NBR 14913, ODIS 体系", "拉美 ABNT 40/45mm 极窄背距插芯把手锁", "⭐⭐ 强相关 (边界)", "背距极窄且门扇仅 30mm 厚，电机底座稍宽即撞击门框防风条"]
]

for row_idx, mat in enumerate(matrix3, 4):
    ws3.append(mat)
    ws3.row_dimensions[row_idx].height = 22
    for col_idx in range(1, len(mat) + 1):
        cell = ws3.cell(row=row_idx, column=col_idx)
        cell.font = font_body
        cell.border = thin_border
        if col_idx in [1, 6]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Auto-adjust column widths
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            # approximate width for chinese/english
            length = sum(2 if ord(c) > 127 else 1 for c in val_str)
            if length > max_len:
                max_len = length
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

out_xlsx = "docs/PROJECT_PLAN_AND_CONVENTIONS.xlsx"
wb.save(out_xlsx)
print(f"Generated {out_xlsx} successfully!")
