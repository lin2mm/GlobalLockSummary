import re

def fix_indigenous_page(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    # 1. 消除图片外层的沉重深黑背景 #0f172a，统一替换为 ASSA ABLOY 浅冷灰工业底 #f8fafc，并加上 1px 中性边框
    t = t.replace('background: #0f172a; border-radius: 6px;', 'background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;')
    
    # 2. 将 object-fit: cover 统一为 object-fit: contain，防止锁芯/把手实图被生硬腰斩
    t = t.replace('object-fit: cover;"/>', 'object-fit: contain; padding: 6px;"/>')
    t = t.replace('object-fit: cover;" />', 'object-fit: contain; padding: 6px;" />')

    # 3. 规范推荐转接件框：消除高亮蓝色底，收敛为 ASSA ABLOY 墨黑极细线框
    t = re.sub(
        r'<div style="margin-top: 12px; padding: 8px 12px; background: #eff6ff; border-radius: 4px; font-size: 0\.78rem; color: #1e40af;">\s*💡?\s*<b>(.*?)</b>\s*(.*?)\s*</div>',
        r'<div style="margin-top: 10px; padding: 6px 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px; font-size: 0.76rem; color: #334155;"><b>\1</b> \2</div>',
        t
    )

    # 4. 规范顶部快速直达锚点条：将彩色国旗与彩色表情符号统一步调
    t = t.replace('background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);',
                  'background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px; padding: 10px 14px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Fixed {path}!")

fix_indigenous_page('content/pages/zh/indigenous-guides.md')
fix_indigenous_page('content/pages/en/indigenous-guides.md')

