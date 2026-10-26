# -*- coding: utf-8 -*-

rule_51 = """
| **51** | 全球合规轻量访客记录与 Cloudflare Web Analytics 统计体系 | 1. **全站合规双轨访客记录**：在全站页脚标准集成无需翻墙、零 Cookie 隐私合规的实时访问计数器，自动呈现 `全站总浏览量 (PV)`、`独立访客数 (UV)` 与 `本页阅读量`；<br>2. **Cloudflare Pages 官方后台日志无缝贯通**：指导在 Cloudflare 控制台直接开启免费且免嵌代码的 Web Analytics 与 HTTP 访问日志，可随时按天、国家、操作系统查看详细的访客历史；<br>3. **测试防线协议断言**：外部统计脚本统一采用显式 `https://` 协议，杜绝协议相对路径引发的本地域探测误判。 | `src/layout.mjs`, `tests/site.test.mjs` |
"""

with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "r", encoding="utf-8") as f:
    text = f.read()

if "| **51** |" not in text:
    target = "| **50** | 画廊卡片信息极致降噪（单图+单标+双微标签）与多重重复按钮根治 | 1. **转接工具（adapters）文字极端减负 70%**：彻底拔除卡片内大段“关键公差与尺寸”、“推荐材质”、“3D打印适配”四行长文本，收敛为标准 ASSA ABLOY 工业结构：**140px 产品剖面图 + 极简标题 + 2 个微参数标签（`⌖ 关键公差` + `🔩 材质`）+ 底部单一直达链接**；<br>2. **避坑工单（field-issues）错位重复彻底根治**：根除了上轮脚本在卡片闭合处意外追加的双重文本与重复按钮（消除 `查看对应锁族图谱与公差 →` 双重错位重叠）；<br>3. **统一为 3 列黄金等高卡片流**：`adapters.html` 与 `field-issues.html` 全网统一采用 `grid-template-columns: repeat(3, 1fr)`，卡片高度完全齐平、内部留白透气，告别密集压迫感。 | `content/pages/zh/adapters.md`, `content/pages/en/adapters.md`, `content/pages/zh/field-issues.md`, `content/pages/en/field-issues.md` |"
    if target in text:
        text = text.replace(target, target + "\n" + rule_51.strip())
        with open("docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully appended rule 51 into docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
    else:
        print("Could not find exact rule 50.")
else:
    print("Rule 51 already present.")
