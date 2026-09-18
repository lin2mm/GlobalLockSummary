#!/usr/bin/env python3
"""
生成 07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx
记录主流基准锁与非主流/小众锁的对比度模型 (WCAG 2.1 AAA)、色块规范与光学淡化参数
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_color_excel():
    wb = openpyxl.Workbook()
    
    # 工作表 1：色块分层设计系统
    ws1 = wb.active
    ws1.title = "01_色块设计系统与参数规范"

    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    border_style = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    headers1 = ["视觉元素", "★ 主流基准锁 (Tier 1 Mainstream)", "🔍 非主流/小众锁 (Tier 2/3 Niche)", "视觉心理学与工程考量 (Design Rationale)"]
    ws1.append(headers1)
    for col_idx in range(1, len(headers1) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    elements_data = [
        ["容器外边框 (Border)", "1.5px solid #0284c7 (高对比钛金蓝强调框)", "1px solid #e2e8f0 (极淡中性雾灰细线)", "主流锁轮廓坚挺，非主流锁边缘弱化，形成清晰的主次分离"],
        ["贯穿指示条 (Accent Bar)", "左侧 4px 实心钛蓝 #0284c7 基准竖条", "左侧 3px 哑光冷灰 #94a3b8 辅条", "提供一眼可见的骨架定位线，扫视瞬间即可捕获主流锁锚点"],
        ["卡片底色 (Background)", "纯白 #ffffff (100% 不透明度)", "低饱和灰蓝 #f8fafc (不透明度 0.88, 饱和度 0.85)", "让非主流锁整体自然退后一层，主流锁浮现为视觉前景焦点"],
        ["顶角徽章 (Corner Badge)", "蓝底白字【★ 主流基准 (MAINSTREAM)】加深投影", "淡灰底中灰字【非主流/小众 (NICHE)】边框标签", "不给小众锁施加刺眼颜色，用低调标签传达其小众特质"],
        ["市占比胶囊 (Share Pill)", "天蓝底深蓝字 #e0f2fe / #0369a1 (≥25%+)", "微灰底灰字 #f1f5f9 / #94a3b8 (<10%)", "量化出海市场保有率，数字即权威依据"],
        ["标题排印 (Typography)", "700 粗体，深邃工业黑 #0f172a", "500 中等粗细，中灰金属色 #475569", "避免文字层面的同质化竞争，突出主流产品品类"],
        ["阴影层深 (Elevation)", "box-shadow: 0 4px 14px rgba(2,132,199,0.08)", "无阴影 (浮动时展示极弱 0 4px 12px 漫反射)", "利用微物理悬浮层深强化视觉权重差异"]
    ]
    for r in elements_data:
        ws1.append(r)

    # 工作表 2：全站 70 款锁型色块分层明细
    ws2 = wb.create_sheet(title="02_70款锁型分层归属表")
    headers2 = ["锁型ID", "锁具名称", "工业板块", "市场层级 (Tier)", "色块模式 (Theme)", "市占比 (Share)", "加装亲和度", "推荐研发采购策略"]
    ws2.append(headers2)
    for col_idx in range(1, len(headers2) + 1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    import json
    with open(os.path.join(ROOT, "content/catalog/gallery.json"), "r", encoding="utf-8") as f:
        locks = json.load(f)

    for lk in locks:
        is_m = lk.get("tierClass") == "Mainstream"
        ws2.append([
            lk.get("id"),
            lk.get("title", {}).get("zh", lk.get("id")),
            lk.get("region"),
            "★ 主流基准 (Mainstream)" if is_m else "🔍 小众/特殊 (Niche)",
            "高对比钛蓝强调 (Bright White + Solid Blue Bar)" if is_m else "低饱和雾灰淡色 (Muted Light Gray + Opacity 0.88)",
            lk.get("marketSharePercent", "≥25%" if is_m else "<10%"),
            lk.get("selectionScore", {}).get("retrofitAffinity", "Grade A"),
            "优先标配现货免打孔套件与大货开模" if is_m else "提供定制 3D 打印支架或长尾选配，避免挤占核心研发资源"
        ])

    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)

    out_path = os.path.join(ROOT, "docs", "07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx")
    wb.save(out_path)
    import shutil
    shutil.copy(out_path, "/home/user/07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx")
    print("Generated docs/07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx successfully!")

if __name__ == "__main__":
    generate_color_excel()
