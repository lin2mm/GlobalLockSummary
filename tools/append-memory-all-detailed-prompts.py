with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'a', encoding='utf-8') as f:
    f.write("""
### 专项记忆复盘：历史所有关于「底部输入框/反馈表单简化」的指示与演进复盘

在过往沟通中，关于底部反馈输入框经历了以下 **3 次演进与指令历史**：

1. **第 1 次指示（建立免登录通道）**：
   - *用户原话诉求*：国内工程师往往没有 GitHub 账号或无法顺畅访问，需要站内直接留资/纠错的极简通道。
   - *响应动作*：在全站底部部署基于 Cloudflare Pages Functions 的 `/api/feedback`，提供无需 GitHub 的直接提交，配有分类下拉与留言框。
2. **第 2 次指示（极简单行输入）**：
   - *用户原话诉求*：“底部沟通表单极简单行输入，不堆砌杂乱元素”。
   - *演进偏差反思*：此前仅将 `<textarea>` 简单换为 `<input type="text">`，但仍然保留了上方的“工程师反馈（免登录）”大标题、描述副标、分类选择下拉框与底部提示文字，整体在屏幕上仍占据了 4 行高度，依然显得不够“极致单行”。
3. **第 3 次彻底根治与长期固化（本次彻底收敛）**：
   - *彻底重构*：将整个底部反馈区彻底压缩为**纯粹的单行浮动条（Ultra-Compact Single Line Bar）**：
     `[ 💬 反馈/缺数据: ] [ 单行输入框 (占满剩余宽度) ] [ 复制反馈 ] [ GitHub Issue ]`
   - *视觉减负*：彻底剔除一切繁冗的“大标题”、“提示段落”、“分类下拉选框”和“底部备注”，实现真正物理意义上的 **1 像素级极简单行条**。

| **18** | 专利图谱实装与命名红线坚守 | 专利规避页严禁出现 Nuki-Like 提法，统一使用「后装智能锁」；在各规避章节下方挂载 1:1 矢量 SVG 专利权利要求对比工程图（如 3 螺钉点压 vs 柔性夹头、弹性夹爪 vs Oldham 十字滑块）。 | `assets/img/patent/`, `content/pages/zh/patent-avoidance.md` |
| **19** | 底部反馈单行条铁律固化 | 底部反馈必须且仅能以单行条（Single Line Strip）形式存在，严禁衍生出多行表单、标题或大段文本。 | `src/layout.mjs`, `assets/css/site.css` |
""")

print("Appended detailed memory review to docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
