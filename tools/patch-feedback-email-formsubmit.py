import json

# 1. 更新 src/layout.mjs 中的 feedback 结构：采用 FormSubmit.co 真正 0 门槛直发 438068235@qq.com
with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

old_feedback_start = '  const isZh = lang === '
old_feedback_end = '  </section>`;'

idx1 = code.find(old_feedback_start)
idx2 = code.find(old_feedback_end, idx1)

if idx1 != -1 and idx2 != -1:
    idx2 += len(old_feedback_end)
    new_feedback = """  const isZh = lang === 'zh';
  const feedback = `<section class="feedback feedback--ultra-compact" id="feedback">
    <form class="feedback__one-click-form" action="https://formsubmit.co/438068235@qq.com" method="POST" style="display: flex; gap: 8px; align-items: center; width: 100%; max-width: 960px; margin: 0 auto; flex-wrap: wrap;">
      <input type="hidden" name="_subject" value="【GlobalLockSummary 工程师直接反馈】${esc(title)}" />
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
      </button>
    </form>
  </section>`;"""
    code = code[:idx1] + new_feedback + code[idx2:]
    with open('src/layout.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Patched layout.mjs with direct FormSubmit email action to 438068235@qq.com!")
else:
    print("Could not find feedback snippet in src/layout.mjs")

