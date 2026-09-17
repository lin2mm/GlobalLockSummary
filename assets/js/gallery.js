/* Interactive filtering and search for the landing page lock gallery wall */
(function () {
  'use strict';

  function initGallery() {
    var root = document.querySelector('[data-gallery-root]');
    if (!root) return;

    var filterBtns = root.querySelectorAll('[data-gallery-filter]');
    var searchInput = root.querySelector('[data-gallery-search]');
    var cards = root.querySelectorAll('[data-gallery-card]');
    var countEl = root.querySelector('[data-gallery-count]');

    var currentRegion = 'all';
    var currentQuery = '';

    function applyFilter() {
      var visibleCount = 0;
      var q = currentQuery.toLowerCase().trim();

      cards.forEach(function (card) {
        var region = card.getAttribute('data-region') || '';
        var searchIndex = (card.getAttribute('data-search-text') || '').toLowerCase();

        var matchesRegion = (currentRegion === 'all' || region === currentRegion);
        var matchesQuery = (!q || searchIndex.indexOf(q) !== -1);

        if (matchesRegion && matchesQuery) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (countEl) {
        countEl.textContent = visibleCount;
      }
    }

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        currentRegion = btn.getAttribute('data-gallery-filter') || 'all';
        applyFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        currentQuery = searchInput.value || '';
        applyFilter();
      });
    }
  }

  if (typeof window !== 'undefined') {
    document.addEventListener('DOMContentLoaded', initGallery);
  }
}());
