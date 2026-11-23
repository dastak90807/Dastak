/* Dastak 90807 shared site header.
   One file controls the header, navigation and search box on every page.
   Pages include it with:  <script src="/assets/shared-header.js?v=N"></script>
   The script sits exactly where the header should appear, and loads
   /assets/shared-header.css with the same version number. */
(() => {
  const script = document.currentScript;
  if (!script || document.querySelector('header.hd')) return;

  const version = new URL(script.src, location.href).searchParams.get('v') || '1';
  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = '/assets/shared-header.css?v=' + version;
  css.setAttribute('blocking', 'render');
  document.head.appendChild(css);

  if (!window.__dastakAnalytics) {
    const analytics = document.createElement('script');
    analytics.defer = true;
    analytics.src = '/assets/analytics.js?v=1';
    document.head.appendChild(analytics);
  }

  script.insertAdjacentHTML('beforebegin',
    '<header class="hd">' +
      '<a class="brand" href="/en/"><img class="brand-logo" src="/assets/dastak-90807-transparent.png" alt="Dastak 90807 — Doorstep Delivery of Services" width="2121" height="741"></a>' +
      '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-navigation" hidden>Menu</button>' +
      '<nav id="site-navigation" aria-label="Main navigation">' +
        '<a href="/en/">Home</a>' +
        '<a href="/en/services/">Services</a>' +
        '<div class="nav-tools">' +
          '<button class="nav-tools-toggle" type="button" aria-expanded="false" aria-controls="citizen-tools-menu">Citizen Tools</button>' +
          '<div class="nav-tools-menu" id="citizen-tools-menu">' +
            '<a href="/en/calculators/">Fee Calculator</a>' +
            '<a href="/en/document-checklist/">Document Checklist</a>' +
            '<a href="/en/citizen-tools/">Official Portals</a>' +
            '<a href="/en/downloads/">Downloads &amp; Forms</a>' +
          '</div>' +
        '</div>' +
        '<a href="/en/guides/">Guides &amp; Updates</a>' +
        '<a href="/en/about/">About</a>' +
        '<a href="/en/contact/">Contact</a>' +
      '</nav>' +
      '<div class="site-search hd-search" role="search" aria-label="Search Dastak">' +
        '<label class="hd-search-label" for="site-search-query">Find a service, guide or form</label>' +
        '<div class="site-search-field">' +
          '<label class="hd-search-icon" for="site-search-query" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg></label>' +
          '<input id="site-search-query" type="search" placeholder="Search services…" autocomplete="off" aria-controls="site-search-results">' +
          '<button type="button" class="site-search-submit">Search</button>' +
        '</div>' +
        '<div id="site-search-results" class="site-search-results" aria-live="polite" hidden></div>' +
      '</div>' +
      '<a class="btn g sm" href="https://wa.me/923455583530">WhatsApp</a>' +
    '</header>');
})();
