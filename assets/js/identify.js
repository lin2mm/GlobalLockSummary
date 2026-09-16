/**
 * Lock identification wizard.
 *
 * All data is inlined into the page at build time (data-questions, data-catalog),
 * so this works with no network requests and no backend — and a crawler reading
 * the raw HTML can still see the questions.
 */
(function () {
  'use strict';

  var root = document.getElementById('wizard');
  if (!root) return;

  var parse = function (name) {
    try { return JSON.parse(root.getAttribute(name) || '{}'); } catch (e) { return {}; }
  };

  var i18n = parse('data-i18n');
  var questions = parse('data-questions');
  var catalog = parse('data-catalog');
  var siteRoot = root.getAttribute('data-root') || '';
  var productUrl = root.getAttribute('data-product-url') || '';
  var productLabel = root.getAttribute('data-product-label') || '';

  /**
   * Link to the commercial retrofit product site, only when one is configured.
   * With no URL the section is not rendered at all — never an empty link.
   */
  function productSection() {
    if (!productUrl || !productLabel) return null;
    var wrap = el('div', 'result__section');
    var link = el('a', 'wizard__btn wizard__btn--primary', productLabel);
    link.href = productUrl;
    link.rel = 'external noopener';
    link.target = '_blank';
    wrap.appendChild(link);
    return wrap;
  }

  if (!questions.length) return;

  var inner = root.querySelector('.wizard__inner');
  var answers = [];
  var step = 0;
  var finished = false;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function statusBadge(status) {
    var b = el('span', 'badge badge--' + status);
    b.textContent = status === 'verified' ? '✓ ' + i18n.statusVerified : '⚠ ' + i18n.statusReview;
    return b;
  }

  function renderQuestion() {
    var q = questions[step];
    inner.innerHTML = '';

    var progressText = i18n.progress
      .replace('{n}', String(step + 1))
      .replace('{total}', String(questions.length));

    inner.appendChild(el('p', 'wizard__progress', progressText));

    var bar = el('div', 'wizard__bar');
    var fill = el('span');
    fill.style.width = Math.round((step / questions.length) * 100) + '%';
    bar.appendChild(fill);
    inner.appendChild(bar);

    inner.appendChild(el('h2', 'wizard__prompt', q.prompt));
    if (q.hint) inner.appendChild(el('p', 'wizard__hint', q.hint));

    var list = el('ul', 'wizard__options');
    q.options.forEach(function (opt) {
      var li = el('li');
      var btn = el('button', null, opt.label);
      btn.type = 'button';
      btn.addEventListener('click', function () {
        answers[step] = { id: opt.id, label: opt.label, add: opt.add || {} };
        step += 1;
        if (step >= questions.length) { finished = true; renderResult(); } else { renderQuestion(); }
      });
      li.appendChild(btn);
      list.appendChild(li);
    });
    inner.appendChild(list);

    if (step > 0) {
      var nav = el('div', 'wizard__nav');
      var back = el('button', null, '‹ ' + i18n.back);
      back.type = 'button';
      back.addEventListener('click', function () { step -= 1; renderQuestion(); });
      nav.appendChild(back);
      var restart = el('button', null, i18n.restart);
      restart.type = 'button';
      restart.addEventListener('click', reset);
      nav.appendChild(restart);
      inner.appendChild(nav);
    }
  }

  function specSheetText(family) {
    var lines = [];
    lines.push('GlobalLockSummary — lock identification');
    lines.push('Date: ' + new Date().toISOString().slice(0, 10));
    lines.push('');
    lines.push('Most likely family: ' + family.title);
    lines.push('Data status: ' + family.status);
    lines.push('Regions: ' + family.regions.join(', '));
    lines.push('');
    lines.push('Answers given:');
    answers.forEach(function (a, idx) {
      lines.push('  ' + (idx + 1) + '. ' + questions[idx].prompt + ' -> ' + a.label);
    });
    lines.push('');
    lines.push('Measure these (fill in):');
    family.measureOrder.forEach(function (m) {
      lines.push('  ' + m.label + ': ____ mm   (typical: ' + m.typical + ')');
    });
    lines.push('');
    lines.push('Retrofit architectures that fit:');
    family.architectures.forEach(function (a) { lines.push('  - ' + a.label); });
    if (!family.architectures.length) lines.push('  - none: see the lock page for why');
    lines.push('');
    lines.push('Reference: ' + window.location.origin + siteRoot + family.url);
    return lines.join('\n');
  }

  function renderResult() {
    var decision = (window.GLSscore || {}).decide
      ? window.GLSscore.decide(answers, catalog)
      : { confident: false, top: null, tied: [], ranked: [] };
    var ranked = decision.ranked || [];
    inner.innerHTML = '';

    // No match, a score too weak to call, or a tie: say so instead of guessing.
    if (!decision.confident) {
      inner.appendChild(el('p', 'wizard__progress', i18n.result));
      inner.appendChild(el('p', 'result__summary', i18n.unknown));
      if (decision.tied && decision.tied.length) {
        var tiedSection = el('div', 'result__section');
        tiedSection.appendChild(el('h3', null, i18n.alternatives));
        var tiedList = el('ul', 'result__alts');
        decision.tied.forEach(function (entry) {
          var li = el('li');
          var a = el('a', null, entry.family.title);
          a.href = siteRoot + entry.family.url;
          li.appendChild(a);
          tiedList.appendChild(li);
        });
        tiedSection.appendChild(tiedList);
        inner.appendChild(tiedSection);
      }
      var restartOnly = el('div', 'wizard__nav');
      var rb = el('button', 'wizard__btn', i18n.restart);
      rb.type = 'button';
      rb.addEventListener('click', reset);
      restartOnly.appendChild(rb);
      inner.appendChild(restartOnly);
      var weakProduct = productSection();
      if (weakProduct) inner.appendChild(weakProduct);
      return;
    }

    var fam = decision.top.family;

    inner.appendChild(el('p', 'wizard__progress', i18n.result));

    var title = el('h2', 'result__title');
    var link = el('a', null, fam.title);
    link.href = siteRoot + fam.url;
    title.appendChild(link);
    title.appendChild(document.createTextNode(' '));
    title.appendChild(statusBadge(fam.status));
    inner.appendChild(title);

    inner.appendChild(el('p', 'result__summary', fam.summary));

    if (fam.measureOrder.length) {
      var sec1 = el('div', 'result__section');
      sec1.appendChild(el('h3', null, i18n.measureNext));
      var ul = el('ul', 'result__measures');
      fam.measureOrder.forEach(function (m) {
        var li = el('li');
        li.appendChild(el('span', 'k', m.label));
        li.appendChild(el('span', 'v', m.typical));
        ul.appendChild(li);
      });
      sec1.appendChild(ul);
      inner.appendChild(sec1);
    }

    if (fam.architectures.length) {
      var sec2 = el('div', 'result__section');
      sec2.appendChild(el('h3', null, i18n.retrofitOptions));
      var al = el('ul', 'result__alts');
      fam.architectures.forEach(function (a) {
        var li = el('li');
        var a2 = el('a', null, a.label);
        a2.href = siteRoot + a.url;
        li.appendChild(a2);
        al.appendChild(li);
      });
      sec2.appendChild(al);
      inner.appendChild(sec2);
    }

    if (ranked.length > 1) {
      var sec3 = el('div', 'result__section');
      sec3.appendChild(el('h3', null, i18n.alternatives));
      var alts = el('ul', 'result__alts');
      ranked.slice(1, 4).forEach(function (r) {
        var li = el('li');
        var a = el('a', null, r.family.title);
        a.href = siteRoot + r.family.url;
        li.appendChild(a);
        alts.appendChild(li);
      });
      sec3.appendChild(alts);
      inner.appendChild(sec3);
    }

    var product = productSection();
    if (product) inner.appendChild(product);

    var nav = el('div', 'wizard__nav');

    var copy = el('button', 'wizard__btn wizard__btn--primary', i18n.copyReport);
    copy.type = 'button';
    copy.addEventListener('click', function () {
      var text = specSheetText(fam);
      var done = function () {
        copy.textContent = i18n.copied;
        setTimeout(function () { copy.textContent = i18n.copyReport; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
      } else {
        fallbackCopy(text, done);
      }
    });
    nav.appendChild(copy);

    var download = el('button', 'wizard__btn', i18n.downloadReport);
    download.type = 'button';
    download.addEventListener('click', function () {
      var blob = new Blob([specSheetText(fam)], { type: 'text/plain;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'lock-spec-' + fam.id + '.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });
    nav.appendChild(download);

    var again = el('button', 'wizard__btn', i18n.restart);
    again.type = 'button';
    again.addEventListener('click', reset);
    nav.appendChild(again);

    inner.appendChild(nav);
  }

  function fallbackCopy(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'absolute';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { /* clipboard unavailable */ }
    document.body.removeChild(ta);
  }

  function reset() {
    answers = [];
    step = 0;
    finished = false;
    renderQuestion();
  }

  renderQuestion();
})();
