/* МСГ — прототип, интерактив. Без зависимостей. */
(function () {
  'use strict';
  var pages = document.querySelectorAll('.page[data-page]');
  var SPA = pages.length > 1;

  function activeRoot() {
    if (!SPA) return document;
    return document.querySelector('.page[data-page]:not([hidden])') || document;
  }

  /* ---------- Роутер (только в одностраничной сборке) ---------- */
  function route() {
    if (!SPA) return;
    var h = location.hash.replace(/^#\/?/, '');
    var name = h.split('/')[0] || 'services';
    var target = document.querySelector('.page[data-page="' + name + '"]') || document.querySelector('.page[data-page="services"]');
    pages.forEach(function (p) { p.hidden = (p !== target); });
    document.title = target.getAttribute('data-title') || document.title;
    window.scrollTo(0, 0);
    initSubnav();
  }
  if (SPA) { window.addEventListener('hashchange', route); }

  /* ---------- Якоря внутри страницы ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (href === '#' ) { e.preventDefault(); return; }
    if (href.indexOf('#/') === 0) return; // переход между страницами
    var el = activeRoot().querySelector(href);
    if (el) {
      e.preventDefault();
      var y = el.getBoundingClientRect().top + window.pageYOffset - 125 - 57 - 8;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  });

  /* ---------- Тень хедера ---------- */
  function onScroll() {
    document.querySelectorAll('.hdr').forEach(function (h) { h.classList.toggle('is-scrolled', window.pageYOffset > 4); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Подсветка якорного подменю ---------- */
  var io;
  function initSubnav() {
    if (io) io.disconnect();
    var root = activeRoot();
    var links = root.querySelectorAll('.subnav a.sn');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (l) { var t = root.querySelector(l.getAttribute('href')); if (t) map[t.id] = l; });
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          map[en.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-200px 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(root.querySelector('#' + CSS.escape(id))); });
  }

  /* ---------- Модальное окно «Оставить заявку» ---------- */
  var modal = document.getElementById('modal');
  function setMode(mode) {
    var box = modal.querySelector('.modal-box');
    box.classList.toggle('mode-cert', mode === 'cert');
    modal.querySelectorAll('.mtabs button').forEach(function (b) {
      var on = b.getAttribute('data-mtab') === mode;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
  }
  function openModal(opts) {
    opts = opts || {};
    var wrap = modal.querySelector('.form-wrap');
    wrap.classList.remove('is-done');
    setMode(opts.tab || 'buy');

    var cm = modal.querySelector('textarea');
    if (cm) cm.value = opts.tariff ? 'Интересует тариф «' + opts.tariff + '»' : '';
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    setTimeout(function () { var f = modal.querySelector('input[name="name"]'); if (f) f.focus(); }, 30);
  }
  function closeModal() { modal.classList.remove('is-open'); document.body.style.overflow = ''; }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-modal]');
    if (t) {
      e.preventDefault();
      openModal({ tab: t.getAttribute('data-modal-tab'), service: t.getAttribute('data-modal-service'), tariff: t.getAttribute('data-modal-tariff') });
      return;
    }
    if (e.target === modal || e.target.closest('.modal-x') || e.target.closest('[data-close]')) closeModal();
    var mt = e.target.closest('.mtabs button');
    if (mt) setMode(mt.getAttribute('data-mtab'));
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  /* ---------- Формы: проверка и состояние успеха ---------- */
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('form.form');
    if (!f) return;
    e.preventDefault();
    var ok = true;
    f.querySelectorAll('[required]').forEach(function (inp) {
      var field = inp.closest('.field');
      var bad = inp.type === 'checkbox' ? !inp.checked : !inp.value.trim();
      if (field) field.classList.toggle('err', bad);
      if (bad) ok = false;
    });
    if (!ok) { var first = f.querySelector('.err input, input[type=checkbox][required]:not(:checked)'); if (first) first.focus(); return; }
    f.parentElement.classList.add('is-done');
  });
  document.addEventListener('click', function (e) {
    var r = e.target.closest('[data-reset]');
    if (r) { var w = r.closest('.form-wrap'); if (w) w.classList.remove('is-done'); }
  });

  /* ---------- Hero с видео: запуск по клику (в прототипе — только смена состояния кнопки) ---------- */
  document.addEventListener('click', function (e) {
    var p = e.target.closest('.hero-video .ph-play');
    if (!p) return;
    var box = p.closest('.hero-video');
    var on = box.classList.toggle('is-playing');
    p.textContent = on ? '❚❚' : '▶';
    p.setAttribute('aria-label', on ? 'Пауза' : 'Смотреть видео');
  });
  /* ---------- Аккордеон «открыт один» ---------- */
  document.addEventListener('toggle', function (e) {
    var d = e.target;
    if (d.tagName !== 'DETAILS' || !d.open) return;
    var grp = d.closest('.acc[data-single]');
    if (!grp) return;
    grp.querySelectorAll(':scope > details').forEach(function (x) { if (x !== d) x.open = false; });
  }, true);

  /* ---------- География: «Показать все города» ---------- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-more]');
    if (!b) return;
    var l = b.closest('.geo-wrap').querySelector('.cities');
    l.classList.remove('more'); b.remove();
  });

  /* ---------- Слайдеры ---------- */
  function initSlider(s) {
    var track = s.querySelector('.slider-track');
    var prev = s.querySelector('.slider-prev'), next = s.querySelector('.slider-next');
    var dotsBox = s.querySelector('.dots');
    var items = track.children;
    function per() { return Math.max(1, Math.round(track.clientWidth / (items[0] ? items[0].getBoundingClientRect().width : 1))); }
    function pagesCount() { return Math.max(1, items.length - per() + 1); }
    function idx() { var w = items[0] ? items[0].getBoundingClientRect().width + 24 : 1; return Math.round(track.scrollLeft / w); }
    function go(i) {
      var w = items[0].getBoundingClientRect().width + 24;
      track.scrollTo({ left: Math.max(0, Math.min(i, pagesCount() - 1)) * w, behavior: 'smooth' });
    }
    function build() {
      if (!dotsBox) return;
      dotsBox.innerHTML = '';
      var n = pagesCount();
      for (var i = 0; i < n; i++) { var d = document.createElement('button'); d.className = 'dot'; d.setAttribute('aria-label', 'Слайд ' + (i + 1)); (function (k) { d.onclick = function () { go(k); }; })(i); dotsBox.appendChild(d); }
      sync();
    }
    function sync() {
      var i = idx(), n = pagesCount();
      if (prev) prev.disabled = i <= 0;
      if (next) next.disabled = i >= n - 1;
      if (dotsBox) Array.prototype.forEach.call(dotsBox.children, function (d, k) { d.classList.toggle('is-active', k === i); });
      var nav = s.querySelector('.slider-nav');
      if (nav) nav.style.display = n <= 1 ? 'none' : '';
      var thumbs = s.parentElement.querySelectorAll('.gal-thumbs button');
      thumbs.forEach(function (t, k) { t.classList.toggle('is-active', k === i); });
    }
    if (prev) prev.onclick = function () { go(idx() - 1); };
    if (next) next.onclick = function () { go(idx() + 1); };
    track.addEventListener('scroll', function () { window.requestAnimationFrame(sync); }, { passive: true });
    s.parentElement.querySelectorAll('.gal-thumbs button').forEach(function (t, k) { t.onclick = function () { go(k); }; });
    s._build = build;
    build();
  }
  var sliders = document.querySelectorAll('.slider');
  sliders.forEach(initSlider);
  window.addEventListener('resize', function () { sliders.forEach(function (s) { s._build && s._build(); }); });
  if (SPA) { window.addEventListener('hashchange', function () { setTimeout(function () { sliders.forEach(function (s) { s._build && s._build(); }); }, 0); }); }

  /* ---------- Библиотека секций: ярлыки-пометки вместо карточек в потоке ---------- */
  function closeAnnPops(except) {
    document.querySelectorAll('.ann-pop.is-open').forEach(function (p) { if (p !== except) p.classList.remove('is-open'); });
  }
  function makeBgSwitch(sec) {
    var bg = document.createElement('div');
    bg.className = 'ann-bg';
    bg.setAttribute('role', 'group');
    bg.setAttribute('aria-label', 'Фон секции');
    function sync() {
      var isAlt = sec.classList.contains('alt');
      Array.prototype.forEach.call(bg.children, function (b) {
        b.classList.toggle('is-active', (b.getAttribute('data-bg') === 'alt') === isAlt);
      });
    }
    [['', 'Белый'], ['alt', 'Серый']].forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = o[1];
      b.setAttribute('data-bg', o[0]);
      b.onclick = function (e) {
        e.stopPropagation();
        sec.classList.toggle('alt', o[0] === 'alt');
        sync();
        joinSections(sec.parentNode);
      };
      bg.appendChild(b);
    });
    sync();
    bg._sync = sync;
    return bg;
  }
  function initAnnotations() {
    var anns = document.querySelectorAll('.ann');
    if (!anns.length) return;
    anns.forEach(function (ann) {
      var box = ann.querySelector('.ann-box');
      var code = ann.querySelector('.id').textContent;
      var label = null;
      // секции этой пометки — все соседи до следующей пометки; подпись варианта относится к следующей секции
      for (var el = ann.nextElementSibling; el && !el.classList.contains('ann'); el = el.nextElementSibling) {
        if (el.classList.contains('grp')) continue;
        var vl = el.querySelector(':scope > .var-label');
        if (vl) { label = vl.textContent; el.classList.add('var-src'); continue; }
        var tag = document.createElement('button');
        tag.type = 'button';
        tag.className = 'ann-tag';
        tag.textContent = code + (label ? ' · ' + label : '');
        var pop = document.createElement('div');
        pop.className = 'ann-pop';
        pop.appendChild(box.cloneNode(true));
        tag.onclick = (function (p) { return function (e) { e.stopPropagation(); closeAnnPops(p); p.classList.toggle('is-open'); }; })(pop);
        if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
        el.appendChild(tag);
        el.appendChild(pop);
        // переключатель фона секции (кроме hero)
        if (el.matches('section.sec') && el.querySelector(':scope > .wrap')) el.appendChild(makeBgSwitch(el));
        label = null;
      }
    });
    document.documentElement.classList.add('ann-ready');
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.ann-pop')) closeAnnPops();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAnnPops(); });
  }
  initAnnotations();

  /* ---------- Библиотека секций: схлопывание отступов соседей с одним фоном ----------
     На обычных страницах это делает CSS (селектор соседей). В библиотеке между секциями стоят
     служебные элементы (пометки, подписи вариантов), поэтому класс sec-join ставим здесь. */
  function joinSections(main) {
    var prev = null;
    Array.prototype.forEach.call(main.children, function (el) {
      if (el.matches('.ann, .grp') || el.querySelector(':scope > .var-label')) return;
      var isSec = el.matches('section.sec');
      el.classList.remove('sec-join');
      var alt = el.classList.contains('alt');
      if (isSec && prev && prev.alt === alt) el.classList.add('sec-join');
      prev = isSec ? { alt: alt } : null; // hero, подменю и прочее разрывают цепочку
    });
  }
  document.querySelectorAll('main').forEach(function (m) {
    if (!m.querySelector(':scope > .ann')) return;
    // в библиотеке фон секций чередуется: белый, серый, белый, серый…
    var n = 0;
    Array.prototype.forEach.call(m.querySelectorAll(':scope > section.sec'), function (s) {
      var bg = s.querySelector(':scope > .ann-bg');
      if (!bg) return;
      s.classList.toggle('alt', n % 2 === 1);
      if (bg._sync) bg._sync();
      n++;
    });
    joinSections(m);
  });

  /* ---------- Старт ---------- */
  if (SPA) route(); else initSubnav();
  onScroll();
})();
