/* Interactive filtering, search, and 4-block navigation for the landing page */
(function () {
  'use strict';

  function initGallery() {
    var root = document.querySelector('[data-gallery-root]');
    if (!root) return;

    var filterBtns = root.querySelectorAll('[data-gallery-filter]');
    var searchInput = root.querySelector('[data-gallery-search]');
    var blocks = root.querySelectorAll('[data-gallery-block]');
    var cards = root.querySelectorAll('[data-gallery-card]');

    var currentRegion = 'all';
    var currentQuery = '';

    function applyFilter() {
      var q = currentQuery.toLowerCase().trim();

      blocks.forEach(function (block) {
        var blockCode = block.getAttribute('data-gallery-block');
        var isBlockMatched = (currentRegion === 'all' || currentRegion === blockCode);
        
        var blockCards = block.querySelectorAll('[data-gallery-card]');
        var visibleInBlock = 0;

        blockCards.forEach(function (card) {
          var searchText = (card.getAttribute('data-search-text') || '').toLowerCase();
          var matchesQuery = (!q || searchText.indexOf(q) !== -1);

          if (isBlockMatched && matchesQuery) {
            card.style.display = '';
            visibleInBlock++;
          } else {
            card.style.display = 'none';
          }
        });

        // Hide block completely if no cards match
        if (visibleInBlock > 0) {
          block.style.display = '';
        } else {
          block.style.display = 'none';
        }
      });
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
