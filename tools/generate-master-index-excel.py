import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path("/home/user/GlobalLockSummary")
CONTENT = ROOT / "content" / "catalog"
DOCS = ROOT / "docs"

wb = openpyxl.Workbook()

# Styles
font_title = Font(name="Arial", size=14, bold=True, color="102A43")
font_section = Font(name="Arial", size=11, bold=True, color="FFFFFF")
font_header = Font(name="Arial", size=10, bold=True, color="1E3A8A")
font_body = Font(name="Arial", size=10, color="1F2937")
font_code = Font(name="Consolas", size=9, color="0F172A")
font_tag = Font(name="Arial", size=9, bold=True, color="166534")

fill_section = PatternFill(start_color="102A43", end_color="102A43", fill_type="solid")
fill_header = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
fill_alt = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

def style_sheet(ws, title, headers, rows):
    ws.title = title[:31]
    ws["A1"] = f"GlobalLockSummary 全局索引 — {title}"
    ws["A1"].font = font_title
    ws.row_dimensions[1].height = 25
    
    ws.append([]) # row 2 empty
    ws.append(headers) # row 3
    ws.row_dimensions[3].height = 22
    
    for col_num, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    for r_idx, row_data in enumerate(rows, 4):
        ws.append(row_data)
        ws.row_dimensions[r_idx].height = 20
        use_fill = fill_alt if r_idx % 2 == 0 else None
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.font = font_body
            cell.border = thin_border
            if use_fill:
                cell.fill = use_fill
            if c_idx == 1 or "ID" in headers[c_idx-1] or "编号" in headers[c_idx-1]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            length = sum(2 if ord(c) > 127 else 1 for c in val_str)
            if length > max_len:
                max_len = length
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

# ----------------- Sheet 1: 全局数据与资产索引总览 (Master Navigation Index) -----------------
ws1 = wb.active
headers1 = ["模块大类", "数据分类 / 业务主题", "涵盖记录数", "物理存储文件", "在线访问页面", "关联抓取实物图路径", "核心作用与工程价值"]
rows1 = [
    ["1. 工业板块与图墙", "5大标准板块与32类实物图谱", "32 种锁型", "content/catalog/gallery.json", "/zh/index.html", "assets/img/gallery/*_real.jpg", "全球存量锁真实安装实景，按 ASSA ABLOY 分区与动态计数直观呈现"],
    ["1. 工业板块与图墙", "3大强相关基准锁 Block-Hero", "3 款基准", "assets/img/hero/*.jpg", "/zh/index.html 展板", "assets/img/hero/hero-*.jpg", "北美 Deadbolt、欧标双锁芯、澳式 001 顶级入口超大图与死穴直达"],
    ["2. 本土辨锁大百科", "5国本土语言测锁与工业术语", "5 大国别体系", "content/catalog/indigenous-lock-guides.json", "/zh/indigenous-guides.html", "assets/img/indigenous/*.png|jpg", "收录德、法、日、英、西本土锁匠量测口诀，破解 Dornmaß、Axe、Entraxe 差异"],
    ["3. 专项研发工具", "日本主流门锁面板刻印速查字典", "5 大主力锁族 (28+刻印)", "content/catalog/japan-engraving-matrix.json", "/zh/japan-engravings.html", "assets/img/indigenous/jp-*.jpg", "刻印即型号，输入 MIWA/GOAL 刻印 1 秒获取 CAD 开孔与专用夹爪"],
    ["3. 专项研发工具", "全球智能锁 Retrofit 标准转接件 BOM", "4 款核心转接套", "content/catalog/adapters-bom.json", "/zh/adapters.html", "assets/img/tools/adapter-7to8mm.png", "法国 7转8mm 变径方轴、德标 8转9mm 逃生套、美标十字尾轴盘、日本捏合爪"],
    ["3. 专项研发工具", "海外主流防盗锁 1:1 官方开孔打样模板", "3 套原厂规范", "content/catalog/drilling-templates.json", "/zh/drilling-templates.html", "assets/img/tools/template-*.png", "北美 ANSI 54mm 大孔、日本 42mm 螺栓距、欧标 72/92mm PZ 开孔规程"],
    ["4. 改装排雷与电商", "全球智能锁改装一线避坑实录", "4 大经典故障源", "content/catalog/field-issues.json", "/zh/field-issues.html", "assets/img/tools/gap-clearance.jpg", "抓取 Reddit / 锁匠工单真实差评：抬把手过载、门缝卡阻、离合反锁、胶贴脱落"],
    ["4. 改装排雷与电商", "海外跨境爆款机械锁兼容性排行榜", "4 国顶流爆款", "content/catalog/bestseller-locks.json", "/zh/bestseller-matrix.html", "assets/img/tools/bestseller-deadbolt.jpg", "美亚 Kwikset、德亚 ABUS、日本乐天 MIWA、英亚 Yale 畅销机械锁改装适配榜"],
    ["5. 核心机读数据", "全站全量机读数据集 API", "全部数据汇总", "_site/data/catalog.json", "/data/catalog.json", "全站资产统一引用", "供企业研发系统、移动端 App、出海选型工具直接一键 GET 拉取调用"],
    ["5. 核心机读数据", "站内全文检索实时倒排索引", "118 个页面索引", "_site/data/search-index.json", "/search.html", "站内全局搜索", "全站全文分词索引，支持任意型号、术语、公差毫秒级搜索联想"]
]
style_sheet(ws1, "全局数据资产索引总览", headers1, rows1)

