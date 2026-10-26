/**
 * Keyboard shortcuts for the 5 major area gallery portal:
 * Press '1' for North America, '2' for Europe, '3' for UK/ANZ, '4' for SEA, '5' for LATAM.
 */
(function () {
  document.addEventListener('keydown', function (e) {
    // Ignore when typing inside input or textarea
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
      return;
    }
    var keyMap = {
      '1': 'na',
      '2': 'europe5',
      '3': 'uk-anz',
      '4': 'sea',
      '5': 'latam'
    };
    var targetCode = keyMap[e.key];
    if (targetCode) {
      var card = document.querySelector('[data-portal-target="' + targetCode + '"]');
      if (card && card.href) {
        card.style.transform = 'scale(0.96)';
        setTimeout(function () {
          window.location.href = card.href;
        }, 120);
      }
    }
  });
})();
