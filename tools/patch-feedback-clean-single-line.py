with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 替换 textarea 为紧凑单行 input
old_textarea = '<textarea data-feedback-message rows="5"></textarea>'
new_input = '<input type="text" data-feedback-message placeholder="选填/简述：如需补充某种锁型或尺寸纠错..." style="width: 100%; padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem;" />'

if old_textarea in code:
    code = code.replace(old_textarea, new_input)
    with open('src/layout.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced textarea with sleek single-line input in src/layout.mjs!")
else:
    print("Target old_textarea not found!")

