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
      window.gtag('event', control.dataset.gaEvent);
    }
  });
})();
// Search pages and FAQs from the static index bundled with the site.
(() => {
  const opener = document.querySelector('.site-search-open');
  if (!opener) return;
  const dialog = document.createElement('div');
  dialog.className = 'site-search-dialog';
  dialog.hidden = true;
  dialog.innerHTML = '<div class="site-search-panel" role="dialog" aria-modal="true" aria-label="Search Dastak 90807"><div class="site-search-head"><label for="site-search-query">Search this website</label><button type="button" class="site-search-close" aria-label="Close search">×</button></div><input id="site-search-query" type="search" placeholder="Try learner, character, 70cc or domicile" autocomplete="off"><div class="site-search-results" aria-live="polite"></div></div>';
  document.body.append(dialog);
  const input = dialog.querySelector('input');
  const results = dialog.querySelector('.site-search-results');
  let entries;
  const close = () => {
    dialog.hidden = true;
    document.body.classList.remove('search-open');
    opener.focus();
  };
  const render = () => {
    const query = input.value.trim().toLowerCase();
    results.replaceChildren();
    if (!query) {
      results.textContent = 'Search services, guides, FAQs and tools.';
      return;
    }
    const words = query.split(/\s+/);
    const matches = (entries || []).map(item => {
      const title = item.title.toLowerCase();
      const summary = item.summary.toLowerCase();
      const score = words.reduce((total, word) => total + (title.includes(word) ? 3 : 0) + (summary.includes(word) ? 1 : 0), 0);
      return { item, score };
    }).filter(result => result.score > 0).sort((a, b) => b.score - a.score).slice(0, 10);
    if (!matches.length) {
      results.textContent = 'No matching pages found. Try another term.';
      return;
    }
    matches.forEach(({ item }) => {
      const link = document.createElement('a');
      link.href = item.url;
      const heading = document.createElement('strong');
      heading.textContent = item.title;
      const detail = document.createElement('small');
      detail.textContent = item.type + (item.summary ? ' · ' + item.summary : '');
      link.append(heading, detail);
      results.append(link);
    });
  };
  opener.addEventListener('click', async () => {
    dialog.hidden = false;
    document.body.classList.add('search-open');
    input.focus();
    render();
    if (entries) return;
    try {
      const response = await fetch('/assets/search-index.json');
      if (!response.ok) throw new Error('Search index unavailable');
      entries = await response.json();
      render();
    } catch {
      results.textContent = 'Search is temporarily unavailable. Browse Services or Citizen Tools instead.';
    }
  });
  dialog.querySelector('.site-search-close').addEventListener('click', close);
  dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
  document.addEventListener('keydown', event => {
    if (dialog.hidden) return;
    if (event.key === 'Escape') close();
    if (event.key === 'Enter' && event.target === input && typeof window.gtag === 'function') {
      window.gtag('event', 'site_search', { search_term: input.value.trim() });
    }
  });
  input.addEventListener('input', render);
})();
