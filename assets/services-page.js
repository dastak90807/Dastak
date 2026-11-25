(function(){var q=document.getElementById('sv-search');if(!q)return;var cards=[].slice.call(document.querySelectorAll('[data-sv-card]')),groups=[].slice.call(document.querySelectorAll('[data-sv-group]')),chips=[].slice.call(document.querySelectorAll('[data-sv-chip]')),empty=document.getElementById('sv-empty'),cat='all';
function run(){var t=q.value.trim().toLowerCase(),shown=0;cards.forEach(function(c){var ok=(!t||(c.getAttribute('data-sv-card')+' '+c.textContent).toLowerCase().indexOf(t)>-1);c.hidden=!ok;});
groups.forEach(function(g){var inCat=cat==='all'||g.getAttribute('data-sv-group')===cat,vis=[].slice.call(g.querySelectorAll('[data-sv-card]')).some(function(c){return !c.hidden});var show=inCat&&vis;g.hidden=!show;if(show)shown++;});
var pop=document.getElementById('sv-popular');if(pop)pop.hidden=!!t||cat!=='all';
empty.style.display=shown?'none':'block';}
q.addEventListener('input',run);chips.forEach(function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-sv-chip');chips.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run();});});})();
