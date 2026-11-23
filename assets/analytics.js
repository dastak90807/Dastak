/* Dastak 90807 analytics.
   Loads Google Analytics 4 once for the whole site and records lead actions.
   Loaded on every page by /assets/shared-header.js, so no page needs editing.
   Only the page path, link position and file name are sent. Names, phone
   numbers or messages typed by visitors are never sent. */
(() => {
  if (window.__dastakAnalytics) return;
  window.__dastakAnalytics = true;

  const MEASUREMENT_ID = 'G-1HYLLE98MM';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', MEASUREMENT_ID);

  const tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
  document.head.appendChild(tag);

  const send = (name, params) => {
    window.gtag('event', name, Object.assign({ page_path: location.pathname, transport_type: 'beacon' }, params));
  };

  const where = el => el.closest('header') ? 'header' : el.closest('footer') ? 'footer' : el.closest('main') ? 'main' : 'page';

  document.addEventListener('click', event => {
    const link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href') || '';

    if (/^https?:\/\/(wa\.me|api\.whatsapp\.com|wa\.link)\//i.test(href)) {
      send('whatsapp_click', { link_location: where(link) });
    } else if (/^tel:/i.test(href)) {
      send('call_click', { link_location: where(link) });
    } else if (/\.(pdf|docx?|xlsx?)(\?|#|$)/i.test(href) || /\/forms\//i.test(href)) {
      send('form_download', { file_name: href.split(/[?#]/)[0].split('/').pop(), link_location: where(link) });
    }
  });

  // The contact form opens WhatsApp when submitted.
  document.addEventListener('submit', event => {
    const form = event.target;
    if (form && form.id === 'wf') send('whatsapp_click', { link_location: 'contact_form' });
  });
})();
