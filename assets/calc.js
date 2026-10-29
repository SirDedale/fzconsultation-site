(function(){
  var form=document.getElementById("calc-form"),out=document.getElementById("calc-out"),dEl=document.getElementById("calc-data");
  if(!form||!out||!dEl)return;
  var D;try{D=JSON.parse(dEl.textContent)}catch(e){return}
  var ui=D.ui;form.elements.cur.value=D.defaultCur;
  function n(k){var v=parseFloat(form.elements[k].value);return isFinite(v)&&v>=0?v:NaN}
  function money(x){try{return new Intl.NumberFormat(D.lang==="fr"?"fr-CA":"en-US",{style:"currency",currency:form.elements.cur.value,maximumFractionDigits:0}).format(x)}catch(e){return Math.round(x)+" "+form.elements.cur.value}}
  function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e}
  function render(){
    var v={};var bad=false;["revenue","lost_pct","staff","rate","idle_pct","hours","penalty","recovery"].forEach(function(k){v[k]=n(k);if(isNaN(v[k]))bad=true});
    out.textContent="";
    if(bad){out.appendChild(el("p","fstatus err",ui.invalid));return}
    var lp=Math.min(v.lost_pct,100)/100,ip=Math.min(v.idle_pct,100)/100;
    var rev=v.revenue*v.hours*lp, prod=v.staff*v.rate*v.hours*ip, pen=v.penalty, rec=v.recovery;
    var total=rev+prod+pen+rec, perHour=v.hours>0?total/v.hours:0;
    var h=el("p","calc-label",ui.total);out.appendChild(h);
    out.appendChild(el("p","calc-total",money(total)));
    if(v.hours>0)out.appendChild(el("p","muted",ui.per_hour.replace("{x}",money(perHour))));
    var parts=[[ui.rev,rev,"c1"],[ui.prod,prod,"c2"],[ui.pen,pen,"c3"],[ui.rec,rec,"c4"]];
    var bar=el("div","stackbar");bar.setAttribute("role","img");
    bar.setAttribute("aria-label",ui.chart+": "+parts.map(function(p){return p[0]+" "+money(p[1])}).join(", "));
    parts.forEach(function(p){if(total>0&&p[1]>0){var s=el("span","seg "+p[2]);s.style.width=(p[1]/total*100)+"%";bar.appendChild(s)}});
    out.appendChild(bar);
    var ul=el("ul","legend");
    parts.forEach(function(p){var li=el("li");var sw=el("span","sw "+p[2]);sw.setAttribute("aria-hidden","true");li.appendChild(sw);li.appendChild(el("span",null,p[0]+" "));li.appendChild(el("strong",null,money(p[1])));ul.appendChild(li)});
    out.appendChild(ul);
    if(v.hours>1){
      var varHour=(rev+prod)/v.hours, half=Math.round(v.hours/2*10)/10, saved=varHour*(v.hours-half);
      var box=el("div","calc-whatif");box.appendChild(el("h3",null,ui.what_if));
      box.appendChild(el("p",null,ui.what_if_t.replace("{x}",money(varHour)).replace("{a}",String(v.hours)).replace("{b}",String(half)).replace("{y}",money(saved))));
      out.appendChild(box);
    }
    if(D.contact){
      var lines=[D.send_intro+" ("+form.elements.cur.value+")",ui.total+": "+money(total)+(v.hours>0?" / "+v.hours+" h":""),ui.rev+": "+money(rev),ui.prod+": "+money(prod),ui.pen+": "+money(pen),ui.rec+": "+money(rec)];
      var go=el("p",null);var a=el("a","btn ghost",D.send);a.href=D.contact+"?topic=intro&message="+encodeURIComponent(lines.join("\n"));go.appendChild(a);out.appendChild(go);
    }
    out.focus({preventScroll:false});
  }
  form.addEventListener("submit",function(e){e.preventDefault();render()});
  form.addEventListener("reset",function(){setTimeout(function(){out.textContent="";var p=el("p","muted",D.lang==="fr"?"Les résultats apparaîtront ici.":"Results will appear here.");out.appendChild(p)},0)});
})();
