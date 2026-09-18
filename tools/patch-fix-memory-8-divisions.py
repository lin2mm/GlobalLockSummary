with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'r', encoding='utf-8') as f:
    mem = f.read()

# 彻底全局替换历史残留的 5 大板块
mem = mem.replace("5 大板块", "8 大工业板块")
mem = mem.replace("5大板块", "8大工业板块")
mem = mem.replace("5 大工业板块", "8 大工业板块")
mem = mem.replace("5大工业板块", "8大工业板块")
mem = mem.replace("5 大区域", "8 大工业板块")
mem = mem.replace("5大区域", "8 大工业板块")

with open('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', 'w', encoding='utf-8') as f:
    f.write(mem)

print("Updated docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md globally to 8 industrial divisions!")
