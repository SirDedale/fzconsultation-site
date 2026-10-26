(function(){
  document.querySelectorAll(".lang a[data-lang]").forEach(function(a){a.addEventListener("click",function(){try{localStorage.setItem("fz-lang",a.getAttribute("data-lang"))}catch(e){}})});
  try{localStorage.setItem("fz-lang",document.documentElement.lang)}catch(e){}
  var header=document.querySelector("header.site"),mt=document.querySelector(".menu-toggle"),mg=document.querySelector(".has-mega"),mgb=document.querySelector(".mega-toggle");
  function closeMega(){if(mg){mg.classList.remove("open");mgb.setAttribute("aria-expanded","false")}}
  if(mgb)mgb.addEventListener("click",function(e){e.stopPropagation();var o=!mg.classList.contains("open");mg.classList.toggle("open",o);mgb.setAttribute("aria-expanded",o?"true":"false")});
  if(mt)mt.addEventListener("click",function(){var o=!header.classList.contains("nav-open");header.classList.toggle("nav-open",o);mt.setAttribute("aria-expanded",o?"true":"false")});
  document.addEventListener("click",function(e){if(mg&&!mg.contains(e.target)&&window.innerWidth>1100)closeMega()});
  document.addEventListener("keydown",function(e){if(e.key==="Escape"){var inMega=mg&&mg.contains(document.activeElement),inNav=header.contains(document.activeElement);closeMega();if(inMega&&mgb)mgb.focus();if(header.classList.contains("nav-open")){header.classList.remove("nav-open");mt.setAttribute("aria-expanded","false");if(inNav&&mt)mt.focus()}}});
  document.querySelectorAll(".year").forEach(function(y){y.textContent=new Date().getFullYear()});

  var f=document.getElementById("contact-form");
  if(f){
    var st=f.querySelector(".fstatus");
    function say(k,cls){st.textContent=st.getAttribute("data-"+k);st.className="fstatus "+(cls||"")}
    f.addEventListener("submit",function(e){
      e.preventDefault();
      if(f._gotcha.value)return;
      if(!f.name.value.trim()||!f.email.checkValidity()||!f.email.value.trim()||!f.message.value.trim()||!f.consent.checked){say("missing","err");return}
      var org=f.organization?f.organization.value:"", topic=f.topic?f.topic.value:"Website";
      var ep=f.getAttribute("data-endpoint");
      if(!ep){
        var body=f.message.value+"\n\n— "+f.name.value+(org?" ("+org+")":"")+"\n"+f.email.value;
        location.href="mailto:"+f.getAttribute("data-email")+"?subject="+encodeURIComponent("[FZ Consultation] "+topic)+"&body="+encodeURIComponent(body);
        say("mailto","ok");return;
      }
      var btn=f.querySelector('button[type="submit"]');btn.disabled=true;
      fetch(ep,{method:"POST",headers:{"Accept":"application/json"},body:new FormData(f)})
        .then(function(r){if(r.ok){f.reset();say("ok","ok")}else{say("err","err")}})
        .catch(function(){say("err","err")})
        .then(function(){btn.disabled=false});
    });
  }
})();
(function(){
  document.querySelectorAll("[data-print]").forEach(function(b){b.addEventListener("click",function(){window.print()})});
  var chips=document.querySelectorAll(".chips .chip");
  if(chips.length){
    var cards=document.querySelectorAll(".cases a[data-sector]"),st=document.querySelector(".chip-status");
    function apply(f){
      var n=0;cards.forEach(function(c){var ok=f==="all"||c.getAttribute("data-sector")===f;c.hidden=!ok;if(ok)n++});
      chips.forEach(function(c){c.setAttribute("aria-pressed",c.getAttribute("data-filter")===f?"true":"false")});
      if(st)st.textContent=f==="all"?"":(n===1?st.getAttribute("data-one"):st.getAttribute("data-many").replace("{n}",n));
    }
    chips.forEach(function(c){c.addEventListener("click",function(){apply(c.getAttribute("data-filter"))})});
  }
})();
