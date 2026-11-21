(() => {
  document.querySelectorAll('[data-calculator]').forEach(widget => {
    const tabs = [...widget.querySelectorAll('[role="tab"]')];
    const panel = widget.querySelector('[role="tabpanel"]');
    const frame = widget.querySelector('iframe');
    const full = widget.querySelector('.calculator-full');
    const activate = tab => {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      panel.setAttribute('aria-labelledby', tab.id);
      if (frame.getAttribute('src') !== tab.dataset.src) frame.src = tab.dataset.src;
      frame.title = tab.dataset.title;
      full.href = tab.dataset.src;
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
        if (event.key === 'ArrowLeft') next = tabs[(index + tabs.length - 1) % tabs.length];
        if (event.key === 'Home') next = tabs[0];
        if (event.key === 'End') next = tabs[tabs.length - 1];
        if (!next) return;
        event.preventDefault();
        activate(next);
        next.focus();
      });
    });
  });
})();

// Category filters and embedded calculator sizing for the content preview.
(() => {
  const filters = [...document.querySelectorAll('[data-guide-filter]')];
  const guideCards = [...document.querySelectorAll('.guide-card[data-guide-category]')];
  const updates = document.querySelector('.guide-updates');
  filters.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.guideFilter;
    filters.forEach(item => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    guideCards.forEach(card => card.hidden = category === 'updates' || category !== 'all' && card.dataset.guideCategory !== category);
    if (updates) updates.hidden = category !== 'all' && category !== 'updates';
  }));

  document.querySelectorAll('.fee-frame').forEach(frame => {
    frame.addEventListener('load', () => {
      const inner = frame.contentWindow;
      if (!inner) return;
      const resize = () => {
        frame.style.height = Math.max(700, inner.document.documentElement.scrollHeight, inner.document.body.scrollHeight) + 'px';
      };
      resize();
      new inner.ResizeObserver(resize).observe(inner.document.body);
      inner.document.addEventListener('click', event => {
        if (event.target.closest('button') && typeof window.gtag === 'function') {
          window.gtag('event', 'calculate_fee');
        }
      });
    });
  });

  document.addEventListener('click', event => {
    const control = event.target.closest('[data-ga-event]');
    if (control && typeof window.gtag === 'function') {
      const params = {};
      for (const [attribute, key] of [['formName', 'form_name'], ['serviceName', 'service_name'], ['toolName', 'tool_name'], ['faqTitle', 'faq_title']]) {
        if (control.dataset[attribute]) params[key] = control.dataset[attribute];
      }
      if (control.tagName === 'DETAILS' && control.dataset.gaEvent === 'home_faq_expand') return;
      window.gtag('event', control.dataset.gaEvent, params);
    }
  });
})();
// Compact navigation: hover on desktop, tap or keyboard on any screen.
(() => {
  const menu = document.querySelector('.nav-tools');
  const toggle = menu?.querySelector('button');
  if (!toggle) return;
  const setOpen = value => { toggle.setAttribute('aria-expanded', String(value)); menu.classList.toggle('is-open', value); };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse' && innerWidth > 980) setOpen(true); });
  menu.addEventListener('pointerleave', event => { if (event.pointerType === 'mouse' && innerWidth > 980) setOpen(false); });
  menu.addEventListener('focusout', event => { if (!menu.contains(event.relatedTarget)) setOpen(false); });
  document.addEventListener('click', event => { if (!menu.contains(event.target)) setOpen(false); });
  menu.addEventListener('keydown', event => { if (event.key === 'Escape') { setOpen(false); toggle.focus(); } });
})();
// Visible search beneath the page introduction; results stay within the page.
(() => {
  const search = document.querySelector('.site-search');
  if (!search) return;
  const input = search.querySelector('input');
  const results = search.querySelector('.site-search-results');
  let entries;
  let loading;
  const render = () => {
    const query = input.value.trim().toLowerCase();
    results.replaceChildren();
    results.hidden = !query;
    if (!query) return;
    if (!entries) { results.textContent = 'Loading search…'; return; }
    const words = query.split(/\s+/);
    const matches = entries.map(item => {
      const title = item.title.toLowerCase();
      const summary = (item.summary || '').toLowerCase();
      const score = words.every(word => (title + ' ' + summary).includes(word)) ? words.reduce((n, word) => n + (title.includes(word) ? 3 : 1), 0) : 0;
      return { item, score };
    }).filter(x => x.score).sort((a,b) => b.score-a.score).slice(0,6);
    if (!matches.length) { results.textContent = 'No results found. Try a service name such as learner, domicile or challan.'; return; }
    matches.forEach(({item}) => {
      const link = document.createElement('a'); link.href = item.url;
      const title = document.createElement('strong'); title.textContent = item.title;
      const detail = document.createElement('small'); detail.textContent = item.type;
      link.append(title, detail); results.append(link);
      link.addEventListener('click', () => { if (typeof window.gtag === 'function') window.gtag('event','site_search',{search_term:input.value.trim()}); });
    });
  };
  const run = async () => {
    render();
    if (!input.value.trim() || entries) return;
    try {
      loading ||= fetch('/assets/search-index.json', { cache: 'no-cache' }).then(response => { if (!response.ok) throw new Error('Unavailable'); return response.json(); });
      entries = await loading; render();
    } catch { loading = null; results.textContent = 'Search could not load. Please try again or open Services from the menu.'; }
  };
  input.addEventListener('input', run);
  input.addEventListener('keydown', event => { if (event.key === 'Enter') { event.preventDefault(); run(); } if (event.key === 'Escape') { input.value = ''; render(); } });
  search.querySelector('button').addEventListener('click', () => { input.focus(); run(); });
})();
