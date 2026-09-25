(function(){
  var root=document.documentElement;
  function setLang(l){
    if(l!=="fr"&&l!=="en")l="fr";
    root.lang=l;
    var t=root.getAttribute("data-title-"+l); if(t)document.title=t;
    var d=root.getAttribute("data-desc-"+l), m=document.querySelector('meta[name="description"]'); if(d&&m)m.setAttribute("content",d);
    document.querySelectorAll("[data-set-lang]").forEach(function(b){b.setAttribute("aria-pressed",b.getAttribute("data-set-lang")===l?"true":"false")});
    try{localStorage.setItem("fz-lang",l)}catch(e){}
  }
  setLang(root.lang);
  document.querySelectorAll("[data-set-lang]").forEach(function(b){b.addEventListener("click",function(){setLang(b.getAttribute("data-set-lang"))})});
  var header=document.querySelector("header.site"), mt=document.querySelector(".menu-toggle"), mg=document.querySelector(".has-mega"), mgb=document.querySelector(".mega-toggle");
  function closeMega(){if(mg){mg.classList.remove("open");mgb.setAttribute("aria-expanded","false")}}
  if(mgb)mgb.addEventListener("click",function(e){e.stopPropagation();var o=!mg.classList.contains("open");mg.classList.toggle("open",o);mgb.setAttribute("aria-expanded",o?"true":"false")});
  if(mt)mt.addEventListener("click",function(){var o=!header.classList.contains("nav-open");header.classList.toggle("nav-open",o);mt.setAttribute("aria-expanded",o?"true":"false")});
  document.addEventListener("click",function(e){if(mg&&!mg.contains(e.target)&&window.innerWidth>1100)closeMega()});
  document.addEventListener("keydown",function(e){if(e.key==="Escape"){closeMega();if(header.classList.contains("nav-open")){header.classList.remove("nav-open");mt.setAttribute("aria-expanded","false")}}});
  document.querySelectorAll("#primary-nav a").forEach(function(a){a.addEventListener("click",function(){closeMega();header.classList.remove("nav-open");if(mt)mt.setAttribute("aria-expanded","false")})});
  document.querySelectorAll(".year").forEach(function(y){y.textContent=new Date().getFullYear()});
})();
