with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 替换 input name="来源页面"
# 原先：<input type="hidden" name="来源页面" value="${esc(path)} (${esc(title)})" />
# 升级：直接生成全球线上可点击的绝对公网 URL (支持 Cloudflare 与 GitHub Pages)，并同时把 URL 传给 FormSubmit
# 同时按钮样式收敛为 ASSA ABLOY 墨黑极简工业按钮 #0B1D47

old_form_snippet = """      <input type="hidden" name="_subject" value="【GlobalLockSummary 工程师直接反馈】${esc(title)}" />
      <input type="hidden" name="_captcha" value="false" />
      <input type="hidden" name="_template" value="table" />
      <input type="hidden" name="来源页面" value="${esc(path)} (${esc(title)})" />
      <span style="font-size: 0.82rem; font-weight: 700; color: #475569; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
        💬 ${isZh ? '反馈' : 'Feedback'}:
      </span>
      <input type="text" name="反馈内容" required placeholder="${isZh ? '一句话写下缺失锁型、尺寸纠错或建议（回车直接发送至维护邮箱）...' : 'Type note or missing spec here (hit Enter to send directly)...'}" 
        style="flex: 1; min-width: 220px; padding: 7px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.82rem; background: #fff;" />
      <button type="submit" style="padding: 7px 18px; font-size: 0.82rem; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; white-space: nowrap; font-weight: 600; box-shadow: 0 1px 3px rgba(37,99,235,0.2);">
        ${isZh ? '直接提交' : 'Submit'}
      </button>"""

new_form_snippet = """      <input type="hidden" name="_subject" value="【GlobalLockSummary 工程师直接反馈】${esc(title)}" />
      <input type="hidden" name="_captcha" value="false" />
      <input type="hidden" name="_template" value="table" />
      <!-- 包含公网 1 键直达链接，邮件中点击直接跳入具体子页面第几层 -->
      <input type="hidden" name="来源子页面直达链接 (Clickable URL)" value="https://globallocksummary.pages.dev/${esc(path.replace(/^\\//, ''))}" />
      <input type="hidden" name="页面标题与层级" value="${esc(title)} [${esc(path)}]" />
      <span style="font-size: 0.82rem; font-weight: 700; color: #0B1D47; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
        💬 ${isZh ? '工程师直通反馈' : 'Feedback'}:
      </span>
      <input type="text" name="反馈建议与纠错内容" required placeholder="${isZh ? '写下锁型补充、尺寸纠错或建议（回车直达邮箱，自动附带本页直达链接）...' : 'Type note or missing spec (hit Enter to send, page URL auto-attached)...'}" 
        style="flex: 1; min-width: 220px; padding: 7px 12px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.82rem; background: #fff;" />
      <button type="submit" style="padding: 7px 18px; font-size: 0.82rem; background: #0B1D47; color: #fff; border: 1px solid #0B1D47; border-radius: 4px; cursor: pointer; white-space: nowrap; font-weight: 600;">
        ${isZh ? '直接提交' : 'Submit'}
      </button>"""

if old_form_snippet in code:
    code = code.replace(old_form_snippet, new_form_snippet)
    print("Updated feedback form in src/layout.mjs with direct clickable URL!")
else:
    print("old_form_snippet not found in src/layout.mjs")

with open('src/layout.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

