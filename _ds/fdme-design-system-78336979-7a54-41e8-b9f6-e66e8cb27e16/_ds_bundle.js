/* @ds-bundle: {"format":3,"namespace":"FDMEDesignSystem_783369","components":[],"sourceHashes":{"shared/site.js":"d9121cc879bd"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.FDMEDesignSystem_783369 = window.FDMEDesignSystem_783369 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// shared/site.js
try { (() => {
// FDME shared: inject nav + footer, wire reveal animations
(async function () {
  try {
    const res = await fetch('shared/nav.html');
    const html = await res.text();
    const slot = document.createElement('div');
    slot.innerHTML = html;
    const nav = slot.querySelector('#fdme-nav');
    if (nav && !document.getElementById('site-nav')) {
      const navEl = nav.content.cloneNode(true);
      const wrap = document.createElement('div');
      wrap.id = 'site-nav';
      wrap.appendChild(navEl);
      document.body.insertBefore(wrap, document.body.firstChild);
    }
    const footer = slot.querySelector('#fdme-footer');
    if (footer && !document.getElementById('site-footer')) {
      const footEl = footer.content.cloneNode(true);
      const wrap = document.createElement('div');
      wrap.id = 'site-footer';
      wrap.appendChild(footEl);
      document.body.appendChild(wrap);
    }
  } catch (e) {
    console.warn('shared nav/footer failed', e);
  }

  // reveal-on-scroll
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    });
  }, {
    threshold: 0.12
  });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "shared/site.js", error: String((e && e.message) || e) }); }

})();
