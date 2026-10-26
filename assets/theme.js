(function(){
  var KEY="fz-theme",root=document.documentElement;
  function stored(){try{var v=localStorage.getItem(KEY);return v==="light"||v==="dark"?v:null}catch(e){return null}}
  function effective(){var t=root.getAttribute("data-theme");if(t)return t;return window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}
  var s=stored();if(s)root.setAttribute("data-theme",s);
  document.addEventListener("DOMContentLoaded",function(){
    var bs=document.querySelectorAll(".theme-toggle");if(!bs.length)return;
    function label(){var next=effective()==="dark"?"light":"dark";bs.forEach(function(b){b.setAttribute("aria-label",b.getAttribute("data-label-"+next));b.setAttribute("title",b.getAttribute("data-label-"+next))})}
    label();
    bs.forEach(function(b){b.addEventListener("click",function(){var next=effective()==="dark"?"light":"dark";root.setAttribute("data-theme",next);try{localStorage.setItem(KEY,next)}catch(e){}label()})});
    if(window.matchMedia)window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change",label);
  });
})();
