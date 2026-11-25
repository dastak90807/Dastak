/* Adds the site menu bar to the top of the fee calculator pages.
   One file controls the menu on all 3 calculators. */
(function(){
  var box=document.getElementById('dastakCalcContainer')||document.querySelector('.main-wrapper');
  if(!box||document.querySelector('.dm'))return;
  var wa='https://wa.me/923455583530';
  var bar=document.createElement('div');
  bar.className='dm';
  bar.innerHTML=
    '<a class="dm-lg" href="/en/"><img src="/assets/dastak-90807-transparent.png" alt="Dastak 90807 - Doorstep Delivery of Services" width="2121" height="741"></a>'+
    '<button class="dm-tg" type="button" aria-expanded="false" aria-controls="dm-nav">&#9776; Menu</button>'+
    '<nav id="dm-nav" aria-label="Main navigation">'+
      '<a href="/en/">Home</a>'+
      '<a href="/en/services/">Services</a>'+
      '<a class="on" href="/en/calculators/" aria-current="page">Fee Calculator</a>'+
      '<a href="/en/guides/">Guides &amp; Updates</a>'+
      '<a href="/en/about/">About</a>'+
      '<a href="/en/contact/">Contact</a>'+
      '<a class="dm-wa2" href="'+wa+'">WhatsApp</a>'+
    '</nav>'+
    '<a class="dm-wa" href="'+wa+'">WhatsApp</a>';
  box.insertBefore(bar,box.firstChild);
  var t=bar.querySelector('.dm-tg');
  t.addEventListener('click',function(){var o=bar.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
})();
