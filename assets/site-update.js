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
