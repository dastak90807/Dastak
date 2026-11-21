(() => {
  const selector = document.getElementById('checklist-service');
  if (!selector) return;
  const content = document.getElementById('checklist-content');
  const title = document.getElementById('checklist-title');
  const variantSelect = document.getElementById('checklist-variant');
  const list = document.getElementById('checklist-items');
  const notes = document.getElementById('checklist-notes');
  const progressText = document.getElementById('checklist-progress-text');
  const progress = document.querySelector('.checklist-progress');
  const share = document.getElementById('checklist-share');
  let services = [];

  const update = () => {
    const service = services[Number(selector.value)];
    if (!service) return;
    const variant = service.variants?.[Number(variantSelect.value)];
    const checked = [...list.querySelectorAll('input:checked')];
    const required = [...list.querySelectorAll('input:not([data-optional])')];
    const ready = required.filter(input => input.checked).length;
    const percent = required.length ? Math.round(ready / required.length * 100) : 100;
    progressText.textContent = ready + ' of ' + required.length + ' required documents ready';
    progress.setAttribute('aria-valuenow', String(percent));
    progress.querySelector('span').style.width = percent + '%';
    const readyList = checked.map(input => '✅ ' + input.dataset.label);
    const missingList = [...list.querySelectorAll('input:not(:checked)')].map(input => '❌ ' + input.dataset.label);
    const message = 'Punjab document checklist\nService: ' + service.name + (variant ? ' — ' + variant.name : '') + '\n\nDocuments ready:\n' + (readyList.join('\n') || 'None marked ready') + '\n\nDocuments missing / need guidance:\n' + (missingList.join('\n') || 'None');
    share.href = 'https://wa.me/923455583530?text=' + encodeURIComponent(message);
  };

  const show = () => {
    const service = services[Number(selector.value)];
    content.hidden = !selector.value || !service;
    if (content.hidden) return;
    title.textContent = service.name;
    variantSelect.hidden = !service.variants;
    if (service.variants) {
      variantSelect.replaceChildren(new Option('Choose the document type', ''));
      service.variants.forEach((variant, index) => variantSelect.add(new Option(variant.name, String(index))));
      variantSelect.value = '';
    }
    renderItems();
  };

  const renderItems = () => {
    const service = services[Number(selector.value)];
    const items = service.variants ? service.variants[Number(variantSelect.value)]?.items : service.items;
    list.replaceChildren();
    notes.replaceChildren();
    if (!items || (service.variants && !variantSelect.value)) {
      progressText.textContent = 'Choose a document type to see its checklist.';
      progress.setAttribute('aria-valuenow', '0');
      progress.querySelector('span').style.width = '0%';
      share.hidden = true;
      return;
    }
    share.hidden = false;
    items.forEach(item => {
      const label = document.createElement('label');
      label.className = 'checklist-item';
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.dataset.label = item.text;
      if (item.optional) checkbox.dataset.optional = 'true';
      const text = document.createElement('span');
      text.textContent = item.text + (item.optional ? ' (if applicable)' : '');
      label.append(checkbox, text);
      list.append(label);
    });
    service.notes.forEach(note => {
      const paragraph = document.createElement('p');
      paragraph.className = 'note';
      paragraph.textContent = note;
      notes.append(paragraph);
    });
    update();
  };
  list.addEventListener('change', update);
  variantSelect.addEventListener('change', renderItems);
  selector.addEventListener('change', () => {
    show();
    if (typeof window.gtag === 'function') window.gtag('event', 'checklist_service_select', { service: services[Number(selector.value)]?.name });
  });
  fetch('/assets/checklist-data.json').then(response => {
    if (!response.ok) throw new Error('Checklist unavailable');
    return response.json();
  }).then(data => {
    services = data;
    show();
  }).catch(() => {
    selector.disabled = true;
    selector.insertAdjacentHTML('afterend', '<p class="note">The checklist is temporarily unavailable.</p>');
  });
})();
