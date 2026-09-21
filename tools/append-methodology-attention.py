with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'r', encoding='utf-8') as f:
    methodology = f.read()

attention_chapter = """
---

## 七、 页面视觉注意力体系与信息聚焦模型（Visual Attention Hierarchy & Progressive Disclosure）

出海工程站点的核心矛盾在于：**硬件工程参数极度冗长硬核（极客维度），但访客或硬件 PM 停留时间极短、认知带宽有限**。
必须建立一套**「视觉注意力三级调光体系」与「渐进式暴露模型」**，让人在 3 秒内看清该看什么、忽略什么。

### 1. 业界标杆设计系统的降噪与聚焦启示（Benchmark Learning Summary）
通过拆解 Apple Developer Design Guidelines、Stripe 开发者文档与 Linear 设计哲学，总结出 4 条核心原则：
1. **F 型与 Z 型视觉着陆锚点（Visual Landing Strip）**：人眼浏览网页首要抓取具有强色彩对比的“视觉锚点”（Visual Anchors），其余区域自动视为背景噪声；
2. **色度与饱和度调光（Chroma De-emphasis）**：非核心模块不应争抢主色调。采用 `grayscale(15~20%)` + 浅灰色背景（#f8fafc）+ 低阴影，形成自然的“景深后退感”；
3. **关键数据 3 秒定律（The 3-Second Metric）**：重要工程结论（如“★ 核心加装基准”、“⚠️ 致命反锁风险”）必须采用独立浮动胶囊 Badge 呈现在卡片左上角，禁止埋藏在段落正文中；
4. **渐进式暴露（Progressive Disclosure）**：
   - **第一眼（L1 显式）**：实物照片、区域标准名、一句话核心避坑定论；
   - **交互悬浮（L2 聚焦）**：鼠标移入时次要板块恢复 100% 饱和度并微微上浮，提供探索奖励；
   - **点击深挖（L3 穿透）**：进入详情页后再展开 5 维详细开模公差、电路电流与开孔打孔纸样。

### 2. 全站 8 大工业板块注意力色系落地规范
* **Tier 1 核心加装基准（北美 ANSI、欧陆 DIN、英澳 AS/BS）**：
  - *视觉处理*：高饱和工业湛蓝（#2563eb）1.5px 边框、8px 弥散主阴影、左上角常驻渐变蓝底白字 `★ 核心加装基准` 徽章，缩放比例 1.01，形成前突聚焦。
* **Tier 2 次要与新兴板块（拉美 ABNT、中东 SASO、日韩 JIS、东南亚 SS、非南亚 BIS）**：
  - *视觉处理*：柔和浅灰背景（#f8fafc）、1px 细淡线（#e2e8f0）、静态图片微灰阶滤波（`filter: grayscale(18%)`），透明度 0.88。鼠标悬浮即刻唤醒为 100% 真实色彩。
"""

if "页面视觉注意力体系与信息聚焦模型" not in methodology:
    methodology = methodology + "\n" + attention_chapter
    with open('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', 'w', encoding='utf-8') as f:
        f.write(methodology)
    print("Added attention hierarchy chapter to docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md")

