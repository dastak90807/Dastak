(() => {
  const search = document.getElementById('forms-search');
  if (!search) return;
  const buttons = [...document.querySelectorAll('[data-form-filter]')];
  const cards = [...document.querySelectorAll('.form-card')];
  let category = 'all';
  const filter = () => {
    const query = search.value.trim().toLowerCase();
    cards.forEach(card => {
      const categoryMatch = category === 'all' || card.dataset.formCategory === category;
      card.hidden = !categoryMatch || !card.textContent.toLowerCase().includes(query);
    });
  };
  search.addEventListener('input', filter);
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.formFilter;
    buttons.forEach(item => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    filter();
  }));
})();
