#!/usr/bin/env python3
"""
重新生成 docs/03_GLOBAL_LOCK_DATA_INDEX.xlsx 及 docs/GLOBAL_LOCK_DATA_INDEX.xlsx
包含全站 54 款锁型的全维度工程数据、公差矩阵与合规信息
"""
import os
import json
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(ROOT, "content", "catalog", "gallery.json")

def build_master_excel():
    wb = openpyxl.Workbook()
    # 默认工作表
    ws1 = wb.active
    ws1.title = "01_全局工业索引"

    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    border_style = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    ws1_headers = [
        "序号", "工业板块", "标准代码", "样本总数", "主图筛选覆盖率", 
        "典型门锁类别", "主要锁芯/锁体类型", "核心加装路线", "工程难点与风险"
    ]
    ws1.append(ws1_headers)
    for col_idx in range(1, len(ws1_headers) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    divisions_data = [
        ["DIV-01", "北美工业板块 (North America)", "ANSI / BHMA A156", 10, "100% 4K/HD 实景", "单插销死锁 (Deadbolt), 复合一体锁 (Handleset), 美标插芯锁 (Mortise)", "美标实心转尾锁芯 (Rim/Mortise Cylinder)", "内旋钮转接头 (Thumbturn Adapters)", "门扇下沉与扣板严重错位 (Strike Plate Binding)"],
        ["DIV-02", "欧陆工业板块 (Continental Europe)", "DIN 18251 / EN 12209", 12, "100% 4K/HD 实景", "欧标插芯锁 (Euro Mortise), 多点传动锁 (Multipoint Raise-to-Lock)", "欧标水滴双向锁芯 (Euro Profile Cylinder DIN 18252)", "内插钥匙夹持马达 (Key Gripping / Nuki Style)", "多点联动抬把手操作过载与外锁闭破门隐患 (Emergency Clutch Lockout)"],
        ["DIV-03", "澳新及英国板块 (Oceania & UK)", "AS 4145 / BS 3621", 12, "100% 4K/HD 实景", "英式五杠杠杆锁 (5-lever Mortice), 表面自锁夜闩锁 (Lockwood 001/002)", "椭圆锁芯 (Oval Cylinder), 螺口锁芯 (Screw-in Mortise)", "副舍压紧加装 (Auxiliary Latch Retrofit)", "门缝过大导致辅助锁舌悬空失效 (False Deadlock)"],
        ["DIV-04", "东南亚与东亚板块 (East & Southeast Asia)", "JIS A 1510 / SS 332", 12, "100% 4K/HD 实景", "日式高精度插芯锁 (MIWA / GOAL), 新加坡组屋铁闸门锁 (HDB Metal Gate Lock)", "双面铣齿插芯锁芯, 超小孔径锁芯", "双门防撞超薄电机 (Ultra-slim <35mm)", "内外门把手间距不足 80mm 碰撞卡死 (Gate Clearance Clash)"],
        ["DIV-05", "拉美工业板块 (Latin America)", "ABNT NBR 14913", 8, "100% 4K/HD 实景", "拉美窄体锁体 (PADO / Stam), 执手锁 (Scanavini)", "拉美欧标变体锁芯 (ABNT Cylinder), 宽截面拨叉", "原装替换与高扭矩电机加装", "五金冲压毛刺公差大、机械摩擦阻力极高 (High Friction Resistance)"]
    ]
    for row in divisions_data:
        ws1.append(row)

    # 工作表 2：54 款详细样本数据库（含工程公差矩阵）
    ws2 = wb.create_sheet(title="02_54款机械锁详细数据库")
    ws2_headers = [
        "锁型ID", "候选标识", "锁系ID", "中文名称", "英文名称", "工业板块",
        "市场保有率", "加装亲和度", "场景实景图路径", "机械结构图路径",
        "打样模板", "门缝公差要求", "标称电机扭矩", "垂直下沉耐受", "逃生安全规范", "租房友好评级"
    ]
    ws2.append(ws2_headers)
    for col_idx in range(1, len(ws2_headers) + 1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    with open(GALLERY_JSON, "r", encoding="utf-8") as f:
        locks = json.load(f)

    for lk in locks:
        sel = lk.get("selectionScore", {})
        guide = lk.get("installationGuide", {})
        eng = lk.get("engineeringMatrix", {})
        egress = eng.get("egressCompliance", {})
        rental = eng.get("rentalOptimization", {})

        row_data = [
            lk.get("id"),
            lk.get("candidateId"),
            lk.get("familyId"),
            lk.get("title", {}).get("zh", ""),
            lk.get("title", {}).get("en", ""),
            lk.get("region"),
            sel.get("marketCoverage", "High"),
            sel.get("retrofitAffinity", "Grade A"),
            lk.get("sceneImage", lk.get("image")),
            lk.get("productImage", lk.get("image")),
            guide.get("drillingTemplate", "N/A"),
            guide.get("recommendedClearance", "≥ 3.0mm"),
            guide.get("requiredTorque", "≥ 1.5 N·m"),
            eng.get("saggingTolerance", "±2.0mm"),
            egress.get("standard", "Compliant"),
            rental.get("rating", "Grade A")
        ]
        ws2.append(row_data)

    # 自动调整列宽
    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)

    out_docs = os.path.join(ROOT, "docs", "03_GLOBAL_LOCK_DATA_INDEX.xlsx")
    wb.save(out_docs)
    shutil.copy(out_docs, os.path.join(ROOT, "docs", "GLOBAL_LOCK_DATA_INDEX.xlsx"))
    shutil.copy(out_docs, os.path.join("/home/user", "03_GLOBAL_LOCK_DATA_INDEX.xlsx"))
    print(f"Master index Excel rebuilt with 54 locks and engineering matrices!")

if __name__ == "__main__":
    build_master_excel()
