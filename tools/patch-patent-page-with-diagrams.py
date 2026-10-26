with open('content/pages/zh/patent-avoidance.md', 'r', encoding='utf-8') as f:
    zh = f.read()

# 替换所有 Nuki-Like 为 后装智能锁
zh = zh.replace("Nuki-Like 智能锁专利壁垒排查与海外规避设计指南", "后装智能锁专利壁垒排查与海外规避设计指南 (Patent FTO)")
zh = zh.replace("Nuki-Like 智能锁专利壁垒与海外规避设计", "后装智能锁专利壁垒与海外规避设计 (Patent FTO Guide)")
zh = zh.replace("以 Nuki、August、SwitchBot、Tedee 为代表的**免换锁加装（Retrofit）智能锁**", "以欧美主流后装为代表的**后装智能锁（免换锁 / 租客无损加装）**")

# 插入对比图
fig_clamping = """
  <!-- 1:1 专利权同等对比图 -->
  <div style="margin: 16px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="/assets/img/patent/patent-clamping-comparison.svg" alt="锁芯夹持专利对比图" style="width: 100%; height: auto; display: block;" />
  </div>
"""

fig_oldham = """
  <!-- 钥匙柄耦合与 Oldham 浮动拨叉对比图 -->
  <div style="margin: 16px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="/assets/img/patent/patent-oldham-coupling-comparison.svg" alt="Oldham 十字滑块浮动规避专利对比图" style="width: 100%; height: auto; display: block;" />
  </div>
"""

if 'patent-clamping-comparison.svg' not in zh:
    zh = zh.replace('</div>\n\n---\n\n### 2.', fig_clamping + '\n</div>\n\n---\n\n### 2.')

if 'patent-oldham-coupling-comparison.svg' not in zh:
    zh = zh.replace('</div>\n\n---\n\n### 3.', fig_oldham + '\n</div>\n\n---\n\n### 3.')

with open('content/pages/zh/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(zh)
print("Updated zh/patent-avoidance.md with patent diagrams and standardised terminology!")

# 更新英文版
with open('content/pages/en/patent-avoidance.md', 'r', encoding='utf-8') as f:
    en = f.read()

en = en.replace("Nuki-Like Smart Lock Patent Avoidance", "Retrofit Smart Lock Patent Avoidance & FTO Guide")
en = en.replace("Nuki-Like", "Retrofit Smart Lock")

if 'patent-clamping-comparison.svg' not in en:
    en = en.replace('</div>\n\n### 2.', fig_clamping + '\n</div>\n\n### 2.')

if 'patent-oldham-coupling-comparison.svg' not in en:
    en = en.replace('</div>\n\n### 3.', fig_oldham + '\n</div>\n\n### 3.')

with open('content/pages/en/patent-avoidance.md', 'w', encoding='utf-8') as f:
    f.write(en)
print("Updated en/patent-avoidance.md with patent diagrams!")

