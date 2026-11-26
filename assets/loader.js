(() => {
  const loader = document.getElementById('dastak-loader');
  if (!loader || window.self !== window.top) return;
  let showTimer;
  let hideTimer;
  let safetyTimer;
  let initial = false;
  let shownAt = 0;
  const clearTimers = () => {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    clearTimeout(safetyTimer);
  };
  const hide = () => {
    clearTimers();
    initial = false;
    loader.classList.remove('is-active');
    loader.setAttribute('aria-hidden', 'true');
  };
  const activate = () => {
    shownAt = performance.now();
    loader.classList.add('is-active');
    loader.setAttribute('aria-hidden', 'false');
  };
  const show = (firstArrival = false) => {
    clearTimers();
    initial = firstArrival;
    if (firstArrival) activate();
    else showTimer = setTimeout(activate, 150);
    safetyTimer = setTimeout(hide, firstArrival ? 600 : 3500);
  };
  const ready = () => {
    clearTimeout(hideTimer);
    if (!initial) return hide();
    // A short first-visit introduction; never delay navigation or page rendering.
    hideTimer = setTimeout(hide, Math.max(0, 450 - (performance.now() - shownAt)));
  };
  let firstVisit = true;
  try {
    firstVisit = sessionStorage.getItem('dastak-loader-seen') !== '1';
    sessionStorage.setItem('dastak-loader-seen', '1');
  } catch { /* Storage may be unavailable; the timeout still guarantees dismissal. */ }
  if (firstVisit) show(true);
  // Hide as soon as the page content is ready; images and analytics keep loading in the background.
  if (document.readyState !== 'loading') ready();
  else document.addEventListener('DOMContentLoaded', ready, { once: true });
  window.addEventListener('load', ready, { once: true });
  window.addEventListener('pageshow', event => {
    if (event.persisted) hide();
    else ready();
  });
  window.addEventListener('pagehide', hide);
  // Interaction always dismisses the visual; it never locks the page.
  document.addEventListener('pointerdown', hide, { passive: true });
  document.addEventListener('keydown', hide);
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
    if (!link || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    try {
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return;
      if (url.pathname === location.pathname && url.search === location.search) return;
      // PDFs and standalone tools should keep their normal browser behavior.
      if (/\.(pdf|zip|png|jpe?g|webp|svg)$/i.test(url.pathname)) return;
      show();
    } catch { /* Invalid links keep their normal browser behavior. */ }
  });
})();
