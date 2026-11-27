(() => {
  const selector = document.getElementById('checklist-service');
  if (!selector) return;
  selector.disabled = true;
  const content = document.getElementById('checklist-content');
  const title = document.getElementById('checklist-title');
  const variantField = document.getElementById('checklist-variant-field');
  const variantSelect = document.getElementById('checklist-variant');
  const list = document.getElementById('checklist-items');
  const notes = document.getElementById('checklist-notes');
  const progressText = document.getElementById('checklist-progress-text');
  const progress = document.querySelector('.checklist-progress');
  const share = document.getElementById('checklist-share');
  let services = [];
  const ur = (document.documentElement.lang || '').toLowerCase().startsWith('ur');
  const L = ur ? {
    ready: (a, b) => b + ' میں سے ' + a + ' ضروری دستاویزات تیار',
    head: 'پنجاب دستاویزات کی چیک لسٹ\nسروس: ', readyH: '\n\nتیار دستاویزات:\n', missH: '\n\nموجود نہیں / رہنمائی چاہیے:\n',
    noneReady: 'کوئی تیار نہیں', none: 'کوئی نہیں', pickType: 'درخواست کی قسم منتخب کریں',
    choose: 'چیک لسٹ دیکھنے کے لیے دستاویز کی قسم منتخب کریں۔', ifApp: ' (اگر لاگو ہو)',
    data: '/assets/checklist-data-ur.json', down: '<p class="note">چیک لسٹ عارضی طور پر دستیاب نہیں۔</p>',
    labels: ['لرنر ڈرائیونگ پرمٹ', 'لائسنس کی تجدید / ڈپلیکیٹ', 'انٹرنیشنل ڈرائیونگ پرمٹ', 'گاڑی کی ملکیت کی منتقلی', 'نئی گاڑی کی رجسٹریشن', 'پولیس کریکٹر سرٹیفیکیٹ', 'پولیس گمشدگی رپورٹ', 'کرایہ دار کی رجسٹریشن', 'ڈومیسائل سرٹیفیکیٹ', 'پیدائش، نکاح یا ای اسٹامپ']
  } : {
    ready: (a, b) => a + ' of ' + b + ' required documents ready',
    head: 'Punjab document checklist\nService: ', readyH: '\n\nDocuments ready:\n', missH: '\n\nDocuments missing / need guidance:\n',
    noneReady: 'None marked ready', none: 'None', pickType: 'Select application type',
    choose: 'Choose a document type to see its checklist.', ifApp: ' (if applicable)',
    data: '/assets/checklist-data.json', down: '<p class="note">The checklist is temporarily unavailable.</p>',
    labels: ['Learner driving permit', 'License renewal / duplicate', 'International driving permit', 'Vehicle ownership transfer', 'New vehicle registration', 'Police character certificate', 'Police loss report', 'Tenant registration', 'Domicile certificate', 'Birth, marriage or e-stamp']
  };

  const update = () => {
    const service = services[Number(selector.value)];
    if (!service) return;
    const variant = service.variants?.[Number(variantSelect.value)];
    const checked = [...list.querySelectorAll('input:checked')];
    const required = [...list.querySelectorAll('input:not([data-optional])')];
    const ready = required.filter(input => input.checked).length;
    const percent = required.length ? Math.round(ready / required.length * 100) : 100;
    progressText.textContent = L.ready(ready, required.length);
    progress.setAttribute('aria-valuenow', String(percent));
    progress.querySelector('span').style.width = percent + '%';
    const readyList = checked.map(input => '✅ ' + input.dataset.label);
    const missingList = [...list.querySelectorAll('input:not(:checked)')].map(input => '❌ ' + input.dataset.label);
    const message = L.head + service.name + (variant ? ' — ' + variant.name : '') + L.readyH + (readyList.join('\n') || L.noneReady) + L.missH + (missingList.join('\n') || L.none);
    share.href = 'https://wa.me/923455583530?text=' + encodeURIComponent(message);
  };

  const show = () => {
    const service = services[Number(selector.value)];
    content.hidden = !selector.value || !service;
    if (content.hidden) return;
    title.textContent = service.name;
    variantField.hidden = !service.variants;
    if (service.variants) {
      variantSelect.replaceChildren(new Option(L.pickType, ''));
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
      progressText.textContent = L.choose;
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
      checkbox.dataset.label = item.text + (item.optional ? L.ifApp : '');
      if (item.optional) checkbox.dataset.optional = 'true';
      const text = document.createElement('span');
      text.textContent = item.text + (item.optional ? L.ifApp : '');
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
  fetch(L.data, { cache: 'no-cache' }).then(response => {
    if (!response.ok) throw new Error('Checklist unavailable');
    return response.json();
  }).then(data => {
    services = data;
    const labels = L.labels;
    [...selector.options].slice(1).forEach((option, index) => { option.textContent = labels[index]; });
    selector.disabled = false;
    show();
  }).catch(() => {
    selector.disabled = true;
    selector.insertAdjacentHTML('afterend', L.down);
  });
})();
