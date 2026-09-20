# -*- coding: utf-8 -*-
import re

# 1. 修订 content/pages/zh/field-issues.md 与 content/pages/en/field-issues.md
# 为每个避坑工单卡片添加整体整卡可点击包装或图片与标题直达对应锁族详情页
mapping_zh = {
    "FL-01": "/zh/locks/us-deadbolt.html",
    "FL-02": "/zh/locks/euro-cylinder-mortise.html",
    "FL-03": "/zh/locks/sea-multipoint.html",
    "FL-04": "/zh/locks/au-rim-nightlatch.html",
    "FL-05": "/zh/locks/latam-narrow-profile.html",
    "FL-06": "/zh/locks/gcc-heavy-mortise.html"
}
mapping_en = {
    "FL-01": "/en/locks/us-deadbolt.html",
    "FL-02": "/en/locks/euro-cylinder-mortise.html",
    "FL-03": "/en/locks/sea-multipoint.html",
    "FL-04": "/en/locks/au-rim-nightlatch.html",
    "FL-05": "/en/locks/latam-narrow-profile.html",
    "FL-06": "/en/locks/gcc-heavy-mortise.html"
}

with open("content/pages/zh/field-issues.md", "r", encoding="utf-8") as f:
    text_zh = f.read()

# 对每个卡片，将图片和标题包装可点击直达目标锁族
for fl_id, target_url in mapping_zh.items():
    # 替换包含该 FL 标牌的卡片中的图片和标题
    # 例如：<div class="gallery-card" ... <span ...>FL-01
    pattern = rf'(<div class="gallery-card"[^>]*>[\s\S]*?<span[^>]*>{fl_id}[^<]*</span>[\s\S]*?</div>\s*<div style="padding: 12px 14px;">\s*<h3[^>]*>)(.*?)(</h3>)'
    m = re.search(pattern, text_zh)
    if m:
        # 给图片包裹链接
        img_wrap_pat = rf'(<div class="gallery-card"[^>]*>[\s\S]*?<div style="height: 140px;[^"]*"[^>]*>)([\s\S]*?<img [^>]*>)([\s\S]*?</div>\s*<div style="padding: 12px 14px;">\s*<h3[^>]*>)(.*?)(</h3>)'
        def repl(match):
            prefix = match.group(1)
            img = match.group(2)
            mid = match.group(3)
            title = match.group(4)
            suffix = match.group(5)
            # 如果标题还没链接
            if '<a href=' not in title:
                title = f'<a href="{target_url}" style="color: inherit; text-decoration: none;">{title}</a>'
            # 如果图片还没链接
            if '<a href=' not in img:
                img = f'<a href="{target_url}" style="display: block; width: 100%; height: 100%;">{img}</a>'
            return f'{prefix}{img}{mid}{title}{suffix}'
        text_zh = re.sub(img_wrap_pat, repl, text_zh, count=1)

with open("content/pages/zh/field-issues.md", "w", encoding="utf-8") as f:
    f.write(text_zh)

with open("content/pages/en/field-issues.md", "r", encoding="utf-8") as f:
    text_en = f.read()

for fl_id, target_url in mapping_en.items():
    img_wrap_pat = rf'(<div class="gallery-card"[^>]*>[\s\S]*?<div style="height: 140px;[^"]*"[^>]*>)([\s\S]*?<img [^>]*>)([\s\S]*?</div>\s*<div style="padding: 12px 14px;">\s*<h3[^>]*>)(.*?)(</h3>)'
    def repl(match):
        prefix = match.group(1)
        img = match.group(2)
        mid = match.group(3)
        title = match.group(4)
        suffix = match.group(5)
        if '<a href=' not in title:
            title = f'<a href="{target_url}" style="color: inherit; text-decoration: none;">{title}</a>'
        if '<a href=' not in img:
            img = f'<a href="{target_url}" style="display: block; width: 100%; height: 100%;">{img}</a>'
        return f'{prefix}{img}{mid}{title}{suffix}'
    text_en = re.sub(img_wrap_pat, repl, text_en, count=1)

with open("content/pages/en/field-issues.md", "w", encoding="utf-8") as f:
    f.write(text_en)

print("Updated field-issues.md (zh & en) with clickable image & title links to lock family detail pages.")
