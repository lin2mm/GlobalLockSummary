import re

def streamline_field_issues(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    # 1. 消除冗长叙事 <p>，只留标题和避坑准则微标签
    t = re.sub(
        r'<p style="font-size: 0\.85rem; color: #475569; line-height: 1\.5; margin: 0 0 10px;">.*?</p>',
        '',
        t
    )

    # 2. 将避坑准则红/橙色大底块换装为 ASSA ABLOY 墨黑极简工业线框微标签
    t = re.sub(
        r'<div style="background: #(?:fef2f2|fff7ed); padding: 8px 10px; border-radius: 4px; font-size: 0\.75rem; color: #(?:991b1b|9a3412); border-left: 3px solid #(?:dc2626|ea580c);">\s*<b>(?:避坑准则|Critical Rule):</b>\s*(.*?)\s*</div>',
        r'<div style="padding: 6px 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px; font-size: 0.74rem; color: #334155; line-height: 1.4;"><b>⌖ 避坑规则:</b> \1</div>',
        t
    )

    # 修复英文版对应规则
    t = re.sub(
        r'<div style="padding: 6px 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px; font-size: 0.74rem; color: #334155; line-height: 1.4;"><b>⌖ 避坑规则:</b> (.*?)</div>',
        lambda m: m.group(0) if 'zh' in path else f'<div style="padding: 6px 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; border-radius: 4px; font-size: 0.74rem; color: #334155; line-height: 1.4;"><b>⌖ Engineering Rule:</b> {m.group(1)}</div>',
        t
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Streamlined {path}!")

streamline_field_issues('content/pages/zh/field-issues.md')
streamline_field_issues('content/pages/en/field-issues.md')

