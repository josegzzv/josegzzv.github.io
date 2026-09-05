/**
 * Lightweight EN/ES toggle for a static page.
 *
 * Two mechanisms, chosen per element:
 *   1. <el class="t" data-en="..." data-es="..." [data-html="1"]>  → text swapped in place
 *   2. <el class="lang lang-en"> / <el class="lang lang-es">         → shown/hidden via CSS (html[data-lang])
 *
 * The hero typed effect is owned here (class .typed-exec) so the strings
 * can be re-initialised on language change without touching main.js.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'jagv.lang';
  var SUPPORTED = ['en', 'es'];
  var typedInstance = null;

  function detectLang() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
    } catch (e) { /* storage unavailable */ }
    var nav = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
    return nav.indexOf('es') === 0 ? 'es' : 'en';
  }

  function applyTexts(lang) {
    var nodes = document.querySelectorAll('.t');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var value = el.getAttribute('data-' + lang);
      if (value === null) continue;
      if (el.getAttribute('data-html') === '1') {
        el.innerHTML = value;
      } else {
        el.textContent = value;
      }
    }
  }

  function applyTyped(lang) {
    var el = document.querySelector('.typed-exec');
    if (!el || typeof Typed === 'undefined') return;
    var raw = el.getAttribute('data-typed-' + lang) || el.getAttribute('data-typed-en') || '';
    var strings = raw.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (typedInstance) {
      typedInstance.destroy();
      typedInstance = null;
      el.textContent = '';
    }
    typedInstance = new Typed('.typed-exec', {
      strings: strings,
      loop: true,
      typeSpeed: 70,
      backSpeed: 35,
      backDelay: 2200,
      smartBackspace: false
    });
  }

  function applyButtons(lang) {
    var btns = document.querySelectorAll('.lang-btn');
    for (var i = 0; i < btns.length; i++) {
      var active = btns[i].getAttribute('data-lang') === lang;
      btns[i].classList.toggle('active', active);
      btns[i].setAttribute('aria-pressed', active ? 'true' : 'false');
    }
  }

  function setLang(lang, persist) {
    if (SUPPORTED.indexOf(lang) === -1) lang = 'en';
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('data-lang', lang);
    applyTexts(lang);
    applyButtons(lang);
    applyTyped(lang);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Initial language before first paint of dynamic bits
    setLang(detectLang(), false);

    var btns = document.querySelectorAll('.lang-btn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener('click', function (ev) {
        ev.preventDefault();
        setLang(this.getAttribute('data-lang'), true);
      });
    }

    var year = document.getElementById('year');
    if (year) year.textContent = String(new Date().getFullYear());
  });

  // Expose for debugging / external hooks
  window.JAGV = window.JAGV || {};
  window.JAGV.setLang = function (l) { setLang(l, true); };
})();
