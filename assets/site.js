(function(){
 var d=document,h=d.documentElement,C=window.KA_CONFIG||{};
 function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
 // language
 var lang=ls('ka_lang')||'th';
 if(/[?&]lang=en/.test(location.search))lang='en';
 function setLang(l){lang=l;h.setAttribute('data-lang',l);h.lang=l;ls('ka_lang',l)}
 setLang(lang);
 // ad test mode: config or ?adtest=1
 if(C.adTest||/[?&]adtest=1/.test(location.search))h.classList.add('ad-test');
 d.addEventListener('DOMContentLoaded',function(){
  d.querySelectorAll('.lang').forEach(function(b){b.onclick=function(){setLang(lang==='en'?'th':'en')}});
  // consent banner (stored in localStorage: ka_consent = granted | denied)
  var c=d.getElementById('consent');
  function show(){c&&c.classList.add('show')}
  if(c){
   if(!ls('ka_consent'))show();
   c.querySelector('.yes').onclick=function(){ls('ka_consent','granted');c.classList.remove('show')};
   c.querySelector('.no').onclick=function(){ls('ka_consent','denied');c.classList.remove('show')};
  }
  d.querySelectorAll('[data-consent-open]').forEach(function(b){b.onclick=show});
  // share: native share sheet, else copy link
  d.querySelectorAll('[data-share]').forEach(function(b){b.onclick=function(){
   var w=b.closest('.share'),u=w.dataset.url,t=w.dataset.title,m=w.querySelector('.share-msg');
   function msg(th,en){m.textContent=lang==='en'?en:th}
   if(navigator.share){navigator.share({title:t,url:u}).catch(function(){});return}
   function fallback(){var i=d.createElement('input');i.value=u;d.body.appendChild(i);i.select();try{d.execCommand('copy');msg('คัดลอกลิงก์แล้ว','Link copied')}catch(e){msg(u,u)}i.remove()}
   if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(function(){msg('คัดลอกลิงก์แล้ว','Link copied')},fallback);else fallback();
  }});
  // category tabs on home
  var tabs=d.getElementById('tabs');
  if(tabs){
   function pick(cat){d.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x.dataset.c===cat)});
    d.querySelectorAll('#room .cab').forEach(function(a){a.style.display=(!cat||a.dataset.c===cat)?'':'none'})}
   tabs.onclick=function(e){var b=e.target.closest('.tab');if(b)pick(b.dataset.c)};
   var HM={'#action':'action','#timing':'timing','#strategy':'strategy','#puzzle':'puzzle'};
   pick(HM[location.hash]||'');addEventListener('hashchange',function(){pick(HM[location.hash]||'')});
  }
 });
})();
