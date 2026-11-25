/* Dastak 90807 WhatsApp Channel button, banner and QR card.
   Loaded on every page by /assets/shared-header.js, so no page needs editing.
   - Every page: WhatsApp Channel icon in the footer social row (same style as the other icons).
   - Home page and guide pages: a short banner above the footer.
   - Contact page: a QR card above "Find me online", plus the icon in that row.
   The channel is for updates only. Bookings stay on WhatsApp 0345-5583530. */
(() => {
  if (window.__dastakChannelCta) return;
  window.__dastakChannelCta = true;

  const CHANNEL_URL = 'https://whatsapp.com/channel/0029VbEdgGRAu3aLblsW5g0Y';
  const QR_SRC = '/assets/qr/dastak-90807-whatsapp-channel-qr-gujar-khan.svg';
  const QR_ALT = 'QR code to follow the Dastak 90807 WhatsApp Channel. Dastak Online Document Facilitation (Registered Facilitator Code 90807), Gujar Khan, Rawalpindi, Punjab';

  const WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-12 7l-5 1 1-4a8 8 0 1 1 16-4z"/><path d="M9.5 8.8c.3 2.4 2.7 4.8 5.2 5.2l1.1-1.3-1.7-1-.8.6c-.8-.4-1.5-1.1-1.9-1.9l.6-.8-1-1.7z" fill="currentColor" stroke="none"/></svg>';

  const UR = (document.documentElement.lang || '').toLowerCase().indexOf('ur') === 0;
  const T = UR ? {
    label: 'واٹس ایپ چینل',
    h2: 'پنجاب کی دستاویزات کی تازہ معلومات کے لیے ہمارا واٹس ایپ چینل جوائن کریں',
    sub: 'دستک 90807 کی طرف سے گوجرخان، راولپنڈی اور پورے پنجاب کے لیے مفت اپ ڈیٹس۔',
    items: ['ڈرائیونگ لائسنس کی تجدید اور ٹریکنگ کی معلومات', 'ٹوکن ٹیکس کی آخری تاریخ اور جرمانے کی یاد دہانی', 'پولیس کریکٹر سرٹیفیکیٹ اور تصدیق سے متعلق مشورے', 'ڈومیسائل، ای اسٹامپ اور گاڑی کی ملکیت کی منتقلی کی گائیڈز'],
    note: 'یہ ایک آزاد فیسیلیٹیٹر چینل ہے (کوڈ <span class="ltr">90807</span>)، سرکاری چینل نہیں۔ بکنگ کے لیے واٹس ایپ <span class="ltr">0345-5583530</span> پر میسج کریں۔',
    btn: 'واٹس ایپ چینل جوائن کریں'
  } : {
    label: 'WhatsApp Channel',
    h2: 'Join our WhatsApp Channel for Punjab document updates',
    sub: 'Free updates from Dastak 90807 for Gujar Khan, Rawalpindi and all Punjab.',
    items: ['Driving license renewal and tracking updates', 'Token tax deadline and penalty reminders', 'Police character certificate and verification tips', 'Domicile, e-stamp and vehicle transfer guides'],
    note: 'Independent facilitator channel (Code 90807), not a government channel. To book, message WhatsApp 0345-5583530.',
    btn: 'Join the WhatsApp Channel'
  };

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
    const isHome = path === '/en/' || path === '/' || path === '/ur/';
    const isGuide = path.indexOf('/en/guides/') === 0 || path.indexOf('/ur/guides/') === 0;
    const footer = document.querySelector('footer.ft');

    // 1) Icon-only button, same style as the other social icons (footer on all pages, "Find me online" on contact)
    document.querySelectorAll('footer .footer-social .soc, .contact-social').forEach(row => {
      if (row.querySelector('.channel-follow')) return;
      const a = link('social-icon channel-follow', WA_ICON);
      a.setAttribute('aria-label', T.label);
      a.title = T.label;
      row.appendChild(a);
    });

    // 2) Banner on the home page and guide pages
    if ((isHome || isGuide) && footer && !document.querySelector('.channel-strip')) {
      const strip = document.createElement('aside');
      strip.className = 'channel-strip' + (isHome ? ' is-home' : (path !== '/en/guides/' && path !== '/ur/guides/' ? ' is-article' : ''));
      strip.setAttribute('aria-label', T.label);
      strip.innerHTML =
        '<div class="channel-strip-in">' +
          '<h2>' + T.h2 + '</h2>' +
          '<p class="channel-strip-sub">' + T.sub + '</p>' +
          '<ul class="channel-strip-list">' + T.items.map(t => '<li>' + t + '</li>').join('') + '</ul>' +
          '<div class="channel-strip-foot">' +
            '<p class="channel-strip-note">' + T.note + '</p>' +
          '</div>' +
        '</div>';
      strip.querySelector('.channel-strip-foot').appendChild(link('channel-btn', WA_ICON + '<span>' + T.btn + '</span>'));
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
      img.alt = UR ? 'دستک 90807 واٹس ایپ چینل فالو کرنے کا QR کوڈ۔ دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی، پنجاب' : QR_ALT;
      img.width = 180;
      img.height = 180;
      img.loading = 'lazy';
      img.decoding = 'async';
      const text = document.createElement('div');
      text.className = 'channel-card-text';
      text.innerHTML =
        (UR ?
        '<p class="ct-eb">تازہ معلومات</p>' +
        '<h2 id="channel-card-h">ہمارا واٹس ایپ چینل فالو کریں</h2>' +
        '<p>فون کے کیمرے سے QR کوڈ اسکین کریں یا بٹن دبائیں۔ پنجاب کی دستاویزات کی فیس میں تبدیلی، نئے قواعد اور مختصر گائیڈز ملیں گی۔</p>' +
        '<p class="channel-note">چینل صرف تازہ معلومات کے لیے ہے۔ بکنگ یا سوال کے لیے واٹس ایپ <span class="ltr">0345-5583530</span> پر میسج کریں۔</p>'
      :
        '<p class="ct-eb">Updates</p>' +
        '<h2 id="channel-card-h">Follow our WhatsApp Channel</h2>' +
        '<p>Scan the QR code with your phone camera, or tap the button. You will get fee changes, new rules and short guides for Punjab document services.</p>' +
        '<p class="channel-note">The channel is for updates only. To book or ask a question, message WhatsApp 0345-5583530.</p>');
      text.appendChild(link('channel-btn', WA_ICON + '<span>' + (UR ? 'واٹس ایپ چینل جوائن کریں' : 'Join the WhatsApp Channel') + '</span>'));
      card.appendChild(img);
      card.appendChild(text);
      online.parentNode.insertBefore(card, online);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