# ----------------- Sheet 2: 日本刻印反查速查索引 -----------------
ws2 = wb.create_sheet()
jp_data = json.loads((CONTENT / "japan-engraving-matrix.json").read_text("utf8"))
headers2 = ["制造品牌", "面板冲压刻印 (フロント刻印)", "机械锁具类别", "标准背距 (Backset)", "对应门厚 (Door Thickness)", "改装难度评级", "推荐加装智能锁 / 适配夹爪", "实物/CAD图片文件", "关键工程死穴与要点"]
rows2 = []
for item in jp_data:
    rows2.append([
        item["brand"],
        item["engraving"],
        item["lockType"],
        item["backset"],
        item["doorThickness"],
        item["retrofitDifficulty"],
        ", ".join(item["compatibleSmartAdapters"]),
        item["cadImage"],
        item["notes"]
    ])
style_sheet(ws2, "日本面板刻印反查索引", headers2, rows2)

# ----------------- Sheet 3: 转接件 BOM 清单索引 -----------------
ws3 = wb.create_sheet()
adp_data = json.loads((CONTENT / "adapters-bom.json").read_text("utf8"))
headers3 = ["转接件编号", "转接件配件全称", "目标国家 / 区域", "解决核心工程痛点", "推荐材质与工艺", "关键尺寸与公差要求", "是否支持3D打印", "对应实物照片", "现场安装注意事项"]
rows3 = []
for item in adp_data:
    rows3.append([
        item["id"],
        item["name"],
        item["targetRegion"],
        item["problemSolved"],
        item["materialRecommendation"],
        item["criticalTolerance"],
        "是 (支持打样)" if item["diy3dPrintReady"] else "否 (必须金属受力)",
        item["image"],
        item["notes"]
    ])
style_sheet(ws3, "转接件BOM与公差索引", headers3, rows3)

# ----------------- Sheet 4: 1:1 开孔打样模板索引 -----------------
ws4 = wb.create_sheet()
tpl_data = json.loads((CONTENT / "drilling-templates.json").read_text("utf8"))
headers4 = ["模板编号", "适配锁族与型号", "遵循国际工业标准", "门面大圆孔尺寸 (Cross Bore)", "门侧锁舌孔 (Edge Bore)", "可选背距档位 (Backset)", "侧边面板开槽 (Stulp Mortise)", "官方工程图纸路径", "打孔施工防呆要点"]
rows4 = []
for item in tpl_data:
    rows4.append([
        item["id"],
        item["lockFamily"],
        item["standard"],
        item["boreHoleDiameter"],
        item["crossBoreDiameter"],
        item["backsetOptions"],
        item["edgeMortise"],
        item["image"],
        item["keyCheckPoints"]
    ])
style_sheet(ws4, "开孔打样工程模板索引", headers4, rows4)

# ----------------- Sheet 5: 跨境电商爆款机械锁兼容索引 -----------------
ws5 = wb.create_sheet()
best_data = json.loads((CONTENT / "bestseller-locks.json").read_text("utf8"))
headers5 = ["榜单编号", "电商销量排名与渠道", "机械锁代表型号", "主导市场区域", "预估市场保有量", "锁芯机械结构", "智能锁改装适配率", "推荐对标智能锁型号", "真实实物照片", "工程避坑与死穴说明"]
rows5 = []
for item in best_data:
    rows5.append([
        item["id"],
        item["rank"],
        item["model"],
        item["region"],
        item["marketShare"],
        item["lockMechanism"],
        item["retrofitFeasibility"],
        item["recommendedSmartLock"],
        item["image"],
        item["engineeringCaveat"]
    ])
style_sheet(ws5, "海外爆款机械锁兼容索引", headers5, rows5)

# ----------------- Sheet 6: 真实故障与差评避坑索引 -----------------
ws6 = wb.create_sheet()
field_data = json.loads((CONTENT / "field-issues.json").read_text("utf8"))
headers6 = ["工单编号", "代表品牌与型号", "目标区域市场", "锁具与门体类型", "海外一线高频故障现象 (Symptom)", "物理与机械失效根因 (Root Cause)", "机械失效模式 (Failure Mode)", "数据抓取来源", "研发与出海必须采取的对策"]
rows6 = []
for idx, item in enumerate(field_data, 1):
    rows6.append([
        f"ISSUE-{idx:02d}",
        item.get("brand", "—"),
        item.get("market", "—"),
        item.get("lockType", "—"),
        item.get("symptom", "—"),
        item.get("rootCause", "—"),
        item.get("mechanicalFailureMode", "—"),
        item.get("source", "—"),
        item.get("engineeringRecommendation", "—")
    ])
style_sheet(ws6, "真实故障避坑工单索引", headers6, rows6)

excel_path = DOCS / "GLOBAL_LOCK_DATA_INDEX.xlsx"
wb.save(excel_path)
print(f"Generated comprehensive Excel index at: {excel_path}")
