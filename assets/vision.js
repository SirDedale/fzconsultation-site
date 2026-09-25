(function(){
  var V=window.VISION,root=window.VISION_ROOT||"",el=document.getElementById("vision");if(!V||!el)return;
  var U=V.ui,Q=V.questions,n=Q.length,ans={},i=-1,org="";
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function answered(q){var a=ans[q.id];return q.type==="multi"?(a&&a.length>0):a!==undefined}
  function intro(){
    el.innerHTML='<label class="vorg">'+esc(U.org)+'<input id="vorg" maxlength="80" value="'+esc(org)+'"></label><div class="qnav"><span></span><button class="btn primary" type="button" id="vs">'+esc(U.start)+'</button></div>';
    document.getElementById("vs").onclick=function(){org=document.getElementById("vorg").value.trim();i=0;step()};
  }
  function step(){
    var q=Q[i],multi=q.type==="multi",a=ans[q.id];
    var h='<div class="qprog"><span>'+U.q+" "+(i+1)+" "+U.of+" "+n+'</span></div><div class="qbar"><span style="width:'+Math.round(i/n*100)+'%"></span></div>';
    h+='<h2 id="vt">'+esc(q.q)+'</h2>'+(multi?'<p class="qhint">'+esc(U.multi)+'</p>':'')+'<fieldset class="qopts" aria-labelledby="vt">';
    q.opts.forEach(function(o,k){var on=multi?(a||[]).indexOf(k)>=0:a===k;h+='<label><input type="'+(multi?"checkbox":"radio")+'" name="v" value="'+k+'"'+(on?" checked":"")+'> '+esc(o)+'</label>'});
    h+='</fieldset><div class="qnav"><button class="btn ghost" type="button" id="vp">'+U.prev+'</button><button class="btn primary" type="button" id="vn"'+(answered(q)?"":" disabled")+'>'+(i===n-1?U.see:U.next)+'</button></div>';
    el.innerHTML=h;
    el.querySelectorAll("input").forEach(function(r){r.addEventListener("change",function(){
      if(multi){ans[q.id]=[].slice.call(el.querySelectorAll("input:checked")).map(function(x){return +x.value})}else ans[q.id]=+r.value;
      document.getElementById("vn").disabled=!answered(q)})});
    document.getElementById("vp").onclick=function(){if(i>0){i--;step()}else{i=-1;intro()}};
    document.getElementById("vn").onclick=function(){if(!answered(q))return;if(i<n-1){i++;step()}else summary()};
  }
  function list(arr){arr=arr.map(function(s){return s.toLowerCase()});return arr.length<2?(arr[0]||U.none):arr.slice(0,-1).join(", ")+" "+U.and+" "+arr[arr.length-1]}
  function byId(id){for(var k=0;k<n;k++)if(Q[k].id===id)return Q[k]}
  function color(p){return p<40?"#b3261e":p<70?"var(--signal)":"#1d7a46"}
  function summary(){
    var P=V.phrases,sc={},mx={};
    Q.forEach(function(q){if(q.type==="single"){sc[q.pillar]=(sc[q.pillar]||0)+ans[q.id];mx[q.pillar]=(mx[q.pillar]||0)+3}});
    var pct={};Object.keys(sc).forEach(function(k){pct[k]=Math.round(sc[k]/mx[k]*100)});
    var vision=U.tpl.replace("{h}",P.horizon[ans.horizon]).replace("{o}",org||U.orgdef)
      .replace("{g}",list(ans.goals.map(function(k){return byId("goals").opts[k]})))
      .replace("{a}",list(ans.areas.map(function(k){return byId("areas").opts[k]})))
      .replace("{x}",P.autonomy[ans.autonomy]).replace("{c}",P.cloud[ans.cloud]);
    var h='<p class="qdom">'+esc(U.vision)+'</p><blockquote class="vquote">'+esc(vision)+'</blockquote>';
    h+='<h3>'+esc(U.readiness)+'</h3><ul class="doms">';
    Object.keys(V.pillars).forEach(function(k){var p=pct[k];h+='<li><a href="'+root+V.pillars[k].href+'">'+esc(V.pillars[k].name)+'</a><div class="dbar"><span style="width:'+p+'%;background:'+color(p)+'"></span></div><span class="dpct">'+p+'%</span></li>'});
    h+='</ul><h3>'+esc(U.reco)+'</h3><ol class="prio">';
    var recs=[];
    if(ans.autonomy===2&&pct.governance<67)recs.push({t:U.caution,href:"ai/agents.html"});
    if(ans.cloud===0&&pct.platform<67)recs.push({t:U.citadel,href:"ai/citadel.html"});
    Object.keys(pct).sort(function(a,b){return pct[a]-pct[b]}).forEach(function(k){if(pct[k]<100)recs.push({t:V.pillars[k].rec,href:V.pillars[k].href})});
    var lines=[];
    recs.slice(0,3).forEach(function(r){lines.push(r.t);h+='<li>'+esc(r.t)+'<a href="'+root+r.href+'">'+esc(U.learn)+' →</a></li>'});
    h+='</ol><div class="qnav vact"><button class="btn ghost" type="button" id="vr">'+esc(U.restart)+'</button><span class="vbtns"><button class="btn ghost" type="button" id="vc">'+esc(U.copy)+'</button><button class="btn ghost" type="button" id="vpr">'+esc(U.print)+'</button><a class="btn primary" id="vm" href="#">'+esc(U.send)+'</a></span></div>';
    el.innerHTML=h;el.scrollIntoView({behavior:"smooth",block:"start"});
    var txt=U.vision+"\n"+vision+"\n\n"+U.readiness+"\n"+Object.keys(V.pillars).map(function(k){return "- "+V.pillars[k].name+": "+pct[k]+"%"}).join("\n")+"\n\n"+U.reco+"\n"+lines.map(function(l,k){return (k+1)+". "+l}).join("\n");
    document.getElementById("vm").href="mailto:"+V.email+"?subject="+encodeURIComponent(U.subject+(org?" — "+org:""))+"&body="+encodeURIComponent(txt);
    document.getElementById("vc").onclick=function(){var b=this;try{navigator.clipboard.writeText(txt).then(function(){b.textContent=U.copied})}catch(e){}};
    document.getElementById("vpr").onclick=function(){window.print()};
    document.getElementById("vr").onclick=function(){ans={};i=-1;intro()};
  }
  intro();
})();
