# -*- coding: utf-8 -*-
with open("src/layout.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 移除页脚中可见的 HTML 文本容器，仅保留静默统计探针或完全转为纯后台 Cloudflare Analytics
old_snippet = """    <div class="wrap site-footer__analytics" style="margin-top: 10px; font-size: 0.72rem; color: #94a3b8; display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
      <span id="busuanzi_container_site_pv" style="display: none;">
        📈 ${lang === 'zh' ? '全站总浏览量' : 'Total Views'}: <span id="busuanzi_value_site_pv" style="font-weight: 700; color: #cbd5e1;"></span>
      </span>
      <span id="busuanzi_container_site_uv" style="display: none;">
        👤 ${lang === 'zh' ? '独立访客数' : 'Total Visitors'}: <span id="busuanzi_value_site_uv" style="font-weight: 700; color: #cbd5e1;"></span>
      </span>
      <span id="busuanzi_container_page_pv" style="display: none;">
        📄 ${lang === 'zh' ? '本页阅读量' : 'Page Views'}: <span id="busuanzi_value_page_pv" style="font-weight: 700; color: #cbd5e1;"></span>
      </span>
    </div>
    <script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>"""

if old_snippet in code:
    code = code.replace(old_snippet + "\n    ", "")
    print("Completely removed visible visitor counter snippet from src/layout.mjs.")
else:
    # 尝试按行移除
    lines = code.split("\n")
    new_lines = []
    skip = False
    for line in lines:
        if 'site-footer__analytics' in line:
            skip = True
            continue
        if skip and 'busuanzi.pure.mini.js' in line:
            skip = False
            continue
        if not skip:
            new_lines.append(line)
    code = "\n".join(new_lines)
    print("Filtered out visitor counter from src/layout.mjs.")

with open("src/layout.mjs", "w", encoding="utf-8") as f:
    f.write(code)

