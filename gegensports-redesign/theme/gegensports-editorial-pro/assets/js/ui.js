(function(){
  var d=document,drawer=d.getElementById('drawer'),sp=d.getElementById('search-panel');
  function setDrawer(o){if(!drawer)return;drawer.classList.toggle('is-open',o);d.documentElement.style.overflow=o?'hidden':'';
    d.querySelectorAll('[data-gsx-drawer]').forEach(function(b){b.setAttribute('aria-expanded',o)});
    if(o){var c=drawer.querySelector('[data-gsx-drawer-close].icon-btn');c&&c.focus()}}
  d.addEventListener('click',function(e){
    var t=e.target.closest('[data-gsx-drawer],[data-gsx-drawer-close],[data-gsx-search]');
    if(!t)return;
    if(t.hasAttribute('data-gsx-drawer'))setDrawer(true);
    else if(t.hasAttribute('data-gsx-drawer-close'))setDrawer(false);
    else if(sp){var o=!sp.classList.contains('is-open');sp.classList.toggle('is-open',o);t.setAttribute('aria-expanded',o);if(o){var i=sp.querySelector('input');i&&i.focus()}}
  });
  d.addEventListener('keydown',function(e){if(e.key==='Escape'){setDrawer(false);if(sp)sp.classList.remove('is-open')}});
  // Açık menü dışına tıklayınca kapat
  d.addEventListener('click',function(e){d.querySelectorAll('.nav-drop[open]').forEach(function(x){if(!x.contains(e.target))x.removeAttribute('open')})});
})();
