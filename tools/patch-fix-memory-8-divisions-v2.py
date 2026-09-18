with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("## 二、全球锁 5 大标准工业板块", "## 二、全球锁 8 大工业板块（4列 × 2行 黄金对称阵列）")
text = text.replace("5 大主入口图片质感重评与替换", "8 大工业板块主入口图片质感重评与替换")
text = text.replace("首页仅保留 5 个区域入口", "首页仅保留 8 个区域入口（4列 × 2行 黄金对称）")
text = text.replace("全球5大版本 32一直没变", "全球工业板块由前期 5 大扩充为标准 8 大工业板块")

with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned up remaining 5-division mentions in docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md")
