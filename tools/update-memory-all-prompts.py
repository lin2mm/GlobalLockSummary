with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **11** | 一键直接下载工作区沉淀文件 | 部署 `/assets/downloads/` 静态服务并在 Data Hub 提供点击直接下载 | `content/pages/zh/data-hub.md`, `assets/downloads/` |
| **12** | 增加 Nuki-Like 智能锁专利规避与出海 FTO 设计指南 | 建立专属导航菜单「专利规避 (Patent FTO)」与详尽规避技术路径 | `content/pages/zh/patent-avoidance.html`, `content/site.json` |
| **13** | 方法论扩充海外合规清单（GDPR / CCPA / SASO / FTO） | 在方法论中增补《第六章：海外多国家合规与数据安全合规清单》 | `docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md` |
""")

print("Updated docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md with batch 11-13")
