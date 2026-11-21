(() => {
  const track = document.getElementById('home-review-track');
  document.querySelectorAll('[data-review-direction]').forEach(button => {
    button.addEventListener('click', () => {
      track.scrollBy({ left: Number(button.dataset.reviewDirection) * (track.clientWidth + 20), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    });
  });
  document.querySelectorAll('.home-faqs details').forEach(item => item.addEventListener('toggle', () => {
    if (item.open && typeof window.gtag === 'function') window.gtag('event', 'home_faq_expand', { faq_title: item.dataset.faqTitle });
  }));
})();
