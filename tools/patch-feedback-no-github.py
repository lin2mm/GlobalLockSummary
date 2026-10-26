with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 彻底移除 GitHub Issue 按钮，实现 [💬 反馈/缺数据: ] [单行输入框] [一键复制发送 (微信/邮件/群)]
old_snippet = """      <a class="feedback__issue" data-feedback-issue href="${esc(site.urls.issues)}/new" target="_blank" rel="noopener" style="padding: 7px 14px; font-size: 0.8rem; background: #2563eb; color: #fff; border-radius: 6px; text-decoration: none; white-space: nowrap; font-weight: 600;">
        GitHub Issue
      </a>"""

new_copy_button = """<button class="feedback__copy" data-feedback-copy type="button" style="padding: 7px 16px; font-size: 0.82rem; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; white-space: nowrap; font-weight: 600; box-shadow: 0 1px 3px rgba(37,99,235,0.2);">
        ${isZh ? '一键复制反馈 (微信/邮件)' : 'Copy Feedback'}
      </button>"""

if old_snippet in code:
    code = code.replace(old_snippet, "")
    code = code.replace('<button class="feedback__copy" data-feedback-copy type="button" style="padding: 7px 14px; font-size: 0.8rem; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; white-space: nowrap; font-weight: 600; color: #334155;">\n        ${esc(feedbackI18n.copy)}\n      </button>', new_copy_button)
    with open('src/layout.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Cleaned up GitHub button and streamlined to 1-click copy in src/layout.mjs!")
else:
    print("old_snippet not found in layout.mjs")

