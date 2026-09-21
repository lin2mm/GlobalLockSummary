import os

path = 'docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

rule_entry = """
### 42. 【根因分析与绝对防御机制】Cloudflare Pages 分支映射与工作区 Staged 差量防丢失铁律
- **事故回溯与真实根因（Post-Mortem）**：
  1. *真实映射链路*：用户在 Cloudflare Pages 后台将 Production Branch（或活跃构建分支）直接指定绑定了长期工作分支 `arena/01a0a966-globallocksummary`。因此每次只要该分支成功 push 且构建通过，`https://globallocksummary.pages.dev/zh/` 就会全量实时更新。
  2. *此前打不开/回退旧版的直接诱因*：在之前的某次提交中，`.github/workflows/pages.yml` 的触发分支被误设为单分支；更严重的是，沙箱在排查时产生了未提交的临时索引（Staged changes），覆盖了正在生效的 `build.mjs`。导致本地 build 降级，生成的 HTML 退化成了带占位符的旧骨架。
  3. *Cloudflare 构建阻塞*：由于工作流与脚本状态异常，远端未能收到正确编译出的最新静态页面，Cloudflare 抓取不到最新构建，回滚降级展示了上一版本的 404 与占位符。
- **永久防范三大防线（Triple Defense Mechanisms）**：
  - **防线一（Git 状态三不原则）**：在任何检查、测试与推送动作前，必须先执行 `git status --porcelain`。若存在未追踪或意外修改，严禁覆盖，必须使用 `git stash` 或显式恢复，坚决杜绝在 dirty working tree 下执行 build。
  - **防线二（构建产物完整性自检断言）**：在 `npm test` 中增加「核心模板与渲染标签自检」断言——严禁产出 HTML 包含未经解析的模板占位符（如 `{{gallery}}`）；一旦检测到，直接中断发布并警报。
  - **防线三（双端推送绝对保持）**：`.github/workflows/pages.yml` 中永远必须保留 `arena/01a0a966-globallocksummary` 触发分支，确保用户无论访问 Cloudflare CDN、Gitee 还是 GitHub Pages，三端始终由当前分支全自动驱动。
"""

if '42. 【根因分析与绝对防御机制】' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(rule_entry)
    print('Rule 42 successfully written.')
else:
    print('Rule 42 already present.')
