import re

for lang in ['zh', 'en']:
    path = f'content/pages/{lang}/indigenous-guides.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. 在每个地区卡片容器上强化清晰的视觉分组
    text = text.replace(
        'style="display: flex; flex-direction: column; gap: 24px; margin: 24px 0;"',
        'style="display: flex; flex-direction: column; gap: 32px; margin: 28px 0;"'
    )
    # 2. 为每个板块卡片统一设定卡片式投影与内边距
    text = text.replace(
        'style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 5px solid #0284c7; border-radius: 8px; padding: 20px; box-shadow: 0 4px 12px rgba(2,132,199,0.06);"',
        'style="background: #ffffff; border: 1.5px solid #0284c7; border-left: 5px solid #0284c7; border-radius: 8px; padding: 24px; box-shadow: 0 4px 14px rgba(2,132,199,0.08);"'
    )
    # 3. 规范化图片容器高度为 240px 并保持 object-fit: contain/cover 优化
    text = text.replace('height: 220px;', 'height: 240px;')
    text = text.replace('height: 200px;', 'height: 240px;')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Polished indigenous-guides visual layout and image containers!")
