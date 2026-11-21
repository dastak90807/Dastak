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
