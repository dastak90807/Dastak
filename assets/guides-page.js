(function(){
  var list=document.getElementById('gp-list'),news=document.getElementById('gp-news'),empty=document.getElementById('gp-empty');
  if(!list)return;
  var items=[].slice.call(list.querySelectorAll('[data-gp-cat]'));
  var chips=[].slice.call(document.querySelectorAll('[data-gp-chip]'));
  var search=document.getElementById('gp-search'),cat='all';
  function apply(){
    var q=(search.value||'').trim().toLowerCase(),shown=0;
    items.forEach(function(el){
      var c=el.getAttribute('data-gp-cat'),t=el.getAttribute('data-gp-text')||'';
      var ok=cat==='news'?false:(cat==='all'||c===cat)&&(!q||t.indexOf(q)>-1)&&!(c==='more'&&(cat!=='all'||q&&t.indexOf(q)<0));
      el.hidden=!ok;if(ok&&c!=='more')shown++;
    });
    var hdr=list.querySelectorAll('.gp-h,.gp-sub,.gp-grid');
    var gridShown=[].slice.call(list.querySelectorAll('.gp-card')).some(function(x){return !x.hidden});
    [].forEach.call(hdr,function(h){h.hidden=!gridShown});
    if(news)news.hidden=!(cat==='all'&&!q||cat==='news');
    empty.hidden=!(shown===0&&cat!=='news');
  }
  chips.forEach(function(b){b.addEventListener('click',function(){
    cat=b.getAttribute('data-gp-chip');
    chips.forEach(function(x){var a=x===b;x.classList.toggle('active',a);x.setAttribute('aria-pressed',String(a))});
    apply();
  })});
  search.addEventListener('input',apply);
})();
