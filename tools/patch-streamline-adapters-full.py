import re

def streamline_adapters(path):
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()

    # 1. 拔除黑色内衬，换为工业浅冷灰工程底
    t = t.replace('background: #0b1120;', 'background: #f8fafc;')
    t = t.replace('padding: 12px; background: #0f172a;', 'padding: 8px; background: #f8fafc;')

    # 2. 拔除长篇冗长的描述 <p>，转换为 ASSA ABLOY 紧凑微标签，消除贴片广告感
    # 将包含较长文本的 <p ...>...</p> 替换为更简明的单行技术说明或直接去除
    t = re.sub(
        r'<p style="font-size: 0\.82rem; color: #475569; line-height: 1\.45; margin: 0 0 8px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">.*?</p>',
        '',
        t
    )

    # 3. 简化尺寸与材质方框，消除厚重背景
    t = t.replace('background: #f8fafc; padding: 8px 10px; border-radius: 4px; font-size: 0.75rem; color: #334155; border-left: 3px solid #0f172a; margin-bottom: 8px;',
                  'padding: 4px 0; font-size: 0.75rem; color: #475569; border-top: 1px solid #f1f5f9; margin-bottom: 6px;')

    # 4. 消除底部杂乱的双重徽章条
    t = re.sub(
        r'<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0\.72rem; color: #64748b; border-top: 1px solid #f1f5f9; padding-top: 8px;">\s*<span>工件要求: <span style="background: #[0-9a-fA-F]+; color: #fff; font-size: 0\.65rem; font-weight: 600; padding: 2px 6px; border-radius: 3px;">(.*?)</span></span>\s*<span style="color: #475569; font-weight: 600;">(.*?)</span>\s*</div>',
        r'<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #64748b; padding-top: 4px;"><span>\1</span><span style="font-weight: 600; color: #0f172a;">\2</span></div>',
        t
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Streamlined {path} successfully!")

streamline_adapters('content/pages/zh/adapters.md')
streamline_adapters('content/pages/en/adapters.md')

