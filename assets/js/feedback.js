/* Per-page engineer feedback:
 * 1. Supports one-click in-site submission without GitHub via /api/feedback (Cloudflare Pages Functions).
 * 2. Returns ticket ID upon success.
 * 3. Gracefully falls back to local clipboard copy and optional GitHub Issue prefill.
 * 4. Never exposes API keys or secrets in client code.
 */
(function () {
  'use strict';

  function issueUrl(issuesUrl, title, pagePath, category, message, contact) {
    var body = [
      'Page: ' + pagePath,
      'Category: ' + category,
      contact ? ('Contact: ' + contact) : '',
      '',
      message,
    ].filter(Boolean).join('\n');
    return issuesUrl.replace(/\/$/, '') + '/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  }

  function reportText(title, pagePath, category, message, contact) {
    return [
      title,
      'Page: ' + pagePath,
      'Category: ' + category,
      contact ? ('Contact: ' + contact) : '',
      '',
      message,
    ].filter(Boolean).join('\n');
  }

  function init(root) {
    var i18n;
    try { i18n = JSON.parse(root.getAttribute('data-i18n') || '{}'); } catch (_) { i18n = {}; }
    var categories = i18n.categories || {};
    var select = root.querySelector('[data-feedback-category]');
    var textarea = root.querySelector('[data-feedback-message]');
    var contactInput = root.querySelector('[data-feedback-contact]');
    var submitBtn = root.querySelector('[data-feedback-submit]');
    var issue = root.querySelector('[data-feedback-issue]');
    var copy = root.querySelector('[data-feedback-copy]');
    var status = root.querySelector('[data-feedback-status]');
    var pageTitle = root.getAttribute('data-page-title') || document.title;
    var pagePath = root.getAttribute('data-page-path') || location.pathname;
    var issuesUrl = root.getAttribute('data-issues-url') || '';

    // Populate category dropdown
    if (select && select.children.length === 0) {
      Object.keys(categories).forEach(function (key) {
        var option = document.createElement('option');
        option.value = key;
        option.textContent = categories[key];
        select.appendChild(option);
      });
    }

    function values() {
      var category = (select && select.value) || Object.keys(categories)[0] || 'other';
      var message = (textarea && textarea.value ? textarea.value.trim() : '');
      var contact = (contactInput && contactInput.value ? contactInput.value.trim() : '');
      return { category: category, message: message, contact: contact };
    }

    function update() {
      var valuesNow = values();
      if (issue) {
        issue.href = issueUrl(
          issuesUrl,
          pageTitle + ' — ' + (categories[valuesNow.category] || valuesNow.category),
          pagePath,
          categories[valuesNow.category] || valuesNow.category,
          valuesNow.message,
          valuesNow.contact
        );
      }
    }

    if (select) select.addEventListener('change', update);
    if (textarea) textarea.addEventListener('input', update);
    if (contactInput) contactInput.addEventListener('input', update);

    // In-site direct submission
    if (submitBtn) {
      submitBtn.addEventListener('click', function () {
        var vals = values();
        if (!vals.message || vals.message.length < 3) {
          if (status) {
            status.textContent = i18n.tooShort || (document.documentElement.lang === 'zh' ? '请至少输入3个字' : 'Please enter at least 3 characters');
            status.className = 'feedback__status feedback__status--err';
          }
          if (textarea) textarea.focus();
          return;
        }

        submitBtn.disabled = true;
        if (status) {
          status.textContent = i18n.submitting || (document.documentElement.lang === 'zh' ? '正在提交...' : 'Submitting...');
          status.className = 'feedback__status';
        }

        fetch('/api/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            category: categories[vals.category] || vals.category,
            message: vals.message,
            contact: vals.contact,
            pageTitle: pageTitle,
            pagePath: pagePath
          })
        })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (data) {
          submitBtn.disabled = false;
          if (status) {
            var succMsg = i18n.submitted || (document.documentElement.lang === 'zh' ? '提交成功！反馈编号：' : 'Feedback submitted! ID: ');
            status.textContent = succMsg + (data.id || '');
            status.className = 'feedback__status feedback__status--ok';
          }
          if (textarea) textarea.value = '';
          update();
        })
        .catch(function (err) {
          submitBtn.disabled = false;
          if (status) {
            var failMsg = i18n.submitFailed || (document.documentElement.lang === 'zh' ? '站内接口未响应，可点击右侧“复制反馈”通过微信/邮件转发' : 'API unavailable. You can click Copy Feedback below.');
            status.textContent = failMsg;
            status.className = 'feedback__status feedback__status--err';
          }
        });
      });
    }

    // Local copy to clipboard
    if (copy) {
      copy.addEventListener('click', function () {
        var valuesNow = values();
        var text = reportText(
          pageTitle,
          pagePath,
          categories[valuesNow.category] || valuesNow.category,
          valuesNow.message,
          valuesNow.contact
        );
        var done = function () {
          if (status) {
            status.textContent = i18n.copied || 'Copied';
            status.className = 'feedback__status feedback__status--ok';
          }
          copy.setAttribute('aria-label', i18n.copied || 'Copied');
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done);
        } else {
          var input = document.createElement('textarea');
          input.value = text;
          document.body.appendChild(input);
          input.select();
          document.execCommand('copy');
          input.remove();
          done();
        }
      });
    }

    update();
  }

  if (typeof window !== 'undefined') {
    window.GlobalLockFeedback = { issueUrl: issueUrl, reportText: reportText, init: init };
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('[data-feedback]').forEach(init);
    });
  }
}());
