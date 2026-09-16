/**
 * Client-side search over the JSON index built by build.mjs.
 * Substring matching across title, description and body text — enough for a
 * reference site, and it needs no service to run.
 */
(function () {
  'use strict';

  var root = document.getElementById('search');
  if (!root) return;

  var i18n;
  try { i18n = JSON.parse(root.getAttribute('data-i18n') || '{}'); } catch (e) { i18n = {}; }
  var siteRoot = root.getAttribute('data-root') || '';
  var lang = root.getAttribute('data-lang') || 'en';
  var index = [];
  var loaded = false;

  root.innerHTML = '';
  var box = document.createElement('div');
  box.className = 'search__box';
  var input = document.createElement('input');
  input.type = 'search';
  input.placeholder = i18n.placeholder || 'Search…';
  input.setAttribute('aria-label', i18n.search || 'Search');
  box.appendChild(input);
  root.appendChild(box);

  var results = document.createElement('ul');
  results.className = 'search__results';
  root.appendChild(results);

  var empty = document.createElement('p');
  empty.className = 'search__empty';
  root.appendChild(empty);

  function normalise(text) {
    return String(text || '').toLowerCase();
  }

  function render(items) {
    results.innerHTML = '';
    if (!items.length) {
      empty.textContent = i18n.noResults || '';
      return;
    }
    empty.textContent = '';
    items.slice(0, 40).forEach(function (item) {
      var li = document.createElement('li');
      var kind = document.createElement('span');
      kind.className = 'search__kind';
      kind.textContent = item.kind;
      li.appendChild(kind);

      var a = document.createElement('a');
      a.href = siteRoot + item.url;
      a.textContent = item.title;
      li.appendChild(document.createElement('br'));
      li.appendChild(a);

      var d = document.createElement('p');
      d.className = 'd';
      d.textContent = item.description;
      li.appendChild(d);
      results.appendChild(li);
    });
  }

  function search(query) {
    var q = normalise(query).trim();
    if (!q) { render([]); empty.textContent = ''; return; }
    var terms = q.split(/\s+/);
    var scored = index.map(function (item) {
      var hayTitle = normalise(item.title);
      var hay = hayTitle + ' ' + normalise(item.description) + ' ' + normalise(item.text);
      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        if (hayTitle.indexOf(terms[i]) !== -1) score += 6;
        else if (hay.indexOf(terms[i]) === -1) { score = -1; break; }
        else score += 1;
      }
      return { item: item, score: score };
    }).filter(function (r) { return r.score > 0; })
      .sort(function (a, b) { return b.score - a.score; });

    render(scored.map(function (r) { return r.item; }));
  }

  fetch(siteRoot + 'data/search-index.json')
    .then(function (response) {
      if (!response.ok) throw new Error('index unavailable');
      return response.json();
    })
    .then(function (data) {
      index = data.filter(function (item) { return item.lang === lang; });
      if (!index.length) index = data;
      loaded = true;
      if (input.value) search(input.value);
    })
    .catch(function () {
      empty.textContent = i18n.noResults || '';
    });

  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    var value = input.value;
    timer = setTimeout(function () {
      if (loaded) search(value);
    }, 120);
  });

  // Allow ?q= from elsewhere on the site.
  var params = new URLSearchParams(window.location.search);
  if (params.get('q')) {
    input.value = params.get('q');
    if (loaded) search(input.value);
  }
})();
