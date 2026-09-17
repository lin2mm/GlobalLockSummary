#!/usr/bin/env python3
"""
重新生成 docs/03_GLOBAL_LOCK_DATA_INDEX.xlsx 及 docs/GLOBAL_LOCK_DATA_INDEX.xlsx
包含全站 54 款锁型的全维度工程数据、公差矩阵、二次修槽扩孔规范与贯穿螺栓避让指引
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
    ws1 = wb.active
    ws1.title = "01_全局工业索引与标准"

    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    border_style = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    ws1_headers = [
        "序号", "工业板块", "标准代码", "样本总数", "主流背距 (Backset)", 
        "中心距 (Centres)", "方轴孔径", "门厚区间", "锁槽二次扩孔规范", "走线与对穿螺栓避让"
    ]
    ws1.append(ws1_headers)
    for col_idx in range(1, len(ws1_headers) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    divisions_data = [
        ["DIV-01", "北美工业板块 (North America)", "ANSI / BHMA A156", 10, "60/70mm 可调", "140mm (5-1/2\")", "1.6×4.8mm 扁平尾轴", "35-51mm", "钻孔54mm贯穿；老木门开裂加装不锈钢防劈裂抱门锁夹套板", "#10-32 对穿螺栓，走线通道置于扁平尾轴正下方，预留≥4mm硅胶套管"],
        ["DIV-02", "欧陆工业板块 (Continental Europe)", "DIN 18251 / EN 12209", 12, "55/65mm (窄框35-45mm)", "室内72mm / 入户92mm", "8×8mm (逃生9×9mm)", "38-65mm", "原槽75-80mm；扩深需沿中心线钻阶梯孔微修，严禁劈裂门扇立挺", "M5 沉头螺栓，锁芯上方设专属穿线橡胶护线圈，严防方轴摩擦线束"],
        ["DIV-03", "澳新及英国板块 (Oceania & UK)", "AS 4145 / BS 3621", 12, "40/60mm", "分体夜闩", "十字/偏心尾轴", "32-45mm", "Lockwood 001 表面装配仅打32mm通孔；门框必须安装加固角铁扣盒", "表面底盘 4 颗 10# 螺钉固定，旋钮传动拨叉内置防缠绕护套"],
        ["DIV-04", "东南亚与东亚板块 (East & Southeast Asia)", "JIS A 1510 / SS 332", 12, "51/64mm", "独立/联动", "8×8mm 高精", "33-42mm", "间隙≤1.0mm高精锁槽；铝合金窄框门必须用金属铣刀开孔，加1.5mm衬板", "M4 高精贯穿螺栓，超薄门用剪切型螺钉，走线通道置于锁体顶部专属滑槽"],
        ["DIV-05", "拉美工业板块 (Latin America)", "ABNT NBR 14913", 8, "40/45mm 极窄", "53/70mm", "8×8mm 宽公差", "30-35mm", "浅槽(深60mm)；向内扩孔必须加装 2.0mm 冷轧钢加强扣板以防撬门", "M4 粗牙螺栓，夹板门必须在内部加装宽平垫片防止门面被压溃变形"]
    ]
    for row in divisions_data:
        ws1.append(row)

    # 工作表 2：54 款详细样本数据库（含工程公差、木槽修凿与避线规范）
    ws2 = wb.create_sheet(title="02_54款机械锁详细数据库")
    ws2_headers = [
        "锁型ID", "候选标识", "锁系ID", "中文名称", "英文名称", "工业板块",
        "市场保有率", "加装亲和度", "场景实景图路径", "机械结构图路径",
        "门缝公差要求", "标称电机扭矩", "垂直下沉耐受", "逃生安全规范", "租房友好评级",
        "钥匙胚槽型", "木槽二次扩孔修整指引", "对穿螺栓避线通道"
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
            guide.get("recommendedClearance", "≥ 3.0mm"),
            guide.get("requiredTorque", "≥ 1.5 N·m"),
            eng.get("saggingTolerance", "±2.0mm"),
            egress.get("standard", "Compliant"),
            rental.get("rating", "Grade A"),
            eng.get("keywaySpecification", "N/A"),
            eng.get("mortiseReworkGuide", "N/A"),
            eng.get("boltWireClearance", "N/A")
        ]
        ws2.append(row_data)

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
    print("Master index Excel updated with Mortise Rework and Wire Guide specs!")

if __name__ == "__main__":
    build_master_excel()
