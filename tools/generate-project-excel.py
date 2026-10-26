#!/usr/bin/env python3
"""
重新生成 docs/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx
涵盖全站 70 款全球锁型、主流 vs 小众四维分级模型与常驻闭环进展
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_project_excel():
    wb = openpyxl.Workbook()
    
    # 工作表 1：项目执行甘特图与迭代计划
    ws1 = wb.active
    ws1.title = "01_执行甘特图与WBS"

    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    border_style = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    headers1 = ["WBS编号", "执行阶段", "核心里程碑与交付物", "负责人/机制", "对齐工业标准", "关联代码/文件", "当前状态", "完成日期"]
    ws1.append(headers1)
    for col_idx in range(1, len(headers1) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    wbs_data = [
        ["WBS-01.1", "阶段一：工业架构建立", "五大工业板块划分 (ASSA ABLOY 运营体系对标)", "自主闭环", "ANSI / DIN / BS / JIS / ABNT", "build.mjs, content/catalog/gallery.json", "已完成", "2026-09-17"],
        ["WBS-01.2", "阶段一：工业架构建立", "样本规模从 38 款扩充至 54 款并最终扩充至 70 款全球全覆盖", "自主闭环", "全球 5 大标准全息覆盖", "tools/expand-to-70-locks.py, gallery.json", "已完成", "2026-09-17"],
        ["WBS-02.1", "阶段二：三层视觉穿透", "第1层 Entry 真实门上实景图 + 严格主流筛选模型", "自主闭环", "市场保有率 ≥25% 优先加权", "build.mjs, docs/05_HIERARCHICAL_GALLERY_INDEX.md", "已完成", "2026-09-17"],
        ["WBS-02.2", "阶段二：三层视觉穿透", "第2层 产品图 + 门上场景图并列卡片流 (Mainstream/Niche 徽章与过滤)", "自主闭环", "ASSA ABLOY 工业极简系统", "build.mjs, site.css", "已完成", "2026-09-17"],
        ["WBS-02.3", "阶段二：三层视觉穿透", "第3层 1:1 开孔打样模板、四步工序与公差矩阵渲染", "自主闭环", "DIN 18251 / ANSI A156 模板", "build.mjs, assets/img/diagrams/", "已完成", "2026-09-17"],
        ["WBS-03.1", "阶段三：视觉与设计精进", "ISO 7001 图标量化评级模型与 16px 光学高辨识锁标升级", "自主闭环", "ISO 7001 / IEC 60417", "docs/06_ICON_DESIGN_AND_RANKING_SYSTEM.xlsx", "已完成", "2026-09-17"],
        ["WBS-03.2", "阶段三：视觉与设计精进", "工业索引全站 2 列 Gallery 风格重构与双模无刷新切换器", "自主闭环", "响应式画廊网格", "content/pages/zh/indigenous-guides.md", "已完成", "2026-09-17"],
        ["WBS-04.1", "阶段四：工程数据矩阵", "全站 70 款锁型公差矩阵、免打孔评级与紧急逃生规范", "自主闭环", "EN 179 / BS 8621 / AS 4145.2", "gallery.json, build.mjs", "已完成", "2026-09-17"],
        ["WBS-04.2", "阶段四：工程数据矩阵", "电机峰值堵转电流、原厂防钻保险等级与门磁抗金属屏蔽指引", "自主闭环", "SKG★★★ / VdS 2162 / CP", "gallery.json, build.mjs", "已完成", "2026-09-17"],
        ["WBS-05.1", "阶段五：常驻守护与免疫", "10分钟常驻守护进程 runner-10m.py 与导航动态锁数量自动化测试断言", "自主闭环", "Jest/Node Test 拦截熔断", "tests/site.test.mjs, runner-10m.py", "已完成", "2026-09-17"]
    ]
    for r in wbs_data:
        ws1.append(r)

    # 工作表 2：主流锁 vs 小众锁四维判别标准与筛选规范
    ws2 = wb.create_sheet(title="02_主流与小众锁筛选规范")
    headers2 = ["分级维度编号", "评判维度", "主流基准锁 (Tier 1 Mainstream)", "小众/特殊锁型 (Tier 2/3 Niche)", "视觉辨识呈现方式", "加装研发与采购策略建议"]
    ws2.append(headers2)
    for col_idx in range(1, len(headers2) + 1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    tier_rules = [
        ["RULE-01", "区域市场保有率 (Market Share)", "≥ 20% ~ 35%+ (该国绝对主力存量)", "< 10% (特定老房、古董、高端特种)", "主流显示蓝底金星 ★ MAINSTREAM 徽章；小众显示深灰 NICHE 徽章", "主流锁必须标配专用转接五金套件，小众锁提供选配或 3D 打印支持"],
        ["RULE-02", "Retrofit 加装匹配度 (Affinity)", "Grade A / A+ (标准旋钮、扁平轴、欧标双钥匙)", "Grade C / D (垂直锁舌、异形圆柱锁芯、十字钥匙)", "卡片直接标明改装友好度等级与无损免打孔评级", "主流锁实现 100% 免打孔退租无痕；小众锁需提供改装支架图纸"],
        ["RULE-03", "原厂五金标准化 (Standardization)", "符合 ANSI A156 / DIN 18251 / BS 3621 通识尺寸", "专属专利非标结构 (如法系 Fichet、纽约 Segal 联锁)", "在第二层画廊与工业索引高亮原厂标准代号", "主流锁直接采购通用现货五金；小众锁需开模定制专用法兰"],
        ["RULE-04", "即时过滤筛选机制 (Instant Filter)", "分类页支持一键筛选【主流基准锁】", "分类页支持一键筛选【小众/特殊锁】", "顶部提供 Mainstream / Niche 动态计数切换按钮", "出海团队下发开模需求时优先过滤主流锁型，防止长尾产品拖垮研发"]
    ]
    for r in tier_rules:
        ws2.append(r)

    # 自动列宽
    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)

    out_path = os.path.join(ROOT, "docs", "02_PROJECT_PLAN_AND_CONVENTIONS.xlsx")
    wb.save(out_path)
    import shutil
    shutil.copy(out_path, os.path.join(ROOT, "docs", "PROJECT_PLAN_AND_CONVENTIONS.xlsx"))
    shutil.copy(out_path, "/home/user/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx")
    print("Regenerated docs/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx successfully!")

if __name__ == "__main__":
    generate_project_excel()
