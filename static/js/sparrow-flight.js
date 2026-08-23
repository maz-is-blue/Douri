/**
 * Douri's signature motif: a sparrow travelling down the dashed track fixed
 * to the right edge of the page, tracking scroll position. Runs on every
 * page (included once from base.html) and also drives the calm section
 * reveal-on-scroll used throughout the site.
 */
(function () {
  'use strict';

  var bird = document.querySelector('[data-sparrow-bird]');

  function updateSparrow() {
    if (!bird) return;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var pct = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    bird.style.top = (5 + pct * 86) + '%';
  }

  var header = document.querySelector('[data-site-header]');
  function updateHeader() {
    if (!header) return;
    var shrunk = window.scrollY > 40;
    header.classList.toggle('is-shrunk', shrunk);
  }

  window.addEventListener('scroll', function () {
    updateSparrow();
    updateHeader();
  }, { passive: true });
  updateSparrow();
  updateHeader();

  // Calm reveal-on-scroll for sections and staggered grids.
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -60px 0px' });

    var targets = document.querySelectorAll('.reveal');
    targets.forEach(function (el, i) {
      var parent = el.parentElement;
      var staggered = parent && parent.hasAttribute('data-stagger');
      var index = staggered ? Array.prototype.indexOf.call(parent.children, el) : 0;
      var delay = Math.min(index * 70, 420);
      el.style.transitionDelay = delay + 'ms';
      io.observe(el);
    });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

  // Hero slideshow: simple auto-advancing crossfade, no external library.
  var hero = document.querySelector('[data-hero]');
  if (hero) {
    var slides = hero.querySelectorAll('.hero-slide');
    var dots = hero.querySelectorAll('[data-hero-dot]');
    var current = 0;

    function show(index) {
      slides.forEach(function (slide, i) {
        slide.classList.toggle('is-active', i === index);
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === index);
      });
      current = index;
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () { show(i); });
    });

    if (slides.length > 1) {
      setInterval(function () { show((current + 1) % slides.length); }, 7000);
    }
  }

  // Copy-to-clipboard for the IBAN on the Support Us page.
  var copyBtn = document.querySelector('[data-copy-iban]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var text = copyBtn.getAttribute('data-copy-iban');
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).catch(function () {});
      }
      var original = copyBtn.textContent;
      copyBtn.textContent = 'Copied';
      setTimeout(function () { copyBtn.textContent = original; }, 1800);
    });
  }
})();
