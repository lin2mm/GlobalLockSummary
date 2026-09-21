# -*- coding: utf-8 -*-
with open("src/layout.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 在页脚注入合规轻量的 Busuanzi 访客记录组件
busuanzi_snippet = """    <div class="wrap site-footer__analytics" style="margin-top: 10px; font-size: 0.72rem; color: #94a3b8; display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
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

target = '<div class="wrap site-footer__meta">'
if target in code and "busuanzi" not in code:
    code = code.replace(target, busuanzi_snippet + "\n    " + target)
    with open("src/layout.mjs", "w", encoding="utf-8") as f:
        f.write(code)
    print("Injected lightweight visitor counter into src/layout.mjs.")
else:
    print("Already injected or target not found.")
