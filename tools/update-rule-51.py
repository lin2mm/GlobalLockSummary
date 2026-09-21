# -*- coding: utf-8 -*-

rule_51_silent = """| **51** | 静默纯后台访客记录铁律（公网前端绝对隐形） | 1. **严禁前端向访客展示任何访问量数字**：遵照用户铁律，彻底拔除前端页面底部任何可见的浏览量、访客数文本及显示容器，保持 ASSA ABLOY 工业克制通透；<br>2. **纯后台无感静默统计机制**：访客记录全部交由 **Cloudflare Pages 原生 Web Analytics 后台** 承载，仅管理员登录控制台可见每日/每周访问趋势、国家分布及具体锁型阅读量；<br>3. **测试防线验证**：全站 229 页保持 100% 干净通透与零外部可见小部件干扰。 | `src/layout.mjs`, `docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md` |"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

# 替换规则 51
import re
text = re.sub(r'\|\s*\*\*51\*\*\s*\|[^\n]*\n', rule_51_silent + '\n', text)

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated rule 51 in docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
