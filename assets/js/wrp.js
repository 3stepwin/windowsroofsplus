/* Windows Roofs Plus — shared site behavior */
(function () {
  'use strict';

  // ── scroll reveal ─────────────────────────────────────────
  var nodes = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && nodes.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    nodes.forEach(function (n) { io.observe(n); });
  } else {
    nodes.forEach(function (n) { n.classList.add('is-in'); });
  }

  // ── mobile menu ───────────────────────────────────────────
  var toggle = document.getElementById('navToggle');
  var menu = document.getElementById('mobileMenu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.innerHTML = open ? '<i class="ri-close-line"></i>' : '<i class="ri-menu-line"></i>';
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<i class="ri-menu-line"></i>';
      }
    });
  }

  // ── current year ──────────────────────────────────────────
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // ── estimate form ─────────────────────────────────────────
  var form = document.getElementById('estimateForm');
  if (!form) return;

  var status = document.getElementById('formStatus');
  var PHONE_HTML = '<a href="tel:+19547068028" style="color:var(--violet-3);font-weight:600">(954) 706-8028</a>';

  function say(html) { if (status) status.innerHTML = html; }

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    var btn = form.querySelector('button[type="submit"]');
    var data = Object.fromEntries(new FormData(form));

    if (data._gotcha) return;                    // honeypot
    if (!data.name || !data.name.trim()) { say('Please enter your name.'); return; }
    if (!data.phone && !data.email) { say('We need a phone number or an email to reach you.'); return; }

    data.page_url = window.location.href;
    data.submitted_at = new Date().toISOString();

    btn.disabled = true;
    var original = btn.innerHTML;
    btn.innerHTML = 'Sending…';
    say('Sending your request…');

    fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json().then(function (b) { return { ok: r.ok, body: b }; }); })
      .then(function (res) {
        if (!res.ok || !res.body.ok) throw new Error(res.body && res.body.message ? res.body.message : 'Request not sent');
        form.reset();
        say('Got it — your request is in. We\'ll reach out shortly. Need us sooner? Call ' + PHONE_HTML + '.');
        btn.innerHTML = 'Request received ✓';
        if (window.location.pathname !== '/thank-you.html') {
          setTimeout(function () { window.location.href = '/thank-you.html'; }, 1200);
        }
      })
      .catch(function (err) {
        say(err.message + '. Please call ' + PHONE_HTML + ' and we\'ll take it from there.');
        btn.disabled = false;
        btn.innerHTML = original;
      });
  });
})();
