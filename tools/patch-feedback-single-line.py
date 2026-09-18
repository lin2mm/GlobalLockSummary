with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    layout = f.read()

# 查找 feedback form 的 HTML 结构
print("Feedback textarea in layout:", "textarea" in layout)
