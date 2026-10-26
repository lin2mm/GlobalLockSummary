with open('build.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 工业索引由 6 升级为 8 大工业板块联动
old_index_nav = """    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (全动态 6)
      label = `${rawLabel} (${indexCount})`;"""

new_index_nav = """    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (全动态 8 大工业体系)
      label = `${rawLabel} (${indexCount})`;"""

code = code.replace("let indexCount = 6;", "let indexCount = 8;")
if old_index_nav in code:
    code = code.replace(old_index_nav, new_index_nav)

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated index counter to 8!")
