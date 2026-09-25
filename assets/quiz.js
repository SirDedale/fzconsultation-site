(function(){
  var Q=window.QUIZ,root=window.QUIZ_ROOT||"",el=document.getElementById("quiz");if(!Q||!el)return;
  var U=Q.ui,n=Q.questions.length,ans=new Array(n),i=-1,industry=null,size=null;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function intro(){
    var h='<p class="qdom">'+esc(U.intro_title)+'</p>';
    h+='<label class="vorg">'+esc(U.org_industry)+'<select id="qind"><option value="">—</option>'+Q.industries.map(function(o,k){return '<option value="'+k+'"'+(industry===k?" selected":"")+'>'+esc(o)+'</option>'}).join('')+'</select></label>';
    h+='<label class="vorg">'+esc(U.org_size)+'<select id="qsize"><option value="">—</option>'+Q.sizes.map(function(o,k){return '<option value="'+k+'"'+(size===k?" selected":"")+'>'+esc(o)+'</option>'}).join('')+'</select></label>';
    h+='<p class="qhint">'+esc(U.org_optional)+'</p>';
    h+='<div class="qnav"><span></span><button class="btn primary" type="button" id="qs">'+esc(U.start)+'</button></div>';
    el.innerHTML=h;
    document.getElementById("qs").onclick=function(){
      var iv=document.getElementById("qind").value, sv=document.getElementById("qsize").value;
      industry=iv===""?null:+iv; size=sv===""?null:+sv; i=0; q();
    };
  }
  function q(){
    var it=Q.questions[i],d=Q.domains[it.d];
    var h='<div class="qprog"><span>'+U.q+" "+(i+1)+" "+U.of+" "+n+'</span></div><div class="qbar"><span style="width:'+Math.round(i/n*100)+'%"></span></div>';
    h+='<p class="qdom">'+esc(d.name)+'</p><h2 id="qt">'+esc(it.q)+'</h2><fieldset class="qopts" aria-labelledby="qt">';
    Q.options.forEach(function(o,k){h+='<label><input type="radio" name="a" value="'+k+'"'+(ans[i]===k?" checked":"")+'> '+esc(o)+'</label>'});
    h+='</fieldset><div class="qnav"><button class="btn ghost" type="button" id="qp">'+U.prev+'</button><button class="btn primary" type="button" id="qn"'+(ans[i]===undefined?" disabled":"")+'>'+(i===n-1?U.see:U.next)+'</button></div>';
    el.innerHTML=h;
    el.querySelectorAll("input").forEach(function(r){r.addEventListener("change",function(){ans[i]=+r.value;document.getElementById("qn").disabled=false})});
    document.getElementById("qp").onclick=function(){if(i>0){i--;q()}else{i=-1;intro()}};
    document.getElementById("qn").onclick=function(){if(ans[i]===undefined)return;if(i<n-1){i++;q();el.querySelector("input").focus()}else summary()};
  }
  function color(p){return p<40?"#b3261e":p<70?"var(--signal)":"#1d7a46"}
  function radarPoint(cx,cy,r,frac,angle){return [cx+r*frac*Math.cos(angle), cy+r*frac*Math.sin(angle)]}
  var RADAR_SHORT={"bc":["Continuité","Continuity"],"dr":["Reprise","Recovery"],"sec":["Sécurité","Security"],"tp":["Tiers & nuage","Third parties"]};
  function shortName(key,fallback){var s=RADAR_SHORT[key];return s?(document.documentElement.lang==="en"?s[1]:s[0]):fallback}
  function radar(pct,keys,names){
    var pad=98,R=90,vb=(R+pad)*2,cx=vb/2,cy=vb/2,N=keys.length,pts=[],labels=[];
    names=keys.map(function(k,idx){return shortName(k,names[idx])});
    for(var k=0;k<N;k++){
      var ang=-Math.PI/2 + k*2*Math.PI/N;
      var p=radarPoint(cx,cy,R,pct[keys[k]]/100,ang);
      pts.push(p.join(","));
      var lp=radarPoint(cx,cy,R+22,1,ang);
      var cosA=Math.cos(ang), sinA=Math.sin(ang), anchor="middle", ly=lp[1];
      if(Math.abs(cosA)>0.35){ anchor=cosA>0?"start":"end"; }
      else { ly = sinA>0 ? lp[1]+8 : lp[1]-6; }
      labels.push('<text x="'+lp[0]+'" y="'+ly+'" text-anchor="'+anchor+'" dominant-baseline="middle" class="rlabel">'+esc(names[k])+'</text>');
    }
    var rings=[0.25,0.5,0.75,1].map(function(f){
      var rp=[]; for(var k=0;k<N;k++){var ang=-Math.PI/2+k*2*Math.PI/N; rp.push(radarPoint(cx,cy,R,f,ang).join(","))}
      return '<polygon points="'+rp.join(" ")+'" class="rring"/>';
    }).join('');
    var axes=""; for(var k=0;k<N;k++){var ang=-Math.PI/2+k*2*Math.PI/N; var ep=radarPoint(cx,cy,R,1,ang); axes+='<line x1="'+cx+'" y1="'+cy+'" x2="'+ep[0]+'" y2="'+ep[1]+'" class="raxis"/>'}
    return '<svg class="radar" viewBox="0 0 '+vb+' '+vb+'" role="img" aria-label="'+esc(U.by)+'">'+rings+axes+
      '<polygon points="'+pts.join(" ")+'" class="rshape"/>'+labels.join('')+'</svg>';
  }
  function summary(){
    var byDom={}, wByDom={};
    Q.questions.forEach(function(it,k){byDom[it.d]=(byDom[it.d]||0)+ans[k]*it.w; wByDom[it.d]=(wByDom[it.d]||0)+3*it.w});
    var keys=Object.keys(Q.domains), pct={}, totalS=0, totalM=0;
    keys.forEach(function(k){pct[k]=Math.round(byDom[k]/wByDom[k]*100); totalS+=byDom[k]; totalM+=wByDom[k]});
    var overall=Math.round(totalS/totalM*100), b=overall<40?0:overall<70?1:2;
    var weakest=keys.slice().sort(function(a,c){return pct[a]-pct[c]})[0];
    var h='<div class="res-top"><svg class="gauge" viewBox="0 0 150 150" role="img" aria-label="'+U.overall+": "+overall+'%"><circle cx="75" cy="75" r="60" fill="none" stroke="var(--line)" stroke-width="14"/><circle cx="75" cy="75" r="60" fill="none" stroke="'+color(overall)+'" stroke-width="14" stroke-linecap="round" stroke-dasharray="'+(2*Math.PI*60)+'" stroke-dashoffset="'+(2*Math.PI*60*(1-overall/100))+'" transform="rotate(-90 75 75)"/><text class="t" x="75" y="82" text-anchor="middle">'+overall+'%</text><text class="s" x="75" y="102" text-anchor="middle">'+esc(U.overall)+'</text></svg>';
    h+='<div><p class="band-name">'+esc(U.bands[b])+'</p><p>'+esc(U.bandtxt[b])+'</p></div></div>';
    h+='<h3>'+esc(U.by)+'</h3><div class="radar-wrap">'+radar(pct,keys,keys.map(function(k){return Q.domains[k].name}))+'</div>';
    h+='<h3>'+esc(U.narrative_title)+'</h3><blockquote class="vquote">'+esc(Q.narrative[weakest])+'</blockquote>';
    if(industry!==null && size!==null){
      h+='<p class="ctxline">'+esc(U.context_lede)+' '+esc(Q.industries[industry].toLowerCase())+esc(U.context_mid)+' <a href="'+root+'resources/cost-of-downtime.html">'+esc(U.context_link)+' →</a></p>';
    }
    h+='<p class="note" style="margin:18px 0 0">'+esc(U.no_single)+'</p>';
    h+='<div class="qnav vact"><button class="btn ghost" type="button" id="qr">'+esc(U.restart)+'</button><span class="vbtns"><button class="btn ghost" type="button" id="qpr">'+esc(U.print)+'</button><a class="btn primary" href="'+root+'contact.html">'+esc(U.cta)+'</a></span></div>';
    el.innerHTML=h; el.scrollIntoView({behavior:"smooth",block:"start"});
    document.getElementById("qr").onclick=function(){ans=new Array(n);i=-1;intro()};
    document.getElementById("qpr").onclick=function(){window.print()};
  }
  intro();
})();
