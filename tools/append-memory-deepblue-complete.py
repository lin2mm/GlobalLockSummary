with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **31** | ASSA ABLOY Deep Blue (#0B1D47) 全站像素级统一落地 | 1. **全网去鲜艳蓝换装 Deep Blue**：全量清除全站历史 `#0284c7` 与 `#0b5fff` 鲜艳蓝色代码，统一收敛为 ASSA ABLOY 官方核心标志色 **`#0B1D47`** 与冷墨灰 **`#0f172a`**；<br>2. **卡片微参数表结构化**：锁型卡片、转接五金卡片、工程案例卡片彻底告别彩色粗框与高饱和发光阴影，全部统一度量衡为 `1px solid #cbd5e1` 浅灰边框 + `3px solid #0B1D47` 墨黑深蓝基准线；<br>3. **全站 100% 自动化测试通过**：动态计数与反向退化断言持续保持满分绿灯。 | `assets/css/site.css`, `build.mjs`, `content/pages/` |
""")

print("Appended batch 31 to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
