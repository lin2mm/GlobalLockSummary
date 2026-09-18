import re

# 压缩 adapters.md 顶部间距与卡片图片尺寸
def compact_adapters(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    # 压缩图片高度从 190px 到 150px
    t = t.replace('height: 190px;', 'height: 150px;')
    # 压缩卡片内 padding 从 16px 到 12px 14px
    t = t.replace('<div style="padding: 16px; flex: 1;', '<div style="padding: 12px 14px; flex: 1;')
    # 限制描述文字最大 2 行
    t = re.sub(
        r'<p style="font-size: 0.84rem; color: #475569; line-height: 1.5; margin: 0 0 10px; flex: 1;">(.*?)</p>',
        r'<p style="font-size: 0.82rem; color: #475569; line-height: 1.45; margin: 0 0 8px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">\1</p>',
        t
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Compacted {path}!")

compact_adapters('content/pages/zh/adapters.md')
compact_adapters('content/pages/en/adapters.md')

# 压缩 field-issues.md 卡片高度
def compact_field_issues(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
    t = t.replace('height: 200px;', 'height: 155px;')
    t = t.replace('<div style="padding: 16px;">', '<div style="padding: 12px 14px;">')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Compacted {path}!")

compact_field_issues('content/pages/zh/field-issues.md')
compact_field_issues('content/pages/en/field-issues.md')

