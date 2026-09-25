(function(){
  var Q=window.QUIZ,root=window.QUIZ_ROOT||"",el=document.getElementById("quiz");if(!Q||!el)return;
  var U=Q.ui,n=Q.questions.length,ans=new Array(n),i=0;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function q(){
    var it=Q.questions[i],d=Q.domains[it.d];
    var h='<div class="qprog"><span>'+U.q+" "+(i+1)+" "+U.of+" "+n+'</span></div><div class="qbar"><span style="width:'+Math.round(i/n*100)+'%"></span></div>';
    h+='<p class="qdom">'+esc(d.name)+'</p><h2 id="qt">'+esc(it.q)+'</h2><fieldset class="qopts" aria-labelledby="qt">';
    Q.options.forEach(function(o,k){h+='<label><input type="radio" name="a" value="'+k+'"'+(ans[i]===k?" checked":"")+'> '+esc(o)+'</label>'});
    h+='</fieldset><div class="qnav"><button class="btn ghost" type="button" id="qp"'+(i===0?" disabled":"")+'>'+U.prev+'</button><button class="btn primary" type="button" id="qn"'+(ans[i]===undefined?" disabled":"")+'>'+(i===n-1?U.see:U.next)+'</button></div>';
    el.innerHTML=h;
    el.querySelectorAll("input").forEach(function(r){r.addEventListener("change",function(){ans[i]=+r.value;document.getElementById("qn").disabled=false})});
    document.getElementById("qp").onclick=function(){if(i>0){i--;q()}};
    document.getElementById("qn").onclick=function(){if(ans[i]===undefined)return;if(i<n-1){i++;q();el.querySelector("input").focus()}else res()};
  }
  function color(p){return p<40?"#b3261e":p<70?"var(--signal)":"#1d7a46"}
  function res(){
    var tot=0,dom={};
    Q.questions.forEach(function(it,k){tot+=ans[k];dom[it.d]=dom[it.d]||{s:0,m:0};dom[it.d].s+=ans[k];dom[it.d].m+=3});
    var pct=Math.round(tot/(n*3)*100),b=pct<40?0:pct<70?1:2,C=2*Math.PI*60,off=C*(1-pct/100);
    var h='<div class="res-top"><svg class="gauge" viewBox="0 0 150 150" role="img" aria-label="'+U.overall+": "+pct+'%"><circle cx="75" cy="75" r="60" fill="none" stroke="var(--line)" stroke-width="14"/><circle cx="75" cy="75" r="60" fill="none" stroke="'+color(pct)+'" stroke-width="14" stroke-linecap="round" stroke-dasharray="'+C+'" stroke-dashoffset="'+off+'" transform="rotate(-90 75 75)"/><text class="t" x="75" y="82" text-anchor="middle">'+pct+'%</text><text class="s" x="75" y="102" text-anchor="middle">'+esc(U.overall)+'</text></svg>';
    h+='<div><p class="band-name">'+esc(U.bands[b])+'</p><p>'+esc(U.bandtxt[b])+'</p></div></div>';
    h+='<h3>'+esc(U.by)+'</h3><ul class="doms">';
    Object.keys(Q.domains).forEach(function(k){var d=Q.domains[k],p=Math.round(dom[k].s/dom[k].m*100);h+='<li><a href="'+root+d.href+'">'+esc(d.name)+'</a><div class="dbar"><span style="width:'+p+'%;background:'+color(p)+'"></span></div><span class="dpct">'+p+'%</span></li>'});
    h+='</ul>';
    var idx=Q.questions.map(function(it,k){return k}).filter(function(k){return ans[k]<3}).sort(function(a,c){return ans[a]-ans[c]||a-c}).slice(0,3);
    if(idx.length){h+='<h3>'+esc(U.prio)+'</h3><ol class="prio">';idx.forEach(function(k){var it=Q.questions[k];h+='<li>'+esc(it.rec)+'<a href="'+root+Q.domains[it.d].href+'">'+esc(U.learn)+' →</a></li>'});h+='</ol>'}
    h+='<div class="qnav"><button class="btn ghost" type="button" id="qr">'+U.restart+'</button><a class="btn primary" href="'+root+'contact.html">'+U.cta+'</a></div>';
    el.innerHTML=h;el.scrollIntoView({behavior:"smooth",block:"start"});
    document.getElementById("qr").onclick=function(){ans=new Array(n);i=0;q()};
  }
  q();
})();
