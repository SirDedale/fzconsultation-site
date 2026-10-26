var wrap=document.querySelector(".search-wrap");
if(wrap){
  var UI={};try{UI=JSON.parse(document.getElementById("search-data").textContent)}catch(e){}
  var form=document.getElementById("search-form"),input=document.getElementById("q"),status=document.getElementById("search-status"),list=document.getElementById("search-results"),more=document.getElementById("search-more");
  var pf=null,hits=[],shown=0,seq=0,timer=null,PAGE=10;
  var load=function(){
    if(!pf){pf=import(wrap.getAttribute("data-pf")).then(function(m){return m.default&&m.default.search?m.default:m})}
    return pf;
  };
  var esc=function(s){var d=document.createElement("div");d.textContent=s;return d.innerHTML};
  var show=async function(){
    var end=Math.min(shown+PAGE,hits.length);
    var datas=await Promise.all(hits.slice(shown,end).map(function(h){return h.data()}));
    datas.forEach(function(d){
      var li=document.createElement("li");
      var t=(d.meta&&d.meta.title?d.meta.title:d.url).replace(/\s*\|\s*FZ Consultation\s*$/,"");
      li.innerHTML='<a class="r-title" href="'+d.url+'">'+esc(t)+'</a><p class="r-ex">'+d.excerpt+'</p><p class="r-url">'+esc(d.url.replace(/index\.html$/,""))+'</p>';
      list.appendChild(li);
    });
    shown=end;more.hidden=shown>=hits.length;
  };
  var run=async function(q){
    var my=++seq;q=q.trim();list.textContent="";more.hidden=true;hits=[];shown=0;
    if(q.length<2){status.textContent=q.length?UI.prompt:"";return}
    status.textContent=UI.loading;
    try{
      var p=await load();var r=await p.search(q);
      if(my!==seq)return;
      hits=r.results;
      if(!hits.length){status.textContent=UI.none.replace("{q}",q);return}
      status.textContent=hits.length===1?UI.count1:UI.countN.replace("{n}",hits.length);
      await show();
    }catch(e){status.textContent=UI.error}
  };
  form.addEventListener("submit",function(e){e.preventDefault();clearTimeout(timer);run(input.value);try{history.replaceState(null,"","?q="+encodeURIComponent(input.value))}catch(x){}});
  input.addEventListener("input",function(){clearTimeout(timer);timer=setTimeout(function(){run(input.value)},250)});
  more.addEventListener("click",show);
  var q0=new URLSearchParams(location.search).get("q");if(q0){input.value=q0;run(q0)}
}
