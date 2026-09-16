/* Per-page engineer feedback: everything stays in the browser until the visitor
 * explicitly opens GitHub or copies the report. No feedback is uploaded here. */
(function () {
  'use strict';

  function issueUrl(issuesUrl, title, pagePath, category, message) {
    var body = [
      'Page: ' + pagePath,
      'Category: ' + category,
      '',
      message,
    ].join('\n');
    return issuesUrl.replace(/\/$/, '') + '/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  }

  function reportText(title, pagePath, category, message) {
    return [
      title,
      'Page: ' + pagePath,
      'Category: ' + category,
      '',
      message,
    ].join('\n');
  }

  function init(root) {
    var i18n;
    try { i18n = JSON.parse(root.getAttribute('data-i18n') || '{}'); } catch (_) { i18n = {}; }
    var categories = i18n.categories || {};
    var select = root.querySelector('[data-feedback-category]');
    var textarea = root.querySelector('[data-feedback-message]');
    var issue = root.querySelector('[data-feedback-issue]');
    var copy = root.querySelector('[data-feedback-copy]');
    var status = root.querySelector('[data-feedback-status]');
    var pageTitle = root.getAttribute('data-page-title') || document.title;
    var pagePath = root.getAttribute('data-page-path') || location.pathname;
    var issuesUrl = root.getAttribute('data-issues-url') || '';

    Object.keys(categories).forEach(function (key) {
      var option = document.createElement('option');
      option.value = key;
      option.textContent = categories[key];
      select.appendChild(option);
    });

    function values() {
      var category = select.value || Object.keys(categories)[0] || 'other';
      var message = textarea.value.trim();
      return { category: category, message: message };
    }

    function update() {
      var valuesNow = values();
      issue.href = issueUrl(issuesUrl, pageTitle + ' — ' + (categories[valuesNow.category] || valuesNow.category), pagePath, categories[valuesNow.category] || valuesNow.category, valuesNow.message);
    }

    select.addEventListener('change', update);
    textarea.addEventListener('input', update);
    copy.addEventListener('click', function () {
      var valuesNow = values();
      var text = reportText(pageTitle, pagePath, categories[valuesNow.category] || valuesNow.category, valuesNow.message);
      var done = function () {
        status.textContent = i18n.copied || 'Copied';
        copy.setAttribute('aria-label', i18n.copied || 'Copied');
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done);
      else {
        var input = document.createElement('textarea');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        input.remove();
        done();
      }
    });
    update();
  }

  if (typeof window !== 'undefined') {
    window.GlobalLockFeedback = { issueUrl: issueUrl, reportText: reportText, init: init };
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('[data-feedback]').forEach(init);
    });
  }
}());
