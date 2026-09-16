/**
 * Site-wide behaviour. Kept intentionally tiny: the pages are readable without it.
 */
(function () {
  'use strict';

  // Mark the current section in the nav, including generated sub-pages
  // (e.g. /locks/euro-cylinder-mortise.html highlights "Locks").
  var path = window.location.pathname.replace(/index\.html$/, '');
  var links = document.querySelectorAll('.nav__link');
  Array.prototype.forEach.call(links, function (link) {
    if (link.hasAttribute('aria-current')) return;
    var href = link.getAttribute('href') || '';
    var normalised = href.replace(/index\.html$/, '');
    if (normalised.length > 1 && path.indexOf(normalised) === 0) {
      link.setAttribute('aria-current', 'page');
    }
  });

  // Open external links safely.
  Array.prototype.forEach.call(document.querySelectorAll('.page__body a[href^="http"]'), function (a) {
    if (a.host && a.host !== window.location.host) {
      a.setAttribute('rel', 'external noopener');
      a.setAttribute('target', '_blank');
    }
  });
})();
