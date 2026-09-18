with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
| **21** | ASSA ABLOY 极简工业克制风排版定论 | 摒弃过度渐变与大阴影，注意力体系全面收敛为 ASSA ABLOY 经典工业五金风（纯白底色、墨黑细线 #0f172a、低饱和度单色徽章、极度精简说明文本），实现少即是多。 | `assets/css/site.css`, `build.mjs` |
| **22** | 彻底移除 GitHub 提交按钮，国内网络 100% 畅通闭环 | 底部反馈条彻底移除打不开的 GitHub Issue 链接，收敛为极简单行「一键复制反馈 (微信/邮件/群)」，国内工程师秒点秒发。 | `src/layout.mjs` |
""")

with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'a', encoding='utf-8') as f:
    f.write("""
---

## 八、 ASSA ABLOY 极简工业风格与注意力降噪结合准则（ASSA ABLOY Minimalist Industrial Aesthetics）

### 1. 为什么工业硬件站点容易“越改越花哨”？
* **认知陷阱**：设计人员往往试图用鲜艳的色彩、渐变色块、浮动卡片和长篇大论去强化重要性，结果导致全屏都是“重点”，满眼都是文字噪声；
* **ASSA ABLOY 经典工业哲学**：
  - **墨黑与极简线条（Solid Charcoal & Clean Borders）**：以 `#0f172a`（深墨冷灰）作为基准强调色，而非刺眼的纯高亮蓝；
  - **白底高透气度（Negative Space）**：大量保留内边距与呼吸感，去除多余的装饰背景；
  - **单行化与标签化（Tag over Prose）**：用 2~4 个字的紧凑标签（如 `★ 核心基准`、`54mm 孔`）代替长句，让工程师眼球快速捕捉参数。

### 2. 极致简化的本地沟通闭环（No External Blocker）
* 严禁在面向国内或多地域工程师的沟通工具中预设“必须访问 GitHub / Google / 海外特定域名”的前提；
* 必须提供“单行输入 + 一键复制到系统剪贴板”的零阻碍通道，支持通过微信、企业微信、飞书或邮件直接转发。
""")

print("Appended wrap-up chapters to memory and methodology!")
