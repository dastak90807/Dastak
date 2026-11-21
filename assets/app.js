(function(){var f=document.getElementById('wf');if(!f)return;f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f),t='Assalam o Alaikum. My name is '+(d.get('n')||'')+'.\nService: '+(d.get('s')||'')+'\nArea: '+(d.get('a')||'')+(d.get('p')?'\nPhone: '+d.get('p'):'')+'\nQuestion: '+(d.get('q')||'');window.location.href=f.getAttribute('data-wa')+'?text='+encodeURIComponent(t);});})();

(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('site-navigation');
  if (!toggle || !nav) return;

  const setExpanded = (expanded) => toggle.setAttribute('aria-expanded', String(expanded));
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    setExpanded(toggle.getAttribute('aria-expanded') === 'false');
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setExpanded(false);
  });
  toggle.closest('header').addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setExpanded(false);
      toggle.focus();
    }
  });
  matchMedia('(max-width: 980px)').addEventListener('change', () => setExpanded(false));
})();

document.querySelectorAll('.announcement-toggle').forEach((toggle) => {
  const announcement = toggle.closest('.top');
  const pauseLabel = toggle.getAttribute('aria-label');
  const resumeLabel = pauseLabel.replace('Pause ', 'Resume ');
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const paused = announcement.toggleAttribute('data-paused');
    toggle.setAttribute('aria-label', paused ? resumeLabel : pauseLabel);
    toggle.textContent = paused ? '▶' : 'Ⅱ';
  });
});

const reviewGallery = document.querySelector('.review-gallery');
if (reviewGallery) {
  const toggle = reviewGallery.querySelector('.review-pause');
  const motion = matchMedia('(prefers-reduced-motion: no-preference)');
  const updateMotion = () => {
    reviewGallery.toggleAttribute('data-motion', motion.matches);
    toggle.hidden = !motion.matches;
  };
  toggle.addEventListener('click', () => {
    const paused = reviewGallery.toggleAttribute('data-paused');
    toggle.textContent = paused ? 'Resume reviews' : 'Pause reviews';
  });
  motion.addEventListener('change', updateMotion);
  updateMotion();
}
