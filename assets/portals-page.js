(function(){
  var list=document.getElementById('pt-list'); if(!list)return;
  var groups=[].slice.call(list.querySelectorAll('.pt-group')),cards=[].slice.call(list.querySelectorAll('.tp-portal'));
  var chips=[].slice.call(document.querySelectorAll('[data-pt-chip]')),search=document.getElementById('pt-search'),empty=document.getElementById('pt-empty'),cat='all';
  function apply(){
    var q=(search.value||'').trim().toLowerCase(),shown=0;
    groups.forEach(function(g){
      var gc=g.getAttribute('data-pt-cat'),any=false;
      [].forEach.call(g.querySelectorAll('.tp-portal'),function(c){
        var ok=(cat==='all'||gc===cat)&&(!q||((c.getAttribute('data-pt-text')||'')+' '+c.textContent.toLowerCase()).indexOf(q)>-1);
        c.hidden=!ok;if(ok){any=true;shown++}
      });
      g.hidden=!any;
    });
    empty.hidden=shown>0;
  }
  chips.forEach(function(b){b.addEventListener('click',function(){
    cat=b.getAttribute('data-pt-chip');
    chips.forEach(function(x){var a=x===b;x.classList.toggle('active',a);x.setAttribute('aria-pressed',String(a))});
    apply();
  })});
  search.addEventListener('input',apply);
})();
