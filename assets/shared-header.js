/* Dastak 90807 shared site header.
   One file controls the header, navigation, search box and EN / اردو language switch on every page.
   Pages include it with:  <script src="/assets/shared-header.js?v=N"></script>
   The script sits exactly where the header should appear, and loads
   /assets/shared-header.css with the same version number.
   Urdu pages (<html lang="ur">) get the Urdu menu automatically. */
(() => {
  const script = document.currentScript;
  if (!script || document.querySelector('header.hd')) return;

  const version = new URL(script.src, location.href).searchParams.get('v') || '1';
  const addCss = (href) => {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = href;
    css.setAttribute('blocking', 'render');
    document.head.appendChild(css);
  };
  addCss('/assets/shared-header.css?v=' + version);
  addCss('/assets/lang-switch.css?v=2');

  if (!window.__dastakAnalytics) {
    const analytics = document.createElement('script');
    analytics.defer = true;
    analytics.src = '/assets/analytics.js?v=1';
    document.head.appendChild(analytics);
  }

  // Pages that have an Urdu version. Add a path here when a new /ur/ page is published.
  const urduPages = [
    '/', '/services/', '/guides/', '/calculators/', '/contact/', '/gujar-khan/',
    '/services/renewal-of-regular-license/', '/services/learner-driving-license/',
    '/services/character-certificate/', '/services/transfer-of-motor-vehicle/',
    '/services/token-tax/', '/services/domicile-certificate/',
    '/guides/punjab-driving-license-renewal-online/', '/guides/how-to-track-driving-license-in-punjab/',
    '/guides/punjab-police-character-certificate-online/', '/guides/vehicle-transfer-token-tax-punjab/'
  ];

  const isUrdu = (document.documentElement.lang || '').toLowerCase().startsWith('ur');
  let path = location.pathname.replace(/index\.html$/, '');
  if (!path.endsWith('/')) path += '/';
  const rest = path.replace(/^\/(en|ur)\//, '/');
  const switchHref = isUrdu ? '/en' + rest : (urduPages.includes(rest) ? '/ur' + rest : '/ur/');

  const t = isUrdu ? {
    home: '/ur/', brandAlt: 'دستک 90807، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن', menu: 'مینیو', navLabel: 'مرکزی مینیو',
    links: [['/ur/', 'ہوم'], ['/ur/services/', 'خدمات'], ['/ur/calculators/', 'فیس کیلکولیٹر', 'nav-calc']],
    tools: 'شہری سہولیات',
    toolLinks: [['/en/document-checklist/', 'دستاویزات کی چیک لسٹ'], ['/en/citizen-tools/', 'سرکاری پورٹلز'], ['/en/downloads/', 'فارمز اور ڈاؤن لوڈز']],
    after: [['/ur/guides/', 'رہنمائی اور تازہ ترین معلومات'], ['/en/about/', 'ہمارے بارے میں'], ['/ur/contact/', 'رابطہ کریں']],
    searchLabel: 'سروس، گائیڈ یا فارم تلاش کریں', searchAria: 'دستک میں تلاش', placeholder: 'سروس تلاش کریں…', searchBtn: 'تلاش',
    switchText: 'English', switchLang: 'en', switchAria: 'یہ صفحہ انگریزی میں پڑھیں', wa: 'واٹس ایپ'
  } : {
    home: '/en/', brandAlt: 'Dastak 90807 — Doorstep Delivery of Services', menu: 'Menu', navLabel: 'Main navigation',
    links: [['/en/', 'Home'], ['/en/services/', 'Services'], ['/en/calculators/', 'Fee Calculator', 'nav-calc']],
    tools: 'Citizen Tools',
    toolLinks: [['/en/document-checklist/', 'Document Checklist'], ['/en/citizen-tools/', 'Official Portals'], ['/en/downloads/', 'Downloads &amp; Forms']],
    after: [['/en/guides/', 'Guides &amp; Updates'], ['/en/about/', 'About'], ['/en/contact/', 'Contact']],
    searchLabel: 'Find a service, guide or form', searchAria: 'Search Dastak', placeholder: 'Search services…', searchBtn: 'Search',
    switchText: 'اردو', switchLang: 'ur', switchAria: 'Read this page in Urdu', wa: 'WhatsApp'
  };

  const link = ([href, text, cls]) => '<a' + (cls ? ' class="' + cls + '"' : '') + ' href="' + href + '">' + text + '</a>';

  script.insertAdjacentHTML('beforebegin',
    '<header class="hd">' +
      '<a class="brand" href="' + t.home + '"><img class="brand-logo" src="/assets/dastak-90807-transparent.png" alt="' + t.brandAlt + '" width="2121" height="741"></a>' +
      '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-navigation" hidden>' + t.menu + '</button>' +
      '<nav id="site-navigation" aria-label="' + t.navLabel + '">' +
        t.links.map(link).join('') +
        '<div class="nav-tools">' +
          '<button class="nav-tools-toggle" type="button" aria-expanded="false" aria-controls="citizen-tools-menu">' + t.tools + '</button>' +
          '<div class="nav-tools-menu" id="citizen-tools-menu">' + t.toolLinks.map(link).join('') + '</div>' +
        '</div>' +
        t.after.map(link).join('') +
      '</nav>' +
      '<div class="site-search hd-search" role="search" aria-label="' + t.searchAria + '">' +
        '<label class="hd-search-label" for="site-search-query">' + t.searchLabel + '</label>' +
        '<div class="site-search-field">' +
          '<label class="hd-search-icon" for="site-search-query" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg></label>' +
          '<input id="site-search-query" type="search" placeholder="' + t.placeholder + '" autocomplete="off" aria-controls="site-search-results">' +
          '<button type="button" class="site-search-submit">' + t.searchBtn + '</button>' +
        '</div>' +
        '<div id="site-search-results" class="site-search-results" aria-live="polite" hidden></div>' +
      '</div>' +
      '<a class="lang-switch" href="' + switchHref + '" hreflang="' + t.switchLang + '" role="switch" aria-checked="' + (isUrdu ? 'true' : 'false') + '" aria-label="' + t.switchAria + '">' +
        '<span class="ls-en" lang="en">Eng</span><span class="ls-track" aria-hidden="true"><span class="ls-knob"></span></span><span class="ls-ur" lang="ur">اردو</span></a>' +
      '<a class="btn g sm" href="https://wa.me/923455583530">' + t.wa + '</a>' +
    '</header>');
})();
