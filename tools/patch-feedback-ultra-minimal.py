with open('src/layout.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 极致单行极简反馈条：一行内整合 [💬 标签 + 单行输入框 + 快速提交/复制按钮]
old_feedback_start = '  const feedback = `<section class="feedback"'
old_feedback_end = '  </section>`;'

idx1 = code.find(old_feedback_start)
idx2 = code.find(old_feedback_end, idx1)

if idx1 != -1 and idx2 != -1:
    idx2 += len(old_feedback_end)
    new_feedback = """  const isZh = lang === 'zh';
  const feedback = `<section class="feedback feedback--ultra-compact" id="feedback" data-feedback
    data-page-title="${esc(title)}" data-page-path="${esc(path)}" data-issues-url="${esc(site.urls.issues)}"
    data-i18n='${feedbackData}'>
    <div style="display: flex; gap: 10px; align-items: center; width: 100%; max-width: 960px; margin: 0 auto; flex-wrap: wrap;">
      <span style="font-size: 0.82rem; font-weight: 700; color: #475569; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
        💬 ${isZh ? '反馈 / 缺数据' : 'Feedback / Missing Spec'}:
      </span>
      <input type="text" data-feedback-message placeholder="${isZh ? '一句话留言：如缺某种锁型、尺寸纠错或加装建议...' : 'One-line note: missing lock, sizing correction, or advice...'}" 
        style="flex: 1; min-width: 220px; padding: 7px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.82rem; background: #fff;" />
      <button class="feedback__copy" data-feedback-copy type="button" style="padding: 7px 14px; font-size: 0.8rem; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; white-space: nowrap; font-weight: 600; color: #334155;">
        ${esc(feedbackI18n.copy)}
      </button>
      <a class="feedback__issue" data-feedback-issue href="${esc(site.urls.issues)}/new" target="_blank" rel="noopener" style="padding: 7px 14px; font-size: 0.8rem; background: #2563eb; color: #fff; border-radius: 6px; text-decoration: none; white-space: nowrap; font-weight: 600;">
        GitHub Issue
      </a>
      <span class="feedback__status" data-feedback-status aria-live="polite" style="font-size: 0.78rem;"></span>
    </div>
  </section>`;"""
    code = code[:idx1] + new_feedback + code[idx2:]
    with open('src/layout.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced feedback with ultra-compact single line strip!")
else:
    print("Could not find feedback snippet in src/layout.mjs")

