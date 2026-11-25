/* Dastak 90807 WhatsApp Channel button, banner and QR card.
   Loaded on every page by /assets/shared-header.js, so no page needs editing.
   - Every page: "WhatsApp Channel" button in the footer follow row.
   - Home page and guide pages: a short banner above the footer.
   - Contact page: a QR card above "Find me online".
   The channel is for updates only. Bookings stay on WhatsApp 0345-5583530. */
(() => {
  if (window.__dastakChannelCta) return;
  window.__dastakChannelCta = true;

  const CHANNEL_URL = 'https://whatsapp.com/channel/0029VbEdgGRAu3aLblsW5g0Y';
  const QR_SRC = '/assets/qr/dastak-90807-whatsapp-channel-qr-gujar-khan.svg';
  const QR_ALT = 'QR code to follow the Dastak 90807 WhatsApp Channel. Dastak Online Document Facilitation (Registered Facilitator Code 90807), Gujar Khan, Rawalpindi, Punjab';
  const ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-12 7l-5 1 1-4a8 8 0 1 1 16-4z"/></svg>';

  const link = (cls, html) => {
    const a = document.createElement('a');
    a.className = cls;
    a.href = CHANNEL_URL;
    a.target = '_blank';
    a.rel = 'noopener';
    a.innerHTML = html;
    return a;
  };

  const run = () => {
    const path = location.pathname.replace(/index\.html$/, '');
    const isHome = path === '/en/' || path === '/';
    const isGuide = path.indexOf('/en/guides/') === 0;
    const footer = document.querySelector('footer.ft');

    // 1) Footer follow row (all pages)
    document.querySelectorAll('footer .footer-social').forEach(box => {
      if (box.querySelector('.channel-follow')) return;
      const a = link('channel-follow', ICON + '<span>WhatsApp Channel</span><span class="ur" lang="ur" dir="rtl">واٹس ایپ چینل</span>');
      a.setAttribute('aria-label', 'Follow the Dastak 90807 WhatsApp Channel (opens WhatsApp)');
      box.appendChild(a);
    });

    // 2) Banner on the home page and guide pages
    if ((isHome || isGuide) && footer && !document.querySelector('.channel-strip')) {
      const strip = document.createElement('aside');
      strip.className = 'channel-strip';
      strip.setAttribute('aria-label', 'WhatsApp Channel');
      strip.innerHTML =
        '<div class="channel-strip-in">' +
          '<div class="channel-strip-text">' +
            '<h2>Get Punjab document updates on WhatsApp</h2>' +
            '<p>Fee changes, new rules and short guides from Dastak 90807. This is an independent facilitator channel (Code 90807), not a government channel. To book, message WhatsApp 0345-5583530.</p>' +
          '</div>' +
        '</div>';
      const btn = link('channel-btn', ICON + '<span>Follow the Channel</span>');
      strip.firstChild.appendChild(btn);
      footer.parentNode.insertBefore(strip, footer);
    }

    // 3) QR card on the contact page
    const online = document.querySelector('.page-contact .ct-online');
    if (online && !document.querySelector('.channel-card')) {
      const card = document.createElement('section');
      card.className = 'ct-card channel-card';
      card.setAttribute('aria-labelledby', 'channel-card-h');
      const img = document.createElement('img');
      img.src = QR_SRC;
      img.alt = QR_ALT;
      img.width = 180;
      img.height = 180;
      img.loading = 'lazy';
      img.decoding = 'async';
      const text = document.createElement('div');
      text.className = 'channel-card-text';
      text.innerHTML =
        '<p class="ct-eb">Updates</p>' +
        '<h2 id="channel-card-h">Follow our WhatsApp Channel</h2>' +
        '<p>Scan the QR code with your phone camera, or tap the button. You will get fee changes, new rules and short guides for Punjab document services.</p>' +
        '<p class="channel-note">The channel is for updates only. To book or ask a question, message WhatsApp 0345-5583530.</p>';
      text.appendChild(link('channel-btn', ICON + '<span>Follow the Channel</span>'));
      card.appendChild(img);
      card.appendChild(text);
      online.parentNode.insertBefore(card, online);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
