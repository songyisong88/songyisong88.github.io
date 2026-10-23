/* Kairon Arcade no-zoom guard v1: stops tap / double-tap / pinch zoom on phones (iOS Safari, LINE, Android). */
(function(){
  if (window.__kaironNoZoom) return; window.__kaironNoZoom = 1;
  var d = document;
  // 1) viewport meta
  var VP = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover';
  var m = d.querySelector('meta[name="viewport"]');
  if (!m) { m = d.createElement('meta'); m.name = 'viewport'; (d.head || d.documentElement).appendChild(m); }
  if (m.getAttribute('content') !== VP) m.setAttribute('content', VP);
  // 2) CSS (inserted early so a page's own stricter rules such as touch-action:none still win)
  var css = 'html,body{touch-action:manipulation;-webkit-text-size-adjust:100%;text-size-adjust:100%;overscroll-behavior:none;-webkit-tap-highlight-color:transparent}'
    + 'body{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}'
    + 'canvas{touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}'
    + 'input,textarea,select,[contenteditable]{-webkit-user-select:text;user-select:text;-webkit-touch-callout:default}'
    + 'input,textarea,select{font-size:max(16px,1em)!important}';
  var s = d.createElement('style'); s.id = 'kairon-no-zoom'; s.textContent = css;
  var h = d.head || d.documentElement;
  h.insertBefore(s, h.firstChild);
  // 3) iOS Safari ignores user-scalable=no: block gesture events
  var pd = function(e){ if (e.cancelable) e.preventDefault(); };
  var act = { passive: false };
  ['gesturestart','gesturechange','gestureend'].forEach(function(t){ d.addEventListener(t, pd, act); });
  // 4) pinch with two fingers
  d.addEventListener('touchmove', function(e){ if (e.touches && e.touches.length > 1) pd(e); }, act);
  // 5) double-tap zoom guard (keeps buttons/links/inputs untouched; re-sends the click elsewhere)
  var INTER = 'a,button,input,select,textarea,label,summary,[role="button"],[onclick],[contenteditable],[tabindex]:not([tabindex="-1"])';
  var last = 0, startPrevented = false;
  window.addEventListener('touchstart', function(e){ startPrevented = e.defaultPrevented; }, { passive: true });
  window.addEventListener('touchend', function(e){
    var now = Date.now(), quick = now - last < 300; last = now;
    if (!quick || e.defaultPrevented || startPrevented || !e.cancelable) return;
    if (e.changedTouches && e.changedTouches.length !== 1) return;
    var t = e.target;
    if (t && t.closest && t.closest(INTER)) return;
    e.preventDefault();
    var p = e.changedTouches[0];
    if (t && t.dispatchEvent) {
      t.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window,
        clientX: p.clientX, clientY: p.clientY, screenX: p.screenX, screenY: p.screenY }));
    }
  }, act);
  // 6) no game uses dblclick for gameplay
  d.addEventListener('dblclick', pd, act);
})();
