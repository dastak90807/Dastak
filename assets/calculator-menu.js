/* Adds the site menu bar to the top of the fee calculator pages.
   One file controls the menu on all 6 calculator pages (3 English, 3 Urdu).
   Language comes from <html lang>; the switch opens the same calculator in the other language. */
(function(){
  var box=document.getElementById('dastakCalcContainer')||document.querySelector('.main-wrapper');
  if(!box||document.querySelector('.dm'))return;
  var ur=(document.documentElement.getAttribute('lang')||'')==='ur';
  var L=ur?'/ur/':'/en/';
  var T=ur?{home:'ہوم',services:'خدمات',calc:'فیس کیلکولیٹر',guides:'رہنمائی اور تازہ ترین معلومات',about:'ہمارے بارے میں',contact:'رابطہ کریں',wa:'واٹس ایپ',menu:'مینو',nav:'مرکزی مینو',sw:'English',swLabel:'یہ کیلکولیٹر انگریزی میں کھولیں',logo:'دستک 90807 - گھر کی دہلیز پر خدمات'}
         :{home:'Home',services:'Services',calc:'Fee Calculator',guides:'Guides &amp; Updates',about:'About',contact:'Contact',wa:'WhatsApp',menu:'Menu',nav:'Main navigation',sw:'اردو',swLabel:'Open this calculator in Urdu',logo:'Dastak 90807 - Doorstep Delivery of Services'};
  var other=location.pathname.replace(/^\/(en|ur)\//,ur?'/en/':'/ur/').replace(/\.html$/,'');
  var wa='https://wa.me/923455583530';
  var bar=document.createElement('div');
  bar.className='dm';
  bar.innerHTML=
    '<a class="dm-lg" href="'+L+'"><img src="/assets/dastak-90807-transparent.png" alt="'+T.logo+'" width="2121" height="741"></a>'+
    '<button class="dm-tg" type="button" aria-expanded="false" aria-controls="dm-nav">&#9776; '+T.menu+'</button>'+
    '<nav id="dm-nav" aria-label="'+T.nav+'">'+
      '<a href="'+L+'">'+T.home+'</a>'+
      '<a href="'+L+'services/">'+T.services+'</a>'+
      '<a class="on" href="'+L+'calculators/" aria-current="page">'+T.calc+'</a>'+
      '<a href="'+L+'guides/">'+T.guides+'</a>'+
      '<a href="'+L+'about/">'+T.about+'</a>'+
      '<a href="'+L+'contact/">'+T.contact+'</a>'+
      '<a class="dm-wa2" href="'+wa+'">'+T.wa+'</a>'+
    '</nav>'+
    '<a class="dm-lang" href="'+other+'" hreflang="'+(ur?'en':'ur')+'" lang="'+(ur?'en':'ur')+'" aria-label="'+T.swLabel+'">'+T.sw+'</a>'+
    '<a class="dm-wa" href="'+wa+'">'+T.wa+'</a>';
  box.insertBefore(bar,box.firstChild);
  var t=bar.querySelector('.dm-tg');
  t.addEventListener('click',function(){var o=bar.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
})();
