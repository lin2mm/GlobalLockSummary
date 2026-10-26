import re

# 1. 修复 field-issues.md 卡片点击与穿帮
def fix_field_issues(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    # 将各卡片用包含准确目标锚点的 <a> 链接包裹，提供 hover 效果
    # FL-01 -> locks/us-single-cylinder-deadbolt.html
    # FL-02 -> locks/bricard-bloctout.html
    # FL-03 -> categories/sea.html
    # FL-04 -> locks/lockwood-001.html
    # FL-05 -> categories/europe5.html
    # FL-06 -> categories/latam.html
    # FL-07 -> categories/gcc.html
    link_map = {
        'FL-01': '/zh/locks/us-single-cylinder-deadbolt.html' if 'zh' in path else '/en/locks/us-single-cylinder-deadbolt.html',
        'FL-02': '/zh/locks/bricard-bloctout.html' if 'zh' in path else '/en/locks/bricard-bloctout.html',
        'FL-03': '/zh/categories/sea.html' if 'zh' in path else '/en/categories/sea.html',
        'FL-04': '/zh/locks/lockwood-001.html' if 'zh' in path else '/en/locks/lockwood-001.html',
        'FL-05': '/zh/categories/europe5.html' if 'zh' in path else '/en/categories/europe5.html',
        'FL-06': '/zh/categories/latam.html' if 'zh' in path else '/en/categories/latam.html',
        'FL-07': '/zh/categories/gcc.html' if 'zh' in path else '/en/categories/gcc.html'
    }

    # 替换 FL-03 图片为完全居中 contain / cover 修复左侧黑块
    t = t.replace('alt="双门极限净距撞击" style="width: 100%; height: 100%; object-fit: cover;"',
                  'alt="双门极限净距撞击" style="width: 100%; height: 100%; object-fit: cover; object-position: center;"')
    
    # 在卡片内添加底部的明确点击交互链接
    for fl_id, target in link_map.items():
        old_pattern = f'({fl_id} · [^<]+</span>)'
        # 我们在标题上添加超链接
        t = re.sub(
            rf'<h3 style="margin: 0 0 8px; font-size: 1\.05rem;">({fl_id}[^<]+)</h3>',
            rf'<h3 style="margin: 0 0 8px; font-size: 1.05rem;"><a href="{target}" style="color: #0f172a; text-decoration: none;">\1</a></h3>',
            t
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Added clickable titles to {path}!")

fix_field_issues('content/pages/zh/field-issues.md')
fix_field_issues('content/pages/en/field-issues.md')

# 2. 修复 adapters.md 点击穿透
def fix_adapters_clickable(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    adapter_links = {
        'ADP-04': '/zh/locks/us-single-cylinder-deadbolt.html' if 'zh' in path else '/en/locks/us-single-cylinder-deadbolt.html',
        'ADP-06': '/zh/locks/bricard-bloctout.html' if 'zh' in path else '/en/locks/bricard-bloctout.html',
        'ADP-03': '/zh/locks/jp-miwa-case.html' if 'zh' in path else '/en/locks/jp-miwa-case.html',
        'ADP-07': '/zh/locks/us-single-cylinder-deadbolt.html' if 'zh' in path else '/en/locks/us-single-cylinder-deadbolt.html',
        'ADP-05': '/zh/locks/lockwood-001.html' if 'zh' in path else '/en/locks/lockwood-001.html',
        'ADP-01': '/zh/categories/europe5.html' if 'zh' in path else '/en/categories/europe5.html',
        'ADP-02': '/zh/categories/europe5.html' if 'zh' in path else '/en/categories/europe5.html',
        'ADP-08': '/zh/categories/latam.html' if 'zh' in path else '/en/categories/latam.html',
        'ADP-11': '/zh/categories/gcc.html' if 'zh' in path else '/en/categories/gcc.html',
        'ADP-12': '/zh/categories/sea.html' if 'zh' in path else '/en/categories/sea.html',
        'ADP-10': '/zh/locks/lockwood-001.html' if 'zh' in path else '/en/locks/lockwood-001.html',
        'ADP-09': '/zh/categories/europe5.html' if 'zh' in path else '/en/categories/europe5.html'
    }

    for adp_id, target in adapter_links.items():
        # 给标题添加可点击超链接
        t = re.sub(
            rf'<h3 style="margin: 0 0 8px; font-size: 1\.05rem; color: #0f172a;">([^<]*?{adp_id}[^<]*?)</h3>',
            rf'<h3 style="margin: 0 0 8px; font-size: 1.05rem; color: #0f172a;"><a href="{target}" style="color: inherit; text-decoration: none;">\1</a></h3>',
            t
        )
        # 如果标题没有匹配上，则匹配常规标题
        t = re.sub(
            rf'(<div class="gallery-card" id="{adp_id.lower()}".*?<h3[^>]*>)(.*?)(</h3>)',
            rf'\1<a href="{target}" style="color: inherit; text-decoration: none;">\2</a>\3',
            t, flags=re.DOTALL
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Added clickable links to {path}!")

fix_adapters_clickable('content/pages/zh/adapters.md')
fix_adapters_clickable('content/pages/en/adapters.md')

